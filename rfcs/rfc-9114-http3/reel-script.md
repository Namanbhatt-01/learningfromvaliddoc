# 🎬 Reel Script: Why HTTP/3 Ditched TCP for UDP (RFC 9114)

> **Format:** 9:16 Vertical Video (Instagram Reels, YouTube Shorts, LinkedIn)  
> **Duration:** 55 seconds  
> **Topic:** RFC 9114 (HTTP/3) & QUIC Protocol  
> **Status:** Ready to Record 🎥

---

## ⏱️ Video Breakdown

| Timestamp | Dialogue / Voiceover (VO) | Visual Cue (B-Roll & Screen) | Text Overlay |
|---|---|---|---|
| **00:00 - 00:04** | *"Why did internet engineers decide to dump TCP and build HTTP/3 on top of UDP? Isn't UDP unreliable?"* | Pointing at camera with skeptical expression; split screen showing `TCP vs UDP` animation | **TCP IS OBSOLETE?! 🤯** |
| **00:04 - 00:14** | *"Here is the dirty secret: in HTTP/2, if you download 20 images at once and ONE single packet drops over Wi-Fi..."* | Animated graphic showing 20 cars on a highway with one broken car stopping the entire road | **HEAD-OF-LINE BLOCKING 🛑** |
| **00:14 - 00:24** | *"...TCP forces every single other stream to freeze until that missing packet is resent. That's Head-of-Line Blocking."* | Terminal screen showing latency spike or Wireshark packet stalling | **ALL STREAMS FREEZE ⏳** |
| **00:24 - 00:36** | *"Enter IETF RFC 9114: HTTP/3. It swaps TCP for QUIC over UDP. Each stream is completely independent."* | Split screen showing packets bypassing the stalled stream smoothly | **RFC 9114: QUIC ⚡** |
| **00:36 - 00:46** | *"Plus, QUIC merges TLS 1.3 encryption directly into the handshake, meaning 0-RTT connection times and seamless Wi-Fi to 5G switching!"* | Side-by-side handshake latency graph: 2 RTT vs 0-1 RTT | **0-RTT HANDSHAKE 🚀** |
| **00:46 - 00:55** | *"I wrote down the complete breakdown, packet flow diagrams, and a python inspection lab in my open-source GitHub repo. Link in bio!"* | Quick screen recording scrolling through the GitHub notes & Mermaid diagram | **NOTES IN GITHUB (LINK IN BIO) 🔗** |

---

## 📱 Social Copy & Post Metadata

### Title / Hook
Why HTTP/3 ditched TCP for UDP! 🌐 (IETF RFC 9114 explained)

### Caption
```text
Did you know that HTTP/3 doesn't use TCP at all? 🤯

In HTTP/2, multiplexing was supposed to fix slow page loads. But because TCP requires strict in-order delivery, losing even 1% of packets on cellular networks stalls ALL multiplexed streams! 

This is known as Transport-Layer Head-of-Line Blocking.

Under RFC 9114, HTTP/3 solves this by running QUIC over UDP:
✅ Independent streams (no global stalling)
✅ 0-RTT connection resumption with integrated TLS 1.3
✅ Seamless connection migration when switching from Wi-Fi to mobile data

I’m doing a full series breaking down official RFCs, CVEs, and research papers with code labs on my GitHub.

Check the repository link in my bio to read the full study notes and run the test lab! 💻🚀

#networking #http3 #computerscience #softwareengineering #webdev #infosec #techreels #coding #systemdesign
```
