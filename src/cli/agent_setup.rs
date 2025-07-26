use clap::Parser;
use ai_tcp_utils::crypto::{generate_keypair, save_agent_config, AgentConfig, CryptoError};
use std::path::Path;

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
pub struct AgentSetupArgs {
    /// Agent ID to register
    #[clap(short, long, value_parser)]
    pub id: String,
    /// Output directory for agent configuration (default: agent_configs/)
    #[clap(short, long, value_parser, default_value = "agent_configs")]
    pub output_dir: String,
}

pub fn run_agent_setup(args: AgentSetupArgs) -> Result<(), CryptoError> {
    println!("Generating keypair for agent: {}", args.id);
    let (public_key, secret_key) = generate_keypair()?;

    let config = AgentConfig {
        id: args.id.clone(),
        public_key,
        secret_key,
    };

    let output_path = Path::new(&args.output_dir).join(format!("{}.json", args.id));
    save_agent_config(&config, &output_path)?;

    println!("Agent {} registered successfully.", args.id);
    println!("Configuration saved to: {}", output_path.display());
    Ok(())
}
