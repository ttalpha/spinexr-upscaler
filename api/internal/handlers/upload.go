package handlers

import (
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"net/http"
	"path/filepath"
	"su-api/internal/utils"
)

const dataDir = "data"

func UploadHandler(c *gin.Context) {
	// Lấy thông tin từ request
	upscale := c.PostForm("upscale")
	bit := c.PostForm("bit")

	// Kiểm tra giá trị upscale hợp lệ
	if upscale != "x2" && upscale != "x4" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Upscale must be 'x2' or 'x4'"})
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

	uploadedFiles := []gin.H{}

	for _, file := range files {
		if !utils.IsDICOM(file.Filename) {
			continue // Bỏ qua file không phải DICOM
		}

		fileUUID := uuid.New().String()
		newFileName := fileUUID + filepath.Ext(file.Filename)
		filePath := filepath.Join(dataDir, newFileName)

		// Lưu file vào thư mục data/
		if err := c.SaveUploadedFile(file, filePath); err != nil {
			continue
		}

		uploadedFiles = append(uploadedFiles, gin.H{
			"uuid":    fileUUID,
			"path":    filePath,
			"upscale": upscale,
			"bit":     bit,
		})
	}

	if len(uploadedFiles) == 0 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "No valid DICOM files uploaded"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Files uploaded successfully", "files": uploadedFiles})
}
