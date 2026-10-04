#!/usr/bin/env python3
"""
Simple script to check if popular domains advertise HTTP/3 (h3)
via the Alt-Svc response header.
"""

import sys
import urllib.request

DOMAINS = [
    "https://cloudflare.com",
    "https://google.com",
    "https://facebook.com",
    "https://github.com",
]

def check_domain(url: str):
    print(f"\nChecking {url}...")
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (HTTP3-Check/1.0)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as res:
            alt_svc = res.headers.get("Alt-Svc")
            server = res.headers.get("Server", "Unknown")
            print(f"  Status: {res.status} ({server})")
            if alt_svc and "h3" in alt_svc:
                print(f"  -> HTTP/3 supported via Alt-Svc: {alt_svc[:50]}...")
            else:
                print(f"  -> No HTTP/3 (h3) Alt-Svc header found.")
    except Exception as err:
        print(f"  -> Error: {err}")

def main():
    targets = sys.argv[1:] if len(sys.argv) > 1 else DOMAINS
    for target in targets:
        if not target.startswith("http"):
            target = f"https://{target}"
        check_domain(target)
    print("\nNote: Browsers read the Alt-Svc header on port 443 TCP to discover UDP HTTP/3 endpoints.")

if __name__ == "__main__":
    main()
