# Test Plan – L10 Automatic Warranty Request Classification

# Test Report – L10 Automatic Warranty Request Classification

## 1. Test Execution Summary

| Item | Result |
|---|---|
| Project | L10 – Automatic Warranty Request Classification |
| Test date | 2026-11-12 |
| Test environment | Windows, Python 3.11 |
| Test framework | Python unittest |
| Total automated unit tests | 19 |
| Passed | 19 |
| Failed | 0 |
| Execution time | 0.085 seconds |
| Overall result | PASS |

### Execution Command

```powershell
python -m unittest discover -s tests -v
```

### 1.1 Objective

Verify the correctness of raw dataset validation, data splitting, prediction input validation, and model prediction output validation. The test plan covers normal, boundary, and invalid-data scenarios.

### 1.2 In Scope

- Validate the raw warranty issue dataset.
- Verify required columns, missing values, descriptions, IDs, and category labels.
- Verify train/validation/test data splitting.
- Check duplicate-description leakage across datasets.
- Test `predict_issue()` with valid, boundary, and invalid inputs.
- Verify model prediction output labels.
- Verify validation errors for invalid raw datasets and missing columns.

### 1.3 Out of Scope

- Public production deployment.
- Integration with an external warranty management system.
- Security penetration testing.
- Automatic warranty priority prediction.
- Performance guarantees on unseen real-world data.

### 1.4 Test Files

- `tests/test_pipeline.py`
- `src/predict.py`
- `src/data/split_data.py`
- `src/data/check_split.py`

## 2. Test Types and Test Cases

The automated test suite contains 19 test cases divided into three categories.

| ID | Category | Test case | Expected result |
|---|---|---|---|
| TC-01 | Normal | Dataset contains all required columns | Test passes |
| TC-02 | Normal | Dataset is not empty | Number of rows is greater than zero |
| TC-03 | Normal | All descriptions are non-empty | Every normalized description is non-empty |
| TC-04 | Normal | All labels belong to the six supported categories | No unsupported labels are found |
| TC-05 | Normal | IDs are present and unique | No missing or duplicate IDs |
| TC-06 | Normal | Predict a valid issue description | A supported category is returned |
| TC-07 | Boundary | Predict a one-character description | Input is processed and a label is returned |
| TC-08 | Boundary | Predict a long description (string repeated 1,000 times) | Input is processed and a label is returned |
| TC-09 | Boundary | Predict a description containing Unicode and special characters | No encoding error occurs and a label is returned |
| TC-10 | Boundary | Predict a description with leading and trailing whitespace | Input is trimmed before prediction |
| TC-11 | Invalid | Empty description | Raises `ValueError` |
| TC-12 | Invalid | Description containing only whitespace | Raises `ValueError` |
| TC-13 | Invalid | Input is not a string | Raises `TypeError` |
| TC-14 | Invalid | Model returns an `UNKNOWN` label | Raises `ValueError` |
| TC-15 | Invalid | Model returns an empty prediction | Raises `ValueError` |
| TC-16 | Invalid | Split dataset is missing a required column | Raises `ValueError` with a clear message |
| TC-17 | Invalid | Raw dataset contains an `UNKNOWN` category label | Raises `ValueError` |
| TC-18 | Invalid | Raw dataset contains an empty description | Raises `ValueError` |
| TC-19 | Invalid | Raw dataset contains a missing category value | Raises `ValueError` |

### Test Distribution

| Category | Number of test cases |
|---|---:|
| Normal | 6 |
| Boundary | 4 |
| Invalid | 9 |
| **Total** | **19** |

## 3. Success Criteria

The automated test suite is considered successful when:

- All 19 automated test cases pass.
- No automated test case fails or raises an unexpected exception.
- The raw dataset contains all required columns.
- The raw dataset has no empty descriptions or unsupported category labels.
- All prediction outputs belong to the six supported categories: `MAN_HINH`, `PIN`, `SAC`, `PHAN_MEM`, `NUOC_VAO`, and `KHAC`.
- No exact normalized-description overlap exists between the train, validation, and test datasets.
- Invalid inputs are rejected with the expected exception types.

Additional pipeline verification criteria:

- The pipeline finishes with `PIPELINE COMPLETED SUCCESSFULLY`.
- The Docker runtime service reaches the `healthy` state.
- Repeated pipeline execution produces the expected dataset sizes and does not append duplicate records.

Docker and repeated-execution checks are additional integration and reproducibility checks; they are not included in the count of 19 unit tests.

## 4. Test Environment and Test Data

### 4.1 Test Environment

| Item | Configuration |
|---|---|
| Operating system | Windows 10/11 |
| Programming language | Python 3.11 |
| Container runtime | Docker Desktop |
| Container orchestration | Docker Compose |
| Main libraries | pandas, scikit-learn, joblib, matplotlib |
| Test framework | Python `unittest` |
| Dependency management | `requirements.txt` |
| Random seed | 42 |

### 4.2 Test Data

The raw dataset is stored at `data/raw/issue_descriptions.csv`.

| Attribute | Value |
|---|---|
| Number of records | 4,000 |
| Required columns | `desc_id`, `issue_desc`, `issue_category` |
| Number of supported categories | 6 |
| Dataset splitting | Train / Validation / Test |
| Splitting strategy | GroupShuffleSplit |
| Random seed | 42 |

Supported categories:

- `MAN_HINH`
- `PIN`
- `SAC`
- `PHAN_MEM`
- `NUOC_VAO`
- `KHAC`

Invalid-data tests use temporary CSV files containing deliberately missing columns, missing values, empty descriptions, or unsupported labels. Prediction tests use mocked model outputs to verify input and output validation.

## 5. Test Execution and Evidence

Run the following commands from the repository root directory.

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Execute the automated test suite:

```powershell
python -m unittest discover -s tests -v
```

Expected summary:

```text
Ran 19 tests

OK
```

Capture a terminal screenshot showing the test names and final execution summary. Update the Test Report only after the corresponding tests have actually been executed.

Additional pipeline and Docker verification commands:

```powershell
python src/run_pipeline.py
docker compose up -d --build
docker compose ps
docker compose --profile pipeline run --rm pipeline
```

Record the actual command output and execution date as evidence in the Test Report.