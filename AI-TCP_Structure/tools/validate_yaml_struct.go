package main

import (
    "flag"
    "fmt"
    "log"
    "os"
    "gopkg.in/yaml.v3"
)

type Agent struct {
    ID     string   `yaml:"id"`
    Name   string   `yaml:"name"`
    Role   string   `yaml:"role"`
    Objectives []string `yaml:"objectives"`
    Constraints []string `yaml:"constraints"`
}

func validateFile(path string) error {
    data, err := os.ReadFile(path)
    if err != nil {
        return err
    }
    var a Agent
    if err := yaml.Unmarshal(data, &a); err != nil {
        return err
    }
    if a.ID == "" || a.Name == "" || a.Role == "" {
        return fmt.Errorf("missing required fields")
    }
    return nil
}

func main() {
    flag.Parse()
    if flag.NArg() == 0 {
        log.Fatal("provide yaml files to validate")
    }
    for _, f := range flag.Args() {
        if err := validateFile(f); err != nil {
            log.Printf("%s: invalid (%v)", f, err)
        } else {
            log.Printf("%s: OK", f)
        }
    }
}

