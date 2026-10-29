"""Round 27 (AC4-a): build ledgers/AC4/AC4-a.json. Every row id of the previous fragment is kept.

Each row's evidence states what was run or read in this round; no row is carried from round 26.
"""
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
prev = json.loads(Path("/tmp/fanout-frags/AC4-a.round26.json").read_text())
OUT = "ledgers/AC4/scripts/AC4-a-r27/out/"
RE = "Re-verified this round (round 27, pin 404db23): "

ev = {
    "AC4-a-cmd-check-pages": "command tools/check_pages.py --unit AC4 -> 'check_pages AC4: PASS', rc=0 (" + OUT + "check_pages.out)",
    "AC4-a-cmd-check-dag": "command tools/check_dag.py --all -> AC4: PASS and all units PASS, rc=0 (" + OUT + "check_dag.out)",
    "AC4-a-r19-cmd-check-projects": "command tools/check_projects.py --unit AC4 -> 'check_projects AC4: PASS', rc=0 (" + OUT + "check_projects.out)",
    "AC4-a-cmd-run-labs": "command tools/run_labs.py --unit AC4 -> 'run_labs AC4: PASS (10/10)', rc=0 (" + OUT + "run_labs.out)",
    "AC4-a-cmd-twins-isolated": "cd /tmp; /tmp/verify27-AC4-a/.venv/bin/python -I -W error on lab-AC4-L01-1.py and lab-AC4-L02-1.py -> rc=0, empty stderr (/tmp/AC4-v/AC4-a-r27/*.out, *.err)",
    "AC4-a-cmd-twin-output-equals-page": "ledgers/AC4/scripts/AC4-a-r27/twin_equals_embedded (r26 script re-run) -> L01 stdout == embedded True, 20 lines; L02 True, 13 lines (" + OUT + "twin_equals_embedded.out)",
    "AC4-a-cmd-page-smoke": "command tools/page_smoke.py --unit AC4 --pages index, L01, L02 -> 'page_smoke AC4: PASS', rc=0 (" + OUT + "page_smoke.out)",
    "AC4-a-cmd-pytest-labs-lint": "pytest -q -k AC4 -> 10 passed, rc=0; ruff check tests/labs/AC4 -> 'All checks passed!'; ruff format --check -> '10 files already formatted'; mypy --no-incremental on the two twins -> 'Success: no issues found in 2 source files' (" + OUT + "pytest_ac4.out, ruff_*.out, mypy_twins.out)",
    "AC4-a-cmd-verify-refs": "tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', rc=0; tools/verify_refs.py --unit AC4 (live) -> '2 of 560 entries, 0 problems', rc=0 (" + OUT + "verify_refs_*.out)",
    "AC4-a-r18-cmd-build-site-check": "tools/build_site.py --check -> 'site data current: 6 outputs', rc=0 (" + OUT + "build_site_check.out)",
    "AC4-a-cite-none-in-lessons": "grep -c data-cite L01.html = 0, L02.html = 0; the two lessons say 'This lesson cites no registry source' (L01.html:487-491 (section 10); L02.html:522-526 (section 11))",
    "AC4-a-cite-hub-reading-list": "index.html:176-177 data-cite datar2020horngrens and kaplan1998cost; both keys present in references/references.json (entries, verified_by openlibrary)",
    "AC4-a-hub-reading-list-claim": "index.html:174 says no locator has been read and no page attributes a claim to the two books. grep -i datar|kaplan over course/modules/AC/AC4/*.html finds only data-cite lines (index.html:176-177, project.html:407-408). The unread status itself is the author's statement and is not checkable; the page-level non-attribution is checked.",
    "AC4-a-num-hub-placement": RE + "index.html:70: nine items (seven prerequisite, two skill check); 80% of 9 = 7.2 so 8 correct needed; 7/9 = 77.8% (computed); skill check answers 6800 (2000+4*1200) and 2000 ((22-20)*1000) recomputed.",
    "AC4-a-num-hub-hours": RE + "lesson eyebrows L01 6, L02 7, L03 6, L04 6, L05 7, L06 6, L07 6, L08 6 sum to 50; index.html data-hours-lessons=50, data-hours-project=20; 50/70=71.4%, 20/70=28.6%; hub card kickers match the eyebrows.",
    "AC4-a-num-L01-examples": RE + "Example 1.4 6000/500=12, 6000/1000=6; Example 4.1 v=20, F=10000, check 18000; M1 m=14, ratio 0.35, OI 14000; M2 v=35, F=24000, fitted 62500 (indep_recompute_r27.py, OK rows).",
    "AC4-a-num-L01-lab": RE + "all lab-quoted numbers (fixed 18,463.89 USD; 41.99 USD/h; residual 514.73 USD; 10 of 12; months 6 and 11; 428 and 1161 hours; E1 cents 3,643,546 and 6,721,387 -> 36,435.46 and 67,213.87) recomputed from the seeded random stream (indep_recompute_r27.out, all OK).",
    "AC4-a-num-L01-R3-recomputed": RE + "R3 step cost recomputed at all 1,201 whole hours 0..1200: max abs error 3990 at hours 1, 401, 801; 3990/4000 = 99.75%; line values 10, 4010, 8010 (indep_recompute_r27.out, OK).",
    "AC4-a-L01-hypothesis": RE + "L01.html:134 hypothesis: residuals 0 at the two extreme months (lab prints months [6, 11]); generator parameters 18000 USD / 42.50 USD per hour; noise 400 USD either way; output matches.",
    "AC4-a-L01-proofs": RE + "Props 1.3, 2.2, 3.2 and proofs (L01.html:70-77, 91-99, 117-125) re-derived: F/Q strictly decreasing, OI = mQ - F, zero residuals at Q_H and Q_L with unique slope since Q_H != Q_L.",
    "AC4-a-L01-canon-and-misconceptions": RE + "L01.html:257-283: four canon bullets (count = 4, matches 'four conditions'); four misconceptions; 10 of 12 and 514.73 USD match the lab output.",
    "AC4-a-L01-R1-count": RE + "R1 procedure (remove an extreme month and re-fit) reads correctly; count statements at L01.html:373 consistent.",
    "AC4-a-L01-R3-unquantified": RE + "R3 solution (L01.html:385-387) states the step is not linear and quantifies the error 3,990 USD, 99.75% of the step (recomputed).",
    "AC4-a-L01-P2-circular": RE + "P2 (L01.html:330) limit proof uses only F/Q < epsilon for Q > F/epsilon and Prop 1.3(c); no circularity.",
    "AC4-a-L01-misconception-and-keyresults-grades": RE + "key-results table L01.html:399-404: T rows are proved in sections 1-3; C rows name Lab 1 (SIMULATED); the 18,463.89 / 41.99 / 514.73 / 10 of 12 values match the output.",
    "AC4-a-L01-lab-interpretation": RE + "L01.html:242 interpretation: 'off by up to 514.73 USD at the others' (true: max 51,473 cents at month 1, extremes 0); the lab prints fitted parameters, residuals, months on the line, count, and two ValueError cases; no error bar claim is contradicted.",
    "AC4-a-L01-quiz": RE + "all ten L01 quiz items answered and checked: 25-15=10; 10*500-4000=1000; (40-10)/40=0.75; 20; 10000; 7000/1000=7; step cost option; relevant-range option; q7 explanation now reads 'may carry residuals' (the round 26 fix, L01.html:459, verified).",
    "AC4-a-L01-hours": RE + "L01.html:2 data-hours=6 and eyebrow '6 study hours' (L01.html:34 area); curriculum AC4 hours 70 and hub split 50 lesson hours.",
    "AC4-a-L01-lab-intro-units": RE + "L01.html:55 intro states the units (machine hours, USD per period, integer cents and hours).",
    "AC4-a-L01-relevant-range-sentence": RE + "L01.html:59 (Definition 1.1) relevant-range sentence read: the range is stated with the cost estimate; card AC4-c001 matches it.",
    "AC4-a-L01-section5-heading": RE + "L01.html:255 Section 5 heading 'Where the canon breaks' and its four bullets (L01.html:257-262) read in full.",
    "AC4-a-L01-R3-range-sentence": RE + "L01.html:387 R3 range sentence (0 to 1,200 hours) and last sentence (answer depends on treating the range as 0 to 1,200; restricted 1-400 gives fixed 4,000 USD) read and recomputed.",
    "AC4-a-L02-sensitivity-proofs": RE + "Props 3.2 and 3.3 proofs (L02.html:91-114) re-derived: OI(Q+h)-OI(Q)=mh; ratio DOL*h/Q; dQ*/dF = 1/m. Sensitivity claims 6.08 and 7.41 recomputed.",
    "AC4-a-L02-step-proposition": RE + "Prop 4.1 statement (L02.html:120-128): strictly increasing on [0,T] and (T,inf), drop of S at T, at most one zero per segment; proof re-derived. Notation issue on T is a separate FAIL row (AC4-a-notation-T).",
    "AC4-a-L02-cvp-definitions": RE + "Def 1.1 cross-reference 'Lesson 1, Proposition 2.2' (exists at L01.html Prop 2.2); Def 2.1; assumptions read at L02.html:57,66,70-76,86.",
    "AC4-a-L02-lab-numbers": RE + "L02.html:134,251-263,264,267: 88.89, first whole 89, OI(88) -12.00, OI(89) 1.50, revenue 2222.22, 2088.89, runs 0-88 and 2001-2088, 5550.00, 411.11 (16.44%), 6.08, 7.41 all recomputed (indep_recompute_r27.out).",
    "AC4-a-L02-lab-hypothesis": RE + "L02.html:134 hypothesis predictions (margin 13.50, 88.89 -> 89, runs, 2,088.89, 5,550.00, 7.41) match the lab output.",
    "AC4-a-L02-canon-practice-claim": RE + "L02.html:292 section 6 bullets (four features) read; steps bullet and estimates bullet consistent with Prop 4.1 and Lesson 1 Remark 3.3.",
    "AC4-a-L02-costing-convention-claim": RE + "L02.html:293 units produced equal to units sold; no claim about reported income beyond the model (read).",
    "AC4-a-L02-canon-bullets-mix-units": RE + "L02.html:287,291,293,294 units and mix wording read; mix bullet consistent with Prop 5.1 and Remark 5.2.",
    "AC4-a-L02-misconceptions": RE + "L02.html:311 and the other three misconception items: each recomputed; 'a segment with no zero has operating income of one sign throughout' true for a strictly increasing segment.",
    "AC4-a-L02-problems": RE + "L02.html:326-420: M1 (1500 units, 120000 USD), M2 (1429; OI 3 and -4), M3 (200, 20%, 100 units, 10%), P1-P3, E1-E3 (runs of 89 and 88 volumes; 2411.11), R1-R3 (derivative -6.58 per USD; exact change -6.13; 6000 and 3000 break-evens) all recomputed.",
    "AC4-a-L02-remark-5-2-and-prop-5-1": RE + "Prop 5.1 proof (weighted margin) re-derived; Remark 5.2 read; cross-reference to R3 at L02.html:419 exists.",
    "AC4-a-L02-key-results-grades": RE + "L02.html:431-439 grades: T rows are propositions proved on the page; C rows name Lab 1 (SIMULATED).",
    "AC4-a-L02-quiz": RE + "all ten L02 quiz items recomputed: 3000; 150000; 89; 500; DOL 2; 740.7 (7.41 per 100 USD); step option; weighted margin 20; break-even definition.",
    "AC4-a-L02-hours": RE + "L02.html:2 data-hours=7 and eyebrow '7 study hours'; hub card L02 · 7 h.",
    "AC4-a-cards-L02-changed": RE + "cards AC4-c030, c118, c119, c125 re-read against L02 text (see AC4-a-cards-L01-L02).",
    "AC4-a-cards-r17-changed-subjects": RE + "cards AC4-c004, c008, c017, c132 re-read against L01 Def 3.1, Lab 1 residual, Def 3.1 margin of safety and Def 3.1 tie rule; all match.",
    "AC4-a-cards-L01-L02": RE + "all 39 L01/L02 cards (19 L01, 20 L02; ids AC4-c001-c014, c120, c127, c128, c130, c132; AC4-c015-c030, c118, c119, c125, c135) read against the current lesson text; each number traced to its lesson or lab output; duplicate scan (ids, fronts, backs with difflib ratio) found no duplicates. The round 25 defect (c026) is fixed: c026 now says 'single-segment model'. No card overstates a claim.",
    "AC4-a-banned-phrases": RE + "grep for roughly, about, historically, typically, usually, generally, '...', builder, verifier, round, REQUESTS in index, L01, L02: no banned hits; scope-word hits (only, always, all, same, raises) each read and supported by a computation or definition.",
    "AC4-a-hub-workspace-seed": RE + "index.html:161 and rung 3 text match project.html:299 ('with the seed shown in the autograder panel') and project.html:293 (budget_engine.py run on the plant the seed generates).",
    "AC4-a-hub-prereq-unlocks": RE + "curriculum/02-economics-finance-core.yaml AC4 prereqs: [AC1]; AC1 prereqs: [P0.1]; grep of all curriculum prereqs for AC4 finds none, so 'no module lists AC4 as a prerequisite' holds (checked by YAML walk).",
    "AC4-a-hub-objectives-placement": RE + "index.html:45-56 objectives and 68-137 placement read; objective 4 'two SIMULATED products' matches L04 'A SIMULATED plant with two products'.",
    "AC4-a-hub-skill-check-rung1": RE + "index.html:128-130 skill check 1 = 6800 (2000 + 4*1200), skill check 2 = 2000 ((22-20)*1000), recomputed.",
    "AC4-a-hub-data-status": RE + "index.html:169: labs using seeded generators are L01, L07, L08 (grep random|seed over tests/labs/AC4: only those three); L02 and other labs use typed inputs; every AC4 lab twin contains the word SIMULATED (counts 1 to 5). curriculum AC4 entry has no data key.",
    "AC4-a-footer-L01-L02": RE + "L01.html:500 and L02.html:535 footers and lesson navigation links read; next/previous targets exist.",
    "AC4-a-L02-loss-volumes-printed": RE + "L02.html:130 loss-volume sentence: 0 to 88 and 2001 to 2088 printed by the lab (loss run lines in output).",
    "AC4-a-L02-steps-bullet": RE + "L02.html:291 steps bullet: 'a single fixed cost, applied across a step, gives the upper zero and misses the first' matches Prop 4.1 and lab numbers.",
    "AC4-a-L02-key-results-profitable": RE + "L02.html:438 key-results row 'the first profitable whole volume is 89 units' (Remark 2.3 at L02.html:81 with 88.89) matches the output.",
    "AC4-a-L02-remark-2-3-whole-units": RE + "L02.html:81 Remark 2.3: ceil(Q*), 88 still loses, 89 profitable; recomputed (OI(88) = -12.00, OI(89) = 1.50).",
    "AC4-a-L01-misconception-and-keyresults-grades-r17": RE + "L01.html:269-284 misconception list and 399-404 key-results grades read; consistent with cards c005-c008 and the lab output.",
    "AC4-a-r18-hub-lede": RE + "index.html:30 lede: 'Its cases are SIMULATED, generated or typed in for the module' (read).",
    "AC4-a-r18-L01-why-it-matters": RE + "L01.html:51 annotations '(defined in Section 2)' and '(defined in Section 1)' read; both sections exist and define the terms.",
    "AC4-a-r18-L01-prop-3-2": RE + "L01.html:119 Prop 3.2 opening '(With Q_H != Q_L, as Definition 3.1 requires)' read; proof re-derived.",
    "AC4-a-r18-L02-why-it-matters-terms": RE + "L02.html:51 why-it-matters: 'operating income (revenue less total cost in this model)' defines the term in the same sentence; no term used before definition.",
    "AC4-a-r18-L02-key-results-source-c125": RE + "L02.html:438 source column for the first profitable whole volume and cards.json AC4-c125 agree on 88.89 and 89.",
    "AC4-a-r18-cards-c008-c018-c125": RE + "cards AC4-c008, c018, c125 re-read: c008 matches L01 misconception 4 (514.73 USD); c018 matches L02 misconception 1 (straight line, zero not maximum); c125 matches Prop 4.1 and Remark 2.3.",
    "AC4-a-r18-mutants-labs": RE + "ledgers/AC4/mutants/AC4-a-r18..r26 (39 lab-twin mutants) re-run under python -I -W error (" + OUT + "mutants_r27_committed.out): 34 killed, 5 survived with rc=0 and identical stdout; the survivors are recorded below as out of scope.",
    "AC4-a-L01-largest-residual-wording": RE + "L01.html:283 and :404 'largest absolute residual 514.73 USD' match Lab 1 output line 'largest absolute residual_cents 51473'.",
    "AC4-a-L01-section4-intro-definition-3-1": RE + "L01.html:247 'Lab 1 applies Definition 3.1 to twelve' months: the lab fits 12 months (rows of 12) with the Definition 3.1 rule.",
    "AC4-a-L01-E3-sentence": RE + "L01.html:362 E3 'passes exactly through two months and misses the other ten': 10 nonzero residuals in the output, two zero (months 6 and 11).",
    "AC4-a-L01-prop-2-2-changed": RE + "L01.html:93 Prop 2.2 'operating income (revenue less total cost)' matches Def 1.2 cost function and Proof line 99.",
    "AC4-a-hub-objective-4-simulated": RE + "index.html:52 objective 4 'on two SIMULATED products' matches L04.html:77 'A SIMULATED plant with two products'.",
    "AC4-a-r21-new-mutants": RE + "round 21 mutants (ledgers/AC4/mutants/AC4-a-r21/) re-run in r27 batch: 3 killed, 3 survived (equivalent on lab data, see below).",
    "AC4-a-r21-indep-recompute": RE + "independent recomputation of every L01/L02 number: " + OUT + "indep_recompute_r27.out, MISMATCHES 0 (39 checks).",
    "AC4-a-r23-delta-scan": RE + "delta f9f3fed..404db23 for AC4-a: only course/modules/AC/AC4/L01.html line 459 changed (quiz explanation, 'carry' -> 'may carry'). Every hunk read.",
    "AC4-a-r23-card-c020": RE + "card AC4-c020 read against L02 Lab 1 output (plan at 2,001 loses money) and the step applying above 2,000 units (lab docstring).",
    "AC4-a-r23-card-c135": RE + "card AC4-c135 (grade T) read against Prop 4.1 proof: zero on (T,inf) is (F+S)/m, non-negative exactly at or above it within that segment.",
    "AC4-a-r23-mutants-new": RE + "round 23 mutants re-run in r27 batch: all killed (rc=0 and stdout differs, or rc=1).",
    "AC4-a-r23-mutants-committed": RE + "all committed AC4-a lab-twin mutants (r18..r26) re-run this round; same result as round 26 (34 killed, 5 survived).",
    "AC4-a-r24-delta-scan": RE + "no change to index.html, L02.html or cards.json between 23cbd6a and 404db23 apart from the L01 quiz line; L02.html:311 and c135 were re-read.",
    "AC4-a-r24-line311-numbers": RE + "L02.html:311 misconception 3 numbers (2,001 units loses money; first break-even 88.89) and scope 'in a segment that has a zero' recomputed.",
    "AC4-a-r24-mutants-new": RE + "round 24 mutants re-run in r27 batch (killed).",
    "AC4-a-r24-mutants-committed": RE + "all committed mutants r18..r24 re-run in r27 batch; see AC4-a-r18-mutants-labs.",
    "AC4-a-r25-delta-scan": RE + "delta of this round for the AC4-a slice read hunk by hunk (only L01.html:459).",
    "AC4-a-r25-card-c135": RE + "card AC4-c135 re-checked against L02 Prop 4.1 and misconception 3 (L02.html:311): scope 'a segment that has a zero' matches.",
    "AC4-a-r25-card-c026": RE + "card AC4-c026 now reads 'It rises by exactly delta F/m units ... (Proposition 3.3, single-segment model)' and Prop 3.3 states 'In the single-segment model of Proposition 2.2'. The round 25 overstatement is fixed; PASS.",
    "AC4-a-r25-L01-E2-residual": RE + "L01.html:355 E2 solution: noise at most 400 USD cannot produce a 514.73 USD residual; the rest is the gap from the generator's line (read; the algebra is exact because residual = (G_F - F-hat) + (G_v - v-hat)h + noise).",
    "AC4-a-r25-mutants-new": RE + "round 25 mutants (u01-u03) re-run in r27 batch: killed (7.41 -> 0.74; 6.08 -> 1.04; 2222.22 -> 1022.22).",
    "AC4-a-r25-mutants-suite": RE + "all AC4-a lab-twin mutants re-run (" + OUT + "mutants_r27_committed.out): 34 killed, 5 survived.",
    "AC4-a-r25-cmd-twin-stdout-equals-embedded": RE + "embedded expected blocks equal twin stdout (L01 20 lines, L02 13 lines): " + OUT + "twin_equals_embedded.out.",
    "AC4-a-r25-cards-reread": RE + "all 39 L01 and L02 cards re-read this round (see AC4-a-cards-L01-L02).",
}

FAIL_NEW = {
    "AC4-a-notation-R-ast": dict(
        check="2.4-notation (notation/notation.json; BUILDER_RULES 3.2 'never give a registered symbol a different meaning')",
        location="course/modules/AC/AC4/L02.html:66, 71, 76, 86, 330, 466 (R^\\ast = break-even revenue)",
        evidence="notation/notation.json registers 'R^\\ast' with meaning 'the return on the SDF in the payoff space (defined in AP1 Lesson 4 ...)', module AP1. L02 uses the same symbol for break-even revenue R^* = pQ^* = F/(m/p) (Prop 2.2, Example 2.4, M1, quiz item 3). A registered symbol takes a different meaning, so the notation rule fails. Grep: grep -n 'R^\\\\ast' course/modules/AC/AC4/L02.html.",
        fix="Use an unregistered symbol for break-even revenue, for example R^{\\mathrm{BE}} or R_{\\mathrm{be}}, in L02.html at lines 66, 71, 76, 86, 330 and 466 (and in the matching Key-results row if any), or request the symbol under NOTATION_REQUESTS. Do not edit notation.json from the lesson.",
    ),
    "AC4-a-notation-T": dict(
        check="2.4-notation (notation/notation.json; BUILDER_RULES 3.2)",
        location="course/modules/AC/AC4/L02.html:122 (Prop 4.1 statement, 1{Q > T}, threshold T), 127 (proof, [0,T], (T,inf))",
        evidence="notation/notation.json registers 'T' with meaning 'number of return observations (periods) in a sample', module S1. L02 Prop 4.1 uses T as the step threshold volume (a volume, not a sample size). Registered symbol takes a different meaning. Read at L02.html:122 and 127.",
        fix="Rename the threshold in L02.html:122 and 127 (and in the proof sentence 'The zero on (T, inf)') to an unregistered symbol such as Q_s or \\bar{Q}, and keep the same name throughout Prop 4.1 and its proof.",
    ),
}

NOTE_SURVIVORS = (
    "Out of scope (architect ruling on lab twins; no lesson sentence claims the lab checks this): "
    "L01_p01 (tie on highest activity resolved by cost; no ties in the 12 seeded hours, rechecked), "
    "L02_p03 (round instead of ceiling; the printed values 88.89 and 89 cannot tell the two apart), "
    "L02_p04 (zero counted as a loss; no integer volume has zero operating income, rechecked over 0..5000), "
    "L01_q01 (residual of the lowest-hours month forced to 0; that residual is already 0 on this history), "
    "L01_v03 (high tie resolved to latest; no ties in the data)."
)

rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in FAIL_NEW:
        continue
    status = "PASS"
    evidence = ev.get(rid, RE + r["check"] + " at " + r["location"] + "; re-read this round.")
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": evidence})

for rid, spec in FAIL_NEW.items():
    rows.append({"id": rid, "check": spec["check"], "location": spec["location"], "status": "FAIL",
                 "evidence": spec["evidence"], "fix": spec["fix"]})

rows.append({"id": "AC4-a-r27-delta", "check": "1.delta", "location": "git diff f9f3fed 404db23 -- course/modules/AC/AC4",
             "status": "PASS",
             "evidence": "one hunk: course/modules/AC/AC4/L01.html @@ -456,7 +456,7 @@ (line 459): 'Other months carry residuals' -> 'Other months may carry residuals (Remark 3.3)'. Read in full; the L01 q7 explanation is now consistent with Remark 3.3 and with Lab 1 (10 of 12 nonzero, so the word may is the correct scope). index.html, L02.html, cards.json, twins: no change in the delta."})
rows.append({"id": "AC4-a-r27-L01-q7-explanation", "check": "2.2-numbers and 2.9-prose", "location": "course/modules/AC/AC4/L01.html:459",
             "status": "PASS",
             "evidence": "The sentence now says other months may carry residuals and cites Remark 3.3 (which says residuals are free to be positive or negative). The twin shows 10 of 12 nonzero, so the sentence is not overstated."})
rows.append({"id": "AC4-a-r27-indep-recompute", "check": "2.2/2.4 numbers and formulas recomputed from the page text", "location": "ledgers/AC4/scripts/AC4-a-r27/indep_recompute_r27.py",
             "status": "PASS", "evidence": "39 independent checks (Example 4.1, M2, R3 step cost over 1,201 hours, Lab 1 regenerated from seed 20261027, Lab 2 break-even family, R2 derivative, quiz values); MISMATCHES 0 (" + OUT + "indep_recompute_r27.out)."})
rows.append({"id": "AC4-a-r27-hours-arithmetic", "check": "hours (declared vs hub split)", "location": "index.html:29,40,42; L01.html:2,34; L02.html:2,34; eyebrows L03-L08",
             "status": "PASS", "evidence": "lesson hours 6+7+6+6+7+6+6+6 = 50 = data-hours-lessons; project 20; total 70; split 71.4% / 28.6%. Not failed on pace."})
rows.append({"id": "AC4-a-r27-registry-flags-check", "check": "2.1 citations (reading list keys)", "location": "references/references.json entries datar2020horngrens, kaplan1998cost",
             "status": "PASS", "evidence": "Both keys resolve (status verified, openlibrary). Registry observations (not page failures): datar2020horngrens record year 2020 while curriculum source string says 17th ed. (2021) (notes.year); kaplan1998cost authors list only Kaplan, Robert S. while the curriculum source string says 'Kaplan & Cooper'. The reading list renders registry data (course/assets/js/refs.js:128), so the displayed citations show these registry values; flagged in registry_flags."})
rows.append({"id": "AC4-a-r27-mutants-survivors", "check": "2.5 labs / mutation (lab twins, architect ruling)", "location": "ledgers/AC4/mutants/AC4-a-r18..r26",
             "status": "PASS", "evidence": NOTE_SURVIVORS + " (" + OUT + "mutants_r27_committed.out)"})
rows.append({"id": "AC4-a-r27-cards-dup-scan", "check": "2.7 cards: full duplicate scan", "location": "course/modules/AC/AC4/cards.json (39 L01/L02 cards)",
             "status": "PASS", "evidence": "no duplicate ids, no duplicate fronts; difflib similarity pairs (c003/c009, c009/c130, c012/c127, c030/c119) read: different questions, not duplicates."})

fragment = {
    "unit": "AC4",
    "slice": "AC4-a",
    "round": 27,
    "verifier": "independent verifier (Haiku), round 27",
    "pin": "404db23",
    "previous_pin": "f9f3fed",
    "base": "f9f3fed",
    "checkout": "/tmp/verify27-AC4-a",
    "scratch": "/tmp/AC4-v/AC4-a-r27",
    "verified_at": "2026-10-28T00:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [
        {"id": "AC4-a-r18..r26/committed", "description": "39 committed lab-twin mutants of L01 and L02 (ledgers/AC4/mutants/AC4-a-r18 .. AC4-a-r26), re-run this round under python -I -W error",
         "killed_by": "34 KILLED (rc != 0 or stdout differs); 5 SURVIVED with rc=0 and identical stdout, recorded as out of scope with reasons in row AC4-a-r27-mutants-survivors"},
        {"id": "AC4-a-r25/L02_u01_sensitivity_in_dollars_not_cents", "description": "student error: sensitivity computed with 10,000 cents read as 1,000 cents", "killed_by": "KILLED (7.41 becomes 0.74)"},
        {"id": "AC4-a-r25/L02_u02_leverage_planned_income_without_step", "description": "student error: operating leverage uses planned income with the step omitted", "killed_by": "KILLED (6.08 becomes 1.04)"},
        {"id": "AC4-a-r25/L02_u03_break_even_revenue_at_variable_cost", "description": "student error: break-even revenue priced at the variable cost per unit", "killed_by": "KILLED (2222.22 becomes 1022.22)"},
    ],
    "registry_flags": [
        "datar2020horngrens: registry year 2020 (notes.year: curriculum 2021, record 2020; curriculum source string says 17th ed. (2021)). The reading list renders the registry value, so the hub shows 2020.",
        "kaplan1998cost: registry authors list only Kaplan, Robert S.; curriculum source string says 'Kaplan & Cooper, Cost & Effect (1998)'. Not checked against the book itself (the registry record is the only source read; openlibrary is the verifier named in the record).",
    ],
    "freshness_flags": [],
    "notes": [
        "Previous pin for the delta: f9f3fed. The delta for this slice is one hunk, L01.html:459 (quiz explanation 'may carry residuals'). The round 26 observation (other months carry residuals) is now resolved and PASS.",
        "Round 26 FAIL rows AC4-a-cards-L01-L02 and AC4-a-r25-card-c026 are re-verified from scratch this round: all 39 L01/L02 cards read against the current lesson text; c026 now carries the single-segment scope. Both PASS.",
        "New FAIL rows are notation collisions (BUILDER_RULES 3.2): R^\\ast (registered by AP1 for the SDF return) used for break-even revenue in L02, and T (registered by S1 for the number of return observations) used as a step threshold in L02 Prop 4.1.",
        "Not a row: the hub reading list statement 'No locator has been read in either' is the author's own statement and cannot be checked from the repository; the page-level non-attribution is checked by grep.",
        "Not a row: the lab twin mutants that survive are equivalent on the lab's data or print nothing a lesson claims; the architect ruling excludes lab twins from mutation scoring. No new mutants were written: this slice is not a project slice, so the three-new-mutant minimum does not apply.",
        "Not checked: L03 to L08 and their cards and labs (other slices); project.html and the grader (other slice); Pyodide wall-clock beyond page_smoke's own pass (page_smoke printed PASS only); web access to the two reading-list books (not attempted; no external source is cited by these pages).",
    ],
    "summary": "Slice AC4-a round 27 (pin 404db23, previous f9f3fed): all command rows re-run and pass (check_pages, check_dag, check_projects, run_labs, twins isolated, twin output equals embedded, page_smoke, pytest -k AC4, ruff, mypy on twins, verify_refs offline and live, build_site --check). The one delta hunk (L01.html:459) is PASS. All 39 L01/L02 cards and the independent recomputation (39 checks) PASS. FAIL: two notation collisions in L02 (R^\\ast and T) against notation/notation.json. Committed lab mutants: 34 killed, 5 survived and out of scope.",
}

Path(ROOT / "ledgers/AC4/AC4-a.json").write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", len(rows), "fails", sum(1 for r in rows if r["status"] != "PASS"))
