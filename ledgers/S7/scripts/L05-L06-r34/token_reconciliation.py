"""Round-34 reconciliation of the numeric tokens that round 33's sweep left unclassed (L05: 158, L06: 96).

Every visible numeric token of course/modules/S/S7/L05.html and L06.html (tags, scripts, styles removed) is
assigned the FIRST class that applies, in this order:
  year          4-digit integer 1900-2030 (citation or date)
  locator       preceded by Section, Lesson, Problem, Remark, Definition, Theorem, Proposition, Lemma, Lab,
                Table, Example, Figure, line(s), p., pp., §, item, row, step, card, or an equation number (n)
  lab-output    the same value (at the token's decimals) is in an expected block of the same page; run_labs matched
                each expected block this round
  rerun-output  the value is in a round-34 re-run output (base twins, variants, sol-E2/E3, L06 E3, MC, null count)
  derived       the value is an output of derive_numbers.py, mc_checks.py or e3_quadrature_and_se.py (page value)
  twin-param    the value occurs in the lab or solution twin source of the page (a parameter of the simulation)
  figure        the value occurs in a figure readout or description (drive_results.json, round 33)
  unclassed     none of the above: printed for manual decision
Run: .venv/bin/python -I ledgers/S7/scripts/L05-L06-r34/token_reconciliation.py <scratch-dir>
"""

from __future__ import annotations

import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
S7 = ROOT / "course" / "modules" / "S" / "S7"
TWINS = ROOT / "tests" / "labs" / "S7"
R34 = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/ap1-r5/L05-L06/r34")
NUM = re.compile(r"(?<![\w.])(\d[\d,]*(?:\.\d+)?)(%?)")
TAGS = re.compile(r"<script.*?</script>|<style.*?</style>|<[^>]+>", re.S)
EXPECTED = re.compile(r'<pre class="expected"[^>]*>(.*?)</pre>', re.S)
LOCATOR = re.compile(
    r"(Sections?|Lessons?|Problems?|Remarks?|Definitions?|Theorems?|Propositions?|Lemmas?|Labs?|Tables?|Examples?|"
    r"Figures?|lines?|pp?\.|§|items?|rows?|steps?|cards?|Notes?|Chapters?|Parts?|Exercises?|E\d|M\d|P\d|R\d|F\d|\(\d+\)\s*$|"
    r"Lab|item|No\.|number|Question)\s*$",
    re.I,
)


def visible_lines(path: Path) -> list[tuple[int, str]]:
    out = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        t = html.unescape(TAGS.sub(" ", line))
        t = re.sub(r"\s+", " ", t)
        if t.strip():
            out.append((i, t))
    return out


def expected_values(path: Path) -> list[float]:
    text = " ".join(html.unescape(TAGS.sub(" ", b)) for b in EXPECTED.findall(path.read_text(encoding="utf-8")))
    return [float(t) for t in re.findall(r"-?\d+(?:\.\d+)?", text)]


def rerun_values() -> list[float]:
    vals: list[float] = []
    for p in list(R34.rglob("*.out")) + list(R34.rglob("*.txt")):
        for t in re.findall(r"-?\d+(?:\.\d+)?", p.read_text(encoding="utf-8", errors="replace")):
            vals.append(float(t))
    return vals


def derived_values() -> list[float]:
    vals: list[float] = []
    for name in ("derive_numbers.out", "mc_checks.out", "e3.out", "lab6_null.out"):
        p = ROOT.parent / "tmp" / name
    for p in [Path("/tmp/ap1-r5/L05-L06/derive_numbers.out"), R34 / "mc_checks.out", R34 / "e3.out", R34 / "lab6_null.out"]:
        if not p.exists():
            continue
        for m in re.finditer(r"page ([\-\d.e]+)", p.read_text(encoding="utf-8")):
            try:
                vals.append(float(m.group(1)))
            except ValueError:
                pass
    # values written as arithmetic in the round-33 and round-34 scripts (printed as 'derived' in their output)
    for p in [Path("/tmp/ap1-r5/L05-L06/derive_numbers.out"), R34 / "mc_checks.out", R34 / "e3.out", R34 / "lab6_null.out"]:
        if p.exists():
            for t in re.findall(r"(?<=[ =(:])-?\d+\.\d+|(?<=[ =(:])-?\d+(?=[ ,)])", p.read_text(encoding="utf-8")):
                vals.append(float(t))
    return vals


def twin_values(page: str) -> list[float]:
    names = {"L05": "lab-S7-L05", "L06": "lab-S7-L06"}[page]
    vals: list[float] = []
    for p in TWINS.glob(f"{names}*.py"):
        vals += [float(t) for t in re.findall(r"\d+(?:\.\d+)?", p.read_text(encoding="utf-8"))]
    for p in TWINS.glob("sol-S7-L0[56]*.py"):
        vals += [float(t) for t in re.findall(r"\d+(?:\.\d+)?", p.read_text(encoding="utf-8"))]
    return vals


def figure_values(page: str) -> list[float]:
    p = Path("/tmp/ap1-r5/L05-L06/drive/drive_results.json")
    if not p.exists():
        return []
    data = json.loads(p.read_text(encoding="utf-8"))
    vals: list[float] = []
    for key, st in data["states"].items():
        if key.startswith(page + "/"):
            for field in ("default_readout", "desc", "after_simulate", "after_search"):
                if field in st:
                    vals += [float(t.replace(",", "")) for t in re.findall(r"\d[\d,]*(?:\.\d+)?", st[field])]
    return vals


def decimals(tok: str) -> int:
    return len(tok.split(".")[1]) if "." in tok else 0


def close(a: float, b: float, dec: int) -> bool:
    # sign-insensitive: the sweep strips minus signs ("-0.232" is shown as 0.232)
    b = abs(b)
    a = abs(a)
    return abs(round(a, dec) - b) < 1e-9 or abs(a - b) <= 0.5 * 10 ** (-dec) + 1e-12


summary: dict[str, Counter] = {}
residue: dict[str, list[tuple[int, str, str]]] = {}
for page in ("L05", "L06"):
    path = S7 / f"{page}.html"
    exp = expected_values(path)
    rer = rerun_values()
    der = derived_values()
    twin = twin_values(page)
    fig = figure_values(page)
    counts: Counter = Counter()
    residue[page] = []
    for line_no, text in visible_lines(path):
        for m in NUM.finditer(text):
            tok = m.group(1).replace(",", "")
            pct = m.group(2) == "%"
            before = text[max(0, m.start() - 22): m.start()]
            try:
                v = float(tok)
            except ValueError:
                continue
            dec = decimals(tok)
            if re.fullmatch(r"(19|20)\d\d", tok) and "." not in tok:
                counts["year"] += 1
                continue
            if LOCATOR.search(before):
                counts["locator"] += 1
                continue
            if dec < 2 and v < 10:  # small integers and one-decimal values match too many numbers to mean anything
                counts["unclassed"] += 1
                residue[page].append((line_no, tok, text[max(0, m.start() - 60): m.end() + 30]))
                continue
            if any(close(e, v, dec) for e in exp) or (pct and any(close(e, v / 100, dec + 2) for e in exp)):
                counts["lab-output"] += 1
                continue
            if any(close(r, v, dec) for r in rer):
                counts["rerun-output"] += 1
                continue
            if any(close(d_, v, dec) for d_ in der):
                counts["derived"] += 1
                continue
            if any(close(t, v, dec) for t in twin):
                counts["twin-param"] += 1
                continue
            if any(close(f, v, dec) for f in fig):
                counts["figure"] += 1
                continue
            counts["unclassed"] += 1
            residue[page].append((line_no, tok, text[max(0, m.start() - 60): m.end() + 30]))
    summary[page] = counts
    print(page, dict(counts), "total", sum(counts.values()))

for page in ("L05", "L06"):
    print(f"\n== residue {page}: {len(residue[page])}")
    for line_no, tok, ctx in residue[page]:
        print(f"{line_no}\t{tok}\t{ctx}")
