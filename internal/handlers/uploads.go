package handlers

import (
	"github.com/gin-gonic/gin"
	_ "github.com/google/uuid"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	_ "strings"
	"time"
	"su-api/internal/utils"
)

const dataDir = "uploads"

func UploadsHandler(c *gin.Context) {
	// Lấy thông tin từ request
	userId := c.Param("userId")
	upscale := c.DefaultPostForm("upscale", "2")
	bit := c.DefaultPostForm("bit", "8")

	// Kiểm tra giá trị upscale hợp lệ
	if upscale != "2" && upscale != "4" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Upscale must be '2' or '4'"})
		return
	}

	// Kiểm tra giá trị bit hợp lệ
	if bit != "8" && bit != "16" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Bit must be '8' or '16'"})
		return
	}

	// Kiểm tra file
	form, err := c.MultipartForm()
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Failed to parse form data"})
		return
	}

	files := form.File["file"]
	if len(files) == 0 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "No files uploaded"})
		return
	}

	// Tạo thư mục userId và timestamp
	timestamp := time.Now().UnixMilli()
	userDir := filepath.Join(dataDir, "u_"+userId, string(timestamp))
	if err := os.MkdirAll(userDir, os.ModePerm); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create directory"})
		return
	}

	uploadedFiles := []gin.H{}
	for _, file := range files {
		if !utils.IsDICOM(file.Filename) {
			continue // Bỏ qua file không phải DICOM
		}

		// Lưu file DICOM vào thư mục đã tạo
		filePath := filepath.Join(userDir, file.Filename)
		if err := c.SaveUploadedFile(file, filePath); err != nil {
			continue
		}

		// Xử lý file DICOM (chuyển thành PNG, upscale, sau đó chuyển lại DICOM)
		dicomPath := filePath
		metaPath := dicomPath[:len(dicomPath)-len(filepath.Ext(dicomPath))] + ".json"
		outpngPath := dicomPath[:len(dicomPath)-len(filepath.Ext(dicomPath))] + ".png"
		outpngUpPath := filepath.Join(userDir, "output.png")
		outdicomPath := dicomPath[:len(dicomPath)-len(filepath.Ext(dicomPath))] + "_processed.dicom"

		// Bước 1: Chuyển DICOM sang PNG
		cmd := exec.Command("python3", "scripts/dicom_to_png.py", "-i", dicomPath, "-o", outpngPath, "-m", metaPath)
		if err := cmd.Run(); err != nil {
			continue
		}

		// Bước 2: Upscale ảnh PNG
		cmd = exec.Command("python3", "models/inference_realesrgan.py", "-n", "RealESRGAN_x4plus", "-i", outpngPath, "-o", outpngUpPath, "-t", "512", "-mp", "models/weights/g_x"+upscale+".pth")
		if err := cmd.Run(); err != nil {
			continue
		}

		// Bước 3: Chuyển lại PNG đã upscale thành DICOM
		cmd = exec.Command("python3", "scripts/png_to_dicom.py", "-i", outpngUpPath, "-o", outdicomPath, "-m", metaPath)
		if err := cmd.Run(); err != nil {
			continue
		}

		// Xoá các file trung gian (PNG, output.png)
		os.Remove(outpngPath)
		os.Remove(outpngUpPath)

		uploadedFiles = append(uploadedFiles, gin.H{
			"filename": file.Filename,
			"output":   outdicomPath,
			"userId":   userId,
		})
	}

	if len(uploadedFiles) == 0 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "No valid DICOM files uploaded"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Files uploaded and processed", "files": uploadedFiles})
}
