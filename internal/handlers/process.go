package handlers

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
	"os/exec"
	"path/filepath"
)

const outputSuffix = "_processed.png"

func ProcessHandler(c *gin.Context) {
	fileUUID := c.Param("uuid")
	dicomPath := filepath.Join(dataDir, fileUUID+".dcm")
	outputPath := filepath.Join(dataDir, fileUUID+outputSuffix)

	cmd := exec.Command("python3", "scripts/process.py", dicomPath, outputPath)
	if err := cmd.Run(); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": fmt.Sprintf("Processing failed: %v", err)})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Processing completed", "uuid": fileUUID, "output": outputPath})
}
