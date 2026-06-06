#!/usr/bin/env python3
"""Citation checker — verify URLs in research-brief.md are live.
Usage: python citation_check.py research-brief.md
Exit 0 = all verified, exit 1 = unverified claims found."""
import re, sys, urllib.request, urllib.error

TIMEOUT = 8
URL_PATTERN = re.compile(r"https?://[^\s\)\]\"'>]+")
CLAIM_LINE = re.compile(r"^[-•*]\s+(.+)", re.M)


def check_url(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status < 400
    except Exception:
        return False


def extract_claims(text):
    """Return list of (claim_text, url_or_None)."""
    results = []
    for m in CLAIM_LINE.finditer(text):
        line = m.group(1).strip()
        urls = URL_PATTERN.findall(line)
        results.append((line, urls[0] if urls else None))
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python citation_check.py research-brief.md")
        sys.exit(1)

    text = open(sys.argv[1], encoding="utf-8").read()
    claims = extract_claims(text)

    if not claims:
        print("No claims found in file.")
        sys.exit(0)

    print(f"\nChecking {len(claims)} claims...\n{'='*50}")
    failed = []

    for claim, url in claims:
        short = claim[:70] + ("..." if len(claim) > 70 else "")
        if url is None:
            print(f"⚠️  [NO URL]  {short}")
            failed.append(claim)
        else:
            ok = check_url(url)
            status = "✅" if ok else "❌"
            print(f"{status} [{url[:50]}]  {short}")
            if not ok:
                failed.append(claim)

    print(f"\n{'='*50}")
    print(f"Result: {len(claims) - len(failed)}/{len(claims)} verified")

    if failed:
        print(f"\n❌ {len(failed)} claim(s) need attention:")
        for f in failed:
            print(f"  • {f[:100]}")
        sys.exit(1)
    else:
        print("✅ All claims have live URLs.")
        sys.exit(0)
