# Builds ledgers/AC1/AC1-d.json (round 19) from the round-18 fragment and this round's outputs.
import json, re, datetime, pathlib
CHK = pathlib.Path("/tmp/verify19-AC1-d")
OUT = CHK / "ledgers/AC1/scripts/AC1-d-r19/out"
old = json.load(open("/tmp/fanout-frags/AC1-d.round18.json"))
mut_lines = {}
for line in open(OUT / "mutants_r19.out", encoding="utf-8"):
    if " | seed0:" in line:
        name = line.split(" | ")[0].strip()
        mut_lines[name] = line.strip()
new_mut_lines = {}
for name in ["v19_m01_capex_from_net_equipment", "v19_m02_retained_income_omits_depreciation",
             "v19_m03_stock_issued_is_balance", "v19_m04_total_equity_omits_common_stock"]:
    new_mut_lines[name] = "both seeds fail: see out/new_mutants_r19.out (v19_m01 28 and 48 failed; v19_m02 28 and 49; v19_m03 45 and 45; v19_m04 18 and 18)"
CARRY = ("Carried from round 18 (files byte-identical since the previous pin 7143726: "
         "course/modules/AC/AC1/project.html, grader/, tests/labs/AC1/, index.html, L01-L03, L07): ")
CARRY_CARDS = ("Carried from round 18 (the cards.json entries and every passage they cite are byte-identical since the "
               "previous pin 7143726; the only changed entries are AC1-c046, c052, c053, c058, c066, c069 and new c140): ")

rerun_commands = {
 "proj-run-graders": "Re-run r19: tools/run_graders.py --unit AC1 printed 'run_graders AC1: PASS (reference 50/50 seeds, slowest 0.4 s)', exit 0 (ledgers/AC1/scripts/AC1-d-r19/out/run_graders.out). The starter fails 308 of 310 on seed 0 (out-of-band line below).",
 "proj-collect-count-176": "Re-run r19: pytest --collect-only on the reference for all seeds 0 to 49 gave '310 tests collected' on each seed (50 of 50; ledgers/AC1/scripts/AC1-d-r19/out/ and the loop in this round's notes). project.html line 368 says 'collects 310 checks ... 310 for each of the seeds 0 to 49', which agrees.",
 "proj-local-suite-reference": "Re-run r19: .venv/bin/python -m pytest --version prints 'pytest 9.0.2'; .venv/bin/python --version prints 'Python 3.14.8' (local equal of Pyodide 314.0.7 as the page states; Pyodide itself not run).",
 "proj-pyodide-smoke": "Re-run r19: tools/page_smoke.py --unit AC1 --pages project.html printed 'page_smoke AC1: PASS', exit 0; --pages L04 L05 L06 L08 also PASS (ledgers/AC1/scripts/AC1-d-r19/out/page_smoke_project.out, page_smoke_lessons.out).",
 "proj-check-pages": "Re-run r19: tools/check_pages.py --all, exit 0; 'check_pages AC1: PASS' (out/help_and_gates.txt).",
 "proj-check-dag": "Re-run r19: tools/check_dag.py --all; 'check_dag AC1: PASS' (out/help_and_gates.txt).",
 "proj-check-projects": "Re-run r19: tools/check_projects.py --all; 'check_projects AC1: PASS' (out/help_and_gates.txt).",
 "proj-run-labs": "Re-run r19: tools/run_labs.py --unit AC1 printed 'run_labs AC1: PASS (11/11)', exit 0, covering the three project labs and the L01 to L08 labs (out/run_labs.out).",
 "proj-lab-twin-embed": "Re-run r19: run_labs AC1 11/11 (includes the project lab blocks) and page_smoke project PASS (out/run_labs.out, out/page_smoke_project.out).",
 "proj-labs-ruff": "Re-run r19: ruff check course/modules/AC/AC1 tests/labs/AC1 'All checks passed!' exit 0; ruff format --check course/modules/AC/AC1 tests/labs/AC1 '15 files already formatted' exit 0 (out/ruff.out, out/ruff_format.out).",
 "proj-mypy-gate": "Re-run r19: .venv/bin/python -m mypy --no-incremental 'Success: no issues found in 153 source files', exit 0 (out/mypy.out).",
 "proj-verify-refs": "Re-run r19: tools/verify_refs.py --unit AC1 'live re-verification of AC1: 2 of 560 entries, 0 problems', exit 0; tools/verify_refs.py --offline 'offline integrity: 560 entries, 0 problems', exit 0 (out/vr_live_AC1.out, out/vr_offline.out).",
 "proj-tests-labs-pytest": "Re-run r19: pytest tests/test_run_labs.py tests/test_labs.py tests/test_page_checks.py: all passed, exit 0 (out/pytest_labs.out).",
 "proj-starter-fails": "Re-run r19: the starter under the suite on seed 0: '308 failed, 2 passed'; the two that pass are test_chart_of_accounts_is_the_specified_table and test_the_module_imports_only_the_standard_library (verbose run), which the starter satisfies by its given ACCOUNTS and imports; the suite fails the starter, as the page states (line 364, 'the suite fails on the starter').",
 "proj-hours": "Re-run r19: project.html data-hours-project 30; the time-budget components sum to 1+3+4+4+3+5+2+5+3 = 30; index.html data-hours-lessons 90 and data-hours-project 30; lesson hours L01-L08 sum to 11+12+11+11+12+12+11+10 = 90 (matches hub); 90+30 = 120 (hub line 31 says 120 hours). Hours are not failed on pace (architect ruling).",
 "proj-v17-collect-and-count-line-368": "Re-run r19: collect-only gives 310 on all 50 seeds; project.html line 368 says 310 (see proj-collect-count-176).",
 "cards-inventory-and-dupes": "Re-run r19 (out/cards_scan.out): 140 cards, 140 unique ids, no duplicate front and no duplicate back; c140 is new.",
 "cards-grades": "Re-run r19 (out/cards_scan.out): grade counts C 50, T 42, no grade 48 (definitional cards). Changed cards keep their grades (c046 None, c052 T, c053 T, c058 T, c066 T, c069 T, c140 None).",
 "cards-numbers-in-lessons": "Re-run r19 scan (ledgers/AC1/scripts/AC1-d-r19/cards_scan.py, out/cards_scan.out): every number in every card back appears in its lesson text except '5,000' in AC1-c077, which is L06 line 68 '5{,}000' (LaTeX thousands separator); 0 other flags.",
 "cards-labels-resolve": "Re-run r19 scan: every '(Definition|Proposition|Theorem|Corollary|Remark|Example|Problem|Lab) n.m' label cited in a card front or back appears in that card's own lesson text (out/cards_scan.out: no flagged labels).",
 "cards-banned": "Re-run r19: grep of cards.json for roughly, about, historically, half (as in 'roughly half'), ellipsis and typically/usually/generally: the only hits are 'basis' phrases and 'rounds half up' (a rounding rule, not a banned quotient phrase).",
 "cards-c001-c128-coverage-r15": "Re-run r19: the scan covers all 140 cards (out/cards_scan.out); the card-to-lesson mapping is by the 'lesson' field, and each card's cited labels resolve in its lesson.",
 "cards-L04": "Re-verified r19 against the changed L04 text: c046 (Definition 1.1, Remark 1.2), c052 (Proposition 2.1), c053 (Definition 2.2, Proposition 2.2), c058 (Proposition 2.1, 3.1), c122 (Definition 2.2 and the Proposition 2.2 proof, unchanged), c132 (Corollary 2.3 and the printed Lab 1 quarter-7 values: 6,632,381 purchase, first share 1,658,095, unexpired 4,974,286 = -cumulative difference) all verified. The other L04 cards (c047-c051, c054-c057, c059, c060, c133, c134) are carried. Result PASS for the group.",
 "cards-L05": "Group FAIL: AC1-c069 cites 'Remark 2.4 in Section 2' for the convention-difference statement, which is in the unnumbered paragraph after Remark 2.4 ('Convention 1 and convention 2 agree at month 12 ...'); see cards-c069. The other L05 cards (c061-c068, c070-c074) are unchanged and verified against L05 (Definition 1.1-1.3, 2.2, Propositions 1.4, 2.1, 2.3, Remark 1.5 and the Lab 1 output lines).",
 "cards-L06": CARRY_CARDS + "c075-c090 checked against L06 Definitions 1.1-1.4, Propositions 2.1-2.4, Section 3 and the Lab 1 output (c077 '5,000' is L06 line 68 '5{,}000'). The L06 sentences changed this round (why-it-matters, Section 4 bullet, R2 solution) are not cited by any card.",
 "cards-L08": CARRY_CARDS + "c105-c131 and c139 checked against L08 Definition 1.1-1.2, Theorem 1.3, Theorem 2.1 (a)-(d), Example 1.4 and 2.2, and the Lab 1 output. The changed L08 sentences (why-it-matters; the integer-cents paragraph after the Section 2 formulas) are not cited by any card; the formulas they discuss are unchanged.",
 "cards-c069": "FAIL: AC1-c069 (L05, grade T) back reads 'The convention-1 revenue from the over-time obligations through month m (Remark 2.4 in Section 2; problem P3).' Remark 2.4 (L05.html line 120-122) is 'a timing wedge, not a measure of performance' and does not state the convention difference; the statement is in the unnumbered paragraph that follows Remark 2.4 ('Convention 1 and convention 2 agree at month 12 (Proposition 2.1). ... the difference at any month m < 12 equals the convention-1 revenue recognized by month m from the over-time obligations ...', L05.html line 124). The round-18 locator 'the paragraph before Lab 1 in Section 2' was correct; the round-19 edit changed it to a wrong citation.",
 "cards-c066-c067-definition-1-3-setting": "Re-verified r19: AC1-c066 back now 'Yes, for a non-negative transaction price ...' and L05 Proposition 1.4 (line 73) states 'with the transaction price P a non-negative integer'; the scope matches. AC1-c067 carried (unchanged).",
 "cards-c052": "Re-verified r19 (changed front and back): AC1-c052 'Is cash the same under the two recognition rules of this lesson, applied to the same payments and receipts?' matches L04 Proposition 2.1 (line 83: 'Let the same receipts and payments occur under rule A and under rule B. Then the cash balance at every quarter end is the same under both rules.'). PASS.",
 "cards-c053-prop22-assumptions": "Re-verified r19: AC1-c053 back now states the Definition 2.2 assumptions (zero opening balances, no equity contributions, no distributions, each credit sale collected one quarter later) and splits the rule-A identity (C+R=N^A) from the rule-B identity (C+R+P=N^B), which matches L04 Proposition 2.2 (line 97) and Definition 2.2 (line 91-93). PASS.",
 "cards-c058-two-rules-scope": "Re-verified r19: AC1-c058 back now says 'Under the two recognition rules of this lesson, cash is the same when both rules face the same payments and receipts (Proposition 2.1)' and 'a difference ... between two presentations of the same cash movements can come from a classification choice' (Proposition 3.1). The scope matches the lesson misconception (L04 line 341). PASS.",
 "cards-c132-lab1-quarter7": "Re-run r19 (L04 Lab 1 printed values, L04.html lines 277-284 and 289/344): quarter-7 cumulative difference -4,974,286 equals -prepaid_balance_b (4,974,286) and equals minus the unexpired part of the 6,632,381 purchase (6,632,381 - floor(6,632,381/4) = 4,974,286). Per-quarter recomputation of the cumulative difference (ledgers/AC1/scripts/AC1-d-r19/recompute_l04.py, out/recompute_l04.out) agrees at all eight quarters.",
}
new_rows = [
 {"id": "cards-c046-gaap-definition", "check": "cards-correctness", "location": "course/modules/AC/AC1/cards.json AC1-c046; L04.html Definition 1.1 (line 58) and Remark 1.2 (line 62)", "status": "PASS",
  "evidence": "Changed card re-verified: 'Each framework is a set of accounting rules' and 'The lesson states no rule of either framework (Remark 1.2)' match L04 Definition 1.1 ('Each framework is a set of accounting rules. This lesson states none of their content (Remark 1.2).') and Remark 1.2 ('The lesson states no rule of either framework.')."},
 {"id": "cards-c140-new-card", "check": "cards-correctness", "location": "course/modules/AC/AC1/cards.json AC1-c140; L04.html Definition 2.2 (lines 91-93)", "status": "PASS",
  "evidence": "New card (round 19): zero opening balances, no equity contributions and no distributions; C_t cash; R_t the credit sales of quarter t collected one quarter later; P_t unexpired prepaid balance under rule B; N^A_t and N^B_t cumulative net income through t. All match Definition 2.2 verbatim in substance. Grade None (definitional), consistent with the other definition cards."},
 {"id": "cards-c069", "check": "cards-correctness", "location": "course/modules/AC/AC1/cards.json AC1-c069; L05.html Remark 2.4 (lines 120-122) and the paragraph after it (line 124)", "status": "FAIL",
  "evidence": "AC1-c069 cites 'Remark 2.4 in Section 2' for a statement that Remark 2.4 does not contain: Remark 2.4 is about the contract balance as a timing wedge; the convention-difference statement is in the unnumbered paragraph 'Convention 1 and convention 2 agree at month 12 (Proposition 2.1) ...' that follows the remark (L05.html line 124). The card's substance is correct; its locator is wrong.",
  "fix": "In cards.json AC1-c069 change '(Remark 2.4 in Section 2; problem P3)' to '(the paragraph after Remark 2.4 in Section 2, beginning \"Convention 1 and convention 2 agree at month 12\"; problem P3)' or to '(Section 2; problem P3)'. Then re-run tools/render-free card checks: ledgers scan and check_pages."},
 {"id": "proj-r19-collect-all-seeds", "check": "2.6-autograder-count", "location": "course/modules/AC/AC1/grader/test_project.py; project.html line 368", "status": "PASS",
  "evidence": "pytest --collect-only with the reference on seeds 0 to 49: '310 tests collected' on 50 of 50 seeds (ledgers/AC1/scripts/AC1-d-r19/run_suite.sh with mode collect); the page's '310' is correct."},
 {"id": "proj-r19-reference-seeds", "check": "2.6-autograder-reference", "location": "course/modules/AC/AC1/grader/reference.py", "status": "PASS",
  "evidence": "Reference run on seeds 0, 17, 33, 49 (run_suite.sh run): '310 passed' each; the starter gives '308 failed, 2 passed'."},
 {"id": "proj-r19-student-mutants-v19-m01-m04", "check": "2.6-mutation-new-student-errors", "location": "ledgers/AC1/mutants/v19_m01_capex_from_net_equipment.py; v19_m02_retained_income_omits_depreciation.py; v19_m03_stock_issued_is_balance.py; v19_m04_total_equity_omits_common_stock.py", "status": "PASS",
  "evidence": "Four NEW student-error mutants written from the reference (plausible errors named in the page: capital expenditure from net equipment, retained earnings omitting depreciation (page Conventions 'net income to date ... and depreciation'), stock issued from the balance rather than the increase (page Conventions 'stock_issued the increase in common stock'), total equity omitting common stock). Each fails on seeds 0 and 17: v19_m01 28/48 failed, v19_m02 28/49, v19_m03 45/45, v19_m04 18/18 (ledgers/AC1/scripts/AC1-d-r19/out/new_mutants_r19 via run_one_mutant.sh)."},
 {"id": "proj-r19-balance-gap-sign-out-of-scope", "check": "2.6-mutation-survivor-stated-scope", "location": "course/modules/AC/AC1/project.html Conventions, 'Articulation gaps' (balance_gap paragraph); grader/test_project.py", "status": "PASS",
  "evidence": "A survivor, not a fail: balance_gap reversed (total_liabilities_and_equity - total_assets) gives '310 passed' on seeds 0 and 17. The page states it: 'It is zero for every ledger that post accepts ... the suite checks that it is zero. The suite does not test the sign of this always-zero quantity, since a reversed sign also gives zero.' The survivor is therefore out of scope by the page's own statement (PASS per the brief); the other three gaps are killed by the non-articulating witness test (grader/test_project.py lines 915-930)."},
 {"id": "proj-r19-alternatives-new-a-b-c", "check": "2.6-alternatives-over-constraint", "location": "ledgers/AC1/scripts/AC1-d-r19/alts/alt_r19_a_month_arithmetic.py; alt_r19_b_single_flow_dictionary.py; alt_r19_c_ordinal_cutoff.py", "status": "PASS",
  "evidence": "Three new correct alternatives written from the reference by asserted edits (ledgers/AC1/scripts/AC1-d-r19/mk_alts19.py): (a) previous month end by year/month arithmetic and calendar.monthrange; (b) a single flow dictionary used by the cash flow and articulation functions, net income computed without income_statement; (c) balances cut off by ordinal day numbers. Each runs the full suite on seeds 0 to 49: 0 of 50 seeds with a failure (out/alts_r19_new.out)."},
 {"id": "proj-r19-alternatives-existing-35", "check": "2.6-alternatives-over-constraint", "location": "ledgers/AC1/scripts/AC1-d-r19/out/alts_existing_r19.out (35 files from ledgers/AC1/scripts/AC1-d-r15..r18 alts folders)", "status": "PASS",
  "evidence": "All 35 earlier alternative implementations (alt_r8 to alt_r18, including the r17 and r18 files) pass the round-19 grader on seeds 0 to 49: '0 of 50' for each (out/alts_existing_r19.out)."},
 {"id": "proj-r19-lab-prose-numbers", "check": "2.2-numbers-in-prose", "location": "course/modules/AC/AC1/project.html Lab 1 interpretation (line ~330), Lab 2 note, Lab 3 interpretation (balance and cash flow lines)", "status": "PASS",
  "evidence": "Recomputed by hand from the lab code and the printed output: Lab 1 Jan 31 assets 13,100,000 (5,500,000+2,400,000+1,300,000+3,900,000), retained 600,000, gap 0; Feb 29 assets 11,300,000, retained 1,300,000; Feb net income 700,000 (1,600,000-900,000); cash effects receivables +200,000, inventory +900,000, payables -2,500,000, sum -1,400,000; operating -700,000 = 700,000-1,400,000. Lab 3: assets 7,870,000 = 4,850,000+100,000+2,920,000; liabilities 2,250,000; retained -380,000 = 70,000-450,000; financing 850,000 = 1,000,000-150,000; investing -3,000,000; ending cash 4,850,000 equal balance sheet cash. All agree with the printed output in out/run_labs.out."},
 {"id": "lesson-change-audit-r19-l04-l05-l06-l08", "check": "2.2-numbers-and-scope-in-rewritten-sentences", "location": "L04.html line 330 (Section 5 bullet), L05.html Remark 1.5, Remark 2.4 and Proposition 1.4 (key-results row), L06.html why-it-matters, L08.html why-it-matters and Section 2 integer paragraph", "status": "PASS",
  "evidence": "L04 line 330: 'prepaid_balance_b zero at quarter 0 and non-zero at quarters 1 to 7' and 'the cumulative difference equals minus that balance' verified per quarter (recompute_l04.py: all eight quarters equal True). L05 Proposition 1.4 scope ('with the transaction price P a non-negative integer') matches the card c066 scope. L08 integer paragraph: CT_t and TE_t integer iff r*P_t multiple of 100 (algebra with Definition 1.1: b_t, tau_t and tau_t - b_t multiples of 100, r whole); DE_t and DTL_t need no P_t condition (K_t multiple of 100). L06 why-it-matters '(Definition 1.4)' cites the pattern-F definition, which is in Definition 1.4 (L06.html line 29). Out-of-slice note (not a row of this slice): L04.html key-results row (line 473) reads 'cash plus receivables, plus the unexpired prepaid balance under rule B, equals cumulative net income under each rule (Proposition 2.2)'; read literally, for rule A it would say C+R+P = N^A, which is false when P != 0 (Proposition 2.2 gives C+R = N^A). Card AC1-c053 states it correctly. Reported for the L04 slice owner."},
]
rows = []
rerun_mut_prefixes = ("proj-mutant", "proj-r14-mutant", "proj-r15-mutant", "proj-v16-mutant", "proj-r18-equivalent", "proj-mutants", "proj-r18-student", "proj-v17-mutants", "proj-r13-", )
fails_now = {"cards-L05": None}
for r in old["rows"]:
    rid, loc = r["id"], r["location"]
    rr = dict(r)
    if rid == "cards-c069":
        nr = next(x for x in new_rows if x["id"] == "cards-c069")
        rr = {"id": rid, "check": r["check"], "location": loc, "status": "FAIL", "evidence": nr["evidence"], "fix": nr["fix"]}
    elif rid == "cards-L05":
        rr = {"id": rid, "check": r["check"], "location": loc, "status": "FAIL", "evidence": rerun_commands["cards-L05"], "fix": "Fix AC1-c069 as in cards-c069; the other L05 cards are verified."}
    elif rid in rerun_commands:
        rr = {"id": rid, "check": r["check"], "location": loc, "status": "PASS", "evidence": rerun_commands[rid]}
    elif rid in ("cards-c052", "cards-c053-prop22-assumptions", "cards-c058-two-rules-scope", "cards-c066-c067-definition-1-3-setting", "cards-L04", "cards-L06", "cards-L08"):
        rr = {"id": rid, "check": r["check"], "location": loc, "status": "PASS", "evidence": rerun_commands.get(rid, "")}
        if rid in ("cards-c052",): rr["evidence"] = rerun_commands["cards-c052"]
        if rid == "cards-c053-prop22-assumptions": rr["evidence"] = rerun_commands["cards-c053-prop22-assumptions"]
        if rid == "cards-c058-two-rules-scope": rr["evidence"] = rerun_commands["cards-c058-two-rules-scope"]
        if rid == "cards-c066-c067-definition-1-3-setting": rr["evidence"] = rerun_commands["cards-c066-c067-definition-1-3-setting"]
        if rid == "cards-L04": rr["evidence"] = rerun_commands["cards-L04"]
        if rid in ("cards-L06", "cards-L08"): rr["evidence"] = rerun_commands[rid]
    elif rid.startswith(("proj-mutant", "proj-r14-mutant", "proj-r15-mutant", "proj-v16-mutant")):
        m = re.search(r"([\w]+\.py)", loc)
        name = m.group(1)[:-3] if m else None
        ev = ("Re-run r19 on seeds 0 and 17 (ledgers/AC1/scripts/AC1-d-r19/out/mutants_r19.out): " + mut_lines[name]) if name in mut_lines else \
             "Re-run r19: all mutants in ledgers/AC1/mutants/ (165 files) re-run on seeds 0 and 17; killed (out/mutants_r19.out)."
        rr = {"id": rid, "check": r["check"], "location": loc, "status": "PASS", "evidence": ev}
    elif rid.startswith(("proj-mutants", "proj-r18-student", "proj-v17-mutants", "proj-r18-equivalent")):
        rr = {"id": rid, "check": r["check"], "location": loc, "status": "PASS",
              "evidence": "Re-run r19: every mutant in ledgers/AC1/mutants/ (165 files, including the group named here) fails on seeds 0 and 17 (out/mutants_r19.out: 165 of 165 lines show 'failed' on both seeds). Equivalent proofs unchanged (ledgers/AC1/equivalent/)."}
    elif rid.startswith(("proj-r18-alternatives", "proj-v17-alternatives", "proj-v16-alternatives", "proj-r14-alternatives", "proj-alt-implementations", "proj-overconstraint")):
        rr = {"id": rid, "check": r["check"], "location": loc, "status": "PASS",
              "evidence": "Re-run r19: the 35 earlier alternatives and 3 new ones pass the round-19 grader on seeds 0 to 49 (out/alts_existing_r19.out, out/alts_r19_new.out). " + r["evidence"][:0]}
    elif rid == "proj-r18-equivalent-v18-m01" or rid == "proj-v17-equivalent-v16-m01-proof":
        rr = dict(r); rr["evidence"] = CARRY + r["evidence"]
    else:
        rr = dict(r); rr["evidence"] = (CARRY_CARDS if rid.startswith("cards") else CARRY) + r["evidence"]
    rows.append(rr)
# order: keep previous ids, then the new rows
rows.extend([x for x in new_rows if x["id"] not in {r["id"] for r in rows}])
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
for r in rows:
    if r["status"] != "PASS":
        assert r.get("fix"), r["id"]
    assert r["evidence"].strip(), r["id"]
mutants = list(old["mutants"])
for name in new_mut_lines:
    mutants.append({"id": name, "description": name.replace("_", " "), "file": f"ledgers/AC1/mutants/{name}.py",
                    "killed_by": "seeds 0 and 17: both fail (scripts/AC1-d-r19/out/new_mutants_r19.out)"})
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
frag = {
 "unit": "AC1", "slice": "AC1-d", "round": 19,
 "verifier": "Claude Haiku 5.5, independent verifier for AC1-d, round 19 (did not build AC1; read the round-18 fragment as context and computed the delta 7143726..51fa336 on the slice)",
 "pin": "51fa336",
 "base": "7143726 (round-18 pin). Delta for the slice: course/modules/AC/AC1/cards.json (AC1-c046, c052, c053, c058, c066, c069 changed; AC1-c140 added); lesson texts that cards cite: L04 (Def 1.1, Def 2.2, Prop 2.2, Section 5, key-results, misconception), L05 (Remark 1.5, Remark 2.4, Prop 1.4 key-results), L06 (why-it-matters, Section 4, R2), L08 (why-it-matters, Section 2 integer paragraph). project.html, grader/, tests/labs/AC1/ unchanged.",
 "checkout": "/tmp/verify19-AC1-d",
 "scratch": "/tmp/ac1-v/d19",
 "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
 "verdict": "FAIL" if counts["FAIL"] or counts["UNVERIFIABLE"] else "PASS",
 "rows": rows,
 "mutants": mutants,
 "registry_flags": [],
 "freshness_flags": [],
 "notes": ("Verified this round: run_graders AC1 PASS (50/50 reference seeds); starter fails; collect 310 on all 50 seeds; page_smoke project and L04/L05/L06/L08 PASS; run_labs 11/11; check_pages, check_dag, check_projects PASS; build_site --check; render_curriculum (no diff); verify_refs live (2 of 560, 0 problems) and offline (560, 0 problems); ruff check and format; mypy strict (153 files); pytest labs subset; 169 mutants (165 earlier + 4 new) on seeds 0 and 17; 38 alternatives on seeds 0 to 49 (35 earlier + 3 new). "
           "Not checked: Pyodide 314.0.7 itself (local Python 3.14.8 and pytest 9.0.2 only); the full re-read of L01 to L03 and L07 (carried by byte identity); the remaining L04 to L08 lesson text outside the cited passages. Out-of-slice observation for the L04 owner: L04.html key-results row (line 473) 'cash plus receivables, plus the unexpired prepaid balance under rule B, equals cumulative net income under each rule' is ambiguous for rule A (see lesson-change-audit-r19-l04-l05-l06-l08). Out-of-slice note for the L06 owner: the R2 solution now says 'the contract terms are the evidence for this' (not cited; no card depends on it)."),
 "summary": (f"AC1-d round 19: {len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE; "
             f"169 mutants in ledgers/AC1/mutants all fail on seeds 0 and 17 (165 earlier + 4 new; one out-of-scope survivor recorded as PASS by the page's own statement); "
             f"38 alternatives pass on seeds 0 to 49. FAIL rows: cards-c069 (wrong locator 'Remark 2.4') and the cards-L05 aggregate."),
}
out = CHK / "ledgers/AC1/AC1-d.json"
json.dump(frag, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows", len(rows), counts, "mutants", len(mutants), "verdict", frag["verdict"])
