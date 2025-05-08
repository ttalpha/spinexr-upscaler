package handlers

import (
	"net/http"
	"os"
	"path/filepath"
	"strings"

	"github.com/gin-gonic/gin"
)

func ListImagesHandler(c *gin.Context) {
	userId := c.Param("userId")
	userDir := filepath.Join(filepath.Dir(os.Args[0]), "uploads", "u_"+userId)

	if _, err := os.Stat(userDir); os.IsNotExist(err) {
		c.JSON(http.StatusNotFound, gin.H{"error": "User not found"})
		return
	}

	var images []gin.H
	err := filepath.Walk(userDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		if !info.IsDir() && (filepath.Ext(info.Name()) == ".dicom" || filepath.Ext(info.Name()) == ".dcm") {
			parts := strings.Split(path, string(os.PathSeparator))
			if len(parts) > 2 {
				timestamp := parts[len(parts)-2]
				images = append(images, gin.H{
					"filename": info.Name(),
					"size": 	 info.Size(),
					"timestamp": timestamp,
				})
			}
		}

		return nil
	})

	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to read directory"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"images": images})
}
