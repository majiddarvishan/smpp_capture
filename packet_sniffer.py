from scapy.all import AsyncSniffer, IP, TCP, Raw
import threading
from smpp_parser import parse_submit_sm, parse_submit_sm_resp, parse_deliver_sm, parse_deliver_sm_resp
from elasticsearch_client import store_in_elasticsearch, update_command_status
from config import SMPP_PORT

packet_queue = queue.Queue()
num_worker_threads = 4  # Adjust based on CPU cores

def process_packet_worker():
    """Worker function to process packets in parallel."""
    while True:
        packet = packet_queue.get()
        if packet is None:
            break  # Exit thread

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

        packet_queue.task_done()

def process_packet(packet):
    """Puts packets in queue for multi-threaded processing."""
    if IP in packet and TCP in packet and packet.haslayer(Raw):
        packet_queue.put(packet)

def start_live_capture():
    """Starts real-time SMPP traffic capture with multi-threaded processing."""
    print("🔴 Capturing SMPP traffic in real-time...")

    # Start worker threads
    for _ in range(num_worker_threads):
        threading.Thread(target=process_packet_worker, daemon=True).start()

    sniffer = AsyncSniffer(filter=f"tcp port {SMPP_PORT}", prn=process_packet, store=False)
    sniffer.start()
