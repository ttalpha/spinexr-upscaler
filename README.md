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
     -F "upscale=4" \
     -F "bit=16"
```
**Phản hồi mẫu:**
```json
{
  "message": "Files uploaded and processed",
  "files": [
    { "filename": "scan1.dcm", "output": "uploads/u_abc123/1743418533703/scan1_processed.dicom", "userId": "abc123" },
    { "filename": "scan2.dcm", "output": "uploads/u_abc123/1743418533703/scan2_processed.dicom", "userId": "abc123" }
  ]
}
```

### Tải file đã xử lý
```sh
curl -O http://localhost:8080/image/abc123/1743418533703/scan1_processed.dicom
```
File PNG sẽ được tải về.

### Lấy danh sách ảnh đã xử lý của user
```sh
curl -X GET http://localhost:8080/abc123/images
```
**Phản hồi mẫu:**
Response:
```json
{
  "images": [
    { "filename": "scan1_processed.dicom", "path": "uploads/u_abc123/1743418533703/scan1_processed.dicom" },
    { "filename": "scan2_processed.dicom", "path": "uploads/u_abc123/1743418533703/scan2_processed.dicom" }
  ]
}
```

---

## 3. Câu trúc API
| Method | Endpoint               | Description |
|--------|------------------------|-------------|
| POST   | `/upload`              | Upload file DICOM và xử lý |
| GET    | `/image/:userId/:filename`      | Tải file DICOM đã xử lý của user |
| GET    | `/:userId/images`                | Lấy danh sách ảnh đã xử lý của user |

---

## 4. Cấu trúc thư mục
```bash
tree -L3 ./
./
├── cmd
│   └── main.go
├── go.mod
├── go.sum
├── internal
│   ├── handlers
│   │   ├── imageHandler.go
│   │   ├── listImagesHandler.go
│   │   └── uploads.go
│   ├── services
│   │   ├── dicom.go
│   │   └── exec.go
│   └── utils
│       └── file.go
├── LICENSE
├── main.go -> cmd/main.go
├── Makefile
├── models -> ../models
├── README.md
├── scripts
│   ├── dicom_to_png.py
│   └── png_to_dicom.py
├── uploads
└── vendor
    ├── github.com
    │   ├── bytedance
    │   ├── cloudwego
    │   ├── gabriel-vasile
    │   ├── gin-contrib
    │   ├── gin-gonic
    │   ├── goccy
    │   ├── google
    │   ├── go-playground
    │   ├── joho
    │   ├── json-iterator
    │   ├── klauspost
    │   ├── leodido
    │   ├── mattn
    │   ├── modern-go
    │   ├── pelletier
    │   ├── twitchyliquid64
    │   └── ugorji
    ├── golang.org
    │   └── x
    ├── google.golang.org
    │   └── protobuf
    ├── gopkg.in
    │   └── yaml.v3
    └── modules.txt

33 directories, 17 files
```

---

## 4. Giấy phép
Dự án được phát hành theo giấy phép MIT.
