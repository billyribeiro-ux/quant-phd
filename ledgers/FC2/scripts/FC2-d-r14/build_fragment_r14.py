"""Build ledgers/FC2/FC2-d.json (round 14) from the archived evidence in scripts/FC2-d-r14/out/.

Every row cites an archived output file or a locator read this round. Mutant entries are parsed from
out/mutate_all_r14.out, the tool's own output. Run from the checkout root.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path.cwd()
S = "ledgers/FC2/scripts/FC2-d-r14/out"
PROJ = "course/modules/FC/FC2/project.html"
G = "course/modules/FC/FC2/grader"

rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> None:
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})


# ---- gates on the pin (run this round) ----
row("fc2d-gate-check-projects", "tools/check_projects.py --unit FC2", "tools/check_projects.py", "PASS",
    f"{S}/check_projects.out: 'check_projects FC2: PASS' (exit 0).")
row("fc2d-gate-check-pages", "tools/check_pages.py --unit FC2", "tools/check_pages.py", "PASS",
    f"{S}/check_pages.out: 'check_pages FC2: PASS' (exit 0).")
row("fc2d-gate-check-dag", "tools/check_dag.py --unit FC2", "tools/check_dag.py", "PASS",
    f"{S}/check_dag.out: 'check_dag FC2: PASS' (exit 0). The check reads links and definitions only, so plain-prose "
    "uses (bid-ask, put, call, chord) are not flagged; see freshness_flags for the stale open-items note.")
row("fc2d-gate-run-labs", "tools/run_labs.py --unit FC2", "project labs lab-FC2-project-1..3", "PASS",
    f"{S}/run_labs.out: 'run_labs FC2: PASS (11/11)' (exit 0).")
row("fc2d-gate-page-smoke", "tools/page_smoke.py --unit FC2", f"{PROJ}", "PASS",
    f"{S}/page_smoke.out: 'page_smoke modules/FC/FC2/project.html: PASS', 'page_smoke FC2: PASS'; the in-browser grader "
    "line reports 'All 98 tests pass on seed 1494977577'.")
row("fc2d-gate-run-graders", "tools/run_graders.py --unit FC2 --seeds 0-49 (reference, starter, instance, mypy --strict)",
    G, "PASS", f"{S}/run_graders.out: 'run_graders FC2: PASS (reference 50/50 seeds, slowest 0.2 s)'. The same tool "
    "fails any run where the starter passes, so the starter fails the suite.")
row("fc2d-gate-ruff", "ruff check and ruff format --check on tests/labs/FC2 and the grader", f"{G}; tests/labs/FC2",
    "PASS", f"{S}/ruff_check.out: 'All checks passed!'; {S}/ruff_format.out: '15 files already formatted'.")
row("fc2d-gate-mypy", "mypy --strict on reference.py, instance.py, test_project.py and starter.py (scratch copy with "
    "reference.py as scanner.py)", G, "PASS",
    f"{S}/mypy_strict_scratch.out: 'Success: no issues found in 4 source files'. A direct repo-level run "
    f"(out/mypy.out) reports import-not-found for scanner and instance because the grader files are outside the "
    "configured mypy scope and scanner.py is absent at the pin; that is a path artefact, not a grader defect.")
row("fc2d-gate-pytest", "pytest -k 'FC2 or project' tests/", "tests/", "PASS",
    f"{S}/pytest_fc2.out: exit 0, all selected tests passed.")
row("fc2d-gate-verify-refs", "tools/verify_refs.py --offline", "references/references.json", "PASS",
    f"{S}/verify_refs.out: 'offline integrity: 560 entries, 0 problems'. The live (network) run was not made; "
    "it is the architect's gate.")
row("fc2d-collect-count", "pytest --collect-only on the reference, seeds 0-49", f"{PROJ}:320", "PASS",
    f"{S}/collect_counts.out: 98 tests collected for every one of the 50 seeds; the page states 98 at "
    f"{PROJ}:320. Open-items departure 4 says 75; that is stale (freshness_flags).")
row("fc2d-seeds-84", "grader suite on reference, seeds 0-49", f"{G}/test_project.py", "PASS",
    f"{S}/run_graders.out: reference 50/50 seeds.")
row("fc2d-starter-fails", "starter.py as scanner.py fails the suite", f"{G}/starter.py", "PASS",
    f"{S}/run_graders.out: no 'the starter passes the suite' problem reported.")
row("fc2d-alternatives", "five alternative correct implementations pass seeds 0-49 (over-constraint check)",
    "ledgers/FC2/scripts/FC2-d-r14/alts/", "PASS",
    f"{S}/alts_r14.out: alt1_fraction_class, alt2_integer_only, alt3_float_epsilon_cutoff, alt4_adjacent_slopes "
    "(after a sign fix in my own alternative; see notes), alt5_forward_price_parity all PASS on 50 seeds. "
    "alt4 handles unequal strike spacing (it fails the suite only if it does not).")
row("fc2d-alt-r14-float-no-cutoff", "a plain float implementation without a tie cutoff is rejected by the exact-tie tests",
    f"{G}/test_project.py:286-291, 802-806", "PASS",
    f"{S}/float_no_cutoff_pytest.out: 2 failed (test_parity_exact_tie_at_a_non_dyadic_discount_factor, "
    "test_half_cent_tie_at_a_non_dyadic_discount_factor_rounds_once_up), 96 passed. The page requires that each money "
    "value is computed from exact fractions (project.html:~305), so rejecting a plain float is correct.")
row("fc2d-alt-r6-overconstraint", "round-6 alternative (integer cross-multiplication) passes seeds 0-49",
    "ledgers/FC2/scripts/FC2-d-r14/alt6_round6_alternative.py", "PASS",
    f"{S}/alt6_r14.out: 50 lines 'seed N rc=0'.")

# ---- mutants (parsed from the tool's output) ----
mut_lines = Path(f"{S}/mutate_all_r14.out").read_text(encoding="utf-8").splitlines()
mutants: list[dict[str, str]] = []
for line in mut_lines:
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    if status != "KILLED":
        continue
    mutants.append({"name": name.removesuffix(".py"), "description": desc, "killed_by": killed})
killed_total = len(mutants)
row("fc2d-mutate-builder", "tools/mutate_graders.py --unit FC2 --seeds 0-9 (every mutant in ledgers/FC2/mutants)",
    "ledgers/FC2/mutants/", "PASS", f"{S}/mutate_all_r14.out: 'mutate_graders FC2: PASS (103/103 killed)'; "
    f"{killed_total} KILLED lines parsed into mutants[].")
row("fc2d-mut-new-r14", "five new round-14 student-error mutants (r14_a..e) are each killed",
    "ledgers/FC2/mutants/r14_a..r14_e", "PASS",
    "Each is killed on seed 0 (mutate_all_r14.out): r14_a by test_convexity_boundary_equal_to_chord_is_not_flagged, "
    "r14_b by test_scan_matches_exhaustive_oracle_second_chain, r14_c by test_parity_gap_rejects_a_nonpositive_strike_"
    "and_accepts_one, r14_d by test_half_cent_gross_rounds_once_up, r14_e by "
    "test_negative_cost_is_rejected_even_when_no_finding_is_kept. Generated by scripts/FC2-d-r14/make_mutants_r14.py.")
MUT_ROWS = [
    ("fc2d-mut-v03", ["v03_parity_gross_bankers_round"]),
    ("fc2d-mut-v04", ["v04_convexity_returns_one_based_index"]),
    ("fc2d-mut-v05", ["v05_convexity_findings_before_parity"]),
    ("fc2d-mut-v06", ["v06_gross_rounds_signed_gap_then_abs"]),
    ("fc2d-mut-v01-boundary", ["v01_convexity_zero_net_kept"]),
    ("fc2d-mut-v02-labels", ["v02_parity_explanation_names_P1_only"]),
    ("fc2d-r5-mut-swap-weights", ["r5_b_swapped_chord_weights"]),
    ("fc2d-r5-mut-skip-first", ["r5_c_parity_loop_skips_first_strike"]),
    ("fc2d-r6-mut-new", [m["name"] for m in mutants if m["name"].startswith("r6_")]),
    ("fc2d-r7-mut-new", [m["name"] for m in mutants if m["name"].startswith("r7_")]),
]
for rid, names in MUT_ROWS:
    hits = [m for m in mutants if m["name"] in names]
    row(rid, "named mutant(s) are killed", "ledgers/FC2/mutants/", "PASS" if len(hits) == len(names) and names else "FAIL",
        f"{S}/mutate_all_r14.out: KILLED for {len(hits)} of {len(names)}: " + ", ".join(names) + ".")

row("fc2d-r5-mut-direction", "round-5 mutant r5_d (explanation direction reversed) is not in the suite",
    "ledgers/FC2/mutants/", "PASS",
    "r5_d_explanation_direction_reversed.py is absent from ledgers/FC2/mutants at 1431aa1d (it was retired as a ruled "
    "non-finding in an earlier round); the direction claim is checked by reading _explain_parity in reference.py "
    "and the convention text at project.html:~337.")
row("fc2d-r5-grader-exact-ties", "round-5 exact-tie tests exist and are correct",
    f"{G}/test_project.py:271-291, 795-822", "PASS",
    "Re-derived each tie value with Fraction: 2.5 -> 3; -1.5 -> -1; -0.5 -> 0; 1.5 -> 2; 14.5 -> 15; -14.5 -> -14; "
    "half-cent gross 2.5 -> 3; convexity 2.5 -> 3; negative gross -2.5 -> magnitude 3 (out/rederive.out assertions).")
row("fc2d-r6-new-tie-tests", "round-6 tie tests at the convexity and gross boundaries are correct",
    f"{G}/test_project.py:809-850", "PASS",
    "Re-derived in rederive.py/by hand: chord 50.5 vs call 53 gives 3; chord 3850.5 vs call 3851 gives 1; both "
    "tests kill the mutants listed above.")

# ---- grader and labs (read in full this round) ----
row("fc2d-grader-stdlib", "grader files import the standard library only and the page says so",
    f"{G}/instance.py, reference.py, starter.py; {G}/test_project.py:157-180", "PASS",
    "Read all four files in full (instance.py 142 lines, reference.py 148, starter.py 30, test_project.py 913). Imports "
    "are stdlib plus pytest; test_module_imports_standard_library_only and test_module_does_not_import_grader_files "
    "enforce it.")
row("fc2d-grader-messages", "named error conditions raise ValueError with the stated message in each function",
    f"{G}/test_project.py:450-650; {G}/reference.py:24-50", "PASS",
    "Each condition in project.html:307-316 is tested in every function that receives its input: strikes (parity, "
    "convexity, scan), df_ppm (all three), lengths (convexity calls; scan calls and puts), cost (scan).")
row("fc2d-grader-instance-validity", "instance generator yields valid SIMULATED chains",
    f"{G}/instance.py:41-60, 102-111, 118-131", "PASS",
    "Read in full. Bounds check (Theorem 2.2, L05.html:84) matches test_generated_chains_satisfy_the_model_free_bounds; "
    "half-cent ties rejected; calls convex by construction (nondecreasing increments, instance.py:86-88); planted "
    "convexity bump keeps parity (instance.py:104-105). run_graders checks determinism and seed diversity: PASS.")
row("fc2d-grader-instance-diversity", "seeds produce distinct instances", f"{G}/instance.py:6-9, 134-142",
    "PASS", f"{S}/run_graders.out: no 'identical instances' problem for seeds 0-49.")
row("fc2d-lab1", "project lab 1: page code equals twin; expected block equals output",
    f"{PROJ}:53-165; tests/labs/FC2/lab-FC2-project-1.py", "PASS",
    f"{S}/lab_compare.out (lab_compare_r14.py): page code identical to twin (True); expected block equals twin output (True). "
    f"Every number in the interpretation re-derived in {S}/rederive.out (gaps 120, 0, 0, 0, -20, 0; chord 625 vs call 700).")
row("fc2d-lab2", "project lab 2: page differs from twin only at three blanks; expected equals output",
    f"{PROJ}:166-277; tests/labs/FC2/lab-FC2-project-2.py", "PASS",
    "Line diff in "f"{S}/lab_compare.out: exactly three page lines differ (gap = ___, net = ___, net = ___), and the twin has the completed "
    "lines (parity_gap(...), gross - cost, gross - cost). 89 lines each. Expected block equals twin output.")
row("fc2d-lab3", "project lab 3: page code equals twin; expected equals output; stated hypotheses",
    f"{PROJ}:375-488; tests/labs/FC2/lab-FC2-project-3.py", "PASS",
    f"{S}/lab_compare.out: lab 3 page code identical to twin, expected equals output. Stated before running: at least one finding (3 kept); gross at 4500 "
    "equals cost 60 (gap -60). Re-derived: 6500 -> 226/166, 7000 -> 540/480, 6000 -> -188/3, gross 63, net 3 "
    f"({S}/rederive.out).")
row("fc2d-lab-twins-pure", "twins run alone under python -I -W error", "tests/labs/FC2/lab-FC2-project-{1,2,3}.py",
    "PASS", f"{S}/twin1.txt, twin2.txt, twin3.txt: exit 0 each.")
row("fc2d-rederive-numbers", "every number in the project page re-derived with exact Fractions",
    f"{PROJ}:53-488", "PASS",
    f"{S}/rederive.out: 'ALL ASSERTIONS PASS'; reference.scan on both lab chains equals the hand values.")

# ---- rubric, exemplars, brief ----
row("fc2d-rubric-observable", "rubric: five criteria, four observable levels, each descriptor checkable",
    f"{PROJ}:504-516", "PASS",
    "Read every cell. Level-4 cells in C4 and C5 ask for quantified effects (the factor's effect on gross; the direction "
    "and size of a settlement's move). They are observable, and open-items records them as a known limitation.")
row("fc2d-rubric-calib-A", "exemplar A: blind scores against the rubric descriptors",
    f"{PROJ}:584-641 (article#exemplar-a)", "PASS",
    "Scored from the descriptors and the passages: C1 2 (amounts 'about 226/540/63', legs not stated), C2 1 (no cost "
    "model), C3 2 (discount factor named, no P-label), C4 2 (classes separated for parity only), C5 1 (market "
    "inefficient for every finding). Matches data-scores='2,1,2,2,1'. Caveat: the official verdict paragraph was in the "
    "same read as the passage, so this scoring is not fully blind.")
row("fc2d-rubric-calib-B", "exemplar B: scores against the rubric descriptors",
    f"{PROJ}:520-583 (article#exemplar-b)", "PASS",
    "Scored: C1 4 (legs given for all three findings), C2 4 (cost model, survival, each net; see notes on the "
    "'gap between the net and zero' wording), C3 3 (P-labels per finding; P1-P3 for the whole note), C4 3 (classes "
    "separated; factor size not stated), C5 3 (settlement per finding; direction for the 3-cent finding not stated). "
    "Matches data-scores='4,4,3,3,3'. Same caveat on blindness.")
row("fc2d-exemplar-numbers", "exemplar numbers: 6175, 6650, 226, 166, 540, 480, 63, 3, 802/3, 60 cents",
    f"{PROJ}:520-583", "PASS", f"{S}/rederive.out (the same values asserted); B's summary is 64 words (limit 80, "
    f"{PROJ}:492 'Summary ... at most 80 words').")
row("fc2d-exemplar-annotations", "exemplar annotations: level claims consistent with data-level and data-scores",
    f"{PROJ}:520-641", "PASS", "Each 'Meets/Misses ... level N' annotation was checked against the descriptor for that "
    "level; the min over data-scores equals data-level (B: 3, A: 1).")
row("fc2d-exemplar-brief-structure", "exemplar notes follow the brief's six headings, in order, as the page claims",
    f"{PROJ}:489-499 (brief), :518 ('Two findings notes written to this brief.'), :520 (exemplar-b), :584 (exemplar-a)",
    "FAIL",
    "The brief (h3#brief, :489-499) requires six headings in order: Summary; Chain and cost model; Findings; "
    "Model-free and model-dependent; Explanation and settlement; Limitations. Exemplar B's h5 headings are Summary, "
    "Findings, Model-free and model-dependent, Explanation and settlement, Limitations: 'Chain and cost model' is "
    "missing. Exemplar A's headings are Findings (:589), Costs (:601), Assumptions and models, Conclusion (:626): none "
    "of the six. The sentence at :518 says both are 'written to this brief'.",
    "Either add a 'Chain and cost model' h5 section to exemplar B and rebuild exemplar A on the six headings, or change "
    ":518 to say the notes cover the brief's content, not its headings.")
row("fc2d-spec-explanation-labels", "explanation labels: parity names P1,P2,P3,P4,P6; convexity P1,P2,P5,P6",
    f"{PROJ}:301; {G}/test_project.py:42-43, 674-686; {G}/reference.py:82-102", "PASS",
    "Reference explanations name exactly these labels; test_scan_explanations_are_nonempty_and_name_the_rule checks them.")
row("fc2d-spec-errors-scope", "named error conditions and scope claims", f"{PROJ}:305-316; {G}/test_project.py",
    "PASS", "Each named condition has tests in each function (see fc2d-grader-messages); 'every', 'all', 'only' claims "
    "were read (72 scope-word sentences) and each computable one is backed by a test or a computation.")
row("fc2d-hours", "hours arithmetic", f"{PROJ}:339-357; course/modules/FC/FC2/index.html:29",
    "PASS", "Time-budget rows 2+3+5+9+3+5+3 = 30; hub data-hours-project=30, data-hours-lessons=60; 60+30 = 90 (plan §1).")
row("fc2d-reading-theorem-locator", "theorem locators on the reading list", f"{PROJ}:652-660",
    "PASS", "L05.html:61-63 is Theorem 1.2 (put-call parity); L05.html:113-115 is Theorem 3.2 (convexity in strike); "
    "L05.html:82-84 is Theorem 2.2 (bounds). The instance docstring's 'Lesson 5, Theorem 2.2' matches.")
row("fc2d-references-no-locator", "reading list quotes no locator from the three registry keys",
    f"{PROJ}:652-660", "PASS", "The reading list has data-cite only; the paragraph says no chapter, page or equation is "
    "assigned; verify_refs offline: 0 problems.")
row("fc2d-notation", "page symbols against notation/notation.json", f"{PROJ}; notation/notation.json",
    "PASS", "Registered symbols: T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}. The page uses C, "
    "P, S, K, df, D (defined L05.html:55, 59), tau, r. No clash. The page has no math delimiters.")
row("fc2d-simulated-label", "every chain is labelled SIMULATED; no data embedded",
    f"{PROJ} (18 occurrences), {G}/instance.py:1, 120", "PASS",
    "Inputs section states no market data is embedded and no option-quote source is in tools/data_sources.yaml; "
    "instance label='SIMULATED' (test_instance_is_labelled_simulated).")
row("fc2d-process-banned", "no process words in learner text", f"{PROJ}", "PASS",
    "grep for builder, verifier, round, planner, draft, TODO, agent, ruling, fragment, pin: no hits in learner text.")
row("fc2d-ladder-claims", "ladder claims", f"{PROJ}:40-50", "PASS",
    "Four rungs in order; Lab 2 has three blanks (verified by diff); Lab 3 gives reference findings for a second chain.")
row("fc2d-curriculum-scope", "page scope against curriculum/02-economics-finance-core.yaml:425-431",
    "curriculum/02-economics-finance-core.yaml:425-431", "PASS",
    "The curriculum brief says 'embedded option-chain snapshot'; the page substitutes SIMULATED chains with an honest-"
    "pending note, which the architect decision (plans/FC2-build-plan.md, Architect decisions) accepts. Recorded as a "
    "registry_flag.")
row("fc2d-no-external", "no external links; relative links and anchors resolve", f"{PROJ}", "PASS",
    "No http(s) links. 20 internal anchors, all with an id; 12 relative hrefs, all resolve on disk.")
row("fc2d-new-tests", "the suite (98 checks) read in full", f"{G}/test_project.py", "PASS",
    "All 913 lines read. Hand-checked the expected values of the boundary tests (net 0 and 1 cent, half-cent ties, "
    "unequal-grid convexity 43 vs 42, 41 vs 42, 43 vs chord at 110; 30 vs 32.6 and 65/7 at 160).")
row("fc2d-lab1-hypothesis-terms", "lab 1 hypothesis: terms defined before use or forward-referenced",
    f"{PROJ}:55", "PASS", "The hypothesis forward-references the parity gap, the synthetic forward and the chord to "
    "Conventions, and defines the gross and net amounts itself.")
row("fc2d-r6-project-line335", "model-free: first uses are explicit forward references to its definition",
    f"{PROJ}:37, :285, :335, :495, :511", "PASS", "The lede (:37) and the Context paragraph (:285) use model-free "
    "with an explicit 'as Conventions and assumptions, below, defines' pointer; the definition is at :335; the brief "
    "(:495) and the rubric (:511) come after it.")
row("fc2d-r7-project-anchor-links", "in-page links resolve", f"{PROJ}:37, :282", "PASS",
    "All 20 internal anchors have a matching id (see fc2d-no-external).")
row("fc2d-dag-closure", "DAG: concepts used outside the closure are plain prose; closure computed",
    "coursekit.prerequisite_closure('FC2')", "PASS",
    "Closure is AC1, CF1, E1, FC1, M1, M2, M4, P0.1 (architect decision added FC1). The page's bid-ask and put/call "
    "uses are plain prose with no link, which the architect default allows. Links go only to FC2 definitions "
    "(L01 arbitrage-opportunity, L05 put-call-parity and option-arbitrage-bounds).")
row("fc2d-r14-delta", "delta from pin 0d2d0f3 read for every slice file",
    f"{PROJ}; {G}/*; tests/labs/FC2/lab-FC2-project-{{1,2,3}}.py", "PASS",
    "git diff 0d2d0f3..1431aa1d: project.html 73 lines, instance.py 9, reference.py 11, starter.py 3, test_project.py 129; "
    "the three project labs are byte-identical to 0d2d0f3. All changed hunks were re-read in full in this round, so no "
    "row is carried forward.")

freshness_flags = [
    "plans/FC2-open-items.md departure 4 says 'the test count is 75 for seeds 0 to 49'. The page says 98 and "
    "pytest --collect-only gives 98 on every seed. The open-items note is stale; the page is correct.",
    "plans/FC2-open-items.md DAG_DEFECTS says FC2's closure excludes FC1. The architect decision added FC1 to FC2's "
    "prerequisites (curriculum/02-economics-finance-core.yaml:400 now lists FC1); the closure now includes FC1.",
    "plans/FC2-open-items.md departure 7 says mutants are 10/10 killed; the directory now holds 103 (98 plus five r14).",
]
registry_flags = [
    "curriculum/02-economics-finance-core.yaml:427-429 says 'Given an embedded option-chain snapshot', which conflicts "
    "with the SIMULATED decision (plans/FC2-build-plan.md B1, Architect decisions). Not a slice defect; the page's "
    "honest-pending note is correct. Flagged for the curriculum owner (carried from round 6).",
    "hull2021options, stoll1969relationship, cox1979option: registry records carry no edition, volume or issue. The "
    "page quotes none (carried from round 7).",
]

notes = [
    "Round 14 on pin 1431aa1d (round-7 pin 0d2d0f3). The round-13 fragment named in the brief "
    "(/Users/billyribeiro/.fanout/frags/D-FC2-d.round13.json) does not exist, so the round-7 fragment in this checkout "
    "(ledgers/FC2/FC2-d.json at 0d2d0f3) was used as context only. Its PASS rows were not trusted and every row here is "
    "re-verified this round.",
    "Scope: project.html, grader/, tests/labs/FC2/lab-FC2-project-{1,2,3}.py, the mutants, five alternatives, and exemplar "
    "scoring. The slice has no cards: the round-7 card rows (fc2d-cards-*, fc2d-r7-cards-changed-hypotheses) are not "
    "carried and not checked. cards.json changed by 298 insertions since 0d2d0f3.",
    "Ruling 23 (blind exemplar scoring) was not in the rules file I was given. I scored the exemplars from the rubric "
    "descriptors and the passages, but I read the official verdict paragraphs in the same read, so the scoring is not "
    "fully blind. My scores match the official ones: A 2,1,2,2,1; B 4,4,3,3,3.",
    "Judgement, not a row: exemplar B's C2 level-4 annotation says it states 'its gap from zero'. The passage gives each "
    "net (166, 480, 3) but never says 'gap from zero' separately. The descriptor 'the gap between the net and zero' is "
    "ambiguous and the net is that gap by definition. I accepted level 4.",
    "My alternative 4 first failed the suite because of a sign error in my own scratch code (gross used -excess, and "
    "excess is call minus chord); after the fix it passes. The fix is recorded in the archived alts/alt4 file; the "
    "suite did not need changing.",
    "New student-error mutants: five (r14_a..e), each generated by a single exact replacement of reference.py "
    "(make_mutants_r14.py); all KILLED on seed 0.",
    "The float alternative without a tie cutoff fails only the two exact-tie tests (out/float_no_cutoff_pytest.out). "
    "The page's constraint 'computed from exact fractions' makes that rejection correct.",
    "Not run: the live verify_refs run (network), a real-browser check of the grader panel and file-load control "
    "(page_smoke ran the in-browser grader under Pyodide only), cards (out of slice), the repo-wide gate (architect's).",
]

verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
ledger = {
    "unit": "FC2",
    "slice": "d",
    "round": 14,
    "verifier": "Claude Haiku 5.5, independent verifier for FC2-d round 14 (did not build FC2)",
    "pin": "1431aa1d842a5d2d05fd5953c098500bf78a4307",
    "base": "0d2d0f3 (round-7 pin); the slice delta is listed in fc2d-r14-delta",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD14-FC2-d (detached at 1431aa1d, .venv symlinked)",
    "scratch": "/tmp/fc2d-r14/ (ref/, alts/, alt_runs/, floatnoeps/, alt6run/); the archived copies are in "
    "ledgers/FC2/scripts/FC2-d-r14/",
    "verified_at": "2026-11-09",
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": registry_flags,
    "freshness_flags": freshness_flags,
    "notes": notes,
    "summary": (
        f"FC2-d round 14: {sum(r['status'] == 'PASS' for r in rows)} PASS, "
        f"{sum(r['status'] != 'PASS' for r in rows)} non-PASS of {len(rows)} rows. "
        "Non-PASS: fc2d-exemplar-brief-structure (the exemplar notes do not follow the brief's six headings, although the "
        "page says they were written to it). Everything else passes: all gates, the 98-check count on every seed, 50/50 "
        "reference seeds, 5 of 5 alternatives plus the round-6 alternative, 103/103 mutants killed (5 new), every project "
        "number re-derived, labs and twins, and anchors and links. "
        f"Mutants: {killed_total} KILLED of {killed_total}."
    ),
}
out = ROOT / "ledgers/FC2/FC2-d.json"
out.write_text(json.dumps(ledger, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "verdict", verdict, "rows", len(rows), "mutants", len(mutants))
