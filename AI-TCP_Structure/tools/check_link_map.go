package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strings"
)

type entry struct {
	YAML    string `json:"yaml"`
	Mermaid string `json:"mermaid"`
	HTML    string `json:"html"`
	Missing bool   `json:"missing"`
}

func main() {
	linkMapPath := flag.String("map", "link_map.json", "path to link_map.json")
	graphDir := flag.String("graph", "graph", "path to graph directory")
	flag.Parse()

	data, err := os.ReadFile(*linkMapPath)
	if err != nil {
		log.Fatalf("failed to read %s: %v", *linkMapPath, err)
	}
	entries := make(map[string]entry)
	if err := json.Unmarshal(data, &entries); err != nil {
		log.Fatalf("failed to parse json: %v", err)
	}

	// Check for missing files referenced in link_map.json
	hasIssue := false
	for id, e := range entries {
		if e.Mermaid == "" {
			fmt.Printf("[Missing File] mermaid path empty for %s\n", id)
			hasIssue = true
			continue
		}
		if _, err := os.Stat(e.Mermaid); err != nil {
			fmt.Printf("[Missing File] %s\n", e.Mermaid)
			hasIssue = true
		}
	}

	// Collect IDs from link_map.json
	defined := make(map[string]struct{}, len(entries))
	for id := range entries {
		defined[id] = struct{}{}
	}

	// Check graph directory for extra files
	files, err := filepath.Glob(filepath.Join(*graphDir, "*.mmd.md"))
	if err != nil {
		log.Fatalf("glob graph: %v", err)
	}
	for _, f := range files {
		name := filepath.Base(f)
		id := strings.TrimSuffix(name, ".mmd.md")
		if _, ok := defined[id]; !ok {
			fmt.Printf("[Extra File] %s\n", f)
			hasIssue = true
		}
	}

	if !hasIssue {
		fmt.Println("[OK]")
	}
}
