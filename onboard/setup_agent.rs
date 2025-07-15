//! setup_agent.rs
//! CUI for first-time onboarding to the KAIRO Mesh.

use std::fs;
use ed25519_dalek::{Keypair, Signature, Signer};
use rand::rngs::OsRng;
use std::io::Write;

fn main() {
    println!("--- KAIRO Mesh Initial Setup ---");

    println!("\nStep 1: Generating Static ID (Key Pair)...");
    let mut csprng = OsRng {};
    let keypair: Keypair = Keypair::generate(&mut csprng);

    let pub_key = hex::encode(keypair.public);
    let priv_key = hex::encode(keypair.secret);

    println!("-> Key Pair generated.");

    fs::create_dir_all("key").unwrap();
    let mut pub_file = fs::File::create("key/public.key").unwrap();
    pub_file.write_all(pub_key.as_bytes()).unwrap();

    let mut priv_file = fs::File::create("key/private.key").unwrap();
    priv_file.write_all(priv_key.as_bytes()).unwrap();

    println!("\nStep 2: Registering with a Seed Node...");
    // TODO: Load seeds from seeds.yml and send a simulated registration.
    println!("-> Registration request sent (simulated).");

    fs::create_dir_all("log").unwrap();
    let mut log_file = fs::OpenOptions::new().append(true).create(true).open("log/onboarding.log").unwrap();
    writeln!(log_file, "Onboarding at {:?} | PublicKey: {}", chrono::Utc::now(), pub_key).unwrap();

    println!("\n--- Onboarding Complete ---");
    println!("Your Mesh Address (Public Key): {}", pub_key);
    println!("Your Agent Token (Private Key): {}", priv_key);

    println!("\nIMPORTANT: Keep your Agent Token secure. It will not be shown again.");
    println!("You can now use this token to launch your AI-TCP instance.");
}
