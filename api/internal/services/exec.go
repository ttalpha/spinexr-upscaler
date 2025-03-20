package services

import (
	"os/exec"
)

// Thực thi script Python xử lý ảnh
func ExecPythonProcess(pngPath string) (string, error) {
	outputPath := pngPath[:len(pngPath)-4] + "_processed.png"
	cmd := exec.Command("python3", "scripts/process.py", pngPath, outputPath)
	err := cmd.Run()
	if err != nil {
		return "", err
	}
	return outputPath, nil
}
