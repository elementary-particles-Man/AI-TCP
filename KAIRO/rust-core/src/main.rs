// Main entry point for the KAIRO Coordination Node.
// This node is responsible for self-governed node registration, key exchange, and virtual IP allocation.

mod coordination;

#[tokio::main]
async fn main() {
    println!("KAIRO Coordination Node starting...");

    // TODO: Initialize logging.

    // Start the API server.
    let routes = coordination::api::register_route(); // Add other routes as they are implemented.

    warp::serve(routes)
        .run(([127, 0, 0, 1], 3030))
        .await;

    println!("KAIRO Coordination Node stopped.");
}
