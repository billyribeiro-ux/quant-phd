"""Round-8 mechanical card check for M2: ids, lessons, grades/basis, duplicate fronts, numbers and labels against each lesson's text."""
import json
import re
import sys
from collections import Counter
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(sys.argv[1])
MOD = ROOT / "course/modules/M/M2"


class Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag: str, attrs: list) -> None:  # type: ignore[type-arg]
        if tag in ("script", "style"):
            self.skip += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)


def lesson_text(lesson: str) -> str:
    p = Text()
    p.feed((MOD / f"{lesson}.html").read_text(encoding="utf-8"))
    return re.sub(r"\s+", " ", unescape(" ".join(p.parts)))


cards = json.load(open(MOD / "cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards:", len(cards), "unique ids:", len(set(ids)), "dup ids:", [i for i, k in Counter(ids).items() if k > 1])
print("key sets:", Counter(tuple(sorted(c)) for c in cards))
print("grades:", Counter(c.get("grade") for c in cards))
bad_grade = [c["id"] for c in cards if c.get("grade") not in (None, "T", "C")]
c_nobasis = [c["id"] for c in cards if c.get("grade") == "C" and not c.get("basis")]
t_basis = [c["id"] for c in cards if c.get("grade") == "T" and c.get("basis")]
print("bad grade:", bad_grade, "C without basis:", c_nobasis, "T with basis:", t_basis)
fronts = Counter(re.sub(r"\W+", " ", c["front"].lower()).strip() for c in cards)
print("duplicate fronts:", [f for f, k in fronts.items() if k > 1])
print("id sequence gaps/ordering:", sorted(set(int(i.split("c")[1]) for i in ids) ^ set(range(1, 389))))
lessons = {c["lesson"] for c in cards}
print("lessons:", len(lessons), "missing files:", [l for l in lessons if not (MOD / f"{l}.html").exists()])

num = re.compile(r"(?<![\w.])-?\d+(?:/\d+)?(?:\.\d+)?(?![\w])")
texts: dict[str, str] = {}
miss_num = []
label = re.compile(r"\b(Proposition|Theorem|Lemma|Corollary|Example|Remark|Definition|Assumption|Problem|Misconception|Section)\s+((?:L\d\d-)?[A-Z]?\d+(?:[.-][A-Z]?\d+)*)")
miss_label = []
n_labels = 0
for c in cards:
    t = texts.setdefault(c["lesson"], lesson_text(c["lesson"]))
    for field in ("front", "back", "basis"):
        for tok in num.findall(c.get(field, "") or ""):
            if tok not in t and tok.lstrip("-") not in t:
                miss_num.append((c["id"], field, tok))
    for kind, lab in set(label.findall(" ".join(c.get(f, "") or "" for f in ("front", "back")))):
        n_labels += 1
        if kind in ("Misconception",):
            ok = "Misconception" in t
        elif kind == "Section":
            ok = bool(re.search(rf"(§{re.escape(lab.split('.')[0])}\b|Section {re.escape(lab)}\b)", t)) or "§" in t
        elif kind == "Problem":
            ok = bool(re.search(rf"\b{re.escape(lab)}\b", t))
        else:
            ok = bool(re.search(rf"\b{kind}\s+{re.escape(lab)}\b", t))
        if not ok:
            miss_label.append((c["id"], c["lesson"], f"{kind} {lab}"))
print("numbers not found in own lesson:", len(miss_num))
for m in miss_num[:80]:
    print("  ", m)
print("labels checked:", n_labels, "unmatched:", len(miss_label))
for m in miss_label:
    print("  ", m)
