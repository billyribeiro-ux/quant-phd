"""Scan a cards.json for duplicate ids, exact duplicate fronts or backs, and near-duplicate fronts or backs.

Usage: python3 -I card_scan_r16.py <cards.json>
"""

import json
import re
import sys
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def main() -> None:
    cards = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    ids = Counter(c["id"] for c in cards)
    print(f"cards {len(cards)} unique_ids {len(ids)} duplicate_ids {[i for i, n in ids.items() if n > 1]}")
    print("lesson counts", dict(sorted(Counter(c["lesson"] for c in cards).items())))
    print("grade counts", dict(sorted(Counter(str(c.get("grade")) for c in cards).items())))
    for field in ("front", "back"):
        seen: dict[str, str] = {}
        for c in cards:
            key = norm(c[field])
            if key in seen:
                print(f"EXACT_DUP {field}: {seen[key]} and {c['id']}")
            else:
                seen[key] = c["id"]
    for field in ("front", "back"):
        pairs = []
        for i, a in enumerate(cards):
            for b in cards[i + 1 :]:
                ratio = SequenceMatcher(None, norm(a[field]), norm(b[field])).ratio()
                if ratio >= 0.75:
                    pairs.append((round(ratio, 3), a["id"], b["id"]))
        pairs.sort(reverse=True)
        print(f"NEAR_DUP {field} (ratio>=0.75): {len(pairs)} pairs")
        for ratio, a, b in pairs[:40]:
            print(f"  {ratio} {a} {b}")


if __name__ == "__main__":
    main()
