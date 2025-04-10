package utils

import (
	_ "fmt"
	"os"
	"path/filepath"
)

func ChkDir(dir string) bool {
	execPath, err := os.Executable()
	if err != nil {
		return false
	}

	execDir := filepath.Dir(execPath)

	scriptsPath := filepath.Join(execDir, dir)

	info, err := os.Stat(scriptsPath)
	if os.IsNotExist(err) {
		return false
	}
	if err != nil {
		return false
	}

	if info.IsDir() {
		return true
	} else {
		return false
	}
}
