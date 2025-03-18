package services

import (
	"fmt"
)

// Convert DICOM to PNG và trích xuất metadata
func ConvertDICOMToPNG(uuid string) (string, map[string]string, error) {
	// Giả lập chuyển đổi
	pngPath := fmt.Sprintf("/data/%s.png", uuid)
	metadata := map[string]string{"PatientName": "John Doe", "StudyDate": "2025-03-11"}
	return pngPath, metadata, nil
}

// Convert PNG -> DICOM giữ nguyên metadata
func ConvertPNGToDICOM(pngPath string, metadata map[string]string) (string, error) {
	dicomPath := pngPath[:len(pngPath)-4] + ".dcm"
	return dicomPath, nil
}
