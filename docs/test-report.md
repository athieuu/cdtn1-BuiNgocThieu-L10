# Test Report – L10 Automatic Warranty Request Classification

## 1. Thông tin chạy kiểm thử
- Repo: `athieuu/cdtn1-BuiNgocThieu-L10`
- Branch: `fix/bt2-feedback-c4-c6-models`
- Môi trường: Windows PowerShell (Python 3.11 theo môi trường project)
- Unit test command: `python -m unittest discover -s tests -v`

## 2. Unit Test – C4

Kết quả chạy thực tế được cung cấp từ terminal:

| Kết quả | Số lượng |
|---|---:|
| Tổng số test | 19 |
| PASS | 19 |
| FAIL | 0 |
| Thời gian chạy | 0.094 giây |

**Kết luận: 19/19 unit test PASS.**

Bộ kiểm thử có các nhóm test:
- **Normal / đúng:** kiểm tra dataset có dữ liệu, đủ cột, mô tả không rỗng, nhãn hợp lệ, ID duy nhất; dự đoán mô tả hợp lệ.
- **Boundary / biên:** mô tả một ký tự, mô tả dài, Unicode/ký tự đặc biệt, khoảng trắng đầu/cuối.
- **Invalid / dữ liệu sai:** mô tả rỗng hoặc whitespace, input không phải chuỗi, nhãn dự đoán không hợp lệ, prediction rỗng, thiếu cột/nhãn, category sai, mô tả raw trống.

Các test được chạy bởi:
```powershell
python -m unittest discover -s tests -v
```

Minh chứng: lưu ảnh chụp terminal có danh sách test và dòng `Ran 19 tests ... OK` vào `docs/screenshot/` rồi commit lên repo.

## 3. Kết quả pipeline và thực nghiệm mô hình

### Data validation và split
- Raw dataset: 4,000 records; 3 columns.
- Missing values: 0; missing IDs: 0; empty descriptions: 0; invalid labels: 0; duplicate IDs: 0.
- Train: 2,778 records; Validation: 596 records; Test: 626 records.
- Exact duplicate descriptions giữa từng cặp split: 0.
- Pipeline chạy hoàn tất thành công.

### Validation model comparison (596 records)

| Model | Role | Accuracy | Macro-F1 | Weighted-F1 |
|---|---|---:|---:|---:|
| TF-IDF + Logistic Regression | Baseline | 0.9933 | 0.9884 | 0.9931 |
| TF-IDF + Multinomial Naive Bayes | Model 1 | 0.9866 | 0.9764 | 0.9859 |
| TF-IDF + Linear SVM | Model 2 | 1.0000 | 1.0000 | 1.0000 |

Linear SVM được chọn vì có Macro-F1 cao nhất trên Validation. Test không tham gia lựa chọn mô hình.

### Final Test evaluation (626 records)
- Accuracy: 1.0000
- Macro-F1: 1.0000
- Weighted-F1: 1.0000
- Support theo nhãn: KHAC 39; MAN_HINH 224; NUOC_VAO 61; PHAN_MEM 85; PIN 143; SAC 74.
- Confusion matrix: không có lỗi ngoài đường chéo theo kết quả terminal.
- Artifact: `reports/test_metrics.json`, `reports/test_confusion_matrix.png`.

## 4. Nhận xét
Unit test xác nhận các trường hợp normal, boundary và invalid đã liệt kê đều chạy PASS. Kết quả test set phản ánh dữ liệu hiện tại, không bảo đảm hiệu năng hoàn hảo trên các yêu cầu bảo hành mới. Mô tả tương tự/near-duplicate giữa các tập có thể khiến metric lạc quan; cần trình bày giới hạn này trong báo cáo.

