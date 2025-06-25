package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strings"

	"gopkg.in/yaml.v3"
)

type Component struct {
	ID   string `yaml:"id"`
	Name string `yaml:"name"`
	Type string `yaml:"type"`
}

type Connection struct {
	From string `yaml:"from"`
	To   string `yaml:"to"`
}

type Intent struct {
	ID          string       `yaml:"id"`
	Name        string       `yaml:"name"`
	Components  []Component  `yaml:"components"`
	Connections []Connection `yaml:"connections"`
}

func parseNode(line string) (id, label, typ string, ok bool) {
	line = strings.TrimSpace(line)
	if line == "" {
		return
	}
	// look for [ or (
	i := strings.IndexAny(line, "[(")
	if i < 0 {
		return
	}
	id = strings.TrimSpace(line[:i])
	closing := byte(']')
	if line[i] == '(' {
		closing = ')'
	}
	j := strings.IndexByte(line[i+1:], closing)
	if j < 0 {
		return
	}
	label = strings.Trim(line[i+1:i+1+j], "\"")
	rest := strings.TrimSpace(line[i+1+j+1:])
	if idx := strings.Index(rest, ":::"); idx >= 0 {
		typ = strings.TrimSpace(rest[idx+3:])
	}
	ok = true
	return
}

func parseEdge(line string) (from, to string, ok bool) {
	line = strings.TrimSpace(line)
	idx := strings.Index(line, "-->")
	if idx < 0 {
		return
	}
	from = strings.TrimSpace(line[:idx])
	rest := strings.TrimSpace(line[idx+3:])
	if strings.HasPrefix(rest, "|") {
		if j := strings.Index(rest[1:], "|"); j >= 0 {
			rest = strings.TrimSpace(rest[j+2:])
		}
	}
	fields := strings.Fields(rest)
	if len(fields) == 0 {
		return
	}
	to = fields[0]
	ok = true
	return
}

func parseMermaid(path string) (*Intent, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()

	nodes := make(map[string]*Component)
	classes := make(map[string]string)
	var conns []Connection

	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" || strings.HasPrefix(line, "```") || strings.HasPrefix(line, "graph") || strings.HasPrefix(line, "classDef") {
			continue
		}
		if strings.HasPrefix(line, "class ") {
			parts := strings.Fields(line)
			if len(parts) >= 3 {
				classes[parts[1]] = parts[2]
				if c, ok := nodes[parts[1]]; ok && c.Type == "" {
					c.Type = parts[2]
				}
			}
			continue
		}
		if strings.Contains(line, "-->") {
			if from, to, ok := parseEdge(line); ok {
				conns = append(conns, Connection{From: from, To: to})
			}
			continue
		}
		if id, label, typ, ok := parseNode(line); ok {
			c := nodes[id]
			if c == nil {
				c = &Component{ID: id}
				nodes[id] = c
			}
			if label != "" {
				c.Name = label
			}
			if typ != "" {
				c.Type = typ
			}
		}
	}
	if err := scanner.Err(); err != nil {
		return nil, err
	}

	for id, typ := range classes {
		if c, ok := nodes[id]; ok {
			if c.Type == "" {
				c.Type = typ
			}
		} else {
			nodes[id] = &Component{ID: id, Name: id, Type: typ}
		}
	}

	comps := make([]Component, 0, len(nodes))
	for _, c := range nodes {
		if c.Name == "" {
			c.Name = c.ID
		}
		comps = append(comps, *c)
	}

	base := filepath.Base(path)
	id := strings.TrimSuffix(base, filepath.Ext(base))
	id = strings.TrimSuffix(id, ".mmd")

	intent := &Intent{
		ID:          id,
		Name:        "Reconstructed Intent",
		Components:  comps,
		Connections: conns,
	}
	return intent, nil
}

func main() {
	if len(os.Args) < 3 {
		log.Fatalf("Usage: %s <input.mmd.md> <output.yaml>\n", os.Args[0])
	}
	inPath := os.Args[1]
	outPath := os.Args[2]

	intent, err := parseMermaid(inPath)
	if err != nil {
		log.Fatalf("parse mermaid: %v", err)
	}

	data, err := yaml.Marshal(intent)
	if err != nil {
		log.Fatalf("marshal yaml: %v", err)
	}

	if err := os.MkdirAll(filepath.Dir(outPath), 0755); err != nil {
		log.Fatalf("mkdir: %v", err)
	}

	if err := os.WriteFile(outPath, data, 0644); err != nil {
		log.Fatalf("write yaml: %v", err)
	}

	fmt.Printf("✅ YAML generated: %s\n", outPath)
}
