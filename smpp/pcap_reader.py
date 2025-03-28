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
from smpp.packet_parser import parse_submit_sm, parse_submit_sm_resp, parse_deliver_sm, parse_deliver_sm_resp
from kafka.kafka_producer import send_to_kafka

def process_pcap_file(pcap_file):
    """Efficiently processes a PCAP file using a streaming approach."""
    print(f"📂 Reading from PCAP file: {pcap_file}")

    with PcapReader(pcap_file) as packets:
        for packet in packets:
            if IP in packet and TCP in packet and packet.haslayer(Raw):
                raw_data = memoryview(packet[Raw].load)  # Zero-copy optimization

                sm_data = parse_submit_sm(raw_data)
                if sm_data:
                    send_to_kafka("smpp-submit", sm_data)

                sm_resp_data = parse_submit_sm_resp(raw_data)
                if sm_resp_data:
                    send_to_kafka("smpp-response", sm_resp_data)

                deliver_data = parse_deliver_sm(raw_data)
                if deliver_data:
                    send_to_kafka("smpp-deliver", deliver_data)

    print("✅ Finished processing PCAP file efficiently.")

