"""Round-36 verifier fragment builder for S7 L01-L02 (pin 47bac8d, base a90b52b).

Input : the round-35 fragment, copied to /tmp/ap1-r5/s7-l12-r36/previous-round35.json before this run.
Output: ledgers/S7/L01-L02.json in the checkout.
Carry rule: 'Carried from round 35 (<files> byte-identical since a90b52b):' after git diff --quiet a90b52b HEAD -- <files>;
for L01.html rows the line-level variant 'except line 133' (the only S7 change; git diff -U0 checked below).
Rows that cite the caption, figure 3 or the removed phrase are re-derived in explicit_r36.py (the builder refuses to carry them).
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PREV = Path("/tmp/ap1-r5/s7-l12-r36/previous-round35.json")
OUT = ROOT / "ledgers" / "S7" / "L01-L02.json"
BASE, PIN = "a90b52b", "47bac8d"
L01 = "course/modules/S/S7/L01.html"
S3_RE = re.compile(r"133|section 3|expected-max|expected max|roughly half|half a standard|figure caption \(line", re.I)
HEAD_RE = re.compile(r"^Carried from round 3[345] \(")

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(1, str(Path(__file__).resolve().parents[1] / "L01-L02-r35"))
from explicit_r36 import CARRY_EXTRA, EXPLICIT, NEW_ROWS, NOTES  # noqa: E402
from explicit_r35 import CARRY_REVIEWED, MUTANT_ROWS  # noqa: E402


def changed(paths: list[str]) -> bool:
    return subprocess.run(["git", "diff", "--quiet", BASE, PIN, "--", *paths], cwd=ROOT, check=False).returncode != 0


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout


# L01.html: exactly one hunk, line 133
hunks = [ln for ln in git("diff", "-U0", BASE, PIN, "--", L01).splitlines() if ln.startswith("@@")]
assert hunks == ["@@ -133 +133 @@"], hunks
# non-S7 gate inputs: comment-only changes
for f in ("pyproject.toml", "tests/test_figure_kernels.py"):
    for ln in git("diff", "-U0", BASE, PIN, "--", f).splitlines():
        if ln[:1] in "+-" and not ln.startswith(("+++", "---")):
            assert ln[1:].strip().startswith("#"), f"non-comment change in {f}: {ln}"

prev = json.loads(PREV.read_text(encoding="utf-8"))
out_rows: list[dict] = []
parsed: dict[str, list[str]] = {}
for row in prev["rows"]:
    rid = row["id"]
    ev = row["evidence"]
    if rid in EXPLICIT:
        new = dict(row)
        new.update(EXPLICIT[rid])
        if new["evidence"].rstrip().endswith("follows:"):
            new["evidence"] = new["evidence"].rstrip() + " " + ev
        out_rows.append(new)
        continue
    if rid in CARRY_EXTRA:
        files = CARRY_EXTRA[rid]
        others = [f for f in files if f != L01]
        if others and changed(others):
            sys.exit(f"ROW {rid}: subject changed since a90b52b: {others}")
        if L01 in files:
            prefix = f"Carried from round 35 ({', '.join(others + [L01])} byte-identical since {BASE} except line 133):"
        else:
            prefix = f"Carried from round 35 ({', '.join(files)} byte-identical since {BASE}):"
        new = dict(row)
        new["evidence"] = prefix + " Round-35 evidence follows: " + ev
        out_rows.append(new)
        continue
    if not HEAD_RE.match(ev):
        sys.exit(f"UNHANDLED row {rid}: {ev[:120]}")
    idx = ev.find("): ")
    assert idx > 0, rid
    region = ev[ev.index("(") + 1: idx]
    rest = ev[idx + 3:]
    head = region.split(" byte-identical since ")[0]
    files = [f.strip() for f in re.split(r",\s+|;\s+", head) if f.strip()]
    l01_in = L01 in region
    if l01_in:
        files_all = [f for f in files if f != L01]
    else:
        files_all = files
    parsed[rid] = files + ([L01] if l01_in and L01 not in files else [])
    if l01_in and rid not in CARRY_REVIEWED and S3_RE.search(row["location"] + " " + rest):
        sys.exit(f"ROW {rid} cites the caption / figure 3 / removed phrase: needs an explicit re-derivation")
    if files_all and changed(files_all):
        sys.exit(f"ROW {rid}: subject changed since a90b52b: {files_all}")
    if l01_in:
        prefix = (
            f"Carried from round 35 ({', '.join(files_all + [L01])} byte-identical since {BASE} except line 133):"
        )
    else:
        prefix = f"Carried from round 35 ({', '.join(files)} byte-identical since {BASE}):"
    new = dict(row)
    new["evidence"] = prefix + " " + rest
    out_rows.append(new)

out_rows.extend(NEW_ROWS)
ids = [r["id"] for r in out_rows]
assert len(ids) == len(set(ids)), "duplicate ids"
prev_ids = {r["id"] for r in prev["rows"]}
assert prev_ids <= set(ids), "a previous row id was dropped"
statuses = [r["status"] for r in out_rows]
fails = [r["id"] for r in out_rows if r["status"] == "FAIL"]
unver = [r["id"] for r in out_rows if r["status"] == "UNVERIFIABLE"]
carried = sum(1 for r in out_rows if r["evidence"].startswith("Carried from round 35"))
reran = len(out_rows) - carried
verdict = "PASS" if all(s == "PASS" for s in statuses) else "FAIL"

frag = dict(prev)
frag.update({
    "round": 36,
    "verifier": (
        "round-36 verifier (independent of the builders and of the round-35 verifier). Orchestrator request: re-derive the six numbers of "
        "the new caption (47bac8d) from scratch, rule on 1.2(c), re-run the gates, and carry every other row by git diff --quiet "
        "against a90b52b."
    ),
    "pin": PIN,
    "base": BASE,
    "previous_ledger": (
        "ledgers/S7/L01-L02.json as it stood in the checkout before round 36 (round 35, pin a90b52b, base e6d10ab, 486 rows, all PASS)"
    ),
    "checkout": str(ROOT),
    "scratch": "/tmp/ap1-r5/s7-l12-r36",
    "verified_at": "2026-10-27T02:40:00+00:00",
    "verdict": verdict,
    "changed_since_base": {
        f"{BASE}..{PIN} (git diff --stat, 3 files)": (
            "course/modules/S/S7/L01.html (line 133 only, @@ -133 +133 @@: the caption now shows the bound formula, the values "
            "2.146/1.539, 3.035/2.508, 4.292/3.852 and the method); pyproject.toml and tests/test_figure_kernels.py (comment lines only, "
            "checked by the builder). All other S7 slice files are byte-identical since a90b52b."
        ),
        "slice files": "course/modules/S/S7/L01.html changed on one line (133); all other slice files byte-identical since a90b52b.",
    },
    "line_numbering": (
        "Rows cite the files of the checkout at 47bac8d. L01.html changed by one replacement at line 133 (no line added or removed), "
        "so every other line number in the round-35 rows is unchanged."
    ),
    "notes": NOTES,
    "mutants": [{"description": d, "killed_by": k} for d, k in MUTANT_ROWS],
    "rows": out_rows,
    "summary": {
        "rows": len(out_rows),
        "pass": statuses.count("PASS"),
        "fail": len(fails),
        "unverifiable": len(unver),
        "carried_from_round_35": carried,
        "rerun_or_rederived_this_round": reran,
        "new_rows_this_round": [r["id"] for r in NEW_ROWS],
        "mutants": len(MUTANT_ROWS),
        "mutants_killed": len(MUTANT_ROWS),
        "fail_ids": fails,
        "unverifiable_ids": unver,
        "verdict_rule": "PASS only if every row is PASS; UNVERIFIABLE counts as a failure.",
    },
})
OUT.write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(frag["summary"], indent=1))
print("verdict", verdict)
