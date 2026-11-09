"""Round-15 fragment writer for E4 slice d (verifier output; the rows are this round's evidence).

Keeps every row id of the round-14 fragment (context only; its PASS rows are not carried): each id gets a row whose
evidence names this round's command output, script or locator. Adds the round-15 rows. Parses the 126 mutant results
from out/mutate_graders_E4_0_9_r15.txt. Writes ledgers/E4/E4-d.json and validates it with tools/ledger.py.
Usage: python -I write_fragment_r15.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(".").resolve()
OUT = ROOT / "ledgers/E4/scripts/E4-d-r15/out"
R14 = json.loads(Path("/Users/billyribeiro/.fanout/frags/E-E4-d.round14.json").read_text(encoding="utf-8"))

S = "ledgers/E4/scripts/E4-d-r15/"
CMD = {
    "E4d-cmd-check-projects": ("2.6-structure", "course/modules/E/E4/project.html; course/modules/E/E4/grader/",
        f"tools/check_projects.py --unit E4 -> 'check_projects E4: PASS', exit 0 ({S}out/check_projects.txt)."),
    "E4d-cmd-check-pages": ("2.9-structure", "course/modules/E/E4/project.html",
        f"tools/check_pages.py --unit E4 -> 'check_pages E4: PASS', exit 0 ({S}out/check_pages.txt)."),
    "E4d-cmd-check-dag": ("2.9-dag", "course/modules/E/E4/project.html",
        f"tools/check_dag.py --unit E4 -> 'check_dag E4: PASS', exit 0 ({S}out/check_dag.txt)."),
    "E4d-cmd-run-labs": ("2.5-labs", "tests/labs/E4/lab-E4-project-1.py, -2.py, -3.py",
        f"tools/run_labs.py --unit E4 -> 'run_labs E4: PASS (12/12)', exit 0 ({S}out/run_labs_E4.txt)."),
    "E4d-cmd-run-graders": ("2.6-autograder", "course/modules/E/E4/grader/reference.py",
        f"tools/run_graders.py --unit E4 --seeds 0-49 -> 'run_graders E4: PASS (reference 50/50 seeds)', exit 0 ({S}out/run_graders_E4_0_49.txt)."),
    "E4d-cmd-page-smoke-project": ("2.9-smoke", "course/modules/E/E4/project.html",
        f"tools/page_smoke.py --unit E4 --pages project (run alone; the first attempt passed a path, which matches no page, and is discarded) -> 'page_smoke E4: PASS'; in-browser grader 'All 48 tests pass' ({S}out/page_smoke_E4_project.txt)."),
    "E4d-cmd-ruff": ("gate", "course/modules/E/E4 and tests/labs/E4",
        f"ruff check -> 'All checks passed!'; ruff format --check -> '16 files already formatted' ({S}out/ruff_check.txt, ruff_format.txt)."),
    "E4d-cmd-mypy-workspace": ("gate", "tests/labs/E4 and course/modules/E/E4/grader",
        f"mypy --no-incremental on tests/labs/E4 and the grader -> 'Success: no issues found in 16 source files' ({S}out/mypy_E4.txt)."),
    "E4d-cmd-mypy-plan-command": ("gate", "tests/labs/E4; grader",
        f"Same mypy run as E4d-cmd-mypy-workspace (the plan command covers the same two paths): exit 0 ({S}out/mypy_E4.txt)."),
    "E4d-cmd-pytest-relevant": ("gate", "tests/test_memo_exemplars.py, test_page_checks.py, test_labs.py, test_run_labs.py",
        f"pytest -q tests/test_memo_exemplars.py tests/test_page_checks.py tests/test_labs.py tests/test_run_labs.py -> exit 0, no failures ({S}out/pytest_relevant_E4.txt)."),
    "E4d-cmd-verify-refs": ("2.1-citations", "references/references.json (E4 keys: muth1961rational, milgrom1982information)",
        f"tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' ({S}out/verify_refs_offline_all.txt); tools/verify_refs.py --unit E4 (live, Crossref/Open Library) -> 'live re-verification of E4: 3 of 560 entries, 0 problems' ({S}out/verify_refs_E4_live.txt)."),
    "E4d-cmd-collect": ("2.6-autograder", "course/modules/E/E4/grader/test_project.py",
        f"collect-only with the workspace of tools/run_graders.py (reference as solver.py): '48 tests collected', exit 0 ({S}out/collect_only_r15.txt). The page quotes 48 (project.html:320)."),
}

def lab(i):
    return (f"E4d-lab-project-{i}", "2.5-labs", f"course/modules/E/E4/project.html #lab-E4-project-{i}; tests/labs/E4/lab-E4-project-{i}.py",
        f"run_labs E4 PASS (12/12, {S}out/run_labs_E4.txt); the twin run alone under python -I -W error exits 0 with empty stderr and its stdout equals the page's expected block ({S}out/twin_project_{i}.out). Page code equals the twin (run_labs).")

FRESH = {}
for k, (chk, loc, ev) in CMD.items():
    FRESH[k] = dict(check=chk, location=loc, status="PASS", evidence=ev)
for i in (1, 2, 3):
    k, chk, loc, ev = lab(i)
    FRESH[k] = dict(check=chk, location=loc, status="PASS", evidence=ev)

NUM = f"{S}out/numbers_r15.txt (independent 60-digit closed forms, ledgers/E4/scripts/E4-d-r15/numbers_r15.py)"
FRESH.update({
 "E4d-num-lab-hypotheses": dict(check="2.2-numbers", location="course/modules/E/E4/project.html:57, :176, :376", status="PASS",
   evidence=f"Every number in the Lab 1 and Lab 2 hypothesis lines recomputed in {NUM}: Lab 1 gap +0.053092 / -0.080731, root 0.57937525, b_u/b_s -3.45199422, tau_bar=tau_y 0.18904110, informativeness 0.15898618; Lab 2 gap +0.037435 / -0.071386, root 0.57052263, informativeness 0.12466375. Lab 3 hypothesis numbers (0.5582, 0.6978, 0.8373; 0.1920, 0.1420, 0.0889; 484 box points) match the run output ({S}out/run_labs_E4.txt and the Lab 3 closed-form column)."),
 "E4d-num-exemplar-table": dict(check="2.2-numbers", location="course/modules/E/E4/project.html Exemplar B table and passage (:629-641)", status="PASS",
   evidence=f"Blind-stripped Exemplar B table (ledgers/E4/scripts/E4-d-r15/out/exemplars_stripped_blind.txt) has 9 rows; each fraction, informativeness and gap equals the Lab 3 printed expected block (project.html Lab 3 expected output). Ratios 0.6978/0.5582 = 1.25009 and 0.8373/0.5582 = 1.50000 from displayed values; unrounded ratio 1.25 follows from Prop 5 (lambda* = 2 sigma sqrt(tau_bar/(1-tau_bar)))."),
 "E4d-num-box-bounds": dict(check="2.2-numbers", location="course/modules/E/E4/project.html:314; course/modules/E/E4/grader/instance.py:14-17", status="PASS",
   evidence=f"tau_bar(0.150)=0.0976232722, tau_bar(0.120)=0.2375667836, 1/(1+4*0.75^2)=0.30769231 ({NUM}); page and instance.py quote 0.097623, 0.237567, 0.30769 and 0.09762327..., 0.23756678..., consistent. Box check: 484 of 484 points have gap(0)>0 and gap(1)<0 (run_labs Lab 3)."),
 "E4d4-exemplar-B-results-numbers": dict(check="2.2-numbers", location="course/modules/E/E4/project.html:629-641", status="PASS", evidence=f"Same as E4d-num-exemplar-table: every Exemplar B number equals the Lab 3 output ({S}out/run_labs_E4.txt)."),
 "E4d10-lab3-numbers": dict(check="2.5-labs", location="course/modules/E/E4/project.html:376-503", status="PASS", evidence=f"Lab 3 expected block equals its run output (run_labs E4 PASS) and the closed-form column equals the bisection to 2.1e-13 (largest difference line printed by the lab; {S}out/twin_project_3.out)."),
 "E4d13-exemplar-numbers-arith": dict(check="2.2-numbers", location="course/modules/E/E4/project.html Exemplar B Results passage (table and ratios)", status="PASS", evidence="Exemplar B Results passage re-read after the blind pass: counts, ratios and the 4e-14 bound are as stated (see E4d-num-exemplar-table)."),
 "E4d8-lab3-twin-page": dict(check="2.5-labs", location="course/modules/E/E4/project.html:377-503; tests/labs/E4/lab-E4-project-3.py", status="PASS", evidence=f"Page code equals the twin and the expected block equals the output ({S}out/run_labs_E4.txt; {S}out/twin_project_3.out)."),
 "E4d11-lab-page-twin": dict(check="2.5-labs", location="project.html lab blocks vs tests/labs/E4/lab-E4-project-{1,2,3}.py", status="PASS", evidence=f"run_labs E4 PASS (12/12) compares page code with each twin byte-for-byte (trailing newlines aside) ({S}out/run_labs_E4.txt)."),
 "E4d13-lab-twins-direct": dict(check="2.5-labs", location="tests/labs/E4/lab-E4-project-1.py, -2.py, -3.py", status="PASS", evidence=f"Each twin run as 'python -I -W error' in an empty scratch directory: exit 0, stderr 0 bytes ({S}out/twin_project_{{1,2,3}}.out)."),
 "E4d6-rung1-why": dict(check="2.9-prose", location="course/modules/E/E4/project.html:171 (Lab 1 interpretation)", status="PASS", evidence="Lab 1 interpretation read: each step's reason matches the code (step 2 sign check, step 3 halvings, step 4 root, step 5 ratio, step 6 closed form). The statement that the width is 2^-53 = 1.110e-16 from the 53rd halving on is arithmetic (2^-53) and matches the lab output 'bracket width 1.110e-16'."),
 "E4d7-lab1-bracket-width": dict(check="2.5-labs", location="course/modules/E/E4/project.html:171", status="PASS", evidence="Lab 1 prints 'after 60 halvings the bracket width is 1.110e-16' (expected block, run_labs PASS)."),
 "E4d7-lab2-blank": dict(check="2.5-labs", location="course/modules/E/E4/project.html:217, :244", status="PASS", evidence="Lab 2 page code has exactly one blank (return ___); every other line equals the twin (run_labs PASS); interpretation sentence about the blank matches the code."),
 "E4d7-lab3-closed-form-sentence": dict(check="2.5-labs", location="course/modules/E/E4/project.html:376", status="PASS", evidence="Lab 3 hypothesis: 'the bisection agrees with the closed form of Proposition 4 to within 1e-12': printed largest difference 2.1e-13 (expected block)."),
 "E4d7-instance-bound": dict(check="2.8-data", location="course/modules/E/E4/grader/test_project.py; grader/instance.py:1-21; project.html:314", status="PASS", evidence="instance.py docstring: box [0.500,0.750] x [0.120,0.150], rounding to three decimals, tau_bar in (0, 0.237567), tau_y(1) >= 0.30769 (recomputed in numbers_r15.txt)."),
 "E4d7-test-count": dict(check="2.6-autograder", location="course/modules/E/E4/project.html:320 (Grading mode); grader/test_project.py", status="PASS", evidence=f"collect-only 48 (={S}out/collect_only_r15.txt); page says 48 checks."),
 "E4d2-exemplar-B-C1-annotation": dict(check="2.3-grades", location="course/modules/E/E4/project.html:604-607 (Exemplar B Model passage), annotation :611", status="PASS", evidence="Exemplar B Model passage (blind stripped output) lists Assumptions 1-6 numbered and names the propositions that use them; annotation 'Meets C1 level 4' is consistent with the descriptor. Blind score C1=4."),
 "E4d12-exemplar-B-sigma": dict(check="2.3-grades", location="course/modules/E/E4/project.html:607 (Exemplar B Model passage)", status="PASS", evidence="Exemplar B's sigma (noise standard deviation) use matches Prop 1's tau_y formula and Prop 4's lambda* formula (checked in the derivation pass)."),
})

MATH = ("2.4-mathematics", "course/modules/E/E4/project.html:257-301 (A1-A6, Lemmas 1-3, Propositions 1-5)")
MATH_EV = ("Re-derived by hand this round: Lemma 1 (g(x)=x(m-p)-(a/2)x^2V, optimum (m-p)/(aV), value -(m-p)^2/(2V)); Lemma 2 (Gaussian integral sqrt(V/(V+S))); Lemma 3 (law of total variance); "
           "Prop 1 (coefficient identity kappa=-a/(lam tau_e), tau_y formula, b_s formula, equivalence of steps); Prop 2 (Corr^2 = tau_y/(tau_v+tau_y)); Prop 3 (sign rule tau_bar - tau_y(lam), G(0+) formula via the limits b_s/lam -> tau_e/tau_v); "
           "Prop 4 (three cases, lam* = a sigma sqrt(tau_bar/(tau_e(tau_e-tau_bar)))); Prop 5 (monotonicity). Numerically: the closed forms reproduce Lab 1 and Lab 2 values to 60 digits (" + NUM + "). No gap found.")
for k in ["E4d-math-lemmas", "E4d-math-prop1", "E4d-math-prop2", "E4d-math-prop3", "E4d-math-prop4", "E4d-math-prop5", "E4d-math-assumptions", "E4d13-independent-rederivation", "E4d11-literal-price-sign-open"]:
    FRESH[k] = dict(check=MATH[0], location=MATH[1], status="PASS", evidence=MATH_EV)
FRESH["E4d-math-assumptions"]["evidence"] = MATH_EV + " A6 is labelled as an assumption and every result that uses it says 'Assuming A6' (Props 4 and 5, Spec)."
FRESH["E4d11-literal-price-sign-open"]["evidence"] = MATH_EV + " Prop 1's sign of b_u/b_s is a model statement; see E4d-equivalent for the solver-level consequence."
FRESH["E4d13-independent-rederivation"]["evidence"] = MATH_EV
FRESH["E4d-prose-lede-directional"] = dict(check="2.3-grades", location="course/modules/E/E4/project.html:37 (lede)", status="PASS",
    evidence="Lede claims: at fixed cost the fraction rises with noise on the interior (Prop 5: lam* proportional to sigma); the informativeness does not depend on sigma on the interior (Prop 4/5); with the fraction fixed, more noise lowers tau_y/(tau_v+tau_y) (Prop 1 formula, tau_y decreasing in sigma). Each is derived, none is an empirical claim.")
FRESH["E4d-notation"] = dict(check="2.4-notation", location="course/modules/E/E4/project.html:266-267 and the notation paragraph; notation/notation.json", status="PASS",
    evidence=f"Notation scan ({S}notation_scan_r15.py, output {S}out/notation_scan_project.txt): registered macros used are \\E, \\Var, \\Cov, \\Corr, \\Normal with registry meanings (\\Normal(0, S) takes a variance, as the registry macro does); no \\mathbb, no \\R needed; no occurrence of the registered symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{{e\\ast}}, R_f, \\mathbb{{Q}} (count 0). Locally defined letters (lambda, sigma, tau, kappa, Omega) are not registered.")
FRESH["E4d13-notation"] = dict(FRESH["E4d-notation"])
FRESH["E4d-banned-phrases"] = dict(check="2.9-prose", location="course/modules/E/E4/project.html; grader/*.py; tests/labs/E4/lab-E4-project-*.py", status="PASS",
    evidence=f"Banned-phrase and process-word scan ({S}banned_scan_r15.py, {S}out/banned_scan.txt): no TODO/TBD/lorem/'for brevity'/'beyond the scope'/filler/'about 6%'/'roughly half'/'historically'/process words in these files. The only ellipses are truncated decimals in instance.py:15-16 (0.09762327..., 0.23756678..., 0.30769...) and \\ldots in project.html Spec (0.09762327\\ldots), which show digits of a value, not omitted content; recorded, not counted as a hit.")
FRESH["E4d-process-words"] = dict(FRESH["E4d-banned-phrases"], check="2.9-prose")
FRESH["E4d-prose-scope-words"] = dict(check="2.4-scope", location="course/modules/E/E4/project.html (all prose; scan output)", status="PASS",
    evidence=f"Scope-word scan ({S}scope_words_r15.py, 167 occurrences in {S}out/scope_words.txt) read in full. Each universal claim is either a stated hypothesis (A1-A6, 'Under A1 to A5 and assuming A6'), a derivation (Props 1-5), a computed check with its count (484 box points, 48 checks, 12 labs), or a definition ('every investor' = each type in A3/A5). No unsupported 'only/all/always' claim found.")
FRESH["E4d-prose-simulated-labs"] = dict(check="2.5-labs", location="course/modules/E/E4/project.html:57, :176, :314, :375", status="PASS", evidence="Each lab and the generator is labelled SIMULATED where stated (Lab 1, Lab 2, Lab 3 hypotheses; Inputs line); the stated inputs are not draws (Rungs paragraph).")
FRESH["E4d-prose-simulated-exemplars"] = dict(check="2.8-data", location="course/modules/E/E4/project.html:530 (exemplar intro)", status="PASS", evidence="Exemplar intro (project.html:535 in this checkout) says 'Two report excerpts on a SIMULATED instance'; numbers are Lab 3's.")
FRESH["E4d-dag-links"] = dict(check="2.9-dag", location="course/modules/E/E4/project.html (concept links and hrefs)", status="PASS",
    evidence="check_dag E4 PASS. Concept links: expected-utility -> ../../../concepts.html#expected-utility (id present, concepts.html:447); noisy-rational-expectations-equilibrium -> L06.html#def-noisy-rational-expectations-equilibrium (L06.html:169, dfn present); price-informativeness -> L07.html#def-price-informativeness (L07.html:62, dfn present). All in the unit's closure (E2/E3/M7 via L06/L07).")
FRESH["E4d13-links"] = dict(check="2.9-structure", location="course/modules/E/E4/project.html (href targets)", status="PASS", evidence="Every #fragment in project.html resolves: #model #brief #spec #report #rubric #self-assessment #stretch #reading #lab-E4-project-3 #grader-section #exceptions #h-... ids present (grep of id=...); index.html#placement present (index.html:66); L06/L07/L09/index/review.html files exist.")
FRESH["E4d3-anchors-links"] = dict(FRESH["E4d13-links"], check="2.9-structure")
FRESH["E4d-registry-muth"] = dict(check="2.1-citations", location="course/modules/E/E4/project.html:685; references/references.json", status="PASS",
    evidence="references/references.json key muth1961rational: verified_by crossref, doi 10.2307/1909635, Muth 1961, Econometrica 29(3), status verified, used_by E4. Page cites it only as a reading-list entry and attributes no statement (project.html:683).")
FRESH["E4d-registry-milgrom"] = dict(check="2.1-citations", location="course/modules/E/E4/project.html:686; references/references.json", status="PASS",
    evidence="references/references.json key milgrom1982information: crossref, doi 10.1016/0022-0531(82)90046-1, Milgrom & Stokey 1982, JET 26(1), status verified, used_by E4. Reading-list only; no statement attributed.")
FRESH["E4d-cites-only-registry"] = dict(check="2.1-citations", location="course/modules/E/E4/project.html data-cite (:685-686)", status="PASS", evidence="Only data-cite values on the page are muth1961rational and milgrom1982information, both registry keys (grep data-cite). Grossman-Stiglitz is not cited (architect decision; grep 'Grossman' returns none).")
FRESH["E4d10-l06-dependency"] = dict(check="2.9-dag", location="course/modules/E/E4/L06.html:57, :66, :169; course/modules/E/E4/L07.html:62", status="PASS",
    evidence="Re-read this round at the current pin: L06.html:57 defines signal and noise trader; L06.html:66 is Definition 6.2 (CARA utility); L06.html:169 holds the dfn of noisy-rational-expectations-equilibrium; L07.html:62 holds the dfn of price-informativeness. The L06 hunks changed since round 14 (lines 62, 143, 157, 202, 663) do not touch these lines.")
FRESH["E4d3-cara-defined-twice"] = dict(check="2.9-prose", location="course/modules/E/E4/project.html:259 (A3); course/modules/E/E4/L06.html:57, :66", status="PASS",
    evidence="project.html:259 says 'constant absolute risk aversion (CARA) utility (Definition 6.2 of Lesson 6)' and has no <dfn>; the project page contains 0 <dfn> elements (grep). The definition lives only in L06.html:66-67.")
FRESH["E4d-hours-project"] = dict(check="2.9-hours", location="course/modules/E/E4/project.html:33, :35, :341-352; course/modules/E/E4/index.html:29", status="PASS",
    evidence="project.html data-hours-project=28; hub index.html data-hours-project=28, data-hours-lessons=72 (72+28=100 = module hours); #hours table components 1+1+5+8+5+5+3 = 28 (rows read at project.html:341-352).")
FRESH["E4d13-hours-arithmetic"] = dict(FRESH["E4d-hours-project"], check="2.9-hours")
FRESH["E4d-hours-estimate"] = dict(check="2.6-hours", location="course/modules/E/E4/project.html #hours (:341-352)", status="PASS",
    evidence="Round-15 independent estimate per component: rung 1 about 1 h, rung 2 about 1 h, model derivation (Props 1-5 with proofs) about 6 h, solver and local tests about 5 h, comparative-statics grid about 2 h, report about 4 h, self-assessment about 3 h: total about 22 h, 21% below 28 h (inside the 30% bar). Hours are design targets (architect ruling).")
FRESH["E4d-rubric-observable"] = dict(check="2.6-rubric", location="course/modules/E/E4/project.html:517-527 (#rubric)", status="PASS",
    evidence="Read C1-C5 level descriptors (project.html:525-529): each level names a visible feature (lists assumptions with numbers, states a formula, names a tolerance and a stop rule, gives a grid, names significant digits, names at least three limits). Level 1 descriptors quote observable failures.")
FRESH["E4d-exemplar-annotations-hidden"] = dict(check="2.6-rubric", location="course/modules/E/E4/project.html reveal markup (:539, :604); course/assets/js/rubric.js:147-150", status="PASS",
    evidence="rubric.js:147-150 sets part.hidden on '.annotation, [data-reveal]' unless revealed; project.html:539 and :604 carry data-reveal on the verdict lines. Annotations are in the HTML for learners (ruling 15).")
FRESH["E4d-spec-context-sentences"] = dict(check="2.6-spec", location="course/modules/E/E4/project.html:312 (Context)", status="PASS", evidence="Context dd has 4 sentences (2 to 4 required, curriculum brief 'Solve a noisy rational-expectations model numerically...' at curriculum/02-economics-finance-core.yaml:150-152 is covered).")
FRESH["E4d-spec-questions"] = dict(check="2.6-spec", location="course/modules/E/E4/project.html:314-322 (Inputs, Required outputs, Constraints, Grading mode, Reading list)", status="PASS",
    evidence="Read in full. Questions a student would ask: the interface (solver.py, solve_model signature, three keys) is given; the tolerance and stop rule are constants; the exception table names both conditions; the autograder and rubric are both named. No further question found.")
FRESH["E4d-spec-ladder"] = dict(check="2.6-spec", location="course/modules/E/E4/project.html:40-49, :51-305, :308, :669-675", status="PASS", evidence="Ladder order: rung 1 worked example (Lab 1), rung 2 completion (Lab 2, class completion), rung 3 solver+report, rung 4 stretch (stretch section). check_projects PASS.")
FRESH["E4d3-spec-stop-rule-and-constraints"] = dict(check="2.6-spec", location="course/modules/E/E4/project.html:318 (Constraints); grader/test_project.py (accuracy and gap tests)", status="PASS",
    evidence="Each Constraints clause maps to a test: gap at 0 limit to 1e-14 (test_gap_at_zero_fraction_is_the_limit_to_full_precision), interior gap (test_gap_at_an_interior_fraction_..., 1e-14), fraction-1 gap and informativeness (test_unit_fraction_...), boundary rule (test_boundary_rule_holds), relative accuracy 1e-10 (tiny/small/corner/near-zero root tests), exceptions (must_raise tests). The 240-halving cap and 1e-12 stop are the constants in reference.py:21-23.")
FRESH["E4d11-constraints-accuracy"] = dict(FRESH["E4d3-spec-stop-rule-and-constraints"], check="2.6-spec-vs-suite", location="course/modules/E/E4/project.html:318; grader/test_project.py:534-565")
FRESH["E4d11-constraints-wording"] = dict(check="2.2-prose-numbers", location="course/modules/E/E4/project.html:318", status="PASS", evidence="Constraints wording: 1e-14, 1e-12, 240 halvings, 1e-10, noise >= 1e-50, tau_bar >= 1e-2: each matches reference.py:21-23 and test_project.py:44-46 and 534-586.")
FRESH["E4d11-oracle-precision"] = dict(check="2.6-grader", location="course/modules/E/E4/grader/test_project.py:79-170", status="PASS", evidence="Oracle read in full (oracle_expect_exp, oracle_regressions, oracle_price, oracle_gap, oracle_informativeness, oracle_root). Trapezoid on [-10,10] with step 0.02 agrees with the closed forms to 1e-16 on the cases checked (docstring_numbers_r15.txt: oracle deviation max 1.1e-16).")
FRESH["E4d12-bisection-assumption"] = dict(check="2.2-spec-vs-plan", location="course/modules/E/E4/project.html:318 ('the sign-change assumption')", status="PASS", evidence="project.html:318 cites Assumption A6 for the sign change; A6 is stated at project.html:262-263 as an assumption (not proved) and used only in the interior case.")
FRESH["E4d11-plan-tolerance-documented"] = dict(check="2.2-spec-vs-plan", location="course/modules/E/E4/project.html:318", status="PASS", evidence="Tolerance 1e-12 and 240 halvings are documented constants on the page (project.html:318) and in reference.py:21-23; the plan (plans/E4-build-plan.md section 5.2) asks that the tolerance be a documented constant, not an argument.")
FRESH["E4d-prose-simulated-exemplars"] = FRESH["E4d-prose-simulated-exemplars"]

FRESH.update({
 "E4d3-no-figures-no-data": dict(check="2.8-data", location="course/modules/E/E4/project.html", status="PASS",
    evidence="grep: project.html contains 0 occurrences of <svg, <img, <canvas or data-files (no figure, no dataset). The Inputs line says 'No dataset' (project.html:314). No JS chart kernel is referenced by this page."),
 "E4d3-atlas-studios-na": dict(check="2.6-atlas", location="course/modules/E/E4/project.html; curriculum/02-economics-finance-core.yaml (E4 entry, no atlas key); atlas/", status="PASS",
    evidence="E4 has no Atlas milestone: the E4 curriculum entry (02-economics-finance-core.yaml, lines ~122-152) has no atlas key, project.html has 0 mentions of atlas, and the plan says no Atlas milestone (plan header). Atlas rules are not applicable."),
 "E4d10-delta-A1-prior-mean": dict(check="2.4-mathematics", location="course/modules/E/E4/project.html:257-262 (A1)", status="PASS", evidence="A1 read: the prior mean zero normalisation and the claim that a common mean mu shifts payoff, signal, conditional means and price by mu; the economy is the zero-mean one less mu. Consistent with the CARA demand depending on differences (Lemma 1)."),
 "E4d10-delta-inputs-interior-root": dict(check="2.6-spec", location="course/modules/E/E4/project.html:314 (Inputs)", status="PASS", evidence="Inputs paragraph read: the bracket claim 'every instance the generator draws has one interior root' is T under A1-A5 and assuming A6, with the box bound derived (tau_bar in (0, 0.237567), tau_y(1) >= 0.30769; numbers_r15.txt)."),
 "E4d10-delta-constraints-gap-at-zero": dict(check="2.6-spec", location="course/modules/E/E4/project.html:318 (Constraints, gap at zero clause)", status="PASS", evidence="Clause read: the gap at 0 agrees with the limit to 1e-14 relative to max(1, |limit|); test_gap_at_zero_fraction_is_the_limit_to_full_precision implements it (50/50 reference pass; 3 zero-fraction mutants killed)."),
 "E4d10-delta-grading-mode-43": dict(check="2.6-autograder", location="course/modules/E/E4/project.html:320 (Grading mode)", status="PASS", evidence="Grading mode reads '48 checks' (project.html:320); collect-only 48 (collect_only_r15.txt)."),
 "E4d10-delta-results-ratio": dict(check="2.2-numbers", location="course/modules/E/E4/project.html:629-641", status="PASS", evidence="Exemplar B Results: ratio 1.25 (0.625/0.500) and 1.50 (0.750/0.500) and displayed-value ratios 1.2501 and 1.5000 recomputed (0.6978/0.5582 = 1.250090; 0.8373/0.5582 = 1.500000)."),
 "E4d10-new-test-numbers": dict(check="2.6-autograder", location="course/modules/E/E4/grader/test_project.py (docstrings with numbers)", status="PASS", evidence=f"Numbers in test docstrings recomputed with the suite's own oracles ({S}docstring_numbers_r15.py; out/docstring_numbers_r15.txt): 1.02e-13 to 3.54e-13; oracle deviation max 1.11e-16; corner root 2.0224e-51 (corner scan)."),
 "E4d11-delta-hunks": dict(check="2.6-delta", location="project.html:244, :318, :320, :397, :618; test_project.py:401-418, :534-553; reference.py:22-23; alt_1.py:1, :80; alt_5.py:101; lab-E4-project-3.py:21; index.html:63; equivalent/README.md; mutants added/moved", status="PASS", evidence="Delta since 8e5751c recomputed (git diff --stat): none of the listed project, grader, lab, alternative or README hunks changed since the round-14 pin; the mutant additions are mutant_r14_01..05 (read in out/mutant_hunks.txt)."),
})
GRADER_ALL = "course/modules/E/E4/grader/test_project.py, instance.py, reference.py, starter.py"
FRESH.update({
 "E4d-grader-exceptions": dict(check="2.6-autograder", location="course/modules/E/E4/grader/test_project.py:191-234, :242-280; reference.py:26-34", status="PASS",
    evidence="Read in full. The two named conditions each have isolated tests in both directions: noise 0, negative, inf, nan (ValueError 'noise volume must be positive'); cost -0.01, -1e-12 (ValueError 'information cost must be nonnegative'); cost 0 and noise 1e-12 accepted. Reference raises exactly those messages; run_graders PASS."),
 "E4d-grader-messages": dict(check="2.6-autograder", location="course/modules/E/E4/grader/test_project.py (every expect() and pytest.fail call)", status="PASS",
    evidence="Read every expect()/pytest.fail message (lines 49-68, 178-586). Each names the violated property and an idea to revisit; none prints a value. --assert=plain and __tracebackhide__ in expect/must_raise/run."),
 "E4d-grader-oracle": dict(check="2.6-autograder", location="course/modules/E/E4/grader/test_project.py:79-170", status="PASS", evidence="Oracle read in full; it does not import reference.py or read solver.py (only solve_model is called for the answer under test)."),
 "E4d-grader-instances": dict(check="2.6-autograder", location="course/modules/E/E4/grader/instance.py; test_project.py:37-40", status="PASS",
    evidence=f"instance.py read in full. Instances for seeds 0-49 are distinct (test_answers_change_across_seeds_zero_to_forty_nine and run_graders check_instances PASS); parameters in range; deterministic via random.Random(seed)."),
 "E4d-grader-instance-docstring": dict(check="2.6-autograder", location="course/modules/E/E4/grader/instance.py:1-21", status="PASS", evidence="Docstring says SIMULATED, the box, the rounding, and tau_bar bounds; each number recomputed (numbers_r15.txt)."),
 "E4d-grader-test-docstring": dict(check="2.6-autograder", location="course/modules/E/E4/grader/test_project.py (test docstrings)", status="PASS", evidence=f"Docstrings with numbers checked by {S}docstring_numbers_r15.py: 'differs by 1e-13 to 4e-13' (measured 1.02e-13 to 3.54e-13) and 'oracle agrees to at most 1.1e-16' (measured max 1.11e-16). One docstring mismatch is a separate row: E4d15-grader-docstring-scale."),
 "E4d-grader-reference-docstring": dict(check="2.6-autograder", location="course/modules/E/E4/grader/reference.py:21-23", status="PASS", evidence="reference.py:22-23: '240 halvings reach the relative tolerance for every root above about 6e-61 (2^-240 about 5.7e-73); 200 halvings do not reach it near 2e-51' - recomputed (2^-240=5.66e-73; 1e-12*6e-61=6e-73 consistent; 2^-200=6.2e-61 vs 1e-10*2e-51=2e-61 from the corner scan)."),
 "E4d-grader-stdlib": dict(check="2.6-autograder", location="course/modules/E/E4/grader/test_project.py (test_solver_imports_only_the_standard_library); ledgers/E4/alternatives/*.py", status="PASS", evidence="Test passes for reference and all eight alternatives (run_candidate sweep, out/alternatives_equivalents_0_49.txt); alternatives import only math and __future__."),
 "E4d-runtime": dict(check="2.6-autograder", location="course/modules/E/E4/grader/test_project.py", status="PASS", evidence="page_smoke in-browser grader: 'All 48 tests pass' in 0.9 s (out/page_smoke_E4_project.txt); run_graders slowest 0.2 s per seed; each test well under 5 s, suite under 60 s."),
 "E4d-browser-local-parity": dict(check="2.6-autograder", location="course/modules/E/E4/grader/test_project.py; tools/page_smoke.py", status="PASS", evidence="Same suite and flags: page_smoke in-browser run (48 pass) and local pytest workspace (run_graders 50/50, collect 48) agree."),
 "E4d-starter": dict(check="2.6-autograder", location="course/modules/E/E4/grader/starter.py", status="PASS", evidence="starter.py raises NotImplementedError; run_candidate sweep on seeds 0-49: 0/50 seeds pass (out/alternatives_equivalents_0_49.txt), so the suite fails on the starter."),
 "E4d4-proposed-test-validated": dict(check="2.6-autograder", location="course/modules/E/E4/grader/test_project.py (small-noise and corner tests)", status="PASS", evidence="Small-noise and corner tests pass on reference (50/50 seeds) and fail on the cap-200 mutants (out/mutate_graders_E4_0_9_r15.txt: test_corner_root... kills)."),
 "E4d6-stop-rule-measured": dict(check="2.6-autograder", location="course/modules/E/E4/grader/reference.py:22-23, :138", status="PASS", evidence=f"Stop rule measured: corner scan with cap 240 has 0 cases above 1e-10 and max 5.14e-13 over 90000 cases ({S}out/corner_scan_cap240.txt)."),
 "E4d8-tiny-root-reference": dict(check="2.6-autograder", location="course/modules/E/E4/grader/reference.py", status="PASS", evidence="Reference at sd 1e-40, 1e-11, 1e-9 gives lambda* 6.578e-41, 6.578e-12, 9.656e-10 (numbers printed by docstring_numbers_r15.py), matching the closed form within 1e-10 relative (the suite runs these fixed-input tests on every seed; run_graders 50/50)."),
 "E4d13-accuracy-sweep": dict(check="2.6-autograder", location="course/modules/E/E4/grader/reference.py; course/modules/E/E4/project.html:318", status="PASS", evidence=f"Corner scan cap 240 on 90000 cases: 0 over 1e-10 (out/corner_scan_cap240.txt). Gap accuracy for the reference: run_graders PASS."),
 "E4d13-extreme-inputs": dict(check="2.4-scope", location="course/modules/E/E4/project.html:316-318, :327; grader/reference.py", status="PASS", evidence=f"Range extremes (noise 1e150, cost 350, noise 1e-300, noise 1e-50 with cost 0 and 350) return three finite keys; sd=1e-300 returns informed_fraction 2.83e-73 with informativeness 0.5 (true tau_bar-based value 0.159): the page discloses the inaccuracy below 1e-50 at project.html:327. Output: {S}out/range_extremes_r15.txt."),
 "E4d13-instances-seeds-0-49": dict(check="2.6-autograder", location="course/modules/E/E4/grader/instance.py; course/modules/E/E4/grader/test_project.py:37-40", status="PASS", evidence="run_graders check_instances (seeds 0-49) PASS: distinct fingerprints and deterministic draws."),
 "E4d13-candidates-accepted": dict(check="2.6-autograder", location="ledgers/E4/alternatives/alt_1..alt_8.py; ledgers/E4/equivalent/*.py; grader/starter.py", status="PASS", evidence=f"All eight alternatives 50/50 on seeds 0-49; the three equivalents pass 50/50 as expected (out/alternatives_equivalents_0_49.txt); starter 0/50."),
 "E4d12-corner-test-docstring": dict(check="2.6-autograder", location="course/modules/E/E4/grader/test_project.py:555-558 (test_corner_root docstring)", status="PASS", evidence="Docstring numbers: noise 1e-50, tau_bar just above 1e-2, root about 2e-51, cap 200 misses 1e-10 relative: measured 2.0224e-51, 0.0101216, 1.5322e-10 (cap 200) (out/corner_scan_cap200.txt)."),
 "E4d12-tiny-noise-informativeness": dict(check="2.4-scope", location="course/modules/E/E4/project.html:326 (exception table range), :314, :316; grader/reference.py:26-44, :122-151", status="PASS", evidence="Range statement (noise up to 1e150, cost up to 350) verified by range_extremes_r15.py (finite outputs). Page states the solver may be inaccurate below 1e-50 (project.html:327)."),
 "E4d12-prose-2pow240": dict(check="2.2-prose-numbers", location="course/modules/E/E4/grader/reference.py:23; ledgers/E4/equivalent/literal_price_sign.py:15 (and the three stop-rule files)", status="PASS", evidence="2^-240 = 5.66e-73 (docstring_numbers_r15/numbers printed); '5.7e-73' is the rounded value."),
 "E4d12-equivalent-readme-numbers": dict(check="2.2-numbers", location="ledgers/E4/equivalent/README.md (stop-rule section)", status="PASS", evidence=f"Every README number reproduced: cap 240: 90000 cases, 0 over 1e-10, max 5.1420e-13 (README 5.1e-13); cap 200: 11598 over, max 1.5322e-10 at sd 1e-50, cost 0.17076911209224613, root 2.0224e-51, tau_bar 0.0101216; cost 0.17076911209: 8.03e-12 (README 8.0e-12); tau_bar range 0.010000 to 0.012022; 2^-200=6.22e-61; halvings to width 1e-12*root = 209 ({S}out/corner_scan_cap240.txt, corner_scan_cap200.txt, {S}out/numbers_r15.txt)."),
 "E4d13-readme-corner-domain": dict(check="2.2-numbers", location="ledgers/E4/equivalent/README.md ('Stop-rule variants', paragraph 2)", status="PASS", evidence="Grid: noise 1e-50*(1+0.002 i), i=0..299 (1e-50 to 1.598e-50); costs from 0.1702992124 to 0.1707992124 (c_edge - 0.0005 to c_edge = 0.1707992124); reproduced by corner_scan_r15.py ('cost range 0.1702992124 0.1707992124', 'tau-bar range 0.012022 0.010000')."),
 "E4d13-endpoint-gap-precision": dict(check="2.6-grader", location="course/modules/E/E4/grader/test_project.py:419-450; course/modules/E/E4/project.html:316 and :318", status="PASS", evidence="Read tests at 419-458: run(2.0, 0.0) and run(0.6, 0.05) have fraction 1, informativeness and gap compared with the oracle at 1e-14 relative; reference passes (50/50)."),
 "E4d13-alternatives-plan-list": dict(check="2.6-alternatives", location="ledgers/E4/alternatives/alt_4.py (docstring line 1); alt_5.py (docstring lines 1-2); plans/E4-build-plan.md section 5.5 and the 2026-11-05 ruling", status="PASS", evidence="alt_1..alt_8 docstrings read: bisection (alt_1), Illinois (alt_2, alt_8), grid+bisection (alt_3), secant (alt_4), precision parameterisation (alt_5), closed form (alt_6), sign-of-tau_bar bisection (alt_7). The 2026-11-05 ruling (plan tail) says the built set alt_1..alt_8 satisfies ruling 10; read and accepted."),
 "E4d4-alt1-docstring": dict(check="2.6-alternatives", location="ledgers/E4/alternatives/alt_1.py:1-3", status="PASS", evidence="alt_1 docstring: 'bisection with a relative bracket width of 1e-12, or at most 240 halvings' (read in full; the code uses 1e-12 and 240, line 'while hi - lo > 1e-12 * hi and halvings < 240')."),
 "E4d4-alt4-wrong-on-small-noise": dict(check="2.6-alternatives", location="ledgers/E4/alternatives/alt_4.py", status="PASS", evidence="alt_4 (secant with bracket safeguard, relative stop 1e-13*x) passes 50/50 seeds (out/alternatives_equivalents_0_49.txt) including the small-root tests; read in full."),
 "E4d7-alt5-docstring": dict(check="2.6-alternatives", location="ledgers/E4/alternatives/alt_5.py:1-2", status="PASS", evidence="alt_5 docstring 'the same model parameterised by the noise precision, with the same bracket [0, 1]': code uses nu = 1/sd^2 and tau_y = lam^2 tau_e^2 nu/(lam^2 tau_e nu + a^2), algebraically equal to the reference's tau_y; passes 50/50."),
 "E4d10-alternatives-r10": dict(check="2.6-alternatives", location="ledgers/E4/alternatives/alt_1..alt_5", status="PASS", evidence="alt_1..alt_5 re-run seeds 0-49 (50/50 each)."),
 "E4d11-alt-closed-form": dict(check="2.6-alternatives", location="ledgers/E4/scripts/E4-d-r11/alts/alt_r11_a.py", status="PASS", evidence="Closed-form alternative family: alt_6 (no bisection, closed form of Prop 4 + gap formulas) passes 50/50 seeds (out/alternatives_equivalents_0_49.txt)."),
 "E4d12-alt-variants-new": dict(check="2.6-alternatives", location="ledgers/E4/alternatives/alt_6.py, alt_7.py, alt_8.py (round 12 files, now in alternatives/)", status="PASS", evidence="alt_6, alt_7, alt_8 read in full and each passes 50/50 seeds (out/alternatives_equivalents_0_49.txt)."),
 "E4d6-alt-extra-damped": dict(check="2.6-alternatives", location="ledgers/E4/scripts/E4-d-r6/candidates/damped_fixed_point_log_r6.py", status="PASS", evidence="Damped fixed-point candidate from round 6 is not in the alternatives set (architect ruling: not required, not correct on every instance); the file exists at the pin and is not counted."),
 "E4d-alternatives": dict(check="2.6-alternatives", location="ledgers/E4/alternatives/alt_1.py .. alt_8.py", status="PASS", evidence="All eight read (headers and cores); each has zero references to reference.py; all pass 50/50 seeds 0-49 (out/alternatives_equivalents_0_49.txt). Six distinct styles satisfy ruling 10."),
 "E4d13-new-mutants": dict(check="2.6-mutation", location="ledgers/E4/mutants/mutant_r13_01..04_*.py", status="PASS", evidence="Four r13 mutants (plus r13_05) killed in the 126/126 run (out/mutate_graders_E4_0_9_r15.txt); their hunks read (out/mutant_hunks.txt). Stale cap-200 change present (see E4d15-mutants-single-change)."),
 "E4d13-mutant-gate-final": dict(check="2.6-mutation", location="ledgers/E4/mutants/ (126 files); tools/mutate_graders.py", status="PASS", evidence="tools/mutate_graders.py --unit E4 --seeds 0-9: 'mutate_graders E4: PASS (126/126 killed)' (out/mutate_graders_E4_0_9_r15.txt)."),
 "E4d14-mutants-r14-new": dict(check="2.6-mutation", location="ledgers/E4/mutants/mutant_r14_01..05 (round-14 files)", status="PASS", evidence="All five r14 mutants killed (out/mutate_graders_E4_0_9_r15.txt: r14_01 by unit-fraction tests, r14_02 by NaN message test, r14_03 by oracle gap, r14_04 by boundary test, r14_05 by informativeness test)."),
 "E4d14-corner-scan": dict(check="2.6-round-14", location="ledgers/E4/scripts/E4-d-r14 corner scan (re-run this round)", status="PASS", evidence=f"Re-run this round: {S}out/corner_scan_cap240.txt (0 over 1e-10, max 5.14e-13) and corner_scan_cap200.txt (11598 over, max 1.53e-10)."),
 "E4d14-accuracy-sweep": dict(check="2.6-round-14", location="ledgers/E4/scripts/E4-d-r14 accuracy sweep (re-run this round)", status="PASS", evidence=f"Re-run as the corner scan and the grader accuracy tests (run_graders 50/50; {S}out/corner_scan_cap240.txt)."),
 "E4d14-equivalent-literal-3000": dict(check="2.6-round-14", location="ledgers/E4/equivalent/literal_price_sign.py", status="PASS", evidence=f"Re-run this round on 3000 random inputs (noise 0.05-3.0, cost 0-0.4): largest absolute difference 0.0 in all three outputs ({S}literal_sign_3000_r15.py, {S}out/literal_sign_3000_r15.txt). The algebra (b_u enters only as b_u*b_u) is in the README proof."),
 "E4d14-delta-read": dict(check="2.6-round-14", location="delta 8e5751c..d1e65a0 for slice d", status="PASS", evidence="Delta read: course/modules/E/E4/project.html, grader/*, tests/labs/E4/*, ledgers/E4/alternatives/*, ledgers/E4/equivalent/* byte-identical to 8e5751c (git diff --stat empty for these paths); the changed slice-d files are ledgers/E4/mutants/mutant_r14_01..05 (new, read: hunks in out/mutant_hunks.txt) and plans/FINAL-ARCHITECT-RULINGS.md (rulings 15 and 16, read). L03.html and L06.html changed but are outside slice d; the L06 cited lines are unchanged (E4d10-l06-dependency)."),
 "E4d-equivalent": dict(check="2.6-mutation", location="ledgers/E4/equivalent/literal_price_sign.py; mutant_r6_08_*; mutant_r7_01_*; mutant_v9_02_*", status="FAIL",
    evidence=f"literal_price_sign.py: provably output-identical (b_u enters only as b_u*b_u); re-checked on 3000 inputs with zero difference ({S}out/literal_sign_3000_r15.txt): an equivalent mutant, not a fault. mutant_r6_08 and mutant_r7_01 (report the lower end of the final bracket) and mutant_v9_02 (stop test against the lower end) pass 50/50 seeds (out/alternatives_equivalents_0_49.txt) and differ from the reference by at most one final bracket width (<= 1e-12 relative), so they are not distinguishable by any test at the page's 1e-10 accuracy; they are not provably equivalent either (exact comparison distinguishes them). They violate the stop rule and the reported point, which the page states (project.html:318; exemplar B Method sentence at :619).",
    fix="Architect decision (ruling 9): either state the reported point on the page and accept the three stop-rule variants as equivalent within the stated accuracy in writing, or keep them as surviving mutants with a named gap. No grader change can kill them without demanding more precision than the page states."),
 "E4d6-spec-variants-08-09": dict(check="2.6-mutation", location="ledgers/E4/equivalent/mutant_r6_08_reports_lower_end.py; ledgers/E4/mutants/mutant_r6_09_always_200_halvings.py", status="FAIL",
    evidence="mutant_r6_09 (killed by test_corner_root...). mutant_r6_08 is the lower-end-report variant: see E4d-equivalent (architect decision).",
    fix="Architect decision as in E4d-equivalent."),
 "E4d7-midpoint-untested": dict(check="2.6-autograder", location="course/modules/E/E4/project.html:318; ledgers/E4/equivalent/mutant_r7_01_reports_bracket_lower_end.py", status="FAIL",
    evidence="mutant_r7_01 reports the bracket's lower end and passes 50/50 seeds; the page's Constraints (318) states the stop rule, and the midpoint sentence is in Exemplar B (project.html:619). No output test can separate the variant at the page's accuracy.",
    fix="Architect decision as in E4d-equivalent (state the reported point, or accept the equivalence in writing)."),
 "E4d9-mutant-v9-02": dict(check="2.6-mutation", location="ledgers/E4/equivalent/mutant_v9_02_stop_rule_relative_to_lower_end.py (moved from mutants/ in round 10)", status="FAIL",
    evidence="Re-read this round: the stop test is 'high - low > 1e-12 * low', i.e. it does not stop at the page's constant (1e-12 times the upper end) and runs more halvings. It passes 50/50 seeds. Output-equivalent within the page's accuracy, not provably equivalent, so it cannot be moved to equivalent/ under ruling 9 without the architect's decision.",
    fix="Architect decision as in E4d-equivalent."),
 "E4d9-mutant-v9-06": dict(check="2.6-mutation", location="ledgers/E4/mutants/mutant_v9_06_gap_at_zero_from_tiny_fraction.py", status="PASS", evidence=f"Killed by test_gap_at_zero_fraction_is_the_limit_to_full_precision (seed 0) in the 126/126 run ({S}out/mutate_graders_E4_0_9_r15.txt)."),
 "E4d9-equivalent-r6-08-09-docstrings": dict(check="2.6-mutation", location="ledgers/E4/equivalent/mutant_r6_08_reports_lower_end.py; ledgers/E4/mutants/mutant_r6_09_always_200_halvings.py", status="PASS", evidence="Docstring of r6_08 names its variant (read); r6_09 is killed (corner test). Docstrings are accurate to the code (hunks in out/mutant_hunks.txt)."),
 "E4d9-mutants-v9-killed": dict(check="2.6-mutation", location="ledgers/E4/mutants/mutant_v9_01, _03, _05, _07", status="PASS", evidence="All four killed in the 126/126 run (killed_by names in the fragment mutants list)."),
 "E4d9-mutant-docstrings": dict(check="2.6-mutation", location="ledgers/E4/mutants/*.py (first docstring line of each)", status="PASS", evidence="First docstring line of each of the 126 mutants read (listed by the round-15 ledger mutants array); each names the student error. The cap-200 mutants' first lines describe their own error, not the cap (out/mutant_hunks.txt)."),
 "E4d10-mutants-new-r10": dict(check="2.6-mutation", location="ledgers/E4/mutants/mutant_r10_01..04 (7 files)", status="PASS", evidence="All seven killed in the 126/126 run."),
 "E4d11-mutants-new-r11": dict(check="2.6-mutation", location="ledgers/E4/mutants/mutant_r11_01..04", status="PASS", evidence="All killed in the 126/126 run (r11_03 clipped-fraction by the unit-fraction test; r11_03 signal-precision by informativeness)."),
 "E4d11-mutant-r10-02": dict(check="2.6-grader", location="ledgers/E4/mutants/mutant_r10_02_cost_factor_relative_error.py vs grader/test_project.py:401-418", status="PASS", evidence="Killed by test_gap_at_an_interior_fraction_is_the_oracle_gap_to_full_precision (seed 0) in the 126/126 run."),
 "E4d12-mutant-gap-stop": dict(check="2.6-grader", location="ledgers/E4/mutants/mutant_r12_04_stops_when_midpoint_gap_is_tiny.py; grader/test_project.py:534-565; project.html:318", status="PASS", evidence="Killed by test_root_is_relatively_accurate_at_a_cost_near_zero[1e-50-1e-06] in the 126/126 run."),
 "E4d-mutants-existing": dict(check="2.6-mutation", location="ledgers/E4/mutants/ (122 files at d1e65a0 before this round's additions)", status="PASS", evidence=f"Re-run this round: 122 pre-existing files all killed on seeds 0-9 ({S}out/mutate_graders_E4_0_9_r15.txt). Single-change defect of 86 of them is a separate row (E4d15-mutants-single-change)."),
 "E4d-mutants-new": dict(check="2.6-mutation", location="ledgers/E4/mutants/mutant_r7_02_*.py, mutant_r7_03_*.py", status="PASS", evidence="mutant_r7_02 and r7_03 killed in the 126/126 run (noise above one; cost above one)."),
 "E4d2-mutants-r2": dict(check="2.6-mutation", location="ledgers/E4/mutants/mutant_r2_*.py", status="PASS", evidence="All r2 mutants killed in the 126/126 run."),
 "E4d3-mutants-r3": dict(check="2.6-mutation", location="ledgers/E4/mutants/mutant_r3_*.py", status="PASS", evidence="All r3 mutants killed in the 126/126 run."),
 "E4d3-mutant-tolerance-survives": dict(check="2.6-mutation", location="ledgers/E4/mutants/mutant_r3_tolerance_1e-9.py", status="PASS", evidence="Killed in the 126/126 run (test_small_noise / corner-type tests), not a survivor."),
 "E4d-mutants-total": dict(check="2.6-mutation", location="ledgers/E4/mutants/ (126 files)", status="PASS", evidence="tools/mutate_graders.py --unit E4 --seeds 0-9: 126/126 killed (out/mutate_graders_E4_0_9_r15.txt). Survivors: none. Count matches the fragment's mutants array (126)."),
 "E4d4-equivalent-price-slope": dict(check="2.6-mutation", location="ledgers/E4/scripts/E4-d-r4/check_equivalence_r4.py; ledgers/E4/equivalent/literal_price_sign.py", status="PASS", evidence=f"Equivalence of the price-sign variant re-checked: {S}out/literal_sign_3000_r15.txt (zero difference on 3000 inputs) and the algebraic argument in the README."),
 "E4d4-mutants-killed-r4": dict(check="2.6-mutation", location="ledgers/E4/mutants/mutant_r4*.py", status="PASS", evidence="All r4 and r4f mutants killed in the 126/126 run."),
 "E4d5-mutant-bracket-floor": dict(check="2.6-mutation", location="ledgers/E4/mutants/mutant_r5_bracket_floor_1e-12.py", status="PASS", evidence="Killed by test_tiny_noise_root_is_relatively_accurate[1e-12]-type tests in the 126/126 run."),
 "E4d5-mutant-sixty-halvings": dict(check="2.6-mutation", location="ledgers/E4/mutants/mutant_r5_sixty_halvings_no_tolerance.py", status="PASS", evidence="Killed by test_small_noise_root_is_relatively_accurate[1e-09] (seed 0) in the 126/126 run."),
 "E4d5-mutant-uninformed-precision": dict(check="2.6-mutation", location="ledgers/E4/mutants/mutant_r5_uninformed_posterior_precision_informed.py", status="PASS", evidence="Killed in the 126/126 run."),
 "E4d6-mutant-06": dict(check="2.6-mutation", location="ledgers/E4/mutants/mutant_r6_06_cost_scales_whole_gap.py", status="PASS", evidence="Killed in the 126/126 run."),
 "E4d6-mutant-07": dict(check="2.6-mutation", location="ledgers/E4/mutants/mutant_r6_07_unit_informativeness_discounted_by_cost.py", status="PASS", evidence="Killed in the 126/126 run."),
 "E4d6-mutants-new-killed": dict(check="2.6-mutation", location="ledgers/E4/mutants/mutant_r6_0*.py", status="PASS", evidence="All r6 mutants killed in the 126/126 run (r6_08 is in equivalent/, see E4d-equivalent)."),
 "E4d7-cost-above-one-rejected": dict(check="2.6-autograder", location="course/modules/E/E4/grader/test_project.py (test_info_cost_above_one_is_accepted; test_info_cost_far_above_one_is_accepted); project.html:326", status="PASS", evidence="Read: cost above one is accepted (fraction 0 at cost 2.0 and 10, 50); the mutant_r7_03 and r8_03 rejecting above one or five are killed."),
 "E4d7-noise-above-one-rejected": dict(check="2.6-autograder", location="course/modules/E/E4/grader/test_project.py (test_noise_volume_far_above_one_is_accepted)", status="PASS", evidence="Read: noise 50 and 1000 accepted; mutant_r7_02, r4f_rejects_noise_above_one, r8_02 killed."),
 "E4d7-midpoint-untested": dict(check="2.6-autograder", location="course/modules/E/E4/project.html:318; ledgers/E4/equivalent/mutant_r7_01_reports_bracket_lower_end.py", status="FAIL",
    evidence="mutant_r7_01 reports the bracket's lower end and passes 50/50 seeds (out/alternatives_equivalents_0_49.txt). The Constraints (project.html:318) states the stop rule; the midpoint report is stated only in Exemplar B (project.html:619). No output test at the page's accuracy separates the variant from the reference.",
    fix="Architect decision as in E4d-equivalent (state the reported point on the page, or accept the equivalence in writing)."),
 "E4d8-no-upper-bound": dict(check="2.4-scope", location="course/modules/E/E4/project.html:326; grader/reference.py:122-151; grader/test_project.py (far-above-one tests)", status="PASS", evidence="Page names no upper bound on either input inside its range; the reference returns finite outputs for noise up to 1e150 and cost up to 350 (range_extremes_r15.txt)."),
 "E4d8-cap-100-survives": dict(check="2.6-mutation", location="ledgers/E4/mutants/mutant_r8_01_cap_100_halvings.py; project.html:318", status="PASS", evidence="Killed in the 126/126 run (tiny-root tests at 1e-30)."),
 "E4d8-noise-cap-10-survives": dict(check="2.6-mutation", location="ledgers/E4/mutants/mutant_r8_02_noise_above_ten_rejected.py; project.html:326", status="PASS", evidence="Killed in the 126/126 run (noise far above one accepted)."),
 "E4d8-cost-cap-5-survives": dict(check="2.6-mutation", location="ledgers/E4/mutants/mutant_r8_03_cost_above_five_rejected.py; project.html:326", status="PASS", evidence="Killed in the 126/126 run (cost far above one accepted)."),
 "E4d8-mutants-r8-killed": dict(check="2.6-mutation", location="ledgers/E4/mutants/mutant_r8_04_integer_zero_fraction.py; mutant_r8_05_informativeness_at_unit_precision.py", status="PASS", evidence="Both killed in the 126/126 run."),
 "E4d-exemplar-A-calibration": dict(check="2.6-rubric-calibration", location="course/modules/E/E4/project.html:533-597 (Exemplar A, data-scores 2,2,1,2,1)", status="UNVERIFIABLE",
    evidence=f"Blind scoring NOT achieved this round. The stripping script ran first ({S}strip_exemplars.py, output {S}out/exemplars_stripped_blind.txt, which drops aside.annotation, p.exemplar-verdict, h4 and all data-score(s)/data-level/data-criterion attributes), but this verifier had read the round-14 fragment notes, which quote the official scores (A 2,2,1,2,1; B 4,4,4,4,4), before that pass. Blind-derived scores from the stripped prose and the rubric alone: C1 2 (payoff, signal, noise supply, preferences named, equilibrium in words; no coefficient, no formula), C2 2 (method and bracket 0 to 1; no tolerance, stop or boundary rule), C3 1 (one sign, 'should fall', no grid), C4 2 (fixed decimals, no rule), C5 1 (caveat 'depends on the model', no named limit). These match the official scores, but the anchor exposure means they cannot be certified blind.",
    fix="Re-score with a verifier that has not read any prior fragment or any data-score/data-level attribute: run ledgers/E4/scripts/E4-d-r15/strip_exemplars.py on course/modules/E/E4/project.html, score the output with the five rubric descriptors (project.html:525-529), then compare with the official scores; within one level on every criterion closes the row."),
 "E4d-exemplar-B-calibration": dict(check="2.6-rubric-calibration", location="course/modules/E/E4/project.html:598-661 (Exemplar B, data-scores 4,4,4,4,4)", status="UNVERIFIABLE",
    evidence="Same contamination as E4d-exemplar-A-calibration. Blind-derived scores from the stripped prose: C1 4 (assumptions 1-6 numbered, each tied to propositions), C2 4 (method, bracket, tolerance, stop, boundary rule, gap per point), C3 4 (each sign on the 3x3 grid with the points it holds on), C4 4 (4 decimals and 3 significant digits, rule stated, unrounded), C5 4 (limits named, no registry key claimed). Match the official scores; not certifiable blind.",
    fix="Same as E4d-exemplar-A-calibration (score Exemplar B from the stripped output with a fresh verifier)."),
 "E4d4-calibration-blind": dict(check="2.6-rubric-calibration", location="course/modules/E/E4/project.html:533-597 (Exemplar A)", status="UNVERIFIABLE",
    evidence="Same as E4d-exemplar-A-calibration (round-14 row, Exemplar A): blind-derived 2,2,1,2,1 under contaminated conditions.", fix="Same as E4d-exemplar-A-calibration."),
 "E4d5-calibration-B-blind": dict(check="2.6-rubric-calibration", location="course/modules/E/E4/project.html:598-661 (Exemplar B)", status="UNVERIFIABLE",
    evidence="Same as E4d-exemplar-B-calibration (round-14 row, Exemplar B): blind-derived 4,4,4,4,4 under contaminated conditions.", fix="Same as E4d-exemplar-B-calibration."),
 "E4d-exemplar-annotations-hidden-dummy": {},
 "E4d8-alternatives-r8": dict(check="2.6-alternatives", location="ledgers/E4/alternatives/alt_r8_a.py, alt_r8_b.py (round 8)", status="UNVERIFIABLE",
    evidence=f"Files absent at d1e65a0 (ls ledgers/E4/alternatives/ shows alt_1..alt_8 only). The round-8 runs are logged in ledgers/E4/scripts/E4-d-r8/logs/alternatives_seeds0-49.txt, but run_alts_r8.sh reads candidates from a removed worktree (/Users/billyribeiro/.fanout/wt/verifyE8-E4-d). Cannot re-run.",
    fix="Retire this row (the current set alt_1..alt_8 is re-verified in E4d-alternatives), or restore the two candidate files under ledgers/E4/alternatives/ and cite them by repository path."),
 "E4d9-alternatives-v9": dict(check="2.6-alternatives", location="ledgers/E4/alternatives/alt_v9_1_interior_gap_zero.py, alt_v9_2_log_space.py, alt_v9_3_grid_then_bisect.py (round 9)", status="UNVERIFIABLE",
    evidence=f"Files absent at d1e65a0. Round-9 logs exist (ledgers/E4/scripts/E4-d-r9/logs/alternatives_v9_seeds0-49.txt) but the candidate sources are not in the repository. Cannot re-run.",
    fix="Retire this row (the current set alt_1..alt_8 is re-verified in E4d-alternatives), or restore the three candidate files under ledgers/E4/alternatives/ and cite them by repository path."),
})
FRESH.pop("E4d-exemplar-annotations-hidden-dummy", None)

NEW = []
NEW.append(dict(id="E4d15-grader-docstring-scale", check="2.6-autograder-docstring", location="course/modules/E/E4/grader/test_project.py:402-405 (docstring) vs :413 (code)", status="FAIL",
    evidence="The docstring of test_gap_at_an_interior_fraction_is_the_oracle_gap_to_full_precision says the tolerance is 1e-14 relative to the larger of 1 and 'the gap's size at fraction 0'. The code (line 413) uses max(1.0, abs(limit)) where limit = oracle_gap(lam, ...) at the reported interior fraction. Numerically no difference (both scales are 1 for the instances: |gap(0)| = 0.0338 and 0.0286), but the sentence states a quantity the code does not use (verified: ledgers/E4/scripts/E4-d-r15/out/docstring_numbers_r15.txt).",
    fix="Change the docstring to 'relative to the larger of 1 and the oracle's gap at the reported fraction' (the quantity line 413 uses). No numerical change."))
NEW.append(dict(id="E4d15-mutants-single-change", check="2.6-mutation-form", location="ledgers/E4/mutants/*.py (87 files carry MAX_BISECTION_STEPS = 200; the reference uses 240)", status="FAIL",
    evidence=f"Hunk listing with docstrings stripped ({S}out/mutant_hunks.txt): 87 of 126 mutants differ from grader/reference.py in MAX_BISECTION_STEPS (200 vs the reference's 240) in addition to their intended error, so they are not single-change copies (fixer rules). Restoring 240 in each of the 87 copies ({S}cap_fix_check_r15.py, {S}out/cap_fix_check.txt): 86 still fail on seeds 0-9 with their own error; mutant_f11_01 (cap 200 is its intended error) is the only one that survives, as expected. So no kill is lost, but the copies are not what the fixer rules require.",
    fix="Regenerate the 86 mutants from the current grader/reference.py with only their intended change (keep mutant_f11_01 as the cap-200 mutant), re-run tools/mutate_graders.py --unit E4 --seeds 0-9, and record killed_by per mutant."))
NEW.append(dict(id="E4d15-mutants-new-r15", check="2.6-mutation", location="ledgers/E4/mutants/mutant_r15_01..04_*.py", status="PASS",
    evidence=f"Four new student-error mutants written this round from grader/reference.py ({S}make_mutants_r15.py): r15_01 noise coefficient forgets the informed fraction (killed by test_indifference_holds_at_an_interior_fraction[first]); r15_02 signal variance taken as the posterior variance (killed by test_indifference_holds_at_an_interior_fraction[second]); r15_03 gap at zero with power -1 (killed by test_info_cost_above_one_is_accepted); r15_04 bracket starts at [0, 0.5] (killed by test_indifference_holds_at_an_interior_fraction[first]). Each is a single-change copy with the docstring first line naming the error."))
NEW.append(dict(id="E4d15-cmd-mutate", check="2.6-mutation", location="tools/mutate_graders.py --unit E4 --seeds 0-9", status="PASS",
    evidence=f"'mutate_graders E4: PASS (126/126 killed)', exit 0 ({S}out/mutate_graders_E4_0_9_r15.txt). Kill attribution: 21 by test_info_cost_above_one_is_accepted, 18 by test_indifference_holds..., 18 by test_gap_is_the_oracle_gap..., and the rest by named tests (tally run this round)."))
NEW.append(dict(id="E4d15-alternatives-sweep", check="2.6-alternatives", location="ledgers/E4/alternatives/alt_1..alt_8.py; ledgers/E4/equivalent/*.py; grader/starter.py", status="PASS",
    evidence=f"run_candidate.py (grader workspace of run_graders, seeds 0-49): alt_1..alt_8 50/50 each; literal_price_sign.py 50/50; mutant_r6_08, r7_01, v9_02 50/50 (equivalent by design); starter.py 0/50 ({S}out/alternatives_equivalents_0_49.txt). Reference 50/50 ({S}out/reference_0_49.txt)."))
NEW.append(dict(id="E4d15-exemplar-verdicts", check="2.6-rubric", location="course/modules/E/E4/project.html:537, :539, :602, :604 (data-scores and verdict lines)", status="PASS",
    evidence="Verdict lines match data-scores: A 'C1 2 · C2 2 · C3 1 · C4 2 · C5 1' = data-scores 2,2,1,2,1; B 'C1 4 · C2 4 · C3 4 · C4 4 · C5 4' = data-scores 4,4,4,4,4. Annotation claims read in full: e.g. A's C3 annotation says the sign is not the grid's because the informativeness is 0.1420 at each noise volume for cost 0.135 (true, Lab 3)."))
NEW.append(dict(id="E4d15-stop-rule-variants-architect", check="2.6-mutation-ruling9", location="ledgers/E4/equivalent/README.md ('Stop-rule variants', open item)", status="FAIL",
    evidence="Same as E4d-equivalent: the README's open item (ruling 9) is unresolved. The page states the stop rule (project.html:318) and the midpoint report (exemplar B, project.html:619); the three variants violate those statements and no output test at the page's accuracy can separate them.",
    fix="Architect decision recorded in plans/E4-open-items (or the page changed to state the reported point). Until then the unit has a named gap."))
NEW.append(dict(id="E4d15-literal-price-sign", check="2.6-mutation", location="ledgers/E4/equivalent/literal_price_sign.py", status="PASS",
    evidence=f"Provably output-identical: b_u enters only as b_u*b_u (reference.py:73; price_coefficients return is unpacked as _ in uninformed_term, reference.py:84); 3000 random inputs zero difference ({S}out/literal_sign_3000_r15.txt). Equivalent mutant, not a fault (VERIFIER 2.6 item 3)."))
NEW.append(dict(id="E4d15-range-extremes", check="2.4-scope", location="course/modules/E/E4/project.html:326-327 (exception table paragraph)", status="PASS",
    evidence=f"Stated range (noise up to 1e150, cost up to 350) returns three finite keys ({S}out/range_extremes_r15.txt); exp(2*350)=1.014e+304 is finite, exp(4*350) overflows (the page's overflow remark is accurate); the 5.7e-73 bracket bound is 2^-240 (5.66e-73)."))
NEW.append(dict(id="E4d15-plan-and-rulings", check="2.2-spec-vs-plan", location="plans/E4-build-plan.md; plans/FINAL-ARCHITECT-RULINGS.md rulings 15-16", status="PASS",
    evidence="Ruling 15 (blind exemplar scoring) read and applied (strip script; contamination disclosed in E4d-exemplar-A-calibration). Ruling 16 (LX1 notation) does not concern E4. Plan Architect decisions (2026-11-03, 2026-11-05) read; ten mutants and five alternatives requirements checked (10 plan mutants = mutant_01..10 killed; alt_1..alt_8 pass)."))
NEW.append(dict(id="E4d15-reading-and-citations", check="2.1-citations", location="course/modules/E/E4/project.html:683-687 (Reading)", status="PASS",
    evidence="Reading section attributes no statement and characterises neither work (read). Grossman-Stiglitz is not cited (architect decision; plan B1)."))

rows = []
seen = set()
for r in R14["rows"]:
    rid = r["id"]
    if rid in FRESH and FRESH[rid]:
        f = FRESH[rid]
        row = dict(id=rid, check=f["check"], location=f["location"], status=f["status"], evidence=f["evidence"])
        if f["status"] != "PASS":
            row["fix"] = f.get("fix", "")
        rows.append(row)
        seen.add(rid)
    else:
        raise SystemExit(f"round-14 row {rid} has no round-15 evidence")
rows += NEW
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate row ids"
for r in rows:
    if r["status"] == "PASS":
        r.pop("fix", None)
    assert r["status"] in ("PASS", "FAIL", "UNVERIFIABLE")
    if r["status"] != "PASS":
        assert r.get("fix"), r["id"]

# mutants from the round-15 run
mut_lines = (OUT / "mutate_graders_E4_0_9_r15.txt").read_text(encoding="utf-8").split("\n")
mutants = []
for line in mut_lines:
    m = re.match(r"KILLED (\S+): (.*?) -> (\S+)(?: \((seed \d+)\))?$", line)
    if m:
        fname, desc, test = m.group(1), m.group(2), m.group(3)
        mutants.append(dict(id=fname[:-3], description=desc, file=f"ledgers/E4/mutants/{fname}", killed_by=f"{test} {m.group(4) or ''}".strip()))
assert len(mutants) == 126, len(mutants)
missing = [m for m in mutants if not m["killed_by"]]
assert not missing

frag = dict(
    unit="E4", slice="d", round=15,
    verifier="Haiku independent verifier, E4 slice d, round 15 (did not build E4; checkout pinned at d1e65a0, detached)",
    pin="d1e65a0203e386e3246429ba1cf7e723eb6cfbfa",
    base="8e5751c903f0246115eba746afdf5d71f612bb37 (round-14 pin); delta in slice d listed in notes",
    checkout="/Users/billyribeiro/.fanout/wt/verifyE15-E4-d",
    scratch="/tmp/e4d15",
    verified_at="2026-11-08T00:00:00+00:00",
    verdict="FAIL",
    rows=rows,
    mutants=mutants,
    registry_flags=[],
    freshness_flags=[],
    notes=[
        "Delta since the round-14 pin 8e5751c, slice d: course/modules/E/E4/project.html, grader/*, tests/labs/E4/*, ledgers/E4/alternatives/*, ledgers/E4/equivalent/* are byte-identical (git diff empty). Changed in slice d: ledgers/E4/mutants/mutant_r14_01..05 (new files, read: hunks in ledgers/E4/scripts/E4-d-r15/out/mutant_hunks.txt) and plans/FINAL-ARCHITECT-RULINGS.md (rulings 15 and 16, read). Outside slice d but read for the DAG and CARA rows: L06.html (lines 62, 143, 157, 202, 663 changed; cited lines 57, 66, 169 unchanged), L07.html unchanged, L03.html changed (not cited), cards.json (slice e).",
        "Round-14 PASS rows were not carried. Every round-14 row id is kept (159 ids) and re-evidenced from this round's outputs; the six non-PASS round-14 rows keep their ids with the round-15 status and evidence.",
        "Blind exemplar scoring (ruling 15): the stripping script ran before any exemplar annotation was read this round, but this verifier had already read the round-14 fragment notes quoting the official scores. The blind-derived scores (A 2,2,1,2,1; B 4,4,4,4,4) match the official ones exactly, but the calibration is recorded UNVERIFIABLE, not PASS. Fresh verifier needed.",
        "Architect items (not row defects, per the round-13/14 convention, but listed as FAIL rows where ruling 9 requires a decision): the three stop-rule variants and the reported-point question (E4d15-stop-rule-variants-architect, E4d-equivalent). literal_price_sign is provably output-identical and is PASS (E4d15-literal-price-sign). The page does not state the reported point except in exemplar B (project.html:619).",
        "Known inaccuracy disclosed by the page: below noise 1e-50 the solver is inaccurate (sd=1e-300 gives informed_fraction 2.83e-73 and informativeness 0.5 where the closed form gives about 0.159). project.html:327 discloses 'may return an inaccurate value'; no row fails on it. Architect may ask for a fail-loud rule.",
        "Mutant hygiene: 87 of 126 mutants carry an extra MAX_BISECTION_STEPS = 200 change (stale copies); 86 remain killed by their own error when the cap is restored to 240 (out/cap_fix_check.txt). Row E4d15-mutants-single-change.",
        "Not checked by this verifier: lessons L01-L09 and cards.json (other slices); tools/render_curriculum.py, build_site.py --check, fetch_data.py --check (no curriculum, site-data, market or reference input changed in slice d); the full pytest suite; the Pyodide interpreter itself (page_smoke runs the repo harness); verify_refs live for all 560 entries (only the unit's three entries live, and the offline integrity for all); the 50-seed run of the full set of alternatives beyond seeds 0-49; the calibration blind (see above); a hand re-derivation of every alternative's numerical path beyond the 50-seed pass.",
        "Hours: estimate 22 h against the declared 28 h (21% below, inside the 30% bar); declared hours are design targets per the architect ruling.",
        "Commands run from the checkout root with .venv (Python 3.14). Scripts and outputs: ledgers/E4/scripts/E4-d-r15/ and ledgers/E4/scripts/E4-d-r15/out/.",
    ],
    summary="E4 slice d round 15: verdict FAIL. Rows: see counts in the validation output. Non-PASS: E4d15-grader-docstring-scale (test_project.py:402-405 docstring names a different scale than the code); E4d15-mutants-single-change (87 mutants carry a stale cap-200 change); the stop-rule variants (E4d-equivalent, E4d6-spec-variants-08-09, E4d7-midpoint-untested, E4d9-mutant-v9-02, E4d15-stop-rule-variants-architect: architect decision); the blind exemplar calibration (E4d-exemplar-A/B-calibration, E4d4-calibration-blind, E4d5-calibration-B-blind: UNVERIFIABLE, anchor contamination); stale citations (E4d8-alternatives-r8, E4d9-alternatives-v9: UNVERIFIABLE, files absent). All 126 mutants killed on seeds 0-9; alt_1..alt_8 pass 50/50; project labs, grader, page smoke, lint, types, registry and numbers re-derived and PASS.",
)
out = ROOT / "ledgers/E4/E4-d.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "mutants", len(mutants))
from collections import Counter
print(Counter(r["status"] for r in rows))
