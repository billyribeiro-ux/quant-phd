"""Build ledgers/E3/E3-g.json (round 7, slice g) from the round-6 row ids and this round's evidence.

Carried rows keep their round-6 id and evidence, prefixed as the verifier rules require. Every other
round-6 id is re-verified on the 9373ef39 pin and gets fresh evidence. One new row is added.
"""

import json
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD7-E3-g")
SCR = "ledgers/E3/scripts/E3-g-r7/"
R6 = Path("/Users/billyribeiro/.fanout/frags/D-E3-g.round6.json")

CARRY_PREFIX = (
    "Carried from round 6 (course/modules/E/E3/L05.html and L06.html byte-identical since the round-6 pin "
    "142ecfc2, and the L05 and L06 entries of cards.json byte-identical; notation/notation.json and "
    "references/references.json unchanged): "
)

CARRY = {
    "E3g-grade-c090",
    "E3g-r2-L05-G1",
    "E3g-r2-L05-G3",
    "E3g-r2-L06-G4",
    "E3g-r2-L05-G2",
    "E3g3-L05-proofs",
    "E3g3-L06-proofs",
    "E3g3-c091-gamma",
    "E3g4-c082-hypotheses",
    "E3g4-c085-hypotheses",
    "E3g4-c091-hypotheses",
    "E3g4-c108-hypotheses",
    "E3g4-c096-context",
    "E3g5-c169-c170-basis",
    "E3g5-notation-PQ",
    "E3g6-L05-cor33-hunk",
}

FRESH = {
    "E3g-notation-c138": (
        "PASS",
        "2.4 notation (E3-c138 uses tau, not alpha)",
        "cards.json E3-c138 (line 396-400); L08.html Definition 1.2 (tau weight, alpha reserved for Lesson 6)",
        "Definition 1.2 writes the weight as tau and says alpha is the gains exponent of Lesson 6; card E3-c138 "
        "uses tau. No symbol clash in L08 (ledgers/E3/scripts/E3-g-r7/L08.txt).",
    ),
    "E3g-grade-c142": (
        "PASS",
        "2.3 grades (E3-c142 is the strict case of Theorem 2.2)",
        "cards.json E3-c142; course/modules/E/E3/L08.html Theorem 2.2 proof (strict case)",
        "Re-derived: m = min_i E_Pi u(f); if the E_Pi u(f) are not all equal then max > m, so their uniform average "
        "exceeds m and u^-1 is strictly increasing, so the inequality is strict. Card T grade matches; the proof text "
        "is unchanged since round 6 (L08 hunks were at Section 5, misconception 3, and the quiz).",
    ),
    "E3g-r2-c145-V1": (
        "PASS",
        "2.9 structure (E3-c145 cites its lesson)",
        "cards.json E3-c145; L08.html Definition 3.1 (timing convention)",
        "Card E3-c145 cites Definition 3.1; L08.txt Definition 3.1 states that the gamble pays at date 1 only and that "
        "the value uses a = 1 - 1/psi. Cross-reference resolves (ledgers/E3/scripts/E3-g-r7/cardref7.py: bad 0).",
    ),
    "E3g-r2-L07-G5": (
        "PASS",
        "2.4 math / 2.6 cards (E3-c118 to c126)",
        "cards.json E3-c118..c126 (E3-c121 changed, see E3g6-c121-unrounded); L07.html Definition 1.1 to Remark 2.3",
        "Re-derived in ledgers/E3/scripts/E3-g-r7/num7.py: omega(3/10)=0.285790884905, omega(3/5)=0.391250770027, "
        "threshold 2/3 and 0.585786437627, ratio 0.730454498236 (8dp 0.73045450); Gamma(A,1)=42.86863274, "
        "Gamma(B,1)=39.12507700. Each card value matches; Example 2.1 table (F_A(50)=7/10, F_B(50)=2/5) checked.",
    ),
    "E3g-r2-L08-G7": (
        "PASS",
        "2.4 math / 2.3 grades (E3-c137 to c143)",
        "cards.json E3-c137..c143; L08.html Definition 1.2, Proposition 1.3, Example 1.4, Theorem 2.2, Proposition 2.4",
        "Proposition 2.4 proof re-read: E_p u(f) = u(w_no) + p(u(w_red)-u(w_no)), bracket > 0 by A2, A3; worst prior "
        "P_0 for red, P_90 for black. Card E3-c143 matches. Example 1.4 mean 45/90 = 1/2 (E3-c139) recomputed.",
    ),
    "E3g-r2-L08-G9": (
        "PASS",
        "2.3 grades / 2.2 numbers (E3-c144, c164, c165, c166)",
        "cards.json E3-c144 (line 955), c164, c165, c166; L08.html Example 2.5, Model 2",
        "Exact Fractions (ledgers/E3/scripts/E3-g-r7/num8.py): known red CE 103125, known black CE 106451.6129032, "
        "ambiguous full-set CE 100000 for red and black, prospect wealth equivalent 99892.76695 (printed 99892.7670), "
        "CE of change -107.23304703 cents. All card numbers match.",
    ),
    "E3g-r2-refs-cross": (
        "PASS",
        "2.9 DAG / cross-lesson references used by the cards",
        "cards.json E3-c081, c112, c129, c146, c154; course/modules/E/E3/L04.html Theorem 1.5 (line 89)",
        "L04.html Theorem 1.5 still reads 'F_X(t) <= F_Y(t) for every real t iff E u(X) >= E u(Y) for every "
        "nondecreasing u : S -> R' (finite S). L04 changed this round only in Example 2.5 and Remark text, not the "
        "theorem. Card E3-c129 reads it correctly with X=B, Y=A.",
    ),
    "E3g-r2-registry": (
        "PASS",
        "2.1 citations (registry keys cited by L05-L08 cards)",
        "cards.json E3-c134 (kahneman1979prospect), E3-c157 (ellsberg1961risk), E3-c158 (gilboa1989maxmin)",
        "references/references.json entries (python -I lookup): kahneman1979prospect, ellsberg1961risk, "
        "gilboa1989maxmin, epstein1989substitution all present with status verified. references.json unchanged "
        "since round 6.",
    ),
    "E3g3-c135-terminology": (
        "PASS",
        "2.9 prose (E3-c135 back vs L07 Section 3)",
        "cards.json E3-c135; course/modules/E/E3/L07.html Section 3 (cumulative repair)",
        "Card says 'the cumulative repair of Section 3 is not derived'; L07.txt Section 3 'One repair is cumulative... "
        "This lesson does not derive that repair.' Consistent.",
    ),
    "E3g3-c132-omega": (
        "PASS",
        "2.2 numbers (E3-c132 weighted value under omega_{1/2})",
        "cards.json E3-c132; L07.html Section 4 misconception 3 (the changed paragraph)",
        "omega(0.01)=0.0834030104725, omega(0.99)=0.8298494763709; 100*omega(0.01)+50*omega(0.99)=49.83277487 -> 49.8328; "
        "EV 50.5. Misconception text and card both give 49.8328 vs 50.5 (num7.py). Net effect 7.3403-8.0075 = -0.6672 -> -0.67.",
    ),
    "E3g3-c097-trivia": (
        "PASS",
        "2.7 cards (E3-c097 removed; id list of the slice)",
        "cards.json id list for L05 and L06 (no E3-c097, no E3-c092)",
        "Slice ids re-listed (84 ids, ledgers/E3/scripts/E3-g-r7/cardref7.py); no duplicate fronts or backs in the unit.",
    ),
    "E3g3-basis-wording": (
        "PASS",
        "2.3 grades (basis strings of the C cards)",
        "cards.json E3-c094, c095, c106, c117, c122, c153 (and C cards c093, c096, c127, c128, c131, c169, c170)",
        "Every C card carries a basis naming its lab or problem (checked in cards_L05_L08 scan). E3-c131 basis "
        "'Lab 1, part C (floating point)' matches its lab.",
    ),
    "E3g3-L07-proofs": (
        "PASS",
        "2.4 math (L07 proofs)",
        "course/modules/E/E3/L07.html Definition 1.2, Example 1.4, Remark 1.3, Remark 1.6, Proposition 2.2, Problems P1-P3",
        "Proposition 2.2 proof: V(A)=omega(3/10)(50^a+100^a), V(B)=omega(3/5)100^a; ratio threshold 1/(1+2^-a) re-derived. "
        "P1 closed form re-derived (denominator (sqrt p + sqrt(1-p))^2 = 1 + 2 sqrt(p(1-p))). Remark 1.6 sum 0.89103669 "
        "(unrounded 0.891036686). See the open item E3g7-ex14-monotone for the monotonicity claim.",
    ),
    "E3g3-attribution": (
        "PASS",
        "2.1 / 2.9 (title-only attributions on E3-c134, c157, c158)",
        "cards.json E3-c134, c157, c158; references/references.json",
        "Registry titles: kahneman1979prospect 'Prospect Theory: An Analysis of Decision under Risk' (1979); "
        "ellsberg1961risk 'Risk, Ambiguity, and the Savage Axioms' (1961); gilboa1989maxmin 'Maxmin expected utility "
        "with non-unique prior' (1989). Pages say 'title only' and state no result from these papers.",
    ),
    "E3g3-delta-r3": (
        "PASS",
        "delta read (round-3 row kept; re-read on this pin)",
        "git diff 142ecfc2 9373ef39 for the slice files",
        "Delta read in full for slice files: course/modules/E/E3/L07.html (Example 1.4 para, misconception 3, R3 solution, "
        "quiz explanation), L08.html (Section 5 bullet 2, misconception 3, quiz option), cards.json (E3-c121, E3-c131). "
        "Outside the slice: L02, L03, L04, grader, project.html, lab-E3-project-3 (not verified here).",
    ),
    "E3g4-c130-argument": (
        "PASS",
        "2.4 math / 2.3 grades (E3-c130 'It can')",
        "cards.json E3-c130; course/modules/E/E3/L07.html Proposition 2.2, Remark 1.6, Lab 1 part C",
        "'It can' follows from Prop 2.2 (A's weights 0.57158177 > B's 0.39125077, Remark 1.6) and Lab 1 part C "
        "(42.8686 > 39.1251). Card grade T for the argument, C for the printed numbers is not needed (numbers are proved "
        "in the Example 1.4 closed form).",
    ),
    "E3g4-c142-hypotheses": (
        "PASS",
        "2.4 math / 2.6 cards (E3-c142 hypotheses)",
        "cards.json E3-c142 (line 941); L08.html Theorem 2.2",
        "Card names A1 to A3 of Theorem 2.2 and A2 (u strictly increasing); Theorem 2.2 A1-A3 are the same. Matches.",
    ),
    "E3g4-c155-notation": (
        "PASS",
        "2.4 notation (E3-c155 symbol)",
        "cards.json E3-c155 (line 1031); L08.html Problem R3",
        "nu is a local symbol in R3 (u = -exp(-nu w)); not a registered symbol (notation/notation.json lists only T, Phi, "
        "gamma_3, gamma_4, R^*, R^{e*}, R_f, Q). No clash.",
    ),
    "E3g4-c172-definition": (
        "PASS",
        "2.4 math / 2.3 (E3-c172 definition)",
        "cards.json E3-c172 (line 1150); L08.html Definition 1.2",
        "Definition 1.2 gives V_tau = tau min + (1 - tau) max, so at tau = 1 it equals min E_P u(f). Card matches.",
    ),
    "E3g4-lab-observations": (
        "PASS",
        "2.7 (lab-versus-theorem pairs)",
        "cards.json E3-c101/c117 (L06), E3-c128/c129 (L07), E3-c146/c153 (L08)",
        "L06 c101 is Proposition 1.4 (T) and c117 is the grid check (C, basis says 'finite grid'). L07 c128 is Lab 1 part D "
        "(C) and c129 is Lesson 4 Theorem 1.5 (T). L08 c146 is Proposition 3.2 (T) and c153 is Lab 1 part B (C). Each "
        "lab-derived card is graded C and names its lab; each theorem card is graded T.",
    ),
    "E3g-dup-scan": (
        "PASS",
        "2.7 duplicates (full scan of the unit's cards, and the slice's 84)",
        "course/modules/E/E3/cards.json (171 cards; 84 in the slice)",
        "Exact duplicate fronts and backs over all 171 cards: none. Near pairs (difflib ratio >= 0.5) with a slice card: "
        "E3-c169/c170 (0.62, U vs CE1 questions), E3-c109/c163 (0.57, narrow vs integrated framing), E3-c137/c172 (0.56, "
        "general tau vs tau = 1). Different questions; no duplicate card.",
    ),
    "E3g-r2-V-symbol": (
        "PASS",
        "3 notation: W (prospect value) collisions",
        "cards E3-c100, c104, c105, c107, c116; L06.html Definition 1.3",
        "W = prospect value in L06 only; L08 uses W only as a Python variable in its lab code (no prose or card use). "
        "L07 has no W. No clash within the slice.",
    ),
    "E3g-r2-numbers": (
        "PASS",
        "2.2 numbers in prose and cards (every number in the slice's cards and lessons)",
        "L05..L08 text (ledgers/E3/scripts/E3-g-r7/L0*.txt); cards.json slice; num7.py, num8.py, mono7.py",
        "Every number in the 84 slice cards appears in the L05-L08 text (cardref7.py: numbers missing: none). "
        "Recomputed with Decimal/Fraction: all L05 CE1 and V0 values (80/49, 8/5, 16/7, 160/71, 3/2), L06 values "
        "(200, 50, -100, 100, -200, 5/3, sqrt(5/3), -8.6835), L07 values (above), L08 values (4180000/41, 99523.8095, "
        "548.7805, 22500/41, 103125, 106451.6129, 98352.94, 105822.78, 476.1905, 99892.7670, -107.2330, 5 - sqrt50). "
        "Lab outputs match the prose in every case.",
    ),
    "E3g-r2-lab-twins": (
        "PASS",
        "2.5 labs: run_labs, twins under python -I -W error, page code equals twin, expected block equals output",
        "tests/labs/E3/lab-E3-L05-1.py .. lab-E3-L08-1.py; course/modules/E/E3/L05.html..L08.html lab sections",
        "tools/run_labs.py --unit E3 --page L05..L08: each 'PASS (1/1)', exit 0 (run_labs_L0*.out). Twins run as "
        "python -I -W error: exit 0, stderr 0 bytes (twin_L05.out, twin_L0*.err). Expected blocks match the twin output "
        "(run_labs compares them under the page's tolerance rule).",
    ),
    "E3g-r2-coverage": (
        "PASS",
        "2.9 / 2.7 retrieval: every key result, definition and misconception has a card",
        "L05..L08 Key results tables and misconception sections; cards.json slice",
        "Each L05-L08 key result row maps to a card (e.g. L05 Thm 1.3 -> c080, Cor 1.4 -> c081, Prop 2.2 -> c084, Thm 3.2 "
        "-> c087, Remark 3.4 -> c089; L08 Prop 2.4 -> c143/c154, Prop 3.2 -> c146, Remark 4.2 -> c148). Each of the 12 "
        "misconceptions has a card (L05 c082/c085/c081; L06 c110/c112/c108; L07 c123/c130/c132; L08 c138/c142/c146/c154).",
    ),
    "E3g-r2-grades": (
        "PASS",
        "2.3 grades: card grades against the lesson key-results grades",
        "cards.json slice (L05 20, L06 19, L07 18, L08 27); lessons' key-results tables",
        "Grade counts (this round): L05 T 11 / C 6 / ungraded 3; L06 T 10 / C 3 / ungraded 6; L07 T 11 / C 5 / ungraded 2; "
        "L08 T 18 / C 3 / ungraded 6. Ungraded cards are definitions or remarks with no result claimed. Every key result "
        "graded T in a table is a T card; every lab-read result is a C card.",
    ),
    "E3g-r2-hypotheses": (
        "PASS",
        "2.4 cards carry the hypotheses of the proposition they cite",
        "cards.json slice T cards; cards E3-c148 and E3-c151 (changed in round 5); L08.html Model 4, Remark 4.2",
        "Re-read every T card that cites a proposition: L05 c080-c089 (A1-A4 or psi = 1/gamma, gamma not 0); L06 c101 "
        "(alpha, delta in (0,1), lambda > 0), c102, c104-c105, c107, c111, c113; L07 c121, c125 (A1-A3), c130, c133, "
        "c135; L08 c138, c141-c143, c146 (A1-A5), c148 (u = -1/w, two outcomes), c150, c151, c155, c164-c166, c179. "
        "All carry their hypotheses.",
    ),
    "E3g-r2-scope-words": (
        "PASS",
        "2.4 / 2.9 scope words in the slice (only, all, always, every, any, same, exactly, ...)",
        "ledgers/E3/scripts/E3-g-r7/L05.txt..L08.txt and cards (grep, scoped reading of each hit)",
        "Re-read every hit (grep -o with context). The changed scope claims, L08 Section 5 bullet 2, L08 misconception 3 "
        "and L08 quiz option, state psi > 0, psi != 1, beta in (0,1) and gamma != 1 (the hypotheses of Proposition 3.2). "
        "Other 'every' and 'only' hits are backed by a stated computation or an explicit hypothesis.",
    ),
    "E3g-r2-process-words": (
        "PASS",
        "1.3 / 1.4 banned and process phrases",
        "L05..L08 text and slice cards (grep for we, our, verifier, builder, round, TODO, FIXME)",
        "Hits: 'We write c1 for the date-1 lottery' (L05, mathematical convention), 'so for x < 0 < y we have' (L06), "
        "'do not round to a whole cent' (L08), 'both round to 3.7436' (E3-c131). None is a process word. check_pages "
        "banned-string check passes (check_pages_L05..L08.out).",
    ),
    "E3g-r2-gates": (
        "PASS",
        "2.9 gates: check_pages, check_dag, check_projects, page_smoke, ruff, mypy, verify_refs",
        "course/modules/E/E3/L05..L08.html; tools/*",
        "ledgers/E3/scripts/E3-g-r7/: check_pages_L05..L08.out 'PASS' (exit 0 each); check_dag.out 'check_dag E3: PASS'; "
        "check_projects.out 'check_projects E3: PASS'; ruff_check.out 'All checks passed!'; ruff_format.out '11 files "
        "already formatted'; verify_refs_offline.out 'offline integrity: 560 entries, 0 problems'.",
    ),
    "E3g-r2-delta": (
        "PASS",
        "delta of the slice since the round-6 pin (142ecfc2..9373ef39)",
        "git diff 142ecfc2 9373ef39 for course/modules/E/E3/cards.json, L05.html..L08.html, notation, references",
        "git diff --stat: L02, L03, L04, L07, L08, cards.json, grader/instance.py, grader/test_project.py, project.html, "
        "tests/labs/E3/lab-E3-project-3.py. L05.html and L06.html unchanged. Slice hunks read in full: L07.html lines "
        "83-86, 335-338, 439, 502; L08.html lines 474, 493, 681; cards.json E3-c121, E3-c131 (E3-c178 is an L03 card).",
    ),
    "E3g3-L08-proofs": (
        "PASS",
        "2.4 mathematics: L08 Proposition 1.3, Theorem 2.2, Proposition 2.4, Example 2.5, Proposition 3.2",
        "course/modules/E/E3/L08.html Model 4 and Remark 4.2 (lines 451, 468 unchanged); L08.txt",
        "Proposition 3.2 proof (injectivity of x^(1/a) and the a-th root with a != 0) re-read and correct; Proposition 2.4 "
        "and Theorem 2.2 re-derived; Remark 4.2 identity (1/2)E_pmin + (1/2)E_pmax = E_midpoint by affinity of E_p[1/w] "
        "re-checked. The round-6 changed hunk (Model 4 / Remark 4.2) is the same text as at round 6.",
    ),
    "E3g3-c148-scope": (
        "PASS",
        "2.3 / 2.4 card E3-c148 scope (Remark 4.2 and Section 5 bullet 4)",
        "cards.json E3-c148 (line 981-986); L08.html Remark 4.2, Section 5",
        "Card says 'This is not a general property of alpha-MEU (Remark 4.2)'; Remark 4.2 restricts to u = -1/w and a "
        "two-outcome gamble; Section 5 bullet 4 says the same. Scope matches.",
    ),
    "E3g3-page-smoke": (
        "PASS",
        "2.5 / 2.9 page_smoke for L05..L08 (zero console errors, math rendered, no external requests)",
        "course/modules/E/E3/L05..L08.html",
        "ledgers/E3/scripts/E3-g-r7/page_smoke_full.out (full run, no --skip-sweep): 'page_smoke E3: PASS', L05..L08 each PASS, "
        "exit 0; labs run inside the smoke test with zero console errors.",
    ),
    "E3g3-gates-projects-ruff": (
        "PASS",
        "2.6 project gates and ruff for the slice's twins",
        "tools/check_projects.py; tests/labs/E3/lab-E3-L05-1.py .. lab-E3-L08-1.py",
        "check_projects E3: PASS; ruff check tests/labs/E3: All checks passed!; ruff format --check: 11 files already formatted.",
    ),
    "E3g3-notation-registry": (
        "PASS",
        "3 notation: registered symbols and macros (T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q; macros \\E, \\Prob, \\R)",
        "notation/notation.json (8 registered symbol entries, 26 macros); L05..L08.html",
        "Macro scan of L05..L08 html: \\gamma, \\beta, \\psi, \\alpha, \\delta, \\lambda, \\ell, \\omega, \\tau, \\varpi, \\nu, "
        "\\theta, \\varepsilon, \\Gamma, \\mathcal{P}, \\bar P, \\ast (only as lambda^\\ast), \\E, \\R, \\Prob. No registered "
        "symbol (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) appears in the slice. Macro use is "
        "registered (\\E, \\R, \\Prob).",
    ),
    "E3g3-notation-collisions": (
        "PASS",
        "3 notation: local letters reused with another meaning inside the slice",
        "cards E3-c088, c148, c155; L05 Corollary 3.3; L08 Remark 4.2, Model 4",
        "Within L05: K, H, a, theta, varepsilon each one meaning. Within L06: g, l (ell), lambda, lambda*, lambda_R each one "
        "meaning. Within L07: omega, eta, alpha, Gamma each one meaning. Within L08: tau (weight), gamma, psi, beta, g(p) "
        "(= E_p[1/w], Model 4 and Remark 4.2 only), w_no/w_L (the same 95000-cent outcome named two ways, not two meanings).",
    ),
    "E3g4-c148-notation": (
        "PASS",
        "2.4 notation (card E3-c148: E_P[1/w])",
        "cards.json E3-c148; L08.html Remark 4.2",
        "Card uses E_P[1/w] as Remark 4.2 defines it (E_P[1/w] = p/w_1 + (1-p)/w_L).",
    ),
    "E3g5-c148-utility": (
        "PASS",
        "2.4 hypotheses of card E3-c148 (utility for the affine identity)",
        "cards.json E3-c148; L08.html Remark 4.2, Model 1",
        "Card names u(w) = -1/w (Model 1) and a two-outcome gamble; Remark 4.2 assumes the same. Hypotheses match.",
    ),
    "E3g5-c151-utility": (
        "PASS",
        "2.4 hypotheses of card E3-c151 (maxmin value 99523.8095)",
        "cards.json E3-c151 (line 1002-1007); L08.html Model 4",
        "Maxmin CE = 1/(1/3/110000 + 2/3/95000) = 99523.8095 (num8.py: 99523.80952380953); worst prior 1/3 = 30/90. Card matches Model 4.",
    ),
    "E3g5-c152-utility": (
        "PASS",
        "2.4 hypotheses of card E3-c152 (risk premium 548.7805)",
        "cards.json E3-c152 (line 1009); L08.html Model 1 and Section 4",
        "102500 - 4180000/41 = 22500/41 = 548.780487804878 (num8.py); 5.4878 CU. Matches card, Problem E3, Section 4.",
    ),
    "E3g-r2-L08-G8": (
        "PASS",
        "2.2 / 2.3 / 2.4 L08 numbers and grades for cards E3-c146, c148, c149, c150, c151, c152",
        "cards.json E3-c146, c148, c149, c150, c151, c152 (changed in round 5, unchanged since); L08.html Section 4",
        "All six card numbers recomputed (num8.py, num7.py): 4180000/41, -2.071068 (5 - sqrt 50), 99523.8095, 548.7805. "
        "Grades T: each is a closed-form result on the page (Models 1, 2, 4 and Proposition 3.2).",
    ),
    "E3g-r2-L07-G6": (
        "PASS",
        "2.6 / 2.8 L07 lab part C and cards E3-c127, c128, c131, c133, c135 (was FAIL in round 6, fixed)",
        "cards E3-c127, c128, c131 (line 863-870), c133, c135; L07.html Lab 1 parts C and D (lab output at L07.txt)",
        "Lab output (L07.txt, twin_L07.out): Gamma(A) 42.8686, Gamma(B) 39.1251 at alpha = 1; 4.8788, 3.9125 at alpha = 0.5; "
        "'10 of 10'. Re-derived (num7.py) and matched. E3-c131 back now reads 3.7436 from 3.74355573 and the 8-decimal "
        "values 42.86863274 - 39.12507700 = 3.74355574 (both round to 3.7436), so the round-6 failure is fixed.",
    ),
    "E3g4-c131-unrounded": (
        "PASS",
        "2.2 numbers: card E3-c131 (unrounded difference) (was FAIL in round 6, fixed)",
        "cards.json E3-c131 (line 863-869); L07.html E2 solution",
        "Round-6 FAIL: the back labelled the 8-decimal values 'unrounded'. Now: 'The unrounded values differ by 3.74355573 "
        "(computed to 40 digits); their eight-decimal roundings ... differ by 3.74355574, and both round to 3.7436.' "
        "num7.py: 40-digit difference 3.7435557330, 8dp difference 3.74355574. Correct.",
    ),
    "E3g6-psi-domain": (
        "PASS",
        "2.4 scope: 'for every psi != 1' now carries psi > 0 (was FAIL in round 6, fixed)",
        "L08.html line 477 (Section 5 bullet 2), line 496 (misconception 3), line 684 (quiz option); cards.json E3-c146 (line 968)",
        "Regex scan of L05..L08.html and cards.json for 'every ... psi': every L08 hit now reads 'psi > 0 with psi != 1' "
        "(lines 477, 496, 684); the card E3-c146 back says 'for every psi and beta' only after its own sentence stating "
        "A1 to A5 (psi > 0, psi not 1, gamma not 1, beta in (0,1), c0 > 0, positive outcomes), so its scope is carried by "
        "its own hypotheses. L05 hits are the distractor '1/gamma at every psi' and 'at every plan' (deterministic, stated).",
    ),
    "E3g6-L07-ex14-unrounded": (
        "PASS",
        "2.2 numbers vs unrounded values: L07 Example 1.4 labels (was FAIL in round 6, fixed)",
        "course/modules/E/E3/L07.html line 86 (Example 1.4 paragraph)",
        "The text now reads 'The values used below, rounded to eight decimals, are ... Their unrounded values, to ten "
        "decimals, are 0.2857908849, 0.3912507700 and 0.3535533906.' num7.py: 0.2857908849045, 0.3912507700268, "
        "0.3535533905933. Correct.",
    ),
    "E3g6-c121-unrounded": (
        "PASS",
        "2.2 numbers vs unrounded values: card E3-c121 back (was FAIL in round 6, fixed)",
        "cards.json E3-c121 (line 790-795)",
        "Back now reads 'To eight decimals, omega(3/10) = 0.28579088, omega(3/5) = 0.39125077 and omega(1/2) = 0.35355339 "
        "(Example 1.4).' num7.py gives 0.2857908849, 0.3912507700, 0.3535533906 (rounded to eight decimals: 0.28579088, "
        "0.39125077, 0.35355339). Correct.",
    ),
    "E3g6-c179": (
        "PASS",
        "2.7 card E3-c179 (new in round 6): Epstein-Zin CE of the Section 4 gamble, Model 3",
        "cards.json E3-c179 (line 1189-1194); L08.html Model 3 and Proposition 3.2",
        "Card: 101951.2195 cents at psi = 1/2, beta = 0.95, gamma = 2 (Model 3, Proposition 3.2). Proposition 3.2 hypotheses "
        "A1 to A5 hold (psi = 1/2 > 0, psi != 1, gamma = 2, beta = 0.95, c0 = 100000 > 0, positive outcomes). Lab part A "
        "prints 101951.2195. Matches.",
    ),
    "E3g6-L07-intro-hunk": (
        "PASS",
        "2.9 prose: L07 introduction paragraph (why it matters)",
        "course/modules/E/E3/L07.html line 52 (introduction) and the header paragraph of the lesson",
        "The introduction says the lesson 'gives a pair of lotteries on which the weighted value ... ranks a first-order-"
        "dominated lottery above its dominator' and that 'its weights are values of Example 1.4'. Both are backed by Example 2.1, "
        "Proposition 2.2 and Example 1.4. No overclaim.",
    ),
    "E3g6-L08-model4-hunk": (
        "PASS",
        "2.4 / 2.9 L08 Model 4 and Remark 4.2 hunks",
        "course/modules/E/E3/L08.html lines 451 and 468 (Model 4 and Remark 4.2 text, unchanged since round 6)",
        "Model 4: worst prior p = 30/90 = 1/3 and maxmin 1/(1/3/w1 + 2/3/wL) = 99523.8095 (num8.py). Remark 4.2 argument "
        "re-derived (affinity of g(p) = p/w1 + (1-p)/wL). Correct.",
    ),
    "E3g6-verify-refs": (
        "PASS",
        "2.1 citations: registry integrity for the slice's keys",
        "references/references.json; cards E3-c134, c157, c158; L05 Section 9, L06 Section 9, L07 Section 8, L08 Section 10",
        "ledgers/E3/scripts/E3-g-r7/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems'. Registry keys "
        "cited in the slice: epstein1989substitution (L05), kahneman1979prospect (L06, L07 cards), ellsberg1961risk and "
        "gilboa1989maxmin (L08), each with status verified.",
    ),
    "E3g6-banned-phrases": (
        "PASS",
        "1.3 / 1.4 banned and process phrases; placeholders in the four lesson texts and slice cards",
        "L05..L08 text and slice cards; tools/check_pages.py banned-string check",
        "check_pages E3 L05..L08: PASS (ledgers/E3/scripts/E3-g-r7/check_pages_L0*.out), which runs the banned-string and "
        "placeholder check. Grep for TODO, FIXME, TBD, lorem, XXX, placeholder over the L05..L08 text and the 84 slice cards: 0 hits.",
    ),
    "E3g6-pytest": (
        "PASS",
        "2.5 relevant pytest over the lab and page tooling",
        "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py (-k E3)",
        "ledgers/E3/scripts/E3-g-r7/pytest_r7.out: 15 test cases (progress line of 15 dots), exit 0.",
    ),
}

NEW_ROWS = [
    {
        "id": "E3g7-ex14-monotone",
        "check": (
            "2.4 math / 2.9 structure: omega_{1/2} is called a weighting function (Definition 1.1 requires nondecreasing "
            "on [0,1]) but nondecreasing is shown only on a grid"
        ),
        "location": (
            "course/modules/E/E3/L07.html line 83 (Example 1.4 title '(a weighting function with eta = 1/2)'), lines 90-92 "
            "(Observation 1.5: 'nondecreasing on the 1001 equally spaced probabilities'; 'beyond the grid it is a "
            "hypothesis'); line 123 (Proposition 2.2 A2 'the weighting function omega = omega_{1/2} of Example 1.4')"
        ),
        "status": "FAIL",
        "evidence": (
            "Definition 1.1 requires omega nondecreasing on [0,1]. Example 1.4 is titled as a weighting function and "
            "Proposition 2.2 A2 uses it as one, but the only monotonicity shown is the grid check of Observation 1.5 "
            "(lab part A: 'nondecreasing = True' on 1001 points), and the same observation says that beyond the grid "
            "it is a hypothesis. The claim is true: the 2,000,001-point check (mono7.py) finds no decrease, and with "
            "q = sqrt(p(1-p)) and g = 1 + 2q, f'(p) = (q + 2p^2) / (2 sqrt(p) q g^2) > 0 on (0,1) (numeric derivative "
            "positive at p = 0.01 ... 0.99). The page does not prove it, and the example's title asserts it."
        ),
        "fix": (
            "In Example 1.4 add: 'Differentiating, omega'(p) = (q + 2p^2)/(2 sqrt(p) q (1 + 2q)^2) with q = sqrt(p(1-p)), "
            "which is positive on (0,1), so omega_{1/2} is nondecreasing on [0,1] and is a weighting function of "
            "Definition 1.1.' Then delete 'and beyond the grid it is a hypothesis' from Observation 1.5 (keep the grid "
            "statements about the sign change and the crossing 0.278 as finite checks)."
        ),
        "verdict": "PLAUSIBLE",
    },
    {
        "id": "E3g7-card-xrefs",
        "check": "2.9 structure: every 'Remark x.y', 'Proposition x.y', 'Example x.y', 'Model', 'Problem', section and misconception reference in the 84 slice cards resolves in its lesson",
        "location": "cards.json slice (84 cards); ledgers/E3/scripts/E3-g-r7/cardref7.py",
        "status": "PASS",
        "evidence": "cardref7.py: checked 84 slice cards, bad 0. Every referenced label (Definition, Proposition, Theorem, Corollary, Remark, Example, Observation, Model, Problem, Lab 1 part) occurs in its own lesson text; every section-number reference (L05 section 5, L06 section 5, L07 section 4, L08 section 6 = Misconceptions) matches the misconception it names.",
        "fix": "",
    },
    {
        "id": "E3g7-hours",
        "check": "2.10 hours arithmetic: hub split against lesson study-hour labels",
        "location": "course/modules/E/E3/index.html (data-hours-lessons 56, project 14; 'Eight lessons of seven study hours each, which is 56 hours in total'); L05..L08.html 'E3 · Lesson n of 8 · 7 study hours'",
        "status": "PASS",
        "evidence": "Eight lessons times 7 hours is 56, matching the hub's 'Eight lessons of seven study hours each, which is 56 hours in total' and the four lesson labels L05..L08 (each '7 study hours'); 56 + 14 = 70, matching 'Module E3 · Tier U · 70 hours'.",
        "fix": "",
    },
]

REMOVED_STATUS_NOTE = (
    "Round-6 FAIL rows E3g-r2-L07-G6, E3g4-c131-unrounded, E3g6-psi-domain, E3g6-L07-ex14-unrounded and "
    "E3g6-c121-unrounded are re-verified on this pin and now PASS (the text fixes are present, see their evidence)."
)


def main() -> int:
    r6 = json.loads(R6.read_text(encoding="utf-8"))
    rows = []
    missing = []
    for old in r6["rows"]:
        rid = old["id"]
        if rid in CARRY:
            rows.append(
                {
                    "id": rid,
                    "check": old["check"],
                    "location": old["location"],
                    "status": "PASS",
                    "evidence": CARRY_PREFIX + old["evidence"],
                }
            )
        elif rid in FRESH:
            status, check, location, evidence = FRESH[rid]
            rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence})
        else:
            missing.append(rid)
    if missing:
        print("UNCOVERED round-6 ids:", missing, file=sys.stderr)
        return 1
    for nr in NEW_ROWS:
        rows.append(
            {
                "id": nr["id"],
                "check": nr["check"],
                "location": nr["location"],
                "status": nr["status"],
                "evidence": nr["evidence"],
                **({"fix": nr["fix"]} if nr.get("fix") else {}),
                **({"verdict": nr["verdict"]} if nr.get("verdict") else {}),
            }
        )
    counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
    for r in rows:
        counts[r["status"]] += 1
    carried = sum(1 for r in rows if r["evidence"].startswith("Carried from round 6"))
    frag = {
        "unit": "E3",
        "slice": "g",
        "round": 7,
        "verifier": "Haiku independent verifier, E3-g round 7 (did not build E3)",
        "pin": "9373ef398589097500ea849e30ff9da423b98943",
        "base": "142ecfc2bd27061de18bd67e83df81e69f5c249d (round-6 pin; delta 142ecfc2..9373ef39 read for the slice)",
        "checkout": "/Users/billyribeiro/.fanout/wt/verifyD7-E3-g (detached at 9373ef39)",
        "scratch": "ledgers/E3/scripts/E3-g-r7/ (strip7.py, cards_L05_L08.txt, L05..L08.txt lesson text read in full, num7.py, num8.py, mono7.py, cardref7.py, gate outputs)",
        "verified_at": "2026-11-04T10:55:08+00:00",
        "verdict": "FAIL",
        "rows": rows,
        "mutants": [],
        "registry_flags": [],
        "freshness_flags": [],
        "notes": [
            "Slice g is the 84 E3 cards of L05 (20), L06 (19), L07 (18) and L08 (27), read against the four lesson texts in full "
            "(L05..L08.txt extracted from the pin's HTML and read line by line; cards read in full in cards_L05_L08.txt).",
            "Delta 142ecfc2..9373ef39 for the slice: L07.html (Example 1.4, Section 4 misconception 3, the R3 solution, quiz explanation), "
            "L08.html (Section 5 bullet 2, misconception 3, quiz option), cards.json (E3-c121, E3-c131). L05.html and L06.html are "
            "byte-identical to the round-6 pin, so their round-6 PASS rows are carried with the prefix.",
            REMOVED_STATUS_NOTE,
            "Not a project slice: no student-error mutants and no alternative implementations are part of this slice. mutants is empty by design.",
            "Outside this slice, not verified here: cards E3-c175 and E3-c178 (L03 card, reworded this round), L02, L03, L04 hunks (not cited as slice subjects beyond L04 Theorem 1.5, which is unchanged).",
            "One FAIL row (E3g7-ex14-monotone) is a rigour gap, not a wrong number: omega_{1/2} is monotone (checked), but the page does not prove it and calls the example a weighting function. Its fix is one derivative line.",
        ],
        "summary": {
            "rows": len(rows),
            "pass": counts["PASS"],
            "fail": counts["FAIL"],
            "unverifiable": counts["UNVERIFIABLE"],
            "mutants": 0,
            "mutants_killed": 0,
            "carried_from_round_6": carried,
        },
    }
    out = ROOT / "ledgers/E3/E3-g.json"
    out.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("wrote", out, "rows", len(rows), counts, "carried", carried)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
