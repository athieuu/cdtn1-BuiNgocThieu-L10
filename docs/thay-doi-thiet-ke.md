# Thay đổi thiết kế BT2

## 1. Tổ chức dữ liệu
- Bổ sung bước kiểm tra chất lượng dữ liệu đầu vào.
- Chia dữ liệu thành Train, Validation và Test theo tỷ lệ xấp xỉ 70/15/15.
- Gom các mô tả trùng khớp trước khi chia để hạn chế trùng dữ liệu giữa các tập.

## 2. Huấn luyện mô hình
- Bổ sung Baseline: TF-IDF kết hợp Logistic Regression.
- Bổ sung mô hình so sánh: TF-IDF kết hợp Linear SVM.
- Chọn mô hình dựa trên Macro-F1 của Validation.
- Chỉ dùng Test để đánh giá cuối cùng sau khi chọn mô hình.

## 3. Đánh giá
- Lưu các chỉ số Accuracy, Macro-F1, Weighted-F1 và chỉ số theo từng lớp.
- Tạo confusion matrix để phân tích kết quả phân loại.

## 4. Kiểm thử
- Bổ sung kiểm thử dữ liệu đầu vào.
- Bổ sung pipeline chạy tuần tự bằng một lệnh.
- Dùng unittest để kiểm tra cấu trúc dữ liệu, mô tả, nhãn và ID.

## 5. Hạn chế
- Các mô tả gần giống nhau vẫn có thể xuất hiện ở nhiều tập dữ liệu.
- Điểm đánh giá cao cần được xem xét cùng hạn chế này.
