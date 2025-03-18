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
	file, err := c.FormFile("file")
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "File upload failed"})
		return
	}

	if !utils.IsDICOM(file.Filename) {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Only DICOM (.dicom, .dcm) files are allowed"})
		return
	}

	// Tạo UUID cho file
	fileUUID := uuid.New().String()
	newFileName := fileUUID + filepath.Ext(file.Filename)
	filePath := filepath.Join(dataDir, newFileName)

	// Lưu file vào thư mục data/
	c.SaveUploadedFile(file, filePath)

	c.JSON(http.StatusOK, gin.H{"message": "File uploaded successfully", "uuid": fileUUID, "path": filePath})
}
