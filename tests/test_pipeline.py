import unittest
import tempfile
import pandas as pd

from pathlib import Path
from unittest.mock import Mock, patch

from src.predict import predict_issue
from src.data import check_split
from src.data import split_data


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "raw" / "issue_descriptions.csv"

REQUIRED_COLUMNS = {"desc_id", "issue_desc", "issue_category"}

VALID_LABELS = {
    "MAN_HINH",
    "PIN",
    "SAC",
    "PHAN_MEM",
    "NUOC_VAO",
    "KHAC",
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
        descriptions = (
            self.df["issue_desc"].fillna("").astype(str).str.strip()
        )
        self.assertTrue(descriptions.ne("").all())

    def test_labels_are_valid(self):
        labels = set(self.df["issue_category"].dropna())
        self.assertTrue(labels.issubset(VALID_LABELS))

    def test_ids_are_unique_and_present(self):
        self.assertTrue(self.df["desc_id"].notna().all())
        self.assertTrue(self.df["desc_id"].is_unique)


class TestPredictIssue(unittest.TestCase):

    def setUp(self):
        self.model = Mock()
        self.model.predict.return_value = ["PIN"]

    def test_predict_valid_description(self):
        description = "Pin điện thoại nhanh hết pin"
        result = predict_issue(self.model, description)
        self.assertEqual(result, "PIN")
        self.model.predict.assert_called_once_with([description])

    def test_predict_single_character_boundary(self):
        description = "x"
        result = predict_issue(self.model, description)
        self.assertEqual(result, "PIN")
        self.model.predict.assert_called_once_with([description])

    def test_predict_special_unicode_characters(self):
        description = "Lỗi pin 🔋 — máy nóng!!!"
        result = predict_issue(self.model, description)
        self.assertEqual(result, "PIN")
        self.model.predict.assert_called_once_with([description])

    def test_trim_description_before_prediction(self):
        description = "  pin hao nhanh  "
        result = predict_issue(self.model, description)
        self.assertEqual(result, "PIN")
        self.model.predict.assert_called_once_with(["pin hao nhanh"])

    def test_reject_invalid_prediction_label(self):
        self.model.predict.return_value = ["UNKNOWN"]
        with self.assertRaisesRegex(ValueError, "invalid label"):
            predict_issue(self.model, "Pin điện thoại nhanh hết pin")

    def test_reject_empty_description(self):
        with self.assertRaises(ValueError):
            predict_issue(self.model, "")
        self.model.predict.assert_not_called()

    def test_reject_whitespace_description(self):
        with self.assertRaises(ValueError):
            predict_issue(self.model, "   ")
        self.model.predict.assert_not_called()

    def test_reject_non_string_description(self):
        with self.assertRaises(TypeError):
            predict_issue(self.model, None)
        self.model.predict.assert_not_called()

    def test_reject_empty_prediction(self):
        self.model.predict.return_value = []
        with self.assertRaisesRegex(ValueError, "empty prediction"):
            predict_issue(self.model, "Pin điện thoại nhanh hết pin")

    def test_predict_long_description_boundary(self):
        description = "Pin điện thoại nhanh hết pin " * 1000
        result = predict_issue(self.model, description)
        self.assertEqual(result, "PIN")
        self.model.predict.assert_called_once_with([description.strip()])


class TestCheckSplit(unittest.TestCase):

    def test_missing_required_column(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            for filename in check_split.FILES:
                if filename == "train.csv":
                    df = pd.DataFrame({"issue_category": ["PIN"]})
                else:
                    df = pd.DataFrame({
                        "issue_desc": ["pin hao"],
                        "issue_category": ["PIN"],
                    })
                df.to_csv(data_dir / filename, index=False)

            with patch("src.data.check_split.DATA_DIR", data_dir):
                with self.assertRaisesRegex(ValueError, "train.csv.*issue_desc"):
                    check_split.main()

    def test_reject_invalid_category_label(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            labels = sorted(VALID_LABELS)
            df = pd.DataFrame({
                "desc_id": range(1, 61),
                "issue_desc": [
                    f"Mô tả lỗi điện thoại số {i}" for i in range(1, 61)
                ],
                "issue_category": [labels[i % len(labels)] for i in range(60)],
            })
            df.loc[0, "issue_category"] = "UNKNOWN"

            input_path = temp_path / "issue_descriptions.csv"
            output_dir = temp_path / "processed"
            df.to_csv(input_path, index=False)

            with patch("src.data.split_data.DATA_PATH", input_path), patch(
                "src.data.split_data.OUTPUT_DIR", output_dir
            ):
                with self.assertRaisesRegex(ValueError, "UNKNOWN"):
                    split_data.main()

    def test_reject_empty_description_in_raw_dataset(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            df = pd.DataFrame({
                "desc_id": range(1, 61),
                "issue_desc": [f"Mô tả lỗi {i}" for i in range(1, 61)],
                "issue_category": ["PIN"] * 60,
            })
            df.loc[0, "issue_desc"] = "   "
            input_path = temp_path / "issue_descriptions.csv"

            df.to_csv(input_path, index=False)
            with patch("src.data.split_data.DATA_PATH", input_path):
                with self.assertRaisesRegex(ValueError, "mô tả rỗng"):
                    split_data.main()

    def test_reject_missing_category_in_raw_dataset(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            df = pd.DataFrame({
                "desc_id": range(1, 61),
                "issue_desc": [f"Mô tả lỗi {i}" for i in range(1, 61)],
                "issue_category": ["PIN"] * 60,
            })
            df.loc[0, "issue_category"] = None
            input_path = temp_path / "issue_descriptions.csv"

            df.to_csv(input_path, index=False)
            with patch("src.data.split_data.DATA_PATH", input_path):
                with self.assertRaisesRegex(ValueError, "nhãn bị thiếu"):
                    split_data.main()


if __name__ == "__main__":
    unittest.main(verbosity=2)
