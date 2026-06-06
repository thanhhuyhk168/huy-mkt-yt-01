#!/usr/bin/env python3
"""Compliance V2 scanner — 32 regex, 6 categories A-F.
YouTube AD-FRIENDLY check for gardening scripts (EN).
Usage: python compliance_scan.py script.txt
Exit 0 = CLEAN/SOFT-FAIL, exit 1 = HARD-FAIL."""
import re, sys

FIX = {
    "A": "→ 'can be harmful to [pet] according to [authority]' + citation",
    "B": "→ 'the protection holds' / 'effective approach' / 'manage X effectively'",
    "C": "→ DELETE entirely, replace with 'most people overlook X because Y'",
    "D": "→ 'measurable results' + data / 'research in [journal] shows X'",
    "E": "→ delve=dig into, leverage=use, moreover=and, myriad of=a bunch of...",
    "F": "→ 'When practitioners have tested' / 'In documented home-garden trials'",
}

PATTERNS = {
    "A": [
        r"\b(kill|fatal|deadly|lethal|toxic)\s+(to|for)\s+(cat|dog|pet|child|baby|infant)",
        r"\b(will\s+kill|always\s+kills|guaranteed\s+to\s+kill)",
        r"\b(poison|destroy|exterminate)\s+(your|their)\s+(cat|dog|pet)",
    ],
    "B": [
        r"\b(indefinitely|forever|permanently|for\s+life|eternal)\b",
        r"\b(never\s+fails|always\s+works|100%\s+(effective|guaranteed))\b",
        r"\b(magic|miracle|secret\s+weapon|silver\s+bullet)\b",
        r"\b(cure|reverse|eliminate)\s+\w+\s+(forever|completely|entirely)",
    ],
    "C": [
        r"\b(they|big\s+\w+|the\s+industry)\s+don'?t\s+want\s+you\s+to\s+know\b",
        r"\b(secret|hidden|forbidden|banned)\s+(truth|method|technique|knowledge)\b",
        r"\bBig\s+(Pharma|Ag|Food|Pesticide|Chemical)\b",
    ],
    "D": [
        r"\b(shocking|unbelievable|jaw-dropping|mind-blowing)\s+results?\b",
        r"\b(doctors|experts|scientists)\s+(hate|fear|don'?t\s+want)\b",
        r"\bone\s+(weird|simple|crazy)\s+(trick|secret|tip)\b",
        r"\b(will|going\s+to)\s+(blow|change|shock)\s+your\s+(mind|world|life)\b",
    ],
    "E": [
        r"\b(delve|leverage|utilize|facilitate|underscore|endeavor)\b",
        r"\b(robust|comprehensive|holistic|pivotal|transformative)\b",
        r"\b(moreover|furthermore|additionally|in\s+conclusion|to\s+summarize|in\s+summary)\b",
        r"\bit\s+is\s+(important|worth|essential)\s+to\s+(note|mention|understand)\b",
        r"\bthe\s+(landscape|realm|tapestry|world)\s+of\s+\w+",
        r"\bnavigate\s+(the\s+)?(complexities|challenges|landscape|nuances)\b",
        r"\b(a\s+)?(myriad|plethora)\s+of\b",
        r"\b(embark\s+on|harness\s+the\s+power|unleash\s+the\s+potential|elevate\s+your)\b",
        r"\b(game-?changer|cutting-?edge|seamlessly|paradigm\s+shift)\b",
        r"\b(in\s+today'?s\s+(fast-?paced|digital)\s+\w+|let'?s\s+dive\s+in)\b",
    ],
    "F": [
        r"\bI'?ve\s+been\s+(gardening|growing|farming)\s+for\s+\d+\s+(years|decades)\b",
        r"\bin\s+my\s+(garden|greenhouse|lab|farm|backyard)\b",
        r"\bI\s+(personally\s+)?(tested|grew|planted|experimented)\b",
        r"\b(when\s+I\s+worked|back\s+when\s+I\s+was)\s+(at|in|for)\b",
        r"\b(told|confided|whispered|revealed)\s+(to\s+)?me\s+(privately|personally|confidentially)\b",
    ],
}


def scan(text):
    hits = {}
    for cat, rxs in PATTERNS.items():
        found = []
        for rx in rxs:
            for m in re.finditer(rx, text, re.IGNORECASE):
                found.append(m.group(0))
        if found:
            hits[cat] = found
    return hits


def verdict(hits):
    c = {k: len(v) for k, v in hits.items()}
    ad = c.get("A", 0) + c.get("B", 0) + c.get("D", 0)
    if ad >= 5 or c.get("C", 0) >= 1 or c.get("F", 0) >= 1 or c.get("E", 0) >= 5:
        return "HARD-FAIL"
    return "SOFT-FAIL" if sum(c.values()) else "CLEAN"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compliance_scan.py <script.txt>")
        sys.exit(1)
    text = open(sys.argv[1], encoding="utf-8").read()
    hits = scan(text)
    v = verdict(hits)
    print(f"\n{'='*50}")
    print(f"VERDICT: {v}")
    print(f"{'='*50}\n")
    if not hits:
        print("✅ No compliance issues found.")
    for cat, found in hits.items():
        print(f"[Category {cat}] {len(found)} match  {FIX[cat]}")
        for f in found:
            print(f"   • {f!r}")
    print()
    sys.exit(1 if v == "HARD-FAIL" else 0)
