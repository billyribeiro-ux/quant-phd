"""Scan AC1 L04-L06 learner text for process words, banned phrases and scope words (slice b)."""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
pats = [r"builder", r"\bbuild\b", r"verifier", r"\bround\b", r"REQUESTS", r"unit report", r"roughly half",
        r"about 6%", r"historically", r"\.\.\.", "…", r"\bonly\b", r"\ball\b", r"as much as", r"\bsame\b",
        r"\bdrives\b", r"\boffsets\b", r"\braises\b", r"\balways\b", r"\bpresentation", r"arrangement"]
for n in ("L04", "L05", "L06"):
    text = (root / f"course/modules/AC/AC1/{n}.html").read_text(encoding="utf-8")
    text = re.sub(r"<[^>]+>", " ", text)
    for p in pats:
        for m in re.finditer(p, text, re.I):
            s = text[max(0, m.start() - 60): m.end() + 40].replace("\n", " ")
            print(n, repr(p), "|", re.sub(r"\s+", " ", s))
