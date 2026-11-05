"""Build the round-13 verifier fragment for SC1 slice e (cards.json against lessons L01 to L08).

Usage: python -I build_fragment_r13.py <checkout> <out_fragment.json>
Every evidence string names a script or gate output under ledgers/SC1/scripts/SC1-e-r13/out/.
"""
import json
import sys

OUT = "ledgers/SC1/scripts/SC1-e-r13/out"
SCR = "ledgers/SC1/scripts/SC1-e-r13"

rows = []


def row(rid, check, location, evidence, status="PASS", fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


row("SC1e-structure-ids", "2.7-cards", "course/modules/SC/SC1/cards.json",
    f"{SCR}/scan_dups_r13.py on cards.json ({OUT}/dups.txt): 217 cards, 217 distinct ids, all match SC1-cNNN; "
    "lesson counts L01 23, L02 32, L03 21, L04 27, L05 35, L06 28, L07 28, L08 23 (sum 217); keys back, basis, cite, "
    "front, grade, id, lesson on every card; grade counts T 125, C 28, none 64. Round-13 delta from 5db69a9 "
    "(git diff, out/delta_5db69a9_e919577.diff): c231 added (L07, grade C), c126 and c201 back text changed, nothing removed.")
row("SC1e-full-read-cards", "2.7-cards", "course/modules/SC/SC1/cards.json (all 217 cards)",
    f"All 217 fronts and backs dumped by {SCR}/dump_cards.py into {OUT}/cards_L01.txt to cards_L08.txt "
    f"(concatenated {OUT}/cards_all.txt, 868 lines) and read in full this round. Each card is checked against its lesson "
    "text in the rows below (L01 to L08 statement rows, the changed-card rows, and the numbers rows).")
row("SC1e-full-read-lessons", "2.9-prose", "course/modules/SC/SC1/L01.html to L08.html",
    "Round 12 left this row UNVERIFIABLE (L04 lines 400 to 468 and L05 to L08 not read). Round 13 renders each lesson with "
    f"{SCR}/html_to_text.py and reads every line of each dump: L01 {OUT}/L01.txt 432 lines; L02 L02.txt 552; L03 L03.txt 482; "
    "L04 L04.txt 468; L05 L05.txt 525; L06 L06.txt 547; L07 L07.txt 600; L08 L08.txt 580. The lab code blocks in the dumps "
    "are read too, and each expected block is compared with the twin stdout by run_labs (row SC1e-labs-page-equals-twin). "
    "No prose defect was found in this full read.")
row("SC1e-near-duplicate-scan", "2.7-cards", "course/modules/SC/SC1/cards.json (all pairs)",
    f"{SCR}/scan_dups_r13.py ({OUT}/dups.txt): no identical front and no identical back. difflib ratio >= 0.6 on front plus back: "
    "max 0.792 (c064/c202, the A4.2(a) linearity card and the tower card), then c202/c222 0.788, c170/c218 0.718, c072/c226 0.713, "
    "c116/c117 0.692 (Lemma 2.1(i) and (ii), different claims), c161/c167 0.672 (tau_a and nu_a definitions), c030/c221 0.669, "
    "c137/c139 0.655 (Theorem 1.3 and Corollary 1.5(a)). Each pair asks a different claim (read in the card dump).")
row("SC1e-learner-text-scan", "2.9-prose", "cards front and back; L01 to L08 text",
    "Process-word regex (builder, verifier, round, fixer, ledger, reviewer, sub-agent) over cards: one hit, SC1-c102, on "
    "'floating-point rounding' (mathematical sense, not the process word). Same words over the lesson dumps: no hit. "
    "Banned-phrase scan (BUILDER_RULES 1.3 and 1.4: TODO, TBD, lorem, for brevity, omitted, beyond the scope, exercise, "
    "obviously, clearly, historically, roughly, well known, important to note, studies show, you can add more) over "
    f"{OUT}/L01.txt to L08.txt and cards_all.txt: no hit.")
row("SC1e-card-numbers-in-lesson", "2.7-cards", "cards with a numeric token",
    f"{SCR}/scan_refs_r13.py ({OUT}/scan_refs.txt): 425 numeric tokens in cards, 0 absent from the card's own lesson text "
    "(substring test, therefore weak; values recomputed in SC1e-numbers-recomputed). 284 cross-reference labels, 20 absent "
    "only because the lesson headers use another format ('R1 · title', '3Where the canon breaks'); each header was read, e.g. "
    "L05 'R2 · A3 at a deterministic time' for c227 and c095, L07 'M2 · Scaling' for c155, L01 '4Where the canon breaks' for c017.")
row("SC1e-numbers-recomputed", "2.2-numbers",
    "cards c010, c011, c029, c030, c051, c111 to c115, c140, c141, c148, c149, c150, c159, c170 to c174, c183, c187, "
    "c220, c221, c225, c229 to c231, and the lesson prose numbers",
    f"Recomputed by hand and by scripts (standard library, no lab code): {SCR}/e3_l02_check.py ({OUT}/e3_l02_check.txt): "
    "xi_{1,1}=0.2331786895, observed level-1 sup 0.116589, twice the unrounded sup 0.233179, twice the printed 0.116589 "
    "0.233178, bound lambda_1/2 = 0.832555 (the L02 E3 sentence). c111 1014 triples = sum over n of n(n+1)/2 + n^2 (summed); "
    "c112 78; c113 281/512, 11/32, 105/512 (Fractions, in the lab output); c114 495 = C(12,8). c170 sum n 2^n = 90114. "
    f"c171 hitting-time theorem gives counts 512, 384, 288, 224, 180 at steps 3, 5, 7, 9, 11 (sum 1588), 794 = P(S_12>=3) count "
    f"({SCR}/l08_check.py, {OUT}/l08_check.txt). c172 E[min(nu_1,16)] = 179587/32768 = 5.480560302734375 exactly, "
    "11.815731 at 64, 24.557203 at 256. c174 erfc(1/sqrt2)=0.3173105079, erfc(0.5)=0.4795001222, f_1(1)=0.241971, f_1(2)=0.109848. "
    f"c148 21778 = 14893 + 6885 ({OUT}/l07_check.txt). c149 91, 107, 113, 121 of 400; SE 0.0210 and 0.0230 by "
    "sqrt(p(1-p)/(n-1)). c150 and c229 gap 0.797885-0.7586 = 0.0393, 0.0393/0.0317 = 1.24 SE. c159 sqrt(33759/63840000)=0.0230. "
    "c187 largest SE gap +13.21 percent (H=2, N=1) from {SCR}/l03_check.py ({OUT}/l03_check.txt). c225 all 16 z within 2.39. "
    "c230 0 violations. c231 78 pairs. L04 e^1, e^(1/4), e^4 match the printed lines; e^8 = 2980.957987042 (computed this round) gives the 2980.957987 printed in E2 and E3.")
row("SC1e-L03-gap", "2.5-labs", "course/modules/SC/SC1/L03.html Lab 1 expected block; cards c051, c052, c187, c225",
    f"{OUT}/twin_L03.stdout (python -I -W error, exit 0, empty stderr): 16 z values; l03_check.py: max |z| 2.39 at H=1, N=2, "
    "second largest 1.84 at H=1, N=128, so 'no other |z| exceeds 1.84' is true; printed SE at H=2, N=1 is 0.1601 against "
    "2 sqrt2/20 = 0.141421, +13.21 percent; largest gap is the one named, and it is within 14 percent; H=2, N=128 SE 0.0125 "
    "against 0.0125.")
row("SC1e-labs-run", "2.5-labs", "tests/labs/SC1/lab-SC1-L01-1.py to lab-SC1-L08-1.py",
    f"{OUT}/run_labs.txt: 'run_labs SC1: PASS (11/11)', exit 0 at e919577. Each lesson twin run alone by {SCR}/run_twins_r13.sh "
    f"under .venv (Python 3.14.8) with python -I -W error from an empty scratch directory: exit 0 for L01 to L08, stderr empty "
    f"(out/twin_L0*.stderr 0 bytes); stdout identical to the round-12 stdout for every lesson. Lesson twins byte-identical since 5db69a9.")
row("SC1e-labs-page-equals-twin", "2.5-labs", "course/modules/SC/SC1/L01.html to L08.html (data-run and expected blocks)",
    f"run_labs --unit SC1 ({OUT}/run_labs.txt) compares each page's code block with its twin and runs each expected block against "
    "the output: PASS 11/11 at e919577. Every expected block in the dumps (L01 lines 184 to 189, L02 254 to 265, L03 195 to 229, "
    "L04 201 to 207, L05 247 to 254, L06 268 to 284, L07 320 to 342, L08 305 to 324) was read against its twin stdout.")
row("SC1e-page-smoke", "2.9-prose", "course/modules/SC/SC1/ (all pages)",
    f"{OUT}/page_smoke.txt: 'page_smoke SC1: PASS', exit 0; each of index, L01 to L08, project.html PASS (zero console errors, "
    "no external requests, all labs run in 0.0 to 1.6 s, grader 136 tests in the browser ('All 136 tests pass on seed 1411571599'). A single-page run "
    "(page_smoke --unit SC1 --pages modules/SC/SC1/L01.html) also printed PASS.")
row("SC1e-check-pages-dag", "2.9-prose", "course/modules/SC/SC1/",
    f"{OUT}/check_pages.txt: 'check_pages SC1: PASS' (exit 0); {OUT}/check_dag.txt: 'check_dag SC1: PASS' (exit 0); "
    f"{OUT}/build_site_check.txt: 'site data current: 6 outputs', exit 0; verify_refs --offline: '560 entries, 0 problems' "
    f"({OUT}/verify_refs.txt). Independent DAG reading of the concept links in L01 to L08: each is on its lesson's Uses line, "
    "introduced by an earlier lesson of this unit, or from M4, M5, M2 or M6 (the prerequisite closure; check_dag PASS). The one "
    "link not on a Uses line is probability-space in L04 line 40, from M6. M6 cross-references checked (L04 line 219 M6 L08 'Filtrations and discrete-time "
    "martingales' exists; L05 line 260 M6 L09 Definition 9.1 is the stopping-time definition).")
row("SC1e-delta-read", "2.9-prose", "cards.json and the lesson hunks changed since 5db69a9 (out/delta_5db69a9_e919577.diff, 373 lines)",
    "Every hunk of the course/modules/SC/SC1 and tests/labs/SC1 delta read: cards.json (c126 back, c201 back, c231 added); "
    "L01 section 2 wording (D1); L02 Lemma 2.3 consequence paragraph, interpretation paragraph, R2 solution; L03 why-it-matters "
    "and Assumption 3.2 wording; L05 A4(i) wording and M1 solution; L07 meta description, hypothesis paragraph, E2 and E3 "
    "wording; L08 Corollary 1.4 proof index change and M1 solution; L01 to L08 index and project pages, grader and "
    "lab-SC1-project-1 are outside this slice. Each changed claim was rechecked against its proof or lab output (rows below).")
row("SC1e-c048-round7", "2.7-cards", "course/modules/SC/SC1/cards.json card SC1-c048; L03.html Theorem 2.3",
    "c048 is not in the 5db69a9 to e919577 diff. L03 lines 80 to 96 (Theorem 2.3): E[(Q-t)^2] = 2 sum Delta_k^2 <= 2 t |P|, "
    "so Q(P_n) to t in mean square under Assumptions 3.1 and 3.2; the card's 'at most 2t|P_n|' and 'to t in mean square' agree.")
row("SC1e-L01-statements", "2.7-cards", "course/modules/SC/SC1/L01.html; cards c001 to c017, c186, c206 to c210",
    f"All 23 L01 cards read against {OUT}/L01.txt: Definition 1.1 (D1)-(D3) (lines 42-50), Proposition 1.2 (H1, H2 A1(a); proof lines "
    "80-86), Remark 1.3 (H2 A1(b), A1(a); lines 90-98), Example 1.4 (lines 106-114), Lab 1 counts 15 of 15 and 81 of 81 "
    "(lines 184-189), section 4 construction (lines 199-203, cards c011-c013 with Remark 2.6 of Lesson 2), section 5 "
    "misconceptions (lines 209-219), problem and quiz items. Hypotheses on the cards match the lesson hypothesis lines.")
row("SC1e-L02-statements", "2.7-cards", "course/modules/SC/SC1/L02.html; cards c018 to c041, c184, c185, c211 to c213, c220 to c224",
    f"All 32 L02 cards read against {OUT}/L02.txt: hats (lines 48-51), Lemma 2.2 (a)-(e) and proof (lines 60-72), Assumption 2.1 "
    "(lines 78-82), Lemma 2.1 (lines 88-102), Lemma 2.3 H2 (line 108) and induction step (lines 116-125), consequence (line 127), "
    "Proposition 2.4 (a) with P(E_m^c)<=2^(-m) (lines 143-145), (b) steps 1-4 (lines 147-156), Assumption A2 (lines 271-275), "
    "Theorem 2.5, Remark 2.6 (lines 289-305), section 4 and 5, problems M1-M3, P1-P3, E1-E3, R1-R3. The c037 count 216 = "
    "2*9+3*8+5*7+9*6+17*5 and 36 pairs cover 17 distinct points: checked.")
row("SC1e-L03-statements", "2.7-cards", "course/modules/SC/SC1/L03.html; cards c042 to c060, c187, c188, c225",
    f"All 21 L03 cards read against {OUT}/L03.txt: Definition 1.1 (lines 40-46), Assumptions 3.1 and 3.2 (lines 48-54), Lemmas "
    "2.1 and 2.2 with proofs (lines 58-76), Theorem 2.3 (lines 80-96), Proposition 2.4 with the closed form by induction "
    "(lines 100-108), Lab 1 (lines 195-229), section 3 canon breaks (lines 237-241), misconceptions (lines 249-257), problems "
    "M1-M3, P1-P3, E1-E3, R1-R3 (lines 269-367), key results (lines 373-381).")
row("SC1e-L04-statements", "2.7-cards", "course/modules/SC/SC1/L04.html; cards c061 to c082, c202 to c204, c222, c226",
    f"Read against {OUT}/L04.txt, lines 14 to 468 in full: Assumption 4.1 (line 48), Assumption 4.2 (a)-(e) (line 54), Definition 1.2 "
    "(line 58), Lemma 2.1 (lines 64-72), Propositions 2.2 to 2.4 with proofs (lines 80-128), the lab (lines 134-209), section 3 "
    "(lines 215-219), misconceptions (lines 227-235), problems M1 to M3, P1 to P3, E1 to E3, R1 to R3 (lines 245-345), and key "
    "results (lines 351-361). Every L04 card matches the statement it cites, and E[Z_t^2] = e^{theta^2 t} checks: "
    "E[W^2] = e^{-theta^2 h} E[e^{2 theta Y}] = e^{theta^2 h}.")
row("SC1e-L05-statements", "2.7-cards", "course/modules/SC/SC1/L05.html; cards c083 to c105, c189, c193 to c200, c214, c227, c228",
    f"Read against {OUT}/L05.txt lines 14 to 525: Assumptions A4(a)-(i) (lines 44-60), Definitions 1.1 and 1.2 (lines 66-74), "
    "Lemma 1.3 (lines 78-92), Theorem 1.4 and Remark 1.5 (lines 100-120), Lemma 2.2 (completing the square, rechecked by hand) and "
    "Theorem 2.1 (lines 138-166), lab (lines 167-256), section 3 with A3 and its sketch (lines 262-284), misconceptions, problems "
    "M1 to M3, P1 to P3, E1 to E3, R1 to R3 (lines 310-410), key results (lines 416-424). Phi(-1/sqrt2) = 0.2397500611 "
    "matches the quiz value 0.23975006.")
row("SC1e-L06-statements", "2.7-cards", "course/modules/SC/SC1/L06.html; cards c106 to c133, c217",
    f"Read against {OUT}/L06.txt lines 14 to 547: Definition 1.1 and Lemma 1.2 (lines 42-50), Proposition 1.3 and Corollary 1.4 "
    "(lines 56-80), Lemma 2.1 (lines 86-98), Definition 2.2 and Proposition 2.3 (lines 100-132, freezing step with h_- = h_+ "
    "by symmetry), Remark 2.4, Theorem 2.5 and Corollary 2.6 (lines 138-166; erfc substitution rechecked), lab (lines 176-286), "
    "section 3 and 4 (lines 292-316), problems M1 to M3, P1 to P3, E1 to E3, R1 to R3 (lines 326-416). Counts recomputed: "
    "1014, 78, 1588, 495, 281/512, 11/32, 105/512, erfc(1/sqrt2) = 0.3173105079.")
row("SC1e-L07-statements", "2.7-cards", "course/modules/SC/SC1/L07.html; cards c134 to c159, c191, c215, c229 to c231",
    f"Read against {OUT}/L07.txt lines 14 to 600: Definitions 1.1 and 1.2, Theorem 1.3 (H1 to H3), Remark 1.4 (limits), "
    "Corollary 1.5 (a) and (b) with A5 and the density integral (lines 80-90, integration by parts rechecked), Definitions 2.1, "
    "Proposition 2.2, Corollary 2.3, Remark 2.4 (lines 96-122), lab (lines 124-342), section 3 and 4 (lines 348-370), problems "
    "M1 to M3, P1 to P3, E1 to E3, R1 to R3 (lines 380-480), key results (lines 486-502). Part A tails 0.375000, 0.332306, "
    "0.321084, 0.318255, 0.317547 recomputed (l07_check.py). Part B counts and differences, Part C gap 0.0393 = 1.24 SE rechecked.")
row("SC1e-L08-statements", "2.7-cards", "course/modules/SC/SC1/L08.html; cards c161 to c183, c201, c205, c218",
    f"Read against {OUT}/L08.txt lines 14 to 580: Definition 1.1 and Proposition 1.2 (lines 42-56), Corollary 1.3 (lines 58-64), "
    "Corollary 1.4 with the changed index m (lines 66-72), Corollary 1.5 with the derivative of F(H) (lines 74-80), Remark 1.6, "
    "Definition 2.1, Propositions 2.2 and 2.3 (lines 90-108), lab (lines 110-326), section 3 jump example (line 332), misconceptions, "
    "problems M1 to M3, P1 to P3, E1 to E3, R1 to R3 (lines 362-464), key results (lines 466-482). f_1(1) = 0.241971 and "
    "f_1(2) = 0.109848 recomputed; E[min(nu_1,16)] = 179587/32768 exact.")
row("SC1e-assumption-labels", "2.7-cards", "cards naming A1 to A5, A4(a)-(i), Assumption 2.1, 3.1, 3.2, 4.1, 4.2(a)-(e)",
    f"A1(a)-(e) cards c206 to c210 match {OUT}/L01.txt lines 58-66; A2 card c033 matches L02 lines 269-273; A3 card c093, c098, "
    "c099 match L05 lines 262-270; A4(a)-(i) cards c193 to c200 and c214 match L05 lines 44-60 (A4(e) used in Theorem 2.1, "
    "A4(i) used only for M2 and the quiz); A4 of Lesson 4 cards c202 to c204, c222 match L04 line 54; A5 card c215 matches "
    "L07 line 78; Assumption 2.1 cards c211 to c213 match L02 lines 78-82; Assumption 3.1 and 3.2 cards c060, c188 match L03 lines 48-54.")
row("SC1e-cross-references", "2.7-cards", "cards naming Problems, Sections, Lab parts and numbered results",
    f"{SCR}/scan_refs_r13.py ({OUT}/scan_refs.txt): 284 labels, 20 flagged for header format only; each confirmed in the lesson "
    "header text (for example c052 'Problem R1' is the L03 header 'R1 · The equal partition in closed form'; c175 'Section 3' is "
    "the L08 header '3Where the canon breaks').")
row("SC1e-hypotheses-carried", "2.4-mathematics", "cards for Lemma, Proposition, Theorem, Corollary and Remark statements",
    "Hypotheses on each card checked against the lesson's hypothesis lines: Proposition 1.2 (H2 A1(a)), Remark 1.3 (H2 A1(b), "
    "A1(a)), Lemma 2.3 (H2 A1(a), A1(b), A1(c), A1(e)), Remark 2.6 (H2 A1(a), A1(b), A1(e), A2, Assumption 2.1), Propositions "
    "2.2 to 2.4 of L04 (H1, H2 at lines 76-78, 92-94, 114-116), Theorem 1.3 and Corollary 1.5 of L07 (H1 to H3, A5), Proposition "
    "2.2(b) of L07 (N divides N'), Proposition 1.2 and Corollary 1.3 to 1.5 of L08 (H1, H2, A3, A4). No card omits a stated hypothesis.")
row("SC1e-grades-audit", "2.3-grades", "cards grade field (T 125, C 28, none 64)",
    "Grade counts from cards.json: T 125, C 28 (includes c231), none 64 (definitions, assumptions and problems that make no claim). "
    "Every C card is a lab or simulation result (for example c010, c037, c038, c051, c072, c091, c092, c111 to c114, c127, c149, "
    "c150, c170 to c174, c187, c216, c218, c225, c226, c229 to c231 and the lab counts); every T card is proved on the page or is a "
    "derived computation from a named assumption (for example c052, c115). The key-results tables grade each row to the same "
    "standard (T for proved, C for lab, not graded for A3 and the path-level reflection).")
row("SC1e-cites-and-registry", "2.1-citations", "course/modules/SC/SC1/cards.json cite fields; lessons' References sections",
    "cite is empty on all 217 cards. The slice cites no registry key. The L03 reference note names shreve2004stochastic, which "
    "exists in references/references.json (line 20734). The second curriculum source, Karatzas and Shreve (curriculum "
    "03-markets.yaml SC1 sources), has no registry record (grep finds it only in references/review_queue.json), so the "
    "References sections of L05, L06, L07 and L08 are right that it is not cited. verify_refs --offline: 560 entries, 0 problems.")
row("SC1e-notation", "2.4-mathematics", "cards and L01 to L08 text; notation/notation.json",
    "notation.json registers T (number of return observations), Phi and Phi^{-1}, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q and "
    "macros. In SC1: T is never a symbol in a card or lesson (the only T's are grade badges and markup; L03 line 100 and L07 "
    "line 44 reserve T and write the horizon as H). Phi is the standard normal CDF in all 76 uses (for example L07 line 58, L05 "
    "P2). Macros used in the lessons are \\Prob, \\E, \\Var, \\Cov, \\R, \\Normal and \\indic (registered), and standard LaTeX "
    "otherwise. Not a registry symbol but noted for the builder: card c011 uses plain F for a finite set of times, while L01 "
    "section 4 writes the sigma-field as \\mathcal F and the set as G; no registry rule is broken.")
row("SC1e-dag", "2.9-prose", "cards; L01 to L08 text; check_dag",
    f"{OUT}/check_dag.txt: 'check_dag SC1: PASS'. Independent reading: L01 uses M4 and M6 concepts listed on its Uses line; L05 "
    "uses the M6 stopping time (defined in M6 Lesson 9, Definition 9.1, and here in section 3, a forward reference announced "
    "in A4(c)); L06 and L07 use Lesson 5 A3, A4 and Lesson 6 Theorem 2.5, all earlier in the unit. No concept is defined twice.")
row("SC1e-scope-words", "2.9-prose", "cards and the changed lesson text",
    "Scope words checked: 'every' (L01 line 114 'For every h in (0,1)'), 'all' (L05 line 167 '225 cases', L06 "
    "line 286 'no case fails'), 'only' (L02 line 329 'Within this construction'; L05 line 296 'coincide only when x=0 and s=0'; "
    "L07 line 354 'no grid tail exceeds'), 'exactly' (L01 line 120 'sum to exactly t', L03 line 96 'exactly 2 sum Delta_k^2'), 'in general' (card c223 and L01 quiz line 356, true for uncorrelated variables), 'for every M >= m_0' (c224, step 3 of Proposition 2.4(b), true). Each is backed "
    "by a proof or an exact computation shown on the page.")
row("SC1e-r8-twin-docstring-only", "2.5-labs", "tests/labs/SC1/ lesson twins (L01 to L08)",
    "Lesson twins byte-identical to 5db69a9 (git diff --quiet 5db69a9 e919577 -- tests/labs/SC1/lab-SC1-L0{1..8}-1.py: no output). "
    "The docstrings were read this round and each claim in them was checked against the output: the L02 docstring's 'identities "
    "that hold for every seed' (exact float equality, since the level terms beyond the depth are exactly 0.0), the L05 docstring's "
    "gaps at the scale of double-precision rounding (5.55e-16), and the L08 docstring's 'checks that identity for every N from 1 "
    "to 12' (Part A pairs 78 of 78). No docstring defect.")
row("SC1e-c052-term", "2.7-cards", "course/modules/SC/SC1/cards.json card SC1-c052 front and back",
    "c052 back: H sqrt(2/N)/20 with t=H; Var(Q)=2H^2/N by Problem R1 of L03 (L03 lines 347-351); sqrt(400)=20. The Lab 1 text "
    "(L03 line 114) gives the same formula. Matches.")
row("SC1e-c150-assumption-reference", "2.7-cards", "course/modules/SC/SC1/cards.json card SC1-c150 back",
    "c150 back reads '0.7586, with standard error 0.0317.' The lab prints 'N = 256 steps: mean grid maximum 0.7586, se 0.0317' "
    f"({OUT}/twin_L07.stdout). The assumption reference is not part of this value. Matches.")
row("SC1e-c140-hypotheses", "2.7-cards", "course/modules/SC/SC1/cards.json card SC1-c140 front",
    "c140 front names H1 (standard BM with continuous paths and B_0=0), H (H>0 fixed), A3 and A4 of Lesson 5, and A5 for part (b). "
    "Matches L07 lines 68-78 (Corollary 1.5: those of Theorem 1.3 for part (a), and A5 additionally for part (b)).")
row("SC1e-c219-new", "2.7-cards", "cards.json (card SC1-c219, removed at 5db69a9)",
    "SC1-c219 is absent from cards.json at e919577 (python check). grep for SC1-c219 in course/modules/SC/SC1/*.html returns 0 in "
    "every page, so no dangling reference.")
row("SC1e-c220-c221-new", "2.4-mathematics", "cards SC1-c220, SC1-c221 (L02)",
    "c220 P(Omega*)=1: L02 lines 143-145 give P(E_m^c)<=2^(-m), P(A_m0^c)<=2^(1-m0), and continuity from below (Assumption 2.1(c)). "
    "c221 sum m r^m = r/(1-r)^2 for r=2^(-1/2), finite (L02 line 150; computed this round: 8.24264068711929).")
row("SC1e-c029-c030-changed", "2.4-mathematics", "cards SC1-c029, SC1-c030",
    "c029: 2^(m-1)*2*e^(-lambda_m^2/2) with lambda_m^2 = 4 m log 2 gives 2^(-m) (L02 line 144). c030: M_m = lambda_m 2^(-(m+1)/2) "
    "= sqrt(2 log 2) sqrt(m) 2^(-m/2) (L02 lines 147-148); m=3 gives 0.721013, the bound printed at m=3 in out/twin_L02.stdout.")
row("SC1e-c011-c013-changed", "2.4-mathematics", "cards SC1-c011, SC1-c012, SC1-c013 (L01 section 4)",
    "The construction (Remark 2.6 of Lesson 2, A1(a), A1(b), A1(e), A2, Assumption 2.1, product space with U uniform and "
    "independent of B) is at L01 line 199; P(U in G)=0 for finite G at line 199; B-tilde discontinuous at U at line 199 and the "
    "continuity event at line 201 and R3 (lines 323-329). The card's 'finite set F' is the same claim with another letter.")
row("SC1e-L08-changed-cards", "2.7-cards", "cards SC1-c162, c165, c171, c201 (L08)",
    f"c162 matches Proposition 1.2 (lines 46-52). c165 matches Corollary 1.5 (density a/(sqrt(2 pi) H^(3/2)) exp(-a^2/(2H))). "
    f"c171 counts 512, 0, 384, 0, 288, 0, 224, 0, 180, 0 and 1588 / 4096 match {OUT}/twin_L08.stdout. c201 new back: the factor 2 "
    "comes from the reflection identity (Theorem 2.5 of Lesson 6, read at L06 lines 146-160), and Proposition 1.2 gives the event "
    "equality. Matches.")
row("SC1e-lab-outputs-cards", "2.5-labs", "cards backed by a lab (c010, c037, c038, c051, c072, c091, c092, c111 to c114, c127, c149, c150, c170 to c174, c187, c216, c218, c225, c226, c229 to c231)",
    f"Each card's printed value compared with {OUT}/twin_L0N.stdout: L01 81 of 81 pairs; L02 216 of 216 and 8 of 8; L03 z table "
    "(16 values), SE 0.1601, 0.0125; L04 1.000000000 and 54.598150033; L05 225 cases, gap 5.55e-16 (tolerance 1e-6), mass "
    "3.81e-29, integrals 1.0000000000; L06 1014, 78, 495, 281/512, 11/32, 105/512, erfc 0.3173105079; L07 21778, 0.2275, 0.3025, "
    "0.7586, 0.0230, 0.0393, 0 violations; L08 1588, 794, 0.387695, 0.193848, 5.480560, 11.815731, 24.557203, z -1.05, -0.69, -0.77, "
    "0.317311, 0.241971, 0.479500, 0.109848.")
row("SC1e-c222-c223-c224-new", "2.7-cards", "cards SC1-c222, SC1-c223, SC1-c224 (L04 4.2(e); L02 Lemma 2.3, Proposition 2.4(b))",
    f"c222 Assumption 4.2(e) E[1|G]=1 matches L04 line 54. c223 (joint normality of U_j, V_j from one family, then A1(c)) matches "
    "L02 lines 123-125 and the R1 solution. c224 (sup|Sigma - Sigma_M| <= sum_{m>M} M_m for M >= m_0) matches L02 lines 152-154.")
row("SC1e-c225-c226-new", "2.5-labs", "cards SC1-c225 (L03 Lab 1), SC1-c226 (L04 Lab 1)",
    f"c225: out/twin_L03.stdout z values, all 16 within +/-3 (largest 2.39). c226: {OUT}/twin_L04.stdout: E[Z_t] = 1.000000000 for "
    "theta -1, 0.5, 2, equal to Z_0 = 1 within 1e-9.")
row("SC1e-c227-c228-new", "2.4-mathematics", "cards SC1-c227, SC1-c228 (L05 Problems R2, R3)",
    "c227 F_s subset F_rho for the constant time rho = s (L05 R2 solution, line 402). c228: {rho_n <= r} = {rho <= k/2^n}, k = "
    "floor(2^n r), inside F_{k/2^n} subset F_r (L05 R3 solution, line 410). Both match.")
row("SC1e-c229-c230-new", "2.5-labs", "cards SC1-c229, SC1-c230 (L07 Lab 1 parts C and B)",
    f"c229: 0.797885 - 0.7586 = 0.0393 and 0.0393/0.0317 = 1.24 SE ({OUT}/twin_L07.stdout). c230: 'pathwise violations (coarse "
    "maximum above fine maximum): 0' in the same output.")
row("SC1e-round12-changed-cards", "2.7-cards",
    "cards SC1-c026, c027, c028, c032, c051, c072, c095, c096, c149, c150, c203, c207 (the twelve round-12 changed cards)",
    "Each card compared with its text in cards_all.txt and with the lesson text it cites: c026 and c027, c028 match L02 Lemma 2.3 "
    "(H2 and the induction step, lines 108, 123-125); c032 matches Proposition 2.4(b) conclusion; c051 matches twin_L03.stdout; "
    "c072 matches the L04 lab line 206; c095 and c096 match L05 R2 and R3; c149 and c150 match the L07 lab lines 335-339; c203 "
    "and c207 match L04 line 54 and L01 A1(b). None of these twelve cards changed in the round-13 delta (only c126, c201 and c231 did).")
row("SC1e-round12-lesson-hunks", "2.9-prose", "L01 to L05 hunks since 11d7077 (round-12 delta)",
    "Superseded by the full round-13 read of every lesson line (row SC1e-full-read-lessons) and the 5db69a9 to e919577 hunk read "
    "(row SC1e-delta-read). The round-12 hunk wordings (L01 A1(b), L02 Lemma 2.3, L03 dyadic depth n, L04 Assumption 4.2) are in the "
    "round-13 read and were checked again.")
row("SC1e-c231-new", "2.5-labs", "card SC1-c231 (L07, grade C) and L07 lab Part A",
    f"Card c231: 'All 78 pairs ... sum of N from 1 to 12, which is 78 ... #{{M_N >= a}} = #{{S_N >= a}} + #{{S_N > a}}'. "
    f"{OUT}/twin_L07.stdout line 1: 'discrete tail identity ... 78 of 78' and line 2 'counting formula agrees ... 78 of 78'. "
    "The lesson L07 E2 and key-results rows cite the same count. Matches.")
row("SC1e-c126-c201-changed", "2.7-cards", "cards SC1-c126 (L06) and SC1-c201 (L08), back text changed in the round-13 delta",
    "c126 new back: 'Theorem 2.5 gives P(M_t>=a)=2 P(B_t>=a), so the running maximum has twice the tail of the endpoint' matches "
    "L06 Theorem 2.5 (lines 146-149) and the L06 misconception at line 306 to 308. c201 new back: 'Corollary 1.3 gives "
    "P(tau_a<=H)=2P(B_H>=a)=2(1-Phi(a/sqrt H))=erfc(a/sqrt(2H)) ... The factor 2 comes from the reflection identity, Theorem 2.5 "
    "of Lesson 6; Proposition 1.2 gives the event equality' matches L08 Corollary 1.3 (lines 60-64) and Proposition 1.2. Both "
    "cards grade T and their basis names the proof used.")
row("SC1e-gates-tools", "2.9-prose", "tests/labs/SC1 twins; tools gate outputs",
    f"ruff check tests/labs/SC1 and ruff format --check tests/labs/SC1: 'All checks passed!' and '11 files already formatted' "
    f"({OUT}/ruff_labs.txt). No Python source in the SC1 lesson or card slice changed in the delta; mypy and the tooling pytest "
    "are not relevant to a cards and prose slice and were not run.")

fragment = {
    "unit": "SC1",
    "slice": "e",
    "round": 13,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-e: all cards of course/modules/SC/SC1/cards.json (217) against lessons L01 to L08; round 13",
    "pin": "e919577b45b431ce68e1e6533b00b8a301277937",
    "base": "5db69a9bee460736c318ebfacc7200ee5a6eb0f0",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE13-SC1-e",
    "scratch": "ledgers/SC1/scripts/SC1-e-r13/out",
    "verified_at": "2026-11-05T17:48:22Z",
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [
        "No 2025-2026 freshness row is needed: SC1 cites no registry key in its cards or lessons; the lesson references name Shreve (registry key shreve2004stochastic) and Karatzas and Shreve (no registry record).",
    ],
    "notes": (
        "Round 13 at e919577 (delta base 5db69a9). Changed since round 12: cards.json (c126 and c201 back text, c231 added), "
        "L01 section 2, L02 Lemma 2.3 consequence and interpretation and R2 solution, L03 why-it-matters and Assumption 3.2, "
        "L05 A4(i) and M1 solution, L07 description, hypothesis paragraph, E2 and E3, L08 Corollary 1.4 proof index and M1 solution. "
        "The round-12 UNVERIFIABLE row SC1e-full-read-lessons is cleared by a full line-by-line read of every lesson dump this round. "
        "No card defect and no lesson defect was found. Observations, not FAIL: card c011 uses plain F for a finite set of times "
        "where L01 section 4 uses the sigma-field F elsewhere (F is not a registry symbol); the L08 density remark (a H^(-3/2)) "
        "implies E[tau_a] is infinite, and the page says only that it does not evaluate E[tau_a], which is accurate. "
        "Mutants: none, because this slice is cards and prose, not a grader. Scripts: ledgers/SC1/scripts/SC1-e-r13/."
    ),
    "summary": (
        "SC1 slice e round 13 at e919577: all 217 cards read against L01 to L08 (full lesson dumps read line by line); "
        "every row PASS; verdict PASS. Previous UNVERIFIABLE row cleared."
    ),
}

if __name__ == "__main__":
    dst = sys.argv[2]
    with open(dst, "w", encoding="utf-8") as fh:
        json.dump(fragment, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"rows {len(rows)} pass {sum(1 for r in rows if r['status'] == 'PASS')}")
