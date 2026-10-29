"""Build ledgers/E2/E2-d.json (round 4) from the rows verified in this round and the mutation battery output.

Usage: .venv/bin/python -I ledgers/E2/scripts/E2-d-r4/build_fragment_r4.py <mutate_output_file>
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
mut_out = Path(sys.argv[1]).read_text().splitlines()
mutants = []
for line in mut_out:
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*?) -> (.*)$", line)
    if not m:
        continue
    status, fname, desc, killed = m.groups()
    mutants.append(
        {
            "id": fname[:-3],
            "description": desc,
            "file": f"ledgers/E2/mutants/{fname}",
            "killed_by": killed if status == "KILLED" else "",
        }
    )
assert len(mutants) == 38, len(mutants)

R = "PASS"
F = "FAIL"
rows = [
    ("proj-gate-check-projects", "gate", "tools/check_projects.py --all", R,
     "Re-run on pin b276325: 'check_projects E2: PASS', exit 0 for all 14 projects."),
    ("proj-gate-check-pages", "gate", "tools/check_pages.py --all", R,
     "Re-run on pin b276325: 'check_pages E2: PASS', exit 0 for all 14 projects."),
    ("proj-gate-check-dag", "gate", "tools/check_dag.py --all", R,
     "Re-run on pin b276325: 'check_dag E2: PASS', exit 0."),
    ("proj-gate-run-graders", "gate", "course/modules/E/E2/grader/reference.py", R,
     "Re-run: tools/run_graders.py --unit E2 --seeds 0-49 -> 'run_graders E2: PASS (reference 50/50 seeds, slowest 0.2 s)', exit 0."),
    ("proj-gate-local-pytest", "gate", "course/modules/E/E2/grader/test_project.py", R,
     "pytest --collect-only on reference+instance+test_project in /tmp/e2d_r4_collect -> '40 tests collected'. The suite itself runs in run_graders (50/50 seeds)."),
    ("proj-gate-mutate-battery", "gate", "ledgers/E2/mutants/*.py", F,
     "Re-run: tools/mutate_graders.py --unit E2 --seeds 0-49 -> 'mutate_graders E2: FAIL (37/38 killed)'. Survivor: x02_zero_bids_never_win.py (suite does not check the winners of a zero-bid tie). Fix: in test_zero_bid_is_accepted assert allocate([0]*N, UNITS) == [True]*UNITS + [False]*(N-UNITS) (lower index wins a tie at zero, project.html Conventions 'Winners', line 170)."),
    ("proj-grader-zero-bid-winners", "grader", "course/modules/E/E2/grader/test_project.py test_zero_bid_is_accepted; project.html Conventions Winners (line 170)", F,
     "A zero bid is valid (project.html Conventions: a bid is a non-negative integer in cents), and allocate awards the units highest bids with a tie to the lower index (project.html line 170). test_zero_bid_is_accepted only calls valid(...) and never checks who wins, so mutant x02_zero_bids_never_win.py (zero bids never win) survives seeds 0-49. Fix: assert allocate([0]*N, UNITS) == [True]*UNITS + [False]*(N-UNITS) and that uniform payments are all 0 for zero bids."),
    ("proj-alt-correct-implementations", "gate", "ledgers/E2/scripts/run_alternatives.py", R,
     "Re-run: python -I ledgers/E2/scripts/run_alternatives.py -> alt01..alt05 each 'PASS suite 50/50 seeds; symmetric-bid mismatches vs reference 0'."),
    ("proj-autograder-instances", "grader", "course/modules/E/E2/grader/instance.py", R,
     "Read in full: n = randint(2,5), units = randint(1, n-1), values and bids randint(0, 10000); matches project.html Inputs (line ~152) and the spec ranges."),
    ("proj-autograder-pyodide", "grader", "course/modules/E/E2/project.html (grader panel), page_smoke", R,
     "Re-run: tools/page_smoke.py --unit E2 --pages project.html -> 'page_smoke E2: PASS'. The Pyodide run of the browser grader itself was not exercised separately (honest gap)."),
    ("proj-autograder-failure-messages", "grader", "course/modules/E/E2/grader/test_project.py", R,
     "Read in full (474 lines). Failure messages name the property and the revisit idea and never print expected values (must_refuse, valid, pytest.fail calls)."),
    ("proj-autograder-exception-table", "grader", "course/modules/E/E2/project.html Conventions 'Exception table' (line ~178-180); test_project.py", R,
     "The four ValueError conditions (format; units bounds; negative bid or value; n<2) match the page; the tests use names regexes (uniform.*discriminatory, units, n, bid|value) tied to the page's messages."),
    ("proj-spec-completeness", "grader", "project.html 'Required outputs' and interface; grader/starter.py", R,
     "Interface signatures on project.html (line ~161-165) match grader/starter.py and reference.py exactly."),
    ("proj-ladder-order", "page", "project.html lines 41-47", R,
     "Rungs 1-4 in order; rung 3 links to spec, autograder, memo sections that exist (#spec, #grader-section, #memo, #stretch)."),
    ("proj-ladder-curriculum-scope", "scope", "curriculum/02-economics-finance-core.yaml lines 83-85; course/modules/E/E2/project.html line 149", F,
     "Curriculum brief: 'Simulate uniform-price vs. discriminatory auctions with strategic bidders and compare revenue, bid shading and allocative efficiency.' Page line 149: 'Strategic bidding is tested in one form only: the single-unit closed form of Proposition A1. For more than one unit ... no multi-unit equilibrium is claimed or required.' The page narrows the curriculum brief; no architect decision recorded in plans/E2-build-plan.md. Fix: architect either restores strategic multi-unit content to the project or amends the curriculum brief (verifier does not edit curriculum)."),
    ("proj-scope-words-one-form", "scope", "project.html line 149 vs grader/test_project.py line 170", F,
     "Line 149 says strategic bidding is 'tested in one form only', but test_project.py test_uniform_symmetric_bid_is_the_value (line 170) tests the second form (uniform symmetric bid = value, Proposition A2). Fix: say 'tested in the single-unit closed forms of Propositions A1 and A2 only'."),
    ("proj-hours-sum", "hours", "project.html lines 183-191 (time budget); data-hours-project", R,
     "1 + 2 + 8 + 3 + 4 + 2 = 20 = data-hours-project=\"20\" (project.html line 35)."),
    ("proj-hours-estimate", "hours", "project.html line 191; course/modules/E/E2/index.html lines 28-29", R,
     "index.html data-hours-lessons=90 + data-hours-project=20 = 110 = module hours. 20/110 = 18.18 %, displayed 18.2 %."),
    ("proj-hours-share-claim", "hours", "project.html line 191", R,
     "Round-3 FAIL is fixed: line 191 now reads '18.2 % of the module's 110 hours (20 divided by 110)', consistent with the hub's 110 and 20."),
    ("proj-lab-1", "lab", "tests/labs/E2/lab-E2-project-1.py; project.html lines 56-101", R,
     "run_labs E2 12/12 PASS; twin run under python -I -W error exit 0; page code and expected block equal output (run_labs)."),
    ("proj-lab-2", "lab", "tests/labs/E2/lab-E2-project-2.py; project.html lines 105-140", R,
     "run_labs PASS; twin run under -I -W error exit 0; expected block matches output [4800,0,4800,0], [5200,0,6100,0], gap 1700."),
    ("proj-lab-3", "lab", "tests/labs/E2/lab-E2-project-3.py; project.html lines 249-383", R,
     "run_labs PASS; twin run under -I -W error exit 0. Each printed line recomputed by hand (ranking, winners, 18600, 21700, 3100, 16.7 %, 22800/23700, 96.2 %, closed forms 3650/4867/5475/5840, revenues 1/3,1/2,3/5,2/3)."),
    ("proj-lab1-numbers", "numbers", "project.html lines 57, 101", R,
     "Hypothesis: 9600, 11300, 1700, 17.7 % (1700/9600 = 17.708). Interpretation: 400 and 1300 cents overpayments (5200-4800, 6100-4800). All match the printed output."),
    ("proj-lab3-numbers", "numbers", "project.html lines 249-383, 459-466, 486-489", R,
     "Every number quoted on the page (18600, 21700, 3100, 16.7 %, 22800, 23700, 96.2 %, 3650/4867/5475/5840, 1/2 and 2/3) recomputed independently and equal to the Lab 3 output. 3100/18600 = 16.67 %."),
    ("proj-prop-A1-proof", "math", "project.html lines 210-215, 496", R,
     "Derivative recomputed: pi'(b) = b^(n-2)/c^(n-1) [(n-1)v - nb] (checked symbolically by hand); sign pattern and maximiser b* = cv verified. Assumption 5 is used at the tie step."),
    ("proj-prop-A2-proof", "math", "project.html lines 220-224", R,
     "Case analysis M<v, M>v, M=v re-derived; each case gives truthful payoff >= any bid's payoff. Proof is correct under Assumptions 1, 2, 4."),
    ("proj-prop-A3-proof", "math", "project.html lines 225-227, 497", R,
     "E[V(1)] = n/(n+1), E[V(2)] = (n-1)/(n+1) via P(V(2)>x) = 1 - x^n - n(1-x)x^(n-1); first price (n-1)/n * n/(n+1) = (n-1)/(n+1). Checked: n=2 gives 1/3, a known value."),
    ("proj-symmetric-bid-oracle", "math", "grader/reference.py symmetric_bid_single_unit; project.html line ~176", R,
     "floor(((n-1)v)/n + 1/2) computed as (2(n-1)v + n)//(2n) in the oracle, equal to the Fraction rule in reference.py; alternatives alt01-alt05 agree with reference for n=2..5, v=0..10000 (0 mismatches)."),
    ("proj-rubric-observability", "rubric", "project.html lines 401-415 and 421-500", R,
     "The rubric table is readable without JavaScript; data-scores attributes equal the official-scoring sentences for both exemplars."),
    ("proj-rubric-exemplar-A-scores", "rubric", "project.html line 422 and data-scores line ~421", R,
     "data-scores 2,4,3,3,3,2 equals the printed 'C1 2 · C2 4 · C3 3 · C4 3 · C5 3 · C6 2'. Each score agrees with the annotation levels (meets/misses) in its passage."),
    ("proj-rubric-exemplar-A-C1", "rubric", "project.html lines 422 (verdict), 438 (memo), 442-443 (annotations)", F,
     "Verdict line 422 and annotation line 443 say the memo 'names no clearing rank k' and that 'k is not named'. The memo at line 438 reads 'Five bidders and three units ... ranked[3]', which names n, k (three units) and the clearing rank. The level-2 score can stand on the missing sentence for each of Assumptions 1 to 5, but the stated reason is wrong. Fix: 'Misses C1 level 3: Assumptions 1 to 5 are listed by name without the sentence each one applies to.' and drop the k claim in line 422."),
    ("proj-rubric-exemplar-A-annotations", "rubric", "project.html lines 422 (verdict), 431 (annotation), appendix A3 in the same exemplar", F,
     "Line 431 says the one-unit expected revenues are given 'with none of the Proposition A3 integrals that produce them', and line 422 says they are 'stated without the integrals of Proposition A3'. The same memo's appendix A3 (line ~ 'A3. The integrals ...') states both integrals. The real gap is that only n = 3 and n = 5 are given, not each n from 2 to 5. Fix: reword lines 422 and 431 to that gap."),
    ("proj-rubric-exemplar-B", "rubric", "project.html lines 511-535", R,
     "Verdict and annotations consistent: C1 2, C2 1, C3 2, C4 2, C5 2, C6 2 with the cited level cells (for example C2 level 1 'states a bid with no derivation')."),
    ("proj-rubric-levels-cover-memo", "rubric", "project.html lines 399-400 and the brief (lines 375-398)", R,
     "Six criteria; each brief section maps to a criterion; the bar at level 3 is stated (line 399-400)."),
    ("proj-atlas-studios", "atlas", "course/modules/E/E2/project.html; check_projects", R,
     "check_projects E2 PASS; project.html has no atlas or studio reference that conflicts with curriculum (no atlas key on E2 per plans/E2-build-plan.md line 29)."),
    ("proj-figures", "figures", "course/modules/E/E2/project.html", R,
     "No figure element on the page; check_pages E2 PASS; page_smoke PASS."),
    ("proj-banned-phrases", "prose", "project.html; cards.json; grader/*.py", R,
     "check_pages PASS. Read for the banned words listed in the gates; no hits in the changed hunks."),
    ("proj-process-words", "prose", "project.html", R,
     "Grep for we, our, I, let's, this section, students, learners, draft, revision: the only hit is the time-budget row 'Design memo draft and revision' (line 189), a task name in the project brief, not a process word about the page. Judged not a finding."),
    ("proj-references", "references", "project.html lines 586-592; references/references.json", R,
     "Reading list keys vickrey1961counterspeculati and milgrom1982theory exist in references/references.json (lines 22219 and 17331). verify_refs --offline: 'offline integrity: 560 entries, 0 problems'."),
    ("proj-notation", "notation", "notation/notation.json; project.html", R,
     "Registered macros: only \\E is used on the page (registered). No registered symbol (T, Phi, gamma_3, gamma_4, R*, R^{e*}, R_f, Q) is used. beta, pi, c, V, M, k, n are unregistered locals, defined on the page."),
    ("proj-cards-duplicates", "cards", "course/modules/E/E2/cards.json", R,
     "121 cards; no duplicate ids, fronts or backs (scripts/E2-d-r4/cards_r4.py output)."),
    ("proj-cards-sample-13", "cards", "cards.json: c011, c023, c035, c069, c081, c083, c084, c085, c095, c097, c101, c112, c113", R,
     "Changed or numerically heavy cards read against the lesson text: c011 (L01 line 153 and Assumption 2, line 145: [0,90]); c023 (L02 line 102: Assumptions 1-4); c035 (L03 line 75: Assumption 3); c069 (L06 Assumptions 1 and 4); c081 (L07 uses x-hat); c083 (c = v_L - p_H v_H with p_L + p_H = 1, so c=0 is the tie); c084/c085 recomputed; c095 (4/9 recomputed); c101 (52613 = 26673331 - 26620718; 52613/79810 = 0.66); c112/c113 (L09 Assumption 1 line 59 and 257); c097 (4000/3). All consistent."),
    ("proj-cards-numbers-in-lesson", "cards", "cards.json; the card's own lesson", R,
     "Scripted presence check (scripts/E2-d-r4/cards_r4.py) flagged 700 (c011), 30,000,000 (c058, c061) and 13 (c120). Manual grep: 700 at L01.html:153; 30000000 at L05.html:224 and :352 (no commas, same number); 13 at L09.html:397. The script's tag stripping drops text after a bare '<' in math, so those were script artifacts. All card numbers are present in their lessons."),
    ("proj-cards-numerics-discrete-EM", "cards", "cards.json E2-c098 (line ~666) and E2-c097, c100, c105; L08.html lines 113, 135, 370-372, 412-413", F,
     "Exact value verified: E[M] = 85418692002000/64048012001 = 1333.6665625260364 (recomputed from the Proposition 2.2 sum with Fractions). But E2-c098 now has grade T while its basis field still reads 'Lab 1, Part B (Proposition 2.2 sum evaluated with fractions)', and L08 line 413 gives basis 'Proposition 2.2 evaluated exactly'. open-items (plans/E2-open-items.md line 35) records this as a lesson defect. Fix: make the card's basis match the lesson (or keep grade C with the lab as basis, if the architect rules the exact arithmetic is not a page derivation)."),
]

out = {
    "unit": "E2",
    "slice": "E2-d",
    "round": 4,
    "verifier": "Claude Haiku 5.5, independent verifier for E2-d, round 4 (did not build E2)",
    "pin": "b276325",
    "base": "ccfdf4c (round-3 pin); delta in slice: project.html lines 149, 170, 191, 223-227, 420-510; cards.json c011, c023, c035, c069, c081, c083, c098, c112, c113",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyC4-E2-d",
    "scratch": "/tmp/e2d_r4_collect",
    "verified_at": "2026-10-28T00:00:00+00:00",
    "verdict": "FAIL",
}
PASS_ = "PASS"
built = []
for rid, cat, loc, st, ev in rows:
    row = {"id": rid, "check": cat, "location": loc, "status": st, "evidence": ev}
    if st != "PASS":
        row["fix"] = ev.split("Fix: ", 1)[1] if "Fix: " in ev else "see evidence"
    built.append(row)
out["rows"] = built
out["verdict"] = "PASS" if all(r["status"] == "PASS" for r in built) and all(m["killed_by"] for m in mutants) else "FAIL"
out["mutants"] = mutants
out["registry_flags"] = []
out["freshness_flags"] = []
out["notes"] = (
    "Round 4 on b276325 (delta ccfdf4c..b276325 in slice: project.html, cards.json; grader/ and tests/labs/E2/lab-E2-project-*.py unchanged). "
    "Re-verified from scratch: every round-3 non-PASS row (scope, hours share (now PASS), exemplar A C1 and annotations) and every row whose subject changed (project.html, cards.json). "
    "Command rows run by me on the pin: check_projects, check_pages, check_dag, run_graders E2 0-49, mutate_graders E2 0-49 (38 mutants incl. 3 new x01-x03), run_labs E2, page_smoke project.html, verify_refs --offline, run_alternatives (5 alternatives), twins under python -I -W error, ruff check and format --check on grader and tests/labs/E2, pytest --collect-only (40). "
    "Not run: mypy --no-incremental (run_graders runs mypy --strict on reference, starter and instance only), the full pytest suite (outside slice d), a Pyodide browser run of the grader panel beyond page_smoke, render/build_site/fetch_data gates (no input in slice changed). "
    "Card coverage: all 121 cards read; number presence scripted; claim-by-claim agreement with the lesson text was checked for the 13 sampled and changed cards only, so the remaining cards are an honest gap at that depth."
)
n_fail = sum(1 for r in built if r["status"] != "PASS")
out["summary"] = (
    f"E2-d round 4: verdict {out['verdict']}. {len(built)} rows: {len(built) - n_fail} PASS, {n_fail} FAIL. "
    f"Mutants: {len(mutants)} files, {sum(1 for m in mutants if m['killed_by'])} killed; x02_zero_bids_never_win survives."
)
Path(ROOT / "ledgers" / "E2" / "E2-d.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
print("wrote", ROOT / "ledgers" / "E2" / "E2-d.json", out["verdict"], out["summary"])
