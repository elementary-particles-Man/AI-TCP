use clap::Parser;

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
pub struct PacketLogArgs {
    /// Path to the log file
    #[clap(short, long, value_parser)]
    pub log_file: String,
    /// Display log entries in detail
    #[clap(short, long)]
    pub verbose: bool,
}

pub fn run_packet_log(args: PacketLogArgs) {
    println!("Reading log file: {}", args.log_file);
    if args.verbose {
        println!("Displaying in verbose mode.");
    }
    // TODO: Implement log reading and display logic
}
