"""Compare each C-graded card's basis with the Source column of its lesson's key-results table.
Prints every card basis that is not a verbatim substring of a key-results Source cell (or of a
key-results Result/Source pair), for L05-L08. Usage: python -I basis_vs_key_g3.py <checkout> <scripts_dir>
"""
import html
import json
import re
import sys

root, scripts = sys.argv[1], sys.argv[2]
cards = json.load(open(f"{root}/course/modules/E/E3/cards.json", encoding="utf-8"))
for L in ("L05", "L06", "L07", "L08"):
    page = open(f"{root}/course/modules/E/E3/{L}.html", encoding="utf-8").read()
    key = page[page.index("Key results") if "Key results" in page else 0:]
    cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", page, re.S)]
    sources = " | ".join(cells)
    for c in cards:
        if c["lesson"] != L or c.get("grade") != "C" or not c.get("basis"):
            continue
        ok = c["basis"] in sources
        print(f"{c['id']} {L} basis verbatim in key-results table: {ok}  basis={c['basis']!r}")
