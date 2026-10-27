"""Round-35 verifier fragment builder for S7 L01-L02 (pin a90b52b, base e6d10ab).

Input : the previous fragment (round 34), copied to a scratch file before this run.
Output: ledgers/S7/L01-L02.json in the checkout.

Carry rule (VERIFIER_RULES 3; architect brief): a row carried from round 33 is re-labelled
'Carried from round 34 (<files> byte-identical since e6d10ab):' only after `git diff --quiet e6d10ab HEAD -- <files>`
returns 0. For course/modules/S/S7/L01.html, whose only change since e6d10ab is line 133 (git diff -U0:
@@ -133 +133 @@), a row is carried with the line-level variant, and only if its location and evidence do not
cite line 133, the caption, the expected-max figure or the removed phrase. Those rows are re-derived below.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PREV = Path("/tmp/ap1-r5/s7-l12-r35/previous-round34.json")
OUT = ROOT / "ledgers" / "S7" / "L01-L02.json"
BASE, PIN = "e6d10ab", "a90b52b"
L01 = "course/modules/S/S7/L01.html"
S3_RE = re.compile(r"133|section 3|expected-max|expected max|roughly half|half a standard|figure caption \(line", re.I)
CARRY_RE = re.compile(r"^Carried from round 33 \((.+?) byte-identical since bcf4e25\):?\s*")


def changed(paths: list[str]) -> bool:
    rc = subprocess.run(["git", "diff", "--quiet", BASE, "HEAD", "--", *paths], cwd=ROOT, check=False).returncode
    return rc != 0


prev = json.loads(PREV.read_text(encoding="utf-8"))
rows_in = {r["id"]: r for r in prev["rows"]}

# ---- explicit round-35 evidence (re-run commands and re-derived rows) ----
from explicit_r35 import CARRY_REVIEWED, EXPLICIT, MUTANT_ROWS, NEW_ROWS, NOTES  # noqa: E402  (same directory)

out_rows: list[dict] = []
carried_files_groups: dict[str, str] = {}
for rid, row in rows_in.items():
    if rid in EXPLICIT:
        new = dict(row)
        new.update(EXPLICIT[rid])
        out_rows.append(new)
        continue
    ev = row["evidence"]
    m = CARRY_RE.match(ev)
    if not m:
        sys.exit(f"UNHANDLED row {rid}: {ev[:120]}")
    files = [f.strip() for f in m.group(1).split(", ")]
    rest = ev[m.end():]
    if L01 in files and rid not in CARRY_REVIEWED and S3_RE.search(row["location"] + " " + ev):
        sys.exit(f"ROW {rid} cites line 133 / caption / figure / removed phrase and needs an explicit re-derivation")
    others = [f for f in files if f != L01]
    if others and changed(others):
        sys.exit(f"ROW {rid}: subject changed since e6d10ab: {[f for f in others if changed([f])]}")
    if L01 in files:
        l01_changed = changed([L01])
        if not l01_changed:
            prefix = f"Carried from round 34 ({', '.join(files)} byte-identical since {BASE}):"
        else:
            head = (", ".join(others) + " byte-identical since " + BASE + "; ") if others else ""
            prefix = (
                f"Carried from round 34 ({head}{L01} byte-identical since {BASE} except line 133, "
                f"the only changed line (git diff -U0 {BASE} HEAD: @@ -133 +133 @@)):"
            )
    else:
        prefix = f"Carried from round 34 ({', '.join(files)} byte-identical since {BASE}):"
    new = dict(row)
    new["evidence"] = prefix + " " + rest
    out_rows.append(new)

out_rows.extend(NEW_ROWS)
ids = [r["id"] for r in out_rows]
assert len(ids) == len(set(ids)), "duplicate ids"
for rid in list(EXPLICIT) + [r["id"] for r in NEW_ROWS]:
    assert rid in ids, rid

statuses = [r["status"] for r in out_rows]
fails = [r["id"] for r in out_rows if r["status"] == "FAIL"]
unver = [r["id"] for r in out_rows if r["status"] == "UNVERIFIABLE"]
carried = sum(1 for r in out_rows if r["evidence"].startswith("Carried from round 34"))
reran = sum(1 for r in out_rows if r["id"] in EXPLICIT or r["id"] in {x["id"] for x in NEW_ROWS})
verdict = "PASS" if all(s == "PASS" for s in statuses) else "FAIL"

frag = dict(prev)
frag.update(
    {
        "round": 35,
        "verifier": (
            "round-35 verifier (independent of the builders and of the round-34 verifier). Rule applied: the architect's "
            "ruling on the Koning row; the L01 caption delta re-derived from scratch; every S7 command re-run; carried rows "
            "re-labelled by git diff --quiet against e6d10ab."
        ),
        "pin": PIN,
        "base": BASE,
        "previous_ledger": (
            "ledgers/S7/L01-L02.json as it stood in this checkout (round 34, pin e6d10ab, base bcf4e25, 473 rows: 471 PASS, "
            "1 FAIL = T34-banned-roughly-half-caption, 1 UNVERIFIABLE = L01-cmd-koning-spot-a2a631a)"
        ),
        "checkout": str(ROOT),
        "scratch": "/tmp/ap1-r5/s7-l12-r35",
        "verified_at": "2026-10-27T02:12:02+00:00",
        "verdict": verdict,
        "changed_since_base": {
            "e6d10ab..a90b52b (git diff --stat, 55 files)": (
                "course/modules/S/S7/L01.html (one line, @@ -133 +133 @@: the section 3 figcaption); tests/test_koning_spot.py "
                "(docstring and TOLERANCE line); pyproject.toml (ruff extend-exclude adds ledgers/*/scripts); VERIFIER_RULES.md "
                "(section 3 bullet on archived scripts); ledgers/AP1/scripts/* and ledgers/S7/scripts/* (archived scripts, no slice "
                "file). Every other S7 slice file (L02.html, cards.json, figures-L01.js, figures-L02.js, tests/labs/S7, "
                "references/references.json, notation/*) is byte-identical to e6d10ab (git diff --quiet, rc 0)."
            ),
            "slice files": "course/modules/S/S7/L01.html changed on one line (133); all other slice files byte-identical since e6d10ab.",
        },
        "line_numbering": (
            "Rows cite the files of the checkout at a90b52b (L01.html 824 lines, L02.html 635 lines). L01.html changed by one "
            "replacement at line 133 (no line added or removed), so every line number in the round-34 rows is unchanged."
        ),
        "notes": NOTES,
        "rows": out_rows,
        "mutants": [
            {"description": d, "killed_by": k}
            for d, k in MUTANT_ROWS
        ],
        "summary": {
            "rows": len(out_rows),
            "pass": statuses.count("PASS"),
            "fail": len(fails),
            "unverifiable": len(unver),
            "carried_from_round_34": carried,
            "rerun_or_rederived_this_round": reran,
            "new_rows_this_round": [r["id"] for r in NEW_ROWS],
            "mutants": len(MUTANT_ROWS),
            "mutants_killed": len(MUTANT_ROWS),
            "fail_ids": fails,
            "unverifiable_ids": unver,
            "verdict_rule": "PASS only if every row is PASS; UNVERIFIABLE counts as a failure.",
        },
    }
)
OUT.write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(frag["summary"], indent=1))
print("verdict", verdict)
