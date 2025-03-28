import argparse
from packet_sniffer import start_live_capture
from pcap_reader import process_pcap_file

def main():
    parser = argparse.ArgumentParser(description="SMPP Submit_SM Packet Analyzer")
    parser.add_argument("--mode", choices=["live", "pcap"], required=True, help="Run mode: 'live' for real-time capture, 'pcap' to read from a file")
    parser.add_argument("--file", type=str, help="PCAP file path (required if mode=pcap)")

    args = parser.parse_args()

    if args.mode == "live":
        print("🔴 Starting Live Capture...")
        start_live_capture()
    elif args.mode == "pcap":
        if not args.file:
            print("❌ Error: Please provide a PCAP file path with --file")
            return
        process_pcap_file(args.file)

if __name__ == "__main__":
    main()
