"""Build the SC1-b round-6 fragment from the round-5 row ids (SC1-b round 6 verifier)."""
import json
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE6-SC1-b")
R5 = json.loads(Path("/Users/billyribeiro/.fanout/frags/E-SC1-b.round5.json").read_text(encoding="utf-8"))
PREFIX = "Round 6 (pin 4bd8cb9; every changed hunk and the full L04-L06 text re-read this round): "

over = {
    "b-assumed-facts-statement": (
        "PASS",
        "L05.html:94 (Lemma 1.3 statement 'Assuming A4(a) and A4(f)'), :110 (Theorem 1.4 'Assuming A4(b)'), :147 (Theorem 2.1 'Assuming A4(e)'); page convention L05.html:70; proof uses at :99-100, :119, :154-155. Round-5 FAIL closed by the delta (lines 94, 110, 147 now carry the 'Assuming' phrase; L05 contains no other numbered result that uses an A4 part without it, re-checked by reading L05 :56-165 and :278-407).",
        None,
    ),
    "b-l06-assumption-scope": (
        "PASS",
        "L06.html:52 ('under Assumptions A3 and A4 of Lesson 5'), :130 (Proposition 2.3 statement 'Assuming A3 and A4(b), A4(c), A4(g) and A4(h)'), :159 (Theorem 2.5 'Assuming A3 and A4'), :176 (Corollary 2.6 'Assuming A3 and A4 of Lesson 5'), :417 (R2 'Assuming A3 and A4 hold for -B'). Round-5 FAIL closed.",
        None,
    ),
    "b-l06-canon-symmetry-attribution": (
        "PASS",
        "L06.html:306 now reads: Proposition 2.3 gives P(E)=P(B_t>a) and uses the symmetry at h_-=h_+, and the no-atom fact P(B_t=a)=0 is also needed; proof L06.html:169-170 (E={W_t>a} via Lemma 2.1(iii), P(W_t>a)=P(B_t>a) by Prop 2.3, P(B_t=a)=0 from the normal density). Round-5 FAIL closed.",
        None,
    ),
    "b-cards-c123-c133": (
        "FAIL",
        "SC1-c128 (cards.json, the block with front 'Misconception: reflecting after the first visit...'): back reads 'Continuity of the path, for {M_t>=a}={tau_a<=t} (Lemma 2.1), and the strong Markov property (A3 of Lesson 5) for the fixed-time law of the reflected value.' The current lesson text L06.html:324 says the fixed-time law 'needs the strong Markov property (Assumption A3 of Lesson 5) and the facts of Assumption A4 of Lesson 5'. The card omits A4, which the delta added to the lesson (diff of L06.html line 324). Cards c111-c122 and c123-c127, c129-c133 agree with the current text (read in full, ledgers/SC1/scripts/SC1-b-r6/out/cards_L04_L06.txt).",
        "Edit the SC1-c128 back so it names A4 as L06.html:324 does, for example 'and the facts of Assumption A4 of Lesson 5 (A4(b), A4(c), A4(g), A4(h) for Proposition 2.3)'; regenerate or re-verify the cards file in the same change.",
    ),
}

rows = []
for r in R5["rows"]:
    rid = r["id"]
    status, evidence, fix = r["status"], r["evidence"], None
    if rid in over:
        status, evidence, fix = over[rid]
    else:
        evidence = PREFIX + r["evidence"]
    row = {"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix or "see evidence"
    rows.append(row)

extra = [
    ("b-r6-delta-hunks", "2.8 delta: every changed hunk of L04-L06, cards.json and the cross-read pages",
     "course/modules/SC/SC1/L04.html (1 hunk, line 245), L05.html (16 lines: 52, 60, 72, 92, 108, 145, 286, 288 ...), L06.html (12 lines: 52, 102, 128, 130, 174, 176, 304, 306, 324), cards.json (c128 unchanged; L01/L02/L07/L08 hunks read), tests/labs/SC1/lab-SC1-L02-1.py (cross-ref only)",
     "PASS",
     "git diff -U2 7376a5e 4bd8cb9 -- course/modules/SC/SC1/L04.html L05.html L06.html read hunk by hunk in full; cards.json hunks listed with git diff -U1 (touch L01, L02, L07, L08 cards only; no L04-L06 card id changed). Each changed sentence re-checked against the proof or the numbers it cites (L04 misconception 2 at :245; L05 Lemma 1.3, Theorem 1.4, Theorem 2.1 statements; L05 :60 and :68 'defined in Section 3'; L06 :52, :130, :159, :176, :304, :306, :324). Tree outside SC1 changed only in other units' labs and the plans ruling 11 (read)."),
    ("b-r6-twin-page-equality", "2.5 labs: page code equals twin; expected block equals twin stdout",
     "course/modules/SC/SC1/L04.html, L05.html, L06.html; tests/labs/SC1/lab-SC1-L04-1.py, lab-SC1-L05-1.py, lab-SC1-L06-1.py", "PASS",
     "ledgers/SC1/scripts/SC1-b-r6/twin_match_r6.py output: 'L04 page code == twin: True', 'L04 expected == twin stdout (exact): True'; identical for L05 and L06 (exit lines in out/twin_match_r6 printed in the run). Twins run alone: out/twin_L04.out, twin_L05.out, twin_L06.out with empty stderr (0 bytes each) under 'python -I -W error' from a scratch cwd."),
    ("b-r6-run-labs", "2.5 labs (run_labs, page by page)", "course/modules/SC/SC1/L04.html, L05.html, L06.html", "PASS",
     "'.venv/bin/python tools/run_labs.py --unit SC1 --page L04' -> 'run_labs SC1: PASS (1/1)' exit 0; same for L05 and L06 (out/run_labs_L04.out, run_labs_L05.out, run_labs_L06.out). An earlier call with --page L04.html returned (0/0) because --page takes the stem; that call was rerun with the stem, so the (0/0) output is not a result."),
    ("b-r6-page-smoke", "2.9 page_smoke for the three pages (run alone, full run including the figure sweep)", "course/modules/SC/SC1/L04.html, L05.html, L06.html", "PASS",
     "'.venv/bin/python tools/page_smoke.py --unit SC1 --pages L04 L05 L06' -> 'page_smoke modules/SC/SC1/L0x.html: PASS' for each, 'page_smoke SC1: PASS', exit 0 (out/page_smoke_full.out); lab runtimes 0.0 s, 0.1 s and 1.3 s."),
    ("b-r6-check-gates", "2.9 check_pages, check_dag, check_projects for SC1", "tools/check_pages.py, check_dag.py, check_projects.py --unit SC1", "PASS",
     "out/check_pages.out 'check_pages SC1: PASS' exit 0; out/check_dag.out 'check_dag SC1: PASS' exit 0; out/check_projects.out 'check_projects SC1: PASS' exit 0."),
    ("b-r6-lint-typecheck-twins", "2.5 labs: ruff check, ruff format --check and mypy on the three twins", "tests/labs/SC1/lab-SC1-L04-1.py, lab-SC1-L05-1.py, lab-SC1-L06-1.py", "PASS",
     "out/ruff_twins.out: 'All checks passed!' and '3 files already formatted', exit 0; out/mypy_twins.out: 'Success: no issues found in 3 source files', exit 0 (mypy --no-incremental)."),
    ("b-r6-pytest-tooling", "2.5 tooling pytest (labs, run_labs, page checks)", "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py", "PASS",
     "'.venv/bin/python -m pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -q' output 406 dots over 6 lines and no F or E, exit 0 (out/pytest_tooling.out). (The earlier -k filtered run selected 11 tests and was discarded.)"),
    ("b-r6-verify-refs", "2.1 citations: offline integrity of the whole registry and the live re-verification of the unit's entries", "references/references.json (shreve2004stochastic); tools/verify_refs.py", "PASS",
     "out/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', exit 0; out/verify_refs_live.out: 'live re-verification of SC1: 1 of 560 entries, 0 problems', exit 0. Karatzas & Shreve (1991), named by the curriculum for SC1, is absent from references.json and present only in references/review_queue.json:1051 (not admissible), so the pages' statement that it is not cited is correct."),
    ("b-r6-recompute", "2.1 numbers in prose and quiz answers recomputed independently (stdlib, Fraction, DP over counts; trapezoid for quadrature)", "course/modules/SC/SC1/L04.html, L05.html, L06.html", "PASS",
     "ledgers/SC1/scripts/SC1-b-r6/recompute_r6.py -> out/recompute_r6.txt: e^1, e^0.25, e^4, e^8 = 2980.957987; L05 225 cases, worst gap 1.1e-16 (trapezoid 4000), tail mass 3.813e-29, integrals 1.000000000000, p_1(0,0)=0.3989422804, Phi(-1/sqrt2)=0.2397500611, 1/(2 sqrt pi)=0.2820947918; L06 triples 1014 equal 1014, pairs 78 equal 78, M_12>=3 1588 of 4096, 495 and 495, P(M_10>=2)=281/512, 2P(S_10>2)=11/32, P(S_10=2)=105/512 (= binom(10,6)/1024), erfc(1/sqrt2)=0.3173105079, half 0.158655253931. Every printed or quoted value matches to the printed precision."),
    ("b-r6-cards-full-scan", "2.10 cards: full scan of L04-L06 cards (fronts and backs), duplicate scan of all 194 cards", "course/modules/SC/SC1/cards.json", "PASS",
     "ledgers/SC1/scripts/SC1-b-r6/out/cards_L04_L06.txt lists all 83 cards with lesson L04, L05 or L06 (SC1-c061 to SC1-c204; c085 and c125 absent, not referenced). Duplicate scan on normalised fronts and backs over 194 cards: no duplicates (python script in the scratch dir)."),
    ("b-r6-notation", "2.3 notation: every math symbol on the three pages against notation/notation.json (T, R^*, R^e*, R_f, Q, gamma_3, gamma_4, Phi)", "course/modules/SC/SC1/L04.html, L05.html, L06.html; notation/notation.json", "PASS",
     "Symbol scan of every \\( \\) span: registered symbols appearing are \\Phi only (L05.html:348, 350, 498, the standard normal CDF, as registered); T, R^*, R^e*, R_f, Q, gamma_3, gamma_4 do not occur. Local symbols M_t, M_N, kappa, tau_a, rho, W_t, X_u, h_-, h_+ are each defined before use on the page where they occur (L06.html:56, 102, 107, 135-144)."),
    ("b-r6-process-words", "2.12 learner text: process words", "course/modules/SC/SC1/L04.html, L05.html, L06.html, cards.json", "PASS",
     "grep for round, verif*, builder, fixer, audit*, revis*, corrected, deviation, open item, plan, todo, draft, agent, ledger, conjecture, placeholder, tbd: only 'Verify' as a student instruction (L05.html:341, L06.html:391) and the lab convention 'Predicted before running'."),
    ("b-r6-hours", "2.2 hours arithmetic", "course/modules/SC/SC1/L04.html:2, L05.html:2, L06.html:2, index.html:29, :150", "PASS",
     "data-hours 9 on L01-L08; 8 x 9 = 72 = data-hours-lessons 72 on index.html:29; data-hours-project 28; 72 + 28 = 100 = module hours; index.html:150 states the sum 72."),
    ("b-r6-open-items-observation", "2.6 plan deviation recorded, not silent (outside the slice; observation only)", "plans/SC1-open-items.md:4 versus course/modules/SC/SC1/L06.html:119", "PASS",
     "L06.html:119 now reads 'On this page the path-level statement is not proved' and does not use the word 'conjecture'. plans/SC1-open-items.md:4 still says Definition 2.2 is 'labelled as a conjecture of that page'. The plans file is not in this slice and was not edited; the deviation itself is recorded and still open."),
]
for rid, check, location, status, evidence in extra:
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence})

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
verdict = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 else "FAIL"

frag = {
    "unit": "SC1",
    "slice": "b",
    "round": 6,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-b, round 6 (did not build SC1)",
    "pin": "4bd8cb9",
    "base": "7376a5e (round-5 pin; delta 7376a5e..4bd8cb9 read for every SC1-b file)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE6-SC1-b",
    "scratch": "ledgers/SC1/scripts/SC1-b-r6",
    "verified_at": "2026-11-04T00:00:00+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Mutants: none. Slice b is lessons L04-L06 and their lab twins; the architect ruling (plans/SC1-build-plan.md:173, item 11) says lab twins are demonstrations, not mutation-ttested, and this slice has no project grader. "
        "Round 5 FAILs (b-assumed-facts-statement, b-l06-assumption-scope, b-l06-canon-symmetry-attribution) are closed at 4bd8cb9 and re-verified. "
        "Because L04.html, L05.html, L06.html and cards.json all changed since 7376a5e, no PASS row was carried by byte-identity; every row was re-derived this round from a full read of the three pages and the cards. "
        "Lab twins are byte-identical to round 5 (sha256 79a56370..., 744046b7..., 8d01822e...), so their rows are re-run, not carried. "
        "Observations, not FAIL: (1) plans/SC1-open-items.md:4 still calls the L06 path-level claim 'a conjecture'; L06.html:119 no longer does (outside slice, not edited). "
        "(2) The intermediate value theorem is used unnumbered in L06 Lemma 2.1 and its problem P2 (elementary calculus; recorded, as in round 5). "
        "(3) Lemma 2.1 of L06 and Corollary 2.6 use the standard Brownian motion B of Section 2 without restating it in their assumption lists; B is fixed at the head of Section 2 (L06.html:102), so no hypothesis is missing. "
        "Not checked: the full repository gate (ruff and mypy over the whole repo, the whole pytest suite, render_curriculum, build_site --check, fetch_data --check, check_pages/check_dag/check_projects --all, verify_refs over the whole registry live); the delta touches no dependency, build configuration, CI or tooling, and the other units' pages and labs (for example tests/labs/SC1/lab-SC1-L02-1.py, which changed in the delta but is outside this slice) were not run. "
        "run_graders and mutate_graders: not applicable (no project grader in slice b). "
        "Live Shreve (2004) and Karatzas & Shreve (1991) were not read; no passage is attributed to either. Crossref/landing re-checks are not applicable to the book entry (openlibrary)."
    ),
    "summary": (
        f"SC1-b round 6: verdict {verdict}. Rows: {counts['FAIL']} FAIL, {counts['PASS']} PASS, {counts['UNVERIFIABLE']} UNVERIFIABLE. "
        "FAIL: b-cards-c123-c133 (card SC1-c128 back omits Assumption A4 that L06.html:324 now names). "
        "Round-5 FAILs b-assumed-facts-statement, b-l06-assumption-scope and b-l06-canon-symmetry-attribution are closed and re-verified. "
        "All command rows (check_pages, check_dag, check_projects, run_labs per page, twins under python -I -W error, page_smoke, ruff, mypy, tooling pytest, verify_refs offline and live) passed."
    ),
}
out = ROOT / "ledgers/SC1/SC1-b.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, counts, verdict, len(rows))
