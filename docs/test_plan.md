# TEST PLAN
## L10 – Automatic Warranty Request Classification

### 1. Thông tin chung

| Nội dung | Chi tiết |
|---|---|
| Project | L10 – Automatic Warranty Request Classification |
| Student | Bui Ngoc Thieu |
| Student ID | 2374802010471 |
| Track | AI |
| Assignment | Graduation Thesis 1 – BT3 |
| Testing Type | Unit Testing, Data Validation, Pipeline Testing, Model Evaluation |
| Programming Language | Python 3.11.5 |
| Testing Framework | unittest |

### 2. Mục tiêu kiểm thử

- Kiểm tra tính hợp lệ và chất lượng dữ liệu đầu vào.
- Kiểm tra chức năng dự đoán loại yêu cầu bảo hành.
- Kiểm tra khả năng xử lý dữ liệu không hợp lệ.
- Kiểm tra tính toàn vẹn của dữ liệu sau khi chia tập.
- Phát hiện và xác nhận việc sửa các lỗi đã ghi nhận trong Bug Log.
- Đánh giá hiệu suất mô hình trên Test Set độc lập.

### 3. Phạm vi kiểm thử

**Trong phạm vi:**
- Dataset validation.
- Prediction input/output validation.
- Required columns validation.
- Category label validation.
- Data splitting.
- Data leakage checking.
- Model evaluation.

**Ngoài phạm vi:**
- Kiểm thử giao diện người dùng.
- Kiểm thử API production.
- Kiểm thử hiệu năng hệ thống ở quy mô lớn.
- Kiểm thử tự động dự đoán mức độ ưu tiên bảo hành.

### 4. Môi trường kiểm thử

| Thành phần | Mô tả |
|---|---|
| OS | Windows |
| Python | 3.11.5 |
| Framework | unittest |
| Model | TF-IDF + LinearSVC |
| Dataset | issue_descriptions.csv |
| Dataset size | 4000 records |
| Labels | MAN_HINH, PIN, SAC, PHAN_MEM, NUOC_VAO, KHAC |

### 5. Test Cases

| TC ID | Test Type | Test Description | Expected Result |
|---|---|---|---|
| TC-01 | Data Quality | Dataset không rỗng | Dataset có dữ liệu |
| TC-02 | Data Quality | Kiểm tra ID duy nhất và tồn tại | Không có ID thiếu hoặc trùng |
| TC-03 | Data Quality | Kiểm tra nhãn hợp lệ | Tất cả nhãn thuộc VALID_LABELS |
| TC-04 | Data Quality | Kiểm tra mô tả rỗng | Không có mô tả rỗng |
| TC-05 | Data Validation | Kiểm tra các cột bắt buộc | Đủ các cột yêu cầu |
| TC-06 | Functional | Dự đoán mô tả hợp lệ | Trả về nhãn hợp lệ |
| TC-07 | Negative / Bug-03 | Prediction trả về UNKNOWN | Hệ thống từ chối nhãn không hợp lệ |
| TC-08 | Boundary | Mô tả rỗng | Phát sinh ValueError |
| TC-09 | Boundary | Mô tả chỉ có khoảng trắng | Phát sinh ValueError |
| TC-10 | Negative | Mô tả không phải chuỗi | Phát sinh TypeError |
| TC-11 | Negative | Prediction rỗng | Hệ thống từ chối kết quả |
| TC-12 | Boundary | Mô tả dài | Xử lý và trả về nhãn hợp lệ |
| TC-13 | Negative / Bug-04 | Dataset thiếu cột bắt buộc | Phát sinh ValueError |
| TC-14 | Negative / Bug-05 | Dataset chứa category không hợp lệ | Phát sinh ValueError |
| TC-15 | Pipeline | Kiểm tra phân chia dataset | Train, Validation, Test đúng kích thước |
| TC-16 | Data Integrity | Kiểm tra Data Leakage | Không có mô tả trùng giữa các tập |
| TC-17 | Model Evaluation | Đánh giá mô hình trên Test Set | Metrics được tính và lưu thành báo cáo |

### 6. Test Data

Dataset `issue_descriptions.csv` có 4000 bản ghi với 6 category.

| Dataset | Samples | Percentage |
|---|---:|---:|
| Train | 2778 | 69.5% |
| Validation | 596 | 14.9% |
| Test | 626 | 15.7% |

Các trường hợp dữ liệu không hợp lệ được tạo bằng unit test nhằm kiểm tra validation logic.

### 7. Test Execution

Chạy toàn bộ Unit Test:

```powershell
python -m unittest discover -s tests -v
```

Chạy Pipeline Test:

```powershell
python src/data/split_data.py
python src/data/check_split.py
python src/models/evaluate_test.py
```

### 8. Entry Criteria

- Dataset đã được chuẩn bị.
- Các chức năng prediction và data validation đã được triển khai.
- Môi trường Python và dependencies đã được cài đặt.
- Các model artifacts cần thiết đã tồn tại.

### 9. Exit Criteria

- Tất cả test case được thực thi.
- Không còn test case FAIL sau khi sửa lỗi.
- Các lỗi phát hiện được ghi nhận trong Bug Log.
- Có ảnh chụp màn hình kết quả thực thi.
- Kết quả đánh giá mô hình được lưu trong thư mục reports.

### 10. Deliverables

- Test Plan: `docs/test-plan.md`
- Test Report: `docs/test-report.md`
- Bug Log: `docs/bug-log.md`
- Screenshots: `docs/screenshot/`
- Model Evaluation: `reports/test_metrics.json`
- Confusion Matrix: `reports/test_confusion_matrix.png`
