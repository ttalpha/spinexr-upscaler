package main

import (
	"log"
	"os"
	"path/filepath"
	"su-api/internal/handlers"
	"su-api/internal/utils"
	"time"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
)

func cleanDataFolder() {
	ticker := time.NewTicker(24 * time.Hour)
	defer ticker.Stop()

	for {
		<-ticker.C

		userDirs, err := os.ReadDir("uploads")
		if err != nil {
			log.Println("Error reading directory:", err)
			continue
		}

		for _, userDir := range userDirs {
			userDir := filepath.Join("uploads", userDir.Name())
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
		log.Println("No .env file found, using default environment variables")
	}

	allowedOrigins := os.Getenv("CORS_ORIGIN")
	if allowedOrigins == "" {
		allowedOrigins = "*"
	}

	go utils.CleanupStaleClients()

	r := gin.Default()

	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{allowedOrigins},
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE"},
		AllowHeaders:     []string{"Content-Type", "Authorization"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
		MaxAge:           12 * time.Hour,
	}))

	r.POST("/upscale", utils.RateLimitMiddleware(3), handlers.UploadsHandler)
	r.GET("/image/:userId/:timestamp/:filename", utils.RateLimitMiddleware(30), handlers.ImageHandler)
	r.GET("/:userId/images", utils.RateLimitMiddleware(30), handlers.ListImagesHandler)

	if err := os.MkdirAll(filepath.Join(filepath.Dir(os.Args[0]), "uploads"), os.ModePerm); err != nil {
		log.Fatal(err)
	}

	go cleanDataFolder()

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	if err := r.Run(":" + port); err != nil {
		log.Fatal("Error running the server:", err)
	}

	return 0
}

func main() {
	if !utils.ChkDir("scripts") && !utils.ChkDir("models") {
		log.Fatal("Folder scripts is missing")
		os.Exit(1)
	}
	os.Exit(realMain())
}
