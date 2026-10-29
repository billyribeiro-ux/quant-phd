"""Dump cards.json one card per line for the full read (id | lesson | front | back)."""
import json
import sys
from pathlib import Path

cards = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
Path(sys.argv[2]).write_text(
    "\n".join(f"{c['id']} | {c['lesson']} | F: {c['front']} | B: {c['back']}" for c in cards), encoding="utf-8"
)
print(len(cards), len({c["id"] for c in cards}))
