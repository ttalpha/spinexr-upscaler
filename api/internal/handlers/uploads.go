package handlers

import (
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
	"su-api/internal/utils"
	"time"

	"github.com/gin-gonic/gin"
)

const dataDir = "uploads"

func UploadsHandler(c *gin.Context) {
	userId := c.PostForm("userId")
	if userId == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "User ID is missing"})
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
	uploadedFiles := make([]gin.H, 0, len(files))
	userDir := filepath.Join(dataDir, "u_"+userId, strconv.FormatInt(timestamp, 10))
	if err := os.MkdirAll(userDir, os.ModePerm); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create directory"})
		return
	}

	for _, file := range files {
		if !utils.IsDICOM(file.Filename) {
			continue
		}

		filePath := filepath.Join(userDir, file.Filename)
		if err := c.SaveUploadedFile(file, filePath); err != nil {
			continue
		}

		dicomPath := filePath
		metaPath := dicomPath[:len(dicomPath)-len(filepath.Ext(dicomPath))] + ".json"
		outpngPath := dicomPath[:len(dicomPath)-len(filepath.Ext(dicomPath))] + ".png"
		outpngUpPath := dicomPath[:len(dicomPath)-len(filepath.Ext(dicomPath))] + "_out.png"

		cmd := exec.Command("python3", "scripts/dicom_to_png.py", "-i", dicomPath, "-o", outpngPath, "-m", metaPath)
		if err := cmd.Run(); err != nil {
			continue
		}

		cmd = exec.Command("python3", "models/inference_realesrgan.py", "-n", "RealESRGAN_x4plus", "-i", outpngPath, "-o", userDir, "-t", "512", "-mp", "models/weights/g_x4_v3.pth")
		if err := cmd.Run(); err != nil {
			continue
		}
		cmd = exec.Command("python3", "scripts/png_to_dicom.py", "-i", outpngUpPath, "-o", dicomPath, "-m", metaPath)
		if err := cmd.Run(); err != nil {
			continue
		}

		os.Remove(outpngPath)
		os.Remove(outpngUpPath)
		os.Remove(metaPath)

		// get file size of the output dicom file
		fileInfo, err := os.Stat(dicomPath)
		if err != nil {
			continue
		}
		fileSize := fileInfo.Size()

		uploadedFiles = append(uploadedFiles, gin.H{
			"filename": file.Filename,
			"output":   dicomPath,
			"size":     fileSize,
		})
	}

	c.JSON(http.StatusOK, gin.H{"message": "Files uploaded and processed", "files": uploadedFiles})
}
