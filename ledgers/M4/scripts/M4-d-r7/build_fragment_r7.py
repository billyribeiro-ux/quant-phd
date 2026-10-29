"""Builds ledgers/M4/M4-d.json for round 7 from the verifier's observed outputs."""
import json
import re
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyB7-M4-d")
OUT = ROOT / "ledgers/M4/M4-d.json"
MUT_OUT = ROOT / "ledgers/M4/scripts/M4-d-r7/mutate_M4_seeds0-9_r7.txt"
CARRY = "Carried from round 6 (project.html lines cited are byte-identical to 44f1eb6 for the hunks; diff hunks touch only lines 203-206 and 248-250): "
CARD_CARRY = "Carried from round 6 (cards.json entries other than the 32 changed or added ids are byte-identical since 44f1eb6): "
GRADER_CARRY = "Carried from round 6 (test_project.py lines cited are byte-identical since 44f1eb6; the only change is an insertion at lines 412-441): "

rows = []
def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

row("P-01", "Lab 1 hypothesis and interpretation numbers (8.4e9, 19800, 0.6, 1.0017, 1.0447, 210946, 243004, ratio 1.152, 1.6667)",
    "course/modules/M/M4/project.html:55-145", "PASS",
    CARRY + "re-ran tests/labs/M4/lab-M4-project-1.py under python -I -W error (exit 0); output in ledgers/M4/scripts/M4-d-r7/labout/lab-M4-project-1.txt.")
row("P-02", "Lab 2 completion page: expected block equals twin output; page code differs from twin only at the two blanks",
    "course/modules/M/M4/project.html:147-192", "PASS", CARRY + "project lab twin unchanged; run_labs M4 13/13 PASS on pin 7aa909e.")
row("P-03", "Lab 3 closed-form numbers: sd 91651.514, z 2.326348, parametric 99% loss 213213, index rows, nu-table",
    "course/modules/M/M4/project.html:266-314", "PASS", CARRY + "re-ran lab-M4-project-3 (exit 0); sqrt(8.4e9)=91651.514 re-derived.")
row("P-04", "Lab 1 code comments: four steps and the Student-t scale algebra",
    "course/modules/M/M4/project.html:58-135", "PASS", CARRY + "code read; scale sqrt((nu-2)/chi_square) is the stated algebra.")
row("P-05", "Appendix derivations E[W^-1]=1/(nu-2), E[W^-2]=1/((nu-2)(nu-4)), divergence exponents",
    "course/modules/M/M4/project.html:325, 429", "PASS", CARRY + "derived by hand from the stated density (round 6); lines unchanged.")
row("P-06", "Conventions and Assumption 1 (Gamma recursion; chi-square density)",
    "course/modules/M/M4/project.html:209-217", "PASS", CARRY + "lines 209-217 unchanged.")
row("P-07", "Cross-references: Lesson 6 Definition 2.1, Lesson 6 Student-t as Z/sqrt(W/nu), Lesson 1 quantile Definition 3.1",
    "course/modules/M/M4/project.html:211, 214, 482", "PASS", CARRY + "lines unchanged; cited lesson locators re-read in L06/L01 text.")
row("P-08", "Contract notes: fourth moment infinite at nu=3,4; sign convention leaves -R law unchanged because R is symmetric",
    "course/modules/M/M4/project.html:228", "PASS", CARRY + "line 228 unchanged; the grader's survivors m11, m17, n02, v4_m02 are the behaviours it discloses.")
row("P-09", "Grader count '131 checks' (changed from 126) equals the real collect-only count",
    "course/modules/M/M4/project.html:206", "PASS",
    "pytest -p no:cacheprovider --collect-only -q test_project.py with reference.py copied to tail_risk.py, python -I -W error: '131 tests collected in 0.02s'.")
row("P-10", "Rubric structure: five criteria, four levels, td cells, caption and check_projects agreement",
    "course/modules/M/M4/project.html:330-343", "PASS", CARRY + "lines unchanged; tools/check_projects.py --unit M4: PASS (exit 0).")
row("P-11", "Exemplar scores agree with their annotations", "course/modules/M/M4/project.html:348-462", "PASS", CARRY + "lines unchanged.")
row("P-12", "Exemplar numbers and word counts: 2267, 32058, 15.2 %, 1.0447 vs 4.5 %, 213213, 243004",
    "course/modules/M/M4/project.html:354-461", "PASS", CARRY + "lines unchanged; 213213 and 243004 re-observed in the lab outputs.")
row("P-13", "Hours arithmetic: budget 2+2+12+8+4+2=30; lessons 10 x 9 = 90; 90+30=120",
    "course/modules/M/M4/project.html:33, 237-243; index.html", "PASS", CARRY + "lines unchanged; check_pages M4: PASS.")
row("P-14", "Internal links and anchors resolve", "course/modules/M/M4/project.html (all href)", "PASS",
    CARRY + "git diff 44f1eb6..7aa909e shows no href change in project.html; check_pages M4 PASS on pin.")
row("P-15", "Process words and banned phrases in learner text (changed cards, grader, page)",
    "course/modules/M/M4/project.html; cards.json; grader/*.py", "PASS",
    "python regex scan for round-N, verifier, builder, fanout, haiku, TODO, FIXME, slice, checkout over the three files: zero hits.")
row("P-16", "Scope words on the page are backed or inside an annotated exemplar fault",
    "course/modules/M/M4/project.html", "PASS", CARRY + "only line 206 (count and the removed autosave sentence) changed; scope words on it unchanged.")
row("P-17", "page_smoke on the project page alone (light and dark, 360 px, labs, in-browser grader)",
    "course/modules/M/M4/project.html", "PASS",
    "tools/page_smoke.py --unit M4 --pages course/modules/M/M4/project.html --skip-labs --skip-sweep: 'page_smoke M4: PASS', exit 0 (ledgers/M4/scripts/M4-d-r7/page_smoke_project_r7.txt). Labs were run separately with run_labs.")
row("P-18", "Constraints item numbers (item 1, 2, 4, 5) refer to the unnumbered Conventions bullets",
    "course/modules/M/M4/project.html:204 vs 209-217", "PASS", CARRY + "line 204 unchanged.")
row("P-19", "--assert=plain claim: the failure shows the test's message and no computed values",
    "course/modules/M/M4/project.html:259", "PASS", CARRY + "line 259 unchanged.")
row("P-20", "Autosave and storage-refusal claim of the autograder panel",
    "course/modules/M/M4/project.html:248-250", "PASS",
    "Round 6 was UNVERIFIABLE because the browser autosave claim could not be run. In 7aa909e the sentence 'Your code is saved in this browser as you type ... if the browser refuses storage, the page says so' is removed (git diff hunk at line 248); grep for 'saved in this browser', 'browser refuses', 'storage' in project.html returns nothing. No claim remains, so there is nothing to verify.")

row("G-01", "Reference solution passes the suite on seeds 0-49 and collects 131 tests",
    "course/modules/M/M4/grader/reference.py; test_project.py", "PASS",
    "tools/run_graders.py --unit M4 --seeds 0-49: 'PASS (reference 50/50 seeds)'. Direct run: QF_SEED=0 pytest on reference as tail_risk.py: '130 passed, 1 skipped'.")
row("G-02", "Starter raises NotImplementedError and the suite fails on it", "course/modules/M/M4/grader/starter.py", "PASS",
    "starter.py copied as tail_risk.py: '129 failed, 1 passed, 1 skipped'.")
row("G-03", "Five round-6 alternatives and two new round-7 alternatives (tolerance 1e-300 pivot check; LDL^T factorisation) pass seeds 0-49",
    "ledgers/M4/scripts/M4-d-r7/alt6_tiny_tolerance.py, alt7_ldl.py; ledgers/M4/scripts/M4-d-r6/alts/alt1-alt5", "PASS",
    "Each alternative as tail_risk.py, QF_SEED 0..49 with -I -W error pytest: alt1..alt5 pass=50 fail=0; alt6_tiny_tolerance pass=50; alt7_ldl pass=50 (the new tiny-variance tests accept these).")
row("G-04", "Tolerance comment claims (maxima and failure counts by nu)", "course/modules/M/M4/grader/test_project.py:31-42", "PASS",
    GRADER_CARRY + "lines 31-42 unchanged.")
row("G-05", "Truncation comment: truncating toward zero gives variance about 2.7; rounding gives about 4 + 1/12",
    "course/modules/M/M4/grader/test_project.py:229-237", "PASS", GRADER_CARRY + "lines 229-237 unchanged.")
row("G-06", "Round-6 mutant r6_01 (three-asset last factor column dropped) is killed", "ledgers/M4/mutants/r6_01_three_asset_last_factor_column_dropped.py", "PASS",
    "mutate_graders --unit M4 --seeds 0-9 (round 7): KILLED r6_01 -> test_gaussian_loss_variance_matches_portfolio_covariance (seed 0).")
row("G-07", "Round-6 mutant r6_02 (chi-square with nu instead of nu/2) is killed", "ledgers/M4/mutants/r6_02_student_t_chi_square_twice_the_degrees.py", "PASS",
    "mutate_graders round 7: KILLED r6_02 -> test_student_t_loss_variance_matches_matched_covariance (seed 3).")
row("G-08", "Round-6 FAIL: mutant r6_03 (pivot tolerance 1e-12 rejects a valid variance of 1e-14) survives the suite", "ledgers/M4/mutants/r6_03_pivot_tolerance_rejects_small_positive_variance.py", "PASS",
    "Fixed in 7aa909e: new tests test_one_position_with_a_tiny_positive_variance_is_accepted and test_one_position_with_a_tiny_positive_variance_has_the_right_loss_variance. mutate_graders round 7: r6_03 is not in the SURVIVED list.")
row("G-09", "Pre-existing surviving mutant m11 (loss sign reversed) is disclosed", "course/modules/M/M4/project.html:204, 228", "PASS",
    "Not a new survivor (round-6 ruling). project.html:228 states 'The suite does not test the sign of the loss' and why. Disclosed.")
row("G-10", "Pre-existing surviving mutant m17 (Student-t draws from seed+1) is disclosed", "course/modules/M/M4/project.html:228", "PASS",
    "Pre-existing survivor. project.html:228 states 'The suite does not check the stream order'; carried.")
row("G-11", "Pre-existing surviving mutant n02 (one chi-square per asset) is disclosed", "course/modules/M/M4/project.html:215, 228", "PASS",
    "Pre-existing survivor. project.html:228 states 'it does not check that the Student-t family uses one chi-square variable per draw'; carried.")
row("G-12", "Pre-existing surviving mutant v4_m02 (matched factor skipped for nu 3 and 4) is disclosed", "course/modules/M/M4/project.html:204, 228", "PASS",
    "Pre-existing survivor. project.html:228: 'The suite therefore does not check the matched factor inside simulate_losses at those values'; carried.")
row("G-13", "Every ValueError condition named on project.html has a test that uses the named input",
    "course/modules/M/M4/grader/test_project.py:89-457", "PASS",
    GRADER_CARRY + "existing tests unchanged; the new tests are at 412-441. mutate_graders round 7 kills 82 of 86 mutants, the 4 survivors are the disclosed ones above.")
row("G-14", "instance.py seeded instance is the only source of the portfolio (no hard-coded answer)", "course/modules/M/M4/grader/instance.py:1-48", "PASS",
    CARRY + "instance.py unchanged since 44f1eb6.")
row("G-15", "Student-t draws must depend on the seed: the page says every run is reproducible from its seed, and a Student-t family that ignores the seed passes the suite",
    "course/modules/M/M4/grader/test_project.py:168-171; course/modules/M/M4/project.html:198", "FAIL",
    "Mutant r7_01_student_t_seed_fixed (rng = random.Random(0 if student else seed)) is SURVIVED on seeds 0-9 (mutate output and run_mut.sh). test_different_seed_gives_different_losses (test_project.py:168-171) only compares the gaussian family. project.html:198: 'it needs every run to be reproducible from its seed'.",
    "Parametrize test_different_seed_gives_different_losses over both families (gaussian and student_t with NU), so that a seed-independent Student-t stream is rejected. Re-run mutate_graders --unit M4 and confirm r7_01 is KILLED. Borderline: the page states reproducibility, not seed sensitivity in words; the verifier fails it closed.")

row("L-01", "Lab twin outputs equal the expected blocks; twins run alone under python -I -W error", "tests/labs/M4/lab-M4-project-{1,2,3}.py", "PASS",
    "run_labs --unit M4: 13/13 PASS; each project twin exit 0 under -I -W error (labout/).")
row("L-02", "Page code equals twin for project labs", "tests/labs/M4", "PASS", CARRY + "project lab twins unchanged.")
row("L-03", "Lesson lab twins L01-L10 run and exit 0 under python -I -W error", "tests/labs/M4/lab-M4-L01-1.py..L10-1.py", "PASS",
    "All 10 lesson twins exit 0 (ledgers/M4/scripts/M4-d-r7/labout/). Output values cited by new cards checked in L-04 and C-04.")
row("L-04", "Docstring of t3_tail_one_sided claims the formula avoids subtracting two nearly equal arctangents for large x; the learner-visible page code carries the same sentence",
    "tests/labs/M4/lab-M4-L10-1.py:60-61; course/modules/M/M4/L10.html:235", "FAIL",
    "The formula (atan(1/y) - y/(1+y^2))/pi with y = x/sqrt 3 subtracts two quantities that are both about 1/y for large x. Measured against a 60-digit Decimal evaluation: relative error 5.5e-11 at x = 1000, 8.2e-13 at x = 100, 1.5e-5 at x = 1e6 (python3 script in the scratch directory). The sentence is false about what the code does.",
    "Replace the docstring sentence with a true one, for example 'P(V > x) for x > 0, as arctan(1/y) minus y/(1+y^2) over pi with y = x/sqrt 3', and drop the cancellation claim. Re-embed L10 with tools/embed_labs.py L10.html --refresh <lab-id>. Outside this slice (lesson lab), recorded because the delta touched it.")

row("C-01", "cards.json schema: 191 cards, unique ids, lessons L01-L10 all have cards, valid grades, C cards carry a basis",
    "course/modules/M/M4/cards.json", "PASS",
    "python check: 191 cards; grades T 171, C 20; per lesson L01 17, L02 19, L03 16, L04 19, L05 18, L06 16, L07 15, L08 17, L09 24, L10 30; no C without basis; no T/basis mismatch; ids unique (c188-c191 are the new entries).")
row("C-02", "Card references resolve (Definition/Proposition/Example/Remark/Problem/Assumption) in the current lesson text",
    "course/modules/M/M4/cards.json vs L01-L10.html", "PASS",
    CARD_CARRY + "all changed or added cards checked against lesson text: c011 Example 3.5 (L01 line 133); c021 Def 2.1; c025 Ex 1.4; c029 Prop 2.2, Ex 2.5; c031 Ex 2.6; c039 Prop 2.3 hypotheses (L03 line 118); c057 Prop 1.8; c064 Problem P3 (L04 line 474); c074 Remark 1.8; c093/c095 Prop 2.6 (L06 line 194); c097 Prop 1.5 (L06 line 134); c102 Prop 1.4 (L07 line 119); c110 (L07 line 342); c119 Ex 1.5 (L08 line 117-120); c137 Section 3; c142 Problem E1 (L09 line 628); c152 Prop 2.1 (L10 line 183); c156 Assumption 3 (L10 line 220); c158 Prop 2.1; c181 Ex 2.5; c184 Lab 1 Part A; c191 Ex 2.5 (L05 line 211).")
row("C-03", "Card numbers appear in their lesson or lab output", "course/modules/M/M4/cards.json", "PASS",
    CARD_CARRY + "every number in the 32 changed or added cards grep-located in its lesson text or lab output: 15.17, 2.92, 2968750000, 54486.24, 1.708, 3.469, 489, 500, 2.065, 2.073, 5.580, 5.625, 0.9770, 2.0055, 0.0230, 0.0055, 0.0031, -0.0235, 2.205308, 40.4006, 64/9, 73/9, 2/9.")
row("C-04", "Lab-sourced card numbers equal the printed output of the lesson twin", "course/modules/M/M4/cards.json (c030, c033, c047, c183, c184, c188, c189, c190, c172)", "PASS",
    "Re-run twins: L02 'mean 3.469', 'losses 489'; L03 'skewness 2.065, kurtosis 5.580'; L04 'cell_0_0 joint 1/10 ... product 4/25', 'independent False'; L08 '(0.9770, -2.0055)' for n=20000 seed 2026; L10 normal n=10000 '+0.0031' (seed 2026), t(3) n=10000 '-0.0235' (seed 2027, SEED+1), Part D '2.205308'. Lab-sourced c172 is an exact closed-form evaluation, which the page labels 'no draws' (L10 line 646).")
row("C-05", "Exact card values recomputed", "course/modules/M/M4/cards.json", "PASS",
    CARD_CARRY + "recomputed: sqrt(2968750000)=54486.2368 -> 54486.24; sqrt(35/12)=1.707825 -> 1.708; sqrt(35/12) with 91/6 and 7/2 gives Var 35/12=2.9167 and E[X^2]=15.1667; 2/9 for Y=X^2 (E[Y]=2/3, E[Y^2]=2/3, Var=2/9); 40.4006; 4 sqrt(3)/pi = 2.2053156; Cov(1_A,1_B)=-ab.")
row("C-06", "Cards agree with the current lesson statements (hypotheses, proposition content, locators)", "course/modules/M/M4/cards.json vs L01-L10.html", "PASS",
    CARD_CARRY + "each changed card compared with its lesson text (see C-02). c039 now carries the Proposition 2.3 hypothesis (finite probability space with positive weights, X takes at least two values, a != 0), matching L03 line 118.")
row("C-07", "No duplicate cards (fronts and backs unique)", "course/modules/M/M4/cards.json", "PASS",
    "python check: no duplicate fronts, no duplicate backs, no duplicate ids across 191 entries.")

row("N-01", "Symbols used in project, grader and cards agree with notation/notation.json",
    "notation/notation.json; course/modules/M/M4/", "PASS",
    "Kurtosis is non-excess in the registry (gamma_4 entry: 'not excess'); c048 (73/9) and c183 (5.625) use that convention. New card c191 uses rho, S_1, S_2, Z_1, Z_2 locally defined in L05 Example 2.5; none is a registry symbol with another meaning.")
row("D-01", "DAG: project, cards and labs reference only prerequisite-closure concepts and lessons (L01-L10)",
    "course/modules/M/M4/project.html; cards.json; check_dag --unit M4", "PASS",
    "tools/check_dag.py --unit M4: PASS (exit 0) on pin 7aa909e.")
row("T-01", "Gates on the slice run on the pin: check_projects, check_pages, check_dag, run_graders, run_labs, ruff, mypy, mutate_graders, page_smoke",
    "ledgers/M4/scripts/M4-d-r7/", "PASS",
    "check_projects PASS; check_pages PASS; check_dag PASS; run_graders 50/50 PASS; run_labs 13/13 PASS; ruff check and ruff format --check on grader/ and tests/labs/M4 PASS. mutate_graders --unit M4 --seeds 0-9: 82/86 killed (the 4 disclosed survivors); r7 mutants 2 of 3 killed (r7_01 survives).")

mutants = []
for line in MUT_OUT.read_text(encoding="utf-8").splitlines():
    m = re.match(r"(KILLED|SURVIVED) (\S+)\.py: (.*?) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    mutants.append({"id": name, "description": desc,
                    "killed_by": None if killed.strip() == "None" else killed.strip()})
mutants.append({"id": "r7_01_student_t_seed_fixed",
                "description": "Round-7 student-error mutant. The Student-t family ignores the seed and always draws from seed 0, so a Student-t run is not reproducible from its seed.",
                "killed_by": None})
mutants.append({"id": "r7_02_two_position_symmetry_unchecked",
                "description": "Round-7 student-error mutant. The symmetry check is skipped for a two-position covariance, so an asymmetric 2 x 2 matrix is read without an error.",
                "killed_by": "test_covariance_must_be_symmetric[gaussian-None-skew0] (seed 0)"})
mutants.append({"id": "r7_03_one_position_pivot_unchecked",
                "description": "Round-7 student-error mutant. The positive-pivot check is skipped for a one-position covariance, so a zero variance is accepted and gives zero losses.",
                "killed_by": "test_singular_covariance_is_rejected[gaussian-None] (seed 0)"})

notes = [
    "Verdict FAIL: G-15 (surviving mutant r7_01: Student-t family ignores the seed; the page says every run is reproducible from its seed; borderline, flagged) and L-04 (false docstring in the lesson-lab twin and the L10 page code: the t(3) tail formula does not avoid cancellation; measured relative error 1.5e-5 at x = 1e6).",
    "G-08 from round 6 is resolved: r6_03 is killed by the new tiny-variance tests.",
    "Four pre-existing survivors (m11, m17, n02, v4_m02) keep mutate_graders at 82/86. Each is disclosed on project.html:228 and is not counted as new (round-6 ruling). Plan 5.3 and the page should be reconciled by the architect.",
    "Hours and the 131-check count are re-derived. The new card cross-references, numbers and lab-sourced values were checked against lesson text and twin outputs.",
    "Not checked: every line of test_project.py beyond the inserted block and the existing ValueError tests (carried by byte-identity); every card that is unchanged (carried); browser rendering beyond page_smoke; the L10 lesson page itself (outside this slice, only the docstring sentence was checked).",
    "Scratch and outputs: ledgers/M4/scripts/M4-d-r7/ (mutate output, labout, page_smoke, run_mut.sh, alt6 and alt7, build_fragment_r7.py). Scratch copies are under /tmp/M4-d-r7-scratch.",
]

summary = {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows),
           "fail": sum(r["status"] == "FAIL" for r in rows),
           "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in rows),
           "mutants": len(mutants), "mutants_killed": sum(1 for m in mutants if m["killed_by"]),
           "new_mutants_round7": 3, "new_mutants_round7_killed": 2}

fragment = {
    "unit": "M4", "slice": "d", "round": 7,
    "verifier": "independent verifier (Haiku), not a builder of M4",
    "pin": "7aa909e", "base": "44f1eb6 (round 6 fragment /Users/billyribeiro/.fanout/frags/B-M4-d.round6.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyB7-M4-d",
    "scratch": "/tmp/M4-d-r7-scratch",
    "verified_at": "2026-10-29T01:54:11+00:00",
    "verdict": "FAIL",
    "rows": rows, "mutants": mutants,
    "registry_flags": [], "freshness_flags": [],
    "notes": notes, "summary": summary,
}
OUT.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(summary))
