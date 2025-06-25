package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"regexp"
	"strings"

	"gopkg.in/yaml.v3"
)

func loadLabels(path string) (map[string]string, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	var root struct {
		Semantics struct {
			Labels map[string]string `yaml:"labels"`
		} `yaml:"semantics"`
	}
	if err := yaml.Unmarshal(data, &root); err != nil {
		return nil, err
	}
	return root.Semantics.Labels, nil
}

func main() {
	flag.Usage = func() {
		fmt.Fprintf(flag.CommandLine.Output(), "Usage: %s <intent.yaml> <input.mmd.md> <output.mmd.md>\n", os.Args[0])
		flag.PrintDefaults()
	}
	flag.Parse()
	if flag.NArg() < 3 {
		flag.Usage()
		os.Exit(1)
	}
	yamlPath := flag.Arg(0)
	inPath := flag.Arg(1)
	outPath := flag.Arg(2)

	labels, err := loadLabels(yamlPath)
	if err != nil {
		log.Fatalf("load labels: %v", err)
	}

	data, err := os.ReadFile(inPath)
	if err != nil {
		log.Fatalf("read mermaid: %v", err)
	}
	lines := regexp.MustCompile("\r?\n").Split(string(data), -1)
	nodeRe := regexp.MustCompile(`^(\s*)([A-Za-z0-9_]+)\[\"([^\"]*)\"\](.*)`)

	for i, line := range lines {
		m := nodeRe.FindStringSubmatch(line)
		if len(m) == 0 {
			continue
		}
		id := m[2]
		if lbl, ok := labels[id]; ok && lbl != "" {
			lines[i] = fmt.Sprintf("%s%s[\"%s\"]%s", m[1], id, lbl, m[4])
		}
	}

	if err := os.MkdirAll(filepath.Dir(outPath), 0755); err != nil {
		log.Fatalf("mkdir: %v", err)
	}
	if err := os.WriteFile(outPath, []byte(strings.Join(lines, "\n")), 0644); err != nil {
		log.Fatalf("write: %v", err)
	}
	fmt.Printf("✅ Labeled graph saved: %s\n", outPath)
}
