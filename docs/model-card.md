# Model Card – L10 Automatic Warranty Request Classification

## 1. Model Details

| Item | Description |
|---|---|
| Model name | L10 Warranty Issue Classifier |
| Project | Automatic Warranty Request Classification |
| Model type | Supervised text classification |
| Selected algorithm | Linear Support Vector Machine (LinearSVC) |
| Feature extraction | TF-IDF |
| Framework | Python, scikit-learn |
| Main artifact | `models/tfidf_linear_svm.joblib` |
| Version | BT3 prototype |
| Supported language | Vietnamese warranty issue descriptions |

The model predicts one of six warranty issue categories from a text description.

## 2. Intended Use

**Primary intended use:**

- Assist warranty staff in categorizing customer-reported device issues.
- Provide an initial category suggestion for a warranty request.
- Support a prototype workflow for automatic warranty request classification.

**Out of scope:**

- Automatically approving or rejecting warranty claims.
- Determining warranty eligibility or repair costs.
- Diagnosing hardware defects with certainty.
- Replacing human inspection or technical evaluation.

Predictions should be reviewed by an authorized staff member before being used for operational decisions.

## 3. Training Data

| Item | Description |
|---|---|
| Dataset | `data/raw/issue_descriptions.csv` |
| Total records | 4,000 |
| Required columns | `desc_id`, `issue_desc`, `issue_category` |
| Input feature | `issue_desc` |
| Target label | `issue_category` |
| Missing values | 0 detected |
| Empty descriptions | 0 detected |
| Invalid labels | 0 detected |
| Duplicate descriptions | 2,652 duplicate-description occurrences/groups as reported by dataset validation |

Supported labels:

- `MAN_HINH`
- `PIN`
- `SAC`
- `PHAN_MEM`
- `NUOC_VAO`
- `KHAC`

The dataset is split by normalized description using a grouped splitting strategy to prevent exact normalized descriptions from appearing in different subsets.

## 4. Data Preprocessing

The pipeline performs the following operations:

1. Validates required dataset columns.
2. Checks missing IDs, empty descriptions, and unsupported category labels.
3. Normalizes descriptions for duplicate-aware splitting.
4. Splits data into training, validation, and test sets using random seed 42.
5. Extracts text features using TF-IDF.
6. Trains and evaluates classification models.

The split contains:

| Dataset | Records | Percentage |
|---|---:|---:|
| Training | 2,778 | 69.45% |
| Validation | 596 | 14.90% |
| Test | 626 | 15.65% |
| Total | 4,000 | 100% |

## 5. Model Architecture

The selected model uses a two-stage text classification pipeline:

- **TF-IDF:** Converts warranty descriptions into numerical text features.
- **LinearSVC:** Predicts the category from the TF-IDF feature representation.

LinearSVC was selected based on validation performance compared with Logistic Regression and Multinomial Naive Bayes.

## 6. Performance

### Validation results

| Model | Accuracy | Macro-F1 | Weighted-F1 |
|---|---:|---:|---:|
| TF-IDF + Logistic Regression | 0.9933 | 0.9884 | 0.9931 |
| TF-IDF + Multinomial Naive Bayes | 0.9866 | 0.9764 | 0.9859 |
| TF-IDF + LinearSVC | 1.0000 | 1.0000 | 1.0000 |

### Final test results

| Metric | Test result |
|---|---:|
| Test samples | 626 |
| Accuracy | 1.0000 |
| Macro-F1 | 1.0000 |
| Weighted-F1 | 1.0000 |

These results describe performance on the available dataset and split. They do not guarantee equivalent performance on new, independently collected real-world requests.

## 7. Limitations

- The model depends on the vocabulary and writing patterns represented in the training dataset.
- Informal language, spelling errors, abbreviations, and descriptions with insufficient context may reduce prediction reliability.
- New issue types outside the six supported labels cannot be classified into a new category without updating the dataset and retraining the model.
- The perfect test score should be interpreted cautiously because the dataset contains repeated descriptions and may contain similar wording patterns.
- Exact normalized duplicates are prevented across splits, but near-duplicate descriptions may still remain.
- No evidence currently establishes performance across different devices, regions, customer populations, or independently collected production data.


## 8. Bias and Group Performance Evaluation

Group performance was evaluated on the independent test set using two grouping methods: actual issue category and description length.

### 8.1. Grouping by Issue Category

| Issue Category | Samples | Accuracy | Precision | Recall | F1-score |
|---|---:|---:|---:|---:|---:|
| MAN_HINH | 224 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| PIN | 143 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| SAC | 74 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| PHAN_MEM | 85 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| NUOC_VAO | 61 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| KHAC | 39 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

### 8.2. Grouping by Description Length

| Description Length | Samples | Accuracy | Macro-F1 |
|---|---:|---:|---:|
| Short (1–30 characters) | 15 | 1.0000 | 1.0000 |
| Medium (31–100 characters) | 611 | 1.0000 | 1.0000 |
| Long (>100 characters) | 0 | N/A | N/A |

The long-description group could not be evaluated because no test samples belonged to this group.

### 8.3. Bias Analysis

The evaluated model achieved perfect classification metrics across all six issue categories and both description-length groups represented in the test set.

No performance disparity was observed in these evaluated groups.

However, these results do not establish that the model is free from bias. The short-description group contains only 15 samples, and the long-description group contains no samples. Therefore, conclusions about these groups are limited.

The evaluation only considers issue categories and description length. It does not assess demographic fairness or performance across user populations.

Further evaluation with larger, more diverse, and independently collected datasets is necessary before real-world deployment.

## 9. Risks and Mitigations

| Risk | Potential impact | Mitigation |
|---|---|---|
| Incorrect category prediction | Warranty requests may be routed to the wrong processing group | Require human review before final classification; monitor errors and collect corrected labels |
| Out-of-scope or ambiguous descriptions | The model may force an unsuitable category | Reject empty or invalid inputs; flag uncertain cases for manual review; consider a confidence or abstention mechanism in a future version |
| Dataset duplication or limited coverage | Evaluation may overestimate real-world performance | Collect independently sourced data, audit near-duplicates, and evaluate on a new holdout dataset |
| Unsupported issue types | New defect categories may be misclassified as one of the existing six labels | Maintain a manual escalation path and update the label set only through a controlled retraining process |

## 10. Ethical Considerations and Maintenance

- The model is a decision-support prototype, not an autonomous decision-maker.
- Human review is required before operational use.
- The current dataset does not support demographic fairness claims.
- New labeled data should be checked for quality, duplication, and label consistency.
- Model performance should be reevaluated after changes to the dataset, preprocessing, or model.
- The model artifact and evaluation reports should be versioned together.
- The model should not be deployed for high-impact warranty decisions without independent validation and operational monitoring.