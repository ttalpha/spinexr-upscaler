package utils

import (
	"net/http"
	"sync"
	"time"

	"github.com/gin-gonic/gin"
	"golang.org/x/time/rate"
)

const (
	requestLimit = 3
	timeWindow   = 5 * time.Minute
)

type Client struct {
	limiter  *rate.Limiter
	lastSeen time.Time
}

var clients = sync.Map{}

func getClientLimiter(ip string) *rate.Limiter {
	now := time.Now()
	val, exists := clients.Load(ip)
	if exists {
		client := val.(*Client)
		client.lastSeen = now
		return client.limiter
	}

	limiter := rate.NewLimiter(rate.Every(timeWindow/time.Duration(requestLimit)), requestLimit)
	clients.Store(ip, &Client{limiter: limiter, lastSeen: now})
	return limiter
}

func RateLimitMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		ip := c.ClientIP()
		limiter := getClientLimiter(ip)

		if !limiter.Allow() {
			c.AbortWithStatusJSON(http.StatusTooManyRequests, gin.H{
				"error": "Too many requests. Try again later.",
			})
			return
		}
		c.Next()
	}
}

func CleanupStaleClients() {
	for {
		time.Sleep(time.Minute)
		clients.Range(func(key, value interface{}) bool {
			client := value.(*Client)
			if time.Since(client.lastSeen) > timeWindow {
				clients.Delete(key)
			}
			return true
		})
	}
}
