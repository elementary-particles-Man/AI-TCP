package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
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

type SecureAPIRequest struct {
	TaskID     string `json:"task_id"`
	Payload    string `json:"payload"`
	SessionKey string `json:"session_key"`
}

type SecureAPIResponse struct {
	Status              string `json:"status"`
	ReceivedTaskID      string `json:"received_task_id"`
	ProcessedPayload    string `json:"processed_payload"`
	ValidatedSessionKey bool   `json:"validated_session_key"`
}

type ErrorResponse struct {
	Status  string `json:"status"`
	Message string `json:"message"`
}

func apiHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Println("--- Request received ---")
	for name, headers := range r.Header {
		for _, h := range headers {
			fmt.Printf("%v: %v\n", name, h)
		}
	}
	fmt.Printf("Method: %s, URL: %s, RemoteAddr: %s\n", r.Method, r.URL, r.RemoteAddr)

	bodyBytes, err := io.ReadAll(r.Body)
	if err != nil {
		log.Printf("Error reading body: %v", err)
		http.Error(w, "can't read body", http.StatusBadRequest)
		return
	}
	r.Body = io.NopCloser(bytes.NewBuffer(bodyBytes))
	fmt.Printf("Request Body: %s\n", string(bodyBytes))

	if r.Method != "POST" {
		http.Error(w, `{"status":"error","message":"Invalid request method"}`, http.StatusMethodNotAllowed)
		return
	}

	var req APIRequest
	decoder := json.NewDecoder(r.Body)
	err = decoder.Decode(&req)
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

func secureAPIHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, `{"status":"error","message":"Invalid request method"}`, http.StatusMethodNotAllowed)
		return
	}

	var req SecureAPIRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, `{"status":"error","message":"Invalid JSON payload"}`, http.StatusBadRequest)
		return
	}

	if len(req.SessionKey) != 32 {
		http.Error(w, `{"status":"error","message":"Invalid session key length"}`, http.StatusBadRequest)
		return
	}

	resp := SecureAPIResponse{
		Status:              "success",
		ReceivedTaskID:      req.TaskID,
		ProcessedPayload:    req.Payload,
		ValidatedSessionKey: true,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

func main() {
	http.HandleFunc("/api", apiHandler)
	http.HandleFunc("/api/secure", secureAPIHandler)
	fmt.Println("Starting server on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
