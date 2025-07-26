use clap::Parser;

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
pub struct PacketReceiveArgs {
    /// Port to listen on
    #[clap(short, long, value_parser, default_value_t = 8080)]
    pub port: u16,
    /// Receive as JSON instead of FlatBuffers binary
    #[clap(long)]
    pub json: bool,
}

pub fn run_packet_receive(args: PacketReceiveArgs) {
    println!("Listening for packets on port: {}", args.port);
    if args.json {
        println!("Expecting: JSON");
    } else {
        println!("Expecting: FlatBuffers Binary");
    }
    use ai_tcp_utils::packet::{deserialize_packet, PacketError};
}
