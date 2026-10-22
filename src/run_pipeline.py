
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

STEPS = [
    ("1. Validate dữ liệu", "src/data/validate_data.py"),
    ("2. Chia train/validation/test", "src/data/split_data.py"),
    ("3. Kiểm tra các tập dữ liệu", "src/data/check_split.py"),
    ("4. Train Baseline", "src/models/train_baseline.py"),
    ("5. Train Linear SVM", "src/models/train_svm.py"),
    ("6. So sánh mô hình trên Validation", "src/models/compare_models.py"),
]


def run_step(name, script):
    print(f"\n{'=' * 60}\n{name}\n{'=' * 60}", flush=True)
    subprocess.run(
        [sys.executable, str(ROOT / script)],
        cwd=ROOT,
        check=True,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Chạy pipeline phân loại yêu cầu bảo hành."
    )
    parser.add_argument(
        "--evaluate-test",
        action="store_true",
        help="Chạy đánh giá cuối trên Test khi được yêu cầu chủ động.",
    )
    args = parser.parse_args()

    for name, script in STEPS:
        run_step(name, script)

    if args.evaluate_test:
        run_step(
            "7. Đánh giá cuối trên Test",
            "src/models/evaluate_test.py",
        )
    else:
        print(
            "\nBỏ qua đánh giá Test. "
            "Chỉ sử dụng Validation để so sánh mô hình."
        )

    print("\nPIPELINE COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()
