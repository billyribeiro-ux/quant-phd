"""Write the round-5 verifier fragment ledgers/E3/E3-e.json from the run outputs in ledgers/E3/scripts/E3-e-r5/.

The verdict is not asserted here: it is PASS only when every row is PASS and every mutant is killed (ledger.py rule).
Run from the checkout root: python -I ledgers/E3/scripts/E3-e-r5/write_fragment_r5.py
"""

import json
import pathlib
import re

ROOT = pathlib.Path.cwd()
S = "ledgers/E3/scripts/E3-e-r5"
mut_out = (ROOT / S / "mutate_graders_E3_seeds0-9_r5.out").read_text(encoding="utf-8").splitlines()
new_out = (ROOT / S / "kill_new_mutants_r5.out").read_text(encoding="utf-8").splitlines()

mutants = []
for line in mut_out:
    m = re.match(r"^(KILLED|SURVIVED) (\S+?)\.py: (.*) -> (.*)$", line)
    if not m:
        continue
    status, stem, desc, killed = m.groups()
    mutants.append({
        "id": stem,
        "description": desc,
        "file": f"ledgers/E3/mutants/{stem}.py",
        "killed_by": None if killed.strip() == "None" else killed.strip(),
    })
for line in new_out:
    m = re.match(r"^(KILLED|SURVIVED) (\S+?)\.py: (.*) -> (.*)$", line)
    if not m:
        continue
    status, stem, desc, killed = m.groups()
    mutants.append({
        "id": stem,
        "description": desc,
        "file": f"ledgers/E3/mutants/{stem}.py",
        "killed_by": None if killed.strip() == "None" else killed.strip(),
    })

GATE_NOTE = "ledgers/E3/scripts/E3-e-r5/"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


CARRY = "Carried from round 4 (grader/instance.py byte-identical since the previous pin 4eb6788f, checked with git diff --quiet): "

row("E3e-01", "2.9 banned strings in learner-visible prose (BUILDER_RULES 1.3-1.4; check_pages 58-73); ellipsis outside code",
    "course/modules/E/E3/project.html; course/modules/E/E3/index.html",
    "PASS",
    "Re-run on pin 440ed3c8: grep -n -i for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an "
    "exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly "
    "and three-dot ellipses over both pages: no hits. check_pages E3: PASS (check_pages_E3.out).")

row("E3e-02", "2.9 process words in learner text (build, builder, round, verifier, REQUESTS, unit report)",
    "course/modules/E/E3/project.html (visible text)",
    "PASS",
    "grep -n -i -w for builder, verifier, build, REQUESTS, round followed by a digit, unit report on project.html: no hits "
    "('rounded' only, in grader docstrings).")

row("E3e-03", "2.9 process references in learner-visible code and docstrings (grader and project lab twins)",
    "course/modules/E/E3/grader/*.py; tests/labs/E3/lab-E3-project-1.py, -2.py, -3.py",
    "PASS",
    "grep -n -i for round (not rounded), verifier, builder, planner, plan over grader/*.py and the three project twins: no hit "
    "that is a process reference.")

row("E3e-04", "2.9 links and anchors: every href, file target, fragment and concept link",
    "course/modules/E/E3/project.html; course/modules/E/E3/index.html",
    "PASS",
    f"{GATE_NOTE}links_r5.py over the pin: project.html 34 links, index.html 27 links, all OK (links_r5.out). Concept links "
    "L06.html#def-prospect-theory, L02.html#def-certainty-equivalent and L03.html#def-crra-utility resolve to dfn ids.")

row("E3e-05", "2.9 structure: hub, lessons, project page complete in BUILDER_RULES order; 2.6 ladder present and in order",
    "course/modules/E/E3/project.html:40-48 (ladder), 51 (rungs), 191 (spec), 233 (questionnaire), 346 (budget), 364 "
    "(autograder), 370 (local), 377 (rung 3 report), 736 (stretch), 744 (reading), 756 (references)",
    "PASS",
    "Section order read in full at 440ed3c8; rung titles 1 to 4 at lines 44-47 in order; check_projects E3: PASS "
    "(check_projects_E3.out); check_pages E3: PASS (check_pages_E3.out).")

row("E3e-06", "2.6 hours arithmetic: budget rows sum to the project hours; hub split sums to 70",
    "course/modules/E/E3/project.html:352-358 (table id=hours), :33 data-hours-project; index.html data-hours-lessons",
    "PASS",
    "Budget rows 1+1+3+4+3+2 = 14 (project.html:352-357) equal the hub's data-hours-project=14; index.html data-hours-lessons=56; "
    "eight lessons each data-hours=7 (grep) = 56; 56+14 = 70 = curriculum.")

row("E3e-07", "2.6 rung 3 matches the curriculum scope exactly",
    "course/modules/E/E3/project.html:195-203; curriculum/02-economics-finance-core.yaml:116-123",
    "PASS",
    "Curriculum brief: questionnaire, estimate risk-aversion and loss-aversion parameters by MLE, report the uncertainty, deliverable "
    "instrument plus estimation report, grading both. Page adds kappa as the third estimated parameter, which architect ruling 6 "
    "(plans/FINAL-ARCHITECT-RULINGS.md item 6) permits; no other scope change found.")

row("E3e-08", "2.6 spec completeness: questions a competent student would still need to ask",
    "course/modules/E/E3/project.html:191-231 (spec, conventions, exception table); grader/starter.py:17,28,33",
    "PASS",
    "Read in full. Signatures on the page equal grader/starter.py:17,28,33 and the three functions. Response and instrument formats "
    "(keys, probability text) are given at lines 197 and 235. No unanswered question found. Questions considered: wealth in the "
    "prospect model (answered, line 210); kappa bounds (answered, line 214); zero-probability prizes (answered, line 215).")

row("E3e-09", "2.6 rubric: C1 level descriptors are observable",
    "course/modules/E/E3/project.html:600 (C1 row), :592 (scoring rule)",
    "PASS",
    "Each C1 level names countable items (pairs, cents, two example pairs, pairs that mix a gain and a loss). Observable.")

row("E3e-10", "2.6 rubric: C5 descriptors observable; exemplar annotations match the descriptors they cite (evidence criterion)",
    "course/modules/E/E3/project.html:604 (C5 row), :665 (exemplar B data-scores), :722-723 (exemplar B C5 annotations)",
    "PASS",
    "Round 4 failure cured. Level 3 descriptor (:604) is 'marked as a computed result of Lab 3'; the level 3 annotation (:722) cites that "
    "element; the level 4 miss (:723) cites the missing registry key and derivation; exemplar B data-scores C5 = 3 (:665).")

row("E3e-11", "2.6 rubric structure: five criteria, four levels each; exemplar annotations carry data-criterion and data-level",
    "course/modules/E/E3/project.html:594-607 (table id=rubric); :612-727 (exemplars)",
    "PASS",
    "Five rows C1-C5, four level columns each. Every annotation carries data-criterion and data-level (grep).")

row("E3e-12", "2.6 calibration: each exemplar scored blind from the rubric alone; scores within one level of the annotations on every criterion",
    "course/modules/E/E3/project.html:612-663 (exemplar A), :665-727 (exemplar B)",
    "PASS",
    "Scored each memo against the rubric text at :600-604 and then compared. Exemplar A: 2,2,1,2,1 against annotated 2,2,1,2,1. "
    "Exemplar B: 3,3,4,3,3 against annotated 3,3,4,3,3. Every criterion within one level; A and B match exactly.")

row("E3e-13", "2.6 exemplar length claims (word counts quoted on the page)",
    "course/modules/E/E3/project.html:610 ('117 words' for A, '435 words' for B)",
    "FAIL",
    f"{GATE_NOTE}exemplar_counts_r5.out (HTMLParser, browser-faithful, whitespace runs, headings included): A 117 (correct), B 582. "
    f"{GATE_NOTE}exemplar_words_regex_r5.out: the 435 comes from a regex tag stripper, which treats the literal '<' in "
    "'\\(0<\\gamma<1\\)' as the start of a tag and deletes text (28 raw '<' in the memo). The count the page's own rule gives is 582. "
    "Also plans/E3-open-items.md:147 still says 103 and 375 (stale).",
    "project.html:610: replace '435 words' by '582 words' (tags removed by an HTML parser, runs of non-whitespace, headings "
    "included). Architect to update plans/E3-open-items.md:147 (it quotes 103 and 375).")

row("E3e-14", "2.2 numbers in exemplars and prose re-derived (exemplar numbers, lab numbers, pair values, grader docstring numbers)",
    "project.html:53, :57, :138, :143, :383-386, :571-577, :610-721; grader/test_project.py:883-885",
    "PASS",
    f"{GATE_NOTE}labs_recompute_r5.out (independent code: Lab 1 CRRA 496/500, prospect -30/500, P(A) 0.480149, log -0.733658, total "
    f"-2.302315; pair 2 CRRA 3000/-513, prospect -762; pair 3 2166/1244, 2144/140; Lab 2 -0.765595182 and -0.625595182; Lab 3 "
    f"0.6352, 6.1503, 2.0201, -7.1445). {GATE_NOTE}lab3_se_r5.out: SE 0.32, 9.59, 1.86; largest score 1e-10 to 4e-10. "
    f"{GATE_NOTE}seed49_se_r5.out and seed49_reverse_r5.out reproduce the docstring numbers 135.05, 97.67, 0.09474, 0.07983, "
    "136.78, 98.09; the percentages -27.7, -15.7, +1.3, +0.4 recomputed. instrument_facts_r5.out: prizes -18700..19000, two or three "
    "prizes per lottery, probabilities sum to 1, 11 of 12 pairs mixed.")

row("E3e-15", "2.1 reading list: registry keys cited, and the statements about which lessons cite which key",
    "course/modules/E/E3/project.html:746 (reading paragraph); L02.html; L05.html:609; L07.html:80; L08.html:67,133",
    "PASS",
    "grep -n data-cite L0*.html: kahneman1979prospect (L07.html:80), gilboa1989maxmin (L08.html:67), ellsberg1961risk (L08.html:133), "
    "all grade C with title-only locators. pratt1964risk occurs in no L0*.html file. epstein1989substitution occurs only at "
    "L05.html:609 (reference note, no data-cite). L02 carries no key. The page's statement matches each of these.")

row("E3e-16", "2.1 attribution on the project page: titles and keys match the registry records",
    "project.html:744-752; references/references.json (five E3 keys)",
    "PASS",
    "Records: pratt1964risk (Econometrica 32, 1/2, 1964), kahneman1979prospect (Econometrica 47, 2, 1979), epstein1989substitution "
    "(Econometrica 57, 4, 1989), ellsberg1961risk (QJE 75, 4, 1961), gilboa1989maxmin (J Math Econ 18, 2, 1989) match the curriculum "
    f"strings. {GATE_NOTE}verify_refs_E3_live_r5.out: 5 of 560 entries re-verified, 0 problems. The page quotes no title.")

row("E3e-17", "2.4 definitions and results cited from the project page exist where cited",
    "project.html:53 and :210 (lesson citations)",
    "PASS",
    "L06.html:61 Definition 1.2 (value function), :68 Definition 1.3 (prospect value); L02.html:99 Definition 1.2 "
    "(certainty equivalent, def-certainty-equivalent); L03.html:87 Definition 1.3 and :173 Proposition 2.7 (affine invariance).")

row("E3e-18", "2.5 Lab 1 prose vs code and output (CRRA utility, two lines per pair, total, pair 2 claims)",
    "project.html:53, :57, :58-137 (lab), :138 (interpretation); tests/labs/E3/lab-E3-project-1.py",
    "PASS",
    "Page code identical to the twin (page_code_vs_twin_r5.out). Printed output re-derived in labs_recompute_r5.out. Interpretation "
    "claims checked: the CRRA values are changes from wealth 100000 cents; prospect values use lambda on losses; pair 2 has a "
    "sure 3000 cents (both models) against a lottery at -762 cents (prospect). Docstrings of crra_certainty_equivalent and "
    "prospect_certainty_equivalent state cents. The per-step why requirement is a separate row (E3e5-01).")

row("E3e-19", "2.5 Lab 1 hypothesis numbers vs expected block",
    "project.html:57 (hypothesis), :131-137 (expected block)",
    "PASS",
    "Hypothesis numbers 496, 500, -30, 500, 0.480149, -0.733658, -2.302315 equal the expected block and labs_recompute_r5.out.")

row("E3e-20", "2.5 Lab 2 (completion) hypothesis numbers and the completed formulas",
    "project.html:141-188; tests/labs/E3/lab-E3-project-2.py",
    "PASS",
    "Hypothesis numbers -0.765595182, -0.625595182 and the probabilities sum to 1 equal labs_recompute_r5.out. Every page line equals "
    "the twin line or contains a blank (page_code_vs_twin_r5.out: none unmatched). Expected block (:183-186) equals the run "
    "(run_labs_project.out: PASS 3/3).")

row("E3e-21", "2.5 Lab 3 (reference case) and its prose: estimates, standard errors, score, log-likelihood, interpretation",
    "project.html:381-386 (hypothesis), :571-578 (expected block and interpretation); :570 second_order_search",
    "PASS",
    "Estimates 0.6352, 6.1503, 2.0201, log-likelihood -7.1445 and eleven mixed pairs reproduced by labs_recompute_r5.out; SEs 0.32, "
    "9.59, 1.86 reproduced by lab3_se_r5.out (steps 1e-4 and 1e-5). Interpretation: the search is a second-derivative search at "
    "step 1e-6 (twin :458), the score is in the three coordinates (twin :548-556), and the lab does not check a maximum (true).")

row("E3e-22", "2.5 lab and code gates for the project labs and grader: twins alone, page equals twin, expected equals output, ruff, mypy",
    "tests/labs/E3/lab-E3-project-1.py, -2.py, -3.py; course/modules/E/E3/grader/",
    "PASS",
    "run_labs E3 --page project: PASS (3/3) (run_labs_project.out). page_code_vs_twin_r5.out: lab 1 and lab 3 identical to the twin, lab 2 "
    "blanks only. ruff check tests/labs/E3 and grader: All checks passed (ruff_check_r5.out); ruff format --check: 15 files formatted "
    "(ruff_format_r5.out). Repository mypy (tools, tests): Success, 331 source files (mypy_repo_r5.out). The strict check of the grader "
    "test file is a separate row (E3e5-02).")

row("E3e-23", "2.4 mathematics on the page: conventions, identification argument, standard-error convention (delta method)",
    "project.html:203 (grading), :209-214 (conventions and estimation)",
    "PASS",
    "Identification: CE of an all-gain or all-loss lottery does not depend on lambda (v divides out), checked algebraically. "
    "SE convention: inverse observed information in (zeta, log lambda, log kappa), with d gamma/d zeta = gamma(1-gamma) as in "
    "test_project.py:876-900 and lab3_se_r5.py. Delta-method statement at :214 is the standard first-order approximation.")

row("E3e-24", "2.4 notation: every symbol and macro on the slice against notation/notation.json; one symbol, one meaning across the unit",
    "course/modules/E/E3/project.html (128 math spans); notation/notation.json",
    "PASS",
    f"{GATE_NOTE}macros_r5.out: the page uses no registered macro; control sequences are Greek letters, \\mathrm, \\texttt, \\ln, \\log, "
    "\\hat. Phi (line 739) has the registered meaning (standard normal distribution function). No gamma subscript, no T, R or Q "
    "symbol. The local letters are defined where used.")

row("E3e-25", "2.9 DAG in prose: concepts used outside the prerequisite closure, by name and unlinked",
    "course/modules/E/E3/project.html (visible text and meta description)",
    "PASS",
    "grep -c on project.html: maximum likelihood, Fisher, confidence interval, convex, concave, Bellman, estimator, risk-neutral, "
    "martingale all 0 except 'maximum-likelihood' in the meta description (line 7), which the architect decisions allow as plain prose. "
    "check_dag E3: PASS (check_dag_E3.out).")

row("E3e-26", "2.9 terms used before definition on the project page",
    "course/modules/E/E3/project.html:53 (forward pointer), :212 (Choice probability), :210 (prospect model)",
    "PASS",
    "'logit rule' at line 53 points forward to the Conventions subsection, which defines it at line 212. Certainty equivalent and "
    "prospect value are linked to Lessons 2 and 6 at line 53.")

row("E3e-27", "2.4 scope words (only, all, always, every, any, same, drives, exactly) carry a computation or a stated hypothesis",
    "course/modules/E/E3/project.html:203 (exactly, every), :213 (only when, all gains, or all losses), :215 (exactly one)",
    "PASS",
    "'only when' at :213 is a necessity claim, and its basis is the lambda-free certainty equivalent argument (verified in E3e-23). "
    "'exactly' at :203 and :215 refers to the exact Fraction sum check in test_project.py.")

row("E3e-28", "2.6 autograder claims stated on the page (tolerances and what the oracle compares exactly)",
    "course/modules/E/E3/project.html:203; grader/test_project.py:158, :176, :196, :208, :219, :224-234, :409, :431, :435, :487, "
    ":548, :564, :577, :900, :959-961",
    "PASS",
    "Round 4 failure cured: the page lists the half-cent allowances that the suite uses. Read against the suite: exact integer equality "
    "to floor(x+1/2) at :158 and :219; ONE_CENT+TOL (half cent plus 1e-6) at :176 (log limit), :196 (CRRA risky lottery) and :208 "
    "(homogeneity); half-cent bound at :231-234 (prospect sure amount); DOMINANCE_SLACK = 1 cent at :959; log-likelihood tolerance "
    "1e-9 times max(1,|v|) at :409, :431, :435 and 1e-9 times |v| at :487 (|v| = 1850 there, so the same); score below 2e-5 at "
    "min over steps (:548); local maximum 1e-9 at :564; 4 SE on 47 of 50 seeds (:577); SE within 10 percent at either step (:900). "
    "45 checks (collect_only_r5.txt).")

row("E3e-29", "2.6 reference passes the suite on seeds 0-49 (local pytest, same flags as the browser)",
    "course/modules/E/E3/grader/reference.py; tools/run_graders.py --unit E3 --seeds 0-49",
    "PASS",
    "run_graders E3 --seeds 0-49: PASS (reference 50/50 seeds, slowest 14.3 s) (run_graders_0-49.out).")

row("E3e-30", "2.6 mutation: re-run all existing mutants; every mutant killed",
    "ledgers/E3/mutants/ (92 pre-existing mutants); tools/mutate_graders.py --unit E3 --seeds 0-9",
    "PASS",
    "mutate_graders E3 --seeds 0-9: PASS (92/92 killed) (mutate_graders_E3_seeds0-9_r5.out). Each killed-by test is listed in the "
    "fragment's mutants.")

row("E3e-31", "2.6 at least three NEW student-error mutants written by the verifier, each killed",
    "ledgers/E3/mutants/g5_01_wealth_check_message_omits_the_quoted_text.py; g5_02_mixed_check_counts_a_zero_prize_as_a_gain.py; "
    "g5_03_crra_change_uses_one_over_gamma_exponent.py; grader/test_project.py (no test with a zero prize)",
    "FAIL",
    "kill_new_mutants_r5.out: g5_01 KILLED by test_crra_requires_wealth_plus_every_prize_to_stay_positive (seed 0); g5_03 KILLED by "
    "test_crra_within_half_cent_of_oracle_for_instance_lotteries (seed 0); g5_02 SURVIVED all seeds 0-9. g5_02 changes a stated "
    "behaviour: project.html:197 and the exception table at :227 require a prize above zero and a prize below zero, each with "
    "positive probability. No existing test has a zero prize with a loss. The candidate test in "
    f"{GATE_NOTE}candidate_zero_prize_test_r5.py passes on reference.py and fails on g5_02 (scratch copy, QF_SEED=0).",
    "Append the test in ledgers/E3/scripts/E3-e-r5/candidate_zero_prize_test_r5.py to course/modules/E/E3/grader/test_project.py "
    "(it uses only must_raise and sol.estimate), then re-run run_graders E3 --seeds 0-49 and mutate_graders E3 --seeds 0-9.")

row("E3e-32", "2.6 five alternative correct implementations pass (over-constraint check)",
    "ledgers/E3/scripts/run_alternatives.py (alt1-alt5)",
    "PASS",
    "run_alternatives.py --seeds 0-9: alt1 10/10, alt2 10/10, alt3 10/10, alt4 10/10, alt5 10/10 PASS "
    "(run_alternatives_seeds0-9_r5.out). Seeds 0-9 per architect ruling 10.")

row("E3e-33", "2.6 test count on the page equals the real collect-only count",
    "course/modules/E/E3/project.html:203 ('runs 45 checks'); grader/test_project.py",
    "PASS",
    "pytest --collect-only on a scratch copy with reference.py as elicit.py: 45 tests collected (collect_only_r5.txt).")

row("E3e-34", "2.6 exception table: named conditions, exception types and message text",
    "course/modules/E/E3/project.html:224-228 (table); grader/reference.py:30, :60, :121, :288, :291; test_project.py:359-381",
    "PASS",
    "reference.py raises ValueError with 'model must be \"crra\" or \"prospect\"' (names both), 'probabilities must sum to 1 (and be "
    "non-negative)' (contains the quoted text), 'wealth plus prize must stay positive' (quoted text), and the estimate conditions "
    "(:288, :291). must_raise checks the quoted text at test_project.py:367, :372, :379.")

row("E3e-35", "2.8 figures on the page (axes, source, caption, SVG title and desc) and figure data",
    "course/modules/E/E3/project.html (no svg, figure or chart element)",
    "PASS",
    "grep -c for '<svg', '<figure' and class=\"chart\" on project.html: 0.")

row("E3e-36", "2.1 registry integrity for the five E3 keys (live)",
    "references/references.json (five E3 keys); tools/verify_refs.py --unit E3",
    "PASS",
    f"verify_refs.py --unit E3 (live): '5 of 560 entries, 0 problems' ({GATE_NOTE}verify_refs_E3_live_r5.out). references.json is "
    "byte-identical to 4eb6788f (git diff --quiet).")

row("E3e-37", "2.9 interactive questionnaire and privacy claims (nothing leaves the browser; export only when every pair has a choice)",
    "course/modules/E/E3/project.html:235, :239-343, :765; course/assets/js/grader.js:18, :33-61; course/assets/js/rubric.js:87",
    "PASS",
    "Read the inline script: no fetch, XHR or beacon. The export button is disabled until a file loads (:271, :308), and export "
    "refuses while any pair lacks a choice (:318-331). grader.js fetches only its own suite files (:18) and stores drafts in "
    "IndexedDB via store.js (:61). Footer claim (:767) matches.")

row("E3e-38", "2.6 rung 4 is genuinely open-ended and not graded",
    "course/modules/E/E3/project.html:736-741 (stretch section)",
    "PASS",
    "Two open-ended extensions (probit link with a stated comparison; probability weighting with an identification argument). "
    "Not tied to the grader or the rubric.")

row("E3e-39", "2.6 suite gap: named probability condition for log_likelihood (sum-to-one checks)",
    "grader/test_project.py:440-476",
    "PASS",
    "Tests refuse a sum below one, a sum above one and a negative probability in log_likelihood, each with 'probabilities must sum to 1' "
    "(contains=). Read in full this round.")

row("E3e-40", "2.2 numbers quoted in grader docstrings (standard-error comparison at steps 1e-5 and 1e-6)",
    "grader/test_project.py:876-888 (docstring)",
    "PASS",
    f"{GATE_NOTE}seed49_se_r5.out (QF_SEED=49, suite's own oracle): se_lambda 135.05 (1e-5) and 97.67 (1e-6); se_gamma 0.09474 and "
    f"0.07983. {GATE_NOTE}seed49_reverse_r5.out: reverse summation order gives 136.78 and 98.09. Percentages recomputed: "
    "-27.7, -15.7, +1.3, +0.4.")

row("E3e-41", "2.6 equivalent-mutant README and any cited ruling for a survivor",
    "ledgers/E3/equivalent/ (absent); plans/FINAL-ARCHITECT-RULINGS.md item 9",
    "PASS",
    "No equivalent mutants are claimed. g5_02 is not equivalent (it changes a stated behaviour) and is a FAIL in E3e-31, not moved to "
    "equivalent/. The 92 pre-existing mutants are all killed.")

row("E3e-42", "2.4 rename consistency (eta to zeta; kappa; lambda; gamma) across page, grader and labs",
    "course/modules/E/E3/project.html (zeta, kappa, lambda, gamma at :203, :214, :578); grader/*.py; tests/labs/E3/lab-E3-project-*.py",
    "PASS",
    "zeta, kappa, lambda and gamma appear with the same meaning in the page, test_project.py, reference.py and the twins; no 'eta' in the "
    "grader (grep).")

row("E3e-43", "2.8 instance docstrings vs code (grader/instance.py)",
    "course/modules/E/E3/grader/instance.py",
    "PASS",
    CARRY + "round-4 row E3e-43 PASS (docstring at instance.py:1 'All values are SIMULATED'; code matches docstring). SIMULATED label "
    "and parameter ranges unchanged in this checkout.")

row("E3e-44", "2.6 dominance witnesses and verdict oracle",
    "grader/test_project.py:958-1043",
    "PASS",
    "Read in full this round. FOSD witness (A = B with each prize raised by 100 cents) and SOSD witness (sure 0 against a fair "
    "+-1000 gamble) are dominated as stated; verdicts compared with expected-utility rankings over step and ramp utilities; "
    "DOMINANCE_SLACK = 1 cent (:959).")

row("E3e-45", "2.6 failure messages name the violated property and never leak the answer",
    "grader/test_project.py:44-59 (expect, must_raise) and every expect() call",
    "PASS",
    "expect() messages are static strings naming the property; must_raise formats only the static condition text; no message "
    "prints a computed value.")

row("E3e-46", "2.6 the same suite passes in Pyodide (browser) and in local pytest",
    "tools/page_smoke.py --unit E3 --pages project; grader/test_project.py",
    "PASS",
    f"page_smoke E3 --pages project: PASS; in-browser grader 'All 45 tests pass on seed 116077631 (27.6 s)' ({GATE_NOTE}"
    "page_smoke_project_r5.out). Local: 45 collected (E3e-33) and reference 50/50 (E3e-29).")

row("E3e-47", "2.6 hours: verifier's own estimate of each deliverable component vs the declared 14 hours (30 percent band)",
    "course/modules/E/E3/project.html:352-358 (budget table)",
    "PASS",
    "Verifier's judgement, not a measurement: rung 1 about 1 h, rung 2 about 1 h, instrument and questionnaire about 3 h, elicit.py "
    "to the interface and a local pass about 5 h, report about 3 h, self-assessment about 2 h = 15 h, 7 percent above 14 h, inside the "
    "30 percent band.")

row("E3e-48", "2.8 SIMULATED labels where generated data is used; no real data without a licence",
    "project.html:53, :57, :366, :379, :383-386, :718; grader/instance.py:1",
    "PASS",
    "Lab 1 hypothesis (:57) and Lab 3 hypothesis (:383) and the twin docstring (:384) say SIMULATED; exemplar B evidence (:718) says "
    "'Lab 3 (SIMULATED)'; instance.py:1 says all values are SIMULATED. No dataset in MANIFEST concerns preferences (plan section 9).")

row("E3e-49", "2.9 page_smoke: console errors, unrendered math, external requests, 360 px",
    "course/modules/E/E3/project.html",
    "PASS",
    f"page_smoke E3 --pages project: PASS (page_smoke_project_r5.out). The tool's checks cover console errors, math, external requests and 360 px.")

row("E3e-50", "2.6 over-constraint: a correct implementation that the standard-error oracle or the suite wrongly rejects",
    "grader/test_project.py:873-909 (standard-error oracle at two steps); ledgers/E3/scripts/run_alternatives.py",
    "PASS",
    "Five correct alternatives (compass and Newton; Newton on analytic-style differences; Nelder-Mead and Newton; bisection inversion; "
    "Decimal half-up) pass 10/10 seeds each (run_alternatives_seeds0-9_r5.out); the SE oracle accepts either step.")

row("E3e4-gates", "Repository gates for the E3 project slice, run by the verifier on pin 440ed3c8",
    "tools/check_pages.py, check_dag.py, check_projects.py, run_labs.py, run_graders.py, page_smoke.py, verify_refs.py, ruff, mypy",
    "PASS",
    "check_pages E3 PASS; check_dag E3 PASS; check_projects E3 PASS; run_labs E3 project PASS (3/3); run_graders E3 0-49 PASS (50/50); "
    "page_smoke E3 project PASS; verify_refs E3 live PASS (5 of 560); ruff check and format PASS; repository mypy PASS (331 files). "
    "Outputs in ledgers/E3/scripts/E3-e-r5/.")

row("E3e4-exemplar-B-level", "Exemplar levels match the binding plan (exemplar-a level 2, exemplar-b level 4)",
    "course/modules/E/E3/project.html:665 (data-level=\"3\"); plans/E3-build-plan.md:392 (data-level \"4\")",
    "FAIL",
    "Still data-level=\"3\" at project.html:665, with data-scores 3,3,4,3,3. plans/E3-build-plan.md:392 requires exemplar-b data-level=\"4\". "
    "No ruling in plans/FINAL-ARCHITECT-RULINGS.md or plans/E3-open-items.md covers the level; the batch 3 ruling covers excerpts only.",
    "Architect rules that exemplar B is level 3 and amends plans/E3-build-plan.md:392, or the builder rewrites exemplar B to meet level 4 "
    "on every criterion (C1 all twelve pairs; C2 precision identification as a result; C4 a direction of bias; C3 and C5 as now), "
    "sets data-level=\"4\" and data-scores=\"4,4,4,4,4\", and re-annotates.")

row("E3e4-C2-observability", "Rubric level descriptors are observable (VERIFIER 2.6 rubric 1): C2 'states the value function'",
    "course/modules/E/E3/project.html:592 (scoring rule), :601 (C2 row), :630-634 (exemplar A)",
    "PASS",
    "Round 4 failure cured. :592 now states that the value function is shown when its formulas for gains and losses are given, and the "
    "logit rule when its choice-probability formula is given. Exemplar A (:630) gives both formulas and :634 cites that element.")

row("E3e4-lab3-rederive", "Lab 3 numbers re-derived independently (not from the twin)",
    "project.html:381-386, :571-578; ledgers/E3/scripts/E3-e-r5/labs_recompute_r5.py, lab3_se_r5.py",
    "PASS",
    "Own grid and coordinate search (labs_recompute_r5.out) and own Newton with central differences (lab3_se_r5.out) reproduce the printed "
    "estimates, log-likelihood -7.1445, SEs and score size.")

row("E3e4-prizes-mixed", "Exemplar B instrument facts: prize range, prizes per lottery, probabilities sum to 1, pair examples, mixed count",
    "project.html:671 (exemplar B instrument); project.html:382-398 (answers block)",
    "PASS",
    f"{GATE_NOTE}instrument_facts_r5.out: prize range -18700 to 19000; two or three prizes per lottery; probabilities of every lottery "
    "sum to exactly 1; pair 0 and pair 3 values as printed; 11 of 12 pairs mixed; both lotteries of pair 3 mix.")

row("E3e4-identification", "Identification claims on the page (lambda identified only from mixed lotteries; the precision claim is labelled a hypothesis)",
    "project.html:213 (Identification); project.html:683 and :688 (exemplar B model and C2 annotation)",
    "PASS",
    "The lambda-free certainty equivalent of all-gain or all-loss lotteries is verified algebraically; exemplar B labels the precision "
    "identification as a hypothesis ('I expect, without computing it here').")

row("E3e4-cross-refs", "Cross-references to lessons on the project page (Lesson 3 Proposition 2.7; Lesson 6 Definitions 1.2 and 1.3; Lesson 2 and 3 concept anchors)",
    "project.html:53, :210; course/modules/E/E3/L03.html:173; L06.html:61, :68; L02.html:99",
    "PASS",
    "Each target exists and says what the page says (Proposition 2.7: affine transformations leave certainty equivalents unchanged; "
    "Definition 1.2: value function; Definition 1.3: prospect value). links_r5.out resolves the anchors.")

row("E3e4-attribution-titles", "Attribution of the lessons' statements about the reading-list papers (title-only claims)",
    "course/modules/E/E3/L07.html:80; L08.html:67; L08.html:133; references/references.json",
    "PASS",
    "Each claim is grade C with data-locator 'registry record: title only; paper not read' and states only the registry title. Titles match "
    "references.json (E3e-16). Re-read this round because L07 and L08 changed.")

row("E3e4-stretch-phi", "Stretch probit link: definition of Phi against the registry",
    "project.html:739; notation/notation.json (symbol \\Phi, \\Phi^{-1}: standard normal CDF and quantile)",
    "PASS",
    "Phi is the standard normal distribution function, matching the registry meaning (macros_r5.out).")

row("E3e4-ruling-392", "The binding plan's exemplar wording agrees with the architect ruling on excerpts (round-12 FAIL resolved)",
    "plans/E3-build-plan.md:392; plans/E3-open-items.md:145-149",
    "PASS",
    "Plan 392 says 'excerpts of memos, not full reports'; the batch 3 ruling says the same. The ruling's word counts (103 and 375) are "
    "stale; see E3e-13.")

row("E3e5-01", "2.9 rung 1 worked example annotated with why at every step (BUILDER_RULES 5.1; plan 6.1 item 1 'each step has a why note')",
    "tests/labs/E3/lab-E3-project-1.py:58-130 (main and its steps); course/modules/E/E3/project.html:55-57, :138",
    "FAIL",
    "The main() loop (twin lines 108-127; page :58-130) has no comment on any step. The reasons exist only in helper docstrings "
    "(crra_certainty_equivalent, prospect_certainty_equivalent) and in the interpretation paragraph (:138), which describes the printed "
    "numbers rather than why each step is computed. Checked by reading the twin and page_code_vs_twin_r5.out.",
    "Add a why comment before each step in the twin's main() (CRRA certainty equivalent, prospect certainty equivalent, the logit "
    "probability, the log of the chosen probability), then run tools/embed_labs.py course/modules/E/E3/project.html --refresh "
    "lab-E3-project-1 and confirm the expected block is unchanged with tools/run_labs.py --unit E3 --page project.")

row("E3e5-02", "2.6 grader test file is type-clean under mypy --strict (BUILDER_RULES 6.1 and 6.2: code is type-checked by mypy strict; type hints)",
    "course/modules/E/E3/grader/test_project.py:388-390",
    "FAIL",
    f"{GATE_NOTE}mypy_strict_grader_test_r5.out: four mypy --strict errors (list-item x3, arg-type x1) on the deliberate wrong-type calls. "
    "Not caught by any gate: the repository mypy covers tools and tests only, and run_graders typechecks reference.py, instance.py and "
    "starter.py only. Line 295 of the same file already uses a type-ignore for an equivalent case.",
    "Mark the deliberate wrong-type arguments on lines 388-390 with '# type: ignore[list-item]' and '# type: ignore[arg-type]', as "
    "line 295 does, without changing what the test asserts.")

row("E3e5-03", "2.5 lab-E3-project-3 'calls the engine on the reference case' (plan 6.1 item 3, binding)",
    "tests/labs/E3/lab-E3-project-3.py; course/modules/E/E3/project.html:381-383; plans/E3-open-items.md section 3 item 2",
    "FAIL",
    "The binding plan says lab-E3-project-3 calls the engine on the reference case. The twin does not import elicit.py; the page tells the "
    "learner to replace second_order_search with a call to their own estimate. The open-items file records this as a deviation (section 3 "
    "item 2) and asks for no ruling, and no architect ruling covers it.",
    "Architect records a ruling accepting the twin-plus-copy design and amends plan 6.1 item 3, or directs a different rung-3 check. "
    "This is an architect decision; the builder cannot resolve it alone.")

row("E3e5-04", "2.4 definitions: the prospect model extends Lesson 6 Definition 1.3 (p_i > 0) to zero-probability prizes",
    "course/modules/E/E3/project.html:210, :215; course/modules/E/E3/L06.html:69",
    "PASS",
    "A zero-probability term contributes p_i v(x_i) = 0, so W is unchanged; the extension is an identity, not a change of definition. "
    "Stated on the page at :215.")

row("E3e5-05", "2.9 hub ladder text agrees with the spec (round 5 change to index.html:146)",
    "course/modules/E/E3/index.html:146; course/modules/E/E3/project.html:197",
    "PASS",
    "Hub says at least 12 pairs with at least one mixed-sign lottery; spec at :197 says the same; the hub's 'Graded by the autograder and "
    "the rubric' matches :203.")

mutant_fail = [m for m in mutants if not m.get("killed_by")]
row_fail = [r for r in rows if r["status"] != "PASS"]
summary = {
    "rows": len(rows),
    "pass": sum(1 for r in rows if r["status"] == "PASS"),
    "fail": sum(1 for r in rows if r["status"] == "FAIL"),
    "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
    "mutants": len(mutants),
    "mutants_killed": sum(1 for m in mutants if m.get("killed_by")),
}
verdict = "PASS" if summary["fail"] == 0 and summary["unverifiable"] == 0 and not mutant_fail else "FAIL"

fragment = {
    "unit": "E3",
    "slice": "e",
    "round": 5,
    "verifier": "Claude Haiku 5.5, independent verifier for E3-e, round 5 (did not build E3; fresh checkout pinned at 440ed3c8; read "
                "VERIFIER_RULES, the verifier rules file, BUILDER_RULES, plans/E3-build-plan.md with its architect decisions, "
                "plans/E3-open-items.md and plans/FINAL-ARCHITECT-RULINGS.md)",
    "pin": "440ed3c8",
    "base": "4eb6788f (round-4 pin; round-4 fragment /Users/billyribeiro/.fanout/frags/D-E3-e.round4.json). Delta 4eb6788f..440ed3c8 "
            "read for project.html (every hunk), grader/test_project.py (every hunk), index.html, and the lesson hunks that carry "
            "reading-list and attribution claims (L07, L08, L05, L02). grader/instance.py, grader/reference.py, grader/starter.py, "
            "tests/labs/E3 and references/references.json are byte-identical to 4eb6788f.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD5-E3-e",
    "scratch": "/tmp/e3e_r5/",
    "verified_at": "2026-11-03",
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Round-5 changes read and re-checked: project.html grading and scoring text, exemplar counts and exemplar B (scores and "
        "C5 annotation), reading section, C2 scoring rule; grader/test_project.py tolerance lines (433-435) and second-participant "
        "test (585-609).",
        "Cards are not in this slice and were not checked.",
        "Mutants: all 92 pre-existing mutants re-run on seeds 0-9 (92/92 killed). Three new student-error mutants written by this "
        "verifier (g5_01 killed, g5_03 killed, g5_02 survived). Alternatives alt1-alt5 run on seeds 0-9 (10/10 each).",
        "Candidate zero-prize test in ledgers/E3/scripts/E3-e-r5/candidate_zero_prize_test_r5.py was run only in a scratch copy; "
        "course files were not edited.",
        "Stale numbers: plans/E3-open-items.md:147 quotes 103 and 375 words; the page's correct count for B is 582 (E3e-13).",
        "Pyodide was checked by page_smoke with one browser seed (116077631); seeds 0-49 were run locally only.",
        "Full repository gates (check_pages --all, check_dag --all, check_projects --all, build_site --check, render_curriculum, "
        "fetch_data --check, verify_refs full run) are outside slice e and were not run.",
    ],
    "summary": summary,
}

out = ROOT / "ledgers/E3/E3-e.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, "rows", summary["rows"], "fail", summary["fail"], "mutants", summary["mutants"], "killed", summary["mutants_killed"], "verdict", verdict)
