package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strings"

	"gopkg.in/yaml.v3"
)

type Component struct {
	ID    string `yaml:"id"`
	Type  string `yaml:"type"`
	Label string `yaml:"label"`
}

type Connection struct {
	From  string `yaml:"from"`
	To    string `yaml:"to"`
	Label string `yaml:"label"`
}

type Intent struct {
	ID          string       `yaml:"id"`
	Title       string       `yaml:"title"`
	Description string       `yaml:"description"`
	Components  []Component  `yaml:"components"`
	Connections []Connection `yaml:"connections"`
}

func loadYAML(path string) (*Intent, error) {
	data, err := ioutil.ReadFile(path)
	if err != nil {
		return nil, err
	}
	var intent Intent
	err = yaml.Unmarshal(data, &intent)
	if err != nil {
		return nil, err
	}
	return &intent, nil
}

func generateMermaid(intent *Intent) string {
	var b strings.Builder

	b.WriteString("graph TD\n")

	// ノード定義
	for _, c := range intent.Components {
		line := fmt.Sprintf("    %s[\"%s\"]:::%s\n", c.ID, c.Label, c.Type)
		b.WriteString(line)
	}

	b.WriteString("\n")

	// 接続定義
	for _, conn := range intent.Connections {
		line := fmt.Sprintf("    %s -->|%s| %s\n", conn.From, conn.Label, conn.To)
		b.WriteString(line)
	}

	b.WriteString("\n")
	b.WriteString("    classDef source fill:#f9f,stroke:#333,stroke-width:1px\n")
	b.WriteString("    classDef process fill:#bbf,stroke:#333,stroke-width:1px\n")
	b.WriteString("    classDef response fill:#bfb,stroke:#333,stroke-width:1px\n")
	b.WriteString("    classDef log fill:#ffb,stroke:#333,stroke-width:1px\n\n")

	// クラス割当
	for _, c := range intent.Components {
		b.WriteString(fmt.Sprintf("    class %s %s\n", c.ID, c.Type))
	}

	return b.String()
}

func main() {
	if len(os.Args) < 2 {
		log.Fatalf("Usage: %s <input.yaml>\n", os.Args[0])
	}
	inputPath := os.Args[1]
	intent, err := loadYAML(inputPath)
	if err != nil {
		log.Fatalf("Failed to load YAML: %v\n", err)
	}

	output := generateMermaid(intent)

	outputPath := fmt.Sprintf("mermaid/%s.mmd.md", intent.ID)
	err = os.MkdirAll("mermaid", 0755)
	if err != nil {
		log.Fatalf("Failed to create output dir: %v\n", err)
	}

	err = ioutil.WriteFile(outputPath, []byte(output), 0644)
	if err != nil {
		log.Fatalf("Failed to write Mermaid file: %v\n", err)
	}

	fmt.Printf("✅ Mermaid diagram generated: %s\n", outputPath)
}
