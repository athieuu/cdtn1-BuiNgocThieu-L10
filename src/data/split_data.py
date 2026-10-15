
from pathlib import Path

import pandas as pd
from sklearn.model_selection import GroupShuffleSplit

DATA_PATH = Path("data/raw/issue_descriptions.csv")
OUTPUT_DIR = Path("data/processed")
RANDOM_SEED = 42


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Không tìm thấy: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH, encoding="utf-8")

    required = {"desc_id", "issue_desc", "issue_category"}
    if not required.issubset(df.columns):
        raise ValueError(f"Dataset cần có các cột: {sorted(required)}")

    if df["issue_desc"].isna().any() or df["issue_category"].isna().any():
        raise ValueError("Dataset có mô tả hoặc nhãn bị thiếu.")

    # Chuẩn hóa để các mô tả giống nhau không bị chia sang nhiều tập
    groups = (
        df["issue_desc"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    if groups.eq("").any():
        raise ValueError("Dataset có mô tả rỗng.")

    # Bước 1: tách 15% test theo nhóm mô tả
    split_test = GroupShuffleSplit(
        n_splits=1,
        test_size=0.15,
        random_state=RANDOM_SEED,
    )
    train_val_idx, test_idx = next(
        split_test.split(df, groups=groups)
    )

    train_val = df.iloc[train_val_idx].copy()
    test = df.iloc[test_idx].copy()

    # Bước 2: lấy khoảng 15% tổng dữ liệu làm validation
    # 15 / 85 = 0.17647
    train_val_groups = groups.iloc[train_val_idx]

    split_val = GroupShuffleSplit(
        n_splits=1,
        test_size=15 / 85,
        random_state=RANDOM_SEED,
    )
    train_idx, val_idx = next(
        split_val.split(train_val, groups=train_val_groups)
    )

    train = train_val.iloc[train_idx].copy()
    val = train_val.iloc[val_idx].copy()

    # Xác nhận không có mô tả trùng giữa các tập
    train_groups = set(
        train["issue_desc"].astype(str).str.strip().str.lower()
    )
    val_groups = set(
        val["issue_desc"].astype(str).str.strip().str.lower()
    )
    test_groups = set(
        test["issue_desc"].astype(str).str.strip().str.lower()
    )

    assert train_groups.isdisjoint(val_groups)
    assert train_groups.isdisjoint(test_groups)
    assert val_groups.isdisjoint(test_groups)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    train.to_csv(OUTPUT_DIR / "train.csv", index=False)
    val.to_csv(OUTPUT_DIR / "validation.csv", index=False)
    test.to_csv(OUTPUT_DIR / "test.csv", index=False)

    print("=== DATA SPLIT REPORT ===")
    for name, part in [
        ("Train", train),
        ("Validation", val),
        ("Test", test),
    ]:
        print(f"{name}: {len(part)} rows ({len(part) / len(df):.1%})")
        print(part["issue_category"].value_counts().to_dict())

    print("\nPASS: Không có mô tả trùng giữa các tập.")
    print(f"Đã lưu dữ liệu vào: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
