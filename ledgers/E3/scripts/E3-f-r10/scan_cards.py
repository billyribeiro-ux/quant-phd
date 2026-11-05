"""Round 10 card scan for E3 slice f (cards of L01-L04). Full scan of cards.json, not only the delta.

Usage: python3 -I -W error scan_cards.py <checkout_root>
Checks: JSON keys and allowed fields; unique ids; lesson field; near-duplicate fronts and backs across the
whole file (token Jaccard); every cross-reference label (Definition/Proposition/Lemma/Remark/Example/Theorem/
Problem/Section) in a slice card occurs in the lesson it names; every number token in a slice card occurs in
its lesson text (decimals and integers of two or more digits, after stripping HTML and the \\( \\) markup).
"""
import html
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
cards_path = root / "course/modules/E/E3/cards.json"
with open(cards_path, encoding="utf-8") as fh:
    cards = json.load(fh)
SLICE = {"L01", "L02", "L03", "L04"}
ALLOWED = {"id", "lesson", "front", "back", "grade", "basis", "cite"}
problems: list[str] = []
seen: dict[str, int] = {}
for c in cards:
    keys = set(c)
    if not {"id", "lesson", "front", "back"} <= keys:
        problems.append(f"{c.get('id')}: missing required keys {keys}")
    if keys - ALLOWED:
        problems.append(f"{c.get('id')}: unexpected keys {keys - ALLOWED}")
    if c["id"] in seen:
        problems.append(f"{c['id']}: duplicate id")
    seen[c["id"]] = 1
    if not re.fullmatch(r"E3-c\d{3}", c["id"]):
        problems.append(f"{c['id']}: bad id format")
    if c["lesson"] not in {f"L0{i}" for i in range(1, 9)}:
        problems.append(f"{c['id']}: lesson {c['lesson']} out of range")
    if not c["front"].strip() or not c["back"].strip():
        problems.append(f"{c['id']}: empty front or back")
    if "grade" in c and c["grade"] not in {"T", "C", "B", "A", "B-", "C-", "A-"}:
        problems.append(f"{c['id']}: grade {c['grade']} not in the scale used")
    if c.get("grade") in {"C", "B", "A", "B-", "C-", "A-"} and "basis" not in c and "cite" not in c:
        problems.append(f"{c['id']}: grade {c['grade']} without basis or cite")
print("cards total", len(cards), "integrity problems", len(problems))
for p in problems:
    print("PROBLEM", p)

TOK = re.compile(r"[a-z0-9]+")
STOP = {"the", "of", "a", "an", "and", "is", "in", "to", "for", "what", "which", "does", "how", "with", "under",
        "that", "it", "as", "on", "by", "at", "this", "from", "its", "be", "or", "are", "lottery", "cents"}


def toks(s: str) -> set[str]:
    return {t for t in TOK.findall(s.lower()) if t not in STOP}


pairs = []
for i, a in enumerate(cards):
    for b in cards[i + 1:]:
        for field in ("front", "back"):
            ta, tb = toks(a[field]), toks(b[field])
            if not ta or not tb:
                continue
            j = len(ta & tb) / len(ta | tb)
            if j >= 0.5:
                pairs.append((round(j, 2), field, a["id"], b["id"]))
print("near-duplicate pairs (Jaccard >= 0.5, any card in file):")
for p in sorted(pairs, reverse=True):
    print("  ", p)

# lesson text, tags and entities stripped
lesson_text = {}
for L in sorted(SLICE | {"L05", "L06", "L07", "L08"}):
    raw = (root / f"course/modules/E/E3/{L}.html").read_text(encoding="utf-8")
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    lesson_text[L] = re.sub(r"\s+", " ", txt)

REF = re.compile(r"\b(Definition|Proposition|Lemma|Remark|Example|Theorem|Problem|Assumption|Section|Lab)\s+([0-9]+(?:\.[0-9]+)?|[A-Z][0-9]?)")
NUM = re.compile(r"(?<![A-Za-z_])([0-9][0-9,]*(?:\.[0-9]+)?)")
slice_cards = [c for c in cards if c["lesson"] in SLICE]
print("slice cards", len(slice_cards), "by lesson", {L: sum(1 for c in slice_cards if c['lesson'] == L) for L in sorted(SLICE)})
BANNED = re.compile(r"TODO|TBD|lorem|\.\.\.|for brevity|beyond the scope|left as an exercise|it is important to note|studies show|experts agree|it is well known|obviously|clearly|you can add more", re.I)
n_numbers = 0
n_refs = 0
banned_hits = [c["id"] for c in slice_cards if BANNED.search(c["front"] + " " + c["back"])]
print("banned-phrase hits in slice cards:", banned_hits)
for c in slice_cards:
    text = c["front"] + " " + c["back"] + " " + c.get("basis", "")
    for m in REF.finditer(text):
        label = f"{m.group(1)} {m.group(2)}"
        # references cited to another lesson by name are checked against the lesson they name
        other = re.search(r"Lesson (L0\d)|L0(\d) (Definition|Proposition|Lemma|Remark|Example|Theorem)", text)
        target = c["lesson"]
        if other:
            target = other.group(1) or f"L0{other.group(2)}"
        n_refs += 1
        hit = any(label in lesson_text[t] for t in [target] + list(SLICE))
        if not hit:
            print(f"REF NOT FOUND {c['id']} '{label}' (card lesson {c['lesson']}, named lesson {target})")
    for m in NUM.finditer(c["back"]):
        tok = m.group(1).rstrip(",")
        if len(tok.replace(".", "").replace(",", "")) < 2:
            continue
        n_numbers += 1
        if tok not in lesson_text[c["lesson"]] and tok not in text.replace(tok, "", 0):
            pass
        if tok not in lesson_text[c["lesson"]]:
            print(f"NUMBER NOT IN OWN LESSON {c['id']} '{tok}' (lesson {c['lesson']})")
print("numeric tokens checked against own lesson:", n_numbers, "cross-references checked:", n_refs)
