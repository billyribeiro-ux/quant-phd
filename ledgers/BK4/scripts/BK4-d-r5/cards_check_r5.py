"""Round-4 mechanical checks of course/modules/BK/BK4/cards.json against the lesson pages (stdlib only).

Usage: python3 -I ledgers/BK4/scripts/BK4-d-r5/cards_check_r4.py <repo-root>
Prints: structure (ids, lessons, grades, bases, cites), number tokens absent from the named lesson text,
cross-reference tokens absent from the named lesson text, exact duplicate fronts/backs, front pairs with token
Jaccard >= 0.5, banned/process-word hits, and every symbol-like token in cards for review.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("extract_text", root / "ledgers/BK4/scripts/BK4-d-r5/extract_text.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def text_of(path):
    r = mod.Render()
    r.feed(Path(path).read_text(encoding="utf-8"))
    return " ".join("".join(r.out).split())


cards = json.loads((root / "course/modules/BK/BK4/cards.json").read_text(encoding="utf-8"))
lessons = {p: text_of(root / f"course/modules/BK/BK4/{p}.html") for p in ("L01", "L02", "L03", "L04", "L05")}
ids = [c["id"] for c in cards]
print("cards:", len(cards), "distinct ids:", len(set(ids)))
print("ids regex ok:", all(re.fullmatch(r"BK4-c\d{3}", i) for i in ids), "sorted:", ids == sorted(ids))
print("keys per card:", sorted({tuple(sorted(c.keys())) for c in cards}))
print("per lesson:", {l: sum(1 for c in cards if c["lesson"] == l) for l in lessons})
print("grades:", {g: sum(1 for c in cards if c.get("grade") == g) for g in ("T", "C", None)})
for c in cards:
    g = c.get("grade")
    if g is None and c.get("basis") is not None:
        print("BASIS WITHOUT GRADE", c["id"])
    if g in ("T", "C") and not str(c.get("basis", "")).strip():
        print("GRADED WITHOUT BASIS", c["id"])
    if g not in (None, "T", "C", "A", "B", "D", "X"):
        print("BAD GRADE", c["id"], g)
    if g and g != "T" and not (c.get("cite") or str(c.get("basis", "")).strip()):
        print("NON-T WITHOUT CITE OR BASIS", c["id"])
    for k in c.get("cite", []):
        print("CITE", c["id"], k)

print("\n== number tokens not found verbatim in the named lesson text ==")
num_re = re.compile(r"(?<![A-Za-z_\w.])(\d[\d,]*(?:\.\d+)?(?:/\d+)?)")
miss = []
for c in cards:
    lt = lessons[c["lesson"]]
    for field in ("front", "back", "basis"):
        for tok in num_re.findall(str(c.get(field, ""))):
            t = tok.rstrip(",")
            if t not in lt:
                miss.append((c["id"], field, t))
for m in miss:
    print(*m)
print("count:", len(miss))

print("\n== cross-reference tokens not found in the named lesson text ==")
xref_re = re.compile(r"\b(Definition|Proposition|Remark|Example|Problem|Corollary|Assumption|Lab \d|Assumptions)\s+(?:[A-Z]?\d+(?:\.\d+)?|\d)(?:\(\w\))?")
bad = []
for c in cards:
    lt = lessons[c["lesson"]]
    for field in ("front", "back", "basis"):
        for m in xref_re.finditer(str(c.get(field, ""))):
            tok = m.group(0)
            if tok in lt:
                continue
            other = [l for l, t in lessons.items() if tok in t]
            bad.append((c["id"], c["lesson"], field, tok, other))
for b in bad:
    print(*b)
print("count:", len(bad))

print("\n== duplicates ==")
fronts, backs = {}, {}
for c in cards:
    fronts.setdefault(c["front"], []).append(c["id"])
    backs.setdefault(c["back"], []).append(c["id"])
print("exact duplicate fronts:", [v for v in fronts.values() if len(v) > 1])
print("exact duplicate backs:", [v for v in backs.values() if len(v) > 1])


def toks(s):
    return set(re.findall(r"[a-z0-9]+", s.lower()))


pairs = []
for i, a in enumerate(cards):
    for b in cards[i + 1:]:
        ta, tb = toks(a["front"]), toks(b["front"])
        j = len(ta & tb) / max(1, len(ta | tb))
        if j >= 0.5:
            pairs.append((round(j, 2), a["id"], b["id"]))
print("front pairs with token Jaccard >= 0.5:", len(pairs))
for p in sorted(pairs, reverse=True):
    print(*p)

print("\n== banned or process words in cards ==")
banned = re.compile(r"TODO|TBD|lorem|\.\.\.|…|for brevity|details omitted|beyond the scope|left as an exercise|"
                    r"you can add|it is important to note|studies show|experts agree|well known|obviously|clearly|"
                    r"\bwe (?:now|then)\b|\bthe reader\b|\bstudents?\b|\bthis unit\b", re.I)
hits = [(c["id"], m.group(0)) for c in cards for f in ("front", "back", "basis") for m in banned.finditer(str(c.get(f, "")))]
print("hits:", hits)

print("\n== symbol-like tokens (for notation review) ==")
sym = re.compile(r"[Ͱ-Ͽἀ-῿]|\b[A-Za-z]\^\{?\\?ast|\\[A-Za-z]+|\b[A-Z]_[a-z0-9]|\b(?:Var|Prob|E)\b")
seen = {}
for c in cards:
    for f in ("front", "back", "basis"):
        for m in sym.finditer(str(c.get(f, ""))):
            seen.setdefault(m.group(0), set()).add(c["id"])
for k in sorted(seen):
    print(repr(k), len(seen[k]))
