package main

import (
    "fmt"
    "gopkg.in/yaml.v3"
    "io/ioutil"
    "log"
    "os"
)

type Component struct {
    ID    string `yaml:"id"`
    Type  string `yaml:"type"`
    Label string `yaml:"label"`
    Name  string `yaml:"name"`
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

func main() {
    if len(os.Args) < 2 {
        log.Fatal("Usage: go run check_semantics.go <path-to-yaml>")
    }

    path := os.Args[1]
    fmt.Printf("Checking %s\n", path)

    data, err := ioutil.ReadFile(path)
    if err != nil {
        log.Fatalf("Failed to read file: %v", err)
    }

    var intent Intent
    err = yaml.Unmarshal(data, &intent)
    if err != nil {
        log.Fatalf("Failed to parse YAML: %v", err)
    }

    compMap := make(map[string]Component)
    for _, c := range intent.Components {
        compMap[c.ID] = c
    }

    for i, conn := range intent.Connections {
        if _, ok := compMap[conn.From]; !ok {
            log.Printf("ERROR %s: connection %d has unknown 'from' component '%s'", path, i+1, conn.From)
        }

        if toComp, ok := compMap[conn.To]; ok {
            if toComp.Type == "source" {
                log.Printf("ERROR %s: connection %d uses 'to' with source component '%s'", path, i+1, conn.To)
            }
        } else {
            log.Printf("ERROR %s: connection %d has unknown 'to' component '%s'", path, i+1, conn.To)
        }
    }
}
