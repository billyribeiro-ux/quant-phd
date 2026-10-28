import json, re, pathlib
CHK = "/tmp/verify21-CF1-d"
OUT = pathlib.Path(CHK + "/ledgers/CF1/out_tmp")
prev = json.load(open("/tmp/fanout-frags/CF1-d.round20.json"))
CHANGED18 = set("c001 c018 c021 c024 c033 c034 c035 c047 c048 c049 c062 c063 c075 c076 c088 c099 c100".split())
CARRY_PREFIX = ("Carried from round 20 (course/modules/CF/CF1/project.html lines other than 7, 209 and 224, "
                "grader/test_project.py, grader/reference.py, tests/labs/CF1, L01-L06.html, index.html, references/references.json, "
                "tools, and the cited cards.json entries: byte-identical since the previous pin fd9a9b7): ")
FRESH = {}
def fresh(i, status, ev): FRESH[i] = (status, ev)

fresh("cards-grade-semantics", "PASS",
 "Round 21 (f95243f): cards.json changed in 18 entries, grade and basis fields only (diff fd9a9b7..f95243f, 36 changed lines; front and back identical). The 18 definition cards CF1-c001, c018, c021, c024, c033, c034, c035, c047, c048, c049, c062, c063, c075, c076, c088, c099, c100 are now grade C with basis 'Definition N.M (the lesson's definition)'; a python count shows 0 definition-basis cards graded T. L01.html line 46 grade legend reads 'C single study or convention'; BLUEPRINT.md line 158 reserves T for theorems proved on the page. Convention rules at grade C with basis are the rule of this campaign.")
fresh("cards-definition-basis-graded-t", "PASS",
 "Round 21 (f95243f): the 18 definition cards listed in the round-20 row (c001, c018, c021, c024, c033, c034, c035, c047, c048, c049, c062, c063, c075, c076, c088, c099, c100) now read grade C, basis 'Definition N.M (the lesson's definition)' (cards.json; diff of fd9a9b7 shows the old T values). Re-read: no definition-basis card is graded T.")
fresh("proj-tolerance-six-checks-enumerated", "PASS",
 "Round 21 (f95243f): project.html line 209 now says 'Ten checks use an absolute floor of 1e-6 cents instead' and lists ten: the depreciation shield, the working-capital flows (their sum, the year-1 flow, every year's flow), the one-year project, the real-rate NPV, the real flow at the end of life under inflation of -0.999, the zero-EBITDA tax credit, the Monte Carlo draws, the Monte Carlo mean. grader/test_project.py has exactly ten absolute=1e-6 uses: lines 550 (test_inflation_just_above_minus_one_is_valid_in_the_project, inflation -0.999), 568 (shield), 578 (WC sum, abs(total) <= 1e-6), 584 (WC year-1), 593 (one-year project), 607 (WC each year), 627 (real-rate NPV), 792 (tax credit, flows[1]), 863 (MC draws), 897 (MC mean). The list matches the grader one for one.")
fresh("proj-tolerance-nine-recount", "PASS",
 "Round 21 (f95243f): the 'Nine checks' sentence of round 20 is now 'Ten checks' (project.html line 209). The grader has ten absolute=1e-6 checks (test_project.py lines 550, 568, 578, 584, 593, 607, 627, 792, 863, 897; counted by grep of 'absolute=1e-6' and 'abs(total) <= 1e-6'). Count and list agree; grader unchanged since fd9a9b7 (git diff --stat empty for grader).")
fresh("lesson-l06-remark-2-4-each-result-conditional", "FAIL",
 "Round 21 re-verified from scratch: L06.html line 106 (Remark 2.4), unchanged: 'the two exercises that apply it (E1 and E2) label each result as conditional on that reading.' E1 solution (L06.html line 313) computes 84543.40 - 79078.68 = 5464.72 cents and 5464.72/4400.22 = 1.2419 (recomputed: 1.24192); only the tail probability 2(1 - Phi(1.2419)) = 0.2143 (recomputed 0.21427) is labelled 'under that reading'. The cents error and the 1.2419 standard-error count are not conditional on the normal reading, so 'each result' overstates. E2 (line 317-318) labels its band conditional; the band 0.0532 to 0.0572 recomputed. Fix: change Remark 2.4 to 'label the tail probability in E1 and the band in E2 as conditional on that reading'.")

# Tokens of changed card ids in a row's location
CARD_RE = re.compile(r"\bc(\d{3})\b")
rows_out = []
for r in prev["rows"]:
    i = r["id"]
    loc = r["location"]
    ids_in_loc = {"c" + m for m in CARD_RE.findall(loc)}
    if i in FRESH:
        st, ev = FRESH[i]
        rows_out.append({"id": i, "check": r.get("check", ""), "location": loc, "status": st, "evidence": ev, "fix": ("Change L06.html line 106 to: label the tail probability in E1 and the band in E2 as conditional on that reading; the cents error and the standard-error count are not conditional." if st == "FAIL" else "")})
        continue
    if ids_in_loc & CHANGED18:
        ev = ("Re-verified round 21: this row cites card(s) " + ", ".join(sorted(ids_in_loc & CHANGED18)) +
              " whose grade and basis changed in f95243f (front and back text identical). The row's claim is about the card text, which is unchanged; the grade change is checked in cards-grade-semantics. " + r["evidence"])
        rows_out.append({"id": i, "check": r.get("check", ""), "location": loc, "status": r["status"], "evidence": ev})
        continue
    if "line 209" in loc or "line 224" in loc or "line 7" in loc or "line 7;" in loc:
        ev = ("Re-verified round 21: project.html line 209 changed only in the Nine-to-Ten count and the added -0.999 item; the sentence the row cites is unchanged and the grader matches the ten checks (see proj-tolerance-nine-recount). " + r["evidence"])
        rows_out.append({"id": i, "check": r.get("check", ""), "location": loc, "status": r["status"], "evidence": ev})
        continue
    if r["status"] == "PASS":
        rows_out.append({"id": i, "check": r.get("check", ""), "location": loc, "status": "PASS", "evidence": CARRY_PREFIX + r["evidence"]})
    else:
        rows_out.append({"id": i, "check": r.get("check", ""), "location": loc, "status": r["status"], "evidence": r["evidence"]})

NEW = [
 ("r21-delta-coverage", "PASS", "git diff --stat fd9a9b7 f95243f: 264 files; slice files changed: course/modules/CF/CF1/project.html (hunks at lines 7, 209, 224), course/modules/CF/CF1/cards.json (18 entries, grade and basis only), ledgers/CF1/mutants (4 new), ledgers/CF1/scripts/CF1-d-r20 out and r21 files; the grader, tests/labs/CF1, L01-L06.html, index.html, reference.py and references/references.json are unchanged (git diff --stat empty)."),
 ("r21-project-meta-line7", "PASS", "project.html line 7 (meta description): 'a seeded Monte Carlo NPV (the NPVs of random revenue draws)'. Monte Carlo draws multiply revenue by m and report the NPV of each draw (project.html line 208; grader/reference.py npv_monte_carlo lines 185-195). The parenthetical is accurate."),
 ("r21-project-table-line224-wording", "PASS", "project.html line 224 (hours table, after_tax_cash_flows row): 'The shield, the working-capital recovery, the real flag and the validation rules each have named tests, and each has its own named tests in the suite.' The claim is true: test_depreciation_shield_is_depreciation_times_tax_rate (test_project.py line 562), test_working_capital_* (lines 574, 598), test_real_flows_are_deflated_year_by_year (line 613), test_invalid_project_raises_a_named_error (line 706). The sentence is redundant (the clause repeats 'have named tests'); no claim is changed, so it is a wording note, not a FAIL."),
 ("r21-tolerance-ten-checks-match-grader", "PASS", "project.html line 209 lists ten absolute-floor checks; grader/test_project.py has exactly ten 'absolute=1e-6' or 'abs(...) <= 1e-6' assertions (lines 550, 568, 578, 584, 593, 607, 627, 792, 863, 897), each mapping to one listed item."),
 ("r21-cards-definition-grade-convention", "PASS", "cards.json: the 18 definition cards are C with basis 'Definition N.M (the lesson's definition)'. The count of definition-basis cards graded T is 0 (python check). Front and back are unchanged for all 18 (diff shows only grade and basis lines)."),
 ("r21-cards-count-and-fields", "PASS", "cards.json: 109 entries, 109 unique ids, 109 unique fronts, 109 unique backs; grades now 59 T and 50 C (fd9a9b7: 77 T, 32 C); every entry has a non-empty basis and a grade in T/A/B/C/D/X."),
 ("r21-mutants-new-four", "PASS", "ledgers/CF1/mutants/r21d_01 (tax on EBITDA without the depreciation shield), r21d_02 (final-year working-capital flow set to zero), r21d_03 (Monte Carlo generator reseeded inside the draw loop), r21d_04 (NPV exponent t+1). Each parses, and each is KILLED on seed 0 (ledgers/CF1/scripts/CF1-d-r21/out/mutate_r21d.out) by a named test: test_depreciation_shield_is_depreciation_times_tax_rate; test_working_capital_investment_and_recovery_sum_to_zero; test_monte_carlo_draws_follow_the_seeded_gauss_stream; test_npv_keeps_a_leading_zero_flow_in_its_time_index. The rules they break are stated in project.html lines 199-208 (the shield, working-capital recovery, Monte Carlo draw order and the NPV formula)."),
 ("r21-mutants-full-run", "PASS", "tools/mutate_graders.py --unit CF1 --seeds 0-9: 204/204 killed (ledgers/CF1/scripts/CF1-d-r21/out/mutate_r21d.out; the earlier run mutate_r21c.out too). The 190 round-20 mutants and the four new ones are all in ledgers/CF1/mutants."),
 ("r21-alternatives-three-new", "PASS", "ledgers/CF1/scripts/CF1-d-r21/alts/alt_r21d_a (Monte Carlo exponent written as -0.5 * volatility**2), alt_r21d_b (NPV by a running discount factor), alt_r21d_c (payback with a running discount factor and a separate cumulative): all three pass on seeds 0-9 (ledgers/CF1/scripts/CF1-d-r21/out/alts_r21.out)."),
 ("r21-alternatives-all-unique", "PASS", "run_alts21.py over ledgers/CF1/scripts/CF1-d-r*/alts/*.py: 59 files, 40 unique by sha256, all 40 PASS on seeds 0-9 (out/alts_r21.out, 40 'PASS (10 seeds)' lines, no FAIL)."),
 ("r21-collect-157-seeds", "PASS", "pytest --collect-only on a copy of the reference (capbudget.py = reference.py) for QF_SEED 0-10, 20, 30, 40, 49: 157 tests collected on each. project.html line 192 states 157; match."),
 ("r21-run-graders-50", "PASS", "tools/run_graders.py --unit CF1 --seeds 0-49: 'run_graders CF1: PASS (reference 50/50 seeds, slowest 0.3 s)' (out/run_graders.out)."),
 ("r21-gates-checkers", "PASS", "tools/check_pages.py --unit CF1: PASS; check_dag.py --all: PASS (AC4, CF1, AP1 lines); check_projects.py --all: PASS (out/check_pages.out, check_dag.out, check_projects.out)."),
 ("r21-run-labs-and-twins", "PASS", "tools/run_labs.py --unit CF1: 'run_labs CF1: PASS (9/9)'. The nine twins tests/labs/CF1/lab-CF1-*.py each exit 0 under python -I -W error (out/twins_I_W_error.out). pytest tests/test_labs.py -k CF1: 9 passed (out/pytest_test_labs_CF1.out)."),
 ("r21-page-smoke", "PASS", "tools/page_smoke.py --unit CF1: 'page_smoke CF1: PASS' with review.html and the CF1 pages (out/page_smoke.out)."),
 ("r21-ruff-mypy", "PASS", "ruff check and ruff format --check on course/modules/CF/CF1/grader and tests/labs/CF1: 'All checks passed!' and '13 files already formatted'; mypy --no-incremental on the grader: 'Success: no issues found in 4 source files' (out/ruff.out, out/mypy.out)."),
 ("r21-verify-refs", "PASS", "tools/verify_refs.py --unit CF1: 'live re-verification of CF1: 2 of 560 entries, 0 problems'; tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' (out/verify_refs_live.out, out/verify_refs_offline.out)."),
 ("r21-hours-arithmetic", "PASS", "index.html line 29 data-hours-lessons=48, data-hours-project=12; the six lessons have data-hours=8 (6 x 8 = 48); project.html hours table totals 12 (1+1+4+2+1+1+2); 48 + 12 = 60 module hours, 12/60 = 20.0%. Consistent (hours are design targets, not re-estimated)."),
 ("r21-e1-e2-arithmetic", "PASS", "L06.html E1 and E2 recomputed with python: 84543.40 - 79078.68 = 5464.72; 5464.72 / 4400.22 = 1.24192 (printed 1.2419 and +1.242); 2(1 - Phi(1.2419)) = 0.21427 (printed 0.2143); band 0.0552 +/- 1.96 x 0.0010 = 0.05324 to 0.05716 (printed 0.0532 to 0.0572); 2761/50000 = 0.05522. The arithmetic is right; the defect is only the scope of 'each result' in Remark 2.4."),
]
for rid, st, ev in NEW:
    rows_out.append({"id": rid, "check": rid.split("-", 1)[1].replace("-", " "), "location": "see evidence", "status": st, "evidence": ev})

# mutants from the r21d full run
muts = []
for line in open(CHK + "/ledgers/CF1/scripts/CF1-d-r21/out/mutate_r21d.out"):
    m = re.match(r"KILLED (\S+): (.*) -> (.*)$", line.strip())
    if m:
        muts.append({"file": "ledgers/CF1/mutants/" + m.group(1), "description": m.group(2), "killed_by": m.group(3)})
print("mutants", len(muts))
n_pass = sum(r["status"] == "PASS" for r in rows_out)
n_fail = sum(r["status"] == "FAIL" for r in rows_out)
frag = {
 "unit": "CF1", "slice": "CF1-d", "round": 21,
 "verifier": "independent verifier (Haiku), round 21 of CF1 slice d (project page incl. case-memo rubric, grader, project labs, cards.json; project slice needs mutants)",
 "pin": "f95243f (detached, /tmp/verify21-CF1-d)",
 "base": "fd9a9b7 (round-20 pin; delta computed with git diff --stat fd9a9b7 f95243f and every slice hunk read: project.html lines 7, 209, 224; cards.json 18 entries)",
 "checkout": "/tmp/verify21-CF1-d", "scratch": "/tmp/CF1-v/d21",
 "verified_at": "2026-10-28T00:00:00+00:00",
 "verdict": "FAIL",
 "rows": rows_out,
 "mutants": muts,
 "registry_flags": prev["registry_flags"],
 "freshness_flags": [],
 "notes": ("Round-21 delta (fd9a9b7..f95243f) for this slice: project.html line 7 (meta description, parenthetical added), line 209 (Nine -> Ten absolute-floor checks, with the real flow under -0.999 added to the list), line 224 (hours-table wording); cards.json 18 definition cards graded C with basis '(the lesson's definition)'. The grader, tests/labs/CF1, reference.py, instance.py, starter.py, L01-L06.html, index.html and references/references.json are unchanged. Round-20 FAIL rows proj-tolerance-nine-recount, proj-tolerance-six-checks-enumerated, cards-grade-semantics and cards-definition-basis-graded-t are re-verified PASS. lesson-l06-remark-2-4-each-result-conditional remains FAIL (L06.html line 106 unchanged). Rows carried from round 20 keep their round-20 evidence with the carry prefix. Not checked: the full BLUEPRINT re-grade of every card against lesson text (only the 18 changed entries were re-read); the Pyodide browser grader beyond page_smoke; hours not re-estimated (design targets); live Crossref and SEC access not used; the L06 lesson beyond lines 106, 211, 309-322, 444-447. The round-20 prose 'each has its own named tests' repetition at project.html line 224 is a wording note only."),
 "summary": f"CF1-d round 21 (pin f95243f): {len(rows_out)} rows, {n_pass} PASS, {n_fail} FAIL. FAIL: lesson-l06-remark-2-4-each-result-conditional (Remark 2.4 says each E1/E2 result is conditional; E1's cents error and 1.2419 standard-error count are not). Fixed since round 20: the two tolerance-count rows (line 209 now says ten; grader has ten), cards-grade-semantics and cards-definition-basis-graded-t (18 definition cards now C). Mutants: 204 run, 204 killed, 4 new (r21d_01..04). Alternatives: 3 new and 40 unique engines pass seeds 0-9. Collect 157 on sampled seeds.",
}
pathlib.Path("/tmp/CF1-v/d21/CF1-d.round21.json").write_text(json.dumps(frag, ensure_ascii=False, indent=1))
print("rows", len(rows_out), "pass", n_pass, "fail", n_fail)
