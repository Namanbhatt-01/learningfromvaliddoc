# RFC [NUMBER]: [TITLE]

> **Status:** [Draft / Proposed Standard / Internet Standard / Informational]  
> **Working Group / Authors:** [e.g., IETF HTTPbis / J. Reschke, etc.]  
> **Source Link:** [https://www.rfc-editor.org/rfc/rfcXXXX](https://www.rfc-editor.org/rfc/rfcXXXX)  
> **Date Published:** [YYYY-MM]  
> **Tags:** `#networking` `#protocols` `#ietf`

---

## ⚡ 30-Second Summary (The Elevator Pitch)
What problem does this RFC solve, why was the previous way broken, and what is the fundamental breakthrough or specification?

---

## 🎯 Background & The "Why"
- **Historical Context:** What did we use before (e.g., HTTP/1.1 or HTTP/2, TLS 1.2, IPv4)?
- **Core Bottlenecks:** Head-of-line blocking, latency, security gaps, round-trips (RTT).
- **Design Goals:** What were the non-negotiables for this specification?

---

## 🛠️ Key Technical Concepts & Mechanisms
Explain the protocol mechanics with precision:
- **Packet / Frame Structure:**
- **Handshake / State Machine:**
- **Error Handling & Edge Cases:**

```mermaid
sequenceDiagram
    autonumber
    Client->>Server: Initial Handshake
    Server-->>Client: Handshake Response
    Client->>Server: Encrypted Payload
```

---

## 🔬 Practical Lab & Verification
How did you test, capture, or verify this protocol in practice?
- **Tools Used:** `tcpdump`, `wireshark`, `curl --http3`, custom python socket script.
- **Commands & Observations:**
```bash
# Example verification command
curl -I --http3 https://cloudflare.com
```

---

## 💡 Practical Takeaways for Engineers
- Where does this apply in modern systems design?
- Common pitfalls or misconceptions.

---

## 🔗 References & Further Reading
- [Official RFC Link](https://www.rfc-editor.org/)
- [Related RFCs](https://...)
