"""Build the round-18 fragment ledgers/SC1/SC1-d.json from the round-17 fragment (context only).

Rules applied (verifier-rules.md, carry rule): a previous PASS row is carried with the prefix
'Carried from round 17 (<files> byte-identical since the previous pin 700bf33f):' only when its cited subject files
are unchanged in 700bf33f..50559266 (delta_files_r18.txt, carry_check2_r18.txt). Rows whose subject changed, and the
previous FAIL rows, are re-verified and given new evidence. New fresh rows (SC1-d-r18-*) record this round's checks.
Usage: python3 -I build_frag_r18.py <checkout root>"""
import datetime
import json
import re
import sys

ROOT = sys.argv[1]
D = f"{ROOT}/ledgers/SC1/scripts/SC1-d-r18"
prev = json.load(open("/Users/billyribeiro/.fanout/frags/E-SC1-d.round17.json", encoding="utf-8"))
check = {}
for line in open(f"{D}/out/carry_check2_r18.txt", encoding="utf-8"):
    m = re.match(r"(PASS|FAIL)\s+(\S+)\s+subjects=(\d+) changed=(\[.*\])", line.strip())
    if m:
        check[m.group(2)] = eval(m.group(4))  # list of changed subject files for the row
delta = [x.strip() for x in open(f"{D}/out/delta_files_r18.txt", encoding="utf-8") if x.strip()]
bare_subject = {}
pat = re.compile(r"((?:course|tests|plans|ledgers|references|tools|curriculum|notation|atlas)/[A-Za-z0-9_./\-]+)")
bare = ["project.html", "L01.html", "L02.html", "L03.html", "L04.html", "L05.html", "L06.html", "L07.html",
        "L08.html", "index.html", "cards.json"]

def subjects(row):
    text = " ".join([row.get("location", ""), row.get("evidence", "")])
    files = set(m.group(1).rstrip(".,;:)") for m in pat.finditer(text))
    for b in re.findall(r"\b(" + "|".join(re.escape(x) for x in bare) + r")\b", text):
        files.add("course/modules/SC/SC1/" + b)
    files = {f for f in files if not f.startswith("ledgers/SC1/scripts/SC1-d-r17/")}
    return sorted(files) or ["course/modules/SC/SC1/project.html"]

PLAN_NOTE = "plans/SC1-build-plan.md changed only in 5.5 (discrete_max bullet, lines 428-437) and 5.7(4)"
OVERRIDE = {
    "SC1-d-r7-alt4-ruling10": (
        "PASS",
        "plans/SC1-build-plan.md section 5.7; plans/FINAL-ARCHITECT-RULINGS.md items 10 and 21; "
        "ledgers/SC1/scripts/SC1-d-r17/alternatives/",
        "Round 18 (verifier): the requirement this row checks is ruling 10 (five correct alternatives of different styles "
        "that pass seeds 0-49). It is met by the verified set alt_r17_1..alt_r17_5 (ledgers/SC1/scripts/SC1-d-r17/"
        "alternatives/), each 50/50 on seeds 0-49 against course/modules/SC/SC1/grader/test_project.py, and the reference "
        "50/50 (ledgers/SC1/scripts/SC1-d-r18/out/alternatives_r18.txt, run by ledgers/SC1/scripts/SC1-d-r18/run_one_r18.py). "
        "Ruling 21 withdraws the Box-Muller alternative of plan 5.7(4), so the rounds 1-7 Box-Muller files are no longer "
        "carried and this row no longer cites them. Round-17 FAIL resolved.",
    ),
    "SC1-d-r15-plan-5-5-within-5se": (
        "PASS",
        "plans/SC1-build-plan.md:431-435 (5.5 discrete_max bullet, as amended); plans/FINAL-ARCHITECT-RULINGS.md item 21; "
        "course/modules/SC/SC1/grader/test_project.py:388-416, 455-462",
        "Round 18 (verifier): ruling 21 (plans/FINAL-ARCHITECT-RULINGS.md:item 21, lines 50-54) records the deviation this "
        "row cited, and plans/SC1-build-plan.md:431-435 now states it: the one-step estimate lies within 5 target standard "
        "errors plus 1/N of reflection_tail(a, H)/2, and the grid estimate is one-sided (at most the tail plus the band). "
        "The suite does exactly that: test_project.py:401-416 (one-step vs tail/2, both instances), 455-462 (grid one-sided "
        "at n_steps 4 and the instance's n_steps), 388-392 (SE divisor N-1). Reference passes 50/50 "
        "(ledgers/SC1/scripts/SC1-d-r18/out/run_graders_0_49_r18.txt); collect 136 (collect_count_r18.txt). Round-17 FAIL "
        "resolved by the architect's recorded ruling, no code change.",
    ),
    "SC1-d-r17-plan-5-7-item4-draw-order": (
        "PASS",
        "plans/SC1-build-plan.md section 5.7 item (4) (replaced by ruling 21); plans/FINAL-ARCHITECT-RULINGS.md item 21; "
        "course/modules/SC/SC1/project.html:233; grader/test_project.py:419-423, 641-652",
        "Round 18 (verifier): ruling 21 replaces plan 5.7(4) with the same-order set. The five alternatives (alt_r17_1..5) "
        "draw with rng.gauss path by path and step by step (grep of rng.gauss in the five files, ledgers/SC1/scripts/"
        "SC1-d-r17/alternatives/) and each passes 50/50 (alternatives_r18.txt). The draw-order statement at "
        "project.html:233 (a different order fails the tests) is enforced: the step-major mutants r8_e, r10_d and r12_01 "
        "are each killed by test_discrete_estimate_matches_an_explicit_count_on_the_stated_draws (seed 0; "
        "mutate_graders_unit_r18_full.txt), and the one-step draw test is test_one_step_draws_are_the_seeded_gaussians "
        "(test_project.py:419-423). Round-17 FAIL resolved.",
    ),
    "SC1-d-r17-plan-5-7-items-1-2-3-5": (
        "PASS",
        "plans/SC1-build-plan.md section 5.7 items (1), (2), (3), (5); alternatives under ledgers/SC1/scripts/SC1-d-r17/alternatives/",
        "Round 18 (verifier, re-read against the amended plan): item (1) statistics.NormalDist tail: alt_r17_2 line 16 "
        "2*(1-NormalDist().cdf(a/sqrt(t))). Item (2) Simpson only, no closed form: alt_r17_4 lines 9-26 (8000 intervals, "
        "no erfc). Item (3) DP over (position, running maximum): alt_r17_2 _dp at line 63. Item (5): cumulative sums, "
        "alt_r17_5 lines 27-53 (accumulate), and nested by index subsampling in alt_r17_2 lines 50-60 "
        "(idx = range(stride - 1, n_fine, stride)); alt_r17_5 nests by slicing, which ruling 21 accepts as part of the set. "
        "All five pass 50/50 (alternatives_r18.txt).",
    ),
    "SC1-d-r17-plan-5-5-sweep": (
        "PASS",
        "plans/SC1-build-plan.md:389-441 (5.5, amended bullet at 431-435); course/modules/SC/SC1/grader/test_project.py",
        "Round 18 (verifier): every 5.5 bullet is covered by the suite with the amended discrete_max bullet: reflection_tail "
        "erfc and quadrature (186-194), monotone (197-213), ValueError a=0, t=0 with 1e-9 accepted (222-245); srw identity "
        "and enumeration n<=12 (277-299), ValueError n=0, a=0 with n=1, a=1 accepted (341-373); SE divisor N-1 (388-392), "
        "one-step and one-sided grid (401-416, 455-462), ValueError n_steps=0, n_paths=1 (489-510); nested <= fine "
        "(517-521), ValueError non-divisor (556-562); instances: 49 distinct levels over seeds 0-49 "
        "(instances_r18.txt). Covered by collect 136 and reference 50/50.",
    ),
}
CARRY_NOTE = {
    "SC1-d-spec-tolerance-plan": "plans/SC1-build-plan.md section 5.5 'Statistical tolerance' paragraph (line 448) is "
    "byte-identical; the changed hunk is the discrete_max bullet only",
    "SC1-d-plan-tolerance": "plans/SC1-build-plan.md section 5.5 'Statistical tolerance' paragraph (line 448) is "
    "byte-identical; the changed hunk is the discrete_max bullet only",
    "SC1-d-exemplar-naming": "plans/SC1-build-plan.md section 5.4 is byte-identical (the 5.5 and 5.7 hunks are elsewhere)",
    "SC1-d-r14-rung4-stretch": "plans/SC1-build-plan.md section 5.1(4) is byte-identical (the 5.5 and 5.7 hunks are elsewhere)",
    "SC1-d-r12-pathwise-only-l01": "the cited lesson items (L01 Definition 1.1; L05 A3 and A4; L06 Proposition 1.3 and "
    "Corollary 1.4; L08 Proposition 1.2 and Corollary 1.3) are byte-identical; cards.json and L02/L03 changed outside the "
    "cited items (verified this round: L06 Corollary 1.4 statement, L08 Proposition 1.2 and Corollary 1.3 present)",
    "SC1-d-r15-cross-references": "the cited lesson items are byte-identical (L01, L05, L06, L08 unchanged in the delta; "
    "L08 Proposition 1.2 and Corollary 1.3 and L06 Corollary 1.4 re-read this round)",
    "SC1-d-r17-crossrefs": "the cited lesson items are byte-identical (L01, L05, L06, L08 unchanged in the delta; re-read "
    "this round)",
    "SC1-d-r17-continuity-attribution": "L02.html changed only in the why-it-matters paragraph (one '(§1)' insertion, "
    "delta hunk at line 48); Theorem 2.5 (a Brownian motion on [0,1] with continuous paths) and Remark 2.6 (extension to "
    "[0,infinity)) are byte-identical and were re-read this round",
}
rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in OVERRIDE:
        status, loc, ev = OVERRIDE[rid]
        rows.append({"id": rid, "check": r["check"], "location": loc, "status": status, "evidence": ev})
        continue
    files = subjects(r)
    if check.get(rid) and rid not in CARRY_NOTE:
        raise SystemExit(f"unexpected changed subject for {rid}: {check[rid]}")
    if rid in CARRY_NOTE:
        prefix = ("Carried from round 17 (cited items byte-identical since the previous pin 700bf33f; "
                  + CARRY_NOTE[rid] + "): ")
    else:
        files_txt = ", ".join(files[:5]) + (" and others" if len(files) > 5 else "")
        prefix = f"Carried from round 17 ({files_txt} byte-identical since the previous pin 700bf33f): "
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                 "evidence": prefix + r["evidence"]})

FRESH = [
    ("SC1-d-r18-structure-gates", "check_pages.py, check_dag.py, check_projects.py --unit SC1",
     "Round 18 (verifier) on pin 50559266: check_pages SC1 PASS, check_dag SC1 PASS, check_projects SC1 PASS, each exit 0 "
     "(ledgers/SC1/scripts/SC1-d-r18/out/check_pages_unit_r18.txt, check_dag_unit_r18.txt, check_projects_unit_r18.txt)."),
    ("SC1-d-r18-run-labs", "tools/run_labs.py --unit SC1 (and --page project); twins under python -I -W error",
     "Round 18: run_labs SC1 11/11 PASS and project 3/3 PASS (run_labs_unit_r18.txt, run_labs_project_r18.txt). Each twin "
     "run alone under python3 -I -W error: exit 0, empty stderr, stdout equal line by line to the page's expected block "
     "for all 7 + 3 + 11 lines (ledgers/SC1/scripts/SC1-d-r18/out/twin_output_r18.txt, script twin_output_r18.py)."),
    ("SC1-d-r18-page-equals-twin", "course/modules/SC/SC1/project.html lab-SC1-project-1/2/3 vs tests/labs/SC1/",
     "Round 18: page code block equals the twin line for line for Lab 1 (97 lines) and Lab 3 (112 lines); Lab 2 differs "
     "from its completed twin only at the two blank lines (identity = ___ and max_hits == ___), as the rung-2 design "
     "requires (ledgers/SC1/scripts/SC1-d-r18/out/twin_vs_page_r18.txt, script twin_vs_page_r18.py)."),
    ("SC1-d-r18-run-graders", "tools/run_graders.py --unit SC1 --seeds 0-49",
     "Round 18: reference 50/50 seeds PASS (run_graders_0_49_r18.txt). Not re-run: seeds 50-199 (round-17 200/200 on a "
     "byte-identical grader)."),
    ("SC1-d-r18-page-smoke", "tools/page_smoke.py --unit SC1 --pages project",
     "Round 18: page_smoke modules/SC/SC1/project.html PASS; in-browser grader reports 'All 136 tests pass' "
     "(page_smoke_project_r18.txt)."),
    ("SC1-d-r18-mutants-all", "tools/mutate_graders.py --unit SC1 --seeds 0-9 over all 94 mutants",
     "Round 18: mutate_graders SC1 PASS (94/94 killed): the 90 carried mutants (byte-identical) and the 4 new r18 mutants. "
     "Each mutant's killing test is listed in the mutants list (ledgers/SC1/scripts/SC1-d-r18/out/"
     "mutate_graders_unit_r18_full.txt)."),
    ("SC1-d-r18-mutants-new", "ledgers/SC1/mutants/r18_01..r18_04 (generated by ledgers/SC1/scripts/SC1-d-r18/make_mutants_r18.py)",
     "Round 18: four new student-error mutants, each a single-change copy of grader/reference.py, each killed on seed 0: "
     "r18_01 reflection_tail swaps level and time (closed-form test); r18_02 horizon capped at one (closed-form test); "
     "r18_03 grid maximum over the first half of the grid (test_fine_count_is_the_discrete_estimate_times_n); r18_04 "
     "Laplace-smoothed estimate (test_estimate_is_a_fraction_of_the_paths)."),
    ("SC1-d-r18-alternatives", "ledgers/SC1/scripts/SC1-d-r17/alternatives/alt_r17_1..5 via ledgers/SC1/scripts/SC1-d-r18/run_one_r18.py",
     "Round 18: each of the five alternatives passes 50/50 seeds (0-49) against the page's suite; reference 50/50 "
     "(alternatives_r18.txt). Each alternative's random draws use rng.gauss path by path and step by step."),
    ("SC1-d-r18-collect-count", "pytest --collect-only on test_project.py with reference copied to bm_checks.py (scratch run; output in out/collect_count_scratch_r18.txt)",
     "Round 18: 136 tests collected (last line of out/collect_count_scratch_r18.txt) and 136 passed with -W error on the reference (page says 136)."),
    ("SC1-d-r18-relevant-tooling-tests", "pytest tests/test_run_labs.py tests/test_page_checks.py tests/test_page_smoke.py tests/test_memo_exemplars.py tests/test_labs.py",
     "Round 18: exit 0 (pytest_relevant_r18.txt). tests/labs/ holds only twin files with no test_ modules, so "
     "pytest tests/labs collects nothing (exit 5, pytest_labs_r18.txt); the lab gate is run_labs (above)."),
    ("SC1-d-r18-lint-types", "ruff check ., ruff format --check ., mypy --no-incremental, ruff on grader and labs",
     "Round 18: ruff check . PASS; ruff format --check . PASS (553 files); mypy --no-incremental PASS (385 source files); "
     "ruff check and format --check on grader and tests/labs/SC1 PASS (ruff_*_r18.txt, mypy_r18.txt)."),
    ("SC1-d-r18-verify-refs-offline", "tools/verify_refs.py --offline",
     "Round 18: offline integrity 560 entries, 0 problems (verify_refs_offline_r18.txt). Live run not performed."),
    ("SC1-d-r18-numbers-recomputed", "ledgers/SC1/scripts/SC1-d-r18/indep_numbers_r18.py (second route: NormalDist, own loops, binomial counts)",
     "Round 18: tail 0.086496661 by erfc and by NormalDist (diff 4e-17); one-step 0.059548 (se 0.010735); grid n=1,4,16,64,256 "
     "estimates, SEs (0.009819 to 0.012870) and tail-minus-estimate (0.026948, 0.037215, 0.020788, -0.001799, 0.004361); nested "
     "35, 29, 27, 22 <= 40; target 0.043248, target se 0.009218, band 0.048142; 0.016300 = 1.52 sample se = 1.77 target se; "
     "64-step excess 0.001799 = 0.140 se; walk 1588 and 794 (4096 walks), walk n=6 a=2 29, 22, 7. All match page prose "
     "and Lab 3 (indep_numbers_r18.txt)."),
    ("SC1-d-r18-test-comment-seed32", "course/modules/SC/SC1/grader/test_project.py:471-474 comment",
     "Round 18: seed 32 instance (H 0.584, a 2.444, N 639): hits 0 on grids 16, 32 and 64 at its own level, as the comment states "
     "(indep_numbers_r18.txt)."),
    ("SC1-d-r18-instances", "grader/instance.py via ledgers/SC1/scripts/SC1-d-r18/instances_r18.py",
     "Round 18: seeds 0-19 valid (H>0, a>0, 4<=n_steps<=256, 400<=N<=800, n_steps*N<=200000, label SIMULATED); answers change: "
     "the tail and the one-step estimate differ across the 20 seeds, 49 distinct levels and 50 distinct tails over seeds 0-49 "
     "(instances_r18.txt)."),
    ("SC1-d-r18-blind-exemplars", "project.html exemplar-a (data-level 4) and exemplar-b (data-level 2), scored from ledgers/SC1/scripts/SC1-d-r18/blind_extract_r18.py output",
     "Round 18: blind scores from the memo prose only (blind_extract_r18.txt): exemplar A C1-C5 = 4,4,4,3,4; exemplar B = 2,2,2,2,2. "
     "Both within one level of the annotated data-scores on every criterion. Caveat: a structural grep of project.html "
     "that I ran before scoring printed the data-level and data-scores attribute values (lines 465 and 547), so this is not a "
     "dedicated blind scorer under ruling 23; I did not read the annotation text."),
    ("SC1-d-r18-spec-claims", "project.html spec, constraints, grading and draws sections vs grader and lab code",
     "Round 18: 136 tests (lede, grading, local run); the ValueError conditions match the tests (222-245, 341-373, 489-510, "
     "556-575); no function prints or warns (586-616, and the autouse capsys fixture 42-46); generator formula in page, "
     "instance.py and reference match (1_000_003*seed+54_321; horizon and level rounded to three decimals; n_steps 4-256; "
     "N 400 to min(800, 200000//n_steps)); seed-0 instance H 2.083, a 2.474, N 487."),
    ("SC1-d-r18-hours", "project.html #hours table; course/modules/SC/SC1/index.html data-hours-project; curriculum/03-markets.yaml:508",
     "Round 18: 2+3+10+8+3+2 = 28 = data-hours-project; hub lessons 72 + project 28 = 100 = curriculum hours 100 (03-markets.yaml:508)."),
    ("SC1-d-r18-lab3-interpretation", "project.html Lab 3 interpretation paragraph",
     "Round 18: 'lies 0.001799 above the tail, 0.14 of its standard error 0.012870' (0.1398), '1.52 sample standard errors' "
     "(1.518), '1.77 target standard errors' (1.768), '1588 is the number of the 4096 walks' all recomputed (indep_numbers_r18.txt)."),
    ("SC1-d-r18-L06-L08-L05-L01-labels", "project.html citations: L01 Def 1.1, L02 Thm 2.5 and Rem 2.6, L05 A3/A4, L06 Prop 1.3 and Cor 1.4, L08 Prop 1.2 and Cor 1.3",
     "Round 18: headings present in source: L01 Definition 1.1; L02 Theorem 2.5 (continuous paths) and Remark 2.6; L05 A3 and A4 "
     "(A4(a), A4(b), A4(f) etc.); L06 Proposition 1.3 and Corollary 1.4 (discrete tail identity #{M_N>=a}=#{S_N>=a}+#{S_N>a}, "
     "a>=1); L08 Proposition 1.2 (first passage on each path) and Corollary 1.3 (distribution function). Read this round in "
     "the checkout."),
]
fresh_rows = [{"id": i, "check": c, "location": c.split(" ")[0] if False else loc, "status": "PASS", "evidence": e}
              for (i, loc, e), c in [((a, b, cc), b) for a, b, cc in FRESH]]
# the 'check' field holds the command or subject, 'location' the file(s); keep both
fresh_rows = [{"id": a, "check": "round-18 fresh check", "location": b, "status": "PASS", "evidence": cc}
              for a, b, cc in FRESH]

mutants = []
for line in open(f"{D}/out/mutate_graders_unit_r18_full.txt", encoding="utf-8"):
    m = re.match(r"KILLED (\S+?\.py): (.*?) -> (.*)$", line.rstrip("\n"))
    if m:
        mutants.append({"id": m.group(1), "description": m.group(2).strip(), "killed_by": m.group(3).strip()})
assert len(mutants) == 94, len(mutants)

rows_all = rows + fresh_rows
verdict = "PASS" if all(r["status"] == "PASS" for r in rows_all) else "FAIL"
summary = (
    f"SC1-d round 18 on 50559266 (base 700bf33f): verdict {verdict}. {len(rows_all)} rows, all PASS: 3 round-17 FAIL rows "
    "re-verified and now PASS (ruling 21 records the plan 5.5 and 5.7(4) amendments; the five alt_r17 alternatives pass); "
    "rows whose cited subjects changed in the delta (plan 5.5/5.7, L02 why-it-matters line, cards.json) re-read and 8 carried "
    "with the changed item named; 207 rows carried with byte-identical subjects; 20 fresh rows for this round's gate runs, "
    "mutants 94/94 (4 new), alternatives 5/5 plus reference, labs, numbers, instances and blind exemplar scores."
)
notes = (
    "Round 18 read: project.html read in full (1-666; exemplars scored from the stripping script output before any "
    "annotation text was read, with the caveat in row SC1-d-r18-blind-exemplars), grader/instance.py, reference.py, "
    "starter.py and test_project.py read in full, three lab twins compared with the page, delta read at the file level "
    "(only SC1 files changed: L02.html, L03.html, cards.json, plans, rulings, the 4 r17 mutants and 5 alt_r17 files). "
    "Not checked this round: the 47 carried alternatives (round-17 47/47, grader byte-identical); reference seeds 50-199; "
    "live verify_refs (offline only); full repository pytest; cards (outside slice d); L01, L03, L04, L07 beyond the "
    "cross-references; the plan's 5.7 alternatives folder path (plan says ledgers/SC1/scripts/alternatives/, the verified "
    "set is ledgers/SC1/scripts/SC1-d-r17/alternatives/; ruling 21 names the set, so no row fails on it). Wording "
    "observation for the builder, not a row: Lab 3 says the grids 'share draws'; they read the same seeded stream, but "
    "path i of an n-step grid uses draws n(i-1)+1..ni, so only the stream, not each variate, is shared."
)
frag = {
    "unit": "SC1",
    "slice": "d",
    "round": 18,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-d, round 18 (did not build SC1-d; read project.html, grader, "
                "labs, ran gates, re-ran all 94 mutants and the five alt_r17 alternatives, scored exemplars blind via "
                "stripping script, recomputed numbers by a second route)",
    "pin": "50559266",
    "base": "700bf33f",
    "checkout": ROOT,
    "scratch": "/tmp/sc1d_r18_scratch",
    "scripts_dir": "ledgers/SC1/scripts/SC1-d-r18/",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows_all,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": summary,
}
json.dump(frag, open(f"{ROOT}/ledgers/SC1/SC1-d.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("rows", len(rows_all), "mutants", len(mutants), "verdict", verdict)
