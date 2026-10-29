"""Build ledgers/CS2/CS2-d.json (round 6) from the outputs recorded under this folder. Run with -I."""
import datetime
import json
import pathlib
import re

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB6-CS2-d")
S = "ledgers/CS2/scripts/CS2-d-r6"
PG = "course/modules/CS/CS2/project.html"
GR = "course/modules/CS/CS2/grader"

rows = [
    ("D-01", "Registry citation: the only cited key and its record", f"{PG}:411, references/references.json:5962",
     "PASS", "cormen2022introduction exists in references/references.json (key at line 5962, openlibrary record). The reading-list text at project.html:413 says the record names no page, so no locator is given; the page attributes no step to it."),
    ("D-02", "Lab 1 prose vs its output (lines 55, 145, 389)", f"{PG}:55,145,389; lab-CS2-project-1",
     "PASS", "run_labs CS2 PASS (14/14) and the twin ran under python -I -W error with exit 0. Printed: 'deque operations: 44 for n = 12 values, bound 4n = 48'; the page quotes 44 and 48. Prose 'the value 1 is still in the window at step 12' matches the window at step 12 [1, 47, 61, 35]."),
    ("D-03", "Lab 2 expected output and prose (lines 185-188)", f"{PG}:185-188; lab-CS2-project-2",
     "PASS", "Recomputed by hand: stream offsets 2,5,1,4,9,3,6,0 give mean 1000003.75 and sum of squared deviations 59.5, so sample variance 59.5/7 = 8.5. Lab output: count 8, mean 1000003.750000, sample variance 8.500000. Prediction line 'above or below 10' is answered by 8.5 < 10."),
    ("D-04", "Lab 3 expected output and prose (lines 329-338)", f"{PG}:329-338; lab-CS2-project-3",
     "PASS", "Independent Fraction recomputation (inline Python run in this round): sum 110046.0, exact mean 10004.181818, exact sample variance 8.313636, median target ceil(5.5-1.1)=5, 5th smallest 10003.2, last-4 min 10001.0 max 10006.3. All match the printed block and the prose at line 338 (which says 4.4 and rank 5)."),
    ("D-05", "Named ValueError conditions (1)-(10) each have a test", f"{PG}:209; {GR}/test_project.py:170-183,416-451,639-699,757-763",
     "PASS", "Mapped each of the ten named conditions to its test: (1) test_welford_mean/variance_before_any_value_raises; (2) test_welford_sample_variance_of_one_value_raises; (3) test_welford_nan_update_raises; (4) test_rolling_window_zero/negative/boolean_false_window_raises; (5) test_rolling_nan_push_raises; (6) test_rolling_minimum/maximum_before_push_raises; (7) test_sketch_epsilon_outside_open_interval_raises (incl. nan, inf, -inf) and test_sketch_boolean_epsilon_raises; (8) test_sketch_nan_add_raises; (9) test_sketch_quantile_below_zero/above_one/nan/outside_closed_interval_raises; (10) test_sketch_quantile_on_empty_sketch_raises. must_raise checks ValueError, so the exception type is the one named."),
    ("D-06", "Boundary and denoted-value rules of Constraints (lines 209, 211)", f"{PG}:209,211; {GR}/test_project.py:250-259,338-395,500-622,711-754",
     "PASS", "Each value rule has a test: update/push/add with bool, padded string, string, None (test_welford_bool/padded/wrong_type/none_input, test_rolling_bool/string/none_push/padded_string_value, test_sketch_value_that_denotes..., test_sketch_none_value_is_refused). Window rules: bool, whole float 3.0, string '3', padded ' 3 ', None, 2.5 (test_rolling_*window*). ddof rules: other values refused, '1'/'0'/1.0/0.0 answered or refused, None must raise (test_welford_other_ddof, test_welford_ddof_that_denotes..., test_welford_none_ddof_is_refused)."),
    ("D-07", "Test count 170 on the page (line 211) versus collect-only", f"{PG}:211; ledgers/CS2/scripts/CS2-d-r6/collect_counts_r6.txt",
     "PASS", "pytest --collect-only -q on the reference solution with QF_SEED=0..49: 50 of 50 seeds report 170 checks (file collect_counts_r6.txt, all lines 170). The page's '170 for each of the seeds 0 to 49' is therefore correct."),
    ("D-08", "Rank-target example in Conventions (line 219)", f"{PG}:219; {GR}/test_project.py:850-865",
     "PASS", "Recomputed: exact target ceil(Fraction(0.1)*20 - Fraction(0.05)*20) = 2 (difference 1.000000000000000055...), float target ceil(0.1*20 - 0.05*20) = 1. The page's 'exact target is 2' and 'gives 1 in 64-bit floats' both hold."),
    ("D-09", "Instance docstring counts for the naive formula (instance.py docstring)", f"{GR}/instance.py:1-22; ledgers/CS2/scripts/CS2-d-r6/naive_offset_r6.py",
     "PASS", "Re-derived over seeds 0-49 with the docstring's exact order (s += x, ss += x*x, mean = s/n, (ss - n*mean*mean)/(n-1)) against the Fraction reference under the suite's tolerance: offset 0: 0 of 16 fail; offset 10000: 22 of 23 fail, seed 41 passes; offset 1000000: 11 of 11 fail. Matches the docstring exactly."),
    ("D-10", "Instance ranges claimed on the page (line 198)", f"{PG}:198; {GR}/instance.py:31-48",
     "PASS", "Read make_instance: length randint(20,400); offset choice of 0, 10000, 1000000; decimals choice of 1 or 6; window randint(2,30); epsilon choice of 0.05, 0.1, 0.2; probes = 9 fixed values plus one round(random(),3). Matches the page's Inputs paragraph and the test test_instance_is_valid_and_labelled_simulated."),
    ("D-11", "Reference passes and starter fails the suite", f"{GR}/reference.py, {GR}/starter.py; ledgers/CS2/scripts/CS2-d-r6/starter_run_r6.out.txt",
     "PASS", "run_graders CS2 --seeds 0-49: PASS (reference 50/50). Starter run with QF_SEED=0: exit 1, 508 NotImplementedError lines, so the suite fails on the starter as plan 6.6 requires."),
    ("D-12", "Sketch guarantee on the reference (property check beyond the suite)", f"{GR}/reference.py QuantileSketch; ledgers/CS2/scripts/CS2-d-r6/fuzz_sketch_r6.py",
     "PASS", "Exact-count fuzz of the two rank inequalities: 40,000 probe checks on 2,500 random streams (sizes 1-400, eps 1e-6 to 0.999999, sorted, descending, ties, offsets) and 6,400 more on another seed: 0 violations."),
    ("D-13", "Sketch docstring invariants (reference docstring: sum of g = n; g + delta <= floor(2 eps n) + 1)", f"{GR}/reference.py:QuantileSketch docstring; ledgers/CS2/scripts/CS2-d-r6/invariant_r6.py",
     "PASS", "Checked after every add on 300 streams (47,338 adds): sum(g) == n in all, and g + delta <= floor(2 eps n) + 1 for every tuple in all."),
    ("D-14", "Five alternative correct implementations pass the suite (over-constraint check)", f"{GR}/test_project.py; ledgers/CS2/scripts/CS2-d-r6/alts/",
     "PASS", "Each run with pytest --assert=plain -W error on seeds 0-49, exit 0 on 50 of 50 seeds: alt_2 (Welford (n-1)/n delta-squared M2 form), alt_3 (exact list, two-pass Fraction variance, brute rolling, exact rank target), alt_4 (reference with sketch cap floor(2 eps n) without +1), alt_5 (Fraction-exact Welford state, brute rolling, reference sketch), alt_r6_01 (reference sketch with GK delta lacking the -1). alt_5 imports the sketch from the checkout path of the reference."),
    ("D-15", "Grader mutants: all existing mutants killed, new student-error mutants killed", f"ledgers/CS2/mutants/; ledgers/CS2/scripts/CS2-d-r6/mutate_final_r6.out.txt",
     "PASS", "tools/mutate_graders.py --unit CS2 --seeds 0-9: PASS, 83/83 killed. The 79 prior mutants were all re-run and killed. New: r6_02 (population divisor at n=2), r6_03 (rank target adds the slack), r6_04 (compression cap 4 eps n), r6_05 (minimum deque expires one push late), each killed by a named test. Also tried r6_01 (GK insertion delta without the -1): it survived, but it keeps the guarantee on 40,000 + 6,400 checks and on 50 seeds, so it is a correct alternative (alt_r6_01), not a student error; it was moved out of mutants."),
    ("D-16", "Ruff and mypy on the project files", f"tests/labs/CS2, {GR}",
     "PASS", "ruff check: All checks passed. ruff format --check: 18 files already formatted. mypy --no-incremental on tests/labs/CS2 and grader: Success, no issues in 18 source files."),
    ("D-17", "Project labs: run and twin under -I -W error, page code equals twin, expected equals output", "tests/labs/CS2/lab-CS2-project-1..3.py; course/modules/CS/CS2/project.html",
     "PASS", "run_labs CS2 PASS (14/14, including the three project labs). Each twin exits 0 under python -I -W error with no stderr."),
    ("D-18", "check_pages, check_projects, check_dag, page_smoke for the project page", f"{PG}; tools/check_*.py",
     "PASS", "check_projects CS2 PASS; check_pages CS2 PASS; check_dag CS2 PASS; page_smoke CS2 PASS (ledgers/CS2/scripts/CS2-d-r6/page_smoke_project_r6.out.txt). The page_smoke run was headless Chromium on the local server."),
    ("D-19", "Hours arithmetic: rung table sums to hub split", f"{PG}:33, 233-241; course/modules/CS/CS2/index.html (data-hours-lessons)",
     "PASS", "Table: 2+3+4+4+4+6+4+3 = 30 = data-hours-project=30 (project.html:33 and index.html). Hub lessons data-hours-lessons=100, so the unit total is 130 as the page says."),
    ("D-20", "Rubric structure and exemplar scores (lines 348-391)", f"{PG}:348-391",
     "PASS", "Six criteria C1-C6, four levels each (rubric table). Exemplar A data-scores 1,1,2,1,1,1 match its official-scoring line; Exemplar B data-scores 4,4,4,4,4,4 match. Exemplar B proof algebra checked by hand: M_{n+1} = M_n + n d^2/(n+1), d = x_{n+1} - m_n, with the cross term zero by the definition of m_n. check_projects enforces 4-7 criteria and exemplars at two levels."),
    ("D-21", "Exemplar B numeric claims", f"{PG}:383-390",
     "PASS", "Lab 3 numbers 8.313636 and the True agreement (lab output); Lab 1 44 operations against 4n = 48 (lab output); the ten probes = 0, 0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 1 plus one seeded value (instance.py PROBES_FIXED and round(rng.random(),3)); streams of one to eight values and epsilon 0.05/0.1/0.2 (test_sketch_rank_guarantee_on_short_streams)."),
    ("D-22", "Notation: symbols on the project page vs notation/notation.json", f"{PG}:198, 218, 376-390; notation/notation.json",
     "PASS", "The registry holds T, Phi and Phi^{-1}, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q. The page uses n, q, v, x_i, m_n, M_n, delta, epsilon, sums and fractions; none is a registered symbol, so no registry conflict. Standard KaTeX commands only."),
    ("D-23", "Terms and symbols defined before use: epsilon in the rank guarantee", f"{PG}:198, 209, 218",
     "FAIL", "Conventions bullet 'The rank guarantee' (line 218) states '<em>qn</em> + <em>εn</em>' and '<em>qn</em> − <em>εn</em>' without saying that ε is the sketch's epsilon. The name epsilon is introduced in Inputs (line 198) and Constraints (line 209), but the symbol is never bound in the statement of the guarantee. The guarantee is the one thing the suite tests, so the binding should be explicit."),
    ("D-24", "Placement and Rung 3 cross-links", f"{PG}:42, 161 (index.html:161, 69-71)",
     "PASS", "index.html line 71 and line 161 both state that a skip needs the placement bar and both skill checks; project.html line 42 says the same."),
    ("D-25", "Tooling claims on the page: Python 3.14 and pytest 9.0.2; code saved in the browser", f"{PG}:249, 257; course/assets/js/grader.js:33-79; course/assets/vendor/pyodide/pyodide-lock.json; requirements-dev.txt:2",
     "PASS", "requirements-dev.txt pins pytest==9.0.2; the vendored Pyodide lock records pytest 9.0.2; local Python 3.14.8. grader.js saves the draft with store.put (400 ms debounce). Read statically; the in-browser Pyodide run itself was not executed (see notes)."),
    ("D-26", "Footer claim: nothing you write leaves the browser", f"{PG}:426; course/assets/js/grader.js:18, py-worker.js:148-150",
     "PASS", "Static reading: grader.js fetch() only loads the grader's own files (text(url) helper); py-worker.js communicates by postMessage only, and no network call is made from the worker. The live browser network trace was not captured in this round."),
    ("D-27", "Cards: structure, ids, grades, lesson coverage", "course/modules/CS/CS2/cards.json (167 cards)",
     "PASS", "167 cards; ids CS2-c001..CS2-c167 contiguous and unique; no duplicate front or back; grades T 129, C 38; every C card has basis and every T card has none; every lesson L01-L11 has at least one card (counts L01-L11: 13,17,15,16,15,14,18,18,12,13,16)."),
    ("D-28", "Cards: C-grade numbers against the printed lab output", "course/modules/CS/CS2/cards.json; lesson expected blocks (run_labs CS2 PASS)",
     "PASS", "Checked against printed lab output: c009, c022, c023, c024, c025, c035, c038, c039, c053, c065, c066, c068, c075, c079, c080, c097, c098, c099, c113 (re-ran the L08 Part C stream: 185 created, 177 removed, 8 levels, 10 orders), c115, c123-c126, c136, c138, c150, c154, c155, c157, c158, c159, c162, c163, c164, c165, c166. Derived figures in c126 (7.87, 1.60e8, 1.34e7) and c151 (198430, 18213) recomputed by hand. All agree."),
    ("D-29", "Cards: T-grade cards agree with the current lesson text and carry their hypotheses", "course/modules/CS/CS2/cards.json (129 T cards)",
     "UNVERIFIABLE", "Only spot-checked. Arithmetic re-derived for c044-c048, c059, c061, c069, c088, c089, c094, c095, c122, c127, c144, c151, c165 and the L10 window and deque claims c128-c137; c129 and c130 read against the L10 Definition 2.1 and Theorem 2.2 text. The other T cards were not read against their lesson's definition, proposition and hypotheses. Fix: read all 129 T cards against their lesson text (Definition/Proposition/Lemma numbers and hypotheses) in the next round."),
]

mutants = []
pat = re.compile(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$")
for line in (ROOT / S / "mutate_final_r6.out.txt").read_text(encoding="utf-8").splitlines():
    m = pat.match(line)
    if m:
        status, fname, desc, killer = m.groups()
        mutants.append({
            "id": fname.removesuffix(".py"),
            "description": desc.strip(),
            "killed_by": killer.strip() if status == "KILLED" else "",
        })

out_rows = []
for rid, check, location, status, evidence in rows:
    row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = {
            "D-23": "Add to the Conventions bullet at project.html:218 a clause such as 'where ε is the epsilon of the sketch, as in Inputs'.",
            "D-29": "Read all 129 T cards in cards.json against their lesson's Definition/Proposition/Lemma text and hypotheses; fix any card that drifts from the lesson.",
        }[rid]
    out_rows.append(row)

counts = {s: sum(1 for r in out_rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
verdict = "PASS" if counts["PASS"] == len(out_rows) else "FAIL"
fragment = {
    "unit": "CS2",
    "slice": "d",
    "round": 6,
    "verifier": "Haiku 5.5 (claude-haiku-5-5), independent verifier, round 6",
    "pin": "44f1eb6a417ce687a9b88c7ee917e72566b29892",
    "base": "none: no round-5 fragment exists at /Users/billyribeiro/.fanout/frags/B-CS2-d.round5.json; the round-5 scripts under ledgers/CS2/scripts/CS2-d-r5 were read for method only",
    "checkout": str(ROOT),
    "scratch": str(ROOT / S),
    "verified_at": datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": out_rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Round 6 slice d: project.html (rubric, exemplars, spec), grader (instance, reference, starter, test_project), project labs 1-3, cards.json (167 cards), grader mutants. Verified on pin 44f1eb6.",
        "Not checked: the in-browser Pyodide run and a live network trace (page_smoke ran headless on the local server); the full T-card proof-to-lesson agreement (row D-29); the C cards not listed in D-28.",
        "Mutants: ledgers/CS2/mutants holds 83 files, all killed. ledgers/CS2/mutants has no survivor; the surviving candidate r6_01 was re-classed as a correct alternative and placed under ledgers/CS2/scripts/CS2-d-r6/alts/.",
        "The fifth alternative (alt_5) imports the reference sketch from the checkout path, so it is reproducible only in this checkout.",
    ],
    "summary": f"{counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE of {len(out_rows)} rows; {len(mutants)} grader mutants, {sum(1 for m in mutants if m['killed_by'])} killed.",
}
path = ROOT / "ledgers/CS2/CS2-d.json"
path.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", path, fragment["summary"], "verdict", verdict)
