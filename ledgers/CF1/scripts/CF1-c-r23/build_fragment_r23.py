# Builds the round-23 slice-c fragment (ledgers/CF1/CF1-c.json). Prior rows come from the round-22 fragment.
# Carried rows keep their previous evidence behind the required prefix; re-verified rows get new evidence.
import json, sys
PREV = "/tmp/fanout-frags/CF1-c.round22.json"
prev = json.load(open(PREV, encoding="utf-8"))
L05_CARRY = ("Carried from round 22 (course/modules/CF/CF1/L05.html, tests/labs/CF1/, references/, tools/, "
             "course/modules/CF/CF1/index.html and L04.html byte-identical since the previous pin fd9a9b7; "
             "this row cites no changed L06.html line and no changed cards.json entry): ")
L06_RE = ("Round 23 re-verification on 503d139: whole L06.html read this round; the only L06.html line changed in "
          "the delta since fd9a9b7 is line 106. ")
RE = {
 "CF1-c-cmd-pin": "git rev-parse HEAD = 503d13980b2ad23201063107a2d6844e00b23d6d; git status: only the untracked .venv symlink (out/pin.txt).",
 "CF1-c-cmd-check_pages": "tools/check_pages.py --all: AC1, AC2, AC4, CF1, AP1 all PASS, rc 0 (ledgers/CF1/scripts/CF1-c-r23/out/check_pages.txt).",
 "CF1-c-cmd-check_dag": "tools/check_dag.py --all: all five units PASS, rc 0 (out/check_dag.txt).",
 "CF1-c-cmd-run_labs": "tools/run_labs.py --unit CF1: 'run_labs CF1: PASS (9/9)', rc 0 (out/run_labs.txt).",
 "CF1-c-cmd-page_smoke": "tools/page_smoke.py --unit CF1 --pages L05 L06: both pages PASS, 'page_smoke CF1: PASS', rc 0; page_smoke timings print lab-CF1-L05-1 0.0 s and lab-CF1-L06-1 0.3 s (out/page_smoke.txt).",
 "CF1-c-cmd-ruff-mypy-labs": "ruff check tests/labs/CF1: 'All checks passed!'; ruff format --check: 9 files already formatted; mypy --no-incremental on both twins: 'Success: no issues found in 2 source files' (out/ruff.txt, out/mypy.txt).",
 "CF1-c-cmd-pytest-labs": "pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_docs_figures.py: all dots, rc 0 (out/pytest_labs.txt).",
 "CF1-c-cmd-verify_refs": "tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems'; tools/verify_refs.py --unit CF1: 'live re-verification of CF1: 2 of 560 entries, 0 problems'; both rc 0 (out/verify_refs_*.txt).",
 "CF1-c-cmd-twin-vs-page": "ledgers/CF1/scripts/CF1-c-r14/twin_vs_page.py run under python -I against 503d139: expected output identical to twin output for L05 and L06; code identical ignoring one trailing newline (out/twin_vs_page.txt).",
 "CF1-c-twin-freshness": "twin_vs_page output: both twins' printed output equals the page's embedded expected block; both twins re-run this round (out/lab_L05.out, out/lab_L06.out, rc 0).",
 "CF1-c-lab-L05-1-run": "tests/labs/CF1/lab-CF1-L05-1.py under python -I -W error: rc 0, stderr empty (out/lab_L05.rc, out/lab_L05.err).",
 "CF1-c-lab-L06-1-run": "tests/labs/CF1/lab-CF1-L06-1.py under python -I -W error: rc 0, stderr empty (out/lab_L06.rc, out/lab_L06.err); printed output matches the page block at L06.html lines 194-205.",
 "CF1-c-cmd-mutants-na-r13": "ledgers/CF1/mutants/ now holds 216 files, all slice-d project-grader mutants. Slice c has no project grader, so no slice-c mutant applies; scope statement re-checked (PASS).",
 "CF1-c-registry-r13": "references/ unchanged since fd9a9b7 (no diff). verify_refs --offline: 560 entries, 0 problems. L06.html line 106 re-read this round: the claim span still states the registry record title and that no result from Glasserman (2003) is stated, graded C with 'passage locator not confirmed'.",
 "CF1-c-attrib-L06-glasserman": L06_RE + "Claim span at line 106 re-read: 'The registry records Glasserman (2003), Monte Carlo Methods in Financial Engineering, and this lesson states no result from it.' The new clause before it does not change the attribution; graded C with the locator stated as unconfirmed (PASS).",
 "CF1-c-num-L06-closed-forms": L06_RE + "Line 111 (lab hypothesis 79078.68 and 49379.84) and Prop 2.3 (lines 92-96): closed forms recomputed as 79078.68 and 49379.84 (out/recompute_L06.txt). PASS.",
 "CF1-c-num-L06-E1-prob": L06_RE + "E1 (line 313): 84543.40-79078.68 = 5464.72; 5464.72/4400.22 = 1.24192, printed 1.2419 from displayed digits and +1.242 by the lab; 2(1-Phi(1.2419)) = 0.21427 -> 0.2143 (out/recompute_L06.txt). PASS.",
 "CF1-c-num-L06-E2-band": L06_RE + "E2 (line 320): 0.0552 +/- 1.96 x 0.0010 = 0.05324 to 0.05716, printed 0.0532 to 0.0572 (out/recompute_L06.txt). PASS.",
 "CF1-c-num-L06-M2-M3": L06_RE + "M2: 35/12 = 2.9167, sqrt = 1.7078; M3: -100 + 50(1/1.1 + 1/1.21) = -13.2231 -> -13.22 (out/recompute_L06.txt). PASS.",
 "CF1-c-num-L06-19.9-22.4": L06_RE + "4400.22/221.01 = 19.9096 -> 19.9; sqrt(500) = 22.3607 -> 22.4 (out/recompute_L06.txt). Line 206 says the lab does not isolate the cause of the gap, which the twin confirms (each se is computed from the sample sd; the closed-form sd is not used for it). PASS.",
 "CF1-c-num-L06-E3-width": L06_RE + "E3 (line 327): 143406.13-14896.62 = 128509.51; /100 = 1285.10; unrounded 128509.503511 (out/lab06_unrounded.txt) -> 128509.50 to two decimals (PASS).",
 "CF1-c-num-recompute-r11": L06_RE + "Lines 96 and 111 of L06.html recomputed (out/recompute_L06.txt); L05.html lines 101 and 218 are unchanged and carried (PASS).",
 "CF1-c-num-L06-s3-quantile-unrounded": L06_RE + "Line 211: printed quantiles 14896.62, 79457.94, 143406.13; unrounded 14896.623057, 79457.938852, 143406.126569 (out/lab06_unrounded.txt); difference 128509.503511 -> 128509.50; gap to the printed difference 0.0065 is rounding. Also negative count 2761/50000 = 0.05522 -> 0.0552 and se 0.0010215 -> 0.0010 (PASS).",
 "CF1-c-r20-L06-line211-recompute": L06_RE + "Line 211 recomputed this round as above (PASS).",
 "CF1-c-r20-L06-quiz-se-explain": L06_RE + "Line 447 explain: count 2761 (out/lab06_unrounded.txt), 2761/50000 = 0.05522, se 0.0010215 -> 0.0010; numeric item data-answer 0.0010, tolerance 0.00005 (PASS).",
 "CF1-c-r18-L06-line106-E1-E2": L06_RE + "Changed clause at line 106 vs E1 (line 313) and E2 (line 320). E1 labels the two-sided tail probability as conditional on the normal reading. E2 labels the band through its 1.96 multiplier ('The 1.96 multiplier is the normal reading of Remark 2.4, which this lesson does not test'); E2 does not use the word 'conditional'. E1's cents error 5464.72 and count 1.2419 carry no conditional label, as the clause says. The twin has no normal test (grep normal/gauss/erf/1.96: no matches). PASS.",
 "CF1-c-r18-E1-E2-arithmetic": L06_RE + "E1 ratio 1.24192, tail 0.21427; E2 band 0.05324-0.05716; E3 width 1285.10 (out/recompute_L06.txt). PASS.",
 "CF1-c-r18-mut-L06-06-10": "Re-run this round (out/lab_mutants.txt, runner ledgers/CF1/scripts/CF1-c-r20/run_lab_mutants_r20.sh): r18_L06_06, 07, 08, 09 exit 0 with different printed output; r18_L06_10 exits 0 with the same printed output (equivalent on the displayed output: its se denominator is n-1 = 49999, which rounds to the same 0.0010; out of scope per the lab-twin ruling).",
 "CF1-c-r18-mut-L05-01-04": "Re-run this round (out/lab_mutants.txt): r18_L05_01, 02, 04 exit 0 with different printed output; r18_L05_03 exits 1 (ZeroDivisionError). PASS.",
 "CF1-c-r18-grade-definition-T": "Re-verified this round against the changed cards: CF1-c062 and CF1-c063 (L05) and CF1-c075, c076, c099, c100 (L06) are now grade C with basis '<Definition> (the lesson's definition)'; CF1-c096 remains C. A definition is not a theorem, and BLUEPRINT section 3 has no convention grade. Stated basis present on every card. PASS (judgement recorded in the notes).",
 "CF1-c-grade-L06": L06_RE + "Key-results table (lines 364-370): T rows are proved in section 2 or Problem P2 (Props 2.1-2.3; P2 at line 295); C rows cite Lab 1 SIMULATED seed 6 (values match out/lab_L06.out). PASS.",
 "CF1-c-math-L06-props": L06_RE + "Props 2.1-2.3 (lines 71-96) and their proofs re-read; the Prop 2.2 algebra is checked: sum (k-c)^2 = m(m-1)(m+1)/12 gives (m^2-1)/12; Remark 2.4 (line 106) says the normal approximation is not proved here (PASS).",
 "CF1-c-math-L06-P3-median": L06_RE + "P3 (line 302): rank ceil(n/2) = (n+1)/2 for odd n; middle value (PASS).",
 "CF1-c-math-L06-R3-same-variance": L06_RE + "R3 (line 352): loadings of one sign make every pairwise covariance positive; the P2 term-by-term argument applies; expectation unchanged (PASS).",
 "CF1-c-lab-L06-normal-overreach": L06_RE + "Remark 2.4 at line 106: 'Lab 1 does not test the normal reading'; the twin contains no normal-distribution computation (grep: no matches) (PASS).",
 "CF1-c-lab-L06-hypothesis": L06_RE + "Line 111 hypothesis against the printed output: four sample means within 3 se (within_3se True x4), sd 49419.62 near 49379.84, se falls roughly as sqrt(n) (interpreted at line 206) (PASS).",
 "CF1-c-lab-L06-sqrt-explanation": L06_RE + "Line 206 explanation re-checked numerically (19.9 vs 22.4) (PASS).",
 "CF1-c-struct-L06": L06_RE + "Whole page read: sections 1-9, lab, quiz, references block, lesson nav to L05 (PASS).",
 "CF1-c-banned-scan": "ledgers/CF1/scripts/CF1-c-r16/banned_scan_r16.py on L05.html and L06.html: 0 hits for both (out/banned_scan.txt).",
 "CF1-c-prose-process-path": "Learner text of L05.html and L06.html read this round: no process words; banned_scan_r16 (which includes the process-word set) reports 0 hits (out/banned_scan.txt).",
 "CF1-c-prose-L06-often-correlated": L06_RE + "Section 4 first bullet (line 226): correlation changes the variance (P2); Lab 1 does not test independence (PASS).",
 "CF1-c-prose-L06-tail-quantiles": L06_RE + "Section 4 third bullet (line 228): Prop 2.1 covers the mean, not the quantiles (PASS).",
 "CF1-c-prose-L06-def12-summaries": L06_RE + "Line 63 Definition 1.2: sample SD divides by n-1, se = sample SD / sqrt(n), nearest-rank ceil(pn); the twin uses statistics.stdev and quantile() (PASS).",
 "CF1-c-prose-L06-misconception1-near": L06_RE + "Misconception 1 (line 240) matches the lab output (four means near the closed form) (PASS).",
 "CF1-c-prose-L06-misconception-count": L06_RE + "Section 5 has three misconceptions (lines 239-248) (PASS).",
 "CF1-c-scope-L06-section4-intro": L06_RE + "Line 223 ('Propositions 2.1 and 2.3 hold for the model they are stated for') and the four bullets at 226-229 (PASS).",
 "CF1-c-quiz-L06q1-units": L06_RE + "L06q1 (lines 380-387): 300/sqrt(100) = 30 cents (PASS).",
 "CF1-c-hours": "data-hours=8 on L05.html and L06.html (line 2 of each, re-read); index.html line 29 data-hours-lessons=48; 6 lessons x 8 h = 48 h, project 12 h, 60 h total: hub split and lesson hours agree (arithmetic only; hours are design targets per the architect ruling).",
 "CF1-c-concepts": "check_dag --all PASS (out/check_dag.txt); L06.html line 63 dfn id def-monte-carlo-npv re-read: unchanged (PASS).",
 "CF1-c-cards-duplicates": "cards.json now has 110 entries (109 before; CF1-c110 is an L01 card added in the delta). Scan: no duplicate ids, fronts or backs (normalised). The previous count of 103 is stale (PASS).",
 "CF1-c-cards-delta-r12": "Cards changed in the delta since fd9a9b7 that are in slice c: CF1-c062, c063 (L05), c075, c076, c084, c099, c100 (L06). Each re-read against its lesson text this round (see CF1-c-cards-L05, CF1-c-cards-L06, CF1-c-r16-cards-c099-def12). CF1-c068 unchanged (PASS).",
 "CF1-c-cards-dupes-r12-cross": "cards.json all 110 entries: no duplicate fronts or backs (scan this round) (PASS).",
 "CF1-c-cards-L05": "L05 cards re-read: CF1-c062 back = Definition 1.1 (L05.html line 60): 'first year-end t >= 1 at which the cumulative undiscounted flow is zero or more (Definition 1.1)'; CF1-c063 back = Definition 1.2 (line 68): same rule on discounted flows with the same interpolation (PASS). Other L05 cards unchanged since fd9a9b7 (CF1-c-cards-L05-other).",
 "CF1-c-cards-L06": "L06 cards re-read: CF1-c075 = Definition 1.1 (line 58); CF1-c076 = Definition 1.2 (line 63); CF1-c099 and c100 = Definition 1.2 (line 63: se and nearest-rank quantile); CF1-c084 = Remark 2.4 clause (line 106); each matches the page; grade C with basis (PASS). Other L06 cards unchanged.",
 "CF1-c-cards-L06-c-other": "CF1-c099 (changed; grade C, basis 'Definition 1.2 (the lesson's definition)') vs L06.html line 63: matches; other L06 cards unchanged (PASS).",
 "CF1-c-cards-L05-other": "CF1-c062 and c063 (changed; re-read in CF1-c-cards-L05); CF1-c068 back ('2.750 years ... does not depend on the 10 per cent rate') unchanged since fd9a9b7 and matches L05.html line 70 (PASS).",
 "CF1-c-r16-cards-c099-def12": "cards.json CF1-c099: back text unchanged; grade now C (was T), basis 'Definition 1.2 (the lesson's definition)'. Text matches L06.html line 63 (PASS; the round-22 grade T is superseded).",
 "CF1-c-r17-cards-c096-grade": "CF1-c096 grade C, basis 'convention, Section 1 (interpolation)' (unchanged). The round-22 comparison was to CF1-c062, now grade C with basis 'Definition 1.1 (the lesson's definition)', so the comparison no longer distinguishes them; the grade rule is unchanged (PASS; the stale comparison is superseded).",
 "CF1-c-delta-cross-slice-notes": "cards.json CF1-c054 (L04) changed: back now reads 'At r* = (C_B - C_A)/(K_B - K_A) - 1 ... (Theorem 4.1). Here K is the outlay and C the inflow'; matches L04.html Theorem 4.1 (line 127: r* = Delta C / Delta K - 1 with Delta K = K_B - K_A). CF1-c056, c058, c060, c094 unchanged. project.html line 192 'collects 157 checks': pytest --collect-only on the reference copy gives 157 tests collected (out/collect_157.txt) (PASS).",
 "CF1-c-r20-project-count-157": "Re-run this round: 157 tests collected (out/collect_157.txt). project.html line 192 unchanged; the rest of project.html is slice d's subject (PASS for the count only).",
 "CF1-c-r17-mutants-lab-L06": "Re-run this round: c17_L06_01, 02, 03, 05 exit 0 with different printed output (out/lab_mutants.txt).",
 "CF1-c-r17-mut-L06-04-equivalent": "Re-run this round: c17_L06_04 exits 0 with the same printed output; the zero-draw check gives 0 exact-zero draws for seed 6 (ledgers/CF1/scripts/CF1-c-r17/out/zero_check.out), so the change is equivalent on this seed. Out of scope per the lab-twin ruling (PASS).",
 "CF1-c-r17-alt-impl": "grep -c assert on both twins: 0 each (re-checked this round) (PASS).",
 "CF1-c-r17-mutants-project-grader": "Scope note re-checked: the 139 count was the round-17 project-grader run (slice d's subject). ledgers/CF1/mutants now holds 216 files, all slice d's. Slice c makes no claim about them (PASS as scope).",
 "CF1-c-r20-lab-mutants-rerun": "Re-run this round (out/lab_mutants.txt): 17 mutants and alternatives. Real differences: 12 (c17_L06_01, 02, 03, 05; r18_L05_01, 02, 04; r18_L06_06, 07, 08, 09) plus r18_L05_03 (exit 1); equivalent on the printed output: c17_L06_04, r18_L06_10. The three alt_r18 alternatives are byte-identical to the L06 baseline (the runner classifies them against L05 by name, a runner artefact; diff of their output against out/base_L06.out is empty). PASS.",
 "CF1-c-r20-new-mutants-na": "Slice c mutation scope re-checked: slice c has no project grader; lab twins are not mutation-tested (architect ruling); no new mutants written this round (PASS).",
}
rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in RE:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": RE[rid]})
    else:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": L05_CARRY + r["evidence"]})
NEW = [
 ("CF1-c-r23-delta-scope", "2.9-structure", "git diff --stat fd9a9b7 503d139 for slice c files",
  "Slice-c delta: L06.html (line 106 only), cards.json (entries CF1-c001, c014, c018, c021, c024, c033-c035, c047-c049, c054, c062, c063, c075, c076, c084, c088, c091, c099, c100; new c110). L05.html, index.html, L04.html, tests/labs/CF1/, references/, tools/ unchanged (git diff --quiet). project.html is slice d's subject and is not verified here."),
 ("CF1-c-r23-L06-line106-clause", "2.4-math", "course/modules/CF/CF1/L06.html line 106 (Remark 2.4) vs E1 line 313 and E2 line 320",
  "New clause checked against E1 and E2: E1 labels the tail probability as conditional on the normal reading; E2 labels the band through its 1.96 multiplier, which the lesson says is the normal reading it does not test (E2 does not use the word 'conditional'). The cents error (5464.72) and the count (1.2419) in E1 carry no conditional label, as the clause says. PASS."),
 ("CF1-c-r23-share-count-2761", "2.2-numbers", "L06.html line 211, line 447 explain, E2 line 320; out/lab06_unrounded.txt",
  "Negative-draw count 2761 of 50000 re-computed from the twin's own generator: share 0.05522 -> 0.0552; se sqrt(p(1-p)/n) = 0.0010215 -> 0.0010. PASS."),
 ("CF1-c-r23-cards-c084", "2.9-structure", "cards.json CF1-c084 back vs L06.html line 106",
  "Back text: 'The tail probability in E1 and the band in E2 are conditional on that reading; the cents error and the count of standard errors in E1 are not.' Matches the page clause; front matches Remark 2.4. PASS."),
 ("CF1-c-r23-cards-grade-C-definitions", "2.3-grades", "cards.json CF1-c062, c063, c075, c076, c099, c100 (grade C, basis '... (the lesson's definition)')",
  "A definition is not a theorem (grade T would overstate). BLUEPRINT section 3 has no convention grade; the program uses C for conventions (the round-17 and round-19 rows record the same judgement). Each card carries its basis. PASS as a recorded judgement; the grade is not a claim about evidence."),
 ("CF1-c-r23-collect-157", "2.7-cards", "grader/test_project.py collected from the reference copy (r20 script)",
  "157 tests collected (out/collect_157.txt). project.html line 192 count matches; the rest of project.html is slice d's subject."),
 ("CF1-c-r23-scope-note", "2.5-labs", "round 23 scope",
  "Re-read in full this round: L05.html and L06.html (whole pages). L05 rows carried by byte-identity (L05.html unchanged). Not verified here: project.html C2 sentence and grader tests (slice d), L01 card CF1-c110 (L01 slice), L04 cards other than CF1-c054 (carried)."),
]
for rid, check, loc, ev in NEW:
    rows.append({"id": rid, "check": check, "location": loc, "status": "PASS", "evidence": ev})
mutants = []
for m in prev["mutants"]:
    mm = dict(m)
    mm["killed_by"] = m["killed_by"] + " | re-run round 23 (ledgers/CF1/scripts/CF1-c-r23/out/lab_mutants.txt): same result"
    mutants.append(mm)
frag = {
 "unit": "CF1", "slice": "CF1-c", "round": 23,
 "verifier": "Haiku 5.5 independent verifier (round 23)",
 "pin": "503d13980b2ad23201063107a2d6844e00b23d6d",
 "base": "fd9a9b72f000e509f3af78babf970cd4c9a847e4 (round-22 fragment pin; previous rows carried only where the cited subject is byte-identical)",
 "checkout": "/tmp/verify23-CF1-c",
 "scratch": "/tmp/CF1-v/c23",
 "verified_at": "2026-10-28T12:00:00+00:00",
 "verdict": "PASS",
 "rows": rows,
 "mutants": mutants,
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
  "Delta since fd9a9b7 (the round-22 fragment pin) for slice c: L06.html line 106 only; cards.json entries listed in CF1-c-r23-delta-scope. L05.html, labs, references, tools, index.html and L04.html are byte-identical, so their previous PASS rows are carried.",
  "Judgement recorded (not a finding): grade C on definition cards (CF1-c062, c063, c075, c076, c099, c100) with basis '(the lesson's definition)'. BLUEPRINT section 3 has no convention grade; the convention rule is applied consistently with CF1-c096.",
  "Lab-twin mutants are out of mutation scope (architect ruling). The two equivalent mutants (c17_L06_04, r18_L06_10) are equivalent on the printed output for seed 6. Alternatives alt_r18_a/b/c are byte-identical to the L06 baseline; the runner classifies them against L05 by name (a runner artefact, not a finding).",
  "Slice c has no project grader, so the project-mutant requirement does not apply; no new student-error mutants were written this round.",
  "Not verified in this slice: project.html C2 sentence and grader tests (slice d); card CF1-c110 (an L01 card, belongs to the L01 slice); the live verify_refs covered 2 of 560 entries only (tool behaviour).",
  "Hours: data-hours=8 on L05 and L06; hub split 48 + 12 = 60 agrees with 6 lessons x 8 h; not re-estimated (design targets).",
 ],
 "summary": "Slice c round 23: verdict PASS. Delta since fd9a9b7 is one L06 clause (line 106) and cards.json entries. Re-verified: the changed clause against E1/E2; every L06 number recomputed (E1 1.2419 and 0.2143; E2 0.0532-0.0572; E3 1285.10; unrounded quantiles and count 2761); changed cards CF1-c062, c063, c075, c076, c084, c099, c100 against their lesson text; command rows re-run; 17 lab-twin mutants re-run. Carried by byte-identity: L05 rows and other unchanged rows. Not verified: project.html and the slice-d grader; L01 card c110.",
}
json.dump(frag, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows", len(rows), "mutants", len(mutants))
