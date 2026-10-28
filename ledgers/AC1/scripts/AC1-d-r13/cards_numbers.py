"""For every card in AC1 cards.json: lists each number in front/back and whether it appears in the card's own lesson text."""

import html
import json
import re
import sys

ROOT = "/tmp/verify13-AC1-d/course/modules/AC/AC1/"


def text_of(lesson: str) -> str:
    raw = open(ROOT + lesson + ".html", encoding="utf-8").read()
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    raw = re.sub(r"<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", html.unescape(raw))


cards = json.load(open(ROOT + "cards.json", encoding="utf-8"))
only = set(sys.argv[1:])
for card in cards:
    if only and card["lesson"] not in only:
        continue
    lesson = text_of(card["lesson"])
    nums = re.findall(r"\d[\d,]*(?:\.\d+)?", card["front"] + " " + card["back"])
    missing = [n for n in nums if n not in lesson and n.rstrip(",") not in lesson]
    print(card["id"], card["lesson"], "numbers:", nums, "MISSING:" if missing else "", missing if missing else "")
