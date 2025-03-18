package handlers

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"os"
	"path/filepath"
)

func DownloadHandler(c *gin.Context) {
	fileUUID := c.Param("uuid")
	filePath := filepath.Join(dataDir, fileUUID+"_processed.png")

	if _, err := os.Stat(filePath); os.IsNotExist(err) {
		c.JSON(http.StatusNotFound, gin.H{"error": "File not found"})
		return
	}

	c.File(filePath)
}
