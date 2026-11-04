"""Dump the rendered text of each BK4 lesson page and every card (stdlib only).

Usage: python3 -I ledgers/BK4/scripts/BK4-d-r6/dump_text.py <repo-root> <outdir>
"""
import importlib.util
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
outdir = Path(sys.argv[2])
spec = importlib.util.spec_from_file_location("extract_text", root / "ledgers/BK4/scripts/BK4-d-r6/extract_text.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
outdir.mkdir(parents=True, exist_ok=True)
for p in ("L01", "L02", "L03", "L04", "L05", "project"):
    r = mod.Render()
    r.feed((root / f"course/modules/BK/BK4/{p}.html").read_text(encoding="utf-8"))
    text = "\n".join(line for line in " ".join("".join(r.out).split()).split(". ") )
    (outdir / f"lesson_{p}.txt").write_text(text, encoding="utf-8")
cards = json.loads((root / "course/modules/BK/BK4/cards.json").read_text(encoding="utf-8"))
with (outdir / "cards_full.txt").open("w", encoding="utf-8") as f:
    for c in cards:
        f.write(f"[{c['id']}] lesson={c['lesson']} grade={c.get('grade')} cite={c.get('cite')} basis={c.get('basis')}\n")
        f.write(f"  F: {c['front']}\n  B: {c['back']}\n")
