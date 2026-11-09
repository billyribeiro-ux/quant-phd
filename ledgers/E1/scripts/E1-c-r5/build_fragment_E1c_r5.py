"""Verifier round 5, unit E1, slice c: writes ledgers/E1/E1-c.json from the round-5 evidence (no row is edited by a tool)."""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
P = "Carried from round 4 (course/modules/E/E1/L08.html and L09.html and the L08-L09 twins and cards byte-identical since the previous pin edbb7aa8; git diff --quiet and card_delta_r5.out): "
PL = "Carried from round 4 (course/modules/E/E1/L08.html, L09.html and the cards of L08 and L09 byte-identical since the previous pin edbb7aa8): "
S = "ledgers/E1/scripts/E1-c-r5/"
rows = []


def row(rid, check, location, evidence, status="PASS", fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# Commands, re-run on the pin dde0486b
row("E1-c-cmd-check-pages", "tools/check_pages.py --unit E1", "course/modules/E/E1/L07.html; L08.html; L09.html",
    f"Re-run on dde0486b: 'check_pages E1: PASS', exit 0 ({S}check_pages_E1.out). Unit-wide, so the changed L02, L04, L06, index and project pages are also covered.")
row("E1-c-cmd-check-dag", "tools/check_dag.py --unit E1", "course/modules/E/E1/L07.html:38-39; L08.html:38-39; L09.html:38-39",
    f"Re-run on dde0486b: 'check_dag E1: PASS', exit 0 ({S}check_dag_E1.out).")
row("E1-c-cmd-check-projects", "tools/check_projects.py --unit E1", "course/modules/E/E1/project.html",
    f"Re-run on dde0486b: 'check_projects E1: PASS', exit 0 ({S}check_projects_E1.out). project.html changed in the delta (lede, Rungs 1-2, Step 5 comment, memo and exemplar sentences); the project is outside slice c.")
row("E1-c-cmd-run-labs", "tools/run_labs.py --unit E1 --page L07 / L08 / L09, and --unit E1", "tests/labs/E1/lab-E1-L07-1.py; lab-E1-L08-1.py; lab-E1-L09-1.py",
    f"Re-run on dde0486b: L07 'run_labs E1: PASS (1/1)', L08 (1/1), L09 (1/1); unit-wide 'run_labs E1: PASS (12/12)', exit 0 ({S}run_labs_L07.out, run_labs_L08.out, run_labs_L09.out, run_labs_E1.out).")
row("E1-c-cmd-twin-isolated", "each twin alone under python -I -W error, empty environment, fresh temp dir", "tests/labs/E1/lab-E1-L07-1.py; lab-E1-L08-1.py; lab-E1-L09-1.py",
    f"Re-run with {S}twin_isolation_r5.sh ({S}twin_isolation_r5.out): L07 exit=0 stderr_bytes=0 stdout_lines=12; L08 exit=0 stderr_bytes=0 stdout_lines=21; L09 exit=0 stderr_bytes=0 stdout_lines=14.")
row("E1-c-lab-code-equals-twin", "page lab code equals twin (html-unescaped)", "course/modules/E/E1/L07.html:140-296; L08.html:149-304; L09.html:142-262",
    f"Re-run with {S}twin_page_r5.py ({S}twin_page_r5.out): L07, L08, L09 code_equals_twin=True; ALL_OK. The three twins are byte-identical to edbb7aa8 (git diff --quiet).")
row("E1-c-lab-expected-equals-output", "expected block equals twin stdout", "course/modules/E/E1/L07.html:297-308; L08.html:305-325; L09.html:263-276",
    f"Re-run with {S}twin_page_r5.py: expected_equals_output=True for L07 (12 lines), L08 (21 lines), L09 (14 lines) ({S}twin_page_r5.out).")
row("E1-c-cmd-page-smoke", "tools/page_smoke.py --unit E1 --pages L07 L08 L09 (run alone)", "course/modules/E/E1/L07.html; L08.html; L09.html",
    f"Re-run on dde0486b: 'page_smoke E1: PASS', exit 0 ({S}page_smoke_L07-L09.out).")
row("E1-c-cmd-ruff", "ruff check and ruff format --check on the slice twins", "tests/labs/E1/lab-E1-L07-1.py; lab-E1-L08-1.py; lab-E1-L09-1.py",
    f"Re-run: 'All checks passed!' exit 0 ({S}ruff_check.out); '3 files already formatted' exit 0 ({S}ruff_format.out).")
row("E1-c-cmd-mypy", "mypy --no-incremental on the three twins", "tests/labs/E1/lab-E1-L07-1.py; lab-E1-L08-1.py; lab-E1-L09-1.py",
    f"Re-run: 'Success: no issues found in 3 source files', exit 0 ({S}mypy.out).")
row("E1-c-cmd-pytest", "pytest tests/test_labs.py -k E1; pytest tests/test_page_checks.py", "tests/test_labs.py; tests/test_page_checks.py",
    f"Re-run: test_labs -k E1 13 tests passed (dot count), exit 0 ({S}pytest_labs_E1.out); test_page_checks 41 tests passed, exit 0 ({S}pytest_page_checks.out).")
row("E1-c-cmd-verify-refs", "tools/verify_refs.py --offline", "references/references.json",
    f"Re-run: 'offline integrity: 560 entries, 0 problems', exit 0 ({S}verify_refs_offline.out). No reference file changed since the previous pin.")

# Math, L07 re-verified this round (changed page; whole file read)
row("E1-c-math-L07-closed-forms", "closed forms CS, PS, W, DWL (Theorem 1.2, Lemma 1.4, Theorem 1.5)", "course/modules/E/E1/L07.html:56-104",
    f"Re-derived by hand (proofs at :75, :94, :104 checked line by line) and by {S}recompute_L07_r5.py ({S}recompute_L07_r5.out, ALL_OK, 64 checks): W closed form equals the integral of P - c; CS + PS = W; DWL = (d - Q)^2/(2b) for monopoly, Cournot and Bertrand in the three cases (a,b,c) = (120,1,20), (90,3,10), (200,4,5).")
row("E1-c-math-L07-corollary-prop23", "Corollary 2.1 values; Proposition 2.3 orderings and shares", "course/modules/E/E1/L07.html:110-135",
    f"Corollary 2.1 values recomputed exactly (monopoly CS d^2/(8b), PS d^2/(4b), W 3d^2/(8b), DWL d^2/(8b); Cournot CS 2d^2/(9b), PS 2d^2/(9b), W 4d^2/(9b), DWL d^2/(18b)). Proposition 2.3 proof arithmetic checked: DWL_M - DWL_C = 5d^2/(72b); CS 1/8, 2/9, 1/2; PS 1/4, 2/9, 0; W 3/8, 4/9, 1/2 (times d^2/b); shares 1/4 and 1/9; accounting check 7/72 and 2/72 ({S}recompute_L07_r5.out).")
row("E1-c-math-L07-example-2-2", "Example 2.2 reference case (120,1,20)", "course/modules/E/E1/L07.html:121-123",
    f"Recomputed: monopoly 1250, 2500, 3750, 1250; Cournot 20000/9, 20000/9, 40000/9, 5000/9 = 555.56 -> 556 half up, rounded totals 2222, 2222, 4444; Bertrand 5000, 0, 5000, 0 ({S}recompute_L07_r5.out, half-up checks PASS).")
row("E1-c-math-L07-R-problems", "research and problem solutions R1-R3 and E1-E3 (L07)", "course/modules/E/E1/L07.html:421-441 (R1 solution at :425)",
    f"Round-4 FAIL (R1 gave one of two roots without saying so) is fixed: :425 now gives Q = d(1 - sqrt2/4) ~ 0.64645 d and the other root d(1 + sqrt2/4), says it also halves the loss (Theorem 1.5), and says it lies in [0, a] when d <= 2 sqrt2 bc since a = d + bc. Checked: (sqrt2/4)^2 = 1/8; 0.64645 in (1/2, 2/3); Cournot/monopoly loss 4/9 < 1/2; the boundary equivalence checked at four values of bc/d ({S}recompute_L07_r5.out). R2: profit (f - c) max(0, a - bf) <= 0 below the cap, zero only at f = c; R3: difference (7 lambda - 2)/72 checked at lambda = 0, 2/7, 1, 3; P3 ratio 9/4; M1, M2, M3, P1, P2, E1, E2, E3 solutions recomputed (M1 150, 450, 600; M2 200/3 = 3600/54; M3 4750).")
for rid, label in [("E1-c-math-L08-grid", "grid-efficiency counts and the diagonal claims"),
                   ("E1-c-math-L08-proofs", "Lemma 2.1, Proposition 2.2, Proposition 2.3, Theorem 2.4, Remark 2.6"),
                   ("E1-c-math-L08-improvements", "Lab 1 Part C improvements and the amount-set claim"),
                   ("E1-c-math-L08-problems", "problem set M1-M3, P1-P3, E1-E3, R1-R3 (L08)")]:
    loc = {"E1-c-math-L08-grid": "course/modules/E/E1/L08.html:144, 305-325, 326",
           "E1-c-math-L08-proofs": "course/modules/E/E1/L08.html:79-140",
           "E1-c-math-L08-improvements": "course/modules/E/E1/L08.html:149-304 (code), 311-320 (output), 326",
           "E1-c-math-L08-problems": "course/modules/E/E1/L08.html:363-459"}[rid]
    row(rid, label, loc, P + f"{label} at round 4 ({loc}).")
row("E1-c-math-L09-closed-forms", "Propositions 1.3, 1.4, 1.6 and Corollary 1.5", "course/modules/E/E1/L09.html:56-116", P + "Propositions 1.3, 1.4, 1.6 and Corollary 1.5 at round 4 (L09.html:56-116).")
row("E1-c-math-L09-public-good", "Proposition 2.2 and the public-good numbers", "course/modules/E/E1/L09.html:127-137; 355-357; 405-408", P + "Proposition 2.2 and public-good numbers at round 4 (L09.html:127-137, 355-357, 405-408, 270-276).")
row("E1-c-math-L09-numbers", "lab numbers and worked numbers (L09)", "course/modules/E/E1/L09.html:263-276; 295-304; 316-325; 366-369; 375-401", P + "lab and worked numbers at round 4 (L09.html:141, 263-276, 295-304, 316-325, 366-369, 375-401).")

# Prose numbers and grades
row("E1-c-prose-numbers-L07", "every number in prose, L07 (classes a, b, c)", "course/modules/E/E1/L07.html:52-340",
    "Whole L07.html read this round. Every prose number recomputed: Example 2.2 values, Corollary 2.1, Proposition 2.3 fractions and shares, the R1 numbers 0.64645 and 0.66667, the 4/9 ratio, 555.56 -> 556, 4444, 2222, the interpretation line 309 (4444, 556), the misconception figures 1250 and 2500 (:327) and 555.56 (:491). Checked by recompute_L07_r5.py.")
row("E1-c-prose-numbers-L08", "every number in prose, L08 (classes a, b, c)", "course/modules/E/E1/L08.html:52-476", P + "every number in prose, L08, at round 4 (L08.html:52-476).")
row("E1-c-prose-numbers-L09", "every number in prose, L09 (classes a, b, c)", "course/modules/E/E1/L09.html:52-511", P + "every number in prose, L09, at round 4 (L09.html:52-511).")
row("E1-c-grades-L07", "grades of claims, L07 (BLUEPRINT 3)", "course/modules/E/E1/L07.html:52-455",
    "L07.html re-read this round: claims are Theorem 1.2, Lemma 1.4, Theorem 1.5, Corollary 2.1, Proposition 2.3 (each data-grade T with a proof on the page), and the key-results table rows (T, each naming its source). Examples and definitions carry no grade. No claim is ungraded.")
row("E1-c-grades-L08", "grades of claims, L08 (BLUEPRINT 3)", "course/modules/E/E1/L08.html:468-472", P + "grades of claims, L08, at round 4 (L08.html:468-472).")
row("E1-c-grades-L09", "grades of claims, L09 (BLUEPRINT 3)", "course/modules/E/E1/L09.html:419-423", P + "grades of claims, L09, at round 4 (L09.html:419-423).")
row("E1-c-problems-L07", "problem set L07 (L07.html:346-441)", "course/modules/E/E1/L07.html:346-441",
    "L07.html:346-441 re-read this round; M1-M3, P1-P3, E1-E3, R1-R3 solutions recomputed (see E1-c-math-L07-R-problems). Each problem has a full worked solution.")
row("E1-c-problems-L08", "problem set L08 (L08.html:363-459)", "course/modules/E/E1/L08.html:363-459", P + "problem set L08 at round 4 (L08.html:363-459).")
row("E1-c-problems-L09", "problem set L09 (L09.html:314-411)", "course/modules/E/E1/L09.html:314-411", P + "problem set L09 at round 4 (L09.html:314-411).")
row("E1-c-quiz-L07", "retrieval quiz L07 (L07.html:465-530)", "course/modules/E/E1/L07.html:465-530",
    "L07.html:465-530 re-read this round; all nine items checked against their explain blocks: 1250; 1250; d; 5000/9 = 555.5556 (tolerance 0.001 covers 555.555556); the Bertrand volume; 0.25; Q = a; 4750 (120*50 - 50^2/2).")
row("E1-c-quiz-L08", "retrieval quiz L08 (L08.html:482-553; explanation at :517)", "course/modules/E/E1/L08.html:482-553; explanation at :517", P + "retrieval quiz L08 at round 4 (L08.html:482-553, explanation :517).")
row("E1-c-quiz-L09", "retrieval quiz L09 (L09.html:433-499)", "course/modules/E/E1/L09.html:433-499", P + "retrieval quiz L09 at round 4 (L09.html:433-499).")
row("E1-c-misconceptions", "misconceptions L07-L09 (3 each)", "course/modules/E/E1/L07.html:325-337; L08.html:342-353; L09.html:293-304",
    "L07.html:325-337 re-read this round: three misconceptions, each checked (profit is not the loss: 1250 vs 2500; Cournot loss d^2/(18b) > 0; competitive outcome maximises total, not consumer surplus). L08 and L09 misconception blocks are byte-identical since edbb7aa8 and carried from round 4.")

# Scope words, process words, banned strings, notation, DAG, cross refs
row("E1-c-scope-words", "scope words (only, all, every, always, any, same, drives, exactly) in slice prose", "course/modules/E/E1/L07.html; L08.html; L09.html",
    "L07 re-read this round: each scope word is tied to a computation or a stated hypothesis (for example 'the midpoint rule is exact for every n' with the linear-integrand reason at :148; 'only (d - Q)^2 enters the loss' with Theorem 1.5 cited at :425; 'the lab checks these inputs only' at :159). L08 and L09 carried from round 4 (byte-identical since edbb7aa8).")
row("E1-c-define-before-use-L07", "define before use, L07 (concept names and symbols)", "course/modules/E/E1/L07.html:52,56,60,62,65,78",
    "Lines 52-78 are byte-identical to edbb7aa8 (git diff hunk only at 422-428). Checked: Definition 1.1 at :60 defines CS, PS and W before use at :65 and :69; the reference at :52 points forward to Definition 1.3 in Section 1; deadweight loss is introduced in the meta row at :39 and defined at :82.")
row("E1-c-define-before-use-L08", "define before use, L08", "course/modules/E/E1/L08.html:52-80 (heading at :77)", P + "define before use, L08, at round 4 (L08.html:52-80).")
row("E1-c-define-before-use-L09-L82", "define before use, L09 (and L08 links to L09)", "course/modules/E/E1/L09.html:52-141; 68; 82; 99-105; 122", P + "define before use, L09, at round 4 (L09.html:52-141, 68, 82, 99-105, 122).")
row("E1-c-dag", "check_dag and unlinked concept uses", "course/modules/E/E1/L07.html:38-39,60,82; L08.html:38-39,72,79; L09.html:38-39,60,122",
    f"Re-run check_dag E1: PASS ({S}check_dag_E1.out). L07 cross-links re-checked: L05.html#def-monopoly, L06.html anchors, concepts.html#definite-integral (L07.html:38-39). No concept link changed in the delta.")
row("E1-c-cross-refs", "cross references to other lessons and exercises", "course/modules/E/E1/L07.html:56,75,111; L08.html:79,139; L09.html:284,300-304",
    "L07 cross-references re-checked this round: Lesson 6 Definition 1.1 hypotheses (L06.html:59-61, b > 0, c > 0, a > bc), Lemma 1.3 (L06.html:69-70), Proposition 1.4, Theorem 2.5, Theorem 3.3, Example 1.5 and Example 2.7 (L06.html:91, 141). The L06 items are unchanged in meaning by the delta. L08 and L09 cross-references carried from round 4 (L01 link at L08.html:38, 79; L08 link in L09.html:38, 284).")
row("E1-c-notation", "notation registry (notation/notation.json) against slice symbols", "notation/notation.json; course/modules/E/E1/L07.html; L08.html; L09.html",
    f"notation/notation.json is byte-identical since edbb7aa8 and has 8 symbol entries (T; Phi and Phi^-1; gamma_3; gamma_4; R^ast; R^(e ast); R_f; the measure Q), from modules S1, M4 and AP1. Grep on the three pages: 0 hits for Phi, gamma_3, gamma_4, R_f, mathbb{{Q}}, and no LaTeX \\ast; the one 'ast' in L07 is 'past' (:425). Symbols in the R1 change (Q, d, b, a, sqrt2) keep the meanings used on the page.")
row("E1-c-process-words", "process words in learner text and code comments", "course/modules/E/E1/L07.html; L08.html; L09.html; tests/labs/E1/lab-E1-L07-1.py; lab-E1-L08-1.py; lab-E1-L09-1.py",
    "Grep (case-insensitive) for verif, round, ledger, builder, draft, fixer, slice, audit, sweep, finding, erratum, correction on the three pages: only 'agent' in the economic sense (L09.html:60, 'one agent's activity') and an instruction 'Verify that it strictly raises both utilities' (L08.html:415). No process words.")
row("E1-c-banned-strings", "BUILDER_RULES 1.3-1.4 banned strings", "course/modules/E/E1/L07.html; L08.html; L09.html",
    "Grep for TODO, TBD, lorem, for brevity, beyond the scope, omitted, roughly, about N%, historically, you can add more, left as an exercise, it can be shown, clearly, obvious, well known, important to note, studies show, experts agree: 0 matches in all three pages (BUILDER_RULES.md:45-52, 116).")
row("E1-c-attribution", "attributions and citations", "course/modules/E/E1/L07.html:535; L08.html:555; L09.html:503",
    "L07.html:535 re-read this round: 'This lesson cites no registry key'; its results are proved on the page or computed by Lab 1. No bibliographic data or theorem number from outside the unit is attributed. L08 and L09 carried from round 4.")
row("E1-c-hours-titles", "hours and hub titles", "course/modules/E/E1/L07.html:2; L08.html:2; L09.html:2; course/modules/E/E1/index.html:42, 138-148",
    "Changed hub line index.html:42 re-verified: '90 h lessons · 30 h project (25% of the 120 h)'. Arithmetic: data-hours of L01-L09 sum to 90 (run), project 30 h (project.html:34), 30/120 = 25%, hub split widths 75%/25%, index.html:138 'Nine lessons of ten study hours each, 90 hours'. Titles: L07 'Surplus and Deadweight Loss' (L07.html:36, index card), L08 'Pareto Efficiency' (L08.html:36), L09 'Externalities and Public Goods' (L09.html:36) match the hub cards.")
row("E1-c-structure", "template order and minimum counts (BUILDER_RULES 4.2)", "course/modules/E/E1/L07.html; L08.html; L09.html",
    "L07 section order re-read this round: why-it-matters, sections 1-8, problem set (M1-M3, P1-P3, E1-E3, R1-R3), quiz (9 items), references, complete button, nav. The delta changes one sentence inside an existing solution element (L07.html:425); element counts are unchanged. L08 and L09 carried from round 4.")
row("E1-c-figures-data", "figures and data (rule 2.8)", "course/modules/E/E1/L07.html; L08.html; L09.html",
    "No figure or data file in the slice: grep -i for chart, figures-, data-files, <svg, <img returns 0 matches in each of L07.html, L08.html, L09.html. Labs use exact arithmetic and simulated or stated illustrative inputs (L07.html:142-145). L08 and L09 carried from round 4.")

# Cards
row("E1-c-cards-coverage", "cards cover every definition, theorem, key formula, key result and misconception of L07-L09", "course/modules/E/E1/cards.json",
    "L07 coverage re-checked: Definition 1.1 (E1-c092), Definition 1.3 (E1-c094), Theorem 1.2 (c093), Lemma 1.4 (c095), Theorem 1.5 (c096), Corollary 2.1 (c097-c099), Example 2.2 (c100), Proposition 2.3 (c101), three misconceptions (c102-c104), Lab 1 (c105). L08 and L09 coverage carried from round 4 (cards c106-c118, c119-c132, c138, c149-c151, c157, c158 cover their definitions, results and misconceptions).")
row("E1-c-cards-sample", "card sample and full read of the 47 slice cards", "course/modules/E/E1/cards.json (E1-c092..E1-c158)",
    f"Every one of the 47 slice cards (lessons L07 14, L08 17, L09 16) was read this round ({S}cards_slice_dump.txt) and compared with the lesson text.")
row("E1-c-cards-full-scan", "full scan for duplicate cards", "course/modules/E/E1/cards.json (156 cards)",
    f"Re-run {S}dup_scan_r5.py ({S}dup_scan_r5.out): 156 cards, 0 exact duplicate fronts or backs. Near-duplicates reviewed and not duplicates: c097/c098/c099 (same template, different values); c088/c159/c160 (one reference-case question split into monopoly, Cournot and Bertrand, with different answers); c131/c150 (different questions on one lab instance); c095/c104, c110/c111 (different claims).")
row("E1-c-cards-agree-L07", "cards E1-c092..E1-c105 agree with lesson text, carry hypotheses, numbers in lesson", "course/modules/E/E1/cards.json: E1-c101 (hypotheses), E1-c092..E1-c105",
    f"Round-4 FAIL (E1-c101 hypothesis wording) is fixed: c101 now reads 'Under the hypotheses of Definition 1.1 of Lesson 6 (b > 0, c > 0, a > bc)', matching L06.html:59-61 and L07.html:127. Every L07 card re-checked against L07.html: c092-c096, c097-c099, c100 (Example 2.2), c101 (Proposition 2.3 orderings and shares), c102-c104 (misconceptions), c105 (Lab 1 Part A); hypotheses carried where a result needs them (c093, c095-c099, c101, c103, c104); numbers present (E1-c-card-numbers-r2).")
row("E1-c-cards-agree-L08", "cards E1-c106..E1-c118, c138, c149, c157, c158 agree with lesson text", "course/modules/E/E1/cards.json",
    "Carried from round 4 (course/modules/E/E1/L08.html byte-identical since edbb7aa8, and these 17 card objects byte-identical in card_delta_r5.out, which shows 46 of 47 slice cards identical and only E1-c101 changed): round-4 check of cards c106-c118, c138, c149, c157, c158 against L08.html (c114 fixed at round 4).")
row("E1-c-cards-agree-L09", "cards E1-c119..E1-c132, c150, c151 agree with lesson text", "course/modules/E/E1/cards.json",
    "Carried from round 4 (course/modules/E/E1/L09.html byte-identical since edbb7aa8, and these card objects byte-identical in card_delta_r5.out): round-4 check of cards c119-c132, c150, c151 against L09.html (c128 fixed at round 4).")
row("E1-c-cards-ids-grades", "ids and grade fields", "course/modules/E/E1/cards.json (E1-c092..c158)",
    "Re-checked this round: 156 unique ids (dup_scan_r5.out), no card missing front or back, grade present on every claim card (T or C with basis), absent on definition and misconception cards, as in the round-4 convention.")
row("E1-c-card-grade-c118", "card E1-c118 grade and basis", "course/modules/E/E1/cards.json (E1-c118)",
    "Carried from round 4 (card object byte-identical since edbb7aa8, per card_delta_r5.out; L08.html byte-identical): grade C with basis 'Lab 1, Part C (one instance, exact arithmetic)' names the lab.")
row("E1-c-card-duplicate-c128-c131", "duplicate check for E1-c128 and E1-c131", "course/modules/E/E1/cards.json (E1-c128, E1-c131)",
    f"Re-run {S}dup_scan_r5.py: c128 (sign of the externality distortion) and c131 (untaxed 80, efficient 68, gap 12) are distinct claims; no exact or near duplicate between them (Jaccard below 0.45 in {S}dup_scan_r5.out).")
row("E1-c-prose-number-L09-E2-2500", "L09 E2 sub-computation 2500 at 4 units", "course/modules/E/E1/L09.html:375", P + "L09.html:375 at round 4.")
row("E1-c-dwl-benchmark-L09", "deadweight-loss benchmark usage between L07 and L09", "course/modules/E/E1/L09.html:38, 99-105; L07.html:81-84; cards.json E1-c123",
    "L07.html:81-84 (Definition 1.3) byte-identical since edbb7aa8 (the only L07 hunk is at 422-428). E1-c123 byte-identical (card_delta_r5.out). L09.html:38, 99-105 carried from round 4 (byte-identical since edbb7aa8).")
row("E1-c-card-c149-self-contained", "card E1-c149 is self-contained", "course/modules/E/E1/cards.json (E1-c149)", P + "card E1-c149 object byte-identical (card_delta_r5.out); self-contained at round 4.")
row("E1-c-recompute-exact-r2", "exact recomputation of every number on L07-L09 (verifier-written)", "ledgers/E1/scripts/E1-c-r5/recompute_L07_r5.py",
    f"L07 numbers recomputed this round in exact arithmetic ({S}recompute_L07_r5.py, ALL_OK, 64 checks). L08 and L09 numbers carried from round 4 (recompute_r4.py in the pin; L08.html and L09.html byte-identical since edbb7aa8).")
row("E1-c-lab-statements-r2", "lab hypotheses and interpretations agree with code and output", "course/modules/E/E1/L07.html:139, 309; L08.html:148, 326; L09.html:141, 277",
    "L07.html:139 (stated hypotheses) and :309 (interpretation) re-read against the twin and expected block this round: the midpoint claim, the cents rounding, the three checks and the 1/4 and 1/9 shares agree with code and output. L08 and L09 carried from round 4.")
row("E1-c-card-numbers-r2", "every number in a slice card back appears in its lesson", "course/modules/E/E1/cards.json (47 slice cards)",
    f"Re-run {S}card_numbers_r5.py ({S}card_numbers_r5.out): 47 slice cards checked, 0 with a number absent from their lesson text (tags stripped, HTML unescaped).")
row("E1-c-card-duplicates-r2", "duplicate cards over the whole deck", "course/modules/E/E1/cards.json (156 cards)",
    f"Re-run {S}dup_scan_r5.py: 0 exact duplicates across 156 cards ({S}dup_scan_r5.out).")
row("E1-c-card-new-c157-c158", "new cards E1-c157 and E1-c158 (L08)", "course/modules/E/E1/cards.json (E1-c157, E1-c158)", P + "E1-c157 and E1-c158 card objects byte-identical (card_delta_r5.out); round-4 check against L08.html.")
row("E1-c-delta-r4", "delta since round-3 pin 8196077d, slice files (historical)", "course/modules/E/E1/L07.html:139; L08.html:144, 517; L09.html:295; cards.json (c104, c114, c128, c157, c158)",
    "Historical row from round 4, kept for id continuity. The cards it names (c104, c114, c128, c157, c158) and L08.html, L09.html are unchanged in the delta to dde0486b (card_delta_r5.out; git diff --quiet). The delta of this round is E1-c-delta-r5.")
row("E1-c-delta-r5", "delta edbb7aa8..dde0486b for slice c subjects", "course/modules/E/E1/L07.html:422-428; cards.json; index.html:42",
    f"git diff --stat edbb7aa8 dde0486b: L07.html has one hunk (422-428, the R1 solution, re-verified above); cards.json changed for 25 cards plus 2 added (c159, c160; L06); slice cards changed: only E1-c101 (46 of 47 identical, {S}card_delta_r5.out); index.html:42 eyebrow (re-verified in E1-c-hours-titles). L08.html, L09.html, the L08-L09 twins, notation/, references/, tools/ are byte-identical (git diff --quiet exit 0). Round-4 FAIL rows E1-c-math-L07-R-problems and E1-c-cards-agree-L07 are re-verified PASS; no round-4 PASS row was carried where its subject changed.")

frag = {
    "unit": "E1",
    "slice": "c",
    "round": 5,
    "verifier": "independent Haiku verifier, round 5 (delta verification), slice c (L07-L09, lab twins and cards); did not build E1",
    "pin": "dde0486beeb0312e4ac1cc03aaa02e56644adb24",
    "base": "edbb7aa8de20e6d2f3035c463a79a318c22623c4 (round-4 pin; delta git diff edbb7aa8 dde0486b)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS5-E1-c (detached at dde0486b; .venv symlink to /Users/billyribeiro/dev/quant-phd/.venv)",
    "scratch": "ledgers/E1/scripts/E1-c-r5/",
    "verified_at": "2026-11-09T09:57:12+00:00",
    "verdict": "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Lab twins are demonstrations; mutation testing applies to project graders only (verifier rules, ruling 9 scope), so no mutants are recorded for slice c. tools/mutate_graders.py and run_graders were not run: slice c has no grader.",
        "Pre-existing files in ledgers/E1/scripts/E1-c-r5/ (recompute_l07_l09.py and recompute_l08_partc_l09.py, tracked at the pin in commit 44f1eb6a) were not written by this round and were not used as evidence; this round's scripts carry the _r5 suffix.",
        "Considered and not raised: L07 R2 'Not trading also earns zero' is outside the model (the cap f <= c leaves the trade demand unchanged); the solution already says the analysis does not cover it.",
        "Considered and not raised: L07 R1 'the root below d' is the asked root; the other root exceeds d, so it is not the one between d/2 and 2d/3.",
        "Could not check: rendered pages at 360 px in light and dark mode beyond page_smoke's geometry checks; a live Pyodide run in a browser (page_smoke only); whole-repository ruff, mypy and pytest (targeted runs only, per the change table); run_graders and mutate_graders (no grader in slice c); the live Crossref run (no citation in slice c); the L08 and L09 numbers were carried from round 4 rather than re-derived, because their subject files are byte-identical to the round-4 pin.",
    ],
    "summary": "",
}
n_pass = sum(1 for r in rows if r["status"] == "PASS")
frag["summary"] = (f"Slice c (L07-L09, twins, cards), round 5 at dde0486b: {frag['verdict']}. {len(rows)} rows: {n_pass} PASS, "
                   f"{len(rows) - n_pass} non-PASS. Re-run this round: all unit commands, twins, card and dup scans. "
                   "Round-4 FAIL rows E1-c-math-L07-R-problems and E1-c-cards-agree-L07 now PASS. L08 and L09 rows carried from round 4 (byte-identical subjects).")
out = root / "ledgers/E1/E1-c.json"
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "verdict", frag["verdict"])
