import unittest
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "raw" / "issue_descriptions.csv"
REQUIRED_COLUMNS = {"desc_id", "issue_desc", "issue_category"}
VALID_LABELS = {
    "MAN_HINH", "PIN", "SAC",
    "PHAN_MEM", "NUOC_VAO", "KHAC"
}

class TestWarrantyData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = pd.read_csv(DATA)

    def test_required_columns_exist(self):
        self.assertTrue(REQUIRED_COLUMNS.issubset(self.df.columns))

    def test_dataset_not_empty(self):
        self.assertGreater(len(self.df), 0)

    def test_no_empty_descriptions(self):
        descriptions = self.df["issue_desc"].fillna("").astype(str).str.strip()
        self.assertTrue(descriptions.ne("").all())

    def test_labels_are_valid(self):
        self.assertTrue(set(self.df["issue_category"].dropna()).issubset(VALID_LABELS))

    def test_ids_are_unique_and_present(self):
        self.assertTrue(self.df["desc_id"].notna().all())
        self.assertTrue(self.df["desc_id"].is_unique)

if __name__ == "__main__":
    unittest.main(verbosity=2)
