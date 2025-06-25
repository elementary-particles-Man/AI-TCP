package main

import (
	"fmt"
	"log"
	"os"

	"gopkg.in/yaml.v3"
)

type Component struct {
	ID   string `yaml:"id"`
	Name string `yaml:"name"`
	Type string `yaml:"type"`
}

type Connection struct {
	From  string `yaml:"from"`
	To    string `yaml:"to"`
	Label string `yaml:"label"`
}

type Intent struct {
	ID          string       `yaml:"id"`
	Name        string       `yaml:"name"`
	Components  []Component  `yaml:"components"`
	Connections []Connection `yaml:"connections"`
}

func loadIntent(path string) (*Intent, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	var intent Intent
	if err := yaml.Unmarshal(data, &intent); err != nil {
		return nil, err
	}
	return &intent, nil
}

func checkIntent(path string, intent *Intent) {
	compMap := make(map[string]Component)
	for _, c := range intent.Components {
		compMap[c.ID] = c
	}

	fromCount := make(map[string]int)
	toCount := make(map[string]int)

	for i, conn := range intent.Connections {
		if conn.From != "" {
			fromCount[conn.From]++
			if c, ok := compMap[conn.From]; ok {
				if c.Type == "source" {
					log.Printf("ERROR %s: connection %d uses 'from' with source component '%s'", path, i+1, conn.From)
				}
			}
		}
		if conn.To != "" {
			toCount[conn.To]++
		}
	}

	for _, c := range intent.Components {
		if c.Type == "response" && toCount[c.ID] == 0 {
			log.Printf("ERROR %s: response component '%s' has no incoming connection", path, c.ID)
		}
	}

	for _, c := range intent.Components {
		if fromCount[c.ID] == 0 && toCount[c.ID] == 0 {
			log.Printf("WARN %s: component '%s' defined but not used in connections", path, c.ID)
		}
	}
}

func main() {
	if len(os.Args) < 2 {
		log.Fatalf("Usage: %s <intent.yaml> [intent.yaml ...]", os.Args[0])
	}
	for _, path := range os.Args[1:] {
		intent, err := loadIntent(path)
		if err != nil {
			log.Printf("Failed to load %s: %v", path, err)
			continue
		}
		fmt.Printf("Checking %s\n", path)
		checkIntent(path, intent)
	}
}
