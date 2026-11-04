"""Build the round-8 fragment for M2 slice e from the round-7 row ids (every id kept)."""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(sys.argv[1]); OUT = ROOT / "ledgers/M2/M2-e.json"
prev = json.loads(Path("/Users/billyribeiro/.fanout/frags/D-M2-e.round7.json").read_text(encoding="utf-8"))
S = "ledgers/M2/scripts/M2-e-r8"
CARRY = "Carried from round 7 (course/modules/M/M2/grader/*, tests/labs/M2/*, course/modules/M/M2/cards.json entries of this lesson, byte-identical since the round-7 pin 9373ef39):"
CARD_LESSONS_CARRIED = ("L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "L09", "L10", "L11", "L12", "L13",
                        "L15", "L16", "L18", "L19", "L20", "L21")

ev = {}
def add(i, status, evidence, fix=None):
    ev[i] = (status, evidence, fix)

add("e2-check-pages", "PASS", f"`.venv/bin/python tools/check_pages.py --unit M2` -> 'check_pages M2: PASS' ({S}/check_pages_M2.out, exit 0)")
add("e2-check-dag", "PASS", f"`.venv/bin/python tools/check_dag.py --unit M2` -> 'check_dag M2: PASS' ({S}/check_dag_M2.out, exit 0)")
add("e2-check-projects", "PASS", f"`.venv/bin/python tools/check_projects.py --unit M2` -> 'check_projects M2: PASS' ({S}/check_projects_M2.out, exit 0)")
add("e2-run-graders", "PASS", f"`tools/run_graders.py --unit M2` -> 'run_graders M2: PASS (reference 50/50 seeds, slowest 0.2 s)' ({S}/run_graders_M2.out)")
add("e2-run-labs-project", "PASS", f"`tools/run_labs.py --unit M2 --page project` -> 'run_labs M2: PASS (3/3)' ({S}/run_labs_project.out). Note: --page takes the file stem, so `--page project.html` selects 0 labs.")
add("e2-lab-page-code-equals-twin", "PASS", f"`tools/run_labs.py --unit M2` -> 'run_labs M2: PASS (27/27)' ({S}/run_labs_M2.out): page code byte-identical to twin for every lab, project labs included")
add("e2-lab-twin-clean-and-expected", "PASS", f"each of the 27 twins run as `python -I -W error tests/labs/M2/<twin>` from an empty directory: rc=0, stderr 0 bytes on all 27 ({S}/twins_alone_r8.out); expected blocks equal output (run_labs, run_labs_M2.out)")
add("e2-page-smoke-project", "PASS", f"`tools/page_smoke.py --unit M2 --pages project.html` -> 'page_smoke M2: PASS' ({S}/page_smoke_project_v8e.out)")
add("e2-pytest-local-and-count", "PASS", f"from a scratch copy of test_project.py, instance.py and reference.py (as sensitivity_engine.py): `pytest --collect-only` -> '87 tests collected' ({S}/pytest_collect.out); `QF_SEED` 0, 7, 49 with `--assert=plain -W error` -> '87 passed' each ({S}/pytest_seed{{0,7,49}}.out); page states 87 ({S}/../project.html line 211)")
add("e2-ruff", "PASS", f"`ruff check` (grader, tests/labs/M2) -> 'All checks passed!' ({S}/ruff_check_v8e.out); `ruff format --check` -> '31 files already formatted' ({S}/ruff_format.out)")
add("e2-mypy-labs", "PASS", f"`mypy --no-incremental tests/labs/M2` -> 'Success: no issues found in 27 source files' ({S}/mypy_labs.out)")
add("e2-mypy-grader-command", "PASS", f"plans/M2-build-plan.md section 8 command (strict mypy on test_project.py, instance.py, sensitivity_engine.py copies) -> 'Success: no issues found in 3 source files' ({S}/mypy_grader.out)")
add("e2-pytest-labs-tests", "PASS", f"`pytest -q tests/test_labs.py tests/test_run_labs.py -k M2` -> rc=0 ({S}/pytest_labs_M2.out)")
add("e2-verify-refs", "PASS", f"`tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems' ({S}/verify_refs_offline_v8e.out); project.html data-cite keys spivak2008calculus and hubbard2015vector are present in references/references.json (checked by JSON load)")
add("e2-hours-arithmetic", "PASS", "project.html time budget rows 4+6+22+6+14+8 = 60 (lines 239-245); data-hours-project=60 (line 33); index.html data-hours-lessons=240 and data-hours-project=60, 240+60=300 (index.html line 29, 31); 24 lessons x 10 hours = 240 (index.html line 142)")
add("e2-project-lab1-numbers", "PASS", f"Lab 1 prose (project.html lines 57, 116) recomputed in exact Fractions ({S}/project_numbers_r8.out): unrounded 1081108.957794 -> 1081108.96, rounds to 1081109; dP/dy -8514667.395286 -> -8514667.40; d2 83766485.119195 -> 83766485.12; -P'/P 7.875864 -> 7.88; central-difference differences 1.56e-2/8514667.40 = 1.8e-9 and 8.36/83766485.12 = 1.0e-7 (run_labs expected block, project.html line 107-115)")
add("e2-project-lab2-numbers", "PASS", "Lab 2 prose (project.html line 121, 195) vs expected block lines 191-194: second difference 8.400000, difference 5.11e-08 (< 1e-7); AD 3.760000, difference 4.44e-16 (< 1e-15); analytic 8.4 = 6+3x0 at x0=0.8 and 3.76 = -2+4.8+0.96 checked by hand; run_labs 3/3")
add("e2-project-lab3-numbers", "PASS", f"Lab 3 prose (project.html lines 270, 377, 454, 470) vs expected block lines 350-376 and exact values ({S}/project_numbers_r8.out): unrounded 2721581.2909 -> rounded 2721581; dP/dy -23407826.805475; smallest central error 7.111207e-04 at 1e-6; observed orders 0.984 and 2.000; forward error falls ~10x per decade 1e-3..1e-6 (1.297200e5/1.302113e4 = 9.96, 1.302113e4/1.302606e3 = 9.996); kink +1/-1/0 at 1e-3; central error larger than minimum at every printed step below 1e-6")
add("e2-project-exemplar-numbers", "PASS", "Exemplar A (project.html lines 418, 429, 454) and Exemplar B (lines 470, 481, 494, 507, 518) numbers recomputed: price 2721581 and 2721581.2909; 7.111207e-04 at 1e-6; 2.329569e-02 at 1e-7 and 5.004462e+02 at 1e-12 (Lab 3 expected lines 359-365); 1/(2h)=5e11 at 1e-12; float spacing 2^-31 = 4.66e-10 near 2.7e6 and 2^-26 = 1.49e-8 near 1e8 (computed); 7.111e-4/23407826.8 = 3.0e-11; Exemplar B 'central error 1.33e-01 at 1e-8, 5.32e-05 at 1e-4, 8.78e-01 at 1e-12' match expected block line 374-376. Exemplar A 'central below forward at each of 12 steps' verified against Lab 3 lines 354-365.")
add("e2-project-spec-signatures", "PASS", "project.html Rung 3 function list (line 207) vs grader/starter.py lines 17-37 and grader/reference.py: fd_derivative(f,x,h,scheme), ad_derivative(f,x), hessian_fd(f,x,h), bond_price_cents(instance)->int, sensitivities(instance) keys dprice_dy, d2price_dy2, duration_analytic, convexity_analytic; instance dict keys face_cents, coupon_bps, maturity_years, yield_bps match instance.py lines 79-86; 'backward quotient is fd_derivative(f, x-h, h, \"forward\")' checked algebraically")
add("e2-project-tolerances-conventions", "PASS", f"every tolerance in project.html lines 226 matched to test_project.py (lines 171-175 1e-6; 199-217 1e-9/1e-6; 230-238 ratio >=3.8; 505 1e-5; 517 1e-6; 612 1e-9 + 1e-12/h^2; 711 1e-6; 724 1e-4; 735-739 1e-9; 837-842 1e-9 at yield -0.99). sin ratio over seeds 0-49 and their second instances recomputed ({S}/sin_ratio_v8e_r8.py -> min 3.9999842, max 3.9999851 at 7 dp, matching line 226). Conventions formulas (lines 217-223) equal reference.py lines 114-157 and the Hessian formula equal reference.py lines 98-110.")
add("e2-project-rubric-calibration", "FAIL", "project.html Exemplar B (line 464 data-scores '4,4,2,3,4'; line 466 'C5 4'; annotation line 522 'Meets C5 level 4'): the rubric's C5 level 4 (line 404) requires the note to state which price each derivative AND EACH RATIO is computed from. The Exemplar B Units passage (line 518) states the basis for the derivatives only; the duration (a ratio) is stated in years with no price basis. Under the scoring rule (line 392) C5 is 3, not 4.", fix="Add to the Exemplar B Units passage (project.html line 518) that the duration is computed from the unrounded price, keeping C5 = 4; or change C5 to 3 in data-scores (line 464), the verdict (line 466) and the annotation (line 522).")
add("e2-project-rubric-observable", "PASS", "project.html rubric table lines 396-406: each level names an observable element (sweep over at least five decades, named case with sweep rows, tolerance shown, derivation of orders, unit form) and the Exemplar annotations (lines 422-523) name the same elements")
add("e2-project-adversarial-atlas-studio", "PASS", "project.html ladder line 42 ('placement bar ... and answered both of its skill checks') matches index.html line 71 ('you must reach the bar and answer both skill checks') and line 173; the rung list lines 44-47 is unchanged; no studio content on this page")
add("e2-project-notation", "PASS", f"notation/notation.json registers 8 symbols and 26 macros (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{{e\\ast}}, R_f, \\mathbb{{Q}}, \\R, \\E, \\se, \\emgamma ...). project.html math (scanned in {S}-independent python: single letters P,y,t,f,x,h,a,b,F,c,H,C,i,j,p,d; commands \\times \\dot \\sum \\tfrac \\sin \\xi \\pm \\mathrm{{i}} \\ge) uses no registered symbol with another meaning. New \\mathrm{{i}} (line 230) is the imaginary unit, defined in the same sentence; index i (Hessian, line 223) is local.")
add("e2-banned-phrases", "PASS", "BUILDER_RULES §1.3-1.4 banned list (tools/check_pages.py lines 58-74) scanned over project.html visible prose (script tags, pre blocks removed) and all 394 cards front/back: 0 hits in project.html; 12 hits in cards are 'fixed'/'round'/'for fixed t' used as mathematics (M2-c239, c246, c302, c307, c329, c365, c368, c375, c382, c387, c394)")
add("e2-scope-words", "PASS", "scope words (only, all, always, every, any, same, drives, exactly, never, each) in project.html prose and in cards L14, L17, L22, L23, L24: each universal statement checked against a computation or stated hypothesis: 'smallest at 1e-6 and larger at every other printed step' (Lab 3 output lines 359-366), 'central more accurate than forward at every printed step' (lines 354-365), 'every step h>0 forward = +1' (Theorem 2.1), 'Proposition 3.3 holds for every shift' (lemma), 'only in the four axis directions' card M2-c257 (not in the changed set)")
add("e2-project-data-simulated", "PASS", "project.html lines 53, 57, 205, 270-272 and the Lab 1 and Lab 3 twin docstrings carry SIMULATED; grader/instance.py docstring line 1 and 19 says SIMULATED; L22 Lab 1 and L23/L24 labs are labelled SIMULATED in their docstrings; Lab 2 uses a test cubic, not data")
add("e2-project-process-words", "PASS", "project.html, cards.json (394 front/back) and grader/*.py messages scanned for verifier/builder/round/ledger/fragment/agent/slice/mutant/draft/workflow/Claude/Haiku: 0 hits in learner text; 'Stated before running' is lab pedagogy, not a process word")
add("e2-grader-instances", "PASS", f"`tools/run_graders.py --unit M2` (seeds 0-49, instance.py unchanged since 9373ef39): instance draws valid in all 50 seeds ({S}/run_graders_M2.out); round-8 alt runs use both instances per seed (run_alts_r8.py)")
add("e2-grader-instance-claims", "PASS", "instance.py docstring lines 5-17 vs make_instance lines 59-73: face 1000000..50000000 (10,000.00 to 500,000.00) line 59; coupon 0..1000 bps (0.00-10.00 %) line 60; years 1..30 line 61; yield 100..1500 bps (1.00-15.00 %) line 62; cubic rejection |second derivative| >= 1 and |p3| >= 0.1 (lines 49-52); half-cent margin 1e-6 (line 28)")
add("e2-grader-reference", "PASS", f"`run_graders --unit M2` reference 50/50 seeds ({S}/run_graders_M2.out); reference.py read in full (157 lines) against project.html conventions")
add("e2-grader-alternatives", "PASS", f"{S}/alts_r8_all.out: round-8 alternatives alt_r8_a (Richardson central, backward recursion), alt_r8_b (complex-step AD, Fraction price), alt_r8_c (NumPy sums, np.round) each 50/50; round-7 alt_r7_a/b, round-6 alt_r6_a/b, round-5 alt_r5_a/b each 50/50. Runner validated: it rejects v8e_02 with 0/50")
add("e2-grader-messages", "PASS", "test_project.py read in full (884 lines): require()/must_raise() messages each name the property and a hint (e.g. lines 174-175, 194-196, 401, 422, 512-519), none prints an expected number")
add("e2-grader-valueerror-scope", "PASS", "must_raise call sites (test_project.py lines 241-300, 370-389, 540-576, 762-798) cover only the three conditions the page names: step <= 0 (zero, negative zero, -1e-300, NaN, -inf), scheme outside forward/central, yield <= -1; the other tests use must_accept or no exception")
add("e2-grader-no-print", "PASS", "test_project.py autouse fixture lines 51-58 captures output and fails on any print; test_module_prints_nothing_and_warns_nothing (851-884) runs the five named functions and asserts no output and no warnings; instance.py and reference.py have no print or warn call")
add("e2-mutants-existing", "PASS", f"`tools/mutate_graders.py --unit M2` ({S}/mutate_M2_r8_v8e06.out): all 155 pre-existing mutants killed; the only survivor in the run is the new v8e_05 (row e8-ad-float-return-contract)")
add("e2-mutants-written", "PASS", "ledgers/M2/mutants/r3_01..r3_04 killed in the round-8 run (mutate_M2_r8_with_new.out)")
add("e2-mut-v2-01", "PASS", "round-2 survivor dprice_dy numerical mutant: killed in round-8 run (mutate_M2_r8_with_new.out)")
add("e2-mut-v2-02", "PASS", "round-2 survivor d2price_dy2 numerical mutant: killed in round-8 run")
add("e2-mut-v2-03", "PASS", "round-2 survivor forward step floored at 1e-8: killed in round-8 run")
add("e4-mutants-new-r4", "PASS", "round-4 mutants killed in round-8 run (mutate_M2_r8_with_new.out)")
add("e2-cards-count", "PASS", "cards.json: 394 cards (json load); per lesson L01 16, L02 13, L03 14, L04 11, L05 13, L06 14, L07 23, L08 20, L09 18, L10 15, L11 16, L12 17, L13 23, L14 20, L15 19, L16 11, L17 15, L18 16, L19 13, L20 14, L21 16, L22 15, L23 24, L24 18 (sum 394). Per-card comparison with 9373ef39: only M2-c399 and M2-c400 differ")
add("e2-cards-dup-ids-fronts", "PASS", f"394 unique ids; 0 duplicate fronts; 0 duplicate backs ({S}/cards_mech_r8.out)")
add("e2-cards-numbers", "PASS", f"mechanical scan ({S}/cards_mech_r8.py -> cards_mech_r8.out): 83 labelled references (Section N, Misconception N, Definition/Prop/Theorem/Lab N) are not literal text in their lesson; manual check shows these are section-heading numbers and quoted misconception paragraphs (e.g. L24 has 3 quoted misconceptions, cards c371-c373 map to them; L14 'Section 3' = heading '3 Forward mode computes the derivative'). For L14, L17, L22, L23, L24 every cited label was located by reading (e.g. L14 Definition 2.1, Proposition 3.1, Example 4.1, Lab 1, Proposition 5.2; L17 Example 1.2, Example 2.3, Lab 1, Problems E2 and R1; L23 Theorem 3.1, Propositions 2.1-3.3; L24 Definition 4.1, Proposition 4.2-4.3, Remark 4.4)")
add("e2-cards-locators", "PASS", f"every card's lesson page exists: 24 pages L01-L24 ({S}/cards_mech_r8.out)")
add("e2-cards-grades", "PASS", "grade values in cards.json are only C, T or absent; changed cards c399, c400 carry no grade (unchanged); L22-L24 grades checked against each lesson's Key results table (L23 Prop 2.1, 2.2, 3.1-3.3 T; Lab 1 entries C; L24 Theorems 2.1, Props 3.1-4.3 T; Lab entries C)")
for n in range(1, 22):
    lid = f"L{n:02d}"
    if lid in CARD_LESSONS_CARRIED:
        ev[f"e2-cards-{lid}"] = ("PASS", CARRY + f" the cards of {lid} (per-card equality with 9373ef39 checked in Python: only M2-c399 and M2-c400 differ in the whole file) and {lid}.html", None)
for lid in ("L14", "L17"):
    pass
add("e2-cards-L14", "PASS", "cards M2-c399 (changed back) re-verified against L14.html: the lesson text (Assumption 1 paragraph; statement 'The exponential and sine rules of Definition 2.1 and the statement of Proposition 3.1 assume them, and the closed forms in Example 4.1, Lab 1 and Proposition 5.2 use them'); Lab 1 code uses math.exp and math.sin (L14.html lab-M2-L14-1). Other L14 cards carried: per-card equality with 9373ef39")
add("e2-cards-L17", "PASS", "cards M2-c400 (changed back) re-verified against L17.html Assumption 1 paragraph: 'Example 1.2, Example 2.3, the Lab 1 hypothesis, Problem E2 and Problem R1 use them'; Lab 1 hypothesis uses cos(y) in the gradient. Other L17 cards carried: per-card equality with 9373ef39")
add("e2-cards-L22", "PASS", "re-read all 15 L22 cards (c323-c337, c404) against the current L22.html text (Definition 1.1, Lemma 1.2, Theorem 1.3, Remark 1.4, Example 1.5, Lab 1 Part A/B output lines 142-149, Example 2.2, Proposition 2.1, Example 2.3, Misconceptions 1-3, Problems M1-M3, P1-P2, E1-E3, R1-R3, Assumption 1.1, Lab 1 misstatements none); the cross-lesson citations (Theorem 1.3 of L21 with its Assumption 1.2 IVT; Assumption 2.1 of L06 = extreme value theorem) checked in L21.html and L06.html")
add("e2-cards-L23", "PASS", "re-read all 24 L23 cards against L23.html (Definition 1.1, Prop 2.1, 2.2, Lab 1 output lines 136-145 for 108110.895779, 108111, 117060, -851466.739529, 8376648.511919, 4.037716e+02, -1.506081e+01, ratios 3.9279/3.9634 and 7.8807/7.9396, 100000 at 0.05; Theorem 3.1, Props 3.2, 3.3, Remark 3.4, Misconceptions 1-3, section 4 rounding); E3 offset 2.78e-18 and P'(0.05)=-7.72e5 verified ({S}/l23_e3_check_r8.out)")
add("e2-cards-L24", "PASS", f"re-read all 18 L24 cards (c358-c375 set, c387, c405, c410) against L24.html: Theorem 2.1 quotients 1/-1/0; Props 3.1-3.2; Definition 4.1; Props 4.2-4.3 minimizers h*=2sqrt(delta/M2), (3delta/M3)^(1/3); Remark 4.4 values -6.603e-9 signed and +1.359e-8 exact at 1e-8 (recomputed: -6.6028e-09); lab values 1.406e-01, 1.359e-05, 3.263e-05, 3.903e-01 (lab output lines 132-146); c370 minimizers 1.8e-8 and 6.3e-6 recomputed; Misconceptions 1-3; Assumption 4.1. Count is 18 (the round-7 row text said 17).")
add("e2-cards-L19-L21-untouched-proof", "PASS", "L19, L20, L21 cards: per-card equality with 9373ef39 (only c399 and c400 differ in the file); L19.html, L20.html, L21.html byte-identical since 9373ef39")
add("e3-cards-whole-set-mechanical", "PASS", f"whole-set rerun ({S}/cards_mech_r8.out): 394 unique ids, 0 duplicate fronts or backs, 24 lesson pages exist, grades in {{C,T,absent}}; per-card diff with 9373ef39 = {{M2-c399, M2-c400}} only")
add("e5-alternatives", "PASS", f"{S}/alts_r8_all.out: the six alternatives of rounds 5-7 pass 50/50 seeds on the pinned grader (the three round-8 alternatives are in e2-grader-alternatives)")
add("e5-mutants-new-r5", "PASS", "ledgers/M2/mutants/r5_01..r5_04 killed in the round-8 run (mutate_M2_r8_with_new.out)")
add("e5-twins-alone", "PASS", f"27 twins alone under python -I -W error: rc=0 and empty stderr ({S}/twins_alone_r8.out)")
add("e5-fragment-gate-set", "PASS", "gates run this round: check_pages, check_dag, check_projects, run_graders, run_labs (27/27), page_smoke project, pytest collect and seeds 0/7/49, ruff check and format, mypy labs and grader command, pytest labs, verify_refs --offline, mutate_graders (160 of 161 killed, the survivor is a FAIL row)")
add("e6-card-M2-c349", "PASS", "M2-c349 (Proposition 3.2) hypotheses 'y0 > -1' and EVT assumption, and the sign statement, match L23.html Proposition 3.2 (line 153 of the clean text) and its proof (P''' < 0)")
add("e6-card-M2-c350", "PASS", "M2-c350 (Proposition 3.3) hypotheses 'y0 > -1' and EVT assumption, and the result, match L23.html Proposition 3.3 (line 157) and proof (line 159)")
add("e6-card-M2-c363-c365", "PASS", "M2-c363 (Proposition 4.2), c364 (Proposition 4.3), c365 (Remark 4.4) re-read against L24.html lines 47-56: hypotheses M2>0, H, Definition 4.1, the bound functions and the minimizers match; the Remark's statement 'Truncation and round-off errors can have opposite signs' with the Lab 1 Part B value at 1e-8 matches")
add("e6-card-M2-c404-c405", "PASS", "M2-c404 (L22 Assumption 1.1, d/da ln a = 1/a, used by Example 1.5) matches L22.html line 42; M2-c405 (L24 Assumption 4.1) matches L24.html line 57")
add("e6-card-M2-c408-c409", "PASS", "M2-c408 (L08) and M2-c409 (L16) cards carried: cards.json entries unchanged since 9373ef39 and L08.html, L16.html byte-identical since 9373ef39 (git diff --stat 9373ef39 HEAD over course/modules/M/M2 lists neither)")
add("e6-instances-50", "PASS", f"instance.py unchanged since 9373ef39; run_graders seeds 0-49 pass ({S}/run_graders_M2.out) and the 50-seed alternative runs build both instances per seed")
add("e6-mutants-new-v6e", "PASS", "ledgers/M2/mutants/v6e_01..v6e_04 killed in the round-8 run (mutate_M2_r8_with_new.out)")
add("e6-L24-E3-unrounded-difference", "PASS", f"round-7 FAIL fixed. L24.html line 348 now says 4.4e-16 with the note that the two six-digit values differ by 4.5e-16 only because each is rounded. Recomputed in float: unrounded central errors 5.85869130986793607e-11 (h=1e-5) and 5.85873571878892108e-11 (h=1e-7), difference 4.44e-16 ({S}/l24_e3_unrounded_r8.out); the lab picks 1e-5 as the smaller value")
add("e7-L22-L24-lesson-numbers", "PASS", f"changed L22 hunks (lines 41, 150: x-hat errors between 1e-8 and 2e-8, largest 2e-8 at a=4 (run output 2.99999998), 3e-17 change in the objective) and L24 E3 hunk recomputed; L22 Part B 'within 5.4e-12' = largest printed error (output line 149); L24 Remark 4.4 values recomputed ({S}/l24_e3_unrounded_r8.out and python check in this round)")
add("e7-round7-mutants-v7e", "PASS", "ledgers/M2/mutants/v7e_01..v7e_04 killed in the round-8 run (mutate_M2_r8_with_new.out)")
add("e7-alternatives-new", "PASS", "round-7 new alternatives alt_r7_a_decimal_price_fsum_richardson.py and alt_r7_b_complex_step_ad_horner_fsum.py: 50/50 each (alts_r8_all.out)")
add("e7-twins-27-alone", "PASS", "27 twins alone under python -I -W error (twins_alone_r8.out)")

rows = []
for r in prev["rows"]:
    i = r["id"]
    status, evidence, fix = ev[i]  # every round-7 id is re-decided this round
    row = {"id": i, "check": r["check"], "location": r["location"], "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix
    rows.append(row)
new_rows = [
    {"id": "e8-ad-float-return-contract", "check": "ad_derivative returns a float (page: 'ad_derivative(f, x), returning a float', project.html line 207); the suite must refuse a return of the int 0",
     "location": "course/modules/M/M2/grader/test_project.py lines 395-413 and 473-479 (test_constant_function_has_zero_derivative uses value == 0.0, which an int 0 passes); mutant ledgers/M2/mutants/v8e_05_ad_zero_derivative_returns_int.py",
     "status": "FAIL",
     "evidence": f"`tools/mutate_graders.py --unit M2` ({S}/mutate_M2_r8_v8e05.out): 'SURVIVED v8e_05_ad_zero_derivative_returns_int.py ... -> None'. The mutant returns int 0 for a zero derivative and the float otherwise; no test isinstance-checks ad_derivative's return. Contract violated: project.html line 207 'ad_derivative(f, x), returning a float'.",
     "fix": "In test_constant_function_has_zero_derivative and test_forward_mode_matches_the_analytic_derivative add require(type(value) is float, 'ad_derivative must return a float (hint: Lesson 14, forward mode returns the derivative as a float)'). Then rerun mutate_graders: v8e_05 must be killed."},
]
rows += new_rows

mutants = []
for n, desc, killed in [
    ("v8e_01_yield_at_minus_one_passes_the_check.py", "yield check uses < instead of <=; exactly -1 divides by zero", "test_yield_at_minus_one_raises_for_price_and_sensitivities (seed 0)"),
    ("v8e_02_price_nudged_up_before_rounding.py", "price adds 1e-9 before round(): exact half cent goes up", "test_exact_halves_round_to_the_even_cent (seed 0)"),
    ("v8e_03_duration_divides_by_the_rounded_price.py", "duration divides by round(price) not the unrounded price", "test_named_ratios_are_the_stated_formulas[inst0] (seed 0)"),
    ("v8e_04_second_derivative_uses_t_times_t_minus_one.py", "d2price_dy2 weights by t(t-1) instead of t(t+1)", "test_second_derivative_matches_the_central_difference_of_the_price[inst0] (seed 0)"),
    ("v8e_05_ad_zero_derivative_returns_int.py", "ad_derivative returns int 0 for a zero derivative (contract: float)", "NONE: survived all 87 tests on the mutate_graders default seed window (see row e8-ad-float-return-contract)"),
    ("v8e_06_fd_forward_zero_numerator_returns_int.py", "fd_derivative forward returns int 0 when f(x+h) == f(x)", "killed in the round-8 run (mutate_M2_r8_v8e06.out)"),
]:
    mutants.append({"name": n, "description": desc, "killed_by": killed})

notes = [
    "Round 8, slice e (project.html, grader/*, project labs, all 394 M2 cards, grader mutants, alternative engines), pin 2d755599. Delta from the round-7 pin 9373ef39 read in full: course/modules/M/M2/L22.html (Example 1.5 and Lab 1 interpretation paragraphs), L24.html (E3 solution), cards.json (only M2-c399 and M2-c400 differ per card), project.html (ladder line 42, conventions-check line 230). The grader, labs, mutants and alternatives are byte-identical to 9373ef39 except the new mutants and scripts added in this round.",
    "Round-7 FAIL e6-L24-E3-unrounded-difference is fixed and re-verified PASS. Round-7 rows whose subjects changed were re-verified from scratch: the cards (L14, L17, L22, L23, L24 and the whole-set mechanical rows), project.html rows (ladder, conventions, scope words, banned phrases, notation, rubric), and the L22 and L24 lesson-number rows. Carried rows (per-card equality with 9373ef39) are marked 'Carried from round 7'.",
    "Two FAIL rows: e2-project-rubric-calibration (round-7 PASS row, now FAIL: Exemplar B C5 official 4 needs the duration basis) and new e8-ad-float-return-contract (grader; mutant v8e_05 survives). Both are reported, not fixed (verifier posture).",
    "Correction to the round-7 row text: L24 has 18 cards, not 17 (cards.json, 18 entries with lesson L24).",
    "Hint wording not graded as a finding: the autograder hint 'Lesson 19, the Hessian by second differences' points at L19, which treats the Hessian by central differences of the gradient (L19.html Lab 1) and does not use the phrase 'second differences'. Learner hint text, not a claim of the page.",
    "Notation: plain Q (difference quotient in L04 and partitions in L07-L09 cards) and plain R (remainder, L23) are lesson-local letters, not the registered \\mathbb{Q} or R^\\ast or R_f; not counted as collisions (same convention as round 6-7).",
    "Scratch hygiene: all round-8 outputs are in ledgers/M2/scripts/M2-e-r8/ and the verifier-written mutants and alternatives are in ledgers/M2/mutants/ (v8e_01..v8e_06) and ledgers/M2/scripts/M2-e-r8/alts_r8/. The existing file ledgers/M2/scripts/M2-e-r7/page_smoke_project.out was not used as evidence.",
    "Not checked: live verify_refs (only --offline; no reference changed); the in-browser Pyodide runtime (only the page_smoke harness and the plain pytest run in a scratch copy); the --assert=plain output claim on page line 261 (not run); the cards of L01-L13, L15-L16, L18, L20-L21 were not re-read (carried by per-card equality with 9373ef39, which is byte-identical); the exact rational value of the sin ratio over seeds (checked with the float quotient the test uses, which reproduces the page's 7-decimal range); lab page code of L22-L24 is outside this slice (covered by run_labs 27/27).",
]
frag = {
    "unit": "M2", "slice": "e", "round": 8, "verifier": "Haiku 5.5 independent verifier (round 8, slice e)",
    "pin": "2d755599d8d74df292e3e43025f0458c4053802e", "base": "9373ef398589097500ea849e30ff9da423b98943",
    "checkout": str(ROOT), "scratch": "/tmp/m2e-r8-* (scratch copies only: alts, twins, text extracts, grader copies)",
    "verified_at": "2026-11-04", "verdict": "FAIL",
    "rows": rows, "mutants": mutants, "registry_flags": [], "freshness_flags": [], "notes": notes,
    "summary": "Slice e round 8: FAIL on two rows. The round-7 FAIL (e6-L24-E3-unrounded-difference) is fixed and PASS. FAIL e2-project-rubric-calibration: Exemplar B's official C5 4 requires the duration basis, which the note does not state (rubric line 404). New FAIL e8-ad-float-return-contract: grader mutant v8e_05 (ad_derivative returns int 0) survives all tests, and the page states ad_derivative returns a float. All other rows PASS: gates re-run, 87 tests at seeds 0/7/49, 160/161 existing and new grader mutants killed, 9 alternative engines 50/50 each, all 22 M2 cards for L14/L17/L22-L24 re-read, 394 cards mechanically compared with the round-7 pin.",
}
OUT.write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", len(rows), "FAIL", sum(r["status"] == "FAIL" for r in rows), "mutants", len(mutants))
