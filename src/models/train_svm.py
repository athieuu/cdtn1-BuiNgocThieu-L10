
from pathlib import Path
import json

import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
)

DATA_DIR = Path("data/processed")
MODEL_DIR = Path("models")
REPORT_DIR = Path("reports")
RANDOM_SEED = 42


def main():
    train_path = DATA_DIR / "train.csv"
    val_path = DATA_DIR / "validation.csv"

    if not train_path.exists() or not val_path.exists():
        raise FileNotFoundError(
            "Thiếu train.csv hoặc validation.csv trong data/processed."
        )

    train = pd.read_csv(train_path, encoding="utf-8")
    val = pd.read_csv(val_path, encoding="utf-8")

    required = {"issue_desc", "issue_category"}

    for name, df in [("train", train), ("validation", val)]:
        if not required.issubset(df.columns):
            raise ValueError(f"{name} thiếu cột: {required - set(df.columns)}")

        if df["issue_desc"].isna().any() or df["issue_category"].isna().any():
            raise ValueError(f"{name} có mô tả hoặc nhãn bị thiếu.")

    model = Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            max_features=50000,
        )),
        ("classifier", LinearSVC(random_state=RANDOM_SEED)),
    ])

    # Fit chỉ trên Train; Validation chỉ dùng đánh giá.
    model.fit(train["issue_desc"], train["issue_category"])
    predictions = model.predict(val["issue_desc"])

    accuracy = accuracy_score(val["issue_category"], predictions)
    macro_f1 = f1_score(
        val["issue_category"], predictions,
        average="macro", zero_division=0
    )
    weighted_f1 = f1_score(
        val["issue_category"], predictions,
        average="weighted", zero_division=0
    )

    print("=== MODEL 2: TF-IDF + LINEAR SVM ===")
    print(f"Validation Accuracy: {accuracy:.4f}")
    print(f"Validation Macro-F1: {macro_f1:.4f}")
    print(f"Validation Weighted-F1: {weighted_f1:.4f}")

    print("\n=== PER-CLASS METRICS ===")
    print(classification_report(
        val["issue_category"],
        predictions,
        zero_division=0,
    ))

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, MODEL_DIR / "tfidf_linear_svm.joblib")

    metrics = {
        "model": "TF-IDF + LinearSVC",
        "evaluation_split": "validation",
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1,
        "train_rows": len(train),
        "validation_rows": len(val),
        "random_seed": RANDOM_SEED,
    }

    with open(REPORT_DIR / "svm_metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    print("\nĐã lưu model: models/tfidf_linear_svm.joblib")
    print("Đã lưu metrics: reports/svm_metrics.json")


if __name__ == "__main__":
    main()
