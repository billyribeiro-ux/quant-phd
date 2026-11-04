"""Check quoted statute strings against the GovInfo compilation PDFs (text extracted with pdftotext -layout).

Usage: python3 -I statute_quotes.py <comps1884.txt> <comps1885.txt> <quotes.json>
quotes.json maps a short id to {"file": "1884"|"1885", "text": "..."}; prints FOUND / MISSING per id.
Whitespace is collapsed, hyphenated line breaks are joined, and the ø77x¿ section markers are kept as printed.
"""

import json
import re
import sys


def normalise(raw: str) -> str:
    text = re.sub(r"-\n\s*", "", raw)  # join hyphenated line breaks
    text = re.sub(r"\s+", " ", text)
    return text


def main() -> None:
    files = {"1884": normalise(open(sys.argv[1], encoding="utf-8").read()),
             "1885": normalise(open(sys.argv[2], encoding="utf-8").read())}
    quotes = json.load(open(sys.argv[3], encoding="utf-8"))
    missing = 0
    for qid, spec in quotes.items():
        hay = files[spec["file"]]
        needle = normalise(spec["text"])
        ok = needle in hay
        missing += 0 if ok else 1
        print(f"{'FOUND  ' if ok else 'MISSING'} {qid}")
    print(f"total {len(quotes)} missing {missing}")


if __name__ == "__main__":
    main()
