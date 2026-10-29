"""Round 25: build the AC4-a fragment from the round-24 fragment (carry and re-verify rules) plus this round's rows."""
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
prev = json.loads(Path("/tmp/fanout-frags/AC4-a.round24.json").read_text(encoding="utf-8"))
CARRY = "Carried from round 24 (cited lines of L01.html, L02.html, index.html and cards.json byte-identical since the previous pin 23cbd6a; the delta touched only L02.html:311 and cards.json AC4-c135): "
REVER = {
    "AC4-a-cmd-check-pages", "AC4-a-cmd-check-dag", "AC4-a-r19-cmd-check-projects", "AC4-a-cmd-run-labs",
    "AC4-a-cmd-twins-isolated", "AC4-a-cmd-twin-output-equals-page", "AC4-a-cmd-page-smoke",
    "AC4-a-cmd-pytest-labs-lint", "AC4-a-cmd-verify-refs", "AC4-a-r18-cmd-build-site-check",
    "AC4-a-banned-phrases", "AC4-a-L02-misconceptions", "AC4-a-cards-L01-L02", "AC4-a-r23-card-c135",
    "AC4-a-r24-line311-numbers", "AC4-a-r24-delta-scan", "AC4-a-r24-mutants-new", "AC4-a-r24-mutants-committed",
    "AC4-a-r23-mutants-committed", "AC4-a-r23-mutants-new", "AC4-a-r18-mutants-labs", "AC4-a-r21-new-mutants",
    "AC4-a-cards-r17-changed-subjects", "AC4-a-cards-L02-changed", "AC4-a-r18-cards-c008-c018-c125",
    "AC4-a-r23-card-c020", "AC4-a-r18-L02-key-results-source-c125", "AC4-a-r24-cmd-twins-cards",
}
REWRITE = {
    "AC4-a-L02-misconceptions": "Re-verified round 25 at pin b49a857: L02.html:311 now reads 'For a plan whose volume lies in a segment that has a zero, operating income is non-negative exactly when that volume is at or above the segment's zero (Proposition 4.1)'. The scope is restricted to a segment with a zero, which Proposition 4.1 supports (OI strictly increasing on each segment, at most one zero per segment, slope m > 0). The numbers recompute: 2,001 units gives OI = -1,186.50 USD (ledgers/AC4/scripts/AC4-a-r25/out/ and recompute_311 output: OI(2001) cents -118650); the loss runs 2001 to 2088 match the Lab 1 output; the 'segment with no zero has one sign' clause follows from strict monotonicity on each segment. Command: python -I ledgers/AC4/scripts/AC4-a-r24/recompute_311.py, all True.",
    "AC4-a-r23-card-c135": "Re-verified round 25: cards.json AC4-c135 now reads front 'For a plan whose volume lies in a segment that has a zero, when is operating income non-negative?' back 'Exactly when that volume is at or above the segment's zero (Proposition 4.1).' Matches L02.html:311 and Proposition 4.1 (segment monotonicity, one zero per segment, m > 0). The scope is now restricted as the lesson sentence is. Grade T is consistent with Proposition 4.1 (theorem).",
    "AC4-a-cards-L01-L02": "FAIL round 25: all 39 L01 and L02 flashcards re-read this round against their lesson text (cards.json lines for AC4-c001..c030, c118..c120, c125, c127, c128, c130, c132, c135). Every card matches its lesson except AC4-c026 (see row AC4-a-r25-card-c026). c135 is now fixed (its previous FAIL is cleared).",
    "AC4-a-r24-line311-numbers": "Re-verified round 25 at pin b49a857: python -I ledgers/AC4/scripts/AC4-a-r24/recompute_311.py run in the checkout. Values: margin 1350 cents, lower zero 88.89, upper zero 2088.89 (> T), OI(2001) = -1186.50 USD, OI(2088) = -12.00, OI(2089) = 1.50, upper iff holds on 2001..5000 True, lower iff holds on 0..2000 True, 2001 >= lower zero with OI < 0 True, sensitivity 7.41. Matches L02.html:311 and Lab 1 output.",
    "AC4-a-r24-delta-scan": "Delta 23cbd6a..b49a857 for the AC4-a slice (git diff --stat 23cbd6a b49a857 -- course/modules/AC/AC4 tests/labs/AC4 references tools course/assets/js): exactly two files changed, L02.html (line 311 only, 1 line) and cards.json (AC4-c135 front and back only). index.html, L01.html, tests/labs/AC4/*, references/, tools/ and course/assets/js/ unchanged. Every other round-24 row is either re-run or carried.",
    "AC4-a-r24-mutants-committed": "Re-run round 25 under python -I -W error: ledgers/AC4/mutants/AC4-a-r18..r25 (36 files) against the unmutated twin stdout (ledgers/AC4/scripts/AC4-a-r25/out/mutants_r25.out): 32 KILLED, 4 SURVIVED with identical stdout and rc=0 (AC4-a-r21/L01_p01, AC4-a-r21/L02_p03, AC4-a-r21/L02_p04, AC4-a-r22/L01_q01), recorded as equivalent or out of scope under the lab-twin ruling (no lesson sentence claims the lab checks those properties).",
    "AC4-a-r24-mutants-new": "Re-run round 25: ledgers/AC4/mutants/AC4-a-r24/L02_t01, t02, t03 all KILLED (out/mutants_r25.out).",
    "AC4-a-r23-mutants-committed": "Re-run round 25 as part of the r18..r25 suite (out/mutants_r25.out): AC4-a-r23 s01, s02, s03 all KILLED.",
    "AC4-a-r23-mutants-new": "Re-run round 25 as part of the r18..r25 suite (out/mutants_r25.out): AC4-a-r23 s01, s02, s03 all KILLED.",
    "AC4-a-r18-mutants-labs": "Re-run round 25 as part of the r18..r25 suite (out/mutants_r25.out): r18 mutants KILLED except the out-of-scope survivors named in AC4-a-r24-mutants-committed.",
    "AC4-a-r21-new-mutants": "Re-run round 25 as part of the r18..r25 suite (out/mutants_r25.out); r21 survivors L01_p01, L02_p03, L02_p04 are out of scope as stated in AC4-a-r24-mutants-committed.",
    "AC4-a-cards-r17-changed-subjects": "Re-read round 25 (cards.json AC4-c004, c008, c017, c132 against L01.html Definitions 3.1, 2.1 and Remark 3.3 and Lab 1 output): every card matches its lesson text. c004 gives the high-low formulas and H, L definitions (L01.html Definition 3.1); c008 gives 514.73 USD (Lab 1 output); c017 matches Definition 3.1 of L02; c132 matches the tie rule in L01 Definition 3.1 and the lab code (earliest month).",
    "AC4-a-cards-L02-changed": "Re-read round 25: AC4-c030 (5,550.00 USD at 2,500 units, Lab 1 output), c118 (411.11 units, 16.44%, upper break-even 2,088.89), c119 (6.08, 1% rise gives 6.08%), c125 (89 units, Proposition 4.1 and Remark 2.3) match the lesson text and the Lab 1 output.",
    "AC4-a-r18-cards-c008-c018-c125": "Re-read round 25: AC4-c008 (514.73 USD largest residual), c018 (break-even is the zero of a line, Proposition 2.2), c125 (89 units) match their lesson text and Lab 1 output.",
    "AC4-a-r23-card-c020": "Re-read round 25: AC4-c020 matches L02.html:173 and the Lab 1 output lines 'loss run units 2001 to 2088' and 'check operating_income(88) -12.00 operating_income(89) 1.50'.",
    "AC4-a-r18-L02-key-results-source-c125": "Carried from round 24 with the card re-read round 25: AC4-c125 matches L02.html:438 and Remark 2.3.",
    "AC4-a-r24-cmd-twins-cards": "Re-run round 25 (ledgers/AC4/scripts/AC4-a-r25/out/twin_L01.out, twin_L02.out; check_twins_cards.py); twin stdout equals the embedded <pre class=\"expected\"> blocks (L01 20 lines, L02 13 lines, compared by python -I in the checkout).",
    "AC4-a-r21-indep-recompute": "Carried from round 24 (cited script and lesson lines byte-identical; the delta touched only L02.html:311).",
}
for r in prev["rows"]:
    rid = r["id"]
    if rid in REWRITE:
        r["evidence"] = REWRITE[rid]
        r["status"] = "PASS" if rid not in ("AC4-a-cards-L01-L02",) else "FAIL"
    elif rid in REVER:
        r["evidence"] = "Re-run or re-read in round 25 (pin b49a857): " + r["evidence"]
    else:
        r["evidence"] = CARRY + r["evidence"]
for r in prev["rows"]:
    if r["status"] == "FAIL" and r["id"] == "AC4-a-cards-L01-L02":
        r["fix"] = "Fix AC4-c026 (see AC4-a-r25-card-c026); the other 38 cards match their lesson text."
    if r["id"] == "AC4-a-r23-card-c135" or r["id"] == "AC4-a-L02-misconceptions":
        r.pop("fix", None)
for r in prev["rows"]:
    if r["status"] == "PASS":
        r.pop("fix", None)
rows_by_id = {r["id"]: r for r in prev["rows"]}
assert rows_by_id["AC4-a-cards-L01-L02"]["status"] == "FAIL"

NEW = [
 {"id": "AC4-a-r25-delta-scan", "check": "delta 23cbd6a..b49a857 for the AC4-a slice, every hunk read",
  "location": "course/modules/AC/AC4/L02.html:311; course/modules/AC/AC4/cards.json AC4-c135",
  "status": "PASS",
  "evidence": "git diff 23cbd6a b49a857 -- course/modules/AC/AC4 tests/labs/AC4 references tools course/assets/js: two files, L02.html (one line, 311) and cards.json (c135 front and back). Both hunks read in full. No other AC4-a file changed."},
 {"id": "AC4-a-r25-card-c135", "check": "card AC4-c135 against L02 Proposition 4.1 and the Lab 1 output",
  "location": "course/modules/AC/AC4/cards.json AC4-c135; L02.html:120-128, 311",
  "status": "PASS",
  "evidence": "Front and back restrict the claim to 'a segment that has a zero' and 'that volume' as L02.html:311 does. Proposition 4.1 proof: each piece has slope m > 0, so each is strictly increasing with at most one zero, which makes 'non-negative exactly when at or above the segment's zero' true. Grade T is the Proposition's grade."},
 {"id": "AC4-a-r25-card-c026", "check": "card AC4-c026 scope against Proposition 3.3 (single-segment model only)",
  "location": "course/modules/AC/AC4/cards.json AC4-c026; L02.html:107-110 (Proposition 3.3 states the single-segment model); L02.html:435 (key-results row says single-segment); L02.html:484-490 (quiz item 7 says 'if the single segment still applies')",
  "status": "FAIL",
  "evidence": "Card front 'How far does the break-even volume move when fixed cost rises by delta F, with the margin unchanged?' and back 'It rises by exactly delta F/m units' carry no single-segment restriction, but Proposition 3.3 (L02.html) is stated only for the single-segment model. The lesson's own key-results row (L02.html:435) and quiz (L02.html:484-490) carry the single-segment qualifier that the card omits. Witness from Lab 1 inputs (computed by python -I in the checkout, first zero = F/m if <= 2000 else (F+S)/m): fixed cost raised from 120,000 to 2,700,001 cents (dF = 2,580,001 cents = 25,800.01 USD). The first break-even moves from 88.89 to 4,000.00 units, a move of 3,911.11 units, while dF/m = 1,911.11 units.",
  "fix": "Restrict the card to the single-segment model, e.g. front 'In the single-segment model of Proposition 2.2, how far does the break-even volume move when fixed cost rises by delta F, with the margin unchanged?' (the lesson's Proposition 3.3 wording), or add 'in the single-segment model' to the back, and do not state it for a step cost."},
 {"id": "AC4-a-r25-L01-E2-residual", "check": "L01 E2 solution: noise alone does not produce the 514.73 USD residual",
  "location": "course/modules/AC/AC4/L01.html:355 (E2 solution); tests/labs/AC4/lab-AC4-L01-1.py NOISE_CENTS",
  "status": "PASS",
  "evidence": "Recomputed with the lab's own simulate and high_low in the checkout: month 1 (556 hours) residual -51,473 cents = own noise -33,460 cents (within the 40,000-cent bound) plus fitted-minus-generator line gap -18,013 cents (approximately -13,203,866/733 = -18,013.46 cents). The sentence 'The rest comes from the gap between the fitted line and the generator's line' is correct."},
 {"id": "AC4-a-r25-mutants-new", "check": "three NEW student-error lab-twin mutants of L02 (round 25)",
  "location": "ledgers/AC4/mutants/AC4-a-r25/L02_u01_sensitivity_in_dollars_not_cents.py, L02_u02_leverage_planned_income_without_step.py, L02_u03_break_even_revenue_at_variable_cost.py",
  "status": "PASS",
  "evidence": "Each run under python -I -W error: rc 0, stdout differs. u01 prints fixed_plus_10000_cents_moves_break_even_units 0.74 (page: 7.41); u02 prints operating_leverage 1.04 (page: 6.08); u03 prints revenue_break_even_usd 1022.22 (page: 2222.22). All killed (out/mutants_r25.out)."},
 {"id": "AC4-a-r25-mutants-suite", "check": "all committed AC4-a lab-twin mutants re-run (r18..r25)",
  "location": "ledgers/AC4/mutants/AC4-a-r18..AC4-a-r25 (36 files); ledgers/AC4/scripts/AC4-a-r25/run_mutants_r25.py",
  "status": "PASS",
  "evidence": "run_mutants_r25.py output: 32 KILLED, 4 SURVIVED (AC4-a-r21/L01_p01_high_chosen_by_cost, AC4-a-r21/L02_p03_first_whole_unit_by_round, AC4-a-r21/L02_p04_zero_counted_as_loss, AC4-a-r22/L01_q01_residual_uses_low_month_only). Each survivor has rc 0 and stdout identical to the twin. Lab twins are out of scope for mutation under the architect ruling: no lesson sentence states that Lab 1 checks those properties (out/mutants_r25.out)."},
 {"id": "AC4-a-r25-cmd-twin-stdout-equals-embedded", "check": "embedded expected blocks equal the twin stdout (both labs, rerun this round)",
  "location": "course/modules/AC/AC4/L01.html <pre class=\"expected\">; L02.html <pre class=\"expected\">",
  "status": "PASS",
  "evidence": "python -I -W error twin stdout compared with the page's expected block after html.unescape: L01 equal (20 lines), L02 equal (13 lines)."},
 {"id": "AC4-a-r25-cards-reread", "check": "all 39 L01 and L02 cards re-read against lesson text this round",
  "location": "course/modules/AC/AC4/cards.json (L01 and L02 cards; 39 in all)",
  "status": "PASS",
  "evidence": "Every L01 and L02 card was read in full and matched against its lesson section (Definitions 1.1, 1.2, 2.1, 3.1; Propositions 1.3, 2.2, 3.2, 3.3, 4.1, 5.1; Remarks 2.3, 3.3; Examples 1.4, 4.1; Lab 1 output of both labs). Exception: AC4-c026 (row AC4-a-r25-card-c026, FAIL). Numbers on cards (88.89, 89, 2,088.89, 2,001, 411.11, 16.44%, 6.08, 5,550.00, 514.73, 18,463.89, 41.99, 10 of 12) appear in their lessons."},
]
prev["rows"] = prev["rows"] + NEW
ids = [r["id"] for r in prev["rows"]]
assert len(ids) == len(set(ids)), "duplicate ids"
prev_ids = [r["id"] for r in json.loads(Path("/tmp/fanout-frags/AC4-a.round24.json").read_text())["rows"]]
assert set(prev_ids) <= set(ids), "a previous row id was dropped"

prev["round"] = 25
prev["verifier"] = "independent verifier (Haiku), round 25"
prev["pin"] = "b49a857"
prev["base"] = "23cbd6a"
prev["checkout"] = "/tmp/verify25-AC4-a"
prev["scratch"] = "/tmp/AC4-v/AC4-a-r25"
prev["verified_at"] = "2026-10-28T00:00:00+00:00"
prev["mutants"] = [
 {"id": "AC4-a-r18..r25 committed lab-twin mutants (36 files)", "description": "committed lab-twin mutants of L01 and L02 (ledgers/AC4/mutants/AC4-a-r18..r25)", "killed_by": "32 KILLED; 4 SURVIVED with identical stdout and rc=0, recorded as equivalent or out of scope (out/mutants_r25.out)"},
 {"id": "AC4-a-r25/L02_u01_sensitivity_in_dollars_not_cents", "description": "NEW student-error: sensitivity computed with 10,000 cents read as 1,000 cents", "killed_by": "KILLED (7.41 becomes 0.74)"},
 {"id": "AC4-a-r25/L02_u02_leverage_planned_income_without_step", "description": "NEW student-error: operating leverage uses planned income with the step omitted", "killed_by": "KILLED (6.08 becomes 1.04)"},
 {"id": "AC4-a-r25/L02_u03_break_even_revenue_at_variable_cost", "description": "NEW student-error: break-even revenue priced at the variable cost per unit", "killed_by": "KILLED (2222.22 becomes 1022.22)"},
]
prev["notes"] = [
 "Delta 23cbd6a..b49a857 for AC4-a: L02.html:311 (one sentence, scope now restricted to 'a segment that has a zero') and cards.json AC4-c135 (same restriction). Both re-verified and PASS. All other changes: none in this slice.",
 "Carry rule: a round-24 PASS is carried only when its cited lines are byte-identical; command rows, the banned-phrase grep, mutant rows and the cards re-read are re-run this round.",
 "New FAIL: AC4-c026 is a card (L02) whose scope is broader than Proposition 3.3 (single-segment model only); witness in row AC4-a-r25-card-c026. The row AC4-a-cards-L01-L02 is FAIL for the same reason.",
 "Observation, not a row: L01.html quiz explanation for question 7 says 'Other months carry residuals (Remark 3.3)'. This text is carried unchanged; in general a month may lie exactly on the line, so the sentence is stronger than Remark 3.3, which says only that residuals are free to be positive or negative. Lab 1 shows 10 of 12 nonzero, which supports the statement for that history only. Recommend 'in Lab 1, ten other months carry residuals'.",
 "Not checked: L03 to L08 and cards of other slices; project.html and the grader; live access to external sources (none needed: registry checks were run by verify_refs live and offline and no page was fetched); Pyodide wall-clock beyond page_smoke's own timer; hour figures not failed on pace (design targets); hub and lesson hours arithmetic carried from round 24 because index.html and the hours lines are unchanged.",
]
prev["summary"] = "Slice AC4-a round 25 (pin b49a857, base 23cbd6a): all command rows re-run and pass; the L02.html:311 rewrite and card AC4-c135 are now correctly scoped and PASS; the 39 L01/L02 cards were re-read and one card, AC4-c026, overstates Proposition 3.3 (FAIL). Mutants: 32 of 36 killed, 4 out of scope, 3 new killed."
out = ROOT / "ledgers/AC4/AC4-a.json"
out.write_text(json.dumps(prev, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(prev["rows"]), "non-pass", [r["id"] for r in prev["rows"] if r["status"] != "PASS"])
