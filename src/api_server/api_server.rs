use axum::{
    routing::post,
    Router,
    Json,
    response::IntoResponse,
};
use serde::{Deserialize, Serialize};
use std::net::SocketAddr;
use bytes::Bytes;

// TODO: KAIROコアクレートをインポート
// use kairo_core::packet_parser::PacketParser;
// use kairo_core::error::KairoError;

// APIが受け取るリクエストのペイロード
#[derive(Deserialize)]
struct ApiRequest {
    payload: serde_json::Value,
}

// APIが返すレスポンス
#[derive(Serialize)]
struct ApiResponse {
    transaction_id: String,
    status: String,
    error: Option<String>,
}

async fn aitcp_handler(body: bytes::Bytes) -> impl IntoResponse {
    println!("Received binary packet of size: {} bytes", body.len());

    // --- KAIRO Integration Point ---
    // let mut parser = PacketParser::new(/* session_key */ vec![0;32]);
    // match parser.parse(&body) {
    //     Ok(inner_packet) => {
    //         // パケットの検証・復号に成功
    //         // ここでペイロードに対する処理を行う
    //         println!("Successfully parsed packet. UUID: {}", inner_packet.uuid());
    //
    //         let response = ApiResponse {
    //             transaction_id: inner_packet.uuid().to_string(),
    //             status: "Processed".to_string(),
    //             error: None,
    //         };
    //         (StatusCode::OK, Json(response)).into_response()
    //     },
    //     Err(e) => {
    //         // パケットの検証・復号に失敗
    //         eprintln!("Packet parsing failed: {:?}", e);
    //         let response = ApiResponse {
    //             transaction_id: "".to_string(), // エラー時はトランザクションIDなし
    //             status: "Error".to_string(),
    //             error: Some(format!("Packet processing error: {:?}", e)),
    //         };
    //         (StatusCode::BAD_REQUEST, Json(response)).into_response()
    //     }
    // }

    // KAIRO統合が完了するまでのスタブレスポンス
    let stub_response = ApiResponse {
        transaction_id: "stub-transaction-id-123".to_string(),
        status: "Received (KAIRO integration pending)".to_string(),
        error: None,
    };
    (axum::http::StatusCode::OK, Json(stub_response))
}

#[tokio::main]
async fn main() {
    let app = Router::new().route("/api/v1/aitcp", post(aitcp_handler));

    let addr = SocketAddr::from(([127, 0, 0, 1], 3000));
    println!("AI-TCP API server listening on {}", addr);

    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}
