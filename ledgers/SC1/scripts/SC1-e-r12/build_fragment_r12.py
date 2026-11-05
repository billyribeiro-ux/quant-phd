"""Writes ledgers/SC1/SC1-e.json (round 12) from the evidence recorded in ledgers/SC1/scripts/SC1-e-r12/."""
import datetime, json, sys

R = "ledgers/SC1/scripts/SC1-e-r12"
O = f"{R}/out"
rows = []

def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

row("SC1e-structure-ids", "2.7-cards", "course/modules/SC/SC1/cards.json", "PASS",
    f"{R}/scan_dups_r12.py on cards.json (out/dups.txt): 216 cards, 216 distinct ids, all match SC1-cNNN; lesson counts L01 23, L02 32, L03 21, L04 27, L05 35, L06 28, L07 27, L08 23 (sum 216); keys back, basis, cite, front, grade, id, lesson. Delta since 11d7077 by {R}/cards_delta.py (out/cards_delta.txt): added SC1-c222 to c230, removed SC1-c219; ids need not be contiguous.")
row("SC1e-full-read-cards", "2.7-cards", "course/modules/SC/SC1/cards.json (all 216 cards)", "PASS",
    f"All 216 fronts and backs printed by {R}/dump_cards.py into out/cards_L01.txt to cards_L08.txt and read this round. Every card was checked against its lesson text in the rows below; the 12 changed, 9 added and 1 removed card are covered by SC1e-round12-changed-cards, SC1e-c222-c223-c224-new, SC1e-c225-c226-new, SC1e-c227-c228-new, SC1e-c229-c230-new and SC1e-c219-new.")
row("SC1e-full-read-lessons", "2.9-prose", "course/modules/SC/SC1/L01.html to L08.html", "UNVERIFIABLE",
    f"Read this round, line by line, from out/L01.txt (432 lines, all), out/L02.txt lines 20 to 552, out/L03.txt lines 36 to 482 and out/L04.txt lines 36 to 400 (code lines of the lab twins were not read line by line; the twins are checked by run_labs and by the twin stdout). Not read line by line: out/L04.txt lines 400 to 468 (key results, quiz), and out/L05.txt, L06.txt, L07.txt, L08.txt apart from the statements, proofs and problems cited by cards (grep excerpts). About 150 KB of rendered text in L05 to L08 and the L04 tail were not read in full, so no complete read is claimed.",
    "Read out/L04.txt lines 400 to 468 and out/L05.txt to out/L08.txt in full, line by line (render with ledgers/SC1/scripts/SC1-e-r12/html_to_text.py), and record each section's status in the next fragment. The rest of the slice is already PASS.")
row("SC1e-near-duplicate-scan", "2.7-cards", "course/modules/SC/SC1/cards.json (all pairs)", "PASS",
    f"{R}/scan_dups_r12.py (out/dups.txt): no identical front and no identical back. difflib ratio >= 0.6 on front+back: c064/c202 0.792 (A4.2(a) linearity and A4.2(b) tower), c202/c222 0.788, c170/c218 0.718 (pairs count of Lab 1 L07/L08), c072/c226 0.713 (E[e^(theta B_t)] at theta=2 vs E[Z_t] at three theta), c116/c117 0.692, c161/c167 0.672, c030/c221 0.669, c137/c139 0.655, c011/c012 0.640 and others down to 0.6. Each pair asks a different fact (read on both cards).")
row("SC1e-learner-text-scan", "2.9-prose", "cards front and back; L01 to L08 text", "PASS",
    f"Process-word regex (builder, verifier, round, fixer, ledger, reviewer, sub-agent) over cards: one hit, SC1-c102, on 'floating-point rounding' (the mathematical sense, not the process word 'round'); no other hit. data-concept markup count in cards.json = 0. The same words searched in out/L01.txt to out/L08.txt (grep -i, whole-word 'round'): zero hits in lesson text.")
row("SC1e-card-numbers-in-lesson", "2.7-cards", "cards with a numeric token", "PASS",
    f"{R}/scan_refs_r12.py (out/scan_refs.txt): 424 numeric tokens in cards, 0 absent from the card's own lesson text (substring test, therefore weak; values recomputed in SC1e-numbers-recomputed). 282 cross-reference labels, 20 flagged only because the lesson headers write 'R2 ·', 'M2 ·' or '3Where the canon breaks' rather than 'Problem R2' or 'Section 3'; each of the 20 was confirmed by grep of its header (out/L03.txt, L05.txt, L06.txt, L07.txt, L08.txt, L01.txt).")
row("SC1e-numbers-recomputed", "2.2-numbers", "cards c010, c011, c029, c030, c051, c111 to c115, c140, c141, c148, c149, c150, c159, c170 to c174, c183, c187, c220, c221, c225, c229", "PASS",
    f"{R}/recompute_r12.py (independent, standard library, no lab code): c111 1014 triples and c112 78 pairs; c170 sum n 2^n over n=1..12 = 90114; c113 281/512, 2P(S10>2)=11/32, P(S10=2)=105/512 (Fractions); c114 495 and 495 by brute force over the 4096 walks of length 12; c129 5 of 8 by brute force; c174 densities 0.241971 and 0.109848 equal central differences of P(tau_1<=H)=0.317311 and 0.479500; c115 erfc(1/sqrt2)=0.3173105079 = 2P(B_1>1); c141 integral 0.3989422804 = 1/sqrt(2 pi); c140 sqrt(2/pi)=0.797885; c148 14893+6885=21778, 21778/65536=0.332306; c159 SE sqrt(121*279/(400^2*399))=0.022996; c171 794 walks with S12>=3 and 1588 = 2 x 794; c172 truncated means 5.48056 and 11.815731; c183 maximiser equals a^2/3; c050 identity N(4N^2-1)/3 true for N<200; c187 relative gaps of the 16 printed SEs: largest +13.21 percent at H=2, N=1, smallest -6.6 percent at H=2, N=2, all within 14 percent; c051 max |z| 2.39 at H=1, N=2, next 1.84; c220/c221 r/(1-r)^2 with r=2^(-1/2) = 8.2426; L02 Problem E3 unrounded level-1 sup 0.1165893 (|xi_11|=0.2331787 from seed 20260101), so the lesson's 0.233179 and 0.233178 statements hold (out/recompute.txt).")
row("SC1e-L03-gap", "2.5-labs", "course/modules/SC/SC1/L03.html Lab 1 expected block; cards c051, c052, c187, c225", "PASS",
    f"out/twin_L03.stdout (python -I -W error, /venv 3.14.8, exit 0, empty stderr): 16 z values; largest |z| 2.39 at H=1, N=2, next largest 1.84 at H=1, N=128; printed SE at H=2, N=1 is 0.1601 against 2 sqrt2/20 = 0.141421, +13.2 percent; H=2, N=128 SE 0.0125 against 0.0125. The card and key-result row match.")
row("SC1e-labs-run", "2.5-labs", "tests/labs/SC1/lab-SC1-L01-1.py to lab-SC1-L08-1.py and project twins", "PASS",
    "out/run_labs.txt: 'run_labs SC1: PASS (11/11)' at 5db69a9, exit 0. Twins also run alone under .venv python -I -W error (exit 0 for L01 to L08; out/twin_L0*.stdout, twin_L0*.stderr empty).")
row("SC1e-labs-page-equals-twin", "2.5-labs", "course/modules/SC/SC1/L01.html to L08.html (data-run and expected blocks)", "PASS",
    "run_labs --unit SC1 (out/run_labs.txt) compares each lab's page code with its twin and runs the expected block against the output; PASS 11/11 at 5db69a9.")
row("SC1e-page-smoke", "2.9-prose", "course/modules/SC/SC1/ (all pages)", "PASS",
    f"out/page_smoke.txt: 'page_smoke SC1: PASS' with L01 to L08, project.html, index.html, concepts.html and review.html each PASS (zero console errors, all labs run, grader 134 tests pass in browser).")
row("SC1e-check-pages-dag", "2.9-prose", "course/modules/SC/SC1/", "PASS",
    "out/check_pages.txt: 'check_pages SC1: PASS'; out/check_dag.txt: 'check_dag SC1: PASS' (both run at 5db69a9).")
row("SC1e-delta-read", "2.9-prose", "cards.json and L01 to L05 html since 11d7077 (index.html and project.html are outside this slice)", "PASS",
    "out/delta_lessons.diff (162 lines, every hunk read): L01 §2 (b) and §4 proof wording; L02 Lemma 2.3 (H2 adds A1(a)), its induction-step proof, Assumption 2.1 quiz note and key-results row; L03 §1 wording (n for dyadic depth), Lab 1 key-results row; L04 Assumption 4.2 (adds (e), restates (c)), Propositions 2.2 to 2.4 proofs, §3 and misconceptions; L05 why-it-matters only. out/cards_delta.txt lists every card change: 12 changed, 9 added, 1 removed.")
row("SC1e-c048-round7", "2.7-cards", "course/modules/SC/SC1/cards.json card SC1-c048; L03.html Theorem 2.3", "PASS",
    f"Card c048 is unchanged (absent from out/cards_delta.txt). L03.txt lines 78 to 96 state Theorem 2.3: Q(P_n) -> t in mean square with E[(Q-t)^2] = 2 sum Delta_k^2 <= 2 t |P| under Assumptions 3.1 and 3.2; the card's 'at most 2t|P_n|' and 'Q(P_n) to t in mean square' agree.")
row("SC1e-L01-statements", "2.7-cards", "course/modules/SC/SC1/L01.html; cards c001 to c017, c186, c206 to c210", "PASS",
    "All 23 L01 cards read against out/L01.txt: Definition 1.1 (D1)-(D3) (lines 42-50), Proposition 1.2 hypotheses H1 and H2 (A1(a)) and proof (lines 72-86), Remark 1.3 (H2 A1(b), A1(a)) (lines 88-98), Example 1.4 (lines 104-114), Lab 1 counts 15 of 15 and 81 of 81 (lines 184-189, twin output), §4 items (lines 199-201, c011 to c013 new wording), §5 misconceptions (lines 209-219), A1(a) to A1(e) (lines 58-66). Card numbers and grades match.")
row("SC1e-L02-statements", "2.7-cards", "course/modules/SC/SC1/L02.html; cards c018 to c041, c184, c185, c211 to c213, c220 to c224", "PASS",
    "All 32 L02 cards read against out/L02.txt: hats Definition 2.1 (lines 46-52), Lemma 2.2 (a)-(e) (lines 56-72), Assumption 2.1 (a)-(c) (lines 78-82), Lemma 2.1 (lines 88-102), Lemma 2.3 H2 and proof (lines 108-127), Proposition 2.4 (a) P(E_m^c)<=2^(-m) (line 143-145), (b) steps 1-4 (lines 147-156), A2 and sketch (lines 271-275), Theorem 2.5 (lines 283-287), Remark 2.6 (lines 295-305), misconceptions (lines 323-333), lab counts 216 of 216 and 8 of 8 (lines 254-264, twin output). c220 says 'lim P(A_m0) >= 1' where the claim is equality; with P <= 1 this is a wording point, not a defect.")
row("SC1e-L03-statements", "2.7-cards", "course/modules/SC/SC1/L03.html; cards c042 to c060, c187, c188, c225", "PASS",
    "All 21 L03 cards read against out/L03.txt: Definition 1.1 (lines 40-46), Assumptions 3.1 and 3.2 (lines 48-54), Lemmas 2.1 and 2.2 (lines 58-76), Theorem 2.3 (lines 80-96), Proposition 2.4 (lines 100-108, closed form by induction), lab z-table and exact sums (lines 195-229), Section 3 canon breaks (lines 237-241), misconceptions (lines 249-257), problems M1 to M3, P1 to P3, E1 to E3, R1 to R3 (lines 267-367), key results (lines 373-381).")
row("SC1e-L04-statements", "2.7-cards", "course/modules/SC/SC1/L04.html; cards c061 to c082, c202 to c204, c222, c226", "PASS",
    "Read against out/L04.txt lines 36-400: Assumption 4.1 (line 48), Assumption 4.2 (a)-(e) (line 54), Definition 1.2 (line 58), Lemma 2.1 (lines 64-72), Propositions 2.2, 2.3 (with the remark, lines 80-110), Proposition 2.4 and proof (lines 118-128), lab quadrature output (lines 201-207, twin), section 3 and misconceptions (lines 215-235), problems M1 to M3, P1 to P3, E1 to E3, R1 to R3 (lines 245-345). Lines 400 to 468 (key results and quiz) not read; no card cites them except by reference to the problems above.")
row("SC1e-L05-statements", "2.7-cards", "course/modules/SC/SC1/L05.html; cards c083 to c105, c189, c193 to c200, c214, c227, c228", "PASS",
    "Per card, against the statement or proof each cites in out/L05.txt: Assumptions A4(a)-(i) (lines 44-60, c193 to c200 and c214 match), Definitions 1.1 and 1.2 (lines 66-74), Lemma 1.3 (lines 78-92), Theorem 1.4 and Remark 1.5 (lines 100-120), Lemma 2.2 and Theorem 2.1 (lines 138-166), lab outputs (out/twin_L05.stdout, 225 cases, gap 5.55e-16 vs tolerance 1e-6), Section 3 A3 (lines 262-282), problems R1 to R3 (lines 388-410), M2, M3, P2 (lines 324-350), misconceptions (lines 294-300). Not read: the remainder of L05 (see SC1e-full-read-lessons).")
row("SC1e-L06-statements", "2.7-cards", "course/modules/SC/SC1/L06.html; cards c106 to c133, c217", "PASS",
    "Per card, against out/L06.txt: Definition 1.1 and Lemma 1.2 (lines 42-50), Proposition 1.3 and Corollary 1.4 (lines 56-80), Lemma 2.1 (lines 86-98), Definition 2.2 and Proposition 2.3 (lines 100-118), Remark 2.4 (lines 134-136), Theorem 2.5 and Corollary 2.6 (lines 138-166), problems M1 to M3, P2, P3, R1 to R3 (lines 326-430), misconceptions and lab (lines 292-316, twin output). Lab counts 1014, 78, 495, 281/512, 11/32, 105/512 match out/twin_L06.stdout.")
row("SC1e-L07-statements", "2.7-cards", "course/modules/SC/SC1/L07.html; cards c134 to c159, c191, c215, c229, c230", "PASS",
    "Per card, against out/L07.txt: Definitions 1.1, 1.2 (lines 42-46), Theorem 1.3 with H1 to H3 (lines 50-58), Remark 1.4 (lines 64-66), Corollary 1.5 (lines 68-74), Assumption A5 (lines 76-78), Definition 2.1, Proposition 2.2, Corollary 2.3, Remark 2.4 (lines 96-120), problems M2, R1, R2, R3, E2, E3 (lines 388-474), lab twin (out/twin_L07.stdout: 0.2275, 0.3025, 0.7586, se 0.0317, nesting violations 0, 0.0393 = 1.24 SE).")
row("SC1e-L08-statements", "2.7-cards", "course/modules/SC/SC1/L08.html; cards c161 to c183, c201, c205, c218", "PASS",
    "Per card, against out/L08.txt: Definition 1.1 and Proposition 1.2 (lines 42-52), Corollary 1.3 (lines 58-64), Corollary 1.4 (lines 66-72), Corollary 1.5 (lines 74-80), Remark 1.6, Definition 2.1, Proposition 2.2 and 2.3 (lines 90-108), Section 3 jump example (line 332), problems M3, E1 to E3, R1 to R3 (lines 414-456), lab twin (out/twin_L08.stdout: 90114 pairs, counts 512 0 384 0 288 0 224 0 180 0, 1588, 0.387695, 0.193848, densities 0.241971 and 0.109848, P 0.317311 and 0.479500).")
row("SC1e-assumption-labels", "2.7-cards", "cards naming A1 to A5, A4(a)-(i), Assumption 2.1, 3.1, 3.2, 4.1, 4.2(a)-(e)", "PASS",
    "A1(a)-(e) cards c206 to c210 match out/L01.txt lines 58-66; A2 card c033 matches out/L02.txt lines 271-273; A3 card c093 and c098, c099 match out/L05.txt lines 262-282 and out/L07.txt; A4(a)-(i) cards c193 to c200 and c214 match out/L05.txt lines 44-60; A5 card c215 matches out/L07.txt lines 76-78; Assumption 2.1 (a)-(c) cards c211 to c213 match out/L02.txt lines 78-82; Assumption 3.1 and 3.2 cards c188 and c060 match out/L03.txt lines 48-54; Assumption 4.1 card c063 matches out/L04.txt line 48; Assumption 4.2 (a)-(e) cards c064, c202, c203, c204, c222 match out/L04.txt line 54.")
row("SC1e-cross-references", "2.7-cards", "cards naming Problems, Sections, Lab parts and numbered results", "PASS",
    f"{R}/scan_refs_r12.py (out/scan_refs.txt): 282 labels, 20 flagged for header format only, each confirmed in the lesson header text (e.g. 'R1 · A time of maximum' in out/L05.txt line 388; 'E2 · Recomputing an exact tail' in out/L07.txt line 440; '4Where the canon breaks' in out/L01.txt line 195 for c017's 'Section 4').")
row("SC1e-hypotheses-carried", "2.4-mathematics", "cards for Lemma, Proposition, Theorem, Corollary and Remark statements", "PASS",
    "Hypotheses on each card checked against the lesson's (H1), (H2), (H3) lines: Proposition 1.2 (H2 A1(a)), Remark 1.3 (H2 A1(b), A1(a)), Lemma 2.3 (H2 A1(a), A1(b), A1(c), A1(e) on out/L02.txt line 108), Remark 2.6 (H2 out/L02.txt line 293), Propositions 2.2 to 2.4 of L04 (H1, H2 lines 76-78, 92-94, 114-116), Theorem 1.3 of L07 (H1 to H3 lines 52-56), Corollary 1.3 to 1.5 of L08 (H1, H2 of Proposition 1.2 and A3, A4 line 60, 68, 76), Corollary 1.5(b) (A5). c140 carries H1, H3 as the lesson states.")
row("SC1e-grades-audit", "2.3-grades", "cards grade field (T 125, C 27, none 64)", "PASS",
    "grade counts from cards.json: T 125, C 27, None 64 (definitions, assumptions and problems that make no claim). Every C card is a lab or simulation result (c010, c037, c038, c051, c072, c091, c092, c111 to c114, c127, c149, c150, c170 to c174, c187, c216, c218, c225, c226, c229, c230 and the lab counts); every T card states a result proved on the page, or a Remark or Problem of the page, under the assumptions it names. No lab-only claim is graded T.")
row("SC1e-cites-and-registry", "2.1-citations", "course/modules/SC/SC1/cards.json cite fields", "PASS",
    "cite is empty on all 216 cards (scan). The slice cites no registry key. The L03 reference note (Shreve, registry key shreve2004stochastic) is not cited by any card, and the lesson says no passage is attributed to it (out/L03.txt line 474).")
row("SC1e-notation", "2.4-mathematics", "cards and L01 to L08 text; notation/notation.json", "PASS",
    "notation/notation.json: T = number of return observations; Phi = standard normal CDF (cards c104, c137 to c141, c155, c156, c164, c165, c191, c201 use Phi as the normal CDF, the same meaning). Lesson L03 out/L03.txt line 100 says the program reserves T for the observation count and writes the endpoint as H. No card or lesson uses T for a time. The other registry symbols (gamma_3, gamma_4, R^*, R^(e*), R_f, Q) do not appear in this slice's cards.")
row("SC1e-dag", "2.9-prose", "cards; L01 to L08 text; check_dag", "PASS",
    "out/check_dag.txt: 'check_dag SC1: PASS'. Cards use concepts introduced in the card's own lesson or the prerequisites named in that lesson's Uses line near the top (e.g. out/L05.txt line 20 names stopping time and filtration from M6).")
row("SC1e-scope-words", "2.9-prose", "cards and the changed lesson text", "PASS",
    "Scope words in the changed text checked: 'in general' (c223, uncorrelated not independent in general, true), 'for every M >= m_0' (c224, proof step 3, true), 'exactly' (c037, c030 closed form, verified by recompute), 'all 16 values' (c225, verified 16 z values within 3), 'within 14 percent' (c187, max 13.21), 'no other |z| exceeds 1.84' (c051, verified), 'for every t >= 0' (c080 R2, lesson statement).")
row("SC1e-r8-twin-docstring-only", "2.5-labs", "tests/labs/SC1/ twins", "PASS",
    "Twins unchanged since 11d7077 (git diff --quiet 11d7077a 5db69a9b -- tests/labs/SC1: no difference). Carried from round 11 (tests/labs/SC1/*.py byte-identical since the previous pin 11d7077): the docstring-only finding is not reopened. Re-run this round: each twin exits 0 under .venv/bin/python -I -W error with empty stderr (out/twin_L0*.stderr).")
row("SC1e-c052-term", "2.7-cards", "course/modules/SC/SC1/cards.json card SC1-c052 front and back", "PASS",
    "c052 back: H sqrt(2/N)/20 with t=H; Var(Q)=2H^2/N by Problem R1 of L03 (out/L03.txt lines 345-351: E[(Q-t)^2]=2t^2/N); sqrt(400)=20. Lesson Lab 1 text (out/L03.txt line 114) gives the same formula. Matches.")
row("SC1e-c150-assumption-reference", "2.7-cards", "course/modules/SC/SC1/cards.json card SC1-c150 back", "PASS",
    "c150 back now reads '0.7586, with standard error 0.0317.' The lab prints 'N = 256 steps: mean grid maximum 0.7586, se 0.0317' (out/twin_L07.stdout). The assumption reference was removed from the card and is not needed for this lab value.")
row("SC1e-c140-hypotheses", "2.7-cards", "course/modules/SC/SC1/cards.json card SC1-c140 front", "PASS",
    "c140 front names H1 (standard BM with continuous paths and B_0=0), H (H>0 fixed), A3 and A4 of Lesson 5, and A5 for part (b). Matches out/L07.txt lines 68-78 (Corollary 1.5 assumptions: those of Theorem 1.3 for part (a), and A5 additionally for part (b)).")
row("SC1e-c219-new", "2.7-cards", "cards.json (card SC1-c219, removed at 5db69a9)", "PASS",
    "SC1-c219 is absent from cards.json at 5db69a9 (out/cards_delta.txt: removed ['SC1-c219']). grep for SC1-c219 in course/modules/SC/SC1/*.html returns 0 in every lesson and project page (no dangling reference). The round 11 row checked c219 as an L01 card; that subject no longer exists, so the row is re-verified by its removal.")
row("SC1e-c220-c221-new", "2.4-mathematics", "cards SC1-c220, SC1-c221 (L02)", "PASS",
    "c220 P(Omega*)=1: out/L02.txt lines 143-145 give P(E_m^c)<=2^(-m), P(A_m0^c)<=2^(1-m0), continuity from below (Assumption 2.1(c)), and P(Omega*)=1; wording point noted in SC1e-L02-statements. c221 sum m r^m = r/(1-r)^2 for r=2^(-1/2) finite (out/L02.txt line 150; numeric 8.2426, out/recompute.txt).")
row("SC1e-c029-c030-changed", "2.4-mathematics", "cards SC1-c029, SC1-c030", "PASS",
    "c029 P(E_m^c)<=2^(-m): 2^(m-1) * 2 e^(-lambda_m^2/2) with lambda_m^2 = 4m log 2 gives 2^(m-1) * 2 * 2^(-2m) = 2^(-m) (out/L02.txt line 144). c030 M_m = lambda_m 2^(-(m+1)/2) = sqrt(2 log 2) sqrt(m) 2^(-m/2): m=3 gives 0.721013, equal to the lab's printed bound at m=3 (out/twin_L02.stdout).")
row("SC1e-c011-c013-changed", "2.4-mathematics", "cards SC1-c011, SC1-c012, SC1-c013 (L01 section 4)", "PASS",
    "out/L01.txt line 199 gives the construction (Remark 2.6 of Lesson 2, Assumptions A1(a), A1(b), A1(e), A2 and Assumption 2.1, product space with U uniform and independent of B). Line 219: P(U in G)=0 for finite G gives the same finite-dimensional laws, (D1)-(D3) hold, and B-tilde is discontinuous at U on every outcome. c011 (laws), c012 (B_U+1, discontinuity), c013 (continuity event holds for B on every outcome and for B-tilde on none) match.")
row("SC1e-L08-changed-cards", "2.7-cards", "cards SC1-c162, c165, c171, c201 (L08)", "PASS",
    "c162 matches out/L08.txt Proposition 1.2 (lines 46-52, equality of events on every continuous path). c165 matches Corollary 1.5 (line 76, density a/(sqrt(2 pi) H^(3/2)) exp(-a^2/(2H))). c171 counts 512, 0, 384, 0, 288, 0, 224, 0, 180, 0 and 1588, 0.387695, 0.193848 match out/twin_L08.stdout. c201 values 0.317311 and 0.1586552539 match out/twin_L08.stdout and out/twin_L07.stdout.")
row("SC1e-lab-outputs-cards", "2.5-labs", "cards backed by a lab (c010, c037, c038, c051, c072, c091, c092, c111 to c114, c127, c149, c150, c170 to c174, c187, c216, c218, c225, c226, c229, c230)", "PASS",
    "Each card's printed value compared with out/twin_L0N.stdout: L01 81 of 81 pairs; L02 216 of 216 and 8 of 8; L03 z table (16 values) and SE 0.1601, 0.0125; L04 1.000000000 and 54.598150033; L05 225 cases, gap 5.55e-16 (tolerance 1e-6), mass 3.81e-29, integrals 1.0000000000; L06 1014, 78, 495, 281/512, 11/32, 105/512, 0.3173105079; L07 0.2275, 0.3025, 0.7586, 0.0317, 0, 0.332306; L08 90114, 1588, 5.480560, 11.815731, 24.557203, 0.317311, 0.241971, 0.479500, 0.109848, 78 of 78.")
row("SC1e-c222-c223-c224-new", "2.7-cards", "cards SC1-c222, SC1-c223, SC1-c224 (L04 4.2(e); L02 Lemma 2.3, Proposition 2.4(b))", "PASS",
    "c222 Assumption 4.2(e) E[1|G]=1 matches out/L04.txt line 54. c223 (Lemma 2.3, joint normality of U_j, V_j from one family, then A1(c) gives independence) matches out/L02.txt lines 123-125 and quiz line 523. c224 (sup|Sigma - Sigma_M| <= sum_{m>M} M_m for M >= m_0) matches out/L02.txt lines 152-154.")
row("SC1e-c225-c226-new", "2.5-labs", "cards SC1-c225 (L03 Lab 1), SC1-c226 (L04 Lab 1)", "PASS",
    "c225: out/twin_L03.stdout z values -- all 16 lie within +/-3 (largest 2.39). c226: out/twin_L04.stdout: E[Z_t] = 1.000000000 for theta -1, 0.5, 2, equal to Z_0 = 1 within 1e-9 (the card's 'at each of the three values').")
row("SC1e-c227-c228-new", "2.4-mathematics", "cards SC1-c227, SC1-c228 (L05 Problems R2, R3)", "PASS",
    "c227 F_s subset F_rho for the constant time rho = s: out/L05.txt line 402 ('Here F_s subset F_rho'). c228: out/L05.txt line 410, {rho_n <= r} = {rho <= k/2^n}, k = floor(2^n r), inside F_{k/2^n} subset F_r. Both match.")
row("SC1e-c229-c230-new", "2.5-labs", "cards SC1-c229, SC1-c230 (L07 Lab 1 parts C and B)", "PASS",
    "c229: 0.797885 - 0.7586 = 0.0393 and 0.0393/0.0317 = 1.24 SE (out/twin_L07.stdout). c230: 'pathwise violations (coarse maximum above fine maximum): 0' (out/twin_L07.stdout).")
row("SC1e-round12-changed-cards", "2.7-cards", "cards SC1-c026, c027, c028, c032, c051, c072, c095, c096, c149, c150, c203, c207 (the twelve changed cards)", "PASS",
    "Each changed card compared with its old and new text (out/cards_delta.txt) and with the lesson text: c026 and c027, c028 match L02 Lemma 2.3 (H2 and the induction step, out/L02.txt lines 108, 123); c032 matches Proposition 2.4(b) conclusion; c051 matches out/twin_L03.stdout; c072 matches out/twin_L04.stdout (theta=2 only); c095 and c096 match out/L05.txt lines 402 and 410; c149 and c150 match out/twin_L07.stdout; c203 matches out/L04.txt line 54 with (e); c207 matches out/L01.txt line 60 (A1(b)).")
row("SC1e-round12-lesson-hunks", "2.9-prose", "L01 to L05 hunks since 11d7077 (delta_lessons.diff)", "PASS",
    "Every changed hunk read (out/delta_lessons.diff, 162 lines): L01 A1(b) wording (§2) and the §4 wording (which cites A1(a), A1(b), A1(e)); L02 Lemma 2.3 H2, proof (cross term by A1(a); joint normality then A1(c); A1(e) grouping) and key results row; L02 quiz note; L03 dyadic depth wording n and key-results row with the 13.2 percent figure (checked by the twin); L04 Assumption 4.2 with (e) and the uses of (a), (c), (e) in the proofs of Propositions 2.2 to 2.4 and §3, misconceptions and P1; L05 why-it-matters only. Every use of an assumption part in the changed proofs is one listed in the assumption.")
fragment = {
    "unit": "SC1",
    "slice": "e",
    "round": 12,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-e: all cards of course/modules/SC/SC1/cards.json (216) against lessons L01 to L08; round 12",
    "pin": "5db69a9bee460736c318ebfacc7200ee5a6eb0f0",
    "base": "11d7077a290f7960b183d3a5a6631af4773888f9",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE12-SC1-e",
    "scratch": f"{O}",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "verdict": "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [
        "Gates run at 5db69a9: check_pages SC1, check_dag SC1, run_labs SC1 (11/11), page_smoke SC1 (all pages PASS), twins under .venv python -I -W error (exit 0).",
        "Not run: ruff, mypy, pytest, verify_refs. No Python module outside the lab twins changed in the range; tests/labs, tools, notation and references are byte-identical since 11d7077; the slice cites no registry key.",
        "Out of slice and not verified here: course/modules/SC/SC1/index.html and project.html (changed in the same range), grader/test_project.py.",
    ],
    "notes": "Round 12 at 5db69a9 (delta base 11d7077). Changed since round 11: L01, L02, L03, L04 (statements and hunks read), cards.json (12 changed, 9 added c222 to c230, 1 removed c219). The round 11 UNVERIFIABLE row SC1e-full-read-lessons is NOT cleared: L04 lines 400 to 468 and L05 to L08 were not read line by line. The only non-PASS row of round 11 (SC1e-full-read-lessons) is still non-PASS. No card defect found in this round; the one process-word regex hit (c102, 'floating-point rounding') is a false positive. Scripts: ledgers/SC1/scripts/SC1-e-r12/.",
    "summary": "",
}
n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_unv = sum(1 for r in rows if r["status"] == "UNVERIFIABLE")
n_fail = sum(1 for r in rows if r["status"] == "FAIL")
fragment["summary"] = f"SC1 slice e round 12 at 5db69a9: {len(rows)} rows; PASS {n_pass}, FAIL {n_fail}, UNVERIFIABLE {n_unv}. Non-PASS: SC1e-full-read-lessons (L04 lines 400-468 and L05-L08 not read line by line). Verdict {fragment['verdict']}."
out = sys.argv[1]
with open(out, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=2)
print("wrote", out, len(rows), "rows", fragment["verdict"])
