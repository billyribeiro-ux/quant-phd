# For every card field, list each labelled reference ("Example 2.6", "Remark 1.4", "Problem R1", "Proposition 2.2(b)",
# "Section 4", "Assumption 1.3", ...) and check that the label is a heading in the lesson text it names (the card's own
# lesson, or the lesson the basis names). Labels not found in the card's own lesson are listed with the lessons that contain them.
import json
import re
import sys

cards = json.load(open(sys.argv[1], encoding="utf-8"))
texts = {f"L0{i}": open(f"{sys.argv[2]}/L0{i}.txt", encoding="utf-8").read() for i in range(1, 6)}
lab = re.compile(r"\b(Example|Remark|Problem|Proposition|Corollary|Definition|Assumption|Lab|Section|Misconception)\s+((?:[A-Z]\d|\d)(?:\.\d+)?)")
heads = {}
for lid, t in texts.items():
    heads[lid] = set()
    for m in re.finditer(r"^(Example|Remark|Problem|Proposition|Corollary|Definition|Assumption)\s+([A-Z]?\d+(?:\.\d+)?)\b", t, re.M):
        heads[lid].add(f"{m.group(1)} {m.group(2)}")
    for m in re.finditer(r"^([A-Z]\d) ·", t, re.M):
        heads[lid].add(f"Problem {m.group(1)}")
    for m in re.finditer(r"^(\d)(?:[A-Za-z])", t, re.M):
        heads[lid].add(f"Section {m.group(1)}")
missing = []
checked = 0
for c in cards:
    for f in ("front", "back", "basis"):
        for m in lab.finditer(c.get(f) or ""):
            kind, num = m.group(1), m.group(2)
            if kind in ("Lab", "Misconception"):
                continue
            key = f"{kind} {num}"
            checked += 1
            if key in heads.get(c["lesson"], set()):
                continue
            where = [l for l in texts if key in heads[l]]
            if not where:
                missing.append((c["id"], c["lesson"], f, key))
            else:
                missing.append((c["id"], c["lesson"], f, key, "found in " + ",".join(where)))
print("labels checked:", checked)
for x in missing:
    print("NOT IN OWN LESSON:", x)
print("unresolved (in no lesson):", sum(1 for x in missing if len(x) == 4))
