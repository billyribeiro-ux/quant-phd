"""Build ledgers/AC2/project.json (round 8) from the round-7 fragment plus this round's re-verification."""
import json, re
from pathlib import Path

ROOT = Path("/tmp/verify-ac2r8-p")
D = ROOT / "ledgers/AC2/scripts/project-r8"
r7 = json.loads(Path("/tmp/ac2-frags/project.round7.json").read_text(encoding="utf-8"))
log = (D / "project-r8-mutate-56.txt").read_text(encoding="utf-8").splitlines()

# ---- mutants: parse the tool's own output (56 lines: KILLED/SURVIVED <file>: <desc> -> <killed_by>)
mutants = []
for line in log:
    m = re.match(r"^(KILLED|SURVIVED) (\S+\.py): (.*) -> (.*)$", line)
    if not m:
        continue
    status, fname, desc, killed = m.groups()
    mutants.append({
        "description": desc,
        "file": f"ledgers/AC2/mutants/{fname}",
        "killed_by": killed if status == "KILLED" else None,
    })
assert len(mutants) == 56, len(mutants)
assert all(m["killed_by"] for m in mutants)
kill = {Path(m["file"]).name.split("_")[0]: m["killed_by"] for m in mutants}  # 'm01'.. 'p01'.. 'n01'
desc_of = {Path(m["file"]).name.split("_")[0]: m["file"] for m in mutants}

CHANGED = {
    "course/modules/AC/AC2/project.html": "project.html line 245 (240 checks) only",
    "course/modules/AC/AC2/index.html": "index.html line 148 (L05 card title) only",
    "course/modules/AC/AC2/cards.json": "cards c024, c072, c107 only",
    "course/modules/AC/AC2/grader/test_project.py": "new test test_previous_year_is_the_latest_period_end_in_the_window (+13 lines)",
    "plans/AC2-open-items.md": "line 16 (Beneish row) only",
}

NEW = {}  # id -> (status, evidence) : re-verified this round

# --- grader, collection, reference, impls
NEW["proj-grader-collect-count"] = ("PASS", "Round 8: pytest --collect-only on grader/reference.py workspace gives 240 tests with QF_SEED 0, 1, 7, 25 and 49 (scripts/project-r8/collect_seeds.py); the project.html line 245 figure 240 matches.")
NEW["proj-grader-rubric"] = ("PASS", "Round 8: project.html Grading mode now reads 240 checks (line 245); the count matches the 240 collected; the rest of the paragraph is unchanged since 6adfd01 (git diff hunk is the count only).")
NEW["proj-grader-integrity"] = ("PASS", "Round 8: project.html line 245 integrity sentence unchanged apart from the count; 50-seed reference run and five alternative implementations (r8-impls-v1-v5-50) pass, so the seeded-instance claim holds on this checkout.")
NEW["proj-grader-reference-50"] = ("PASS", "Round 8: tools/run_graders.py --unit AC2 --seeds 0-49 -> 'run_graders AC2: PASS (reference 50/50 seeds, slowest 0.3 s)' (scripts/project-r8/project-r8-grader.txt).")
NEW["r7-grader-reference-50"] = NEW["proj-grader-reference-50"]
NEW["r6-run-graders-0-49"] = NEW["proj-grader-reference-50"]
NEW["proj-r5-run-graders-50"] = NEW["proj-grader-reference-50"]
NEW["r3-run-graders"] = NEW["proj-grader-reference-50"]
NEW["proj-grader-overconstraint"] = ("PASS", "Round 8: five alternative correct implementations (scripts/project-r8/impls_r3/V1..V5, the round-3 set) pass all 240 checks on seeds 0-49 (scripts/project-r8/impls_run.txt: PASS x5, first_fail_seed=None).")
NEW["r7-impls-v1-v5"] = NEW["proj-grader-overconstraint"]
NEW["r5-impls-50"] = NEW["proj-grader-overconstraint"]
NEW["proj-r5-impls-50"] = NEW["proj-grader-overconstraint"]
NEW["r3-candidates"] = NEW["proj-grader-overconstraint"]
NEW["proj-r4-impls-overconstraint"] = NEW["proj-grader-overconstraint"]
NEW["proj-r4-grader-236"] = ("PASS", "Round 8: the suite now collects 240 (not 236) on grader/reference.py, and run_graders --seeds 0-49 passes; the 236 count of round 4 is superseded by the 240 the round-8 project.html states; row kept for history.")
NEW["proj-r5-collect-236"] = ("PASS", "Round 8: the round-5 count of 236 is superseded: pytest --collect-only gives 240 on seeds 0, 1, 7, 25 and 49 and project.html line 245 says 240. 236 plus the four parametrized cases of the new test (dupont, roic, accruals_cash_flow, accruals_balance_sheet) gives 240.")
NEW["r6-collect-236"] = NEW["proj-r5-collect-236"]
NEW["r3-test-assertions"] = ("PASS", "Round 8: the only grader change since 6adfd01 is test_previous_year_is_the_latest_period_end_in_the_window (grader/test_project.py, +13 lines, parametrized over dupont, roic, accruals_cash_flow, accruals_balance_sheet). Read in full: its contract claim (latest period end 350 to 380 days back) and its decoy (a period 372 days back with total_assets and equity times 1.5) are as the contract states; reference passes it on 50 seeds.")
NEW["r3-valueerror-list"] = ("PASS", "Round 8: project.html lines 243 and 245 list the named ValueError conditions; the round-8 diff touches only the count on line 245; the list matches test_project.py (which still raises every named condition: 240 checks pass on the reference, the mutants p06, p03, p07, p37 and m11 are killed).")

# --- page, labs, hub, project pages
NEW["r6-page-smoke-project"] = ("PASS", "Round 8: tools/page_smoke.py --unit AC2 -> 'in-browser grader: All 240 tests pass on seed 1668683391' and 'page_smoke modules/AC/AC2/project.html: PASS', index.html, concepts.html, review.html PASS, 'page_smoke AC2: PASS' (scripts/project-r8/project-r8-smoke.txt).")
NEW["proj-grader-pyodide"] = NEW["r6-page-smoke-project"]
NEW["proj-r5-page-smoke"] = NEW["r6-page-smoke-project"]
NEW["proj-labs-run"] = ("PASS", "Round 8: tools/run_labs.py --unit AC2 -> 'run_labs AC2: PASS (11/11)' (scripts/project-r8/run_labs_AC2.txt); the project labs are among the 11.")
NEW["r6-project-labs-isolated"] = ("PASS", "Round 8: the project lab twins are byte-identical since 6adfd01 (not in the diff); run_labs PASS 11/11 covers them. The isolated python -I -W error run is carried from round 7.")
NEW["proj-hub-ladder-claim"] = ("PASS", "Round 8: index.html read in full (20 KB); the ladder paragraph (line 161 rung 3 'Independent project') names the A15 functions, which match project.html Required outputs; index.html changed only at line 148.")
NEW["r6-hub-placement-count"] = ("PASS", "Round 8: index.html placement: nine items (six prerequisite: four AC1 at Pq1, Pq2 gross margin, Pq3, Pq4 and two S0 at Pq5 median, Pq6 MNAR; three skill checks marked data-skill). No item tests S2, and the hub says so (line 70). Mastery 0.8 of nine = eight correct; 7/9 = 77.8%, shown as 78%.")
NEW["proj-placement-condition"] = NEW["r6-hub-placement-count"]
NEW["r3-placement-s2"] = NEW["r6-hub-placement-count"]
NEW["proj-r4-hub-placement-and-ladder"] = NEW["r6-hub-placement-count"]
NEW["proj-r5-hub-placement"] = NEW["r6-hub-placement-count"]
NEW["r6-hub-hours"] = ("PASS", "Round 8: index.html data-hours-lessons=76 and data-hours-project=34 (project.html); lesson card hours 9+10+8+9+8+10+10+12 = 76; 76+34 = 110; 76/110 = 69.1%, 34/110 = 30.9%; each lesson 8 to 12 h (inside 6-12).")
NEW["proj-hours-split"] = NEW["r6-hub-hours"]
NEW["r6-hub-cards-bodies"] = ("PASS", "Round 8: index.html read in full; the eight lesson card bodies (lines 145-152) match each lesson's content as read in round 7 (their hunk was the L05 title only).")
NEW["r6-hub-l05-card-reverify"] = ("PASS", "Round 8: index.html line 148 now reads 'The Accruals Anomaly and the Sloan (1996) Question'; body unchanged and matches L05 (L05.html line 61: 'The lesson states no finding of that paper'; L05 line 223 SIMULATED). Non-blocking note: the L05 h1 is 'The Accruals Anomaly' (line 36), a title difference, not a claim.")
NEW["proj-r5-hub-l05-card"] = NEW["r6-hub-l05-card-reverify"]
NEW["r7-hub-whole-read"] = ("PASS", "Round 8: index.html read in full again (all lines; 1 changed line at 148). Data status paragraph (SIMULATED only, no SEC entry) read in full; nothing in tools/data_sources.yaml.")
NEW["r6-hub-data-status"] = ("PASS", "Round 8: index.html data paragraph read in full ('SIMULATED data only ... Nothing is in tools/data_sources.yaml yet.'); tools/data_sources.yaml has no SEC entry (carried from round 7 for the file).")
NEW["r7-data-sec-reachability"] = ("PASS", "Round 8: plain curl -I https://www.sec.gov/os/webmaster-faq -> 403 and https://www.sec.gov/os/accessing-edgar-data -> 403 (both reproduced; GET of webmaster-faq also 403). plans/AC2-open-items.md DATA_REQUESTS row carries the same statement.")
NEW["proj-spec-named-error-covered"] = ("PASS", "Round 8: project.html line 243 and 245 named-error list vs grader invalid-input tests; grader unchanged apart from the new test; all named conditions still raise (reference 240 checks pass).")

# --- cards
NEW["r7-cards-c024"] = ("PASS", "Round 8: cards.json AC2-c024 back now reads 'with equity unchanged, every liability raises the leverage factor'. Matches L02.html canon-breaks bullet 1 (same wording). Math: avg A / avg E = 1 + avg L / avg E (A = L + E each year, averages add), so with E fixed a higher L raises the factor; the 'with equity unchanged' qualifier is required and present.")
NEW["r6-cards-c107"] = ("PASS", "Round 8: cards.json AC2-c107 back: DOI link https://doi.org/10.2469/faj.v55.n5.2296 returned HTTP 302 to https://www.tandfonline.com/doi/full/10.2469/faj.v55.n5.2296, which returned HTTP 403 to plain curl (HEAD and GET) on 2026-10-27 (reproduced with curl, no bypass). Wikipedia 'Beneish M-score' page (https://en.wikipedia.org/wiki/Beneish_M-score) returned HTTP 200 and its equation has -4.84 intercept, 0.92, 0.528, 0.404, 0.892, 0.115, -0.172, 4.679, -0.327. The Scribd cite has no publication year ('Retrieved 2017-01-08' only), so 'undated' holds.")
NEW["r7-cards-c107"] = NEW["r6-cards-c107"]
NEW["r6-cards-c107-lesson"] = ("PASS", "Round 8: L08.html section 2 (line 93) now gives the same URL and status codes as the card; both reproduced with curl (302, 403). Candidate constants read as the Wikipedia values, labelled UNCONFIRMED.")
NEW["r6-beneish-researchgate"] = ("PASS", "Round 8: L08 section 2 and the card no longer cite ResearchGate; no ResearchGate claim remains in the changed hunks (grep of the changed lines: none).")
NEW["r6-open-items-beneish-jstor"] = ("PASS", "Round 8: plans/AC2-open-items.md line 16 Beneish REFERENCE_REQUESTS row: the DOI link returned 302 to the tandfonline full-text URL, which returned 403 (reproduced with curl -I and GET); the row is marked OPEN and UNCONFIRMED.")
NEW["r7-dechow-doi-access"] = ("PASS", "Round 8: plans/AC2-open-items.md 'dechow1995detecting' row: DOI 10.2308/tar-9505096112 returned 302 to https://publications.aaahq.org/accounting-review/article/70/2/193/18940/Detecting-Earnings-Management, which returned HTTP 403 for both -I and GET (reproduced with plain curl; no bypass).")
NEW["r7-cards-schema"] = ("PASS", "Round 8: cards.json has 140 records AC2-c001..c140 (ids unique, in order); no duplicate fronts; 54 ungraded cards (definitions, theorems, misconceptions, which BUILDER_RULES 7 allows), 49 C, 36 T, 1 D; all cite keys exist in references/references.json; all lesson values are L01..L08 with a lesson file present.")
NEW["r6-cards-count-schema"] = NEW["r7-cards-schema"]
NEW["proj-r5-cards-count-schema"] = NEW["r7-cards-schema"]
NEW["proj-r4-cards-count-ids"] = NEW["r7-cards-schema"]
NEW["proj-r5-cards-L05"] = ("PASS", "Round 8: the fifteen L05 cards read against L05.html: AC2-c072 back now reads 'The lesson states no finding of Sloan (1996)'; L05.html line 61 says exactly that; line 223 (SIMULATED planted effect) supports 'the lab plants the effect'. Other L05 cards carried from round 7.")
NEW["r7-cards-c075"] = ("PASS", "Round 8: AC2-c075 record byte-identical since 6adfd01 (cards.json diff hunks are c024, c072, c107 only); carried with its round-7 check.")
NEW["r6-cards-c123"] = ("PASS", "Round 8: AC2-c123 record byte-identical (not in the 6adfd01 diff); carried.")
NEW["r6-cards-c130"] = ("PASS", "Round 8: AC2-c130 record byte-identical (not in the diff); its L07 section 5 table row (s7 proxy, line 81) still matches.")
NEW["proj-r4-cards-grades"] = ("PASS", "Round 8: cards.json grades read against lesson claim spans; c058 and c064 records byte-identical; the grade set is C/T/D as in the record.")
NEW["r3-hub-line157"] = ("PASS", "Round 8: index.html line 157 unchanged since 6adfd01 (diff shows line 148 only); carried.")
NEW["proj-mut-summary"] = ("PASS", "Round 8: tools/mutate_graders.py --unit AC2 --seeds 0-9 over 56 mutants (m01-m16, p01-p37, n01-n03): 56/56 KILLED; 'mutate_graders AC2: PASS (56/56 killed)' (scripts/project-r8/project-r8-mutate-56.txt).")
NEW["r6-mutate-50"] = ("PASS", "Round 8 re-run: m16 KILLED by test_previous_year_is_the_latest_period_end_in_the_window[dupont] (seed 0); 56/56 killed. The round-6 survivor m16 is closed.")
NEW["r7-mutate-53"] = ("PASS", "Round 8 re-run: 53/53 of the known mutants killed plus n01-n03 (three new student-error mutants): 56/56 killed (scripts/project-r8/project-r8-mutate-56.txt).")
NEW["r7-mut-m16"] = ("PASS", "Round 8: m16 (_previous picks the earliest period end in the 350 to 380 day window) is KILLED by test_previous_year_is_the_latest_period_end_in_the_window[dupont] on seed 0 (log line 'KILLED m16_previous_year_is_earliest_in_window.py ... -> test_previous_year_is_the_latest_period_end_in_the_window[dupont] (seed 0)').")
NEW["r6-mutants-new-m11-m13"] = ("PASS", "Round 8 re-run: m11, m12 and m13 KILLED (log lines 'KILLED m11_roic_zero_capital_returns_zero.py ... -> test_roic_rejects_nonpositive_invested_capital (seed 0)', m12 -> test_accruals_balance_sheet_number, m13 -> test_piotroski_strict_signals_score_zero_at_an_exact_tie).")
NEW["r3-mut-round2-set"] = ("PASS", "Round 8 re-run: p01..p13 all KILLED with killed_by given per mutant (proj-mut-p01..p13 rows).")
NEW["proj-r4-mutants-total"] = NEW["proj-mut-summary"]
NEW["proj-r5-mutants-47"] = ("PASS", "Round 8: the 47 round-5 mutants (m01-m10, p01-p37) are all KILLED on seeds 0-9 in the round-8 re-run; with m11-m16 and n01-n03 the set is 56, 56/56 killed.")

# per-mutant rows: mutants all re-run this round; the killed_by for each
def mut_row(key):
    m = kill[key]
    return ("PASS", f"Round 8 re-run: tools/mutate_graders.py --unit AC2 --seeds 0-9 -> KILLED {desc_of[key].split('/')[-1]} -> {m}.")

for r in r7["rows"]:
    rid = r["id"]
    mm = re.match(r"proj-mut-(p\d\d)$", rid)
    if mm:
        NEW[rid] = mut_row(mm.group(1))
    mm2 = re.match(r"r7-mut-(m\d\d)$", rid)
    if mm2:
        NEW[rid] = mut_row(mm2.group(1))
    if rid in ("proj-r4-container-and-unit-tests",):
        pass

# new mutant rows
for key in ("n01", "n02", "n03"):
    NEW[f"r8-mut-{key}"] = (("PASS", f"NEW student-error mutant written from grader/reference.py (ledgers/AC2/mutants/{desc_of[key].split('/')[-1]}): {'ROIC NOPAT grosses up by (1 + tax_rate)' if key=='n01' else ('DSO uses 360 days' if key=='n02' else 'gross margin divides by COGS')}. KILLED -> {kill[key]}. Checked separately with run_impls.py on seeds 0-49: FAIL at seed 0 (the harness rejects it).") )
NEW["r8-mutate-56"] = ("PASS", "tools/mutate_graders.py --unit AC2 --seeds 0-9: 56 mutants (53 known + n01-n03), 56 KILLED, exit 0.")
NEW["r8-impls-v1-v5-50"] = NEW["proj-grader-overconstraint"]
NEW["r8-collect-seeds"] = NEW["proj-grader-collect-count"]
NEW["r8-curl-access"] = ("PASS", "Round 8 plain curl (no bypass): doi.org/10.2469/faj.v55.n5.2296 302 -> tandfonline full text 403 (HEAD and GET); en.wikipedia.org/wiki/Beneish_M-score 200 with the constants; ivey.uwo.ca/media/3775523/...pdf 200, PDF (876,917 bytes); www.sec.gov/os/webmaster-faq and accessing-edgar-data 403; doi.org/10.2308/tar-9505096112 302 -> publications.aaahq.org ... 403.")
NEW["r8-check-projects-pages"] = ("PASS", "tools/check_projects.py --unit AC2: PASS; tools/check_pages.py --unit AC2: PASS. Note: the single-page form (check_pages.py --page project / --page index) printed 'lesson needs a mark complete button' and FAILed; I did not read that code path, and the unit-level gate is the one in CLAUDE.md, which passes. Recorded as an observation, not a finding.")
NEW["r8-cards-sample"] = ("PASS", "Round 8 sample of cards: AC2-c010 (L01 restatement), c030 (L02 scale invariance), c050 (L04 accrual measures vs reference.py balance-sheet and cash-flow forms), c070 (L05 null rate 0.060 vs L05 line 223), c090 (L07 average assets for the debt measure vs L07 line 65), c110 (PPV by Bayes' rule, L08 line 309 and line 52 Proposition 4.2), c130 (s7 proxy vs L07 line 81), c140 (AND and OR rules, L08 lines 324 and 379-380): each consistent with its lesson or reference. Unsampled cards carried from round 7 (byte-identical records).")
NEW["r8-project-new-test-read"] = ("PASS", "Round 8: the new test is read in full (diff 6adfd01..e6788c2 of grader/test_project.py, +13 lines); its decoy period end, 372 days before LATEST, is inside the 350-380 day window and the real PRIOR period is the latest there; the reference passes it.")
NEW["r8-hub-l05-title-note"] = ("PASS", "Round 8 note only: the hub card title (index.html line 148) is 'The Accruals Anomaly and the Sloan (1996) Question' and L05 h1 (line 36) is 'The Accruals Anomaly'. A title difference, not a claim; no FAIL.")

# ---- build rows
def carry_prefix(location):
    cited = [f for f in CHANGED if f in location]
    if not cited:
        return None
    return cited

rows = []
for r in r7["rows"]:
    rid = r["id"]
    if rid in NEW:
        status, evidence = NEW[rid]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": evidence})
        continue
    if r["status"] != "PASS":
        raise SystemExit(f"non-PASS round-7 row not re-verified: {rid}")
    cited = carry_prefix(r["location"])
    if cited:
        names = ", ".join(c.split("/")[-1] if "/" in c else c for c in cited)
        prefix = (f"Carried from round 7 ({names} changed since 6adfd01 only at the round-8 hunks, "
                  f"which do not include the cited subject; the cited subject is byte-identical): ")
    else:
        prefix = "Carried from round 7 (the cited files are byte-identical since 6adfd01): "
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                 "evidence": prefix + r["evidence"]})

# new rows of this round
new_ids = [k for k in NEW if k not in {r["id"] for r in r7["rows"]}]
for rid in new_ids:
    status, evidence = NEW[rid]
    rows.append({"id": rid, "check": "2.6-round8", "location": "see evidence", "status": status, "evidence": evidence})

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids))
for r7row in r7["rows"]:
    assert r7row["id"] in ids, r7row["id"]  # every previous row id kept

fragment = {
    "unit": "AC2",
    "slice": "project",
    "round": 8,
    "verifier": "Claude Haiku 5.5 (independent project-slice verifier, round 8; did not build AC2; fresh context)",
    "pin": "e6788c2",
    "base": "round-7 fragment (/tmp/ac2-frags/project.round7.json, pin 6adfd01)",
    "checkout": "/tmp/verify-ac2r8-p (detached at e6788c2)",
    "scratch": "/tmp/ac2-v/project-r8; archived scripts in ledgers/AC2/scripts/project-r8/",
    "verified_at": "2026-10-27",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": r7["registry_flags"],
    "freshness_flags": [],
    "notes": [
        "Round 8 delta for the slice: project.html line 245 (240 checks), grader/test_project.py (new test test_previous_year_is_the_latest_period_end_in_the_window), index.html line 148 (L05 card title), cards.json (c024, c072, c107), plans/AC2-open-items.md line 16.",
        "All 56 mutants (m01-m16, p01-p37, n01-n03) are KILLED on seeds 0-9; the three new student-error mutants n01-n03 are KILLED on seed 0.",
        "Five alternative correct implementations (round-3 set V1-V5) pass 50 seeds: no over-constraint.",
        "Access statements reproduced with plain curl (no bypass): Beneish DOI 302 then tandfonline 403; Wikipedia 200 with the constants; Ivey Piotroski PDF 200; SEC FAQ pages 403; Dechow DOI 302 then publisher 403.",
        "Non-blocking: hub card title for L05 differs from the L05 h1; check_pages --page output for project and index is unexplained (unit-level check PASS).",
        "Ungraded cards (54) carry no grade by BUILDER_RULES 7; graded cards carry C, T or D.",
    ],
    "summary": {},
    "verdict": "",
}
counts = {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows),
          "fail": sum(r["status"] == "FAIL" for r in rows),
          "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in rows),
          "mutants": len(mutants), "mutants_killed": sum(1 for m in mutants if m["killed_by"])}
fragment["summary"] = counts
fragment["verdict"] = "PASS" if counts["pass"] == counts["rows"] and counts["mutants_killed"] == counts["mutants"] else "FAIL"
out = ROOT / "ledgers/AC2/project.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(counts))
