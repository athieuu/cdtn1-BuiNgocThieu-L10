
from pathlib import Path
import json

import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)

MODEL_PATH = Path("models/tfidf_linear_svm.joblib")
TEST_PATH = Path("data/processed/test.csv")
REPORT_DIR = Path("reports")
RANDOM_SEED = 42


def main():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Không tìm thấy model: {MODEL_PATH}")
    if not TEST_PATH.exists():
        raise FileNotFoundError(f"Không tìm thấy Test set: {TEST_PATH}")

    test = pd.read_csv(TEST_PATH, encoding="utf-8")
    required = {"issue_desc", "issue_category"}

    if not required.issubset(test.columns):
        raise ValueError(f"Test set thiếu cột: {required - set(test.columns)}")
    if test["issue_desc"].isna().any() or test["issue_category"].isna().any():
        raise ValueError("Test set có mô tả hoặc nhãn bị thiếu")

    model = joblib.load(MODEL_PATH)

    # Đánh giá cuối cùng: không fit hoặc điều chỉnh model trên Test.
    y_true = test["issue_category"]
    y_pred = model.predict(test["issue_desc"])

    accuracy = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)
    weighted_f1 = f1_score(
        y_true, y_pred, average="weighted", zero_division=0
    )
    report = classification_report(
        y_true, y_pred, output_dict=True, zero_division=0
    )

    labels = sorted(set(y_true) | set(y_pred))
    matrix = confusion_matrix(y_true, y_pred, labels=labels)

    print("=== FINAL TEST EVALUATION: TF-IDF + LINEAR SVM ===")
    print(f"Test samples: {len(test)}")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Macro-F1: {macro_f1:.4f}")
    print(f"Weighted-F1: {weighted_f1:.4f}")
    print("\n=== PER-CLASS METRICS ===")
    print(classification_report(y_true, y_pred, zero_division=0))
    print("Confusion matrix (rows=true, columns=predicted):")
    print(pd.DataFrame(matrix, index=labels, columns=labels))

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    output = {
        "model": "TF-IDF + LinearSVC",
        "evaluation_split": "test",
        "test_rows": len(test),
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1,
        "per_class_metrics": report,
        "labels": labels,
        "confusion_matrix": matrix.tolist(),
        "random_seed": RANDOM_SEED,
    }

    with open(
        REPORT_DIR / "test_metrics.json", "w", encoding="utf-8"
    ) as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    display = ConfusionMatrixDisplay(
        confusion_matrix=matrix,
        display_labels=labels,
    )
    display.plot(xticks_rotation=45, values_format="d")
    plt.title("Linear SVM - Test Confusion Matrix")
    plt.tight_layout()
    plt.savefig(REPORT_DIR / "test_confusion_matrix.png", dpi=160)
    plt.close()

    print("\nĐã lưu: reports/test_metrics.json")
    print("Đã lưu: reports/test_confusion_matrix.png")


if __name__ == "__main__":
    main()
