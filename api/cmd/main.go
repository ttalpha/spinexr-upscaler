package main

import (
	"log"
	"os"
	"time"
	"su-api/internal/handlers"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
	"path/filepath"
)

const timeClr = 6
const autoClr = false

func cleanDataFolder() {
	ticker := time.NewTicker(24 * time.Hour)
	defer ticker.Stop()

	for {
		<-ticker.C

		files, err := os.ReadDir("uploads")
		if err != nil {
			log.Println("Error reading directory:", err)
			continue
		}

		for _, file := range files {
			userDir := filepath.Join("uploads", file.Name())
			if info, err := os.Stat(userDir); err == nil && info.IsDir() {
				if time.Since(info.ModTime()) > 24*time.Hour {
					os.RemoveAll(userDir)
					log.Printf("Deleted old user directory: %s", userDir)
				}
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

	r.POST("/upload", handlers.UploadAndProcessHandler)
	r.GET("/image/:userId/:filename", handlers.ImageHandler)
	r.GET("/:userId/images", handlers.ListImagesHandler)

	if err := os.MkdirAll("uploads", os.ModePerm); err != nil {
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
