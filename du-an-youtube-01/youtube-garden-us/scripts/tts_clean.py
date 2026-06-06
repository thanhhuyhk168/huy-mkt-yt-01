#!/usr/bin/env python3
"""TTS Clean converter — prep script for ElevenLabs / voice AI.
Numbers→words, $/%/units, strip markdown, anti-CAPS.
pip install num2words
Usage: python tts_clean.py script.txt > script_voiceAI.txt"""
import re, sys

try:
    from num2words import num2words
except ImportError:
    print("ERROR: run 'pip install num2words' first", file=sys.stderr)
    sys.exit(1)


def money(m):
    return num2words(int(m.group(1))) + " dollars"


def percent(m):
    return num2words(int(m.group(1))) + " percent"


def plain_num(m):
    try:
        return num2words(int(m.group(0)))
    except Exception:
        return m.group(0)


def clean(text):
    # Strip markdown headings
    text = re.sub(r"^#+\s*", "", text, flags=re.M)
    # Strip markdown formatting
    text = re.sub(r"[*_`>|]", "", text)
    # Strip structural labels like [HOOK], [MID-HOOK], [NEED DATA]
    text = re.sub(r"\[[^\]]*\]", "", text)
    # Em dash, ellipsis → readable punctuation
    text = text.replace("—", ", ").replace("…", ".")
    # Smart quotes → straight
    text = text.replace("“", '"').replace("”", '"').replace("’", "'")
    # $30 → thirty dollars
    text = re.sub(r"\$(\d+)", money, text)
    # 50% → fifty percent
    text = re.sub(r"(\d+)%", percent, text)
    # Plain numbers → words
    text = re.sub(r"\b\d+\b", plain_num, text)
    # Anti emphasis-CAPS: 3+ uppercase letters that aren't acronyms → capitalize
    text = re.sub(r"\b([A-Z]{3,})\b", lambda m: m.group(1).capitalize(), text)
    # Collapse extra blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tts_clean.py <script.txt>")
        print("Output: cleaned text printed to stdout")
        print("Tip: python tts_clean.py script.txt > script_voiceAI.txt")
        sys.exit(1)
    result = clean(open(sys.argv[1], encoding="utf-8").read())
    print(result)
