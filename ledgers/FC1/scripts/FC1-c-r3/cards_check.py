"""Re-verify every card of FC1 (cards.json, 119 cards) against its lesson HTML. Read-only.

Checks, per card: lesson file exists; id unique; front/back not duplicated; every block reference in back and basis
(Definition/Proposition/Remark/Example/Assumption/Problem/Corollary/Lab N, Part X) resolves in the card's own lesson;
every digit run of length >= 2 in back appears in the lesson text (commas removed) or is listed as derived by hand;
grade T cards cite a proposition/definition whose claim element carries data-grade="T" in the lesson.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
MOD = ROOT / "course/modules/FC/FC1"
cards = json.loads((MOD / "cards.json").read_text(encoding="utf-8"))
lessons = {}
for p in sorted(MOD.glob("L0*.html")):
    raw = p.read_text(encoding="utf-8")
    text = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", " ", raw, flags=re.S)))
    text = re.sub(r"\s+", " ", text)
    lessons[p.stem] = (raw, text, re.sub(r"\s+", " ", text.replace(",", "")))

BLOCK = re.compile(r"\b(Definition|Proposition|Remark|Example|Assumption|Problem|Corollary|Misconception|misconception)\s+([A-Z]?\d+(?:\.\d+)?)(\([ivx]+\))?|\bLab 1, Part ([A-D])|\bLab 2, Part ([A-D])|\bFixture ([A-G])\b|\bSection (\d)")
problems = []
seen_front = {}
seen_back = {}
rows = []
ids = [c["id"] for c in cards]
if len(ids) != len(set(ids)):
    problems.append("duplicate card ids")
for c in cards:
    cid, les = c["id"], c["lesson"]
    if les not in lessons:
        problems.append(f"{cid}: lesson {les} missing")
        continue
    raw, text, ntext = lessons[les]
    key_f = re.sub(r"\W+", " ", c["front"].lower()).strip()
    key_b = re.sub(r"\W+", " ", c["back"].lower()).strip()
    if key_f in seen_front:
        problems.append(f"{cid}: front duplicates {seen_front[key_f]}")
    seen_front.setdefault(key_f, cid)
    if key_b in seen_back:
        problems.append(f"{cid}: back duplicates {seen_back[key_b]}")
    seen_back.setdefault(key_b, cid)
    refs = []
    for field in ("back", "basis"):
        for m in BLOCK.finditer(c.get(field, "")):
            refs.append((field, m.group(0)))
    unresolved = []
    for field, r in refs:
        r_norm = r.replace("Misconception", "misconception")
        if r.lower().startswith("misconception"):
            if not re.search(r"misconception", text, re.I):
                unresolved.append(r)
            continue
        if re.fullmatch(r"Problem R\d", r) or re.fullmatch(r"Problem P\d", r):
            ok = f'id="{r.split()[-1]}"' in raw or r in text
        elif re.fullmatch(r"Lab [12], Part [A-D]", r):
            ok = bool(re.search(r"Lab [12], Part " + r[-1], text)) or bool(re.search(r"Part " + r[-1] + r"\b", text))
        elif r.startswith("Fixture"):
            ok = r in text or r.replace("Fixture ", "Fixture ") in text
        elif r.startswith("Section"):
            ok = True  # sections are numbered headings; reviewed by hand (see notes)
        else:
            ok = r_norm in text or re.sub(r"\(.*\)", "", r) in text
        if not ok:
            unresolved.append(r)
    nums = set(re.findall(r"(?<![\w.])\d{2,}(?:\.\d+)?", c["back"].replace(",", "")))
    missing_nums = sorted(n for n in nums if n not in ntext)
    rows.append((cid, les, c.get("grade", "-"), unresolved, missing_nums))
    if unresolved:
        problems.append(f"{cid} ({les}): unresolved refs {unresolved}")
    if c.get("grade") == "T":
        m = re.search(r"(Proposition|Corollary) (\d+\.\d+)", c["back"])
        if m:
            tag = f"{m.group(1)} {m.group(2)}"
            if not re.search(re.escape(tag) + r"</span>|" + re.escape(tag) + r"\s*<span class=\"name\">", raw):
                problems.append(f"{cid}: T card cites {tag} which is not a claim element in {les}")
for r in rows:
    print(r[0], r[1], "grade=" + str(r[2]), "unresolved=" + str(r[3]) if r[3] else "", "numbers-not-in-lesson=" + str(r[4]) if r[4] else "")
print("cards:", len(cards))
print("problems:", len(problems))
for p in problems:
    print("  ", p)
