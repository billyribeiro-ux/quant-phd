"""Round-17 AC4-b verifier helper: visible-text extraction of L03/L04 and the cards delta since d57df1e.

Run from the checkout root: .venv/bin/python -I ledgers/AC4/scripts/AC4-b-r17/card_delta_and_text.py
Writes the extracted text to /tmp/AC4-v/AC4-b/ (scratch) and prints the card delta for lessons L03/L04.
"""

import html
import json
import re
import subprocess
from pathlib import Path

ROOT = Path.cwd()
SCRATCH = Path("/tmp/AC4-v/AC4-b")
SCRATCH.mkdir(parents=True, exist_ok=True)

for name in ("L03", "L04"):
    raw = (ROOT / f"course/modules/AC/AC4/{name}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>", "", raw, flags=re.S)
    raw = re.sub(r"<style.*?</style>", "", raw, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", "", raw))
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    (SCRATCH / f"{name}.txt").write_text("\n".join(lines), encoding="utf-8")
    print(name, len(lines), "lines")

new = {c["id"]: c for c in json.loads((ROOT / "course/modules/AC/AC4/cards.json").read_text(encoding="utf-8"))}
old_raw = subprocess.run(
    ["git", "show", "d57df1e:course/modules/AC/AC4/cards.json"], capture_output=True, text=True, check=True
).stdout
old = {c["id"]: c for c in json.loads(old_raw)}
for cid in sorted(set(old) | set(new)):
    card = new.get(cid)
    if card is None or card["lesson"] not in ("L03", "L04"):
        continue
    if cid not in old:
        print("NEW", cid, card["lesson"])
    elif old[cid] != card:
        print("CHANGED", cid, card["lesson"])
print("removed", [k for k in old if k not in new])
