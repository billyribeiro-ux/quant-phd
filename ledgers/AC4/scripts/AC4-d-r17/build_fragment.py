"""Build the round-17 AC4-d fragment (L07, L08 and lab twins) with the verdict computed from the rows."""
import json
import sys

S = "/tmp/AC4-v/AC4-d-r17"
SC = "ledgers/AC4/scripts/AC4-d-r17"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        assert fix, rid
        r["fix"] = fix
    rows.append(r)


CARRY = "Carried from round 16 (notation/ and course/modules/AC/AC4/L07.html, L08.html byte-identical since the previous pin d57df1e): "

# ---- command rows, all re-run on fefbf8b
row("AC4-d-cmd-pin", "2.9-structure",
    "repository; course/modules/AC/AC4/L07.html, L08.html, cards.json, tests/labs/AC4/lab-AC4-L07-1.py, lab-AC4-L08-1.py",
    "PASS",
    "git rev-parse --short HEAD in /tmp/verify17-AC4-d -> fefbf8b (detached). git diff --name-only d57df1e fefbf8b (non-ledger files) lists no tools/, tests/ (except AC1/CF1 labs), notation/ or my four files. 'git diff --quiet d57df1e fefbf8b -- L07.html L08.html lab-AC4-L07-1.py lab-AC4-L08-1.py' exits 0 (byte-identical). cards.json changed for AC4-c091, AC4-c102 (in my slice) and added AC4-c120..c134 (c129, c134 in my slice). Transcript of the git commands is in the rows that follow.")
row("AC4-d-cmd-run_labs", "2.5-labs", "tools/run_labs.py --unit AC4; tests/labs/AC4/*", "PASS",
    "python tools/run_labs.py --unit AC4 -> 'run_labs AC4: PASS (10/10)' (transcript " + S + "/run_labs.out).")
row("AC4-d-cmd-twin-isolated", "2.5-labs", "tests/labs/AC4/lab-AC4-L07-1.py; tests/labs/AC4/lab-AC4-L08-1.py", "PASS",
    ".venv/bin/python -I -W error tests/labs/AC4/lab-AC4-L07-1.py exit 0 and output printed in full (" + S + "/L07.out); same for L08 (" + S + "/L08.out, exit 0). Output equals the page expected block: see AC4-d-r17-cmd-embed.")
row("AC4-d-cmd-page_smoke", "2.5-labs", "tools/page_smoke.py --unit AC4 --pages L07 L08; L07.html, L08.html", "PASS",
    "page_smoke modules/AC/AC4/L07.html: PASS; modules/AC/AC4/L08.html: PASS; 'page_smoke AC4: PASS'. Runtime: lab-AC4-L07-1 0.0 s, lab-AC4-L08-1 0.0 s (boot 1.1 s with numpy). Transcript " + S + "/page_smoke.out.")
row("AC4-d-cmd-check_pages", "2.9-structure", "tools/check_pages.py --all; L07.html, L08.html, cards.json grade and basis rules", "PASS",
    "tools/check_pages.py --all exit 0; 'check_pages AC4: PASS' (and every other unit PASS). Transcript " + S + "/check_pages.out.")
row("AC4-d-cmd-check_dag", "2.9-dag", "tools/check_dag.py --all", "PASS",
    "tools/check_dag.py --all exit 0; 'check_dag AC4: PASS'. Transcript " + S + "/check_dag.out.")
row("AC4-d-cmd-check_projects", "2.9-structure", "tools/check_projects.py --all", "PASS",
    "tools/check_projects.py --all exit 0; 'check_projects AC4: PASS'. Transcript " + S + "/check_projects.out.")
row("AC4-d-cmd-lint-mypy", "2.9-lint", "tests/labs/AC4/lab-AC4-L07-1.py; tests/labs/AC4/lab-AC4-L08-1.py", "PASS",
    ".venv/bin/python -m ruff check on both twins: 'All checks passed!' exit 0; ruff format --check exit 0; .venv/bin/python -m mypy --no-incremental on both twins: 'Success: no issues found in 2 source files' exit 0. Transcripts " + S + "/ruff.out, mypy.out.")
row("AC4-d-cmd-pytest", "2.9-tests", "tests/test_labs.py, tests/test_page_checks.py, tests/test_page_smoke.py", "PASS",
    ".venv/bin/python -m pytest -q on the three files: exit 0, 176 progress dots (72 + 72 + 32 lines of dots). Transcript " + S + "/pytest.out.")
row("AC4-d-cmd-verify_refs", "2.1-citations", "tools/verify_refs.py --offline; tools/verify_refs.py --unit AC4; references/references.json", "PASS",
    "verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' exit 0. verify_refs.py --unit AC4: 'live re-verification of AC4: 2 of 560 entries, 0 problems' exit 0. Transcripts " + S + "/verify_refs_offline.out, verify_refs_unit.out.")
row("AC4-d-r17-cmd-mutate_graders", "2.5-labs", "tools/mutate_graders.py --unit AC4 --seeds 0-4; ledgers/AC4/mutants/*.py (top level, the earlier project-grader mutants)", "PASS",
    "Re-run of every earlier AC4 mutant (top-level ledgers/AC4/mutants/*.py, which are complete project-grader modules, outside my slice): 'mutate_graders AC4: PASS (121/121 killed)'. The tool globs only the top level, so the lab mutants written this round under ledgers/AC4/mutants/AC4-d-r17/ are not part of this gate. Transcript " + S + "/mutate_grader.out.")
row("AC4-d-r17-cmd-embed", "2.5-labs", "course/modules/AC/AC4/L07.html and L08.html embedded data-run code and class=expected blocks; tests/labs/AC4/lab-AC4-L07-1.py, lab-AC4-L08-1.py", "PASS",
    SC + "/embed_check.py: embedded code == twin file (True) for both labs; expected block == live output of python -I -W error on the twin (True) for both labs. Transcript " + S + "/embed_check.out.")

# ---- citations, numbers, grades, math
row("AC4-d-2.1-citations-L07-L08", "2.1-citations", "course/modules/AC/AC4/L07.html line 479; L08.html line 468", "PASS",
    "Both pages state that no registry source is cited. grep for data-ref, cite, or a registry key in L07.html and L08.html: the only match is the empty <ol data-references> element. verify_refs (AC4-d-cmd-verify_refs) passes with 0 problems.")
row("AC4-d-2.2-numbers-L07", "2.2-numbers", "L07.html §2 (lines 128-134), §4 (lines 129-134), §5 (line 297), §7 (lines 313, 315, 317), M1-M3 (lines 325-335), E1-E3 (lines 357-365), key-results table (lines 389-395)", "PASS",
    "Re-derived each displayed number from the stated inputs: D = max(0, 5000+8000-10000) = 3000; t_min = 40+3000*20/5000 = 52; Sigma = 5000*40-3000*20 = 140000; at t=52 Delta_S = 0, Delta_B = 140000; at t=46 Delta_S = -30000; K=12000: D=1000, t_min=44, Sigma=180000; r=50: Sigma=-10000; misconception 1 (46 gives -30000); misconception 2 (v=40,p=60,K=10000,E=8000,q=2000,r=55: D=0, t_min=40, Delta_B=-10000, Sigma=30000). Lab counts: 14 over, 75 empty, 111 feasible, 72 binding, 186 checked, 72/111 = 0.6486, 75/186 = 0.4032 (independent integer recomputation " + SC + "/indep_recompute.py: L07 over 14 fits 186 empty 75 feasible 111 binding 72 checked 186). First six lab rows (t_min, t_max, D) match lab output and the integer recomputation.")
row("AC4-d-2.2-numbers-L08", "2.2-numbers", "L08.html §1 (line 115), §3 (line 109), §4 (lines 115-122), §5 (lines 128, 130), §6 (lines 284-286), §7 (line 291), §8 (lines 302-306), M1-M3 (lines 314-324), E1-E3 (lines 346-354), key-results (lines 378-384)", "PASS",
    "Re-derived: C=1000, OI=120, r=9%, tau=20%: RI 30, NOPAT 96, EVA 6, Lemma 8.2 check -24 = -0.2*120. Capitalized outlay 100 over 5 years (first-year 20): dOI=dC=80, RI 102.8 (dRI 72.8), EVA 62.8 (dEVA 56.8). §5 X: RI 15, Y: RI 20, ratios 0.12, 0.10. SIM-G: 2250 - 0.2*13680 = 2250 - 2736 = -486. Lab table recomputed by " + SC + "/indep_recompute.py for all 8 divisions (RI and EVA in cents match the printed values exactly). Capitalization lines: SIM-A dOI=dC=8000, dRI=7280, dEVA=5680. §7: C=1400 gives RI -6; M3: dRI 36.4, dEVA 28.4. Lab pair count 4 of 28 reproduced. 4/28 = 1/7 = 0.1429.")
row("AC4-d-2.2-numbers-L07-E1-seed", "2.2-numbers", "L07.html E1 solution (line 357); tests/labs/AC4/lab-AC4-L07-1.py", "PASS",
    SC + "/seed_scan.py (run on the twin with SEED replaced, seeds 1..40): the empty-range count 75 occurs only at seeds 31 (feasible 119, so 194 pairs with q<=K) and 40 (feasible 114, so 189); no seed among 1..40 gives 75 empty out of 186. The claim 'None of seeds 1 to 40 reproduces the pair of 75 empty ranges out of 186' holds. Output " + S + "/seed_scan.out.")
row("AC4-d-L08-E1-seed-claim", "2.2-numbers", "L08.html E1 solution (line 346)", "PASS",
    SC + "/seed_scan.py, L08 part: discordant-pair count 4 occurs exactly at seeds 14, 20, 26 and 28 of seeds 1..40; every other seed gives a count other than 4 (values 0, 1, 2, 3, 5, 6, 7, 9). The claim 'Seeds 14, 20, 26 and 28 of seeds 1 to 40 also give 4 discordant pairs, and the other 36 give other counts' holds. 4/28 = 1/7 = 0.1429.")
row("AC4-d-2.3-grades-L07", "2.3-grades", "L07.html grade spans and key-results table (§9, lines 384-399); card grades AC4-c087..c096, c117", "PASS",
    "Derived claims (Lemma 7.2, Theorem 7.3, P1, P2, worked-case arithmetic) are graded T with derivations on the page. Lab-read counts (75/111/186, 72 binding) are graded C with the basis 'Lab 1 (SIMULATED)'. No claim about real divisions is graded above C. Cards: T for derived (c087-c094, c117), C for lab-read (c095, c096). Definition cards c082-c086 carry no grade field, as in the rest of the course.")
row("AC4-d-2.3-grades-L08", "2.3-grades", "L08.html grade spans and key-results table (§10, lines 375-386); card grades AC4-c097..c116, c129, c134", "PASS",
    "Proposition 8.4, Lemmas 8.2 and 8.3, P3 and the worked arithmetic are T. Lab-read identity lines and the 4-of-28 pair count and SIM-G values are C with basis 'Lab 1 (SIMULATED)'. The 9% and 900 bp are stated inputs, labelled as such (line 387). Cards c101, c108, c109, c113, c114 are C; c105-c107, c115, c116, c103, c104, c100, c102, c129, c134 are T; definition cards c097-c099 carry no grade field.")
row("AC4-d-2.4-math-L07", "2.4-math", "L07.html Lemma 7.2 (lines 89-96), proof (line 98), §2 paragraph (line 100), Theorem 7.3 (lines 110-118) and proof (line 120), §3 algebra (lines 104-108)", "PASS",
    "Re-derived: Delta_S(t) >= 0 iff q(t-v) >= D(p_m-v) iff t >= t_min (q>0). Delta_B(t) >= 0 iff t <= r. Sum = q(r-v) - D(p_m-v), t cancels. Part 2: t_min <= t_max multiplied by q gives q(r-v) - D(p_m-v) >= 0. D <= q from E <= K, so t_min <= p_m. All consistent with the page text; checked numerically by the lab identities (AC4-d-2.5-lab-L07).")
row("AC4-d-2.4-math-L08", "2.4-math", "L08.html Definition 8.1 (lines 65-76), Lemma 8.2 (line 86), Lemma 8.3 (lines 88-92), Proposition 8.4 (lines 100-107), §3 sentence at line 109, P1-P3 (lines 329-339)", "PASS",
    "Re-derived: EVA - RI = OI(1-tau) - OI = -tau*OI. RI >= 0 iff OI >= rC iff OI/C >= r for C>0. dRI - dEVA = tau*dOI, zero iff tau=0 or dOI=0. With r>0, tau<=1, dC>0 and dOI<=0: dRI = dOI - r dC < 0 and dEVA = (1-tau) dOI - r dC < 0 (the line 109 claim, lowers both). Same-base P3 correct.")
row("AC4-d-2.4-notation", "2.4-notation", "notation/notation.json (macros and 8 registered symbols); L07.html and L08.html notation", "PASS",
    CARRY + "the subjects are byte-identical (git diff --quiet d57df1e fefbf8b -- notation exits 0; L07.html and L08.html unchanged). Previous evidence: notation/notation.json macros and 8 registered symbols; both pages use the registered symbols.")
row("AC4-d-2.5-lab-L07", "2.5-labs", "L07.html Lab 1 (§4, lines 136-293); tests/labs/AC4/lab-AC4-L07-1.py", "PASS",
    "Hypothesis (line 140) is tested by the lab: supplier increment zero at t_min, buyer zero at t_max, Sigma identity at lo, hi and midpoint (lines 268-273), biconditional nonempty iff Sigma>=0 (line 270). Seeded (SEED=20261027), no network, exact Fractions; page_smoke lab time 0.0 s; expected block equals live output. Interpretation (line 292) is consistent: 14 pairs with q>K excluded, 186 checked, 3400.00 cents = 34.00 SCU. The equality boundary is not exercised by the data: see AC4-d-r17-boundary-L07 (FAIL).")
row("AC4-d-2.5-lab-L08", "2.5-labs", "L08.html Lab 1 interpretation (line 279), §6 (line 284), §5 (lines 128-130); tests/labs/AC4/lab-AC4-L08-1.py", "PASS",
    "Hypothesis (line 134) tested: identity EVA-RI = -tau*OI for 8/8 (line 231), sign identity RI>=0 iff OI/C>=r for 8/8 (line 232), discordant pair count 4 of 28 (lines 236-244). Seeded, exact Fractions, expected equals live output. Interpretation matches output: C column has eight distinct values (line 130 claim true); capitalization lines equal Proposition 8.4 values. The equality boundary is not exercised: see AC4-d-r17-boundary-L08 (FAIL).")

# ---- cards
row("AC4-d-2.7-cards-L07-L08", "2.7-cards", "course/modules/AC/AC4/cards.json: AC4-c082..c096, c117 (L07); c097..c109, c113..c116, c129, c134 (L08)", "PASS",
    "All 35 L07/L08 cards read against the current lesson text. Changed this round: AC4-c091 (checked against Theorem 7.3 part 1 and Lemma 7.2, row AC4-d-r17-cards-c091-changed) and AC4-c102 (checked against §5 and misconception 3, row AC4-d-r17-cards-c102-changed). New: AC4-c129 and AC4-c134 (row AC4-d-r17-cards-c129-c134-new). Every card number appears in its lesson (e.g. 46, 52, 140,000, 72.8, 56.8, 4 of 28, 186, 75, 111, 72). Card grades agree with the page's grades (T for derived, C for lab-read). No duplicate card id, front or back across all 134 AC4 cards (AC4-d-r6-cards-dup-scan).")
row("AC4-d-2.7-cards-c088-outside-option", "2.7-cards", "cards.json AC4-c088 (back); L07.html line 315", "PASS",
    "AC4-c088 back: v=40, p_m=60, K=10,000, E=8,000, q=2,000, r=55, D=0, t_min=40, 2,000 x (55-60) = -10,000, surplus 30,000 positive. All match L07.html line 315 (misconception 2). Card is T-graded, arithmetic matches.")
row("AC4-d-2.7-cards-c100-lemma83", "2.7-cards", "cards.json AC4-c100 (back); L08.html §4 (lines 117-120) and Lemma 8.3 (line 90)", "PASS",
    "AC4-c100 back: RI nonnegative iff OI/C >= r (Lemma 8.3), capitalization moves RI 30 to 102.8 (§4 line 119 and misconception 1 line 302). Consistent.")
row("AC4-d-r3-L07-cards-c117", "2.7-cards", "cards.json AC4-c117 (L07); L07.html §4 line 134 and M2 line 331", "PASS",
    "AC4-c117 back: K=12,000 gives D=1,000 and floor 40+1,000x20/5,000 = 44 (line 134 and M2 line 331, t_min 44). Consistent; T-graded.")
row("AC4-d-r3-L08-cards-c113-c116", "2.7-cards", "cards.json AC4-c113, c114, c115, c116 (L08); L08.html §4 (lines 117-120), §5-§6 (lines 128-130, 284)", "PASS",
    "c113: SIM-D C 124,000 vs SIM-A 59,000, RI -4130.00 vs -2440.00, returns 5.67% vs 4.86%, both below 9% (matches the table line 266 and misconception 3). c114: SIM-G RI 2250.00, EVA -486.00 (line 269, §6). c115: 72.8, 30 to 102.8. c116: 56.8, 6 to 62.8. All match.")
row("AC4-d-r6-cards-dup-scan", "2.7-cards", "course/modules/AC/AC4/cards.json (all 134 AC4 cards)", "PASS",
    "Python scan of cards.json at fefbf8b: 134 cards, no duplicate id, no duplicate front (case-insensitive), no duplicate back. Key sets: back/front/id/lesson with optional grade and basis. Output in this verifier's scratch.")
row("AC4-d-2.8-data", "2.8-data", "L07.html, L08.html (no data-files attribute)", "PASS",
    "grep for data-files in both pages: no match (False, False). Both labs read no snapshot; both use generated SIMULATED data (seed 20261027).")

# ---- prose, DAG, hours
row("AC4-d-2.9-prose-banned", "2.9-prose", "course/modules/AC/AC4/L07.html, L08.html prose (outside code and math); changed lines L07 315 and 357", "PASS",
    "Script " + SC + "/prose_scan.py (output " + S + "/prose_scan.out): 26 banned-list hits and 82 scope-word hits, each read in context. Each hit is an ordinary use (about what firms do, how often a range is empty, several terms, many outside units, some pairs), not an approximation of a number and not a banned phrase (roughly half, about 6%, historically). No banned phrase in L07 or L08 prose. data-files absent in both pages. Scope words (all, every, only, always, never, same, drives, offsets, raises, as much as) each checked against a computation or the page's own proof: L07 lines 52, 100, 134, 140, 297, 303, 313, 317, 357, 376, 378; L08 lines 52, 109, 130, 134, 284, 291, 302, 303, 304, 306, 346, 361, 369. 'hand-built' describes the examples, not a builder.")
row("AC4-d-2.9-dag-definitions", "2.9-dag", "L07.html dfn transfer-pricing (line 69); L08.html dfn residual-income (line 67) and economic-value-added (line 71)", "PASS",
    "check_dag.py --all PASS (AC4). Each concept defined once: transfer-pricing (L07 line 69), residual-income and economic-value-added (L08 lines 67, 71). Links to contribution-margin resolve to AC4/L01.html#def-contribution-margin (defined at L01 line 88); income-statement and balance-sheet resolve to concepts.html anchors (defined at AC1/L02 per concepts.html lines 103 and 108). No concept used before its prerequisite.")
row("AC4-d-2.9-hours", "2.9-hours", "L07.html, L08.html data-hours (line 2) and eyebrow (line 35); AC4 index.html data-hours-lessons (line 29), hours-split, cards (lines 150-151)", "PASS",
    "Lesson hours: L01..L08 data-hours = 6,7,6,6,7,6,6,6 summing to 50 = index data-hours-lessons=50; project 20; total 70 = index title '70 hours'. L07 and L08 declare 6 h, matching their eyebrows (line 35) and the hub cards (L07 · 6 h, L08 · 6 h). Arithmetic consistent (no pace estimate judged, per architect ruling).")
row("AC4-d-L07-opportunity-cost-def", "2.4-math", "course/modules/AC/AC4/L07.html §1 line 72; §2 lines 98/100; §6 line 303", "PASS",
    "§1 line 72: displaced units D=max(0,q+E-K); opportunity cost per internal unit D(p_m-v)/q; q-D absorbed by spare capacity equals min(q, K-E) (checked by algebra). Line 98/100 consistent with Lemma 7.2. Line 303 (no outside sale gives t_min=v) consistent with D(p_m-v) replaced by 0.")
row("AC4-d-L07-extra-capacity-scope", "2.4-math", "course/modules/AC/AC4/L07.html §4 line 134, after the K = 12,000 case", "PASS",
    "Line 134 claim: with D>0 and p_m>v, more capacity lowers t_min and raises Sigma; with D=0 it changes neither; r does not move. Derivation: D=max(0,q+E-K) is nonincreasing in K, decreasing whenever D>0, so t_min = v + D(p_m-v)/q falls strictly and Sigma = q(r-v)-D(p_m-v) rises strictly when D>0 and p_m>v; D=0 stays 0. Numbers: K 10,000 to 12,000: t_min 52 to 44 and Sigma 140,000 to 180,000.")
row("AC4-d-L07-uses-undeclared", "2.9-dag", "course/modules/AC/AC4/L07.html line 38 (meta 'Uses:')", "PASS",
    "Meta 'Uses:' lists contribution margin, linking to AC4/L01.html#def-contribution-margin, which is defined there (L01 line 88). Definitions used in L07 (contribution margin, transfer pricing, supplier and buyer gains) are the ones the page defines or links; no undeclared prerequisite.")
row("AC4-d-L08-uses-undeclared", "2.9-dag", "course/modules/AC/AC4/L08.html line 38 (meta 'Uses:')", "PASS",
    "Meta 'Uses:' lists income statement and balance sheet, linking to concepts.html#income-statement and #balance-sheet, both present in concepts.html (lines 108, 103). Both are AC1 concepts (AC1/L02 'defined here').")
row("AC4-d-L08-tau-zero-scope", "2.4-math", "course/modules/AC/AC4/L08.html §3 line 109, after Proposition 8.4", "PASS",
    "Line 109: dRI - dEVA = tau*dOI, so equal iff tau=0 or dOI=0; with r>0, tau<=1, dC>0, a choice raising C without raising OI lowers both. Verified algebraically (see AC4-d-2.4-math-L08).")
row("AC4-d-L08-base-sign-scope", "2.2-numbers", "course/modules/AC/AC4/L08.html §7 line 291, 'The base decides the level'", "PASS",
    "Line 291: OI=120, r=9%: C=1000 gives RI 30; C=1400 gives RI -6 (120-126). Sign changes with the base. Computed: 120-0.09*1400 = -6.")
row("AC4-d-L08-size-claim", "2.7-cards", "course/modules/AC/AC4/L08.html §8 misconception 3 (lines 305-306); cards.json AC4-c102 (back)", "PASS",
    "Re-verified against the changed card AC4-c102 (row AC4-d-r17-cards-c102-changed). Misconception 3 claims: same return above r gives larger RI for larger division (RI=(OI/C-r)C, correct); SIM-D vs SIM-A numbers (124,000 vs 59,000; -4130.00 vs -2440.00; 5.67% vs 4.86%) match the table; §5 X/Y 15 vs 20 and 0.12 vs 0.10 match.")
row("AC4-d-L08-quiz-agreement-claim", "2.9-quiz", "course/modules/AC/AC4/L08.html quiz L08q5 option (line 423) and explanation (line 426)", "PASS",
    "Correct option: residual income is an amount that depends on the size of the base, the ratio ignores scale, and the bases differ. Explanation: with a common base the orders always agree (P3); with different bases they can disagree, as 4 of the 28 pairs do. Consistent with the lab: no two of the eight bases coincide, and the 4 discordant pairs are between differing bases.")
row("AC4-d-r2-L08-lab-pair-scope", "2.5-labs", "course/modules/AC/AC4/L08.html §5 paragraph after the 'same base' sentence (line 130)", "PASS",
    "Line 130: same base implies same order (P3, verified), the 28 pairs of 8 divisions (C(8,2)=28), and 'the C column lists eight different values' (lab output lines 263-270: 59000, 53000, 173000, 124000, 78000, 27000, 127000, 161000, all distinct; verified by " + SC + "/indep_recompute.py).")
row("AC4-d-L07-why-line52", "2.4-math", "course/modules/AC/AC4/L07.html why-it-matters, line 52", "PASS",
    "Line 52: the price moves profit between divisions; the firm's gain from the sale does not depend on the price (Theorem 7.3 part 3, verified); 'a supplier with spare capacity and one at full capacity face different costs' (D=0 gives zero opportunity cost; D>0 gives positive, by Lemma 7.2 and §4 numbers).")
row("AC4-d-L07-misconception2-market-price", "2.4-math", "course/modules/AC/AC4/L07.html §7 misconception 2, line 315", "PASS",
    "Re-computed: v=40, p_m=60, K=10,000, E=8,000, q=2,000, r=55 gives D=0, t_min=40, Delta_B(60)=-10,000, Sigma=30,000 (positive), a price of 40 to 55 makes the sale. Matches the line.")
row("AC4-d-L07-R1-title", "2.9-structure", "course/modules/AC/AC4/L07.html R1 title and solution, lines 369-372", "PASS",
    "R1 solution: delivery cost c changes the outside contribution to p_m-v-c, so t_min = v + D(p_m-v-c)/q (Lemma 7.2 with p_m-v replaced); t_max = r unchanged since the buyer's gain does not involve outside sales. Algebraically correct; labelled as a hypothesis.")
row("AC4-d-L08-why-capital-charge-rate", "2.9-dag", "course/modules/AC/AC4/L08.html why-it-matters, line 52", "PASS",
    "Line 52: both measures depend on OI, C and r, and EVA also on tau; the two differ by a term in tau and OI (Lemma 8.2, verified). Accounting choices move both (Proposition 8.4). Consistent with §1-§3.")
row("AC4-d-L08-misconception1-C-positive", "2.4-math", "course/modules/AC/AC4/L08.html §8 misconception 1, line 302", "PASS",
    "Line 302: C>0, RI>=0 iff OI/C>=r (Lemma 8.3); capitalization moves RI from 30 to 102.8 SCU (§4 line 119, verified 72.8 change). Consistent.")
row("AC4-d-r3-L07-s1-s5-s6-text", "2.4-math", "course/modules/AC/AC4/L07.html §1 (line 70), §5 (line 297), §6 bullets (lines 302-305)", "PASS",
    "Line 70 (Definition 7.1): transfer price moves money, leaves firm's cash flow unchanged, §3 proves it (Theorem 7.3 part 3). §5 line 297 counts (14/75/111/72) and share 72/111 verified. §6 bullets: one period, outside sale availability, no tax term, capacity hard limit; each matches the stated model in §1 and the lab docstring.")
row("AC4-d-r3-L08-why-and-s3-s5-text", "2.4-math", "course/modules/AC/AC4/L08.html why-it-matters (line 52), §1 OI/C paragraph (line 78), §3 (lines 98-109), §5 (lines 126-130)", "PASS",
    "§3: change formulas (Proposition 8.4) verified; the tau*dOI relation verified; §5 claims verified numerically (RI_X=15, RI_Y=20, 0.12, 0.10; 4 of 28). Consistent.")

# ---- new round-17 rows: delta, changed cards, computations, mutants, boundary
row("AC4-d-r6-delta-coverage", "2.9-structure", "git diff --stat d57df1e fefbf8b, and --name-only (non-ledger); course/modules/AC/AC4/L07.html, L08.html, cards.json, tests/labs/AC4/lab-AC4-L07-1.py, lab-AC4-L08-1.py", "PASS",
    "Delta since the previous pin d57df1e: 11 commits, 1594 files, of which non-ledger files are AC1/CF1/M1 course and labs, AC4 L01, L02, L05, L06, cards.json, grader, project.html, and CF1 plan. My slice files: L07.html, L08.html and both twins are byte-identical (git log empty). cards.json: AC4-c091 and AC4-c102 changed (both in my slice); AC4-c129 and AC4-c134 added (L08); other changed cards (c003..c078) belong to L01-L06 (not my slice). Re-verified every row whose subject changed; carried only the notation row (its subject byte-identical).")
row("AC4-d-r17-cards-c091-changed", "2.7-cards", "cards.json AC4-c091 (back, T), L07.html Theorem 7.3 part 1 (line 114), Lemma 7.2 (lines 91-95)", "PASS",
    "Old back: 'Delta_S + Delta_B = Sigma'. New back: exactly the prices in [t_min, t_max]; both gains nonnegative there; outside it at least one gain negative (Theorem 7.3 part 1). Checked: Delta_S < 0 for t < t_min and Delta_B < 0 for t > t_max (Lemma 7.2 signs), so the new back is correct. The card's front and back agree with Theorem 7.3 part 1, which the page proves (line 120).")
row("AC4-d-r17-cards-c102-changed", "2.7-cards", "cards.json AC4-c102 (back, T), L08.html misconception 3 (line 306), §5 (lines 128-130)", "PASS",
    "New back: 'False as a general rule... For two divisions with the same return on capital above the rate, the larger one has the larger residual income, because RI = (OI/C - r)C. Which division is better depends on the question asked.' The removed §5 example sentence is not required by the card. Each sentence is true: RI=(OI/C-r)C is algebra (correct), and the 'depends on the question asked' conclusion matches misconception 3 (line 306). No number appears that is absent from the page.")
row("AC4-d-r17-cards-c129-c134-new", "2.7-cards", "cards.json AC4-c129 (X: RI 15, C=500, OI=60, r=9%) and AC4-c134 (Y: RI 20, C=2,000, OI=200, r=9%), L08 (T); L08.html §5 line 128", "PASS",
    "§5 line 128: X C=500, OI=60: RI = 60-0.09*500 = 15; Y C=2,000, OI=200: RI = 200-180 = 20; r=9% in both. Cards match the text; both cited numbers appear in §5 and in misconception 3 (line 306). Grade T for stated-input arithmetic (consistent with AC4-c107).")
row("AC4-d-r17-indep-recompute", "2.2-numbers", SC + "/indep_recompute.py (integer-only, does not import the twins); L07 and L08 printed counts and table", "PASS",
    "Independent integer recomputation: L07 over 14, fits 186, empty 75, feasible 111, binding 72, checked 186; 72/111 = 0.6486, 75/186 = 0.4032; first-six t_min values 3400, 3600, 6193.02, 4823.32, 3600, 4932.04 and t_max values match the printed table. L08: discordant 4 of 28; RI and EVA for all 8 divisions match the printed table exactly (e.g. SIM-G 2250.00 and -486.00). Output " + S + "/indep.out.")
row("AC4-d-r17-boundary-probe", "2.5-labs", SC + "/boundary_scan.py; " + SC + "/boundary_witness.py", "PASS",
    "The equality boundary is absent from the generated data: boundary_scan over the lab seed and seeds 1..40 finds 0 L07 pairs with t_min = t_max, 0 with Sigma = 0, 0 L08 divisions with RI = 0, 0 with OI/C = r, and 0 rank ties. The boundary exists in the model: boundary_witness.py shows the worked case with r = 52 has t_min = t_max = 52 and Sigma = 0 (supplier and buyer gains 0), and a division with C=100,000, OI=9,000, r=9% has RI = 0 and OI/C = 9% = r. Output " + S + "/boundary.out, boundary_witness.out.")
row("AC4-d-r17-boundary-L07", "2.5-labs", "tests/labs/AC4/lab-AC4-L07-1.py line 270 (assert (lo <= hi) == (firm_surplus >= 0)) and line 257 (empty = t_min > t_max); L07.html line 140 ('exactly when'), Theorem 7.3 part 2 (line 115) and its proof (line 120, t_min <= t_max)", "FAIL",
    "Mutant r17_L07_m03 (ledgers/AC4/mutants/AC4-d-r17/r17_L07_m03_strict_nonempty.py) changes the empty test to t_min >= t_max, i.e. counts a single-point range (t_min = t_max, Sigma = 0) as empty. The printed output is unchanged (SAME_AS_EXPECTED), so the mutant survives. The page states the behaviour the mutant violates: Theorem 7.3 part 2 says the range is nonempty iff Sigma >= 0, its proof says iff t_min <= t_max (non-strict), and the lab hypothesis (line 140) says 'nonempty exactly when Sigma >= 0'. No generated pair lies on the boundary (boundary_scan), so the lab's exact checks never test the equality case.",
    fix="Add the boundary case to Lab 1 (for example the worked case of §4 with r = 52 gives t_min = t_max = 52 and Sigma = 0; the pair must be included in the printed output and in the exact-check count), and make the printed count and the check at line 270 exercise it. Then re-run the lab, refresh the expected block with embed_labs.py, and cite the boundary row in the hypothesis. Re-run ruff, mypy, page_smoke on L07.")
row("AC4-d-r17-boundary-L08", "2.5-labs", "tests/labs/AC4/lab-AC4-L08-1.py line 232 (sign_ok with >=); L08.html line 134 (hypothesis 'sign identity of Lemma 8.3 holds exactly'), Lemma 8.3 (line 90, 'RI >= 0 iff OI/C >= r')", "FAIL",
    "Mutant r17_L08_m02_ratio_ge_strict.py changes the sign test to strict (RI > 0 iff OI/C > r). Output unchanged (SAME_AS_EXPECTED, 'RI >= 0 exactly when OI/C >= r holds for 8/8'), so the mutant survives. Lemma 8.3 states the non-strict equivalence (line 90, proof line 92). No generated division has RI = 0 or OI/C = r (boundary_scan), so the printed check never tests the equality the lemma and the hypothesis claim.",
    fix="Add a boundary division to Lab 1 (for example C = 100,000 cents, OI = 9,000 cents, r = 9% gives RI = 0 and OI/C = r) to the table and to the sign-identity check, so that a strict test fails the printed 8/8 line; refresh the expected block with embed_labs.py and re-run page_smoke on L08.")
row("AC4-d-r17-mutants-killed", "2.5-labs", "lab mutants in ledgers/AC4/mutants/AC4-d-r17/ (9 files), checked against the page expected blocks", "PASS",
    "Six of eight non-equivalent lab mutants are killed: L07 m01 (displaced ignores E: rows 3 and 4 change), m02 (floor without division by q: AssertionError), m04 (buyer gain sign: AssertionError), m05 (firm surplus adds v: AssertionError); L08 m01 (EVA without tax: table changes), m03 (capitalized without amortization credit: capitalization lines change). The two survivors are recorded as FAIL rows AC4-d-r17-boundary-L07 and AC4-d-r17-boundary-L08. Transcript " + S + "/mutants_alts_rerun.out.")
row("AC4-d-r17-mutant-L08-m04-ties", "2.5-labs", "ledgers/AC4/mutants/AC4-d-r17/r17_L08_m04_discord_ignores_ties.py (equivalent on the data)", "PASS",
    "Equivalent (out of scope): the mutant drops the 'by_ri != 0 and by_ratio != 0' guard, so ties would count as discordant. boundary_scan finds 0 rank ties over the lab seed and seeds 1..40, so output is identical; the page states no tie rule (lines 126-134 say only 'disagree'). Not a FAIL: no sentence on the page is violated. Kept out of the mutant list per the equivalent-mutant rule.")
row("AC4-d-r17-alternatives", "2.5-labs", "ledgers/AC4/scripts/AC4-d-r17/alts/*.py (valid alternative implementations of the L07 and L08 twins), run by alt_and_run.py", "PASS",
    "Four valid alternatives reproduce the expected block exactly: displaced units as E - min(E, K-q); nonempty tested as Sigma >= 0 instead of t_min <= t_max; RI with integer-scaled tax arithmetic; discordance by sign of differences. One alternative (floor computed in Decimal at 28 significant digits) is not exact and fails the exact-identity assert with AssertionError; the page says every check uses exact fractions (line 140), so this is consistent with the page and not an over-constraint. Output " + S + "/mutants_alts_rerun.out.")
row("AC4-d-r17-process-words", "2.9-prose", "course/modules/AC/AC4/L07.html, L08.html learner text", "PASS",
    "Script " + SC + "/prose_scan.py: process-word hits outside code blocks are 'built' in 'hand-built' (L07 lines 126, 315; L08 lines 113, 128), which describes the example. No process words (build, builder, round, verifier, REQUESTS, unit report).")
row("AC4-d-r17-prose-scope-words", "2.9-prose", "course/modules/AC/AC4/L07.html, L08.html scope and causal sentences (lines listed in AC4-d-2.9-prose-banned)", "PASS",
    "Each scope or causal sentence in the changed and unchanged prose was checked against a computation: 'extra capacity lowers the floor' (L07 134, direction and conditions verified), 'a choice that raises the base without raising operating income lowers both' (L08 109, verified), 'the lowest price never exceeds p_m' (L07 100, P2), 'the firm keeps Sigma whatever the price' (L07 122, Theorem 7.3 part 3), 'Same-base pairs cannot disagree' (L08 134, P3). No overreach found.")
row("AC4-d-r17-cards-scope", "2.7-cards", "cards.json AC4-c082..c134 for L07 and L08 (35 cards)", "PASS",
    "Every L07/L08 card read against the lesson text it cites. Numbers on each card occur in the lesson (for example 46, 52, 140,000 for c087/c094; 186, 75, 111, 72 for c095/c096; 4 of 28 for c109; 72.8 and 56.8 for c115/c116). No card asserts a result that the page does not prove or read off the lab output.")
row("AC4-d-r17-cards-cover", "2.7-cards", "cards.json (L07 cards c082..c096, c117; L08 cards c097..c109, c113..c116, c129, c134)", "PASS",
    "Coverage: each L07 and L08 section's claims have at least one card (definitions §1, §2 opportunity cost and gains, §3 surplus, §4 worked, §5 counts, §6 bounds, §7 misconceptions covered by c087, c088, c089; L08 definitions c097, c098, c099; §2 lemmas c103, c104; §3 c105; §4 c107, c115, c116; §5 c095, c096 (L07 counts), c102, c106, c129, c134; §6 c113, c114; §8 misconceptions c100, c101, c102).")

mutants = []
def m(name, desc, killed_by):
    e = {"id": name, "description": desc, "file": "ledgers/AC4/mutants/AC4-d-r17/" + name + ".py"}
    if killed_by:
        e["killed_by"] = killed_by
    mutants.append(e)

m("r17_L07_m01_displaced_ignores_external", "Student error: displaced units written as max(0, q - K), forgetting the outside sales E. Changes lab rows 3 and 4.", "expected block mismatch (lab output rows 3-4)")
m("r17_L07_m02_floor_no_division_by_q", "Student error: t_min written as v + D(p_m-v) without dividing by q (units lost).", "AssertionError: supplier gain at t_min nonzero (exact-check assert)")
m("r17_L07_m03_strict_nonempty", "Student error: empty range counted as t_min >= t_max (strict nonempty). Equality never occurs in the data.", None)
m("r17_L07_m04_buyer_gain_sign", "Student error: buyer gain written as q(t - r), wrong sign.", "AssertionError: buyer gain at t_max nonzero (exact-check assert)")
m("r17_L07_m05_firm_surplus_uses_price", "Student error: firm surplus adds v to the closed form, so the identity Delta_S+Delta_B=Sigma fails.", "AssertionError: supplier+buyer != firm_surplus (exact-check assert)")
m("r17_L08_m01_eva_no_tax", "Student error: NOPAT written as OI, forgetting the tax term.", "expected block mismatch (EVA column)")
m("r17_L08_m02_ratio_ge_strict", "Student error: sign identity written with strict inequalities (RI > 0 iff OI/C > r). Equality never occurs in the data.", None)
m("r17_L08_m03_capitalized_no_amortization_credit", "Student error: capitalization adds the full outlay to OI and C (no first-year amortization).", "expected block mismatch (capitalized lines)")

notes = [
    "Slice AC4-d (L07.html, L08.html, lab twins tests/labs/AC4/lab-AC4-L07-1.py and lab-AC4-L08-1.py, and the L07/L08 cards). Round 17 at pin fefbf8b; previous pin d57df1e (round-16 fragment /tmp/fanout-frags/AC4-d.round16.json, which is labelled round 6 internally and pin d57df1e; its PASS rows were re-verified, not trusted).",
    "Delta: L07.html, L08.html and both twins are byte-identical to d57df1e. cards.json changed for AC4-c091 and AC4-c102 (both changed text) and added AC4-c129 and AC4-c134 (both L08); all other card changes are in L01-L06 (not my slice).",
    "Changed prose re-verified line by line: L07 line 315 (misconception 2, unchanged), L07 line 357 (E1, unchanged), L08 line 306 (misconception 3, unchanged). No new error found in any rewritten sentence; the two FAIL rows are lab-coverage gaps, not prose errors.",
    "Hours: lesson declarations 6,7,6,6,7,6,6,6 = 50 (hub data-hours-lessons=50), project 20, total 70. No pace estimate judged.",
    "Earlier AC4 mutants: top-level ledgers/AC4/mutants/*.py are project-grader modules (outside slice AC4-d). Re-run by tools/mutate_graders.py --unit AC4 --seeds 0-4: 121/121 killed. Not counted as slice mutants.",
    "Lab-level student-error mutants written this round: nine, in ledgers/AC4/mutants/AC4-d-r17/ (a subdirectory, so the top-level grader gate does not glob them). Six killed, two survive (FAIL rows), one equivalent on the data (PASS row, kept out of the list).",
    "Could not check: tools/run_graders.py, build_site.py --check, fetch_data.py --check and the full pytest suite (outside slice AC4-d; not needed for a targeted check per the change set). No external source was opened; L07/L08 cite none. Full mypy strict on the whole project was not run; mypy was run on the two twins only.",
    "Gap, not a prose error: the lab's exact checks never reach the equality boundary of Theorem 7.3 part 2 or Lemma 8.3 (see the two FAIL rows, each with a fix).",
]

fragment = {
    "unit": "AC4",
    "slice": "AC4-d",
    "round": 17,
    "verifier": "round-17 independent Haiku verifier for slice AC4-d (L07, L08 and their lab twins); did not build AC4 and shares no context with its builders",
    "pin": "fefbf8b",
    "base": "d57df1e (previous pin; round-16 fragment /tmp/fanout-frags/AC4-d.round16.json used as context, its PASS rows re-verified or carried by byte-identical subject)",
    "checkout": "/tmp/verify17-AC4-d (detached worktree at fefbf8b, .venv symlink)",
    "scratch": S,
    "verified_at": "2026-10-28T12:00:00+00:00",
    "verdict": "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS",
    "registry_flags": [],
    "freshness_flags": [],
    "rows": rows,
    "mutants": mutants,
    "notes": notes,
    "summary": {
        "rows": len(rows),
        "PASS": sum(1 for r in rows if r["status"] == "PASS"),
        "non_PASS": sum(1 for r in rows if r["status"] != "PASS"),
        "mutants": len(mutants),
        "mutants_killed": sum(1 for x in mutants if x.get("killed_by")),
    },
}
out = sys.argv[1]
with open(out, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("rows", len(rows), "verdict", fragment["verdict"], fragment["summary"])
