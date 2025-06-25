package main

import (
    "flag"
    "html/template"
    "log"
    "os"
    "path/filepath"

    "gopkg.in/yaml.v3"
)

type Message struct {
    Speaker string `yaml:"speaker"`
    Text    string `yaml:"text"`
}

type Log struct {
    ID       string    `yaml:"id"`
    Messages []Message `yaml:"messages"`
}

const htmlTemplate = `<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>{{.ID}}</title>
<style>
table{border-collapse:collapse;width:100%}
th,td{border:1px solid #ccc;padding:8px;text-align:left}
th{background:#f2f2f2}
</style>
</head>
<body>
<h2>Negotiation Log: {{.ID}}</h2>
<table>
<tr><th>Speaker</th><th>Text</th></tr>
{{range .Messages}}
<tr><td>{{.Speaker}}</td><td>{{.Text}}</td></tr>
{{end}}
</table>
</body>
</html>`

func main() {
    input := flag.String("input", filepath.Join("yaml_logs", "log_test_case_001.yaml"), "input yaml log")
    output := flag.String("output", filepath.Join("negotiation_logs", "negotiation_test.html"), "output html file")
    flag.Parse()

    data, err := os.ReadFile(*input)
    if err != nil {
        log.Fatalf("read input: %v", err)
    }
    var logData Log
    if err := yaml.Unmarshal(data, &logData); err != nil {
        log.Fatalf("unmarshal yaml: %v", err)
    }

    if err := os.MkdirAll(filepath.Dir(*output), 0755); err != nil {
        log.Fatalf("make dir: %v", err)
    }
    f, err := os.Create(*output)
    if err != nil {
        log.Fatalf("create output: %v", err)
    }
    defer f.Close()

    tmpl := template.Must(template.New("html").Parse(htmlTemplate))
    if err := tmpl.Execute(f, logData); err != nil {
        log.Fatalf("execute template: %v", err)
    }
    log.Printf("wrote %s", *output)
}

