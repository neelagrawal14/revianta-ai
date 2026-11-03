import os
import httpx
from backend.services.live_research_service import search_live
from datetime import datetime
from typing import Any

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from psycopg.rows import dict_row
from psycopg.conninfo import conninfo_to_dict
from backend.auth import router as auth_router, get_current_user

load_dotenv()

app = FastAPI(title="Revianta AI API", version="1.0.0")
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analysis_results: dict[int, dict[str, Any]] = {}
pipeline = None


def database_config():
    url = os.getenv("DATABASE_URL", "").strip()
    if url:
        return url

    return {
        "host": os.getenv("PGHOST", "localhost"),
        "port": int(os.getenv("PGPORT", "5432")),
        "dbname": os.getenv("PGDATABASE", "revianta_ai"),
        "user": os.getenv("PGUSER", "postgres"),
        "password": os.getenv("PGPASSWORD", ""),
    }


def db_connection():
    config = database_config()

    if isinstance(config, dict):
        if not config.get("password"):
            raise HTTPException(
                status_code=503,
                detail="Database password is not configured.",
            )
        return psycopg.connect(**config, row_factory=dict_row)

    return psycopg.connect(config, row_factory=dict_row)


def get_pipeline():
    global pipeline
    if pipeline is None:
        from ai_engine.pipeline import ReviantaPipeline
        pipeline = ReviantaPipeline()
    return pipeline


def get_project_or_404(project_id: int, user_id: int):
    with db_connection() as conn:
        project = conn.execute(
            """
            SELECT id, name, title, description, status,
                   created_by, created_at, updated_at
            FROM projects
            WHERE id = %s AND owner_user_id = %s
            """,
            (project_id, user_id),
        ).fetchone()

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "Revianta AI API"}


@app.get("/api/projects")
def list_projects(
    limit: int = 100,
    offset: int = 0,
    current_user: dict = Depends(get_current_user),
):
    limit = max(1, min(limit, 500))
    offset = max(0, offset)
    user_id = int(current_user["id"])

    with db_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, name, title, description, status,
                   created_by, created_at, updated_at
            FROM projects
            WHERE owner_user_id = %s
            ORDER BY id DESC
            LIMIT %s OFFSET %s
            """,
            (user_id, limit, offset),
        ).fetchall()
        total = conn.execute(
            "SELECT COUNT(*) AS total FROM projects WHERE owner_user_id = %s",
            (user_id,),
        ).fetchone()["total"]

    return jsonable_encoder({"items": rows, "total": total})


@app.post("/api/projects", status_code=201)
def create_project(
    payload: dict[str, Any],
    current_user: dict = Depends(get_current_user),
):
    name = str(payload.get("name") or payload.get("projectName") or "").strip()
    title = str(payload.get("title") or name).strip()
    description = str(payload.get("description") or payload.get("idea") or "").strip()

    if not name or not title:
        raise HTTPException(status_code=422, detail="Project name and title are required.")

    user_id = int(current_user["id"])
    created_by = current_user["name"]
    with db_connection() as conn:
        project = conn.execute(
            """
            INSERT INTO projects (name, title, description, created_by, owner_user_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, name, title, description, status,
                      created_by, created_at, updated_at
            """,
            (name, title, description, created_by, user_id),
        ).fetchone()
    return jsonable_encoder(project)


@app.get("/api/projects/{project_id}")
def get_project(project_id: int, current_user: dict = Depends(get_current_user)):
    return jsonable_encoder(get_project_or_404(project_id, int(current_user["id"])))


@app.patch("/api/projects/{project_id}")
def update_project(
    project_id: int,
    payload: dict[str, Any],
    current_user: dict = Depends(get_current_user),
):
    user_id = int(current_user["id"])
    get_project_or_404(project_id, user_id)
    allowed = {"name", "title", "description", "status"}
    updates = {key: value for key, value in payload.items() if key in allowed}
    if not updates:
        raise HTTPException(status_code=422, detail="No editable fields supplied.")
    assignments = ", ".join(f"{key} = %s" for key in updates)
    values = list(updates.values()) + [project_id, user_id]
    with db_connection() as conn:
        project = conn.execute(
            f"""
            UPDATE projects
            SET {assignments}, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s AND owner_user_id = %s
            RETURNING id, name, title, description, status,
                      created_by, created_at, updated_at
            """,
            values,
        ).fetchone()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return jsonable_encoder(project)


@app.delete("/api/projects/{project_id}")
def delete_project(project_id: int, current_user: dict = Depends(get_current_user)):
    user_id = int(current_user["id"])
    get_project_or_404(project_id, user_id)
    with db_connection() as conn:
        conn.execute("DELETE FROM projects WHERE id = %s AND owner_user_id = %s", (project_id, user_id))
    analysis_results.pop(project_id, None)
    return {"deleted": True, "project_id": project_id}


@app.post("/api/projects/{project_id}/analyze")
def analyze_project(
    project_id: int,
    payload: dict[str, Any] | None = None,
    current_user: dict = Depends(get_current_user),
):
    project = get_project_or_404(project_id, int(current_user["id"]))
    payload = payload or {}

    text = str(
        payload.get("project_text")
        or payload.get("description")
        or project.get("description")
        or project.get("title")
        or ""
    ).strip()

    if not text:
        raise HTTPException(
            status_code=422,
            detail="Add a project description before running analysis.",
        )

    try:
        # Stage 1: existing Revianta AI analysis pipeline.
        result = get_pipeline().analyze_project(
            project_text=text,
            similar_texts=payload.get("similar_texts"),
            dataset_count=int(payload.get("dataset_count", 1)),
            research_dependency_count=int(
                payload.get("research_dependency_count", 2)
            ),
            deployment_required=bool(
                payload.get("deployment_required", False)
            ),
            hardware_required=bool(
                payload.get("hardware_required", False)
            ),
            real_time_required=bool(
                payload.get("real_time_required", False)
            ),
            data_quality=float(payload.get("data_quality", 0.6)),
            market_uncertainty=float(
                payload.get("market_uncertainty", 0.5)
            ),
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        print(f"Analysis failed for project {project_id}: {exc}")
        raise HTTPException(
            status_code=500,
            detail="Analysis failed. Check the backend terminal logs.",
        ) from exc

    # Stage 2: trained XGBoost prediction + SHAP explanation.
    # Do not substitute training averages for actual project values.
    numeric_fields = [
        "team_size",
        "planned_timeline_months",
        "technical_difficulty",
    ]
    missing_numeric = [
        field for field in numeric_fields
        if payload.get(field) is None
    ]

    if missing_numeric:
        result["stage2"] = {
            "status": "needs_input",
            "message": (
                "Stage 2 requires actual project values for "
                "team_size, planned_timeline_months, and "
                "technical_difficulty."
            ),
            "missing_fields": missing_numeric,
        }
    else:
        try:
            # stage2_predictor.py is located in the project root.
            from stage2_predictor import predict_project

            hardware_value = payload.get("hardware_required")
            if isinstance(hardware_value, bool):
                hardware_category = "yes" if hardware_value else "no"
            else:
                hardware_category = str(
                    hardware_value or "unknown"
                ).strip().lower()

            stage2_input = {
                "project_title": str(
                    payload.get("project_title")
                    or project.get("title")
                    or project.get("name")
                    or "Untitled project"
                ),
                "technologies_used": str(
                    payload.get("technologies_used")
                    or payload.get("technologies")
                    or text
                ),
                "dataset_availability": str(
                    payload.get("dataset_availability", "unknown")
                ).strip().lower(),
                "hardware_required": hardware_category,
                "similar_project_awareness": str(
                    payload.get("similar_project_awareness", "unknown")
                ).strip().lower(),
                "research_availability": str(
                    payload.get("research_availability", "unknown")
                ).strip().lower(),
                "team_size": payload["team_size"],
                "planned_timeline_months": payload[
                    "planned_timeline_months"
                ],
                "technical_difficulty": payload["technical_difficulty"],
            }

            stage2_prediction = predict_project(stage2_input, explain=True)
            result["stage2"] = {
                "status": "completed",
                **stage2_prediction,
            }
        except (ValueError, TypeError) as exc:
            result["stage2"] = {
                "status": "invalid_input",
                "message": str(exc),
            }
        except Exception as exc:
            print(f"Stage 2 failed for project {project_id}: {exc}")
            result["stage2"] = {
                "status": "unavailable",
                "message": (
                    "Stage 2 prediction failed. "
                    "Check backend terminal logs."
                ),
            }

    result["analysis_timestamp"] = datetime.now().isoformat()
    analysis_results[project_id] = result
    return jsonable_encoder(result)


@app.get("/api/projects/{project_id}/analysis/status")
def analysis_status(project_id: int, current_user: dict = Depends(get_current_user)):
    get_project_or_404(project_id, int(current_user["id"]))
    result = analysis_results.get(project_id)
    return {
        "status": "completed" if result else "not_run",
        "has_result": result is not None,
    }


@app.get("/api/projects/{project_id}/technology-map")
def technology_map(project_id: int, current_user: dict = Depends(get_current_user)):
    get_project_or_404(project_id, int(current_user["id"]))
    result = analysis_results.get(project_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Run analysis first")
    return {"technologies": result["project"]["technologies"]}


@app.get("/api/projects/{project_id}/knowledge-graph")
def knowledge_graph(project_id: int, current_user: dict = Depends(get_current_user)):
    get_project_or_404(project_id, int(current_user["id"]))
    result = analysis_results.get(project_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Run analysis first")
    return result["knowledge_graph"]


@app.get("/api/projects/{project_id}/timeline")
def project_timeline(project_id: int, current_user: dict = Depends(get_current_user)):
    get_project_or_404(project_id, int(current_user["id"]))
    result = analysis_results.get(project_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Run analysis first")
    return result["trend"]


@app.get("/api/projects/{project_id}/complexity")
def project_complexity(project_id: int, current_user: dict = Depends(get_current_user)):
    get_project_or_404(project_id, int(current_user["id"]))
    result = analysis_results.get(project_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Run analysis first")
    return result["complexity"]


@app.get("/api/projects/{project_id}/risk")

@app.get("/api/projects/{project_id}/risk")
def project_risk(
    project_id: int,
    current_user: dict = Depends(get_current_user),
):
    get_project_or_404(project_id, int(current_user["id"]))

    result = analysis_results.get(project_id)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Run analysis first",
        )

    nrie = result.get("nrie") or {}
    risk_scores = nrie.get("risk_scores") or {}
    explanations = nrie.get("explanations") or {}

    dimension_labels = {
        "technical": "Technical Risk",
        "dataset": "Dataset Risk",
        "implementation": "Implementation Risk",
        "novelty": "Novelty Risk",
        "research": "Research Risk",
        "deployment": "Deployment Risk",
        "business": "Business Risk",
    }

    dimensions = []

    for key, label in dimension_labels.items():
        if key not in risk_scores:
            continue

        score = float(risk_scores[key])
        explanation = explanations.get(key) or {}
        severity = str(
            explanation.get("level")
            or (
                "High" if score >= 60
                else "Medium" if score >= 35
                else "Low"
            )
        ).title()

        recommendation = explanation.get("recommendation")

        dimensions.append({
            "id": key,
            "label": label,
            "score": score,
            "severity": severity,
            "reason": str(
                explanation.get("reason")
                or "No detailed explanation is available."
            ),
            "factors": (
                [str(recommendation)]
                if recommendation else []
            ),
        })

    risk_score = float(nrie["overall_risk"])
    health_score = float(nrie["health_score"])
    recommendations = result.get("recommendations", [])

    return {
        "overallHealth": health_score,
        "overallRisk": risk_score,
        "riskLevel": (
            "high" if risk_score >= 65
            else "medium" if risk_score >= 35
            else "low"
        ),
        "modelVersion": nrie.get("engine"),
        "dimensions": dimensions,
        "aiRecommendation": (
            " ".join(str(item) for item in recommendations)
            if isinstance(recommendations, list)
            else str(recommendations or "")
        ),
        "stage2": result.get("stage2"),
        "note": (
            "Stage 1 risk metrics are rule-based. Stage 2 is a "
            "separate trained outcome classifier and provides "
            "decision support, not a guaranteed outcome."
        ),
    }

    get_project_or_404(project_id, int(current_user["id"]))
    result = analysis_results.get(project_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Run analysis first")

    nrie = result["nrie"]
    risk_score = float(nrie["overall_risk"])
    health_score = float(nrie["health_score"])

    return {
        "overallHealth": health_score,
        "overallRisk": risk_score,
        "riskLevel": (
            "high" if risk_score >= 65
            else "medium" if risk_score >= 35
            else "low"
        ),
        "modelVersion": None,
        "dimensions": nrie.get("risk_scores", []),
        "aiRecommendation": (
            " ".join(str(item) for item in result.get("recommendations", []))
            if isinstance(result.get("recommendations"), list)
            else str(result.get("recommendations", ""))
        ),
        "stage2": result.get("stage2"),
        "note": (
            "Stage 1 risk metrics are rule-based. Stage 2 is a separate "
            "trained outcome classifier and should be interpreted as "
            "decision support."
        ),
    }


@app.get("/api/projects/{project_id}/recommendations")
def project_recommendations(project_id: int, current_user: dict = Depends(get_current_user)):
    get_project_or_404(project_id, int(current_user["id"]))
    result = analysis_results.get(project_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Run analysis first")
    return result["recommendations"]


@app.get("/api/recommendations")
def recommendations(current_user: dict = Depends(get_current_user)):
    user_id = int(current_user["id"])
    with db_connection() as conn:
        rows = conn.execute(
            "SELECT id FROM projects WHERE owner_user_id = %s",
            (user_id,),
        ).fetchall()
    owned_ids = {int(row["id"]) for row in rows}
    return [
        {"project_id": project_id, "recommendations": result.get("recommendations", [])}
        for project_id, result in analysis_results.items()
        if project_id in owned_ids
    ]


@app.get("/api/research/search")
def search_research(q: str, limit: int = 10):
    q = q.strip()
    if not q:
        raise HTTPException(status_code=422, detail="Search query is required")

    limit = max(1, min(limit, 50))

    try:
        from backend.services.project_research_service import ProjectResearchService

        config = database_config()
        if isinstance(config, str):
            parsed = conninfo_to_dict(config)
            service = ProjectResearchService(
                host=parsed.get("host", "localhost"),
                port=int(parsed.get("port", 5432)),
                database=parsed.get("dbname", "revianta_ai"),
                user=parsed.get("user", "postgres"),
                password=parsed.get("password"),
            )
        else:
            service = ProjectResearchService(
                host=config["host"],
                port=config["port"],
                database=config["dbname"],
                user=config["user"],
                password=config["password"],
            )

        results = service.find_research(q, limit)
        return {"query": q, "results": results}
    except HTTPException:
        raise
    except Exception as exc:
        print(f"Research search failed: {exc}")
        raise HTTPException(
            status_code=500,
            detail="Research search failed. Check database configuration and backend logs.",
        ) from exc


@app.get("/api/live-search")
async def live_research_search(
    source: str,
    q: str,
    limit: int = 10,
):
    source = source.strip().lower()
    q = q.strip()

    if source not in {"papers", "github", "datasets", "patents"}:
        raise HTTPException(
            status_code=422,
            detail="Unsupported source.",
        )

    if not q:
        raise HTTPException(
            status_code=422,
            detail="Search query is required.",
        )

    try:
        results = await search_live(source, q, limit)
        return {
            "source": source,
            "query": q,
            "count": len(results),
            "results": results,
        }
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except httpx.HTTPStatusError as exc:
        print(
            f"Live search provider error ({source}): "
            f"HTTP {exc.response.status_code}"
        )
        raise HTTPException(
            status_code=502,
            detail=(
                f"The {source} provider returned HTTP "
                f"{exc.response.status_code}. Try again later."
            ),
        ) from exc
    except httpx.RequestError as exc:
        print(f"Live search connection failed ({source}): {exc}")
        raise HTTPException(
            status_code=502,
            detail=f"Could not connect to the {source} provider.",
        ) from exc
