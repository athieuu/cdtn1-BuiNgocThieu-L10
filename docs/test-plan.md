# Test Plan – L10 Automatic Warranty Request Classification

## 1. Mục tiêu
Kiểm chứng tính đúng đắn của kiểm tra dữ liệu đầu vào, hàm dự đoán và validation dữ liệu trước khi chia tập. Phân loại kiểm thử thành ba nhóm theo yêu cầu C4: test đúng (normal), test biên (boundary), test dữ liệu sai (invalid).

## 2. Phạm vi
- `tests/test_pipeline.py`
- `src/predict.py`
- `src/data/split_data.py`
- `src/data/check_split.py`

## 3. Test cases

| ID | Nhóm | Test case | Kết quả mong đợi |
|---|---|---|---|
| TC-01 | Đúng | Dataset có đủ cột bắt buộc | Test PASS |
| TC-02 | Đúng | Dataset có dữ liệu | Số dòng > 0 |
| TC-03 | Đúng | Các mô tả không rỗng | Tất cả mô tả sau strip khác rỗng |
| TC-04 | Đúng | Nhãn thuộc 6 nhãn hợp lệ | Không có nhãn ngoài danh sách |
| TC-05 | Đúng | ID tồn tại và duy nhất | Không thiếu/trùng ID |
| TC-06 | Đúng | Dự đoán mô tả hợp lệ | Trả về nhãn hợp lệ |
| TC-07 | Biên | Mô tả một ký tự | Xử lý được và trả nhãn |
| TC-08 | Biên | Mô tả dài (lặp chuỗi 1000 lần) | Xử lý được và trả nhãn |
| TC-09 | Biên | Mô tả có Unicode/ký tự đặc biệt | Không lỗi, trả nhãn |
| TC-10 | Biên | Mô tả có khoảng trắng đầu/cuối | Chuỗi được strip trước predict |
| TC-11 | Sai | Mô tả rỗng | Ném ValueError |
| TC-12 | Sai | Mô tả toàn khoảng trắng | Ném ValueError |
| TC-13 | Sai | Input không phải chuỗi | Ném TypeError |
| TC-14 | Sai | Model trả nhãn UNKNOWN | Ném ValueError |
| TC-15 | Sai | Model trả prediction rỗng | Ném ValueError |
| TC-16 | Sai | File split thiếu cột bắt buộc | Ném ValueError thông báo rõ |
| TC-17 | Sai | Raw dataset có nhãn UNKNOWN | Ném ValueError |
| TC-18 | Sai | Raw dataset có mô tả trống | Ném ValueError |
| TC-19 | Sai | Raw dataset thiếu category | Ném ValueError |

## 4. Cách chạy
Từ thư mục gốc repo, sử dụng Python 3.11 và dependencies đã pin:

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

## 5. Evidence
Chụp ảnh màn hình terminal sau khi chạy toàn bộ suite. Ảnh cần hiển thị danh sách test và summary tổng số test / kết quả. Chỉ cập nhật trạng thái PASS trong Test Report sau khi suite thực tế chạy thành công.
