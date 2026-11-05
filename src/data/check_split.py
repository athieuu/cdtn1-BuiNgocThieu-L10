from pathlib import Path
import pandas as pd


DATA_DIR = Path("data/processed")
FILES = ["train.csv", "validation.csv", "test.csv"]

REQUIRED_COLUMNS = {"issue_desc", "issue_category"}


def main():
    datasets = {}

    for filename in FILES:
        path = DATA_DIR / filename

        if not path.exists():
            raise FileNotFoundError(
                f"Không tìm thấy file: {path}"
            )

        df = pd.read_csv(path, encoding="utf-8")

        # Validate required columns
        missing_columns = REQUIRED_COLUMNS - set(df.columns)

        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(
                f"{filename} thiếu cột bắt buộc: {missing}"
            )

        datasets[filename] = df

        print(f"\n=== {filename} ===")
        print(f"Số dòng: {len(df)}")
        print("Phân bố nhãn:")
        print(
            df["issue_category"]
            .value_counts()
            .to_string()
        )

    description_sets = {
        name: set(
            df["issue_desc"]
            .astype(str)
            .str.strip()
            .str.lower()
        )
        for name, df in datasets.items()
    }

    pairs = [
        ("train.csv", "validation.csv"),
        ("train.csv", "test.csv"),
        ("validation.csv", "test.csv"),
    ]

    print("\n=== DUPLICATE LEAKAGE CHECK ===")

    for first, second in pairs:
        overlap = (
            description_sets[first]
            & description_sets[second]
        )

        print(
            f"{first} vs {second}: "
            f"{len(overlap)} mô tả trùng"
        )

        if overlap:
            raise ValueError(
                f"Phát hiện dữ liệu trùng giữa "
                f"{first} và {second}"
            )

    print(
        "\nPASS: Ba tập dữ liệu không có mô tả trùng nhau."
    )


if __name__ == "__main__":
    main()