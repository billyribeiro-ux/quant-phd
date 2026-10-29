import json
P = "course/modules/E/E5/"
C6 = "Carried from round 6 (cited lines byte-identical since the previous pin 9fd6aed): "
C6L1 = "Carried from round 6 (course/modules/E/E5/L01.html and tests/labs/E5/lab-E5-L01-1.py byte-identical since 9fd6aed): "
rows = []
def R(id_, check, location, status, evidence):
    rows.append({"id": id_, "check": check, "location": location, "status": status, "evidence": evidence})

R("E5a-r3-hub-prereq-titles", "Hub prerequisite titles match curriculum strings", P + "index.html:35", "PASS",
  C6 + "line 35 unchanged in the 9fd6aed..0d2d0f3 delta (git diff hunks at index.html:33 and :147-151 only).")
R("E5a-r3-hub-card-titles", "Hub card titles equal lesson h1", P + "index.html:145-152", "PASS",
  "Re-verified this round: card titles at index.html:146-153 equal L01.html:35, L02.html:35, L03.html:36, L04.html:36, L05.html:36, L06.html:36, L07.html:36, L08.html:36 (grep '<h1>'). Card bodies at :150-151 re-read against L05 A1 and L06 A3 (see E5a-r7-hub-card-bodies).")
R("E5a-r3-nav-titles-L02-L03", "Lesson-nav labels equal target h1", P + "L02.html:490; L03.html:617", "PASS",
  C6 + "L02.html:490 and L03.html:617 are outside the changed lines (L02 :368, L03 :611).")
R("E5a-r3-hub-grammar", "Learner prose is grammatical", P + "index.html:33", "PASS",
  "Re-read this round: index.html:33 is grammatical after the round-7 edit ('The module is closed-economy, and it is static except for ... and it does not cover ...'). The content error in the same sentence is row E5a-r6-hub-lede-static-claim.")
R("E5a-r3-L02-exactly-when", "Claim about a theorem matches its statement", P + "L02.html:104 vs Theorem 2.3 at :107-110", "PASS",
  C6 + "lines 104 and 107-110 unchanged.")
R("E5a-r3-L03-attribution-wording", "References paragraph consistent with page naming", P + "L03.html:611", "PASS",
  "Re-read this round: L03.html:611 still says the lesson 'has not read that paper and attributes no result to it'. No attribution beyond the registry key.")
R("E5a-r3-L03-sign-lemma-first-use", "Terms defined before use", P + "L03.html:52 vs :138", "PASS",
  C6 + "lines 52 and 138 unchanged.")
R("E5a-card-uniqueness-contradiction", "Cards agree with the current lesson statement (Prop 2.2 says exactly one POSITIVE steady state)", P + "cards.json (E5-c041); L03.html:52, :98, :527", "PASS",
  C6 + "cards.json E5-c041 is outside the delta (delta cards are E5-c065, c068, c091-c101); L03.html:52, :98, :527 unchanged.")
R("E5a-cmd-check-pages", "check_pages unit E5 and per page L01, L02, L03", "tools/check_pages.py --unit E5 [--page L01|L02|L03]", "PASS",
  "Run this round at 0d2d0f3: 'check_pages E5: PASS' (--unit E5, all pages incl. hub); 'check_pages E5 L01: PASS'; 'check_pages E5 L02: PASS'; 'check_pages E5 L03: PASS'. Note: --page index is not a valid selector for the hub (it reports 13 lesson-only problems); the hub is covered by --unit E5.")
R("E5a-cmd-check-dag", "check_dag E5", "tools/check_dag.py --unit E5", "PASS",
  "Run this round: 'check_dag E5: PASS'. check_projects.py --unit E5: 'check_projects E5: PASS'.")
R("E5a-cmd-run-labs", "run_labs per page", "tools/run_labs.py --unit E5 --page L01|L02|L03", "PASS",
  "Run this round: 'run_labs E5: PASS (1/1)' for each of L01, L02, L03.")
R("E5a-cmd-page-smoke", "page_smoke index, L01-L03", "tools/page_smoke.py --unit E5 --pages index L01 L02 L03", "PASS",
  "Run this round: 'page_smoke modules/E/E5/L03.html: PASS', 'page_smoke E5: PASS'.")
R("E5a-twins-isolated", "Twins run alone under python -I -W error", "tests/labs/E5/lab-E5-L01-1.py, lab-E5-L02-1.py, lab-E5-L03-1.py", "PASS",
  "Run this round in the checkout: 'python -I -W error' exit 0 for all three; L01 last line 'chain product of link ratios 3/2 equals direct ratio 3/2: True'; L02 'log growth is at most simple growth in every period: True'; L03 'equal_within_tolerance True'. Twins byte-identical to 9fd6aed (L01, L02, L03); the L05 twin is the only changed twin in the delta.")
R("E5a-page-code-equals-twin", "Page code block equals twin", P + "L01.html, L02.html, L03.html data-run blocks", "PASS",
  "run_labs E5 PASS for L01, L02, L03 this round (the page-vs-twin code comparison is run_labs' check). L02 and L03 code blocks were not in the delta; only prose lines changed.")
R("E5a-expected-equals-output", "Expected block equals output", P + "L01.html, L02.html, L03.html pre.expected", "PASS",
  "run_labs E5 PASS for L01, L02, L03 this round. L02 output at 0d2d0f3 printed in full (average capital term 0.010667; average residual with alpha 0.4: 0.010665; average log growth of Y 0.029453). L03 expected block (lines 347-382) equals the printed output of the twin (first_period_gap_below_tolerance 692).")
R("E5a-lint-and-tests", "Lint, types, tests for the E5 twins", "tests/labs/E5; mypy; pytest -k E5", "PASS",
  "Run this round: 'ruff check tests/labs/E5' All checks passed; 'ruff format --check' 11 files already formatted; 'mypy --no-incremental tests/labs/E5' Success: no issues found in 11 source files; 'pytest -q -k E5' 12 passed (100%).")
R("E5a-registry-keys", "Reading-list keys exist and match the registry", P + "index.html:178-181; references/references.json", "PASS",
  "Carried from round 6 (index.html:178-181 unchanged; references/ unchanged in the delta). Run this round: 'verify_refs.py --offline': '560 entries, 0 problems'.")
R("E5a-no-friedman", "No stray attribution", "index.html, L01-L03", "PASS",
  "Re-run this round: grep -i friedman over index.html, L01.html, L02.html, L03.html: no hit (exit 1).")
R("E5a-p01-concept-anchors", "P0.1 concept links resolve and read 'not yet released'", P + "index.html:60,65; L01.html:37; concepts.html:39,40,44", "PASS",
  C6 + "index.html:60 and :65 unchanged; course/concepts.html unchanged in the delta (grep 'not yet released' count 946 this round).")
R("E5a-notation", "Symbols match notation/notation.json (no registered symbol reused)", "index.html, L01-L03 math", "PASS",
  "Re-read this round: the only new math in the delta is L02.html:368 (alpha, overline-free Delta ln K_t, the decimal values) which uses the same symbols as L02.html:75, :97-98; L03.html:611 has no symbols. notation/ unchanged in the delta.")
R("E5a-banned-and-process-words", "No process words in learner text", "course/modules/E/E5/L02.html:133, :272; index.html; L01-L03", "PASS",
  "Re-read this round: L02.html:368 ('rounding artifact') and L03.html:611 ('graded C') contain no banned or process words; L02:133 and :272 unchanged since 9fd6aed.")
R("E5a-hours-arithmetic", "Hours arithmetic", P + "index.html:29, :39-42, :146-153", "PASS",
  "Re-verified this round: data-hours-lessons 80 and data-hours-project 30 (index.html:29); split 72.7% + 27.3% = 100% (:40); eight cards at 10 h each (:146-153) = 80 h; 80 + 30 = 110 h (:31, :42).")
R("E5a-placement-arithmetic", "Placement counts and fractions", P + "index.html:70-139 (quiz), :72", "PASS",
  C6 + "index.html:70-139 unchanged. Re-counted: 9 items (7 prerequisite: P0.1 1, E1 2, M1 2, M2 2; 2 skill checks); 7/9 = 77.8 percent, 8/9 = 88.9 percent. Checked: ln(e^2)=2; dy/dx at x=2 is -0.25; ln(1.1)=0.0953; Laspeyres 4/3 = 1.333333.")
R("E5a-data-status-basis", "Data status matches the registry", P + "index.html:171; tools/data_sources.yaml:91-107", "PASS",
  C6 + "index.html:171 unchanged; tools/data_sources.yaml unchanged in the delta.")
R("E5a-r5-index-data-line", "Data line on the hub is accurate", P + "index.html:37", "PASS",
  C6 + "index.html:37 unchanged.")
R("E5a-r5-hub-prereq-concept-status", "Prereq paragraph agrees with concept index status", P + "index.html:60 vs course/concepts.html:39, :40, :44, :70, :12", "PASS",
  C6 + "index.html:60 and course/concepts.html unchanged in the delta.")
R("E5a-L01-numbers", "Prose numbers match unrounded values and lab output", P + "L01.html:107-130, 156, 262-289, 298-310, 336-343, 355-439, 504-530", "PASS",
  C6L1 + "L01 is not in the delta.")
R("E5a-L01-theorems", "Theorems, propositions and proofs are correct", P + "L01.html:70-152", "PASS", C6L1 + "L01 not in the delta.")
R("E5a-L01-lab-claims", "Sentences about what the lab prints and checks match code and output", P + "L01.html:156, :157-292, :311", "PASS",
  C6L1 + "L01 and its twin not in the delta; the run this round prints the lines cited in round 6.")
R("E5a-L01-simulated-label", "Lab labelled SIMULATED where it is generated", P + "L01.html:51, :156, :161, :311, :546", "PASS", C6L1 + "L01 not in the delta.")
R("E5a-L02-numbers", "Prose numbers match unrounded values and lab output", P + "L02.html:368 (E3 solution); other L02 numbers", "PASS",
  "Re-verified this round (fixes the round-6 FAIL). Recomputed with ledgers/E5/scripts/E5-a-r7/recompute_l02.py (python -I): unrounded mean dln K = 0.035556180724540344; alpha 0.3 capital term 0.010666854 -> 0.010667 (printed); alpha 0.4 capital term 0.014222472 -> 0.014222; rounded route 0.4 x 0.035557 = 0.0142228 -> 0.014223. The new L02.html:368 states 0.0355562, 0.014222, 0.014223 correctly. The lab does not print the unrounded average, so the sentence 'the lab does not print it' is correct. Other L02 numbers: carried from round 6 (cited lines unchanged). The E3 instruction wording is a separate row.")
R("E5a-L02-theorems", "Theorems and proofs are correct", P + "L02.html:72-131", "PASS", C6 + "L02 :72-131 unchanged.")
R("E5a-L02-lab-claims", "Sentences about what the lab prints and checks match code and output", P + "L02.html:137, :138-247, :262, :51", "PASS",
  C6 + "cited lines unchanged; the L02 twin output printed this round matches the page statements (residual identity True; capital share and labour share lines; residual depends on alpha True).")
R("E5a-L02-simulated-label", "Lab labelled SIMULATED where it is generated; honest-pending note accurate", P + "L02.html:51, :133, :137, :138-141, :494", "PASS",
  C6 + "cited lines unchanged; the twin's docstring says SIMULATED and the run this round prints 'SIMULATED economy: seed 2026'.")
R("E5a-L02-table-row-simple-growth", "Key-results rows match the page", P + "L02.html:405-408", "PASS", C6 + "unchanged.")
R("E5a-L03-numbers", "Prose numbers match unrounded values and lab output", P + "L03.html:52, :116, :147, :161-187, :383, :402-410, :430-500", "PASS",
  "Re-verified this round by hand and against the printed twin output: k* = (10/3)^(10/7) = 5.5843115042 (Part A); output per worker 1.6752934513; dk/ds = k*/(0.7 x 0.2) = 39.8879393156; dk/ddelta = -k*/(0.7 x 0.06) = -132.9597977186; elasticity 10/7 = 1.4285714286; first period gap below 1e-12 is 692 (printed line); Part C 27 below and 23 above (grid i/5, i = 1..50, k* = 5.584 lies between 27/5 and 28/5); M1 k* = 6.25, y* = 2.5, c* = 1.875; M2 k1 = 1.15, k2 = 1.3030951324; M3 derivatives 50 and -125; E1 ratio 0.1217 (0.122); E2 change 0.3988793932, 7.14 percent; E3 change -0.1329597977.")
R("E5a-L03-theorems", "Theorems, propositions and proofs are correct", P + "L03.html:70-187, 184-187, 527-531", "PASS",
  C6 + "cited ranges unchanged (the delta in L03 is line 611 only). Proof of Prop 4.2 re-derived: H_k = -(1-alpha)(n+delta) at k*; dk*/ds = -H_s/H_k = k*/((1-alpha)s).")
R("E5a-L03-lab-claims", "Sentences about what the lab prints and checks match code and output", P + "L03.html:52, :192, :376-381, :383", "PASS",
  C6 + "cited lines unchanged; Parts A to E match the twin's printed lines.")
R("E5a-r5-L03-misconceptions", "Misconceptions and their numbers", P + "L03.html:399-411", "PASS", C6 + "unchanged; 39.8879393156 and -132.9597977186 re-derived above.")
R("E5a-r5-L03-R1-solution", "R1 solution is correct and states the right step", P + "L03.html:497-500", "PASS", C6 + "unchanged.")
R("E5a-r5-L03-remark-4.3", "Remark 4.3 elasticity", P + "L03.html:187", "PASS", C6 + "unchanged; 1/(1-0.3) = 10/7.")
R("E5a-r5-L01-R2-cards", "Cards that restate L01 propositions match the lesson", P + "cards.json:88, :104 (E5-c014, E5-c016)", "PASS", C6L1 + "cards.json:88 and :104 are not in the delta.")
R("E5a-r5-cards-L01-L03", "Cards agree with the current lesson text and carry the hypotheses", P + "cards.json E5-c001 to E5-c052", "PASS",
  C6 + "the delta in cards.json (E5-c065, c068, c091-c101) is outside E5-c001 to E5-c052.")
R("E5a-r5-cards-numbers-in-lessons", "Every card number appears in its lesson", P + "cards.json E5-c019..c052", "PASS", C6 + "unchanged; L03 numbers re-checked above.")
R("E5a-r5-DAG-concept-links", "Concept links and DAG closure", P + "index.html; L01-L03 data-concept links", "PASS",
  "check_dag E5 PASS this round. Concept links in index.html:33-35, :60-65 unchanged; no new data-concept links in the delta.")
R("E5a-r7-delta-read", "Round-7 delta read hunk by hunk", "index.html:33, :147-151; L02.html:368; L03.html:611; cards.json (outside slice)", "PASS",
  "git diff 9fd6aed 0d2d0f3 read for every slice file: index.html (lines 33, 150, 151 changed; 37, 60 unchanged), L02.html (line 368 only), L03.html (line 611 only), L01.html and the three slice twins unchanged. cards.json changes are E5-c065, c068 (L04) and c091-c101 (L06): none is in L01-L03. The L05 twin and L04/L05/L06/L07 pages changed outside this slice and are not graded here.")
R("E5a-r7-hub-card-bodies", "Hub card bodies agree with the lessons they describe", P + "index.html:150, :151", "PASS",
  "L05 card 'A linear aggregate-demand curve taken as the model's specification' matches L05 Assumption A1 (aggregate demand is linear in the price level, L05.html:59) and Remark 1.2 (L05.html:79). L06 card 'the unemployment rate at which inflation does not change under adaptive expectations' matches Assumption A3 (L06.html:73) and Corollary 3.2 (L06.html:278): inflation changes by -beta(u - u^n), so it is unchanged exactly at u = u^n.")
R("E5a-r6-hub-lede-static-claim", "Hub lede claims about the model's dynamics are accurate", P + "index.html:33", "FAIL",
  "The round-6 defect (no adaptive-expectations path in the static claim) is fixed: the carve-out now names 'the adaptive-expectations path of Lesson 6', and L06 has a 12-period adaptive-expectations path (L06.html:127, :183, :234). But the same sentence still says the module 'states the static models that a policy discussion uses: the Solow growth model, ... the Phillips curve with its natural rate', i.e. it classes the Solow recursion (L03 Definition 1.1, k_{t+1} = g(k_t)) and the Phillips curve (L06, pi_t depends on pi_(t-1)) as static, and then says the module is static except for those same two. The lede contradicts itself.")
R("E5a-r6-L03-refs-all-T", "Grade claims in the references paragraph are accurate", P + "L03.html:611", "FAIL",
  "The round-6 defect is fixed: L03.html:611 now grades lab-printed values C ('The values that Lab 1 prints ... are graded C and name the lab'), which matches the grade legend (L03.html:47). New defect in the same sentence: 'the first-period gap count of 692' is wrong. 692 is the first period index at which the gap falls below 1e-12 (L03.html:364, :383, :572), not a count of gaps. Fix: replace 'the first-period gap count of 692' with 'the first period at which the gap is below 1e-12 (692)'.")
R("E5a-r7-L02-E3-instruction", "Exercise instruction matches the solution's inputs", P + "L02.html:366-368 (E3, 'Using only the printed average capital term')", "FAIL",
  "The exercise says 'Using only the printed average capital term, compute ... at alpha = 0.4', but its solution's headline value 0.014222 is obtained from the unrounded average 0.0355562, which the lab does not print (the solution says so). From the printed value alone the answer is 0.4 x 0.035557 = 0.014223, which the same solution calls a rounding artifact. The question is therefore not answerable 'using only the printed' value to the stated 6-decimal answer. Fix: change the instruction to 'Using the printed average capital term, and stating the rounding basis, compute ...' and give both values (0.014223 from printed values; 0.014222 from the unrounded average), or drop the word 'only'.")

summary = ("E5-a round 7 at 0d2d0f3: FAIL. Three non-PASS rows. (1) E5a-r6-hub-lede-static-claim (index.html:33): the L06 carve-out is fixed, "
  "but the same sentence still lists Solow and the Phillips curve as static models and then says the module is static except for them. "
  "(2) E5a-r6-L03-refs-all-T (L03.html:611): the lab-value grade is now C (fixed), but 'first-period gap count of 692' misdescribes the period index 692. "
  "(3) E5a-r7-L02-E3-instruction (L02.html:366-368): 'Using only the printed average capital term' is answered with an unprinted unrounded value. "
  "The round-6 L02 numeric FAIL (0.014223 vs 0.014222) is fixed and re-verified. All commands pass.")

frag = {
 "unit": "E5", "slice": "a", "round": 7,
 "verifier": "Haiku independent verifier, E5-a round 7 (did not build E5)",
 "pin": "0d2d0f3",
 "base": "9fd6aed (round-6 pin); delta in slice: index.html lines 33, 150, 151; L02.html line 368; L03.html line 611; cards.json outside L01-L03 only",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyC7-E5-a (detached at 0d2d0f3, .venv symlinked)",
 "scratch": "/tmp",
 "verified_at": "2026-10-29",
 "verdict": "FAIL",
 "rows": rows,
 "mutants": [],
 "registry_flags": ["references/ and tools/ unchanged in 9fd6aed..0d2d0f3; verify_refs --offline: 560 entries, 0 problems (run this round)."],
 "freshness_flags": [
   "Outside slice a (noted, not graded here): course/modules/E/E5/project.html:343 cites plans/E5-open-items.md in learner text, a process reference; belongs to the project slice (b/c)."
 ],
 "notes": "Slice: index.html, L01.html, L02.html, L03.html and the twins tests/labs/E5/lab-E5-L01-1.py, lab-E5-L02-1.py, lab-E5-L03-1.py. Read this round in full: index.html (1-188), L03.html (1-624), and the changed hunks of L02.html (the E3 solution, :355-372) and L03.html :608-612. L01.html is byte-identical to 9fd6aed and was carried by rule with a prefix. Rows that cite lines unchanged in the delta were carried with the prefix; rows touching a changed line were re-verified. Mutants: none; lessons carry no project graders and lab twins are demonstrations under the rulings. Commands run at 0d2d0f3: check_pages --unit E5 (PASS, and per page L01/L02/L03 PASS; --page index is not a valid hub selector); check_dag E5 PASS; check_projects E5 PASS; run_labs E5 per page PASS; page_smoke index L01-L03 PASS; twins under python -I -W error exit 0; ruff check and format --check on tests/labs/E5 PASS; mypy --no-incremental tests/labs/E5 PASS; pytest -q -k E5 12 passed; verify_refs --offline 560 entries, 0 problems. Could not check: the full pytest suite and the full gate (only the E5 slice and its commands); L04-L08, project.html and their cards (other slices); the rendered browser view; prose beyond the checked lines of L01 (carried). Not read in full this round: L01.html and the twin code bodies beyond the carried reasoning.",
 "summary": summary,
}
out = "ledgers/E5/E5-a.json"
json.dump(frag, open(out, "w"), indent=1, ensure_ascii=False)
print("rows", len(rows), "non-pass", [r["id"] for r in rows if r["status"] != "PASS"])
