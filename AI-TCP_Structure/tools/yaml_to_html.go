// yaml_to_html.go converts an intent YAML file to an HTML table.
//
// Usage:
//   go run yaml_to_html.go <input.yaml> <output.html>
// Example:
//   go run yaml_to_html.go ../yaml/intent_001.yaml ../html_logs/intent_001.html

package main

import (
	"html/template"
	"log"
	"os"
	"path/filepath"

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

const htmlTemplate = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>{{ .Title }}</title>
  <style>
    table { border-collapse: collapse; width: 100%; font-family: sans-serif; }
    th, td { border: 1px solid #aaa; padding: 6px; text-align: left; }
    th { background-color: #f0f0f0; }
    caption { font-size: 1.2em; margin: 10px; font-weight: bold; }
  </style>
</head>
<body>
  <h2>{{ .Title }}</h2>
  <p>{{ .Description }}</p>

  <table>
    <caption>🧱 Components</caption>
    <tr><th>ID</th><th>Type</th><th>Label</th></tr>
    {{ range .Components }}
    <tr><td>{{ .ID }}</td><td>{{ .Type }}</td><td>{{ .Label }}</td></tr>
    {{ end }}
  </table>

  <br>

  <table>
    <caption>🔗 Connections</caption>
    <tr><th>From</th><th>To</th><th>Label</th></tr>
    {{ range .Connections }}
    <tr><td>{{ .From }}</td><td>{{ .To }}</td><td>{{ .Label }}</td></tr>
    {{ end }}
  </table>
</body>
</html>
`

func main() {
	if len(os.Args) < 3 {
		log.Fatalf("Usage: %s <input.yaml> <output.html>\n", os.Args[0])
	}
	inputPath := os.Args[1]
	outputPath := os.Args[2]

	yamlFile, err := os.ReadFile(inputPath)
	if err != nil {
		log.Fatalf("Failed to read YAML: %v", err)
	}

	var intent Intent
	err = yaml.Unmarshal(yamlFile, &intent)
	if err != nil {
		log.Fatalf("Failed to parse YAML: %v", err)
	}

	tmpl, err := template.New("html").Parse(htmlTemplate)
	if err != nil {
		log.Fatalf("Failed to parse template: %v", err)
	}

	err = os.MkdirAll(filepath.Dir(outputPath), 0755)
	if err != nil {
		log.Fatalf("Failed to create output directory: %v", err)
	}

	outputFile, err := os.Create(outputPath)
	if err != nil {
		log.Fatalf("Failed to create HTML file: %v", err)
	}
	defer outputFile.Close()

	err = tmpl.Execute(outputFile, intent)
	if err != nil {
		log.Fatalf("Template execution failed: %v", err)
	}

	log.Printf("✅ HTML generated: %s\n", outputPath)
}
