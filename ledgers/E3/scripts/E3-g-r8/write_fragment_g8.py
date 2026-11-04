import json
from datetime import datetime, timezone

R7 = json.load(open('/Users/billyribeiro/.fanout/frags/D-E3-g.round7.json', encoding='utf-8'))
PIN = '2d755599d8d74df292e3e43025f0458c4053802e'
PREV = '9373ef398589097500ea849e30ff9da423b98943'
S = 'ledgers/E3/scripts/E3-g-r8/'
old = {r['id']: r for r in R7['rows']}

CARRY = 'Carried from round 7 (course/modules/E/E3/L05.html, L06.html and the L05/L06 entries of cards.json byte-identical since the round-7 pin 9373ef39; notation/notation.json, references/references.json, tests/labs/E3/ unchanged): '
MIXED = 'Carried from round 7 (L05/L06 members only: L05.html, L06.html and their card entries byte-identical since the round-7 pin 9373ef39): '

fresh = {
 'E3g-notation-c138': 'Re-read L08 Definition 1.2 (ledgers/E3/scripts/E3-g-r8/L08.txt): weight written tau, alpha reserved for Lesson 6 (L06.html line 28 says alpha is the curvature parameter for gains). cards.json E3-c138 (one-element prior set, T) matches Proposition 1.3. No registered symbol used (notation/notation.json has no tau or alpha).',
 'E3g-grade-c142': 'Re-derived Theorem 2.2 strict case: if the E_Pi u(f) are not all equal then max > m, so their uniform average exceeds m and u^-1 is strictly increasing, so the inequality is strict. E3-c142 (T) states the strict case with A2 (u strictly increasing) and A3 (finite outcomes). L08 text read in full; the proof is unchanged.',
 'E3g-r2-c145-V1': 'L08 Definition 3.1 read in full: gamble pays at date 1 only, a = 1 - 1/psi, value formula as in Epstein-Zin. E3-c145 cites Definition 3.1 and matches it (cardref8.py: checked 85, bad 0).',
 'E3g-r2-L07-G5': 'Re-verified this round (L07 changed): Definition 1.1 to Remark 2.3 read in full (L07.txt). E3-c118 to c126 match the lesson. Example 1.4 now has the derivative proof (checked, see E3g8-L07-ex14-derivative). E3-c121 values 0.28579088, 0.39125077, 0.35355339 re-derived with Decimal at 60 digits (ledgers/E3/scripts/E3-g-r8/num_L07_r8.py).',
 'E3g-r2-L08-G7': 'Re-verified (L08 read in full): Definition 1.2, Proposition 1.3, Example 1.4, Theorem 2.2, Proposition 2.4 match E3-c137 to c143 and the card grades; the Proposition 2.4 proof (bracket positive, min at p=0 and at q=0) checked.',
 'E3g-r2-L08-G9': 'Re-verified: E3-c144 (changed this round, now red bet only, 103125 cents) and E3-c164, c165, c166 against Example 2.5 and Model 2 (L08.txt). 103125 = 1/((1/3)/110000 + (2/3)/100000) and -107.2330 cents = 100 x (-1.072330 CU) re-derived (num_L07_r8.py, Fraction check in ledgers/E3/scripts/E3-g-r8/).',
 'E3g-r2-refs-cross': 'Re-verified: L04 Theorem 1.5 (L04.txt line 36) is unchanged by the delta (the L04 hunks are at lines 175, 492, 572 of L04.html and touch the lab hypothesis and problems only). E3-c129 and the L07 Section 2 citation match its statement (FOSD B over A iff E u(B) >= E u(A) for nondecreasing u on S). Cited L05/L06 cards unchanged.',
 'E3g-r2-registry': 'Re-verified: references/references.json titles: kahneman1979prospect = "Prospect Theory: An Analysis of Decision under Risk"; ellsberg1961risk = "Risk, Ambiguity, and the Savage Axioms"; gilboa1989maxmin = "Maxmin expected utility with non-unique prior". E3-c134, c157, c158 and the lesson text (title only) match. verify_refs --offline: 560 entries, 0 problems.',
 'E3g3-c135-terminology': 'Re-verified: L07 Section 3 (cumulative repair, "not derived") and E3-c135 (Tail_B(50)=Tail_A(50)=3/5, Tail_B(100)=3/5 > Tail_A(100)=3/10, Problem R2) checked; numbers from Example 2.1.',
 'E3g3-c132-omega': 'Re-verified: E3-c132 (49.8328 against 50.5) and L07 Section 4 misconception 3 (unchanged paragraph) match; 0.99 x 50 + ... computed: omega(0.01)*100 + omega(0.99)*50 = 49.83277487 (Decimal), expected value 50.5.',
 'E3g3-L07-proofs': 'Re-verified L07 proofs in full: Definition 1.2, Example 1.4 (new derivative proof checked line by line: q\'=(1-2p)/(2q), g\'=(1-2p)/q, qg - 2p(1-2p) = q + 2p^2 using q^2 = p - p^2; omega\' = (q+2p^2)/(2 sqrt(p) q (1+2q)^2) matches a finite difference to 2e-9), Remark 1.3, Remark 1.6, Proposition 2.2, Problems P1-P3 (P3 threshold re-derived).',
 'E3g3-attribution': 'Re-verified: E3-c134, c157, c158 cite only registry keys present in references/references.json; the lesson texts say title only; the titles match (see E3g-r2-registry).',
 'E3g3-delta-r3': 'Delta 9373ef39..2d755599 for the slice re-read (ledgers/E3/scripts/E3-g-r8/): L07.html lines 83-92 (Example 1.4 derivative, Observation 1.5), L08.html line 427 (Section 4 interpretation paragraph, "the expectation of 1/w is affine in p") and line 699 (quiz option L08q10), cards.json E3-c131, E3-c144, new E3-c182. Other hunks in the commit are L02, L03, L04, E4, FC, CS2 and project/grader files, not slice subjects (cards c047, c050, c067, c178, c180, c181 are L03/L04).',
 'E3g4-c130-argument': 'Re-verified: E3-c130 (0.57158177 > 0.39125077; 42.8686 and 39.1251) against Proposition 2.2, Remark 1.6 and Lab 1 part C (run output in ledgers/E3/scripts/E3-g-r8/twin_L07.out).',
 'E3g4-c142-hypotheses': 'Re-verified: E3-c142 carries Theorem 2.2 hypotheses A1 to A3 in its back text; L08 Theorem 2.2 read in full.',
 'E3g4-c155-notation': 'Re-verified: E3-c155 (u strictly increasing, -exp(-nu w), any nu > 0) matches Theorem 2.2 A2 and Problem R3 in L08.txt; the symbol nu is local to L08 and not registered in notation/notation.json.',
 'E3g4-c172-definition': 'Re-verified: E3-c172 (V_tau at tau = 1 equals min over P of E_P u(f)) matches L08 Definition 1.2.',
 'E3g4-lab-observations': 'Carried for E3-c101 and E3-c117 (L06 cards, byte-identical since round 7). Re-verified for E3-c128 and E3-c129 (L07), E3-c146 and E3-c153 (L08) against lab output in ledgers/E3/scripts/E3-g-r8/twin_L07.out and twin_L08.out.',
 'E3g-dup-scan': 'Re-run on the current cards.json: 174 cards in the file, 85 in L05 to L08, no duplicate ids, no duplicate fronts or backs. Near-duplicate scan (Jaccard > 0.35): E3-c144 and E3-c182 share a template but ask the red and black CE respectively (different facts, 103125 vs 106451.6129); no other pair in the slice is a duplicate.',
 'E3g-r2-numbers': 'Every number in L07 and L08 prose and cards recomputed with Decimal (60 digits) and Fraction (ledgers/E3/scripts/E3-g-r8/num_L07_r8.py and the inline checks recorded in the notes). Examples: omega(3/10)=0.2857908849, omega(3/5)=0.3912507700, omega(1/2)=0.3535533906, omega(2/5)=0.31945492, ratio 0.7304544982, Gamma(A)=42.8686327357 and Gamma(B)=39.1250770027 at alpha=1, diff 3.7435557330; L08: 4180000/41=101951.2195, 99523.8095 (1/3), 99892.7670, 548.7805 (=22500/41), 98352.94 (p=1/4), 105822.78 (p=3/4). All match.',
 'E3g-r2-lab-twins': 'Re-run this round for L07 and L08: python3 -I -W error tests/labs/E3/lab-E3-L07-1.py and L08 exit 0, empty stderr; page code equals the twin (stripped), and the expected block equals the twin output (stripped) for both. run_labs E3 --page L07 and --page L08: PASS. L05/L06 twins and pages are byte-identical to round 7 (carried).',
 'E3g-r2-coverage': 'Re-verified L07 and L08 key-results rows and misconceptions against cards: L07 rows map to E3-c121, c120, c123, c125/c124/c126, c129, c122, c134; misconceptions to c130, c123, c132. L08 rows map to c138, c141, c143/c154, c146, c149/c150/c151/c179, c148, c165/c144/c182, c157, c158; misconceptions to c154, c138/c142, c146/c153. L05/L06 coverage carried.',
 'E3g-r2-grades': 'Re-counted this round: L05 20, L06 19, L07 18, L08 28 (was 27; E3-c182 added, T). Key-results table grades match the card grades (L07: T,T,T,T,T,C,C,T; L08: T,T,T,T,T,T,T,C,C,T as listed). No card grade changed except E3-c131 wording (grade C unchanged).',
 'E3g-r2-hypotheses': 'Re-verified every T card in L07 and L08 against its proposition hypotheses: E3-c124 to c126 (A1 to A3 of Proposition 2.2), c129 (finite outcome set), c141, c143, c146 (A1 to A5), c148 (u = -1/w, two-outcome gamble), c150 and c164 to c166 (alpha, delta, lambda and the prize structure stated), c179 (psi = 1/2, beta = 0.95, gamma = 2 satisfy A1 to A5), c155 (A2 only, as the card says), c182 and c144 (u = -1/w stated).',
 'E3g-r2-scope-words': 'Grep of L07 and L08 text and cards for only, all, always, every, any, exactly, drives, same, each: each hit read in context; each universal claim has a computation or a named hypothesis (Example 1.4 derivative and MVT; Proposition 3.2 A1 to A5; Theorem 2.2 A2; Remark 1.6 arithmetic).',
 'E3g-r2-process-words': 'grep -i -E "\\b(we|our|verifier|builder|round|TODO|FIXME)\\b" over L07.txt and L08.txt: only "rounds" in the L08 Lab 1 docstring (code, not learner prose).',
 'E3g-r2-gates': 'Re-run this round: check_pages --unit E3 PASS (exit 0), --page L07 PASS, --page L08 PASS; check_dag --unit E3 PASS; check_projects --unit E3 PASS; page_smoke --unit E3 --pages L07 L08 PASS; build_site --check "site data current: 6 outputs" exit 0; render_curriculum.py produced no change to CURRICULUM.md or curriculum/curriculum.json (git diff empty); verify_refs --offline 560 entries 0 problems; pytest -k E3 on tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py: 15 passed; ruff check tests/labs/E3 tools/check_pages.py: all checks passed. Outputs in ledgers/E3/scripts/E3-g-r8/.',
 'E3g-r2-delta': 'Delta 9373ef39..2d755599 for the slice files: course/modules/E/E3/cards.json (per-id diff: changed ids E3-c131, E3-c144, E3-c182 in L05 to L08; other changed ids are L03/L04 c047, c050, c067, c178, c180, c181), L07.html, L08.html; L05.html, L06.html, notation/, references/, tests/labs/E3/ and tools/ and tests/*.py unchanged (git diff --quiet).',
 'E3g3-L08-proofs': 'Re-verified L08 Model 4 and Remark 4.2 in full (L08.txt): the sentence "the inverse expectation is affine in p" is replaced by "the expectation of 1/w is affine in p" in both the Section 4 interpretation paragraph (line 427) and quiz option L08q10 (line 699). The corrected wording is right: E_P[1/w] = p/w1 + (1-p)/wL is affine in p, and CE = 1/E_P[1/w].',
 'E3g3-c148-scope': 'Re-verified: E3-c148 (back text: "This is not a general property of alpha-MEU (Remark 4.2)") matches Remark 4.2 hypotheses (u = -1/w, two-outcome gamble).',
 'E3g3-page-smoke': 'Re-run: page_smoke --unit E3 --pages L07 L08 PASS (both pages, labs lab-E3-L07-1 and lab-E3-L08-1 run). L05 and L06 pages carried from round 7 (byte-identical).',
 'E3g3-gates-projects-ruff': 'Re-run: check_projects --unit E3 PASS (exit 0); ruff check tests/labs/E3 tools/check_pages.py: All checks passed (exit 0). Project files are outside this slice.',
 'E3g3-notation-registry': 'notation/notation.json byte-identical to the round-7 pin (8 symbol entries, 26 macros). Symbols used by L07 and L08 (omega, tau, alpha, gamma, psi, beta, eta, q, g, Gamma, V, CE, P-bar, nu, varpi, lambda, delta) are not registered; none collides with a registered symbol (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q). Local q and g are defined in Example 1.4 before use.',
 'E3g3-notation-collisions': 'L08 Remark 4.2, Model 4 and L08 Problem R3 read: no registered symbol reused. E3-c088 (L05 Corollary 3.3) is carried.',
 'E3g4-c148-notation': 'Re-verified: E3-c148 and L08 Remark 4.2 use only the local symbols tau and g and the registered-free letter p; no collision.',
 'E3g5-c148-utility': 'Re-verified: E3-c148 and L08 Model 1 and Remark 4.2: u(w) = -1/w (CRRA, gamma = 2) stated where the utility is used.',
 'E3g5-c151-utility': 'Re-verified: E3-c151 (99523.8095 cents at P(red)=1/3, with u = -1/w) against Model 4 and lab output part A (twin_L08.out line 7).',
 'E3g5-c152-utility': 'Re-verified: E3-c152 (548.7805 cents = 5.4878 CU) against the L08 Problem E3 solution and Remark 4.2; 102500 - 4180000/41 = 22500/41.',
 'E3g-r2-L08-G8': 'Re-verified: E3-c146, c148, c149, c150, c151, c152 against L08 Section 4 (Models 1 to 4) and Remark 4.2; all numbers re-derived (see E3g-r2-numbers).',
 'E3g-r2-L07-G6': 'Re-verified: E3-c127, c128, c131, c133, c135 against L07 Lab 1 parts C and D and the lab output (twin_L07.out lines 17 to 19); c131 wording updated this round (see E3g8-c131-basis).',
 'E3g4-c131-unrounded': 'Re-verified: E3-c131 (3.7436; unrounded difference 3.74355573 at 40 digits, reproduced with Decimal at 60 digits: 3.7435557330) and the L07 E2 solution text. The 40-digit values are not printed by the lab; the card basis is the float evaluation of the lab quantities (also 3.74355573). See E3g8-c131-basis.',
 'E3g6-psi-domain': 'Re-verified L08 Section 5 bullet 2, misconception 3 and quiz option (lines 477, 496, 684 of L08.html): psi > 0 and psi != 1 are stated; E3-c146 (line 968) matches.',
 'E3g6-L07-ex14-unrounded': 'Re-verified L07 Example 1.4 paragraph (L07.html line 86): unrounded values 0.2857908849, 0.3912507700, 0.3535533906 match the Decimal computation exactly to 10 decimals.',
 'E3g6-c121-unrounded': 'Re-verified: E3-c121 (cards.json lines 790-795) gives omega closed form and eight-decimal values 0.28579088, 0.39125077, 0.35355339, matching the 60-digit computation.',
 'E3g6-c179': 'Re-verified: E3-c179 (101951.2195 cents at psi = 1/2, beta = 0.95, gamma = 2; Model 3, Proposition 3.2) matches L08 Model 3 and the lab output part A (twin_L08.out line 6).',
 'E3g6-L07-intro-hunk': 'Re-verified L07 introduction (L07.html line 52 region, L07.txt): "Expected utility with a nondecreasing utility cannot do this on a finite set of outcomes (Lesson 4, Theorem 1.5)" matches L04 Theorem 1.5 (L04.txt line 36).',
 'E3g6-L08-model4-hunk': 'Re-verified L08.html lines 451 and 468 (Section 4 Model 4 and Remark 4.2 unchanged since round 6) plus the changed line 427 wording (see E3g3-L08-proofs).',
 'E3g6-verify-refs': 'Re-run verify_refs --offline: "offline integrity: 560 entries, 0 problems", exit 0.',
 'E3g6-banned-phrases': 'check_pages --unit E3 PASS (the banned-string check covers L07 and L08 prose): exit 0.',
 'E3g6-pytest': 'Re-run: pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -k E3: 15 passed (exit 0).',
 'E3g7-ex14-monotone': 'FIXED on this pin and re-verified. L07.html Example 1.4 now proves nondecreasing by the derivative (omega\'(p) = (q + 2p^2)/(2 sqrt(p) q (1+2q)^2) > 0 on (0,1), checked symbolically and by finite difference, max error 2e-9), with continuity on [0,1] and the mean value theorem; Observation 1.5 now says the monotonicity is proved in Example 1.4, and the grid facts (1 sign change, last grid point 0.278; omega(0.279) = 0.27844 < 0.279) are labelled finite checks. The round-7 FAIL is closed.',
 'E3g7-card-xrefs': 'Re-run cardref8.py on this pin: "checked 85 bad 0", "numbers missing: []", no duplicate fronts or backs.',
 'E3g7-hours': 'L07 and L08 headers read: "E3 · Lesson 7 of 8 · 7 study hours" and "E3 · Lesson 8 of 8 · 7 study hours"; index.html byte-identical to round 7 (not in the delta), so the hub split is unchanged; check_pages E3 PASS (hub hours arithmetic). L05 and L06 hours carried.',
}

carry = {
 'E3g-grade-c090': 'L05 Corollary 3.3, Remark 3.4 and E3-c090: ',
 'E3g-r2-L05-G1': 'L05 cards E3-c078 to c087 and L05 Definitions/Theorems: ',
 'E3g-r2-L05-G3': 'L05 Remark 1.5 and L06 Propositions 1.4, 2.1, 2.2 with E3-c098 to c105: ',
 'E3g-r2-L06-G4': 'L06 Remarks 2.4, 2.5, 3.1, 3.2 and E3-c107, c108, c109 to c113, c163: ',
 'E3g3-c091-gamma': 'E3-c091 and L05 Remark 3.4, Theorem 3.2: ',
 'E3g3-c097-trivia': 'L05 and L06 card id lists (no E3-c092 and no E3-c097 in the current cards.json, confirmed this round): ',
 'E3g3-L06-proofs': 'L06 Proposition 1.4, Propositions 2.1, 2.2 and Remarks 1.5, 2.4, 2.5, 3.1, 3.2: ',
 'E3g4-c082-hypotheses': 'E3-c082 and L05 Remark 1.5: ',
 'E3g4-c085-hypotheses': 'E3-c085 and L05 Remark 2.3, Proposition 2.2: ',
 'E3g4-c091-hypotheses': 'E3-c091 and L05 Remark 3.4: ',
 'E3g4-c108-hypotheses': 'E3-c108 and L06 Remark 2.5: ',
 'E3g4-c096-context': 'E3-c096 and L05 Lab 1 predicted block: ',
 'E3g5-c169-c170-basis': 'E3-c169, c170 (L05, grade C) and the L05 Lab 1 predicted block: ',
 'E3g-r2-V-symbol': 'E3-c100, c104, c105, c107, c116 and L06 Definition 1.3: ',
 'E3g-r2-L05-G2': 'E3-c088, c089, c090, c091 and L05 Corollary 3.3, Remark 3.4: ',
 'E3g3-L05-proofs': 'L05 proofs (L05.txt, Corollary 3.3 line unchanged since round 6): ',
 'E3g5-notation-PQ': 'L05 Corollary 3.3 and E3-c088 with notation/notation.json (byte-identical): ',
 'E3g6-L05-cor33-hunk': 'L05.html line 147 and text/L05.txt Corollary 3.3: ',
}
mixed = {
 'E3g3-basis-wording': 'L05 and L06 members (E3-c093, c094, c095, c096, c106, c117, c169, c170): carried. Re-read this round for the L07 and L08 members: E3-c122 (grade C, Lab 1 part A, 0.278), c127 and c128 (Lab 1 parts C and D), c131 (grade C, see E3g8-c131-basis), c153 (grade C, Lab 1 part B): basis wording matches the lab output (ledgers/E3/scripts/E3-g-r8/twin_L07.out and twin_L08.out). ',
 'E3g4-lab-observations': 'See the fresh part in the evidence below. ',
 'E3g-r2-lab-twins': 'L05 and L06 twins and pages carried; L07 and L08 re-run this round: ',
 'E3g3-page-smoke': 'L05 and L06 pages carried; L07 and L08 re-run this round: ',
 'E3g3-notation-collisions': 'L05 Corollary 3.3 (E3-c088) carried; L08 re-verified this round: ',
 'E3g7-hours': 'L05 and L06 hours carried. ',
}

rows = []
for rid in [r['id'] for r in R7['rows']]:
    prev = old[rid]
    if rid in fresh:
        ev = fresh[rid]
        if rid in ('E3g4-lab-observations', 'E3g3-basis-wording', 'E3g-r2-lab-twins', 'E3g3-page-smoke', 'E3g3-notation-collisions', 'E3g7-hours'):
            pass
        status = 'PASS'
    elif rid in carry:
        status = 'PASS'
        ev = CARRY + carry[rid] + prev['evidence']
    elif rid in mixed:
        status = 'PASS'
        ev = MIXED + mixed[rid] + fresh.get(rid, prev['evidence'])
    else:
        raise SystemExit('unassigned ' + rid)
    if rid in ('E3g4-lab-observations', 'E3g3-basis-wording', 'E3g-r2-lab-twins', 'E3g3-page-smoke', 'E3g3-notation-collisions', 'E3g7-hours'):
        ev = ev
    rows.append({'id': rid, 'check': prev['check'], 'location': prev['location'], 'status': status, 'evidence': ev})

# fix mixed rows where fresh text was prepended with a carry prefix already handled above
new_rows = [
 {'id': 'E3g8-delta', 'check': 'Delta 9373ef39..2d755599 for every slice subject',
  'location': 'course/modules/E/E3/L07.html lines 83-92; L08.html lines 427 and 699; cards.json E3-c131, E3-c144, E3-c182 (new)',
  'status': 'PASS',
  'evidence': 'git diff 9373ef39 2d755599 for the slice: L07.html (Example 1.4 derivative paragraph and the Observation 1.5 rewording), L08.html (Section 4 interpretation paragraph, quiz option L08q10), cards.json (per-id diff: E3-c131 back, E3-c144 front and back, new E3-c182 in L08). Every changed slice hunk was read and re-verified (rows E3g8-*). L05.html, L06.html, L04 Theorem 1.5 text, notation/, references/, tests/labs/E3/, tools/ are unchanged in the slice.'},
 {'id': 'E3g8-L07-ex14-derivative', 'check': 'Mathematics of the new derivative proof in Example 1.4',
  'location': 'course/modules/E/E3/L07.html lines 85-87 (Example 1.4)',
  'status': 'PASS',
  'evidence': 'Derived by hand and checked: q = sqrt(p(1-p)), g = 1 + 2q, omega = sqrt(p)/g; q\' = (1-2p)/(2q); g\' = (1-2p)/q; numerator times 2 sqrt(p) q equals qg - 2p(1-2p) = q + 2q^2 - 2p + 4p^2 = q + 2p^2 (since 2q^2 = 2p - 2p^2). Hence omega\' = (q + 2p^2)/(2 sqrt(p) q (1+2q)^2) > 0 on (0,1). Finite-difference check max abs error 2.2e-9 at 19 points (num_L07_r8.py). Continuity on [0,1] (omega(0)=0, omega(1)=1). MVT gives nondecreasing. The "0 <= omega <= sqrt(p) <= 1" claim: omega = sqrt(p)/(1+2q) with q >= 0.'},
 {'id': 'E3g8-obs15', 'check': 'Observation 1.5 wording and the printed grid facts',
  'location': 'course/modules/E/E3/L07.html lines 90-92; twin_L07.out line 11',
  'status': 'PASS',
  'evidence': 'Lab output: "sign changes of omega(p) - p = 1; last point with omega(p) > p = 0.278" (twin_L07.out line 11). Recomputed on the 1001-point grid with floats: 1 sign change, last grid point with omega > p is 0.278, omega(0.279) = 0.2784398 < 0.279, so the crossing is in (0.278, 0.279). The new sentence "Example 1.4 proves both by the closed form and its derivative" is correct (see E3g8-L07-ex14-derivative). Grid facts are labelled finite checks.'},
 {'id': 'E3g8-L07-numbers', 'check': 'Numbers in the new and changed L07 prose (Remark 1.6, Proposition 2.2, Lab 1, Misconception 3, Problems M1, E1, E2, E3)',
  'location': 'course/modules/E/E3/L07.html Example 1.4 values, Remark 1.6, Proposition 2.2, section 4, section 5 problems',
  'status': 'PASS',
  'evidence': 'Decimal (60 digits): omega(3/10)=0.2857908849..., omega(3/5)=0.3912507700..., omega(1/2)=0.3535533906..., omega(2/5)=0.319454916; sum A = 0.8910366858 (prints 0.89103669); 2 omega(3/10)=0.5715817698 (0.57158177); ratio 0.7304544982 (0.73045450); printed-digit quotient 0.7304544858 (0.73045449, as the page says); thresholds 2/3 and 0.5857864376 (0.58578644); Gamma(A)=42.8686327357, Gamma(B)=39.1250770027 at alpha=1 (print 42.8686, 39.1251), diff 3.7435557330 (3.7436 to 4 dp); alpha=1/2: 4.8787555762 and 3.9125077003; omega(0.01)=0.0834030105, omega(0.99)=0.8298494764; counterexample 49.8327748658 (49.8328) against 50.5; overweighting 7.3403, underweighting 8.0075, net -0.6672 (-0.67); omega(1/4) = 2 - sqrt(3) = 0.2679491924 = 1/(2+sqrt 3). E3 ETA=1 gap: max over the grid 0.31256 at p = 0.862 (page: 3.13e-1). Every number matches.'},
 {'id': 'E3g8-L08-interp-q10', 'check': 'Wording change "expectation of 1/w is affine in p" in the Section 4 interpretation paragraph and quiz option L08q10',
  'location': 'course/modules/E/E3/L08.html line 427 and line 699 (quiz option data-correct)',
  'status': 'PASS',
  'evidence': 'The former wording "inverse expectation is affine in p" was wrong (the inverse of an affine function is not affine); the new "expectation of 1/w is affine in p" is right: E_P[1/w] = p/w1 + (1-p)/wL, and the CE is 1/E_P[1/w] (Model 1, Remark 4.2). The explanation div (Remark 4.2 midpoint) is unchanged and correct. Lab 1 part A output (twin_L08.out lines 3 to 8) matches the claims.'},
 {'id': 'E3g8-c131-basis', 'check': 'E3-c131 (grade C) numeric answer and basis wording',
  'location': 'course/modules/E/E3/cards.json E3-c131; L07.html E2 solution',
  'status': 'PASS',
  'evidence': 'Answer 3.7436 re-derived: Gamma(A)-Gamma(B) at alpha=1 = 150 omega(3/10) - 100 omega(3/5) = 3.7435557330 (Decimal 60 digits), which rounds to 3.7436 at 4 dp; the eight-decimal values 42.86863274 - 39.12507700 = 3.74355574 also give 3.7436; the printed (separately rounded) 42.8686 - 39.1251 = 3.7435. Note for the grade: the lab prints only four decimals, so the 40-digit value is not printed by Lab 1 part C; the float evaluation of the same quantities (3.74355573) is what the lab computes, so the basis "Lab 1, part C (floating point)" is accurate in substance. Not a defect; recorded as a note.'},
 {'id': 'E3g8-c144-c182', 'check': 'E3-c144 (red CE) and new E3-c182 (black CE) against Example 2.5',
  'location': 'course/modules/E/E3/cards.json E3-c144, E3-c182; L08.html Example 2.5',
  'status': 'PASS',
  'evidence': '1/((1/3)/110000 + (2/3)/100000) = 103125 exactly (Fraction); 1/((2/3)/110000 + (1/3)/100000) = 106451.6129032 (106451.6129). Both values appear in Example 2.5. The new card is a sibling of c144 for the other colour, not a duplicate (near-duplicate scan, ledgers/E3/scripts/E3-g-r8/cardnum_r8.py). Grade T is correct: closed form with u = -1/w stated.'},
 {'id': 'E3g8-L08-numbers', 'check': 'Numbers in L08 Section 4 table, Remark 4.2, Problems M1 to M3, E1 to E3, R2, quiz',
  'location': 'course/modules/E/E3/L08.html Section 4 table, Remark 4.2, Problem set, quiz',
  'status': 'PASS',
  'evidence': 'Exact Fractions: EU CE = 4180000/41 = 101951.2195 (whole cent 101951); prospect V_p = 5 - sqrt(50) = -2.0710678, CE of change -1.0723305 CU, wealth 99892.7670 (99893); maxmin at p=1/3 = 99523.8095 (99524); alpha-MEU tau=1/2 = 101951.2195; risk premium 102500 - 101951.2195 = 548.7805 = 22500/41 = 5.4878 CU; p=1/4 CE 98352.9412 (98352.94), p=3/4 CE 105822.7848 (105822.78); full-set maxmin 95000 at p=0 (Section 5) and 100000 for Example 2.5 colours; lab output part A line 5 gap 4.44e-16 (twin_L08.out line 5); part B gaps -2.91e-11 and 0.00e+00. All match the page.'},
 {'id': 'E3g8-card-numbers', 'check': 'Every number on a slice card appears in its lesson; no duplicate cards',
  'location': 'course/modules/E/E3/cards.json (85 cards in L05 to L08)',
  'status': 'PASS',
  'evidence': 'ledgers/E3/scripts/E3-g-r8/cardnum_r8.py: 85 slice cards, 0 numbers absent from the own lesson text; no duplicate ids, fronts or backs across the 174-card file. cardref8.py: checked 85, bad 0. Card cross-references (Definition, Proposition, Theorem, Remark, Example, Model, Problem, Lab 1 parts) resolve.'},
 {'id': 'E3g8-notation-local', 'check': 'Local symbols q and g in Example 1.4 and g(p) in Model 4 against notation/notation.json',
  'location': 'course/modules/E/E3/L07.html Example 1.4 (paragraph 3); L08.html Model 4 and Remark 4.2',
  'status': 'PASS',
  'evidence': 'notation/notation.json (byte-identical to round 7) registers only T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q and the macros \\E, \\Prob, \\Var, etc. q and g are not registered and are defined where used (q = sqrt(p(1-p)), g = 1 + 2q in Example 1.4; g(p) = E_p[1/w] in Model 4). No registered symbol is used with another meaning in L07 or L08 (grep of the page sources).'},
 {'id': 'E3g8-gates', 'check': 'Gate commands re-run on pin 2d755599',
  'location': 'course/modules/E/E3/L07.html, L08.html, cards.json; tools/*',
  'status': 'PASS',
  'evidence': 'check_pages --unit E3: PASS (exit 0); --page L07 and --page L08: PASS; check_dag --unit E3: PASS; check_projects --unit E3: PASS; run_labs --unit E3 --page L07 and L08: PASS; page_smoke --unit E3 --pages L07 L08: PASS; build_site --check: "site data current: 6 outputs" exit 0; render_curriculum.py: no change to CURRICULUM.md or curriculum/curriculum.json; verify_refs --offline: 560 entries, 0 problems; pytest -k E3 (3 files): 15 passed; ruff check tests/labs/E3 tools/check_pages.py: passed. Logs in ledgers/E3/scripts/E3-g-r8/.'},
 {'id': 'E3g8-lab-twins-run', 'check': 'Lab twins under python -I -W error; page code equals twin; expected block equals output (L07, L08)',
  'location': 'tests/labs/E3/lab-E3-L07-1.py, lab-E3-L08-1.py; course/modules/E/E3/L07.html, L08.html',
  'status': 'PASS',
  'evidence': 'python3 -I -W error tests/labs/E3/lab-E3-L07-1.py: exit 0, empty stderr (twin_L07.err); L08 likewise (twin_L08.err). Page <code data-run> equals twin (stripped; byte-identical except one trailing newline). <pre class="expected"> equals the twin output (stripped) for both labs (18 and 24 lines).'},
 {'id': 'E3g8-scope-process', 'check': 'Scope words and process words in the changed hunks',
  'location': 'course/modules/E/E3/L07.html Example 1.4 and Observation 1.5; L08.html line 427',
  'status': 'PASS',
  'evidence': 'Scope words in the new text (for every, any, only, all) are read in context: "for every p" (a derivative claim on (0,1)), "any" not used in new claims; no process words (we, our, verifier, builder, round, TODO) in L07 or L08 prose. Full greps: ledgers/E3/scripts/E3-g-r8/L07.txt, L08.txt.'},
]
rows.extend(new_rows)

notes = [
 'Slice g: the 85 E3 cards of L05 (20), L06 (19), L07 (18) and L08 (28), read against the four lesson texts in full (L05..L08.txt extracted from the pin with strip7.py, ledgers/E3/scripts/E3-g-r8/). L05 and L06 pages, their cards and their labs are byte-identical to the round-7 pin, so their round-7 PASS rows are carried with the prefix.',
 'Round-7 FAIL E3g7-ex14-monotone is closed on this pin: Example 1.4 proves monotonicity by the derivative, and Observation 1.5 now calls the grid facts finite checks. Verified by hand and by finite difference (E3g8-L07-ex14-derivative).',
 'The delta also changed L08 wording in two places (inverse expectation -> expectation of 1/w, which is the correct statement) and card E3-c144 was split into E3-c144 (red) and the new E3-c182 (black), both T and both verified against Example 2.5.',
 'Outside this slice, not checked here: cards E3-c047, c050, c067, c178, c180, c181 (L03/L04), L02, L03, L04 hunks (L04 Theorem 1.5 text itself unchanged), project.html and grader/test_project.py (E3 project slice). The E3 project grader was not mutated or run (not a project slice).',
]

frag = {
 'unit': 'E3',
 'slice': 'g',
 'round': 8,
 'verifier': 'Haiku independent verifier, E3-g round 8 (did not build E3)',
 'pin': PIN,
 'base': PREV + ' (round-7 pin; delta 9373ef39..2d755599 read for the slice)',
 'checkout': '/Users/billyribeiro/.fanout/wt/verifyD8-E3-g (detached at 2d755599)',
 'scratch': 'ledgers/E3/scripts/E3-g-r8/ (L05..L08.txt, cards_L07_L08.txt, num_L07_r8.py, cardnum_r8.py, cardref8.py, write_fragment_g8.py, gate outputs and twin outputs)',
 'verified_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
 'verdict': 'PASS',
 'rows': rows,
 'mutants': [],
 'registry_flags': [],
 'freshness_flags': ['Round-7 pin 9373ef39 is an ancestor of the pin; delta touched other units (E4, FC, CS2, SC1, BK4, LX1, PC3) which are out of scope for this slice.'],
 'notes': notes,
 'summary': {
   'rows': len(rows),
   'pass': sum(1 for r in rows if r['status'] == 'PASS'),
   'fail': sum(1 for r in rows if r['status'] != 'PASS'),
   'carried_from_round_7': sum(1 for r in rows if r['evidence'].startswith('Carried from round 7')),
   'mutants': 0,
   'mutants_killed': 0,
 },
}
json.dump(frag, open('ledgers/E3/E3-g.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('rows', len(rows), 'pass', frag['summary']['pass'], 'carried', frag['summary']['carried_from_round_7'])
