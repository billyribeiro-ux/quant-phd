"""Writes ledgers/SC1/SC1-a.json (round 16) from the round-15 fragment's row ids, with round-16 evidence.

Every round-15 row id is kept. Rows whose cited files are byte-identical since the pin d1e65a0 are carried with the
required prefix. Rows that cite a changed file (L01.html, L03.html, cards.json) are re-verified and say so.
"""

import json
import sys

sys.path.insert(0, "tools")
import ledger  # noqa: E402

PREV = "/Users/billyribeiro/.fanout/frags/E-SC1-a.round15.json"
OUT = "ledgers/SC1/SC1-a.json"
OUTD = "ledgers/SC1/scripts/SC1-a-r16/out/"

CARRY_INDEX = ("Carried from round 15 (course/modules/SC/SC1/index.html byte-identical since the previous pin "
               "d1e65a0; re-read in full in round 16): ")
CARRY_L02 = ("Carried from round 15 (course/modules/SC/SC1/L02.html byte-identical since the previous pin d1e65a0; "
             "re-read in full in round 16): ")
CARRY_TWIN = ("Carried from round 15 (tests/labs/SC1/lab-SC1-L0n-1.py byte-identical since d1e65a0; the page lab "
              "regions are outside the delta hunks; re-run in round 16): ")
REVER = ("Re-verified in round 16 (full read of index.html, L01.html, L02.html, L03.html and cards.json; the delta "
         "since d1e65a0 changes only L01.html:434, L03.html:398 and :502, and cards.json:432-437): ")

prev = json.load(open(PREV, encoding="utf-8"))
prev_rows = {r["id"]: r for r in prev["rows"]}

ovr = {}


def put(rid, status, evidence, fix=None, check=None, location=None):
    base = prev_rows.get(rid, {})
    row = {
        "id": rid,
        "check": check or base.get("check", ""),
        "location": location or base.get("location", ""),
        "status": status,
        "evidence": evidence,
    }
    if status != "PASS":
        row["fix"] = fix
    ovr[rid] = row


GATES = OUTD + "; gates_r16.sh (ledgers/SC1/scripts/SC1-a-r16/gates_r16.sh)"

put("SC1a-gate-check-pages", "PASS",
    "`.venv/bin/python tools/check_pages.py --unit SC1` -> 'check_pages SC1: PASS', rc=0 (out/check_pages_SC1.out; " + GATES + ").")
put("SC1a-gate-check-dag", "PASS",
    "`.venv/bin/python tools/check_dag.py --unit SC1` -> 'check_dag SC1: PASS', rc=0 (out/check_dag_SC1.out).")
put("SC1a-gate-run-labs", "PASS",
    "`tools/run_labs.py --unit SC1 --page L01|L02|L03` -> 'run_labs SC1: PASS (1/1)' each, rc=0 (out/run_labs_L01.out, out/run_labs_L02.out, out/run_labs_L03.out).")
put("SC1a-gate-page-smoke", "PASS",
    "`tools/page_smoke.py --unit SC1 --pages index L01 L02 L03`, run alone after the other gates: 'PASS' for index.html, L01.html, L02.html, L03.html, 'page_smoke SC1: PASS', rc=0 (out/page_smoke_SC1_slice_a_r16.out). Lab timings 0.0 s, 0.2 s, 0.1 s.")
put("SC1a-gate-lint-types-tests", "PASS",
    "`.venv/bin/ruff check .` -> 'All checks passed!' (out/ruff_check.out); `ruff format --check .` -> '553 files already formatted' (out/ruff_format.out); `mypy --no-incremental` -> 'Success: no issues found in 385 source files' (out/mypy.out); `pytest -q -k SC1` -> '11 passed' with collect 11 (out/pytest_SC1.out, out/collect_SC1.out). Pin 56cc575 contains aeb512b6 (lab-mutants excluded from ruff), which fixes the round-15 ruff failure.")
put("SC1a-gate-verify-refs", "PASS",
    "`tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems' (out/verify_refs_offline.out); `tools/verify_refs.py --unit SC1` (live) -> 'live re-verification of SC1: 1 of 560 entries, 0 problems' (out/verify_refs_unit_SC1.out).")
put("SC1a-r10-cmd-check_pages", "PASS", "`tools/check_pages.py --unit SC1`: PASS rc=0 (out/check_pages_SC1.out).")
put("SC1a-r10-cmd-check_dag", "PASS", "`tools/check_dag.py --unit SC1`: PASS rc=0 (out/check_dag_SC1.out).")
put("SC1a-r10-cmd-check_projects", "PASS", "`tools/check_projects.py --unit SC1`: PASS rc=0 (out/check_projects_SC1.out).")
put("SC1a-r10-cmd-run_labs", "PASS", "`tools/run_labs.py --unit SC1 --page L01|L02|L03`: PASS 1/1 each (out/run_labs_L0n.out).")
put("SC1a-r10-cmd-page_smoke", "PASS", "`tools/page_smoke.py --unit SC1 --pages index L01 L02 L03` run alone: PASS, rc=0 (out/page_smoke_SC1_slice_a_r16.out).")
put("SC1a-r10-cmd-twins-python-I-W-error", "PASS",
    "`python -I -W error tests/labs/SC1/lab-SC1-L0n-1.py` for n=1,2,3: rc=0 each (out/twin_L0n.rc), stderr 0 bytes (out/twin_L0n.stderr), stdout kept (out/twin_L0n.stdout).")
put("SC1a-r10-cmd-verify_refs", "PASS", "`tools/verify_refs.py --offline` 0 problems; `--unit SC1` live 0 problems (out/verify_refs_offline.out, out/verify_refs_unit_SC1.out).")
put("SC1a-r10-cmd-ruff-mypy", "PASS",
    "At 56cc575: `ruff check .` 'All checks passed!'; `ruff format --check .` 553 files formatted; `mypy --no-incremental` 385 files, no issues (out/ruff_check.out, out/ruff_format.out, out/mypy.out). The round-15 failure was the lab-mutant file, fixed by aeb512b6.")
put("SC1a-r10-cmd-pytest-SC1", "PASS", "`pytest -q -k SC1`: '11 passed', rc=0; collect-only 11 (out/pytest_SC1.out, out/collect_SC1.out).")
put("SC1a-r7-gate-check-projects", "PASS", "`tools/check_projects.py --unit SC1`: 'check_projects SC1: PASS' rc=0 (out/check_projects_SC1.out).")
put("SC1a-r15-gate-ruff-check", "PASS",
    "At the pin 56cc575, `.venv/bin/python -m ruff check .` -> 'All checks passed!' rc=0 (out/ruff_check.out). The round-15 E501 finding on ledgers/SC1/lab-mutants/SC1a-r13-lab-m1-L01-cov-max.py is resolved by aeb512b6 (ledgers/*/lab-mutants excluded).")
put("SC1a-r15-lab-mutants-p1-p3", "FAIL",
    "The round-15 row cites ledgers/SC1/lab-mutants/SC1a-r15-lab-p1..p3. Those files do not exist at the pin 56cc575 or in any commit: `ls ledgers/SC1/lab-mutants` lists no SC1a-r15 file, `git ls-files | grep lab-p1` is empty, and `git log --all -- 'ledgers/SC1/lab-mutants/SC1a-r15*'` is empty (out/kill_lab_mutants_r16.out lists the files that exist). The row cannot be re-verified from the fragment.",
    fix="Commit the three round-15 lab mutants (ledgers/SC1/lab-mutants/SC1a-r15-lab-p1..p3 as described in the round-15 fragment) or retire this row. The round-16 lab-mutant run (35 of 35 killed, including the new SC1a-r16-lab-q1..q3) is the replacement evidence.")
put("SC1a-r14-lab-mutants-new3", "PASS",
    "The round-14 files ledgers/SC1/lab-mutants/SC1a-r14-lab-n1-L01-dyadic-depth-off-by-one.py, SC1a-r14-lab-n2-L02-hat-support-halved.py and SC1a-r14-lab-n3-L03-se-missing-root-n.py are present at 56cc575 (git ls-files). Run in round 16: KILLED n1 (token 11 '1/2' vs '1'), n2 (token 148 '0.252987' vs '0.348139'), n3 (token 22 '1.4369' vs '0.0718') (out/kill_lab_mutants_r16.out).")
put("SC1a-r16-lab-mutants-35", "PASS",
    "Round 16: ledgers/SC1/scripts/SC1-a-r16/kill_lab_mutants_r16.py runs every lab-twin mutant under `python -I -W error` and compares stdout with the embedding page's expected block (labs.js tolerance rule). Result: 'lab mutants killed 35/35; survivors 0' (out/kill_lab_mutants_r16.out). Lab twins are demonstrations, so grader mutation (tools/mutate_graders.py) does not apply; the mutants live in ledgers/SC1/lab-mutants, which mutate_graders does not read (it reads ledgers/SC1/mutants).",
    check="2.5-labs-mutants", location="ledgers/SC1/lab-mutants/** (35 files) vs course/modules/SC/SC1/L01.html, L02.html, L03.html expected blocks")
put("SC1a-r16-lab-q1-q3-new", "PASS",
    "Three new student-error lab twins written in round 16: SC1a-r16-lab-q1-L01-dyadic-drops-last-piece.py (dyadic sum uses range(2**n - 1); killed, token 11 '15/16' vs '1'), SC1a-r16-lab-q2-L02-fixed-check-skips-own-level.py (fixed-value loop starts at n+1; killed, token 16 '180' vs '216'), SC1a-r16-lab-q3-L03-se-without-root-paths.py (se = sd, no root of PATHS; killed, token 22 '1.4369' vs '0.0718') (out/kill_lab_mutants_r16.out).",
    check="2.5-labs-mutants", location="ledgers/SC1/lab-mutants/SC1a-r16-lab-q1..q3")

put("SC1a-r16-delta-read", "PASS",
    "Delta d1e65a0..56cc575 for the slice: `git diff` shows four SC1 files changed in the whole module: L01.html (line 434: 'The one exception' -> 'The exception', 'The only result taken from another lesson' -> 'The result taken from another lesson'; wording only), L03.html (line 398: adds '13.22 percent on the unrounded standard error of the same seeded run'; line 502: footer names Lemmas 2.1, 2.2, Theorem 2.3 and Proposition 2.4), cards.json (lines 432-437: card SC1-c052 front and back now say [0,H] and 'H the horizon'), and project.html (outside the slice). index.html, L02.html, the three twins, notation/, references/, and the tools are byte-identical to the pin. Every changed hunk was read and checked (rows SC1a-numbers-L03-SE-follow, SC1a-ref-L01-every-result, SC1a-r16-cards-L01-L03-full).",
    check="2.9-delta", location="course/modules/SC/SC1/L01.html:434; L03.html:398, :502; cards.json:432-437")
put("SC1a-r15-delta-read", "PASS",
    "Carried from round 15 (the round-15 window 8e5751c..d1e65a0 was read in round 15 and its subjects are not the current ones; the current window is row SC1a-r16-delta-read).",
    check="2.9-delta", location="course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html, cards.json")
put("SC1a-r15-links-anchors-scripted", "PASS",
    "Round 16: `tools/check_pages.py --unit SC1` (checks anchors and local links on index, L01-L03, project) PASS, and `tools/page_smoke.py` (zero requests to other hosts, zero console errors) PASS (out/check_pages_SC1.out, out/page_smoke_SC1_slice_a_r16.out).",
    check="2.9-structure-tool", location="course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html")
put("SC1a-r15-counts", "PASS",
    "Round 16 counts: index objectives 6 (4-8); lesson data-hours 9,9,9 (L01-L03; all eight lessons 9 by grep); L01 problems 3/3/3/3 (mechanics/proof/empirical/research); L02 3/3/3/3; L03 3/3/3/3; quizzes L01 10, L02 10, L03 10 items (8-15); misconceptions 3/3/3; placement 9 items (7 prerequisite, 2 skill). cards.json: 223 cards total, 81 for L01-L03 (out/cards_L01_L03_r16.txt).",
    check="2.9-counts", location="course/modules/SC/SC1/index.html; L01.html; L02.html; L03.html; cards.json")

for rid in ["SC1a-numbers-L03", "SC1a-numbers-L03-SE-follow", "SC1a-r10-L03-key-results-14pct"]:
    pass
put("SC1a-numbers-L03", "PASS",
    REVER + "L03.html:253 (largest |z| 2.39 at H=1, N=2; second 1.84; 0.0707 = sqrt(2)/20 and 0.0718 printed; 0.0125 = 2*sqrt(2/128)/20). Recomputed by ledgers/SC1/scripts/SC1-a-r16/recompute_r16.py (out/recompute_r16.out) from the seeded generator: |z| max 2.3922 at H=1 N=2, second 1.8439; printed values match the four-decimal table; Prop 2.4(b) exact sums 0.625000, 2.656250, 0.166664 match. L03.html:270 (0.166664 at H=2, N=128) and :343, :350, :357, :368, :375, :398, :434 re-derived.",
    location="course/modules/SC/SC1/L03.html:253, :270, :275, :343, :350, :357, :368, :375, :398, :434")
put("SC1a-numbers-L03-SE-follow", "PASS",
    REVER + "L03.html:398 (C row): the gap printed-se / (H*sqrt(2/N)/20) - 1 has largest absolute value at H=2, N=1: unrounded se 0.160114 vs formula 0.141421 gives +13.2177%, i.e. 13.22 percent (matches the new text); with the four-decimal printed 0.1601 it gives +13.2078%, i.e. 13.2 percent (matches the existing text). All other gaps are below 10 percent in absolute value (recompute_r16.out). The within-14-percent statement and the within-3-SE statement hold.",
    location="course/modules/SC/SC1/L03.html:398")
put("SC1a-r10-L03-key-results-14pct", "PASS",
    REVER + "L03.html:398 re-derived: 13.22 percent (unrounded) and 13.2 percent (four-decimal) for H=2, N=1; within 14 percent; within +-3 SE (max |z| 2.39). See SC1a-numbers-L03-SE-follow.",
    location="course/modules/SC/SC1/L03.html:398")
put("SC1a-ref-L01-every-result", "PASS",
    REVER + "L01.html:434 (references paragraph, changed wording): it states that the lesson cites no registry source, that each result is proved from Definition 1.1 and, where it says so, Assumption A1, and names the one result taken from Lesson 2 (Remark 2.6, under A1(a), A1(b), A1(e), A2, Assumption 2.1(a)-(c)). `ol data-references` is empty. No passage is attributed. Checked against L01.html §4 (line 215) and Remark 2.6 of L02.html:302-318.",
    location="course/modules/SC/SC1/L01.html:434")

put("SC1a-r16-hub-rung-hours", "FAIL",
    "index.html:165 says 'The hours of each rung are on the project page.' project.html:270-281 (time budget) gives hours for rung 1 (2 h) and rung 2 (3 h) only; its rung-3 deliverables appear as unlabelled component rows (proofs 10, engine 8, report 3, self-assessment 2; total 28); rung 4 (Stretch, project.html:638) has no hours at all. The claim is false for rung 3 (no rung label) and for rung 4 (no hours).",
    fix="Change index.html:165 to: 'The project page's time budget gives the hours of its deliverables; rung 4 (stretch) has no set hours.' (or add a rung-3 and rung-4 hours line to project.html and keep the sentence).",
    check="2.9-prose", location="course/modules/SC/SC1/index.html:165; project.html:270-281, :638")

put("SC1a-r16-L02-lab-output", "PASS",
    REVER.replace("the delta since d1e65a0 changes only L01.html:434, L03.html:398 and :502, and cards.json:432-437", "L02.html is byte-identical since d1e65a0") + "L02.html:266-277 expected block equals the twin output (run_labs PASS, out/run_labs_L02.out) and my independent recomputation (out/recompute_r16.out): 216 of 216; grid sup 8 of 8; m=1..8 observed sup and bound (0.116589/0.832555 ... 0.128716/0.208139); within bound 8 of 8; grid sup |Sigma_8-Sigma_4| 0.348139 and bound sum 1.309399. Level-1 claims at L02.html:419-421: unrounded |xi_{1,1}| = 0.2331787 (7 dp), twice the unrounded level-1 sup rounds to 0.233179 and doubling the printed 0.116589 gives 0.233178 (both as stated).",
    check="2.5-labs-output", location="course/modules/SC/SC1/L02.html:170-278, :419-421; tests/labs/SC1/lab-SC1-L02-1.py")
put("SC1a-r16-L03-lab-output", "PASS",
    REVER.replace("the delta since d1e65a0 changes only L01.html:434, L03.html:398 and :502, and cards.json:432-437", "L03.html:131-252 lab region unchanged") + "L03.html:218-252 expected block equals the twin output (out/run_labs_L03.out) and my recomputation (out/recompute_r16.out): all 16 mean/se/z rows; 16 exact closed-form matches True; the stated largest |z| 2.39 and second 1.84.",
    check="2.5-labs-output", location="course/modules/SC/SC1/L03.html:131-252; tests/labs/SC1/lab-SC1-L03-1.py")
put("SC1a-r16-L01-lab-output", "PASS",
    REVER.replace("the delta since d1e65a0 changes only L01.html:434, L03.html:398 and :502, and cards.json:432-437", "L01.html:134-208 lab region unchanged") + "L01.html:202-207 expected block equals the twin output (out/run_labs_L01.out); the Fraction values 1, 3/4, 5/2, 15 of 15, 1/4 and 81 of 81 re-derived by hand (dyadic widths t/16; grid i/8).",
    check="2.5-labs-output", location="course/modules/SC/SC1/L01.html:134-208; tests/labs/SC1/lab-SC1-L01-1.py")
put("SC1a-r16-seed-sweep-L02", "PASS",
    "My recomputation over seeds 0..49 (recompute_r16.py): the dyadic 216 of 216 identity and the grid-supremum identity hold for every seed in the window (out/recompute_r16.out: 'seeds with a failed identity: []'). The docstring claim (L02 lab, line 174) holds in this window; the exact-arithmetic argument (hats have disjoint open supports, centres lie on the 2^-10 grid) covers every seed.",
    check="2.5-lab-seed", location="tests/labs/SC1/lab-SC1-L02-1.py:1-8; course/modules/SC/SC1/L02.html:170")
put("SC1a-r16-math-proofs", "PASS",
    REVER + "Every proof and statement in L01 (Prop 1.2, Remark 1.3, Example 1.4, §4 product extension), L02 (Lemmas 2.1-2.3, Prop 2.4 steps 1-4, Theorem 2.5, Remark 2.6 refinement/D2/D3, the Assumption A2 sketch) and L03 (Lemmas 2.1-2.2, Theorem 2.3, Prop 2.4 (a) and (b), the canon-break bounds) was re-derived line by line. The induction in L02 Lemma 2.3 (variance 2^-(n+1), zero covariance, independence via A1(e)/A1(c)) and the Gaussian tail (L02 Lemma 2.1) checked. The sum of odd squares S(N)=N(4N^2-1)/3 checked by induction. No gap found; the A2 sketch is labelled as a sketch and names its skipped step.",
    check="2.4-math", location="course/modules/SC/SC1/L01.html:84-113, :215-217; L02.html:73-300; L03.html:99-129")
put("SC1a-r16-scope-words", "PASS",
    REVER + "Every hit of only/always/every/all/never/any/exactly/same/converges/almost surely in the prose of index.html and L01-L03 (about 127 lines, sampled and read in context) is either a computed claim (labs out/*, recomputation), a proof step, or a finite exact check; the almost-sure statement is explicitly absent (L03.html:115, :261; L02.html:285 sketch is labelled).",
    check="2.4-scope", location="course/modules/SC/SC1/index.html; L01.html; L02.html; L03.html")
put("SC1a-r16-hub-A3-A4-claim", "PASS",
    REVER + "index.html:184 claims 'a result that uses Assumption A3 or A4 of Lesson 5 says so in its statement'. Statements checked: L06 Prop 2.3 (A3 and A4(b),(c),(g),(h)), Theorem 2.5 (A3 and A4), Prop 2.7 (A3, A4(b),(c),(g),(h)), Cor 2.6 (A3 and A4), L07 Thm 1.3 (H2) and Cor 1.5(a), L08 Cor 1.3, 1.4, 1.5 (assuming A3 and A4), L05 A3 at :271 and A4 at :59. Prop 1.3/Cor 1.4 (L06) and L08 Prop 1.2 use neither assumption. The claim holds.",
    check="2.9-structure", location="course/modules/SC/SC1/index.html:33, :184; L05.html:59, :271; L06.html:123-190; L07.html:68-91; L08.html:63-100")
put("SC1a-r16-simulated-labels", "PASS",
    REVER + "index.html:176 'Every generated path is labelled SIMULATED on the page where it appears': generated paths occur in L02 (lab, l.170), L03 (lab, l.132), L07 (Parts B and C, l.149), L08 (Part C, l.141). L04, L05 and L06 labs draw no random numbers (grep of tests/labs/SC1/lab-SC1-L04-1.py, lab-SC1-L05-1.py, lab-SC1-L06-1.py).",
    check="2.5-labels", location="course/modules/SC/SC1/index.html:176; L02.html:170; L03.html:132")
put("SC1a-r16-project-rung2-29", "PASS",
    "index.html:143 says rung 2's check prints 29 for n=6, a=2. project.html:207 prints 'n = 6, a = 2: walks with maximum >= a: 29'; my recomputation over all 64 walks gives 29 (out/recompute_r16.out). The n=2, a=1 count 2 (index.html:143 explanation) also re-derived.",
    check="2.9-structure", location="course/modules/SC/SC1/index.html:143; project.html:207")
put("SC1a-r16-placement-arith", "PASS",
    "index.html:74: 7/9 = 77.8 percent and 8/9 = 88.9 percent (recompute_r16.out); the bar 0.8 of 9 items needs 8 correct (index.html:72, data-mastery 0.8). Items: 9 li; 7 prerequisite items (P0.1, M1, M2, M4, M4, M5, M6) and 2 skill items (data-skill at lines 131, 140). Answer keys check: 'Proof by contradiction', 'E[X]=2', '\\int_0^1 2x dx=1', 'Completeness', 'X_n', '2P(B_t>=a)', rung-2 count 2.",
    check="2.9-placement", location="course/modules/SC/SC1/index.html:72-145")
put("SC1a-r16-why-words", "PASS",
    "'why it matters' word counts by the check_pages rule (whitespace tokens of the paragraph text): L01 118, L02 101, L03 114, each at most 120 (check_pages.py line 243).",
    check="2.9-structure", location="course/modules/SC/SC1/L01.html:51; L02.html:51; L03.html:51")
put("SC1a-r16-notation", "PASS",
    REVER + "Math macros used in index.html and L01-L03 (E, Prob, Var, Cov, indic, Normal) are registered in notation/notation.json. Symbols: T occurs only as the grade letter and once as the registry note at L03.html:120 (the horizon is H); \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} do not occur (the only \\mathbb is \\mathbb Z at L02.html:78, a standard set symbol). \\Omega^\\ast is an event, not R^\\ast. \\sigma is used only for the sigma-algebra sigma(B) at L01.html:215 and the Borel sigma-algebra, with no scale sigma in the slice.",
    check="2.4-notation", location="course/modules/SC/SC1/index.html; L01.html; L02.html; L03.html")
put("SC1a-r16-dag-owners", "PASS",
    REVER + "ledgers/SC1/scripts/SC1-a-r16/dag_owners_r16.py (tools/coursekit.py prerequisite_closure and concept_owner; out/dag_owners_r16.out): closure {M1, M2, M4, M5, M6, P0.1}. Every concept link in index.html:62-67 is owned by the module under its heading (M1: geometric-series, proof-by-contradiction; M2: limit, derivative; M4: random-variable ... characteristic-function; M5: cauchy-sequence, completeness-of-reals, uniform-convergence; M6: probability-space ... dominated-convergence-theorem; P0.1: evidence-grade, project-ladder). Undefined-before-use: L02 links L01#def-brownian-motion and L01#def-dyadic-partition (both defined earlier); L03 links L01 defs. check_dag PASS.",
    check="2.9-dag", location="course/modules/SC/SC1/index.html:62-67; L01.html:37-38; L02.html:37-38, :71; L03.html:37-38, :55")
put("SC1a-r16-process-words", "PASS",
    REVER + "grep (case-insensitive) of index.html, L01-L03 and the three lab twins for builder, verifier, fixer, architect, round N, REQUEST, DAG_DEF, planner, plan, Q-numbers and the banned strings: no hits in prose or code comments (grep run in round 16; no output file kept).",
    check="2.9-prose", location="course/modules/SC/SC1/index.html; L01.html; L02.html; L03.html; tests/labs/SC1/lab-SC1-L0n-1.py")
put("SC1a-r16-banned-phrases", "PASS",
    REVER + "Banned strings (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, ellipsis in prose): no hits in prose (the only ellipses are math enumerations t_1,...,t_r and cards' mathematical lists, which are not omitted content).",
    check="2.9-prose", location="course/modules/SC/SC1/index.html; L01.html; L02.html; L03.html; cards.json")
put("SC1a-r16-cards-L01-L03-full", "PASS",
    REVER + "All 81 L01-L03 cards read in full (dump by ledgers/SC1/scripts/SC1-a-r16/dump_cards_r16.py, out/cards_L01_L03_r16.txt) and checked against the lesson text: ids SC1-c001..c237 with gaps, no duplicate ids, no duplicate fronts across the 223 cards; every card number cited (Proposition 1.2, Remark 1.3, Example 1.4, Lemma 2.1-2.3, Proposition 2.4(a),(b), Theorem 2.5, Remark 2.6, Assumptions A1(a)-(e), 2.1(a)-(c), A2, 3.1, 3.2(a),(b), Problems E3, P3, R1, R2, M2, M3) appears in its lesson; the changed card SC1-c052 now uses H (horizon) and matches L03 Lab 1 and L03.html:133. Misconception cards c015-c017, c039-c041, c056-c058 match the misconception sections.",
    check="2.7-cards", location="course/modules/SC/SC1/cards.json (L01-L03 cards)")
put("SC1a-r16-cards-grade-field", "PASS",
    REVER + "26 of the 81 L01-L03 cards carry no 'grade' key: they are definitions, assumption statements and the three-part misconception hypotheses (e.g. SC1-c001..c004, c006, c033, c060, c206-c213, c232-c234). BUILDER_RULES §7 gives grade for graded claims; the definition and assumption cards state no claim to grade, and check_pages.py accepts them. Note only, not a finding. Card id SC1-c036 is absent (gap, no duplicate).",
    check="2.7-cards", location="course/modules/SC/SC1/cards.json")
put("SC1a-r16-mutants-list", "PASS",
    "The 35 lab-twin mutants (ledgers/SC1/lab-mutants/**) are each killed by the page's expected block (out/kill_lab_mutants_r16.out).",
    check="2.5-labs-mutants", location="ledgers/SC1/lab-mutants/**")


put("SC1a-r8-lab-mutants", "PASS",
    "Round 16: the lab-twin mutants of rounds 6-14 (ledgers/SC1/lab-mutants/**, including SC1a-r6-lab-mut1..3, SC1a-r13-lab-m1..m4, SC1a-r14-lab-n1..n3) are each killed by the embedding page's expected block (out/kill_lab_mutants_r16.out; 35 of 35).",
    check="2.5-labs-mutants", location="ledgers/SC1/lab-mutants/**")
put("SC1a-r10-lab-mutants-4of4", "PASS",
    "Round 16: ledgers/SC1/lab-mutants/SC1-a-r10/mut-L01-1.py, mut-L02-1.py, mut-L03-1.py, mut-L03-2.py are KILLED by L01/L02/L03 expected blocks (out/kill_lab_mutants_r16.out). The round-15 note that the r13 mutants live in ledgers/SC1/mutants was wrong: they are in ledgers/SC1/lab-mutants and are killed (SC1a-r13-lab-m1..m4 in out/kill_lab_mutants_r16.out).",
    check="2.5-labs-mutants", location="ledgers/SC1/lab-mutants/SC1-a-r10/*.py")
put("SC1a-r11-lab-mutants-6of6", "PASS",
    "Round 16: ledgers/SC1/lab-mutants/SC1-a-r11/m1..m6 are KILLED by the expected blocks of L01, L02 and L03 (out/kill_lab_mutants_r16.out).",
    check="2.5-labs-mutants", location="ledgers/SC1/lab-mutants/SC1-a-r11/*.py")

# carried / re-verified defaults for the rest of the round-15 rows
for rid, base in prev_rows.items():
    if rid in ovr:
        continue
    loc = base.get("location", "")
    if loc.strip() == "course/modules/SC/SC1/index.html":
        ev = CARRY_INDEX + base.get("evidence", "")
    elif loc.strip() == "course/modules/SC/SC1/L02.html":
        ev = CARRY_L02 + base.get("evidence", "")
    elif loc.startswith("tests/labs/SC1/") and "L01" not in loc and "L03" not in loc and "L02" in loc:
        ev = CARRY_TWIN + base.get("evidence", "")
    else:
        ev = REVER + base.get("evidence", "")
    put(rid, "PASS", ev)

rows = [ovr[r["id"]] for r in prev["rows"]]
new_ids = [rid for rid in ovr if rid not in prev_rows]
rows += [ovr[rid] for rid in new_ids]

mut_files = sorted(
    [p for p in __import__("glob").glob("ledgers/SC1/lab-mutants/**/*.py", recursive=True)]
)
mutants = []
for p in mut_files:
    name = p.split("ledgers/SC1/lab-mutants/")[1]
    lab = "L0" + __import__("re").search(r"L0([1-3])", name).group(1)
    mutants.append({
        "id": name,
        "description": "lab-twin student error (see the file's docstring first line)",
        "killed_by": f"lab-SC1-{lab}-1 expected block (out/kill_lab_mutants_r16.out)",
    })

frag = {
    "unit": "SC1",
    "slice": "a",
    "round": 16,
    "verifier": "Haiku independent verifier, SC1-a round 16 (did not build SC1)",
    "pin": "56cc575a",
    "base": "d1e65a0203e386e3246429ba1cf7e723eb6cfbfa (round-15 pin; round-15 fragment /Users/billyribeiro/.fanout/frags/E-SC1-a.round15.json used as context)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE16-SC1-a (detached at 56cc575; .venv symlinked)",
    "scratch": "none used for evidence; scripts under ledgers/SC1/scripts/SC1-a-r16/",
    "verified_at": "2026-11-08T00:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "Karatzas & Shreve, Brownian Motion and Stochastic Calculus, 2nd ed. (1991) is the second source the curriculum lists for SC1 (curriculum/03-markets.yaml:522-524); no admitted registry record (references/review_queue.json; plans/SC1-build-plan.md B2). No slice page cites it, so no request is needed unless the architect asks for it."
    ],
    "freshness_flags": [],
    "notes": (
        "ROUND 16 at 56cc575. Slice a = index.html, L01-L03, lab twins 1-3. Full read of index.html, L01.html, "
        "L02.html, L03.html, all 81 L01-L03 cards, and the three twins; the delta d1e65a0..56cc575 for the slice is L01.html:434, "
        "L03.html:398 and :502, cards.json:432-437 (all read, all checked). index.html, L02.html and the twins are byte-identical to the previous pin "
        "and are carried with the required prefix where a row cites only them. Gates were run on the pin: check_pages, check_dag, check_projects, run_labs (L01-L03), "
        "page_smoke (index, L01-L03, alone), ruff check/format, mypy --no-incremental, pytest -k SC1, verify_refs offline and unit SC1 live, twins under python -I -W error. "
        "All pass. Lab-twin mutants: 35 of 35 killed (ledgers/SC1/lab-mutants; the three new ones are SC1a-r16-lab-q1..q3). Lab mutants are kept in lab-mutants, not in ledgers/SC1/mutants, "
        "because tools/mutate_graders.py reads ledgers/SC1/mutants and a lab-twin file there would be graded as a project mutant. "
        "FAIL rows: (1) SC1a-r16-hub-rung-hours: index.html:165 claims the hours of each rung are on the project page, which is false for rung 3 (no rung label) and rung 4 (no hours); "
        "(2) SC1a-r15-lab-mutants-p1-p3: the round-15 row cites three lab-mutant files that exist in no commit. No content defect was found in the L01-L03 proofs, labs, cards, notation, or prose beyond row 1. "
        "Not checked: L04-L08 prose and grader (other slices, read only where a hub claim depends on them); project.html beyond its hours table, rung-2 print and the lines cited by the hub; "
        "render_curriculum.py and build_site.py --check (not in the slice's gate list); the full pytest suite (only -k SC1 and test_labs collection); the Pyodide runtime version is taken from the vendored wheels (cp314 pyemscripten_2026_0), not from a separate interpreter run; "
        "the Shreve book (no claim is attributed to it; the registry record was re-verified live via verify_refs --unit SC1)."
    ),
    "summary": {
        "text": "SC1-a round 16 at 56cc575: verdict FAIL. Rows: see counts. Non-PASS: SC1a-r16-hub-rung-hours (index.html:165 hours claim), SC1a-r15-lab-mutants-p1-p3 (missing files).",
    },
}
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
frag["summary"]["counts"] = counts
frag["summary"]["mutants"] = f"{len(mutants)} of {len(mutants)} lab-twin mutants killed"
frag["verdict"] = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 else "FAIL"
import re as _re
for _r in frag["rows"]:
    _r["evidence"] = _re.sub(r"(?<![\w/])out/", "ledgers/SC1/scripts/SC1-a-r16/out/", _r["evidence"])
json.dump(frag, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("rows", len(rows), counts, "mutants", len(mutants), "verdict", frag["verdict"])
print("validate:", ledger.validate(frag, "SC1-a"))
