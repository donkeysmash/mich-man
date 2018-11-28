package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
)

// Restaurants has list of restaurant
type Restaurants []Restaurant

type Restaurant struct {
	Address      string `json:"address"`
	Country      string `json:"country"`
	Cuisine      string `json:"cuisine"`
	Latitude     string `json:"latitude"`
	Longitude    string `json:"longitude"`
	Name         string `json:"name"`
	Neighborhood string `json:"neighborhood"`
	NumStar      int8   `json:"num_star"`
	PriceRange   string `json:"price_range"`
	Region       string `json:"region"`
	URL          string `json:"url"`
	Website      string `json:"website"`
}

func main() {
	fmt.Printf("%s", "Hello world")

	jsonFile, err := os.Open("../data/jp2018.json")
	if err != nil {
		fmt.Println(err)
	}
	defer jsonFile.Close()

	byteValue, _ := ioutil.ReadAll(jsonFile)

	var restaurants Restaurants

	json.Unmarshal(byteValue, &restaurants)

	fmt.Printf("bye")
}
