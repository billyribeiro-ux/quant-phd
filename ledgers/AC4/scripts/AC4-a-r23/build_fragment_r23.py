"""Round 23 AC4-a fragment builder: carries round-22 rows whose cited subjects are unchanged, overrides re-run and changed rows."""
import json, sys
from pathlib import Path

ROOT = Path(sys.argv[1])
prev = json.loads(Path("/tmp/fanout-frags/AC4-a.round22.json").read_text(encoding="utf-8"))
CARRY = ("Carried from round 22 (course/modules/AC/AC4/index.html, L01.html, L02.html and tests/labs/AC4/ byte-identical "
         "since the previous pin d160ac3; cards.json changed only at c020, c037, c095, c108, c113 and by additions c135 to c140, "
         "none of them cited by this row): ")
OUT = "ledgers/AC4/scripts/AC4-a-r23/out/"

def body(ev):
    if ev.startswith("Carried from round 21 ("):
        return ev[ev.index("): ") + 3:]
    if ev.startswith("Carried from round 22 ("):
        return ev[ev.index("): ") + 3:]
    return ev

RERUN = {
 "AC4-a-cmd-check-pages": "Re-run round 23: tools/check_pages.py --unit AC4 rc=0, 'check_pages AC4: PASS' (out/check_pages.out).",
 "AC4-a-cmd-check-dag": "Re-run round 23: tools/check_dag.py --all rc=0; 'check_dag AC4: PASS' among the units (out/check_dag.out).",
 "AC4-a-r19-cmd-check-projects": "Re-run round 23: tools/check_projects.py --unit AC4 rc=0, 'check_projects AC4: PASS' (out/check_projects.out).",
 "AC4-a-cmd-run-labs": "Re-run round 23: tools/run_labs.py --unit AC4 rc=0, 'run_labs AC4: PASS (10/10)' (out/run_labs.out).",
 "AC4-a-cmd-twins-isolated": "Re-run round 23: python -I -W error on lab-AC4-L01-1.py and lab-AC4-L02-1.py: rc=0, stderr empty (out/twin_L01.out, out/twin_L02.err, out/twin_L02.out).",
 "AC4-a-cmd-twin-output-equals-page": "Re-run round 23 by ledgers/AC4/scripts/AC4-a-r23/check_twins_cards.py (out/twins_cards.out): L01 20 of 20 lines equal the embedded block at L01.html:222-241; L02 13 of 13 lines equal the block at L02.html:251-263.",
 "AC4-a-cmd-page-smoke": "Re-run round 23: tools/page_smoke.py --unit AC4 --pages index.html L01.html L02.html rc=0, 'page_smoke AC4: PASS' (out/page_smoke.out).",
 "AC4-a-cmd-pytest-labs-lint": "Re-run round 23: pytest -q -k AC4 rc=0, 10 dots (out/pytest_ac4.out); ruff check tests/labs/AC4 'All checks passed!'; ruff format --check '10 files already formatted' (out/ruff_check.out, out/ruff_format.out).",
 "AC4-a-cmd-verify-refs": "Re-run round 23: tools/verify_refs.py --unit AC4 rc=0 'live re-verification of AC4: 2 of 560 entries, 0 problems'; tools/verify_refs.py --offline rc=0 'offline integrity: 560 entries, 0 problems' (out/verify_refs_live_AC4.out, out/verify_refs_offline.out).",
 "AC4-a-r18-cmd-build-site-check": "Re-run round 23 on the changed cards.json: tools/build_site.py --check rc=0, 'site data current: 6 outputs' (out/build_site_check.out).",
 "AC4-a-banned-phrases": "Re-run round 23: grep -n -i -E 'roughly|about [0-9]|historically|typically|usually|generally|often|in general|\\.\\.\\.|…|verif|round [0-9]|builder|unit report' on index.html, L01.html, L02.html: no hits (exit 1 from grep means none).",
 "AC4-a-r21-indep-recompute": "Re-run round 23: ledgers/AC4/scripts/AC4-a-r21/indep_recompute_r21.py rc=0 (out/indep_recompute_r21.out): 'R3 max abs error USD 3990 at hours [1, 401, 801] ratio 0.9975'; 'E1 run lengths 89 88'; 'DOL 6.081081'; '100 USD fixed rise moves break-even 7.407407'; 'dispersed -6.130268'; 'oi2000 USD 25800.0 oi2001 USD -1186.5'; 'zero check any integer oi==0 []'.",
 "AC4-a-r18-mutants-labs": "Re-run round 23 (ledgers/AC4/scripts/AC4-a-r23/run_mutants_r23.py, out/mutants_r23.out): 27 committed lab-twin mutants (r18 10, r19 5, r20 3, r21 6, r22 3): 23 KILLED (nonzero exit or stdout differs), 4 SURVIVED with stdout identical and rc=0 (AC4-a-r21/L01_p01, L02_p03, L02_p04; AC4-a-r22/L01_q01), recorded as equivalent or out of scope (see mutants).",
 "AC4-a-r21-new-mutants": "Re-run round 23 (out/mutants_r23.out): AC4-a-r21/L01_p01 SURVIVED (equivalent on this input); L01_p02 KILLED; L02_p01, L02_p02 KILLED; L02_p03 SURVIVED (equivalent on this input); L02_p04 SURVIVED (no integer volume has OI exactly 0). Same classes as round 22.",
}

rows = []
for r in prev["rows"]:
    rid = r["id"]
    row = dict(id=rid, check=r["check"], location=r["location"], status=r["status"], evidence=r["evidence"])
    if rid in RERUN:
        row["evidence"] = RERUN[rid]
    elif rid == "AC4-a-cards-L01-L02":
        row["status"] = "FAIL"
        row["location"] = "course/modules/AC/AC4/cards.json (39 L01 and L02 cards: AC4-c001 to c030, c118 to c120, c125, c127, c128, c130, c132, c135)"
        row["evidence"] = ("Round 23: 38 of the 39 cards are byte-identical to d160ac3; AC4-c020 was rewritten and re-checked (row AC4-a-r23-card-c020, PASS); "
                           "AC4-c135 is new and fails its scope (row AC4-a-r23-card-c135). Set and ids verified by ledgers/AC4/scripts/AC4-a-r23/check_twins_cards.py (out/twins_cards.out).")
        row["fix"] = "Fix AC4-c135 as stated in AC4-a-r23-card-c135."
    elif rid == "AC4-a-L02-misconceptions":
        row["status"] = "FAIL"
        row["location"] = "course/modules/AC/AC4/L02.html:311 (misconception 3, sentence 'In a segment where Proposition 4.1 gives a zero ...')"
        row["evidence"] = ("Round 23 re-read: the sentence states that operating income is non-negative exactly when the plan's volume is at or above the segment's zero, with no restriction to volumes inside that segment. "
                           "Read with the lower segment's zero (88.89, Lab 1 output line 'single_formula_break_even_units 88.89'), volume 2,001 is at or above 88.89 but operating income there is -1,186.50 USD (Lab 1 output 'check' and the 2,001 example at L02.html:311 itself), so the unrestricted reading is false. The other three misconceptions and the rest of the section are unchanged and were re-read at L02.html:300-317 (Prop 2.2, Prop 4.1, Def 2.1 claims hold).")
        row["fix"] = "Replace 'a plan's operating income is non-negative exactly when its volume is at or above that zero' with 'within that segment, a plan's operating income is non-negative exactly when its volume is at or above that segment's zero'."
    else:
        row["evidence"] = CARRY + body(r["evidence"])
    rows.append(row)

rows.append(dict(id="AC4-a-r23-delta-scan", check="delta d160ac3..503d139 for the slice (git diff --stat, git diff -- course/modules/AC/AC4 tests/labs/AC4)",
    location="course/modules/AC/AC4/cards.json; L07.html and L08.html (other slices); index.html, L01.html, L02.html, tests/labs/AC4 unchanged",
    status="PASS",
    evidence="git diff --stat d160ac3 503d139 lists no change to AC4/index.html, L01.html, L02.html or tests/labs/AC4/. In my slice the only changes are cards.json: AC4-c020 text shortened (Prop 4.1 sentence removed), AC4-c135 added (L02). Other card changes (c037, c095, c108, c113) and L03, L07, L08 hunks belong to other slices and were not judged here. Output saved as ledgers/AC4/scripts/AC4-a-r23/out/delta.out."))

rows.append(dict(id="AC4-a-r23-card-c020", check="card AC4-c020 (L02) against L02 Lab 1 output and Prop 4.1",
    location="course/modules/AC/AC4/cards.json AC4-c020; L02.html:173 (lab docstring), output lines 'loss run units 2001 to 2088' and 'check operating_income(88) -12.00 operating_income(89) 1.50'",
    status="PASS",
    evidence="Back: 'False. In Lab 1 a plan at 2,001 units is above the first break-even of 88.89 units and loses money, because the step applies to every unit above 2,000 units.' Output: single_formula_break_even_units 88.89; loss run units 2001 to 2088; operating_income(2001) = 1350*2001 - 120000 - 2700000 = -118650 cents = -1,186.50 USD (recomputed in out/indep_recompute_r21.out). 'every unit above 2,000' is read as every volume above 2,000 (the step is one lump of 27,000 USD at any volume above 2,000, not a per-unit charge; L02.html:173 and E1 at L02.html:380 use the same meaning). Basis Lab 1 (SIMULATED), grade C, correct. The removed Prop 4.1 sentence now sits in AC4-c135."))

rows.append(dict(id="AC4-a-r23-card-c135", check="new card AC4-c135 (L02, grade T) against Proposition 4.1 and the Lab 1 output",
    location="course/modules/AC/AC4/cards.json AC4-c135; L02.html:120-128 (Prop 4.1)",
    status="FAIL",
    evidence="Front: 'In a segment that has a zero, when is operating income non-negative?' Back: 'Exactly when the volume is at or above that segment's zero (Proposition 4.1).' Prop 4.1 gives strict increase within each segment and at most one zero, so the equivalence holds for volumes inside that segment. The back states it for 'the volume' with no restriction to the segment: the lower segment's zero is 88.89 and Lab 1 gives operating income -1,186.50 USD at 2,001 units, a volume at or above 88.89 that lies outside that segment. The grade T is correct for the in-segment statement.",
    fix="Back: 'Within that segment, exactly when the volume is at or above that segment's zero (Proposition 4.1).' Keep grade T."))

rows.append(dict(id="AC4-a-r23-mutants-new", check="three new student-error lab-twin mutants of L02 (ledgers/AC4/mutants/AC4-a-r23/)",
    location="ledgers/AC4/mutants/AC4-a-r23/L02_s01_share_over_break_even.py, L02_s02_step_at_or_above_2000.py, L02_s03_sensitivity_truncated.py",
    status="PASS",
    evidence="Run by ledgers/AC4/scripts/AC4-a-r23/run_mutants_r23.py (out/mutants_new_r23.out): s01 (share of plan over the upper break-even) prints share_of_planned 19.68 vs 16.44: KILLED. s02 (step from 2,000 inclusive) prints loss run units 2000 to 2088: KILLED. s03 (sensitivity truncated, not rounded) prints 7.40 vs 7.41: KILLED. Lab mutants are demonstrations; these kills show the printed claims are sensitive to the stated conventions."))

rows.append(dict(id="AC4-a-r23-mutants-committed", check="every committed AC4-a lab-twin mutant re-run (r18 to r22)",
    location="ledgers/AC4/mutants/AC4-a-r18 .. AC4-a-r22 (27 files); out/mutants_r23.out",
    status="PASS",
    evidence="Re-run under python -I -W error against the unmutated twin stdout: 23 KILLED, 4 SURVIVED (stdout identical, rc=0): AC4-a-r21/L01_p01_high_chosen_by_cost, AC4-a-r21/L02_p03_first_whole_unit_by_round, AC4-a-r21/L02_p04_zero_counted_as_loss, AC4-a-r22/L01_q01_residual_uses_low_month_only. Per the architect ruling on lab mutants these are out of scope unless a lesson sentence claims the lab checks the property; none does (L02 Remark 2.3 says only that Lab 1 prints both values; the zero case is not claimed). Recorded as equivalent on this input (PASS)."))

mutants = [
 {"id": "AC4-a-r18..r22 (27 committed lab-twin mutants)", "description": "committed lab-twin mutants of L01 and L02 (ledgers/AC4/mutants/AC4-a-r18..r22)", "killed_by": "23 KILLED (nonzero exit or stdout differs); 4 SURVIVED with identical stdout and rc=0 and recorded as equivalent or out of scope (out/mutants_r23.out)"},
 {"id": "AC4-a-r23/L02_s01_share_over_break_even", "description": "NEW student-error: share of plan divided by the upper break-even", "killed_by": "KILLED (share_of_planned 19.68 vs 16.44)"},
 {"id": "AC4-a-r23/L02_s02_step_at_or_above_2000", "description": "NEW student-error: step applied from 2,000 units inclusive", "killed_by": "KILLED (loss run units 2000 to 2088)"},
 {"id": "AC4-a-r23/L02_s03_sensitivity_truncated", "description": "NEW student-error: printed sensitivity truncated instead of rounded", "killed_by": "KILLED (7.40 vs 7.41)"},
]

verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
frag = {
 "unit": "AC4", "slice": "AC4-a", "round": 23,
 "verifier": "independent verifier (Haiku), round 23",
 "pin": "503d139", "base": "d160ac3",
 "checkout": "/tmp/verify23-AC4-a", "scratch": "/tmp/AC4-v/AC4-a",
 "verified_at": "2026-10-28T00:00:00+00:00",
 "verdict": verdict,
 "rows": rows,
 "mutants": mutants,
 "registry_flags": [], "freshness_flags": [],
 "notes": [
  "Delta d160ac3..503d139 for AC4-a: cards.json only (c020 shortened; c135 added). index.html, L01.html, L02.html and tests/labs/AC4 unchanged, so every page row not re-run carries its round-22 result with the carry prefix.",
  "Scope rule applied: a carried PASS whose cited subject is byte-identical is carried; a changed or re-judged subject is re-verified. The L02 misconception 3 sentence (line 311) is byte-identical to round 22 but is re-judged FAIL on the scope of 'the volume'.",
  "Project slices rule (new mutants) not applicable: this slice has no project grader. Three new lab-twin mutants were added anyway. Alternative correct implementations were not run (no grader in this slice).",
  "Not checked: L07, L08, L03 and the cards c037, c095, c108, c113, c136 to c140 (other slices); project.html and the grader; the reachable reference pages beyond the two AC4 registry entries (the live verify_refs check reads the registry only; no external page was fetched); Pyodide wall clock beyond page_smoke's own timer; hours are design targets and were not failed on pace; hub-to-lesson hours arithmetic was carried (no hub or lesson hour changed).",
 ],
 "summary": "",
}
frag["summary"] = (f"Slice AC4-a round 23 (pin 503d139, base d160ac3): {len(rows)} rows, "
    f"{sum(r['status']=='PASS' for r in rows)} PASS, {sum(r['status']=='FAIL' for r in rows)} FAIL. "
    "FAIL: AC4-c135 (new card) states 'exactly when the volume is at or above the segment's zero' without restricting to that segment (2,001 units is above 88.89 and loses 1,186.50 USD), and the byte-identical L02 misconception 3 sentence (line 311) has the same unrestricted scope; the cards-L01-L02 row fails for the same card. Everything else re-run passes: check_pages, check_dag, check_projects, run_labs 10/10, twins equal their embedded blocks, page_smoke, pytest, ruff, verify_refs live and offline, build_site --check. Mutants: 23 of 27 committed killed (4 equivalent or out of scope), 3 new killed.")
out = ROOT / "ledgers/AC4/AC4-a.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "verdict", verdict)
