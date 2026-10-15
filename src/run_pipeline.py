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
    ("7. Đánh giá cuối trên Test", "src/models/evaluate_test.py"),
]

for name, script in STEPS:
    print(f"\n{'=' * 60}\n{name}\n{'=' * 60}", flush=True)
    subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT, check=True)

print("\nPIPELINE COMPLETED SUCCESSFULLY")
