"""Verifier M5-d round 1: automated card audit for course/modules/M/M5/cards.json.

Checks: every card's lesson page exists; every number token in front/back appears in that lesson's visible text;
duplicate fronts; and the registry entries cited by the project page (abbott2015understanding, rudin1976principles).
"""

from __future__ import annotations

import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
M5 = ROOT / "course/modules/M/M5"


def visible(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text))


def main() -> int:
    cards = json.loads((M5 / "cards.json").read_text(encoding="utf-8"))
    print("cards", len(cards))
    fronts = Counter(c["front"].strip().lower() for c in cards)
    dups = [f for f, n in fronts.items() if n > 1]
    print("duplicate fronts", dups)
    ids = Counter(c["id"] for c in cards)
    print("duplicate ids", [i for i, n in ids.items() if n > 1])
    lessons = Counter(c["lesson"] for c in cards)
    print("cards per lesson", dict(sorted(lessons.items())))
    missing_num: list[str] = []
    missing_page: list[str] = []
    cache: dict[str, str] = {}
    for c in cards:
        page = M5 / f"{c['lesson']}.html"
        if not page.exists():
            missing_page.append(c["id"])
            continue
        if c["lesson"] not in cache:
            cache[c["lesson"]] = visible(page)
        text = cache[c["lesson"]]
        for field in ("front", "back"):
            for tok in re.findall(r"\d+(?:\.\d+)?", c[field]):
                if tok not in text:
                    missing_num.append(f"{c['id']}.{field}:{tok}")
    print("missing lesson pages", missing_page)
    print("number tokens absent from the lesson text", len(missing_num), missing_num[:40])
    reg = json.loads((ROOT / "references/references.json").read_text(encoding="utf-8"))
    entries = reg["entries"]
    keys = {e.get("key") or e.get("id"): e for e in entries} if isinstance(entries, list) else entries
    for k in ("abbott2015understanding", "rudin1976principles"):
        print(k, "registry:", json.dumps(keys.get(k), ensure_ascii=False)[:300])
    return 0


if __name__ == "__main__":
    sys.exit(main())
