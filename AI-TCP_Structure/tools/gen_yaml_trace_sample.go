package main

import (
    "bufio"
    "flag"
    "fmt"
    "log"
    "os"
    "path/filepath"
    "strings"

    "gopkg.in/yaml.v3"
)

// Message represents a single dialogue line
type Message struct {
    Speaker string `yaml:"speaker"`
    Text    string `yaml:"text"`
}

// Log represents a negotiation log
type Log struct {
    ID       string    `yaml:"id"`
    Messages []Message `yaml:"messages"`
}

func main() {
    input := flag.String("input", "dialogue_sample.txt", "input dialogue text")
    output := flag.String("output", filepath.Join("yaml_logs", "log_test_case_001.yaml"), "output yaml log")
    flag.Parse()

    f, err := os.Open(*input)
    if err != nil {
        log.Fatalf("failed to open input: %v", err)
    }
    defer f.Close()

    var msgs []Message
    scanner := bufio.NewScanner(f)
    for scanner.Scan() {
        line := scanner.Text()
        if len(line) == 0 {
            continue
        }
        var speaker, text string
        n, err := fmt.Sscanf(line, "%[^:]: %s", &speaker, &text)
        if err != nil || n < 2 {
            parts := strings.SplitN(line, ":", 2)
            if len(parts) == 2 {
                speaker = strings.TrimSpace(parts[0])
                text = strings.TrimSpace(parts[1])
            } else {
                log.Printf("skip malformed line: %s", line)
                continue
            }
        }
        msgs = append(msgs, Message{Speaker: speaker, Text: text})
    }
    if err := scanner.Err(); err != nil {
        log.Fatalf("scan input: %v", err)
    }

    logData := Log{ID: "log_test_case_001", Messages: msgs}

    if err := os.MkdirAll(filepath.Dir(*output), 0755); err != nil {
        log.Fatalf("make dir: %v", err)
    }
    outFile, err := os.Create(*output)
    if err != nil {
        log.Fatalf("create output: %v", err)
    }
    defer outFile.Close()

    enc := yaml.NewEncoder(outFile)
    enc.SetIndent(2)
    if err := enc.Encode(logData); err != nil {
        log.Fatalf("encode yaml: %v", err)
    }
    log.Printf("wrote %s", *output)
}

