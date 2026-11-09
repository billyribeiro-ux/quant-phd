"""Round-18 LX1-c: writes the fragment ledgers/LX1/LX1-c.json (verifier-written; every row cites an output or a file read this round)."""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
S = "ledgers/LX1/scripts/LX1-c-r18"
OUT = S + "/out/"
PREV = json.load(open("/Users/billyribeiro/.fanout/frags/E-LX1-c.round17.json"))
prev_ids = [r["id"] for r in PREV["rows"]]
C = "course/modules/LX/LX1/project.html"
CARRY = "Carried from round 17 (course/assets/data/market/fx_monthly.csv and MANIFEST.json byte-identical since the previous pin): "

R = {}
def row(rid, check, loc, status, ev, fix=None):
    R[rid] = dict(id=rid, check=check, location=loc, status=status, evidence=ev)
    if status != "PASS":
        R[rid]["fix"] = fix

row("proj-rung1-step3-rounding-claim", "2.5-labs", C + ":177, :179", "PASS",
    f"Fresh. {C}:177 states 11764705.882 cents (10000000/0.85) and :179 states 3069053.708 cents. {OUT}rederive_labs12_r18.out: 11764705.88235294 cents, 117647.06 dollars; difference 3069053.7084 cents -> 30690.54. {OUT}twins_r18.out: page code equals twin (0 differing lines); twin stdout equals expected block.")
row("proj-real-value-vs-lesson2", "2.9-prose", C + ":55-59; course/modules/LX/LX1/L02.html:84-90, :123, :127-131", "PASS",
    f"Fresh read. {C}:55-59: V_t = D/P_t stated as Lesson 2's V_t = D P_0/P_t with P_0 = 1; burden change 100(P_0/P_t - 1). L02.html:84-90 (A2), (A3) and Proposition 2.1; :123 Proposition 2.1(a) step; :127-131 Remark 3.3 text (no cause, no size) read.")
row("proj-manifest-note-misattributed", "2.2-numbers", C + ":271, :279, :294; course/assets/data/market/MANIFEST.json (fx_monthly)", "PASS",
    "Fresh. MANIFEST fx_monthly: title 'Month-end foreign exchange rates, ten currencies, USD per unit of foreign currency'; first 1971-01, last 2026-09; retrieved 2026-10-19; transform inverts CAD, CHF, DKK, JPY, NOK, SEK (GBP not inverted). Page :271, :279, :294 match. Command: python -I rederive_r18.py (out/rederive_r18.out: 669 rows, GBP 0 blanks).")
row("proj-lab3-citation-string", "2.1-citation", C + ":279, :287; MANIFEST.json fx_monthly citation", "PASS",
    "Fresh. Page :279 and :287 citation 'Board of Governors of the Federal Reserve System, G.5/H.10 Foreign Exchange Rates (noon buying rates in New York)' equals MANIFEST citation field; retrieved 2026-10-19 equal.")
row("proj-reading-reinhart-registry", "2.1-citation", C + ":626-640; references/references.json", "PASS",
    "Fresh. Reading list at :630-632 cites friedman1963monetary, eichengreen1992golden, garber2000famous; each is a registry record (status verified, used_by LX1). reinhart2009this is a verified registry record (Reinhart & Rogoff, Princeton UP, 2009) that the spec lists as optional (page :269/spec reading list in plans/LX1-build-plan.md §5.2); its omission is permitted.")
row("proj-spec-current-undefined", "2.6-spec", C + ":439, :301-302, :444", "PASS",
    "Fresh. Brief item 1 (:439) defines a current condition as dated within the twelve months ending at the last month of the data used, and gives the snapshot window 2025-10 to 2026-09. See notes for the one clarifying question a student could ask (a non-snapshot source).")
row("proj-exemplar-A-condition", "2.6-exemplars", C + ":490", "PASS",
    "Fresh read of :490: names the episode (Eichengreen 1992 title period 1919-1939, registry title field matches references.json eichengreen1992golden) and the condition (GBP window three 2025-10 to 2026-09; MANIFEST last 2026-09). Descriptive check only; not scored (ruling 23).")
row("proj-gate-commands", "gate", "ledgers/LX1/scripts/LX1-c-r18/run_gates_r18.sh; out/*.out", "PASS",
    "Re-run this round: check_pages --unit LX1 PASS (rc 0); check_dag LX1 PASS; check_projects LX1 PASS; run_labs LX1 PASS (3/3 project labs); verify_refs --offline 560 entries 0 problems; verify_refs --unit LX1 4 entries 0 problems; fetch_data --check 3 datasets 0 problems; build_site --check current; mutate_graders --unit LX1 rc 0 (rubric unit); ruff check and format clean; mypy --no-incremental no issues in 385 files; pytest labs/refs passed. Note: check_pages --unit LX1 --page project exits 1 with 11 lesson-template problems (out/check_pages_project.out); the tool's docstring (tools/check_pages.py:25) says project pages are checked by check_projects.py, so that invocation is not a gate; the applicable gates pass.")
row("proj-lab1-twin-run", "2.5-labs", C + ":78-149; tests/labs/LX1/lab-LX1-project-1.py", "PASS",
    f"{OUT}twins_r18.out (ledgers/LX1/scripts/LX1-c-r18/harness_r18.py twins): lab-LX1-project-1 page-vs-twin diffs=0; twin rc=0 under python -I -W error, stderr 0 bytes; stdout equals expected block (20 lines). page_smoke project PASS (out/page_smoke_project_r18.out).")
row("proj-lab1-numbers", "2.2-numbers", C + ":77, :150-169", "PASS",
    f"{OUT}rederive_labs12_r18.out (Fraction, exact): real debt falling 100000.00 103092.78 106382.98 109890.11 113636.36 117647.06; rising 100000.00 97087.38 94339.62 91743.12 89285.71 86956.52; burden 17.65 and -13.04; difference 30690.54. All equal the hypothesis (:77) and the expected block (:150-169).")
row("proj-lab2-twin-run", "2.5-labs", C + ":182-256; tests/labs/LX1/lab-LX1-project-2.py", "PASS",
    f"{OUT}twins_r18.out: lab-LX1-project-2 page-vs-twin diffs=0 (the only differing lines are the two ___ blanks); twin rc=0 under python -I -W error; stdout equals expected block (10 lines).")
row("proj-lab2-numbers", "2.2-numbers", C + ":184, :247-256", "PASS",
    f"{OUT}rederive_labs12_r18.out: real debt 40000.00 40404.04 40816.33 41666.67 42105.26 43010.75; burden 7.53. Hypothesis :184 states 43010.75 and 7.53 and equals the block.")
row("proj-lab2-check-claims", "2.2-numbers", C + ":257", "PASS",
    f"Line :257 claims: leaving out the division prints 40000.00 in every period (existing mutant lx1c_m01 KILLED, out/kill_all_r18.out); inverting the ratio prints -7.00 in place of 7.53 (rederive: inverted burden -7.00; mutant lx1c_m02 KILLED). The instant check compares output with the expected block (course/assets/js/labs.js:133-137, compareOutput), which is the 'compares the whole block' statement.")
row("proj-lab3-twin-run", "2.5-labs", C + ":285-432; tests/labs/LX1/lab-LX1-project-3.py", "PASS",
    f"{OUT}twins_r18.out: lab-LX1-project-3 page-vs-twin diffs=0; twin rc=0 under python -I -W error in a scratch dir holding data/fx_monthly.csv; stdout equals expected block (19 lines). page_smoke project PASS.")
row("proj-lab3-numbers", "2.2-numbers", C + ":287, :412-430", "PASS",
    f"{OUT}rederive_r18.out (exact recomputation, statistics.stdev cross-check in the same file): window one n=668, exact zeros 3, sd 2.7935277918 %/mo -> 2.79, largest 13.58 (1985-03); window two n=321, zeros 2 (2012-07, 2019-11), sd 2.4699501387 -> 2.47, largest -9.66 (2008-10); window three n=12, zeros 0, sd 1.9020185800 -> 1.90, largest 2.96 (2026-04); ratio 0.8841688 -> 0.88; difference 0.3235777 -> 0.32. All equal the expected block.")
row("proj-lab3-L04-cross-check", "2.1-citation", "course/modules/LX/LX1/L04.html:314, :317; " + C + ":284, :298", "PASS",
    "L04.html:314 prints 0.027935 (window one) and :317 prints 0.024700 (window two) as decimals; rederive gives 0.027935277918 and 0.024699501387, which round to these six places. L04 windows 1971-02 and 2000-01 with counts 668 and 321 are in the same lesson (grep). L04 lab not re-run here (it is another slice); its printed values were recomputed.")
row("proj-lab3-docstring-claims", "2.5-labs", C + ":288-315 (twin docstring mirrored); tests/labs/LX1/lab-LX1-project-3.py:1-40", "PASS",
    "Docstring claims read against code: reads GBP column (code COLUMN); blank or non-decimal cell raises ValueError (load_column DECIMAL_PATTERN; input test out/blank_cell_r18.out and gap_and_text_cell_r18.out: twin rc=1 with the cell named); a month that does not follow raises (gap test: 'month 1985-04 does not follow 1985-02'); no row skipped or filled; show() prints the exact binary value half up (Decimal(value)); ratio and difference from unrounded sds (synthetic input out/lab3_synth_r18.out rounding_seed11: printed-value difference -0.07, twin -0.08 = unrounded -0.08).")
row("proj-lab3-interpretation-claims", "2.2-numbers", C + ":431; course/modules/LX/LX1/L04.html:84-94 (Definition 2.1, (A2), Proposition 2.2)", "PASS",
    "Each :431 claim re-derived: 13.58 percent in 1985-03 is outside window two (window two starts 2000-01); difference 0.32; window three has 12 changes with 11 degrees of freedom; the two window-two zero changes are 2012-07 and 2019-11 (rederive_r18.out); Proposition 2.2 (L04.html:90-94) gives zero change under (A2) (L04.html:92); 321 against 2. The 'fixed rate held over window two' sentence is a conditional on the model under (A2), stated as such.")
row("proj-lab3-difference-line-r5", "2.5-labs", C + ":287, :412-431; tests/labs/LX1/lab-LX1-project-3.py (difference line)", "PASS",
    "The difference line is show(100*(sd_one - sd_two)) from unrounded sds. Real data cannot tell this from a printed-value difference (0.32 both ways), so the claim was tested on synthetic inputs: out/lab3_synth_r18.out rounding_seed11 shows the twin prints -0.08 (unrounded) where a printed-value difference gives -0.07; mutant lx1c_r18n02 is KILLED there.")
row("proj-lab-simulated-labels", "2.8-data", C + ":42, :77, :80, :184, :187, :283-287", "PASS",
    "Labs 1 and 2 carry SIMULATED in hypothesis and docstring (:77, :80, :184, :187) and in the page text (:42). Lab 3 (real data) has zero occurrences of SIMULATED in :282-432 (grep count 0) and names its dataset, licence and retrieval date at :287.")
row("proj-data-licence-quote", "2.8-data", C + ":279; https://www.federalreserve.gov/disclaimer.htm", "PASS",
    "Plain curl this round: HTTP 200, 85306 bytes (out/licence_page_r18.html). The page contains 'Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission. Please cite to the Board as the source of the information.' This equals page :279 and the MANIFEST licence field, and grants redistribution.")
row("proj-data-snapshot-rebuild", "2.8-data", "course/assets/data/market/fx_monthly.csv; course/assets/data/market/MANIFEST.json (fx_monthly)", "PASS",
    CARRY + "this round, command 'shasum -a 256 course/assets/data/market/fx_monthly.csv' (this round) = 60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e, equal to MANIFEST sha256 for fx_monthly; bytes 67392 equal. fetch_data --check: 3 datasets, 0 problems. The live-feed rebuild was not repeated this round (no network rebuild needed for a byte-identical snapshot).")
row("proj-data-fields", "2.8-data", C + ":271, :279-280, :292-294; course/assets/data/market/fx_monthly.csv", "PASS",
    f"{OUT}rederive_r18.out: header month,AUD,CAD,CHF,DKK,EUR,GBP,JPY,NOK,NZD,SEK (equal to page :271 list); 669 rows 1971-01 to 2026-09; EUR blank cells 336 before 1999-01; GBP blank cells 0.")
row("proj-data-no-other-series", "2.8-data", C + ":280; course/assets/data/market/MANIFEST.json", "PASS",
    "MANIFEST columns: fx_daily AUD, CAD, CHF, EUR, GBP, JPY; fx_monthly ten currencies; ust_daily tbill_3m, cmt_10y. No gold, price-level, output, unemployment or bank-failure column or title, so the page's 'None of the three is ...' (:280) holds.")
row("proj-spec-ladder", "2.6-spec", C + ":40-48, :73-258, :261-275, :618-624", "PASS",
    "Rung 1 fully solved with a why line per step (:173-180) and annotated lab (:75-171); rung 2 completion lab with class 'lab completion' (:182) and two blanks; rung 3 spec and brief (:261-275, :436-446); rung 4 stretch (:618-624). Tier U: full rung 1 required and given.")
row("proj-spec-curriculum-scope", "2.6-spec", "curriculum/06-profession-capstone.yaml:42-49; " + C + ":263-273, :436-446", "PASS",
    "Curriculum: title 'Then vs. now', brief 'Pick one historical episode and one current market condition ... where the analogy holds and where it breaks', deliverable 'Two-page essay, every claim cited.', grading rubric. The page's context, required outputs, brief items 1-6 and grading mode match this scope; no extra deliverable.")
row("proj-hours", "2.6-hours", C + ":33, :35, :448-461; course/modules/LX/LX1/index.html:29", "PASS",
    "Table sums: 1 + 1 + 2 + 1.5 + 2.5 + 2 = 10 = data-hours-project (:33) and eyebrow '10 hours' (:35); hub data-hours-lessons 40 + data-hours-project 10 = 50. Verifier's own estimate: rung 1 1; rung 2 0.5-1; selection and sourcing 2.5-3.5; mechanism 1.5-2; drafting 3-4; self-assessment 1.5-2; range 10-13.5, midpoint 11.75 h, 17.5% from 10 h, inside the 30% band.")
row("proj-rubric-observable", "2.6-rubric", C + ":466, :472-476", "PASS",
    "Each level cell names an element a rater can check (counts of dates, locators, chain steps, rule and formula cells, named limits, sources, similarities). Vague-word scan: no 'appropriate', 'good', 'sufficient', 'adequate'; 'Picks two events' (C1 L1) and 'Mentions a caveat' (C5 L1) name checkable acts. Rule at :466 makes a wrong shown element not count, so correctness is part of each presence check.")
row("proj-calibration-exemplars", "2.6-rubric-calibration", C + ":484-606 (exemplar annotations); :466 scoring rule; ledgers/LX1/scripts/LX1-c-r18/out/blind_prose_r18.txt", "UNVERIFIABLE",
    "Pending blind (ruling 23): not scored by this verifier. The descriptors are not mutually exclusive as text, so the calibration row is pending-blind by the stated rule: C1 L3 and L2 both hold for dates given for both and one locator missing (:473/:472); C2 L2 first clause (similarity and difference, no chain) and L1 (similarity, no chain) both hold (:473); C3 L3 and L2 both hold when at most two claims lack a locator (:474); C4 L3 exception and L2 clause 2 overlap for one missing rule (:475); C5 L3 and L2 both hold for two limits with no test (:476). The highest-level rule at :466 resolves each overlap, but the text is not exclusive.",
    "Architect: run the blind scorer on exemplar-a and exemplar-b (ruling 23) and compare with the official scores in the page (:486, :548) within one level per criterion. Optional: write each descriptor so that the levels do not overlap, or keep the cumulative rule and say so in the caption.")
row("proj-exemplar-numbers", "2.2-numbers", C + ":501-534 (exemplar A), :523, :534; :552-605 (exemplar B), :577, :581", "PASS",
    "Exemplar A: 17.65 (Lab 1 Part B), 2.47, 2.79, 1.90, ratio 0.88 (unrounded 0.8841688), 13.58 in 1985-03 (positive), 0 zero changes in window three: all equal rederive_r18.out. Exemplar B: 2.47/2.79 = 0.885 -> 0.89 (arithmetic correct); unrounded 0.88 gives a 11.58 percent fall, 'about 12 percent' at :581 is correct. 'per year' at :577 is the wrong-unit error the official verdict names (:548), not a number error.")
row("proj-reading-keys", "2.1-citation", C + ":630-632; references/references.json", "PASS",
    "Each key on the reading list resolves to a verified registry record: friedman1963monetary (Milton Friedman, 1963), eichengreen1992golden (Barry Eichengreen, 1992, title 'Golden fetters: the gold standard and the Great Depression, 1919-1939'), garber2000famous (Peter M. Garber, 2000). Page names no second author (correct for friedman per the registry).")
row("proj-notation", "2.4-notation", C + " TeX spans; notation/notation.json", "PASS",
    f"{OUT}notation_scan_r18.out: symbols used D, P_t, P_0, P_5, S_m, V_t, V_0, n, m, t, \\ln; registered symbols T, R_f, \\Phi, \\gamma_3, \\gamma_4, \\mathbb{{Q}} and others; collisions []. No registered symbol is reused.")
row("proj-scope-words", "2.9-prose", C + ":62, :170, :176, :179, :257, :280, :431, :473, :475, :476 (changed lines)", "PASS",
    "Scope words on changed lines: 'every' at :280 (MANIFEST columns, checked), :431 (each window's changes, checked from rederive), :473/:475 (rubric cells, text read); 'the whole block' at :257 (labs.js compareOutput, read); 'none' at :280 (MANIFEST titles/columns). Each has a computation, a MANIFEST field or a code line.")
row("proj-process-words", "2.9-prose", C + " (rendered prose); out/scan_r18.out", "PASS",
    f"{OUT}scan_r18.out: TODO, TBD, lorem, 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'experts agree', 'it is well known', obviously, clearly, 'historically', 'It can be shown', Pseudocode, 'round [0-9]', verifier, builder, ruling, 'this round', LX1-c: all 0. 'checks that' 1 hit (:466, rater instruction, not a process word).")
row("proj-links-anchors", "2.9-structure", C + " (href and id); course/modules/LX/LX1/index.html; L02.html", "PASS",
    "Script ledgers/LX1/scripts/LX1-c-r18/anchors_manifest_r18.py (out/anchors_manifest_r18.out): 22 internal href values checked against the file's ids and the target files' ids; 0 broken (the one external licence link was fetched by curl, see proj-data-licence-quote). Includes index.html#placement (exists, data-mastery 0.8), #spec, #data, #brief, #rubric-section, #self-assessment, #stretch, and L02.html#def-debt-deflation.")
row("proj-page-smoke", "2.9-structure", C + "; out/page_smoke_project_r18.out", "PASS",
    "page_smoke --unit LX1 --pages project (this round): 'page_smoke modules/LX/LX1/project.html: PASS', 'page_smoke LX1: PASS', rc 0; labs lab-LX1-project-1..3 each 0.0 s after a 1.1 s runtime boot.")
row("proj-atlas-autograder-na", "2.6-grading", "curriculum/06-profession-capstone.yaml:49; out/run_graders_LX1_r18.out; course/modules/LX/LX1/ (no grader/)", "PASS",
    "Grading is rubric (curriculum yaml:49). run_graders --unit LX1 this round: 'run_graders LX1: no autograder (grading: rubric)', rc 0; no grader directory in course/modules/LX/LX1; grep of atlas/ for 'LX1' returns 0 files, so no Atlas milestone.")
row("proj-mutants-student-errors", "2.6-mutation (rubric-unit analogue)", "ledgers/LX1/mutants/ (79 files); " + S + "/out/kill_all_r18.out; blank_cell_r18.out; blank_first_row_r17n01.out; lab3_synth_r18.out", "PASS",
    "Five new student-error mutants of Lab 3 written this round (lx1c_r18n01 to n05: lookahead change, difference from printed sds, zero test after rounding to four places, window two centred on the window-one mean, blank carried forward). All 79 lab mutants run: 74 KILLED on the shipped run. Five survive the shipped run because the shipped snapshot has no blank cell, no tiny move, and no rounding tie; each is killed by a distinguishing input: r18n02 by rounding_seed11 (synthetic), r18n03 by tiny_moves, r18n04 by rounding_seed8, r18n05 and r17n01 by the blank-cell input (rc 0 and rc 1 vs twin rc 1), r17n01 also by a blank first-row input (ZeroDivisionError vs twin ValueError). Note: the shipped run does not exercise the blank-cell check; the page's sentence about it is true of the twin (see proj-lab3-raise-claims-untested).")
row("proj-alternatives", "2.6-mutation (over-constraint)", S + "/alts/alt_r18_A_lab1_decimal.py; alt_r18_B_lab3_statistics.py", "PASS",
    f"Two alternative correct implementations pass the shipped run under -I -W error: alt A (Decimal at 40 digits, quantize half up, lab 1) and alt B (statistics.stdev, math.log1p on the exact ratio minus one, index windows, lab 3). Both print the expected block (harness cands: SURVIVED). Round-17 alt_r17_C is stale (prints a removed line) and is not reused.")
row("proj-exemplar-b-annotations-vs-descriptors", "2.6-rubric", C + ":548-606 (exemplar B annotations)", "PASS",
    "Annotations paraphrase level cells; read against :472-476. One paraphrase is looser than the cell: :593 'lists similarities and one difference' for the C2 L2 cell which reads 'at least one difference'. Not a scoring act; the blind scorer decides scores.")
row("proj-brief-rubric-escape-clauses", "2.6-rubric", C + ":442, :474, :475", "PASS",
    "'or the essay states that it makes no such claim' applies only to claims not graded B or C (grade scale :66, which matches BLUEPRINT §3 table). Observable by the rater; no level is reachable without an element the rater can see.")
row("proj-exemplar-locators", "2.1-citation", C + ":490, :500, :511, :522, :534; course/modules/LX/LX1/L02.html; L04.html:333", "PASS",
    "Every locator in both exemplars resolves: title field and MANIFEST last field (:490); L02 Proposition 2.1(a) and Remark 3.3 (:500, L02.html:123, :127); MANIFEST transform field (:511); Lab 1 Part B and Lab 3 printed rows (:522); Lesson 4 Section 4 item 'Exchange rates only.' (L04.html:333) (:534).")
row("proj-exemplar-a-c5-limit-count", "2.6-rubric", C + ":476, :534, :539-540", "PASS",
    "The C5 cells (:476) say L4 two limits each with a test, L3 two limits one with a test, L2 at least one limit. Exemplar A's limits text (:534) names three limits; its annotation (:539-540) reads against those cells. Counts are consistent with the cells as written.")
row("proj-rubric-c3-inference-gap", "2.6-rubric", C + ":474-475, :440", "PASS",
    "C3 L4 and L3 cells (:474) accept 'marked as the writer's own inference' with no locator; brief item 2 (:440) asks for the failure evidence. No inference-marked claim can reach a level only by its absence of a locator unless the cell says so.")
row("proj-exemplar-A-limit1-cip-locator", "2.1-citation", C + ":534; course/modules/LX/LX1/L04.html:333", "PASS",
    "Exemplar A limit one cites 'Lesson 4, Section 4, item Exchange rates only' and says the file has no interest-rate column; L04.html:333 has that item (Section 4 at :329) and says the snapshot holds exchange rates and no interest-rate column. Locator resolves.")
row("proj-l04-model-name-stale", "2.9-prose", C + ":431; course/modules/LX/LX1/L04.html:84-85", "PASS",
    "Page's 'Definition 2.1' and 'Proposition 2.2' names resolve to L04.html:84 (Definition 2.1, fixed-exchange-rate model) and :90 (Proposition 2.2, zero dispersion in the model); (A2) at :92.")
row("proj-exemplar-a-c2-annotation", "2.6-rubric", C + ":500-520; course/modules/LX/LX1/L02.html (Definition, Proposition 2.1(a), Remark 3.3)", "PASS",
    "Exemplar A mechanism passages cite Proposition 2.1(a) (L02.html:123), assumptions (A2) and (A3) (L02.html:84-90) and Remark 3.3 (L02.html:127-131); each cited statement matches its text.")
row("proj-r18-delta-hunks", "2.9-prose / delta", "git diff 700bf33f 50559266 -- course/modules/LX/LX1/project.html tests/labs/LX1 ledgers/LX1 course/assets/data/market", "PASS",
    "Delta read hunk by hunk (14 changed lines in project.html): :167-170 Lab 1 interpretation (SIMULATED wording), :176 worked step 2, :254-257 Lab 2 interpretation, :279-280 data paragraph, :431 Lab 3 interpretation, :470-476 rubric C2 (L2 and L4/L3 cells), C4 (L2 cell). tests/labs/LX1 is unchanged in the delta (git diff stat), so all three project twins are the same bytes as at 700bf33f. Lesson L01 and cards changed in the delta but are other slices. L02, L04, index.html, MANIFEST, fx_monthly.csv, references.json, notation.json are byte-identical to 700bf33f.")
row("proj-r14-delta-hunks", "2.9-prose / history", "git merge-base --is-ancestor 8e5751c9 50559266 and d1e65a0 50559266", "PASS",
    CARRY.replace("(course/assets/data/market/fx_monthly.csv and MANIFEST.json byte-identical since the previous pin)", "(historical audit of commits 8e5751c9..d1e65a0; both are ancestors of the pin, verified by git merge-base --is-ancestor this round)") + "historical; the current delta is proj-r18-delta-hunks.")
row("proj-r15-delta-hunks", "2.9-prose / history", "git merge-base --is-ancestor d1e65a0 50559266 and 56cc575a 50559266", "PASS",
    CARRY.replace("(course/assets/data/market/fx_monthly.csv and MANIFEST.json byte-identical since the previous pin)", "(historical audit of commits d1e65a0..56cc575a; both are ancestors of the pin, verified this round)") + "historical; the current delta is proj-r18-delta-hunks.")
row("proj-data-embedded-claim", "2.8-data", C + ":280; course/assets/data/market/MANIFEST.json (fx_daily, fx_monthly, ust_daily)", "PASS",
    "Page says the site embeds three series (fx_daily, fx_monthly, ust_daily); MANIFEST holds exactly those three ids (ledgers/LX1/scripts/LX1-c-r18/anchors_manifest_r18.py, out/anchors_manifest_r18.out).")
row("proj-lab3-raise-claims-untested", "2.5-labs", C + ":308-309 (Check paragraph), :431 (no agreement line); tests/labs/LX1/lab-LX1-project-3.py", "PASS",
    "The page's Check sentence (:308-309) is true of the twin: blank GBP cell raises ValueError naming the cell (out/blank_cell_r18.out, rc 1); non-decimal cell 'abc' raises (out/gap_and_text_cell_r18.out, rc 1); a month gap raises (same file, rc 1); the unchanged snapshot runs (rc 0). The shipped snapshot has no blank, so the shipped run does not exercise the check. The agreement check is gone from the page and the twin (no 'agree' hit in the scan). Coverage gap for the repo, not a page claim: the architect may add a test under tests/ for the blank and gap cases.")
row("proj-rubric-c5-count-wording", "2.6-rubric", C + ":476", "PASS",
    "C5 cells read: L4 'Names at least two limits ... for each, the evidence that would test it'; L3 'at least two limits, one with the test'; L2 'at least one limit'; L1 'Mentions a caveat without naming what it limits.' Counts match each other and the brief (two limits, one with a test, :269, :443).")
row("proj-rubric-c4-formula-gap", "2.6-rubric", C + ":475 (L2 and L1 cells; L3 cell requires formula, base and sign)", "PASS",
    "Fixed in this delta. The L2 cell now reads 'or gives every computed number unrounded values and a stated rule, but omits, or gives wrong, the formula or the base and sign of some number or percent change'. Every case is now described: wrong formula or base (L2), missing rule for some numbers (L2), rounded input (L2), no rule or no number (L1). A wrong computed number is caught by the 'cited lab line prints' requirement in L4/L3 (the printed line disagrees), so it falls to L2.")
row("proj-rubric-c2-count-wording", "2.6-rubric", C + ":473 (L2 cell)", "PASS",
    "Fixed in this delta. The C2 L2 cell reads 'Lists similarities and at least one difference', matching L1's 'Names at least one similarity' and the other disjuncts.")
row("proj-rubric-c2-gap", "2.6-rubric", C + ":473 (L2 cell, clause 'does not name what some step rests on')", "PASS",
    "Fixed in this delta. The basis-missing essay (chains of at least three steps, analogy-holds steps and failure step named, basis missing for some step) is described by the L2 clause, so it scores 2, not 0. The bubble case is a separate, open gap (proj-rubric-exhaustive-r14).")
row("proj-rubric-c3-level3-gap", "2.6-rubric", C + ":474 (L3 cell)", "PASS",
    "The C3 L3 cell now requires 'every claim graded B or C names its counter-evidence, or the essay states that it makes no such claim', so an essay without counter-evidence cannot reach L3 on this criterion. L2 (at most two uncited) then describes it.")
row("proj-dag-concepts", "2.9-DAG", C + "; course/modules/LX/LX1/L02.html:110; course/modules/LX/LX1/L01.html:65", "PASS",
    "check_dag LX1 PASS (out/check_dag_LX1.out). The page uses one data-concept link, debt-deflation (to L02.html#def-debt-deflation, defined in L02 at :110, a Lesson 2 definition that precedes this use in reading order). 'fundamental value, as Lesson 1 defines it' is plain prose (L01.html:65 dfn id def-fundamental-value); no outside-closure concept is linked.")
row("proj-rubric-exhaustive-r14", "2.6-rubric (exhaustive; BUILDER text)", C + ":473 (C2 L2 cell); :473 L3 and L4 bubble clauses", "FAIL",
    "A C2 essay with full chains (at least three steps each, basis named for each step, analogy-holds steps and failure step with evidence) that calls a price move a bubble without naming its benchmark fails L4 and L3 on the bubble clause, and matches no L2 clause that is about the bubble. It scores L2 only if it also lists similarities and at least one difference (L2 first clause); otherwise no clause describes it, so it scores 0 under the 'no level describes' rule. The score therefore depends on whether the essay happens to list a difference, not on the bubble error. Pattern 3 of the plan's ten student errors lands here.",
    "Add to the C2 L2 cell (:473, third column) a clause such as 'or calls a price move a bubble without naming the benchmark it departs from (a fundamental value, or a cited source)', so that a complete essay with that one error scores 2 by the stated rule.")
row("proj-student-error-coverage", "2.6-rubric (student-error analogue)", C + ":472-476; plans/LX1-build-plan.md §5.4 (ten patterns)", "FAIL",
    "Ten plan patterns mapped to the cells. (1) real debt as nominal: C4 cited formula is wrong, so L2 clause 3, caught. (2) percent change with no base or sign: C4 L3 and L4 require base and sign, L2 clause 3, caught. (3) bubble for any price rise, no fundamental stated: C2 L4 and L3 fail, L2 has no clause for it, outcome 0 or 2 depending on incidental wording. NOT CAUGHT by a defined level. (4) locator that does not contain the claim: C3 L4 and L3 fail, and a wrong shown element does not count (:466), so the claim counts as uncited, caught. (5) analogy asserted to hold, no failure step: C2 L2 clause 'chain but no failure step' or L1, caught. (6) numbers rounded before computing: C4 L2 clause 1, caught. (7) causal gold-standard claim with no source: uncited, C3 L3 fails, caught at L2 or L1. (8) current-condition number with no source: C3 and C4, caught. (9) rung-2 blank filled from memory: the instant check compares the whole expected block (labs.js), mutants m01-m06 killed, caught by the lab. (10) episode date with no locator: C1 L2, caught.",
    "Fix as for proj-rubric-exhaustive-r14: give pattern 3 a defined level in C2 L2.")

row("proj-round11-delta-project-page", "2.9-prose / delta", C + ":62, :475, :534", "PASS",
    "Round-11 lines re-read at their current positions: :62 (the three windows and their change counts 668, 321, 12, each checked against rederive_r18.out), :475 (C4 L2 cell, changed this round, read), :534 (exemplar A limit two, the window start and the 13.58 percent 1985-03 change, checked against rederive_r18.out).")
row("proj-spec-limits-test-each", "2.6-spec", C + ":269, :443, :476, :534", "PASS",
    "Required output (:269) asks for two limits 'with the test that would settle at least one of them'; brief item 5 (:443) says the same; C5 cells (:476) grade the count and the test; exemplar A limit one (:534) names a test (an interest-rate series over the same months). Spec, brief and rubric agree.")
row("proj-notation-n-undefined", "2.9-prose / notation", C + ":60, :431; " + "tests/labs/LX1/lab-LX1-project-3.py:305 (docstring)", "PASS",
    "n is first used at :60 as the denominator n - 1 of 'the sample standard deviation of its monthly log changes'. n is not given a separate definition, but in that sentence it is the count of the changes in the window, which the same sentence defines (sample standard deviation of its changes). :431 (11 degrees of freedom for 12 changes) confirms n = number of changes. Standard statistical convention; not a notation collision (notation scan clean).")
row("proj-spec-window-start-must", "2.6-spec", C + ":62, :431; tests/labs/LX1/lab-LX1-project-3.py (WINDOW_TWO_FROM)", "PASS",
    "The window start of window two (2000-01) is stated on the page (:62) and in the lab (WINDOW_TWO_FROM = '2000-01'). :431 says the window start is a candidate limit that the essay may name or not. Nothing in the spec requires a different start, so the requirement that a window start be stated is met by the page's own definitions.")

# ---- corrections to earlier wording (kept explicit so the evidence matches the reads) ----
R["proj-r18-delta-hunks"] = dict(id="proj-r18-delta-hunks", check="2.9-prose / delta",
    location="git diff -U0 700bf33f 50559266 -- course/modules/LX/LX1/project.html", status="PASS",
    evidence="Delta read hunk by hunk: 7 changed lines in project.html, :170 (Lab 1 interpretation), :176 (worked step 2), :257 (Lab 2 interpretation), :280 (data paragraph, three series), :431 (Lab 3 interpretation), :473 (rubric C2 L2 cell), :475 (rubric C4 L2 cell). tests/labs/LX1 is unchanged in the delta (git diff stat lists no LX1 lab twin), so the three project twins are byte-identical to 700bf33f. L01 and cards.json changed in the delta but are other slices. L02, L04, index.html, MANIFEST, fx_monthly.csv, references.json, notation.json are byte-identical to 700bf33f.")
R["proj-rubric-observable"]["evidence"] = ("Each level cell names an element a rater can check (counts of dates, locators, chain steps, rule and formula cells, named limits, sources, similarities). Vague-word grep of project.html for appropriate, good, sufficient, adequate: 0 hits (the 'strong' hits are HTML tags). 'Picks two events' (C1 L1) and 'Mentions a caveat' (C5 L1) name checkable acts. The rule at :466 makes a wrong shown element not count, so correctness is part of each presence check. Exclusivity and exhaustiveness are checked in proj-calibration-exemplars and proj-rubric-exhaustive-r14.")
R["proj-calibration-exemplars"]["location"] = C + ":484-606 (exemplar annotations); :466 scoring rule; :473-476 (cells)"
R["proj-rubric-c3-inference-gap"]["evidence"] = ("C3 L4 accepts a claim 'marked as the writer's own inference' without a locator; C3 L3 accepts at most two claims without a locator (:474). Brief item 2 (:440) asks for failure evidence for the analogy, not for inference-marked claims. Both cells are read as written; the inference-marked route is bounded by the L3 count.")
R["proj-data-snapshot-rebuild"]["location"] = "course/assets/data/market/fx_monthly.csv; course/assets/data/market/MANIFEST.json (fx_monthly)"

# ---- the one new row and the mutant table ----
row("proj-lab3-blank-gap-inputs", "2.5-labs", "tests/labs/LX1/lab-LX1-project-3.py; " + S + "/out/blank_cell_r18.out; gap_and_text_cell_r18.out; blank_first_row_r17n01.out", "PASS",
    "Distinguishing inputs run against the twin under python -I -W error (scratch copies of the snapshot): blank GBP at 1985-03 -> ValueError naming the cell (rc 1); blank at 1971-01 -> ValueError (rc 1); month gap (1985-03 removed) -> ValueError 'month 1985-04 does not follow 1985-02' (rc 1); non-decimal 'abc' -> ValueError (rc 1); unchanged snapshot -> rc 0. Supports the page's Check sentence (:308-309).")

mut_lines = open(S + "/out/kill_all_r18.out", encoding="utf-8").read().splitlines()
verdicts = {}
for ln in mut_lines:
    parts = [p.strip() for p in ln.split("|")]
    if len(parts) >= 3:
        verdicts[parts[1]] = (parts[0], parts[2])
SURV = {
    "lx1c_r18n02_lab3_difference_of_printed_sds.py": "lab3_synth_r18.out: killed on synthetic input rounding_seed11 (twin -0.08, printed-value difference -0.07)",
    "lx1c_r18n03_lab3_zero_change_tested_after_rounding_to_four_places.py": "lab3_synth_r18.out: killed on synthetic input tiny_moves (zero counts differ)",
    "lx1c_r18n04_lab3_window_two_centred_on_window_one_mean.py": "lab3_synth_r18.out: killed on synthetic input rounding_seed8 (ratio and difference differ)",
    "lx1c_r18n05_lab3_blank_cell_carried_forward_as_flat_rate.py": "blank_cell_r18.out: twin rc 1 (ValueError at 1985-03), mutant rc 0",
    "r17n01_lab3_blank_gbp_cell_read_as_zero.py": "blank_first_row_r17n01.out: blank at 1971-01: twin ValueError, mutant ZeroDivisionError; blank_cell_r18.out rc 1 both",
}
mutants = []
for path in sorted((ROOT / "ledgers/LX1/mutants").glob("*.py")):
    name = path.name
    first = path.read_text(encoding="utf-8").splitlines()[0].strip('"').strip()
    if name in SURV:
        killed = SURV[name]
    else:
        status, reason = verdicts[f"ledgers/LX1/mutants/{name}"] if f"ledgers/LX1/mutants/{name}" in verdicts else verdicts[name]
        assert status == "KILLED", (name, status)
        killed = "harness_r18.py cands on the current twin (out/kill_all_r18.out): " + reason
    mutants.append(dict(id=name, description=first, killed_by=killed))
assert len(mutants) == 79, len(mutants)

covered = set(R)
missing = [i for i in prev_ids if i not in covered]
assert not missing, missing
rows = [R[i] for i in prev_ids if i in R] + [R[i] for i in R if i not in prev_ids]
nonpass = [r["id"] for r in rows if r["status"] != "PASS"]
frag = {
    "unit": "LX1",
    "slice": "LX1-c",
    "round": 18,
    "verifier": "Claude Haiku 5.5 (claude-haiku-5-5), independent verifier for LX1-c, round 18 (did not build LX1)",
    "pin": "505592668894eff518befad086df192000dc86c0",
    "base": "700bf33f (round-17 pin; the round-17 fragment is /Users/billyribeiro/.fanout/frags/E-LX1-c.round17.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE18-LX1-c",
    "scratch": "ledgers/LX1/scripts/LX1-c-r18/ (scripts and out/); no scratch outside the repo except /tmp copies removed after each run",
    "verified_at": "2026-11-09T05:30:00Z",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta 700bf33f -> 50559266 for LX1-c: course/modules/LX/LX1/project.html (7 changed lines, all read: :170, :176, :257, :280, :431, :473, :475). tests/labs/LX1 unchanged. Fixed since round 17 and now PASS: C2 L2 count wording, C2 basis gap, C4 formula/base gap, C3 L3 counter-evidence gap. Still open: C2 bubble-benchmark clause has no L2 descriptor (proj-rubric-exhaustive-r14, proj-student-error-coverage).",
        "Exclusivity (as text): C1 L3/L2, C2 L2 first clause/L1, C3 L3/L2, C4 L3/L2 clause 2, C5 L3/L2 overlap; the line-466 highest-level rule resolves each, so each essay has one score. That is why the calibration row is UNVERIFIABLE-pending-blind by the stated condition. Exemplars were not scored by this verifier (ruling 23).",
        "Judgment, not a FAIL: C1 with dates for both episode and condition and no locator for either falls to L1 ('Picks two events'), because L2 says 'missing for one of them'. The outcome is defined by the highest-level rule, so exhaustiveness holds; the architect may want 'for one or both of them'.",
        "Judgment, not a FAIL: a wrong locator counts as uncited under the :466 rule (a wrong shown element does not count), so pattern 4 is capped at L2 and falls to L1 with more than two such claims.",
        "Lab mutants: 79 files in ledgers/LX1/mutants (74 earlier plus lx1c_r18n01 to n05). 74 killed on the shipped run. The 5 survivors of the shipped run are Lab 3 mutants equivalent on the shipped snapshot (no blank, no tiny move, no rounding tie), each killed by a distinguishing input recorded in killed_by. LX1 is rubric-only; these are student-error analogues, not grader mutants (ruling).",
        "Lab mutant r17n01's docstring says a blank cell is 'taken as a flat rate', but its code (cell or '0') makes the log change fail, so it is killed by a crash, not by a flat rate. Its kill is valid (its ZeroDivisionError differs from the twin's ValueError on a blank in the first row). Recorded for the architect; no change made.",
        "Two alternative correct implementations pass the shipped run (alt_r18_A lab 1 Decimal; alt_r18_B lab 3 statistics.stdev and log1p with index windows).",
        "check_pages --unit LX1 --page project exits 1 (lesson-template checks applied to the project page). check_pages.py:25 says project pages are checked by check_projects.py, so this is not counted as a gate failure; the unit-wide check_pages and check_projects both PASS.",
        "Clarifying question a competent student could ask (not a FAIL): 'current condition' is dated against 'the last month of the data you use' (:439); for a source outside the snapshot, the student must infer which month that is. The spec states the rule, so the row is PASS.",
        "Not checked by this verifier: exemplar scores (blind scorer, ruling 23); a live-feed rebuild of fx_monthly.csv (carried from round 17; the bytes match MANIFEST sha256 this round); visual rendering beyond page_smoke; the L01, L02, L04 and cards slices (other verifiers) beyond the lines this page cites; render_curriculum.py --check (no curriculum input changed in the delta); the full pytest suite (only labs and refs were run); hours were re-estimated roughly, not timed.",
    ],
    "summary": f"LX1-c round 18 on 505592668894eff: verdict FAIL. {len(rows)} rows: {sum(1 for r in rows if r['status']=='PASS')} PASS, {sum(1 for r in rows if r['status']=='FAIL')} FAIL, {sum(1 for r in rows if r['status']=='UNVERIFIABLE')} UNVERIFIABLE. Non-PASS: {', '.join(nonpass)}. Mutants: 79 lab mutants, 79 killed (74 on the shipped run; 5 by distinguishing inputs). Alternatives: 2 pass.",
}
out = ROOT / "ledgers/LX1/LX1-c.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "nonpass", nonpass, "mutants", len(mutants))
