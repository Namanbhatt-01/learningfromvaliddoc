# RFC 9114: HTTP/3 - Video Script

- **Instagram Reel:** [Pending / Add link here]
- **Duration:** ~45 seconds
- **Status:** Ready to shoot

---

## Talking Script

- **Hook:** Did you know HTTP/3 doesn't use TCP at all? It runs completely over UDP.
- **The Problem:** In HTTP/2, we multiplexed everything through a single TCP connection. But if you're on mobile and drop a single packet, TCP freezes all other streams until that packet gets retransmitted. That's head-of-line blocking.
- **How It Works:** RFC 9114 solves this by moving multiplexing into QUIC over UDP. Each stream is isolated. If stream 2 loses a packet, stream 3 and 4 keep loading without interruption.
- **Bonus:** Handshakes take only 1 round trip (or 0 on reconnect) because TLS 1.3 is built right into the transport.
- **CTA:** I put together full reading notes and a quick python test script on my GitHub—link in bio.

---

## Instagram Caption

Why HTTP/3 ditched TCP for UDP 👇

HTTP/2 multiplexing had a hidden trap: TCP head-of-line blocking. If a single packet drops on a mobile connection, the whole TCP pipeline stalls.

RFC 9114 standardizes HTTP/3 over QUIC (UDP):
- Independent streams (one dropped packet doesn't stall the connection)
- 0–1 RTT connection setup with built-in TLS 1.3
- Seamless Wi-Fi to 5G switching via 64-bit Connection IDs

Full reading notes and a python test script are on my GitHub (link in bio).

#networking #http3 #computerscience #softwareengineering #webdev
