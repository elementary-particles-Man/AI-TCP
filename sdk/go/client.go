package aitcp

import (
    "bytes"
    "context"
    "encoding/json"
    "errors"
    "fmt"
    "net/http"
    "time"
    // "[path_to_kairo_rust_ffi]" // CGO経由でKAIROのRustコアをインポートする想定
)

// Client represents a connection to the AI-TCP network.
type Client struct {
    host       string
    apiKey     string
    httpClient *http.Client
    // kairoSession *kairo.Session // KAIROセッション管理用
}

// Config holds the configuration for the AI-TCP client.
type Config struct {
    Host    string
    APIKey  string
    Timeout time.Duration
}

// SendResponse defines the structure for the API response.
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
        // kairoSession: kairo.NewSession(), // KAIROセッションの初期化
    }, nil
}

// Send sends a single payload and waits for a response.
func (c *Client) Send(ctx context.Context, payload interface{}) (*SendResponse, error) {
    // 1. (Go) アプリケーションのペイロードをInnerPacket用のバイト列にシリアライズする
    //    例: JSON, Protobuf, or other formats
    innerPayloadBytes, err := json.Marshal(payload)
    if err != nil {
        return nil, err
    }

    // 2. (Go -> Rust) シリアライズされたペイロードをKAIROのRustコアに渡す
    //    Rustコアが以下の処理を全て実行する:
    //    a. InnerPacketをFlatBuffersで構築
    //    b. ペイロードをLZ4で圧縮
    //    c. InnerPacket全体をChaCha20-Poly1305で暗号化
    //    d. 最終的なAiTcpPacketをEd25519で署名
    //
    // aiTcpPacketBinary, err := kairo.BuildAndProtectPacket(c.kairoSession, innerPayloadBytes)
    // if err != nil {
    //     return nil, err
    // }
    
    // --- 現段階でのスタブ実装 ---
    // 上記のRust連携が実装されるまで、APIサーバーへのJSON送信を維持
    req, err := http.NewRequestWithContext(ctx, "POST", c.host+"/api/v1/aitcp", bytes.NewBuffer(innerPayloadBytes))
    if err != nil {
        return nil, err
    }

    req.Header.Set("Content-Type", "application/json")
    req.Header.Set("X-API-Key", c.apiKey)

    resp, err := c.httpClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    if resp.StatusCode != http.StatusOK {
        return nil, errors.New(fmt.Sprintf("API server returned non-OK status: %s", resp.Status))
    }

    var sendResponse SendResponse
    if err := json.NewDecoder(resp.Body).Decode(&sendResponse); err != nil {
        return nil, err
    }

    return &sendResponse, nil
}

// Stream is a placeholder for the streaming implementation.
func (c *Client) Stream(ctx context.Context) (<-chan []byte, error) {
    // TODO: ストリーミングロジックを実装
    return nil, errors.New("streaming not yet implemented")
}