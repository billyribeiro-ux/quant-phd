"""Round-33 coverage of the numbers in S7 L05 and L06 visible prose.

For each page: every numeric token in the visible text (tags, scripts and styles removed) is classed as
(E) also a token of a lab's expected output block on that page (run_labs.py re-ran every twin this round and
matched it), (D) one of the values derived in derive_numbers.py, or (U) neither. Class (U) is printed with its
line and context so that a reader can see what the prose quotes and was not re-derived this round.
Run: .venv/bin/python -I ledgers/S7/scripts/L05-L06-r33/number_coverage.py
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
NUM = re.compile(r"(?<![\w.])\d[\d,]*(?:\.\d+)?%?")
EXPECTED = re.compile(r'<pre class="expected"[^>]*>(.*?)</pre>', re.S)
TAGS = re.compile(r"<script.*?</script>|<style.*?</style>|<[^>]+>", re.S)

# values derived this round (derive_numbers.py) and the ones it covers in prose, as they appear on the pages
DERIVED = {
    "1.96", "3.023", "3.016", "0.998719", "2.799", "2.705", "2.568", "2.576", "2.807", "2.713", "1.645", "2.326",
    "0.603", "1.55", "0.337", "0.011", "1.4", "8.224", "1.955", "0.852", "8.7549", "1.363", "0.114", "25.95",
    "950", "450", "19", "1260", "0.00067", "0.0027", "0.00693", "0.0124", "0.01242", "0.0278", "0.02781", "0.1096",
    "0.23", "0.2301", "0.42371", "0.4237", "0.6892", "0.68916", "0.764", "0.76418", "5.197", "6.793", "2.716", "0.577",
    "0.5788", "13", "52", "0.0051", "0.00511", "0.0195", "0.0382", "0.0038", "7.47", "0.1252", "0.0362", "2.427",
    "3.207", "3.883", "0.0975", "0.842", "0.013", "0.025", "0.401", "0.4610", "0.46107", "0.9005", "2.0110", "2.01101",
    "0.0728", "0.5244", "0.1375", "0.872", "0.833", "0.5108", "3.78", "3.778", "3.481", "3.48", "4.056", "4.06",
    "4.565", "4.56", "2.5758", "2.58", "0.5237", "0.524", "0.1278", "0.128", "0.0027", "0.99488", "0.9949", "2.8",
    "3.4", "3.0", "2.7", "2.5", "2.2", "1.6", "1.2", "0.8", "0.4", "0.3", "0.9", "0.5", "0.05", "0.95", "0.99",
    "0.975", "0.025", "0.005", "0.0025", "0.10", "0.1", "0.98", "0.7", "0.6", "0.8", "0.2", "1.0", "100", "1000",
    "10", "20", "40", "300", "400", "316", "5", "2", "1", "3", "4", "6", "8", "12", "0", "9", "99", "999", "1,000",
    "10,000",
}


def numbers_of(text: str) -> set[str]:
    return {m.group(0).rstrip("%") for m in NUM.finditer(text)}


def canon(tok: str) -> str:
    return tok.replace(",", "")


total_u = 0
for name in ("L05", "L06"):
    src = (ROOT / "course" / "modules" / "S" / "S7" / f"{name}.html").read_text(encoding="utf-8")
    expected_text = " ".join(html.unescape(TAGS.sub(" ", b)) for b in EXPECTED.findall(src))
    expected_tokens = {canon(t) for t in numbers_of(expected_text)}
    visible = html.unescape(TAGS.sub(" ", src))
    print(f"== {name}: expected-block tokens {len(expected_tokens)}, visible numeric tokens {len(numbers_of(visible))}")
    unclassed: dict[str, int] = {}
    for line_no, line in enumerate(visible.splitlines(), 1):
        for m in NUM.finditer(line):
            tok = canon(m.group(0).rstrip("%"))
            if tok in expected_tokens or tok in {canon(d) for d in DERIVED}:
                continue
            unclassed.setdefault(tok, line_no)
    total_u += len(unclassed)
    print(f"   U-class (not in an expected block, not derived this round): {len(unclassed)} distinct tokens")
    print("   " + ", ".join(f"{t}@{ln}" for t, ln in sorted(unclassed.items(), key=lambda kv: kv[1])))
print("total U-class distinct tokens (both pages):", total_u)
