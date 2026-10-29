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
