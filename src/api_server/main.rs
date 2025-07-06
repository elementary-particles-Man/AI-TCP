use axum::{extract::DefaultBodyLimit, routing::post, Router, Json, http::StatusCode, response::IntoResponse};
use std::net::SocketAddr;
use serde::Serialize;
use bytes::Bytes;

// KAIROコアライブラリをインポート
// このパスはKAIRO側のlib.rsの定義に依存する
use kairo_rust_core::packet_parser::PacketParser;
use kairo_rust_core::error::KairoError;

// APIが返すレスポンス
#[derive(Serialize)]
struct ApiResponse {
    transaction_id: String,
    status: String,
    error: Option<String>,
}

// ボディとしてバイナリデータ(Bytes)を受け取るように変更
async fn aitcp_handler(body: Bytes) -> impl IntoResponse {
    println!("Received binary packet of size: {} bytes", body.len());

    // --- KAIRO Integration Point ---
    // ここでKAIROのパーサーを呼び出し、パケットを検証する
    let mut parser = packet_parser::PacketParser::new(vec![0; 32]); // セッションキーはダミー

    match parser.parse(&body) {
        Ok(packet) => {
            // パケットの検証・復号に成功
            let response = ApiResponse {
                transaction_id: packet.header.transaction_id,
                status: "success".to_string(),
                error: None,
            };
            (StatusCode::OK, Json(response))
        }
        Err(e) => {
            // エラーが発生
            eprintln!("Packet parsing error: {}", e);
            let response = ApiResponse {
                transaction_id: "".to_string(), // エラー時は空
                status: "error".to_string(),
                error: Some(e.to_string()),
            };
            (StatusCode::BAD_REQUEST, Json(response))
        }
    }
}

#[tokio::main]
async fn main() {
    // axumのルーターを定義
    // パケットサイズの上限を1MBに設定
    // Tゲットであるべき
    // そのため、main関数はここに配置する
    let app = Router::new().route("/api/v1/aitcp", post(aitcp_handler))
        .layer(DefaultBodyLimit::max(1024 * 1024)); // 1MB limit

    let addr = SocketAddr::from(([127, 0, 0, 1], 3000));
    println!("AI-TCP API server with KAIRO integration listening on {}", addr);

    axum::serve(tokio::net::TcpListener::bind(&addr).await.unwrap(), app)
        .await
        .unwrap();
}