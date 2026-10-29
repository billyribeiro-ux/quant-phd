import json, sys
sys.path.insert(0, '/Users/billyribeiro/.fanout/wt/verifyB12-M4-a/tools')
import ledger

S = 'ledgers/M4/scripts/M4-a-r12/'
C = 'Carried from round 11 (course/modules/M/M4/index.html and tools/notation/references byte-identical since the previous pin f42f4329; no hunk in the cited lines):'
rows = []
def row(i, check, loc, status, ev, fix=""):
    r = {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

row("M4a-R01", "Page, DAG and project structure gates for M4", "tools/check_pages.py --unit M4; tools/check_dag.py --unit M4; tools/check_projects.py --unit M4", "PASS",
    "Re-run at ff38842: 'check_pages M4: PASS' (exit 0), 'check_dag M4: PASS' (exit 0), 'check_projects M4: PASS' (exit 0). Logs: " + S + "check_pages.log, check_dag.log, check_projects.log.")
row("M4a-R02", "Lab runs for L01-L04 (run_labs) and page smoke", "tests/labs/M4/lab-M4-L01..L04-1.py; course/modules/M/M4/L01..L04.html; course/modules/M/M4/index.html", "PASS",
    "Re-run: 'python tools/run_labs.py --unit M4' -> 'run_labs M4: PASS (13/13)' (run_labs_unit.log, exit 0). tools/page_smoke.py --unit M4 --pages index L01 L02 L03 L04 -> 'page_smoke M4: PASS' (exit 0). Note: '--page' with a path returned '(0/0)' so the unit-wide run was used as the authoritative count.")
row("M4a-R03", "Twins alone under python -I -W error; page code equals twin; expected block equals output", "tests/labs/M4/lab-M4-L01-1.py .. lab-M4-L04-1.py vs course/modules/M/M4/L01..L04.html", "PASS",
    "Each twin copied to an empty scratch dir and run 'python3 -I -W error' (python3, not the venv interpreter): L01, L02, L03, L04 each exit 0, stderr 0 bytes (twins_run.log). Page code vs twin and expected vs output enforced by run_labs (13/13, byte-identical and expected-equal). mypy --no-incremental on the four twins: 'Success: no issues found in 4 source files' (mypy_twins.log).")
row("M4a-R04", "Hub index.html: hours split and lesson hours arithmetic", "course/modules/M/M4/index.html:29, :40, :42", "PASS",
    C + " index.html:29 data-hours-lessons=90, data-hours-project=30; :42 '90 h lessons · 30 h project (25% of 120 h)'; 10 x 9 h = 90; 90 + 30 = 120; 30/120 = 25%.")
row("M4a-R05", "Hub index.html prose claims for L01-L10", "course/modules/M/M4/index.html:68-141", "PASS", C + " no hunk in index.html; not re-read line by line this round.")
row("M4a-R06", "Hub index.html numeric and scope claims", "course/modules/M/M4/index.html:79, :93, :135, :138-140", "PASS", C)
row("M4a-R07", "Hub references and curriculum citations", "course/modules/M/M4/index.html:183; references/references.json:3127-3170; curriculum", "PASS", C + " references/ and curriculum/ are unchanged in the delta (git diff --name-only f42f4329 ff388424 has no entries outside course/, tests/labs/, ledgers/).")
row("M4a-R08", "Hub card descriptions for L01-L10 against current lesson headings", "course/modules/M/M4/index.html:149-158; L01.html:35, L02.html:35, L03.html:35, L04.html:36", "PASS",
    C + " the L01/L02 hunks of this delta are at lines 140, 143 (L01) and 146, 149 (L02) only; cited line 35 is unchanged. Headings re-read: L01 h1 'Random Variables, Distributions and Quantiles', L02 h1 'Expectation and Variance', L03 h1 'Skewness and Kurtosis', L04 h1 'Independence and Conditional Expectation (Elementary)'.")
row("M4a-R09", "Hub prerequisite and lesson-order statements", "course/modules/M/M4/index.html:37-64; L01.html:37; L02.html:37, :94", "PASS", C + " git diff shows no hunk at L01.html:37 or L02.html:37, :94.")
row("M4a-R10", "Hub project ladder and project symbols", "course/modules/M/M4/index.html:162-170; course/modules/M/M4/project.html", "PASS",
    "index.html:164-170 names tail_risk.py, matched_scale, simulate_losses, quantile_99 and a proof appendix on finiteness of the matched Student-t; project.html contains all three function names (grep count 14) and tail_risk.py (lines 46, 202); the appendix A3 covers finiteness (project.html:322). check_projects M4 PASS (R01). project.html text itself is outside slice a and covered by its own slice.")
row("M4a-R11", "L01 whole-page reading: definitions, propositions, proofs, examples, misconceptions, problems, quiz", "course/modules/M/M4/L01.html:55-493", "PASS",
    "Full re-read this round of L01.html lines 55-511 (subject changed at :140 and :143). Checked: Prop 2.2 (a)-(d) and proof; Prop 3.2 proof; Remark 3.3 proof; Prop 3.4 and Example 3.5 (148.5 -> 149); Example 3.6 values F = 1/10, 3/10, 3/5, 4/5, 9/10, 1 and Q(1/2)=Q(3/5)=0, Q(61/100)=1; misconception 3 (148.5 -> 149); M1 (F=1/2 on [0,1), Q(1/2)=0), M2 (F(5)=7/10, Q(7/10)=5, Q(71/100)=7), M3 (40p=36 and 36.04 -> 37); R1 Q^s(3/5)=1; E1 F(2)=9/10; quiz items (Q(1/2)=1 for 1/4,1/2,1/4; 0.833 = 5/6; 198; 149). Printed Lab 1 output (run in ff38842) matches every value quoted in the prose (L01 twin output, see R03).")
row("M4a-R12", "L02 whole-page reading: definitions, propositions, proofs, examples, misconceptions, problems, quiz", "course/modules/M/M4/L02.html:55-402", "PASS",
    "Full re-read this round of L02.html lines 55-510 (subject changed at :146 and :149). Recomputed: E[X]=7/2, E[X^2]=91/6, Var=35/12, Var(2X)=35/3; loss E[L]=12500, E[L^2]=3125000000, Var=2968750000, sd=54486.24 (sqrt checked); E[L]=5000, Var=2.25e8, sd=15000 (M2); Var(aX)=36 (M3); R2 296875 and 544.8624; E[X]=3/10 for the L01 table; misconception numbers 15.17 and 2.92; quiz answers 3.5, 1, 12, 21/100, 225000000, 15000, 5. Lab output (run in ff38842): 489 losses, mean 3.469 (-0.031), 12225.0 cents, sd 54486.24 match the page prose.")
row("M4a-R13", "L03 prose and proof numbers", "course/modules/M/M4/L03.html:70-71, :90-96", "PASS", C + " L03.html unchanged. Not re-read line by line this round.")
row("M4a-R14", "L03 closed forms and printed skewness/kurtosis", "course/modules/M/M4/L03.html:64, :106, :251-252, :270", "PASS",
    "Re-run this round: skewed law mean 7/4, m2=163/16, m3=2157/32, m4=149461/256, m3^2/m2^3 = 18610596/4330747 (2.0730), m4/m2^2 = 149461/26569 (5.6254); Bernoulli(1/10): 64/9 and 73/9 match (1-2p)^2/(pq) and (1-3pq)/(pq). Printed lines equal these (L03 run). Lines in the page cited as carried from round 11 (" + C[len('Carried from round 11 ('):].split(')')[0] + ").")
row("M4a-R15", "L03 cross-references to L10", "course/modules/M/M4/L03.html:252; course/modules/M/M4/L10.html:65-66, :150-151", "PASS", C + " L10.html unchanged.")
row("M4a-R16", "L04 proofs, examples, Prop 1.4 and quiz", "course/modules/M/M4/L04.html:54-530; line 322; Prop 1.4 at :74-75; quiz q5 at :4", "PASS", C + " L04.html unchanged. Its printed numbers were re-run this round: Part A 3/50 both sides; Part B covariance 0, cell (0,0) 1/3 vs 1/9; Part C E[X|Y=0]=1, E[X|Y=1]=2/3, sum 4/5.")
row("M4a-R17", "L04 claims at line 300", "course/modules/M/M4/L04.html:300", "PASS", C + " Re-run output matches: 'table dependent independent False', 'table product cell_0_0 joint 3/50 ... 3/50'. The line-300 sentence 'The lab checks three exact tables' matches Parts A (2 tables) and B (1 table).")
row("M4a-R18", "Lab interpretation and hypothesis sentences agree with printed output (L01-L04)", "course/modules/M/M4/L01.html:140, :270; L02.html:146, :263; L03.html:127, :243; L04.html:174, :300", "PASS",
    "L01:140 and :270 and L02:146 and :263 re-read this round against the run output (all quoted values match). L03 and L04 lines are carried (" + "unchanged files): run output re-checked in R14 and R17.")
row("M4a-R19", "Labs: seeded and exact only; no data read; SIMULATED labelling", "tests/labs/M4/lab-M4-L01..L04-1.py; course/modules/M/M4/index.html:37, :175", "PASS",
    "Twins re-run this round (R03): standard library only, no network, exit 0; L02 and L03 seeded samples labelled SIMULATED in the page prose. index.html unchanged.")
row("M4a-R20", "Notation registry against symbols used in the slice", "notation/notation.json; L02.html:74-111; L03.html", "PASS",
    "notation/ unchanged. L02.html:74-111 (Proposition 1.3 and its proof, Example 1.4) carried: no hunk in that range. Symbols in the re-read L01/L02 text (Omega, p_k, F_k, Q, E, Var, mu, sigma, L, D) are used with the same meaning throughout those pages. L03 carried.")
row("M4a-R21", "Notation and learner-text checks, L03 and L04 cross-lesson symbols", "index.html:183; L03.html:106; L03.html:251-252; L04.html:6, :36, :538", "PASS", C + " L03 and L04 unchanged.")
row("M4a-R22", "No process words or placeholders in learner text", "index.html; L01-L04.html", "PASS",
    "grep -i over index.html and L01-L04.html for TODO, TBD, lorem, placeholder, draft, verifier, builder, 'round N': no match (empty output). L01 and L02 full text re-read this round.")
row("M4a-R23", "Lab heading numbering and lab naming", "course/modules/M/M4/L02.html:145, L03.html:126; L01.html:139, L04.html:173", "PASS",
    "L02.html:145 'Lab 1 · Exact expectations and variances of two finite laws...' and L01.html:139 'Lab 1 · The distribution function and quantile...' re-read this round (no hunk at those lines). L03/L04 carried.")
row("M4a-R24", "Ruff, format and mypy strict on the twins; page smoke", "tests/labs/M4/lab-M4-L01..L04-1.py; tools/page_smoke.py", "PASS",
    "ruff check tests/labs/M4 course/modules/M/M4 -> 'All checks passed!' (ruff.log, exit 0); ruff format --check tests/labs/M4 -> '13 files already formatted'; no twin line over 120 characters (awk); mypy --no-incremental on L01-L04 twins -> 'Success: no issues found in 4 source files'; page_smoke PASS (R02).")
row("M4a-R25", "Relevant pytest modules and verify_refs", "tests/test_docs_figures.py; tools/verify_refs.py --offline", "PASS",
    "verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' (verify_refs.log, exit 0). pytest -q tests/test_docs_figures.py -> 14 passed (pytest_docs.log, exit 0). tests/labs pytest not run in full.")
row("M4a-R26", "Grader, project.html and cards outside slice a (round-11 FAIL row kept by id)", "course/modules/M/M4/grader/test_project.py; course/modules/M/M4/project.html; course/modules/M/M4/cards.json (non-slice cards)", "UNVERIFIABLE",
    "Not checked in slice a. This delta changed grader/test_project.py (lines 279-297), project.html (:206, :215, :228, :322, :358-359) and non-slice cards. The round-11 survivor m11_loss_sign_flipped.py was tied to project.html:215; that sentence now says the suite does not test the sign (project.html:228), so its status belongs to the grader slice. Run tools/mutate_graders.py --unit M4 in that slice. Counted as not PASS here (fail closed).",
    "Verify in the slice that owns course/modules/M/M4/grader/test_project.py and project.html: re-run run_graders and mutate_graders for M4 and re-read project.html:206-228.")
row("M4a-R27", "Nav labels and titles match the target lesson h1", "course/modules/M/M4/L03.html:477-478; L04.html:6, :36, :538; index.html:152; L02.html:504", "PASS",
    "L02.html:503-504 read this round: 'L01 · Random Variables, Distributions and Quantiles' matches L01 h1; 'L03 · Skewness and Kurtosis' matches L03 h1. L01.html:504-505 read: 'M4 overview' and 'L02 · Expectation and Variance' matches L02 h1. L03 and L04 and index carried (unchanged).")
row("M4a-R28", "Cards changed in this delta (M4-c006, M4-c033, M4-c066) and card numbers in lesson", "course/modules/M/M4/cards.json (ids M4-c006 L01, M4-c033 L02, M4-c066 L04); L01.html, L02.html, L04.html", "PASS",
    "c006: Prop 2.2(d) exists (L01.html:85); 'x_1 < x_2 through x_m' hypothesis matches Prop 2.2. c033: '489' and '500' appear in L02.html:261 and :366; 'one run and gives no spread' matches L02.html:263 and :366. c066: '3/50', 'product of the marginals ... also 3/50' matches the L04 Part A output (cell (0,0) joint 3/50, product 3/50). No duplicate card ids or fronts in cards.json (191 cards). Other slice-a cards (L01-L04, 72 cards) carried: their lesson pages are unchanged. Number-in-lesson check: two regex hits (M4-c043 '5/3', M4-c044 '2/5') are LaTeX \\tfrac in L03.html:391, :439, :441 and not missing.")
row("M4a-R29", "Lab twin docstring lists its standard-library imports (L01-L04)", "tests/labs/M4/lab-M4-L02-1.py:3 and L02.html:149; tests/labs/M4/lab-M4-L03-1.py:3 and L03.html:130; compare lab-M4-L01-1.py:3 and L01.html:143", "FAIL",
    "The docstring says 'Standard library only (fractions, math, random)' in L02 (twin :3 and page :149) and in L03 (twin :3 and page :130), but both twins import 'from collections.abc import Sequence' (L02 twin line 18; L03 twin line 18). This delta added 'collections.abc' to the L01 list (L01.html:143, twin :3) and not to L02 or L03, so the three docstrings are now inconsistent. The L01 list itself is complete (itertools, collections.abc, fractions all imported at twin lines 16-18).",
    "Add ', collections.abc' to the parenthetical list in the L02 and L03 docstrings (twin line 3 and page line 149 for L02; twin line 3 and page line 130 for L03), keeping twin and page byte-identical, then run tools/embed_labs.py course/modules/M/M4/L02.html --refresh lab-M4-L02-1 (and L03 with lab-M4-L03-1), and re-run tools/run_labs.py --unit M4.")

fragment = {
    "unit": "M4", "slice": "a", "round": 12,
    "verifier": "Claude Haiku 5.5 independent verifier (verifyB12-M4-a)",
    "pin": "ff388424d9d056b7a57868dab5ae7f7cdeef60f6",
    "base": "f42f4329dcb0b5c2257e40cd6c27e734fa700d46",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyB12-M4-a",
    "scratch": S, "verified_at": "2026-10-29T12:00:00+00:00",
    "verdict": "FAIL", "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": ["Pin ff38842 vs previous pin f42f432: slice-a files changed: course/modules/M/M4/L01.html (line 140 hypothesis, line 143 docstring), course/modules/M/M4/L02.html (line 146 hypothesis, line 149 docstring), tests/labs/M4/lab-M4-L01-1.py and lab-M4-L02-1.py (docstring line 3), course/modules/M/M4/cards.json (M4-c006, c033, c066 among others). index.html, L03.html, L04.html, notation/, references/, tools/ byte-identical."],
    "notes": "Full re-read of L01.html and L02.html this round (changed pages). L03/L04 and index.html were not re-read line by line; their rows are carried by byte-identity (diff shows no hunk in those files). Mutants: slice a has no project grader; none written, and none of the 101 existing mutants in ledgers/M4/mutants was re-run because they target grader/test_project.py (another slice). Not run: tests/labs pytest in full, tools/fetch_data.py --check, run_graders/mutate_graders (grader is another slice), cards of L03/L04 re-verified only by spot-check.",
    "summary": "Slice a verdict FAIL: R29 (in slice, FAIL): the L02 and L03 lab docstrings list 'Standard library only (fractions, math, random)' but both twins also import collections.abc, while the L01 docstring (edited this delta) lists it. R26 (outside slice a, UNVERIFIABLE here) is the round-11 grader row, owned by the grader slice. 27 PASS, 1 FAIL, 1 UNVERIFIABLE. Fix: add 'collections.abc' to the list in L02 and L03 docstrings (twin and page), then tools/embed_labs.py course/modules/M/M4/L02.html --refresh lab-M4-L02-1 and the same for L03, and re-run run_labs --unit M4."
}
# R28 is PASS, R29 is the FAIL: ids R01..R29 keep the M4a-R numbering
out = '/Users/billyribeiro/.fanout/wt/verifyB12-M4-a/ledgers/M4/M4-a.json'
import os
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(fragment, open(out, 'w'), indent=2, ensure_ascii=False)
print(ledger.validate(json.load(open(out)), 'M4-a'))
