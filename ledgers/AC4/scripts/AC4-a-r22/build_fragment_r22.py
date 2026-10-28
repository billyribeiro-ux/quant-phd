"""Build ledgers/AC4/AC4-a.json for round 22 from the round-21 ids plus the round-22 delta rows."""
import json, sys
from pathlib import Path

ROOT = Path(sys.argv[1])
prev = json.load(open("/tmp/fanout-frags/AC4-a.round21.json"))
CARRY = ("Carried from round 21 (cited lines byte-identical since the previous pin f95243f; "
         "the round-22 hunks at L01.html:283,402,404 and L02.html:89,267,433,435,437 are not cited by this row):")
RERUN = "Re-run round 22"
FIXED = {}
def fresh(rid, status, location, evidence):
    FIXED[rid] = dict(status=status, location=location, evidence=evidence)

# Previously FAIL rows, re-verified from scratch
fresh("AC4-a-num-L01-lab", "PASS", "L01.html:134,222-241,242,283,348-362,403-404",
      "Lab run (python -I -W error) output equals the embedded expected block line for line (20 lines; out/twin_L01.out, twin-match check); L01.html:283 and :404 now say 'largest absolute residual 514.73 USD', equal to printed 'largest absolute residual_cents 51473' (= max |residual|); E1 months 6 and 11 and hours/costs match printed rows; E2 and E3 match; L01.html:134 hypothesis predictions hold (months 6 and 11 exact, residuals 0 by Prop 3.2); L01.html:242 'up to 514.73' matches max residual at month 1, a non-extreme month.")
fresh("AC4-a-L01-canon-and-misconceptions", "PASS", "L01.html:257-283",
      "Re-read 257-283: 259 'Lesson 2 shows what a step in fixed cost does' (L02 Prop 4.1 present); 261 'Remark 3.3' exists (L01.html:128-129); 271 Example 1.4 numbers 6,000/500=12 and 6,000/1,000=6 recomputed; 275 Remark 2.3 exists (L01.html:102); 279 printed 10 of 12 nonzero residuals (output line 239); 283 largest absolute residual 514.73 USD = printed 51473 cents.")
fresh("AC4-a-L01-misconception-and-keyresults-grades", "PASS", "L01.html:399-404",
      "Rows 399-402 T grades re-proved (Prop 2.2, Prop 1.3(b), Prop 3.2 with Q_H != Q_L as in Def 3.1 L01.html:112). Row 403 C: printed 1846389 cents = 18,463.89 USD and 4198.96 cents = 41.99 USD/h; the difference from the generator is exactly the extreme-month noise, since F_hat = F + n_H - (v_hat - v)Q_H and v_hat = v + (n_H - n_L)/(Q_H - Q_L) (algebra re-derived). Row 404 now 'largest absolute residual 514.73 USD, 10 of 12 off the line' = printed 51473 and 'months with nonzero residual 10 of 12'.")
fresh("AC4-a-L01-misconception-and-keyresults-grades-r17", "PASS", "L01.html:269-284, 399-404",
      "Re-read 269-284 (misconceptions 1-4, all checked: 270-271 Prop 1.3(b) and Example 1.4; 274-275 Prop 2.2 and Remark 2.3; 278-279 Prop 3.2 and Lab 1 count; 283 largest absolute residual) and 399-404 as in the row above.")
fresh("AC4-a-L01-largest-residual-wording", "PASS", "course/modules/AC/AC4/L01.html:283, :404",
      "Both sentences now say 'largest absolute residual 514.73 USD'. Lab 1 line 76 of the twin prints max(abs(r)) = 51473 cents; the committed-mutant run killed the sign-blind variant (ledgers/AC4/mutants/AC4-a-r18/L01_m03_largest_signed_not_absolute.py, KILLED stdout differs).")

# Changed-subject rows, re-verified for the round-22 delta
fresh("AC4-a-L02-lab-numbers", "PASS", "course/modules/AC/AC4/L02.html:134,251-263,264,267",
      "Twin output (out/twin_L02.out) equals embedded block (13 lines). Line 267 numbers recomputed independently (out/indep_recompute_r21.out and round-22 recompute): margin of safety 2500 - 28200/13.5 = 411.11 units; 411.11/2500 = 16.44%; OI(2500) = 5550.00 USD; DOL = 33750/5550 = 6.081 -> 6.08; 1% volume (25 units) to OI(2525)=5887.50 gives +6.081% = DOL x 1%; Prop 3.3 100/13.5 = 7.41. 'because no step lies between 2,500 and 2,525': the only step in the lab is above 2,000 units (lab code STEP_ABOVE_UNITS=2000); the scan of integers 2501-2525 finds no step crossing.")
fresh("AC4-a-L02-key-results-grades", "PASS", "L02.html:431-439",
      "Rows 433, 435, 437 changed and re-proved: 433 'With m > 0' (Remark 2.3 uses strict monotonicity from Prop 2.2, which needs m > 0); 435 'In the single-segment model' (Prop 3.3 is stated for the single-segment model of Prop 2.2); 437 'With constant unit shares' (Prop 5.1 defines constant shares w_k). Unchanged rows 431-432, 434, 436 re-read. Row 438 C: printed 'operating income ... 0 to 88 ... 2001 to 2088' and 'first whole unit 89' match output lines 252, 256-257; row 439 matches lines 258-260.")
fresh("AC4-a-L02-key-results-profitable", "PASS", "L02.html:433 (with L02.html:81)",
      "Row 433 'With m > 0, the smallest whole volume with non-negative operating income is ceil(Q*)' re-proved: OI strictly increasing when m > 0, so OI(n) >= 0 iff n >= Q*; Remark 2.3 (L02.html:81) gives 88.89 -> 89 and 'Lab 1 prints both values' (output lines 252: single_formula 88.89 and first_whole_unit 89).")
fresh("AC4-a-L02-remark-2-3-whole-units", "PASS", "course/modules/AC/AC4/L02.html:81 (Remark 2.3)",
      "Re-read; 'Lab 1 prints both values' true (single_formula_break_even_units 88.89 first_whole_unit 89, output line 252). Lines unchanged since f95243f.")

fresh("AC4-a-cmd-check-pages", "PASS", "course/modules/AC/AC4/index.html, L01.html, L02.html",
      "Re-run round 22: tools/check_pages.py --unit AC4 rc=0, 'check_pages AC4: PASS' (out/check_pages.out).")
fresh("AC4-a-cmd-check-dag", "PASS", "course/modules/AC/AC4/L01.html:59,88; L02.html:57,66; index.html:62-63",
      "Re-run round 22: tools/check_dag.py --all rc=0; 'check_dag AC4: PASS' (out/check_dag.out).")
fresh("AC4-a-r19-cmd-check-projects", "PASS", "course/modules/AC/AC4/project.html (unit AC4 entry)",
      "Re-run round 22: tools/check_projects.py --unit AC4 rc=0, 'check_projects AC4: PASS' (out/check_projects.out).")
fresh("AC4-a-cmd-run-labs", "PASS", "tests/labs/AC4/lab-AC4-L01-1.py, lab-AC4-L02-1.py",
      "Re-run round 22: tools/run_labs.py --unit AC4 rc=0, 'run_labs AC4: PASS (10/10)' (out/run_labs.out).")
fresh("AC4-a-cmd-twins-isolated", "PASS", "tests/labs/AC4/lab-AC4-L01-1.py, lab-AC4-L02-1.py",
      "Re-run round 22: python -I -W error on each twin: rc=0, stderr empty (out/twin_L01.out, out/twin_L02.out).")
fresh("AC4-a-cmd-twin-output-equals-page", "PASS", "L01.html:222-241; L02.html:251-263",
      "Re-run round 22: stdout of each twin equals the embedded expected block (L01 20/20 lines, L02 13/13 lines) by a script comparing html-unescaped block text with stdout.")
fresh("AC4-a-cmd-page-smoke", "PASS", "course/modules/AC/AC4/index.html, L01.html, L02.html",
      "Re-run round 22: tools/page_smoke.py --unit AC4 --pages index.html L01.html L02.html rc=0, 'page_smoke AC4: PASS' (out/page_smoke.out); the page run took 0.6 s total.")
fresh("AC4-a-cmd-pytest-labs-lint", "PASS", "tests/labs/AC4/lab-AC4-L01-1.py, lab-AC4-L02-1.py",
      "Re-run round 22: pytest -q -k AC4 rc=0 (10 passed, out/pytest_ac4.out); ruff check tests/labs/AC4 'All checks passed!'; ruff format --check '10 files already formatted' (out/ruff_check.out, out/ruff_format.out).")
fresh("AC4-a-cmd-verify-refs", "PASS", "references/references.json entries datar2020horngrens, kaplan1998cost",
      "Re-run round 22: tools/verify_refs.py --unit AC4 rc=0 'live re-verification of AC4: 2 of 560 entries, 0 problems'; tools/verify_refs.py --offline rc=0 'offline integrity: 560 entries, 0 problems' (out/verify_refs_live_AC4.out, out/verify_refs_offline.out).")
fresh("AC4-a-r18-cmd-build-site-check", "PASS", "course/modules/AC/AC4/cards.json",
      "Re-run round 22: tools/build_site.py --check rc=0, 'site data current: 6 outputs' (out/build_site_check.out).")
fresh("AC4-a-r18-mutants-labs", "PASS", "ledgers/AC4/mutants/AC4-a-r18/ (10), AC4-a-r19/ (5), AC4-a-r20/ (3), AC4-a-r21/ (6), AC4-a-r22/ (3)",
      "Re-run round 22 of every committed lab mutant (out/mutants_all_r22.out): 24 committed (r18 10, r19 5, r20 3, r21 6) plus 3 new; 23 KILLED in total, the 18 r18-r20 mutants all KILLED; 4 SURVIVED (r21 p01, p03, p04 and new q01), each recorded as equivalent or out of scope in the mutants list.")
fresh("AC4-a-r21-new-mutants", "PASS", "ledgers/AC4/mutants/AC4-a-r21/",
      "Re-run round 22 (out/mutants_all_r22.out): p02 KILLED (stdout differs); p01, p03, p04 SURVIVED with identical stdout and rc=0; recorded as equivalent or out of scope (lab twins, architect ruling; see mutants list).")
fresh("AC4-a-r21-indep-recompute", "PASS", "ledgers/AC4/scripts/AC4-a-r21/indep_recompute_r21.py",
      "Re-run round 22: rc=0; output 'R3 max abs error USD 3990 at hours [1, 401, 801] ratio 0.9975', 'step drop -2698650', 'oi2000 USD 25800.0 oi2001 USD -1186.5', 'E1 run lengths 89 88' (out/indep_recompute_r21.out).")
fresh("AC4-a-num-L01-R3-recomputed", "PASS", "L01.html:385-387; L01.html:473",
      "Re-run round 22 recompute (indep_recompute_r21.py): max abs error 3,990 USD at 1, 401, 801 hours; ratio 3990/4000 = 0.9975; table step values 4000/8000/12000 re-derived; line-fit values 10, 4010, 8010 re-derived.")
fresh("AC4-a-banned-phrases", "PASS", "index.html, L01.html, L02.html",
      "Re-run round 22: grep (case-insensitive) for roughly, 'about <digit>', historically, typically, usually, generally, often, in general, '...', '…', verifier, builder, round, unit report, REQUESTS, build: no matches in the three pages. Scope word 'only' at L02.html:76 is backed by strict monotonicity in the proof.")

CARRY_IDS = {
 "AC4-a-cite-none-in-lessons", "AC4-a-cite-hub-reading-list", "AC4-a-hub-reading-list-claim", "AC4-a-num-hub-placement",
 "AC4-a-num-hub-hours", "AC4-a-num-L01-examples", "AC4-a-L01-hypothesis", "AC4-a-L01-proofs", "AC4-a-L01-R1-count",
 "AC4-a-L01-R3-unquantified", "AC4-a-L01-P2-circular", "AC4-a-L01-quiz", "AC4-a-L01-lab-interpretation", "AC4-a-L01-hours",
 "AC4-a-L01-lab-intro-units", "AC4-a-L01-relevant-range-sentence", "AC4-a-L01-section5-heading", "AC4-a-L01-R3-range-sentence",
 "AC4-a-L02-sensitivity-proofs", "AC4-a-L02-step-proposition", "AC4-a-L02-cvp-definitions", "AC4-a-L02-lab-hypothesis",
 "AC4-a-L02-canon-practice-claim", "AC4-a-L02-costing-convention-claim", "AC4-a-L02-canon-bullets-mix-units",
 "AC4-a-L02-misconceptions", "AC4-a-L02-problems", "AC4-a-L02-remark-5-2-and-prop-5-1", "AC4-a-L02-quiz", "AC4-a-L02-hours",
 "AC4-a-cards-L02-changed", "AC4-a-cards-r17-changed-subjects", "AC4-a-cards-L01-L02", "AC4-a-hub-workspace-seed",
 "AC4-a-hub-prereq-unlocks", "AC4-a-hub-objectives-placement", "AC4-a-hub-skill-check-rung1", "AC4-a-hub-data-status",
 "AC4-a-footer-L01-L02", "AC4-a-L02-loss-volumes-printed", "AC4-a-L02-steps-bullet", "AC4-a-r18-hub-lede",
 "AC4-a-r18-L01-why-it-matters", "AC4-a-r18-L01-prop-3-2", "AC4-a-r18-L02-why-it-matters-terms",
 "AC4-a-r18-L02-key-results-source-c125", "AC4-a-r18-cards-c008-c018-c125", "AC4-a-L01-section4-intro-definition-3-1",
 "AC4-a-L01-E3-sentence", "AC4-a-L01-prop-2-2-changed", "AC4-a-hub-objective-4-simulated",
}
rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in FIXED:
        f = FIXED[rid]
        rows.append(dict(id=rid, check=r["check"], location=f["location"], status=f["status"], evidence=f["evidence"]))
    elif rid in CARRY_IDS:
        rows.append(dict(id=rid, check=r["check"], location=r["location"], status="PASS",
                         evidence=CARRY + " " + r["evidence"]))
    else:
        raise SystemExit(f"row {rid} not classified")
for rid in FIXED:
    if rid not in {r["id"] for r in prev["rows"]}:
        raise SystemExit(f"fixed id {rid} unknown")
print("classified", len(rows), "carried", sum(1 for r in rows if r["evidence"].startswith("Carried")), file=sys.stderr)
mutants = [
 {"id": "AC4-a-r22/L02_q01_step_at_2510", "description": "NEW student-error lab twin mutant: step threshold moved from 2000 to 2510 (tests the 2,500-2,525 'no step' sentence)", "killed_by": "KILLED stdout differs (out/mutants_all_r22.out)"},
 {"id": "AC4-a-r22/L02_q02_margin_ratio_over_price_minus_fixed", "description": "NEW lab twin mutant: margin reduced by 1 cent (price - variable - 1)", "killed_by": "KILLED stdout differs"},
 {"id": "AC4-a-r22/L01_q01_residual_uses_low_month_only", "description": "NEW lab twin mutant: residual of the 428-hour month forced to 0", "killed_by": "SURVIVED, equivalent: the true residual of month 6 (428 h) is already 0 (output line 230), so the output is identical; equivalent mutant, PASS"},
 {"id": "AC4-a-r21/L01_p01_high_chosen_by_cost", "description": "lab twin mutant AC4-a-r21 (committed)", "killed_by": "SURVIVED on this seed: the highest-cost month is also the highest-hours month, so output identical; equivalent on this input, out of scope (lab demonstration)"},
 {"id": "AC4-a-r21/L02_p03_first_whole_unit_by_round", "description": "lab twin mutant AC4-a-r21 (committed)", "killed_by": "SURVIVED: round(88.89)=89 equals ceil here; lab claims no ceiling check (Remark 2.3 says only that Lab 1 prints both values); equivalent on this input, out of scope"},
 {"id": "AC4-a-r21/L02_p04_zero_counted_as_loss", "description": "lab twin mutant AC4-a-r21 (committed)", "killed_by": "SURVIVED: no integer volume has OI exactly 0 (F/m = 88.89 and 2088.89 not integers), so the loss-run output is identical; lab claims no zero-case check; out of scope"},
]
mutants.insert(0, {"id": "AC4-a-r18..r20 (18 committed lab mutants)", "description": "lab twin mutants committed in r18-r20 (ledgers/AC4/mutants/AC4-a-r18, -r19, -r20)", "killed_by": "all 18 KILLED stdout differs or nonzero exit (out/mutants_all_r22.out)"})
frag = dict(
    unit="AC4", slice="AC4-a", round=22,
    verifier="independent verifier (Haiku), round 22",
    pin="d160ac3", base="f95243f",
    checkout=str(ROOT), scratch="/tmp/fanout-scratch-AC4a-r22",
    verified_at="2026-10-28T14:17:38+00:00",
    verdict="PASS",
    rows=rows, mutants=mutants,
    registry_flags=[], freshness_flags=[],
    notes=[
     "Delta f95243f..d160ac3 for AC4-a (git diff --stat): course/modules/AC/AC4/L01.html (2 lines: 283, 404 'largest' -> 'largest absolute'; the 402 key-result row gained ', when the two activities differ (Q_H != Q_L)'), L02.html (heading 89; 267 sentence; rows 433, 435, 437), L07/L08 and cards.json c093 are AC4-b/AC4-c slices, not read here. index.html and tests/labs/AC4 unchanged.",
     "Every hunk of the slice was read and re-derived: L01 lab output 20/20 lines equal; largest absolute residual 51473 cents; L02 sensitivity sentence recomputed (margin 411.11, 16.44%, DOL 6.081, 1% change 6.081%, no step in 2501-2525, 7.41 units).",
     "Previous FAIL rows (round 21: L01 largest-residual wording and the four rows citing it) re-verified and now PASS.",
     "Carried rows cite only lines outside the round-22 hunks; each carry is prefixed with the byte-identical statement.",
     "Not checked: project.html and project graders (other slice); the references' page content beyond the two AC4 registry entries (the live check does not read SEC/Springer pages, none are cited here); Pyodide wall-clock beyond page_smoke's own timer; hours are design targets per the architect ruling and were not failed on pace.",
    ],
    summary="Slice AC4-a round 22 (pin d160ac3, base f95243f): %d rows, all PASS. Delta: L01 wording (largest absolute residual; Q_H != Q_L condition) and L02 sentences (heading, 2,500-2,525 no-step sentence, key-result conditions) re-verified against the lab output and independent recomputation. Round-21 FAIL rows fixed. 3 new lab mutants (2 killed, 1 equivalent) plus all 24 committed mutants re-run (23 killed in total, 4 survivors recorded as equivalent or out of scope)." % len(rows),
)
out = ROOT / "ledgers/AC4/AC4-a.json"
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out)
