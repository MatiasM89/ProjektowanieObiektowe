package controllers

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"

	"github.com/labstack/echo/v4"
)

type WeatherResponse struct {
	Main struct {
		Temp     float64 `json:"temp"`
		Humidity int     `json:"humidity"`
	} `json:"main"`
	Weather []struct {
		Description string `json:"description"`
	} `json:"weather"`
	Name string `json:"name"`
}

type WeatherRequest struct {
	City string `json:"city" query:"city"`
}

func GetWeather(c echo.Context) error {
	var req WeatherRequest
	c.Bind(&req)

	if req.City == "" {
		req.City = c.QueryParam("city")
	}

	weather := fetchWeather(req.City)

	return c.JSON(http.StatusOK, weather)
}

func fetchWeather(city string) *WeatherResponse {
	apiKey := os.Getenv("OPENWEATHERMAP_API_KEY")
	url := fmt.Sprintf("http://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s&units=metric", city, apiKey)
	resp, _ := http.Get(url)
	body, _ := io.ReadAll(resp.Body)
	resp.Body.Close()

	var weather WeatherResponse
	json.Unmarshal(body, &weather)

	return &weather
}