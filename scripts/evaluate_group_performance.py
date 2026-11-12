
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_recall_fscore_support,
)

ROOT = Path(__file__).resolve().parents[1]
TEST_FILE = ROOT / "data" / "processed" / "test.csv"
MODEL_FILE = ROOT / "models" / "tfidf_linear_svm.joblib"

LABELS = [
    "MAN_HINH",
    "PIN",
    "SAC",
    "PHAN_MEM",
    "NUOC_VAO",
    "KHAC",
]


def calculate_metrics(y_true, y_pred):
    """Calculate accuracy and macro-F1 for one group."""

    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred have different lengths.")

    if len(y_true) == 0:
        return {
            "samples": 0,
            "accuracy": None,
            "precision": None,
            "recall": None,
            "f1": None,
        }

    present_labels = sorted(set(y_true))

    accuracy = accuracy_score(y_true, y_pred)

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true,
        y_pred,
        labels=present_labels,
        average="macro",
        zero_division=0,
    )

    # Accuracy = 1.0 means every prediction is correct.
    # Therefore, Macro-F1 must also equal 1.0.
    if accuracy == 1.0 and f1 != 1.0:
        raise ValueError(
            "Metric inconsistency detected: "
            f"accuracy={accuracy}, macro_f1={f1}. "
            "Please inspect the prediction data."
        )

    return {
        "samples": len(y_true),
        "accuracy": round(float(accuracy), 4),
        "precision": round(float(precision), 4),
        "recall": round(float(recall), 4),
        "f1": round(float(f1), 4),
    }


def main():
    # 1. Check input files
    if not TEST_FILE.exists():
        raise FileNotFoundError(
            f"Test dataset not found: {TEST_FILE}"
        )

    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_FILE}"
        )

    # 2. Load test data
    data = pd.read_csv(TEST_FILE)

    required = {"issue_desc", "issue_category"}
    missing = required - set(data.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    if data.empty:
        raise ValueError("Test dataset is empty.")

    if data["issue_desc"].isna().any():
        raise ValueError("Test dataset contains missing descriptions.")

    if data["issue_category"].isna().any():
        raise ValueError("Test dataset contains missing category labels.")

    # 3. Prepare data
    descriptions = data["issue_desc"].astype(str).to_numpy()
    y_true = data["issue_category"].astype(str).to_numpy()

    invalid_labels = sorted(set(y_true) - set(LABELS))

    if invalid_labels:
        raise ValueError(
            f"Invalid category labels: {invalid_labels}"
        )

    # 4. Load model and predict
    model = joblib.load(MODEL_FILE)
    y_pred = np.asarray(model.predict(descriptions))

    if len(y_pred) != len(y_true):
        raise ValueError(
            "Prediction count does not match test data."
        )

    y_pred = y_pred.astype(str)

    invalid_predictions = sorted(set(y_pred) - set(LABELS))

    if invalid_predictions:
        raise ValueError(
            f"Model returned invalid labels: {invalid_predictions}"
        )

    results = []

    # 5. Grouping method 1: actual issue category
    for label in LABELS:
        mask = y_true == label

        if not np.any(mask):
            continue

        metrics = calculate_metrics(
            y_true[mask],
            y_pred[mask],
        )

        results.append({
            "grouping": "issue_category",
            "group": label,
            **metrics,
        })

    # 6. Grouping method 2: description length
    lengths = np.array([
        len(description) for description in descriptions
    ])

    length_groups = {
        "Short (1-30)": (lengths >= 1) & (lengths <= 30),
        "Medium (31-100)": (lengths >= 31) & (lengths <= 100),
        "Long (>100)": lengths > 100,
    }

    for group_name, mask in length_groups.items():
        metrics = calculate_metrics(
            y_true[mask],
            y_pred[mask],
        )

        results.append({
            "grouping": "description_length",
            "group": group_name,
            **metrics,
        })

    # 7. Save group performance report
    output = pd.DataFrame(results)

    output_dir = ROOT / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "group_performance.csv"
    output.to_csv(output_file, index=False)

    # 8. Display results
    print("\n=== GROUP PERFORMANCE EVALUATION ===")
    print(output.to_string(index=False))

    print("\n=== PREDICTION SUMMARY ===")
    correct = int(np.sum(y_true == y_pred))
    total = len(y_true)

    print(f"Total samples: {total}")
    print(f"Correct predictions: {correct}")
    print(f"Incorrect predictions: {total - correct}")
    print(f"Overall accuracy: {accuracy_score(y_true, y_pred):.4f}")

    print(f"\nSaved group metrics to: {output_file}")


if __name__ == "__main__":
    main()
