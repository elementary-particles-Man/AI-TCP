// gen_link_map.go generates a JSON map linking YAML, Mermaid and HTML files.
//
// Usage:
//   go run gen_link_map.go <yaml_dir> <html_dir> <graph_dir> <output.json>
// Example:
//   go run gen_link_map.go ../yaml ../html_logs ../graph ../link_map/map.json

package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strings"
)

type entry struct {
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
	if len(os.Args) < 5 {
		log.Fatalf("Usage: %s <yaml_dir> <html_dir> <graph_dir> <output.json>\n", os.Args[0])
	}
	yamlDir := os.Args[1]
	htmlDir := os.Args[2]
	graphDir := os.Args[3]
	outFile := os.Args[4]

	entries := make(map[string]entry)

	files, err := filepath.Glob(filepath.Join(yamlDir, "*.yaml"))
	if err != nil {
		log.Fatalf("glob yaml: %v", err)
	}

	for _, yf := range files {
		id, err := readID(yf)
		if err != nil {
			log.Printf("warning: %v", err)
			continue
		}
		e := entry{YAML: filepath.ToSlash(yf)}

		mPath := filepath.Join(graphDir, id+".mmd")
		if _, err := os.Stat(mPath); err == nil {
			e.Mermaid = filepath.ToSlash(mPath)
		} else {
			e.Missing = true
		}

		hPath := filepath.Join(htmlDir, id+".html")
		if _, err := os.Stat(hPath); err == nil {
			e.HTML = filepath.ToSlash(hPath)
		} else {
			e.Missing = true
		}

		entries[id] = e
	}

	if err := os.MkdirAll(filepath.Dir(outFile), 0755); err != nil {
		log.Fatalf("create dir: %v", err)
	}

	data, err := json.MarshalIndent(entries, "", "  ")
	if err != nil {
		log.Fatalf("marshal: %v", err)
	}
	if err := os.WriteFile(outFile, data, 0644); err != nil {
		log.Fatalf("write: %v", err)
	}
	fmt.Printf("Wrote %s\n", outFile)
}
