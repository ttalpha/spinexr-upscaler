package handlers

import (
	"net/http"
	"os"
	"path/filepath"

	"github.com/gin-gonic/gin"
)

func ImageHandler(c *gin.Context) {
	userId := c.Param("userId")
	timestamp := c.Param("timestamp")
	filename := c.Param("filename")
	filePath := filepath.Join("uploads", "u_"+userId, timestamp, filename)

	if _, err := os.Stat(filePath); os.IsNotExist(err) {
		c.JSON(http.StatusNotFound, gin.H{"error": "File not found"})
		return
	}

	c.File(filePath)
}
