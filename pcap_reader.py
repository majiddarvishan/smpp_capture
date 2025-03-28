# from scapy.all import rdpcap, IP, TCP, Raw
# from smpp_parser import (
#     parse_submit_sm, parse_submit_sm_resp,
#     parse_deliver_sm, parse_deliver_sm_resp
# )
# from elasticsearch_client import store_in_elasticsearch, update_command_status

# def process_pcap_file(pcap_file):
#     """Reads packets from a PCAP file and processes all SMPP packets."""
#     print(f"📂 Reading from PCAP file: {pcap_file}")
#     packets = rdpcap(pcap_file)

#     for packet in packets:
#         if IP in packet and TCP in packet and packet.haslayer(Raw):
#             raw_data = packet[Raw].load

#             for parser in [parse_submit_sm, parse_deliver_sm]:
#                 sm_data = parser(raw_data)
#                 if sm_data:
#                     store_in_elasticsearch(sm_data)
#                     continue

#             for parser in [parse_submit_sm_resp, parse_deliver_sm_resp]:
#                 sm_resp_data = parser(raw_data)
#                 if sm_resp_data:
#                     update_command_status(
#                         sm_resp_data["sequence_number"],
#                         sm_resp_data["command_status"],
#                         sm_resp_data["response_time_ms"],
#                         sm_resp_data["message_type"]
#                     )

#     print("✅ Finished processing PCAP file.")

from scapy.all import PcapReader, IP, TCP, Raw
from smpp_parser import parse_submit_sm, parse_submit_sm_resp, parse_deliver_sm, parse_deliver_sm_resp
from elasticsearch_client import store_in_elasticsearch, update_command_status

def process_pcap_file(pcap_file):
    """Efficiently processes PCAP files using a streaming approach."""
    print(f"📂 Reading from PCAP file: {pcap_file}")

    with PcapReader(pcap_file) as packets:
        for packet in packets:
            if IP in packet and TCP in packet and packet.haslayer(Raw):
                raw_data = memoryview(packet[Raw].load)  # Zero-copy optimization

                for parser in [parse_submit_sm, parse_deliver_sm]:
                    sm_data = parser(raw_data)
                    if sm_data:
                        store_in_elasticsearch(sm_data)

                for parser in [parse_submit_sm_resp, parse_deliver_sm_resp]:
                    sm_resp_data = parser(raw_data)
                    if sm_resp_data:
                        update_command_status(
                            sm_resp_data["sequence_number"],
                            sm_resp_data["command_status"],
                            sm_resp_data["response_time_ms"],
                            sm_resp_data["message_type"]
                        )

    print("✅ Finished processing PCAP file efficiently.")
