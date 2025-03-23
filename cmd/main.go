package main

import (
	"log"
	"os"
	"path/filepath"
	"time"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
	"su-api/internal/handlers"
)

const dataDir = "data"
const timeClr = 6
const autoClr = false

func cleanDataFolder() {
	for {
		time.Sleep(timeClr * time.Hour)

		files, err := filepath.Glob(filepath.Join(dataDir, "*"))
		if err != nil {
			log.Println("Lỗi khi lấy danh sách file:", err)
			continue
		}

		for _, file := range files {
			err := os.Remove(file)
			if err != nil {
				log.Println("Lỗi khi xóa file:", file, err)
			} else {
				log.Println("Đã xóa file:", file)
			}
		}
	}
}

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

	if autoClr {
		go cleanDataFolder()
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
