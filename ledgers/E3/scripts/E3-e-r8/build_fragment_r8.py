"""Round-8 builder for the E3 slice e ledger fragment (ledgers/E3/E3-e.json).

Reads the outputs of the round-8 runs under ledgers/E3/scripts/E3-e-r8/ (mutation, new-mutant kills, alternatives), writes
the fragment, and validates it with tools/ledger.py. Every row's evidence names a script or output file by repository path.
Run from the checkout root: .venv/bin/python -I ledgers/E3/scripts/E3-e-r8/build_fragment_r8.py
"""

import json
import pathlib
import re
import sys
from datetime import UTC, datetime

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD8-E3-e")
OUT_DIR = ROOT / "ledgers/E3/scripts/E3-e-r8"
ROUND7 = pathlib.Path("/Users/billyribeiro/.fanout/frags/D-E3-e.round7.json")
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

S = "ledgers/E3/scripts/E3-e-r8/"
CARRY = "Carried from round 7 ({files} byte-identical since the previous pin, or its cited lines outside the delta hunks): "


def carry(files: str, text: str) -> str:
    return CARRY.format(files=files) + text


# ----- mutation results ------------------------------------------------------------------------------------------------
mutants: list[dict[str, str | None]] = []
pattern = re.compile(r"^KILLED (\S+\.py): (.*) -> (.*) \((seed \d+|[^)]*)\)$")
for line in (OUT_DIR / "mutate_E3_seeds0-9_r8.out").read_text(encoding="utf-8").splitlines():
    if not line.startswith("KILLED "):
        continue
    m = pattern.match(line)
    assert m, line
    name, description, test, seed = m.group(1), m.group(2), m.group(3), m.group(4)
    mutants.append({
        "id": name,
        "description": description,
        "file": f"ledgers/E3/mutants/{name}",
        "killed_by": f"{test} ({seed}; tools/mutate_graders.py --unit E3 --seeds 0-9, {S}mutate_E3_seeds0-9_r8.out)",
    })
assert len(mutants) == 113, len(mutants)

for name, description in (
    ("e8e_02_prospect_model_name_lookup_raises_key_error.py",
     "Unknown model name raises KeyError from a dict lookup, where the page requires ValueError naming the two models."),
    ("e8e_03_crra_gamma_zero_rounds_exact_half_down.py",
     "At gamma = 0 the exact expected prize rounds an exact half down (ceil of x minus one half), against the page's rule."),
):
    kill_text = (OUT_DIR / "kill_new_e8e_r8.out").read_text(encoding="utf-8")
    first = re.search(re.escape(name) + r": killed on (\d+) of (\d+) seeds, survived on (\d+) seeds\n  seed \d+: FAILED (\S+)",
                      kill_text)
    assert first and first.group(1) == first.group(2) and first.group(3) == "0", name
    mutants.append({
        "id": name,
        "description": description,
        "file": f"ledgers/E3/mutants/{name}",
        "killed_by": f"{first.group(4)} (50 of 50 seeds; {S}kill_new_e8e_r8.out)",
    })

mutant_kill_summary = f"{len(mutants)} listed mutants; all killed (113 of 113 in the round-8 mutate run, 2 new ones on 50 of 50 seeds)"

# ----- alternatives ------------------------------------------------------------------------------------------------------
alt_lines = [
    line for line in (OUT_DIR / "run_alternatives_seeds0-9_r8.out").read_text(encoding="utf-8").splitlines()
    if re.match(r"^alt\d: ", line)
]
alt_status = "; ".join(alt_lines)
alts_all_pass = len(alt_lines) == 5 and all("PASS (10/10 seeds)" in line for line in alt_lines)

# ----- round-7 ids (all must be carried or re-decided) --------------------------------------------------------------------
r7_ids = [r["id"] for r in json.loads(ROUND7.read_text(encoding="utf-8"))["rows"]]

rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> None:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        assert fix, rid
        item["fix"] = fix
    rows.append(item)


GATES = f"{S}gates_r8.out"
ASCII = ""

# 2.9 prose and links
row("E3e-01", "2.9 banned strings in learner-visible prose; ellipsis outside code",
    "course/modules/E/E3/project.html; index.html; L01-L08.html", "PASS",
    f"{S}prose_scan_r8.py (section 1): the BUILDER_RULES 1.3-1.4 patterns of tools/check_pages.py:58-74 plus U+2026 and "
    "'it can be shown', matched over visible prose with script, style, pre and math removed: zero BANNED hits. "
    f"check_pages --unit E3 PASS in {GATES}.")
row("E3e-02", "2.9 process words in learner text",
    "course/modules/E/E3/project.html; L02-L08.html; index.html", "PASS",
    f"{S}prose_scan_r8.out section 1: PROCESS hits are 'round'/'rounds' (rounding), 'resolved' (a gamble resolved at a date) "
    "and 'pin down' (statistical idiom) only; no builder, verifier, ledger, round or pin reference in learner prose.")
row("E3e-03", "2.9 process references in learner-visible code and docstrings",
    "course/modules/E/E3/grader/*.py; tests/labs/E3/lab-E3-project-1..3.py", "PASS",
    "grep -n -i -E 'verifier|builder|mutant|fragment|ledger|architect|ruling|round [0-9]|fixer|reviewer|slice' over "
    "grader/*.py, the three project twins and project.html: no hit. 'pin down' and 'before running' (project.html:393, :706) "
    "are statistical wording.")
row("E3e-04", "2.9 links and anchors on project and hub pages; concept links resolve",
    "course/modules/E/E3/*.html", "PASS",
    f"{S}links_r8.py -> {S}links_r8.out: 185 local hrefs checked, 0 problems (each file exists, each fragment is an id on "
    "its file, each concept link targets its <dfn id=def-X> or a concepts.html anchor).")
row("E3e-05", "2.6 structure and ladder order",
    "course/modules/E/E3/project.html:40-48 (ladder), 201 (spec), 243 (questionnaire), 356 (budget), 374 (autograder), "
    "387 (report), 747 (stretch), 755 (reading)", "PASS",
    "Re-read project.html in full: four rungs in order (ladder :43-48); rung 1 (:44, changed this round) is still a fully "
    "solved, annotated worked example (lab-E3-project-1, why comments at tests/labs/E3/lab-E3-project-1.py:58-137); spec, "
    "questionnaire, budget, autograder, report, stretch and reading sections follow in that order. check_projects --unit E3 "
    f"PASS in {GATES}.")
row("E3e-06", "2.6 hours arithmetic",
    "project.html:33 (data-hours-project=14), :362-368 (table id=hours); index.html:29 (data-hours-lessons=56)", "PASS",
    carry("project.html:33 and :362-368 and index.html:29",
          "hours 1+1+3+4+3+2 = 14 equals data-hours-project and the hub total 56 + 14 = 70 equals the curriculum 70."))
row("E3e-07", "2.6 rung 3 scope matches curriculum brief",
    "project.html:205-215; curriculum/02-economics-finance-core.yaml:116-123", "PASS",
    carry("project.html:205-215 and curriculum/02-economics-finance-core.yaml",
          "spec lines are outside the delta hunks (:44, :221, :720, :757)."))
row("E3e-08", "2.6 spec completeness (a competent student needs no clarifying question)",
    "project.html:203-215 (spec), :220-225 (conventions); grader/starter.py", "PASS",
    "Re-read this round. The new whole-cents rule (project.html:221) states the one exception the reference uses "
    "(reference.py:122-124, exact Fraction sum at gamma = 0 under crra), so a student has what is needed. Signatures in "
    "grader/starter.py match the spec at :209.")
row("E3e-09", "2.6 rubric C1 observable",
    "project.html:611 (C1 row)", "PASS",
    carry("project.html:611 and the rubric table", "the C1 descriptors are observable (count, scale, pair listing, probabilities)."))
row("E3e-10", "2.6 rubric C5 observable; exemplar annotations match descriptors",
    "project.html:616 (C5 row); :684-738 (exemplar B annotations)", "PASS",
    "Re-read project.html:684-738 after the change at :720. Each annotation's level matches the descriptor it cites "
    "(for example :722 'states no direction of bias for either limit' is the level-4 C4 descriptor's negation); see E3e-12.")
row("E3e-11", "2.6 rubric structure: five criteria, four levels; data-criterion and data-level present",
    "project.html:607-617 (table id=rubric); :623-738 (exemplars)", "PASS",
    "table#rubric has rows C1-C5 with data-criterion and four level cells (:611-615); exemplar-a data-level=2 (:623), "
    "exemplar-b data-level=3 (:676). The mismatch of exemplar-b with plans/E3-build-plan.md:392 is row E3e4-exemplar-B-level.")
row("E3e-12", "2.6 calibration: exemplar scores within one level of annotations (blind scoring)",
    "project.html:609-615 (rubric text), :623-674 (exemplar A), :676-738 (exemplar B)", "PASS",
    "Blind scoring from the rubric text alone, annotations hidden. Exemplar A: C1 2 (count and scale, no pair), C2 2 (no "
    "per-response term), C3 1 (no standard error), C4 2 (one limit), C5 1 (no grade or key) = data-scores 2,2,1,2,1. "
    "Exemplar B: C1 3 (two pairs, not all twelve), C2 3 (precision identification a hypothesis), C3 4 (SE, convergence, "
    "sample size, unreliable case), C4 3 (no direction of bias), C5 3 (Lab 3 results without key) = data-scores 3,3,4,3,3. "
    "Each matches its annotations exactly.")
row("E3e-13", "2.2 word counts quoted for exemplars (memo text, headings included, tags removed)",
    "course/modules/E/E3/project.html:621", "PASS",
    f"{S}prose_scan_r8.out section 2: exemplar-a memo blocks 117 words, exemplar-b 435 words (headings included, tags "
    "removed, whitespace runs); the page states 117 and 435.")
row("E3e-14", "2.2 numbers in prose, exemplars, lab expected blocks and grader docstrings re-derived",
    "project.html:53, :57, :138, :143, :147, :148, :383-386, :571-578, :610-721; grader/test_project.py seed-49 doc", "PASS",
    f"run_labs E3 11/11 in {GATES} (Lab 1 :141-147 vs :57, :148; Lab 2 :193-196 vs :153; Lab 3 :582-588 vs :583-585, :589, "
    ":641, :706, :717). Lab 3 values from the twin output: gamma 0.6352, lambda 6.1503, kappa 2.0201, SE 0.32, 9.59, 1.86, "
    "log-likelihood -7.1445, largest score 3.55e-10 (unchanged lines). Grader seed-49 docstring: outside the delta.")
row("E3e-15", "2.1 reading list: registry keys and which lessons cite which key (round-7 FAIL, now fixed)",
    "project.html:757 (reading paragraph), :759-763; L02.html:616; L07.html:80; L08.html:67,133; L05.html:609; index.html:166", "PASS",
    f"{S}prose_scan_r8.out section 4 (grep of data-cite and key names): pratt1964risk appears in L02.html:616 (reference "
    "note, no data-cite) and in no claim; kahneman1979prospect is attached to L07.html:80 (grade C); ellsberg1961risk to "
    "L08.html:133 (C); gilboa1989maxmin to L08.html:67 (C); epstein1989substitution only as a name at L05.html:609. The "
    "project.html:757 sentence now reads 'lists pratt1964risk in its references without attaching it to a claim', which "
    "matches L02.html:616. Round-7 FAIL resolved.")
row("E3e-16", "2.1 attribution: titles and keys match registry records",
    "project.html:755-765; L02.html:616; L07.html:80; L08.html:67,133,619-620; references/references.json (five E3 keys)", "PASS",
    "references/references.json: pratt1964risk 'Risk Aversion in the Small and in the Large', Econometrica 32(1-2) (1964), "
    "matches L02.html:616; kahneman1979prospect 'Prospect Theory: An Analysis of Decision under Risk' contains the phrase "
    "'prospect theory' (L07.html:80 claim is true); ellsberg1961risk 'Risk, Ambiguity, and the Savage Axioms' contains "
    "'ambiguity' (L08.html:133 true); gilboa1989maxmin 'Maxmin expected utility with non-unique prior' contains 'maxmin "
    "expected utility' (L08.html:67 true). Each claim carries data-locator 'registry record: title only; paper not read'. "
    "Grade C is conservative for a bibliographic fact and is not a mismatch with BLUEPRINT's table.")
row("E3e-17", "2.4 definitions and results cited from the project page exist",
    "project.html:53, :210, :213, :220, :222; L02.html:99; L03.html:173; L06.html:61, :68", "PASS",
    carry("project.html:53, :210, :213, :220, :222 and L02, L03 (other than :564), L06",
          f"the concept links resolve (links_r8.out, 0 problems); Lesson 3 Proposition 2.7 is the affine-invariance result (L03 text)."))
row("E3e-18", "2.5 Lab 1 prose vs code and output",
    "project.html:55-149; tests/labs/E3/lab-E3-project-1.py", "PASS",
    f"run_labs E3 11/11 ({GATES}). Output pair 2 'CRRA cents A, B: 3000 -513 | prospect cents A, B: 3000 -762' matches the "
    "prose at project.html:148 ($30.00 sure; $40 with probability 1/4, -$20 with probability 3/4). Docstring units (cents, "
    "units of $100) match the functions.")
row("E3e-19", "2.5 Lab 1 hypothesis numbers vs expected block",
    "project.html:57, :141-147", "PASS",
    f"Expected before-run numbers at :57 (496, 500, -30, 500, P(A)=0.480149, -0.733658, -2.302315) equal the expected block "
    f"at :141-147; run_labs E3 11/11 ({GATES}).")
row("E3e-20", "2.5 Lab 2 hypothesis numbers and completed formulas",
    "project.html:153-197; tests/labs/E3/lab-E3-project-2.py", "PASS",
    f"run_labs E3 11/11 ({GATES}) reproduces -0.765595182 (A) and -0.625595182 (B) and the completion rule; unchanged lines.")
row("E3e-21", "2.5 Lab 3 estimates, standard errors, score, log-likelihood, interpretation",
    "project.html:391-589; tests/labs/E3/lab-E3-project-3.py", "PASS",
    f"run_labs E3 11/11 ({GATES}); lines 391-589 are outside the delta. {S}exemplar_b_facts_r8.out: 12 answers, 11 with a mixed "
    "lottery, matching the hypothesis at :393.")
row("E3e-22", "2.5 lab and code gates for project labs and grader",
    "tests/labs/E3/lab-E3-project-1..3.py; course/modules/E/E3/grader/", "PASS",
    f"{GATES}: run_labs E3 11/11; run_graders E3 0-49 50/50; page_smoke project PASS; ruff check and ruff format on the E3 "
    "course and labs clean; mypy --no-incremental 385 files clean; pytest tests/test_labs.py -k E3 green.")
row("E3e-23", "2.4 mathematics on the page: conventions, identification, delta-method SE convention",
    "project.html:213-224 (conventions bullets)", "PASS",
    "Identification (:223): the gain branch of v does not contain lambda, and the loss branch is -lambda(-x)^(1-gamma); "
    "inverting the loss branch of W = -lambda * sum p (-x)^(1-gamma) gives c = -(-W/lambda)^(1/(1-gamma)), so lambda cancels "
    "exactly when all prizes have one sign (re-derived). Delta method (:224): SE(g(xi)) ~ |g'(xi)| SE(xi) is the standard "
    "first-order rule, and grader/reference.py:5-8 uses it. Choice probability (:222): logistic in z = kappa dCE/10000, "
    "units of $100 (matches choice_probability_a in the Rung 1 twin).")
row("E3e-24", "2.4 notation: symbols and macros on the slice vs notation/notation.json",
    "project.html (math spans); L01-L08 and index (macros); notation/notation.json", "PASS",
    f"{S}prose_scan_r8.out section 3 and {S}symbol_contexts_r8.py output: registered macros used (\\E, \\Prob, \\Var, \\R, "
    "\\indic) keep their registered meaning; \\Phi (project.html:750) is the standard normal CDF, as registered in the symbols "
    "list (module M4); T (number of observations) is not used as math (the two 'T =' hits are Python identifiers in "
    "L02 and L04 twins); R^\\ast (AP1) is not used; lambda^\\ast (L06) is a local threshold, not R^\\ast; gamma is risk "
    "aversion, which notation.json reserves as free; alpha and delta are defined in L06 Definition 1.2; tau is defined in "
    "L08 Section 3; varpi is defined in its exercise; Gamma (L07 E2) is the lab's local name for V_omega, stated on the page.")
row("E3e-25", "2.9 DAG in prose: concepts outside the prerequisite closure",
    "project.html (visible text, meta description); L02-L08", "PASS",
    f"check_dag --unit E3 PASS ({GATES}); links_r8.out (every concept link resolves). The new L07 text names 'the mean value "
    "theorem' in plain prose with no link and no dfn (L07.html:88), which the architect default permits for a concept outside "
    "the closure (plans/E3-build-plan.md, Architect decisions).")
row("E3e-26", "2.9 terms used before definition on the project page",
    "project.html:53, :205, :213, :220, :223, :224", "PASS",
    carry("project.html:53, :205, :213, :220, :223, :224",
          "the logit rule at :53 is a linked forward reference to the convention at :222, as the sentence says."))
row("E3e-27", "2.4 scope words carry a computation or hypothesis (changed prose)",
    "project.html:44, :221; L02.html:209; L04.html:176, :493, :579; L07.html:88, :92; L08.html:425, :697", "PASS",
    "project.html:221 'No other rounding is applied': reference.py rounds once on every other path (_half_up at :100-127 and "
    "the prospect return). project.html:44 'not generated from the parameters': the answers are literal in "
    "tests/labs/E3/lab-E3-project-1.py (pairs list at :54-58). L02.html:209 'under u = w the premium is zero at each scale "
    "that Part A and Part C print': lab output 'linear_premium_cents 0' at eps 1, 0.5, 0.1. L04.html:176 and :493: the test "
    "set is the proof witnesses at support points (L04.html:98, :150) plus three CRRA utilities (lab lines 108-120, 176-198). "
    "L07.html:92 'finite checks on the grid, not theorems': lab part A prints the two facts (see E3e-58). L08.html:425: "
    "remark 4.2 gives E[1/w] = p/w1 + (1-p)/wL, affine in p (checked, E3e-59).")
row("E3e-28", "2.6 autograder claims stated on the page (tolerances and oracles)",
    "project.html:213; grader/test_project.py:151-212, :423-430, :535-541, :543-568, :571-584, :585-602, :603-629", "PASS",
    carry("grader/test_project.py (its only delta hunks are at :251-288, messages only; `git diff 9373ef39 2d755599 -- "
          "course/modules/E/E3/grader/test_project.py` shows the same expect() conditions with new message text)",
          "the tolerance lines cited are unchanged."))
row("E3e-29", "2.6 reference passes the suite on seeds 0-49",
    "course/modules/E/E3/grader/reference.py; tools/run_graders.py --unit E3 --seeds 0-49", "PASS",
    f"{GATES}: 'run_graders E3: PASS (reference 50/50 seeds, slowest 16.3 s)'.")
row("E3e-30", "2.6 mutation: re-run all existing mutants on seeds 0-9",
    "ledgers/E3/mutants/ (113 files: 112 at the pin plus r8_01 written this round; e8e_02 and e8e_03 are killed separately); tools/mutate_graders.py --unit E3 --seeds 0-9",
    "PASS",
    f"{S}mutate_E3_seeds0-9_r8.out: 'mutate_graders E3: PASS (113/113 killed)', exit 0; every KILLED line names the test "
    "that kills it.")
row("E3e-31", "2.6 at least three NEW student-error mutants written by the verifier, each killed",
    "ledgers/E3/mutants/r8_01_*.py, e8e_02_*.py, e8e_03_*.py", "PASS",
    f"Three new round-8 mutants, each a complete elicit.py with a first-line docstring: r8_01 (gamma = 0 CRRA sums floats: a "
    "float sum misrounds an exact half, e.g. prizes [-1169, 7186] with probabilities 5/6, 1/6 give 223 where the rule "
    f"gives 224; {S}float_half_search_r8.py), killed by test_crra_gamma_zero_is_expected_final_wealth_exactly; e8e_02 (model "
    "name lookup raises KeyError), killed on 50 of 50 seeds by test_model_name_must_be_crra_or_prospect; e8e_03 (gamma = 0 "
    "rounds the exact half down), killed on 50 of 50 seeds by test_crra_gamma_zero_is_expected_final_wealth_exactly. "
    f"Kill outputs: {S}kill_new_e8e_r8.out and {S}mutate_E3_seeds0-9_r8.out.")
row("E3e-32", "2.6 five alternative correct implementations pass (over-constraint check)",
    "ledgers/E3/scripts/run_alternatives.py (alt1..alt5); ledgers/E3/scripts/E3-e-r8/run_alternatives_seeds0-9_r8.out", "PASS"
    if alts_all_pass else "FAIL",
    f"{S}run_alternatives_seeds0-9_r8.out: {alt_status}")
row("E3e-33", "2.6 test count on the page equals the collect-only count",
    "project.html:213 ('runs 46 checks'); grader/test_project.py", "PASS",
    "pytest --collect-only -q on the suite with reference.py as elicit.py: '46 tests collected' (run this round, scratch copy "
    "under /var/folders, repository copy untouched); page says 46; page_smoke in-browser 'All 46 tests pass' "
    f"({GATES}).")
row("E3e-34", "2.6 exception table: conditions, types and message text",
    "project.html:232-238; grader/reference.py:28-60, :116-121; test_project.py:287-386, :630-638", "PASS",
    carry("project.html:232-238 and grader/reference.py", "the table rows and the message texts are unchanged."))
row("E3e-35", "2.8 figures on the page",
    "course/modules/E/E3/project.html (no svg or figure); L02-L08 (page_smoke sweep)", "PASS",
    f"grep: project.html contains no <svg> or <figure>. {GATES}: page_smoke passes on L02, L03, L04, L07, L08 "
    "(zero console errors, no unrendered math, no overflow at 360 px).")
row("E3e-36", "2.1 registry integrity for the five E3 keys (offline gate)",
    "references/references.json; tools/verify_refs.py --offline", "PASS",
    f"{GATES}: 'offline integrity: 560 entries, 0 problems'.")
row("E3e-37", "2.9 questionnaire and privacy claims",
    "project.html:245, :247, :273-353, :376, :778; course/assets/js/grader.js; rubric.js", "PASS",
    carry("project.html:245, :247, :273-353, :376, :778 and the two JS files",
          "those lines are outside the delta hunks (:44, :221, :720, :757)."))
row("E3e-38", "2.6 rung 4 is open-ended and not graded",
    "project.html:747-753", "PASS", carry("project.html:747-753", "the stretch section is outside the delta hunks."))
row("E3e-39", "2.6 suite gap: named probability condition for log_likelihood",
    "grader/test_project.py:458-507", "PASS", carry("grader/test_project.py:458-507", "the test body is outside the delta hunks."))
row("E3e-40", "2.2 numbers quoted in grader docstrings (seed-49 standard errors and reverse-order shifts)",
    "grader/test_project.py seed-49 docstring (test_standard_errors_match_the_coordinate_change_oracle)", "PASS",
    carry("grader/test_project.py", "the seed-49 docstring is outside the delta hunks (:251-288)."))
row("E3e-41", "2.6 equivalent-mutant README for a survivor",
    "ledgers/E3/equivalent/ (absent at pin 2d755599)", "PASS",
    f"{S}mutate_E3_seeds0-9_r8.out: no survivor (113/113 killed), so no mutant is equivalent-only and no equivalent/ README is "
    "needed. The directory does not exist at the pin.")
row("E3e-42", "2.4 rename consistency (zeta, kappa, lambda, gamma, xi)",
    "project.html:203, :213-214, :224; grader/*.py; tests/labs/E3/lab-E3-project-3.py", "PASS",
    carry("project.html:203, :213-214, :224 and the grader files", "those lines are outside the delta hunks."))
row("E3e-43", "2.2/2.6 instance docstring vs code (grader/instance.py)",
    "course/modules/E/E3/grader/instance.py:11-14, :17-19", "PASS",
    carry("grader/instance.py", "the file is not in the round-8 delta (git diff --stat 9373ef39..2d755599)."))
row("E3e-44", "2.6 dominance witnesses and verdict oracle",
    "grader/test_project.py:1106-1165 (FOSD and SOSD tests)", "PASS",
    carry("grader/test_project.py:1106-1165", "the lines are outside the delta hunks."))
row("E3e-45", "2.6 failure messages name the property and do not leak the answer",
    "grader/test_project.py:44-63 and every expect()/must_raise call; the round-8 message changes at :251-288", "PASS",
    "The 26-line round-8 delta changes messages only: 'with lambda = 2 a loss weighs more than a gain of the same size: follow "
    "the loss weight' (no -25), 'an exact half cent just above zero must go toward plus infinity: the rule is floor(c + 1/2)' "
    "(no answer), and the others name the rule. Other messages carried from round 7.")
row("E3e-46", "2.6 same suite passes in Pyodide and locally",
    "tools/page_smoke.py --unit E3 --pages project", "PASS",
    f"{GATES}: page_smoke project PASS, 'in-browser grader: All 46 tests pass'; run_graders local 50/50.")
row("E3e-47", "2.6 hours: verifier's estimate of each deliverable vs the declared 14 hours (30 percent band)",
    "project.html:362-368", "PASS",
    carry("project.html:362-368", "the table is outside the delta hunks; the verifier's component estimates (engine with the "
          "exact rules and the logit MLE, instrument, report) sit within 30 percent of 14 hours as in round 7."))
row("E3e-48", "2.8 SIMULATED labels where generated data is used; no real data",
    "project.html:44, :53, :57, :376, :393, :396, :549-589; grader/instance.py:1", "PASS",
    "project.html:44 names the SIMULATED participant; :53, :57, :376, :393, :396 label the generated data; instance.py:1 "
    "states it is SIMULATED.")
row("E3e-49", "2.9 page_smoke: console errors, unrendered math, external requests, 360 px",
    "course/modules/E/E3/project.html and L02, L03, L04, L07, L08", "PASS",
    f"{GATES}: page_smoke --unit E3 --pages project L02 L03 L04 L07 L08, all PASS.")
row("E3e-50", "2.6 over-constraint: a correct implementation that the SE or suite wrongly rejects",
    "grader/test_project.py:918-950 (SE oracle); ledgers/E3/scripts/run_alternatives.py", "PASS" if alts_all_pass else "FAIL",
    f"alternatives: {alt_status}; the SE oracle lines are outside the delta.")
row("E3e4-gates", "Repository gates for the E3 project slice (pin 2d755599)",
    "tools/check_pages.py --unit E3; check_dag.py; check_projects.py; run_labs.py; verify_refs.py --offline; run_graders.py; "
    "page_smoke.py; ruff; mypy; pytest tests/test_labs.py -k E3", "PASS",
    f"{GATES} (exit codes all 0; check_pages, check_dag, check_projects PASS; run_labs E3 11/11; verify_refs 560/0; "
    "run_graders 50/50; page_smoke PASS; ruff clean; mypy 385 files; pytest green). The full repository gate (every unit) was "
    "not run; this slice's gates are the E3 ones.")
row("E3e4-exemplar-B-level", "Exemplar levels match the binding plan (exemplar-a level 2, exemplar-b level 4)",
    "course/modules/E/E3/project.html:676 (data-level=3); plans/E3-build-plan.md:392 (exemplar-b data-level 4)", "FAIL",
    "project.html:676 still reads data-level=\"3\" (the round-8 delta does not touch it) and the page's own verdict (:678) says "
    "exemplar B 'falls short of level 4' on C1, C2, C4 and C5. plans/E3-build-plan.md:392 still reads "
    "'exemplar-b (data-level=\"4\")'. plans/FINAL-ARCHITECT-RULINGS.md ruling 7 and plans/E3-open-items.md:145-149 amend only "
    "the length, not the level. Exemplar-a level 2 matches.",
    "Architect decision needed: (a) rewrite exemplar B so it meets level 4 on all five criteria (all twelve pairs in cents "
    "with exact probabilities, the precision identification stated as a result, a direction of bias for each limit, a key or "
    "derivation for each Lab 3 result), then set data-level=\"4\" and data-scores at project.html:676; or (b) record a ruling "
    "that exemplar B is level 3 and amend plans/E3-build-plan.md:392 to data-level \"3\".")
row("E3e4-C2-observability", "Rubric level descriptors observable (C2)",
    "project.html:612, :630-634, :695-699", "PASS",
    carry("project.html:612, :630-634, :695-699", "the C2 descriptors and exemplar C2 annotations are outside the delta."))
row("E3e4-lab3-rederive", "Lab 3 numbers re-derived independently",
    "project.html:391-589; tests/labs/E3/lab-E3-project-3.py", "PASS",
    carry("project.html:391-589 and tests/labs/E3/lab-E3-project-3.py",
          f"run_labs E3 11/11 ({GATES}) reproduces every printed Lab 3 value."))
row("E3e4-prizes-mixed", "Exemplar B instrument facts (prize range, prizes per lottery, probabilities sum to 1, pair facts)",
    "project.html:680-698", "PASS",
    f"{S}exemplar_b_facts_r8.out (reads the ANSWERS literal of tests/labs/E3/lab-E3-project-3.py): prize range -18700 to "
    "19000; 2 or 3 prizes per lottery; every probability list sums to exactly 1; 11 of 12 answers have a mixed lottery "
    "(answer 4 has none); pair 0 and pair 3 as described.")
row("E3e4-identification", "Identification claims (lambda identified only by mixed lotteries; precision claim labelled)",
    "project.html:213, :223, :694, :717", "PASS",
    "Re-derived under E3e-23. The precision identification (:694, :717) is labelled 'a hypothesis for you to test', not a result.")
row("E3e4-cross-refs", "Cross-references to lessons (Lesson 3 Proposition 2.7; Lesson 6 Definitions 1.2 and 1.3; Lesson 2 Proposition 1.3)",
    "project.html:53, :210, :220; L03.html:173; L06.html:61, :68; L02.html:99", "PASS",
    carry("project.html:53, :210, :220, L03.html:173, L06.html:61, :68, L02.html:99",
          "L03 changed only at :564 (references), and the links resolve (links_r8.out)."))
row("E3e4-attribution-titles", "Attribution of lesson statements about reading-list papers (title-only claims)",
    "course/modules/E/E3/L07.html:80; L08.html:67, :133, :619-620", "PASS",
    "Verified against references/references.json titles (see E3e-16).")
row("E3e4-stretch-phi", "Stretch probit link: Phi against the registry",
    "project.html:750; notation/notation.json (Phi, module M4)", "PASS",
    "project.html:750 defines Phi as the standard normal distribution function; notation.json symbols list gives "
    "'\\Phi, \\Phi^{-1}: standard normal CDF and its inverse' (M4). Same meaning.")
row("E3e4-ruling-392", "Plan's exemplar wording agrees with the architect ruling on excerpts",
    "plans/E3-build-plan.md:392; plans/E3-open-items.md:145-149; plans/FINAL-ARCHITECT-RULINGS.md ruling 7", "PASS",
    "plans/E3-build-plan.md:392 says the exemplars are 'excerpts of memos, not full reports', as the open-items ruling (:145-149) "
    "and FINAL ruling 7 require. The level conflict on the same line is row E3e4-exemplar-B-level.")
row("E3e5-01", "Rung 1 worked example: each step carries a why note (plan 6.1 item 1)",
    "tests/labs/E3/lab-E3-project-1.py:58-137; project.html:55-57, :138", "PASS",
    carry("tests/labs/E3/lab-E3-project-1.py and project.html:55-57", "the lab is unchanged; the rung text at :44 changed only in its participant wording (E3e-r8-01)."))
row("E3e5-02", "Grader test file type-clean under mypy --strict (BUILDER_RULES 6.1 and 6.2)",
    "course/modules/E/E3/grader/test_project.py", "PASS",
    f"{S}mypy_strict_grader_r8.out: 'Success: no issues found in 1 source file' for test_project.py with reference.py as "
    "elicit.py and instance.py in a scratch copy (run this round after the message edits).")
row("E3e5-03", "Lab-E3-project-3 calls the engine on the reference case (plan 6.1 item 3, binding)",
    "tests/labs/E3/lab-E3-project-3.py; course/modules/E/E3/project.html:391-399; plans/E3-build-plan.md:292; "
    "plans/E3-open-items.md section 3 item 2", "FAIL",
    "plans/E3-build-plan.md:292 requires lab-E3-project-3 to call the engine and print the estimates. The twin defines its own "
    "value, certainty_equivalent, grid_start, second_order_search and observed_information (tests/labs/E3/lab-E3-project-3.py:"
    "35-149) and calls no engine. plans/E3-open-items.md (section 3 item 2) records the deviation (a lab cannot import the "
    "learner's module, and grader/reference.py is excluded from deployment). No FINAL ruling accepts it.",
    "Architect ruling needed: accept the twin form (it reproduces the reference numbers; the learner's engine cannot be "
    "imported in the browser) and amend plans/E3-build-plan.md:292 to say so, or require a different lab design. Do not change "
    "the twin without that ruling.")
row("E3e5-04", "Prospect model extends Lesson 6 Definition 1.3 (p_i > 0) to zero-probability prizes",
    "project.html:220, :225; course/modules/E/E3/L06.html:68-69", "PASS",
    carry("project.html:220, :225 and L06.html:68-69", "the lines are outside the delta hunks."))
row("E3e5-05", "Hub ladder text agrees with the spec (index.html:146 vs project.html:207, :213)",
    "course/modules/E/E3/index.html:146; project.html:207, :213", "PASS",
    carry("index.html:146 and project.html:207, :213", "the lines are outside the delta hunks."))
row("E3e6-01", "Lab-E3-project-3 docstring describes code that exists (rung-3 twin instructions)",
    "tests/labs/E3/lab-E3-project-3.py:4-6 (embedded at project.html:398-399)", "PASS",
    carry("tests/labs/E3/lab-E3-project-3.py", "the twin is unchanged in the delta."))
row("E3e-51", "2.2/2.6 docstring number in the new grader test (test_estimate_counts_a_mixed_lottery_whether_or_not_it_was_chosen)",
    "course/modules/E/E3/grader/test_project.py:806-815 (docstring 'standard errors above 10^5')", "FAIL",
    f"{S}degenerate_se_r8.py -> {S}degenerate_se_r8.out: the all-A set built from the test's own B_SIDE_SURE_A and "
    "B_SIDE_LOTTERIES gives kappa_hat 924.73, se_gamma 692.39, se_lambda 692051.98, se_kappa 1981269.33 with reference.py. "
    "'standard errors above 10^5' is false for gamma (692.39); it holds only for lambda and kappa. Still open at the pin.",
    "In course/modules/E/E3/grader/test_project.py docstring of test_estimate_counts_a_mixed_lottery_whether_or_not_it_was_chosen, "
    "change 'standard errors above 10^5' to 'standard errors of lambda and kappa above 10^5 (se_gamma about 692)'. The grader "
    "test file is another slice's to edit; reported only.")
row("E3e-52", "2.6 new grader fixture facts: the whether-or-not-chosen test's B-side lotteries are mixed",
    "course/modules/E/E3/grader/test_project.py:780-806 (B_SIDE_SURE_A, B_SIDE_LOTTERIES)", "PASS",
    carry("grader/test_project.py:780-806", "the fixtures are outside the delta hunks."))
row("E3e-53", "2.6 new zero-prize test: a gain and a zero prize is not mixed (test_estimate_needs_a_mixed...)",
    "course/modules/E/E3/grader/test_project.py:696-714", "PASS",
    carry("grader/test_project.py:696-714", "the test body is outside the delta hunks."))
row("E3e-54", "2.6 round-7 verifier mutants: three new student-error mutants, each killed",
    "ledgers/E3/mutants/r7_01_*.py, r7_02_*.py, r7_03_*.py", "PASS",
    f"{S}mutate_E3_seeds0-9_r8.out lists each r7 mutant as KILLED (113/113).")
row("E3e-55", "2.4 round-7 Lesson 2 prose: A4 wording, Lab 1 Part A premium, Problem P2 claim, references",
    "course/modules/E/E3/L02.html:84, :136, :381, :399, :616", "PASS",
    carry("L02.html:84, :136, :381, :399", "those lines are outside the one delta hunk (:209); :616 re-read this round, see E3e-15."))
row("E3e-56", "2.4 round-7 Lesson 3 references: Module M1 results cited (round-8 change at :564)",
    "course/modules/E/E3/L03.html:564; course/modules/M/M1/L03.html:60, :92, :112-116", "PASS",
    "The round-8 wording cites M1 L03 Proposition 1.4, Proposition 1.6(b), its addition rule (A2) and the uniqueness in A3. "
    "Read in course/modules/M/M1/L03.html: A2 (addition) at the assumptions block; A3 (inverse: exactly one real x with e^x = y); "
    "Proposition 1.4 (ln(e^x) = x); Proposition 1.6(b) (ln(ab) = ln a + ln b). L03 Proposition 2.4's proof uses 'ln c = m "
    "exactly when c = e^m' by Proposition 1.4 and the uniqueness in A3 (course/modules/E/E3/L03.html, the proof before Example "
    "2.5). All cited results exist with those statements.")
row("E3e-57", "2.5 round-7 Lesson 4 prose: Example 2.5 wording, interpretation counts, E1 and E2 (round-8 changes at :176, :493, :573-579)",
    "course/modules/E/E3/L04.html:52, :165-172, :176, :485, :493, :573-579, :591", "PASS",
    f"Changed hunks re-verified against the twin output printed this round (python -I -W error tests/labs/E3/lab-E3-L04-1.py: "
    "'FOSD verdicts over the 24 pairs: X dominates Y 3, Y dominates X 10, identical 1, no ranking 10'; SOSD over 8 equal-mean "
    "pairs; named pair B integrated Y at 4000 = 500), and run_labs E3 11/11 in " + GATES + " checks the page blocks. "
    "E2 now says 'first-order verdicts (labelled FOSD in its output)' and the output labels them FOSD. Unchanged cited lines "
    "carried from round 7.")
row("E3e-58", "2.2 round-7 Lesson 7 numbers: omega values, weighted-value counterexample, and Example 1.4 (round-8 change at :86-92)",
    "course/modules/E/E3/L07.html:86, :88, :92, :98, :127, :334, :336-338, :505", "PASS",
    f"{S}l07_example14_r8.py -> {S}l07_example14_r8.out: closed form equals the general formula (max gap 3.331e-16); the new "
    "derivative matches central differences (max error 2.5e-8); omega(3/10) = 0.2857908849, omega(3/5) = 0.3912507700, "
    "omega(1/2) = 0.3535533906 = 1/(2 sqrt 2); nondecreasing on the 1001-point grid; in [0,1]; 1 sign change of omega - p "
    "between interior grid points; last grid point with omega > p is 0.278; 0 <= omega <= sqrt p <= 1. The derivative algebra "
    "(q g - 2p(1-2p) = q + 2p^2 using q^2 = p - p^2) re-derived by hand. Lines :127, :334, :336-338, :505 carried.")
row("E3e-59", "2.4 round-7 Lesson 8 prose: Definition 3.1, Proposition 3.2, Remark 4.2 (round-8 changes at :425 and :697)",
    "course/modules/E/E3/L08.html:142-160, :412-419, :425, :477, :496, :683, :697", "PASS",
    "Changed :425 says 'the expectation of 1/w is affine in p (Remark 4.2)'; Remark 4.2 says E_P[1/w] = p/w1 + (1-p)/wL is affine in "
    "p (Lesson 8 text). Model numbers re-derived: Model 1 CE = 1/(0.5/110000 + 0.5/95000) = 101951.22 cents; maxmin worst prior "
    "1/3 gives 1/(1/3/110000 + 2/3/95000) = 99523.81 cents; Model 2 change -107.23 cents (v(x) = sqrt x, -2 sqrt(-x) for "
    "W = 0.5*10 - 0.5*2 sqrt(50) = -2.0711, CE = -(1.0355)^2 = -1.0723 CU). Changed :697 option is the same statement, and "
    "the symmetry of the prior set {30/90..60/90} about 1/2 is checked. Definition 3.1 and Proposition 3.2 hunks unchanged.")
row("E3e-60", "2.1 round-7 hub reading paragraph and the Lesson 2 and 3 'name only' statements",
    "course/modules/E/E3/index.html:166; L01.html; L02.html:616; L03.html:564", "PASS",
    "index.html:166 unchanged (carried). L02.html:616 and L03.html:564 re-read this round (E3e-15, E3e-56). L01.html carried.")

# ----- round-8 rows for the new or changed subjects -----------------------------------------------------------------------
row("E3e-r8-01", "2.5 rung 1 text: 'answers written into the lab for this example, not generated from the parameters'",
    "course/modules/E/E3/project.html:44; tests/labs/E3/lab-E3-project-1.py:54-58", "PASS",
    "The participant's answers in the lab are literal ('A', 'B', 'A' in the pairs list), not drawn from gamma, lambda or kappa; "
    "the parameters enter only through the likelihood (lab lines 67-70, 119-136). The statement is true.")
row("E3e-r8-02", "2.4 whole-cents exception at gamma = 0 (crra): exact Fraction sum before the single rounding",
    "course/modules/E/E3/project.html:221; grader/reference.py:122-124; grader/test_project.py:146, :264, :281", "PASS",
    "reference.py:122-124 sums p*x as Fraction and returns floor(sum + 1/2), the rule the page states. The page's "
    "'no other rounding' holds (_half_up on the other crra and prospect paths). Test coverage: test :146 checks every "
    "instance lottery at gamma = 0 against nearest(expected prize); :281 checks the half-cent case. A float misrounding input "
    f"exists (prizes [-1169, 7186], probabilities 5/6 and 1/6: exact 447/2 gives 224, the float sum 223.49999999999977 gives "
    f"223; {S}float_half_search_r8.py), and mutant r8_01 is killed.")
row("E3e-r8-03", "2.5 exemplar B C4 misses text (round-8 change at :720)",
    "course/modules/E/E3/project.html:717, :720-722", "PASS",
    "The new text 'states no direction of bias for either limit' is true of the memo at :717, which names two limits and gives "
    "no direction of either. Consistent with the level-3 scoring of C4 (E3e-12).")
row("E3e-r8-04", "2.6 grader test messages changed at :251-288",
    "course/modules/E/E3/grader/test_project.py:251-288", "PASS",
    "git diff 9373ef39 2d755599 shows the same expect() conditions with new message text. Each message names the rule or property; "
    "none states the answer (-25, 25, 3, 1, 0). run_graders 50/50 PASS and page_smoke's in-browser suite passes 46 of 46.")
row("E3e-r8-05", "2.5 Lesson 2 hypothesis (:209): \\Var macro, numbers and predictions",
    "course/modules/E/E3/L02.html:209; tests/labs/E3/lab-E3-L02-1.py", "PASS",
    "Output of the twin (run here with python -I -W error): CE 9493 cents, premium 5.065835 CU vs approximation 4.500000 "
    "(gap 0.565835 > 0); premium/eps^2 at eps 1, 0.5, 0.25, 0.1, 0.01: 5.065835, 4.619495, 4.528811, 4.504565, 4.500046; gaps "
    "shrink (gaps_shrink_as_eps_falls True); linear utility premium 0 at eps 1, 0.5, 0.1. \\Var is registered in "
    "notation.json (\\operatorname{Var}). The prediction 'monotone pattern' is labelled as a numerical prediction.")
row("E3e-r8-06", "2.5 Lesson 4 hypothesis (:176) and :493 bullet: the test set is the proof witnesses at support points",
    "course/modules/E/E3/L04.html:98, :150, :176, :493; tests/labs/E3/lab-E3-L04-1.py:8-14, :108-120", "PASS",
    "Theorem 1.5 'If' uses u_t = 1{s > t} (L04.html:98); Theorem 2.3 'If' uses u_t = min(s - t, 0) (L04.html:150); the lab's "
    "test set is those utilities at each support point plus three CRRA utilities (lab lines 108-120 and 176-198). "
    "Lab output: FOSD and expected-utility verdicts agree on 24 of 24 pairs; SOSD on 8 of 8 equal-mean pairs; 10 of 24 "
    "pairs with no first-order ranking and 2 of 8 with no second-order ranking; the bullet's counts match.")
row("E3e-r8-07", "2.1 FINAL-ARCHITECT-RULINGS item 11 (rung 2 completion blanks) and the lab twin",
    "plans/FINAL-ARCHITECT-RULINGS.md:24-25; tests/labs/E3/lab-E3-project-2.py; course/modules/E/E3/project.html:151-198", "PASS",
    f"run_labs E3 11/11 ({GATES}) applies the completion rule: every page line equals the twin line or contains a blank. Item 11 "
    "is the rule the page follows; not a defect.")

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
missing = [i for i in r7_ids if i not in ids]
assert not missing, missing

verdict_rows = [r for r in rows if r["status"] != "PASS"]
fragment = {
    "unit": "E3",
    "slice": "e",
    "round": 8,
    "verifier": "Claude Haiku 5.5, independent verifier for E3-e, round 8 (did not build E3; read verifier-rules.md, "
                "VERIFIER_RULES.md, BUILDER_RULES.md, plans/E3-build-plan.md with architect decisions, plans/E3-open-items.md, "
                "plans/FINAL-ARCHITECT-RULINGS.md, and the round-7 fragment as context only)",
    "pin": "2d755599 (2d755599d8d74df292e3e43025f0458c4053802e)",
    "base": "9373ef39 (round-7 pin; round-7 fragment /Users/billyribeiro/.fanout/frags/D-E3-e.round7.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD8-E3-e",
    "scratch": "/tmp/e3e_r8/ and /tmp/e3e_r8_* (scratch copies only)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL" if verdict_rows else "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Delta 9373ef39..2d755599 inside the slice, read in full: project.html hunks at :44 (rung 1), :221 (whole cents at gamma 0), "
        ":720 (exemplar B C4 misses), :757 (reading paragraph); grader/test_project.py at :251-288 (messages only; expect() "
        "conditions unchanged); L02.html:209 (hypothesis, \\Var); L03.html:564 (references); L04.html:176, :493, :573-579 (hypothesis, "
        "bullet, E1 and E2); L07.html:86-92 (Example 1.4 derivative, Observation 1.5); L08.html:425, :697 (1/w affine wording); "
        "plans/FINAL-ARCHITECT-RULINGS.md item 11. instance.py, starter.py, reference.py and the lab twins of E3 are unchanged in the "
        "delta. Round-7 FAIL E3e-15 is now PASS. Round-7 FAILs E3e4-exemplar-B-level, E3e5-03 and E3e-51 remain (architect decisions "
        "and one docstring edit; no ruling or edit in the delta). cards.json is not in this slice and was not checked. "
        "Not run: the repository-wide gates for other units; the live verify_refs run (offline only); the full pytest suite (only "
        "tests/test_labs.py -k E3)."
    ),
    "summary": (
        f"{len(rows)} rows: {sum(r['status'] == 'PASS' for r in rows)} PASS, {len(verdict_rows)} non-PASS "
        f"(E3e4-exemplar-B-level, E3e5-03, E3e-51). Mutants: {mutant_kill_summary}. Alternatives: {alt_status}. Gates: "
        f"{GATES}. Scripts and outputs under ledgers/E3/scripts/E3-e-r8/."
    ),
}
out = ROOT / "ledgers/E3/E3-e.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
problems = ledger.validate(json.loads(out.read_text(encoding="utf-8")), "E3-e")
print("rows", len(rows), "non-PASS", [r["id"] for r in verdict_rows], "mutants", len(mutants))
print("validate:", problems)
