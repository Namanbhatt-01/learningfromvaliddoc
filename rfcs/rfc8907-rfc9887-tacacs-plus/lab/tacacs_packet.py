#!/usr/bin/env python3
"""
TACACS+ Packet Dissector & Obfuscation Inspector (RFC 8907 vs RFC 9887)
Demonstrates:
  1. The 12-byte fixed binary header structure.
  2. Legacy MD5 pseudo-pad XOR generation (RFC 8907).
  3. Why legacy encryption is fragile and why RFC 9887 mandates TLS 1.3.
"""

import hashlib
import struct

# TACACS+ Constants
TAC_PLUS_MAJOR_VER = 0xC
TAC_PLUS_MINOR_VER_DEFAULT = 0x0
TAC_PLUS_AUTHEN = 0x01
TAC_PLUS_AUTHOR = 0x02
TAC_PLUS_ACCT = 0x03

TAC_PLUS_UNENCRYPTED_FLAG = 0x01
TAC_PLUS_SINGLE_CONNECT_FLAG = 0x04

def generate_legacy_md5_pad(session_id: int, secret: bytes, version: int, seq_no: int, length: int) -> bytes:
    """
    Implements RFC 8907 Section 4.5 pseudo-random pad generation:
    pad_1 = MD5(session_id + key + version + seq_no)
    pad_i = MD5(session_id + key + version + seq_no + pad_{i-1})
    """
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

def build_header(seq_no: int, session_id: int, payload_len: int, unencrypted: bool = False) -> bytes:
    """
    Builds the 12-byte RFC 8907 fixed header:
    - 1 byte:  version (major 4 bits, minor 4 bits)
    - 1 byte:  type (0x01 Authen, 0x02 Author, 0x03 Acct)
    - 1 byte:  seq_no
    - 1 byte:  flags
    - 4 bytes: session_id
    - 4 bytes: length
    """
    version = (TAC_PLUS_MAJOR_VER << 4) | TAC_PLUS_MINOR_VER_DEFAULT
    flags = TAC_PLUS_UNENCRYPTED_FLAG if unencrypted else 0x00
    pkt_type = TAC_PLUS_AUTHOR

    return struct.pack("!BBBBII", version, pkt_type, seq_no, flags, session_id, payload_len)

def main():
    print("=" * 65)
    print("TACACS+ Protocol Packet Analysis: RFC 8907 vs RFC 9887")
    print("=" * 65)

    secret = b"cisco123"
    session_id = 0x1A2B3C4D
    seq_no = 1
    sample_payload = b"user=admin service=shell cmd=show running-config"

    print(f"\n[1] Sample Payload to Authorize: '{sample_payload.decode()}'")
    print(f"    Payload Size: {len(sample_payload)} bytes")

    # 1. RFC 8907 Legacy Obfuscation
    print("\n[2] RFC 8907 Legacy MD5 Obfuscation (Port 49)")
    pad = generate_legacy_md5_pad(session_id, secret, (TAC_PLUS_MAJOR_VER << 4), seq_no, len(sample_payload))
    ciphertext = xor_bytes(sample_payload, pad)
    header_legacy = build_header(seq_no, session_id, len(sample_payload), unencrypted=False)

    print(f"    12-byte Plaintext Header (hex): {header_legacy.hex()}")
    print(f"    Obfuscated Body (hex):          {ciphertext.hex()}")
    print("    Security Flaw: The 12-byte header transmits session_id, seq_no,")
    print("    and version in plain view. If an attacker captures predictable")
    print("    CLI command strings, they can deduce the keystream and brute-force")
    print("    the pre-shared secret offline.")

    # 2. RFC 9887 Modern TLS 1.3 Transport
    print("\n[3] RFC 9887 over TLS 1.3 (Port 300)")
    header_tls = build_header(seq_no, session_id, len(sample_payload), unencrypted=True)
    print(f"    12-byte Header (UNENCRYPTED_FLAG set): {header_tls.hex()}")
    print("    Transport Requirement: Enclosed entirely within TLS 1.3 tunnel.")
    print("    Confidentiality & Integrity: Handled via modern AEAD ciphers")
    print("    (e.g., AES-GCM or ChaCha20-Poly1305) with mutual X.509 certificates.")

    print("\n" + "=" * 65)

if __name__ == "__main__":
    main()
