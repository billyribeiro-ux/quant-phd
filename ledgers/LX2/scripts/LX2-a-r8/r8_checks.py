"""Round 8 targeted checks for LX2 slice a (hub index.html, L01, L02, lab twins).

Usage: python -I ledgers/LX2/scripts/LX2-a-r8/r8_checks.py <source_dir> <checkout_dir>
<source_dir> holds the pdftotext output re-fetched this round (fetch_sources.sh). Prints, for each check, the
observed result so that the fragment can cite it.
"""

import os
import re
import subprocess
import sys

SRC, CHK = sys.argv[1], sys.argv[2]


def alnum(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"[^a-z0-9]", "", s.lower())


def pages(path: str) -> list[tuple[str, str]]:
    raw = open(path, encoding="utf-8", errors="replace").read().split("\f")
    out = []
    for c in raw:
        m = re.search(r"^\s*(\d{3})\s{2,}\S|\S\s{2,}(\d{3})\s*$", c, re.M)
        out.append(((m.group(1) or m.group(2)) if m else "?", c))
    return out


def find(path: str, needle: str) -> list[str]:
    hits = []
    for num, c in pages(path):
        if alnum(needle) in alnum(c):
            hits.append(num)
    return hits


print("== 1. Thomas dissent (O'Hagan p. 680): quoted fragment as printed in L02 line 109")
o = os.path.join(SRC, "ohagan.txt")
print("L02 wording 'the misappropriation theory fails to provide a coherent and consistent interpretation':",
      find(o, "the misappropriation theory fails to provide a coherent and consistent interpretation") or "NOT FOUND")
print("verbatim source wording (Commission's ... consistent):",
      find(o, "Commission's misappropriation theory fails to provide a coherent and consistent interpretation") or "NOT FOUND")
print("source sentence context (verbatim, pdftotext):")
txt = open(o, encoding="utf-8", errors="replace").read()
i = txt.find("Because the Commission")
print("   ", re.sub(r"\s+", " ", txt[i : i + 170]))

print("== 2. O'Hagan footnote 5 (p. 653 n. 5) and classical-theory sentence (pp. 651-652)")
print("footnote 5 sentence (O'Hagan's) found on:",
      find(o, "Under the misappropriation theory, O'Hagan's securities trading does not escape Exchange Act sanction"))
print("classical sentence first half, then second half:",
      find(o, "Under the traditional or classical theory of insider trading liability, 10b and Rule 10b-5 are violated when a corporate insider trades in the securities of his corporation") ,
      find(o, "on the basis of material, nonpublic information"))

print("== 3. Dirks dissent location and benefit-test counter-evidence (pages)")
d = os.path.join(SRC, "dirks.txt")
for needle in ["Justice Blackmun, with whom Justice Brennan", "engrafts a special motivational requirement",
               "Personal gain is not an element", "somewhat cynical view, gifts involve personal gain",
               "Accepting the Court's view of tippee liability", "relationship of trust and confidence between the insider and the shareholder",
               "objective facts and circumstances that often justify such an inference", "Scienter in some cases is relevant",
               "a question of fact, will not always be easy", "the test is whether the insider personally will benefit"]:
    print(f"  {needle[:60]!r}: p. {find(d, needle)}")

print("== 4. Dirks p.660 knowledge condition (cited by Remark 3.3) and p.662 benefit test")
print("  'the tippee knows or should know that there has been a breach':", find(d, "the tippee knows or should know that there has been a breach"))
print("  'Absent some personal gain, there has been no breach of duty to stockholders':", find(d, "Absent some personal gain, there has been no breach of duty to stockholders"))

print("== 5. Registry and notation")
ref = open(os.path.join(CHK, "references/references.json"), encoding="utf-8").read()
print("  'conflict' occurrences in references/references.json:", len(re.findall(r"conflict", ref, re.I)))
print("  'fiduciary' occurrences in references/references.json:", len(re.findall(r"fiduciary", ref, re.I)))
