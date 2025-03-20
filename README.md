# Spinexr Upscaler API

Spinexr Upscaler API là một dịch vụ RESTful API giúp upload, xử lý và tải xuống các file DICOM. API hỗ trợ upscale ảnh (x2, x4) và bit depth (8, 16) thông qua script xử lý bằng Python.

## 1. Cài đặt và Chạy API

### Yêu cầu:
- Go 1.18+
- Python 3.x
- Thư viện Python: `?`
- Hệ điều hành: Linux / macOS / Windows

### Cách chạy API:
1. **Clone repository**
```sh
git clone https://github.com/your-repo/spinexr-upscaler-api.git
cd spinexr-upscaler-api
```
2. **Biên dịch ứng dụng**
```sh
go build -o su-api
```
3. **Chạy API với cổng 8080**
```sh
./su-api
```

---

## 2. Sử dụng API với `curl`

### Upload file DICOM
Gửi file DICOM với thông số **upscale** (chỉ nhận `x2` hoặc `x4`) và **bit** (chỉ nhận `8` hoặc `16`).

```sh
curl -X POST http://localhost:8080/upload \
     -F "file=@scan1.dcm" \
     -F "file=@scan2.dcm" \
     -F "upscale=x2" \
     -F "bit=8"
```
**Phản hồi mẫu:**
```json
{
  "message": "Files uploaded successfully",
  "files": [
    { "uuid": "123e4567-e89b-12d3-a456-426614174000", "path": "data/123e4567-e89b-12d3-a456-426614174000.dcm", "upscale": "x2", "bit": "8" }
  ]
}
```

### Xử lý file DICOM
Sử dụng UUID nhận được khi upload để xử lý file.
```sh
curl -X POST "http://localhost:8080/process/123e4567-e89b-12d3-a456-426614174000?upscale=x4&bit=16"
```
**Phản hồi mẫu:**
```json
{
  "message": "Processing completed",
  "files": [
    { "uuid": "123e4567-e89b-12d3-a456-426614174000", "output": "data/123e4567-e89b-12d3-a456-426614174000_processed.png", "upscale": "x4", "bit": "16" }
  ]
}
```

### Tải file đã xử lý
```sh
curl -O http://localhost:8080/download/123e4567-e89b-12d3-a456-426614174000
```
File PNG sẽ được tải về.

---

## 3. Câu trúc API
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/upload` | Upload file DICOM |
| `POST` | `/process/:uuid` | Xử lý file DICOM |
| `GET`  | `/download/:uuid` | Tải file PNG đã xử lý |

---

## 4. Giấy phép
Dự án được phát hành theo giấy phép MIT.
