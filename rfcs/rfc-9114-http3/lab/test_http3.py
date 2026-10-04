#!/usr/bin/env python3
"""
HTTP/3 & QUIC Inspector Probe
Used for testing and verifying RFC 9114 support in the wild.
"""

import sys
import urllib.request
import urllib.parse
from http.client import HTTPResponse

TARGETS = [
    "https://cloudflare.com",
    "https://google.com",
    "https://facebook.com",
    "https://github.com",
]

def check_h3_support(url: str):
    print(f"\n🔍 Probing: {url}")
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (HTTP3-RFC9114-Lab-Probe/1.0)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            alt_svc = response.headers.get("Alt-Svc")
            server = response.headers.get("Server", "Unknown")
            print(f"  ├─ Status: {response.status} {response.reason}")
            print(f"  ├─ Server: {server}")
            if alt_svc and "h3" in alt_svc:
                print(f"  └─ 🚀 HTTP/3 (QUIC) ADVERTISED: ✅")
                print(f"     Alt-Svc header: {alt_svc[:60]}...")
            else:
                print(f"  └─ ⚠️  No explicit HTTP/3 (h3) Alt-Svc advertisement found.")
    except Exception as e:
        print(f"  └─ ❌ Error querying {url}: {e}")

def main():
    print("=" * 60)
    print("⚡ RFC 9114 (HTTP/3) Edge Advertisement Probe")
    print("=" * 60)
    targets = sys.argv[1:] if len(sys.argv) > 1 else TARGETS
    for target in targets:
        if not target.startswith("http"):
            target = f"https://{target}"
        check_h3_support(target)
    print("\n" + "=" * 60)
    print("💡 Note: Browsers use the 'Alt-Svc' header on HTTP/2 responses")
    print("   to learn that an HTTP/3 endpoint is available via UDP/443.")
    print("=" * 60)

if __name__ == "__main__":
    main()
