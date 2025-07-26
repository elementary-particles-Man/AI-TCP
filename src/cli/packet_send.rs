use clap::Parser;

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
pub struct PacketSendArgs {
    /// Agent ID for signing the packet
    #[clap(short, long, value_parser)]
    pub agent_id: String,
    /// Destination address
    #[clap(short, long, value_parser)]
    pub destination: String,
    /// Payload data (string or file path)
    #[clap(short, long, value_parser)]
    pub data: String,
    /// Send as JSON instead of FlatBuffers binary
    #[clap(long)]
    pub json: bool,
}

pub fn run_packet_send(args: PacketSendArgs) {
    println!("Sending packet from agent: {}", args.agent_id);
    println!("To: {}", args.destination);
    println!("Data: {}", args.data);
    if args.json {
        println!("Format: JSON");
    } else {
        println!("Format: FlatBuffers Binary");
    }
    use ai_tcp_utils::packet::{build_packet, serialize_packet, deserialize_packet, PacketError};
}
