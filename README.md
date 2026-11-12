# Automatic Warranty Request Classification

**Student:** Bui Ngoc Thieu  
**Student ID:** 2374802010471  
**Track:** AI  
**Course:** Graduation Thesis 1, Semester 1, 2026–2027  
**Business Flow:** L10 – Automatic Warranty Request Classification

## 1. Objective

Build a machine learning system that classifies customer warranty issue descriptions into six categories:

- `MAN_HINH` – Screen issues
- `PIN` – Battery issues
- `SAC` – Charging issues
- `PHAN_MEM` – Software issues
- `NUOC_VAO` – Water damage
- `KHAC` – Other issues

The system aims to help warranty staff categorize customer requests more efficiently and consistently.

**Note:** Automatic priority-level prediction is not currently implemented.

## 2. Technology Stack

- Python 3.11
- pandas
- scikit-learn
- joblib
- matplotlib
- unittest

## 3. Dataset

The dataset is stored at `data/raw/issue_descriptions.csv`.

It contains 4,000 records and three columns:

| Column | Description |
|---|---|
| `desc_id` | Description identifier |
| `issue_desc` | Customer's warranty issue description |
| `issue_category` | Target issue category |

The dataset is split into training, validation, and test sets. Exact duplicate descriptions are grouped to prevent identical descriptions from appearing across different splits.

Similar descriptions may still occur across splits and can make evaluation metrics overly optimistic.

## 4. Environment Requirements

- Python 3.11
- Dependencies listed in `requirements.txt`
- Dataset available at `data/raw/issue_descriptions.csv`

## 5. Installation

Clone the repository:

```bash
git clone https://github.com/athieuu/cdtn1-BuiNgocThieu-L10.git
cd cdtn1-BuiNgocThieu-L10
```

Create and activate a virtual environment in Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Ensure the dataset exists at:

```text
data/raw/issue_descriptions.csv
```

The CSV file must contain `desc_id`, `issue_desc`, and `issue_category`.

## 6. Run the Pipeline

Run the pipeline from the repository root:

```powershell
python src/run_pipeline.py
```

The pipeline performs the following steps:

1. Validate the raw dataset.
2. Split the dataset into training, validation, and test sets.
3. Check the data splits for exact duplicate descriptions.
4. Train TF-IDF + Logistic Regression (baseline).
5. Train TF-IDF + Multinomial Naive Bayes.
6. Train TF-IDF + Linear SVM.
7. Compare the three models using validation metrics.

The pipeline does **not** evaluate the test set by default. The test set is used only after model selection is complete.

To perform the final evaluation of the selected model:

```powershell
python src/run_pipeline.py --evaluate-test
```

## 7. Models and Evaluation Results

### 7.1 Validation Model Comparison

The models were compared using the validation set (596 records). Logistic Regression is the baseline, while Multinomial Naive Bayes and Linear SVM are the two comparison models.

| Model | Role | Accuracy | Macro-F1 | Weighted-F1 |
|---|---|---:|---:|---:|
| TF-IDF + Logistic Regression | Baseline | 0.9933 | 0.9884 | 0.9931 |
| TF-IDF + Multinomial Naive Bayes | Model 1 | 0.9866 | 0.9764 | 0.9859 |
| TF-IDF + Linear SVM | Model 2 | 1.0000 | 1.0000 | 1.0000 |

Linear SVM was selected because it achieved the highest validation Macro-F1. The held-out test set was not used for model selection.

### 7.2 Final Test Evaluation

After selecting Linear SVM based on validation results, the model was evaluated once on the held-out test set containing 626 records.

| Metric | Test Score |
|---|---:|
| Accuracy | 1.0000 |
| Macro-F1 | 1.0000 |
| Weighted-F1 | 1.0000 |

All six categories achieved precision, recall, and F1-score of 1.0000 on this test run.

| Category | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| KHAC | 1.0000 | 1.0000 | 1.0000 | 39 |
| MAN_HINH | 1.0000 | 1.0000 | 1.0000 | 224 |
| NUOC_VAO | 1.0000 | 1.0000 | 1.0000 | 61 |
| PHAN_MEM | 1.0000 | 1.0000 | 1.0000 | 85 |
| PIN | 1.0000 | 1.0000 | 1.0000 | 143 |
| SAC | 1.0000 | 1.0000 | 1.0000 | 74 |

The confusion matrix is saved at `reports/test_confusion_matrix.png`. This run shows no off-diagonal errors.

### 7.3 Interpretation and Limitations

These metrics describe performance on the current dataset; they do not guarantee perfect classification of new customer requests. Exact duplicate descriptions were grouped before splitting, but semantically or lexically similar descriptions may remain across splits and make the evaluation optimistic. Further evaluation should use more diverse, independently collected warranty descriptions and additional near-duplicate analysis.

## 8. Testing

Run the unit tests from the repository root:

```powershell
python -m unittest discover -s tests -v
```

The test suite is designed to cover normal cases, boundary cases (single-character and long descriptions, Unicode/special characters, surrounding whitespace), and invalid cases (empty/whitespace descriptions, non-string input, invalid/empty model prediction, missing dataset columns, invalid or missing labels and empty descriptions in the raw dataset).

Test Plan and Test Report:
- `docs/test-plan.md`
- `docs/test-report.md`

Capture terminal screenshots of the actual unit-test run and store them under `docs/screenshot/`. The test report should only state the observed number of tests and pass/fail status after the suite has been run locally.

## 9. Project Structure

```text
cdtn1-BuiNgocThieu-L10/
├── data/
│   ├── raw/
│   └── processed/
├── docs/
├── models/
├── reports/
├── src/
│   ├── data/
│   ├── models/
│   ├── predict.py
│   └── run_pipeline.py
├── tests/
│   └── test_pipeline.py
├── .gitignore
├── requirements.txt
└── README.md
```

Generated model artifacts are excluded from Git through `.gitignore`.

## 10. Limitations and Future Work

- Investigate near-duplicate descriptions and their impact on evaluation.
- Expand evaluation and document confusion-matrix findings.
- Maintain reproducibility across repeated pipeline runs.
- Implement and evaluate automatic priority-level prediction if required by the final project scope.

## 11. Documentation

Project documentation and diagrams are available in the `docs/` directory, including the Software Requirements Specification, machine learning problem statement, AI usage disclosure, architecture diagram, and pipeline diagram.
