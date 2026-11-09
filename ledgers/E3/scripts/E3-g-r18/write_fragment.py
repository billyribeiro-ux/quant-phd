"""Round-18 verifier: builds ledgers/E3/E3-g.json from the round-15 base fragment and this round's evidence.
Every round-15 row id is kept. Rows whose cited subject changed between dde0486b and 4540351d are re-verified
(new evidence); the rest are carried with the round-15 evidence and the carry prefix."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
VERIFIED_AT = sys.argv[2]
base = json.load(open("/Users/billyribeiro/.fanout/frags/D-E3-g.round15.json", encoding="utf-8"))
r15 = {r["id"]: r for r in base["rows"]}

PREFIX = "Carried from round 15 (subject byte-identical since the previous pin dde0486b; only the footer line of course/modules/E/E3/L07.html differs, and the footer is not cited): "
CARRY_FILES = {
    "L07": "the cited sections of course/modules/E/E3/L07.html and the cards.json entries E3-c118 to c135 and c187",
}

REVERIFY = {
 "E3g12-c078": "Re-verified at 4540351d: cards.json E3-c078 (changed Omega text) vs L05.html Definition 1.1 (line 65-66 current): V0 = [(1-beta) c0^Omega + beta (E V1^(1-gamma))^(Omega/(1-gamma))]^(1/Omega), Omega = 1-1/psi, V1 = c1; assumptions match A1-A4. PASS.",
 "E3g12-c080": "Re-verified: cards.json E3-c080 vs Theorem 1.3(a) (L05.html line 78) and proof (b) (line 85): formula with Omega; strictly increasing in CE1 for fixed c0, beta, gamma, psi under A1-A4. PASS.",
 "E3g12-c084": "Re-verified: cards.json E3-c084 vs Proposition 2.2 statement and changed proof (L05.html lines 162-167): MRS = (1-beta)/beta (c1/c0)^(1-Omega) = ... (c1/c0)^(1/psi); derivative d lnMRS / d ln(c1/c0) = 1/psi by hand; EIS = psi. Numeric closed-form check (4/9) in numbers_L05_L08.out. PASS.",
 "E3g12-c085": "Re-verified: cards.json E3-c085 vs Remark 2.3 (L05.html) and Proposition 2.2 (changed proof): CE1 = c1 for every gamma != 1 so V0 depends on c0, c1, beta, psi only; EIS = psi. Lab lines 'closed form agrees' and EIS lines match twin stdout (twin_check.out). PASS.",
 "E3g12-c086": "Re-verified: cards.json E3-c086 vs Remark 3.1 (changed text: theta := (1-gamma)/Omega, Omega = 1-1/psi): theta = 1 iff Omega = 1-gamma iff psi = 1/gamma. PASS.",
 "E3g12-c087": "Re-verified: cards.json E3-c087 vs Theorem 3.2 (L05.html line 191-193; changed proof line 200): (1-gamma)U = V0^(1-gamma) at psi = 1/gamma; gamma > 0 by A2; checked by hand (proof) and lab line 'True' (twin stdout). PASS.",
 "E3g12-c091": "Re-verified: cards.json E3-c091 vs Remark 3.4 (L05.html, unchanged) and Proposition 2.2 (changed proof, statement unchanged): CRRA elasticity 1/gamma for gamma != 0 (undefined at 0); Epstein-Zin gives psi. PASS.",
 "E3g12-c093": "Re-verified: cards.json E3-c093 (V0 = 80/49) vs the lab expected line 'EZ value V0 = 80/49' (twin stdout, twin_check.out) and Problem E1 solution (changed Omega wording, value unchanged); numbers_L05_L08.out: V0 = 80/49. PASS.",
 "E3g12-c094": "Re-verified: cards.json E3-c094 vs lab EIS lines 'psi = 0.5: EIS estimate 0.5000', '2.0: 2.0000', '0.25: 0.2500' (expected block equals twin stdout, twin_check.out); analytic EIS = psi. PASS.",
 "E3g12-c095": "Re-verified: cards.json E3-c095 vs lab lines 412-413 (U(4,4) = -0.2500, U(1,10) = -0.5500, V0(4,4) = 4.0000, V0(1,10) = 4.3311): twin stdout equal; numbers_L05_L08.out: U(4,4) = -0.25, U(1,10) = -0.55, V0(4,4) = 4.0, V0(1,10) = 4.331139. PASS.",
 "E3g12-c096": "Re-verified: cards.json E3-c096 vs lab lines 'risky tree with gamma = 0.5/2.0/3.0: CE1 = 2.2500 / 1.6000 / 1.3720' (twin stdout equal); recomputed 2.25, 1.6, 1.371989. PASS.",
 "E3g12-c100": "Re-verified: cards.json E3-c100 (PV := sum p_i v(x_i), changed) vs Definition 1.3 (L06.html line 69): probabilities p_i > 0 summing to 1; the probabilities are used unweighted, L07 adds weighting. PASS.",
 "E3g12-c104": "Re-verified: cards.json E3-c104 (PV text) vs Proposition 2.1 (L06.html line 98): lambda* = pg/((1-p) l); PV(lambda) = pg - (1-p) lambda l decreasing; PV(1) = EV; sign pattern follows. PASS.",
 "E3g12-c105": "Re-verified: cards.json E3-c105 vs Proposition 2.2 (L06.html line 108): lambda* = p g^alpha/((1-p) l^delta); PV zero at lambda*, positive below, negative above. PASS.",
 "E3g12-c106": "Re-verified: cards.json E3-c106 vs Example 2.3 (L06.html line 118, changed W -> PV): EV 200, lambda* = 5/3, PV 200, 50, -100 at lambda 1, 3/2, 2; recomputed exactly (numbers_L05_L08.out, L06 lines). Stale basis field noted under E3g18-c106-basis. PASS.",
 "E3g12-c107": "Re-verified: cards.json E3-c107 (PV text) vs Remark 2.4 (L06.html line 123): same sign as CE because v is continuous, strictly increasing, v(0) = 0. PASS.",
 "E3g12-c111": "Re-verified: cards.json E3-c111 vs Remark 3.2 (L06.html section 3, unchanged text) and Example 2.3 (line 118, changed only W -> PV): for p = 1/2, outcomes 800 cents either side of EV, the value (1/2)800^alpha(1-lambda) gives the sign change at lambda = 1 and lambda_R = 1; the threshold in general is lambda_R. PASS.",
 "E3g12-c112": "Re-verified: cards.json E3-c112 vs Section 5 first misconception (L06.html, unchanged) and Example 2.3 (line 118, changed only W -> PV): PV = 50 > 0 at lambda = 3/2 and EV = 200; PV negative only above lambda* = 5/3 (Proposition 2.1). PASS.",
 "E3g12-L05-L08-key-results": "Re-verified every Key results row of L05 (section 7, rows citing Corollary 1.4, Remark 2.3, Proposition 2.2, Theorem 3.2, Remark 3.4, Lab 1), L06 (rows citing Proposition 1.4, Remark 1.5, Propositions 2.1, 2.2, Remark 2.4 (PV rename), Remark 2.5, Example 2.3), L07 (rows citing Example 1.4, Remark 1.6, Proposition 2.2, Theorem 1.5 of Lesson 4, Observation 1.5 with grade C) and L08 (rows citing Propositions 1.3, 2.4, 3.2, Theorem 2.2, Remark 4.2, Example 2.5, the four CEs, and the two registry-title rows graded C; see E3g18-grade-legend-footer). Each statement matches its cited result and the printed lab values. PASS.",
 "E3g12-c116": "Re-verified: cards.json E3-c116 (PV text, grade C, basis Lab 1 power block) vs lab expected lines 'threshold lam* = 1.2910' and 'PV at lam = 2 with alpha = delta = 0.5: -8.6835' (twin stdout equal); recomputed sqrt(5/3) = 1.290994 and PV(2) = -8.683509. PASS.",
 "E3g12-c117": "Re-verified: cards.json E3-c117 vs lab grid lines (expected block: concave on gains True; v'' >= 0 on losses True; increasing True; |v(-x)|/v(x) = 2 True) equal to twin stdout; the grid code (midpoint inequalities, 4 gains, 4 losses) read in the twin. PASS.",
 "E3g12-c143": "Re-verified: changed cards.json E3-c143 vs Proposition 2.4 (L08.html line 161-170) and its proof (line 176): E_p u(f) is increasing in p for a red bet (w_red > w_no, u strictly increasing), so the worst prior for red is P_0; the card's shortened back keeps only the red case, which the proposition states. PASS.",
 "E3g12-c145": "Re-verified: changed cards.json E3-c145 (Omega = 1 - 1/psi) vs Definition 3.1 (L08.html line 199-201): timing convention, gamble pays at date 1 only. PASS.",
 "E3g12-c146": "Re-verified: cards.json E3-c146 vs Proposition 3.2 (L08.html lines 207-220: A1-A5) and changed proof (line 227): EZ CE = (E c1^(1-gamma))^(1/(1-gamma)); formula contains neither psi, beta nor c0; section 6 third misconception (line 610-612) matches. PASS.",
 "E3g12-c153": "Re-verified: cards.json E3-c153 vs lab part B lines 487-494 (EZ CE 101951.219512; largest gap 2.91e-11; all six below 1e-6): equal to twin stdout (twin_check.out); twin edited only in the Omega rename. PASS.",
 "E3g12-c169": "Re-verified: cards.json E3-c169 (U = -49/80) vs Problem E1 solution (L05.html, changed Omega wording) and lab line 'CRRA expected utility U = -49/80'; recomputed exactly. PASS.",
 "E3g12-c170": "Re-verified: cards.json E3-c170 (CE1 = 8/5) vs Remark 1.5 (L05.html line 139) and lab line 'CRRA certainty equivalent CE1 = 8/5'; recomputed 1/((1/2)(1) + (1/2)(1/4)) = 8/5. PASS.",
 "E3g12-c179": "Re-verified: cards.json E3-c179 vs Model 3 (L08.html line 530, changed: Omega = -1; Proposition 3.2 gives 101951.2195) and lab part A line 'Epstein-Zin, psi = 0.5, beta = 0.95 ... CE = 101951.2195'; bisection recomputed (numbers_L05_L08.out: 101951.219512). PASS.",
 "E3g12-c184": "Re-verified: cards.json E3-c184 vs lab line 'MRS ... closed form agrees with the numeric MRS: True' (twin stdout) and Proposition 2.2; closed form (0.1/0.9)(4/2)^2 = 0.4444 in numbers_L05_L08.out. PASS.",
 "E3g12-c185": "Re-verified: cards.json E3-c185 (mean 5/2) vs Remark 1.5 and lab line 'mean of c1 = 5/2' (twin stdout); exact recomputation 1/2*1 + 1/2*4 = 5/2. PASS.",
 "E3g12-L05-prose-numbers": "Re-verified all numbers in the changed L05 text (Definition 1.1, Theorem 1.3, Proposition 2.2 proof, Remark 3.1, Theorem 3.2 proof, problem solutions E1, M2, M3, P3, quiz keys): Omega = -1 at psi = 1/2 and 1/2 at psi = 2; MRS closed form; theta = -2; E1 value 80/49 and U = -49/80; CE1 = 2 (M1 quiz); Remark 1.5 CE 8/5 and 12/5; recomputed in numbers_L05_L08.out. PASS.",
 "E3g12-L06-prose-numbers": "Re-verified all numbers in the changed L06 text (Definition 1.3, Proposition 2.1, 2.2, Example 2.3, Remark 2.4, Remark 2.5, Remark 3.2, misconceptions, problems M1, M2, E2, E3, R2, quiz items): 200/50/-100; lambda* 5/3; 1.2910; PV(2) = -8.6835; combined 100, separate -200; 700-300 lambda and 1000-600 lambda; M1 lambda* 3/2 and PV -100; E3 values 250 and 100 at lambda 3/2; lambda_R = sqrt(2)/2 for p=1/3; numbers_L05_L08.out. PASS.",
 "E3g12-L08-prose-numbers": "Re-verified all numbers in the changed L08 text (Definition 3.1, Proposition 3.2 proof, Model 1-4 table, Model 2 inverse -1.072330 CU and 99892.7670 cents, Model 3, section 5 numbers, Remark 4.2, problems M1-M3, E1-E3, R1-R3, quiz): 4180000/41 = 101951.2195; 99523.8095 = 2090000/21; 548.7805 = 22500/41; 103125 = 1650000/16; 106451.6129 = 3300000/31; 98352.94 and 105822.78; gap 2.91e-11; numbers_L05_L08.out. PASS.",
 "E3g12-L05-L08-problem-solutions": "Re-verified every problem solution of L05 (M1-M3, P1-P3, E1, E3-type items), L06 (M1-M3, P1-P3, E1-E3, R1-R3), L07 (M1-M3, P1-P3, E1-E3, R1-R3) and L08 (M1-M3, P1-P3, E1-E3, R1-R3) against the stated formulas; the changed solutions (L05 E1, M3, P3; L06 M1, M2, P2; L08 R1) re-derived by hand. No defect. PASS.",
 "E3g12-L05-L08-quiz-keys": "Re-verified: 44 quiz items extracted from the four pages (L05 12, L06 10, L07 11, L08 11) with a script; every data-correct option and data-answer/data-tolerance checked: L05 2, -2, 1.632653 (80/49 within 5e-7), 4; L06 1.6667 (5/3 within 1e-4), -100, 1.2910 (within 1e-4); L07 0.26795, 39.1251, 0.35355, 0.278; L08 101951.22, 99523.81, 103125, 548.78, 99892.77 (within 0.01). PASS.",
 "E3g12-lab-twins-run": "Re-ran at 4540351d: twin_check.py: for L05, L06, L07, L08 the page code equals the twin byte for byte and the expected block equals the stdout of python -I -W error (rc 0, empty stderr) (out/twin_check.out); tests/labs/E3 twins changed for L05, L06, L08 and re-run. PASS.",
 "E3g12-check-pages-dag-projects": "Re-ran at 4540351d: check_pages --unit E3 --page L05..L08 PASS; check_dag --unit E3 PASS; check_projects --unit E3 PASS (out/check_pages_L0x.out, check_dag_unit.out, check_projects_unit.out). PASS.",
 "E3g12-verify-refs": "Re-ran verify_refs.py --offline: 560 entries, 0 problems (out/verify_refs_offline.out). No references/ file changed in the delta, so no live run is required by the protocol; not run live. Registry records for kahneman1979prospect, ellsberg1961risk, gilboa1989maxmin and epstein1989substitution read directly from references/references.json (titles: 'Prospect Theory: An Analysis of Decision under Risk', 'Risk, Ambiguity, and the Savage Axioms', 'Maxmin expected utility with non-unique prior', 'Substitution, Risk Aversion, ...'). PASS.",
 "E3g12-L04-theorem-cross-lesson": "Re-verified: L04.html Theorem 1.5 (lines 89-90) is unchanged in this delta (L04 changed only the why-it-matters paragraph): 'F_X(t) <= F_Y(t) for every t iff E u(X) >= E u(Y) for every nondecreasing u'; with X = B, Y = A it is the use in L07 section 0 and section 2 and in card E3-c129. PASS.",
 "E3g12-notation": "Re-verified: notation/notation.json has 8 symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q) and 26 macros; the L05-L08 inventory (math_inventory.py, out) uses none of the registered symbols with another meaning and uses only registered macros (E, Prob, R). Local symbols: Omega (L05 Def 1.1 line 65; L08 Def 3.1 line 142, same meaning), PV (L06 Def 1.3 line 69), omega (L07), varpi and tau (L08), each with one meaning. PASS.",
 "E3g12-scope-words-cards": "Re-verified scope words in the L05-L08 cards and in the changed prose: 'for every', 'exactly', 'only', 'always' statements (cards c080, c082, c083, c085, c088, c090, c107, c110, c117, c143, c154, c155) each carry the hypotheses of the cited result (A1-A4, psi = 1/gamma, positive consumption, A1-A3 of Proposition 2.4). PASS.",
 "E3g12-process-words-cards": "Re-verified: grep of cards.json (L05-L08) and of the four pages for process words (round, delta, revised, renamed, fixed in, verifier, builder, previous version, updated) finds none in learner text; 'fixed' occurs only as a mathematical 'for fixed c0' and 'fixed decimals'. PASS.",
 "E3g12-dup-scan": "Re-ran: cards.json has 178 cards, 178 unique ids, no duplicate fronts or backs (script output in out/card_numbers.out and the inline scan). PASS.",
 "E3g12-card-numbers": "Re-ran card_numbers.py (strip helper present, -I): for every L05-L08 card, every number token in front and back appears in the stripped lesson text; 'cards 178 unique ids True; duplicate fronts []; done'. PASS.",
 "E3g14-lab-L05-printed": "Re-verified: lab L05 printed values recomputed (numbers_L05_L08.out) and the expected block equals twin stdout (twin_check.out). PASS.",
 "E3g14-lab-L06-printed": "Re-verified: lab L06 printed values recomputed (numbers_L05_L08.out) and the expected block equals twin stdout (twin_check.out). PASS.",
 "E3g14-lab-L07-printed": "Re-verified: lab L07 printed values (parts A-D) equal twin stdout (twin_check.out); values 42.8686, 39.1251, 4.8788, 3.9125, 10 of 10, 0.278 recomputed. PASS.",
 "E3g14-lab-L08-printed": "Re-verified: lab L08 printed values (parts A-D) equal twin stdout (twin_check.out); 101951.2195, 99892.7670, 99523.8095, 103125.0000, 100000.0000 recomputed. PASS.",
 "E3g14-page-smoke": "Re-ran page_smoke.py --unit E3 --pages L05 L06 L07 L08: PASS, each lab runs in the runtime (out/page_smoke_L05_L08.out). PASS.",
 "E3g14-ruff-mypy": "Re-ran ruff check tests/labs/E3 course/modules/E/E3/grader (All checks passed), ruff format --check tests/labs/E3 (11 files already formatted), mypy --no-incremental (Success: no issues found in 386 source files). PASS.",
 "E3g14-pytest-relevant": "Re-ran tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py, tests/test_curriculum.py, tests/test_docs_figures.py, tests/test_refs.py: all pass (out/pytest_named.out); pytest -k E3 over tests/ also passes (out/pytest_labs_E3.out). PASS.",
 "E3g15-L05-changes": "Re-verified: L05 text changed since round 15: Proposition 2.2 proof and Remark 3.1, Theorem 3.2 proof, lab formulas and ValueError text, quiz explanations (Omega); Remark 1.5 and Definition 2.1 are byte-identical since dde0486b. All re-read and re-derived above. PASS.",
 "E3g15-L06-changes": "Re-verified: L06 Proposition 1.4 and its proof are byte-identical since dde0486b; the changed text (Definition 1.3, Section 2, Remark 2.4, lab, M1, M2, P2, quiz items, footer) re-read and re-derived above; section 7 rows and section 4 bullets unchanged in this delta. PASS.",
 "E3g15-lab-twin-L06": "Re-verified: tests/labs/E3/lab-E3-L06-1.py (changed W -> PV in labels and docstrings) equals the page code byte for byte; stdout equals the expected block (twin_check.out, rc 0). PASS.",
 "E3g15-numbers": "Re-verified: independent recomputation of the numbers of L05-L08 with Fraction and Decimal (numbers_L05_L08.py, out/numbers_L05_L08.out); no unrounded-vs-displayed mismatch in prose (note: the L07 eight-decimal quotient 0.28579088/0.39125077 = 0.73045449 as the page states). PASS.",
 "E3g15-attributions": "Re-verified from references/references.json: the title facts stated on L07 (prospect theory in the 1979 title), L08 (ambiguity in the 1961 title; maxmin expected utility in the 1989 Gilboa-Schmeidler title) and the L05 Epstein-Zin registry key are correct; the title-only grade is addressed under E3g18-grade-legend-footer. PASS.",
 "E3g15-gate-check-and-build": "Re-ran build_site.py --check (site data current: 6 outputs), render_curriculum.py (curriculum valid), and git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json (empty diff, rc 0). PASS.",
 "E3g15-gate-run-labs": "Re-ran run_labs.py --unit E3 --page L05, L06, L07, L08: each PASS (1/1). PASS.",
}

CARRY = [k for k in r15 if k not in REVERIFY]
rows = []
for rid, src in r15.items():
    if rid in REVERIFY:
        rows.append({"id": rid, "check": src["check"], "location": src["location"], "status": "PASS",
                     "evidence": REVERIFY[rid]})
    else:
        ev = src["evidence"]
        page = re.search(r"L0[5-8]", src["check"] + " " + src["location"])
        cards = re.findall(r"E3-c\d{3}", src["check"])
        if cards:
            files = f"cards.json {cards[0]} and the cited block of course/modules/E/E3/{page.group(0)}.html" if page else f"cards.json {cards[0]}"
        elif page:
            files = f"the cited block of course/modules/E/E3/{page.group(0)}.html (page footer aside)"
        else:
            files = "the cited subject (no changed hunk in the cited subject)"
        rows.append({"id": rid, "check": src["check"], "location": src["location"], "status": "PASS",
                     "evidence": f"Carried from round 15 ({files} byte-identical since the previous pin): " + ev[:900]})

NEW = [
 {"id": "E3g18-delta-inventory", "check": "2.9 delta dde0486b..4540351d within slice g (L05-L08, cards, twins): every changed hunk enumerated",
  "location": "git diff -U0 dde0486b 4540351d -- course/modules/E/E3/L05.html L06.html L07.html L08.html cards.json tests/labs/E3",
  "status": "PASS",
  "evidence": "L05.html hunks at lines 65-66, 78, 84-85, 117-119, 131, 142, 171-173, 212, 335, 400, 407, 432, 443, 538, 547, 620 (Omega rename, lab formulas, quiz/problem text, footer); L06.html hunks at 69 (Definition 1.3), 94-123 (Section 2 and Remarks), 133 (lab hypothesis), 146-273 (lab code and expected block), 331-365 (M1, M2, P2), 475-545 (quiz items, footer); L07.html footer only; L08.html hunks at 142-160 (Definition 3.1, Proposition 3.2), 284-289 (ez_value), 447 (Model 3), 587 (R1), 725 (footer); cards.json changed entries E3-c078, c080, c100, c104, c105, c107, c116, c143, c145 (plus L01, L03 entries outside slice); tests/labs/E3 changed lab-E3-L05-1.py, lab-E3-L06-1.py, lab-E3-L08-1.py (L01 twin outside slice). Every changed hunk in slice L05-L08 is re-verified above; unchanged subjects are carried."},
 {"id": "E3g18-rename-complete", "check": "2.4 renames complete: a -> Omega (L05-L08, cards, twins) and W -> PV (L06, cards c100-c116, L06 twin)",
  "location": "course/modules/E/E3/L05.html, L06.html, L07.html, L08.html, cards.json, tests/labs/E3/lab-E3-L05-1.py, lab-E3-L06-1.py, lab-E3-L08-1.py",
  "status": "PASS",
  "evidence": "grep for a residual prospect value W (in math, prose, cards, twins) returns nothing in L05-L08; grep for the exponent a (a = 1 - 1/psi, a^, a/(1-gamma)) in L05-L08, cards and twins returns nothing; Omega is defined once per lesson before first use (L05 Definition 1.1 line 65; L08 Definition 3.1 line 142) with the same meaning; PV is defined in L06 Definition 1.3 (line 69) before its first use; lab output 'PV' lines equal the expected block (twin_check.out)."},
 {"id": "E3g18-omega-notation", "check": "2.4/2.9 notation: Omega and PV against notation/notation.json and the E3 unit",
  "location": "notation/notation.json (8 symbols, 26 macros); course/modules/E/E3/L05.html, L08.html; cards.json E3-c078, c080, c145",
  "status": "PASS",
  "evidence": "notation.json registers no Omega and no PV, and BUILDER_RULES 3.1-3.2 leaves conventionally local letters to each lesson; within E3, \\Omega appears only in L05 and L08 with the exponent meaning (23 and 51 occurrences by math_inventory.py), and no E3 lesson uses \\Omega for a sample space; no registered symbol (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q) appears in L05-L08. Out of slice: L03 renamed a to \\iota (lines 67-122) and cards E3-c036, c037, c177; \\iota is a local letter and is not in notation.json; outside slice, not rated."},
 {"id": "E3g18-twins-run", "check": "2.5 twins alone under python -I -W error; page code equals twin; expected block equals stdout (L05, L06, L08 changed; L07 unchanged)",
  "location": "tests/labs/E3/lab-E3-L05-1.py, lab-E3-L06-1.py, lab-E3-L07-1.py, lab-E3-L08-1.py; course/modules/E/E3/L05-L08.html lab sections",
  "status": "PASS",
  "evidence": "ledgers/E3/scripts/E3-g-r18/twin_check.py at 4540351d: L05 lab-E3-L05-1 page_code_equals_twin=True expected_equals_stdout=True rc=0; L06 lab-E3-L06-1 True True rc=0; L07 lab-E3-L07-1 True True rc=0; L08 lab-E3-L08-1 True True rc=0; stderr empty. run_labs.py --unit E3 --page L05..L08 PASS (1/1 each)."},
 {"id": "E3g18-c106-basis", "check": "2.3 grade and basis fields of card E3-c106 (grade T)",
  "location": "course/modules/E/E3/cards.json E3-c106",
  "status": "PASS",
  "evidence": "Card E3-c106 has grade T and a leftover basis field ('Example 2.3') from its earlier grade C. The claim is a computed Example 2.3 result (200, 50, -100; lambda* = 5/3), so the grade T is supported. Metadata only; no claim affected. Builder may remove the basis field."},
 {"id": "E3g18-grade-legend-footer", "check": "2.3/2.9 grade C legend, grade-C rows and the new site footer on L05-L08 against BLUEPRINT section 3",
  "location": "course/modules/E/E3/L05.html line 620, L06.html line 545, L07.html line 571, L08.html line 725 (footer); L05.html line 46 and L06.html line 46 (legend 'C single study or lab result'); L07.html line 47 and L08.html line 47 (legend 'C single study'); L07.html line 463 and L08.html lines 620-621 (grade-C key-result rows); cards.json E3-c134, E3-c157, E3-c158 (grade C, no basis)",
  "status": "FAIL",
  "evidence": "The delta changed the footer of L05, L06, L07 and L08 to 'Each graded result carries a proof or a lab result labelled C.' The page's own grade legend defines C as 'single study or lab result' (L05, L06) or 'single study' (L07, L08), and BLUEPRINT section 3 defines C as 'working paper, practitioner research, or single-sample evidence'. Four grade-C rows cite only a registry title (L07.html line 463 kahneman1979prospect 'title only'; L08.html lines 620-621 ellsberg1961risk and gilboa1989maxmin 'title only'), and cards E3-c134, E3-c157, E3-c158 are grade C with no basis: none is a lab result or a study, so the footer claim is false for them. The L07 legend omits 'lab result' while L07 row 462 grades a Lab 1 finite-grid result C (legend inconsistency, carried text). The footer also drops the BLUEPRINT section 3 standard ('every substantive claim carries an evidence grade and at least one citation key'). The same footer sentence appears on E2 and M2 pages (grep), so the convention is program-wide.",
  "fix": "Either (a) restore the BLUEPRINT wording in the four footers ('Every claim carries an evidence grade and a registry citation.') and make the L07 and L08 legends match L05/L06, or (b) keep the new footer and regrade the title-only rows (L07 line 463; L08 lines 620-621; cards E3-c134, c157, c158) to a grade with a basis, or move them out of the graded key-results tables as registry facts. Apply the same change to the E2 and M2 pages that carry the sentence."},
 {"id": "E3g18-page-structure-footers", "check": "2.9 structure: page footers and the L05-L08 hub links after the delta",
  "location": "course/modules/E/E3/L05.html, L06.html, L07.html, L08.html (footer and Previous/Next links)",
  "status": "PASS",
  "evidence": "check_pages.py PASS for L05-L08 (out/check_pages_L0x.out); footer line is the only non-content change on L07 (git diff -U0: one hunk at line 571); Previous/Next links unchanged in the delta."},
]
rows += NEW

fragment = {
 "unit": "E3",
 "slice": "g",
 "round": 18,
 "verifier": "Haiku 5.5 independent verifier, slice g, round 18 (closing delta verification)",
 "pin": "4540351dc664559cdfd371b908f2b4e644cf4297",
 "base": "dde0486beeb0312e4ac1cc03aaa02e56644adb24 (round-15 pin; base fragment /Users/billyribeiro/.fanout/frags/D-E3-g.round15.json, the latest E3-g fragment on disk; the task's round-17 path does not exist)",
 "checkout": str(ROOT),
 "scratch": "/Users/billyribeiro/.fanout/scratch/E3-g-r18",
 "verified_at": VERIFIED_AT,
 "verdict": "FAIL",
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
  "Slice: E3 L05-L08 lesson pages, the 87 retrieval cards of L05 (22), L06 (19), L07 (18 plus E3-c187), L08 (28), and the lab twins for L05, L06, L07, L08. Lessons, cards and twins are not a project slice, so no grader mutation applies (VERIFIER rulings: lab twins are demonstrations); mutants: none.",
  "Base: the task names round-17 base /Users/billyribeiro/.fanout/frags/D-E3-g.round17.json, which does not exist; the latest E3-g fragment on disk is round 15 at pin dde0486b, which is the base used. Its 126 row ids are all kept.",
  "Delta dde0486b..4540351d inside the slice: L05 (Omega rename in Definition 1.1, Theorem 1.3, Proposition 2.2 proof, Remark 3.1, Theorem 3.2 proof, lab formulas and ValueError text, problem and quiz text, footer), L06 (PV rename in Definition 1.3, Section 2, Remark 2.4, lab, M1, M2, P2, quiz items, footer), L07 (footer only), L08 (Omega in Definition 3.1, Proposition 3.2, ez_value docstring, Model 3, R1, footer), cards c078, c080, c100, c104, c105, c107, c116, c143, c145, twins L05, L06, L08.",
  "Outside slice, observed and not rated: L01 (mixture weight renamed to Xi; cards E3-c005, c007, c008, c017; twin lab-E3-L01-1), L03 (power exponent renamed to iota in F2, Definition 1.1, Proposition 1.2, Proof, cards E3-c036, c037, c177), L04 (why-it-matters paragraph only; Theorem 1.5 and Theorem 2.3 unchanged), E3 project.html and grader/reference.py text lines.",
  "Gates run at 4540351d (all rc 0): check_pages L05-L08, check_dag, check_projects, run_labs L05-L08, page_smoke L05-L08, ruff check, ruff format --check, mypy --no-incremental, verify_refs --offline (560 entries, 0 problems), build_site --check, render_curriculum with empty git diff, pytest tests/test_docs_figures.py tests/test_refs.py, pytest -k E3 over tests/, pytest named modules (test_labs, test_run_labs, test_page_checks, test_curriculum, test_docs_figures, test_refs). Outputs in ledgers/E3/scripts/E3-g-r18/out/.",
  "Independent recomputation: ledgers/E3/scripts/E3-g-r18/numbers_L05_L08.py (Fraction and 60-digit Decimal) recomputes every number in the changed prose and in the lab outputs; card_numbers.py finds no card number absent from its lesson.",
  "Not checked: live Crossref (verify_refs live) because references/ is unchanged in the delta; run_graders and mutate_graders (no project grader in slice g; the E3 project and grader changed outside the slice); browser screenshots beyond page_smoke; the Epstein-Zin lab grid beyond the printed values and the stated tolerances; the L01, L03 and L04 hunks as subjects (outside the slice, only cross-references were read).",
  "Rulings applied: hours are design targets (no hours arithmetic changed in the slice); lab twins are demonstrations, so no twin mutation; registry titles were read from references/references.json directly.",
  "Only one non-PASS row: E3g18-grade-legend-footer (FAIL). It is a claim-level defect introduced by the delta footer change; no mathematical, numerical, card-to-lesson or lab defect was found in the slice."
 ],
 "summary": {
  "rows": len(rows),
  "pass": sum(1 for r in rows if r["status"] == "PASS"),
  "fail": sum(1 for r in rows if r["status"] == "FAIL"),
  "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
  "card_rows": sum(1 for r in rows if r["id"].startswith("E3g12-c")),
  "carried_rows": sum(1 for r in rows if r["evidence"].startswith("Carried from round 15")),
  "reverified_rows": sum(1 for r in rows if not r["evidence"].startswith("Carried from round 15")),
  "mutants": 0,
  "mutants_killed": 0,
 },
}
missing = set(r15) - set(r["id"] for r in rows)
assert not missing, missing
out = ROOT / "ledgers/E3/E3-g.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "carried", len(CARRY), "reverified", len(REVERIFY), "missing", missing)
