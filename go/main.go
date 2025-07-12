package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
)

type APIRequest struct {
	TaskID  string `json:"task_id"`
	Payload string `json:"payload"`
}

type APIResponse struct {
	Status           string `json:"status"`
	ReceivedTaskID   string `json:"received_task_id"`
	ProcessedPayload string `json:"processed_payload"`
}

func apiHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		http.Error(w, `{"status":"error","message":"Invalid request method"}`, http.StatusMethodNotAllowed)
		return
	}

	var req APIRequest
	decoder := json.NewDecoder(r.Body)
	err := decoder.Decode(&req)
	if err != nil {
		http.Error(w, `{"status":"error","message":"Invalid JSON payload"}`, http.StatusBadRequest)
		return
	}

	resp := APIResponse{
		Status:           "success",
		ReceivedTaskID:   req.TaskID,
		ProcessedPayload: req.Payload,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

func main() {
	http.HandleFunc("/api", apiHandler)
	fmt.Println("Starting server on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
