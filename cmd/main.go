package main

import (
	"log"
	"os"

	"github.com/gin-gonic/gin"
	"su-api/internal/handlers"
)

const dataDir = "data"

func main() {
	r := gin.Default()

	r.POST("/upload", handlers.UploadHandler)
	r.POST("/process/:uuid", handlers.ProcessHandler)
	r.GET("/download/:uuid", handlers.DownloadHandler)

	if err := os.MkdirAll(dataDir, os.ModePerm); err != nil {
		log.Fatal(err)
	}

	r.Run(":8080")
}
