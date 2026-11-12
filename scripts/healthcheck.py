
from pathlib import Path
import sys

try:
    import pandas
    import sklearn
    import joblib
    import matplotlib

    dataset = Path("data/raw/issue_descriptions.csv")

    if not dataset.exists():
        raise FileNotFoundError("Raw dataset not found")

    import pandas as pd

    data = pd.read_csv(dataset)

    required = {"desc_id", "issue_desc", "issue_category"}

    if not required.issubset(data.columns):
        raise ValueError("Dataset is missing required columns")

    if len(data) == 0:
        raise ValueError("Dataset is empty")

    print("HEALTHCHECK PASSED")

except Exception as exc:
    print(f"HEALTHCHECK FAILED: {exc}", file=sys.stderr)
    sys.exit(1)
