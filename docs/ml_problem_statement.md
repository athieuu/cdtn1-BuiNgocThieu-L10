# ĐẶC TẢ BÀI TOÁN MACHINE LEARNING

## Tự động phân loại yêu cầu bảo hành

**Sinh viên:** Bùi Ngọc Thiệu
**MSSV:** [2374802010471]
**Chuyên ngành:** AI
**Luồng nghiệp vụ:** L10 – Tự động phân loại yêu cầu bảo hành
**Phiên bản:** 1.0 (Bản nháp)

## 1. Xác định bài toán

### 1.1. Mô tả vấn đề

Mekong Mobile tiếp nhận các yêu cầu bảo hành có chứa mô tả lỗi thiết bị dưới dạng văn bản tự do. Việc phân loại các mô tả này bằng phương pháp thủ công có thể tốn thời gian và dẫn đến sự thiếu nhất quán trong quá trình phân loại.

Dự án hướng đến xây dựng mô hình học máy có khả năng tự động dự đoán nhóm sự cố dựa trên mô tả lỗi bảo hành của khách hàng. Kết quả dự đoán sẽ hỗ trợ nhân viên tiếp nhận trong quá trình xử lý yêu cầu bảo hành.

### 1.2. Loại bài toán Machine Learning

* **Phương pháp học:** Học có giám sát (Supervised Learning).
* **Loại bài toán:** Phân loại văn bản đa lớp (Multi-class Text Classification).
* **Đầu vào:** Mô tả lỗi thiết bị dưới dạng văn bản.
* **Đầu ra:** Nhóm sự cố được dự đoán từ danh sách nhãn có sẵn trong bộ dữ liệu.

Mô hình sẽ dự đoán một nhóm sự cố cho mỗi mô tả lỗi hợp lệ.

## 2. Định nghĩa nhãn

### 2.1. Nhãn phân loại

Nhãn mục tiêu là nhóm sự cố tương ứng với từng mô tả lỗi bảo hành.

Mỗi nhãn đại diện cho một loại sự cố thiết bị được định nghĩa trước trong bộ dữ liệu của case study.

### 2.2. Nguồn nhãn

Nhãn được lấy từ bộ dữ liệu mô tả lỗi bảo hành đã được gán nhãn trong case study Mekong Mobile.

Tên và định nghĩa chính xác của từng nhóm sự cố cần được xác nhận bằng cách kiểm tra bộ dữ liệu gốc và tài liệu mô tả dữ liệu.

### 2.3. Nguyên tắc gán nhãn

* Sử dụng nhãn được gán trong bộ dữ liệu gốc làm nhãn chuẩn.
* Không tự ý tạo thêm nhóm sự cố khi chưa được phê duyệt.
* Kiểm tra các bản ghi bị thiếu hoặc có nhãn không nhất quán trước khi huấn luyện.
* Chỉ chỉnh sửa nhãn khi có căn cứ từ tài liệu dữ liệu hoặc kết quả rà soát được phê duyệt.

## 3. Bộ dữ liệu

### 3.1. Nguồn dữ liệu

Dự án sử dụng bộ dữ liệu mô tả lỗi bảo hành thuộc case study Mekong Mobile.

Theo case study, bộ dữ liệu dự kiến có khoảng 4.000 mô tả lỗi đã được gán nhãn. Số lượng bản ghi thực tế có thể sử dụng sẽ được xác nhận sau khi kiểm tra dữ liệu.

### 3.2. Đặc trưng đầu vào và nhãn mục tiêu

| Trường dữ liệu | Vai trò           | Mô tả                                 |
| -------------- | ----------------- | ------------------------------------- |
| Mô tả lỗi      | Đặc trưng đầu vào | Văn bản mô tả sự cố của thiết bị      |
| Nhóm sự cố     | Nhãn mục tiêu     | Nhóm lỗi được gán cho mô tả tương ứng |

Các trường dữ liệu khác chỉ được sử dụng nếu xác nhận có liên quan và có sẵn.

### 3.3. Tiền xử lý dữ liệu

* Kiểm tra các mô tả lỗi bị thiếu hoặc để trống.
* Kiểm tra các bản ghi không có nhãn mục tiêu.
* Loại bỏ các bản ghi trùng lặp hoàn toàn khi phù hợp.
* Chuẩn hóa văn bản một cách nhất quán, không làm mất thông tin quan trọng.
* Chuyển đổi văn bản thành dạng số phù hợp với mô hình.

### 3.4. Chia tập dữ liệu

Dữ liệu dự kiến được chia thành ba tập:

| Tập dữ liệu | Tỷ lệ | Mục đích                                               |
| ----------- | ----: | ------------------------------------------------------ |
| Training    |   70% | Huấn luyện mô hình                                     |
| Validation  |   15% | Điều chỉnh tham số và lựa chọn mô hình                 |
| Test        |   15% | Đánh giá mô hình cuối cùng trên dữ liệu chưa từng thấy |

Sử dụng một giá trị random seed cố định để đảm bảo khả năng tái lập kết quả. Ưu tiên chia dữ liệu theo phương pháp phân tầng (Stratified Split) để duy trì tỷ lệ nhãn giữa các tập khi có thể.

Tập Test không được sử dụng trong quá trình huấn luyện hoặc điều chỉnh tham số mô hình.

## 4. Mô hình và phương pháp cơ sở

### 4.1. Mô hình đề xuất

Mô hình ban đầu sử dụng TF-IDF để biểu diễn văn bản kết hợp với một thuật toán học máy như Logistic Regression.

Đây là phương pháp đơn giản, phù hợp để xây dựng mô hình phân loại văn bản ban đầu và làm cơ sở so sánh với các mô hình phức tạp hơn.

### 4.2. Mô hình cơ sở (Baseline)

Baseline được đề xuất là mô hình luôn dự đoán nhóm sự cố xuất hiện nhiều nhất trong tập Training.

Mô hình đề xuất sẽ được so sánh với Baseline bằng chỉ số Macro F1-score để đánh giá mức độ cải thiện.

## 5. Chỉ số đánh giá và tiêu chí chấp nhận

### 5.1. Các chỉ số đánh giá

| Chỉ số         | Ý nghĩa                                                             |
| -------------- | ------------------------------------------------------------------- |
| Accuracy       | Tỷ lệ dự đoán chính xác trên tổng số bản ghi                        |
| Precision      | Tỷ lệ dự đoán đúng trong số các bản ghi được dự đoán thuộc một nhóm |
| Recall         | Tỷ lệ bản ghi thực tế thuộc một nhóm được mô hình nhận diện đúng    |
| Macro F1-score | Trung bình F1-score của các nhóm, mỗi nhóm có trọng số như nhau     |

Macro F1-score được chọn làm chỉ số đánh giá chính vì phản ánh hiệu suất trên tất cả các nhóm sự cố, hạn chế việc các nhóm có nhiều dữ liệu chi phối kết quả chung.

### 5.2. Tiêu chí chấp nhận

* Mô hình cần đạt Macro F1-score tối thiểu 0,75 trên tập Test.
* Mô hình đề xuất cần có Macro F1-score cao hơn Baseline.
* Kết quả đánh giá cần bao gồm báo cáo phân loại theo từng nhóm để xác định các nhóm có hiệu suất thấp.

Các ngưỡng trên là đề xuất ban đầu cho dự án và cần được xem xét lại sau khi kiểm tra dữ liệu và kết quả Baseline.

## 6. Rủi ro về Bias và đạo đức

### 6.1. Rủi ro 1: Mất cân bằng nhãn

Một số nhóm sự cố có thể có số lượng bản ghi huấn luyện nhiều hơn đáng kể so với các nhóm khác. Do đó, mô hình có thể hoạt động tốt trên các nhóm phổ biến nhưng dự đoán kém trên các nhóm ít dữ liệu.

**Biện pháp giảm thiểu:**

* Kiểm tra phân bố nhãn trước khi huấn luyện.
* Sử dụng phương pháp chia dữ liệu phân tầng khi phù hợp.
* Đánh giá Macro F1-score và Recall theo từng nhóm.
* Cân nhắc sử dụng trọng số lớp hoặc lấy mẫu lại nếu cần thiết.

### 6.2. Rủi ro 2: Nhãn dữ liệu không chính xác hoặc thiếu nhất quán

Bộ dữ liệu ban đầu có thể chứa các nhãn sai, không rõ ràng hoặc được gán không nhất quán. Mô hình có thể học những sai sót này và lặp lại chúng trong quá trình dự đoán.

**Biện pháp giảm thiểu:**

* Kiểm tra các nhãn bị thiếu hoặc không nhất quán.
* Rà soát các bản ghi có nội dung không rõ ràng khi có thể.
* Ghi lại những trường hợp chỉnh sửa nhãn đã được phê duyệt.
* Cho phép nhân viên kiểm tra và điều chỉnh kết quả dự đoán.

### 6.3. Rủi ro 3: Phụ thuộc quá mức vào kết quả dự đoán

Nhân viên có thể chấp nhận kết quả dự đoán không chính xác mà không kiểm tra lại mô tả lỗi ban đầu. Điều này có thể dẫn đến việc phân loại sai yêu cầu bảo hành.

**Biện pháp giảm thiểu:**

* Hiển thị kết quả dự đoán dưới dạng thông tin tham khảo.
* Cho phép nhân viên điều chỉnh nhóm sự cố được dự đoán.
* Cung cấp quy trình kiểm tra thủ công khi mô hình không thể đưa ra kết quả hợp lệ.
* Không sử dụng dự đoán làm căn cứ duy nhất cho các quyết định bảo hành.

## 7. Giới hạn của mô hình

* Mô hình chỉ có thể dự đoán các nhóm sự cố xuất hiện trong dữ liệu huấn luyện.
* Hiệu suất phụ thuộc vào chất lượng, số lượng và phân bố của bộ dữ liệu.
* Mô hình có thể hoạt động kém với mô tả quá ngắn, không rõ ràng hoặc khác biệt đáng kể so với dữ liệu huấn luyện.
* Dự đoán mức độ ưu tiên chưa nằm trong bài toán ML đã xác nhận, cho đến khi có nhãn ưu tiên hoặc quy tắc nghiệp vụ được phê duyệt.

## 8. Kết quả đầu ra dự kiến

Với mỗi mô tả lỗi bảo hành đầu vào, mô hình dự kiến trả về:

* Nhóm sự cố được dự đoán.
* Trạng thái phân loại, cho biết hệ thống có tạo được kết quả hay không.

Kết quả sẽ được hiển thị cho nhân viên tiếp nhận để kiểm tra và tham khảo trong quá trình xử lý yêu cầu bảo hành.
