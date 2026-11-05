"""Scan SC1 lesson math spans and cards for macros and single-letter symbols; compare with notation/notation.json.

Usage: python -I notation_scan.py <notation.json> <html...> <cards.json>. Prints macro counts, registry symbols used,
and every math span containing a registered symbol (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q})."""
import json
import re
import sys
from collections import Counter

reg = json.load(open(sys.argv[1], encoding="utf-8"))
macros = set(reg["macros"])
spans_all = []
for path in sys.argv[2:-1]:
    text = open(path, encoding="utf-8").read()
    for m in re.finditer(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", text, re.S):
        body = m.group(1) if m.group(1) is not None else m.group(2)
        spans_all.append((path, text.count("\n", 0, m.start()) + 1, body))
cards = json.load(open(sys.argv[-1], encoding="utf-8"))
for c in cards:
    for field in ("front", "back"):
        spans_all.append((f"card:{c['id']}:{field}", 0, c[field]))
cnt = Counter()
for _, _, body in spans_all:
    for mac in re.findall(r"\\[A-Za-z]+", body):
        cnt[mac] += 1
print("macro counts (math spans and cards):")
for mac, n in cnt.most_common():
    flag = "" if mac in macros else "  <-- not in registry"
    print(f"  {mac} {n}{flag}")
probe = [r"\bT\b", r"\\Phi", r"\\gamma_[34]", r"R\^\\ast", r"R\^\{e\\ast\}", r"R_f", r"\\mathbb\{Q\}", r"\\eta", r"\bU\b", r"\\eta\^", r"\\sigma\^", r"\\argmax", r"\\nu\b", r"\\tau\b", r"\\kappa", r"\\varphi", r"\\phi"]
for pat in probe:
    hits = [(p, ln, b) for p, ln, b in spans_all if re.search(pat, b)]
    print(f"probe {pat}: {len(hits)} spans")
    for p, ln, b in hits[:6]:
        print(f"    {p}:{ln}: {b[:110]!r}")
