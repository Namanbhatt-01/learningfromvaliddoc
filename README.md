# Learning From Valid Docs

My personal public notes and video scripts breaking down core computer science specifications—IETF RFCs, CVE postmortems, academic papers, and technical standards (IEEE/ISO).

Most online tutorials water down technical concepts or pass along second-hand explanations. I created this repo to read the original primary sources, test things in a local lab, take clear notes, and record short video breakdowns explaining what actually happens at the protocol/code level.

---

## Current Studies & Video Tracker

| ID | Topic | Category | Notes | Lab / Code | Reel / Short | Status |
|---|---|---|---|---|---|---|
| **RFC 9114** | HTTP/3 over QUIC | Networking (IETF) | [Notes](rfcs/rfc-9114-http3/README.md) | [test_http3.py](rfcs/rfc-9114-http3/lab/test_http3.py) | [Script](rfcs/rfc-9114-http3/reel-script.md) | Ready to shoot |
| **CVE-2024-3094** | XZ Utils Backdoor (IFUNC hijacking) | Security / CVE | Coming up | - | - | Reading spec |
| **Vaswani et al. (2017)** | Attention Is All You Need | ML / Papers | Coming up | - | - | Queued |
| **IEEE 802.11be** | Wi-Fi 7 Multi-Link Operation | Wireless (IEEE) | Coming up | - | - | Queued |

---

## Directory Structure

```text
.
├── rfcs/               # IETF RFCs (HTTP/3, TLS 1.3, TCP specs)
├── cves/               # Root-cause analysis of real vulnerabilities
├── research-papers/    # Foundational computer science papers
├── standards/          # IEEE, ISO, NIST standards
├── articles/           # Deep dives from company engineering blogs
├── templates/          # Markdown templates for notes and video scripts
└── scripts/
    └── new_study.py    # Helper to scaffold folders and templates
```

Each topic folder includes:
- `README.md`: My technical notes, architectural details, packet flows, and personal takeaways.
- `reel-script.md`: The 60-second video script (hook, visual cues, voiceover, and captions).
- `lab/`: Code, curl snippets, Wireshark pcaps, or test scripts verifying the spec.
- `assets/`: Diagrams, screenshots, and visual references.

---

## Adding a New Entry

Use the helper script to create the folders and fill in the base templates:

```bash
# Interactive:
python3 scripts/new_study.py

# Or with arguments:
python3 scripts/new_study.py --type rfc --id 8446 --title "TLS 1.3"
python3 scripts/new_study.py --type cve --id 2021-44228 --title "Log4Shell"
python3 scripts/new_study.py --type paper --id 2014 --title "Raft Consensus"
```

---

## Video Format

For each document, I record a 45–60 second vertical video (Reels/Shorts/TikTok/LinkedIn):
1. **0–3s:** The Hook (common misconception or surprising fact from the spec).
2. **3–15s:** What problem or limitation triggered the need for this document.
3. **15–40s:** How it works under the hood (terminal capture, packet trace, or diagram).
4. **40–50s:** The real-world impact (performance numbers, security implications).
5. **50–60s:** Call to action pointing to this repo for notes and lab code.

---

## License
MIT
