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

```bash
python src/run_pipeline.py
```

The pipeline performs the following steps:

1. Validate the raw dataset.
2. Split the dataset into training, validation, and test sets.
3. Check the data splits for exact duplicate descriptions.
4. Train a TF-IDF + Logistic Regression baseline.
5. Train a TF-IDF + Linear SVM model.
6. Compare models using validation metrics.

The pipeline does **not** evaluate the test set by default. The test set should be used only after model selection is complete.

## 7. Models and Validation Results

The models are compared using:

- Accuracy
- Macro-F1
- Weighted-F1
- Per-class precision, recall, and F1-score

Current validation results:

| Model | Accuracy | Macro-F1 | Weighted-F1 |
|---|---:|---:|---:|
| TF-IDF + Logistic Regression | 0.9933 | 0.9884 | 0.9931 |
| TF-IDF + Linear SVM | 1.0000 | 1.0000 | 1.0000 |

Linear SVM currently ranks first by validation Macro-F1. These results should be interpreted alongside the potential impact of near-duplicate descriptions.

## 8. Testing

Run unit tests from the repository root:

```bash
python -m unittest discover -s tests -v
```

The tests cover:

- Required dataset columns
- Dataset availability
- Non-empty descriptions
- Valid category labels
- Unique identifiers
- Valid prediction input
- Empty and whitespace-only descriptions
- Non-string prediction input

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
