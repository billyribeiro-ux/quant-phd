"""Build the round-1 closing-delta fragment for M2 slice e (pin 95f3f8cb, base fragment round 11 pin ccaeeaf4).

Every PASS row cites a command output or a diff/grep produced in ledgers/M2/scripts/M2-e-r1/ or in the scratch
directories named in the notes. Carried rows keep their base id and carry the required prefix.
"""

import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

CHECKOUT = Path("/Users/billyribeiro/.fanout/wt/verifyF21-M2-e")
S = CHECKOUT / "ledgers/M2/scripts/M2-e-r1"
BASE = Path("/Users/billyribeiro/.fanout/frags/D-M2-e.round11.json")
OUT = CHECKOUT / "ledgers/M2/M2-e.json"

base = json.loads(BASE.read_text(encoding="utf-8"))
base_rows = {r["id"]: r for r in base["rows"]}

CARRY = "Carried from round 11 ({files} byte-identical since the previous pin ccaeeaf4): "


def carry(files: str, row_id: str) -> str:
    return CARRY.format(files=files) + base_rows[row_id]["evidence"]


R = {}  # id -> (status, evidence, fix)


def ok(row_id: str, evidence: str) -> None:
    R[row_id] = ("PASS", evidence, None)


def car(row_id: str, files: str) -> None:
    R[row_id] = ("PASS", carry(files, row_id), None)


PROJ = "course/modules/M/M2/project.html (its only changed line is the Lab 2 hypothesis)"
GRADER = "course/modules/M/M2/grader/test_project.py"

# --- gates and project page -------------------------------------------------------------------------------------
ok("e2-check-pages", "check_pages.py --unit M2 -> 'check_pages M2: PASS', exit 0 (r1_check_pages.out); covers "
   "banned strings and cards.json ids, lesson, grade and keys over 398 cards.")
ok("e2-check-dag", "check_dag.py --unit M2 -> 'check_dag M2: PASS', exit 0 (r1_check_dag.out).")
ok("e2-check-projects", "check_projects.py --unit M2 -> 'check_projects M2: PASS', exit 0 (r1_check_projects.out); "
   "re-run because project.html changed (Lab 2 hypothesis line).")
ok("e2-run-graders", "run_graders.py --unit M2 --seeds 0-49 -> 'reference 50/50 seeds, slowest 0.2 s', exit 0 "
   "(r1_run_graders.out).")
ok("e2-run-labs-project", "run_labs.py --unit M2 -> 'run_labs M2: PASS (27/27)', exit 0 (r1_run_labs_M2.out); the three "
   "project labs are among the 27.")
ok("e2-lab-page-code-equals-twin", "run_labs.py --unit M2 (r1_run_labs_M2.out) asserts each lab's page code is "
   "byte-identical to tests/labs/M2 twin for all 27 labs, including project 1-3; the changed page line is prose, not code.")
ok("e2-lab-twin-clean-and-expected", "All 27 twins run alone with 'python -I -W error' in empty scratch dirs: exit 0, "
   "stderr 0 bytes for each (/tmp/m2e_r1_twins/index.txt). run_labs expected-block check PASS (r1_run_labs_M2.out). "
   "Changed twins L06, L07, L13, L14 re-run and their printed values checked against cards.")
ok("e2-page-smoke-project", "page_smoke.py --unit M2 --pages modules/M/M2/project.html -> 'page_smoke M2: PASS', exit 0 "
   "(r1_page_smoke_project.out).")
ok("e2-pytest-local-and-count", "Grader collect-only in a scratch copy (test_project.py, instance.py, reference.py as "
   "sensitivity_engine.py): '89 tests collected' (r1_grader_collect.out), equal to the page's '89 tests' (project.html:211). "
   "QF_SEED 0-3, -W error: 89 passed each (r1_grader_pytest_seed0.out, scratch runs).")
ok("e2-ruff", "ruff check tests/labs/M2 course/modules/M/M2/grader: 'All checks passed!' (r1_ruff_labs.out); ruff format "
   "--check: '31 files already formatted' (r1_ruff_format.out).")
ok("e2-mypy-labs", "mypy tests/labs/M2 --no-incremental: 'Success: no issues found in 27 source files' (r1_mypy_labs.out).")
ok("e2-mypy-grader-command", "Plan section 8 grader command (mypy --strict --no-incremental on scratch copies): "
   "'Success: no issues found in 3 source files' (r1_mypy_grader_strict.out).")
ok("e2-pytest-labs-tests", "pytest -q tests/test_labs.py tests/test_run_labs.py -k M2: 27 passed, exit 0 (r1_pytest_labs.out).")
ok("e2-verify-refs", "verify_refs.py --offline: '560 entries, 0 problems', exit 0 (r1_verify_refs_offline.out). "
   "references.json changed in one entry only (black1973pricing: used_by gains FC2, generated_at); no M2 page cites it "
   "(grep of course/modules/M/M2 = 0 hits). Live re-resolution of M2 entries: " +
   CARRY.format(files="the M2-cited registry entries") + base_rows["e2-verify-refs"]["evidence"] +
   " (live run not repeated this round).")
ok("e2-hours-arithmetic", "index.html hub: '240 h lessons · 60 h project (20%)'; the 24 lesson cards each read '10 h' "
   "(grep), 24 x 10 = 240; project time budget sums to the declared 60 h (check_projects PASS). index.html changed only in "
   "the placement quiz and the L21 card blurb; no hour figure changed.")
car("e2-project-lab1-numbers", PROJ + " Lab 1 section")
ok("e2-project-lab2-numbers", "Lab 2 hypothesis (changed). Test cubic 1 - 2x + 3x^2 + 0.5x^3 (tests/labs/M2/"
   "lab-M2-project-2.py docstring and cubic()). Printed: second difference 8.400000 vs analytic 8.4, |diff| 5.11e-08 "
   "(< 1e-7, claim holds); AD derivative 3.760000 vs analytic 3.76, |diff| 4.44e-16 (< 1e-15, claim holds) "
   "(scratch run, /tmp/m2e_r1_lab2). Analytic values re-derived: f''(0.8) = 6 + 3(0.8) = 8.4; f'(0.8) = -2 + 6(0.8) + "
   "1.5(0.8)^2 = 3.76. Prose 'Lesson 13 writes them and subtracts them for the first difference' matches L13 Section 2 "
   "(the two expansions and their symmetric pair, L13.html).")
car("e2-project-lab3-numbers", PROJ + " Lab 3 section")
car("e2-project-exemplar-numbers", PROJ + " Exemplars A and B")
car("e2-project-spec-signatures", PROJ + " Rung 3, grader/starter.py, grader/reference.py")
car("e2-project-tolerances-conventions", PROJ + " Conventions and Tolerances, " + GRADER)
car("e2-project-rubric-calibration", PROJ + " rubric table and Exemplars; no M2 blind scoring file exists in "
    "~/.fanout/blind/ (BK4, CS2, E1, E3, E4, FC2, LX1, M5, PC3 only), so the base calibration rows are carried")
car("e2-project-rubric-observable", PROJ + " rubric table")
car("e2-project-adversarial-atlas-studio", PROJ + " adversarial question bank and atlas/studio sections")
ok("e2-project-notation", "Changed hunk (Lab 2 hypothesis) uses f, x, h, a, x_0 and the dot part of a dual number; "
   "notation/notation.json registers 8 symbols (T, Phi, gamma_3, ...), none used with a different meaning in the hunk. "
   "Changed cards use K as the tail index (c008, c390); K and M appear in no notation entry (notation.json read in full).")
ok("e2-banned-phrases", "banned_and_process_scan (r1_banned_process_scan.out): no BANNED hit in cards.json, project.html, "
   "grader/test_project.py or grader/instance.py.")
ok("e2-scope-words", "Changed cards with scope words checked against lesson text: c064 ('every result that uses it begins "
   "Assuming Assumption 2.1': Theorems 2.2 and 2.3 and Corollary 3.1 of L06.html each begin so), c161 (always/only: "
   "L11 line 277 and 293), c263 (all: L17 Section 4), c425 (only: L09 lines 124, 328), c422 (exactly: lab asserts "
   "equality, lab-M2-L07-1.py). The project.html changed hunk has no scope word (git diff grep).")
ok("e2-project-data-simulated", "Lab 2 uses a test cubic described as 'a test function and not a bond' (twin docstring); "
   "no market-data claim in the changed hunk; SIMULATED labels of Labs 1 and 3 unchanged.")
ok("e2-project-process-words", "Process-word scan (r1_banned_process_scan.out): only 'round' as a verb in test messages "
   "('round to the nearest cent'); no process word in cards.json or project.html.")
ok("e2-grader-instances", "run_graders.py: instance.py deterministic and varying across seeds, 50/50 seeds PASS "
   "(r1_run_graders.out).")
car("e2-grader-instance-claims", "course/modules/M/M2/grader/instance.py")
ok("e2-grader-reference", "run_graders.py: reference passes 50/50 seeds (r1_run_graders.out); grader pytest QF_SEED 0-3: "
   "89 passed each.")
ok("e2-grader-alternatives", "run_alternatives (r1_alternatives.out): 24 of 24 alternative implementations pass seeds 0-49 "
   "(ledgers/M2/scripts/M2-e-r3/alts, M2-e-r5 .. M2-e-r11 alts dirs).")
car("e2-grader-messages", GRADER)
car("e2-grader-valueerror-scope", GRADER)
car("e2-grader-no-print", GRADER)
ok("e2-mutants-existing", "mutate_graders.py --unit M2 (r1_mutate_graders_M2.out): 'PASS (175/175 killed)', exit 0. The "
   "set includes w11e_01..04, which are not in the base pin's history (freshness flag).")
ok("e2-mutants-written", "Standing mutant set re-run (r1_mutate_graders_M2.out): every file under ledgers/M2/mutants/ "
   "reported KILLED; no survivor; no equivalent mutant needed.")
ok("e2-mut-v2-01", "v2_01_dprice_dy_is_a_numerical_central_difference.py: KILLED in r1_mutate_graders_M2.out.")
ok("e2-mut-v2-02", "v2_02_d2price_dy2_is_a_numerical_second_difference.py: KILLED in r1_mutate_graders_M2.out.")
ok("e2-mut-v2-03", "v2_03_fd_step_floored_at_one_hundred_millionth.py: KILLED in r1_mutate_graders_M2.out.")
ok("e4-mutants-new-r4", "Round-4 mutants are members of the standing set in ledgers/M2/mutants/ (175 files); every one is "
   "reported KILLED in r1_mutate_graders_M2.out.")
# --- cards -----------------------------------------------------------------------------------------------------
ok("e2-cards-count", "cards.json: 398 cards, ids unique (r1_card_dupes.out). Base count 394 at ccaeeaf4; this delta removes "
   "11 (c048, c129, c144, c160, c208, c397, c399, c400, c401, c405, c409) and adds 15 (c414, c415, c417, c418, c420 to "
   "c430). 394 - 11 + 15 = 398. No M2 page states a card count (grep).")
ok("e2-cards-dup-ids-fronts", "card_dupes_r1: exact duplicate fronts [] and exact duplicate backs []; ids unique. "
   "Semantic duplicates are the separate row e10-cards-c412-duplicates-c065.")
ok("e2-cards-numbers", "card_numbers_r11.py on HEAD (r1_card_numbers.out): 'cards checked: 398 ... with a number absent "
   "from their lesson: 0'.")
ok("e2-cards-locators", "Every cited Theorem, Proposition, Example, Remark, Lemma, Corollary, Problem, Assumption and "
   "Section label of all 398 cards resolves in its lesson text (scan: ledgers/M2/scripts/M2-e-r1/locators_r1.py, output r1_locators.out). The 55 'Misconception N' "
   "labels are the list-order numbering of each lesson's Misconceptions section; for each changed card the list position "
   "was checked against the statement quoted in the lesson.")
ok("e2-cards-grades", "check_pages cards checks PASS (r1_check_pages.out). Changed grades: c013 T->none (a remark about "
   "Definition 2.1), c085 C->T (x^11/(1-x) at x=3/10 from Example 2.4 and Proposition 2.3, 0.3^11/0.7 = 2.5307e-6, "
   "arithmetic checked), c415 C (lab output).")
ok("e2-cards-L01", "Changed cards c002, c006, c008, c009, c010, c013, c390, c391, c424, c426 read against L01.html: "
   "Definition 2.1, Example 2.3 (|a_n-2| = 1/(n+1)), Proposition 3.1 with K, Example 4.1 (c009 contradiction recomputed), "
   "Section 5. Lab 1 output for N = 1000 and error 1.000000e-03 at n = 999 (c006) matches the twin.")
ok("e2-cards-L02", "L02.html changed (prose only). Cards citing Example 2.1, Example 2.3, Corollary 2.2 and Remark 3.1 "
   "(c018, c021, c022, c023) re-read: identity continuous by Example 2.1; Corollary 2.2 applied to the identity gives the "
   "square (Example 2.3). Matches the changed L02 text. Other L02 cards byte-identical.")
ok("e2-cards-L03", "c038 (changed, w(x) = sign function) matches L03.html (h renamed w; one-sided limits -1 and 1; "
   "Proposition 2.2; Misconception 2). c027 (changed) re-read against Definition 1.1. c030, c033 locators resolve.")
ok("e2-cards-L04", "c044 (changed) matches L04 Example 3.1 and Misconception 1 ('a formula does not guarantee'). "
   "c047 numbers: |Q(h)-3| at h = 1e-6 is 3.000001e-6 = 3h + h^2 (checked). c045, c049 locators resolve.")
ok("e2-cards-L05", "c055 (95.0625 = 6 x 1.5 x 3.25^2, checked), c056 (32.062500235, 2.35e-07, lab output), c057 "
   "(29/49 = 0.591837, 3.33e-10, lab output), c058 (95.062500855, 8.55e-07, lab output), c059/c060 (Misconceptions 1, 2), "
   "c379, c393 (Assumption 1.4 text), c427 (f'' and f''' definitions, L05.html) all agree with L05.html.")
ok("e2-cards-L06", "Changed c062, c064, c068, c069, c070, c394, c414 read against L06.html. c068: x^3 strictly increasing "
   "is proved on the page (L06.html line 201, y^2 + xy + x^2 = (x + y/2)^2 + 3y^2/4). c069 and c070: lab output 8 of 16 "
   "and f(-1) = 2, f(1) = -2. c064 scope claim verified (Theorems 2.2, 2.3, Corollary 3.1). c414: critical point defined "
   "in Section 1. Duplicate relation with c065/c066 is recorded in e10-cards-c412-duplicates-c065.")
ok("e2-cards-L07", "Changed c085, c087 read against L07.html (Example 2.4; Lemma 3.1 states 0 <= t < 1, line 319). c086 "
   "(-2048 = -1 - (2^11 - 1), arithmetic checked), c092 (lab part D), c093 (27 checks, lab output), c096, c422 (lab "
   "asserts exact equality, twin lines 70-76).")
ok("e2-cards-L08", "Changed c099 (Theorem 1.2 = Rolle, L08.html line 76), c113 (Remark 3.2, L08.html line 246), c428 "
   "(Assumption 1.1 = Assumption 2.1 of Lesson 6, line 61) read against L08.html; c101-c111 locators resolve. The new "
   "Rolle card c417 and the EVT restatement c428 are recorded under e10-cards-c412-duplicates-c065.")
ok("e2-cards-L09", "c423 (both endpoint sums 1/8, integral 1/6 by a forward reference, Definition 1.3 with sup/inf, "
   "Misconception 2), c425 (Theorem 2.2 and Corollary 2.3 are for monotone f only, line 124) read against L09.html; "
   "c123, c125-c127 locators and lab numbers unchanged.")
ok("e2-cards-L10", "Changed c135, c137 read against L10.html (continuity of f not a hypothesis; a <= b with the empty-interval "
   "convention), c418 (Theorem 1.2 used in the proof of Theorem 2.1 at line 399 and in Proposition 4.1 at line 288), c421 "
   "(increment defined at line 99), c429 (restates Theorem 2.3 of Lesson 6; duplicate relation recorded under e10 row).")
ok("e2-cards-L11", "Changed c161 (dropping the boundary term forces the integral to 0; it is 1/2, so 1 is needed) read "
   "against L11.html line 293. c150-c155 values re-derived: 1/60, 1/30, 1/2, 8/3 and 3/2 all re-derived. c153 "
   "hypotheses include the integrability of f on [g(a), g(b)] (L11.html, Theorem 3.1 example text). c162 (1/3 for limits "
   "0 and 1).")
ok("e2-cards-L12", "Changed c169 (integrals 1 and 1/2, Example 2.3), c176 (Misconception 2 and Remark 3.4, integrand tends "
   "to 0), c177 (truncation error 1/b, exact) read against L12.html; c170, c171 lab numbers unchanged.")
ok("e2-cards-L13", "Changed c187 (h* = (3 delta/M3)^(1/3); B' = M3/3 h - delta/h^2; h* <= h0 condition; P3), c380 (Assumption "
   "1 users: M3, E1, E2 (uses e), E3, R1, R3, Section 5, Lab 1, checked in L13.html), c381 (2.154e-07, 1.548e-06 lab output) "
   "and c191-c197 (lab ratios 10.03, 100.00, 32.6, 301.1; printed errors) re-checked against the changed twin output.")
ok("e2-cards-L14", "Changed c212 (x.val > 0 else 0 gives tangent 0; >= 0 gives 1; R3 solution at L14.html line 550). "
   "c207 (251 points below 1e-12, lab output), c209 (2.5067615350 by dual numbers and closed form, lab output). "
   "c208 and c399 removed (no claim restated elsewhere; observation).")
ok("e2-cards-L15", "Changed c225 (paragraph after Example 2.4, L15.html line 134), c233 (2/(3 sqrt 3) = 0.3849002 in "
   "Problem E1, value 0.38490018 checked), c234 (f(1/n,1/n) = 1/(2n), Problem E3, arithmetic checked), c413 (Section 3 "
   "continuity definition, L15.html line 143), c415 (lab output n=10 and n=10000) read against L15.html and twin output.")
ok("e2-cards-L16", "L16.html changed (one-variable rules sentence). c239-c249 locators resolve and content is unchanged. "
   "c409 removed: the L16 Assumption 1 (derivative of exp) no longer has a card; coverage observation, not a ruling-26 kind.")
ok("e2-cards-L17", "Changed c263 read against L17.html Section 4 (g = xy/(x^2+y^2): partials 0 at the origin, directional "
   "derivatives exist only in the axis directions; line 261 and 288). c259-c261 unchanged; twin output unchanged. c400 removed.")
ok("e2-cards-L18", "c265-c279 locators resolve. c270 (Jacobian [[2,-4],[4,2]], remainder (s1^2 - s2^2, 2 s1 s2) with length "
   "|h|^2 re-derived), c271-c272 (lab output rows 2, -4, 4, 2 and 25 grid points), c277 (Problem R1, Section 5, L18.html "
   "lines 288, 446). c401 removed.")
ok("e2-cards-L19", "Changed c293 read against L19 Misconception 2 and the twin output (f_xy(0.5, 0.25) = 2.148721, printed "
   "by lab-M2-L19-1; closed-form Hessian entries re-derived by hand). c287, c288, c289, c292, c294 lab outputs match.")
car("e2-cards-L20", "course/modules/M/M2/L20.html and its 14 cards")
car("e2-cards-L21", "course/modules/M/M2/L21.html and its 16 cards")
ok("e2-cards-L22", "Changed c330 (V(a) = a^2/4, V' = a/2, x_hat = y* = a/2 at Example 2.2; naive partial at Misconception 1), "
   "c334 (Misconception 2; closed domain at Example 2.3), c404 (assumed derivative of ln, Example 1.5). Lab 1 outputs "
   "for c328 (0.40546511 etc. equal ln a), c329 (max error 5.4e-12) and c336 (x_hat error 1e-8) match.")
car("e2-cards-L23", "course/modules/M/M2/L23.html and its 24 cards")
ok("e2-cards-L24", "Changed and new cards c420 (Assumption 4.1 and the lab's e at x0 = 1, L24.html line 185), c430 (D+, "
   "D0 and the 'both signs of h' sentence, L24.html line 74), c372 (Misconception 2). c405 removed. Unchanged cards "
   "c358-c373 locators resolve.")
ok("e2-cards-L19-L21-untouched-proof", "Row name reflects the base delta. L19 is no longer untouched (c293 changed; "
   "re-verified under e2-cards-L19). L20.html, L21.html and their cards are byte-identical since ccaeeaf4 (git diff).")
ok("e3-cards-whole-set-mechanical", "Whole-set mechanical checks on 398 cards: numbers (0 missing), exact duplicates (0), "
   "ids unique, locators resolve, grades valid (r1_card_numbers.out, r1_card_dupes.out, r1_check_pages.out). Semantic "
   "duplicates are in e10-cards-c412-duplicates-c065.")
ok("e5-alternatives", "run_alternatives (r1_alternatives.out): 24 of 24 correct implementations pass seeds 0-49.")
ok("e5-mutants-new-r5", "Round-5 mutants in the standing set (r1_mutate_graders_M2.out): all KILLED.")
ok("e5-twins-alone", "27 twins alone under python -I -W error (/tmp/m2e_r1_twins/index.txt): all exit 0, empty stderr.")
ok("e5-fragment-gate-set", "Gate set run this round: check_pages, check_dag, check_projects, run_graders, run_labs, "
   "build_site --check, verify_refs --offline, ruff (check and format), mypy (labs and grader), pytest (labs, grader "
   "collect and seeds), page_smoke (project), mutate_graders, alternatives, render_curriculum --check, fetch_data --check "
   "(r1_*.out in ledgers/M2/scripts/M2-e-r1/).")
ok("e6-card-M2-c349", "M2-c349 and L23.html byte-identical to ccaeeaf4 (cards.json object equal, git diff); the base "
   "PASS stands on identical subjects; re-run of the gate set passes.")
car("e6-card-M2-c350", "M2-c350 and L23.html")
car("e6-card-M2-c363-c365", "M2-c363, M2-c364, M2-c365 and L24.html")
ok("e6-card-M2-c404-c405", "c404 changed (Lesson 22 'assumed and not proved' wording), re-read against L22.html and "
   "verified in e2-cards-L22. c405 removed; its subject (Assumption 4.1) is carded by c420, verified in e2-cards-L24.")
ok("e6-card-M2-c408-c409", "M2-c408 and M2-c411 absent at HEAD (also absent at ccaeeaf4). M2-c409 removed in this delta, "
   "so the hypothesis check on it no longer applies; coverage observation recorded in e2-cards-L16.")
ok("e6-instances-50", "run_graders.py seeds 0-49: instance validity and reference pass (r1_run_graders.out).")
ok("e6-mutants-new-v6e", "v6e_01..v6e_04 in ledgers/M2/mutants/: all KILLED in r1_mutate_graders_M2.out.")
car("e6-L24-E3-unrounded-difference", "course/modules/M/M2/L24.html (E3 solution and interpretation)")
car("e7-L22-L24-lesson-numbers", "course/modules/M/M2/L22.html, L23.html and L24.html")
ok("e7-round7-mutants-v7e", "v7e_01..v7e_04 in ledgers/M2/mutants/: all KILLED in r1_mutate_graders_M2.out.")
ok("e7-alternatives-new", "24 of 24 alternatives pass seeds 0-49 (r1_alternatives.out).")
ok("e7-twins-27-alone", "27 twins alone under python -I -W error: exit 0, empty stderr (/tmp/m2e_r1_twins/index.txt).")
car("e8-ad-float-return-contract", GRADER + " (float checks in the forward-mode and zero-derivative tests); pytest "
    "QF_SEED 0-3 re-run this round: 89 passed each")
ok("e9-delta-read", "This round's delta over slice paths was read in full: git diff --stat ccaeeaf4..95f3f8cb for "
   "course/modules/M/M2 (21 files), tests/labs/M2 (8 files), ledgers/M2/mutants (4 added), references and pyproject "
   "(global). Hunks read: project.html (1 line), index.html (3 hunks), cards.json (36 changed, 15 added, 11 removed), "
   "lesson HTML L01-L18 (word diffs).")
car("e9-ad-int-zero-at-origin", GRADER)
car("e9-fd-int-zero-at-origin", GRADER)
ok("e9-mutants-new-v9e", "v9e_01..v9e_05 in ledgers/M2/mutants/: all KILLED in r1_mutate_graders_M2.out.")
ok("e9-alternatives-r9", "24 of 24 alternatives pass seeds 0-49 (r1_alternatives.out).")
R["e10-cards-c412-duplicates-c065"] = (
    "FAIL",
    "Semantic duplicates reintroduced in this delta. (1) M2-c417 (L08, grade T): 'what does Rolle's theorem state' "
    "answered with the same hypotheses and conclusion as M2-c065 (L06 Theorem 2.2, grade T); L08.html line 76 states the "
    "same Rolle theorem. This is the exact pair the base row (round-10 FAIL) removed M2-c412 for. (2) M2-c429 (L10, grade "
    "T): 'Theorem 1.2 of Lesson 10 (mean value theorem): what does it state' duplicates M2-c066 (L06 Theorem 2.3). "
    "(3) M2-c428 (L08): 'What is Assumption 1.1' restates M2-c064 (L06, 'Is Assumption 2.1 proved?'); near duplicate, "
    "same fact. Each card is correct as a statement; the defect is that the same question is carded twice. Ruling 26 does "
    "not list duplicates among its FAIL kinds; this is classified LOW (card style) by this verifier.",
    "Delete M2-c417, M2-c429 (or reword them as questions about where Lesson 8 and Lesson 10 use the theorem, as M2-c418 "
    "does), and fold M2-c428 into M2-c064. Re-run check_pages --unit M2 and build_site --check. If the orchestrator "
    "classifies this as LOW under ruling 26, record it in plans/KNOWN-ISSUES.md with this row id instead of fixing.",
)
ok("e10-cards-changed-c027-c047-c177-c352", "c027 (L03 Definition 1.1), c047 (L04 lab numbers, 3.000001), c177 (L12 "
   "truncation error 1/b) and c352 (L23 Misconception 1) re-read against their lessons this round; all agree. c027, c047, "
   "c177 and c352 changed or sit in changed lessons; re-verified, not carried.")
ok("e10-cards-c413-new-L15", "c413 (L15 Section 3 continuity definition, L15.html line 143) unchanged and agrees with "
   "the lesson text; L15 locators resolve.")
car("e10-sin-ratio-range", PROJ + " Tolerances, " + GRADER)
ok("e10-hours-estimate-under-ruling", "check_projects PASS (time budget sums to the declared 60 h, r1_check_projects.out); "
   "hub 60 h (20%) in index.html.")
car("e10-spec-clarifying-questions", PROJ + " Rung 3 Specification")
ok("e10-links-anchors", "project.html: 10 internal href='#...' anchors, all resolve to an id (script run this round).")
ok("e10-alternatives-r10", "24 of 24 alternatives pass seeds 0-49 (r1_alternatives.out).")
ok("e10-mutants-r10-new", "w10e_01..w10e_05 in ledgers/M2/mutants/: all KILLED in r1_mutate_graders_M2.out.")
ok("e11-cards-c390-changed", "M2-c390 (L01 tail from index K) read against L01.html Section 3 and Proposition 3.1; agrees.")
ok("e11-cards-deleted-c408-c411", "M2-c408 and M2-c411 absent at HEAD (checked by id); no claim of theirs is restated by "
   "a card the delta removed.")
ok("e11-mutants-new-w11e", "w11e_01..w11e_04 present (added after ccaeeaf4 in commit 329c1d7f) and all KILLED in "
   "r1_mutate_graders_M2.out.")
ok("e11-alternatives-new-r11", "alt6 and alt7 in ledgers/M2/scripts/M2-e-r11/alts_r11: both pass 50/50 seeds (r1_alternatives.out).")
ok("e11-build-site-check", "build_site.py --check -> 'site data current: 6 outputs', exit 0 (r1_build_site_check.out).")
ok("e11-curriculum-regeneration-out-of-slice", "Out of slice; re-run because curriculum sources changed: "
   "render_curriculum.py --check -> 'curriculum valid: 25 parts, 134 modules, 157 projects', exit 0 "
   "(r1_render_curriculum_check.out); fetch_data.py --check -> '3 datasets, 0 problems' (r1_fetch_data_check.out).")

# --- assemble ---------------------------------------------------------------------------------------------------
missing = [i for i in base_rows if i not in R]
extra = [i for i in R if i not in base_rows]
if missing or extra:
    sys.exit(f"row id mismatch: missing={missing} extra={extra}")

rows = []
for r in base["rows"]:
    status, evidence, fix = R[r["id"]]
    row = {"id": r["id"], "check": r["check"], "location": r["location"], "status": status, "evidence": evidence}
    if fix:
        row["fix"] = fix
    rows.append(row)

mutants = []
pat = re.compile(r"^KILLED (\S+)\.py: (.*) -> (.*)$")
for line in (S / "r1_mutate_graders_M2.out").read_text(encoding="utf-8").splitlines():
    m = pat.match(line)
    if m:
        mutants.append({"id": m.group(1), "description": m.group(2).strip(), "killed_by": m.group(3).strip()})
if len(mutants) != 175:
    sys.exit(f"expected 175 killed mutants, got {len(mutants)}")

counts = {}
for r in rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
verdict = "PASS" if counts.get("PASS", 0) == len(rows) else "FAIL"

fragment = {
    "unit": "M2",
    "slice": "e",
    "round": 1,
    "verifier": "Haiku 5.5 independent verifier (round 1, slice e, closing delta)",
    "pin": "95f3f8cb",
    "base": "ccaeeaf4 (base fragment ~/.fanout/frags/D-M2-e.round11.json, its round-11 pin)",
    "checkout": str(CHECKOUT),
    "scratch": "/tmp/m2e_r1_* (grader copies, lab twin runs /tmp/m2e_r1_twins, lab 2 run, locator scan)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [
        "The base fragment states pin ccaeeaf4 contains ledgers/M2/mutants/w11e_01..04 and ledgers/M2/scripts/M2-e-r11/alts_r11 "
        "and alternatives_r11.out. git cat-file shows they are absent at ccaeeaf4; they were added in commit 329c1d7f "
        "(Final verification: round 11 fixes), which is an ancestor of HEAD. They were run in this round from HEAD.",
        "The base fragment's pin ccaeeaf4 is the commit 'Final verification: round 10 fixes'; base rows that cite round-11 "
        "files are therefore not reproducible from ccaeeaf4 alone.",
    ],
    "notes": [
        "Closing delta over slice e: git diff ccaeeaf4..95f3f8cb. Slice paths changed: course/modules/M/M2/cards.json "
        "(36 changed, 15 added, 11 removed), project.html (one line: Lab 2 hypothesis), index.html (placement quiz, L21 card "
        "blurb), lesson HTML L01-L18 (prose; cards re-read against each changed lesson), tests/labs/M2 twins L06, L07, L13, "
        "L14 (all 27 twins re-run), ledgers/M2/mutants w11e_01..04 (present at HEAD, all killed). grader/ unchanged. "
        "Global files read: references/references.json (one entry used_by; not M2-cited), pyproject.toml (ruff exclude), "
        "curriculum sources and program.json (brief text of an out-of-slice project; render and build checks pass).",
        "FAIL is one row: e10-cards-c412-duplicates-c065 (semantic duplicates M2-c417/c065, M2-c429/c066, near-duplicate "
        "M2-c428/c064). Every other row is PASS. No ruling-26 defect kind was found in the changed subjects: no false math, "
        "no missing hypothesis, no wrong number, no over-grade, no failing gate, no surviving non-equivalent mutant, no lab "
        "statement the code does not support. The duplicate row is classified LOW by this verifier (see its evidence); the "
        "orchestrator decides whether to fix or defer it to plans/KNOWN-ISSUES.md.",
        "Mutants: 175 of 175 killed on HEAD (standing set, including the four w11e mutants). No new mutants were written "
        "(ruling 37). Alternatives: 24 of 24 pass seeds 0-49.",
        "Carried rows (prefix 'Carried from round 11'): their subjects are byte-identical to ccaeeaf4 by git diff (project.html "
        "changes only one line, the Lab 2 hypothesis; grader/ unchanged; L20, L21, L23, L24 html unchanged; L22 html "
        "unchanged). Lab 1 and Lab 3 numbers and the rubric and exemplar text are carried on that basis.",
        "Index placement quiz (index.html, changed) is outside the rows of this slice except e2-hours-arithmetic. Its two "
        "numeric skill checks were re-derived: x^4 central second difference at h = 0.1 is 12.02 (1.1^4 + 0.9^4 - 2 = "
        "0.1202, divided by 0.01); x^3 central difference is 3 + h^2 = 3.01. Its prose was not re-verified against the "
        "lessons (observation).",
        "Observations, not fails: M2-c409, c399, c400, c401 and c208 were removed; the L16 Assumption 1 (exp derivative) "
        "and the L14, L17, L18 Assumption 1 cards no longer have their own card. Coverage observation, not a ruling-26 kind.",
        "Observation: M2-c013 changed grade from T to none (a remark about Definition 2.1). Accepted as a non-graded remark.",
        "Line numbers cited as Lxx.html line N refer to the plain-text extraction of that page (ledgers/M2/scripts/M2-e-r1/extract_lesson_text_r1.py, output in /tmp/m2e_r1_text), except where a row says raw HTML (for example L06.html line 201, L08.html lines 61 and 76, which were read from the raw file).",
        "Not checked: a line-by-line read of all 24 lesson pages (only the changed lines of L01-L18 and the cards that "
        "cite them); live Crossref/Open Library re-resolution of registry entries; the blind rubric scorer for M2 (none "
        "exists in ~/.fanout/blind/); page_smoke for the changed lesson pages (not slice e); lab expected blocks in lesson "
        "pages beyond run_labs' own check.",
    ],
    "summary": f"Slice e closing delta round 1 (pin 95f3f8cb, base ccaeeaf4): {counts.get('PASS', 0)} of {len(rows)} rows "
               f"PASS, {counts.get('FAIL', 0)} FAIL (e10-cards-c412-duplicates-c065, LOW card-style duplicates). Mutants "
               f"175/175 killed. Gates: all PASS.",
}

OUT.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", OUT, "rows", len(rows), counts, "mutants", len(mutants), "verdict", verdict)
