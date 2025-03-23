package main

import (
	"log"
	"os"
	"time"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
	"su-api/internal/handlers"
)

const dataDir = "data"

func realMain() int {
	if err := godotenv.Load(); err != nil {
		log.Println("Không tìm thấy file .env, sử dụng giá trị mặc định")
	}

	allowedOrigins := os.Getenv("CORS_ORIGIN")
	if allowedOrigins == "" {
		allowedOrigins = "*"
	}

	r := gin.Default()

	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{allowedOrigins},
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE"},
		AllowHeaders:     []string{"Content-Type", "Authorization"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
		MaxAge:           12 * time.Hour,
	}))

	r.POST("/upload", handlers.UploadHandler)
	r.POST("/process/:uuid", handlers.ProcessHandler)
	r.GET("/download/:uuid", handlers.DownloadHandler)
	r.GET("/uuid", handlers.ListUUIDHandler)

	if err := os.MkdirAll(dataDir, os.ModePerm); err != nil {
		log.Fatal(err)
	}

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	if err := r.Run(":" + port); err != nil {
		log.Fatal("Lỗi khi khởi động server:", err)
	}

	return 0
}

func main() {
	os.Exit(realMain())
}
