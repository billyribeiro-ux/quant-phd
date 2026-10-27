"""Scratch builder for the round-6 L03-L04 fragment. Reads the round-5 ledger, writes the round-6 fragment."""
import datetime
import json
from pathlib import Path

CK = Path("/tmp/verify-ap1-r8-i")
OUT = CK / "ledgers/AP1/L03-L04.json"
prev = json.loads(OUT.read_text(encoding="utf-8"))  # round-5 fragment (working copy), read before overwrite
assert len(prev["rows"]) == 83 and prev["summary"]["pass"] == 83

P = {r["id"]: r for r in prev["rows"]}

L03 = "course/modules/AP/AP1/L03.html"
L04 = "course/modules/AP/AP1/L04.html"
BYTE_PREFIX = "Carried from round 5 ({f} byte-identical since 33fd452; `git diff --quiet 33fd452 1325ded -- {f}` exits 0): "
LINE_PREFIX = (
    "Carried from round 5 (line-level: {f} changed since 33fd452 only at `@@ -{n} +{n} @@` "
    "(`git diff -U0 33fd452 1325ded`); this row's lines ({lines}) are outside that hunk): "
)


def body(rid):
    ev = P[rid]["evidence"]
    marker = "round-4 evidence follows): "
    if marker in ev:
        ev = ev.rsplit(marker, 1)[1]
    return ev.strip()


def carried_line(rid, check, location, lines, files=None):
    f = files or L03
    prefix = LINE_PREFIX.format(f=f, n=443, lines=lines) if f == L03 else LINE_PREFIX.format(f=f, n=358, lines=lines)
    return {"id": rid, "check": check, "location": location, "status": "PASS",
            "evidence": prefix + "Round-5 evidence (pin 33fd452) for the same lines: " + body(rid)}


def carried_byte(rid, check, location, files, extra=""):
    return {"id": rid, "check": check, "location": location, "status": "PASS",
            "evidence": BYTE_PREFIX.format(f=files) + extra + " Round-5 evidence: " + body(rid)}


def carried_both(rid, check, location, lines):
    """Rows whose lines sit in both pages: both changed hunks are outside the row's lines."""
    prefix = (
        "Carried from round 5 (line-level: L03.html changed since 33fd452 only at `@@ -443 +443 @@` and "
        "L04.html only at `@@ -358 +358 @@` (`git diff -U0 33fd452 1325ded`); this row's lines ({l}) are outside both): "
    ).format(l=lines)
    return {"id": rid, "check": check, "location": location, "status": "PASS",
            "evidence": prefix + "Round-5 evidence (pin 33fd452) for the same lines: " + body(rid)}


rows = []
# ---------------- command rows, re-run on 1325ded this round ----------------
rows.append({"id": "L03-L04-cmd-pin", "check": "2.9-structure",
             "location": "repository; course/modules/AP/AP1/L03.html, L04.html, cards.json, tests/labs/AP1/*, references/references.json, tools/data_sources.yaml, tools/page_smoke.py, index.html, pyproject.toml",
             "status": "PASS",
             "evidence": "Pin 1325ded (detached worktree /tmp/verify-ap1-r8-i; `git status` clean except this ledger). Delta since 33fd452 (`git diff --stat 33fd452 1325ded`, 26 files): slice files changed: L03.html and L04.html, one line each (`git diff -U0 33fd452 1325ded` -> `@@ -443 +443 @@` L03, `@@ -358 +358 @@` L04; four changed lines in total, each a regenerated expected-output digit). `git diff --quiet 33fd452 1325ded` is 0 for course/modules/AP/AP1/cards.json, tests/labs/AP1, references/references.json, notation/notation.json, course/assets/data/market, curriculum/03-markets.yaml, curriculum/curriculum.json, tools/coursekit.py, tools/run_labs.py, tools/verify_refs.py, tools/check_pages.py, tools/check_dag.py, tools/check_projects.py, tools/fetch_data.py, tools/ledger.py. Changed and re-checked this round: tools/data_sources.yaml (two `checked 2026-10-23` -> `checked 2026-10-26` date strings on fx_daily and fx_monthly; licence and licence_url unchanged), tools/page_smoke.py (re-run, PASS), course/modules/AP/AP1/index.html (line 183, hub prompt `\\operatorname` -> `\\diag`; page_smoke index PASS), pyproject.toml (ruff extend-exclude adds ledgers/*/equivalent; ruff re-run on the twins, PASS). Toolchain on 1325ded: Python 3.14.8, numpy 2.4.6, scipy 1.18.0 (`.venv/bin/python -c`), the same as round 5; vendored Pyodide scipy 1.18.0 (course/assets/vendor/LOCK.json)."})
rows.append({"id": "L03-L04-cmd-run_labs", "check": "2.5-lab",
             "location": "tools/run_labs.py; tests/labs/AP1/*; L03.html, L04.html",
             "status": "PASS",
             "evidence": "Re-run on 1325ded: `.venv/bin/python tools/run_labs.py --unit AP1` -> `run_labs AP1: PASS (22/22)`, rc 0; `--unit AP1 --page L03` -> `run_labs AP1: PASS (4/4)`; `--unit AP1 --page L04` -> `run_labs AP1: PASS (4/4)`. Each twin ran under `python -I -W error` in a scratch cwd with a minimal environment; stdout matched the page's expected block under the page's rule."})
rows.append({"id": "L03-L04-cmd-page_smoke", "check": "2.9-structure",
             "location": "tools/page_smoke.py",
             "status": "PASS",
             "evidence": "Re-run on 1325ded: `.venv/bin/python tools/page_smoke.py --unit AP1 --pages L03 L04` -> rc 0; `page_smoke modules/AP/AP1/L03.html: PASS`, `page_smoke modules/AP/AP1/L04.html: PASS`, `page_smoke AP1: PASS`; log /tmp/ap1-r5/L03-L04/page_smoke_L03_L04.log. Runtime boot 1.1 s and 1.2 s; all 6 labs ran in Pyodide with the status 'matches the expected result'. Also `page_smoke --unit AP1 --pages index` -> PASS (hub line 183 change, KaTeX strict re-parse). Pyodide digits captured this round by a scratch Playwright script (/tmp/ap1-r5/L03-L04/pyodide/capture_outputs.py, reusing tools/page_smoke.py serve/load, Run clicked on every lab): each lab's status read 'matches the expected result' (tolerance compare, run_labs-equivalent); L04-4 printed `T = 332; E_T[x* x] - 1 for every currency: max abs 1.2e-14`."})
rows.append({"id": "L03-L04-cmd-check_pages_dag", "check": "2.9-structure",
             "location": "tools/check_pages.py, tools/check_dag.py, tools/check_projects.py, curriculum/curriculum.json",
             "status": "PASS",
             "evidence": "Re-run on 1325ded: `check_pages.py --unit AP1` -> `check_pages AP1: PASS`; `check_pages.py --unit AP1 --page L03` -> `check_pages AP1 L03: PASS`; `--page L04` -> `check_pages AP1 L04: PASS`; `check_dag.py --unit AP1` -> `check_dag AP1: PASS`; `check_projects.py --unit AP1` -> `check_projects AP1: PASS` (all rc 0). curriculum/curriculum.json byte-identical since 33fd452."})
rows.append({"id": "L03-L04-cmd-lint", "check": "2.5-lab",
             "location": "tests/labs/AP1/lab-AP1-L03-1.py, lab-AP1-L03-2.py, sol-AP1-L03-E1.py, sol-AP1-L03-E2.py, lab-AP1-L04-1..4.py",
             "status": "PASS",
             "evidence": "Re-run on the 8 slice twins with explicit paths (the twins are byte-identical since 33fd452): `.venv/bin/ruff check <8 files>` -> 'All checks passed!' rc 0; `.venv/bin/ruff format --check <8 files>` -> '8 files already formatted' rc 0; `.venv/bin/mypy <8 files>` -> 'Success: no issues found in 8 source files' rc 0 (log /tmp/ap1-r5/L03-L04/mypy_twins.log). Note: the first attempt passed the eight paths as one shell word (zsh does not split it) and failed with E902; the re-run is the one recorded."})
rows.append({"id": "L03-L04-cmd-verify_refs-offline", "check": "2.1-citation",
             "location": "tools/verify_refs.py --offline; tools/fetch_data.py --check",
             "status": "PASS",
             "evidence": "Re-run on 1325ded: `.venv/bin/python tools/verify_refs.py --offline` -> `offline integrity: 560 entries, 0 problems` rc 0; `.venv/bin/python tools/fetch_data.py --check` -> `fetch_data: 3 datasets, 0 problems`. references/references.json byte-identical since 33fd452."})
rows.append({"id": "L03-L04-cmd-verify_refs-live", "check": "2.1-citation",
             "location": "tools/verify_refs.py --unit AP1",
             "status": "PASS",
             "evidence": "Re-run live on 1325ded with network: `.venv/bin/python tools/verify_refs.py --unit AP1` -> rc 0, final line exactly `live re-verification of AP1: 9 of 560 entries, 0 problems` (log /tmp/ap1-r5/L03-L04/verify_refs_live.log). No proxy or access error occurred."})

# ---------------- rows whose evidence changed this round ----------------
rows.append({"id": "L03-L04-cite-cochrane2005asset", "check": "2.1-citation",
             "location": "course/modules/AP/AP1/L03.html line 193 (locator '§4.2, beginning p. 67'); L04.html line 127 and key-results row line 510 (locator '§4.1, beginning p. 62')",
             "status": "PASS",
             "evidence": "Carried from round 5 (line-level: L03.html changed since 33fd452 only at line 443, L04.html only at line 358; these lines are outside both; `git diff -U0 33fd452 1325ded`). The live registry check is re-run this round: `verify_refs.py --unit AP1` -> 9 of 560 entries, 0 problems (row cmd-verify_refs-live). Round-5 evidence (pin 33fd452) for the same lines: " + body("L03-L04-cite-cochrane2005asset")})
rows.append({"id": "L03-L04-math-L03-E2", "check": "2.4-math",
             "location": "course/modules/AP/AP1/L03.html Problem E2 (lines 385-446): prompt, snippet sol-AP1-L03-E2, expected block (439-443), solution paragraph (444)",
             "status": "FAIL",
             "evidence": "Re-derived this round. (a) Snippet run under `python -I -W error` (scratch cwd): output is exactly the page's expected block, including the changed line 443 `shade exact gap: margin +0.000e+00, detection value 3.987137, cash flows of the returned theta from -2.0e-15 to 1.0e+00` (exact-string compare True; 3 repeats identical). (b) Solution paragraph numbers: margin +1.419e-05 at 0.2078 (printed +1.419e-05), detection value 0 at 0.2078 (printed 0.000000), margin 0 at the exact gap (printed +0.000e+00), detection value 3.987137 at the exact gap and at shades 1e-9 and 1e-12 (printed), smallest cash flows -3.7e-08 and -3.7e-11 (printed) all match. (c) The option `primal_feasibility_tolerance: 1e-7` is in the snippet; the 'also its default' claim holds on CPython: scipy 1.18.0 `_linprog_highs` docstring 'Default is 1e-07' (line 135), and the vendored Pyodide scipy is 1.18.0 (LOCK.json). (d) FAIL: line 444 says the violation is 'not rounding error, which would be of order 10^-16 on cash flows of order 1'. The lab's own exact-gap row, same expected block, prints rounding noise -2.0e-15 on cash flows of order 1, i.e. order 10^-15 (CPython; the snippet is not run in Pyodide, see row r6-pyodide-scope). The conclusion (the -3.7e-11 violation is not rounding, four orders larger) still holds; the stated magnitude does not match the printed digit. See the fix on row L03-L04-r6-prose-L03-444-rounding.",
             "fix": "L03.html line 444: change 'of order \\(10^{-16}\\) on cash flows of order 1' to 'of order \\(10^{-15}\\) on cash flows of order 1'. No other change. Then re-run run_labs --page L03 and page_smoke --pages L03 and re-verify this row and L03-L04-num-L03-E2."})
rows.append({"id": "L03-L04-num-L03-E2", "check": "2.2-number",
             "location": "course/modules/AP/AP1/L03.html Problem E2 prompt and solution (lines 387, 439-444)",
             "status": "FAIL",
             "evidence": "Every printed number in the expected block (lines 439-443) and every number quoted in the solution (line 444: +1.419 x 10^-5, 0, 3.7 x 10^-8, 3.7 x 10^-11, 3.987137, margin 0 at the exact gap, primal tolerance 10^-7) matches the twin's output when run under `python -I -W error` (re-derived this round; see row L03-L04-math-L03-E2). The one failing item is the magnitude 'of order 10^-16' for rounding on cash flows of order 1, which the same block's exact-gap row (-2.0e-15) contradicts; see row L03-L04-r6-prose-L03-444-rounding.",
             "fix": "Same single wording change as row L03-L04-math-L03-E2 (L03.html line 444: 10^{-16} -> 10^{-15}). Re-verify after the edit."})
rows.append({"id": "L03-L04-lab-sol-AP1-L03-E2", "check": "2.5-lab",
             "location": "tests/labs/AP1/sol-AP1-L03-E2.py and its data-check snippet in L03.html (lines 389-443)",
             "status": "PASS",
             "evidence": "Re-run this round. The twin is byte-identical to 33fd452 (`git diff --quiet 33fd452 1325ded -- tests/labs/AP1` exits 0), and run_labs --page L03 (PASS 4/4) checks the page's snippet against the twin byte for byte. Exact-string compare of the twin's stdout (under `python -I -W error`, scratch cwd, minimal env) with the page's expected block, lines 439-443: True. The changed expected line now reads `-2.0e-15` on the exact-gap row, matching the new digit. Snippet not executed in Pyodide (the browser runs only the two L03 labs; L03 has two Run buttons). ruff, ruff format and mypy clean (row cmd-lint)."})
rows.append({"id": "L03-L04-num-L04-lab4-E2", "check": "2.2-number",
             "location": "course/modules/AP/AP1/L04.html Lab 4 hypothesis/interpretation (lines 335-361), Problem E2 (lines 456-458)",
             "status": "PASS",
             "evidence": "Re-run this round. CPython (twin, scratch cwd with data/fx_monthly.csv, sha256 60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e, equal to MANIFEST): `T = 332; E_T[x* x] - 1 for every currency: max abs 7.2e-15`, `x*: mean 0.9996, s.d. 0.1410, min 0.2078, max 1.5187`, `weights b: [-1.61 -1.29 -7.75  2.69  2.35  2.85  0.91  0.28  2.6 ]`; the first line equals the page's regenerated expected block (exact-string compare True). Pyodide (captured this round): `max abs 1.2e-14`, same x* and weights. The round-5 value 8.9e-15 is no longer printed anywhere. The prose's 'order of 10^-14' holds on both runtimes (row L03-L04-r6-prose-L04-361-order). 1/1.003 = 0.997009 (recomputed round 5, script identical this round, row L03-L04-r6-recompute-scripts)."})
rows.append({"id": "L03-L04-lab-lab-AP1-L04-4", "check": "2.5-lab",
             "location": "tests/labs/AP1/lab-AP1-L04-4.py and its section in L04.html (lines 335-361, expected block line 358)",
             "status": "PASS",
             "evidence": "Re-run this round. Page code byte-identical to the twin (run_labs --page L04 PASS 4/4; twin byte-identical since 33fd452). `python -I -W error` in a scratch cwd with data/fx_monthly.csv: rc 0, stderr empty, stdout equals the page's expected block exactly (scripted compare True). Reads only data/fx_monthly.csv, the one entry in data-files (line 335). Pyodide (captured): `max abs 1.2e-14`, runs in well under the 10 s limit (page_smoke 0.0 s after preload). Deterministic, no RNG, no network. The interpretation (line 361) calls the in-sample pricing an arithmetic check, not evidence, which still holds."})
rows.append({"id": "L03-L04-math-L04-thm3-2-sdf-existence-uniqueness", "check": "2.4-math",
             "location": "course/modules/AP/AP1/L04.html lines 109-125 (Theorem 3.2 and proof); definition sentence line 119",
             "status": "PASS",
             "evidence": "Re-checked this round: the theorem and proof text (lines 109-125) and the definition sentence (line 119) are outside the changed line 358, so the round-5 derivation stands (round-5 evidence below, unchanged). The numeric note is updated: Lab 2 prints pricing errors `[0. 0. 0.]` (E[x* x] - p, CPython and Pyodide, this round); Lab 4 prints max abs 7.2e-15 on CPython and 1.2e-14 on Pyodide (both within the 10^-14 order that the page states). Round-5 evidence: " + body("L03-L04-math-L04-thm3-2-sdf-existence-uniqueness").replace("Lab 2 and Lab 4 print pricing errors of 0 and 8.9e-15.", "(Round-5 printed 8.9e-15 for Lab 4; superseded this round by 7.2e-15.)")})
rows.append({"id": "L03-L04-data-fx_monthly", "check": "2.8-figure",
             "location": "course/modules/AP/AP1/L04.html Lab 4 data-files=fx_monthly.csv (line 335); tools/data_sources.yaml fx_monthly note; course/assets/data/market/MANIFEST.json",
             "status": "PASS",
             "evidence": "Re-checked this round because tools/data_sources.yaml changed (the two diff hunks change only the 'checked' date text, 2026-10-23 -> 2026-10-26; licence and licence_url unchanged). (a) `shasum -a 256 course/assets/data/market/fx_monthly.csv` = 60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e = MANIFEST sha256 for fx_monthly; the snapshot directory is byte-identical since 33fd452. (b) MANIFEST licence quote 'Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission. Please cite to the Board as the source of the information.' with licence_url https://www.federalreserve.gov/disclaimer.htm: re-fetched this round (curl, HTTP 200, /tmp/ap1-r5/L03-L04/fx-r6/disclaimer.htm): the quoted sentence is present (grep count 1), so it grants redistribution. (c) data_sources.yaml note quotes checked against https://www.federalreserve.gov/releases/h10/about.htm (re-fetched, HTTP 200, /tmp/ap1-r5/L03-L04/fx-r6/about.htm): 'noon buying rates in New York for cable transfers payable in the listed currencies' (count 1), 'certified by the Federal Reserve Bank of New York for customs purposes as required by section 522 of the amended Tariff Act of 1930' (count 1), 'Last Update: February 06, 2023' (count 1); about.htm contains no 'public domain', 'terms of use' or 'copyright' text (count 0). `.venv/bin/python tools/fetch_data.py --check` -> 3 datasets, 0 problems. (d) Rebuild from the live feed, as BUILDER_RULES §6.6 requires for sha256: `tools/fetch_data.py --fetch --only fx_monthly` run in a scratch copy (`git archive 1325ded`, /tmp/ap1-r5/L03-L04/rebuild; the checkout's snapshot was not touched) built 669 rows, 67392 bytes, 1971-01 to 2026-09, and the rebuilt CSV is byte-identical to the snapshot (cmp; sha256 60572240...e3e in both). The provenance raw_sha256 differs: checked-in 8f370f9c...c6a8, today's download 17d087d0...52e4 (the issuer file changed; expected and not a failure, BUILDER_RULES §6.6). The rebuilt MANIFEST's `retrieved` (2026-10-27) was in the scratch copy only; the checkout's MANIFEST and `retrieved` 2026-10-19 are unchanged."})
rows.append({"id": "L03-L04-struct-L04-order", "check": "2.9-structure",
             "location": "course/modules/AP/AP1/L04.html; course/modules/AP/AP1/index.html (line 183 changed this round)",
             "status": "PASS",
             "evidence": "Re-run this round: check_pages --unit AP1 --page L04 PASS; page_smoke --unit AP1 --pages L04 PASS; page_smoke --unit AP1 --pages index PASS (the hub's changed line 183, a `\\diag` macro in a prompt, renders under the strict KaTeX re-parse). L04.html changed only at line 358 (inside Lab 4, which does not move any section); section order and counts unchanged. Hub data-hours unchanged (round-5 scan: 84 + 36 = 120). Round-5 evidence: " + body("L03-L04-struct-L04-order")})
rows.append({"id": "L03-L04-struct-L03-order", "check": "2.9-structure",
             "location": "course/modules/AP/AP1/L03.html",
             "status": "PASS",
             "evidence": "Re-run this round: check_pages --unit AP1 --page L03 PASS and page_smoke --unit AP1 --pages L03 PASS. The only L03 change is one replaced line of text inside a <pre> (line 443), so no section, heading, problem or count moves (line count unchanged). Round-5 evidence: " + body("L03-L04-struct-L03-order")})
rows.append({"id": "L03-L04-struct-DAG-unlinked", "check": "2.9-structure",
             "location": "course/modules/AP/AP1/L03.html, L04.html; curriculum/03-markets.yaml",
             "status": "PASS",
             "evidence": "check_dag --unit AP1 re-run PASS (row cmd-check_pages_dag). curriculum/03-markets.yaml byte-identical since 33fd452. The changed lines (L03 443, L04 358) contain no concept link. Round-5 evidence: " + body("L03-L04-struct-DAG-unlinked")})
rows.append({"id": "L03-L04-banned-scan", "check": "2.9-banned",
             "location": "course/modules/AP/AP1/L03.html, L04.html",
             "status": "PASS",
             "evidence": "Re-run this round with the BUILDER_RULES §1.3 strings (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, can be shown, roughly, historically, 'about N%', '...', the ellipsis character): grep -n -i over both pages returns only the six quiz stems that end in an ellipsis (L03.html lines 537, 546, 569; L04.html lines 524, 547, 556), the same lines as round 5. The two changed lines (L03 443, L04 358) contain none of the strings (diff inspected)."})
rows.append({"id": "L03-L04-banned-ellipsis-quiz", "check": "2.9-banned",
             "location": "course/modules/AP/AP1/L03.html quiz items 5, 6, 9 (lines 537, 546, 569); course/modules/AP/AP1/L04.html quiz items 1, 4, 5 (lines 524, 547, 556)",
             "status": "PASS",
             "evidence": "Same six lines, unchanged this round (grep re-run). Carried judgement from round 5: each stem is an answer cue ('play the role of…', 'equals…'), not omitted content. Advisory: this is a judgement by the verifier, not a machine check, and BUILDER_RULES §1.3 lists 'an ellipsis standing for omitted content' as banned."})
rows.append({"id": "L03-L04-math-notation", "check": "2.4-math",
             "location": "course/modules/AP/AP1/L03.html, L04.html (all TeX); notation/notation.json (byte-identical since 33fd452)",
             "status": "PASS",
             "evidence": "Line-level carry: the only changed lines (L03 443, L04 358) are inside <pre> output blocks and contain no TeX delimiters or macros (`git diff -U0 33fd452 1325ded` shows only the digits). notation/notation.json byte-identical (`git diff --quiet`). Round-5 evidence: " + body("L03-L04-math-notation")})

# ---------------- line-level carries, outside both changed hunks ----------------
L03_LINES = {
    "L03-L04-grade-L03-cochrane-span": ("193", L03),
    "L03-L04-grade-L03-proposition2.2": ("68", L03),
    "L03-L04-grade-L03-theorem3.1": ("89", L03),
    "L03-L04-grade-L03-proposition3.2": ("105", L03),
    "L03-L04-grade-L03-theorem4.1": ("178", L03),
    "L03-L04-grade-L03-corollary4.2": ("196", L03),
    "L03-L04-grade-L03-keyresults": ("436-441", L03),
    "L03-L04-grade-ungraded-framing": ("52", L03),
    "L03-L04-math-L03-prop2-2": ("60-75", L03),
    "L03-L04-math-L03-thm3-1-prop3-2": ("88-112", L03),
    "L03-L04-math-L03-thm4-1-duality": ("177-191", L03),
    "L03-L04-math-L03-cor4-2": ("195-203", L03),
    "L03-L04-math-L03-ex2-3": ("79-82", L03),
    "L03-L04-math-L03-ex4-3": ("207-210", L03),
    "L03-L04-math-L03-problems-M": ("301-321", L03),
    "L03-L04-math-L03-problems-P": ("326-346", L03),
    "L03-L04-math-L03-E1": ("351-381", L03),
    "L03-L04-math-L03-E3": ("394", L03),
    "L03-L04-math-L03-R1": ("454", L03),
    "L03-L04-math-L03-R2-R3": ("465-470, 477", L03),
    "L03-L04-num-L03-lab1": ("116, 170, 278", L03),
    "L03-L04-num-L03-boundary-0.2078": ("170, 268", L03),
    "L03-L04-num-L03-lab2-ex": ("212, 260 and the quiz", L03),
    "L03-L04-num-L03-lab-E1": ("380", L03),
    "L03-L04-lab-lab-AP1-L03-1": ("114-171", L03),
    "L03-L04-lab-lab-AP1-L03-2": ("212-260", L03),
    "L03-L04-lab-sol-AP1-L03-E1": ("358-381", L03),
    "L03-L04-data-simulated-labels": ("116, 145, 361, 393 (SIMULATED labels; none on line 443)", L03),
    "L03-L04-struct-L03-empty-references": ("572", L03),
}
for rid, (lines, f) in L03_LINES.items():
    rows.append(carried_line(rid, P[rid]["check"], P[rid]["location"], lines, f))

L04_LINES = {
    "L03-L04-grade-L04-proposition2-1": "70",
    "L03-L04-grade-L04-theorem2-2": "80",
    "L03-L04-grade-L04-theorem3-1": "100",
    "L03-L04-grade-L04-theorem3-2": "110",
    "L03-L04-grade-L04-corollary3-3": "130",
    "L03-L04-grade-L04-theorem4-1": "142",
    "L03-L04-grade-L04-proposition5-2": "278",
    "L03-L04-grade-L04-keyresults": "502-508",
    "L03-L04-math-L04-prop2-1-thm2-2": "69-91",
    "L03-L04-math-L04-riesz": "99-107",
    "L03-L04-math-L04-cor3-3-thm4-1": "129-151",
    "L03-L04-math-L04-ex4-2": "176-184",
    "L03-L04-math-L04-ex5-1-prop5-2": "270-285",
    "L03-L04-math-L04-lab3-kkt": "289",
    "L03-L04-math-L04-section6-P3": "328, 422-442",
    "L03-L04-math-L04-problems-M": "397-417",
    "L03-L04-math-L04-E1-E2": "451, 458",
    "L03-L04-math-L04-E3": "470",
    "L03-L04-math-L04-R1-R3": "477-499",
    "L03-L04-num-L04-lab1-ex4-2": "176-222",
    "L03-L04-num-L04-lab2-E1": "263 and E1",
    "L03-L04-num-L04-ex5-1-lab3-E3": "270-289, 323",
    "L03-L04-num-L04-M-quiz": "M1, M2, quiz items 2 and 6",
    "L03-L04-lab-lab-AP1-L04-1": "182-223",
    "L03-L04-lab-lab-AP1-L04-2": "225-290",
    "L03-L04-lab-lab-AP1-L04-3": "292-333",
    "L03-L04-fig-L04-projection-diagram": "153-175",
    "L03-L04-struct-L04-order-unused": "",
}
for rid, lines in L04_LINES.items():
    if rid not in P:
        continue
    rows.append(carried_line(rid, P[rid]["check"], P[rid]["location"], lines, L04))

rows.append({"id": "L03-L04-fig-L03-none", "check": "2.8-figure",
             "location": "course/modules/AP/AP1/ (no figures-L03.js or figures-L04.js)",
             "status": "PASS",
             "evidence": "Re-checked this round: `ls course/modules/AP/AP1/ | grep -ci figures` -> 0. L03 and L04 contain no chart figure; the figure rules do not apply."})

# cards: the file is byte-identical, so every card row carries by byte identity.
for rid in ["L03-L04-card-sample-c025", "L03-L04-card-sample-c031", "L03-L04-card-sample-c042", "L03-L04-card-dup-scan"]:
    rows.append(carried_byte(rid, P[rid]["check"], P[rid]["location"], "course/modules/AP/AP1/cards.json",
                             extra="The cited lesson lines are outside both changed hunks."))
rows.append({"id": "L03-L04-card-identity", "check": "2.7-card",
             "location": "course/modules/AP/AP1/cards.json",
             "status": "PASS",
             "evidence": "`git diff --quiet 33fd452 1325ded -- course/modules/AP/AP1/cards.json` exits 0: the file is byte-identical this round, so the 25 L03/L04 cards are identical to round 5 as JSON objects by construction. Round-5 evidence: " + body("L03-L04-card-identity")})

# ---------------- rows re-derived to PASS (numbers recomputed this round) ----------------
rows.append({"id": "L03-L04-r6-digit-L03-E2", "check": "2.5-lab",
             "location": "tests/labs/AP1/sol-AP1-L03-E2.py; course/modules/AP/AP1/L03.html line 443 (expected block)",
             "status": "PASS",
             "evidence": "Digit re-derived by running the twin: `python -I -W error sol-AP1-L03-E2.py` in a scratch cwd prints `shade exact gap: margin +0.000e+00, detection value 3.987137, cash flows of the returned theta from -2.0e-15 to 1.0e+00`. Three repeated runs printed the same digit. Exact-string compare with the page's line 443: True. Old digit -7.8e-16 is no longer present in the pinned tree (`git grep -n '7.8e-16'` -> none). Scope: CPython only; the E2 snippet has no Run button in the browser (L03 has two Run buttons, both for labs 1 and 2), so no Pyodide digit exists for this line."})
rows.append({"id": "L03-L04-r6-digit-L04-4", "check": "2.5-lab",
             "location": "tests/labs/AP1/lab-AP1-L04-4.py; course/modules/AP/AP1/L04.html line 358 (expected block)",
             "status": "PASS",
             "evidence": "Digit re-derived by running the twin under `python -I -W error` with data/fx_monthly.csv in the scratch cwd: `T = 332; E_T[x* x] - 1 for every currency: max abs 7.2e-15`; stdout equals the page's line 358 exactly. Pyodide (captured in the browser this round): `max abs 1.2e-14`. Both are in the decade 10^-14, which is what the page claims (row L03-L04-r6-prose-L04-361-order). Old digit 8.9e-15 is not in the pinned tree (`git grep` -> none outside ledgers/)."})
rows.append({"id": "L03-L04-r6-prose-L03-444-rounding", "check": "2.2-number",
             "location": "course/modules/AP/AP1/L03.html line 444 (solution paragraph, sentence 'It is not rounding error, which would be of order 10^-16 on cash flows of order 1')",
             "status": "FAIL",
             "evidence": "The regenerated line 443 prints exact-gap cash flows from -2.0e-15 to 1.0e+00 under python -I -W error (CPython, three runs). That is rounding noise on cash flows of order 1 at order 10^-15, one decade above the 10^-16 the sentence gives for rounding. The sentence's conclusion does not change: the non-boundary violations -3.7e-08 and -3.7e-11 are four and five orders larger than the exact-gap noise, so they are not rounding. The magnitude claim, however, is stated as a fact about rounding on this lab and the lab's own output now contradicts it. The old digit -7.8e-16 was already order 10^-15 in base-10 rounding, so the sentence was imprecise before this round as well. Judged on the claim (not the digit): FAIL on the wording; this is a judgement the caller may weigh, the rule being fail-closed.",
             "fix": "L03.html line 444: replace 'of order \\(10^{-16}\\) on cash flows of order 1' with 'of order \\(10^{-15}\\) on cash flows of order 1'. Leave the rest of the sentence. Then re-run run_labs --page L03 and page_smoke --pages L03, and re-verify rows L03-L04-math-L03-E2, L03-L04-num-L03-E2 and this row."})
rows.append({"id": "L03-L04-r6-prose-L04-361-order", "check": "2.2-number",
             "location": "course/modules/AP/AP1/L04.html line 361 (interpretation: 'The pricing errors are of the order of \\(10^{-14}\\)')",
             "status": "PASS",
             "evidence": "Claim checked on both runtimes: CPython max abs 7.2e-15 (twin, this round) and Pyodide max abs 1.2e-14 (browser, this round). Both are order 10^-14. The claim is true on both; the regenerated digit does not change it. Line 337 'to rounding error' (hypothesis) is also true on both."})
rows.append({"id": "L03-L04-r6-grep-old-digits", "check": "2.9-structure",
             "location": "course/modules/AP/AP1/L03.html, L04.html, cards.json, tests/labs/AP1/*, and the pinned tree (git grep)",
             "status": "PASS",
             "evidence": "`grep -n -E '7\\.8|8\\.9'` over both pages, cards.json and the twins: no hit. `grep -n -E 'e-15 to 1|E_T.x.* x. - 1'` over the same files: L03 line 443 (new digit -2.0e-15), L04 line 358 (new digit 7.2e-15) and the twin's print statement (L04 print line in lab-AP1-L04-4.py and L04.html line 355). `git grep -n -E '7\\.8e-?16|8\\.9e-?15' 1325ded -- ':!ledgers'` -> no hit in course/, tests/, tools/, curriculum/ or references/. 'machine precision' appears only at L03 line 444 ('the margin is 0 to machine precision'); the margin printed on line 443 is +0.000e+00 on CPython, so that statement is true (no Pyodide margin exists, see r6-pyodide-scope)."})
rows.append({"id": "L03-L04-r6-pyodide-scope", "check": "2.5-lab",
             "location": "course/modules/AP/AP1/L03.html Run buttons; L03.html line 443-444 claims; L04.html line 358-361 claims",
             "status": "PASS",
             "evidence": "Scratch Playwright run (/tmp/ap1-r5/L03-L04/pyodide/capture_outputs.py) clicked every Run button on both pages: L03 has 2 (labs 1, 2), L04 has 4 (labs 1-4). The sol-AP1-L03-E1/E2 snippets are checked locally only (run_labs and the page's own comment: 'checked solution code is run by the student locally, not on the page'). So the L03 line 443-444 digit and margin claims are CPython-only and make no Pyodide claim; the L04 claim (row r6-prose-L04-361-order) is checked on both runtimes."})
rows.append({"id": "L03-L04-r6-recompute-scripts", "check": "2.2-number",
             "location": "round-5 scripts /tmp/ap1-r5/L03-L04/scripts/{recompute_examples,r3_lp,r3_lp2,r3_ray,r3_tail}.py",
             "status": "PASS",
             "evidence": "Re-run on 1325ded's toolchain (3.14.8, numpy 2.4.6, scipy 1.18.0): recompute_examples.py output identical to the round-5 log (diff empty); r3_lp.py, r3_lp2.py, r3_ray.py, r3_tail.py outputs identical to their round-5 logs (diff empty). These re-derive Example 2.3, M1-M3, E3, R2, Example 4.2, Example 5.1, Problem R3 bounds (0.410000058 and 0.7 etc.) and the Lab 3 KKT numbers that the carried rows cite."})

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
missing = set(P) - set(ids)
print("prev ids not yet handled:", sorted(missing))

order = {rid: i for i, rid in enumerate(P)}
rows.sort(key=lambda r: (order.get(r["id"], 10_000), r["id"]))
for r in rows:
    if r["status"] != "PASS":
        assert r.get("fix"), r["id"]
    assert set(r) >= {"id", "check", "location", "status", "evidence"}, r["id"]
n = len(rows)
npass = sum(r["status"] == "PASS" for r in rows)
fails = [r["id"] for r in rows if r["status"] != "PASS"]
verdict = "PASS" if not fails else "FAIL"
now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
frag = {
    "unit": "AP1",
    "slice": "L03-L04",
    "round": 6,
    "verifier": "round-6 independent verifier for slice L03-L04 (did not build AP1; shares no context with the builders or earlier verifiers)",
    "pin": "1325ded",
    "base": "33fd452",
    "previous_ledger": "ledgers/AP1/L03-L04.json as it stood in this checkout at the start of round 6 (the round-5 fragment, pin 33fd452: 83 rows, 83 PASS). Read in full: all 83 rows, every evidence field. The committed copy at 1325ded is the round-4 fragment (commit f574bfa) and was not the round-5 record.",
    "checkout": "/tmp/verify-ap1-r8-i (detached worktree at 1325ded)",
    "scratch": "/tmp/ap1-r5/L03-L04",
    "verified_at": now,
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice delta 33fd452..1325ded: exactly four changed lines in the slice: L03.html line 443 (the 'shade exact gap' line of the sol-AP1-L03-E2 expected block: -7.8e-16 -> -2.0e-15) and L04.html line 358 (the Lab 4 expected block: max abs 8.9e-15 -> 7.2e-15). Both are regenerated digits. No other slice file changed (cards.json, tests/labs/AP1, references, notation, market data and curriculum are byte-identical; index.html, tools/data_sources.yaml, tools/page_smoke.py and pyproject.toml changed outside the slice and were re-checked where they touch it).",
        "Digit rulings. (1) No prose, card, example or claim relies on the old digits -7.8e-16 or 8.9e-15: a grep over the slice, cards and twins finds no 7.8 or 8.9 and no old digit anywhere in the pinned tree outside ledgers/. (2) The regenerated digits are what the twins print under python -I -W error (CPython, rows r6-digit-L03-E2 and r6-digit-L04-4). (3) Pyodide: the L04 Lab 4 digit was captured in the browser (1.2e-14); the L03 snippet is not run in the browser, so no Pyodide digit exists for line 443. (4) Judgement: the L03 line 444 sentence 'rounding ... would be of order 10^-16 on cash flows of order 1' is contradicted by the regenerated -2.0e-15 in the same block (order 10^-15). The conclusion is unaffected, but the stated magnitude is not. FAIL with a one-token fix (rows L03-L04-r6-prose-L03-444-rounding, L03-L04-math-L03-E2, L03-L04-num-L03-E2). The caller may overrule this as an order-of-magnitude hedge; the verifier fails closed.",
        "Statement 'the margin is 0 to machine precision' (L03 444): margin printed +0.000e+00 on CPython; the snippet has no Pyodide run. True as written.",
        "L04 'pricing errors of the order of 10^-14' (L04 361): true on CPython (7.2e-15) and Pyodide (1.2e-14).",
        "Toolchain unchanged from round 5 (Python 3.14.8, numpy 2.4.6, scipy 1.18.0; vendored Pyodide scipy 1.18.0). Every command row was re-run on 1325ded; every carried numeric row was carried only because its lines are outside the changed hunks AND the lab outputs / recomputation scripts were re-run this round (run_labs, recompute_examples.py, r3_*.py identical to their round-5 logs).",
        "Carry convention: byte-identical subjects use 'Carried from round 5 (<files> byte-identical since 33fd452)'; L03.html and L04.html use the line-level variant with the hunk header from `git diff -U0 33fd452 1325ded`. Round-5 evidence text is retained after the prefix.",
        "Quiz stems ending in an ellipsis (L03 537, 546, 569; L04 524, 547, 556) are judged PASS by carry from round 5 as answer cues. This is a verifier judgement, not a machine check.",
        "Live citation check: `verify_refs.py --unit AP1` -> 9 of 560 entries, 0 problems (no proxy error this round). Mutants: none (the slice has no grader).",
        "Pyodide and CPython statements: the rounding-noise claims are order-of-magnitude statements. Judged on the claims: the 10^-14 claim holds on both runtimes; the 10^-16 claim fails on CPython, where the page's own output shows 10^-15.",
    ],
    "summary": {"rows": n, "pass": npass, "fail": n - npass, "unverifiable": 0, "mutants": 0, "fail_ids": fails},
}
OUT.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", OUT, "rows", n, "pass", npass, "fail", fails, "verdict", verdict)
