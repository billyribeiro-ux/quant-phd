"""Dump every BK4 card in full, one field per line (stdlib only).

Usage: python3 -I ledgers/BK4/scripts/BK4-d-r7/dump_cards_r7.py <repo-root>
"""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/BK/BK4/cards.json").read_text(encoding="utf-8"))
for c in cards:
    print(f"[{c['id']}] lesson={c['lesson']} grade={c.get('grade')} cite={c.get('cite')} basis={c.get('basis')}")
    print(f"  F: {c['front']}")
    print(f"  B: {c['back']}")
