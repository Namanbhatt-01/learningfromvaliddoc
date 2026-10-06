# TACACS+ Protocol Evolution - Video Script

- **Instagram Reel:** [Pending / Add link here]
- **Duration:** ~50 seconds
- **Topic:** RFC 8907 vs RFC 9887 (TACACS+ over TLS 1.3)
- **Status:** Ready to shoot

---

## Talking Script

- **Hook:** Did you know that for over 20 years, the protocol protecting access to enterprise routers ran on an expired 1997 draft and fake encryption?
- **The Protocol:** TACACS+ controls Authentication, Authorization, and Accounting on network devices. Unlike RADIUS, it inspects every single CLI command an engineer types.
- **The Problem:** But until RFC 8907 was published in 2020, it was never an official internet standard. Worse, its encryption was just an MD5 XOR loop. Because the 12-byte header is in plaintext, an attacker on the management network could easily deduce the pad and crack the shared secret.
- **The Fix:** RFC 9887 completely fixes this. It mandates TLS 1.3 as the minimum transport, moves traffic to a dedicated port 300, and enables mutual certificate authentication.
- **Bonus:** RFC 9950 standardized a YANG data model so we can automate all of this via NETCONF instead of manual CLI configs.
- **CTA:** I put together full protocol packet breakdowns, cryptographic math, and configuration examples on GitHub, link in bio.

---

## Instagram Caption

The protocol protecting enterprise routers just got a major overhaul (RFC 8907 to RFC 9887).

For decades, TACACS+ was the industry standard for controlling router CLI access. But it had two massive issues:
1. It wasn't an official IETF standard until 2020 (RFC 8907).
2. Its legacy encryption was just an MD5 XOR stream cipher with plaintext headers, leaving it vulnerable to known-plaintext and offline brute-force attacks.

RFC 9887 modernizes TACACS+ for zero-trust environments:
- Mandates TLS 1.3 as the transport baseline
- Replaces legacy port 49 with port 300 (tacacss)
- Enforces mutual certificate authentication (mTLS) instead of weak shared secrets
- Paired with RFC 9950 for programmatic YANG automation via NETCONF

Full packet anatomy diagrams, cryptographic breakdown, and Cisco configuration snippets are live on my GitHub (link in bio).

#networking #cybersecurity #ietf #tacacs #tls13 #cisco #networkengineering #infosec
