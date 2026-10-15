
import json
from pathlib import Path

REPORT_DIR = Path("reports")


def main():
    files = {
        "TF-IDF + Logistic Regression":
            REPORT_DIR / "baseline_metrics.json",
        "TF-IDF + Linear SVM":
            REPORT_DIR / "svm_metrics.json",
    }

    results = []

    for model_name, path in files.items():
        if not path.exists():
            raise FileNotFoundError(
                f"Chưa tìm thấy {path}. "
                "Hãy chạy các script huấn luyện trước."
            )

        with open(path, encoding="utf-8") as f:
            metrics = json.load(f)

        results.append({
            "model": model_name,
            "accuracy": metrics["accuracy"],
            "macro_f1": metrics["macro_f1"],
            "weighted_f1": metrics["weighted_f1"],
        })

    results.sort(
        key=lambda result: result["macro_f1"],
        reverse=True,
    )

    print("=== VALIDATION MODEL COMPARISON ===")

    for index, result in enumerate(results, start=1):
        print(f"\n{index}. {result['model']}")
        print(f"   Accuracy:    {result['accuracy']:.4f}")
        print(f"   Macro-F1:    {result['macro_f1']:.4f}")
        print(f"   Weighted-F1: {result['weighted_f1']:.4f}")

    print(
        "\nMô hình đứng đầu theo Macro-F1: "
        f"{results[0]['model']}"
    )
    print("Chưa sử dụng tập Test.")


if __name__ == "__main__":
    main()
