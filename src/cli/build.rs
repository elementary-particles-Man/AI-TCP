extern crate flatbuffers_build;

use flatbuffers_build::BuilderOptions;
use std::env;
use std::path::PathBuf;

fn main() {
    let flatc_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("..").join("..").join("KAIRO");
    let flatc_path = flatc_dir.canonicalize().unwrap();
    
    // Add the directory containing flatc to the PATH for the build script
    let path_env = env::var_os("PATH").unwrap_or_default();
    let mut paths = env::split_paths(&path_env).collect::<Vec<_>>();
    paths.push(flatc_path);
    env::set_var("PATH", env::join_paths(paths).unwrap());

    BuilderOptions::new_with_files(&["../../KAIRO/schema/ai_tcp_packet.fbs", "../../KAIRO/schema/ephemeral_session.fbs"])
        .compile()
        .expect("flatbuffer compilation failed");
}