"""Independent re-derivation for M4 slice a (hub index.html, L01-L04, lab twins, cards L01-L04).

Run from the checkout root:  .venv/bin/python ledgers/M4/scripts/M4-a-r1/recheck_slice_a.py

Prints one line per check: CHECK <name>: OK or MISMATCH with the values.
Every number is recomputed here with fractions, never copied from the page.
"""

from __future__ import annotations

import html
import json
import math
import re
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
M4 = ROOT / "course" / "modules" / "M" / "M4"
failures: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    status = "OK" if ok else "MISMATCH"
    print(f"CHECK {name}: {status}{(' ' + detail) if detail else ''}")
    if not ok:
        failures.append(name)


def plain(path: Path) -> str:
    s = path.read_text(encoding="utf-8")
    s = re.sub(r"<script.*?</script>", "", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(s)


# ---- L01 law of Example 3.6 and Lab 1
law = [(-2, F(1, 10)), (-1, F(2, 10)), (0, F(3, 10)), (1, F(2, 10)), (2, F(1, 10)), (3, F(1, 10))]


def cdf(x: int) -> F:
    return sum((p for v, p in law if v <= x), F(0))


def quant(p: F) -> int:
    return min(v for v, _ in law if cdf(v) >= p)


check("L01 CDF values", [cdf(v) for v, _ in law] == [F(1, 10), F(3, 10), F(3, 5), F(4, 5), F(9, 10), F(1)])
check("L01 Q(1/2)=0, Q(3/5)=0, Q(61/100)=1", (quant(F(1, 2)), quant(F(3, 5)), quant(F(61, 100))) == (0, 0, 1))
check("L01 Q(99/100)=3, F(2)=9/10<99/100", quant(F(99, 100)) == 3 and cdf(2) < F(99, 100))
check("L01 Q(p)=1 exactly on (3/5,4/5]", all((quant(F(j, 1000)) == 1) == (F(3, 5) < F(j, 1000) <= F(4, 5)) for j in range(1, 1001)))
grid = [F(j, 100) for j in range(1, 101)]
check("L01 F(Q(p))>=p on 100 grid points", all(cdf(quant(p)) >= p for p in grid))
check("L01 strict-rule Q^s(3/5)=1", min(v for v, _ in law if cdf(v) > F(3, 5)) == 1)
check("L01 ceil(pn): n=150 p=0.99 -> 149; n=200 -> 198", math.ceil(F(99, 100) * 150) == 149 and math.ceil(F(99, 100) * 200) == 198)
check("L01 74/75 below 0.99 (page line 278)", F(148, 150) == F(74, 75) and F(148, 150) < F(99, 100))
check("L01 Example 1.3 P(X<=1)=5/6", F(1, 2) + F(1, 3) == F(5, 6))
check("L01 skill check quantile (0.5) of (1/4,1/2,1/4) is 1", min(v for v, p in [(0, F(1, 4)), (1, F(1, 2)), (2, F(1, 4))] if sum(q for u, q in [(0, F(1, 4)), (1, F(1, 2)), (2, F(1, 4))] if u <= v) >= F(1, 2)) == 1)
check("L01 mech-2 values 2,5,7 with 1/5,1/2,3/10", F(1, 5) + F(1, 2) == F(7, 10) and F(1, 5) + F(1, 2) + F(3, 10) == 1)
check("L01 mech-3 ceil(40*0.9)=36, ceil(40*0.901)=37", math.ceil(F(40) * F(9, 10)) == 36 and math.ceil(F(40) * F(901, 1000)) == 37)

# ---- L02 die and loss
die = [(k, F(1, 6)) for k in range(1, 7)]
loss = [(0, F(19, 20)), (250000, F(1, 20))]


def ex(l):
    return sum((v * p for v, p in l), F(0))


def var_def(l):
    m = ex(l)
    return sum(((v - m) ** 2 * p for v, p in l), F(0))


def var_sc(l):
    m = ex(l)
    return sum((v * v * p for v, p in l), F(0)) - m * m


check("L02 die E=7/2, E[X^2]=91/6, Var=35/12", ex(die) == F(7, 2) and sum(v * v * p for v, p in die) == F(91, 6) and var_def(die) == F(35, 12) == var_sc(die))
check("L02 Var(2X)=35/3 = 4*35/12", var_def([(2 * v, p) for v, p in die]) == F(35, 3) == 4 * F(35, 12))
check("L02 loss E=12500, E[L^2]=3125000000, Var=2968750000", ex(loss) == 12500 and sum(v * v * p for v, p in loss) == 3125000000 and var_def(loss) == 2968750000 == var_sc(loss))
check("L02 sqrt(2968750000) ~ 54486.24", f"{math.sqrt(2968750000):.2f}" == "54486.24")
check("L02 sqrt(35/12) ~ 1.708", f"{math.sqrt(35 / 12):.3f}" == "1.708")
check("L02 R2 Var(L/100)=296875, sd 544.8624", var_def([(F(v, 100), p) for v, p in loss]) == 296875 and f"{math.sqrt(296875):.4f}" == "544.8624")
check("L02 M2 loss 0/50000 with 9/10,1/10: Var=2.25e8, sd=15000", var_def([(0, F(9, 10)), (50000, F(1, 10))]) == 225000000 and math.sqrt(225000000) == 15000)
check("L02 M1 indicator p=3/10: Var=21/100", F(3, 10) - F(9, 100) == F(21, 100))
check("L02 E2 expected losses 10000/20=500, 500-489=11", 10000 * F(1, 20) == 500 and 500 - 489 == 11)
check("L02 misconception: 91/6 ~ 15.17 and 35/12 ~ 2.92", f"{91 / 6:.2f}" == "15.17" and f"{35 / 12:.2f}" == "2.92")

# L02 counterexample to the card/misconception claim 'variance is never E[X^2]'
pm = [(-1, F(1, 2)), (1, F(1, 2))]
check("L02 counterexample: X=+-1 has Var(X)=E[X^2]=1 (so 'Var is never E[X^2]' is false)", var_def(pm) == 1 and sum(v * v * p for v, p in pm) == 1 and ex(pm) == 0)

# L02 P2 and P3 computations
check("L02 P3 V=-U: Var(U+V)=0, Var(U)+Var(V)=2", var_def([(-1, F(1, 2)), (1, F(1, 2))]) == 1)

# ---- L03 skewed law and Bernoulli
sk = [(0, F(1, 2)), (1, F(1, 4)), (2, F(1, 8)), (10, F(1, 8))]
m = ex(sk)


def cm(l, k):
    mu = ex(l)
    return sum(((v - mu) ** k * p for v, p in l), F(0))


m2, m3, m4 = cm(sk, 2), cm(sk, 3), cm(sk, 4)
check("L03 mean 7/4, m2=163/16, m3=2157/32, m4=149461/256", (m, m2, m3, m4) == (F(7, 4), F(163, 16), F(2157, 32), F(149461, 256)))
check("L03 squared skewness 18610596/4330747", m3 * m3 / m2 ** 3 == F(18610596, 4330747))
check("L03 kurtosis 149461/26569 = 5.6254", m4 / m2 ** 2 == F(149461, 26569) and f"{float(m4 / m2 ** 2):.4f}" == "5.6254")
check("L03 skewness 2.0730", f"{float(m3) / float(m2) ** 1.5:.4f}" == "2.0730")
check("L03 section 3 third-moment terms sum", F(-1372, 512) + F(-54, 512) + F(1, 512) + F(35937, 512) == F(34512, 512) == F(2157, 32))
check("L03 reduction 35937-34512 = 1425", 35937 - 34512 == 1425)
def bern(p: F) -> list[tuple[int, F]]:
    return [(0, 1 - p), (1, p)]


for p, g4 in [(F(1, 10), F(73, 9)), (F(1, 4), F(7, 3))]:
    pq = p * (1 - p)
    check(f"L03 Bernoulli p={p} closed-form gamma4 = {g4}", (1 - 3 * pq) / pq == g4 == cm(bern(p), 4) / cm(bern(p), 2) ** 2)
check(
    "L03 Bernoulli p=1/10 squared skewness 64/9 (direct moments and closed form)",
    cm(bern(F(1, 10)), 3) ** 2 / cm(bern(F(1, 10)), 2) ** 3 == F(64, 9) == (1 - 2 * F(1, 10)) ** 2 / F(9, 100),
)
check("L03 p=1/4 gamma3 = 2/sqrt3 ~ 1.155", abs(2 / math.sqrt(3) - 1.1547) < 1e-4 and abs((1 - F(1, 2)) / math.sqrt(3 / 16) - 2 / math.sqrt(3)) < 1e-12)
check("L03 sample gaps: 2.073-2.065 = 0.008, 5.625-5.580 = 0.045", round(2.073 - 2.065, 3) == 0.008 and round(5.625 - 5.580, 3) == 0.045)
check("L03 canon example -2,1,3 with 2/5,1/2,1/10: mean 0, m3 0, m2 3, m4 15", ex([(-2, F(2, 5)), (1, F(1, 2)), (3, F(1, 10))]) == 0 and cm([(-2, F(2, 5)), (1, F(1, 2)), (3, F(1, 10))], 3) == 0 and cm([(-2, F(2, 5)), (1, F(1, 2)), (3, F(1, 10))], 2) == 3 and cm([(-2, F(2, 5)), (1, F(1, 2)), (3, F(1, 10))], 4) == 15)
check("L03 kurtosis 15/9 = 5/3 ~ 1.6667", F(15, 9) == F(5, 3) and f"{5 / 3:.4f}" == "1.6667")
check("L03 Bernoulli skewness 8/3 ~ 2.6667", F(8, 3) == F(4, 5) / F(3, 10) and f"{8 / 3:.4f}" == "2.6667")
check("L03 Remark: Bernoulli 1/10 kurtosis 73/9 ~ 8.11", f"{73 / 9:.2f}" == "8.11")
sym = [(-1, F(1, 2)), (1, F(1, 2))]
check("L03 R1: symmetric two-point law at mu +- sigma has gamma4 = 1", cm(sym, 4) / cm(sym, 2) ** 2 == 1)

# ---- L04 tables
dep = {(0, 0): F(1, 10), (0, 1): F(3, 10), (1, 0): F(2, 10), (1, 1): F(2, 10), (2, 0): F(1, 10), (2, 1): F(1, 10)}
check("L04 Example 2.5 table sums to 1", sum(dep.values()) == 1)
py0 = sum(p for (x, y), p in dep.items() if y == 0)
py1 = sum(p for (x, y), p in dep.items() if y == 1)
px = {x: sum(p for (xx, y), p in dep.items() if xx == x) for x in (0, 1, 2)}
check("L04 marginals P(Y=0)=2/5, P(Y=1)=3/5, E[X]=4/5", py0 == F(2, 5) and py1 == F(3, 5) and sum(x * q for x, q in px.items()) == F(4, 5))
c0 = sum(x * p for (x, y), p in dep.items() if y == 0) / py0
c1 = sum(x * p for (x, y), p in dep.items() if y == 1) / py1
check("L04 E[X|Y=0]=1, E[X|Y=1]=2/3, total expectation", c0 == 1 and c1 == F(2, 3) and c0 * py0 + c1 * py1 == F(4, 5))
check("L04 dependent cell (0,0): 1/10 vs 4/25", dep[(0, 0)] == F(1, 10) and px[0] * (py0) == F(4, 25))
check("L04 ratio (1/10)/(4/25)=5/8", (F(1, 10)) / F(4, 25) == F(5, 8))
check("L04 M1 table: product 0.3*0.4=0.12 != 0.1", F(3, 10) * F(4, 10) == F(12, 100) and F(1, 10) != F(12, 100))
check("L04 M1 E[X|Y=1]=0.4/0.6=2/3", F(4, 10) / F(6, 10) == F(2, 3))
check("L04 M3 product indicators cells 1/8,1/8,3/8,3/8", F(1, 4) * F(1, 2) == F(1, 8) and F(3, 4) * F(1, 2) == F(3, 8))
check(
    "L04 Example 1.9 uniform {-1,0,1}, Y=X^2: E[X]=0, E[Y]=2/3, E[XY]=0, Cov=0, p(0,0)=1/3 vs 1/9",
    sum(x * F(1, 3) for x in (-1, 0, 1)) == 0
    and sum(x * x * F(1, 3) for x in (-1, 0, 1)) == F(2, 3)
    and sum(x * x * x * F(1, 3) for x in (-1, 0, 1)) == 0
    and F(1, 3) == F(1, 3)
    and F(1, 3) * F(1, 3) == F(1, 9),
)
check("L04 canon marginals example: p(0,0)=1/2 vs 1/4", F(1, 2) * 1 != F(1, 4) and F(1, 2) * F(1, 2) == F(1, 4))
check("L04 R1: Y=|X| covariance 0 and E[Y]=2/3", sum(abs(x) * F(1, 3) for x in (-1, 0, 1)) == F(2, 3) and sum(x * abs(x) * F(1, 3) for x in (-1, 0, 1)) == 0)

# ---- Lab twins: stdout must equal the page's expected block byte-for-byte
for lesson in ("L01", "L02", "L03", "L04"):
    twin = ROOT / "tests" / "labs" / "M4" / f"lab-M4-{lesson}-1.py"
    out = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True, cwd="/tmp", timeout=60
    )
    page = plain(M4 / f"{lesson}.html")
    html_text = (M4 / f"{lesson}.html").read_text(encoding="utf-8")
    m_exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', html_text, flags=re.S)
    expected = html.unescape(m_exp.group(1)) if m_exp else ""
    check(f"{lesson} twin exit 0, empty stderr", out.returncode == 0 and out.stderr == "")
    check(f"{lesson} stdout equals page expected block", out.stdout.rstrip("\n") == expected.rstrip("\n"), f"lines={len(out.stdout.splitlines())}")
    _ = page

# ---- Cards L01-L04: unique ids, no duplicate fronts or backs across the file, numbers appear in lesson
cards = json.loads((M4 / "cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
check("cards: ids unique across file", len(ids) == len(set(ids)), f"n={len(ids)}")
fronts = [re.sub(r"\W+", " ", c["front"].lower()).strip() for c in cards]
backs = [re.sub(r"\W+", " ", c["back"].lower()).strip() for c in cards]
check("cards: no duplicate fronts across file", len(fronts) == len(set(fronts)))
check("cards: no duplicate backs across file", len(backs) == len(set(backs)))
lesson_text = {l: plain(M4 / f"{l}.html") for l in ("L01", "L02", "L03", "L04")}
numtok = re.compile(r"(?<![A-Za-z_])\d+(?:\.\d+)?(?:/\d+)?")
missing = []
for c in cards:
    if c["lesson"] not in lesson_text:
        continue
    text = lesson_text[c["lesson"]].replace(",", "")
    for tok in set(numtok.findall(c["back"])):
        if tok in {"1", "0", "2", "3"}:
            continue
        if tok.lstrip("0") == "" or tok in text:
            continue
        # fractions may be written as \tfrac{a}{b} in the source: accept a/b matched on the page in braces form
        a, _, b = tok.partition("/")
        if b and re.search(rf"{a}\W+{b}\b", text):
            continue
        missing.append((c["id"], tok))
check("cards L01-L04: every card number appears in its lesson text (heuristic, see list)", not missing, f"missing={missing}")
c_ids = {c["id"] for c in cards if c["lesson"] in lesson_text}
check("cards L01-L04 count", len(c_ids) == 83, f"n={len(c_ids)}")

print("FAILURES:", failures if failures else "none")
sys.exit(1 if failures else 0)
