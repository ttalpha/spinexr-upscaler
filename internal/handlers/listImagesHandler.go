package handlers

import (
	"net/http"
	"os"
	"path/filepath"

	"github.com/gin-gonic/gin"
)

func ListImagesHandler(c *gin.Context) {
	userId := c.Param("userId")
	userDir := filepath.Join("uploads", "u_"+userId)

	// Kiểm tra nếu thư mục của user không tồn tại
	if _, err := os.Stat(userDir); os.IsNotExist(err) {
		c.JSON(http.StatusNotFound, gin.H{"error": "User not found"})
		return
	}

	// Lấy danh sách các thư mục timestamp của userId
	var images []gin.H
	err := filepath.Walk(userDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		// Kiểm tra nếu là file DICOM
		if !info.IsDir() && (filepath.Ext(info.Name()) == ".dicom" || filepath.Ext(info.Name()) == ".dcm") {
			images = append(images, gin.H{
				"filename": info.Name(),
				"path":     path,
			})
		}

		return nil
	})

	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to read directory"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"images": images})
}
