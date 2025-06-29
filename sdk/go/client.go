package aitcp

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"time"
)

const ( 
	apiEndpoint = "/api/v1/aitcp"
)

// Client represents the AI-TCP client.
type Client struct {
	host       string
	apiKey     string
	httpClient *http.Client
}

// Config holds the configuration for the AI-TCP client.
type Config struct {
	Host    string
	APIKey  string
	Timeout time.Duration
}

// TODO: Define a more specific response structure.
type SendResponse struct {
	TransactionID string `json:"transaction_id"`
	Status        string `json:"status"`
}

// NewClient creates a new AI-TCP client.
func NewClient(cfg Config) (*Client, error) {
	if cfg.Host == "" || cfg.APIKey == "" {
		return nil, errors.New("host and apiKey are required")
	}
	return &Client{
		host:   cfg.Host,
		apiKey: cfg.APIKey,
		httpClient: &http.Client{
			Timeout: cfg.Timeout,
		},
	},
	nil
}

// Send sends a single payload and waits for a response.
func (c *Client) Send(ctx context.Context, payload interface{}) (*SendResponse, error) {
	// TODO: This is a stub.
	// 1. Get/reuse a secure session.
	// 2. Serialize payload to InnerPacket (FlatBuffers).
	// 3. This serialized data would be sent to the KAIRO core (Rust) for compression, encryption, and signing.
	// 4. For now, we just marshal the payload to JSON and send it.

	jsonPayload, err := json.Marshal(payload)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal payload: %w", err)
	}

	req, err := http.NewRequestWithContext(ctx, "POST", c.host+apiEndpoint, bytes.NewBuffer(jsonPayload))
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("X-API-Key", c.apiKey)

	res, err := c.httpClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("failed to send request: %w", err)
	}
	defer res.Body.Close()

	if res.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("server returned non-OK status: %s", res.Status)
	}

	var sendResponse SendResponse
	if err := json.NewDecoder(res.Body).Decode(&sendResponse); err != nil {
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	return &sendResponse, nil
}

// Stream is a placeholder for the streaming implementation.
func (c *Client) Stream(ctx context.Context) (<-chan []byte, error) {
	// TODO: Implement streaming logic (e.g., WebSockets, gRPC streams)
	return nil, errors.New("streaming not yet implemented")
}
