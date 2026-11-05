import json
from pathlib import Path
import numpy as np
import pandas as pd
import shap
import xgboost as xgb
from scipy.sparse import load_npz
ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "stage2"
MODEL_PATH = DATA / "models" / "nrie_stage2_xgboost.json"
FEATURE_PATH = DATA / "features" / "X_test.npz"
NAMES_PATH = DATA / "features" / "feature_names.csv"
OUTPUT_PATH = DATA / "models" / "sample_shap_explanation.json"
CLASS_NAMES = {0: "Fully", 1: "Partially", 2: "Abandoned"}
X = load_npz(FEATURE_PATH)
feature_names = pd.read_csv(NAMES_PATH)["feature_name"].tolist()
model = xgb.XGBClassifier()
model.load_model(str(MODEL_PATH))
row = X[0:1]
probabilities = model.predict_proba(row)[0]
predicted_class = int(np.argmax(probabilities))
shap_values = np.asarray(shap.TreeExplainer(model).shap_values(row))
contributions = shap_values[0, :, predicted_class]
top_indices = np.argsort(np.abs(contributions))[-10:][::-1]
result = {
    "model": "nrie_stage2_xgboost",
    "sample_index": 0,
    "predicted_class_id": predicted_class,
    "predicted_outcome": CLASS_NAMES[predicted_class],
    "probabilities": {
        CLASS_NAMES[i]: float(probabilities[i])
        for i in range(len(probabilities))
    },
    "shap_explanation": {
        "explained_class": CLASS_NAMES[predicted_class],
        "method": "SHAP TreeExplainer",
        "top_features": [
            {
                "feature": feature_names[i],
                "contribution": float(contributions[i]),
                "direction": "toward"
                if contributions[i] > 0
                else "away" if contributions[i] < 0
                else "neutral",
            }
            for i in top_indices
        ],
    },
    "note": "Explanation for saved test sample 0; not a new user project prediction.",
}
OUTPUT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
print("Saved:", OUTPUT_PATH)
print("Predicted outcome:", result["predicted_outcome"])
print("Top SHAP features:", len(result["shap_explanation"]["top_features"]))
