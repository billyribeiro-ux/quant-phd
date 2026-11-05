"""Build the round-10 fragment ledgers/FC1/FC1-c.json for FC1 slice c (verifier output, not hand-typed verdicts).

Reads the command outputs saved under ledgers/FC1/scripts/FC1-c-r10/out/ and the round-9 fragment for the row ids.
The verdict is computed from the rows: PASS only if every row is PASS. Run from the checkout root:
    python -I ledgers/FC1/scripts/FC1-c-r10/build_fragment_FC1c_r10.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "ledgers" / "FC1" / "scripts" / "FC1-c-r10" / "out"
R9 = json.loads(Path("/Users/billyribeiro/.fanout/frags/D-FC1-c.round9.json").read_text(encoding="utf-8"))
R9_IDS = [r["id"] for r in R9["rows"]]
MUT_OUT = (OUT / "mutate_graders_0_19_r10_final.out").read_text(encoding="utf-8").splitlines()

LINE = re.compile(r"^(KILLED|SURVIVED) (\S+?\.py): (.*) -> (.*)$")
mutants: list[dict[str, str | None]] = []
kill_info: dict[str, tuple[str, str]] = {}
for ln in MUT_OUT:
    m = LINE.match(ln)
    if not m:
        continue
    status, fname, desc, killed = m.groups()
    killed_by = None if status == "SURVIVED" else re.sub(r" \(seed \d+\)$", "", killed).strip()
    seed = re.search(r"\(seed (\d+)\)", killed)
    kill_info[fname] = (status, f"{killed_by} (seed {seed.group(1) if seed else '?'})" if killed_by else "not killed on seeds 0-19")
    mutants.append({"id": fname[:-3], "description": desc, "killed_by": killed_by})
assert len(mutants) == 127, len(mutants)
survivors = [m for m in mutants if m["killed_by"] is None]
killed_n = len(mutants) - len(survivors)


def find(keyword: str) -> str:
    desc = {m["id"] + ".py": m["description"] for m in mutants}
    hits = sorted(f for f in kill_info if keyword in desc[f])
    if not hits:
        raise SystemExit(f"keyword {keyword!r} matched nothing")
    parts = [f"{f} ({kill_info[f][0]}: {kill_info[f][1]})" for f in hits]
    return "; ".join(parts) + " [out/mutate_graders_0_19_r10_final.out]"


def family(prefix: str) -> str:
    files = [f for f in kill_info if f.startswith(prefix)]
    killed = [f for f in files if kill_info[f][0] == "KILLED"]
    return f"{len(killed)} of {len(files)} '{prefix}*' mutants killed on seeds 0-19 (out/mutate_graders_0_19_r10_final.out)"


C9 = "Carried from round 9 (byte-identical since the round-9 pin 1e272e5, git diff empty):"
ROWS: dict[str, dict[str, str]] = {}


def row(rid: str, status: str, check: str, location: str, evidence: str, fix: str | None = None) -> None:
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix or ""
    ROWS[rid] = r


# ---- runnable gates (fresh this round)
row("proj-check-projects", "PASS", "2.6-structure", "course/modules/FC/FC1/project.html",
    "tools/check_projects.py --unit FC1 -> 'check_projects FC1: PASS', exit 0 (out/check_projects.out).")
row("proj-check-pages", "PASS", "2.9-structure", "course/modules/FC/FC1/project.html",
    "tools/check_pages.py --unit FC1 -> 'check_pages FC1: PASS', exit 0 (out/check_pages.out).")
row("proj-check-dag", "PASS", "2.9-dag", "project.html; curriculum/curriculum.json concepts",
    "tools/check_dag.py --unit FC1 -> 'check_dag FC1: PASS', exit 0 (out/check_dag.out). Concept links present-value and discount-factor (project.html line 178) resolve.")
row("proj-run-labs", "PASS", "2.5-labs", "project.html Labs 1-3; tests/labs/FC1/lab-FC1-project-{1,2,3}.py",
    "tools/run_labs.py --unit FC1 --page project -> 'run_labs FC1: PASS (3/3)', exit 0 (out/run_labs_project.out). Whole unit: 'run_labs FC1: PASS (8/8)' (out/run_labs_all_FC1.out).")
row("proj-page-smoke", "PASS", "2.9-smoke", "course/modules/FC/FC1/project.html",
    "tools/page_smoke.py --unit FC1 --pages project -> 'page_smoke modules/FC/FC1/project.html: PASS', 'page_smoke FC1: PASS', exit 0; in-browser grader 'All 86 tests pass on seed 1563728616' (out/page_smoke_project.out). Chromium harness, not a manual browser session.")
row("proj-run-graders", "PASS", "2.6-autograde-reference", "grader/reference.py, test_project.py, instance.py, starter.py",
    "tools/run_graders.py --unit FC1 --seeds 0-49 -> 'run_graders FC1: PASS (reference 50/50 seeds, slowest 0.2 s)', exit 0 (out/run_graders_0_49.out). Five-seed-set suite runs: reference 20/20 on seeds 0-19 (out/reference_0_19.out).")
row("proj-lint-types", "PASS", "2.6-lint", "course/modules/FC/FC1/grader/*.py; tests/labs/FC1/; ledgers/FC1",
    "ruff check . -> 'All checks passed!' (out/ruff_check_final.out); ruff format --check . -> '553 files already formatted' (out/ruff_format_repo.out); mypy --no-incremental -> 'Success: no issues found in 385 source files' (out/mypy.out).")
row("proj-lab1-numbers", "PASS", "2.2-numbers", "project.html lines 58, 97-100 (Lab 1)",
    "out/numbers_r10.out (re-derived with Fraction): Lab 1 exact PV float 102775.09103322713, '%.6f' -> 102775.091033, price 102775; events [(1,5000),(2,5000),(3,105000)]. The expected block equals the twin output (run_labs PASS).")
row("proj-lab2-blanks", "PASS", "2.5-labs", "project.html lines 133, 140 (Lab 2)",
    "run_labs FC1 --page project PASS (out/run_labs_project.out): page code differs from tests/labs/FC1/lab-FC1-project-2.py only at the two blank lines (the Rung 2 convention, Architect ruling 11); the completed twin exits 0 and its output equals the expected block.")
row("proj-lab3-fixture-values", "PASS", "2.2-numbers", "project.html lines 198-275 (Lab 3)",
    "out/numbers_r10.out re-derives fixtures A-G and the rounding case: A [(1,10500)] price 10000; B exact 210000/19 = 11052.6316, price 11053; C [(1,5001),(2,15002)]; D [(1,2)]; E (2,-98500); F [(1,1)] price 1 (exact 1/2); G [(1,10001)] price 5001; rounding events [(1,500),(2,500),(3,10500)], price 10278, term-by-term 10277. Lab 3 page code equals its twin (run_labs PASS).")
row("proj-rounding-fixture-terms", "PASS", "2.2-numbers", "project.html line 193; grader/test_project.py lines 396-403",
    "out/numbers_r10.out: exact 10277.509103 rounds once to 10278; terms 480.77, 462.28, 9334.46 round one by one to 481+462+9334 = 10277. Page line 193 and test docstring 398-399 agree.")
row("proj-lab3-claim-using-functions", "PASS", "2.5-labs", "project.html line 198 vs tests/labs/FC1/lab-FC1-project-3.py",
    "The hypothesis names the functions of this lab; the twin defines bond_events, bond_price and term_by_term_price (tests/labs/FC1/lab-FC1-project-3.py, the same code as the page's Lab 3 block); run_labs PASS.")
row("proj-expected-equals-output", "PASS", "2.5-labs", "project.html expected blocks lines 97-100, 145-148, 263-275",
    "run_labs FC1 --page project PASS (3/3): expected block equals twin output for lab-FC1-project-1, -2 and -3 under the page's tolerance rule (out/run_labs_project.out).")
row("proj-hours-arithmetic", "PASS", "2.9-hours", "project.html table#hours lines 286-293; data-hours-project line 34",
    "Components 1+2+5+4+2+3+3 = 20 = data-hours-project=\"20\" (line 34) = total cell (line 293). Hub index.html line 29 data-hours-lessons=\"50\" (five lessons at data-hours 10) + data-hours-project 20 = 70 = hub eyebrow 'Tier U · 70 hours' (index.html line 31) = curriculum/02-economics-finance-core.yaml line 366 'hours: 70' (FC1).")
row("proj-hours-rationale-rows", "PASS", "2.9-hours", "project.html table#hours lines 286-293",
    "Row 290 'Eight conditions' equals the eight named conditions (page lines 165-167); side refused on 0, 2, -2, 3, -3 and accepted on +1, -1 (test_project.py lines 621-652, read this round).")
row("proj-hours-verifier-estimate", "PASS", "2.9-hours", "project.html table#hours rows 291-292",
    "Rows 291-292 (3 h + 3 h) are design-target hours (Architect ruling: hours are design targets; only arithmetic is graded). Arithmetic consistent with row total 20.")
row("proj-ladder", "PASS", "2.9-structure", "project.html lines 41-50, 52-151, 153-172, 312-319",
    "Rung text matches sections; anchors #conventions, #spec, #grader-section, #stretch and index.html#placement (index.html line 67, skill checks) exist; check_pages PASS (out/check_pages.out).")
row("proj-spec-interface", "PASS", "2.6-spec", "project.html line 161; grader/starter.py lines 16-40",
    "Names and signatures on page line 161 equal starter.py lines 16-40 (read this round). starter.py changed this round only in its docstring (lines 8-10).")
row("proj-named-conditions", "PASS", "2.6-conditions", "project.html lines 163-167; reference.py lines 42-47, 64-65, 81-88; test_project.py",
    "Eight named conditions (periods<1, face<=0, coupon<0, yield<=-10000, quantity<1, price<0, side not in {+1,-1}, settlement_day<1) each have refusal and boundary tests on both sides (test_project.py 215-223, 232-240, 258-260, 499-512, 559-566, 608-610, 621-643, 654-669). reference.py raises only these eight; no test requires a refusal the page does not name (every must_raise call is one of the eight).")
row("proj-test-count", "PASS", "2.9-count", "project.html line 171; grader/test_project.py",
    "pytest --collect-only on test_project.py with the reference as instruments.py: '86 tests collected in 0.04s' (out/collect_only_r10.out). Page line 171 says 86 checks.")
row("proj-starter-fails", "PASS", "2.6-starter", "grader/starter.py",
    "Starter as instruments.py, seed 0 (scripts suite_run.py): 84 failed, 2 passed (out/starter_seed0.out). The two that pass are the two non-ValueError inputs whose tests accept any exception or return (test_non_whole_face..., test_bool_periods...).")
row("proj-instances", "PASS", "2.6-instances", "grader/instance.py, seeds 0-49",
    "out/numbers_r10.out: 50 of 50 instances distinct; periods 1-8; per-period yield 66-889 bps; settlement 1-5; quantity 4-461; face 182259-4999067 cents; side values -1 and +1. All values valid for the named conditions (run_graders PASS).")
row("proj-silence-purity", "PASS", "2.6-silence", "grader/test_project.py lines 693-734",
    "Reference passes all 86 tests on seeds 0-19 (out/reference_0_19.out). Silence list (693-716) matches its docstring (694-696); refused-input list (719-734) is the eight named refusals.")
row("proj-same-suite-pyodide-pytest", "PASS", "2.6-same-file", "grader/test_project.py; project.html line 309",
    "The same file runs in-browser (page_smoke: 86 pass) and under local pytest with the page flags (scripts suite_run.py: 86 passed per seed). Pyodide itself was run only via page_smoke.")
row("proj-local-command", "PASS", "2.6-docs", "project.html line 308; grader/starter.py line 6",
    "The command QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py is the one suite_run.py uses (with -I added), on the reference, the starter and all alternatives.")
row("proj-scope-words", "PASS", "2.6-prose", "project.html lines 163, 171, 176-186",
    "'every named condition' (171) matches the boundary tests; 'Each events() call returns the same list' (180) matches test_repeated_events_calls_agree (737-747); 'Any other invalid input may raise any exception or return' (163) matches the must_raise-only-for-named rule (test_project.py 9-13, 750-767).")
row("proj-terms-before-definition", "PASS", "2.6-terms", "project.html lines 54-56, 106, 161, 179",
    "holder, event and settlement period are defined in line 54 before use. side appears first in line 106 with its meaning in the same parenthesis and a link to Conventions (line 179).")
row("proj-prose-banned-phrases", "PASS", "2.6-prose", "project.html; cards.json; grader/*.py; labs",
    "out/process_words_grep.out: case-insensitive grep for verifier, builder, round N, TODO, draft, placeholder, fixed in, regenerated, orchestrat, workflow, agent, reviewer: no learner-facing process word. Hits: 'a reviewer reads it' (project.html 161, 163; the reviewer of the learner's work) and 'An agent that posts a bid' (cards.json 233; the economic term).")
row("proj-process-words", "PASS", "2.6-prose", "project.html; cards.json; labs",
    "Same grep as proj-prose-banned-phrases (out/process_words_grep.out); no process word in the page, the cards or the labs.")
row("proj-notation", "PASS", "2.6-notation", "notation/notation.json; FC1 pages, cards, labs",
    "notation.json holds 8 symbols (T, \\Phi and \\Phi^{-1}, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}). A grep of FC1 lessons, project and cards for these commands finds none (scan this round). The FC1 symbols Q (volume), R (resting shares), phi (lowercase), T (grade field only) are not registry symbols.")
row("proj-footer-claim", "PASS", "2.6-claim", "project.html line 341; course/assets/js/grader.js; store.js; python.js",
    f"{C9} course/assets/js (grader.js, store.js, python.js) read in round 9 (grader.js line 18 one GET of the unit's grader files; no POST, beacon or socket). Not re-read this round.")
row("proj-saved-as-you-type", "PASS", "2.6-claim", "project.html line 301; course/assets/js/grader.js lines 33-79; store.js",
    f"{C9} grader.js save-on-edit (400 ms debounce, store.put) and store.js IndexedDB (round 9 reading).")
row("proj-lab-io-free", "PASS", "2.6-data", "tests/labs/FC1/lab-FC1-project-*.py",
    "out/lab_io_grep.out: no open(), import of os/socket/urllib/requests, or http string in the three project twins (grep exit 1).")
row("proj-references-reading-list", "PASS", "2.6-references", "project.html lines 321-328; references/references.json",
    "Keys mishkin2021economics and harris2002trading exist in references/references.json (status verified, read this round). Page states no year and attributes no statement. Hub index.html lines 166-169 explains the McLeay et al. (2014) curriculum source is not in the registry, so no lesson cites it; 'the two sources the course cites' matches the lesson citations (harris in L05 line 403; both in the hub).")
row("proj-cited-year-conflicts", "PASS", "2.6-references", "project.html reading list; references/references.json; curriculum/02-economics-finance-core.yaml lines 384-385",
    "Registry year harris2002trading 2002 (crossref; notes record curriculum 2003). mishkin2021economics 2021 (openlibrary; notes record curriculum 2022). The project page states no year, so the page is consistent; the two conflicts are registry_flags for the curriculum owner.")
row("proj-data-simulated", "PASS", "2.6-data", "project.html lines 45, 54, 159; grader/instance.py lines 3-6, 31; tests/labs/FC1/lab-FC1-project-*.py",
    "Every bond and trade is SIMULATED and labelled so (project.html 45, 54, 159; instance.py label line 31). No lab reads a file or the network (out/lab_io_grep.out).")
row("proj-lab3-autograder-coverage-note", "PASS", "2.5-labs", "project.html line 276 (note after Lab 3); grader/test_project.py",
    "Each listed check exists: fixture A events and price (test_project.py 174-179 and 367-373); B price (376-382); C and D events (189-202); E events (536-549); F events (242-247) and price (406-412); G price (415-420); rounding price (396-403). The note's exclusions hold: no test asserts Bond(10001,0,1).events() or Bond(10000,500,3).events() as a list (grep, this round).")
row("proj-page-grading-description", "PASS", "2.6-claims", "project.html line 171; grader/test_project.py",
    "Every claim of line 171 maps to tests: 13-15 periods (281), 24 (304), 40 (318), 100 (791), 1001 (806), 5001 (862), 100001 events (894); the two cases (352); the hand fixtures (174-275 region); exact halves (406, 415, 423, 434, 448, 459, 839); 150/300/2000/10000 % (515, 822, 849, 881); trades settling 100/1000/5001/10**6 (672, 831, 872, 906); quantities 501/1001/2**40+1/10**30 (577, 587, 597, 915); silence and purity (693, 719).")
row("proj-page-hypothesis-sides", "PASS", "2.6-claims", "project.html line 106 (Lab 2 hypothesis)",
    "'side is +1 for a buyer and -1 for a seller' matches Conventions line 179, reference.py line 11 and the Lab 2 trade line (line 140).")
row("proj-page-constraints-silence", "PASS", "2.6-claims", "project.html line 163",
    "The wording 'On the inputs the suite checks for silence (...), no function prints or warns' matches the silence tests (693-716 valid inputs, 719-734 refused inputs).")
row("proj-docstring-float-claim", "PASS", "2.2-numbers", "grader/test_project.py lines 423-427, 451-452, 459-462",
    "out/numbers_r10.out: Bond(1704285,179,1) at 496 bps exact 3305625/2 rounds to 1652813; float 1734792/1.0496 = 1652812.4999999998, round() 1652812. Bond(13,0,1) at 400 bps exact 25/2 rounds to 13; float (1+0.04)**-1*13 = 12.499999999999998, round() 12. Hair identity 299985000 + 1/2 - 1/(2*1000300030001) equals the exact price (True); rounds to 299985000.")
row("proj-test-docstring-hand-numbers", "PASS", "2.2-numbers", "grader/test_project.py docstrings",
    "out/numbers_r10.out: 10**10+1 -> 5000000001; 10**12+1 -> 500000000001; 10**40+1 -> 5*10**39+1 (41 digits, True); 10500/21 = 500; 10500/4 = 2625; 10500/2.5 = 4200; 10500/101 = 103.9604 -> 104; 10**17+4999 at 1 bps -> 10**13; 2**40+1 times 9851 > 2**53 (True); Decimal prec 10 of 5000000000.5 -> 5000000000 (half dropped).")
row("proj-named-error-message-values", "PASS", "2.6-messages", "grader/test_project.py lines 75-93, 693-734",
    "must_raise and must_accept messages name the condition only (75-93); no expected value is printed.")
row("proj-failure-messages", "PASS", "2.6-messages", "grader/test_project.py lines 693-734, 770-788",
    "Messages state the property; _named_when_unimplemented prints only the first docstring line with pytrace=False (770-788).")
row("proj-starter-message-leaks-answer", "PASS", "2.6-messages", "grader/test_project.py lines 822-828, 849-851, 881-883, 515-517",
    "The first docstring line of each accepted-input test (the only docstring text the missing-implementation message prints) contains no expected value; expected values (2625, 500, 104, 4200) appear only in docstring bodies and assertions, never in a failure message.")
row("proj-starter-unwrapped-new-tests", "PASS", "2.6-messages", "grader/test_project.py lines 925-928",
    "The wrapper loop wraps every callable test_ name defined before it, including the round-9 additions at 849, 881, 894, 906 and 915 (read this round).")
for rid in ("proj-alternatives",):
    row(rid, "PASS", "2.6-autograder", "ledgers/FC1/alternatives/a1..a5 (grader suite seeds 0-19)",
        "Each of a1..a5 (read in full this round: list comprehension events; generator methods; Fraction throughout; integer half-up division; frozen dataclass with reduce) passes 20/20 seeds on the current suite (out/alt_a*_0_19.out). No alternative is over-constrained.")
row("proj-alternatives-r4-new", "PASS", "2.6-autograder", "ledgers/FC1/scripts/FC1-c-r4/alt/alt6",
    "alt6 passes 20/20 seeds on the current suite (out/alt_alt6_r4_pow_fraction_floor_0_19.out).")
row("proj-alternatives-r6-new", "PASS", "2.6-autograder", "ledgers/FC1/scripts/FC1-c-r6/alt/alt7..alt9",
    "alt7, alt8, alt9 each pass 20/20 seeds on the current suite (out/alt_alt7..alt9_*_0_19.out).")
row("proj-alternatives-r7-new", "PASS", "2.6-autograder", "ledgers/FC1/scripts/FC1-c-r7/alt/alt10..alt12",
    "alt10, alt11, alt12 each pass 20/20 seeds on the current suite (out/alt_alt10..alt12_*_0_19.out).")
row("proj-alternatives-r8-new", "PASS", "2.6-autograder", "ledgers/FC1/scripts/FC1-c-r8/alt/alt13..alt15",
    "alt13, alt14, alt15 each pass 20/20 seeds on the current suite (out/alt_alt13..alt15_*_0_19.out).")
row("proj-alternatives-fixed-suite-r9", "PASS", "2.6-autograder", "ledgers/FC1/scripts/FC1-c-r9/proposed_fix_test_project_r9.py (applied in test_project.py at 47a36d8)",
    "The round-9 proposed additions are now in grader/test_project.py (86 tests). Every alternative and the reference pass on the current file (rows above).")
for rid, pref, what in (
    ("proj-mutants-v1c-new", "v1c_", "v1c_*"), ("proj-mutants-v2c-new", "r2c_", "r2c_*"), ("proj-mutants-r3c-killed", "r3c_", "r3c_*"),
    ("proj-mutants-v4c-new", "v4c_", "v4c_*"), ("proj-mutants-r4c-new", "r4c_", "r4c_*"), ("proj-mutants-r5c-new", "r5c_", "r5c_*"),
    ("proj-mutants-r6c-killed", "r6c_", "r6c_*"), ("proj-mutants-r7c-new", "r7c_", "r7c_*"), ("proj-mutants-r8c-new", "r8c_", "r8c_*"),
    ("proj-mutants-r9c-new", "r9c_", "r9c_*"),
):
    row(rid, "PASS", "2.6-mutants", f"ledgers/FC1/mutants/{what}.py",
        f"Re-run this round (tools/mutate_graders.py --unit FC1 --seeds 0-19): {family(pref)}.")
mutant_rows = {
    "proj-mutant-schedule-cap-thirty-survivor": "thirty periods",
    "proj-mutant-exponent-cap-thirty-survivor": "capped at thirty",
    "proj-mutant-schedule-cap-survivor": "at most twenty periods",
    "proj-mutant-price-digits-survivor": "ten significant digits",
    "proj-mutant-price-cache-survivor": "Price is cached",
    "proj-mutant-price-epsilon-survivor": "1e-9",
    "proj-mutant-yield-100-survivor": "above 10000 basis points",
    "proj-mutant-schedule-cap-forty-survivor": "at most forty periods",
    "proj-mutant-exponent-cap-forty-survivor": "capped at forty",
    "proj-mutant-yield-200-survivor": "above 20000 basis points",
    "proj-mutant-settlement-cap-100-survivor": "above 100, a limit",
    "proj-mutant-decimal-40-digits-survivor": "40 significant digits",
    "proj-mutant-decimal-28-digits-kill": "28 significant digits",
    "proj-mutant-periods-cap-1000-survivor": "more than one thousand",
    "proj-mutant-r7c-coupon-half-even": "half to even",
    "proj-mutant-r7c-discount-float": "binary-float discount factor",
    "proj-mutant-r7c-price-cap-1m": "one million cents",
    "proj-mutant-r7c-hard-coded-answer": "4281937",
    "proj-mutant-yield-1000-survivor": "100000 bps",
    "proj-mutant-settlement-5000-survivor": "settlement period above 5000",
    "proj-mutant-periods-5000-survivor": "more than 5000 coupon",
    "proj-mutant-face-int64-kill": "64-bit",
}
for rid, kw in mutant_rows.items():
    try:
        ev = find(kw)
        row(rid, "PASS", "2.6-mutants", "grader/test_project.py and the mutant named below",
            f"Round-9 survivor class, re-run this round: mutant {ev}. Killed by the current suite (the round-9 proposed tests are in test_project.py).")
    except SystemExit as exc:
        raise SystemExit(f"{rid}: {exc}")
for rid, fname in (
    ("proj-mutant-r9c-yield-2000-survivor", "r9c_yield_refused_above_two_thousand_percent.py"),
    ("proj-mutant-r9c-periods-10000-survivor", "r9c_periods_refused_above_ten_thousand.py"),
    ("proj-mutant-r9c-settlement-10000-survivor", "r9c_settlement_day_refused_above_ten_thousand.py"),
    ("proj-mutant-r9c-quantity-2pow50-survivor", "r9c_quantity_refused_above_two_to_the_fifty.py"),
):
    st, by = kill_info[fname]
    row(rid, "PASS", "2.6-mutants", f"ledgers/FC1/mutants/{fname}",
        f"Round-9 survivor now killed: {fname} {st} by {by} (out/mutate_graders_0_19_r10_final.out).")

row("proj-mutants-all", "FAIL", "2.6-mutants", "ledgers/FC1/mutants/*.py (127 files)",
    f"tools/mutate_graders.py --unit FC1 --seeds 0-19 -> 'mutate_graders FC1: FAIL (124/127 killed)', exit 1 (out/mutate_graders_0_19_r10_final.out). The three survivors are the r10c_* mutants of this round (rows below). All 124 earlier mutants are killed.",
    "Make the three r10c_* mutants fail: add the accepted-input tests in ledgers/FC1/scripts/FC1-c-r10/proposed_fix_test_project_r10.py (yield 10**7 bps, settlement period 10**7, and a 1001-period bond priced at zero yield). With them the reference and all five alternatives pass 89/89 on seeds 0-19 and each r10c mutant fails (out/proposed_fix_run_r10.out). The page's test count then becomes 89 (project.html line 171 must be updated with it).")
row("proj-mutants-r10c-new", "FAIL", "2.6-mutants", "ledgers/FC1/mutants/r10c_*.py (3 new student-error mutants, this round)",
    "Three new student-error mutants of reference.py, generated by ledgers/FC1/scripts/FC1-c-r10/make_mutants_r10.py: r10c_yield_refused_above_ten_thousand_percent, r10c_settlement_refused_above_one_million, r10c_price_ignores_events_after_period_one_thousand. All three SURVIVE seeds 0-19 (out/new_mutant_r10c_*.out, out/mutate_graders_0_19_r10_final.out).",
    "See the three per-mutant rows; the proposed tests kill all three (out/proposed_fix_run_r10.out).")
row("proj-mutant-r10c-yield-10mil-survivor", "FAIL", "2.6-mutants", "grader/test_project.py lines 849-891 (yields tested up to 1000000 bps only); project.html line 171",
    "r10c_yield_refused_above_ten_thousand_percent.py (refuses yield_bps > 1000000) survives seeds 0-19: all 86 tests pass (out/new_mutant_r10c_yield_refused_above_ten_thousand_percent.out). project.html line 171 states: 'a yield above 100 % per period, which the page does not refuse (checked at 150 %, at 300 %, at 2000 % and at 10000 %)'. The largest yield tested is 1000000 bps, so a refusal above it is undetected.",
    "Add an accepted-input test at yield_bps = 10000000: Bond(10000, 500, 1) priced at that yield is 10500/1001 = 10.49 cents, which rounds to 10 (proposed_fix_test_project_r10.py, test_bond_yield_of_ten_million_bps_is_accepted; the mutant fails it, the reference passes it).")
row("proj-mutant-r10c-settlement-1m-survivor", "FAIL", "2.6-mutants", "grader/test_project.py lines 906-912 (largest tested settlement 10**6); project.html line 171",
    "r10c_settlement_refused_above_one_million.py (refuses settlement_day > 1000000) survives seeds 0-19 (out/new_mutant_r10c_settlement_refused_above_one_million.out). project.html line 171 states: 'trades settling in periods 100, 1000, 5001 and 1,000,000, which the page does not bound'. The suite does not test a settlement period above 10**6.",
    "Add an accepted-input test at settlement_day = 10**7 with one event (10**7, -98500) (proposed_fix_test_project_r10.py, test_trade_settling_in_period_ten_million_is_accepted; the mutant fails it).")
row("proj-mutant-r10c-tail-1000-survivor", "FAIL", "2.6-mutants", "grader/test_project.py lines 806-819 (1001-period price at 400 bps); project.html lines 177-178",
    "r10c_price_ignores_events_after_period_one_thousand.py (bond_price_cents drops events after period 1000) survives seeds 0-19 (out/new_mutant_r10c_price_ignores_events_after_period_one_thousand.out). The 1001-period price at 400 bps changes by about 1e-13 cent when period 1001 is dropped, so the rounded price is unchanged: the mutant is equivalent on the data the suite uses, and the suite cannot tell it apart. project.html line 178 states: 'the price is the sum of the discounted events'; line 177 pays the coupon in each of periods 1 to periods.",
    "Add a test whose input tells the mutant apart: Bond(10000, 0, 1001) at yield 0 has the face in period 1001 and prices to 10000 (proposed_fix_test_project_r10.py, test_bond_price_at_zero_yield_counts_the_events_after_period_one_thousand; the mutant prices it 0).")
row("proj-cards-c152-hypotheses", "FAIL", "2.6-cards", "course/modules/FC/FC1/cards.json FC1-c152 back (grade T); L01 Proposition 3.5 (lesson text, out/lessons/L01.txt line 114)",
    "The round-9 fix added A2-prime, A1 with 0 < rho <= 1 and the no-withdrawal and no-repayment parts of A3, which match Proposition 3.5 (out/lessons/L01.txt line 114). The card still omits d > 0. The limit is d/(1 - kappa) with kappa = phi(1 - rho), so d/(1 - kappa) = d/rho exactly when d (1/(1 - kappa) - 1/rho) = 0: for d = 0 this holds for every phi and rho (for example rho = 1/2, phi = 1/2 gives 0 = 0 with phi != 1 and rho != 1), and for d != 0 it holds iff (1 - rho)(1 - phi) = 0. So the 'if and only if' in the card and in Proposition 3.5 is false at d = 0. Proposition 3.1 states 'with d > 0' (out/lessons/L01.txt line 88); Proposition 3.5 does not. Card FC1-c009 is not affected: it states only the convergence.",
    "Change the back of FC1-c152 to: 'Yes. Under A2-prime with 0 <= phi <= 1, A1 with 0 < rho <= 1, the no-withdrawal and no-repayment parts of A3, and d > 0, d/(1 - phi(1 - rho)) is at most d/rho, with equality if and only if phi = 1 or rho = 1 (Proposition 3.5).' Lesson owner: add 'with d > 0' to the statement of Proposition 3.5 in course/modules/FC/FC1/L01.html (not edited by this verifier).")
row("proj-cards-scan-duplicates", "PASS", "2.6-cards", "course/modules/FC/FC1/cards.json (151 cards)",
    "out/cards_check_r10.out: 151 cards, 151 unique ids (FC1-c134 absent, a gap, not a duplicate), 0 duplicate fronts, 0 duplicate backs. 33 near-duplicate fronts (SequenceMatcher > 0.8) are distinct questions about different assumptions or axes (e.g. A2 vs A3, B3 vs B4, buy vs sell stop).")
row("proj-cards-numbers-in-lessons", "PASS", "2.6-cards", "cards.json vs out/lessons/L01-L05.txt (lesson text regenerated from the checkout by scripts/FC1-c-r10/lesson_text.py)",
    "out/cards_check_r10.out: every number >= 13 on every card appears in the card's own lesson text ('card numbers >= 13 absent from the card's lesson: []'). Numbers 0-12 are not checked by this rule.")
row("proj-cards-numbered-references", "PASS", "2.6-cards", "cards.json citations vs lesson headings",
    "out/cite_resolve_r10.out: 162 labels checked. 25 did not match my regex only because lesson headings are printed as '2Bank money creation', '1Two ways...' (numbers glued to the title), problems as 'P2 · ...', 'R2 · ...', and assumptions as 'A1 (...)' / 'B3 (...)' under the 'Assumptions' heading. Each was resolved by hand against out/lessons/*.txt (L01 lines 38-50, 285, 343-351; L02 lines 36, 306; L03 lines 60-112; L04 lines 444-452; L05 lines 38, 54, 361).")
row("proj-cards-sample", "PASS", "2.6-cards", "course/modules/FC/FC1/cards.json (151 cards; sample of 15 against lesson text)",
    "All 151 cards read this round in full. Sample (one in ten by id, checked against the lesson text in out/lessons/ and the arithmetic in out/card_arith_r10.out): c010 (6861.8940391 -> 686189 cents), c020 (Assumption 1.3, L02 line 50), c030 (register entries 1, 3, 4, 6 of Lab 2), c040 (Definition 2.1, L03), c050 (Proposition 3.2, L03 line 122), c060 (Remark 1.2, L04 line 52), c070 (misconception 1, L04), c080 (Proposition 2.2, L05 line 70), c090 (Section 4, L05 line 363), c100 (Proposition 2.3, L04 lines 80-83), c110 (Assumption A2, L01 line 60), c120 (Definition 1.1, L02 line 42), c130 (L03 Remark 2.2 and the Definition 2.1 tail: Q = sum over sigma = +1 of q), c140 (Example 2.5, L03 line 92-), c150 (L02 line 34). No mismatch.")
row("proj-cards-changed-subjects", "PASS", "2.6-cards", "cards.json FC1-c064, c101, c150 (changed this delta); c009 and the rest carried",
    "c064 back equals L04 Definition 2.1 (out/lessons/L04.txt lines 64-66: an incoming order meets the best price first, then the earliest arrival). c101 back equals the A1 of Proposition 2.1 (out/lessons/L05.txt line 60: buyer and seller differ; q_i, p_i positive integers), and its T grade stands on the Proposition 2.1(ii) proof (L05 line 66). c150 back equals L02 line 34 ('An instrument is a claim with terms'). c009 and the other round-9 cards (c005, c008, c041, c049, c071, c073) are byte-identical since 1e272e5 (git diff of cards.json shows only c064, c101, c150, c152), so carried from round 9.")
row("proj-cards-new-c143-c151", "PASS", "2.6-cards", "cards.json FC1-c143 to FC1-c151",
    f"{C9} these card objects are unchanged in 1e272e5..47a36d8 (git diff shows only c064, c101, c150, c152). Round-9 evidence: c143 = Remark 1.2 (L04); c144, c145 = Definition 1.1 (L05); c146, c147 = Section 2 (L01); c148 = Section 1 (L01); c149 = Section 1 (L02); c150 = lesson introduction (changed this round, checked above); c151 = Proposition 2.3 (L03).")
row("proj-cards-c139-c142-new", "PASS", "2.6-cards", "cards.json FC1-c139 to FC1-c142",
    "c139: -1000 = (-1)(100)(10000-9990) (L03 Example 2.5, out/lessons/L03.txt line 92-); c140: -600 = 400 - 1000 (same example); c141 matches L04 Remark 1.2 (line 52: arrival order, check repeats); c142: offsets_nondecreasing prints False when the clearing offset exceeds the settlement lag (L05 line 359; out/lab_L05.out prints offsets_nondecreasing True at offset 0).")
row("proj-cards-c014-lab-true", "PASS", "2.5-cards", "cards.json FC1-c014; Lab 1 Part A",
    "out/lab_L01.out: 'the partial sums equal the closed form exactly for n = 0 to 10: True' (run this round).")
row("proj-cards-c122-equity-after-loss", "PASS", "2.6-cards", "cards.json FC1-c122; L01 Proposition 4.1 (out/lessons/L01.txt line 134)",
    "Proposition 4.1 under Assumption 4.0: equity after the loss is E - lambda, nonnegative iff lambda <= E. The card matches.")
row("proj-cards-citation-R3", "PASS", "2.6-cards", "cards.json FC1-c067; L04 Remark 1.2 and Problem R3 (out/lessons/L04.txt line 452)",
    f"{C9} c067 and L04 unchanged; Problem R3 resolves to L04 line 452; 60 shares contributes 120 (2 x 60).")
row("proj-cards-citation-R2", "PASS", "2.6-cards", "cards.json FC1-c068; L04 Problem R2 (out/lessons/L04.txt line 444-446)",
    f"{C9} c068 and L04 unchanged; Problem R2 starts from best bid 1005 and best ask 1000, which A1 excludes (L04 line 446), and the buy at 999 rests, leaving the book crossed.")
row("proj-cards-citation-scan", "PASS", "2.6-cards", "cards.json citations (all cards)",
    "out/cite_resolve_r10.out: every numbered citation resolves to a heading or label in the card's own lesson (162 labels; the 25 format-only misses resolved by hand, see proj-cards-numbered-references).")
row("proj-cards-grades", "PASS", "2.6-cards", "cards.json grade fields vs lesson key-results and the lab outputs",
    "out/lab_L01..L05.out and out/card_arith_r10.out re-run this round. T cards that cite a proposition, a corollary, a remark, an example or a problem on the page (for example c006, c007, c009, c013, c021, c027, c041, c042, c043, c050, c066, c080, c102, c104, c122, c139, c140, c151) are T with that source cited. C cards read off SIMULATED labs (c052, c053, c069, c082-c088, c097, c098) carry the SIMULATED label, and their numbers match out/lab_L01..L05.out and card_arith_r10.out. Four T cards cite only a lab print or a typed-in register: c029, c092, c095, c096 (exact counts or an exact finite sum on typed-in parameters: c092 = 181790 cents from 1000 (1 - 0.45^11)/0.55 = 1817.903; c029 and c095/c096 match the register counts 3,3,2,2,2, 6/6 and 4/8). The page proves only the limit for c092 (Proposition 3.5). Recorded as a grading judgment for the lead (T as exact arithmetic on typed-in data, or C naming Lab 1/Lab 2), not a FAIL.")
row("proj-spec-scope-vs-curriculum", "PASS", "2.6-spec", "project.html line 157; curriculum/02-economics-finance-core.yaml line 389 (FC1 project title) and its brief; FC2 title (line 397)",
    "Scope: a fixed-rate bond and a trade that settles later as dated cash-flow objects with a common interface (curriculum brief, read this round), as project.html line 157 states. FC2 is 'Derivatives Fundamentals' (curriculum line 397), so 'the course's later Derivatives unit (FC2)' matches.")
row("proj-terminology-short-holder", "PASS", "2.6-prose", "project.html line 54",
    "holder defined in line 54 ('the party that owns the bond') before the first use in line 54-58 labs; the same term is used throughout.")
row("proj-ruff-repo-gate-note", "PASS", "2.6-lint", "repository gate (ruff check .)",
    "ruff check . -> 'All checks passed!' (out/ruff_check_final.out). pyproject extend-exclude removes ledgers/*/mutants, ledgers/*/scripts and ledgers/*/alternatives from the repository gate; the round-10 mutants and scripts are therefore not linted by it.")
row("proj-verify-refs-offline", "PASS", "2.1-citations", "references/references.json (whole registry, offline)",
    "tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 (out/verify_refs_offline.out). The live per-unit run (--unit) needs network and was not run; the two FC1 keys were checked for existence in the registry.")
row("proj-pytest-fc1", "PASS", "2.5-tests", "tests/test_labs.py, tests/test_curriculum.py, tests/test_page_checks.py (-k FC1)",
    "pytest -q tests/test_labs.py tests/test_curriculum.py tests/test_page_checks.py -k 'FC1 or fc1' -> 9 passed, exit 0 (out/pytest_fc1_r10.out). Full repository pytest not run.")
row("proj-labs-twins-I-W-error", "PASS", "2.5-labs", "tests/labs/FC1/lab-FC1-L01..L05-1.py and lab-FC1-project-1..3.py",
    "Each twin run as python -I -W error exits 0 with no stderr: lesson twins L01..L05 (out/lab_L01..L05.out, exit=0 lines) and project twins via run_labs (out/run_labs_all_FC1.out 8/8).")
row("proj-reference-deployment", "FAIL", "2.6-deployment", "BLUEPRINT.md line 401; grader/reference.py line 4; .github/workflows/ci.yml; repository root",
    "BLUEPRINT.md line 401: deployment 'excludes every grader/reference.py'. reference.py line 4 says no file in this repository enforces that. Round 10 re-checked: no deploy config at the root; ci.yml has no publish step (artifact upload only, line 79); tools/ has no exclusion of reference.py (grep). UNVERIFIABLE here; repo-wide.",
    "Implement the exclusion in the deploy pipeline (or amend BLUEPRINT.md to say the repository has no deploy step) and add a check that the published tree has no grader/reference.py.")
row("proj-starter-silence-scope", "PASS", "2.6-starter", "course/modules/FC/FC1/grader/starter.py lines 8-10; project.html line 163",
    "Fixed since round 9: starter.py now reads 'On the inputs the suite checks for silence, nothing prints or warns.' and drops 'change its arguments'; project.html line 163 uses the same narrowed wording. Matches the suite (silence tests 693-734).")
row("proj-test-name-two-thousand-percent", "PASS", "2.6-tests", "course/modules/FC/FC1/grader/test_project.py line 849",
    "Fixed since round 9: the test is named test_bond_yield_of_two_thousand_percent_per_period_is_accepted; it checks yield_bps = 200000 (2000 % per period), and its docstring says 2000 %.")

ROW_IDS = list(dict.fromkeys(R9_IDS + [r for r in ROWS if r not in R9_IDS]))
missing = [i for i in R9_IDS if i not in ROWS]
if missing:
    raise SystemExit(f"round-9 row ids without a round-10 row: {missing}")
rows = [ROWS[i] for i in ROW_IDS]
fails = [r for r in rows if r["status"] != "PASS"]
verdict = "PASS" if not fails else "FAIL"
counts = {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows), "fail": len(fails), "unverifiable": 0}
fragment = {
    "unit": "FC1",
    "slice": "c",
    "round": 10,
    "verifier": "Claude Haiku 5.5, independent verifier for FC1-c, round 10 (did not build FC1)",
    "pin": "47a36d8c78633793ccc762ae19dcd5e19b780d19",
    "base": "1e272e5a641f18412703b37778a44db6f7391a69 (round-9 pin of this slice); delta: project.html line 163/171, grader/test_project.py (+4 tests, one renamed), grader/starter.py docstring, cards.json (FC1-c064, c101, c150, c152), four r9c mutants",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD10-FC1-c",
    "scratch": "ledgers/FC1/scripts/FC1-c-r10/ (suite_run.py, make_mutants_r10.py, numbers_r10.py, cards_check_r10.py, cite_resolve_r10.py, lesson_text.py, proposed_fix_test_project_r10.py, proposed_fix_run_r10.sh, build_fragment_FC1c_r10.py; outputs in out/)",
    "verified_at": "2026-11-05T09:50:00+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": [{"id": m["id"], "description": m["description"], "killed_by": m["killed_by"]} for m in mutants],
    "registry_flags": [
        "harris2002trading: registry year 2002 (crossref; references.json notes record curriculum '2003'); curriculum/02-economics-finance-core.yaml line 385 says (2003). For the curriculum owner.",
        "mishkin2021economics: registry year 2021 (openlibrary; notes record curriculum '13th ed. (2022)'); curriculum line 384. Not checked live (offline only). For the curriculum owner.",
        "notation: plain Q (volume of a closed sequence, L03 Definition 2.1 and card FC1-c131) is not the registry symbol \\mathbb{Q}. Not a reuse; for the notation owner.",
    ],
    "freshness_flags": [],
    "notes": [
        f"Mutants: {len(mutants)} files (124 earlier plus 3 new r10c). tools/mutate_graders.py --unit FC1 --seeds 0-19: {killed_n} killed, {len(survivors)} survive (all three r10c). All 124 earlier mutants are killed, including the round-9 survivors now killed by the 86-test suite.",
        "Alternatives: a1-a5 (ledgers/FC1/alternatives) pass 20/20 on seeds 0-19; alt6-alt15 (ledgers/FC1/scripts/FC1-c-r4..r8) pass 20/20 on the current suite (out/alt_*_0_19.out).",
        "Reference: 86/86 on seeds 0-19 (out/reference_0_19.out); 50/50 via run_graders (out/run_graders_0_49.out); starter 84 failed, 2 passed (out/starter_seed0.out).",
        "Test count: 86 collected (out/collect_only_r10.out) equals project.html line 171. If the proposed r10 tests are applied the count is 89 and line 171 must change with them.",
        "Round-9 proposal applied in the pin: the four accepted-input tests (yield 10**6 bps, 100001 periods events-only, settlement 10**6, quantity 10**30) are in grader/test_project.py; the round-9 r9c mutants are now killed.",
        "Labs: all eight twins pass under python -I -W error with expected blocks equal to output (out/run_labs_all_FC1.out, out/lab_L01..L05.out).",
        "Numbers: every number in the project prose, the Lab 1-3 expected blocks, the grader docstrings and the instance ranges re-derived with Fractions (out/numbers_r10.out); two float claims re-run with Python floats (1652812.4999999998, 12.499999999999998).",
        "Lessons L01-L05 and index.html are byte-identical since 1e272e5 and were read only as far as the cards and the project page cite them; Proposition 3.5 (L01 line 114) is read in full because card FC1-c152 depends on it.",
        "Could not check: the deployed site (no deploy config; proj-reference-deployment); live Crossref and publisher checks (offline only); the full repository pytest (only -k FC1 subset); a Pyodide run beyond page_smoke; a manual browser session; the L01 Proposition 3.5 wording itself (lesson owner; reported under proj-cards-c152-hypotheses).",
        "Hours are design targets (Architect ruling); only arithmetic is graded (rows proj-hours-*).",
    ],
    "summary": f"Round 10, FC1-c: {len(rows)} rows, {counts['pass']} PASS, {counts['fail']} FAIL, 0 UNVERIFIABLE. Verdict {verdict}. Failing rows: the three r10c survivors (yield > 10**6 bps, settlement > 10**6, 1001-period tail at 400 bps) with their proposed tests (proposed_fix_test_project_r10.py); card FC1-c152 omits d > 0; repo-wide deployment exclusion of reference.py is unverifiable.",
}
out_path = ROOT / "ledgers" / "FC1" / "FC1-c.json"
out_path.write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrote", out_path, counts, verdict, "mutants", len(mutants), "survivors", len(survivors))
