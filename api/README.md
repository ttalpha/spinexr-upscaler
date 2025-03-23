# Spinexr Upscaler API

Spinexr Upscaler API là một dịch vụ RESTful API giúp upload, xử lý và tải xuống các file DICOM. API hỗ trợ upscale ảnh (2, 4) và bit depth (8, 16) thông qua script xử lý bằng Python.

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
Gửi file DICOM với thông số **upscale** (chỉ nhận `2` hoặc `4`) và **bit** (chỉ nhận `8` hoặc `16`).

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
curl -X POST "http://localhost:8080/process/123e4567-e89b-12d3-a456-426614174000?upscale=4&bit=16"
```
**Phản hồi mẫu:**
```json
{
  "message": "Processing completed",
  "files": [
    { "uuid": "123e4567-e89b-12d3-a456-426614174000", "output": "data/123e4567-e89b-12d3-a456-426614174000_processed.png", "upscale": "4", "bit": "16" }
  ]
}
```

### Tải file đã xử lý
```sh
curl -O http://localhost:8080/download/123e4567-e89b-12d3-a456-426614174000
```
File PNG sẽ được tải về.

### Get list of existing UUIDs
```sh
curl -X GET "http://localhost:8080/uuid"
```
**Phản hồi mẫu:**
Response:
```json
{
  "uuids": ["uuid1", "uuid2", "uuid3"]
}
```

---

## 3. Câu trúc API
| Method | Endpoint               | Description |
|--------|------------------------|-------------|
| POST   | `/upload`              | Upload file DICOM |
| POST   | `/process/:uuid`       | Process file DICOM |
| GET    | `/download/:uuid`      | Download processed PNG |
| GET    | `/uuid`                | Get list of existing UUIDs |

---

## 4. Cấu trúc thư mục
```bash
┌─[dora@localhost]─[~/su-api]
└──╼ $tree ./
./
├── assets
│   └── dicom
│       └── 0a7f1942e568e05704c976da16c9d1a5.dicom
├── cmd
│   └── main.go
├── go.mod
├── go.sum
├── internal
│   ├── handlers
│   │   ├── download.go
│   │   ├── process.go
│   │   ├── upload.go
│   │   └── uuid.go
│   ├── services
│   │   ├── dicom.go
│   │   ├── exec.go
│   │   └── process.go
│   └── utils
│       └── file.go
├── LICENSE
├── main.go -> cmd/main.go
├── Makefile
├── README.md
└── scripts
    └── process.py

9 directories, 17 files
```

---

## 4. Giấy phép
Dự án được phát hành theo giấy phép MIT.
