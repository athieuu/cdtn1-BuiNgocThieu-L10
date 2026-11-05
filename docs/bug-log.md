# Bug Log

## BUG-01: Xác minh kiểm tra dữ liệu đầu vào của hàm dự đoán

- **Phạm vi:** `src/predict.py`
- **Nội dung kiểm tra:** Đảm bảo hàm dự đoán xử lý đúng mô tả hợp lệ và từ chối đầu vào không hợp lệ.
- **Cách kiểm chứng:** Chạy `python -m unittest discover -s tests -v`.
- **Kết quả thực tế:** Các test `test_predict_valid_description`, `test_reject_empty_description`, `test_reject_non_string_description` và `test_reject_whitespace_description` đều PASS.
- **Kết luận:** Các trường hợp đầu vào được kiểm tra đều đáp ứng kết quả mong đợi. Chưa ghi nhận lỗi trong phạm vi kiểm thử này.
- **Trạng thái:** Đã kiểm chứng – PASS.

## BUG-02: Xác minh tính nhất quán khi chạy lại pipeline

- **Phạm vi:** `src/run_pipeline.py`
- **Nội dung kiểm tra:** Xác minh quy trình kiểm tra dữ liệu, chia tập dữ liệu và huấn luyện mô hình có tạo ra kết quả nhất quán khi chạy lại.
- **Cách kiểm chứng:** Chạy `python src/run_pipeline.py` hai lần liên tiếp và so sánh báo cáo đầu ra.
- **Kết quả thực tế:** Cả hai lần chạy đều kết thúc với `PIPELINE COMPLETED SUCCESSFULLY`. Số lượng dữ liệu, phân bố nhãn và các chỉ số validation của hai mô hình đều giống nhau.
- **Kết luận:** Chưa ghi nhận sự không nhất quán trong hai lần chạy đã kiểm tra. Kết quả chưa chứng minh tính tái lập trong mọi môi trường.
- **Trạng thái:** Đã kiểm chứng – PASS.

## BUG-03: Model trả về nhãn phân loại không hợp lệ

- **Mức độ:** Major
- **Phạm vi:** `src/predict.py`
- **Mô tả:** Hàm `predict_issue()` chấp nhận nhãn dự đoán ngoài danh sách 6 nhãn hợp lệ.
- **Cách tái hiện:** Thiết lập `model.predict.return_value = ["UNKNOWN"]` và gọi `predict_issue()` với mô tả hợp lệ.
- **Nguyên nhân:** Hàm chưa xác thực nhãn đầu ra của model.
- **Cách sửa:** Bổ sung `VALID_LABELS` và kiểm tra nhãn trước khi trả về kết quả.
- **Kiểm thử:** Test trước khi sửa FAIL với lỗi `ValueError not raised`. Sau khi sửa, test riêng và toàn bộ 10 unit tests đều PASS.
- **Commit:** [cdcf688](https://github.com/athieuu/cdtn1-BuiNgocThieu-L10/commit/cdcf688)
- **Trạng thái:** Fixed – PASS.

## BUG-04: Thiếu cột bắt buộc gây lỗi KeyError không rõ ràng

- **Mức độ nghiêm trọng:** Minor (Nhẹ)
- **Thành phần:** `src/data/check_split.py`
- **Mô tả lỗi:** Chương trình kiểm tra dữ liệu chưa xác thực các cột bắt buộc trước khi truy cập cột `issue_desc`. Khi file dữ liệu thiếu cột này, chương trình phát sinh lỗi `KeyError` thay vì thông báo lỗi dữ liệu rõ ràng.
- **Cách tái hiện:** Tạo file `train.csv` chỉ chứa cột `issue_category`, không có cột `issue_desc`, sau đó chạy hàm `check_split.main()`.
- **Nguyên nhân:** Chưa có bước kiểm tra sự tồn tại của các cột bắt buộc trước khi xử lý dữ liệu.
- **Giải pháp:** Bổ sung kiểm tra schema cho các cột `issue_desc` và `issue_category`. Nếu thiếu cột, chương trình phát sinh `ValueError` kèm thông báo tên file và cột bị thiếu.
- **Kiểm thử:** Trước khi sửa, test thất bại với lỗi `KeyError: 'issue_desc'`. Sau khi sửa, test `test_missing_required_column` PASS. Toàn bộ 13 test trong bộ kiểm thử đều PASS.
- **Trạng thái:** Đã sửa - PASS