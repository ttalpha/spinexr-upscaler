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

const timeClr = 6
const autoClr = false

func cleanDataFolder() {
	for {
		time.Sleep(timeClr * time.Hour)

		files, err := os.ReadDir("uploads")
		if err != nil {
			log.Println("Lỗi khi lấy danh sách file:", err)
			continue
		}

		for _, file := range files {
			// Lọc các thư mục con không phải của user
			if file.IsDir() {
				if err := os.RemoveAll("uploads/" + file.Name()); err != nil {
					log.Println("Lỗi khi xóa thư mục:", file.Name(), err)
				} else {
					log.Println("Đã xóa thư mục:", file.Name())
				}
			}
		}
	}
}

func realMain() int {
	// Tải file .env
	if err := godotenv.Load(); err != nil {
		log.Println("Không tìm thấy file .env, sử dụng giá trị mặc định")
	}

	allowedOrigins := os.Getenv("CORS_ORIGIN")
	if allowedOrigins == "" {
		allowedOrigins = "*"
	}

	// Khởi tạo Gin router
	r := gin.Default()

	// CORS middleware
	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{allowedOrigins},
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE"},
		AllowHeaders:     []string{"Content-Type", "Authorization"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
		MaxAge:           12 * time.Hour,
	}))

	r.POST("/uploads/:userId", handlers.UploadsHandler) // Upload và xử lý ảnh
	r.GET("/image/:userId/:filename", handlers.ImageHandler) // Tải ảnh DICOM của userId
	r.GET("/:userId/images", handlers.ListImagesHandler) // Lấy danh sách ảnh đã xử lý của userId

	// Khởi tạo thư mục uploads nếu chưa có
	if err := os.MkdirAll("uploads", os.ModePerm); err != nil {
		log.Fatal(err)
	}

	// Xóa dữ liệu tự động
	if autoClr {
		go cleanDataFolder()
	}

	// Cấu hình port
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	// Khởi động server
	if err := r.Run(":" + port); err != nil {
		log.Fatal("Lỗi khi khởi động server:", err)
	}

	return 0
}

func main() {
	os.Exit(realMain())
}
