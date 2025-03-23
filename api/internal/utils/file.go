package utils

import "path/filepath"

func IsDICOM(filename string) bool {
	ext := filepath.Ext(filename)
	return ext == ".dicom" || ext == ".dcm"
}
