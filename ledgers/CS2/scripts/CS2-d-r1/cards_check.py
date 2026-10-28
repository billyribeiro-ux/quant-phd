"""Card checks for CS2 (verifier scratch): grade/basis/cite presence, and every number on a card found in its lesson text."""
import html, json, re, sys
from collections import Counter
root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/CS/CS2/cards.json"))
print("cards", len(cards))
print("grade counts", Counter(c.get("grade", "(none)") for c in cards))
print("basis present", sum(1 for c in cards if c.get("basis")), "cite present", sum(1 for c in cards if c.get("cite")))
bad = [c["id"] for c in cards if c.get("grade", "T") != "T" and not (c.get("basis") or c.get("cite"))]
print("non-T without basis/cite:", bad)
lessontext = {}
for L in sorted({c["lesson"] for c in cards}):
    raw = open(f"{root}/course/modules/CS/CS2/{L}.html", encoding="utf-8").read()
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    lessontext[L] = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    lessontext[L] = re.sub(r"\s+", " ", lessontext[L])
missing = []
for c in cards:
    text = c["front"] + " " + c["back"]
    nums = set(re.findall(r"(?<![A-Za-z_])\d+(?:\.\d+)?", text))
    for n in nums:
        if n not in lessontext[c["lesson"]] and n not in lessontext["L01"] :
            missing.append((c["id"], c["lesson"], n))
        elif n not in lessontext[c["lesson"]]:
            missing.append((c["id"], c["lesson"], n))
print("numbers on cards not found in their lesson text:", len(missing))
for m in missing[:60]:
    print("  ", m)
