"""Builds ledgers/AC4/AC4-a.json (round 19) from the round-18 fragment and this round's evidence.

Carried rows keep their round-18 evidence under the carry prefix; only rows whose cited subject is
byte-identical since the round-18 pin (7143726) are carried. Every other row is re-verified this round.
"""
import datetime, json, sys

R18 = json.load(open("/tmp/fanout-frags/AC4-a.round18.json"))
prev = {r["id"]: r for r in R18["rows"]}
OUT = sys.argv[1]

def carry(rid, files):
    r = dict(prev[rid])
    r["evidence"] = f"Carried from round 18 ({files} byte-identical since the previous pin): " + r["evidence"]
    return r

def fresh(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix is not None:
        r["fix"] = fix
    return r

rows = [
 # commands, re-run this round
 fresh("AC4-a-cmd-check-pages", "command: tools/check_pages.py --all", "course/modules/AC/AC4/index.html, L01.html, L02.html", "PASS",
       "re-run on pin 51fa336: 'check_pages AC4: PASS' (output in ledgers/AC4/scripts/AC4-a-r19/check_pages.out, /tmp/AC4-v/a/r19/check_pages.out)"),
 fresh("AC4-a-cmd-check-dag", "command: tools/check_dag.py --all", "course/modules/AC/AC4/L01.html:59,88; L02.html:57,66; index.html:62-63", "PASS",
       "re-run: 'check_dag AC4: PASS' (all units PASS)"),
 fresh("AC4-a-r19-cmd-check-projects", "command: tools/check_projects.py --all", "course/modules/AC/AC4/project.html (unit AC4 entry)", "PASS",
       "re-run: 'check_projects AC4: PASS'; project.html itself is another slice and was not read"),
 fresh("AC4-a-cmd-run-labs", "command: tools/run_labs.py --unit AC4", "tests/labs/AC4/lab-AC4-L01-1.py, lab-AC4-L02-1.py", "PASS",
       "re-run: 'run_labs AC4: PASS (10/10)'"),
 fresh("AC4-a-cmd-twins-isolated", "twins run alone under python -I -W error, from /tmp, absolute interpreter path",
       "tests/labs/AC4/lab-AC4-L01-1.py, lab-AC4-L02-1.py", "PASS",
       "re-run: L01 rc=0 (20 output lines), L02 rc=0 (13 output lines) (/tmp/AC4-v/a/r19/twin_L01.out, twin_L02.out)"),
 fresh("AC4-a-cmd-twin-output-equals-page", "page <pre class=expected> equals the isolated twin stdout",
       "L01.html:222-241; L02.html:251-263", "PASS",
       "ledgers/AC4/scripts/AC4-a-r19/expected_vs_twin.py: L01 20 lines IDENTICAL, L02 13 lines IDENTICAL"),
 fresh("AC4-a-cmd-page-smoke", "command: tools/page_smoke.py --unit AC4", "course/modules/AC/AC4/index.html, L01.html, L02.html", "PASS",
       "re-run: 'page_smoke AC4: PASS' (L01, L02, index, project, concepts, review all PASS; boot 1.2 s)"),
 fresh("AC4-a-cmd-pytest-labs-lint", "pytest tests/test_labs.py -k AC4; ruff; mypy on the two twins",
       "tests/labs/AC4/lab-AC4-L01-1.py, lab-AC4-L02-1.py", "PASS",
       "pytest -k AC4: 10 passed; ruff check and ruff format --check: all passed; mypy --no-incremental on both twins: no issues (ledgers/AC4/scripts/AC4-a-r19/)"),
 fresh("AC4-a-cmd-verify-refs", "command: tools/verify_refs.py --offline and --unit AC4 (live)",
       "references/references.json entries datar2020horngrens, kaplan1998cost", "PASS",
       "offline: 560 entries, 0 problems; live AC4: 2 of 560 entries, 0 problems"),
 fresh("AC4-a-r18-cmd-build-site-check", "command: tools/build_site.py --check (cards.json changed in the delta)",
       "course/modules/AC/AC4/cards.json", "PASS", "re-run rc=0: 'site data current: 6 outputs'"),
 # citations and hub
 fresh("AC4-a-cite-none-in-lessons", "lesson pages cite no registry key", "L01.html:487-491; L02.html:522-525", "PASS",
       "grep for horngren, kaplan, datar, data-ref in L01/L02: no hit; only the empty <ol data-references></ol> at L01.html:490 and L02.html:525"),
 carry("AC4-a-cite-hub-reading-list", "index.html"),
 carry("AC4-a-hub-reading-list-claim", "index.html"),
 carry("AC4-a-num-hub-placement", "index.html"),
 fresh("AC4-a-num-hub-hours", "hub split and lesson hours", "index.html:29,40,42,144-151; L01.html:34; L02.html:34; L03-L08 eyebrows", "PASS",
       "re-read: lesson eyebrows L01 6, L02 7, L03 6, L04 6, L05 7, L06 6, L07 6, L08 6 study hours sum to 50; hub cards 6,7,6,6,7,6,6,6; hub '50 h lessons · 20 h project (28.6% of 70 h)'; 20/70 = 28.6%; progress bar 71.4%/28.6%. No arithmetic inconsistency. (Pace is not judged: hours are design targets.)"),
 carry("AC4-a-num-L01-examples", "L01.html:81,251,298,305,310-312,348-349"),
 fresh("AC4-a-num-L01-lab", "lab numbers quoted on L01", "L01.html:134,222-241,242,283,348-362,403-404", "PASS",
       "re-checked against the twin output: 'months with nonzero residual 10 of 12' (L01.html:279, 362, 401-404); 'months on the fitted line exactly [6, 11]' (L01.html:362); largest absolute residual 51473 cents = 514.73 USD (L01.html:283); the generator and high-low figures 1846389 cents = 18,463.89 USD and 4198.96 cents/hour = 41.99 USD (L01.html:401)"),
 fresh("AC4-a-num-L01-R3-recomputed", "R3 step-cost arithmetic recomputed over every whole hour 0..1200", "L01.html:385-387; L01.html:473", "PASS",
       "ledgers/AC4/scripts/AC4-a-r19/recompute_r19.py: 1201 whole hours counted; max |cost - line| = 3990 at 1, 401, 801 h; 3990/4000 = 99.75%; line gives 10, 4010, 8010 at those hours. The page's 'Computed at each of the 1,201 whole hours from 0 to 1,200' matches."),
 carry("AC4-a-L01-hypothesis", "L01.html:134"),
 carry("AC4-a-L01-proofs", "L01.html:70-77,91-99,117-125"),
 fresh("AC4-a-L01-canon-and-misconceptions", "Section 5 and Section 6 claims", "L01.html:257-283", "PASS",
       "re-read in full. Section 6 line 279 rewritten: 'chosen by two observations only (Proposition 3.2), so the other months do not enter the estimate' follows from Definition 3.1 ('The method uses only the two extreme months'); 'ten of the twelve months' matches the lab; 'the method states no error measure' matches Remark 3.3 ('carries no measure of its own error'). Section 5 and the other misconceptions unchanged and re-read."),
 carry("AC4-a-L01-R1-count", "L01.html:373"),
 fresh("AC4-a-L01-R3-unquantified", "R3 says the step is not linear and states the error", "L01.html:387", "PASS",
       "re-read: 'It is not a linear function of hours' and the 3,990 USD error (99.75% of the step) are both stated and recomputed"),
 carry("AC4-a-L01-P2-circular", "L01.html:330"),
 fresh("AC4-a-L01-misconception-and-keyresults-grades", "grades in key results table match the evidence", "L01.html:399-404", "PASS",
       "re-read: T for Prop 2.2, Prop 1.3, Prop 3.2 (proved on the page); C for the SIMULATED high-low estimate and the 514.73 USD residual, each naming Lab 1 (SIMULATED) (matches E3 and misconception text)"),
 carry("AC4-a-L01-lab-interpretation", "L01.html:242"),
 fresh("AC4-a-L01-quiz", "L01 quiz answers and explanations", "L01.html:413-484 (explanations at 473 and 459)", "PASS",
       "re-read all quiz items: the factual items 10, 1000, 0.75, 20, 10000, 7 re-derived (25-15, 10*500-4000, 40-10 over 40, (30000-18000)/600, 30000-20*1000, 7000/1000); L01q7 explanation at line 459 rewritten and checked against Remark 3.3; L01q9 explanation at 473 checked against R3 (1-400 h constant at 4000 USD, so no slope fits 8000 USD)"),
 carry("AC4-a-L01-hours", "L01.html:2,34"),
 carry("AC4-a-L01-lab-intro-units", "L01.html:55"),
 carry("AC4-a-L01-relevant-range-sentence", "L01.html:59"),
 carry("AC4-a-L01-section5-heading", "L01.html:255"),
 fresh("AC4-a-L01-R3-range-sentence", "R3 range sentence (0 to 1,200 hours) and last sentence of the R3 solution", "L01.html:387", "PASS",
       "re-read: the problem states the range 0 to 1,200 hours; the solution's last sentence (range 1 to 400 hours gives a fixed 4,000 USD) matches the cost table at 1-400 h"),
 carry("AC4-a-L02-sensitivity-proofs", "L02.html:91-114"),
 carry("AC4-a-L02-step-proposition", "L02.html:120-128"),
 fresh("AC4-a-L02-cvp-definitions", "Definition 1.1 and Definition 2.1 assumptions and cross-references", "L02.html:57,66,70-76,86", "PASS",
       "re-read L02.html:53-76 and 84-88. Definition 1.1 at line 57 now lists its assumptions as a list ('Its assumptions are: ...'): one product or fixed mix; price and variable cost fixed over the range; fixed cost fixed over the range; units produced equal to units sold. The next sentence ('conventions of the model', 'Section 6 lists the places where they fail', 'the lab in Section 4 breaks one of them') is consistent: the step at L02:118-122 breaks the fixed-cost assumption. Cross-references to Lesson 1 Proposition 2.2 match L01.html:92. 'stated with every use' appears nowhere else (grep)."),
 carry("AC4-a-L02-lab-numbers", "L02.html:134,251-263,264,267"),
 carry("AC4-a-L02-lab-hypothesis", "L02.html:134"),
 carry("AC4-a-L02-canon-practice-claim", "L02.html:292"),
 carry("AC4-a-L02-costing-convention-claim", "L02.html:293"),
 carry("AC4-a-L02-canon-bullets-mix-units", "L02.html:287,291,293,294"),
 carry("AC4-a-L02-misconceptions", "L02.html:300-317"),
 fresh("AC4-a-L02-problems", "L02 problem set arithmetic and solutions", "L02.html:326-420 (R3 at 414-420 re-verified; M3 at 341-344, E2 at 384-394, R1 at 402-405 re-read)", "PASS",
       "R3 re-verified fresh: stem 'Product 2 is sold only when total volume is 1,000 units or more, and at and above that volume it makes up half the units' matches the solution's shares (0 below, 1/2 at and above); weighted margins 0.5*10 = 10 and 0.5*30 + 0.5*10 = 20 (recomputed in recompute_r19.py); 60000/10 = 6000 (outside the range below 1,000) and 60000/20 = 3000 (inside). Other problems at L02.html:326-416 and 420 are byte-identical since the previous pin and carried from round 18."),
 fresh("AC4-a-L02-remark-5-2-and-prop-5-1", "Proposition 5.1 and Remark 5.2 (with problem R3 at L02:419)", "L02.html:283 (with 419)", "PASS",
       "Proposition 5.1 text at 283 unchanged; the R3 solution at 419 rewritten stem is consistent with it (constant shares are needed; the shares change at 1,000 units, so the weighted margin changes from 10 to 20 USD); recomputed 3000 units"),
 fresh("AC4-a-L02-key-results-grades", "key-results table grades and sources", "L02.html:431-439", "PASS",
       "re-read the table: every T row is proved in the section cited (§2, §3, §4, §5); the C rows name Lab 1 (SIMULATED). Row at line 438 (first profitable whole volume) now reads 'Lab 1 (SIMULATED); Proposition 4.1 gives 88.89 and Remark 2.3 rounds it up to 89'. Proposition 4.1 supplies the formula 'Each zero in a segment is given by the formula of Proposition 2.2', and the value 88.89 = 1200/13.5 is the evaluation of that formula (recomputed); Remark 2.3 gives ceil(Q*) = 89. Row at 439 (5,550.00 USD, 411.11 units, 16.44%, 6.08) recomputed: OI(2500) = 5550.00, margin 2500 - 2088.89 = 411.11, 411.11/2500 = 16.44%, DOL = 13.5*2500/5550 = 6.08."),
 carry("AC4-a-L02-quiz", "L02.html:448-519"),
 carry("AC4-a-L02-hours", "L02.html:2,34"),
 carry("AC4-a-cards-L02-changed", "cards.json entries AC4-c030, c118, c119, c125"),
 carry("AC4-a-cards-r17-changed-subjects", "cards.json AC4-c004, c008, c017, c132 entries"),
 fresh("AC4-a-cards-L01-L02", "all L01/L02 flashcards: back vs current lesson text", "course/modules/AC/AC4/cards.json (38 L01 and L02 cards: AC4-c001 to c030, c118 to c120, c125, c127, c128, c130, c132)", "FAIL",
       "AC4-c007 (L01, 'True or false: the high-low line is the best line through the data') says 'the method does not minimize the error across the history'. The delta removed that clause from L01.html:279 (diff: old text 'The method does not minimize the error across the history, and it has no stated error measure' became 'the method states no error measure'), and no other L01/L02 sentence states it (grep 'minimi' in L01.html and L02.html: only the wrong quiz option at L01.html:457). The card therefore asserts a claim with no locator in the current lesson. The other 37 L01/L02 cards agree with their lesson text (numbers 10 of 12, 514.73 USD, 88.89, 2,088.89, 89, 5,550.00, 411.11, 16.44%, 6.08, 2,001 to 2,088 re-checked against the twin output). Note: the round-18 row said 37 cards; the file has 38.",
       "FIX: in course/modules/AC/AC4/cards.json, AC4-c007 back: replace 'and the method does not minimize the error across the history' with 'and the method states no error measure (Remark 3.3)'; then re-run tools/build_site.py --check."),
 fresh("AC4-a-banned-phrases", "banned phrases and process words in index, L01, L02 (grep, then each hit read)", "index.html, L01.html, L02.html", "PASS",
       "grep for roughly, about, historically, typically, usually, generally, ..., round, builder, verifier, request, unit report, minimi: each hit read; the new sentences contain none of these (the word 'half' is a number: L02.html:367, 417, 419)"),
 carry("AC4-a-hub-workspace-seed", "index.html:161 (project.html:299 NOT read this round, other slice)"),
 carry("AC4-a-hub-prereq-unlocks", "index.html"),
 carry("AC4-a-hub-objectives-placement", "index.html"),
 carry("AC4-a-hub-skill-check-rung1", "index.html"),
 fresh("AC4-a-hub-data-status", "data status: which labs use generated data", "index.html:169; tests/labs/AC4/*.py", "PASS",
       "grep for random/seed: L01, L07 and L08 twins use random.Random(seed) generators; L02, L05 and L06 twins contain no random or seed (inputs typed). Hub line 169 names 'Lessons 1, 7 and 8' for seeded data and 'the other labs use inputs the author typed': matches. L05-L08 twin changes this round are docstring and code only and do not change which labs generate data."),
 carry("AC4-a-footer-L01-L02", "L01.html:500; L02.html:535"),
 carry("AC4-a-L02-loss-volumes-printed", "L02.html:130"),
 carry("AC4-a-L02-steps-bullet", "L02.html:291"),
 carry("AC4-a-L02-key-results-profitable", "L02.html:81,433 and cards.json AC4-c125"),
 carry("AC4-a-L02-remark-2-3-whole-units", "L02.html:81"),
 fresh("AC4-a-L01-misconception-and-keyresults-grades-r17", "L01 misconception list and key-results grades", "L01.html:269-284, 399-404", "PASS",
       "re-read: item at 279 is the rewritten one checked above (ten of twelve; no error measure); grades at 399-404 match"),
 carry("AC4-a-r18-hub-lede", "index.html:30"),
 carry("AC4-a-r18-L01-why-it-matters", "L01.html:51"),
 carry("AC4-a-r18-L01-prop-3-2", "L01.html:119"),
 fresh("AC4-a-r18-L02-why-it-matters-terms", "L02 why-it-matters: terms used before they are defined in the same sentence", "L02.html:51", "PASS",
       "FAIL in round 18 is fixed. Each term is defined in the sentence or the sentence points to its definition: CVP (defined in Section 1, Definition 1.1); break-even point (defined in Section 2, Definition 2.1); 'operating income' is glossed in the same sentence ('revenue less total cost in this model'); margin of safety and operating leverage are 'both defined in Section 3' (Definition 3.1, Proposition 3.2); 'step' is glossed ('a fixed cost that jumps at a threshold volume', the Section 4 definition at L02.html:118)."),
 fresh("AC4-a-r18-L02-key-results-source-c125", "L02 key-results row for the first profitable whole volume: source column versus card AC4-c125", "L02.html:438; cards.json AC4-c125", "PASS",
       "FAIL in round 18 is fixed: the source column now reads 'Lab 1 (SIMULATED); Proposition 4.1 gives 88.89 and Remark 2.3 rounds it up to 89', and card AC4-c125 says the same (Proposition 4.1 lower-segment break-even 88.89; Remark 2.3 whole-unit rounding to 89). Recomputed: 1200/13.5 = 88.89, ceil = 89; OI(88) = -12.00 and OI(89) = 1.50 USD (twin output)."),
 carry("AC4-a-r18-cards-c008-c018-c125", "cards.json entries AC4-c008, c018, c125"),
]

# lab mutants: re-run of the ten round-18 mutants and five new ones
rows.append(fresh("AC4-a-r18-mutants-labs", "student-error mutants of the L01 and L02 twins run against each page's expected block",
    "ledgers/AC4/mutants/AC4-a-r18/ (10), ledgers/AC4/mutants/AC4-a-r19/ (5)", "PASS",
    "all 15 KILLED (ledgers/AC4/scripts/AC4-a-r19/mutants.out); lab-mutants are out of project-grader scope (architect ruling), recorded as demonstration checks"))

MUT_NAMES = [
 ("L01_m01_high_is_lowest_month", "high-low uses the lowest month as the high (r18)"),
 ("L01_m02_residual_sign_flipped", "residual sign flipped (r18)"),
 ("L01_m03_largest_signed_not_absolute", "largest signed residual, not absolute (r18)"),
 ("L01_m04_nonzero_count_counts_positive_only", "nonzero count counts positive residuals only (r18)"),
 ("L02_m01_first_whole_unit_floor", "first whole unit by floor, not ceiling (r18)"),
 ("L02_m02_scan_limit_2000", "loss scan stops at 2000 units (r18)"),
 ("L02_m03_step_applied_from_2000", "step applied from 2000 inclusive (r18)"),
 ("L02_m04_margin_of_safety_single_formula", "margin of safety from the lower zero (r18)"),
 ("L02_m05_zero_margin_accepted", "zero margin accepted (r18)"),
 ("L02_m06_planned_income_before_step", "planned income ignores the step (r18)"),
 ("L01_n01_fixed_from_low_month", "intercept from the low month, not the high (r19)"),
 ("L01_n02_slope_divides_by_hours", "slope divides by the high hours instead of the hours difference (r19)"),
 ("L02_n01_leverage_on_revenue", "operating leverage uses revenue, not contribution (r19)"),
 ("L02_n02_loss_run_end_inclusive", "loss-run end off by one (inclusive of the first profitable unit) (r19)"),
 ("L02_n03_sensitivity_plus_one_unit", "1% volume change replaced by +1 unit (r19)"),
]
mutants = []
for name, desc in MUT_NAMES:
    killed_by = "ledgers/AC4/scripts/AC4-a-r19/mutate_labs_r19.py (KILLED, ledgers/AC4/scripts/AC4-a-r19/mutants.out)"
    mutants.append({"id": name, "description": desc, "killed_by": killed_by})

now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
frag = {
 "unit": "AC4", "slice": "AC4-a", "round": 19,
 "verifier": "round-19 independent verifier (Haiku) for slice AC4-a: hub index.html, L01, L02 and lab twins lab-AC4-L01-1, lab-AC4-L02-1",
 "pin": "51fa336",
 "base": "7143726 (round-18 pin). Delta for this slice: L01.html:279, 362, 387, 459; L02.html:51, 57, 417, 438; cards.json AC4-c074, c082, c095, c108 (only c074-c108 changed, none in L01/L02). Lab twins L01/L02 and index.html unchanged; L05-L08 twins changed (other slices).",
 "checkout": "/tmp/verify19-AC4-a (detached worktree at 51fa336, .venv symlinked)",
 "scratch": "/tmp/AC4-v/a/r19",
 "verified_at": now,
 "verdict": "FAIL",
 "rows": rows,
 "mutants": mutants,
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
  "Delta re-verified line by line: L01.html:279 (misconception, nonzero residuals in ten of twelve months; no error measure), 362 (E3, lab prints months on the line exactly [6, 11]), 387 (R3, 1,201 whole hours, max error 3,990 USD = 99.75%), 459 (L01q7 explanation); L02.html:51 (why-it-matters glosses), 57 (Definition 1.1 assumptions list), 417 and 419 (R3 stem and solution), 438 (key-results source). All recomputed in ledgers/AC4/scripts/AC4-a-r19/recompute_r19.py.",
  "Fresh FAIL: card AC4-c007 back still says the method 'does not minimize the error across the history', a clause the delta removed from L01.html:279; the card must match the current lesson (CLAUDE.md, BUILDER_RULES card rule). Fix: edit the back of AC4-c007 in course/modules/AC/AC4/cards.json to replace 'and the method does not minimize the error across the history' with 'and the method states no error measure (Remark 3.3)', then run tools/build_site.py --check.",
  "Round-18 FAIL rows AC4-a-r18-L02-why-it-matters-terms and AC4-a-r18-L02-key-results-source-c125 are fixed and PASS now.",
  "Carried rows state the cited lines byte-identical since 7143726; for L01.html and L02.html the carry prefix names the cited lines because the files changed elsewhere (hunks listed in base). Rows whose cited lines are inside a changed hunk were re-verified.",
  "Hub index.html is byte-identical since the previous pin, so its carried rows keep the round-18 evidence; the hub data-status row (cites tests/labs/AC4/*.py) and the hours row were re-verified fresh because the twins and lesson eyebrows were read again.",
  "Alternative correct implementations (over-constraint check) were not run: the slice is lesson text and demonstration labs, and the architect ruling makes lab twins demonstrations; the project-grader alternatives belong to the project slice.",
 ],
 "summary": "",
 "__RESULT__": None,
}
rows_pass = sum(1 for r in rows if r["status"] == "PASS")
rows_fail = sum(1 for r in rows if r["status"] == "FAIL")
frag["summary"] = (f"Slice AC4-a round 19 (pin 51fa336): {len(rows)} rows; {rows_pass} PASS, {rows_fail} FAIL "
                   f"(AC4-a-cards-L01-L02: card AC4-c007 keeps a clause the delta removed from L01.html:279). "
                   f"Round-18 FAIL rows fixed. {len(mutants)} lab mutants (10 re-run, 5 new) all killed.")
del frag["__RESULT__"]
json.dump(frag, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", OUT, len(rows), rows_pass, rows_fail)
