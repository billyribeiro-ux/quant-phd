"""Round-10: where each E3 reading-list key is cited (data-cite or text) in the E3 lessons and project page, and the
registry record fields for those keys (read from references/references.json)."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
KEYS = ["pratt1964risk", "kahneman1979prospect", "epstein1989substitution", "ellsberg1961risk", "gilboa1989maxmin"]
pages = sorted((ROOT / "course/modules/E/E3").glob("*.html"))
for key in KEYS:
    hits = []
    for p in pages:
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if key in line:
                plain = re.sub(r"<[^>]+>", "", line).strip()
                hits.append(f"{p.name}:{i} {'[data-cite]' if 'data-cite' in line else ''} {plain[:110]}")
    print(f"== {key}")
    for h in hits:
        print("   ", h)
data = json.loads((ROOT / "references/references.json").read_text(encoding="utf-8"))
recs = data.get("entries", data) if isinstance(data, dict) else data
if isinstance(recs, dict):
    recs = [dict(v, key=k) for k, v in recs.items()]
for r in recs:
    if r.get("key") in KEYS:
        print({k: r.get(k) for k in ("key", "title", "year", "venue", "journal", "authors", "doi") if k in r})
