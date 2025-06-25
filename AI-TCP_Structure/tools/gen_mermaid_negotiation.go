package main

import (
    "flag"
    "fmt"
    "log"
    "os"
    "path/filepath"
    "strings"

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

func main() {
    input := flag.String("input", filepath.Join("yaml_logs", "log_test_case_001.yaml"), "input yaml log")
    output := flag.String("output", filepath.Join("negotiation_logs", "negotiation_test.mmd.md"), "output mermaid file")
    flag.Parse()

    data, err := os.ReadFile(*input)
    if err != nil {
        log.Fatalf("read input: %v", err)
    }
    var logData Log
    if err := yaml.Unmarshal(data, &logData); err != nil {
        log.Fatalf("unmarshal yaml: %v", err)
    }

    var mmd strings.Builder
    mmd.WriteString("graph TD\n")
    for i, msg := range logData.Messages {
        nodeID := fmt.Sprintf("n%d", i)
        label := fmt.Sprintf("%s: %s", msg.Speaker, msg.Text)
        mmd.WriteString(fmt.Sprintf("    %s[\"%s\"]\n", nodeID, label))
        if i > 0 {
            prev := fmt.Sprintf("n%d", i-1)
            mmd.WriteString(fmt.Sprintf("    %s --> %s\n", prev, nodeID))
        }
    }

    if err := os.MkdirAll(filepath.Dir(*output), 0755); err != nil {
        log.Fatalf("make dir: %v", err)
    }
    if err := os.WriteFile(*output, []byte(mmd.String()), 0644); err != nil {
        log.Fatalf("write output: %v", err)
    }
    log.Printf("wrote %s", *output)
}

