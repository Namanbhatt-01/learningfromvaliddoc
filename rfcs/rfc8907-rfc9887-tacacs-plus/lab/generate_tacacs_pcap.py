#!/usr/bin/env python3
"""
TACACS+ RFC 8907 Authentic PCAP Generator
Generates a real Ethernet/IPv4/TCP packet capture file (.pcap) containing
a full AAA session between a Cisco router (192.168.10.1) and TACACS+ server (192.168.10.254):
  1. TCP Handshake (SYN, SYN-ACK, ACK on Port 49)
  2. Authentication START (Action: Login, User: 'admin', Port: 'tty0')
  3. Authentication REPLY (Status: GETPASS, Prompt: 'Password: ')
  4. Authentication CONTINUE (User enters 'SecretAdminPass2026')
  5. Authentication REPLY (Status: PASS / 0x01)
  6. Authorization REQUEST (User executes: 'service=shell cmd=show running-config')
  7. Authorization RESPONSE (Status: PASS_ADD / 0x01)
  8. TCP Connection Teardown (FIN, ACK)

Open the resulting .pcap in Wireshark or inspect with tshark!
Wireshark Decryption Setting:
  Edit -> Preferences -> Protocols -> TACACS+ -> Encryption Key: 'cisco123'
"""

import hashlib
import struct
import time
from pathlib import Path

# Addresses
SRC_MAC = bytes.fromhex("005056a1b2c3")  # Router
DST_MAC = bytes.fromhex("005056d4e5f6")  # TACACS+ Server
SRC_IP = "192.168.10.1"
DST_IP = "192.168.10.254"
CLIENT_PORT = 49152
SERVER_PORT = 49
SHARED_SECRET = b"cisco123"
SESSION_ID = 0x3A8F12D0

# TACACS+ Header Constants
TAC_PLUS_MAJOR_VER = 0xC
TAC_PLUS_MINOR_VER = 0x0
TAC_PLUS_AUTHEN = 0x01
TAC_PLUS_AUTHOR = 0x02

# Authentication Action / Types
TAC_PLUS_AUTHEN_LOGIN = 0x01
TAC_PLUS_AUTHEN_TYPE_ASCII = 0x01
TAC_PLUS_AUTHEN_SVC_LOGIN = 0x01

# Statuses
TAC_PLUS_AUTHEN_STATUS_PASS = 0x01
TAC_PLUS_AUTHEN_STATUS_GETPASS = 0x02
TAC_PLUS_AUTHOR_STATUS_PASS_ADD = 0x01

def ip_to_bytes(ip_str: str) -> bytes:
    return bytes(map(int, ip_str.split(".")))

def calculate_checksum(data: bytes) -> int:
    if len(data) % 2 == 1:
        data += b"\x00"
    s = sum(struct.unpack("!%dH" % (len(data) // 2), data))
    s = (s >> 16) + (s & 0xFFFF)
    s += s >> 16
    return ~s & 0xFFFF

def build_ipv4_header(src_ip: str, dst_ip: str, payload_len: int, proto: int = 6, ident: int = 1001) -> bytes:
    total_len = 20 + payload_len
    header_no_cs = struct.pack(
        "!BBHHHBBH4s4s",
        0x45, 0x00, total_len, ident, 0x4000, 64, proto, 0,
        ip_to_bytes(src_ip), ip_to_bytes(dst_ip)
    )
    cs = calculate_checksum(header_no_cs)
    return struct.pack(
        "!BBHHHBBH4s4s",
        0x45, 0x00, total_len, ident, 0x4000, 64, proto, cs,
        ip_to_bytes(src_ip), ip_to_bytes(dst_ip)
    )

def build_tcp_header(src_ip: str, dst_ip: str, src_port: int, dst_port: int,
                     seq: int, ack: int, flags: int, payload: bytes = b"") -> bytes:
    offset_flags = (5 << 12) | flags
    window = 65535
    tcp_no_cs = struct.pack("!HHIIHHHH", src_port, dst_port, seq, ack, offset_flags, window, 0, 0)
    
    # Pseudo-header for checksum
    pseudo = struct.pack("!4s4sBBH", ip_to_bytes(src_ip), ip_to_bytes(dst_ip), 0, 6, 20 + len(payload))
    cs = calculate_checksum(pseudo + tcp_no_cs + payload)
    return struct.pack("!HHIIHHHH", src_port, dst_port, seq, ack, offset_flags, window, cs, 0)

def generate_md5_pad(session_id: int, secret: bytes, version: int, seq_no: int, length: int) -> bytes:
    session_bytes = struct.pack("!I", session_id)
    version_byte = bytes([version])
    seq_byte = bytes([seq_no])
    pad = b""
    last_hash = b""
    while len(pad) < length:
        h = hashlib.md5()
        h.update(session_bytes)
        h.update(secret)
        h.update(version_byte)
        h.update(seq_byte)
        if last_hash:
            h.update(last_hash)
        last_hash = h.digest()
        pad += last_hash
    return pad[:length]

def xor_bytes(data: bytes, pad: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(data, pad))

def build_tacacs_packet(pkt_type: int, seq_no: int, session_id: int, raw_body: bytes, secret: bytes) -> bytes:
    version = (TAC_PLUS_MAJOR_VER << 4) | TAC_PLUS_MINOR_VER
    flags = 0x00  # Obfuscated
    length = len(raw_body)
    pad = generate_md5_pad(session_id, secret, version, seq_no, length)
    encrypted_body = xor_bytes(raw_body, pad)
    header = struct.pack("!BBBBII", version, pkt_type, seq_no, flags, session_id, length)
    return header + encrypted_body

# Payload Builders
def build_authen_start(user: str = "admin", port: str = "tty0") -> bytes:
    user_b = user.encode()
    port_b = port.encode()
    rem_addr_b = b"192.168.10.50"
    data_b = b""
    hdr = struct.pack(
        "!BBBBBBBB",
        TAC_PLUS_AUTHEN_LOGIN,
        1,  # priv_lvl
        TAC_PLUS_AUTHEN_TYPE_ASCII,
        TAC_PLUS_AUTHEN_SVC_LOGIN,
        len(user_b),
        len(port_b),
        len(rem_addr_b),
        len(data_b)
    )
    return hdr + user_b + port_b + rem_addr_b + data_b

def build_authen_reply_getpass(msg: str = "Password: ") -> bytes:
    msg_b = msg.encode()
    data_b = b""
    hdr = struct.pack("!BBHH", TAC_PLUS_AUTHEN_STATUS_GETPASS, 0x00, len(msg_b), len(data_b))
    return hdr + msg_b + data_b

def build_authen_continue(user_msg: str = "SecretAdminPass2026") -> bytes:
    user_msg_b = user_msg.encode()
    data_b = b""
    hdr = struct.pack("!HHB", len(user_msg_b), len(data_b), 0x00)
    return hdr + user_msg_b + data_b

def build_authen_reply_pass() -> bytes:
    msg_b = b"Authentication successful\n"
    data_b = b""
    hdr = struct.pack("!BBHH", TAC_PLUS_AUTHEN_STATUS_PASS, 0x00, len(msg_b), len(data_b))
    return hdr + msg_b + data_b

def build_author_request(user: str = "admin", cmd: str = "show running-config") -> bytes:
    user_b = user.encode()
    port_b = b"tty0"
    rem_addr_b = b"192.168.10.50"
    args = [b"service=shell", f"cmd={cmd}".encode()]
    arg_lengths = [len(a) for a in args]

    hdr = struct.pack(
        "!BBBBBBBB",
        0x01,  # authen_method: TAC_PLUS_AUTHEN_METH_TACACSPLUS
        1,     # priv_lvl
        TAC_PLUS_AUTHEN_TYPE_ASCII,
        TAC_PLUS_AUTHEN_SVC_LOGIN,
        len(user_b),
        len(port_b),
        len(rem_addr_b),
        len(args)
    )
    arg_lens_b = bytes(arg_lengths)
    args_b = b"".join(args)
    return hdr + arg_lens_b + user_b + port_b + rem_addr_b + args_b

def build_author_response_pass(cmd: str = "show running-config") -> bytes:
    args = [b"service=shell", f"cmd={cmd}".encode()]
    arg_lengths = [len(a) for a in args]
    msg_b = b"Command authorized"
    data_b = b""
    hdr = struct.pack("!BBHH", TAC_PLUS_AUTHOR_STATUS_PASS_ADD, len(args), len(msg_b), len(data_b))
    arg_lens_b = bytes(arg_lengths)
    args_b = b"".join(args)
    return hdr + arg_lens_b + msg_b + data_b + args_b

def generate_pcap(output_path: Path):
    packets = []
    base_time = time.time()
    current_time = base_time

    # State tracking
    cli_seq = 1000
    srv_seq = 5000
    ident = 200

    def add_packet(from_client: bool, flags: int, payload: bytes = b""):
        nonlocal current_time, cli_seq, srv_seq, ident
        current_time += 0.015  # 15ms latency step
        src_ip = SRC_IP if from_client else DST_IP
        dst_ip = DST_IP if from_client else SRC_IP
        src_port = CLIENT_PORT if from_client else SERVER_PORT
        dst_port = SERVER_PORT if from_client else CLIENT_PORT
        smac = SRC_MAC if from_client else DST_MAC
        dmac = DST_MAC if from_client else SRC_MAC

        s_seq = cli_seq if from_client else srv_seq
        s_ack = srv_seq if from_client else cli_seq

        eth = dmac + smac + struct.pack("!H", 0x0800)
        ip = build_ipv4_header(src_ip, dst_ip, 20 + len(payload), proto=6, ident=ident)
        ident += 1
        tcp = build_tcp_header(src_ip, dst_ip, src_port, dst_port, s_seq, s_ack, flags, payload)
        raw_pkt = eth + ip + tcp + payload

        # Advance sequence number
        if len(payload) > 0:
            if from_client:
                cli_seq += len(payload)
            else:
                srv_seq += len(payload)
        elif flags & 0x02 or flags & 0x01:  # SYN or FIN consumes 1 seq
            if from_client:
                cli_seq += 1
            else:
                srv_seq += 1

        sec = int(current_time)
        usec = int((current_time - sec) * 1_000_000)
        pcap_rec_hdr = struct.pack("!IIII", sec, usec, len(raw_pkt), len(raw_pkt))
        packets.append(pcap_rec_hdr + raw_pkt)

    # 1. TCP 3-Way Handshake
    add_packet(from_client=True, flags=0x02)   # SYN
    add_packet(from_client=False, flags=0x12)  # SYN-ACK
    add_packet(from_client=True, flags=0x10)   # ACK

    # 2. TACACS+ Authentication START (User: admin)
    start_payload = build_authen_start(user="admin")
    start_tac = build_tacacs_packet(TAC_PLUS_AUTHEN, 1, SESSION_ID, start_payload, SHARED_SECRET)
    add_packet(from_client=True, flags=0x18, payload=start_tac)  # PSH-ACK
    add_packet(from_client=False, flags=0x10)                   # ACK

    # 3. Server Reply: GETPASS ("Password: ")
    getpass_payload = build_authen_reply_getpass()
    getpass_tac = build_tacacs_packet(TAC_PLUS_AUTHEN, 2, SESSION_ID, getpass_payload, SHARED_SECRET)
    add_packet(from_client=False, flags=0x18, payload=getpass_tac)
    add_packet(from_client=True, flags=0x10)

    # 4. Client Continue: Password
    continue_payload = build_authen_continue(user_msg="SecretAdminPass2026")
    continue_tac = build_tacacs_packet(TAC_PLUS_AUTHEN, 3, SESSION_ID, continue_payload, SHARED_SECRET)
    add_packet(from_client=True, flags=0x18, payload=continue_tac)
    add_packet(from_client=False, flags=0x10)

    # 5. Server Reply: PASS
    pass_payload = build_authen_reply_pass()
    pass_tac = build_tacacs_packet(TAC_PLUS_AUTHEN, 4, SESSION_ID, pass_payload, SHARED_SECRET)
    add_packet(from_client=False, flags=0x18, payload=pass_tac)
    add_packet(from_client=True, flags=0x10)

    # 6. Authorization Request: cmd=show running-config
    author_req_payload = build_author_request(cmd="show running-config")
    author_req_tac = build_tacacs_packet(TAC_PLUS_AUTHOR, 1, 0x4B9C23E1, author_req_payload, SHARED_SECRET)
    add_packet(from_client=True, flags=0x18, payload=author_req_tac)
    add_packet(from_client=False, flags=0x10)

    # 7. Authorization Response: PASS_ADD
    author_resp_payload = build_author_response_pass(cmd="show running-config")
    author_resp_tac = build_tacacs_packet(TAC_PLUS_AUTHOR, 2, 0x4B9C23E1, author_resp_payload, SHARED_SECRET)
    add_packet(from_client=False, flags=0x18, payload=author_resp_tac)
    add_packet(from_client=True, flags=0x10)

    # 8. TCP Teardown (FIN-ACK)
    add_packet(from_client=True, flags=0x11)   # FIN-ACK
    add_packet(from_client=False, flags=0x11)  # FIN-ACK
    add_packet(from_client=True, flags=0x10)   # ACK

    # Write PCAP
    global_hdr = struct.pack(
        "!IHHiIII",
        0xA1B2C3D4,  # magic microsecond
        2, 4,        # major, minor
        0, 0,        # timezone, sigfigs
        65535,       # snaplen
        1            # LINKTYPE_ETHERNET
    )

    with open(output_path, "wb") as f:
        f.write(global_hdr)
        for pkt in packets:
            f.write(pkt)

    print(f"[+] PCAP file written: {output_path}")
    print(f"[+] Total packets generated: {len(packets)}")
    print(f"[+] Wireshark decryption secret: '{SHARED_SECRET.decode()}'")

def main():
    out = Path(__file__).resolve().parent / "tacacs_rfc8907_session.pcap"
    generate_pcap(out)

if __name__ == "__main__":
    main()
