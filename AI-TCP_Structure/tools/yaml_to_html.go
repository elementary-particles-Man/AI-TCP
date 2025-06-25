// yaml_to_html.go converts an intent YAML file to an HTML table.
//
// Usage:
//   go run yaml_to_html.go <input.yaml> <output.html>
// Example:
//   go run yaml_to_html.go ../yaml/intent_001.yaml ../html_logs/intent_001.html

package main

import (
	"bufio"
	"html/template"
	"log"
	"os"
	"path/filepath"
	"strings"
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

// parseSimpleYAML parses a minimal YAML structure without external dependencies.
// It expects a top-level mapping with optional fields:
// id, name/title, description, components, connections.
// Components and connections are simple sequences of mappings.
func parseSimpleYAML(path string) (Intent, error) {
	file, err := os.Open(path)
	if err != nil {
		return Intent{}, err
	}
	defer file.Close()

	var intent Intent
	scanner := bufio.NewScanner(file)
	var section string
	var comp Component
	var conn Connection
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			continue
		}
		if strings.HasPrefix(line, "#") {
			continue
		}

		switch {
		case line == "components:":
			if comp.ID != "" || comp.Label != "" || comp.Type != "" {
				intent.Components = append(intent.Components, comp)
				comp = Component{}
			}
			section = "components"
			continue
		case line == "connections:":
			if conn.From != "" || conn.To != "" || conn.Label != "" {
				intent.Connections = append(intent.Connections, conn)
				conn = Connection{}
			}
			section = "connections"
			continue
		}

		if section == "components" {
			if strings.HasPrefix(line, "- ") {
				if comp.ID != "" || comp.Label != "" || comp.Type != "" {
					intent.Components = append(intent.Components, comp)
					comp = Component{}
				}
				line = strings.TrimPrefix(line, "- ")
			}
			if strings.HasPrefix(line, "id:") {
				comp.ID = strings.TrimSpace(strings.TrimPrefix(line, "id:"))
			} else if strings.HasPrefix(line, "name:") {
				comp.Label = strings.TrimSpace(strings.TrimPrefix(line, "name:"))
			} else if strings.HasPrefix(line, "type:") {
				comp.Type = strings.TrimSpace(strings.TrimPrefix(line, "type:"))
			} else if strings.HasPrefix(line, "label:") {
				comp.Label = strings.TrimSpace(strings.TrimPrefix(line, "label:"))
			}
			continue
		}

		if section == "connections" {
			if strings.HasPrefix(line, "- ") {
				if conn.From != "" || conn.To != "" || conn.Label != "" {
					intent.Connections = append(intent.Connections, conn)
					conn = Connection{}
				}
				line = strings.TrimPrefix(line, "- ")
			}
			if strings.HasPrefix(line, "from:") {
				conn.From = strings.TrimSpace(strings.TrimPrefix(line, "from:"))
			} else if strings.HasPrefix(line, "to:") {
				conn.To = strings.TrimSpace(strings.TrimPrefix(line, "to:"))
			} else if strings.HasPrefix(line, "label:") {
				conn.Label = strings.TrimSpace(strings.TrimPrefix(line, "label:"))
			}
			continue
		}

		// top-level fields
		if strings.HasPrefix(line, "id:") {
			intent.ID = strings.TrimSpace(strings.TrimPrefix(line, "id:"))
		} else if strings.HasPrefix(line, "title:") {
			intent.Title = strings.TrimSpace(strings.TrimPrefix(line, "title:"))
		} else if strings.HasPrefix(line, "name:") {
			intent.Title = strings.TrimSpace(strings.TrimPrefix(line, "name:"))
		} else if strings.HasPrefix(line, "description:") {
			intent.Description = strings.TrimSpace(strings.TrimPrefix(line, "description:"))
		}
	}

	// append final pending entries
	if comp.ID != "" || comp.Label != "" || comp.Type != "" {
		intent.Components = append(intent.Components, comp)
	}
	if conn.From != "" || conn.To != "" || conn.Label != "" {
		intent.Connections = append(intent.Connections, conn)
	}

	return intent, scanner.Err()
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

	intent, err := parseSimpleYAML(inputPath)
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
