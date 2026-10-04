# Learning From Valid Docs

My personal public notes and experiments studying core computer science specifications—IETF RFCs, CVE postmortems, academic papers, and technical standards (IEEE/ISO).

Most online tutorials water down technical concepts or pass along second-hand explanations. I created this repo to read the original primary sources, test things in a local lab, take clear notes, and post short companion video breakdowns on Instagram.

---

## Studies & Tracker

| Spec / ID | Category | Summary | Notes | Lab / Code | Video |
|---|---|---|---|---|---|
| **RFC 9114** | Networking (IETF) | HTTP/3: Replacing TCP with QUIC to fix head-of-line blocking | [Notes](rfcs/rfc-9114-http3/README.md) | [test_http3.py](rfcs/rfc-9114-http3/lab/test_http3.py) | [Script](rfcs/rfc-9114-http3/script.md) · [Instagram](#) |
| **CVE-2024-3094** | Security / CVE | XZ Utils Backdoor: IFUNC hooking and payload extraction | Coming up | - | Coming up |
| **Vaswani et al. (2017)** | ML / Papers | Attention Is All You Need | Coming up | - | Coming up |
| **IEEE 802.11be** | Wireless (IEEE) | Wi-Fi 7 Multi-Link Operation (MLO) | Coming up | - | Coming up |

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

Each study directory contains:
- `README.md`: Technical notes, packet flows, edge cases, and personal takeaways.
- `lab/`: Code, curl snippets, Wireshark captures, or test scripts.
- `script.md`: A concise 45-60 second talking script and Instagram Reel link.
- `assets/`: Diagrams, screenshots, and visual references.

---

## Adding a New Entry

To scaffold a new study workspace:

```bash
# Interactive prompt:
python3 scripts/new_study.py

# Or via flags:
python3 scripts/new_study.py --type rfc --id 8446 --title "TLS 1.3"
python3 scripts/new_study.py --type cve --id 2021-44228 --title "Log4Shell"
python3 scripts/new_study.py --type paper --id 2014 --title "Raft Consensus"
```

---

## License
MIT
