"""Round 3 verifier E3-e: writes ledgers/E3/E3-e.json from the round-3 evidence in this checkout's scripts directory."""
import json, re
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD3-E3-e")
S = "ledgers/E3/scripts/E3-e-r3/"
P = "Carried from round 2 (course/modules/E/E3/project.html byte-identical in the changed lines' complement, checked by diff against c737272: changed lines 44,53,69,143,195,201,203,214,224-227,383,395,457-458,532,578,610,671; the carried span is unchanged): "

def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r

rows = [
 row("E3e-01", "2.9 banned strings", "course/modules/E/E3/project.html (visible prose)", "PASS",
     f"{S}r3_check_pages_E3.out: 'check_pages E3: PASS'. Hand scan of the changed hunks for TODO, TBD, lorem, brevity, beyond the scope: no hit."),
 row("E3e-02", "2.9 process words in learner text", "project.html; grader/*.py; tests/labs/E3/lab-E3-project-*.py", "PASS",
     "grep -i -E 'plan |Q12|architect|builder|verifier|ruling|section 10|ledger|slice|TODO|TBD|lorem' over those files: no hit (only L05/L08 use 'plan' as an economic term, outside this slice)."),
 row("E3e-03", "2.9 process references in learner-visible code", "course/modules/E/E3/grader/test_project.py (docstrings)", "PASS",
     "The same grep over grader/*.py: no reference to a plan, a question number or a ruling. Recovery-test docstring 'a threshold of this suite, stated on the project page' (test_project.py:566-570) and score docstring 'a tolerance of this suite stated on the page' (:524-530); neither cites a plan."),
 row("E3e-04", "2.9 links and anchors", "course/modules/E/E3/project.html (34 href/src)", "PASS",
     "Python check (href/src targets exist; '#' anchors exist in the target file): 34 checked, bad: []. No external href/src. page_smoke project PASS (r3_page_smoke_project.out)."),
 row("E3e-05", "2.9 structure; 2.6 ladder and spec sections", "project.html:40-230", "PASS",
     f"{S}r3_check_projects_E3.out: 'check_projects E3: PASS'. Ladder has four rungs (:43-48); spec dl has Context, Inputs, Required outputs, Constraints, Grading mode, Reading list (:193-206); Conventions (:208-216); exception table (:218-230)."),
 row("E3e-06", "2.6 hours arithmetic", "project.html:352-358; index.html:29; curriculum/02-economics-finance-core.yaml:91", "PASS",
     "Rows 1+1+3+4+3+2 = 14 (:352-358) = data-hours-project=14 (:33). index.html:29 data-hours-lessons=56; 56+14=70 = curriculum hours 70 (yaml:91)."),
 row("E3e-07", "2.6 rung 3 matches curriculum scope exactly", "project.html:195, 199, 203 vs curriculum/02-economics-finance-core.yaml:116-121", "PASS",
     "Brief (yaml:118-121) names gamma and lambda; the page estimates kappa too (:195 discloses it). Plans/E3-build-plan.md:551-553 (open question 4) RECOMMENDS 'a logit choice rule with precision kappa, and three estimated parameters', and the binding header 'Architect decisions (2026-10-28, binding)' (plans/E3-build-plan.md:669) says 'Where the plan states a recommendation for an open question, follow it.' So the three-parameter scope is the binding decision and the page discloses the deviation from the brief wording. Judgement: PASS on that basis; the parent may overrule (the round-2 'exactly' reading is stricter)."),
 row("E3e-08", "2.6 spec completeness (questions a student would ask): exception table names functions", "project.html:224-227", "PASS",
     "Rows now name the function: :224 certainty_equivalent_cents; :225 certainty_equivalent_cents, log_likelihood and estimate; :226 certainty_equivalent_cents; :227 estimate. Tests: model name test_model_name_must_be_crra_or_prospect (test_project.py:286); probability rule for CE test_probabilities_must_be_nonnegative_and_sum_to_exactly_one (:300-357); for log_likelihood test_log_likelihood_refuses_a_sum_below_one/above_one/a_negative_probability (:439-468); for estimate test_estimate_refuses_* (:739-780); wealth test (:358); empty responses test_estimate_needs_responses (:609). r3_mutate: e2_01 (log_likelihood skips probability checks) KILLED."),
 row("E3e-09", "2.6 rubric level descriptors observable (C1)", "project.html:600 (C1, level 1 cell)", "PASS",
     P + "rubric cell :600 unchanged; re-read: level 1 'No instrument described: no count of pairs, no prize scale, and no pair shown.'"),
 row("E3e-10", "2.6 rubric descriptors and calibration (C5)", "project.html:604, 612-614, 657-659", "PASS",
     P + "lines 604, 612-614 and 657-659 unchanged; Exemplar A C5 level 1 and the official C5 1 are consistent with the level 1 descriptor ('no empirical claim ... has a grade or a registry key')."),
 row("E3e-11", "2.6 rubric structure", "project.html:596-606 (rubric), :612, :665 (exemplars), :727-731 (self-assessment)", "PASS",
     P + "the rubric table and the self-assessment block are byte-identical; exemplar article tags :612 and :665 read (data-level/data-scores/verdict agree: A 2,2,1,2,1; B 3,4,4,3,4)."),
 row("E3e-12", "2.6 calibration of both exemplars (blind scoring)", "project.html:665-725 (Exemplar B), :675 (C1 annotation), :687 (C2 annotation)", "FAIL",
     "Blind scoring of Exemplar B against the descriptors: C1 3 (count, cents, a reason for losses at :671 'The pairs include losses because a lottery whose prizes are all gains, or all losses, has a certainty equivalent that does not depend on lambda', two pairs, pair 0 and pair 3, verified in r3_exemplar_b_facts.out). The round-2 C1 defect is RESOLVED. C2 4 is not supported: the C2 level-4 element is 'states which pairs identify loss aversion and which identify precision'. The memo gives the loss-aversion pairs, but the precision identification is only 'I expect, without computing it here, that precision is identified by the spread of the differences in certainty equivalent ... that is a hypothesis for you to test' (:683). The annotation at :687 says 'Meets C2 level 4', so the official C2 4 (:665 data-scores, :667 verdict) rests on an untested hypothesis. Other criteria: C3 4, C4 3, C5 4 agree with the descriptors.",
     "Either state the precision identification as a result with its computation (the page must then show it, e.g. by a printed lab check), or re-score Exemplar B C2 as 3: data-scores '3,3,4,3,4' at :665, the C2 figure in the verdict at :667, and the annotation at :687 must say level 3."),
 row("E3e-13", "2.6 exemplar length claims", "project.html:610 (length of Exemplar A and B)", "FAIL",
     f"{S}r3_exemplar_counts.out (HTML parser, runs of characters between spaces, tags removed): Exemplar A 103 words headings included (matches :610). Exemplar B 554 words headings included (per block 150, 162, 83, 99, 60); 543 with headings excluded; 562 with TeX spans as one token. Page :610 says 408. Block 1 cross-checked with wc -w (150). Neither method gives 408.",
     "Change '408' in project.html:610 to 554 (headings included, the stated method), or state the method that gives 408 (none found)."),
 row("E3e-14", "2.2 numbers in exemplars and prose", "project.html:57, 138, 143, 383-394, 571-577, 610-721", "PASS",
     f"{S}r3_exemplar_b_facts.out: prizes range -18700..19000 (page: -18 700 and 19 000); every lottery has 2 or 3 prizes; probabilities sum to exactly 1; 11 of 12 pairs mixed. Pair 0 and pair 3 as printed in the memo. Lab output {S}r3_lab_twin_check.out matches the expected blocks; estimates 0.6352/6.1503/2.0201, SE 0.32/9.59/1.86, log-likelihood -7.1445, largest score 3.55e-10 match Lab 3."),
 row("E3e-15", "2.1 reading list: registry keys, freshness, attribution", "project.html:743-752; course/modules/E/E3/L07.html:80; L08.html:67, :133; L02.html:616", "PASS",
     "references/references.json: the five keys exist (pratt1964risk, kahneman1979prospect, epstein1989substitution, ellsberg1961risk, gilboa1989maxmin), status verified. Claims: L07:80 kahneman (grade C, title only); L08:67 gilboa (C); L08:133 ellsberg (C); L02:616 Pratt 'for the name only'. Three keys carry a claim in Lessons 5-8, as project.html:744 says. verify_refs offline: r3_verify_refs_offline.out (560 entries, 0 problems)."),
 row("E3e-16", "2.1 attribution on the project page", "project.html:205, :744", "PASS",
     "Page attributes no statement to any registry key (:205, :744). The page has no class=claim element (grep), so the every-claim clause is vacuous here; the page's only attributions are the Lesson citations, each checked in E3e-17."),
 row("E3e-17", "2.4 definitions cited from the page", "project.html:53, :210; L02.html:98; L03.html:88, :173; L06.html:69, :89", "PASS",
     "Anchors exist: L02 def-certainty-equivalent, L03 def-crra-utility, L06 def-prospect-theory (grep id=\"def-\"). L06 Definition 1.2 (value function) and Definition 1.3 (prospect value) match the page's convention at :210. L03 Proposition 2.7 (affine transformations leave CEs unchanged; L03.html:173) matches :53."),
 row("E3e-18", "2.5 Lab 1 prose vs code (CRRA utility)", "project.html:53, :57, :82-83, :120-126, :138", "PASS",
     f"{S}r3_lab_twin_check.out: page code == twin (True); twin under python -I -W error exit 0; output == expected (True). Prose values 496/500, -30/500, P(A)=0.480149, log -0.733658, sum -2.302315, 3000 and -762 match the output. Prose 'a positive multiple of W^(1-gamma)/(1-gamma)' is correct for gamma<1."),
 row("E3e-19", "2.5 Lab 1 (worked example)", "project.html:55-139; tests/labs/E3/lab-E3-project-1.py", "PASS",
     f"{S}r3_lab_twin_check.out (as E3e-18). The hypothesis block (:57) and the interpretation (:138) agree with the printed lines."),
 row("E3e-20", "2.5 Lab 2 (completion problem)", "project.html:141-188; tests/labs/E3/lab-E3-project-2.py", "PASS",
     f"{S}r3_lab_twin_check.out: the page shows the blanked code (its differences from the twin are exactly the two blanks, which is the design); twin exit 0; twin output == expected block (-0.765595182, -0.625595182, 0.465057055, True, True). Prose z = -0.14 (2*(1500-2200)/10000) is correct."),
 row("E3e-21", "2.5 Lab 3 (reference case) and its prose", "project.html:381-579; tests/labs/E3/lab-E3-project-3.py", "PASS",
     f"{S}r3_lab_twin_check.out: page code == twin; twin exit 0; output == expected (answers 12, mixed 11, gamma 0.6352, se 0.32, lambda 6.1503, se 9.59, kappa 2.0201, se 1.86, log-likelihood -7.1445, score 3.55e-10, domain True). Prose 'standard error of lambda larger than lambda' (9.59 > 6.1503) holds."),
 row("E3e-22", "2.5 lab and code gates", "tests/labs/E3/*; grader/*.py; project.html", "PASS",
     f"{S}r3_run_labs_E3.out: run_labs E3: PASS (11/11). {S}r3_pytest_labs_E3.out: 15 passed (tests/test_labs.py -k E3). ruff check and format --check on the grader and twins: {S}r3_ruff_check.out, r3_ruff_format.out (all passed). mypy --no-incremental: {S}r3_mypy.out (331 files, no issues)."),
 row("E3e-23", "2.4 mathematics on the page (conventions, identification, delta method)", "project.html:53, :195-214", "PASS",
     "Half-cent rule floor(c+1/2) (:211) gives 2.5->3, -0.5->0 (checked). z-scale 'per $100' (:212) matches the code (z = kappa*dCE/10000). Identification (:213): the gain branch has no lambda, and the loss branch divides out lambda, so an all-gain or all-loss lottery has a CE free of lambda (checked algebraically and in the grader's oracle). Delta-method statement (:214) is the standard first-order rule."),
 row("E3e-24", "2.4 notation: one symbol, one meaning across the unit (plan section 4)", "project.html:214, :394-395, :434, :436, :439; plans/E3-build-plan.md:207-210; course/modules/E/E3/L05.html:131; L08.html:541", "FAIL",
     f"Registry symbols: no use of T, gamma_3, gamma_4, R^ast, R^{{e ast}}, R_f, \\mathbb{{Q}}, raw \\mathbb{{E}} in E3 pages ({S}r3_symbol_uses_in_math.out). The round-2 collisions are resolved: eta renamed to upsilon/chi in L02 (git diff c737272..a007712), zeta no longer used in L02, kappa no longer a CARA coefficient in L08 (L08 uses nu). Remaining collision: theta. Plan section 4 (plans/E3-build-plan.md:207-210) fixes theta = (1-gamma)/(1-1/psi) as the Epstein-Zin exponent ratio 'so that one symbol has one meaning across the unit'; L05 Remark 3.1 (L05.html:131) uses it so. The project uses theta for the coordinate vector (project.html:214 'g(theta)', :394-395, :434 'theta = (zeta, log lambda, log kappa)', :436; grader/reference.py:178-179 and the lab-3 twin use the same name). L08.html:541 uses theta as a mixture weight.",
     "Rename the project's coordinate vector (for example to xi) in project.html:214, :394-395, :434 and in the lab-3 twin and grader variables; rename L08's mixture weight (L08.html:541-543) to a symbol the plan does not reserve. Outside this slice, L01.html:86 uses alpha as a mixture weight while plan section 4 reserves alpha as the value exponent: report to the unit's notation owner."),
 row("E3e-25", "2.9 DAG: concepts used outside the unit's prerequisite closure", "project.html:53, :57-61, :214, :578; check_dag output", "PASS",
     f"{S}r3_check_dag.out: check_dag E3: PASS. Concept links in project.html are only prospect-theory, certainty-equivalent and crra-utility (grep data-concept), all E3 lessons inside the closure."),
 row("E3e-26", "2.9 terms used before definition", "project.html:53, :197, :214", "PASS",
     "logit is defined in the same paragraph at :53; score is defined at :203; observed information and identification are defined at :213-214 before the grader text uses them."),
 row("E3e-27", "2.9 scope words", "project.html:201, :203, :212-215", "PASS",
     "'every named invalid input' (:201): each table row has a test (see E3e-08). 'every model whose utility' is no longer used in the grader comments; the comments at test_project.py:964 and :968 now say 'the increasing models that this suite uses'."),
 row("E3e-28", "2.6 autograder claims stated on the page", "project.html:201-203, :366, :372-374", "PASS",
     "45 checks (collect-only {S}r3_collect_only.out = 45). Recovery: 47 of 50 seeds, 4 SEs (test_project.py:566-583). Score: 2e-5 with steps 1e-5 and 1e-6, smaller largest component (test_project.py:524-549). No print or warning: test_engine_imports_only_the_standard_library_with_no_network_and_prints_nothing (test_project.py:1073)."),
 row("E3e-29", "2.6 reference passes seeds 0-49", "grader/reference.py; tools/run_graders.py --unit E3 --seeds 0-49", "PASS",
     f"{S}r3_run_graders_0_49.out: 'run_graders E3: PASS (reference 50/50 seeds, slowest 14.0 s)'."),
 row("E3e-30", "2.6 mutation: every mutant killed (existing and new)", "ledgers/E3/mutants/ (76 files)", "PASS",
     f"{S}r3_mutate_E3_0_9.out: 'mutate_graders E3: PASS (76/76 killed)', seeds 0-9. The restored r10n06 (logit overflow) is killed by test_log_likelihood_stays_finite_for_a_large_choice_precision; e2_01 is killed by test_log_likelihood_refuses_a_sum_below_one. ledgers/E3/equivalent/ no longer exists."),
 row("E3e-31", "2.6 three new student-error mutants written by the verifier", "ledgers/E3/mutants/e3e3_01..03", "PASS",
     "Three mutants written for this round (student errors): e3e3_01 naive logistic choice probability (overflow at large negative z) KILLED by the large-kappa test; e3e3_02 estimates rounded to four decimals KILLED by test_score_is_zero_at_the_estimate; e3e3_03 likelihood sum skips the first response KILLED by test_log_likelihood_matches_oracle_at_the_true_parameters. Their files were already present (untracked) in this checkout when the round started; their content and kill status were re-checked here."),
 row("E3e-32", "2.6 alternative correct implementations (over-constraint)", "ledgers/E3/scripts/run_alternatives.py (alt1-alt5), seeds 0-49", "PASS",
     f"Fresh runs at a007712 (ledgers/E3/scripts/E3-e-r2/run_alt_one_r2.py, 50 seeds each): {S}r3_alt_alt1_0_49.out PASS 50/50; r3_alt_alt2_0_49.out PASS 50/50; r3_alt_alt3_0_49.out PASS 50/50; r3_alt_alt5_0_49.out PASS 50/50; alt4 in five windows r3_alt4_0-9 ... r3_alt4_40-49, each PASS 10/10."),
 row("E3e-33", "2.6 test count on the page equals collect-only", "project.html:203 ('45 checks'); grader/test_project.py", "PASS",
     f"{S}r3_collect_only.out: 45 tests collected (against a reference copy as elicit.py). Page line 203 says 45; the in-browser run prints 'All 45 tests pass' ({S}r3_page_smoke_project.out)."),
 row("E3e-34", "2.6 exception table: conditions and messages", "project.html:218-230; grader/reference.py:30, :60, :121, :138; test_project.py:286-383, :557-602", "PASS",
     "Each row of the table has a test that demands the named type and, where the table quotes a message, checks the text (must_raise contains=...). The reference passes them (run_graders 50/50)."),
 row("E3e-35", "2.8 figures (cards: not in this slice)", "project.html (no figure); course/modules/E/E3/cards.json (not read)", "PASS",
     "project.html has no svg, figure or img (grep). cards.json is outside this slice and was not read."),
 row("E3e-36", "2.1 reference registry integrity (live)", "references/references.json (5 E3 keys)", "PASS",
     f"{S}r3_verify_refs_offline.out: 560 entries, 0 problems. The five E3 keys are present with status verified (python read of entries)."),
 row("E3e-37", "2.9 interactive questionnaire and privacy claims", "project.html:235, :239-343, :765; course/assets/js/grader.js:18; store.js", "PASS",
     "The questionnaire script (project.html:239-343) makes no network call. grader.js:18 fetches only the page's own grader files by relative URL. store.js saves to IndexedDB (local). page_smoke project: zero requests to any host but the local server ({S}r3_page_smoke_project.out). No JS or hub file changed since c737272 (git diff --stat)."),
 row("E3e-38", "2.6 rung 4 open-ended", "project.html:734-740", "PASS",
     "Two open-ended extensions; the probit link uses Phi, the registered standard normal CDF (notation/notation.json \\Phi). The text states the hypothesis to be tested."),
 row("E3e-39", "2.6 suite gap: named probability condition for log_likelihood", "grader/test_project.py:439-476", "PASS",
     "New tests test_log_likelihood_refuses_a_sum_below_one, _above_one, _a_negative_probability (each must_raise with 'probabilities must sum to 1') and accepts_probabilities_that_sum_to_exactly_one. Mutant e2_01 (log_likelihood skips the checks) is KILLED (r3_mutate_E3_0_9.out)."),
 row("E3e-40", "2.2 prose number in a docstring", "grader/test_project.py:873-888 (test_standard_errors_match_the_coordinate_change_oracle docstring)", "PASS",
     f"Re-derived with the suite's own oracle at QF_SEED=49 ({S}r3_se_seed49.py, {S}r3_se_seed49.out): forward se_lambda 135.054 (step 1e-5), 97.675 (1e-6); se_gamma 0.09474, 0.07983; lambda -27.68%, gamma -15.73% from 1e-5 to 1e-6. Reverse order: lambda 136.779 (+1.28%, docstring '+1.3%', '135.05 to 136.78') and 98.086 (+0.42%, docstring '+0.4%', '97.67 to 98.09'). All printed numbers in the docstring reproduce. The round-2 '1.3%' sentence in the old docstring is gone."),
 row("E3e-41", "2.6 equivalent-mutant README and cited ruling", "ledgers/E3/equivalent/README.md (removed); plans/E3-open-items.md", "PASS",
     "ledgers/E3/equivalent/ does not exist at a007712 (ls). r10n06 is back in ledgers/E3/mutants/ and killed (E3e-30). No ruling is cited for it. The open-items file has no ruling about overflow."),
 row("E3e-42", "2.4 rename consistency (eta -> zeta; kappa)", "project.html; grader/test_project.py; tests/labs/E3/lab-E3-project-3.py", "PASS",
     "grep: no eta in project.html, grader or lab-3 twin; zeta and kappa used consistently (the coordinate definitions at project.html:203, :214 and test_project.py match)."),
 row("E3e-43", "2.8 instance docstrings vs code (instance.py)", "course/modules/E/E3/grader/instance.py:1-28, :53-259", "PASS",
     "Docstring bullets vs code: gamma in [0.10, 0.80] (round(uniform(0.10,0.80),3), :212); lambda [1,3] (:213); kappa [0.5,5] (:214); wealth 50,000-200,000 dollars (randrange(5_000_000, 20_000_001, 100) cents, :215); 200 pairs (_PAIRS=200, :45); magnitudes 500..50000 cents (= $5-$500, :60); denominators (4,5,10,20) (:44); >= 100 mixed pairs (_MIN_MIXED_PAIRS=100, :48, used at :232); Hessian negative definite (:235); boundary margin 0.5 (_BOUNDARY_MARGIN=0.5 :147, used at :237); half-cent margin 1e-6 (_TIE_MARGIN :43, used at :101 and :249). The new _boundary_loglik docstring (:151-157) matches its use at :237."),
 row("E3e-44", "2.6 dominance witnesses and verdict oracle", "grader/test_project.py:960-968 and :1013-1043", "PASS",
     "FIRST_ORDER_MODELS has three entries (crra 0, crra 0.5, prospect TRUE) and its comment says 'the increasing models that this suite uses'; SECOND_ORDER_MODELS has two (crra 0, crra 0.5) and its comment (for gamma > 0 the prospect value is convex below zero) is correct: v''(x) = lambda(1-gamma)gamma(-x)^(-gamma-1) > 0 for x < 0 when gamma > 0. Tests pass on the reference (run_graders)."),
 row("E3e-45", "2.6 failure messages name the property and never leak the answer", "grader/test_project.py:43-62 and every expect()", "PASS",
     "expect() and must_raise() take a property hint; the hints name the property and contain no computed value (read in full)."),
 row("E3e-46", "2.6 same suite in Pyodide and local pytest", "page_smoke project; tools/run_graders.py", "PASS",
     f"{S}r3_page_smoke_project.out: 'in-browser grader: All 45 tests pass'; r3_run_graders_0_49.out: 50/50 reference."),
 row("E3e-47", "2.6 hours estimate (verifier's own)", "project.html:352-358", "PASS",
     "Time budget rows as E3e-06; each rationale names the component the hours buy; 14 hours is the sum."),
 row("E3e-48", "2.8 SIMULATED labels and no real data", "project.html:53, :57, :61, :143, :197, :366, :379, :383, :386, :671", "PASS",
     "Lab 1 and Lab 3 data are labelled SIMULATED; Lab 2 is stated as 'stated values, not data'; instance.py docstring: nothing is a real participant."),
 row("E3e-49", "2.9 page_smoke: console errors, math, external requests", "project.html", "PASS",
     f"{S}r3_page_smoke_project.out: 'page_smoke modules/E/E3/project.html: PASS'; 'page_smoke E3: PASS'."),
 row("E3e-50", "2.6 over-constraint: a correct implementation crashes the standard-error oracle", "grader/test_project.py:873-909 (the skip at :890-891)", "PASS",
     "The step with a non-positive inverse diagonal is skipped (test_project.py:890-891). Alternatives alt2 and alt4 (the two that failed on seed 49 in round 2) now PASS 50/50 (r3_alt_alt2_0_49.out; r3_alt4_40-49.out covers seed 49: PASS 10/10)."),
]

mutant_lines = (ROOT / S / "r3_mutate_E3_0_9.out").read_text(encoding="utf-8").splitlines()
mutants = []
for line in mutant_lines:
    m = re.match(r"KILLED (\S+): (.*?) -> (\S+) \(seed (\d+)\)", line)
    if m:
        mutants.append({"id": m.group(1).removesuffix(".py"), "description": m.group(2),
                        "killed_by": f"{m.group(3)} (seed {m.group(4)})", "file": f"ledgers/E3/mutants/{m.group(1)}"})
assert len(mutants) == 76, len(mutants)

counts = {}
for r in rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
verdict = "PASS" if counts.get("PASS") == len(rows) and all(m.get("killed_by") for m in mutants) else "FAIL"
frag = {
    "unit": "E3", "slice": "e", "round": 3,
    "verifier": "Claude Haiku 5.5, independent verifier for E3-e, round 3 (did not build E3; fresh checkout; read VERIFIER_RULES and the verifier rules file; round-2 fragment used as context only)",
    "pin": "a007712f", "base": "c737272f (round-2 pin); delta c737272..a007712 read for every E3-slice hunk (project.html, grader/*.py, lab-E3-project-1/3, L02-L04, L08, cards, plans, ledgers)",
    "checkout": str(ROOT), "scratch": "/tmp/e3e_r3/", "verified_at": "2026-11-03T08:55:00+00:00",
    "verdict": verdict, "rows": rows, "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [
        "plans/E3-open-items.md:147 (architect ruling, round 13) states the exemplar memo lengths as 103 and 375 words; the page now says 408 for Exemplar B and the measured count is 554. The ruling text is stale."
    ],
    "notes": [
        "Commands and outputs: ledgers/E3/scripts/E3-e-r3/ (r3_*.out). Long runs: run_graders 0-49 (50/50), mutate_graders 0-9 (76/76), alternatives alt1-alt5 seeds 0-49 (all 50/50, alt4 in windows).",
        "Lab twins: r3_lab_twin_check.py compares page code with each twin (Lab 2 differs only by its two blanks, by design), runs each twin under python -I -W error, and compares output with the expected block.",
        "Judgement calls, for the parent: E3e-07 PASS rests on the binding plan recommendation (plans/E3-build-plan.md:551-553 with the header at :669). E3e-12 FAIL on C2 is a calibration judgement: the precision identification in Exemplar B is an explicit hypothesis, not a stated result.",
        "Round-2 rows E3e-07 (scope), E3e-08 (table), E3e-12 (C1 part), E3e-24 (eta/zeta/kappa part), E3e-30, E3e-32, E3e-39, E3e-40, E3e-41, E3e-50 re-verified from scratch at a007712; PASS rows were re-read where their subject changed.",
        "Not checked: the full hours of cards.json and the rest of the slice's cards (outside slice e); notation outside E3 pages; the live pytest of the whole repository (not in scope); L01 alpha collision reported only as an observation.",
    ],
    "summary": {"rows": len(rows), "pass": counts.get("PASS", 0), "fail": counts.get("FAIL", 0),
                "unverifiable": counts.get("UNVERIFIABLE", 0), "mutants_killed": sum(1 for m in mutants if m.get("killed_by")),
                "mutants": len(mutants)},
}
out = ROOT / "ledgers/E3/E3-e.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, frag["summary"], frag["verdict"])
