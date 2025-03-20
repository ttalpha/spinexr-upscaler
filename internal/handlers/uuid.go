package handlers

import (
	"net/http"
	"os"
	"strings"

	"github.com/gin-gonic/gin"
)

func ListUUIDHandler(c *gin.Context) {
	files, err := os.ReadDir(dataDir)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to read directory"})
		return
	}

	var uuids []string
	for _, file := range files {
		if !file.IsDir() && strings.HasSuffix(file.Name(), ".dcm") {
			uuid := strings.TrimSuffix(file.Name(), ".dcm")
			uuids = append(uuids, uuid)
		}
	}

	c.JSON(http.StatusOK, gin.H{"uuids": uuids})
}
