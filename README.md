# Automatic Warranty Request Classification

**Student:** Bui Ngoc Thieu – 2374802010471 – Track AI  
**Course:** Graduation Thesis 1, Semester 1, 2026–2027  
**Business Flow:** L10 – Automatic Warranty Request Classification

## 1. Objective

Build an AI-based warranty request classification system that automatically classifies customer issue descriptions into six categories:

- `MAN_HINH` – Screen issues
- `PIN` – Battery issues
- `SAC` – Charging issues
- `PHAN_MEM` – Software issues
- `NUOC_VAO` – Water damage
- `KHAC` – Other issues

The system aims to support warranty staff in categorizing customer requests more efficiently and consistently.

**Note:** Automatic priority-level determination is not currently implemented.

## 2. Environment Requirements

- Python 3.11
- Dependencies listed in `requirements.txt`
- Environment variables: see `.env.example`

## 3. Getting Started

### 3.1. Clone the repository

```bash
git clone https://github.com/athieuu/cdtn1-BuiNgocThieu-L10.git
cd cdtn1-BuiNgocThieu-L10
```

### 3.2. Create a virtual environment

**Windows PowerShell:**

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3.3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3.4. Prepare the dataset

Place the source dataset at:

```text
data/raw/issue_descriptions.csv
```

The CSV file must contain the following columns:

- `desc_id`
- `issue_desc`
- `issue_category`

### 3.5. Run the pipeline

```bash
python src/run_pipeline.py
```

The pipeline validates the dataset, checks data quality, splits the data, trains and compares classification models, selects a model using validation metrics, and evaluates the selected model on the test set.

## 4. Project Structure

```text
.
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   ├── srs.md
│   ├── ml_problem_statement.md
│   ├── ai-disclosure.md
│   ├── MLPipeline.drawio
│   └── So_do_kien_truc.drawio
├── reports/
├── src/
│   ├── data/
│   │   ├── validate_data.py
│   │   ├── check_near_duplicates.py
│   │   ├── check_split.py
│   │   └── split_data.py
│   ├── models/
│   │   ├── train_baseline.py
│   │   ├── train_svm.py
│   │   ├── compare_models.py
│   │   └── evaluate_test.py
│   └── run_pipeline.py
├── tests/
│   └── test_pipeline.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 5. Testing

Run the automated tests with:

```bash
python -m unittest discover -s tests -v
```

The tests check dataset validation and related pipeline requirements.

The pipeline and tests should be run from the repository root with the required dataset and dependencies available.

## 6. Current Status

- [x] Project initialized and repository structure created
- [x] Dataset validation and data quality checks implemented
- [x] Dataset splitting implemented to reduce exact-description overlap between splits
- [x] Baseline Logistic Regression model implemented
- [x] Linear SVM model implemented
- [x] Model selection based on validation metrics implemented
- [x] Test-set evaluation and confusion matrix generated
- [x] Automated dataset validation tests implemented
- [ ] Warranty request handling module
- [ ] Automatic priority-level classification

## 7. Model Evaluation

The current experiments compare Logistic Regression as the baseline with Linear Support Vector Classification (LinearSVC).

Model selection is based on validation metrics. The selected model is then evaluated on the held-out test set.

See the generated files in `reports/` for the recorded metrics and confusion matrix.

**Data limitation:** Similar or repeated issue descriptions may occur in the dataset. This can make evaluation metrics overly optimistic, even when exact duplicates are separated across splits. Results should therefore be interpreted with this limitation in mind.

## 8. Documentation

- `docs/srs.md` – Software Requirements Specification
- `docs/ml_problem_statement.md` – Machine learning problem statement
- `docs/ai-disclosure.md` – AI usage disclosure
- `docs/MLPipeline.drawio` – Machine learning pipeline diagram
- `docs/So_do_kien_truc.drawio` – System architecture diagram
