from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
import shap
import xgboost as xgb
from scipy.sparse import hstack, csr_matrix
ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "stage2"
MODEL_PATH = DATA / "models" / "nrie_stage2_xgboost.json"
ARTIFACT_PATH = DATA / "features" / "feature_transformers.joblib"
FEATURE_NAMES_PATH = DATA / "features" / "feature_names.csv"
CLASS_NAMES = {
    0: "Fully",
    1: "Partially",
    2: "Abandoned",
}
def load_artifacts():
    for path in (MODEL_PATH, ARTIFACT_PATH, FEATURE_NAMES_PATH):
        if not path.is_file():
            raise FileNotFoundError(f"Required artifact not found: {path}")
    artifacts = joblib.load(ARTIFACT_PATH)
    model = xgb.XGBClassifier()
    model.load_model(str(MODEL_PATH))
    feature_names = pd.read_csv(FEATURE_NAMES_PATH)["feature_name"].tolist()
    if len(feature_names) != model.n_features_in_:
        raise ValueError(
            f"Feature mismatch: names={len(feature_names)}, "
            f"model expects={model.n_features_in_}"
        )
    return model, artifacts, feature_names
def prepare_project(project, artifacts):
    required = [
        "project_title",
        "technologies_used",
        "dataset_availability",
        "hardware_required",
        "similar_project_awareness",
        "research_availability",
        "team_size",
        "planned_timeline_months",
        "technical_difficulty",
    ]
    missing = [key for key in required if key not in project]
    if missing:
        raise ValueError("Missing project fields: " + ", ".join(missing))
    row = pd.DataFrame([project])
    # Apply the same text cleaning used during training.
    for column in artifacts["text_columns"]:
        row[column] = row[column].fillna("").astype(str).str.strip()
    # Normalize categorical fields. Unseen values map to "unknown"
    # when that category exists in the fitted encoder.
    for column, allowed in zip(
        artifacts["categorical_columns"],
        artifacts["encoder"].categories_,
    ):
        value = row.at[0, column]
        value = "unknown" if pd.isna(value) else str(value).strip()
        allowed_strings = [str(item) for item in allowed]
        if value not in allowed_strings:
            if "unknown" in allowed_strings:
                value = "unknown"
            else:
                raise ValueError(
                    f"Unsupported value for {column}: {value}"
                )
        row.at[0, column] = value
    # Validate and transform numeric fields.
    for column in artifacts["numeric_columns"]:
        value = pd.to_numeric(row.at[0, column], errors="coerce")
        if pd.isna(value) or not np.isfinite(float(value)):
            raise ValueError(f"{column} must be a valid finite number")
        row.at[0, column] = float(value)
    if row.at[0, "team_size"] < 1:
        raise ValueError("team_size must be at least 1")
    if row.at[0, "planned_timeline_months"] <= 0:
        raise ValueError("planned_timeline_months must be positive")
    if not 1 <= row.at[0, "technical_difficulty"] <= 5:
        raise ValueError("technical_difficulty must be between 1 and 5")
    # Match training's combined text: title + space + technologies.
    combined_text = (
        row["project_title"].astype(str)
        + " "
        + row["technologies_used"].astype(str)
    )
    X_text = artifacts["tfidf"].transform(combined_text)
    X_cat = artifacts["encoder"].transform(
        row[artifacts["categorical_columns"]]
    )
    X_num = csr_matrix(
        artifacts["scaler"].transform(
            row[artifacts["numeric_columns"]]
        )
    )
    X = hstack([X_text, X_cat, X_num], format="csr")
    if X.shape[1] != 1020:
        raise ValueError(
            f"Expected 1020 features, generated {X.shape[1]}"
        )
    return X
def predict_project(project, explain=True, top_n=10):
    model, artifacts, feature_names = load_artifacts()
    X = prepare_project(project, artifacts)
    probabilities = model.predict_proba(X)[0]
    predicted_class = int(model.predict(X)[0])
    result = {
        "model": "nrie_stage2_xgboost",
        "prediction_type": "new_project_inference",
        "predicted_class_id": predicted_class,
        "predicted_outcome": CLASS_NAMES[predicted_class],
        "probabilities": {
            CLASS_NAMES[int(class_id)]: float(probability)
            for class_id, probability in zip(
                model.classes_, probabilities
            )
        },
        "shap_explanation": None,
        "note": (
            "Model prediction is decision support, not a guarantee "
            "of the project's eventual outcome."
        ),
    }
    if explain:
        explanation = shap.TreeExplainer(model).shap_values(X)
        values = np.asarray(explanation)
        # Current multiclass SHAP format: samples x features x classes.
        if values.ndim == 3:
            contributions = values[0, :, predicted_class]
        elif values.ndim == 2:
            contributions = values[0]
        else:
            raise ValueError(
                f"Unexpected SHAP output shape: {values.shape}"
            )
        indices = np.argsort(np.abs(contributions))[-top_n:][::-1]
        result["shap_explanation"] = {
            "explained_class": CLASS_NAMES[predicted_class],
            "method": "SHAP TreeExplainer",
            "interpretation": (
                "Positive values push the model output toward the "
                "explained class; negative values push it away. "
                "They are not probabilities or causal effects."
            ),
            "top_features": [
                {
                    "feature": feature_names[int(i)],
                    "contribution": float(contributions[i]),
                    "direction": (
                        "toward" if contributions[i] > 0
                        else "away" if contributions[i] < 0
                        else "neutral"
                    ),
                }
                for i in indices
            ],
        }
    return result
if __name__ == "__main__":
    sample_project = {
        "project_title": "AI Based Pothole Detection System",
        "technologies_used": "Python, YOLO, OpenCV, FastAPI",
        "dataset_availability": "available",
        "hardware_required": "no",
        "similar_project_awareness": "many_exist",
        "research_availability": "plenty",
        "team_size": 4,
        "planned_timeline_months": 4,
        "technical_difficulty": 3,
    }
    output = predict_project(sample_project, explain=True)
    print(json.dumps(output, indent=2))
    output_path = DATA / "models" / "sample_new_project_prediction.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"\nSaved prediction to: {output_path}")
