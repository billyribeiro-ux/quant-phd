"""Writes ledgers/SC1/SC1-e.json (round 1, delta verification of slice e from base e919577b to 95f3f8cb)."""
import json

S = "ledgers/SC1/scripts/SC1-e-r1"
C13 = "Carried from round 13 (JSON objects identical to e919577b; "
rows = []

def row(rid, check, location, evidence, status="PASS"):
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence})

row("SC1e-structure-ids", "2.7-cards", "course/modules/SC/SC1/cards.json",
    "Re-run this round: 227 cards, 227 distinct ids matching SC1-cNNN (c240 absent, a gap allowed by ruling 2); "
    "lesson counts L01 25, L02 33, L03 24, L04 27, L05 36, L06 29, L07 28, L08 25 (sum 227); 160 cards carry grade, basis, cite; "
    "67 ungraded cards carry no grade or basis key (check_pages reads grade as optional); grade counts T 128, C 32, none 67. "
    "Delta from e919577b (ledgers/SC1/scripts/SC1-e-r1/out/card_delta_r1.txt, from card_delta_r1.py): removed c217; added c232-c239, c241-c243; "
    "35 cards changed; 181 unchanged. check_pages --unit SC1: PASS (out/check_pages.txt).")
row("SC1e-full-read-cards", "2.7-cards", "course/modules/SC/SC1/cards.json (all 227 cards)",
    "All 227 cards were examined this round. The 46 changed or added cards were read in full (out/changed_cards_new.txt, 184 lines) and each is checked "
    "against the current lesson text in the rows below. The 181 unchanged cards were read as front and back dumps (out/keyword_hits.txt lists the 115 that touch a changed "
    "claim, with their lesson text; the other 84 were read in truncated fields). Scope note: the unchanged cards were read in truncated form, not as "
    "full-length dumps; their JSON objects are identical to e919577b.")
row("SC1e-full-read-lessons", "2.9-prose", "course/modules/SC/SC1/L01.html to L08.html",
    "Delta scope (ruling 30). L07.html and L08.html are byte-identical to e919577b (git diff --quiet). L01 to L06 changed: every changed line of the 388-line diff "
    "(out/delta_e919577_95f3f8cb_lessons.diff) was read, and each changed claim was checked against the rendered text (out/L01.txt to L08.txt, rendered from the current pages by html_to_text.py). "
    "Unchanged lines were not re-read line by line this round (their text is identical to e919577b, read in round 13). No prose defect in the changed text. "
    "Observations, not FAIL: see notes.")
row("SC1e-near-duplicate-scan", "2.7-cards", "course/modules/SC/SC1/cards.json (all pairs)",
    "Re-run: scan_cards_r1.py (out/cards_scan_r1.txt): no identical front and no identical back. difflib ratio on front plus back >= 0.6: "
    "max 0.792 (c064/c202), then c202/c222 0.788, c045/c237 0.766 (E[X^4]=3Delta^2 and Var(X^2)=2Delta^2, two claims of Lemma 2.2), c170/c218 0.718, c072/c226 0.713, "
    "c116/c117 0.692, c210/c233 0.689 (the two sentences of A1(e)), c064/c222 0.682, c030/c221 0.677, c174/c242 0.674, c161/c167 0.672, c137/c139 0.655, c044/c236 0.612 (E[Z^4] and E[Z^2]). "
    "Each pair asks a different claim (read in the dumps).")
row("SC1e-learner-text-scan", "2.9-prose", "cards front and back; L01 to L08 text",
    "Re-run: process-word regex (builder, verifier, round, fixer, ledger, reviewer, sub-agent) and the BUILDER_RULES banned-phrase list over the 227 cards and out/L01.txt to L08.txt: no hit (out/cards_scan_r1.txt contains no such line).")
row("SC1e-card-numbers-in-lesson", "2.7-cards", "cards with a numeric token and a cross-reference label",
    "Re-run scan_refs_r13.py on the current cards (out/scan_refs_r1.txt): 437 numeric tokens checked, 0 absent from the card's own lesson text (substring test, weak; values recomputed in SC1e-numbers-recomputed). "
    "291 reference labels, 20 absent only because the lesson headers use another format; each was confirmed in the header text: c052 'R1 · The equal partition in closed form' (L03), c105 'M3 · Independence of the next increment' (L05), "
    "c157 'R2 · No atoms at positive levels' (L07), c159 'E3 · The printed standard error' (L07), c227 'R2 · A3 at a deterministic time' (L05), c017 '4Where the canon breaks' (L01), and the rest by the same pattern.")
row("SC1e-numbers-recomputed", "2.2-numbers", "changed cards c011-c013, c030-c032, c044-c045, c052, c092, c110, c114, c159, c171, c174, c187, c201, c221, c224, c236-c242 and the lesson prose numbers",
    "Recomputed this round with standard-library scripts and the lab outputs: H^4(4N^2-1)/(3N^3) at H=2, N=128 = 1048560/6291456 = 0.166664 (L03 misconception, twin_L03.stdout); "
    "Lab 1 standard errors unrounded (out/l03_gap_r1.txt): largest gap +13.208 percent from printed values, +13.218 percent unrounded, both at H=2, N=1; "
    "495 = C(12,8) and the twin's 495 for M_12>=3 with S_12=2 (twin_L06.stdout Part C); 1588/4096 = 0.387695 and 794/4096 = 0.193848 (twin_L08.stdout Part A); "
    "erfc(1/sqrt2) = 0.3173105079 and erfc(0.5) = 0.4795001222 (twin_L08.stdout Part D, P(tau_1<=H)); density 0.241971 at H=1 and 0.109848 at H=2 (twin_L08.stdout Part D); "
    "1.0000000000 for t=0.5, 1, 2 (twin_L05.stdout); M_m = lambda_m 2^(-(m+1)/2) = sqrt(2 log 2) sqrt(m) 2^(-m/2) (algebra); sum m r^m = r/(1-r)^2 at r = 2^(-1/2); "
    "P(E_m^c) <= 2^(m-1) * 2 * e^(-lambda_m^2/2) = 2^(-m); SE of a proportion with divisor n-1: sqrt(33759/63840000) = 0.0230 (x=121, n=400); "
    "Var(Q) for Q = N X_N^2 with X_N ~ N(0, t/N): 2t^2 for every N; E[X^4]=3Delta^2 and Var(X^2)=2Delta^2 (L03 Lemma 2.2 proof).")
row("SC1e-L03-gap", "2.5-labs", "course/modules/SC/SC1/L03.html Lab 1 expected block; cards c051, c052, c187, c225",
    "Re-run with the unrounded standard errors (out/l03_gap_r1.txt, from tests/labs/SC1/lab-SC1-L03-1.py with the lab's own seed and draw order): "
    "max |z| = 2.392 at H=1, N=2 (printed 2.39), the next largest |z| is 1.84 at H=1, N=128; all 16 |z| <= 2.39, so 'within plus or minus 3 SE' holds. "
    "The printed SE gap is within 14 percent for all 16 rows (largest +13.208 percent at H=2, N=1; the unrounded gap is +13.218 percent, so 'about 13.2 percent' and 'the unrounded SE gives 13.22 percent' are both right). "
    "0.1601/(2 sqrt2/20) - 1 = 13.208 percent, matching the card c187 wording 'largest relative gap +13.2 percent'.")
row("SC1e-labs-run", "2.5-labs", "tests/labs/SC1/lab-SC1-L01-1.py to lab-SC1-L08-1.py",
    "Re-run this round: each twin alone under .venv python -I -W error from an empty scratch directory (out/twin_L0*.stdout and .stderr; run_twins_r1.sh): exit 0 for L01 to L08, stderr 0 bytes, "
    "stdout byte-identical to the round-13 stdout for all eight. run_labs --unit SC1: PASS (11/11) (out/run_labs.txt). ruff check and ruff format --check tests/labs/SC1: clean (out/ruff_labs_sc1.txt, out/ruff_format_labs_sc1.txt). "
    "mypy --no-incremental tests/labs/SC1: no issues (out/mypy_SC1_labs.txt). pytest tests/test_run_labs.py tests/test_labs.py -k SC1: exit 0 (out/pytest_SC1.txt). The twins are byte-identical to e919577b (not in the diff).")
row("SC1e-labs-page-equals-twin", "2.5-labs", "course/modules/SC/SC1/L01.html to L08.html (data-run and expected blocks)",
    "run_labs --unit SC1 re-run: PASS 11/11 (out/run_labs.txt), which compares each page's code block with its twin and each expected block with the output. "
    "No lab-block hunk appears in the L01 to L06 delta (out/delta_e919577_95f3f8cb_lessons.diff).")
row("SC1e-page-smoke", "2.9-prose", "course/modules/SC/SC1/L01.html to L08.html",
    "Re-run: page_smoke --unit SC1 --pages L01 L02 L03 L04 L05 L06 L07 L08: PASS for each of the eight pages (out/page_smoke_L01_L08.txt, exit 0).")
row("SC1e-check-pages-dag", "2.9-prose", "course/modules/SC/SC1/",
    "Re-run: check_pages --unit SC1 PASS (out/check_pages.txt); check_dag --unit SC1 PASS (out/check_dag.txt); check_projects --unit SC1 PASS (out/check_projects_SC1.txt); "
    "build_site --check: site data current (out/build_site_check.txt); verify_refs --offline: 560 entries, 0 problems (out/verify_refs_offline.txt). "
    "The L04 Uses line now links Lesson 3 Lemma 2.2 and no longer links quadratic-variation; check_dag PASS covers the prerequisite closure.")
row("SC1e-delta-read", "2.9-prose", "cards.json and the lesson hunks changed since e919577b (out/delta_e919577_95f3f8cb_lessons.diff, 388 lines; out/delta_e919577_95f3f8cb_cards.diff)",
    "Every hunk of the course/modules/SC/SC1 L01 to L06 and cards.json delta was read. Changed claims were rechecked against proofs, lab outputs and the other cards (rows below). "
    "Out of the slice: index.html, project.html, grader/ (base scope) were not read in this round.")
row("SC1e-c048-round7", "2.7-cards", "course/modules/SC/SC1/cards.json card SC1-c048; L03.html Theorem 2.3",
    "c048 is JSON-identical to e919577b. The Theorem 2.3 statement (L03 lines 80 to 84) is unchanged; the paragraph after the theorem (line 96) changed and was rechecked: 'under Assumptions 3.1 and 3.2 the random sums converge to it in mean square'. The card's 'to t in mean square' and 'at most 2t|P_n|' agree.")
row("SC1e-L01-statements", "2.7-cards", "course/modules/SC/SC1/L01.html; cards c001 to c017, c186, c206 to c210, c232, c233",
    "Changed L01 hunks read against L01.txt: why-it-matters (Assumption A1(a) stated in §2 at L01 line 56; Assumption 2.1(a)-(c) of Lesson 2), the Remark 1.3 counterexample (B_1 = +1 or -1 with probability 1/2: mean 0, variance 1, P(B_1=1)=1/2 != 0, so not normal), misconception (Definition 1.1 fixes the value at time 0 and the fdd), table rows, quiz explanation. "
    "Cards c017 (changed), c207 (changed), c210 (changed), c232 and c233 (new) match L01 lines 58 to 66 (A1(a)-(e)). c008 and c014 (unchanged) remain consistent with the Remark 1.3 text.")
row("SC1e-L02-statements", "2.7-cards", "course/modules/SC/SC1/L02.html; cards c018 to c041, c184, c185, c211 to c213, c220 to c224, c243",
    "Changed L02 hunks read: Lemma 2.1 (lambda >= 0, hypothesis 2.1(a)); Proposition 2.4 (H3 Assumption 2.1(a)-(c)); step 1 (M_m = lambda_m 2^(-(m+1)/2) = sqrt(2 log 2) sqrt(m) 2^(-m/2)); step 2 (r = 2^(-1/2)); step 3 bound by the tail sum; "
    "Assumption A2 sketch (dyadic times t^(k) in [t,1]); Theorem 2.5 (H2); Remark 2.6 (H2); canon bullet; R2 solution (P(E_m^c) <= 2^(-m) from 2^(m-1) * 2 * 2^(-2m); the union bound and continuity from below use 2.1(c)). "
    "Cards c029, c030, c031, c032, c034, c035, c220, c221, c224 (changed) and c033 (unchanged) match. Observation (not a FAIL): the A2 sketch's characteristic function exp(-u^2(t^(k)-s^(k))/2) is correct only for t^(k) >= s^(k); see notes.")
row("SC1e-L03-statements", "2.7-cards", "course/modules/SC/SC1/L03.html; cards c042 to c060, c187, c188, c225, c234, c236, c237",
    "Changed L03 hunks read: why-it-matters; the Theorem 2.3 paragraphs; canon bullet 'Independence is not optional' (Var(Q)=N^2 * 2(t/N)^2=2t^2); misconceptions 1 and 3; Lemma 2.2 with mean 0 and variance Delta>0 (proof X = sqrt(Delta) Z, uses Lemma 2.1 E[Z^2]=1, E[Z^4]=3); "
    "key-results rows; quiz explanation (not a card). Cards c044, c045, c052, c054, c060, c236, c237 (changed or new) and c056 (unchanged) match. c234 matches Assumption 3.2(b).")
row("SC1e-L04-statements", "2.7-cards", "course/modules/SC/SC1/L04.html; cards c061 to c082, c202 to c204, c222, c226",
    "Changed L04 hunks: the Uses line (quadratic-variation link removed; 'moments of one increment in Lemma 2.2 of Lesson 3' added; L03 Lemma 2.2 is the moments lemma) and the canon-break bullet 'Adding the deterministic drift t breaks the martingale property' (same mathematics). "
    "Card c073 (unchanged) E[X_t|F_s]=B_s+t matches. No other L04 hunk.")
row("SC1e-L05-statements", "2.7-cards", "course/modules/SC/SC1/L05.html; cards c083 to c105, c189, c092, c093, c095 to c099, c193 to c200, c214, c227, c228, c238",
    "Changed L05 hunks: M3 statement (now 'assuming A1(a)' ... 'assuming A1(b)') and solution: (B_1, B_2-B_1) jointly normal because each coordinate is a linear combination of the independent normals B_1 and B_2-B_1 (D2, D3), then A1(c) gives independence from zero covariance. Card c105 (changed) matches. "
    "Cards c099 (changed: A3 requires rho <= c), c197 and c200 (changed wording), c214 (changed: A4(i)) and c092 and c238 (lab digits) match L05 lines 44 to 60, 262 to 270 and the twin output (twin_L05.stdout).")
row("SC1e-L06-statements", "2.7-cards", "course/modules/SC/SC1/L06.html; cards c106 to c133, c235, c239",
    "Changed L06 hunks read and the new Proposition 2.7 proof checked step by step: "
    "Step 1, the pathwise identity W_s = 2B_{s ∧ rho} - B_s on [0,t] (case tau_a >= t and case tau_a < t) holds; "
    "Step 2, W_{s_j} = V_j - U_j with U_j = X_{(s_j - rho)^+}; "
    "Step 3, theta_j = s_j ∧ rho is a stopping time, F_{theta_j} is contained in F_rho (theta_j <= rho), and V_j is F_{theta_j}-measurable by A4(h); "
    "Step 4, freezing (A4(b)) with Z = (V, rho) and Y = X, which is independent of F_rho by A3 applied to the bounded time rho <= t; -X has the law of X (continuous paths, same fdd), so the two conditional expectations agree; "
    "Step 5, fdd equality on [0,t] for every t and continuity of W on [0,infinity). A3 is applied only to rho = tau_a ∧ t, as L05 A3 requires (rho <= c); A4(b), (c), (g), (h) are each used. "
    "Cards c110 (changed), c114 (changed, 495), c119 (changed), c122 (changed, grade None to T), c235 (new), c239 (new, 495 for S_12=4) match. c217 removed: its content (Prop 2.3 uses only rho <= t) is still covered by c133. "
    "Observation: Proposition 2.7 cites Proposition 2.3 for rho being a stopping time; that fact is proved in the proof of Proposition 2.3 (see notes).")
row("SC1e-L07-statements", "2.7-cards", "course/modules/SC/SC1/L07.html; cards c134 to c159, c191, c215, c229 to c231",
    "L07.html is byte-identical to e919577b and carried. Changed cards c157 (P(M_H=a)=0 chain: {M_H>=b} increases to {M_H>a} as b downarrow a; continuity from below and Theorem 1.3 give P(M_H>a)=P(M_H>=a)) and c159 (x successes in n indicators; matches the L07 E3 text 'for x successes in n indicators', sqrt(x(n-x)/(n^2(n-1))), 0.0230 at x=121, n=400) match L07 lines 448 to 472. "
    "The other L07 cards are JSON-identical to e919577b (carried).")
row("SC1e-L08-statements", "2.7-cards", "course/modules/SC/SC1/L08.html; cards c161 to c183, c201, c205, c218, c241, c242",
    "L08.html is byte-identical to e919577b and carried. Changed cards c171, c174 and c201 and new cards c241, c242 are checked against twin_L08.stdout Parts A and D and the L08 Proposition 1.2 event equality; "
    "c201: P(tau_a <= H) = P(M_H >= a) = 2 P(B_H >= a) by Proposition 1.2 and Theorem 2.5 of Lesson 6. Other L08 cards are JSON-identical (carried).")
row("SC1e-assumption-labels", "2.7-cards", "cards naming A1 to A5, A4(a)-(i), Assumption 2.1(a)-(c), 3.1, 3.2(a)-(b), 4.1, 4.2(a)-(e)",
    "A1(a)-(e): cards c206 to c210 and c232, c233 match L01.txt lines 58 to 66 (A1(b) is the linear-combination and vector sentence, A1(e) the disjoint-functions and blocks sentences). "
    "A2: c033 matches L02 lines 271 to 273. A3: c093, c098, c099 match L05 lines 262 to 270. A4(a)-(i): c193 to c200 and c214 match L05 lines 44 to 60. A4 of L04: c202 to c204, c222 match L04 line 54. A5: c215 matches L07 line 78. "
    "Assumption 2.1(a)-(c): c211 to c213 match L02 lines 78 to 82, and the changed cards that name 2.1(a)-(c) match L02 lines 84, 137, 281, 293. Assumption 3.1, 3.2(a), 3.2(b): c188, c060, c234 match L03 lines 48 to 54.")
row("SC1e-cross-references", "2.7-cards", "cards naming Problems, Sections, Lab parts and numbered results",
    "Re-run scan_refs_r13.py (out/scan_refs_r1.txt): 291 labels checked; the 20 absent labels are header-format only and were confirmed in the headers (see SC1e-card-numbers-in-lesson). Cards c017, c052, c105, c157, c159 (changed) and c227 (unchanged) point to existing headers.")
row("SC1e-hypotheses-carried", "2.4-mathematics", "cards for Lemma, Proposition, Theorem, Corollary and Remark statements",
    "Hypotheses on each changed card match the lesson's hypothesis lines: Lemma 2.1 (lambda >= 0, 2.1(a)); Proposition 2.4 (H1, H2 and H3 = 2.1(a)-(c)); Theorem 2.5 and Remark 2.6 (A2 and 2.1(a)-(c)); "
    "Lemma 2.2 of L03 (mean 0, Delta > 0; c045, c237); Proposition 2.7 (B standard with continuous paths, a > 0; A3 for tau_a ∧ t; A4(b), (c), (g), (h)); Corollary 1.4 of L06 (integers N >= 1, a >= 1 and Proposition 1.3's hypotheses; c110). No card omits a stated hypothesis.")
row("SC1e-grades-audit", "2.3-grades", "cards grade field (T 128, C 32, none 67)",
    "Grade changes audited: c122 None to T (Remark 2.4 is a statement about Proposition 2.3 that is proved there; the whole-path claim is Proposition 2.7); c235 T (Proposition 2.7, proved); c236 and c237 T (Lemma 2.1 and Lemma 2.2 proofs); "
    "c238, c239, c241, c242 C (Lab 1 outputs of L05, L06 and L08: 1.0000000000, 495, 1588/4096 and the densities). The key-results rows change in the same way (L06 Proposition 2.7 row T; L03 lab row C). No C row is claimed as a proof.")
row("SC1e-cites-and-registry", "2.8-registry", "course/modules/SC/SC1/cards.json cite fields; lessons' References sections; references/references.json",
    "No card has a non-empty cite list (checked: out/cards_95f3f8cb.json). Lesson References sections (L01, L02 changed text) still state that the lesson cites no registry source. "
    "references/references.json changed only in generated_at and in DV1's used_by (FC2 added); verify_refs --offline: 560 entries, 0 problems (out/verify_refs_offline.txt).")
row("SC1e-notation", "2.9-notation", "cards and L01 to L08 text; notation/notation.json",
    "notation/notation.json is byte-identical to e919577b (not in the diff) and registers 8 symbols (T, Phi, R^*, ...). SC1 uses H for the horizon: L03 line 100 and L07 line 44 say the program reserves T for the number of return observations. "
    "Phi is the standard normal CDF in L05, L07 and L08, which matches the registry. The new Proposition 2.7 symbols (W, V, U, X, Y, Z, theta_j, Psi, G_±) are not registered. "
    "Observation: G is the sigma-field in the A4(b) application and G_± are the functions in Proposition 2.7 Step 4 (see notes).")
row("SC1e-dag", "2.9-prose", "cards; L01 to L08 text; check_dag",
    "check_dag --unit SC1: PASS (out/check_dag.txt). The changed concept links are on the lesson's Uses line or within the same unit: L04 links L03 Lemma 2.2 (plain link); L06 Proposition 2.7 cites Lesson 5 A3 and A4 (same unit). No new concept used outside the prerequisite closure.")
row("SC1e-scope-words", "2.9-prose", "cards and the changed lesson text",
    "Scope words in the changed text (only, all, every, any, same, exactly, always): each is supported. Examples: L01 footer 'each result is proved on the page, except the one taken from Lesson 2 (Remark 2.6)'; L06 'Propositions 2.3 and 2.7 use rho = tau_a ∧ t, which is bounded'; "
    "c110 'The term P(S_N=a) has no continuous counterpart' (Theorem 2.5 has no such term); c122 'The whole path needs Proposition 2.7'; c060 'Assumed, not proved'.")
row("SC1e-r8-twin-docstring-only", "2.5-labs", "tests/labs/SC1/ lesson twins (L01 to L08)",
    C13 + "tests/labs/SC1 is not in the e919577b..HEAD diff). Twins were re-run this round: SC1e-labs-run PASS.")
row("SC1e-c052-term", "2.7-cards", "course/modules/SC/SC1/cards.json card SC1-c052 front and back",
    "c052 changed to the horizon H (front 'equal steps of [0,H] with 400 simulated paths'; back 'H sqrt(2/N)/20, with H the horizon'). The L03 lab text (line 114) uses H; Problem R1 (line 347) and the L03 notation paragraph (line 100) agree. Value recomputed in SC1e-numbers-recomputed.")
row("SC1e-c150-assumption-reference", "2.7-cards", "course/modules/SC/SC1/cards.json card SC1-c150 back",
    C13 + "c150 and L07 Lab 1 Part C unchanged). The card's '0.7586, with standard error 0.0317' matches L07 line 502 and the L07 lab output.")
row("SC1e-c140-hypotheses", "2.7-cards", "course/modules/SC/SC1/cards.json card SC1-c140 front",
    C13 + "c140 and L07 Corollary 1.5(b) unchanged). The hypotheses on the card (A5 included) match L07 lines 80 to 90.")
row("SC1e-c219-new", "2.7-cards", "cards.json (card SC1-c219, removed at 5db69a9)",
    "No card with id SC1-c219 exists at e919577b or 95f3f8cb (ids checked in card_delta_r1.py output); no duplicate content introduced by the delta.")
row("SC1e-c220-c221-new", "2.7-cards", "cards SC1-c220, SC1-c221 (L02)",
    "Both changed (assumption labels 2.1(a)-(c) and 'step 2' with r = 2^(-1/2)). c220: P(Omega*) = 1 from P(E_m^c) <= 2^(-m), P(A_{m0}^c) <= 2^(1-m0) and continuity from below. c221: M_m <= sqrt(2 log 2) m r^m and sum m r^m = r/(1-r)^2 < infinity. Both match L02 lines 143 to 154.")
row("SC1e-c029-c030-changed", "2.7-cards", "cards SC1-c029, SC1-c030",
    "c029 (changed labels): P(E_m^c) <= 2^(-m), by Lemma 2.1 and the union bound over 2^(m-1) coefficients (L02 line 144). c030 (changed to 'step 1' with H2): M_m = lambda_m 2^(-(m+1)/2) = sqrt(2 log 2) sqrt(m) 2^(-m/2), the step-1 bound of L02 line 148. Both verified by computation.")
row("SC1e-c011-c013-changed", "2.7-cards", "cards SC1-c011, SC1-c012, SC1-c013 (L01 section 4)",
    "Changed card hypotheses name Assumption 2.1(a)-(c) of Lesson 2 and match L01 line 199. c011 back uses P(U in G) = 0 for a finite set of times G (L01 line 321: each finite set of times avoids U with probability one). c012: B~_U = B_U + 1 and B~_t = B_t for t != U, so B~ is discontinuous at U on every outcome. c013: the continuity event holds for B on every outcome and for B~ on no outcome.")
row("SC1e-L08-changed-cards", "2.7-cards", "cards SC1-c162, c165, c171, c201 (L08)",
    C13 + "c162 and c165 unchanged; c171 and c201 changed and re-verified in SC1e-L08-statements). c171 counts 512, 0, 384, 0, 288, 0, 224, 0, 180, 0 sum to 1588 (twin_L08.stdout Part A).")
row("SC1e-lab-outputs-cards", "2.5-labs", "cards backed by a lab (c010, c037, c038, c051, c072, c091, c092, c111 to c114, c127, c149, c150, c170 to c174, c187, c216, c218, c225, c226, c229 to c231 and the lab counts)",
    "All eight twin outputs are byte-identical to the round-13 outputs (out/twin_L0*.stdout). The changed lab-backed cards c092 (1.0000000000 for t = 0.5, 1, 2), c114 (495), c171, c174, c238 (Simpson, ten decimals), c239 (495 for S_12 = 4), c241 and c242 match the outputs. The unchanged lab-backed cards are JSON-identical to e919577b (carried) and their outputs are unchanged.")
row("SC1e-c222-c223-c224-new", "2.7-cards", "cards SC1-c222, SC1-c223, SC1-c224 (L04 4.2(e); L02 Lemma 2.3, Proposition 2.4(b))",
    "c222 and c223 are JSON-identical (carried; their L04 and L02 text is unchanged in these claims). c224 changed and re-verified: sup_t |Sigma(t) - Sigma_M(t)| <= sum_{m > M} M_m for M >= m0 (L02 step 3, line 153).")
row("SC1e-c225-c226-new", "2.7-cards", "cards SC1-c225 (L03 Lab 1), SC1-c226 (L04 Lab 1)",
    C13 + "c225 and c226 unchanged; their lab outputs unchanged). c225's claim (all 16 |z| within 3) re-verified this round: max |z| = 2.392 (out/l03_gap_r1.txt).")
row("SC1e-c227-c228-new", "2.7-cards", "cards SC1-c227, SC1-c228 (L05 Problems R2, R3)",
    C13 + "c227 and c228 unchanged; the L05 R2 and R3 text is unchanged: the L05 delta contains only the M3 hunk).")
row("SC1e-c229-c230-new", "2.7-cards", "cards SC1-c229, SC1-c230 (L07 Lab 1 parts C and B)",
    C13 + "c229 and c230 unchanged; L07 lab outputs unchanged).")
row("SC1e-round12-changed-cards", "2.7-cards", "cards SC1-c026, c027, c028, c032, c051, c072, c095, c096, c149, c150, c203, c207",
    "Of these twelve cards, c032 and c207 changed in this delta and were re-verified (c032: Proposition 2.4(b) on Omega*, steps 3 and 4; c207: A1(b) first sentence, with the second sentence moved to c232). "
    "The other ten are JSON-identical to e919577b (carried).")
row("SC1e-round12-lesson-hunks", "2.9-prose", "L01 to L05 hunks since 11d7077 (round-12 delta), as they stand at e919577b and at 95f3f8cb",
    "The round-12 hunks are part of e919577b, and the hunks since e919577b are read in SC1e-delta-read. No round-12 hunk was reverted in this delta.")
row("SC1e-c231-new", "2.7-cards", "card SC1-c231 (L07, grade C) and L07 lab Part A",
    C13 + "c231 unchanged). L07 Part A and its twin output unchanged (twin_L07.stdout).")
row("SC1e-c126-c201-changed", "2.7-cards", "cards SC1-c126 (L06) and SC1-c201 (L08)",
    "c126 JSON-identical (carried; Theorem 2.5 gives P(M_t >= a) = 2 P(B_t >= a)). c201 changed and re-verified: P(tau_a <= H) = P(M_H >= a) = 2 P(B_H >= a), by Proposition 1.2 (event equality) and Theorem 2.5 of Lesson 6.")
row("SC1e-gates-tools", "2.9-gates", "tests/labs/SC1 twins; tools gate outputs for SC1",
    "Slice gates re-run this round (ledgers/SC1/scripts/SC1-e-r1/run_gates_r1.sh; outputs in out/): check_pages PASS; check_dag PASS; check_projects PASS; run_labs PASS (11/11); page_smoke PASS for L01 to L08; build_site --check current; verify_refs --offline 560 entries, 0 problems; ruff check and ruff format --check on tests/labs/SC1 clean. "
    "Plus twins alone under python -I -W error (exit 0, stderr empty), mypy --no-incremental tests/labs/SC1 (no issues), pytest -k SC1 on test_run_labs and test_labs (exit 0).")
row("SC1e-r1-card-delta", "2.7-cards", "course/modules/SC/SC1/cards.json (e919577b to 95f3f8cb)",
    "Card-level delta (card_delta_r1.py, out/card_delta_r1.txt): removed c217 (Proposition 2.3 finiteness question; its content stays covered by c133); added c232, c233, c234, c235, c236, c237, c238, c239, c241, c242, c243; changed 35 cards (listed in card_delta_r1.txt). "
    "Each changed or added card is read in full (out/changed_cards_new.txt) and checked in the rows above. The id gap at c240 is allowed by ruling 2.")

notes = (
    "Delta verification of slice e (ruling 30) from the round-13 fragment (pin e919577b) to 95f3f8cb. Every non-PASS row of round 13 (none) and every row whose subject changed was re-verified; "
    "rows whose subject is JSON-identical or byte-identical were carried, marked with the carry prefix. Verdict PASS: no ruling-26 defect kind was found in the changed hunks or the changed or added cards (false or unproved mathematical statement, missing hypothesis, wrong number, over-graded claim, failing gate, surviving non-equivalent mutant, lab statement the code does not support). "
    "No mutants were written (ruling 37; slice e has no grader). "
    "Observations, not FAIL, for a later round if the owner wants them fixed: "
    "(1) LOW, lessons L02 Assumption A2 sketch: 'their characteristic functions are exp(-u^2 (t^(k) - s^(k))/2)' is correct only when t^(k) >= s^(k); the sketch takes s and t unrestricted. The sketch is labelled 'Sketch, not a proof', and the sign slip predates this delta (it sits in the paragraph whose dyadic-time wording changed). "
    "(2) LOW, L06 Proposition 2.7 proof, Step 3 and its opening: it cites Proposition 2.3 for 'rho is a stopping time with rho <= t'; that fact is proved in the proof of Proposition 2.3, not in its statement. "
    "(3) LOW, L06 Proposition 2.7 proof: G denotes the sigma-field F_rho in the A4(b) application and G_± denote the functions of Step 4 (a within-proof symbol overlap; not a registry symbol). "
    "(4) Not a defect: card c217 was removed without replacement; c133 still covers 'Proposition 2.3 uses only rho <= t'. "
    "Out of slice and not read this round: course/modules/SC/SC1/index.html (its new Proposition 2.7 and Theorem 2.5 references point to existing numbered results in L06), project.html, grader/, and tests/labs/SC1/lab-SC1-project-1.py. "
    "Not run: the full repository gate (ruff over all, full mypy, render_curriculum, test_docs_figures); none of those inputs is in the slice. "
    "Mutants: none (ruling 37). Registry: no SC1 cite. Scripts: ledgers/SC1/scripts/SC1-e-r1/ (run_gates_r1.sh, run_twins_r1.sh, scan_cards_r1.py, card_delta_r1.py, l03_gap_r1.py, build_fragment_r1.py)."
)

freshness = ["No 2025-2026 freshness row is needed: SC1 cites no registry key in its cards or lessons; the lesson references name Shreve (registry key shreve2004stochastic) and Karatzas and Shreve (no registry record)."]

frag = {
    "unit": "SC1",
    "slice": "e",
    "round": 1,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-e, delta verification (ruling 30) of round 13 from e919577b to 95f3f8cb",
    "pin": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
    "base": "e919577b45b431ce68e1e6533b00b8a301277937",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyF31-SC1-e",
    "scratch": "ledgers/SC1/scripts/SC1-e-r1/out",
    "verified_at": "2026-11-09T16:45:00Z",
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": freshness,
    "notes": notes,
    "summary": (f"SC1 slice e round 1 (delta from e919577b to 95f3f8cb, rulings 30 and 37): {len(rows)} rows, all PASS. "
                "Changed lessons L01 to L06 and cards (35 changed, 11 added, c217 removed) were re-verified; L07 and L08 pages are byte-identical and carried. "
                "No FAIL row; four LOW observations are listed in notes."),
}
json.dump(frag, open("ledgers/SC1/SC1-e.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("rows", len(rows), "ids unique", len({r["id"] for r in rows}) == len(rows))
