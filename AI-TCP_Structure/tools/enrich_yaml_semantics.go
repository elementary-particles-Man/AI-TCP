package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"path/filepath"

	"gopkg.in/yaml.v3"
)

func main() {
	desc := flag.String("description", "", "Semantics description")
	next := flag.String("next", "", "Recommended next intent id")
	outDir := flag.String("out", "enriched_yaml", "Output directory")
	flag.Parse()

	if flag.NArg() < 1 {
		log.Fatalf("Usage: %s <input.yaml> [options]", os.Args[0])
	}
	input := flag.Arg(0)

	data, err := os.ReadFile(input)
	if err != nil {
		log.Fatalf("read input: %v", err)
	}

	m := make(map[string]interface{})
	if err := yaml.Unmarshal(data, &m); err != nil {
		log.Fatalf("parse yaml: %v", err)
	}

	sem, ok := m["semantics"].(map[string]interface{})
	if !ok {
		sem = make(map[string]interface{})
	}
	if *desc != "" {
		sem["description"] = *desc
	}
	if *next != "" {
		sem["recommended_next"] = *next
	}
	if len(sem) > 0 {
		m["semantics"] = sem
	}

	outPath := filepath.Join(*outDir, filepath.Base(input))
	if err := os.MkdirAll(filepath.Dir(outPath), 0755); err != nil {
		log.Fatalf("mkdir: %v", err)
	}
	outData, err := yaml.Marshal(m)
	if err != nil {
		log.Fatalf("marshal: %v", err)
	}
	if err := os.WriteFile(outPath, outData, 0644); err != nil {
		log.Fatalf("write: %v", err)
	}
	fmt.Printf("✅ Enriched YAML saved: %s\n", outPath)
}
