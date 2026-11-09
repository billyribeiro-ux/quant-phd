"""Round 1 verifier checks for slice c (L07-L08): cards, card numbers vs lesson text, duplicates, scope words.

Standard library only. Run from the checkout root:
    .venv/bin/python -I ledgers/FC2/scripts/FC2-c-r1/v1_cards_and_prose.py
"""

from __future__ import annotations

import difflib
import html
import itertools
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
UNIT = ROOT / "course" / "modules" / "FC" / "FC2"


def visible(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", raw)
    text = html.unescape(text)
    text = text.replace("−", "-").replace("\\times", "x")
    return re.sub(r"\s+", " ", text)


def numbers(s: str) -> list[str]:
    s = s.replace("−", "-").replace("⁻", "-")
    s = re.sub(r"10\^\{?(-?\d+)\}?", lambda m: "1e" + m.group(1), s)
    s = re.sub(r"10⁻(\d+)", lambda m: "1e-" + m.group(1), s)
    s = re.sub(r"×\s*1e", "e", s)
    found = re.findall(r"\d+\.\d+|\d+", s)
    return [f for f in found if len(f) >= 2 and f not in {"10", "20", "12", "11", "13"}]


def main() -> None:
    cards = json.loads((UNIT / "cards.json").read_text(encoding="utf-8"))
    ids = [c["id"] for c in cards]
    print(f"cards total={len(cards)} unique_ids={len(set(ids))}")
    lessons = {"L07": visible(UNIT / "L07.html"), "L08": visible(UNIT / "L08.html")}
    slice_cards = [c for c in cards if c["lesson"] in lessons]
    print(f"slice cards (L07+L08) = {len(slice_cards)}: {[c['id'] for c in slice_cards]}")
    for c in slice_cards:
        text = lessons[c["lesson"]]
        back_nums = numbers(c["back"])
        missing = [n for n in back_nums if n not in text.replace(",", "")]
        print(
            f"{c['id']} {c['lesson']} grade={c.get('grade', '-')} basis={c.get('basis', '-')} "
            f"back_numbers={back_nums} not_in_lesson={missing}"
        )
    print("--- near-duplicates over the whole cards file (fronts or backs ratio > 0.6)")
    hits = []
    for a, b in itertools.combinations(cards, 2):
        r1 = difflib.SequenceMatcher(None, a["front"], b["front"]).ratio()
        r2 = difflib.SequenceMatcher(None, a["back"], b["back"]).ratio()
        if r1 > 0.6 or r2 > 0.6:
            hits.append((round(r1, 2), round(r2, 2), a["id"], b["id"], a["lesson"], b["lesson"]))
    for h in sorted(hits, reverse=True):
        print(h)
    print(f"near-duplicate pairs: {len(hits)}")
    print("--- scope words in L07 and L08 prose (word, count)")
    for name, text in lessons.items():
        words = re.findall(r"\b(every|all|only|any|always|never|exactly|same|shows?|proves?|unique)\b", text, flags=re.I)
        counts: dict[str, int] = {}
        for w in words:
            counts[w.lower()] = counts.get(w.lower(), 0) + 1
        print(name, dict(sorted(counts.items())))


if __name__ == "__main__":
    main()
