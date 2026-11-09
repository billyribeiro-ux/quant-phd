"""Check every curly-quoted passage in cards.json against the source texts (round-11 extractions).

Usage: python3 -I quote_check_cards_r15.py <cards.json> <src_dir>
Prints one line per card quote: card id, found-in source or MISS. Normalises quotes, dashes,
whitespace, the section sign and PDF footnote digits is NOT done: a MISS is reported as is.
"""
import json
import re
import sys

cards_path, src = sys.argv[1], sys.argv[2]
cards = json.load(open(cards_path, encoding="utf-8"))


def norm(s: str) -> str:
    s = s.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("−", "-").replace("§", "section ")
    s = s.replace("''", '"').replace("‐", "-")
    s = re.sub(r"\s+", " ", s)
    return s.lower()


sources = {
    "dirks": "dirks.norm.txt",
    "ohagan": "ohagan.norm.txt",
    "c1884": "c1884.norm.txt",
    "c1885": "c1885.norm.txt",
    "cfa3a": "cfa-iii-a.norm.txt",
    "cfa6a": "cfa-vi-a.norm.txt",
    "att": "att_raw.txt",
    "sr2602": "sr2602a1.txt",
}
texts = {k: norm(open(f"{src}/{v}", encoding="utf-8", errors="replace").read()) for k, v in sources.items()}
pat = re.compile(r"“([^”]+)”")
for c in cards:
    for field in ("front", "back"):
        for q in pat.findall(c.get(field, "")):
            nq = norm(q).strip(" .,;:").strip()
            hits = [k for k, t in texts.items() if nq and nq in t]
            print(f"{c['id']} {field} {'FOUND ' + ','.join(hits) if hits else 'MISS'} :: {q}")
