package handlers

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"os/exec"
	"path/filepath"
	"strings"
)

const outputSuffix = "_processed.png"

func ProcessHandler(c *gin.Context) {
	uuids := strings.Split(c.Param("uuid"), ",") // Hỗ trợ nhiều UUID

	upscale := c.Query("upscale")
	bit := c.Query("bit")

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

	processedFiles := []gin.H{}

	for _, fileUUID := range uuids {
		dicomPath := filepath.Join(dataDir, fileUUID+".dcm")
		outputPath := filepath.Join(dataDir, fileUUID+outputSuffix)

		// Chạy script xử lý với upscale và bit
		cmd := exec.Command("python3", "scripts/process.py", dicomPath, outputPath, upscale, bit)
		if err := cmd.Run(); err != nil {
			continue // Bỏ qua file nếu xử lý lỗi
		}

		processedFiles = append(processedFiles, gin.H{
			"uuid":    fileUUID,
			"output":  outputPath,
			"upscale": upscale,
			"bit":     bit,
		})
	}

	if len(processedFiles) == 0 {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "No files processed"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Processing completed", "files": processedFiles})
}
