use axum::{response::IntoResponse, routing::post, Json, Router};
use serde::{Deserialize, Serialize};
use std::net::SocketAddr;
use bytes::Bytes;

// KAIROコアライブラリをインポート
// このパスはKAIRO側のlib.rsの定義に依存する
use kairo_core::packet_parser::PacketParser;
use kairo_core::error::KairoError;

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
    let mut parser = PacketParser::new(vec![0; 32]); // セッションキーはダミー

    match parser.parse(&body) {
        Ok(_packet) => {
            // パケットの検証・復号に成功
            // TODO: 復号されたペイロードに対する処理を実装
            // let uuid = inner_packet.uuid();
            let response = ApiResponse {
                transaction_id: "parsed-transaction-id".to_string(), // 仮のID
                status: "Processed by KAIRO".to_string(),
                error: None,
            };
            (axum::http::StatusCode::OK, Json(response)).into_response()
        }
        Err(e) => {
            eprintln!("Packet parsing failed: {:?}", e);
            let response = ApiResponse {
                transaction_id: "".to_string(),
                status: "Error".to_string(),
                error: Some(format!("Packet processing error: {:?}", e)),
            };
            (axum::http::StatusCode::BAD_REQUEST, Json(response)).into_response()
        }
    }
}

#[tokio::main]
async fn main() {
    let app = Router::new().route("/api/v1/aitcp", post(aitcp_handler));

    let addr = SocketAddr::from(([127, 0, 0, 1], 3000));
    println!("AI-TCP API server with KAIRO integration listening on {}", addr);

    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}