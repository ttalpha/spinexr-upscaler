package services

import (
	"fmt"
	"os/exec"
	"path/filepath"
)

const outputSuffix = "_processed.png"

func ProcessDICOM(filename string) (string, error) {
	dicomPath := filepath.Join("data", filename)
	outputPath := filepath.Join("data", filename+outputSuffix)

	cmd := exec.Command("python3", "scripts/process.py", dicomPath, outputPath)
	if err := cmd.Run(); err != nil {
		return "", fmt.Errorf("processing failed: %v", err)
	}

	return outputPath, nil
}
