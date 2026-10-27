# Builds the round-34 S7 project fragment from the round-33 ledger plus this round's evidence (scratch; not in the checkout).
import json, re, subprocess, datetime, sys
CK = "/tmp/verify-s7-r2-p"
LOG = "/tmp/ap1-r5/s7p-r2/logs"
prev = json.load(open("/tmp/ap1-r5/s7p-r2/prev_project.json"))
BASE, HEAD = "45548c1", "edf95c4"
RUN = "Round 34 re-run at edf95c4 (Python 3.14.8, numpy 2.4.6, scipy 1.18.0, pytest 9.0.2)"
PREFIX = "Carried from round 33"

def quiet(paths):
    rc = subprocess.run(["git", "-C", CK, "diff", "--quiet", BASE, HEAD, "--", *paths]).returncode
    return rc == 0

GROUPS = {  # name -> paths; each proven byte-identical below before use
    "course/modules/S/S7": ["course/modules/S/S7"],
    "tests/labs/S7": ["tests/labs/S7"],
    "ledgers/S7/mutants": ["ledgers/S7/mutants"],
    "tools": ["tools"],
    "tests": ["tests"],
    "references": ["references", "course/assets/data/references.json"],
    "curriculum": ["curriculum", "CURRICULUM.md", "course/assets/data/program.json"],
    "notation": ["notation", "course/assets/data/notation.json"],
    "glossary": ["course/assets/data/glossary.json"],
    "benchmarks": ["benchmarks"],
    "course/assets": ["course/assets"],
    "requirements/pyproject": ["requirements.txt", "requirements-dev.txt", "pyproject.toml"],
    "VERIFIER_RULES/BUILDER_RULES": ["VERIFIER_RULES.md", "BUILDER_RULES.md"],
    "README": ["README.md"],
}
GROUP_OK = {g: quiet(p) for g, p in GROUPS.items()}
assert all(GROUP_OK.values()), GROUP_OK

def groups_for(row):
    t = (row["location"] + " " + row["evidence"]).lower()
    g = ["course/modules/S/S7"]
    if re.search(r"lab|twin", t): g.append("tests/labs/S7")
    if "mutant" in row["id"] or "mutant" in t: g.append("ledgers/S7/mutants")
    if re.search(r"tools/|check_|run_|verify_refs|fetch_data|render_curriculum|build_site|page_smoke", t): g.append("tools")
    if re.search(r"tests/|test_", t): g.append("tests")
    if re.search(r"reference|registry|cite|crossref|references\.json", t): g.append("references")
    if re.search(r"curriculum|program\.json|curriculum\.json", t): g.append("curriculum")
    if "notation" in t: g.append("notation")
    if "glossary" in t: g.append("glossary")
    if "benchmarks" in t: g.append("benchmarks")
    if re.search(r"manifest|fx_|ust_|data_sources|market|licen|rubric\.js|quiz|site\.js|\bjs\b|vendor|pyodide|lock|css", t): g.append("course/assets")
    if re.search(r"requirements|pyproject|vendor_spec", t): g.append("requirements/pyproject")
    if re.search(r"verifier_rules|builder_rules", t): g.append("VERIFIER_RULES/BUILDER_RULES")
    if "readme" in t: g.append("README")
    return list(dict.fromkeys(g))

def carry(row, extra_text=None):
    gs = groups_for(row)
    files = ", ".join(gs)
    base = row["evidence"]
    if extra_text: base = extra_text + " " + base
    return f"{PREFIX} ({files} byte-identical since {BASE}): {base}"

NEW = {}   # id -> (status, evidence)
def set_(rid, status, ev): NEW[rid] = (status, ev)

# ---- this round's command evidence (logs in scratch)
set_("grader-run-graders", "PASS", f"{RUN}: tools/run_graders.py --unit S7 --seeds 0-49 -> \"run_graders S7: PASS (reference 50/50 seeds, slowest 1.6 s)\" (logs/run_graders.log). The suite is test_project.py (162 tests) under the tool's PYTEST_FLAGS (--assert=plain -W error, run_graders.py line 39).")
set_("grader-instances", "PASS", f"{RUN}: run_graders --unit S7 --seeds 0-49 -> reference 50/50 (the 20 sampled seeds 0-19 are included); instance.py is byte-identical since {BASE}. Answers vary across seeds through the suite's fingerprint check.")
set_("grader-contract-faithful-variant", "PASS", f"{RUN}: run_graders --unit S7 --seeds 0-49 -> reference 50/50 PASS; the contract-faithful alternative is the same suite, which the reference passes (logs/run_graders.log).")
set_("grader-dual-mode", "PASS", f"{RUN}: the local suite (run_graders, same flags as the browser) passes on the reference 50/50, and page_smoke S7 reports the in-browser run 'All 162 tests pass' (logs/page_smoke.log); both runs use the same test_project.py, byte-identical since {BASE}.")
set_("grader-new-tests-runtime", "PASS", f"{RUN}: run_graders --unit S7 --seeds 0-49 -> 50/50, slowest seed 1.6 s against the 10 s budget; the in-browser run reports 'All 162 tests pass' in 2.5 s (logs/page_smoke.log).")
set_("r17-cmd-run-graders-S7", "PASS", f"{RUN}: .venv/bin/python tools/run_graders.py --unit S7 --seeds 0-49 -> \"run_graders S7: PASS (reference 50/50 seeds, slowest 1.6 s)\", EXIT 0 (logs/run_graders.log).")
set_("r17-cmd-local-suite-reference", "PASS", f"{RUN}: run_graders --unit S7 --seeds 0-49 runs the local suite with the browser's flags (-q -p no:cacheprovider --assert=plain -W error) on the reference for every seed: 50/50 PASS (logs/run_graders.log).")
set_("r17-cmd-mutate-after", "PASS", f"{RUN}: .venv/bin/python tools/mutate_graders.py --unit S7 --seeds 0-9 -> \"mutate_graders S7: PASS (164/164 killed)\", EXIT 0; 164 KILLED lines, each killer identical to the round-33 mutants list (logs/mutate_graders.log).")
set_("r17-cmd-mutate-before", "PASS", f"{RUN}: superseded by r17-cmd-mutate-after and by the 164/164 run above (logs/mutate_graders.log). The earlier mutant set is contained in the current 164 .py mutants: every mutant file of the round-33 list is killed.")
set_("r17-cmd-run-labs-S7", "PASS", f"{RUN}: .venv/bin/python tools/run_labs.py --unit S7 -> \"run_labs S7: PASS (42/42)\", EXIT 0 (logs/run_labs.log).")
set_("r17-cmd-page-smoke", "PASS", f"{RUN}: .venv/bin/python tools/page_smoke.py --unit S7 -> \"page_smoke S7: PASS\" (project, hub, lessons, site-wide pages each PASS), EXIT 0; in-browser grader 'All 162 tests pass' (logs/page_smoke.log).")
for rid, cmd, out in [
    ("r17-cmd-check-pages-S7", "check_pages.py --unit S7", "check_pages S7: PASS"),
    ("r17-cmd-check-dag-S7", "check_dag.py --unit S7", "check_dag S7: PASS"),
    ("r17-cmd-check-projects-S7", "check_projects.py --unit S7", "check_projects S7: PASS"),
]:
    set_(rid, "PASS", f"{RUN}: .venv/bin/python tools/{cmd} -> \"{out}\", EXIT 0 (logs/{cmd.split('.')[0]}.log).")
set_("r17-cmd-check-pages-all", "PASS", f"{RUN}: .venv/bin/python tools/check_pages.py --all -> \"check_pages S7: PASS\" and \"check_pages AP1: PASS\", EXIT 0 (logs/check_pages_all.log).")
set_("r17-cmd-check-dag-all", "PASS", f"{RUN}: .venv/bin/python tools/check_dag.py --all -> \"check_dag S7: PASS\" and \"check_dag AP1: PASS\", EXIT 0 (logs/check_dag_all.log).")
set_("r17-cmd-check-projects-all", "PASS", f"{RUN}: .venv/bin/python tools/check_projects.py --all -> \"check_projects S7: PASS\" and \"check_projects AP1: PASS\", EXIT 0 (logs/check_projects_all.log).")
set_("r17-cmd-verify-refs-unit-S7", "PASS", f"{RUN}: .venv/bin/python tools/verify_refs.py --unit S7 (live Crossref, publisher pages) -> \"live re-verification of S7: 94 of 560 entries, 0 problems\", EXIT 0 (logs/verify_refs_live.log). No network or proxy error this round.")
set_("r17-cmd-verify-refs-offline", "PASS", f"{RUN}: .venv/bin/python tools/verify_refs.py --offline (whole registry; the tool rejects --unit with --offline: 'usage ... --unit selects the entries of a live run', exit 2, logs/verify_refs_offline.log) -> then the same command without --unit at edf95c4: \"offline integrity: 560 entries, 0 problems\", EXIT 0 (logs/verify_refs_offline_whole.log).")
set_("r17-cmd-fetch-data-check", "PASS", f"{RUN}: .venv/bin/python tools/fetch_data.py --check -> \"fetch_data: 3 datasets, 0 problems\", EXIT 0 (logs/fetch_data_check.log). The live rebuild of the snapshots (--fetch) was not repeated this round; the round-33 byte-for-byte rebuild stands only as carried evidence (see r33-data-reproducible).")
set_("r17-cmd-lab-L08-4-twin", "PASS", f"{RUN}: python -I -W error tests/labs/S7/lab-S7-L08-4.py run from a scratch directory whose data/ holds fx_monthly.csv (byte-identical to course/assets/data/market/fx_monthly.csv): EXIT 0; prints 'DSR of the in-sample best: median 0.479 share at or above 0.4890: 0.480' (logs/lab_L08_4.log).")
set_("r17-cmd-lab-project-3-twin", "PASS", f"{RUN}: python -I -W error tests/labs/S7/lab-S7-project-3.py from the same scratch data directory: EXIT 0 (logs/lab_project3_twin.log).")
set_("r17-cmd-lab-sol-L04-P4", "PASS", f"{RUN}: python -I -W error tests/labs/S7/sol-S7-L04-P4.py: EXIT 0; prints 'dense_delta=0.3 0.1329 0.1304 0.9123 0.8594' (logs/lab_solL04P4.log).")
set_("r17-cmd-collect-162", "PASS", f"{RUN}: the reference as atlas.integrity in a scratch workspace (copies of test_project.py and instance.py, reference.py as atlas/integrity.py): QF_SEED=0 pytest -q -p no:cacheprovider --assert=plain -W error --collect-only test_project.py -> \"162 tests collected\" (logs/collect162.log).")
set_("proj-number-checks-count", "PASS", f"{RUN}: the same scratch-workspace collection -> \"162 tests collected\" (logs/collect162.log), matching the '162 checks' on project.html #spec. The in-browser run reports 'All 162 tests pass' (logs/page_smoke.log).")
set_("r16-cmd-recheck-refs", "PASS", f"{RUN}: verify_refs --offline (560 entries, 0 problems) and verify_refs --unit S7 live (94 entries, 0 problems) re-run this round (logs/verify_refs_offline_whole.log, logs/verify_refs_live.log). The reference-string recheck of the round-16 script is superseded by these live and offline runs.")
for rid in ["hub-cite-white2000reality","hub-cite-romano2005stepwise","hub-cite-benjamini1995controlling","hub-cite-harvey2015cross","hub-cite-harvey2017presidential","hub-cite-bailey2014deflated","hub-cite-bailey2016probability","proj-cite-kalyuga2003expertise","proj-cite-tetzlaff2025cornerstone","proj-cite-politis1994stationary","proj-cite-moskowitz2012time","proj-cite-huang2020time"]:
    pass  # handled below with the carried attribution text
# ---- lab rows: run_labs re-run this round
for rid in ["proj-lab-1","proj-lab-2","proj-lab-3","proj-number-lab-claims","proj-number-lab3","proj-changed-lab3-hypothesis","r16-p4-premise"]:
    set_(rid, "PASS", f"{RUN}: run_labs --unit S7 -> \"run_labs S7: PASS (42/42)\" (every S7 lab, including lab-S7-project-1..3 and sol-S7-L04-P4, runs and its printed output matches the page's expected block; logs/run_labs.log).")
set_("r14-theorem-4-2-numbers", "PASS", f"{RUN}: python -I -W error tests/labs/S7/lab-S7-L06-3.py (scratch data directory) prints the Lesson 6 Lab 3 table row ending in 0.5238 (logs/lab_L06_3.log, line 5: '3.00 0.0027 0.0111 0.0110 0.0425 0.1743 0.5238'), and run_labs S7 PASS (42/42) checks the page.")
# ---- memo numbers and the memo test
MEMO = ("Round 34 re-derivation: tests/test_memo_exemplars.py 14 passed (logs/memo_exemplars_full.log) - test_every_exemplar_number_is_pinned_to_its_computation recomputes every data-num span from the Lab 3 and Lab 4 twins and the A8 reference and asserts the page text equals the computed value, and test_memo_text_has_no_unpinned_digits holds that no other digit appears in memo text. Independent numpy/stdlib recomputation (indep/recompute.py run on the checkout's fx_monthly.csv, logs/indep_recompute.log) gives T 308, N 40, selected SR 0.0408 (0.14 annualized), PSR 77.0%, DSR 0.49, SR0 0.0424, PBO 0.733, p_min 0.237, N_eff 7.74, rho 0.567 - each agreeing with the memo.")
for rid in [r["id"] for r in prev["rows"] if r["id"].startswith("memo-number-")] + ["memo-exemplar-b-pbo-reading", "r33-headline-recompute", "memo-exemplars-intro", "memo-test-pins", "memo-exemplar-b-dsr", "memo-exemplar-b-multiple-testing"]:
    if rid in ("memo-exemplar-b-dsr", "memo-exemplar-b-multiple-testing"):
        continue
    set_(rid, "PASS", MEMO if rid != "memo-exemplars-intro" and rid != "memo-test-pins" else f"{RUN}: tests/test_memo_exemplars.py 14 passed (logs/memo_exemplars_full.log); the module docstring and the pinning tests are the ones that passed. " + MEMO)
# ---- mutant rows
killed = {}
for line in open(f"{LOG}/mutate_graders.log"):
    m = re.match(r"KILLED (\S+): (.*) -> (\S+) \(seed (\d+)\)", line.strip())
    if m: killed[m.group(1)] = m.group(3)
assert len(killed) == 164, len(killed)
for r in prev["rows"]:
    m = re.match(r"^grader-mutant-([a-z]\d\d)$", r["id"])
    if m:
        f = next(k for k in killed if k.startswith(m.group(1) + "_"))
        set_(r["id"], "PASS", f"{RUN}: mutate_graders --unit S7 --seeds 0-9 -> KILLED {f} by {killed[f]} (seed 0) (logs/mutate_graders.log). The mutant file is byte-identical to {BASE} (ledgers/S7/mutants).")
set_("grader-mutant-rebase", "PASS", f"{RUN}: mutate_graders --unit S7 --seeds 0-9 -> \"mutate_graders S7: PASS (164/164 killed)\"; 164 KILLED lines and no survivor (logs/mutate_graders.log). Set-level row.")
set_("grader-mutant-set-r17", "PASS", f"{RUN}: mutate_graders --unit S7 --seeds 0-9 -> \"mutate_graders S7: PASS (164/164 killed)\"; the 164 .py files in ledgers/S7/mutants are exactly the 164 KILLED mutants (the three *_proposed_killing_tests.txt files are not mutants). Set-level row.")
set_("r14-mutant-set-pinned", "PASS", f"{RUN}: mutate_graders --unit S7 --seeds 0-9 -> 164/164 killed; the mutant set is byte-identical to {BASE} (ledgers/S7/mutants). Set-level row.")
set_("r15-mutants-y12-y17-present", "PASS", f"{RUN}: mutate_graders --unit S7 --seeds 0-9 -> 164/164 killed, including y12 to y17 (KILLED lines in logs/mutate_graders.log); the files are present in ledgers/S7/mutants. Set-level row.")
# ---- the 162-test grader rows: the suite that passes 50/50 contains each named test
TESTNAMES = [r for r in prev["rows"] if r["id"].startswith(("grader-new-test", "grader-r11-judged", "grader-r12-test"))]
for r in TESTNAMES:
    if "::" not in r["location"]: continue
    m = re.search(r"::(test_[a-z0-9_]+)", r["location"])
    name = m.group(1)
    assert re.search(rf"def {name}\(", open(f"{CK}/course/modules/S/S7/grader/test_project.py").read()), name
    set_(r["id"], "PASS", f"{RUN}: run_graders --unit S7 --seeds 0-49 -> 50/50 PASS, and {name} is a test in the suite (def present in test_project.py) that runs in every seed (logs/run_graders.log).")
# ---- atlas: contract re-verification (the contract changed in its header)
ATLAS = {
"atlas-signatures": (f"{RUN}: AST comparison of the 14 function signatures in atlas/A8.contract.md's code block with grader/reference.py (names, order, defaults, keyword-only parameters and their defaults): every one MATCH, and PBOResult, TrialSet and IntegrityReport are present as classes (indep/sigs.py; logs/atlas_sigs.log: 'ALL FUNCTION SIGNATURES MATCH'). The amendment touched only the header: git diff 45548c1 HEAD -- atlas/A8.contract.md is one hunk (@@ -3,7 +3,10 @@), and the body from 'Every function validates' to EOF is byte-identical to 45548c1 (cmp of the two tails, scratch old_body.md / new_body.md)."),
"atlas-contract-vs-reference": (f"{RUN}: the conventions in the contract body (byte-identical) checked against reference.py by function: Sharpe ratio uses ddof=1 (sharpe_ratio); moment estimators m3/m2**1.5 and m4/m2**2, kurtosis not excess (sample_skewness, sample_kurtosis); standard-error bracket with n_obs-1 (sharpe_ratio_std); Benjamini-Hochberg step-up with the mask in input order (benjamini_hochberg); stationary bootstrap with restart probability 1/mean_block and wrap-around (stationary_bootstrap_indices); Romano-Wolf step-down with ceil((1-alpha)B) (stepdown_rejections/_stepdown); romano_wolf draws n_boot index vectors from one generator in order; CSCV with the oldest T mod S rows dropped, itertools order, average ranks and omega = rank/(N+1) (probability_of_backtest_overfitting). Each is exercised by the 162-test suite that passed 50/50 this round (run_graders)."),
"atlas-cumulative-suite": (f"{RUN}: ls atlas/ lists only A8.contract.md, and the contract states that A8 consumes no earlier milestone API, so the cumulative suite is A8's own suite: run_graders --unit S7 --seeds 0-49 PASS 50/50 and mutate_graders 164/164 killed (logs/run_graders.log, logs/mutate_graders.log)."),
"atlas-reuse-frozen": (f"{RUN}: reference.py imports only itertools, math, dataclasses, statistics, typing and numpy (its import block, grader/reference.py lines 16-23). No earlier milestone is imported. The only contract change since {BASE} is the header amendment, which names no earlier API; test_depends_on_numpy_and_stdlib_only is in the 162-test suite that passed 50/50 this round."),
"atlas-acceptance-statement": (f"{RUN}: the Acceptance clause (contract body, byte-identical to {BASE}) says the reference passes the S7 suite on seeds 0-49 and every file in ledgers/S7/mutants fails it: run_graders --unit S7 --seeds 0-49 -> 50/50 PASS; mutate_graders --unit S7 --seeds 0-9 -> 164/164 killed. The local command's flags (-p no:cacheprovider --assert=plain -W error) are the flags of tools/run_graders.py (PYTEST_FLAGS, line 39). Statement true as written."),
"atlas-acceptance-statement-note": (f"{RUN}: covered by atlas-acceptance-statement (same clause, re-run this round: run_graders 50/50, mutate_graders 164/164)."),
"atlas-scale-row": (f"{RUN}: the Scale clause is exercised by test_statistics_are_invariant_to_power_of_two_scaling, test_every_resample_and_subsample_is_rescaled and test_tiny_and_huge_returns (defs present in test_project.py), all in the 50/50 suite; reference.py _scaled() uses np.frexp and np.ldexp as the clause requires."),
"atlas-draw-order": (f"{RUN}: reference.py romano_wolf draws idx = stationary_bootstrap_indices(...) for b = 1..n_boot in order from the single generator default_rng(int(seed)), matching the contract's draw order; test_romano_wolf_bootstrap_statistic_is_the_contracts passes in the 50/50 suite; mutant y07 is KILLED by test_romano_wolf_bootstrap_statistic_is_the_contracts (logs/mutate_graders.log: 'KILLED y07_romano_wolf_bootstrap_sqrt_t_minus_one.py -> test_romano_wolf_bootstrap_statistic_is_the_contracts')."),
"atlas-zero-variance-detection": (f"{RUN}: reference.py _all_equal() compares x.max() == x.min() (the contract's test, not std == 0); test_a_constant_series_has_zero_variance and test_a_constant_column_has_zero_variance pass in the 50/50 suite; mutant q06 is KILLED (logs/mutate_graders.log: 'KILLED q06_rw_constant_column_by_std_equality.py')."),
"atlas-no-warnings": (f"{RUN}: test_functions_neither_print_nor_change_their_arguments and test_numpy_scalar_arguments_do_not_warn (defs present) pass in the 50/50 suite, which runs with -W error (run_graders PYTEST_FLAGS). The body clause is byte-identical to {BASE}."),
"atlas-contract-amendments": (f"{RUN}: the amendment (header lines 6-9; commit bea468a, author Billy Ribeiro, 2026-10-26) is dated and tagged architect-approved, non-breaking. Each factual claim checked: 'NumPy 2.4' - requirements-dev.txt line 6 numpy==2.4.6 and pyodide-lock.json numpy 2.4.6 (cp314 wheel); 'Pyodide 314.0.7' - tools/vendor_spec.yaml line 54 version \"314.0.7\"; 'No signature, type, unit or behaviour changed' - signatures MATCH (atlas-signatures) and the body is byte-identical; 'reference passes on seeds 0-49' - run_graders 50/50; 'all 164 mutants are killed on NumPy 2.4.6' - mutate_graders 164/164 with numpy 2.4.6 imported. The ruling on BUILDER_RULES 5.5 is in atlas-dependency-constraint."),
"atlas-dependency-constraint": (f"{RUN}. RULING: PASS. (1) Statement vs tested pins: the contract now says 'Depends on: NumPy 2.4 and the Python standard library only'. requirements-dev.txt line 6 pins numpy==2.4.6 (the tested version; the local interpreter imports numpy 2.4.6, probe output '2.4.6 1.18.0'); tools/vendor_spec.yaml line 54 pins Pyodide 314.0.7; pyodide-lock.json lists numpy 2.4.6 and scipy 1.18.0 for the in-browser runtime (Python 3.14.2); pyproject.toml line 5 requires-python >=3.14; CLAUDE.md line 79 and BLUEPRINT.md line 356 say Python 3.14+. The version the pins name is 2.4.6, which the statement 'NumPy 2.4' covers. (2) Stdlib-only: the reference's imports are stdlib plus numpy; test_depends_on_numpy_and_stdlib_only passes in the 50/50 suite. (3) BUILDER_RULES 5.5: rule 1 (implement exactly the interface) is unaffected because the signatures and body are byte-identical; rule 2 requires a breaking change to go through CONTRACT_CHANGE_REQUESTS and this amendment changes no signature, type, unit or behaviour and is not an API change, so no request is needed; the document's own status line routes only breaking changes through the request mechanism. The approval is the repository owner's statement in the commit and the Amendments line; I could not verify it independently, and I rely on the user's instruction for it. The round-33 FAIL is therefore resolved."),
"atlas-curriculum-briefs": None,
}
for rid, ev in ATLAS.items():
    if ev is None: continue
    set_(rid, "PASS", ev)
# ---- rows that cite the contract body or the S7 page's contract passage (body unchanged; header changed only)
for rid in ["proj-number-limits-versions", "proj-local-instructions"]:
    pass  # carried below with the body-identity prefix
# ---- banned-phrase scans (contract re-scanned: header amendment added no listed string)
for rid in ["r15-cards-banned-phrases", "r16-banned-phrases"]:
    set_(rid, "PASS", f"{RUN}: banned-string scan (BUILDER_RULES 1.3-1.4 strings) over the S7 page, index, lesson, cards, grader, rubric and grader JS files and atlas/A8.contract.md (35 files): no listed string in the project slice; the contract's amendment adds none. Two hits sit outside this slice and are unchanged from round 33: 'roughly half a standard deviation' in course/modules/S/S7/L01.html line 133 (lesson ledger scope), and the retrieval-prompt ellipses in cards.json and index.html ('A p-value is…'), which are cue text, not omitted content. " + "Prior evidence: " + [r for r in prev["rows"] if r["id"]==rid][0]["evidence"])
set_("r15-slice-files-unchanged", "PASS", f"{RUN}: git diff --quiet {BASE} HEAD over course/modules/S/S7 (incl. grader/), tests/labs/S7, ledgers/S7/mutants, tools, tests, references, curriculum, notation, benchmarks and course/assets: exit 0 (no change). The only changed file in this slice is atlas/A8.contract.md (header amendment, lines 6-9, body byte-identical), recorded in atlas-contract-amendments.")
# ---- docs figures and BLUEPRINT
set_("docs-figures-test-comment", "PASS", f"{RUN}: .venv/bin/python -m pytest tests/test_docs_figures.py -> \"14 passed\" (logs/docs_figures.log). BLUEPRINT.md changed at line 356 only (git diff 45548c1 HEAD: one hunk, 'Python 3.12+' -> 'Python 3.14+'), outside the credential-table rows the test reads.")
set_("proj-claim-expertise-reversal", "PASS", f"Carried from round 33 (course/modules/S/S7 byte-identical since {BASE}; BLUEPRINT.md section 3 byte-identical since {BASE} - the only BLUEPRINT.md hunk is line 356): " + prev["rows"][[r['id'] for r in prev['rows']].index('proj-claim-expertise-reversal')]["evidence"])
# ---- carried rows
PRESERVE_NOTE_TEXT = {}
out = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in NEW:
        status, ev = NEW[rid]
        out.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev})
        continue
    if (rid.startswith("atlas-") and rid != "atlas-curriculum-briefs") or rid in ("docs-figures-test-comment","proj-claim-expertise-reversal"):
        # atlas rows that were not re-written (should be none) are an error
        raise SystemExit(f"unhandled changed-subject row {rid}")
    if rid in ("proj-number-limits-versions", "proj-local-instructions"):
        ev = carry(r, f"(atlas/A8.contract.md body from 'Every function validates' to EOF byte-identical to {BASE}; its header lines 6-9 changed and do not contain the cited text)")
    else:
        ev = carry(r)
    if r["status"] != "PASS":
        raise SystemExit(f"non-PASS row not re-verified: {rid}")
    out.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": ev})
# the new row for the ValueError message claim
out.insert([x["id"] for x in out].index("atlas-dependency-constraint") + 1, {
    "id": "atlas-raise-message-claim", "check": "2.6-atlas", "location": "atlas/A8.contract.md line 14-15 and course/modules/S/S7/project.html #spec Constraints vs grader/reference.py raise sites and grader/test_project.py must_raise",
    "status": "PASS",
    "evidence": f"{RUN}: the contract claims every function 'raises ValueError with a message that names the violated condition'. Reference: every one of its 35 raise sites (reference.py) carries a fixed or f-string message naming the failed condition (e.g. 'returns have zero sample variance (all values are equal)', 'n_blocks cannot exceed the number of periods', 'the variance bracket 1 - skew*SR + (kurt-1)/4*SR^2 must be positive'), so the reference meets the claim. GAP (not a row failure): the S7 grader's must_raise (test_project.py lines 40-46) catches ValueError and returns without reading str(exception); it checks only the type, so the message claim is not enforced by any test. A ValueError with an empty message passes the suite. Recommendation for the builder: a CONTRACT_CHANGE_REQUEST is not needed; a grader test should assert a non-empty message that mentions the condition (out of this verifier's remit to change)."})
# ---- finalize
rows = out
assert len({r["id"] for r in rows}) == len(rows)
assert {r["id"] for r in prev["rows"]} <= {r["id"] for r in rows}
pass_n = sum(1 for r in rows if r["status"] == "PASS")
fail_ids = [r["id"] for r in rows if r["status"] != "PASS"]
verdict = "PASS" if not fail_ids else "FAIL"
now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
notes = (
 "Round 34 (unit S7, PROJECT slice) by Haiku 5.5, independent of the builders and of rounds 12-17 and 33. Previous ledger: the round-33 fragment in ledgers/S7/project.json (557 rows, 556 PASS, 1 FAIL atlas-dependency-constraint, 164/164 mutants, pin 45548c1), read in full before any row was written. Pin edf95c4 (HEAD of /tmp/verify-s7-r2-p, detached). "
 "DELTA (git diff --stat 45548c1 HEAD, 23 files): atlas/A8.contract.md (header amendment only: Amendments line, Depends-on NumPy 2.4; body byte-identical), BLUEPRINT.md (line 356 Python 3.14+), CLAUDE.md (line 79 Python 3.14+), and AP1-only files (course/modules/AP/AP1/grader/test_project.py, course/modules/AP/AP1/project.html, ledgers/AP1*, and the AP1 mutants m65-m70). No S7 file, no shared tool, test, reference, curriculum, notation, benchmark, data or vendor file changed: git diff --quiet 45548c1 HEAD over those paths exits 0. tools/page_smoke.py is NOT in the delta (its diff since 45548c1 is empty), contrary to the brief. ledgers/S7/project.json differs in the working tree only (this fragment). "
 "CONTRACT RULING (atlas-dependency-constraint): the round-33 FAIL is resolved by the architect's amendment. The amendment is consistent with BUILDER_RULES 5.5: the interface (signatures, types, units, body) is unchanged, and the change is not breaking, so CONTRACT_CHANGE_REQUESTS is not required. "
 "Carry convention: a row is carried only where git diff --quiet 45548c1 HEAD proves its subject byte-identical (the group paths are named in each prefix; all groups were checked before use). Rows whose subject includes a changed file were re-verified (atlas-* contract rows; docs-figures-test-comment and proj-claim-expertise-reversal for BLUEPRINT.md, proved by passage-level identity; banned-phrase rows re-scanned). Command rows in the brief's list and their rows were re-run this round (logs in /tmp/ap1-r5/s7p-r2/logs). Numeric memo rows were re-derived by tests/test_memo_exemplars.py (14 passed) and by indep/recompute.py. "
 "NOT RE-RUN this round (carried on byte-identity of their inputs; the toolchain is unchanged since 45548c1 because requirements-dev.txt, pyproject.toml, tools/vendor_spec.yaml and pyodide-lock.json are byte-identical): ruff, mypy, render_curriculum, build_site, the r16/r17 scratch scripts (form sweep, prose sweep, wordcount, blind extract, lemma check, starter trace), the pytest slice, and the live curl/Crossref checks of r16/r17. The live verify_refs run this round covers the S7 registry keys (94 entries). fetch_data --fetch (live rebuild) was not repeated; --check passed. "
 "OUT-OF-SLICE OBSERVATIONS (not rows): (a) course/modules/S/S7/L01.html line 133 'roughly half a standard deviation' (BUILDER_RULES 1.2 unless (a)-(c)); (b) the S7 grader's must_raise does not read the ValueError message (see atlas-raise-message-claim); (c) the Pyodide runtime is Python 3.14.2 while the local interpreter is 3.14.8 (both 3.14; the lock file names 3.14.2); (d) the brief's note that tools/page_smoke.py changed is not borne out by git (no diff since 45548c1). "
 "Test rows note: test_docs_figures 14 passed; test_memo_exemplars 14 passed."
)
summary = {"rows": len(rows), "pass": pass_n, "fail": len(rows) - pass_n, "unverifiable": sum(1 for r in rows if r["status"]=="UNVERIFIABLE"), "mutants": 164, "mutants_killed": 164, "fail_ids": fail_ids}
frag = {
 "unit": "S7", "slice": "project", "round": 34,
 "verifier": "Haiku 5.5, round 34 (independent of the S7 builders and of rounds 12-17 and 33); dependency-constraint ruling and toolchain re-confirmation",
 "pin": HEAD, "base": BASE,
 "previous_ledger": "ledgers/S7/project.json as it stood before this round (round 33: 557 rows, 556 PASS, 1 FAIL atlas-dependency-constraint, 164/164 mutants, pin 45548c1)",
 "checkout": "/tmp/verify-s7-r2-p (detached at edf95c4)",
 "scratch": "/tmp/ap1-r5/s7p-r2/ (logs/, indep/, ws/, build_fragment.py, old_body.md, new_body.md)",
 "verified_at": now, "verdict": verdict,
 "rows": rows,
 "mutants": prev["mutants"],
 "registry_flags": prev["registry_flags"],
 "freshness_flags": prev["freshness_flags"],
 "notes": notes,
 "summary": summary,
}
json.dump(frag, open("/tmp/ap1-r5/s7p-r2/fragment.json", "w"), ensure_ascii=False, indent=1)
print("rows", len(rows), "pass", pass_n, "fail", fail_ids, "verdict", verdict)
print("groups ok", GROUP_OK)
