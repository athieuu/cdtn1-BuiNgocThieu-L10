# Đặc tả yêu cầu phần mềm (SRS)

## Phân loại tự động yêu cầu bảo hành

**Sinh viên:** Bùi Ngọc Thiệu – 2374802010471 – Track AI
**Học phần:** Chuyên đề tốt nghiệp 1, Học kỳ 1, 2026–2027
**Luồng nghiệp vụ:** L10 – Phân loại tự động yêu cầu bảo hành
**Phiên bản:** 1.0 (Bản nháp)

## 1. Giới thiệu

### 1.1 Mục đích

Tài liệu này đặc tả các yêu cầu chức năng và phi chức năng của hệ thống Phân loại tự động yêu cầu bảo hành. Hệ thống nhằm hỗ trợ nhân viên tiếp nhận bảo hành bằng cách tự động phân loại mô tả lỗi của yêu cầu bảo hành.

### 1.2 Phát biểu bài toán

Mekong Mobile tiếp nhận các yêu cầu bảo hành có chứa mô tả lỗi thiết bị dưới dạng văn bản tự do. Việc phân loại thủ công các mô tả này có thể tốn thêm công sức và dẫn đến phân loại thiếu nhất quán.

Hệ thống đề xuất sử dụng một mô hình phân loại văn bản để dự đoán nhóm sự cố từ mô tả lỗi bảo hành của khách hàng. Kết quả dự đoán được hiển thị cho nhân viên để tham khảo trong quá trình xử lý yêu cầu.

### 1.3 Phạm vi

Hệ thống cho phép nhân viên tiếp nhận bảo hành gửi mô tả lỗi, nhận nhóm sự cố được dự đoán và xem lại kết quả phân loại. Nhân viên có thể chỉnh sửa nhóm sự cố khi dự đoán chưa chính xác. Quản trị viên có thể xem danh sách nhóm sự cố được hỗ trợ, thống kê phân loại và các trường hợp được xác nhận là phân loại sai.

Hệ thống tập trung vào việc phân loại sự cố. Việc phân công bảo hành, lên lịch sửa chữa, quản lý kho linh kiện và toàn bộ vòng đời bảo hành nằm ngoài phạm vi hiện tại.

### 1.4 Định nghĩa

| Thuật ngữ         | Định nghĩa                                                           |
| ----------------- | -------------------------------------------------------------------- |
| Yêu cầu bảo hành  | Yêu cầu do khách hàng gửi để được bảo hành sản phẩm.                 |
| Mô tả lỗi         | Thông tin văn bản tự do mô tả vấn đề của thiết bị.                   |
| Nhóm sự cố        | Nhãn được định nghĩa trước, đại diện cho một loại lỗi của thiết bị.  |
| Mô hình phân loại | Mô hình học máy dự đoán nhóm sự cố từ văn bản.                       |
| Dự đoán           | Nhóm sự cố do mô hình phân loại trả về.                              |
| Nhân viên         | Nhân viên tiếp nhận bảo hành, người gửi và xem xét các mô tả lỗi.    |

## 2. Mô tả tổng quan

### 2.1 Bối cảnh sản phẩm

Hệ thống là một bản mẫu ứng dụng độc lập dùng để phân loại mô tả lỗi bảo hành. Hệ thống gồm giao diện nhập liệu, thành phần tiền xử lý văn bản, mô hình phân loại học máy và thành phần hiển thị kết quả.

### 2.2 Nhóm người dùng

| Người dùng                   | Mô tả                                                                                                          |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Nhân viên tiếp nhận bảo hành | Gửi mô tả lỗi, xem kết quả dự đoán và chỉnh sửa nhóm sự cố khi cần.                                            |
| Quản trị viên                | Xem danh sách nhóm sự cố được hỗ trợ, thống kê phân loại và các trường hợp được xác nhận phân loại sai.        |

### 2.3 Môi trường vận hành

* Ngôn ngữ lập trình: Python 3.11
* Xử lý dữ liệu: pandas
* Học máy: scikit-learn
* Môi trường phát triển: Jupyter Notebook / Visual Studio Code
* Quản lý phiên bản: Git và GitHub

### 2.4 Giả định và ràng buộc

* Hệ thống sử dụng bộ dữ liệu mô tả lỗi bảo hành được cung cấp cho bài toán nghiên cứu, tùy thuộc vào khả năng cung cấp dữ liệu.
* Mô hình phân loại chỉ có thể dự đoán các nhóm sự cố xuất hiện trong dữ liệu huấn luyện.
* Nhân viên chịu trách nhiệm xem xét kết quả dự đoán trước khi sử dụng trong xử lý bảo hành thực tế.
* Việc phân loại mức độ ưu tiên cần có quy tắc nghiệp vụ được định nghĩa riêng hoặc nhãn ưu tiên đã được xác minh. Chức năng này chưa được xem là một phần của mô hình văn bản cho đến khi được xác nhận.

## 3. Yêu cầu chức năng

| Mã    | Yêu cầu                                                                                           | Mức ưu tiên |
| ----- | ------------------------------------------------------------------------------------------------- | ----------- |
| FR-01 | Hệ thống phải cho phép nhân viên nhập và gửi mô tả lỗi bảo hành.                                  | MUST        |
| FR-02 | Hệ thống phải kiểm tra mô tả lỗi được gửi không bị bỏ trống.                                      | MUST        |
| FR-03 | Hệ thống phải dự đoán nhóm sự cố từ mô tả lỗi hợp lệ bằng mô hình phân loại.                      | MUST        |
| FR-04 | Hệ thống phải hiển thị nhóm sự cố được dự đoán cho nhân viên.                                     | MUST        |
| FR-05 | Hệ thống phải cho phép nhân viên chỉnh sửa nhóm sự cố được dự đoán.                               | SHOULD      |
| FR-06 | Hệ thống phải thông báo cho nhân viên khi mô tả lỗi bị bỏ trống.                                  | SHOULD      |
| FR-07 | Hệ thống phải hiển thị danh sách các nhóm sự cố mà hệ thống hỗ trợ.                               | SHOULD      |
| FR-08 | Hệ thống phải hiển thị số lượng yêu cầu đã được phân loại theo từng nhóm sự cố.                   | COULD       |
| FR-09 | Hệ thống phải cho phép quản trị viên xem các trường hợp được nhân viên xác nhận là phân loại sai. | COULD       |

### 3.1 Chi tiết yêu cầu chức năng

**FR-01 – Gửi mô tả lỗi**

* Hệ thống phải cung cấp ô nhập mô tả lỗi bảo hành.
* Nhân viên phải có thể gửi mô tả để phân loại.

**FR-02 – Kiểm tra mô tả lỗi**

* Hệ thống phải từ chối mô tả trống hoặc chỉ chứa khoảng trắng.
* Hệ thống phải hiển thị thông báo xác thực khi mô tả không hợp lệ.

**FR-03 – Phân loại mô tả lỗi**

* Hệ thống phải xử lý mô tả hợp lệ và trả về nhóm sự cố được dự đoán.
* Nếu mô hình không thể trả về dự đoán hợp lệ, hệ thống phải báo rằng việc phân loại không thành công.

**FR-04 – Hiển thị kết quả phân loại**

* Hệ thống phải hiển thị nhóm sự cố được dự đoán.
* Hệ thống phải phân biệt được dự đoán thành công với phân loại thất bại.

**FR-05 – Chỉnh sửa nhóm sự cố được dự đoán**

* Nhân viên phải có thể chọn nhóm sự cố đã chỉnh sửa từ danh sách nhóm được hỗ trợ.
* Hệ thống phải lưu lại nhóm sự cố đã chỉnh sửa cho trường hợp tương ứng.

## 4. Yêu cầu phi chức năng

| Mã     | Yêu cầu                                 | Ngưỡng chấp nhận                                                                                                                   |
| ------ | --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| NFR-01 | Thời gian phản hồi phân loại            | Hệ thống phải trả về kết quả phân loại trong vòng 3 giây cho ít nhất 95% yêu cầu trong môi trường kiểm thử đã định nghĩa.          |
| NFR-02 | Thời gian phản hồi khi kiểm tra đầu vào | Hệ thống phải hiển thị thông báo xác thực trong vòng 1 giây sau khi gửi mô tả trống.                                               |
| NFR-03 | Hiệu năng phân loại                     | Mô hình phải đạt macro F1-score tối thiểu 0.75 trên tập dữ liệu kiểm tra độc lập (held-out).                                       |
| NFR-04 | Xử lý lỗi                               | Hệ thống phải hiển thị thông báo lỗi rõ ràng cho 100% các trường hợp phân loại thất bại được mô phỏng trong kiểm thử.              |
| NFR-05 | Khả năng tái lập                        | Việc chia dữ liệu và huấn luyện mô hình phải sử dụng random seed cố định để hỗ trợ tái lập thí nghiệm.                             |

**Lưu ý:** Các ngưỡng trên là tiêu chí chấp nhận đề xuất cho bản mẫu. Cần được xem xét và điều chỉnh dựa trên bộ dữ liệu, mô hình cơ sở (baseline) và góp ý của giảng viên.

## 5. Yêu cầu dữ liệu

### 5.1 Nguồn dữ liệu

Dự án dựa trên tình huống nghiên cứu Mekong Mobile. Bộ dữ liệu được kỳ vọng chứa các mô tả lỗi bảo hành và nhãn nhóm sự cố tương ứng. Tên tệp chính xác, số lượng bản ghi sử dụng được và phân bố nhãn cần được xác minh với bộ dữ liệu được cung cấp trên LMS của học phần trước khi triển khai.

### 5.2 Dữ liệu đầu vào

| Trường            | Kiểu   | Mô tả                          | Ràng buộc                                                  |
| ----------------- | ------ | ------------------------------ | ---------------------------------------------------------- |
| issue_description | String | Văn bản mô tả lỗi của thiết bị | Bắt buộc; không được để trống hoặc chỉ chứa khoảng trắng   |

### 5.3 Dữ liệu đầu ra

| Trường                | Kiểu              | Mô tả                                              |
| --------------------- | ----------------- | -------------------------------------------------- |
| predicted_category    | String            | Nhóm sự cố do mô hình dự đoán                      |
| classification_status | String            | Cho biết phân loại thành công hay thất bại         |
| corrected_category    | String (tùy chọn) | Nhóm sự cố do nhân viên chọn để chỉnh sửa dự đoán  |

### 5.4 Xử lý dữ liệu

* Kiểm tra mô tả bị thiếu hoặc trống.
* Áp dụng các bước tiền xử lý văn bản được định nghĩa cho mô hình đã chọn.
* Chuyển văn bản đã xử lý sang dạng biểu diễn mà mô hình yêu cầu.
* Sử dụng mô hình để dự đoán nhóm sự cố.
* Trả kết quả dự đoán về cho ứng dụng.

### 5.5 Chia dữ liệu

Bộ dữ liệu phải được chia thành tập huấn luyện, tập kiểm định và tập kiểm tra. Tỷ lệ chia đề xuất là 70% huấn luyện, 15% kiểm định và 15% kiểm tra. Việc chia nên giữ nguyên tỷ lệ các nhãn khi có thể. Tập kiểm tra phải được tách riêng khỏi quá trình huấn luyện và điều chỉnh mô hình.

## 6. Truy vết yêu cầu

| Mã FR | User Story | Use Case                                    | MoSCoW        |
| ----- | ---------- | ------------------------------------------- | ------------- |
| FR-01 | US1        | UC01 – Gửi mô tả lỗi                        | MUST          |
| FR-02 | US1, US5   | UC01 – Gửi mô tả lỗi                        | MUST / SHOULD |
| FR-03 | US2        | UC02 – Phân loại mô tả lỗi                  | MUST          |
| FR-04 | US3        | UC03 – Xem kết quả phân loại                | MUST          |
| FR-05 | US4        | UC04 – Chỉnh sửa nhóm sự cố được dự đoán    | SHOULD        |
| FR-06 | US5        | UC01 – Gửi mô tả lỗi                        | SHOULD        |
| FR-07 | US6        | UC05 – Xem danh sách nhóm sự cố được hỗ trợ | SHOULD        |
| FR-08 | US7        | UC06 – Xem thống kê phân loại               | COULD         |
| FR-09 | US8        | UC07 – Xem các trường hợp phân loại sai     | COULD         |

### 6.1 Ghi chú về truy vết

* Mỗi yêu cầu chức năng được liên kết với ít nhất một User Story và một Use Case.
* Các yêu cầu MUST thể hiện luồng phân loại cốt lõi.
* Các yêu cầu SHOULD và COULD là tính năng bổ sung, có thể được ưu tiên tùy theo thời gian triển khai.
* Dự đoán mức độ ưu tiên chưa được đưa vào như một yêu cầu học máy đã xác nhận cho đến khi nhãn dữ liệu hoặc quy tắc nghiệp vụ được xác minh.