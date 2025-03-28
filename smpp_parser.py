# from struct import unpack

# # Define TLV Parameter Map
# TLV_PARAMETERS = {
#     0x0005: "dest_addr_subunit",
#     0x0006: "dest_network_type",
#     0x0007: "dest_bearer_type",
#     0x0201: "user_message_reference",
#     0x0204: "source_port",
#     0x0205: "destination_port",
#     0x020A: "sar_msg_ref_num",
#     0x020C: "sar_total_segments",
#     0x020D: "sar_segment_seqnum",
#     0x1501: "message_payload",
# }

# def parse_tlv_parameters(payload, offset):
#     """Extracts TLV parameters from the payload."""
#     tlv_data = {}
#     while offset + 4 <= len(payload):
#         tag = unpack(">H", payload[offset:offset+2])[0]
#         length = unpack(">H", payload[offset+2:offset+4])[0]
#         offset += 4
#         if offset + length > len(payload):
#             break
#         value = payload[offset:offset+length]
#         offset += length
#         param_name = TLV_PARAMETERS.get(tag, f"unknown_0x{tag:04X}")
#         tlv_data[param_name] = value.hex() if len(value) > 4 else value.decode(errors="ignore")
#     return tlv_data

# def parse_submit_sm(payload):
#     """Parses an SMPP Submit_SM packet and extracts relevant fields."""
#     try:
#         if len(payload) < 16:
#             return None
#         command_id = unpack(">I", payload[4:8])[0]
#         sequence_number = unpack(">I", payload[12:16])[0]
#         if command_id != 0x00000004:
#             return None

#         offset = 16
#         service_type = payload[offset:offset + payload[offset:].index(b"\x00")].decode()
#         offset += len(service_type) + 1
#         source_addr_ton = payload[offset]
#         source_addr_npi = payload[offset + 1]
#         offset += 2
#         source_addr = payload[offset:offset + payload[offset:].index(b"\x00")].decode()
#         offset += len(source_addr) + 1
#         dest_addr_ton = payload[offset]
#         dest_addr_npi = payload[offset + 1]
#         offset += 2
#         destination_addr = payload[offset:offset + payload[offset:].index(b"\x00")].decode()
#         offset += len(destination_addr) + 1
#         esm_class = payload[offset]
#         data_coding = payload[offset + 7]
#         sm_length = payload[offset + 9]
#         offset += 10
#         short_message = payload[offset:offset + sm_length].decode(errors="ignore")
#         offset += sm_length
#         tlv_data = parse_tlv_parameters(payload, offset)

#         return {
#             "sequence_number": sequence_number,
#             "service_type": service_type,
#             "source_addr": source_addr,
#             "destination_addr": destination_addr,
#             "esm_class": esm_class,
#             "data_coding": data_coding,
#             "short_message": short_message,
#             "tlv_parameters": tlv_data
#         }

#     except Exception as e:
#         print(f"❌ Error parsing Submit_SM: {e}")
#         return None

from struct import unpack
import time

def get_current_time_ms():
    """Returns current time in milliseconds."""
    return int(time.time() * 1000)

def parse_submit_sm(payload):
    """Parses an SMPP Submit_SM packet."""
    try:
        if len(payload) < 16:
            return None
        command_id = unpack(">I", payload[4:8])[0]
        sequence_number = unpack(">I", payload[12:16])[0]

        if command_id != 0x00000004:  # Only process Submit_SM
            return None

        return {
            "sequence_number": sequence_number,
            "command_id": command_id,
            "command_status": None,
            "message_type": "Submit_SM",
            "submit_time_ms": get_current_time_ms(),
            "response_time_ms": None
        }

    except Exception as e:
        print(f"❌ Error parsing Submit_SM: {e}")
        return None

def parse_submit_sm_resp(payload):
    """Parses an SMPP Submit_SM_RESP packet."""
    try:
        if len(payload) < 16:
            return None
        command_id = unpack(">I", payload[4:8])[0]
        command_status = unpack(">I", payload[8:12])[0]
        sequence_number = unpack(">I", payload[12:16])[0]

        if command_id != 0x80000004:  # Submit_SM_RESP ID
            return None

        return {
            "sequence_number": sequence_number,
            "command_status": command_status,
            "message_type": "Submit_SM_RESP",
            "response_time_ms": get_current_time_ms()
        }

    except Exception as e:
        print(f"❌ Error parsing Submit_SM_RESP: {e}")
        return None

def parse_deliver_sm(payload):
    """Parses an SMPP Deliver_SM packet."""
    try:
        if len(payload) < 16:
            return None
        command_id = unpack(">I", payload[4:8])[0]
        sequence_number = unpack(">I", payload[12:16])[0]

        if command_id != 0x00000005:  # Only process Deliver_SM
            return None

        return {
            "sequence_number": sequence_number,
            "command_id": command_id,
            "command_status": None,
            "message_type": "Deliver_SM",
            "submit_time_ms": get_current_time_ms(),
            "response_time_ms": None
        }

    except Exception as e:
        print(f"❌ Error parsing Deliver_SM: {e}")
        return None

def parse_deliver_sm_resp(payload):
    """Parses an SMPP Deliver_SM_RESP packet."""
    try:
        if len(payload) < 16:
            return None
        command_id = unpack(">I", payload[4:8])[0]
        command_status = unpack(">I", payload[8:12])[0]
        sequence_number = unpack(">I", payload[12:16])[0]

        if command_id != 0x80000005:  # Deliver_SM_RESP ID
            return None

        return {
            "sequence_number": sequence_number,
            "command_status": command_status,
            "message_type": "Deliver_SM_RESP",
            "response_time_ms": get_current_time_ms()
        }

    except Exception as e:
        print(f"❌ Error parsing Deliver_SM_RESP: {e}")
        return None
