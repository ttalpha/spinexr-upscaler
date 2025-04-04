package handlers

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"time"
	"su-api/internal/utils"
	"fmt"
)

func UploadAndProcessHandler(c *gin.Context) {
	userId := c.Param("userId")
	upscale := c.DefaultPostForm("upscale", "2")
	bit := c.DefaultPostForm("bit", "8")

	if upscale != "2" && upscale != "4" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Upscale must be '2' or '4'"})
		return
	}

	if bit != "8" && bit != "16" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Bit must be '8' or '16'"})
		return
	}

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

	timestamp := time.Now().UnixMilli()
	userDir := filepath.Join("uploads", "u_"+userId, fmt.Sprintf("%d", timestamp))

	if err := os.MkdirAll(userDir, os.ModePerm); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create directory"})
		return
	}

	uploadedFiles := []gin.H{}
	for _, file := range files {
		if !utils.IsDICOM(file.Filename) {
			continue
		}

		filePath := filepath.Join(userDir, file.Filename)
		if err := c.SaveUploadedFile(file, filePath); err != nil {
			continue
		}

		dicomPath := filePath
		outpngPath := dicomPath[:len(dicomPath)-len(filepath.Ext(dicomPath))] + ".png"
		outpngUpPath := filepath.Join(userDir, "output.png")
		outdicomPath := dicomPath[:len(dicomPath)-len(filepath.Ext(dicomPath))] + "_processed.dicom"

		cmd := exec.Command("python3", "scripts/dicom_to_png.py", "-i", dicomPath, "-o", outpngPath)
		if err := cmd.Run(); err != nil {
			continue
		}

		cmd = exec.Command("python3", "models/inference_realesrgan.py", "-n", "RealESRGAN_x4plus", "-i", outpngPath, "-o", outpngUpPath)
		if err := cmd.Run(); err != nil {
			continue
		}

		cmd = exec.Command("python3", "scripts/png_to_dicom.py", "-i", outpngUpPath, "-o", outdicomPath)
		if err := cmd.Run(); err != nil {
			continue
		}

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
