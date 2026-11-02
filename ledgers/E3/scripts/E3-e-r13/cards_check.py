"""E3-e round 10: structural and number checks on course/modules/E/E3/cards.json (run with python -I)."""
import collections
import html
import json
import re
import sys

ROOT = sys.argv[1]
d = json.load(open(f"{ROOT}/course/modules/E/E3/cards.json", encoding="utf-8"))
print("cards", len(d))
print("dup ids", [i for i, n in collections.Counter(c["id"] for c in d).items() if n > 1])
print("dup fronts", [k for k, n in collections.Counter(c["front"].strip().lower() for c in d).items() if n > 1])
print("grades", collections.Counter(c.get("grade") for c in d))
text = {}
for L in sorted({c["lesson"] for c in d}):
    h = open(f"{ROOT}/course/modules/E/E3/{L}.html", encoding="utf-8").read()
    h = re.sub(r"<script.*?</script>|<style.*?</style>", "", h, flags=re.S)
    text[L] = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)))
miss = []
for c in d:
    for n in set(re.findall(r"\d+(?:\.\d+)?", c["back"])):
        if n not in text[c["lesson"]]:
            miss.append((c["id"], n))
print("card numbers absent from own lesson", miss)
labref = []
for c in d:
    for kind, num in set(re.findall(r"\b(Definition|Proposition|Theorem|Lemma|Remark|Example|Problem|Observation|Corollary|Model)s? ([0-9A-Z]+(?:\.[0-9]+)?)", c["back"] + " " + c["front"])):
        if not re.search(kind + r"s?\s+" + re.escape(num) + r"\b", text[c["lesson"]]):
            labref.append((c["id"], kind, num))
print("labelled results absent from own lesson", labref)
