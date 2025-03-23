package handlers

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"os/exec"
	"path/filepath"
	"strings"
	_ "strconv"
)

const outputSuffix = "_processed"

func ProcessHandler(c *gin.Context) {
	uuids := strings.Split(c.Param("uuid"), ",") // Hỗ trợ nhiều UUID

	upscale := c.Query("upscale")
	bit := c.Query("bit")

	// Kiểm tra giá trị upscale hợp lệ
	if upscale != "2" && upscale != "4" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Upscale must be '2' or '4'"})
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
		metaPath := filepath.Join(dataDir, fileUUID+".json")
		outpngPath := filepath.Join(dataDir, fileUUID+outputSuffix+".png")
                outpngUpPath := filepath.Join(dataDir, fileUUID+outputSuffix+"-complete.png")
		outdicomPath := filepath.Join(dataDir, fileUUID+outputSuffix+".dcm")

		// Dicom to PNG
		cmd := exec.Command("python3", "scripts/dicom_to_png.py", "-i", dicomPath, "-o", outpngPath, "-m", metaPath)
		if err := cmd.Run(); err != nil {
			continue
		}

		cmd = exec.Command("python3", "models/inference_realesrgan.py", "-n", "RealESRGAN_x4plus", "-i", outpngPath, "-o", outpngUpPath, "-mp", "models/data/x"+upscale+"/net_g_latest.pth")
                if err := cmd.Run(); err != nil {
                        continue
                }

		cmd = exec.Command("python3", "scripts/png_to_dicom.py", "-i", outpngUpPath, "-o", outdicomPath, "-m", metaPath)
                if err := cmd.Run(); err != nil {
                        continue
                }

		processedFiles = append(processedFiles, gin.H{
			"uuid":    fileUUID,
			"output":  outdicomPath,
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
