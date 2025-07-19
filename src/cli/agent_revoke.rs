use clap::Parser;

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
pub struct AgentRevokeArgs {
    /// Agent ID to revoke
    #[clap(short, long, value_parser)]
    pub id: String,
    /// Reason for revocation
    #[clap(short, long, value_parser, default_value = "No reason provided")]
    pub reason: String,
}

pub fn run_agent_revoke(args: AgentRevokeArgs) {
    println!("Revoking agent: {}", args.id);
    println!("Reason: {}", args.reason);
    // TODO: Implement agent revocation logic
}
