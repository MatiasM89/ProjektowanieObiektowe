package main

import (
	"weather/controllers"
	"github.com/joho/godotenv"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func main() {
	godotenv.Load();

	e := echo.New()

	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	e.GET("/weather", controllers.GetWeather)
	e.POST("/weather", controllers.GetWeather)

	 e.Start(":8080")
}