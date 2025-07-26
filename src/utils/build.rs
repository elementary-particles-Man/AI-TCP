extern crate flatbuffers_build;

use flatbuffers_build::BuilderOptions;
use std::env;
use std::path::PathBuf;
use std::process::Command;

fn main() {
    let flatc_path = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("..").join("..").join("KAIRO").join("flatc.exe");
    let flatc_path = flatc_path.canonicalize().unwrap();
    
    // Add the directory containing flatc to the PATH for the build script
    let path_env = env::var_os("PATH").unwrap_or_default();
    let mut paths = env::split_paths(&path_env).collect::<Vec<_>>();
    paths.push(flatc_path.parent().unwrap().to_path_buf()); // flatcの親ディレクトリをPATHに追加
    env::set_var("PATH", env::join_paths(paths).unwrap());

    // flatcの実行パスとバージョンを確認
    let output = Command::new(&flatc_path)
        .arg("--version")
        .output()
        .expect("Failed to execute flatc --version");
    println!("flatc --version stdout: {}", String::from_utf8_lossy(&output.stdout));
    println!("flatc --version stderr: {}", String::from_utf8_lossy(&output.stderr));

    let out_dir = env::var("OUT_DIR").unwrap();
    println!("OUT_DIR: {}", out_dir);
    println!("Expected AITCP path: {}/AITCP/ai_tcp_packet_generated.rs", out_dir);
    println!("Expected aitcp path: {}/aitcp/ephemeral_session_generated.rs", out_dir);

    BuilderOptions::new_with_files(&["../../KAIRO/schema/ai_tcp_packet.fbs", "../../KAIRO/schema/ephemeral_session.fbs"])
        .compile()
        .expect("flatbuffer compilation failed");
}
