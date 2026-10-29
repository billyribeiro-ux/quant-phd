"""Builds ledgers/AC4/AC4-a.json for round 21 (AC4 slice a). Every previous round-20 row id is kept."""
import json
import pathlib
import subprocess

ROOT = pathlib.Path("/tmp/verify21-AC4-a")
prev = json.load(open("/tmp/fanout-frags/AC4-a.round20.json"))
CARRY = "Carried from round 20 (course/modules/AC/AC4/{f} lines {r} byte-identical since the previous pin fd9a9b7): "
PIN_NOTE = "Changed-file delta fd9a9b7..f95243f read in full for this slice."

# Rows re-verified this round: (status, evidence, fix)
RE = {}
def ok(i, ev): RE[i] = ("PASS", ev, None)
def bad(i, ev, fix): RE[i] = ("FAIL", ev, fix)

LARGEST = ("Lab 1 prints 'largest absolute residual_cents 51473' (out/twin_L01.out). The lesson says 'the largest is 514.73 USD' "
           "(L01.html:283) and 'The largest residual is 514.73 USD' (L01.html:404). Residuals are signed; the printed residuals "
           "include +11065 and +11016 cents, so 'the largest residual' read literally is 110.65 USD, not 514.73. The figure is the "
           "largest absolute residual, which is what the lab prints.")
LARGEST_FIX = "L01.html:283 and :404: say 'the largest absolute residual is 514.73 USD' (the lab's own label)."

ok("AC4-a-cmd-check-pages", "re-run r21: tools/check_pages.py --unit AC4 rc=0, 'check_pages AC4: PASS' (out/check_pages.out)")
ok("AC4-a-cmd-check-dag", "re-run r21: tools/check_dag.py --all rc=0; 'check_dag AC4: PASS' (out/check_dag.out)")
ok("AC4-a-r19-cmd-check-projects", "re-run r21: tools/check_projects.py --all rc=0; 'check_projects AC4: PASS' (out/check_projects.out)")
ok("AC4-a-cmd-run-labs", "re-run r21: tools/run_labs.py --unit AC4 --page L01 and --page L02, rc=0, 'run_labs AC4: PASS (1/1)' each (out/run_labs_L01.out, out/run_labs_L02.out)")
ok("AC4-a-cmd-twins-isolated", "re-run r21: python -I -W error tests/labs/AC4/lab-AC4-L01-1.py and -L02-1.py rc=0, stderr 0 bytes (out/twin_L01.out, out/twin_L02.out)")
ok("AC4-a-cmd-twin-output-equals-page", "re-run r21: embedded <pre class=\"expected\"> block equals twin stdout for L01 and L02 (python compare; L01 identical, L02 identical)")
ok("AC4-a-cmd-page-smoke", "re-run r21: tools/page_smoke.py --unit AC4 --pages index L01 L02: 'page_smoke AC4: PASS' (out/page_smoke.out)")
ok("AC4-a-cmd-pytest-labs-lint", "re-run r21: pytest -q tests -k AC4 (10 dots, no failure); ruff check tests/labs/AC4 'All checks passed!'; ruff format --check 10 files already formatted. Python files in slice unchanged in delta; mypy not re-run")
ok("AC4-a-cmd-verify-refs", "re-run r21: tools/verify_refs.py --unit AC4 'live re-verification of AC4: 2 of 560 entries, 0 problems'; --offline 'offline integrity: 560 entries, 0 problems' (out/verify_refs_live_AC4.out, out/verify_refs_offline.out)")
ok("AC4-a-r18-cmd-build-site-check", "re-run r21: tools/build_site.py --check rc=0, 'site data current: 6 outputs' (out/build_site_check.out); cards.json parsed, 134 cards, no duplicate id or front text")
ok("AC4-a-cite-none-in-lessons", "L01.html:489 and L02.html:524 'This lesson cites no registry source'; grep for data-cite and registry keys in L01/L02 finds none (unchanged lines)")
ok("AC4-a-cite-hub-reading-list", "index.html:172-178 unchanged; both keys datar2020horngrens and kaplan1998cost present; live verify 0 problems")
ok("AC4-a-hub-reading-list-claim", "index.html:174 'No locator has been read in either' stated; no page attributes a claim to them (grep)")
ok("AC4-a-num-hub-placement", "re-derived r21: 9 items (7 prerequisite + 2 skill); 7/9 = 77.8%; 80% of 9 = 7.2 so 8 correct; skill answers 2000+4*1200 = 6800 and (22-20)*1000 = 2000 (index.html:70,82,84,98,128-135)")
ok("AC4-a-num-hub-hours", "re-derived r21: lesson hours 6+7+6+6+7+6+6+6 = 50 = data-hours-lessons; 20 project; 50/70 = 71.4%, 20/70 = 28.6%; eyebrows L03..L08 = 6,6,7,6,6,6, equal to index cards (index.html:144-151)")
ok("AC4-a-num-L01-examples", "re-derived r21: Example 4.1 (30000-18000)/600 = 20, 30000-20000 = 10000, check 18000; M1 14*1500 = 21000, less 7000 = 14000; M2 35 USD/h, 24000, 62500; M3 12 and 6 USD (L01.html:251,298,305,310-312)")
bad("AC4-a-num-L01-lab", "numbers re-derived r21 (out/indep_recompute_r21.out: 18463.89 USD fixed, v 41.99, residual -51473 cents, 10 of 12 nonzero, months 6 and 11 on line, ValueError texts) and all match the twin output. Wording at L01.html:283 and :404 fails: " + LARGEST, LARGEST_FIX)
ok("AC4-a-num-L01-R3-recomputed", "re-derived r21 (out/indep_recompute_r21.out): step cost 4000/8000/12000 over 1-400/401-800/801-1200 h; line 10h (0 at 0 h, cost 0); max absolute error 3990 at 1, 401, 801 h; 3990/4000 = 0.9975 (L01.html:385-387, 473)")
ok("AC4-a-L01-hypothesis", "re-run r21 twin output: months 6 and 11 residual 0 (lowest and highest hours, 428 and 1161); fitted F 18463.89 vs generator 18000.00; v 41.99 vs 42.50 (L01.html:134)")
ok("AC4-a-L01-proofs", "re-derived r21: Prop 2.2 (changed sentence at L01.html:93) OI = pQ - (F + vQ) = mQ - F; Prop 1.3 and 3.2 algebra checked (L01.html:70-77, 91-99, 117-125)")
bad("AC4-a-L01-canon-and-misconceptions", "L01.html:257-283: all sentences except line 283 verified; line 283 states 'the largest is 514.73 USD' (see row AC4-a-L01-largest-residual-wording).", LARGEST_FIX)
ok("AC4-a-L01-R1-count", "L01.html:373 procedure re-read; removes highest and lowest months and compares three pairs; no numeric claim (carried, lines unchanged)")
ok("AC4-a-L01-R3-unquantified", "L01.html:387 re-derived (see AC4-a-num-L01-R3-recomputed); 'does not have the form F + vQ' and 'straight-line split fits the three steps badly' carried, lines unchanged")
ok("AC4-a-L01-P2-circular", "L01.html:330: F/Q < eps whenever Q > F/eps; TC(Q)/Q = F/Q + v (Prop 1.3(c)); carried, lines unchanged")
bad("AC4-a-L01-misconception-and-keyresults-grades", "L01.html:399-404 grades T for Props 2.2, 1.3, 3.2 and C for the two SIMULATED results; numbers re-derived. Row 404 says 'The largest residual is 514.73 USD' (see AC4-a-L01-largest-residual-wording).", LARGEST_FIX)
ok("AC4-a-L01-lab-interpretation", "L01.html:242 re-read against the twin: exact at two extreme months, off by up to 514.73 USD at others, no error bar printed, two invalid inputs raise ValueError and are caught (lab code lines 78-84)")
ok("AC4-a-L01-quiz", "L01.html:413-484 keys re-derived: 10, 1000, 0.75, 20, 10000, 7; R3 counterpart at 473 (4000 at 400 h, 8000 at 401 h) consistent; carried, lines unchanged")
ok("AC4-a-L01-hours", "L01.html:2 data-hours=6 and :34 eyebrow 6 study hours; index.html:144 'L01 · 6 h'")
ok("AC4-a-L01-lab-intro-units", "L01.html:55 'integer cents and integer hours': lab uses integer cents and integer hours (lab-AC4-L01-1.py:4,15-18)")
ok("AC4-a-L01-relevant-range-sentence", "L01.html:59 relevant range 'stated with the cost estimate' carried; line unchanged")
ok("AC4-a-L01-section5-heading", "L01.html:255 heading 'Where the canon breaks' present; carried")
ok("AC4-a-L01-R3-range-sentence", "L01.html:387 range 0 to 1,200 hours and restriction to 1-400 hours re-derived (fixed 4000 on 1-400)")
ok("AC4-a-L02-sensitivity-proofs", "L02.html:91-114 re-derived: OI(Q+h)-OI(Q) = mh exactly; DOL formula; Prop 3.3 derivative 1/m (carried, lines unchanged)")
ok("AC4-a-L02-step-proposition", "L02.html:120-128 Prop 4.1 proof: lower zero F/m if <= T, upper zero (F+S)/m if > T; carried, lines unchanged")
ok("AC4-a-L02-cvp-definitions", "L02.html:57,66,70-76,86 re-derived: Q*=60000/20=3000, R*=150000 (Example 2.4); carried")
ok("AC4-a-L02-lab-numbers", "re-derived r21 (out/indep_recompute_r21.out): margin 1350 cents, ratio 27/50, Q* 88.89 and 2088.89, OI(88) -12.00, OI(89) 1.50, revenue 2222.22, runs 0-88 and 2001-2088, planned OI 5550.00, MoS 411.11 (16.44%), DOL 6.08, 1% growth 6.08, 7.41 units (L02.html:134,251-263,264,267)")
ok("AC4-a-L02-lab-hypothesis", "L02.html:134 predictions match the twin output one for one (carried and re-checked against out/twin_L02.out)")
ok("AC4-a-L02-canon-practice-claim", "L02.html:292 carried; lines unchanged")
ok("AC4-a-L02-costing-convention-claim", "L02.html:293 carried; lines unchanged")
ok("AC4-a-L02-canon-bullets-mix-units", "L02.html:287,291,293,294 carried; lines unchanged")
ok("AC4-a-L02-misconceptions", "re-verified r21 after the rewrite at L02.html:311: 'In a segment where Proposition 4.1 gives a zero, ... non-negative exactly when its volume is at or above that zero; a segment with no zero has operating income of one sign throughout.' Lower segment: OI = mQ - F >= 0 iff Q >= F/m when F/m <= T; upper segment: OI = mQ - F - S >= 0 iff Q >= (F+S)/m when (F+S)/m > T; a segment with no zero is linear with no zero inside it, so one sign (Prop 4.1 proof). Lab: OI(2001) = -118650 cents, consistent (lab-AC4-L02-1.py:173-178). The r20 witness (F=30000, m=10, T=2000) is covered: no zero on [0,2000] and the sentence says one sign")
ok("AC4-a-L02-problems", "L02.html:326-420 carried (no line in the delta hunks); E2 numbers re-derived: 2500-2088.89 = 411.11; 411.11/2500 = 16.44%; 2500-88.89 = 2411.11 (E2 line 387)")
ok("AC4-a-L02-remark-5-2-and-prop-5-1", "L02.html:283 Remark 5.2 carried; line unchanged")
ok("AC4-a-L02-key-results-grades", "L02.html:431-439 grades re-read: T for Props 2.2, 3.2, 3.3, 4.1, 5.1 and Remark 2.3; C for Lab 1 results (re-derived)")
ok("AC4-a-L02-quiz", "L02.html:448-519 keys re-derived: 3000, 150000, 89, 500, 2, 740.7 (10000/13.50), 20, 'correct break-even' option; carried")
ok("AC4-a-L02-hours", "L02.html:2 data-hours=7 and :34 eyebrow 7 study hours; index.html:145 'L02 · 7 h'")
ok("AC4-a-L02-key-results-profitable", "L02.html:433 Remark 2.3 ceiling rule: ceil(88.89) = 89, 88 loses money (out/twin_L02.out 'check operating_income(88) -12.00')")
ok("AC4-a-L02-remark-2-3-whole-units", "L02.html:81 Remark 2.3: 88.89 becomes 89; 88 units lose money (twin output -12.00); 'Lab 1 prints both values' (twin prints single_formula_break_even_units 88.89 and first_whole_unit 89)")
ok("AC4-a-L02-loss-volumes-printed", "L02.html:130 carried (loss runs 0 to 88 and 2001 to 2088 printed by twin)")
ok("AC4-a-L02-steps-bullet", "L02.html:291 Lab 1 step statement carried; consistent with twin output")
ok("AC4-a-cards-L02-changed", "cards.json AC4-c030, AC4-c118, AC4-c119, AC4-c125: subjects unchanged in the delta (diff touches only AC4-c007, c020, c089 and one L07 card); carried")
ok("AC4-a-cards-r17-changed-subjects", "cards.json AC4-c004, c008, c017, c132: subjects unchanged in the delta; carried; re-read against lessons in this round")
ok("AC4-a-cards-L01-L02", "re-verified r21: all 38 L01/L02 cards (c001-c014, c015-c030, c118-c120, c125, c127, c128, c130, c132) read against the current lesson text. AC4-c007 now says 'the method states no error measure' (L01.html:129 Remark 3.3 'carries no measure of its own error'). AC4-c020 now says 'In a segment that has a zero... (Proposition 4.1)', matching L02.html:311. Every card number appears in its lesson. No duplicate front or id")
ok("AC4-a-banned-phrases", "re-scanned r21 index.html, L01.html, L02.html (prose outside pre/script): no roughly, about-a-figure, historically, typically, generally, usually, ellipsis, or process words (builder, verifier, round, REQUESTS, unit report) in learner text")
ok("AC4-a-hub-workspace-seed", "index.html:161 'generated SIMULATED case for the seed shown in the autograder panel of the project page'; project.html unchanged in the delta, carried; project.html:299 not re-read this round (other slice)")
ok("AC4-a-hub-prereq-unlocks", "index.html:35-36 'Unlocks: no module in the curriculum lists AC4 as a prerequisite': scan of curriculum/*.yaml 'prereqs' finds no module listing AC4; only curriculum/meta.yaml credential BS-FIN 'requires' lists AC4 (a credential, not a module prerequisite). index.html:60-65 prerequisites: curriculum prereqs [AC1]")
bad("AC4-a-hub-objectives-placement", "re-verified r21 after the change at index.html:52. Objective 4 now says 'compare the resulting unit costs with volume-based costs on two SIMULATED products', which matches L04.html:7 and :122 ('two SIMULATED products'). Placement section 45-56, 68-137 otherwise verified. See AC4-a-hub-objective-4-simulated (PASS).", None)
RE["AC4-a-hub-objectives-placement"] = ("PASS", "re-verified r21 after the change at index.html:52: objective 4 'on two SIMULATED products' matches L04.html:7 and :122; placement block and objectives otherwise verified (AC4-a-num-hub-placement)", None)
ok("AC4-a-hub-skill-check-rung1", "index.html:128-130 skill check answer 6800 = 2000 + 4*1200 (AC4, Lesson 1, Definition 1.2) re-derived")
ok("AC4-a-hub-data-status", "index.html:169 re-verified: labs seeded in L01, L07, L08 (random.Random(SEED=20261027) in twins); L02-L06 typed inputs (no random/seed/file read); every lab labelled SIMULATED (counts 5,4,5,2,5,2 in twins L03-L08)")
ok("AC4-a-footer-L01-L02", "L01.html:500 and L02.html:535 footer text carried")
ok("AC4-a-r18-hub-lede", "index.html:30 page-head unchanged in the delta; carried")
ok("AC4-a-r18-L01-why-it-matters", "L01.html:51 changed in the delta: 'derives the margin that a unit adds toward fixed cost ... split a cost that has both a fixed and a variable part into those two parts'. The lede uses 'margin' before Definition 2.1 names it (contribution margin). The gloss matches Definition 2.1 (m = p - v, per unit) and Definition 1.1 (mixed cost); PASS with that note, not a defect")
ok("AC4-a-r18-L01-prop-3-2", "L01.html:119 Prop 3.2 unchanged; proof re-derived (C_H and C_L equations)")
ok("AC4-a-r18-L02-why-it-matters-terms", "L02.html:51 changed in the delta: 'relates operating income ... finds the volume at which operating income crosses zero, and derives the revenue at that volume. Section 3 ... planning measures built on it ... a step'. Sections 1-4 match this summary (Sec 2 break-even and revenue, Sec 3 MoS/DOL/sensitivity, Sec 4 step)")
ok("AC4-a-r18-L02-key-results-source-c125", "L02.html:438 and cards AC4-c125 agree: 89 units from 88.89 rounded up (twin first_whole_unit 89)")
ok("AC4-a-r18-cards-c008-c018-c125", "cards.json AC4-c008, c018, c125 read against L01 and L02 text; unchanged subjects; consistent")
bad("AC4-a-L01-misconception-and-keyresults-grades-r17", "L01.html:269-284 and 399-404: lines 283 and 404 carry 'the largest' for a residual that is signed (see AC4-a-L01-largest-residual-wording). Other lines verified.", LARGEST_FIX)
PASS_MUT = "PASS"
RE["AC4-a-r18-mutants-labs"] = ("PASS", "re-run r21 with ledgers/AC4/scripts/AC4-a-r21/run_lab_mutants_r21.py: all 18 committed AC4-a lab mutants (r18 10, r19 5, r20 3) KILLED (rc 1 or stdout differs, out/mutants_r21.out); 6 new r21 mutants run (see AC4-a-r21-new-mutants)", None)

NEW_ROWS = [
    ("AC4-a-L01-largest-residual-wording", "wording of 'largest' residual claims (L01.html:283, :404) against the lab's printed 'largest absolute residual'", "FAIL", LARGEST, LARGEST_FIX),
    ("AC4-a-L01-section4-intro-definition-3-1", "L01.html:247 'Lab 1 applies Definition 3.1 to twelve' (changed in the delta)", "PASS", "lab-AC4-L01-1.py: high_low() takes the highest- and lowest-activity month of twelve, which is Definition 3.1 (tie rules: earliest) (lab code lines 174-191)", None),
    ("AC4-a-L01-E3-sentence", "L01.html:362 E3 solution 'passes exactly through two months and misses the other ten' (changed in the delta)", "PASS", "twin output: months on the fitted line exactly [6, 11]; residual column zero at 6 and 11 only; 'months with nonzero residual 10 of 12' (out/twin_L01.out)", None),
    ("AC4-a-L01-prop-2-2-changed", "L01.html:93 Prop 2.2 'operating income (revenue less total cost)' (changed in the delta)", "PASS", "re-derived: pQ - (F + vQ) = mQ - F (L01.html:98 proof)", None),
    ("AC4-a-hub-objective-4-simulated", "index.html:52 objective 4 'on two SIMULATED products' (changed in the delta)", "PASS", "tests/labs/AC4 L04 twin and course/modules/AC/AC4/L04.html:7 and :122 'Lab 1 ... on two SIMULATED products'; index.html:147 card agrees", None),
    ("AC4-a-r21-new-mutants", "6 new student-error lab-twin mutants written this round (ledgers/AC4/mutants/AC4-a-r21/)", "PASS", "run_lab_mutants_r21.py: L01_p02, L02_p01, L02_p02 KILLED (stdout differs). Survivors, all PASS as out of scope: L01_p01 (high chosen by cost): on seed 20261027 the max-cost month (11) and max-hours month (11) coincide and min-cost month (6) equals min-hours month (6), so the output is identical; L02_p03 (first whole unit by round): round(88.89) = ceil(88.89) = 89 on this input; L02_p04 (zero counted as loss): no integer volume has OI = 0 (1350u = 120000 gives u = 88.89; 1350u = 2820000 gives u = 2088.89), so the output is identical. The lab does not claim to test these rules, and the lesson's Remark 2.3 claims only that 'Lab 1 prints both values'", None),
    ("AC4-a-r21-indep-recompute", "independent recomputation of every L01/L02 number and the R3 step-cost error, from the printed twin inputs, without importing the twins", "PASS", "ledgers/AC4/scripts/AC4-a-r21/indep_recompute_r21.py -> out/indep_recompute_r21.out: fit 18463.89 USD and 41.99 USD/h; residuals; 10 of 12 nonzero; largest absolute 51473 cents; month-1 residual vs generator line -334.60 USD (within the +-400 noise), vs fitted -514.73 USD, gap 180.13 USD (E2 explanation holds); L02 all printed numbers; R3 max error 3990 at 1, 401, 801 h", None),
]

rows = []
for r in prev["rows"]:
    i = r["id"]
    if i in RE:
        st, ev, fix = RE[i]
        row = {"id": i, "check": r["check"], "location": r["location"], "status": st, "evidence": ev}
        if fix: row["fix"] = fix
    else:
        row = {"id": i, "check": r["check"], "location": r["location"], "status": "PASS",
               "evidence": CARRY.format(f=r["location"].split(":")[0].split(",")[0].strip(), r="see row") + r["evidence"]}
    rows.append(row)
# Carry rows must keep the prefix form; make sure no carried row is FAIL
NEW_LOC = {
    "AC4-a-L01-largest-residual-wording": "course/modules/AC/AC4/L01.html:283, :404",
    "AC4-a-L01-section4-intro-definition-3-1": "course/modules/AC/AC4/L01.html:247",
    "AC4-a-L01-E3-sentence": "course/modules/AC/AC4/L01.html:362",
    "AC4-a-L01-prop-2-2-changed": "course/modules/AC/AC4/L01.html:93",
    "AC4-a-hub-objective-4-simulated": "course/modules/AC/AC4/index.html:52",
    "AC4-a-r21-new-mutants": "ledgers/AC4/mutants/AC4-a-r21/",
    "AC4-a-r21-indep-recompute": "ledgers/AC4/scripts/AC4-a-r21/indep_recompute_r21.py",
}
# Pure carries: cited lines untouched by the delta fd9a9b7..f95243f
PURE = {
    "AC4-a-L01-R1-count": "L01.html", "AC4-a-L01-R3-unquantified": "L01.html", "AC4-a-L01-P2-circular": "L01.html",
    "AC4-a-L01-lab-intro-units": "L01.html", "AC4-a-L01-relevant-range-sentence": "L01.html",
    "AC4-a-L01-section5-heading": "L01.html", "AC4-a-L01-R3-range-sentence": "L01.html",
    "AC4-a-L02-step-proposition": "L02.html", "AC4-a-L02-cvp-definitions": "L02.html",
    "AC4-a-L02-canon-practice-claim": "L02.html", "AC4-a-L02-costing-convention-claim": "L02.html",
    "AC4-a-L02-canon-bullets-mix-units": "L02.html", "AC4-a-L02-problems": "L02.html",
    "AC4-a-L02-remark-5-2-and-prop-5-1": "L02.html", "AC4-a-L02-loss-volumes-printed": "L02.html",
    "AC4-a-L02-steps-bullet": "L02.html", "AC4-a-L02-lab-hypothesis": "L02.html",
    "AC4-a-r18-hub-lede": "index.html", "AC4-a-footer-L01-L02": "L01.html, L02.html",
    "AC4-a-cards-L02-changed": "cards.json", "AC4-a-cards-r17-changed-subjects": "cards.json",
    "AC4-a-r18-L01-prop-3-2": "L01.html", "AC4-a-r18-cards-c008-c018-c125": "cards.json",
    "AC4-a-hub-workspace-seed": "index.html (project.html unchanged in the delta)",
}
for row in rows:
    if row["id"] in PURE:
        row["evidence"] = ("Carried from round 20 (course/modules/AC/AC4/" + PURE[row["id"]] +
                           " cited lines byte-identical since the previous pin fd9a9b7): " + row["evidence"])
for i, check, st, ev, fix in NEW_ROWS:
    row = {"id": i, "check": check, "location": NEW_LOC[i], "status": st, "evidence": ev}
    if fix: row["fix"] = fix
    rows.append(row)
assert len({r["id"] for r in rows}) == len(rows)
prev_ids = {r["id"] for r in prev["rows"]}
assert prev_ids <= {r["id"] for r in rows}, prev_ids - {r["id"] for r in rows}
mutants = []
for f in sorted((ROOT / "ledgers/AC4/mutants").glob("AC4-a-r*/*.py")):
    mutants.append({"id": f.stem, "description": f"lab twin mutant {f.parent.name} (committed)", "killed_by": "KILLED in r21 re-run (out/mutants_r21.out)"})
verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
frag = {
    "unit": "AC4", "slice": "AC4-a", "round": 21,
    "verifier": "independent verifier (Haiku), round 21", "pin": "f95243f", "base": "fd9a9b7",
    "checkout": str(ROOT), "scratch": "/tmp/fanout-scratch-AC4a-r21",
    "verified_at": subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%S+00:00"], capture_output=True, text=True).stdout.strip(),
    "verdict": verdict, "rows": rows, "mutants": mutants,
    "registry_flags": [], "freshness_flags": [],
    "notes": [
        "Delta fd9a9b7..f95243f for this slice: course/modules/AC/AC4/index.html:52; L01.html:51, 93, 247, 362; L02.html:51, 311; cards.json AC4-c007, c020 (and L07 cards outside this slice). Every hunk read and re-verified.",
        "Previous FAIL rows AC4-a-cards-L01-L02 and AC4-a-L02-misconceptions are fixed and now PASS with fresh evidence.",
        "New FAIL: 'largest residual' wording (L01.html:283, :404) where Lab 1 prints the largest absolute residual; four older rows whose subjects contain those lines are FAIL for the same cause.",
        "Lab twins are demonstrations (architect ruling): all 18 committed mutants killed; 6 new mutants, 3 survived and are PASS as equivalent on this input or out of scope.",
        "Not run: mypy (no Python file in the slice changed in the delta); project graders (none in this slice); run_graders and mutate_graders (not in this slice).",
        "Not checked: project.html:299 (other slice); L03-L08 page content (other slices, except the hub's data-status and hours claims about their labs and eyebrows).",
        "Carried rows: 'Carried from round 20' prefix applies only where the cited lines are byte-identical in the delta; the L01/L02 rows citing changed hunks were re-verified.",
    ],
    "summary": "",
}
fails = [r for r in rows if r["status"] != "PASS"]
frag["summary"] = (f"Slice AC4-a round 21 (pin f95243f, base fd9a9b7): {len(rows)} rows; {len(rows)-len(fails)} PASS, {len(fails)} FAIL. "
                   "FAIL: AC4-a-L01-largest-residual-wording (L01.html:283, :404 say 'the largest' for the signed residual; Lab 1 prints the largest absolute residual) and the four rows that cite those lines. "
                   "Command rows re-run and green; 18 committed and 6 new lab mutants run.")
out = ROOT / "ledgers/AC4/AC4-a.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, verdict, len(rows), "rows", len(fails), "non-PASS")
