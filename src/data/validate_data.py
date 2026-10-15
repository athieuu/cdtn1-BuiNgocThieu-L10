
from pathlib import Path
import pandas as pd

# Đường dẫn tính từ thư mục gốc của project
DATA_PATH = Path("data/raw/issue_descriptions.csv")

REQUIRED_COLUMNS = {
    "desc_id",
    "issue_desc",
    "issue_category",
}

VALID_CATEGORIES = {
    "MAN_HINH",
    "PIN",
    "SAC",
    "PHAN_MEM",
    "NUOC_VAO",
    "KHAC",
}


def validate_data(data: pd.DataFrame) -> dict:
    """Kiểm tra chất lượng dữ liệu và trả về các chỉ số đo được."""
    missing_columns = REQUIRED_COLUMNS - set(data.columns)

    if missing_columns:
        raise ValueError(
            f"Thiếu cột bắt buộc: {sorted(missing_columns)}"
        )

    description = data["issue_desc"].fillna("").astype(str).str.strip()
    labels = data["issue_category"].fillna("").astype(str).str.strip()

    invalid_description = description.eq("")
    missing_id = data["desc_id"].isna()
    invalid_label = ~labels.isin(VALID_CATEGORIES)
    duplicate_id = data["desc_id"].duplicated(keep=False)
    duplicate_description = description.ne("") & description.duplicated(
        keep=False
    )

    # Phát hiện cùng mô tả nhưng mang nhiều nhãn khác nhau
    label_counts = pd.DataFrame({
        "description": description,
        "label": labels,
    })
    label_counts = label_counts[label_counts["description"].ne("")]
    inconsistent_groups = (
        label_counts.groupby("description")["label"]
        .nunique()
        .gt(1)
    )
    inconsistent_descriptions = int(inconsistent_groups.sum())

    report = {
        "total_rows": len(data),
        "total_columns": len(data.columns),
        "missing_values_total": int(data.isna().sum().sum()),
        "missing_ids": int(missing_id.sum()),
        "empty_descriptions": int(invalid_description.sum()),
        "invalid_labels": int(invalid_label.sum()),
        "duplicate_ids": int(duplicate_id.sum()),
        "rows_with_duplicate_descriptions": int(
            duplicate_description.sum()
        ),
        "descriptions_with_conflicting_labels": inconsistent_descriptions,
        "number_of_categories": int(labels[~invalid_label].nunique()),
        "category_distribution": labels.value_counts().to_dict(),
    }

    return report


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Không tìm thấy dataset: {DATA_PATH.resolve()}\n"
            "Hãy chạy lệnh từ thư mục gốc của project."
        )

    data = pd.read_csv(DATA_PATH, encoding="utf-8")
    report = validate_data(data)

    print("=== DATA VALIDATION REPORT ===")
    for key, value in report.items():
        print(f"{key}: {value}")

    has_errors = any(
        report[key] > 0
        for key in (
            "missing_ids",
            "empty_descriptions",
            "invalid_labels",
        )
    )

    if has_errors:
        raise SystemExit(
            "\nVALIDATION FAILED: Phát hiện dữ liệu không hợp lệ."
        )

    print("\nVALIDATION PASSED: Không phát hiện lỗi dữ liệu bắt buộc.")


if __name__ == "__main__":
    main()
