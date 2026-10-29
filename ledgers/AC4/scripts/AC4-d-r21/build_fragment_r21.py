import json, re, sys
ROOT = "/tmp/verify21-AC4-d"
S = f"{ROOT}/ledgers/AC4/scripts/AC4-d-r21"
prev = json.load(open("/tmp/fanout-frags/AC4-d.round20.json"))
prev_rows = {r["id"]: r for r in prev["rows"]}
CARRY = "Carried from round 20 (cited passage byte-identical since the previous pin fd9a9b7; the round-21 delta touches only L07 lines 134, 378 and 420-421 and L08 lines 63 and 291 of the lesson pages): "
CARRY_TWIN = "Carried from round 20 (tests/labs/AC4 twins and their embedded blocks byte-identical since fd9a9b7, git diff --stat empty): "
CARRY_CMD = "Carried from round 20 (cited project-grader and lab files byte-identical since fd9a9b7, git diff --stat empty): "

fresh = {}   # id -> (status, evidence, fix)
def F(id_, status, ev, fix=None):
    fresh[id_] = (status, ev, fix)

# ---- command rows, re-run this round
F("AC4-d-cmd-pin", "PASS", "git rev-parse --short HEAD prints f95243f; git symbolic-ref -q HEAD prints nothing (detached); git status shows only untracked .venv.")
F("AC4-d-r6-delta-coverage", "PASS", "git diff --stat fd9a9b7 f95243f for course/modules/AC/AC4/*, tests/labs/AC4/*, cards.json: L07.html (4 hunks: lines 134, 378, 420-421 and the two table rows), L08.html (2 hunks: lines 63, 291), cards.json (3 hunks: c007 and c020 are L01/L02 and outside this slice; c089 and c095 are in this slice), index.html (1 line: the hub objective 'compare ... on two SIMULATED products', outside this slice), tests/labs/AC4 unchanged. Every hunk read in full context.")
F("AC4-d-cmd-run_labs", "PASS", "tools/run_labs.py --unit AC4 (exit 0): 'run_labs AC4: PASS (10/10)' in " + S + "/run_labs.out.")
F("AC4-d-cmd-twin-isolated", "PASS", "python -I -W error tests/labs/AC4/lab-AC4-L07-1.py and lab-AC4-L08-1.py: exit 0, empty stderr. Python extracted embedded <pre class=expected> of each page and compared with the run: L07 True, L08 True (" + S + "/twin_L0*.out).")
F("AC4-d-cmd-page_smoke", "PASS", "tools/page_smoke.py --unit AC4 --pages L07 L08: 'page_smoke modules/AC/AC4/L07.html: PASS', 'page_smoke modules/AC/AC4/L08.html: PASS', 'page_smoke AC4: PASS' (" + S + "/page_smoke.out).")
F("AC4-d-cmd-check_pages", "PASS", "tools/check_pages.py --all (exit 0): 'check_pages AC4: PASS' (" + S + "/check_pages.out).")
F("AC4-d-cmd-check_dag", "PASS", "tools/check_dag.py --all (exit 0): 'check_dag AC4: PASS' (" + S + "/check_dag.out).")
F("AC4-d-cmd-check_projects", "PASS", "tools/check_projects.py --all (exit 0): 'check_projects AC4: PASS' (" + S + "/check_projects.out).")
F("AC4-d-cmd-lint-mypy", "PASS", "ruff check tests/labs/AC4/: 'All checks passed!'; ruff format --check tests/labs/AC4/: '10 files already formatted'; mypy --no-incremental on lab-AC4-L07-1.py and lab-AC4-L08-1.py: 'Success: no issues found in 2 source files' (" + S + "/ruff_check.out, mypy_twins.out).")
F("AC4-d-cmd-pytest", "PASS", "pytest -q -k 'AC4 or ac4' tests/test_labs.py tests/test_page_smoke.py tests/test_page_checks.py: exit 0, 10 dots; collect-only on tests/test_labs.py -k 'AC4 or ac4' gives 10 tests (" + S + "/pytest_ac4.out, collect.out).")
F("AC4-d-cmd-verify_refs", "PASS", "tools/verify_refs.py --unit AC4: 'live re-verification of AC4: 2 of 560 entries, 0 problems' (exit 0); tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' (" + S + "/vr_live.out, vr_offline.out). The pages cite no registry key, so the check is the unit-level one.")
F("AC4-d-r17-cmd-embed", "PASS", "Embedded <pre class=expected> of L07.html and L08.html compared with the fresh run of each twin (exact string after html.unescape and strip): both True (" + S + "/twin_L0*.out and the Python comparison in the twin-isolated row).")
# ---- numbers and grades on changed spans
F("AC4-d-2.2-numbers-L07", "PASS", "L07.html §4 line 134 (changed), §4 worked case (lines 126-134), §5 (327), interpretation (322), M1, M2, M3, P2 numbers: recomputed by " + S + "/recompute_r21.py (exact Fractions): D=3000, t_min=52, Sigma=140000, dS(52)=0, dB(52)=140000, dS(46)=-30000; K=12000: D=1000, t_min=44, Sigma=180000; M3 r=50: t_min 52 > 50, Sigma=-10000; misconception 2: D=0, t_min=40, dB(60)=-10000, Sigma=30000. Lab 1 counts re-derived from the seeded generator: over 14, fits 187, empty 75, feasible 112, binding 73; 73/112=0.6518, 75/187=0.4011 (both displayed correctly).")
F("AC4-d-2.2-numbers-L08", "PASS", "L08.html §4 (lines 115-122), §5 (128), §6 (296-298), §7 (303), §8 (318-319), M3 (lines 333-337), E1 (358), Lab 1 table and interpretation (291): recomputed in " + S + "/recompute_r21.py: RI 30, EVA 6, Lemma 8.2 check -24=-0.20*120; capitalized dRI 72.8 (RI 102.8), dEVA 56.8 (EVA 62.8); M3 RI 66.4, EVA 34.4, dRI 36.4, dEVA 28.4; 4/28 = 0.1429. Lab printed values 7280 and 5680 cents equal 72.80 and 56.80 SCU.")
F("AC4-d-2.3-grades-L07", "PASS", "L07.html §9 key-results table (lines 417-425) after the round-21 edits: every T row is a theorem (Lemma 7.2, Theorem 7.3 parts 2 and 3, P1), a hand computation on stated inputs (§4, M2), or P2 (grade T, scope issue recorded in AC4-d-r21-P2-scope-q-le-K); every C row names Lab 1 and an output line that exists (counts line, binding line, four check lines). The changed row 2 cites P1 for every t and Theorem 7.3 part 3 for t in the range, both correct.")
F("AC4-d-2.3-grades-L08", "PASS", CARRY + "L08.html §10 key-results table (lines 390-396): T rows are Lemma 8.2, Lemma 8.3, Proposition 8.4, P3 and the §4 arithmetic; C rows name Lab 1 identity, sign and pair-count lines.")
F("AC4-d-2.5-lab-L08", "PASS", "L08.html Lab 1 hypothesis (line 134) and interpretation (line 291, changed): the interpretation sentence now says §4 applies Proposition 8.4 to a change of 80 SCU in OI and base on a different division and gets 72.8 and 56.8 SCU. Checked: §4 uses the hand-built division C=1,000, OI=120 (different from SIM-A); the lab prints 7280 and 5680 cents, i.e. 72.80 and 56.80 SCU; the lab does not evaluate the Proposition 8.4 formula (main() computes RI and EVA directly and prints the differences).")
F("AC4-d-r17-indep-recompute", "PASS", "Own recompute " + S + "/recompute_r21.py of the generator-based counts (14, 75, 112, 73, boundary surplus 0) and of the L08 table lines matches the printed output; earlier independent transcription AC4-d-r20 carried for the seed-based claims.")
F("AC4-d-r20-indep-recompute", "PASS", "Re-run this round: " + S + "/recompute_r21.py reproduces L07 counts 14/75/112/73, boundary t_min=t_max=5200 cents and surplus 0, and the L08 capitalization figures.")
F("AC4-d-2.9-hours", "PASS", "L01 6, L02 7, L03 6, L04 6, L05 7, L06 6, L07 6 (data-hours, line 2), L08 6: sum 50 = index.html data-hours-lessons=\"50\" (line 29). data-hours-project=\"20\". Hub data-hours values unchanged by the delta (only the objective text on the hub changed).")
F("AC4-d-2.8-data", "PASS", "grep -c data-files on L07.html and L08.html: 0 and 0 (re-run this round).")
F("AC4-d-2.9-prose-banned", "PASS", "Grep of both pages' learner text for roughly, 'about <digit>', historically, typically, usually, ellipses (... and the ellipsis character), generally, builder, verifier, round, build, REQUEST and unit report: no hit in learner prose. The only hit is 'often' in L07 line 408 ('more often'), an ordinary word that is not on the banned list; no banned phrase occurs.")
F("AC4-d-r17-process-words", "PASS", "Same grep as AC4-d-2.9-prose-banned for build, builder, round, verifier, REQUEST, unit report: zero hits in learner text of L07.html and L08.html (the word 'round' does not occur in either page's learner prose).")
F("AC4-d-r20-scope-words", "PASS", "Fresh grep of learner text for only, all, every, always, exactly, same, none, drives, offsets, raises, any (" + S + "/ and the output in this row's run): each changed sentence checked: L07 line 134 ('when capacity binds... because D falls as K rises (§2)'; computed in recompute_r21.py), L08 line 63 ('does not say where a reader obtains them'; no 'obtain' or 'read from' sentence on the page), L08 line 291, key-results row 2 ('for every price', P1 and Theorem 7.3 part 3 as cited), P2 statement (scope issue recorded separately).")
F("AC4-d-r3-L07-cards-c117", "PASS", CARRY + "cards.json c117 (K=12000 gives D=1000 and t_min=44): matches M2 (line 361) and §4 (line 134, the changed sentence keeps the same numbers).")
# ---- structure and lab twins
F("AC4-d-r17-cmd-mutate_graders", "PASS", CARRY_CMD + "round-20 run of tools/mutate_graders.py --unit AC4 (project grader, outside this slice): 'mutate_graders AC4: PASS (139/139 killed)' (ledgers/AC4/scripts/AC4-d-r20/mutate_graders_r20.out). Project files unchanged since fd9a9b7 (git diff --stat empty for course/modules/AC/AC4/project.html and grader).")
F("AC4-d-r17-mutants-killed", "PASS", "Fresh transplant of every one-line lab mutant (ledgers/AC4/mutants/AC4-d-r17, -r18, -r19: " + S + "/transplant_r21.out): 30 KILLED output-differs; the r18 L08_n07 mutant rebased by hand onto the current twin is also killed (8/9 sign line, " + S + "/L08_n07_rebased_on_current_twin.py); the not-transplantable files (target line absent from the current twin) are the superseded del_*, boundary, n03, n07, n08, n10, n11, n12 and the r17 m02 and m03 files, listed in AC4-d-r20-superseded-mutants. Survivors: r17_L08_m04 and L08_n09 (equivalent, see AC4-d-r20-equivalent-survivors).")
F("AC4-d-r18-mutants-run", "PASS", "Fresh transplant re-run (" + S + "/transplant_r21.out) of the r18 files: n01, n02, n04, n05, n06 and L08_n01..n06, n08 KILLED; L08_n07 KILLED after rebasing (see AC4-d-r17-mutants-killed); the others not transplantable (superseded).")
F("AC4-d-r18-L08-mutants-killed", "PASS", "L08_n01 to L08_n08 each killed: n01 to n06 and n08 by output difference in the fresh transplant; n07 killed after rebasing its one changed line onto the current twin (sign line prints 8/9, not 9/9): " + S + "/L08_n07_rebased_on_current_twin.py and its output.")
F("AC4-d-r19-mutants-rerun", "PASS", "All r17, r18, r19 mutant files re-run this round through the transplant (" + S + "/transplant_r21.out): 30 KILLED; the r17, r18 superseded and not-transplantable ones are as recorded in AC4-d-r20-superseded-mutants.")
F("AC4-d-r19-m19-new-mutants", "PASS", "ledgers/AC4/mutants/AC4-d-r19/m19_*.py: m19_L07_firm_surplus_uses_buyer_ceiling_price, m19_L07_t_min_divides_by_capacity, m19_L08_first_year_charge_over_life_plus_one, m19_L08_residual_income_after_tax: all four KILLED (output differs) in the fresh transplant.")
F("AC4-d-r20-new-mutants", "PASS", "ledgers/AC4/mutants/AC4-d-r20: m20_L07_displaced_forgets_internal_order KILLED (output differs); m20_L07_sign_check_strict_at_zero KILLED (output differs); m20_L08_eva_taxes_residual_income KILLED on a direct run against the current twin (output differs: the EVA line changes); m20_L07_midpoint_check_uses_lower_end SURVIVES (see AC4-d-r20-lab-midpoint-survivor).")
F("AC4-d-r20-equivalent-survivors", "PASS", "r17_L08_m04_discord_ignores_ties and L08_n09_discord_pairs_same_name_order both survive the fresh transplant (" + S + "/transplant_r21.out) and are output-equivalent on the shipped seed: 0 ties in either measure among 28 pairs and the self-pair contributes zero differences (" + "ledgers/AC4/scripts/AC4-d-r20/ties_and_equiv_r20.out).")
F("AC4-d-r20-lab-midpoint-survivor", "PASS", "m20_L07_midpoint_check_uses_lower_end replaces the midpoint by t_min in the lab. Fresh run (" + S + "/transplant_r20_rerun.out): output identical, exit 0, so the mutant survives. The shipped lab checks the midpoint (tests/labs/AC4/lab-AC4-L07-1.py midpoint() and the sum loop over (t_min, t_max, midpoint)). Under the architect ruling (lab twins are demonstrations; a survivor is not a finding unless the lesson claims a property the shipped lab does not have) this is PASS, and it is flagged for the orchestrator because L07 line 140 claims the sum identity is checked 'at both ends and at the midpoint'.")
F("AC4-d-r20-superseded-mutants", "PASS", CARRY_TWIN + "targets absent from the current twin (no assert statement exists in tests/labs/AC4/lab-AC4-L07-1.py; r17 m02/m03 and r18 n03, n07, n08, n10-n12 transplant as not-applicable). Recorded in " + S + "/transplant_r21.out.")
F("AC4-d-r17-alternatives", "PASS", CARRY_TWIN + "alternative correct implementations in ledgers/AC4/scripts/AC4-d-r19/alts and AC4-d-r20/alts (seven files) were run in round 20 and exit 0 with the embedded output; the twins they test are unchanged.")
F("AC4-d-r19-alts", "PASS", CARRY_TWIN + "the four round-19 alternatives (ledgers/AC4/scripts/AC4-d-r19/alts) were re-run in round 20 and matched the embedded output; the twins are unchanged.")
F("AC4-d-r20-alts", "PASS", CARRY_TWIN + "the three round-20 alternatives (ledgers/AC4/scripts/AC4-d-r20/alts) were re-run in round 20 and matched the embedded output; the twins are unchanged.")
F("AC4-d-r17-mutant-L08-m04-ties", "PASS", CARRY_TWIN + "equivalent on the shipped seed (0 ties among 28 pairs).")
F("AC4-d-r18-equiv-L08-n09", "PASS", CARRY_TWIN + "self pairs contribute zero differences in both measures; a self pair is excluded by ties, so the output is unchanged on the shipped seed.")
F("AC4-d-r20-delta-hunk-check", "PASS", "git diff fd9a9b7 f95243f for L07.html (4 hunks) and L08.html (2 hunks) and cards.json c089 and c095: every hunk read in full context. The hunk-level findings are separate rows: L07 line 134 (AC4-d-L07-extra-capacity-scope, PASS), L07 P2 and table row 4 (AC4-d-r21-P2-scope-q-le-K, FAIL), L07 table row 2 (AC4-d-r21-L07-table-row2-every-price, PASS), L08 lines 63 and 291 (AC4-d-r21-L08-line63-sourcing and AC4-d-2.5-lab-L08, PASS), c089 (AC4-d-r20-card-c089-theorem-scope, PASS), c095 (AC4-d-r19-cards-c095-basis, PASS), c093 (AC4-d-r21-c093-hypothesis, FAIL).")
# ---- L07 / L08 lesson sentences
F("AC4-d-L07-extra-capacity-scope", "PASS", "L07.html line 134 (changed): 'When capacity binds (D > 0) and p_m > v, extra capacity lowers the supplier's floor and raises the surplus, because D falls as K rises (§2) and both t_min and Sigma depend on D through D(p_m - v); when D = 0, it changes neither. The buyer's ceiling r = 80 does not move.' Checked: D = max(0, q+E-K) falls as K rises (§2 line 76-86); t_min = v + D(p_m-v)/q and Sigma = q(r-v) - D(p_m-v) both depend on D through D(p_m-v) (Lemma 7.2, §3); with D > 0 and p_m > v the derivative of D in K is -1, so t_min falls and Sigma rises; with D = 0, K changes nothing; t_max = r has no K. Numbers K=12000 gives D=1000, t_min=44, Sigma=180000 (recompute_r21.py). Wording 'extra capacity' is limited to the binding case by the same sentence.")
F("AC4-d-2.5-lab-L07", "PASS", CARRY_TWIN + "Lab 1 hypothesis (line 140), §4 lead-in (line 136), interpretation (line 322): the hypothesis matches the twin (supplier-gain zero at t_min, nonempty iff Sigma >= 0, both at the boundary pair, sum identity at both ends and midpoint). Twin unchanged since fd9a9b7.")
F("AC4-d-r18-L07-checks-not-in-output", "PASS", CARRY_TWIN + "the four check lines are printed from computed counts (supplier_zero, sign_match, midpoint_inside, sum_identity), confirmed in the fresh run (" + S + "/twin_L07.out).")
F("AC4-d-r20-L07-hunk-P3", "PASS", CARRY + "L07.html P3 (lines 379-380): statement 'Suppose v = 0 and q <= K' and the solution are unchanged.")
F("AC4-d-r20-L07-hunk-line322", "PASS", CARRY + "L07.html line 322 interpretation, unchanged.")
F("AC4-d-r20-L07-hunk-line65", "PASS", CARRY + "L07.html line 65, unchanged.")
F("AC4-d-r20-L07-hunk-line347", "PASS", CARRY + "L07.html line 347, unchanged.")
F("AC4-d-r20-L08-line52", "PASS", CARRY + "L08.html line 52 (why-it-matters), unchanged.")
F("AC4-d-r20-card-c089-theorem-scope", "PASS", "cards.json c089 back (changed) now: 'The two gains sum to the firm-wide surplus for every price: Delta_S(t) + Delta_B(t) = Sigma (Section 3 and P1; Theorem 7.3, part 3 states it for t in the range).' Checked against L07.html §3 (line 104: 'Adding the two gains removes the price'; the identity holds for every t) and P1 (line 370-372: 'the sum is Sigma for every t'), and §7 misconception 3 (line 347). Theorem 7.3 part 3 (line 116) is for t in the range, as stated. PASS.")
F("AC4-d-r19-cards-c095-basis", "PASS", "cards.json c095 basis (line 674, changed) now reads 'Lab 1 (SIMULATED), output lines for the counts and the four check lines'. The lab prints four check lines: 'supplier gain is zero at t_min', 'range is nonempty exactly when ...', 'midpoint of the range lies inside it', 'gains sum to the surplus at both ends and the midpoint' (twin_L07.out). PASS.")
F("AC4-d-r17-cards-scope-ok", "PASS", "c082 (lesson §1 definition: 'a fact that Section 3 proves' matches §3), c095 (basis now names the four check lines: PASS) and c108 (two identity lines of Lab 1: 8/8 and 9/9 printed) agree with the current lesson and output.")
F("AC4-d-2.7-cards-L07-L08", "PASS", "Re-checked every L07 and L08 card (35 cards, c082-c134) against the current lesson text: cards.json cards printed in " + S + "/cards_L07_L08.txt. Previously failing cards c089 and c095 now agree (see their rows). The new failing card c093 is recorded in AC4-d-r21-c093-hypothesis, not here.")
F("AC4-d-r17-cards-scope", "FAIL", "Every L07 and L08 card re-read against the current lesson text this round (" + S + "/cards_L07_L08.txt). c082, c089, c095, c108 and the rest agree; c093 does not: its back states 'Since E <= K and p_m >= v, the floor t_min is at most p_m (Problem P2)', but P2 now requires q > 0 (and, for the lowest-price claim to refer to t_min as defined in Lemma 7.2, q <= K). See AC4-d-r21-c093-hypothesis.", "Add the hypotheses that P2 states to card AC4-c093 once P2 is corrected (AC4-d-r21-P2-scope-q-le-K).")
F("AC4-d-r17-cards-cover", "PASS", "cards_scan_r21: " + S + "/cards_scan_r21.out: 134 cards; no duplicate id, front or back; 35 cards for L07 (c082-c096, c117) and L08 (c097-c109, c113-c116, c129, c134) (run as the cover check).")
F("AC4-d-r6-cards-dup-scan", "PASS", "cards_scan_r21.out: cards 134, dup id [], dup front [], dup back [].")
F("AC4-d-2.1-citations-L07-L08", "PASS", "L07.html References (line 507-510) and L08.html References (line 480-482) state that the page cites no registry source; neither page contains a citation key. verify_refs live AC4 and offline runs (AC4-d-cmd-verify_refs) PASS.")
F("AC4-d-2.7-cards-c088-outside-option", "PASS", CARRY + "c088 back and §7 misconception 2 (line 345, unchanged): v=40, p_m=60, K=10000, E=8000, q=2000, r=55: D=0, t_min=40; buyer gain -10000; Sigma 30000 (recompute_r21.py).")
F("AC4-d-r3-L08-cards-c113-c116", "PASS", CARRY + "c113-c116 match §4 (72.8, 30 to 102.8, 56.8, 6 to 62.8: recompute_r21.py) and Lab 1 rows (SIM-A, SIM-D, SIM-G).")
F("AC4-d-L08-why-capital-charge-rate", "PASS", "L08.html why-it-matters (line 52, unchanged since fd9a9b7) and the §1 input paragraph (line 63, changed) agree: both say the rates are inputs and the lesson derives neither.")
F("AC4-d-r21-P2-scope-q-le-K", "FAIL", "L07.html P2 (line 378, changed): 'Using q > 0, E <= K and p_m >= v, prove that t_min <= p_m.' and key-results row 4 (line 421, changed): 'The lowest price never exceeds p_m, when q > 0, E <= K and p_m >= v'. The round-20 text was 'Using E <= K, q <= K and p_m >= v'. The q <= K hypothesis was removed, but t_min is defined only in Lemma 7.2 (lines 90-96) under 'Let q > 0 and q <= K', and §2 (line 76) states 'Assume q <= K. If it is not, no transfer is possible', so the displaced-unit count D = max(0, q+E-K) and t_min have no meaning on this page for q > K. The algebra of P2 is valid for the formula (checked: D <= q whenever E <= K over a grid including q > K, recompute_r21.out), so the defect is the scope: the claim is stated for inputs where the object it bounds is not defined by the lesson.", "Restore 'q <= K' to the P2 statement (line 378) and to key-results row 4 (line 421), so they match Lemma 7.2; add the same hypothesis to card AC4-c093 (AC4-d-r21-c093-hypothesis).")
F("AC4-d-r21-c093-hypothesis", "FAIL", "cards.json AC4-c093 back: 'No. Since E <= K and p_m >= v, the floor t_min is at most p_m (Problem P2).' It omits q > 0 (which P2 states and which the division in P2's proof needs) and, like P2, omits q <= K, the hypothesis of Lemma 7.2 under which t_min is defined. The card therefore states a T result with fewer hypotheses than the lesson gives it.", "Change the back to: 'No. Since q > 0, q <= K, E <= K and p_m >= v, the floor t_min is at most p_m (Problem P2, after the fix to P2).'")
F("AC4-d-r21-L07-table-row2-every-price", "PASS", "L07.html key-results row 2 (line 420, changed): 'The sum of the two gains is the firm-wide surplus Sigma, for every price | T | P1 (every t); Theorem 7.3 part 3 states it for t in the range'. Checked against P1 (line 370-372: the sum is Sigma for every t, the terms in t cancel) and Theorem 7.3 part 3 (line 116, 'for every t in the range'). The row now attributes the every-t claim to P1, which is correct.")
F("AC4-d-r21-L08-line63-sourcing", "PASS", "L08.html line 63 (changed): 'The page takes operating income and the capital base as given numbers, on the base the reader chooses, and does not say where a reader obtains them.' Checked by grep on the page: no sentence says where OI or C is obtained ('obtain', 'read from', 'is read' absent; the balance sheet appears only in the Uses meta row, line 38, and as a distractor in quiz L08q9). The negative claim is true of the page as shipped. PASS.")
F("AC4-d-L08-tau-zero-scope", "PASS", CARRY + "L08.html §3 line 109, unchanged: dRI - dEVA = tau*dOI, equal iff tau = 0 or dOI = 0.")
F("AC4-d-L08-base-sign-scope", "PASS", CARRY + "L08.html §7 line 303, unchanged: OI=120, r=9%: C=1000 gives RI 30; C=1400 gives RI -6 (recompute_r21.py: 120 - 0.09*1400 = -6).")
F("AC4-d-L08-misconception1-C-positive", "PASS", CARRY + "L08.html §8 misconception 1 (line 314), unchanged.")
F("AC4-d-L08-size-claim", "PASS", CARRY + "L08.html §8 misconception 3 (lines 318-319) and card c102: unchanged. Recomputed: RI = OI - rC for SIM-D (7030 - 0.09*124000 = -4130) and SIM-A (2870 - 0.09*59000 = -2440).")
F("AC4-d-L08-quiz-agreement-claim", "PASS", CARRY + "L08.html quiz L08q5 explanation (quiz, lines 434-440), unchanged.")
F("AC4-d-L08-E1-seed-claim", "PASS", CARRY_TWIN + "E1 (line 358) seed claim: seed scan (AC4-d-r20 seed_scan_r20.out) for seeds 1 to 40 unchanged; generator lab unchanged.")
F("AC4-d-2.2-numbers-L07-E1-seed", "PASS", CARRY_TWIN + "E1 (line 387) seed claim, seeds 1 to 40 (AC4-d-r20 seed_scan_r20.out); the generator is unchanged.")
F("AC4-d-r19-seed-scan", "PASS", CARRY_TWIN + "ledgers/AC4/scripts/AC4-d-r20/seed_scan_r20.py and seed_scan_r20.out (seeds 1 to 40 from the twins' own generators).")
F("AC4-d-r18-L07-E1-wording", "PASS", CARRY + "L07.html E1 solution (line 387): '75/187 = 0.4011' (recomputed this round), 'the boundary pair is not empty' (t_min = t_max, so nonempty).")
F("AC4-d-r2-L08-lab-pair-scope", "PASS", CARRY + "L08.html §5 paragraph (line 130) 'the orders agree' and the pair-count scope (28 pairs, ties not counted: code 'and by_ri != 0 and by_ratio != 0'), unchanged apart from the lines verified this round.")
F("AC4-d-r3-L08-why-and-s3-s5-text", "PASS", CARRY + "L08.html why-it-matters (line 52), §1 OI/C paragraph (line 78), §3 (lines 98-109), §5 (lines 126-130): unchanged; every term named.")
F("AC4-d-r3-L07-s1-s5-s6-text", "PASS", CARRY + "L07.html §1 (line 70), §5 (line 327), §6 bullets (332-335): unchanged; 201=200+1, 14 with q>K, 187=75+112, 73/112=0.6518 recomputed.")
F("AC4-d-r19-L08-period-convention", "PASS", CARRY + "L08.html §3 line 98 and the §4 worked capitalization (lines 115-122): unchanged.")
F("AC4-d-r18-L08-section3-later-periods", "PASS", CARRY + "L08.html §3 line 98 and §4 (lines 117-122): unchanged.")
F("AC4-d-r18-L08-section7-tax-effect", "PASS", CARRY_TWIN + "L08.html §7 bullet 'Tax and book treatment' (line 306) and the lab's capitalized() docstring: unchanged; the lab applies TAX_BP to the changed OI and models no book/tax difference.")
F("AC4-d-r18-L07-midpoint-test-point", "PASS", CARRY_TWIN + "lab midpoint (lines 222-224) and sum identity at (t_min, t_max, midpoint) (lines 289-296): unchanged; output line 'gains sum ... at both ends and the midpoint' printed from the computed count.")
F("AC4-d-r18-L07-boundary-both-strict", "PASS", CARRY_TWIN + "nonempty (lines 218-219) and sign line are non-strict at equality; boundary printed nonempty True.")
F("AC4-d-r17-boundary-L07", "PASS", CARRY_TWIN + "BOUNDARY (v=4000, p_m=6000, K=10000, E=8000, q=5000, r_net=5200): t_min=t_max=5200, surplus 0 (recompute_r21.py).")
F("AC4-d-r17-boundary-L08", "PASS", CARRY_TWIN + "BOUNDARY = Division(C=1000, OI=90): OI/C = 9% = r, RI = 0; included in sign_ok; printed 'RI >= 0 True'.")
F("AC4-d-r17-boundary-probe", "PASS", CARRY_TWIN + "equality scan (AC4-d-r20 equality_scan_r20.py, .out) unchanged.")
F("AC4-d-L07-misconception2-market-price", "PASS", CARRY + "L07.html §7 misconception 2 (line 345) and L07q7 explanation (line 480): v=40, p_m=60, K=10000, E=8000, q=2000, r=55: D=0, t_min=40, dB(60)=-10000, Sigma=30000 (recompute_r21.py).")
F("AC4-d-L07-R1-title", "PASS", CARRY + "L07.html R1 (lines 399-402): unchanged; t_min = v + D(p_m - v - c)/q.")
F("AC4-d-L07-opportunity-cost-def", "PASS", CARRY + "L07.html §1 (line 72) and §2 (lines 98, 100): unchanged.")
F("AC4-d-L07-why-line52", "PASS", CARRY + "L07.html why-it-matters (line 52): unchanged.")
F("AC4-d-L07-uses-undeclared", "PASS", CARRY + "L07.html meta 'Uses: contribution margin' (line 38) links to AC4/L01.html#def-contribution-margin, unchanged.")
F("AC4-d-L08-uses-undeclared", "PASS", CARRY + "L08.html meta 'Uses' (line 38), unchanged.")
F("AC4-d-2.9-dag-definitions", "PASS", CARRY + "dfn transfer-pricing (line 69), residual-income and economic-value-added (lines 67, 71): unchanged.")
F("AC4-d-2.4-math-L07", "PASS", CARRY + "Lemma 7.2 (lines 89-96), proof (98), §2 (76-86), Theorem 7.3 (111-118) and proof (120): unchanged; the Lemma and Theorem proofs re-derived this round (recompute_r21.py: Delta_S(t) >= 0 iff t >= t_min for q > 0).")
F("AC4-d-2.4-math-L08", "PASS", CARRY + "L08.html Definition 8.1 (65-76), Lemma 8.2 (86), Lemma 8.3 (92), Proposition 8.4 (103-107), §3 (109): unchanged; re-derived (EVA-RI = -tau OI; the Proposition 8.4 differences).")
F("AC4-d-2.4-notation", "PASS", "notation/notation.json and references/ and tools/ unchanged since fd9a9b7 (git diff --stat empty); the round-21 delta adds no symbol to either page (L07 P2 and key-results row use existing symbols q, E, K, p_m, v; L08 line 63 and 291 use OI, C, r, tau).")

# ---- assemble
rows = []
defaulted = []
for pid, pr in prev_rows.items():
    if pid in fresh:
        status, ev, fix = fresh[pid]
        r = {"id": pid, "check": pr["check"], "location": pr["location"], "status": status, "evidence": ev}
        if fix: r["fix"] = fix
    else:
        assert pr["status"] == "PASS", pid  # every non-PASS previous row is in `fresh`
        defaulted.append(pid)
        r = {"id": pid, "check": pr["check"], "location": pr["location"], "status": "PASS", "evidence": CARRY + pr["evidence"]}
    rows.append(r)
new_ids = [k for k in fresh if k not in prev_rows]
for k in new_ids:
    status, ev, fix = fresh[k]
    r = {"id": k, "check": "2.4-math" if "P2" in k or "c093" in k else "2.9-prose", "location": "see evidence", "status": status, "evidence": ev}
    if fix: r["fix"] = fix
    rows.append(r)
# enrich check/location for the new rows
loc = {
 "AC4-d-r21-P2-scope-q-le-K": ("2.4-math", "course/modules/AC/AC4/L07.html line 378 (P2 statement) and line 421 (key-results row 4); course/modules/AC/AC4/L07.html lines 90-96, 76"),
 "AC4-d-r21-c093-hypothesis": ("2.7-cards", "course/modules/AC/AC4/cards.json AC4-c093 (back)"),
 "AC4-d-r21-L07-table-row2-every-price": ("2.4-math", "course/modules/AC/AC4/L07.html line 420 (key-results row 2)"),
 "AC4-d-r21-L08-line63-sourcing": ("2.9-prose", "course/modules/AC/AC4/L08.html line 63"),
}
for r in rows:
    if r["id"] in loc:
        r["check"], r["location"] = loc[r["id"]]
    if r["id"] == "AC4-d-L07-extra-capacity-scope":
        pass

# ---- mutants: parse the transplant outputs
mutants = []
def add_from(path, rnd_default=None):
    for line in open(path, encoding="utf-8"):
        m = re.match(r"^(r\d\d) (\S+\.py): KILLED (.*?)\s*\|?\s*(line:.*)?$", line.strip())
        if not m: continue
        rnd, name, how, desc = m.group(1), m.group(2), m.group(3), (m.group(4) or "")
        folder = f"AC4-d-{rnd}"
        mutants.append({"id": f"{rnd}:{name}", "description": desc or f"lab-twin mutant {name}",
                        "file": f"ledgers/AC4/mutants/{folder}/{name}",
                        "killed_by": f"transplanted onto the current twin (round 21): {how}"})
add_from(f"{S}/transplant_r21.out")
mutants.append({"id": "r18-rebased:L08_n07_ri_side_strict_only.py",
                "description": "round-18 L08 mutant n07 (strict RI test on the division side only), rebased by hand onto the current twin (sign line drops the boundary)",
                "file": "ledgers/AC4/scripts/AC4-d-r21/L08_n07_rebased_on_current_twin.py",
                "killed_by": "direct run: output differs (sign line 8/9 instead of 9/9)"})
for name in ("m20_L07_displaced_forgets_internal_order.py", "m20_L07_sign_check_strict_at_zero.py"):
    mutants.append({"id": f"r20:{name}", "description": "round-20 lab-twin mutant " + name,
                    "file": f"ledgers/AC4/mutants/AC4-d-r20/{name}",
                    "killed_by": "transplanted onto the current twin (round 21): output-differs"})
mutants.append({"id": "r20:m20_L08_eva_taxes_residual_income.py",
                "description": "Lab-twin mutant (round 20): EVA computed as (OI - rC)(1 - tau); not a one-line change, a full copy of the twin run directly",
                "file": "ledgers/AC4/mutants/AC4-d-r20/m20_L08_eva_taxes_residual_income.py",
                "killed_by": "direct run (round 21): output differs from the embedded expected block"})

counts = {"PASS": sum(1 for r in rows if r["status"] == "PASS"), "FAIL": sum(1 for r in rows if r["status"] == "FAIL")}
frag = {
 "unit": "AC4",
 "slice": "AC4-d",
 "round": 21,
 "verifier": "round-21 independent Haiku verifier for slice AC4-d (L07, L08 and their lab twins); did not build AC4 and shares no context with its builders",
 "pin": "f95243f",
 "base": "fd9a9b7 (round-20 pin; /tmp/fanout-frags/AC4-d.round20.json used as context, its PASS rows re-verified or carried only where the cited passage is byte-identical)",
 "checkout": "/tmp/verify21-AC4-d (detached worktree at f95243f, .venv symlink, vendor copied)",
 "scratch": "/tmp/AC4-d-v21 (scratch); command outputs and copies in ledgers/AC4/scripts/AC4-d-r21/",
 "verified_at": "2026-10-28T12:00:00+00:00",
 "verdict": "FAIL",
 "rows": rows,
 "mutants": mutants,
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
  "Delta fd9a9b7..f95243f for the slice: L07.html lines 134, 378 (P2 statement), 420 and 421 (key-results rows 2 and 4); L08.html lines 63 and 291; cards.json c089 and c095 (L07). L01/L02 cards (c007, c020), the AC4 hub line 52 and the M1/AC1/CF1 files are outside this slice and were not judged.",
  "FAIL rows: AC4-d-r21-P2-scope-q-le-K (the q <= K hypothesis was dropped from P2 and the key-results row, but t_min and D are defined on this page only under q <= K) and AC4-d-r21-c093-hypothesis (card c093 states the P2 result with fewer hypotheses). AC4-d-r17-cards-scope is FAIL for the same card (c093). Fixes: restore 'q <= K' in P2 (line 378) and key-results row 4 (line 421), and add the hypotheses to card c093.",
  "Fixed since round 20 and verified: c089 (back now cites Section 3 and P1 for every t; Theorem 7.3 part 3 for t in the range) and c095 basis (names the four check lines, which the lab prints).",
  "Lab twins and their embedded blocks are byte-identical to fd9a9b7 (git diff --stat empty), so the seed-based and generator-based rows are carried with that basis. All command rows were re-run on f95243f.",
  "Mutants: no new student-error mutants were written this round because this is a lesson slice, not a project slice (the >=3 new mutant rule applies to project graders). All earlier lab-twin mutants were re-run: 30 killed by the transplant, 4 killed in the round-20 set, one r18 mutant (L08_n07) killed after rebasing its changed line, survivors AC4-d-r20-lab-midpoint-survivor (midpoint replaced by t_min; the shipped lab checks the midpoint, PASS under the architect ruling, flagged to the orchestrator because L07 line 140 says the sum identity is checked at the midpoint) and the two equivalents r17_L08_m04 and L08_n09.",
  "Alternative correct implementations: not rerun this round (the twins are unchanged and the round-19 and round-20 alternatives were carried). The hub hours (50 + 20) were checked by arithmetic only; hours are design targets and were not judged on pace.",
  "Not checked: verify_refs live beyond the unit run (no network use beyond the tool's own run); the Pyodide timing beyond page_smoke; the round-20 seed scans were carried, not re-run; the project grader (mutate_graders) was carried, not re-run, because no project file changed."
 ],
 "summary": {"rows": len(rows), "pass": counts["PASS"], "fail": counts["FAIL"], "defaulted_carry": len(defaulted), "mutants_killed": len(mutants)},
}
json_path = f"{ROOT}/ledgers/AC4/AC4-d.json"
import os
os.makedirs(os.path.dirname(json_path), exist_ok=True)
json.dump(frag, open(json_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("rows", len(rows), "pass", counts["PASS"], "fail", counts["FAIL"], "defaulted", defaulted)
print("new", new_ids)
print("mutants", len(mutants))
