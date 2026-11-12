# Test Report – L10 Automatic Warranty Request Classificationưq

## Thông tin chạy kiểm thử
- Repo: `athieuu/cdtn1-BuiNgocThieu-L10`
- Branch: `fix/bt2-feedback-c4-c6-models`
- Môi trường: Windows PowerShell (Python 3.11 theo môi trường project)
- Unit test command: `python -m unittest discover -s tests -v`

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
| Execution time | 0.194 seconds |
| Overall result | PASS |

### Execution Command

```powershell
python -m unittest discover -s tests -v
```

### Actual Terminal Output

```text
Ran 19 tests in 0.194s

OK
```

## 2. Representative Test Case Results

The following 12 cases represent the main functional, boundary, invalid-data, security, and reproducibility scenarios. The automated cases are covered by the 19-test unit suite. Manual checks are identified separately.

| ID | Preconditions | Test steps | Test data | Expected result | Priority | Actual result | Status |
|---|---|---|---|---|---|---|---|
| TC-01 | Raw dataset is available | Load dataset and check required columns | `issue_descriptions.csv` | All required columns exist | High | Required columns were present | PASS |
| TC-02 | Raw dataset is available | Check dataset size and description values | 4,000 records | Dataset is non-empty and descriptions are valid | High | Dataset validation passed | PASS |
| TC-03 | Prediction function and mock model are available | Predict a valid description | Valid warranty issue description | Return a supported category | High | Valid category returned | PASS |
| TC-04 | Prediction function and mock model are available | Predict a one-character description | `"A"` | Input is processed and a category is returned | Medium | Input validation and prediction passed | PASS |
| TC-05 | Prediction function and mock model are available | Predict a long description | Description repeated 1,000 times | Input is processed without an unexpected exception | Medium | Long input was processed | PASS |
| TC-06 | Prediction function and mock model are available | Predict a Unicode description | Vietnamese text and special characters | No encoding error; return a category | Medium | Unicode input was processed | PASS |
| TC-07 | Prediction function is available | Submit an empty description | `""` | Raise `ValueError` | High | `ValueError` was raised | PASS |
| TC-08 | Prediction function is available | Submit a non-string input | `123` | Raise `TypeError` | High | `TypeError` was raised | PASS |
| TC-09 | Prediction function and mock model are available | Return an unsupported prediction label | `UNKNOWN` | Raise `ValueError` | High | Invalid prediction was rejected | PASS |
| TC-10 | Temporary raw dataset can be created | Load a dataset containing an unsupported category | `UNKNOWN` | Raise `ValueError` | High | Invalid category was rejected | PASS |
| TC-11 | Repository root is available | Check `.env` ignore and tracking status | `.env` | `.env` is ignored and is not tracked | High | `.env` was absent, ignored by Git, and not tracked | PASS |
| TC-12 | Docker and project files are available | Execute the pipeline twice and compare generated outputs | Same raw dataset and random seed 42 | Dataset sizes and outputs remain consistent; no duplicate records are appended | Medium | Repeated execution produced consistent outputs according to the recorded verification | PASS |

**Execution note:** TC-01 to TC-10 are automated test scenarios represented by the unit test suite. TC-11 and TC-12 are manual verification scenarios and are not included in the count of 19 automated unit tests.

## 3. Dataset Validation Results

| Validation item | Result |
|---|---:|
| Raw dataset records | 4,000 |
| Missing required columns | 0 |
| Missing IDs | 0 |
| Empty descriptions | 0 |
| Invalid category labels | 0 |
| Duplicate IDs | 0 |
| Exact duplicate descriptions across splits | 0 |

### Dataset Split Results

| Dataset | Records | Percentage |
|---|---:|---:|
| Train | 2,778 | 69.45% |
| Validation | 596 | 14.90% |
| Test | 626 | 15.65% |
| **Total** | **4,000** | **100%** |

The split process uses `GroupShuffleSplit` with random seed 42 to prevent exact normalized-description overlap across datasets.

## 4. Model Evaluation Results

### Validation Results

| Model | Accuracy | Macro-F1 | Weighted-F1 |
|---|---:|---:|---:|
| TF-IDF + Logistic Regression | 0.9933 | 0.9884 | 0.9931 |
| TF-IDF + Multinomial Naive Bayes | 0.9866 | 0.9764 | 0.9859 |
| TF-IDF + Linear SVM | 1.0000 | 1.0000 | 1.0000 |

### Final Test Results

Selected model: **TF-IDF + Linear SVM**

| Metric | Result |
|---|---:|
| Test samples | 626 |
| Accuracy | 1.0000 |
| Macro-F1 | 1.0000 |
| Weighted-F1 | 1.0000 |

The test confusion matrix showed no misclassified samples in the evaluated test set.

**Limitation:** These results describe performance on the current dataset split. Similar or near-duplicate descriptions may make the evaluation optimistic. The results do not guarantee equivalent performance on new real-world warranty requests.

## 5. Pipeline and Docker Verification

Previously executed integration checks:

| Verification | Expected result | Recorded result |
|---|---|---|
| `docker compose up -d --build` | Docker image builds and runtime starts | Completed successfully |
| `docker compose ps` | Runtime service reports healthy | Healthy |
| `docker compose --profile pipeline run --rm pipeline` | Pipeline completes successfully | `PIPELINE COMPLETED SUCCESSFULLY` |
| Docker unit test execution | All 19 tests pass | `Ran 19 tests ... OK` |

## 6. Test Evidence

Evidence to retain in the project:

- Terminal screenshot showing all 19 unit tests and the final `OK` summary.
- Docker runtime status showing `healthy`.
- Pipeline execution output showing `PIPELINE COMPLETED SUCCESSFULLY`.
- Model evaluation metrics and confusion matrix in the `reports/` directory.

The automated test execution on 2026-11-12 completed with 19 passed tests and zero failures.

## 7. Overall Conclusion

The automated unit test suite passed all 19 tests. Dataset validation, prediction input validation, prediction output validation, and data splitting checks behaved as expected in the tested scenarios.

The project pipeline and Docker runtime were also successfully executed in the recorded integration checks.

The system is considered to have passed the current BT3 test scope. Further evaluation with independent real-world warranty requests is recommended before production use.