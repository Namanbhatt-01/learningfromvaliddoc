# Reel Script: Why HTTP/3 Ditched TCP for UDP

- **Length:** ~50 seconds
- **Format:** 9:16 Vertical Video (Reels / Shorts / TikTok)
- **Topic:** RFC 9114 / QUIC
- **Recording status:** Ready to shoot

---

## Script & Visuals

| Time | What I say (Voiceover) | What is on screen | On-screen text |
|---|---|---|---|
| **0:00 - 0:04** | "Did you know that HTTP/3 doesn't use TCP at all? It actually runs completely over UDP." | Looking at camera, holding up phone or sitting at desk. | Why HTTP/3 runs on UDP 👇 |
| **0:04 - 0:13** | "To understand why, look at HTTP/2. It let browsers download multiple files over one single TCP connection. That seemed great..." | Screen recording: browser network tab downloading 30 images at once. | HTTP/2 multiplexing |
| **0:13 - 0:24** | "...until you hit packet loss. Because TCP guarantees strict order, if even one packet drops over flaky mobile data, everything freezes while waiting for that single retransmit." | Simple diagram or terminal showing dropped packet stalling the rest of the stream. | Head-of-line blocking 🛑 |
| **0:24 - 0:35** | "That's why RFC 9114 created HTTP/3. It uses QUIC on top of UDP. Multiplexing moves directly into the transport layer, so streams are completely independent." | Visual comparison: TCP single lane vs QUIC multi-lane highway. | RFC 9114 + QUIC ⚡ |
| **0:35 - 0:45** | "One dropped packet only delays that specific file. The rest of the page keeps loading. Plus, the handshake is down to a single round trip." | Terminal showing `curl --http3` or `Alt-Svc` header response. | 1-RTT Handshake |
| **0:45 - 0:52** | "I wrote down my complete reading notes and a quick python test script in my GitHub repo—link is in my bio." | Quick screencast of the GitHub repo and README. | Notes in bio 🔗 |

---

## Social Caption

Why HTTP/3 ditched TCP for UDP 👇

When HTTP/2 came out, multiplexing felt like magic. But it created a hidden bottleneck: TCP head-of-line blocking. 

If you download 20 files on mobile and packet #3 drops, TCP pauses delivery of all subsequent packets until packet #3 gets resent.

RFC 9114 fixes this with HTTP/3:
- Runs on QUIC (over UDP)
- Streams are completely independent (no connection freeze on packet loss)
- Faster connection setup (0–1 RTT with built-in TLS 1.3)
- Survives Wi-Fi to mobile data handoffs seamlessly

I've documented my full notes from reading the RFC plus a python test script on GitHub. Link in my bio.

#softwareengineering #networking #webdevelopment #http3 #computerscience #programming
