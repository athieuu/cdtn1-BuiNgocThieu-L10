# Bug Log – L10 Automatic Warranty Request Classification

## 1. Overview

This document records the actual defects identified and fixed during the development and testing of the L10 classification system.

| Bug ID | Severity | Component | Status |
|---|---|---|---|
| BUG-03 | Major | `src/predict.py` | Fixed |
| BUG-04 | Minor | `src/data/check_split.py` | Fixed |
| BUG-05 | Minor | `src/data/split_data.py` | Fixed |

Three defects were identified and fixed. BUG-03 is classified as Major because accepting unsupported prediction labels can cause invalid classification results to be returned to downstream components.

## 2. Fixed Bugs

### BUG-03 – Model Returns an Invalid Classification Label

- **Severity:** Major
- **Detected by test case:** TC-09 – Invalid model prediction label.
- **Component:** `src/predict.py`
- **Symptom:** `predict_issue()` accepted a prediction label outside the six supported categories.
- **Reproduction steps:**
  1. Create a mock model.
  2. Set `model.predict.return_value = ["UNKNOWN"]`.
  3. Call `predict_issue()` with a valid description.
  4. Observe that the invalid label was not rejected before the fix.
- **Root cause:** The prediction function did not validate the model's output against the supported category list.
- **Fix:** Added `VALID_LABELS` and validation of the predicted label before returning the result.
- **Verification:** Before the fix, the test failed because `ValueError` was not raised. After the fix, `test_reject_invalid_prediction_label` passed. The complete 19-test suite also passed in the latest execution.
- **Commit:** [cdcf688 – Validate prediction output labels](https://github.com/athieuu/cdtn1-BuiNgocThieu-L10/commit/cdcf688)
- **Status:** Fixed – PASS.

### BUG-04 – Missing Required Column Causes an Unclear KeyError

- **Severity:** Minor
- **Detected by test case:** TC-16 – Missing required column in split dataset validation.
- **Component:** `src/data/check_split.py`
- **Symptom:** The checker accessed `issue_desc` before validating the dataset schema. A missing column caused an unclear `KeyError`.
- **Reproduction steps:**
  1. Create a temporary `train.csv` containing only the `issue_category` column.
  2. Run `check_split.main()`.
  3. Observe the `KeyError` before the fix.
- **Root cause:** Required-column validation was missing before data processing.
- **Fix:** Added schema validation for the required `issue_desc` and `issue_category` columns. Missing columns now produce a clear `ValueError`.
- **Verification:** Before the fix, the test failed with `KeyError: 'issue_desc'`. After the fix, `test_missing_required_column` passed. The latest complete suite passed all 19 tests.
- **Commit:** [59f7ff3 – Validate required columns in split checker](https://github.com/athieuu/cdtn1-BuiNgocThieu-L10/commit/59f7ff3)
- **Status:** Fixed – PASS.

### BUG-05 – Dataset Accepts an Unsupported Category Label

- **Severity:** Minor
- **Detected by test case:** TC-17 – Invalid category label in raw dataset.
- **Component:** `src/data/split_data.py`
- **Symptom:** The data splitting process accepted an `issue_category` value outside the six supported categories.
- **Reproduction steps:**
  1. Create a temporary raw dataset with the required columns.
  2. Replace one valid category with `UNKNOWN`.
  3. Run the data splitting process.
  4. Observe that the invalid label was not rejected before the fix.
- **Root cause:** The splitting process did not validate category labels before creating the train, validation, and test datasets.
- **Fix:** Added `VALID_LABELS` containing `MAN_HINH`, `PIN`, `SAC`, `PHAN_MEM`, `NUOC_VAO`, and `KHAC`. The program now raises `ValueError` when unsupported labels are found.
- **Verification:** Before the fix, `test_reject_invalid_category_label` failed because `ValueError` was not raised. After the fix, the test passed. The latest complete suite passed all 19 tests.
- **Commit:** [7437d72 – Validate category labels before data splitting](https://github.com/athieuu/cdtn1-BuiNgocThieu-L10/commit/7437d72)
- **Status:** Fixed – PASS.

## 3. Verification Notes

The following checks were performed during development. They are verification activities, not additional software defects.

### VN-01 – Prediction Input Validation

- **Component:** `src/predict.py`
- **Verification:** Tested valid descriptions, empty descriptions, whitespace-only descriptions, and non-string inputs.
- **Result:** The corresponding prediction unit tests passed.

### VN-02 – Pipeline Reproducibility

- **Component:** `src/run_pipeline.py`
- **Verification:** Executed the pipeline twice and compared dataset sizes, label distributions, and validation metrics.
- **Result:** Both executions completed with `PIPELINE COMPLETED SUCCESSFULLY`, and the recorded outputs were consistent.
- **Limitation:** This verification covers the tested environment and configuration only; it does not guarantee identical results in every environment.

## 4. Summary

- Total actual defects recorded: 3.
- Fixed defects: 3.
- Major defects: 1.
- Minor defects: 2.
- Latest automated unit test execution: 19 passed, 0 failed.

All three recorded defects have corresponding fix commits and post-fix test evidence.