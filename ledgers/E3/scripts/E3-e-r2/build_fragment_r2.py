"""Build ledgers/E3/E3-e.json for verifier E3-e, round 2 (pin c737272, base d0f39c0).

Every mutant row is read from the mutate_graders output in ledgers/E3/scripts/E3-e-r2/ so the ledger cites repository
files. Usage (from the checkout root): python -I ledgers/E3/scripts/E3-e-r2/build_fragment_r2.py
"""

import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path.cwd()
S = ROOT / "ledgers/E3/scripts/E3-e-r2"
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

CHECKOUT = str(ROOT)
EV = "ledgers/E3/scripts/E3-e-r2/"


def text(name: str) -> str:
    return (S / name).read_text(encoding="utf-8")


# ---- mutants: every file in ledgers/E3/mutants (run by tools/mutate_graders.py) plus the restored r10n06 -------------
mutants = []
for line in text("mutate_E3_0_9.out").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+)\.py: (.*) -> (.*)$", line)
    if m:
        status, name, desc, killed = m.groups()
        mutants.append(
            {
                "id": name,
                "description": desc.strip(),
                "killed_by": None if killed.strip() == "None" else killed.strip(),
                "evidence": f"{EV}mutate_E3_0_9.out ({status})",
            }
        )
for line in text("named_mutants_r2.out").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+)\.py: (.*)$", line)
    if m and m.group(2).startswith("r10n06"):
        status, name, killed = m.groups()
        mutants.append(
            {
                "id": "r10n06_restored_from_d0f39c0",
                "description": "Logit log term computed as naive log(1 + exp(t)) (overflows for large |t|); restored "
                "from d0f39c0 after the builder deleted it from mutants/ (not counted by mutate_graders).",
                "killed_by": None if killed.strip() == "None" else killed.strip(),
                "evidence": f"{EV}named_mutants_r2.out ({status}); {EV}probe_r10n06_large_kappa.out",
            }
        )

alt_lines = []
for n in range(1, 6):
    if n != 4:
        body = (S / f"alt_alt{n}_0_49.out").read_text(encoding="utf-8").strip().splitlines()
        alt_lines.append(next((ln for ln in body if ln.startswith(f"alt{n}: ")), f"alt{n}: no result line"))
    else:
        windows = ["0-9", "10-19", "20-29", "30-39", "40-49"]
        results = []
        for w in windows:
            body = (S / f"alt4_{w}.out").read_text(encoding="utf-8").strip().splitlines()
            results.append(next((ln for ln in body if ln.startswith("alt4: ")), f"alt4 window {w}: no result line"))
        ok = all(" PASS " in ln for ln in results)
        alt_lines.append("alt4: " + ("PASS (50/50 seeds, five windows: " if ok else "FAIL (windows: ") + " | ".join(r.replace("alt4: ", "") for r in results) + ")")
alt_all_pass = all(" PASS " in ln for ln in alt_lines)

rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

# ---- rows (ids E3e-01..E3e-38 kept from round 1; E3e-39.. are new in round 2) -------------------------------------
row("E3e-01", "2.9 banned strings", "course/modules/E/E3/project.html (visible prose)", "PASS",
    f"{EV}check_pages_E3.out: check_pages E3: PASS (banned-string check, BUILDER_RULES 1.3). Hand scan for TODO, TBD, lorem, "
    "brevity, beyond the scope: no hit; 'omitted probability weighting' (project.html:603, :710) is not a banned phrase.")
row("E3e-02", "2.9 process words in learner text", "project.html; grader/*.py; tests/labs/E3/lab-E3-project-*.py; L02-L08", "PASS",
    f"{EV}symbol_scan.py over those files for plan|Q12|architect|builder|verifier|ruling|section 10|ledger|slice: no hit "
    "in learner text.")
row("E3e-03", "2.9 process references in learner-visible code", "grader/test_project.py:515-517", "PASS",
    "Round-1 FAIL resolved: the recovery-test docstring no longer cites 'plan section 10 Q12'; it reads 'a threshold of this "
    f"suite, stated on the project page' (test_project.py:515-517). {EV}symbol_scan.py: no Q12 or plan reference in grader/*.py.")
row("E3e-04", "2.9 links and anchors", "course/modules/E/E3/project.html (34 href/src)", "PASS",
    f"{EV}link_check.py: 34 href/src checked, 0 problems, no external references; every #anchor exists; "
    "project page has 0 svg/figure/img/canvas. page_smoke project: PASS (no external requests).")
row("E3e-05", "2.9 structure; 2.6 ladder and spec sections", "project.html:40-230", "PASS",
    "Ladder with four rungs (:43-48); Rung 1 and 2 labs (:55-189); spec dl Context, Inputs, Required outputs, Constraints, "
    "Grading mode, Reading list (:193-206); Conventions (:208-216); Exception table (:218-230). check_projects E3: PASS "
    f"({EV}check_projects_E3.out).")
row("E3e-06", "2.6 hours arithmetic", "project.html:352-358; index.html:29", "PASS",
    "Components 1+1+3+4+3+2 = 14 = total row and data-hours-project=14 (:33, :358). Hub data-hours-lessons=56 "
    "(index.html:29) + 14 = 70 = curriculum/02-economics-finance-core.yaml:91 hours: 70.")
row("E3e-07", "2.6 rung 3 matches curriculum scope exactly", "project.html:195, 199, 203 vs curriculum/02-economics-finance-core.yaml:118-121", "FAIL",
    "Curriculum brief (unchanged since round 1): 'estimate the participant's risk-aversion and loss-aversion parameters by "
    "MLE'. The page's Rung 3 requires three estimates (gamma, lambda and kappa; project.html:195 'the brief names the first "
    "two; the precision kappa is a third estimated parameter'; :199 estimate returns kappa_hat, se_kappa; :203 zeta, log lambda, "
    "log kappa). The disclosure at :195 does not make the scope match 'exactly'.",
    "Architect decision: either amend the E3 brief in curriculum/02-economics-finance-core.yaml (then regenerate), or drop "
    "the kappa estimate from Rung 3 (fix kappa and remove kappa_hat, se_kappa, the kappa checks and Lab 3 kappa output).")
row("E3e-08", "2.6 spec completeness (questions a student would ask)", "project.html:225-227 (exception table rows)", "FAIL",
    "Question 1: the row 'responses is empty, or no response has a lottery that mixes...' (:227) does not name a function. "
    "Does log_likelihood (which takes responses) also raise ValueError in that case? The reference does not (log_likelihood "
    "returns a value for a response with no mixed lottery; the suite tests only estimate). Question 2: the row for "
    "non-negative/sum-to-1 probabilities (:225) is general; the suite does not test that log_likelihood raises for it "
    "(see E3e-39, where the reference raises and a mutant that skips the check survives).",
    "Name the function in each table row: e.g. 'estimate' for the mixed-lottery row; 'every function that takes "
    "probabilities' for the probability row. Then add the matching test(s) to test_project.py.")
row("E3e-09", "2.6 rubric level descriptors observable (C1)", "project.html:600 (C1, level 1 cell)", "PASS",
    "Round-1 FAIL resolved: level 1 is now 'No instrument described: no count of pairs, no prize scale, and no pair shown.' "
    "(:600), which is observable.")
row("E3e-10", "2.6 rubric descriptors and calibration (C5)", "project.html:604, 612-614, 657-659", "PASS",
    "Round-1 FAIL resolved: C5 level 2 'At least one empirical claim has a grade and a registry key, and at least one lacks "
    "one' and level 1 'No empirical claim has a grade or a registry key' (:604). Exemplar A (:612-614) official C5 1 and its "
    "annotation (:659, 'Meets C5 level 1') now agree with the descriptors; blind scoring of Exemplar A gives C5 1.")
row("E3e-11", "2.6 rubric structure", "project.html:596-606 (rubric), :612, :665 (exemplars), :727-731 (self-assessment)", "PASS",
    "Five criteria (C1-C5), four levels each (:600-604); two exemplars with annotations (:612, :665); self-assessment form "
    "(:727-731). Re-read in full this round.")
row("E3e-12", "2.6 calibration of both exemplars (blind scoring)", "project.html:665-725 (Exemplar B), :675 (C1 annotation)", "FAIL",
    "Blind scoring of Exemplar B: C1 2, C2 4, C3 4, C4 3, C5 4 against official 3,4,4,3,4: every criterion within one level "
    "(calibration rule passes). But the C1 annotation at :675 says 'Meets C1 level 3: the count, the scale in cents, the "
    "reason for losses, and two example pairs'. The memo (:671) gives count, cents and examples and says that both lotteries "
    "mix a gain and a loss, but states no reason for including losses (the sentence 'the estimate refuses any set of answers "
    "with no mixed lottery' is a consequence, not a reason). The annotation names an element the memo does not contain.",
    "Either add a sentence giving the reason (for example, that losses are needed so that loss aversion is identified) or "
    "change the C1 annotation to level 2 and the official C1 score (:665 data-scores, :667 verdict) to 2.")
row("E3e-13", "2.6 exemplar length claims", "project.html:610 (length of Exemplar A and B)", "FAIL",
    f"Exemplar A memo: 103 words, headings included (matches :610). Exemplar B memo: the page says 375 words, headings "
    f"included. Recount with {EV}exemplar_and_grader_counts.py: 525 words, headings included (per block 117, 166, 83, 99, 60); "
    "507 with TeX math spans removed. Neither method gives 375.",
    "Change '375' in project.html:610 to the measured count (525 words, headings included), or state the counting method "
    "and the value it gives.")
row("E3e-14", "2.2 numbers in exemplars and prose", "project.html:57, 138, 143, 383-394, 571-577, 610-721", "PASS",
    f"Lab printed values re-run this round ({EV}twins_project.out, run_labs_E3.out): gamma_hat 0.6352, lambda_hat 6.1503, "
    "kappa_hat 2.0201, se 0.32/9.59/1.86, log-likelihood -7.1445, largest score 3.55e-10, 12 answers, 11 mixed-sign. Exemplar B "
    f"instrument facts recomputed ({EV}exemplar_and_grader_counts.py): prizes from -18700 to 19000 cents, two or three prizes "
    "per lottery, pair 0 and pair 3 values as printed, every probability list sums to exactly 1.")
row("E3e-15", "2.1 reading list: registry keys, freshness, attribution", "project.html:743-752; L07.html:80; L08.html:67, :133; L02.html:616", "PASS",
    "All five keys exist in references/references.json with status verified (pratt1964risk, kahneman1979prospect, "
    "epstein1989substitution, ellsberg1961risk, gilboa1989maxmin). Claims in Lessons 5-8 carry data-cite on three keys "
    "(kahneman in L07.html:80, gilboa and ellsberg in L08.html:67 and :133), which matches 'Three of the five ... Lessons 5 to 8' "
    "(:744). Pratt named in L02.html:616 without a claim, as stated. Epstein-Zin has no claim in L05 and the page says so. "
    f"Offline registry check: {EV}verify_refs_offline.out (560 entries, 0 problems).")
row("E3e-16", "2.1 attribution on the project page", "project.html:205, :744 and every class=claim", "PASS",
    "The project page attributes nothing to a source: the only source references are the reading list (:743-752). "
    "Numbers are attributed to Lab 3 (:717, :721) and to the page's definitions.")
row("E3e-17", "2.4 definitions cited from the page", "project.html:53, :210; L02.html:98; L03.html:88, :173; L06.html:69, :89", "PASS",
    f"Anchors resolved by {EV}link_check.py: L02#def-certainty-equivalent, L03#def-crra-utility, L06#def-prospect-theory, "
    "L06#def-loss-aversion present. 'Lesson 3, Proposition 2.7' (:53) is the affine-transformation proposition at L03.html:173, "
    "and a positive factor 1/(1-gamma) is an affine transform with b = 0.")
row("E3e-18", "2.5 Lab 1 prose vs code (CRRA utility)", "project.html:53, :82-83, :120-126, :138", "PASS",
    "Round-1 FAIL resolved. The code's CRRA utility is w**(1-gamma) with no 1/(1-gamma) (project.html:82-83), and the text says "
    "'a positive multiple of W^{1-gamma}/(1-gamma)' (:138), which is correct. main() prints two lines per pair (:120-126), "
    "as :138 states. The factor-removal sentence at :53 is consistent with the code.")
row("E3e-19", "2.5 Lab 1 (worked example)", "project.html:55-139; tests/labs/E3/lab-E3-project-1.py", "PASS",
    f"Twin run with python -I -W error: exit 0, output equals the page's expected block ({EV}twins_project.out). Hypothesis "
    "values (496/500, -30/500, P(A)=0.480149, -0.733658, total -2.302315) match the output.")
row("E3e-20", "2.5 Lab 2 (completion problem)", "project.html:141-188; tests/labs/E3/lab-E3-project-2.py", "PASS",
    f"Completed twin prints -0.765595182 (A), -0.625595182 (B), P(A)=0.465057055 with z=-0.14 (checked by arithmetic); "
    f"run_labs E3 PASS 11/11 ({EV}run_labs_E3.out) verifies the blanks against the twin.")
row("E3e-21", "2.5 Lab 3 (reference case) and its prose", "project.html:381-579; tests/labs/E3/lab-E3-project-3.py", "PASS",
    "Twin output equals the expected block; hypothesis claims verified: 11 of 12 mixed, largest score 3.55e-10 below 1e-6, "
    "se_lambda 9.59 larger than lambda_hat 6.1503, and the sentence that the score check does not show a maximum is accurate.")
row("E3e-22", "2.5 lab and code gates", "tests/labs/E3/*; grader/*.py; project.html", "PASS",
    f"run_labs E3 PASS 11/11; pytest tests/test_labs.py -k E3: 15 passed ({EV}pytest_labs_E3.out); ruff check and format "
    f"--check on grader and lab twins: pass ({EV}ruff_E3_slice.out); mypy --no-incremental: 'Success: no issues found in 331 "
    f"source files' ({EV}mypy.out); page_smoke project: PASS, in-browser grader 39 of 39 ({EV}page_smoke_project.out).")
row("E3e-23", "2.4 mathematics on the page (conventions, identification, delta method)", "project.html:53, :195-214", "PASS",
    "Re-derived by hand: CRRA CE c = (E[W^{1-g}])^{1/(1-g)} - W; prospect CE c = V^{1/(1-g)} for V >= 0 and -(-V/lambda)^{1/(1-g)} "
    "for V < 0 (matches reference.py:94-97 and project.html:210); lambda drops out of an all-gain or all-loss lottery "
    "(gain branch has no lambda; loss branch is -lambda(-x)^(1-g), inverted by dividing by lambda), so a pair identifies lambda "
    "only with a mixed lottery (:213). Delta method d gamma/d zeta = gamma(1-gamma) (:214). Tests at test_project.py:246-257 and "
    "719-736 confirm the exact values -25, +25, 225 and -225.")
row("E3e-24", "2.4 notation: registry and unit-level collisions", "project.html:195, :203, :212-214, :737; L02.html:185-197; L08.html:598-600; L07.html:84, :148", "FAIL",
    "Registry check PASSES: no use of T, gamma_3, gamma_4, R^ast, R^{e ast}, R_f or \\mathbb{Q} in the E3 pages; \\Phi (project.html:737) "
    "is the standard normal distribution function, the registered meaning; every macro used (\\E, \\Prob, \\R, \\Var) is "
    f"registered and there is no direct \\mathbb ({EV}registry_symbol_scan.py, {EV}tex_macro_census.py). The rename is applied in "
    "the project (no eta left, see E3e-42), but it moved a collision: the project's logit coordinate is now zeta (project.html:203, "
    "214, 434) while L02.html:185-197 uses zeta(epsilon) for the remainder function in the same unit. kappa was not renamed: "
    "it is the choice precision (project.html:57, :195, :212) and, in L08.html:598-600, the CARA coefficient of u(W) = -exp(-kappa W). "
    "eta is the weighting exponent in L07 (:84, :148) and the remainder in L02 (:191-197). The registry is silent on "
    "these local letters, so this is a judgement: the same letter carries two meanings inside one unit, and the rename itself created the zeta collision.",
    "Give each meaning one symbol within E3: rename L02's zeta(epsilon) and eta(pi) (or the logit coordinate), and rename "
    "either kappa in L08 (the CARA coefficient) or the choice precision in project.html, Lab 1-3 and grader (kappa_hat keys "
    "change with it). Check cards.json for the same symbols.")
row("E3e-25", "2.9 DAG: concepts used outside the closure", "project.html:53, :57-61, :214, :578; check_dag output", "PASS",
    f"check_dag: PASS for all units ({EV}check_dag.out). The page links three concepts defined in its own unit's lessons "
    "(prospect-theory L06, certainty-equivalent L02, crra-utility L03). MLE, delta method, Newton's method and observed information "
    "appear as plain prose with no link and no dfn, as the architect decision requires for out-of-closure concepts.")
row("E3e-26", "2.9 terms used before definition", "project.html:53, :197, :214", "PASS",
    "'logit' is named at :53 with its formula and a pointer to the Rung 3 convention, which defines it (:212). 'mixed' is defined "
    "in the sentence that first uses it (:197). 'observed information' first appears at :214 (its definition) and is used afterwards at :356 and :393.")
row("E3e-27", "2.9 scope words", "project.html:201, :203, :212-215", "PASS",
    "'every' (:201: every money output is an int) is checked by test_wrong_types and the int-type tests; 'only' (:213) is a "
    "necessity claim that holds (proved above, E3e-23); 'exactly' (:215) is enforced by the exact-Fraction test at "
    "test_project.py:300-355; 'all' (:213 'all gains, or all losses') is the definition used in the proof.")
row("E3e-28", "2.6 autograder claims stated on the page", "project.html:201-203, :366, :372-374", "PASS",
    f"'39 checks' = collect-only 39 ({EV}collect_only.out); 'warnings as errors' = pytestmark filterwarnings('error') "
    "(test_project.py:31); 'no print, no warning' = test_engine_imports_only... (test_project.py:990-1015); the score tolerance 2e-5 "
    "and steps 1e-5/1e-6 match test_project.py:494-497; 47 of 50 within four SE match test_project.py:513-530.")
row("E3e-29", "2.6 reference passes seeds 0-49", "grader/reference.py; tools/run_graders.py --unit E3 --seeds 0-49", "PASS",
    f"{EV}run_graders_E3_0_49.out: 'run_graders E3: PASS (reference 50/50 seeds, slowest 15.3 s)', exit 0.")
row("E3e-30", "2.6 mutation: every mutant killed (existing and new)", "ledgers/E3/mutants/ (69 files); ledgers/E3/equivalent/", "FAIL",
    f"{EV}mutate_E3_0_9.out: 'mutate_graders E3: FAIL (68/69 killed)'; the only survivor is e2_01 (E3e-39). The round-1 survivor "
    "r10n06_logit_log_term_naive_exp_overflow.py is no longer in ledgers/E3/mutants/: git shows it deleted at c737272 and it was "
    "not moved to equivalent/ (only README.md is there). The restored file survives seeds 0-9 "
    f"({EV}named_mutants_r2.out: SURVIVED) and raises OverflowError at kappa=1e5, where the reference returns -1850.197 "
    f"({EV}probe_r10n06_large_kappa.out). It is a real fault on a valid input (kappa > 0, project.html:212, :214), so it cannot be "
    "moved out as equivalent.",
    "Restore the mutant to ledgers/E3/mutants/ and add a test whose input tells it apart: log_likelihood on a response with "
    "CE_A - CE_B = -185 cents and kappa = 1e5 must return a finite value equal to the oracle (about -1850.197). Then rerun "
    "tools/mutate_graders.py --unit E3 --seeds 0-9 and require every mutant killed.")
row("E3e-31", "2.6 three new student-error mutants written by the verifier", "ledgers/E3/mutants/e2_01..e2_03", "PASS",
    "Three complete modules, each reference.py with one change and a one-line docstring: e2_01 log_likelihood skips the probability "
    "checks; e2_02 observed information by central differences of step 1e-3; e2_03 prospect refuses non-positive final wealth. "
    f"Written by {EV}make_mutants_r2.py. Results: e2_02 KILLED by test_standard_errors_match_the_delta_method_oracle (seed 2); "
    "e2_03 KILLED by test_crra_requires_wealth_plus_every_prize_to_stay_positive (seed 0); e2_01 SURVIVED (E3e-39).")
row("E3e-32", "2.6 alternative correct implementations (over-constraint)", "ledgers/E3/scripts/run_alternatives.py (alt1-alt5), seeds 0-49", "PASS" if alt_all_pass else "FAIL",
    f"{EV}alt_alt1..3,5_0_49.out and alt4_<window>.out (run_alt_one_r2.py, one process per alternative or window): " + "; ".join(alt_lines)
    + ". alt2 and alt4 each fail only seed 49, both with the ValueError of test_standard_errors_match_the_delta_method_oracle (test_project.py:811): see E3e-50. Scratch run of alt4 seed 49 in /tmp/e3e_r2/alt4/seed49.out: 38 passed, 1 failed (that test).",
    None if alt_all_pass else "Fix the over-constrained test (E3e-50); every alternative must then pass 50 of 50 seeds.")
row("E3e-50", "2.6 over-constraint: a correct implementation crashes the standard-error oracle", "grader/test_project.py:807-815 (math.sqrt at :811)", "FAIL",
    f"alt2 (grid, then Newton with central differences step 1e-6) is correct and passes 49 of 50 seeds; it fails seed 49 with "
    "'ValueError: expected a nonnegative input, got -23.27...' raised by math.sqrt(cov[1][1]) at test_project.py:811. Probe "
    f"({EV}probe_alt2_seed49.out): for alt2's estimate the oracle's inverse diagonal at step 1e-5 is (0.2148, 44.75, 0.06336), "
    "(alt4, the bisection inversion, fails the same way: 'ValueError: expected a nonnegative input, got -6.48...' on seed 49). "
    "and its SEs (0.09615, 138.379, 0.57384) match alt2's own SEs (0.09613, 138.354, 0.57388) to 0.1%, so the step-1e-5 "
    "branch would pass. At step 1e-6 the oracle's inverse diagonal is (0.01024, -23.28, 0.05716): a negative variance. The loop "
    "computes the step-1e-6 oracle before it checks 'matched', so the exception escapes and the test errors instead of "
    "accepting the step-1e-5 match. A student's correct engine with a step-1e-6 Hessian fails the same way.",
    "In test_standard_errors_match_the_delta_method_oracle, skip a step whose inverse diagonal is not positive (record no match "
    "for that step) instead of calling math.sqrt on it; then rerun all five alternatives on seeds 0-49.")
row("E3e-33", "2.6 test count on the page equals collect-only", "project.html:203 ('39 checks'); grader/test_project.py", "PASS",
    f"collect-only: 39 tests ({EV}collect_only.out). Page: 'runs 39 checks' (:203); page_smoke in-browser: 'All 39 tests pass'. "
    "Round 1 said 38 (before the new float-resolution test).")
row("E3e-34", "2.6 exception table: conditions and messages", "project.html:218-230; grader/reference.py:30, :60, :121, :138; test_project.py:286-379, :557-602", "PASS",
    "Each row's message is contained in the reference's ValueError text (model names, 'probabilities must sum to 1', 'wealth plus "
    "prize must stay positive'); each named condition has a test. The open question on the mixed-lottery row is E3e-08, not a "
    "message defect.")
row("E3e-35", "2.8 figures (cards: not in this slice)", "project.html (no figure); course/modules/E/E3/cards.json (not read)", "PASS",
    "The project page has no figure: 0 svg, figure, img or canvas elements (link_check.py output). Cards are not in this slice "
    "(task says 'No cards'); cards.json was grepped only for the symbol rename (see E3e-24).")
row("E3e-36", "2.1 reference registry integrity (live)", "references/references.json (5 E3 keys)", "PASS",
    f"Carried from round 1 (references/references.json byte-identical since the previous pin d0f39c0; git diff --quiet): live "
    f"Crossref resolution of the five keys passed in round 1. Offline integrity re-run this round: {EV}verify_refs_offline.out "
    "('offline integrity: 560 entries, 0 problems'). No live Crossref call was made in round 2.")
row("E3e-37", "2.9 interactive questionnaire and privacy claims", "project.html:235, :239-343, :765; course/assets/js/grader.js:18; store.js", "PASS",
    "The questionnaire script exports only when every pair has a choice (project.html:328-331); it makes no fetch, XHR or beacon; "
    "grader.js fetches only the local grader files (grader.js:18); storage is IndexedDB in store.js; 'nothing you write leaves it' (:765) "
    "is consistent with that code.")
row("E3e-38", "2.6 rung 4 open-ended", "project.html:734-740", "PASS",
    "Two stretch tasks (a probit model; a probability-weighting function) with no answer key and no fixed output.")
row("E3e-39", "2.6 suite gap: named probability condition for log_likelihood", "grader/test_project.py (no test); project.html:201, :225", "FAIL",
    f"Mutant e2_01 (log_likelihood skips the probability checks) SURVIVES seeds 0-9 ({EV}named_mutants_r2.out, {EV}mutate_E3_0_9.out). "
    f"Probe ({EV}gap_probe_log_likelihood.py): a response with probs_a 1/2 and 499/1000 makes the reference raise 'probabilities "
    "must sum to 1 (and be non-negative)' and makes e2_01 return -0.7082688. project.html:225 names that condition with ValueError, "
    "and project.html:201 says every named invalid input raises it.",
    "Add a test: log_likelihood (and estimate) on responses with probabilities summing to 999/1000, and with a negative "
    "probability, must raise ValueError whose message contains 'probabilities must sum to 1'. Then e2_01 is killed.")
row("E3e-40", "2.2 prose number in a docstring", "grader/test_project.py:799-802", "FAIL",
    "The docstring says: 'the evaluation order of the same log-likelihood alone moves the standard error of lambda by about 1.3%'. "
    f"Recomputed ({EV}seed49_docstring_numbers.py, {EV}order_check.py, run with QF_SEED=49): reversing the response order changes "
    "se_lambda by 0.00%; changing the order of the cross-difference terms changes se_lambda by 0.31% at step 1e-5 and 21.65% at "
    "step 1e-6. The other seed-49 numbers in the same docstring reproduce (135.05 and 97.67; 0.09474 and 0.07983; -27.7%; -15.7%).",
    "Replace '1.3%' with the measured figures (0.3% at step 1e-5; 21.7% at step 1e-6, under a changed term order) or delete the claim.")
row("E3e-41", "2.6 equivalent-mutant README and cited ruling", "ledgers/E3/equivalent/README.md; plans/E3-open-items.md", "FAIL",
    "README says the r10n06 mutant 'is kept here, outside mutants/' and cites 'architect ruling 9'. ledgers/E3/equivalent/ holds "
    "only README.md. The only ruling numbered 9 in plans/E3-open-items.md (batch 3, round 9) concerns plan 6.5 items 6, 7 and 9 "
    "(dominance and Epstein-Zin mutants), not numerical range; no other ruling is about overflow or stability. The equivalence argument is also false: the mutant "
    f"raises OverflowError at kappa = 1e5 where the reference returns a value ({EV}probe_r10n06_large_kappa.out).",
    "Delete the equivalence claim; restore the mutant to mutants/ and kill it (E3e-30); remove equivalent/README.md unless a "
    "real architect ruling is quoted.")
row("E3e-42", "2.4 rename consistency (eta -> zeta; kappa)", "project.html; grader/test_project.py; tests/labs/E3/lab-E3-project-3.py", "PASS",
    "A regex scan (no standalone eta, ETA or \\eta) of project.html, test_project.py, reference.py, instance.py and the Lab 3 twin finds no hit; test_project.py docstrings "
    "at :474, :795 and the Lab 3 twin docstring (lab-E3-project-3.py:11-12, :51-52) use zeta; the embedded Lab 3 code is byte-identical "
    "to the twin (run_labs E3 PASS). L07.html:415-417 refers to the lab's variable ETA as a name, not as the logit coordinate. "
    "The remaining collisions are E3e-24.")
row("E3e-43", "2.8 instance docstrings vs code (instance.py)", "grader/instance.py:1-28, :53-259", "PASS",
    f"Ranges, wealth, 200 pairs, 500-50000 cent magnitudes, denominators 4/5/10/20, the 100-mixed-pair rule, the Hessian check, the "
    "0.5 boundary margin and the 1e-6 half-cent margin all match the code. Sample of 25 seeds (0-48 step 2): every lottery's "
    f"probabilities are positive and sum to 1 and the prizes are in range; 25 distinct answer digests ({EV}instance_sample_20.py).")
row("E3e-44", "2.6 dominance witnesses and verdict oracle", "grader/test_project.py:884-961", "PASS",
    "FOSD witness: A = B + 100 cents in every prize, so F_A <= F_B everywhere (A dominates first order). SOSD witness: A sure 0, "
    "B a fair gamble on -1000/+1000 (A dominates second order). The verdict functions compare the same inequality as the "
    "docstrings; the suite passes on the reference for 50 seeds (E3e-29).")
row("E3e-45", "2.6 failure messages name the property and never leak the answer", "grader/test_project.py:43-62 and every expect()", "PASS",
    "expect() and must_raise() use fixed hint strings with no interpolated expected or actual value (only the caller's condition "
    "text); pytest.fail(..., pytrace=False) and --assert=plain are used. Messages checked by reading the file.")
row("E3e-46", "2.6 same suite in Pyodide and local pytest", "page_smoke project; tools/run_graders.py", "PASS",
    f"In-browser grader: 39 of 39 pass ({EV}page_smoke_project.out); local pytest per seed through run_graders on 50 seeds "
    "(E3e-29).")
row("E3e-47", "2.6 hours estimate (verifier's own)", "project.html:352-358", "PASS",
    "My component estimates: Rung 1 about 1 h; Rung 2 about 1 h; instrument and questionnaire file about 3 h; elicit.py with local "
    "tests about 7 h (certainty equivalent and validation, log-likelihood, Newton with standard errors, exception table, tests); "
    "uncertainty and report about 3 h; self-assessment about 2 h. Total about 17 h, +21% against 14 h, inside the 30% limit. "
    "The 4 h line for elicit.py is about 75% low on its own; the rule applies to the total.")
row("E3e-48", "2.8 SIMULATED labels and no real data", "project.html:53, :57, :61, :197, :379, :383, :386, :366", "PASS",
    "Each lab and the questionnaire are labelled SIMULATED or declare the participant as stated input; project labs have 0 "
    "data-files attributes (grep).")
row("E3e-49", "2.9 page_smoke: console errors, math, external requests", "project.html", "PASS",
    f"{EV}page_smoke_project.out: 'page_smoke modules/E/E3/project.html: PASS'; 'page_smoke E3: PASS'.")

# ---- assemble and validate -------------------------------------------------------------------------------------------
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
killed = sum(1 for m in mutants if m["killed_by"])
verdict = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 and killed == len(mutants) else "FAIL"
fragment = {
    "unit": "E3",
    "slice": "e",
    "round": 2,
    "verifier": "Claude Haiku 5.5, independent verifier for E3-e, round 2 (did not build E3; fresh checkout; read VERIFIER_RULES and the verifier rules file; round-1 fragment used as context only)",
    "pin": "c737272",
    "base": "d0f39c0 (round-1 pin); delta d0f39c0..c737272 read for every hunk in the slice (project.html, grader/test_project.py, tests/labs/E3/lab-E3-project-3.py, L07.html:414-417, L08.html:105-113, 493-496, 613-616, curriculum/02-economics-finance-core.yaml FC1 hunk, ledgers/E3/mutants and equivalent)",
    "checkout": CHECKOUT,
    "scratch": "/tmp/e3e_r2/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Every project and grader file was read in full: project.html (767 lines), grader/test_project.py (1015), reference.py (317), instance.py (259), starter.py (35); lab twins 1-3 read; L02, L03, L06, L07, L08 and index.html read where the project cites them or where the delta touches them.",
        "Commands run this round (outputs in ledgers/E3/scripts/E3-e-r2/): run_labs --unit E3 (11/11); check_pages --unit E3; check_dag --all; check_projects --unit E3; run_graders --unit E3 --seeds 0-49 (50/50); mutate_graders --unit E3 --seeds 0-9 (68/69); verify_refs --offline (560 entries, 0 problems); ruff check and format --check on grader and lab twins; mypy --no-incremental (331 files); pytest tests/test_labs.py -k E3 (15 passed); page_smoke --pages project (PASS); collect-only (39); twins under python -I -W error (exit 0 each).",
        "The verifier-written mutants e2_01 (survives), e2_02 and e2_03 (killed) are in ledgers/E3/mutants/; the restored r10n06 is not in the repository directory and is recorded here with killed_by null.",
        "Not checked: a live Crossref run (not needed; registry unchanged since round 1); cards.json (out of this slice); L01, L04, L05 (out of this slice; L05 grepped only for the symbol rename); the deployment exclusion of grader/reference.py (BLUEPRINT.md:400-401 states it; no deploy script in this checkout); the hub index.html beyond the hours line; the L07 and L08 proofs changed in the delta (other slices), whose numbers I did not recompute (for example L07.html:417 gap 3.13e-1 and L08.html Remark 2.3 and the table near line 616 (certainty equivalents 99523.8095 and 101951.2195)).",
    ],
    "summary": {
        "rows": len(rows),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": counts["UNVERIFIABLE"],
        "mutants_killed": killed,
        "mutants": len(mutants),
    },
}
problems = ledger.validate(fragment, "E3-e")
out = ROOT / "ledgers/E3/E3-e.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("validate:", problems or "clean")
print("verdict:", verdict, "rows:", len(rows), counts, "mutants:", killed, "/", len(mutants))
