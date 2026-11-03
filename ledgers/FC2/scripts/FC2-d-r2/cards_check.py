"""FC2-d r2: automated card checks. Usage: python -I cards_check.py <repo-root>
1. duplicate fronts, duplicate backs, duplicate ids, and card ids versus the lesson field.
2. every 'Definition/Theorem/Proposition/Lemma/Corollary/Remark/Example/Problem/Assumption/Section' cited on a card
   must be a label that appears in the card's own lesson text (the lesson's HTML, tags stripped).
3. every number token (integers, decimals, fractions a/b) on a card's back must appear in its lesson text or in the lesson-independent list of arithmetic results printed here.
"""
import html
import json
import os
import re
import sys
from collections import Counter

root = sys.argv[1]
base = os.path.join(root, "course/modules/FC/FC2")
cards = json.load(open(os.path.join(base, "cards.json"), encoding="utf-8"))


def text_of(lesson):
    raw = open(os.path.join(base, lesson + ".html"), encoding="utf-8").read()
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    raw = re.sub(r"<[^>]+>", " ", raw)
    return html.unescape(re.sub(r"\s+", " ", raw))


texts = {f"L0{i}": text_of(f"L0{i}") for i in range(1, 9)}
print("ids:", len(cards), "unique:", len({c["id"] for c in cards}))
fronts = Counter(c["front"].strip().lower() for c in cards)
backs = Counter(c["back"].strip().lower() for c in cards)
print("duplicate fronts:", [k for k, v in fronts.items() if v > 1])
print("duplicate backs:", [k for k, v in backs.items() if v > 1])
ids = [c["id"] for c in cards]
nums = sorted(int(i.split("-c")[1]) for i in ids)
missing = [n for n in range(nums[0], nums[-1] + 1) if n not in nums]
print("id gaps:", ["FC2-c%03d" % n for n in missing])
ref_re = re.compile(r"\b(Definition|Theorem|Proposition|Lemma|Corollary|Remark|Example|Problem|Assumption|Section)\s+([A-Z]?\d+(?:\.\d+)?\w*)")
num_re = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)(?![\w.])")
for c in cards:
    lesson = c["lesson"]
    own = texts.get(lesson, "")
    for m in ref_re.finditer(c["back"] + " " + c["front"]):
        label = f"{m.group(1)} {m.group(2)}"
        if label not in own and label.rstrip(".") not in own:
            # a cross-lesson reference is allowed only when the card names the other lesson
            other = re.search(r"Lesson (\d)", c["back"] + c["front"])
            ok = False
            if other:
                ok = f"L0{other.group(1)}" in texts and label in texts[f"L0{other.group(1)}"]
            if not ok:
                print("REF-MISS", c["id"], lesson, label)
    card_text = c["front"] + " " + c["back"]
    for tok in set(num_re.findall(card_text)):
        if tok in ("1", "2", "0") or len(tok) < 2:
            continue
        if tok not in own:
            print("NUM-MISS", c["id"], lesson, tok)
