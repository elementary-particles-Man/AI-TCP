package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strings"
)

type Entry struct {
	YAML    string `json:"yaml"`
	Mermaid string `json:"mermaid,omitempty"`
	HTML    string `json:"html,omitempty"`
	Missing bool   `json:"missing,omitempty"`
}

func readID(path string) (string, error) {
	f, err := os.Open(path)
	if err != nil {
		return "", err
	}
	defer f.Close()
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if strings.HasPrefix(line, "id:") {
			return strings.TrimSpace(strings.TrimPrefix(line, "id:")), nil
		}
	}
	if err := scanner.Err(); err != nil {
		return "", err
	}
	return "", fmt.Errorf("id not found in %s", path)
}

func main() {
	yamlDir := flag.String("yaml", "yaml", "YAML directory")
	mermaidDir := flag.String("mermaid", "mermaid", "Mermaid directory")
	htmlDir := flag.String("html", "html_logs", "HTML logs directory")
	output := flag.String("output", "link_map.json", "Output JSON file")
	flag.Parse()

	entries := make(map[string]Entry)

	yamlFiles, err := filepath.Glob(filepath.Join(*yamlDir, "*.yaml"))
	if err != nil {
		log.Fatalf("glob yaml: %v", err)
	}

	for _, yf := range yamlFiles {
		id, err := readID(yf)
		if err != nil {
			log.Printf("warning: %v", err)
			continue
		}
		e := Entry{YAML: filepath.ToSlash(yf)}

		mermaidPath := filepath.Join(*mermaidDir, id+".mmd.md")
		if _, err := os.Stat(mermaidPath); err == nil {
			e.Mermaid = filepath.ToSlash(mermaidPath)
		} else {
			log.Printf("missing mermaid for %s", id)
			e.Missing = true
		}

		htmlPath := filepath.Join(*htmlDir, id+".html")
		if _, err := os.Stat(htmlPath); err == nil {
			e.HTML = filepath.ToSlash(htmlPath)
		} else {
			log.Printf("missing html for %s", id)
			e.Missing = true
		}

		entries[id] = e
	}

	data, err := json.MarshalIndent(entries, "", "  ")
	if err != nil {
		log.Fatalf("marshal json: %v", err)
	}

	if err := os.WriteFile(*output, data, 0644); err != nil {
		log.Fatalf("write output: %v", err)
	}
	fmt.Printf("Wrote %s\n", *output)
}
