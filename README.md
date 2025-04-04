# X-ray Upscaler

## Goal
The goal of this project is to develop an AI model that can upscale X-ray images, improving their resolution and clarity for better medical analysis.

## Project Setup

### Prerequisites
- Anaconda or Miniconda (for `server/` and `ai/` only)
- CUDA 12.6 (for `server/` and `ai/` only)
- Node.js 18 or higher (for `web/` and `desktop/` only)

### Installation

#### AI Model
Follow instructions on [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN)

#### Desktop Application
1. Navigate to the `desktop/` directory:
    ```sh
    cd desktop
    ```
2. Install the required npm packages:
    ```sh
    npm install
    ```
3. Run the desktop application:
    ```sh
    npm start
    ```

#### Web Application
1. Navigate to the `web` directory:
    ```sh
    cd web
    ```
2. Install the required npm packages:
    ```sh
    npm install
    ```
3. Run the web application:
    ```sh
    npm run dev
    ```
4. Open the browser at [http://localhost:5173](http://localhost:5173)

<<<<<<< HEAD
### Server
1. Navigate to the `server` directory:
    ```sh
    cd server
    ```
2. Create a conda environment:
    ```sh
    conda create -n server python=3.12.7
    ```
3. Activate the conda environment:
    ```sh
    conda activate server
    ```
4. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```
5. Run the server:
    ```sh
    flask --app . run --debug
    ```
6. Open the browser at [http://localhost:5000](http://localhost:5000)

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## Acknowledgments
- Special thanks to all contributors and supporters of this project.
=======
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
>>>>>>> ac754b6175ef22e399fda23af8ce0d5c65d50598
