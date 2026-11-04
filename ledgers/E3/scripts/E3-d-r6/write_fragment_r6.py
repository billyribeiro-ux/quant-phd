"""Build ledgers/E3/E3-d.json (round 6) from the evidence files in this folder. Run from the checkout root.

Statuses come from the files named in each evidence string; nothing is asserted without a file behind it.
"""
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

root = Path.cwd()
S = root / "ledgers/E3/scripts/E3-d-r6"


def read(name):
    return (S / name).read_text(encoding="utf-8")


def alt_line(text, name):
    m = re.search(rf"^{name}: (PASS|FAIL) \((\d+)/(\d+) seeds[^)]*\)", text, re.M)
    return m


alt_a = read("alternatives_0_9_r6.out")
alt4_lo = read("alt4_seeds_0_4_r6.out")
alt4_hi = read("alt4_seeds_5_9_r6.out")
alt5 = read("alt5_seeds_0_9_r6.out")
alt_rows = []
for name in ("alt1", "alt2", "alt3"):
    m = alt_line(alt_a, name)
    alt_rows.append((name, m.group(0) if m else None, "PASS" if m and m.group(1) == "PASS" and m.group(2) == m.group(3) == "10" else "FAIL"))
ma = alt_line(alt4_lo, "alt4")
mb = alt_line(alt4_hi, "alt4")
alt4_ok = bool(ma and mb and ma.group(1) == "PASS" and mb.group(1) == "PASS" and ma.group(2) == "5" and mb.group(2) == "5")
alt4_text = f"seeds 0-4: {ma.group(0) if ma else 'no summary'}; seeds 5-9: {mb.group(0) if mb else 'no summary'}"
m5 = alt_line(alt5, "alt5")
alt5_ok = bool(m5 and m5.group(1) == "PASS" and m5.group(2) == m5.group(3) == "10")

mut_lines = read("mutate_E3_0_9_r6.out").splitlines()
new_lines = read("new_mutants_r6.out").splitlines()
mutants = []
for line in mut_lines + new_lines:
    m = re.match(r"^(KILLED|SURVIVED) (\S+?)\.py: (.*?) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    entry = {"id": name, "description": desc}
    if status == "KILLED":
        entry["killed_by"] = killed
    mutants.append(entry)

rows = []


def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


row("gate-check-pages", "tools/check_pages.py --all", "course/modules/E/E3/project.html", "PASS",
    "ledgers/E3/scripts/E3-d-r6/check_pages.out: 'check_pages E3: PASS', rc=0")
row("gate-check-dag", "tools/check_dag.py --all", "course/modules/E/E3/project.html", "PASS",
    "ledgers/E3/scripts/E3-d-r6/check_dag.out: 'check_dag E3: PASS', rc=0")
row("gate-check-projects", "tools/check_projects.py --all", "course/modules/E/E3/project.html", "PASS",
    "ledgers/E3/scripts/E3-d-r6/check_projects.out: 'check_projects E3: PASS', rc=0")
row("gate-run-labs-project", "tools/run_labs.py --unit E3 --page project", "project.html Labs 1-3", "PASS",
    "ledgers/E3/scripts/E3-d-r6/run_labs_project.out: 'run_labs E3: PASS (3/3)', rc=0")
row("gate-run-graders-seeds-0-49", "tools/run_graders.py --unit E3 --seeds 0-49", "course/modules/E/E3/grader/", "PASS",
    "ledgers/E3/scripts/E3-d-r6/run_graders_0_49.out: 'run_graders E3: PASS (reference 50/50 seeds, slowest 14.3 s)', rc=0")
row("gate-collect-45", "pytest --collect-only in a grader workspace (reference as elicit.py)",
    "course/modules/E/E3/grader/test_project.py; project.html:213", "PASS",
    "ledgers/E3/scripts/E3-d-r6/collect_only_r6.out: '45 tests collected'; grep -c '^def test_' = 45; project.html:213 says 45")
row("gate-page-smoke-project", "tools/page_smoke.py --unit E3 --pages project", "course/modules/E/E3/project.html", "PASS",
    "ledgers/E3/scripts/E3-d-r6/page_smoke_project.out: 'in-browser grader: All 45 tests pass on seed 548330789', 'page_smoke E3: PASS', rc=0")
row("gate-ruff-check-repo", "ruff check . (repo, pyproject extend-exclude applies)", "repo", "PASS",
    "ledgers/E3/scripts/E3-d-r6/ruff_check_repo_r6.out: 'All checks passed!', rc=0")
row("gate-ruff-format-E3", "ruff format --check course/modules/E/E3/grader tests/labs/E3", "course/modules/E/E3/grader; tests/labs/E3", "PASS",
    "ledgers/E3/scripts/E3-d-r6/ruff_format.out: '15 files already formatted', rc=0")
row("gate-ruff-format-repo", "ruff format --check . (repo)", "ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py:3", "FAIL",
    "ledgers/E3/scripts/E3-d-r6/ruff_format_repo_r6.out: '1 file would be reformatted, 479 files already formatted', rc=1. The file is outside E3-d and unchanged in this round.",
    "Outside this slice (M3 owner): run .venv/bin/ruff format ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py, then re-run ruff format --check .")
row("gate-mypy-strict", "mypy --no-incremental (repo, strict config)", "repo", "PASS",
    "ledgers/E3/scripts/E3-d-r6/mypy.out: 'Success: no issues found in 331 source files', rc=0")
row("gate-verify-refs-offline", "tools/verify_refs.py --offline", "references/references.json", "PASS",
    "ledgers/E3/scripts/E3-d-r6/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', rc=0")
row("gate-pytest-docs-labs", "pytest tests/test_docs_figures.py tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_memo_exemplars.py", "tests/", "PASS",
    "ledgers/E3/scripts/E3-d-r6/check_docs_figures.out: dots to 100%, rc=0")
row("gate-mutate-E3-existing-99", "tools/mutate_graders.py --unit E3 --seeds 0-9 (all 99 mutants present at the pin)", "ledgers/E3/mutants/", "PASS",
    "ledgers/E3/scripts/E3-d-r6/mutate_E3_0_9_r6.out: 'mutate_graders E3: PASS (99/99 killed)', EXIT 0")
row("mut-e3d5-01-zero-prize-mixed-test-fixed", "round-5 FAIL re-verified: zero prize counted as a gain is killed", "ledgers/E3/mutants/e3d5_01_zero_prize_counts_as_a_gain_in_the_mixed_test.py; grader/test_project.py:635-705", "PASS",
    "mutate_E3_0_9_r6.out: 'KILLED e3d5_01 ... -> test_estimate_needs_a_mixed_sign_lottery (seed 0)'")
row("gate-mutants-count-fixed", "round-5 FAIL re-verified: every mutant at the pin killed", "ledgers/E3/mutants/", "PASS",
    "mutate_E3_0_9_r6.out: 99/99 killed (round 5 had 95/96)")
row("mut-e3d6-01-zero-prize-counts-as-loss", "new student-error mutant: zero prize counted as a loss in the mixed-sign test",
    "grader/test_project.py:635-705 (test_estimate_needs_a_mixed_sign_lottery); ledgers/E3/mutants/e3d6_01_zero_prize_counts_as_a_loss_in_the_mixed_test.py", "FAIL",
    "ledgers/E3/scripts/E3-d-r6/new_mutants_r6.out: 'SURVIVED e3d6_01 ... -> None' on seeds 0-9. Witness W1 (witness_zero_loss_r6.py): response 0 A=[300,0] probs [1/2,1/2], B=[200] prob 1; response 1 pure gains. Reference: ValueError 'need mixed-sign lotteries' (the required refusal). Mutant: no ValueError (it goes on to the optimiser). project.html:207 states the mixed condition as 'a prize above zero and a prize below zero, each with positive probability'; project.html:237 names the ValueError when no response has such a lottery.",
    "Add to test_estimate_needs_a_mixed_sign_lottery a must_raise(ValueError) on witness W1 (response 0 with prizes_a [300, 0] and probs ['1/2','1/2'], prizes_b [200] with probs ['1']; response 1 pure gains). Verify the reference refuses it and mutant e3d6_01 is KILLED on seed 0.")
row("mut-e3d6-02-mixed-check-reads-chosen-lottery-only", "new student-error mutant: mixed-sign condition reads only the chosen lottery",
    "grader/test_project.py (test_estimate_accepts_a_mixed_lottery_on_the_b_side_alone and the mixed-sign tests); ledgers/E3/mutants/e3d6_02_mixed_check_reads_only_the_chosen_lottery.py", "FAIL",
    "ledgers/E3/scripts/E3-d-r6/new_mutants_r6.out: 'SURVIVED e3d6_02 ... -> None' on seeds 0-9. Witness (witness_unchosen_r6.py): the grader's B-side data with every choice set to 'A', so every mixed lottery is unchosen. Reference: accepts and returns estimates (gamma_hat 0.0319, lambda_hat 48.1447). Mutant: ValueError 'need mixed-sign lotteries'. project.html:207 ('at least one pair in the instrument has a lottery that mixes a gain and a loss') and project.html:237 ('no response has a lottery that mixes') apply to any lottery, chosen or not.",
    "Add a test: 12 responses, every choice 'A', A lotteries pure, B lotteries as in B_SIDE_LOTTERIES; the estimate must return the seven named finite fields and must not raise ValueError. Verify the reference passes and mutant e3d6_02 is KILLED.")
row("mut-e3d6-03-loss-inverse-divides-after-power", "new student-error mutant: loss inverse divides by lambda after the power",
    "grader/test_project.py:854-861", "PASS",
    "ledgers/E3/scripts/E3-d-r6/new_mutants_r6.out: 'KILLED e3d6_03 ... -> test_prospect_matches_oracle_for_instance_lotteries (seed 0)'")
for name, line, ok in alt_rows:
    row(f"alt-{name[-1]}", f"alternative correct implementation {name} (ledgers/E3/scripts/run_alternatives.py)",
        "ledgers/E3/scripts/run_alternatives.py", "PASS" if ok == "PASS" else "FAIL",
        f"ledgers/E3/scripts/E3-d-r6/alternatives_0_9_r6.out: '{line}'",
        None if ok == "PASS" else "Over-constraint: see the failing seed output in the alternatives file")
row("alt-4", "alternative correct implementation alt4 (bisection inversion), seeds 0-9 split into two processes",
    "ledgers/E3/scripts/run_alternatives.py", "PASS" if alt4_ok else "FAIL",
    f"ledgers/E3/scripts/E3-d-r6/alt4_seeds_0_4_r6.out and alt4_seeds_5_9_r6.out: {alt4_text}",
    None if alt4_ok else "Over-constraint or incomplete run: see alt4 output files")
row("alt-5", "alternative correct implementation alt5 (Decimal half-cent rule), seeds 0-9",
    "ledgers/E3/scripts/run_alternatives.py", "PASS" if alt5_ok else "FAIL",
    f"ledgers/E3/scripts/E3-d-r6/alt5_seeds_0_9_r6.out: '{m5.group(0) if m5 else 'no summary'}'",
    None if alt5_ok else "Over-constraint or incomplete run: see alt5 output file")

for k in (1, 2, 3):
    row(f"lab-twin-{k}", f"python -I -W error on tests/labs/E3/lab-E3-project-{k}.py", f"tests/labs/E3/lab-E3-project-{k}.py", "PASS",
        f"/tmp/verifyD6-E3-d/twin{k}.out rc=0, stderr 0 bytes; diff against page expected block: only the final newline")
row("lab-page-code-equals-twin", "page code of Labs 1-3 equals the twin", "project.html:58-140, 153-191, 394-581", "PASS",
    "extract_labs.py: Labs 1 and 3 identical except the final newline; Lab 2 page code has the four blanks '___' by design and the twin fills them with the two expressions the interpretation names (-math.log1p(math.exp(-z)), -math.log1p(math.exp(z)))")
row("lab-expected-equals-output", "expected block equals the twin output", "project.html:141-147, 193-196, 582-588", "PASS",
    "diff of each twin output against its page expected block: identical apart from the final newline")
row("lab1-prose-numbers", "numbers in Lab 1 prose vs printed output", "project.html:57, 148", "PASS",
    "twin1.out: pair 1 CRRA 496 500, prospect -30 500, P(A) 0.480149, log -0.733658; pair 2 prospect -762, CRRA 3000; sum -2.302315 (recomputed as 0.733658+1.014598+0.554059)")
row("lab2-prose-numbers", "numbers in Lab 2 prose vs printed output", "project.html:153, 193-197", "PASS",
    "twin2.out: -0.765595182, -0.625595182, P(A) 0.465057055; z = -0.14 recomputed from CE_A 1500, CE_B 2200, kappa 2")
row("lab3-prose-numbers", "numbers and claims in Lab 3 prose vs printed output", "project.html:393, 589", "PASS",
    "twin3.out: gamma_hat 0.6352, lambda_hat 6.1503, kappa_hat 2.0201, se 0.32 9.59 1.86, LL -7.1445, score 3.55e-10; mixed-sign answers 11 (pair 4 is the only pair with no mixed lottery, recomputed from the ANSWERS list)")
row("exemplar-word-count-A", "exemplar A memo word count = 117", "project.html:621", "PASS",
    "words_r6.py / words_r6b.py: whitespace-separated runs of the four memo blocks with tags removed = 117")
row("exemplar-word-count-B", "exemplar B memo word count = 582", "project.html:621", "FAIL",
    "words_r6.py / words_r6b.py: five memo blocks; whitespace-separated runs after tag removal = 435 (split on whitespace); split(' ') gives 440 (tags removed) or 450 (tags replaced by a space). No counting variant gives 582. Round 5 said 435; the delta changed the claim to 582.",
    "project.html:621: change '582 words' to '435 words' (the count from words_r6.py), or state the counting rule that gives another figure and show it.")
row("exemplar-scores-annotations", "exemplar data-scores and annotation levels agree with official scoring", "project.html:623-738", "PASS",
    "data-scores A 2,2,1,2,1 and B 3,3,4,3,3 equal the official-scoring sentences; annotation levels agree with each score")
row("seed49-se-docstring-numbers", "seed-49 SE step sensitivity quoted in test_project.py docstring", "course/modules/E/E3/grader/test_project.py:924-929", "PASS",
    "se_seed49_r6.out: forward h=1e-5 lambda 135.0541, h=1e-6 97.6747 (-27.7%), gamma 0.09474 and 0.07983 (-15.7%); reverse order 136.7795 (+1.3%) and 98.0856 (+0.4%)")
row("seed30-kappa-below-one", "LOW_KAPPA participant (generator seed 30) has kappa below 1 (page: 'precision below 1')", "project.html:213; test_project.py:36", "PASS",
    "se_seed49_r6.out: make_instance(30) kappa 0.635")
row("hours-arithmetic", "project hours sum and hub split", "project.html:357-368; index.html:29-43", "PASS",
    "1+1+3+4+3+2 = 14 = data-hours-project 14; lessons 8 x 7 = 56 = data-hours-lessons 56; 56 + 14 = 70 = 'Tier U · 70 hours'")
row("tolerance-disclosure", "every tolerance the suite applies is disclosed on the page (round-5 FAIL re-verified)", "project.html:213 vs test_project.py:224-237, 409-438, 518-572, 896-948", "PASS",
    "project.html:213 now states the prospect check 'tested in value units with a slack of 10^-9 times one plus the absolute value of the lottery's value', matching test_prospect_sure_amount_has_the_lottery_value_to_the_cent (line 233); the other tolerances were re-read and match")
row("spec-probability-text-fixed", "spec: probability text and sure amounts (round-5 spec-clarifying row re-verified)", "project.html:207", "PASS",
    "project.html:207 now says 'or a whole number such as \"1\" or \"0\" (a sure amount has probability \"1\")'; the grader's zero-probability and sure-amount tests use these forms")
row("questionnaire-fraction-contract", "spec says each probability is text that Fraction reads exactly; the questionnaire validator must enforce that",
    "project.html:207 vs project.html:273 (isProbability regex)", "FAIL",
    "The inline regex /^\\d+(\\/\\d+)?$/ accepts '1/0' and '0/0'; Python Fraction('1/0') and Fraction('0/0') raise ZeroDivisionError (ledgers/E3/scripts/E3-d-r6/fraction_and_counterfactual_r6.out: '1/0 ... questionnaire accepts=True; Fraction reads -> raises ZeroDivisionError'). The export therefore writes a responses.json the engine cannot read, and project.html:245 says the export has the form of (b).",
    "project.html:273: change the regex to /^\\d+(\\/[1-9]\\d*)?$/ (rejects zero denominators, keeps '0/5', '1', '0').")
row("grader-counterfactual-225-over-2", "grader docstring counterfactual is arithmetically right", "course/modules/E/E3/grader/test_project.py:845-847", "FAIL",
    "The docstring says 'A loss weight in this branch would give 225 / 2 instead'. With v(x)=x^(1/2) and the lottery 100 and 400 (value 15), a loss weight applied to the value gives 30 and the sure amount 900 cents; dividing the value by 2 gives 7.5 and 56.25 cents; 225 / 2 = 112.5 is what dividing the sure amount by lambda gives.",
    "Rewrite the sentence: 'A loss weight applied to the value would give 900 cents instead; dividing the sure amount by lambda would give 225 / 2.' Check the two numbers in python before committing.")
row("notation", "every symbol vs notation/notation.json", "project.html math (129 spans)", "PASS",
    "Registered symbols: only \\Phi is used (project.html stretch, 'standard normal distribution function'), which matches notation.json; T, R^*, R_f, gamma_3, gamma_4, Q are not used; gamma, lambda, kappa, zeta, xi, c, z, v, w, W, P are local per notation.json 'about'")
row("citations-reading", "reading section and citations vs lessons and registry", "project.html:757, 759-763", "PASS",
    "data-cite in lessons: kahneman1979prospect (L07, grade C, title only), ellsberg1961risk and gilboa1989maxmin (L08, grade C); pratt1964risk has no data-cite in L02 (named only); epstein1989substitution in L05 'registry record only ... no result'; all five keys exist in references/references.json")
row("concept-links", "concept links resolve to defined anchors", "project.html:53, 205, 207, 213", "PASS",
    "L02#def-certainty-equivalent, L03#def-crra-utility, L04#def-first-order-stochastic-dominance, L06#def-prospect-theory exist; the L03 Proposition 2.7 cited at project.html:53 is 'affine transformations leave certainty equivalents unchanged'")
row("lesson-definitions-cited", "L06 Definitions 1.2 and 1.3 and the CRRA normalised form", "project.html:53, 220", "PASS",
    "L06 Def 1.2 v(x)=x^alpha, -lambda(-x)^delta with alpha, delta, lambda > 0; Def 1.3 W = sum p_i v(x_i); L03 Def 1.3 u_gamma(w) = (w^(1-gamma)-1)/(1-gamma); project's affine relation w^(1-gamma) = (1-gamma)u_gamma(w)+1 is correct")
row("conventions-vs-grader", "conventions and identification sentences vs grader and reference", "project.html:220-225; grader/reference.py", "PASS",
    "reference.py implements the CRRA and prospect formulas, half-up rounding floor(y+1/2), exceptions with the stated messages; identification claim (all-gain or all-loss lottery independent of lambda) recomputed algebraically")
row("exception-table-vs-reference", "exception table rows vs reference.py and grader tests", "project.html:228-240", "PASS",
    "reference.py raises ValueError for model name, probability sum/sign ('probabilities must sum to 1'), wealth+prize <= 0 ('wealth plus prize must stay positive'), and empty responses or no mixed lottery; grader tests cover each row (lines 287-383, 630-733)")
row("scope-words", "scope words (only, all, every, exactly, same, any) in learner prose", "project.html:44, 57, 110, 119, 205-213, 223-225, 682, 722, 729, 757", "PASS",
    "each 'all gains or all losses' claim (line 223) is an algebraic fact (lambda cancels); 'only a mixed lottery can identify' (line 682) follows from line 223; 'exactly' sums are Fraction checks; 'every ... on at least 47 of 50' matches test_project.py:585-600")
row("process-words", "no process words in learner-visible text", "project.html visible text", "PASS",
    "scan of visible text (script and tags removed) for round, verif, build, fix, draft, pending, TODO, placeholder, agent, slice: no hit in visible text (hits only in code comments and docstrings)")
row("dag-unlinked-names", "concepts used by name outside the prerequisite closure (plan section 7 table)", "project.html visible text", "PASS",
    "plans/E3-build-plan.md section 7 names (maximum-likelihood, Fisher information, confidence interval, estimator, convex, Bellman, risk-neutral, martingale, risk premium, stochastic discount) are absent from project.html visible text (scan); used terms: logit (defined on the page, plain prose per section 7), Hessian (M2 hessian, closure), probability weighting (E3's own, L07, used after it), standard normal (plain)")
row("questionnaire-no-egress", "questionnaire script sends nothing", "project.html:249-353", "PASS",
    "grep: no fetch, XMLHttpRequest, sendBeacon or WebSocket in project.html; the only localStorage use is the theme key in the head script (line 8)")
row("grader-no-network-and-no-print", "grader imports and output checks", "course/modules/E/E3/grader/test_project.py:1092-1143", "PASS",
    "test walks the AST of elicit.py, requires stdlib modules and no NETWORK_MODULES; capsys check requires empty stdout and stderr; reference imports only math, collections.abc, fractions, typing")
row("instance-validity", "instances for seeds 0-49 meet the instance guards (run_graders)", "course/modules/E/E3/grader/instance.py", "PASS",
    "run_graders E3 0-49 PASS (its instance checks run on each seed); instance docstring guards re-read")
row("reading-and-report-claims", "claims about what the report and the lab print", "project.html:589, 682, 706, 716, 729", "PASS",
    "each printed number in exemplar text (0.6352, 6.1503, 2.0201, 0.32, 9.59, 1.86, -7.1445, 3.55e-10) appears in twin3.out; the 'mixed-sign answers: 11' count is printed")
row("not-checked-site-js", "browser behaviour outside project.html (autograder panel, code autosave, footer claim 'nothing you write leaves it', 'Lab 2 graded instantly')",
    "assets/js/site.js (not in slice)", "UNVERIFIABLE",
    "No browser run in this round; site.js is outside slice d. The page_smoke in-browser grader ran the suite once (45 pass).",
    "A browser run of the autograder panel and the questionnaire export is needed to check the autosave and export claims.")

frag = {
    "unit": "E3",
    "slice": "d",
    "round": 6,
    "verifier": "Claude Haiku 5.5, independent verifier for E3-d, round 6 (did not build E3)",
    "pin": "142ecfc2bd27061de18bd67e83df81e69f5c249d",
    "base": "440ed3c8216725d498d9c6d7c746907d4d418198 (round-5 pin). Delta 440ed3c..142ecfc in slice d: project.html (lines 54-57, 106-148, 194-204, 213, 290-293, 452-455, 618-621), grader/test_project.py (lines 385-411, 634-705), tests/labs/E3/lab-E3-project-1.py and -3.py (comments and grid_start docstring), mutants e3d6 are new; lessons L01-L08 and cards.json changed in the delta and were read only where a page claim cites them",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD6-E3-d",
    "scratch": "/tmp/verifyD6-E3-d",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Scripts: ledgers/E3/scripts/E3-d-r6/ (run_gates_r6.sh, extract_labs.py, words_r6.py, words_r6b.py, se_seed49_r6.py, "
        "witness_zero_loss_r6.py, witness_unchosen_r6.py, run_new_mutants_r6.py, write_fragment_r6.py) and the outputs beside them. "
        "Mutation run: mutate_E3_0_9_r6.out (99 files at the pin, seeds 0-9). New mutants: ledgers/E3/mutants/e3d6_01..03, run in new_mutants_r6.out. "
        "Alternatives: run_alternatives.py from the pin; alt1-3 in alternatives_0_9_r6.out (the run was stopped during alt4 and split); alt4 in alt4_seeds_0_4_r6.out and alt4_seeds_5_9_r6.out; alt5 in alt5_seeds_0_9_r6.out. "
        "Could not check: a real browser run of the autograder panel and the questionnaire (site.js is outside slice d); the rubric's calibration beyond the stated scores (cards excluded); "
        "live verify_refs (no reference changed); hours beyond arithmetic; a full repo pytest (only the five test files named in the gate list). "
        "The round-5 row exemplar-scores-consistent is not carried; the round-5 rows gate-ruff-format and the mutant count are re-verified above."
    ),
    "summary": "",
}
frag["summary"] = (
    f"E3-d round 6 at 142ecfc: verdict FAIL. Rows {len(rows)} (pass {sum(r['status']=='PASS' for r in rows)}, "
    f"fail {sum(r['status']=='FAIL' for r in rows)}, unverifiable {sum(r['status']=='UNVERIFIABLE' for r in rows)}). "
    f"Mutants {sum(1 for m in mutants if m.get('killed_by'))}/{len(mutants)} killed."
)
out = root / "ledgers/E3/E3-d.json"
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "mutants", len(mutants))
