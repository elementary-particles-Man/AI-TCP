package main

import (
	"flag"
	"fmt"
	"io/fs"
	"log"
	"os"
	"path/filepath"
	"sort"
	"strings"
)

func sanitize(path string) string {
	s := strings.ReplaceAll(path, string(os.PathSeparator), "_")
	s = strings.ReplaceAll(s, ".", "_")
	s = strings.ReplaceAll(s, "-", "_")
	return s
}

func main() {
	flag.Usage = func() {
		fmt.Fprintf(flag.CommandLine.Output(), "Usage: %s <root_dir> <output_file>\n", os.Args[0])
		flag.PrintDefaults()
	}
	flag.Parse()
	if flag.NArg() < 2 {
		flag.Usage()
		os.Exit(1)
	}
	rootDir := flag.Arg(0)
	outputFile := flag.Arg(1)

	var entries []struct {
		rel   string
		isDir bool
	}

	if err := filepath.WalkDir(rootDir, func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			return err
		}
		if path == rootDir {
			return nil
		}
		rel, err := filepath.Rel(rootDir, path)
		if err != nil {
			return err
		}
		entries = append(entries, struct {
			rel   string
			isDir bool
		}{rel: rel, isDir: d.IsDir()})
		return nil
	}); err != nil {
		log.Fatalf("walk: %v", err)
	}

	sort.Slice(entries, func(i, j int) bool { return entries[i].rel < entries[j].rel })

	nodeSet := make(map[string]string)
	edges := []string{}
	rootID := "root"
	nodeSet[rootID] = fmt.Sprintf("%s[\"%s\"]", rootID, filepath.Base(rootDir))

	for _, e := range entries {
		id := sanitize(e.rel)
		label := filepath.Base(e.rel)
		if e.isDir {
			label += "/"
		} else {
			lower := strings.ToLower(label)
			switch {
			case strings.HasSuffix(lower, ".yaml") || strings.HasSuffix(lower, ".yml"):
				label = "YAML: " + label
			case strings.HasSuffix(lower, ".mmd.md") || strings.HasSuffix(lower, ".mmd"):
				label = "Mermaid: " + label
			case strings.HasSuffix(lower, ".md"):
				label = "MD: " + label
			}
		}
		nodeSet[id] = fmt.Sprintf("%s[\"%s\"]", id, label)

		parent := filepath.Dir(e.rel)
		parentID := rootID
		if parent != "." {
			parentID = sanitize(parent)
		}
		edges = append(edges, fmt.Sprintf("    %s --> %s", parentID, id))
	}

	nodes := make([]string, 0, len(nodeSet))
	for _, v := range nodeSet {
		nodes = append(nodes, "    "+v)
	}
	sort.Strings(nodes)

	lines := []string{"```mermaid", "graph TD"}
	lines = append(lines, nodes...)
	lines = append(lines, edges...)
	lines = append(lines, "```")

	if err := os.MkdirAll(filepath.Dir(outputFile), 0755); err != nil {
		log.Fatalf("mkdir: %v", err)
	}
	if err := os.WriteFile(outputFile, []byte(strings.Join(lines, "\n")), 0644); err != nil {
		log.Fatalf("write: %v", err)
	}
	fmt.Printf("Generated %s\n", outputFile)
}
