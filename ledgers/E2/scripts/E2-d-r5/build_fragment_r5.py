"""Builds ledgers/E2/E2-d.json (round 5, verifier E2-d). Evidence strings cite commands re-run on pin 04626e9."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
mutate_out = Path("/tmp/e2d_r5_mutate.out").read_text(encoding="utf-8").splitlines()
mutants = []
for line in mutate_out:
    m = re.match(r"KILLED (\S+): (.*) -> (.*) \(seed (\d+)\)$", line.strip())
    if m:
        mutants.append({
            "id": m.group(1).removesuffix(".py"),
            "description": m.group(2),
            "file": f"ledgers/E2/mutants/{m.group(1)}",
            "killed_by": f"{m.group(3)} (seed {m.group(4)})",
        })
assert len(mutants) == 41, len(mutants)

R = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    R.append(r)

# gates, re-run on pin 04626e9
row("proj-gate-check-pages", "gate", "tools/check_pages.py --all", "PASS", "Re-run: 'check_pages E2: PASS' (exit 0).")
row("proj-gate-check-dag", "gate", "tools/check_dag.py --all", "PASS", "Re-run: 'check_dag E2: PASS' (exit 0).")
row("proj-gate-check-projects", "gate", "tools/check_projects.py --all", "PASS", "Re-run: 'check_projects E2: PASS' (exit 0).")
row("proj-gate-run-graders", "gate", "course/modules/E/E2/grader/reference.py", "PASS", "Re-run: tools/run_graders.py --unit E2 --seeds 0-49 -> 'run_graders E2: PASS (reference 50/50 seeds, slowest 0.1 s)'.")
row("proj-gate-local-pytest", "gate", "course/modules/E/E2/grader/test_project.py", "PASS", "Scratch /tmp/e2d_r5_run (reference copied as auction_sim.py): QF_SEED=12345 pytest -q -p no:cacheprovider --assert=plain -W error test_project.py -> '40 passed'; --collect-only -> '40 tests collected'.")
row("proj-gate-mutate-battery", "gate", "ledgers/E2/mutants/*.py (41 files)", "PASS", "Re-run: tools/mutate_graders.py --unit E2 --seeds 0-49 -> 'mutate_graders E2: PASS (41/41 killed)' (/tmp/e2d_r5_mutate.out). Round-4 survivor x02_zero_bids_never_win.py is now killed by test_zero_bid_is_accepted. New y01-y03 killed.")
row("proj-alt-correct-implementations", "gate", "ledgers/E2/scripts/run_alternatives.py", "PASS", "Re-run: python -I ledgers/E2/scripts/run_alternatives.py -> alt01..alt05 each 'PASS suite 50/50 seeds; symmetric-bid mismatches vs reference 0', exit 0.")
row("proj-page-smoke", "gate", "tools/page_smoke.py --unit E2 --pages project.html", "PASS", "Re-run: 'page_smoke E2: PASS'. The in-browser Pyodide run of the grader was not exercised separately (honest gap).")
row("proj-gate-ruff-mypy", "gate", "pyproject.toml; grader/*.py; tests/labs/E2/lab-E2-project-*.py", "PASS", "ruff check . -> 'All checks passed!'; ruff format --check course/modules/E/E2/grader -> '4 files already formatted'; mypy --no-incremental (repo config) -> 'Success: no issues found in 229 source files'.")
row("proj-gate-verify-refs", "gate", "tools/verify_refs.py --offline", "PASS", "Re-run: 'offline integrity: 560 entries, 0 problems'.")
row("proj-lab-1", "lab", "tests/labs/E2/lab-E2-project-1.py; project.html lines 55-102", "PASS", "run_labs E2 12/12 PASS (covers page code = twin and expected block = output). Twin under python -I -W error exit 0.")
row("proj-lab-2", "lab", "tests/labs/E2/lab-E2-project-2.py; project.html lines 104-142", "PASS", "run_labs E2 PASS; twin under -I -W error exit 0; expected block [4800,0,4800,0], [5200,0,6100,0], gap 1700 matches.")
row("proj-lab-3", "lab", "tests/labs/E2/lab-E2-project-3.py; project.html lines 249-384", "PASS", "run_labs E2 PASS; twin under -I -W error exit 0; every printed line recomputed by hand and by Fraction code (ranking [2,0,1,3,4], winners [0,1,2], 18600, 21700, 3100, 16.7 %, 22800/23700, 96.2 %, 3650/4867/5475/5840, 1/2, 2/3, 3/5 neither; n=2..5 expected revenues equal).")
row("proj-lab3-model-docstring", "lab", "project.html line 254; tests/labs/E2/lab-E2-project-3.py line 3 (docstring)", "FAIL",
    "The docstring says 'each uniform on the cent grid [0, 10000]'. The code is continuous: expected_order_statistic integrates over [0,1] (lab line ~313-318) and first_price_payoff uses cutoff/CAP as a continuous probability (line ~321-328). Page Assumption 2 (project.html line 203) says values are uniform on [0, 10000] cents, a continuous model. 'On the cent grid' describes a discrete model the lab does not compute.",
    "Replace 'each uniform on the cent grid [0, 10000]' with 'each uniform on [0, 10000] cents, a continuous model as in Assumption 2' in the page and the twin (the twin must be re-embedded with tools/embed_labs.py --refresh lab-E2-project-3 by the builder).")

# grader
row("proj-autograder-instances", "grader", "course/modules/E/E2/grader/instance.py", "PASS", "Read in full (36 lines): n = randint(2,5), units = randint(1, n-1), values and bids randint(0, 10000), label SIMULATED; matches project.html lines 151-152.")
row("proj-autograder-pyodide", "grader", "project.html grader panel (line 235); page_smoke", "PASS", "page_smoke E2 PASS. The in-browser run was not exercised separately (honest gap).")
row("proj-autograder-failure-messages", "grader", "course/modules/E/E2/grader/test_project.py", "PASS", "Read in full (477 lines). must_refuse and valid never print expected values; failure texts name the property and the revisit idea.")
row("proj-autograder-exception-table", "grader", "project.html line 176; test_project.py lines 186-300", "PASS", "Four ValueError conditions (format; units bounds; negative bid or value; n<2) match the page; tests use name regexes uniform.*discriminatory, units, n, bid|value.")
row("proj-grader-zero-bid-winners", "grader", "test_project.py lines 313-321; project.html line 169-172 (Conventions)", "PASS", "Round-4 FAIL fixed: test_zero_bid_is_accepted now asserts allocate([0]*N, UNITS) == [True]*UNITS + [False]*(N-UNITS), uniform payments all 0, discriminatory revenue 0. Mutant x02 is killed.")
row("proj-grader-seed-claim", "grader", "project.html line 164 ('on the seeded instance and on further seeds')", "FAIL",
    "The suite checks the seeded instance and exactly one further instance (test_project.py line 31: OTHER = make_instance(SEED + 7_919)), plus a fixed value sweep. 'Further seeds' (plural) overstates the suite.",
    "Replace 'on the seeded instance and on further seeds' with 'on the seeded instance and on a second seeded instance, and on a fixed sweep of values'.")
row("proj-spec-completeness", "grader", "project.html lines 153-159; grader/starter.py lines 15-36", "PASS", "Five signatures on the page equal starter.py and reference.py.")
row("proj-grader-over-constraint", "grader", "test_project.py; ledgers/E2/scripts/run_alternatives.py", "PASS", "Five alternative correct implementations pass seeds 0-49 with zero symmetric-bid mismatches vs reference; ValueError is demanded only for the four conditions the page names (lines 176, 162).")

# ladder, scope, hours
row("proj-ladder-order", "page", "project.html lines 41-47", "PASS", "Rungs 1-4 in order; links #spec, #grader-section, #memo, #stretch resolve (ids present).")
row("proj-ladder-curriculum-scope", "scope", "curriculum/02-economics-finance-core.yaml 83-85; project.html line 149; plans/E2-build-plan.md lines 295-296, 489-492, 623-624", "PASS",
    "Round-4 FAIL cleared: plans/E2-build-plan.md now carries the binding Architect decisions (line 623-624: 'the project tests the single-unit closed form and the multi-unit payment and allocation rules only (no multi-unit equilibrium is claimed)'). Page line 149 states exactly that.")
row("proj-scope-words-one-form", "scope", "project.html line 149; test_project.py lines 170-178", "PASS", "Round-4 FAIL cleared: line 149 now says 'tested in the single-unit closed forms of Propositions A1 and A2 only'; the suite tests A1 (test_first_price_symmetric_bid..., line 136) and A2 (test_uniform_symmetric_bid_is_the_value, line 170).")
row("proj-hours-sum", "hours", "project.html lines 186-192", "PASS", "1 + 2 + 8 + 3 + 4 + 2 = 20 = data-hours-project=\"20\" (line 33).")
row("proj-hours-estimate", "hours", "project.html line 192; course/modules/E/E2/index.html lines 28-29", "PASS", "index data-hours-lessons=90 + data-hours-project=20 = 110. 20/110 = 18.18 %, displayed 18.2 %.")
row("proj-hours-share-claim", "hours", "project.html line 192", "PASS", "'18.2 % of the module's 110 hours (20 divided by 110)' is arithmetically consistent with the hub.")

# math
row("proj-prop-A1-proof", "math", "project.html lines 211-217", "PASS", "Re-derived: pi(b)=(v-b)(b/c)^(n-1) on [0,c]; pi'(b)=b^(n-2)/c^(n-1)[(n-1)v-nb]; sign change at cv; cv<=c; b>c gives v-b<v-c. Assumption 5 used at the tie step. Correct.")
row("proj-prop-A2-proof", "math", "project.html lines 221-222", "PASS", "Case analysis M<v, M>v, M=v re-derived; uniform winner pays highest rival bid M; truthful bid weakly dominant. Correct (uses Assumption 1 and the uniform-price rule).")
row("proj-prop-A3-proof", "math", "project.html lines 226-227", "PASS", "E[V(1)] = n/(n+1), E[V(2)] = (n-1)/(n+1) via P(V(2)>x) = 1 - x^n - n(1-x)x^(n-1); first price (n-1)/n * n/(n+1) = (n-1)/(n+1). Correct; n=2 gives 1/3, matching Lab 3.")
row("proj-symmetric-bid-oracle", "math", "grader/reference.py symmetric_bid_single_unit; project.html line 175", "PASS", "floor((n-1)v/n + 1/2) = (2(n-1)v + n)//(2n) (algebra verified); page example 'rounded half up' cases in test_symmetric_bid_rounds_an_exact_half_cent_up agree.")

# numbers
row("proj-lab1-numbers", "numbers", "project.html lines 57, 101", "PASS", "9600, 11300, 1700, 17.7 % (1700/9600 = 17.708); 400 and 1300 overpayments (5200-4800, 6100-4800). Printed output agrees (run_labs).")
row("proj-lab3-numbers", "numbers", "project.html lines 251, 384, 427, 462, 486", "PASS", "All quoted numbers recomputed: 18600, 21700, 3100, 16.7 % (3100/18600), 22800, 23700, 96.2 %, 3650/4867/5475/5840, 1/2 (n=3), 2/3 (n=5). n=2..5 expected revenues equal (Fraction).")

# rubric
row("proj-rubric-observability", "rubric", "project.html lines 404-415", "PASS", "Rubric table readable without JavaScript; six criteria, four levels each.")
row("proj-rubric-exemplar-A-scores", "rubric", "project.html line 421 data-scores and line 423 verdict", "PASS", "data-scores 2,4,3,3,3,2 equals the printed 'C1 2 · C2 4 · C3 3 · C4 3 · C5 3 · C6 2'. Arithmetic consistency only; the C2 = 4 score itself is not supported (see proj-rubric-exemplar-A-C2).")
row("proj-rubric-exemplar-A-C1", "rubric", "project.html lines 423, 438-444", "PASS", "Round-4 FAIL cleared: verdict now says C1 falls to level 2 because Assumptions 1-5 are listed by name without the sentence each applies to; the memo does name n (five bidders) and k (three units) and ranked[3]. Consistent with level 2.")
row("proj-rubric-exemplar-A-annotations", "rubric", "project.html lines 423, 432", "PASS", "Round-4 FAIL cleared: the one-unit expected revenues are given for n = 3 and n = 5 only (line 462); appendix A3 does state the integrals, so the claim is now the true gap.")
row("proj-rubric-exemplar-A-C2", "rubric", "project.html lines 421-423 (C2 = 4 in data-scores and verdict), 450-456 (Single-unit bids passage), 496-500 (appendix)", "FAIL",
    "Exemplar A is scored C2 = 4 and annotated 'Meets C2 level 4', but the rubric's level-3 cell for C2 (line 409) requires 'Gives the uniform bid as the value, with Proposition A2'. The Single-unit bids passage (lines 450-456) never mentions the uniform bid, and the appendix (lines 496-500) proves only A1 and A3 (A2 absent). The brief's section 3 (line 392) and the Appendix list (line 397) also require A2. The level-4 score is unsupported.",
    "Either add the uniform-bid sentence and the A2 proof to exemplar A, or lower C2 to 3 in data-scores (line 421), the verdict (line 423) and the annotation (line 455), so data-scores becomes 2,3,3,3,3,2.")
row("proj-rubric-exemplar-B", "rubric", "project.html lines 510-568", "PASS", "data-scores 2,1,2,2,2,2 matches verdict; annotations (C3 misses level 3 for 'about 20000'; C2 level 1 for a bid with no derivation; C4 level 2 for words only) agree with the rubric cells.")
row("proj-rubric-exemplar-B-brief", "rubric", "project.html lines 510-568 vs brief lines 388-398", "FAIL",
    "Exemplar B is introduced as 'written to this brief' (line 419), but its body is 106 words (brief: 500 to 1000, line 398) and it uses five headings, omitting the brief's 'Revenue, shading and efficiency' and 'Recommendation and limits' sections and renaming the others (brief: six sections in order, line 388-396). No annotation mentions this.",
    "Either bring exemplar B to the brief's six headings and length at level 2 content, or change line 419 to say the exemplars are abridged excerpts and state which brief elements they omit.")
row("proj-rubric-numbers-rule", "rubric", "project.html line 399 (Numbers) vs line 408 (C1 level 3 cell) and line 419", "FAIL",
    "The brief's Numbers rule (line 399) says every number the memo quotes is printed by run_report.py. The C1 level-3 cell (line 408) requires the value distribution 'uniform on [0,10000] cents', and exemplar A quotes it (line 439). Lab 3 does not print the cap. The rule and the cell contradict each other, and line 419 patches the exemplar intro but not the brief.",
    "Amend line 399 to allow 'or the value cap of 10000 cents from the model', so the brief's rule matches C1 level 3.")
row("proj-rubric-levels-cover-memo", "rubric", "project.html lines 375-400", "PASS", "Each brief section maps to a criterion; the bar at level 3 is stated (line 400).")

# others
row("proj-atlas-studios", "atlas", "project.html; check_projects", "PASS", "check_projects E2 PASS; no atlas or studio reference on the page.")
row("proj-figures", "figures", "project.html", "PASS", "No figure element; page_smoke PASS.")
row("proj-banned-phrases", "prose", "project.html; cards.json; grader/*.py", "PASS", "check_pages PASS; no banned phrase in changed hunks.")
row("proj-process-words", "prose", "project.html lines 190 ('Design memo draft and revision'), 208 ('this section')", "PASS", "No 'we', 'our', 'let's', 'learner'. 'draft and revision' is a time-budget task name and 'this section' describes the page's own derivation section; both are unchanged since the round-4 pin and judged not process words, as in round 4.")
row("proj-references", "references", "project.html lines 589-592; references/references.json", "PASS", "Keys vickrey1961counterspeculati and milgrom1982theory exist; verify_refs --offline 560 entries, 0 problems.")
row("proj-notation", "notation", "notation/notation.json; project.html", "PASS", "Only \\E is used from the registry; no registered symbol (T, Phi, gamma_3, gamma_4, R*, R^{e*}, R_f, Q) appears. pi, beta, c, v, b, V, M, k, n are unregistered locals defined on the page.")
row("proj-dag-concepts", "dag", "project.html lines 208, 394; L02.html #def-bayesian-nash-equilibrium; L08.html #def-winners-curse", "PASS", "Both concept links resolve to <dfn> ids (count 1 each). Concepts used are in E2's own lessons L01-L09; check_dag E2 PASS.")

# cards
row("proj-cards-duplicates", "cards", "course/modules/E/E2/cards.json", "PASS", "123 cards (E2-c001 to E2-c123): 0 duplicate ids, 0 duplicate fronts, 0 duplicate backs (scripts/E2-d-r5/r5_checks.py). Round 4 counted 121; c122 and c123 are new this pin.")
row("proj-cards-changed-36", "cards", "cards.json: c008 c015 c016 c017 c025 c026 c029 c032 c035 c041 c048 c050 c051 c052 c053 c060 c062 c065 c066 c072 c073 c075 c076 c080 c081 c086 c093 c103 c104 c106 c116 c122 c123 (and c098, c100, c105 below)", "PASS",
    "Every changed card re-read against its lesson: L01 Prop 3.2 and Remark 3.3 (c008, c015); L01 misconception example 5/3/6 (c016); L02 Prop 2.5 (c025, c026); L03 Prop 2.3 and proof (c035, c122, c123); L04 Spence and Remark 2.1 and 1,000,000/5,000,000 (c048, c050, c051); L05 Rothschild paragraph (c060); L06 Holmstrom paragraph, 525,000 and 600,000 (c072, c073); L07 'Nothing here is claimed for several agents' and grid_points_passing 15 (c080, c081, c086); L08 Prop 2.1 and Def 1.3 (c093, c103, c104, c106); L09 Part A bid 8000 pays 7000 (c116). Mechanical number check: 36 changed cards, 0 numbers missing from lesson text (scripts/E2-d-r5/numcheck_changed_cards.out).")
row("proj-cards-sample-13", "cards", "cards.json unchanged cards c011 c023 c069 c083 c084 c085 c095 c097 c101 c112 c113 and others", "PASS",
    "Carried from round 4 (the cards' bytes are identical to the round-4 pin b276325, as the cards.json diff shows none of these ids): c011 (L01 line 153 and Assumption 2), c023, c069, c083, c112, c113 re-read in round 4 and unchanged.")
row("proj-cards-numbers-in-lesson", "cards", "cards.json; scripts/E2-d-r5/numcheck_changed_cards.out", "PASS", "All numbers on the 36 changed cards occur in their lesson text (after removing LaTeX thousands separators).")
row("proj-cards-numerics-discrete-EM", "cards", "cards.json E2-c098 (line 664), E2-c100 (line 678), E2-c105 (line 715); L08.html line 113 and line 413", "FAIL",
    "Exact value confirmed: E[M] = 85418692002000/64048012001 = 1333.6665625260364 (scripts/E2-d-r5/r5_checks.py). But the grade is not supported. c098 is now T with the basis removed. c100 and c105 were C with basis 'Lab 1, Part B' and are now T. Their numbers (1333.67, the rounded shading 1334, the -0.67 cents) come from the evaluated fraction, which is not derived on the page. BLUEPRINT §3 reserves T for results 'proved on the page'. BUILDER_RULES §2(c) allows a number only if 'derived in a calculation shown on the page', and §7 requires a lab-established result to name the lab in basis. L08 line 113 says 'grade T, basis: Proposition 2.2; Lab 1 Part B uses it' and line 413 says 'Proposition 2.2 evaluated exactly with fractions', which do not agree with each other.",
    "Set E2-c098, E2-c100 and E2-c105 back to grade C with basis 'Lab 1, Part B (exact evaluation of the Proposition 2.2 sum with fractions)', and make L08 lines 113, 135 and 413 carry the same grade and basis (builder of L08 to edit, not this verifier). Alternatively the architect rules the exact arithmetic is a page derivation and the calculation is shown on the page.")

# freshness and notes
freshness = [
    "plans/E2-open-items.md line 32 says cards.json 'has 121 cards (E2-c001 to E2-c121)'. The file now has 123 (c122, c123 added this pin). Update the open-items note.",
    "L08.html lines 113 and 413 (outside this slice) state grade T for the discrete E[M]; see proj-cards-numerics-discrete-EM.",
]
notes = (
    "Round 5 on pin 04626e9 (base b276325, round-4 pin). Delta in slice: project.html lines 149, 173 (new Shading convention), 420-510 (exemplars); test_project.py lines 313-321; cards.json (36 cards changed or added, including c098, c100, c105 which were C and became T). "
    "Verifier-added mutants y01-y03 (ledgers/E2/mutants/) and the generator scripts/E2-d-r5/make_mutants_r5.py. Exemplar word counts: exemplar A summary 72 words, body 594; exemplar B body 106 (scripts/E2-d-r5/r5_checks.py). "
    "Honest gaps: (1) the in-browser Pyodide run of the grader and the self-assessment JavaScript were not exercised beyond page_smoke; (2) the reading-list titles come from references.json and were not re-read against the published works (no network access used); (3) the L08 lesson itself is outside this slice, so the L08 side of the EM grade is reported, not fixed."
)
summary = None  # filled below

non_pass = [r["id"] for r in R if r["status"] != "PASS"]
verdict = "PASS" if not non_pass else "FAIL"
fragment = {
    "unit": "E2",
    "slice": "E2-d",
    "round": 5,
    "verifier": "Claude Haiku 5.5, independent verifier for E2-d, round 5 (did not build E2)",
    "pin": "04626e9",
    "base": "b276325 (round-4 pin); delta in slice: project.html, test_project.py, cards.json (36 cards), lab-E2-project-3 twin unchanged",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyC5-E2-d",
    "scratch": "/tmp/e2d_r5_run; /tmp/e2d_r5_helpers",
    "verified_at": "2026-10-28T00:00:00+00:00",
    "verdict": verdict,
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": freshness,
    "notes": notes,
    "summary": f"E2-d round 5: {len(R)} rows, {len(R) - len(non_pass)} PASS, {len(non_pass)} non-PASS ({', '.join(non_pass)}). Mutants: 41 of 41 killed (38 existing + 3 new y01-y03); 5 alternatives pass. Gates re-run: check_pages, check_dag, check_projects, run_graders 50/50, mutate_graders, page_smoke, run_labs 12/12, ruff, mypy, verify_refs all green.",
}
out = ROOT / "ledgers" / "E2" / "E2-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(R), "non-pass", non_pass)
