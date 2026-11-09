"""FC2 slice b round 2: cards (L04-L06) and page hygiene checks, run from the checkout.

Run: .venv/bin/python -I -W error ledgers/FC2/scripts/FC2-b-r2/v2_cards_and_hygiene.py <checkout> <round1_cards.json>
<round1_cards.json> is `git show aeb512b6:course/modules/FC/FC2/cards.json` (the round-1 pin).
"""

from __future__ import annotations

import collections
import difflib
import glob
import html
import json
import os
import re
import sys

ROOT = sys.argv[1]
OLD_CARDS = sys.argv[2]
FC2 = os.path.join(ROOT, "course", "modules", "FC", "FC2")


def read(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


cards_all = json.loads(read(os.path.join(FC2, "cards.json")))
old_all = json.loads(read(OLD_CARDS))
slice_cards = [c for c in cards_all if c["lesson"] in ("L04", "L05", "L06")]
print(f"cards: total={len(cards_all)} L04-L06={len(slice_cards)} "
      f"per lesson={dict(collections.Counter(c['lesson'] for c in slice_cards))}")

# 1. cited locators exist in the cited lesson (Definition/Theorem/Proposition/Remark/Example/Lemma/Corollary/Problem)
pages = {}
for L in ("L04", "L05", "L06"):
    pages[L] = html.unescape(re.sub(r"<[^>]+>", " ", read(os.path.join(FC2, L + ".html"))))
pat = re.compile(r"\b(Definition|Theorem|Proposition|Remark|Example|Lemma|Corollary|Problem)\s+(\d+\.\d+|[A-Z]\d)")
missing = []
for c in slice_cards:
    text = c["front"] + " " + c["back"] + " " + c.get("basis", "")
    for m in pat.finditer(text):
        tail = text[m.end(): m.end() + 30]
        lm = re.search(r"of Lesson (\d)", tail)
        lesson = "L0" + lm.group(1) if lm else c["lesson"]
        if lesson not in pages:
            continue
        if not re.search(r"\b%s\s+%s\b" % (m.group(1), re.escape(m.group(2))), pages[lesson]):
            missing.append((c["id"], m.group(0), lesson))
print("cited locators missing from their lesson:", missing or "none")

# 2. full-file duplicate ids and fronts; near-duplicates among the slice and the whole unit
ids = [c["id"] for c in cards_all]
print("duplicate ids in cards.json:", len(ids) - len(set(ids)))
fr = collections.Counter(c["front"].strip().lower() for c in cards_all)
print("duplicate fronts in cards.json:", [k for k, v in fr.items() if v > 1] or "none")
near = []
for a in slice_cards:
    for b in cards_all:
        if b["id"] == a["id"]:
            continue
        rf = difflib.SequenceMatcher(None, a["front"].lower(), b["front"].lower()).ratio()
        rb = difflib.SequenceMatcher(None, a["back"].lower(), b["back"].lower()).ratio()
        if rf > 0.9 and rb > 0.9:
            near.append((a["id"], b["id"]))
print("near-duplicate pairs (front>0.9 and back>0.9):", sorted(set(tuple(sorted(p)) for p in near)) or "none")

# 3. delta of L04-L06 cards against the round-1 pin
om = {c["id"]: c for c in old_all}
nm = {c["id"]: c for c in cards_all}
changed = sorted(i for i in set(om) & set(nm) if om[i] != nm[i] and nm[i]["lesson"] in ("L04", "L05", "L06"))
removed = sorted(i for i in set(om) - set(nm) if om[i]["lesson"] in ("L04", "L05", "L06"))
added = sorted(i for i in set(nm) - set(om) if nm[i]["lesson"] in ("L04", "L05", "L06"))
print("L04-L06 cards changed since round-1 pin:", changed)
print("L04-L06 cards removed since round-1 pin:", removed or "none")
print("L04-L06 cards added since round-1 pin:", added)
for i in changed:
    for k in sorted(set(om[i]) | set(nm[i])):
        if om[i].get(k) != nm[i].get(k):
            print(f"   {i}.{k}: {om[i].get(k)!r} -> {nm[i].get(k)!r}")

# 4. grade rule (ruling 9): T cards must not rest only on lab output
for c in slice_cards:
    basis = c.get("basis", "")
    if c.get("grade") == "T" and "Lab" in basis and not re.search(r"Example|Problem|Section", basis):
        print("T card with lab-only basis:", c["id"], basis)

# 5. why-it-matters: word counts and the r >= 0 hypothesis on the American-call equality
for L in ("L04", "L05", "L06"):
    s = read(os.path.join(FC2, L + ".html"))
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', s, re.S)
    t = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
    print(f"{L} why-it-matters words={len(t.split())}")
    if "American call" in t:
        sentence = [x for x in re.split(r"(?<=[.])\s", t) if "American call" in x]
        print(f"   {L} sentence with American call: {sentence}")
        print(f"   {L} sentence states a non-negative rate: "
              f"{bool(re.search(r'non-negative rate|r ≥ 0', ' '.join(sentence)))}")

# 6. hours: lessons sum and hub split
hours = {}
for L in ("L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08"):
    hours[L] = int(re.search(r'data-hours="(\d+)"', read(os.path.join(FC2, L + ".html"))).group(1))
hub = read(os.path.join(FC2, "index.html"))
print("lesson hours:", hours, "sum", sum(hours.values()),
      "hub lessons/project:", re.search(r'data-hours-lessons="(\d+)"', hub).group(1),
      re.search(r'data-hours-project="(\d+)"', hub).group(1))

# 7. banned phrases and process words in the three pages
banned = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "it can be shown", "builder", "verifier", "round ", "architect", "previous draft"]
for L in ("L04", "L05", "L06"):
    prose = html.unescape(re.sub(r"<[^>]+>", " ", read(os.path.join(FC2, L + ".html")))).lower()
    hits = [b for b in banned if b.lower() in prose]
    print(f"{L} banned or process phrase hits: {hits or 'none'}")

# 8. dfn terms of the unit defined twice (plain or concept), across all course modules
terms = collections.defaultdict(list)
for f in glob.glob(os.path.join(ROOT, "course", "modules", "**", "*.html"), recursive=True):
    for m in re.finditer(r"<dfn([^>]*)>(.*?)</dfn>", read(f), re.S):
        t = html.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip().lower()
        terms[t].append(os.path.relpath(f, os.path.join(ROOT, "course", "modules")))
fc2_terms = {t: v for t, v in terms.items() if any("FC/FC2" in x for x in v)}
print("FC2 dfn terms defined more than once across modules:",
      {t: v for t, v in fc2_terms.items() if len(v) > 1} or "none")
print("FC2 dfn terms defined in L04-L06:", sorted(t for t, v in fc2_terms.items()
                                               if any(x.endswith(("L04.html", "L05.html", "L06.html")) for x in v)))
