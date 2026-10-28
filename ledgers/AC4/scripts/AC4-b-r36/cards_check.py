"""Check every digit string on the L03 and L04 card backs appears in the html-stripped lesson text."""

import html
import json
import re
import sys

root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/AC/AC4/cards.json", encoding="utf-8"))


def strip(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        s = fh.read()
    s = re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", s))


text = {t: strip(f"{root}/course/modules/AC/AC4/{t}.html") for t in ("L03", "L04")}
slice_cards = [c for c in cards if c["lesson"] in ("L03", "L04")]
missing = []
for c in slice_cards:
    for d in set(re.findall(r"\d[\d,.]*\d|\d", c["back"])):
        d = d.rstrip(".,")
        if d not in text[c["lesson"]]:
            missing.append((c["id"], d))
print("slice cards", len(slice_cards), "missing digit strings", missing)
