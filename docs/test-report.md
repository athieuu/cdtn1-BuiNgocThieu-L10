# Test Report – L10 Automatic Warranty Request Classification

## 1. Thông tin chạy pipeline
- Repo: `athieuu/cdtn1-BuiNgocThieu-L10`
- Branch: `fix/bt2-feedback-c4-c6-models`
- Môi trường: Windows PowerShell, Python 3.11 (theo môi trường project)
- Pipeline: `python src/run_pipeline.py`
- Đánh giá Test: `python src/run_pipeline.py --evaluate-test`

## 2. Kết quả kiểm thử pipeline và thực nghiệm mô hình

### Data validation và split
- Raw dataset: 4,000 records; 3 columns.
- Missing values: 0; missing IDs: 0; empty descriptions: 0; invalid labels: 0; duplicate IDs: 0.
- Train: 2,778 records; Validation: 596 records; Test: 626 records.
- Exact duplicate descriptions across each pair of splits: 0.
- Pipeline completed successfully.

### Validation model comparison (596 records)

| Model | Role | Accuracy | Macro-F1 | Weighted-F1 |
|---|---|---:|---:|---:|
| TF-IDF + Logistic Regression | Baseline | 0.9933 | 0.9884 | 0.9931 |
| TF-IDF + Multinomial Naive Bayes | Model 1 | 0.9866 | 0.9764 | 0.9859 |
| TF-IDF + Linear SVM | Model 2 | 1.0000 | 1.0000 | 1.0000 |

Linear SVM was selected based on the highest validation Macro-F1.

### Final Test evaluation (626 records)
- Accuracy: 1.0000
- Macro-F1: 1.0000
- Weighted-F1: 1.0000
- Per-class support: KHAC 39; MAN_HINH 224; NUOC_VAO 61; PHAN_MEM 85; PIN 143; SAC 74.
- Confusion matrix: no off-diagonal errors reported.
- Artifacts: `reports/test_metrics.json`, `reports/test_confusion_matrix.png`.

## 3. Unit test status (C4)

**Pending actual unit-test run.** The local pipeline output supplied confirms data validation, split checks, three model training/comparison, and final Test evaluation, but it does not show the unittest suite run.

Run:
```powershell
python -m unittest discover -s tests -v
```

After execution, record the observed number of tests, PASS, FAIL, and attach terminal screenshots in `docs/screenshot/`. Do not label the unit-test suite PASS until the output confirms it.
