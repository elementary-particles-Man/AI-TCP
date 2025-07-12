package main

import (
	"encoding/json"
	"log"
	"net/http"
)

// APIRequest defines the expected structure of the incoming JSON payload.
type APIRequest struct {
	TaskID  string `json:"task_id"`
	Payload string `json:"payload"`
}

// APIResponse defines the structure of a successful response.
type APIResponse struct {
	Status           string `json:"status"`
	ReceivedTaskID   string `json:"received_task_id"`
	ProcessedPayload string `json:"processed_payload"`
}

// ErrorResponse defines the structure for error messages.
type ErrorResponse struct {
	Status string `json:"status"`
	Error  string `json:"error"`
}

func apiHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	if r.Method != http.MethodPost {
		w.WriteHeader(http.StatusMethodNotAllowed)
		json.NewEncoder(w).Encode(ErrorResponse{Status: "error", Error: "method not allowed"})
		return
	}

	var req APIRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(ErrorResponse{Status: "error", Error: "invalid JSON"})
		return
	}

	if req.TaskID == "" || req.Payload == "" {
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(ErrorResponse{Status: "error", Error: "task_id and payload are required"})
		return
	}

	resp := APIResponse{
		Status:           "success",
		ReceivedTaskID:   req.TaskID,
		ProcessedPayload: req.Payload,
	}
	json.NewEncoder(w).Encode(resp)
}

func main() {
	http.HandleFunc("/api", apiHandler)
	log.Println("starting server on :8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatalf("server failed: %v", err)
	}
}
