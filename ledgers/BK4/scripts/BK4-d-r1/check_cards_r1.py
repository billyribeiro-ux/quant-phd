# BK4 slice d, round 1 (verifier F31): cards.json delta and card-level checks, pin 95f3f8cb vs base e919577b.
import difflib
import json
import re
import subprocess
import sys
from fractions import Fraction

ROOT = "/Users/billyribeiro/.fanout/wt/verifyF31-BK4-d"
BASE = "e919577b45b431ce68e1e6533b00b8a301277937"
OUT = ROOT + "/ledgers/BK4/scripts/BK4-d-r1/out/"


def strip(name):
    return subprocess.run(
        [sys.executable, "-I", ROOT + "/ledgers/BK4/scripts/BK4-d-r1/strip.py", ROOT + "/course/modules/BK/BK4/" + name],
        capture_output=True,
        text=True,
        check=True,
    ).stdout


lessons = {n: strip(f"{n}.html") for n in ["L01", "L02", "L03", "L04", "L05"]}
cur = json.load(open(ROOT + "/course/modules/BK/BK4/cards.json", encoding="utf-8"))
base_raw = subprocess.run(
    ["git", "-C", ROOT, "show", f"{BASE}:course/modules/BK/BK4/cards.json"], capture_output=True, text=True, check=True
).stdout
base = json.loads(base_raw)
cur_by = {c["id"]: c for c in cur}
base_by = {c["id"]: c for c in base}
added = sorted(set(cur_by) - set(base_by))
removed = sorted(set(base_by) - set(cur_by))
modified = sorted(i for i in set(cur_by) & set(base_by) if cur_by[i] != base_by[i])
unchanged = sorted(i for i in set(cur_by) & set(base_by) if cur_by[i] == base_by[i])
print("cards: base", len(base), "current", len(cur), "unique", len({c['id'] for c in cur}))
print("added:", added)
print("removed:", removed)
print("modified:", modified)
print("unchanged count:", len(unchanged))
for i in modified:
    for k in cur_by[i]:
        if cur_by[i][k] != base_by[i].get(k):
            print(f"  {i} field {k} changed")
print("fields of current cards:", sorted({k for c in cur for k in c}))
print("lesson of current cards:", {l: sum(1 for c in cur if c['lesson'] == l) for l in ['L01', 'L02', 'L03', 'L04', 'L05']})
print("grades:", {g: sum(1 for c in cur if c.get('grade') == g) for g in ['T', 'C', None]})
# ungraded cards must carry no grade key; graded must have basis
bad = [c["id"] for c in cur if ("grade" in c) != ("basis" in c)]
print("grade/basis presence mismatch:", bad)
refs = json.load(open(ROOT + "/references/references.json", encoding="utf-8"))
keys = {e["key"]: e for e in refs["entries"]}
for c in cur:
    for k in c.get("cite", []):
        e = keys.get(k)
        print("cite", c["id"], k, "found" if e else "MISSING", (e or {}).get("used_by"))

# Changed and added cards: label references must exist in their lesson text
labels = re.compile(r"(Proposition|Example|Remark|Problem|Definition|Assumption|Corollary|Lab 1|Lab 2|Lab 3|Section|Part|Assumptions)\s+([A-Z]?[0-9.]+[a-z]?|[A-Z][0-9]|[A-Z]\b)")
print("--- label references in changed/added cards")
for i in added + modified:
    c = cur_by[i]
    text = c["front"] + " " + c["back"] + " " + c.get("basis", "")
    refs_found = sorted(set(m.group(0) for m in labels.finditer(text)))
    lesson_text = lessons[c["lesson"]]
    for r in refs_found:
        ok = r in lesson_text
        print(i, c["lesson"], repr(r), "in lesson" if ok else "NOT IN LESSON TEXT")

# Every number on a changed or added card must appear in its lesson text (rule 10)
numtok = re.compile(r"\d[\d,./]*\d|\d")
print("--- numbers on changed/added cards vs lesson text")
for i in added + modified:
    c = cur_by[i]
    text = c["front"] + " " + c["back"] + " " + c.get("basis", "")
    nums = sorted(set(m.group(0).rstrip(".,") for m in numtok.finditer(text)))
    lt = lessons[c["lesson"]]
    missing = [n for n in nums if n not in lt]
    print(i, "numbers:", nums, "missing from lesson:", missing)

# Exact arithmetic on the changed cards' numbers
print("--- exact checks")
print("c012 share 1533900/2841600 =", Fraction(1533900, 2841600), float(Fraction(1533900, 2841600)), "round4", round(1533900 / 2841600, 4))
print("c012 gross check 2841600 =", 2841600, "moved", 1533900)
print("c089 1-(7/8)^3 =", 1 - Fraction(7, 8) ** 3, "=169/512 ?", 1 - Fraction(7, 8) ** 3 == Fraction(169, 512))
print("c089 3p=3/8 =192/512 ?", Fraction(3, 8) == Fraction(192, 512), "p=1/8 =64/512 ?", Fraction(1, 8) == Fraction(64, 512))
for p in [Fraction(k, 1000) for k in range(1, 1000)]:
    if (1 - (1 - p) ** 3) == 3 * p or p == 3 * p:
        print("EQUALITY FOUND at p", p)
print("c089 0<p<1 scan: 3p equals neither law at 999 rational p in (0,1)")
p = Fraction(1, 8)
print("c088 A4 mean p*k*sum(l)=", p * 2500 * (1 + 2 + 4), "exact cents 4375/2 =", Fraction(4375, 2), "half-up", (Fraction(4375, 2) + Fraction(1, 2)).__floor__())
# c088: under A3 the mean is p*kappa*sum(l) by Proposition 2.2 enumeration; check by enumeration with random rational p, kappa, l
import itertools
ok = True
for pp in [Fraction(1, 8), Fraction(1, 3), Fraction(2, 7)]:
    for kap in [1, 2500]:
        for ls in [(1, 2, 4), (0, 3, 5), (2, 2, 2)]:
            e3 = Fraction(0)
            e4 = Fraction(0)
            for x in itertools.product([0, 1], repeat=3):
                pr = Fraction(1)
                for xi in x:
                    pr *= pp if xi else (1 - pp)
                e3 += pr * kap * sum(l * xi for l, xi in zip(ls, x))
            # A4: all fail together with prob p, cost kap*sum(l) on failure
            e4 = pp * kap * sum(ls)
            closed = pp * kap * sum(ls)
            ok = ok and e3 == closed == e4
            print("p", pp, "kappa", kap, "l", ls, "E3", e3, "E4", e4, "closed", closed)
print("c088 mean identity holds on sample:", ok)
