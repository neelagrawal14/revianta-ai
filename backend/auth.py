
import os
import re
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
import psycopg
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, Field, field_validator
from pwdlib import PasswordHash
from psycopg.rows import dict_row

load_dotenv()

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
password_hash = PasswordHash.recommended()
bearer_scheme = HTTPBearer(auto_error=False)

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = 30


def get_jwt_secret() -> str:
    secret = os.getenv("JWT_SECRET_KEY", "").strip()
    if len(secret) < 32:
        raise HTTPException(
            status_code=503,
            detail="Authentication secret is not configured correctly.",
        )
    return secret


def get_db_connection():
    database_url = os.getenv("DATABASE_URL", "").strip()

    if not database_url:
        raise HTTPException(
            status_code=503,
            detail="DATABASE_URL is not configured.",
        )

    return psycopg.connect(database_url, row_factory=dict_row)


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty.")
        return value

    @field_validator("email")
    @classmethod
    def clean_email(cls, value: str) -> str:
        value = value.strip().lower()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
            raise ValueError("Enter a valid email address.")
        return value


class LoginRequest(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=1, max_length=128)

    @field_validator("email")
    @classmethod
    def clean_email(cls, value: str) -> str:
        return value.strip().lower()


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    created_at: datetime


def create_access_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(minutes=ACCESS_TOKEN_MINUTES),
    }
    return jwt.encode(payload, get_jwt_secret(), algorithm=JWT_ALGORITHM)


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please log in to continue.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(
            credentials.credentials,
            get_jwt_secret(),
            algorithms=[JWT_ALGORITHM],
        )
        user_id = int(payload["sub"])
    except (jwt.InvalidTokenError, ValueError, KeyError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session is invalid or expired. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    with get_db_connection() as conn:
        user = conn.execute(
            """
            SELECT id, name, email, created_at
            FROM users
            WHERE id = %s
            """,
            (user_id,),
        ).fetchone()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account no longer exists.",
        )

    return user


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest):
    with get_db_connection() as conn:
        existing = conn.execute(
            "SELECT id FROM users WHERE email = %s",
            (payload.email,),
        ).fetchone()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists.",
            )

        hashed_password = password_hash.hash(payload.password)

        try:
            user = conn.execute(
                """
                INSERT INTO users (name, email, password_hash)
                VALUES (%s, %s, %s)
                RETURNING id, name, email, created_at
                """,
                (payload.name, payload.email, hashed_password),
            ).fetchone()
        except psycopg.errors.UniqueViolation:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists.",
            )

    return {
        "user": user,
        "access_token": create_access_token(user["id"]),
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_MINUTES * 60,
    }


@router.post("/login")
def login(payload: LoginRequest):
    with get_db_connection() as conn:
        user = conn.execute(
            """
            SELECT id, name, email, password_hash, created_at
            FROM users
            WHERE email = %s
            """,
            (payload.email,),
        ).fetchone()

    if user is None or not password_hash.verify(
        payload.password, user["password_hash"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    public_user = {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "created_at": user["created_at"],
    }

    return {
        "user": public_user,
        "access_token": create_access_token(user["id"]),
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_MINUTES * 60,
    }


@router.get("/me")
def me(current_user=Depends(get_current_user)):
    return {"user": current_user}


@router.post("/logout")
def logout(current_user=Depends(get_current_user)):
    # JWTs are stateless. The client must discard its access token.
    return {"message": "Logged out. Discard the access token on the client."}
