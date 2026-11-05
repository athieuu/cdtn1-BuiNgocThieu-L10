# TEST REPORT — L10 Automatic Warranty Request Classification

## 1. Thông tin kiểm thử

- **Dự án:** Automatic Warranty Request Classification — L10
- **Mã sinh viên:** 2374802010471
- **Phiên bản:** BT3
- **Môi trường:** Python 3.11.5
- **Framework kiểm thử:** unittest
- **Model:** TF-IDF + LinearSVC
- **Dataset:** 4.000 mẫu mô tả sự cố bảo hành
- **Test dataset:** 626 mẫu

## 2. Test Cases

| TC ID | Component | Test Scenario | Input / Precondition | Test Steps | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|---|---|
| TC-01 | Dataset | Dataset không rỗng | `issue_descriptions.csv` | Kiểm tra số lượng mẫu | Dataset có dữ liệu | Dataset có 4.000 mẫu | PASS |
| TC-02 | Dataset | Kiểm tra ID duy nhất | Dataset gốc | Kiểm tra ID bị thiếu hoặc trùng | Tất cả ID hợp lệ và duy nhất | Không có ID thiếu hoặc trùng | PASS |
| TC-03 | Dataset | Kiểm tra nhãn hợp lệ | Dataset gốc | Đối chiếu nhãn với tập nhãn cho phép | Chỉ chứa 6 nhãn hợp lệ | Tất cả nhãn hợp lệ | PASS |
| TC-04 | Dataset | Kiểm tra mô tả rỗng | Dataset gốc | Kiểm tra mô tả bị thiếu hoặc rỗng | Không có mô tả rỗng | Không có mô tả rỗng | PASS |
| TC-05 | Dataset | Kiểm tra cột bắt buộc | Dataset gốc | Kiểm tra schema | Có `desc_id`, `issue_desc`, `issue_category` | Đủ cột bắt buộc | PASS |
| TC-06 | Prediction | Dự đoán mô tả hợp lệ | `"pin hao nhanh"` | Gọi `predict_issue()` | Trả về nhãn hợp lệ | Hàm trả về nhãn hợp lệ | PASS |
| TC-07 | Prediction | Nhãn dự đoán không hợp lệ — BUG-03 | Model trả về `UNKNOWN` | Gọi `predict_issue()` | Phát sinh `ValueError` | Trước khi sửa: FAIL; sau khi sửa: ValueError, PASS | PASS |
| TC-08 | Prediction | Mô tả rỗng | `""` | Gọi `predict_issue()` | Phát sinh `ValueError` | Test PASS | PASS |
| TC-09 | Prediction | Mô tả chỉ có khoảng trắng | `"   "` | Gọi `predict_issue()` | Phát sinh `ValueError` | Test PASS | PASS |
| TC-10 | Prediction | Input không phải chuỗi | `123` | Gọi `predict_issue()` | Phát sinh `TypeError` | Test PASS | PASS |
| TC-11 | Prediction | Model trả về prediction rỗng | `[]` | Gọi `predict_issue()` | Phát sinh `ValueError` | Test PASS | PASS |
| TC-12 | Prediction | Mô tả dài | Chuỗi mô tả dài | Gọi `predict_issue()` | Hàm xử lý và trả về nhãn hợp lệ | Test PASS | PASS |
| TC-13 | Data Validation | Thiếu cột bắt buộc — BUG-04 | Dataset thiếu `issue_desc` | Gọi `check_split.main()` | Phát sinh `ValueError` có thông báo cột thiếu | Trước sửa: KeyError; sau khi sửa: ValueError, PASS | PASS |
| TC-14 | Data Validation | Nhãn category không hợp lệ — BUG-05 | Dataset chứa `UNKNOWN` | Gọi `split_data.main()` | Phát sinh `ValueError` | Trước khi sửa: không phát sinh ValueError; sau khi sửa: PASS | PASS |
| TC-15 | Data Split | Kiểm tra chia dữ liệu | Dataset gốc, RANDOM_SEED=42 | Chạy `split_data.py` | Chia train/validation/test theo tỷ lệ dự kiến | Train 2778, validation 596, test 626 | PASS |
| TC-16 | Data Leakage | Kiểm tra trùng mô tả giữa các tập | Các tập dữ liệu đã chia | Chạy `check_split.py` | Không có mô tả trùng giữa các tập | Leakage = 0 | PASS |
| TC-17 | Model Evaluation | Đánh giá model trên test set | 626 test samples | Chạy `evaluate_test.py` | Tính Accuracy, Macro-F1, Weighted-F1 và confusion matrix | Accuracy = 1.0000; Macro-F1 = 1.0000; Weighted-F1 = 1.0000 | PASS |

## 3. Tổng kết kiểm thử

- Unit tests: 14/14 PASS.
- Data split: PASS.
- Data leakage check: PASS.
- Model evaluation: PASS.
- Bugs được sửa và xác minh: BUG-03, BUG-04, BUG-05.
- Accuracy trên test set: 100%.
- Macro-F1 trên test set: 100%.
- Weighted-F1 trên test set: 100%.

**Kết luận:** Các kiểm thử đã thực hiện đều đạt kết quả mong đợi. Hệ thống phân loại sự cố bảo hành đáp ứng các kiểm tra về dữ liệu, validation đầu vào, validation đầu ra và đánh giá model trong phạm vi kiểm thử đã thực hiện.
