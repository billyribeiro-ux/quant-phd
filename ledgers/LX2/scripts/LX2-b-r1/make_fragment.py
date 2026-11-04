"""Write the LX2 slice-b round-1 verification fragment (ledgers/LX2/LX2-b.json). Evidence cites scripts in this folder."""

import json
from pathlib import Path

S = "ledgers/LX2/scripts/LX2-b-r1/"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- labs and gates
row("lab-L03-run-isolated", "2.5 labs", "tests/labs/LX2/lab-LX2-L03-1.py",
    "PASS", "python -I -W error tests/labs/LX2/lab-LX2-L03-1.py exit 0, empty stderr; run_labs --unit LX2 -> 'run_labs LX2: PASS (7/7)' (" + S + "run_labs.out).")
row("lab-L04-run-isolated", "2.5 labs", "tests/labs/LX2/lab-LX2-L04-1.py",
    "PASS", "python -I -W error tests/labs/LX2/lab-LX2-L04-1.py exit 0, empty stderr (" + S + "check_embed.out); run_labs 7/7 PASS (" + S + "run_labs.out).")
row("lab-L03-page-equals-twin", "2.5 labs", "course/modules/LX/LX2/L03.html lines 104-327; tests/labs/LX2/lab-LX2-L03-1.py",
    "PASS", "check_embed.py: 'code equals twin (final newline ignored): True' (" + S + "check_embed.py, " + S + "check_embed.out).")
row("lab-L04-page-equals-twin", "2.5 labs", "course/modules/LX/LX2/L04.html lines 149-312; tests/labs/LX2/lab-LX2-L04-1.py",
    "PASS", "check_embed.py: 'code equals twin (final newline ignored): True' (" + S + "check_embed.out).")
row("lab-L03-expected-equals-output", "2.5 labs", "course/modules/LX/LX2/L03.html lines 328-344",
    "PASS", "check_embed.py: 'expected equals printed output: True' (embedded block equals the twin's run stdout) (" + S + "check_embed.out).")
row("lab-L04-expected-equals-output", "2.5 labs", "course/modules/LX/LX2/L04.html lines 313-360",
    "PASS", "check_embed.py: 'expected equals printed output: True' (" + S + "check_embed.out).")
row("lab-L03-independent-recompute", "2.5 labs / 2.2 numbers", "course/modules/LX/LX2/L03.html lines 328-344, 345, 381, 385, 486",
    "PASS", "recompute_l03.py (own re-implementation of the seeded book, same draw order, not an import): orders 331, executions 207, traded 4060, cancel events 69, crossed 0, identity failures 0, resting 170, market cancelled 30, trader cancelled 2020; table ratios 6/97, 3/104, 5/34, 6/29, 17/50, 21/37 all match; 3*97=291 < 6*104=624; 1050 vs 629; 59/986 (" + S + "recompute_l03.out).")
row("lab-L04-independent-recompute", "2.5 labs / 2.2 numbers", "course/modules/LX/LX2/L04.html lines 313-360, 361",
    "PASS", "recompute_l04.py (own generator, U then V per period, Fraction arithmetic, own rounding): errors list, hits 9/24, hit rate 3/8, bias 41/12 (3.4167), sum 82, first-12 1/4 and 11/3, last-12 1/2 and 19/6, MAE 13/3, 11/3->3.6667, 19/6->3.1667, -7/3->-2.3333, 44/117->0.3761, 20/39->0.5128, E[e]=1, band counts 9,27,44,60 (" + S + "recompute_l04.out).")
row("lab-L03-hypothesis-and-docstring", "2.5 labs / 2.2 lab-claims", "course/modules/LX/LX2/L03.html line 103; tests/labs/LX2/lab-LX2-L03-1.py lines 3-22",
    "PASS", "Hypothesis: zero crossed events, zero identity failures, zero tally disagreements = printed lines 3-5 (run output); cancel rates 5,10,25,40,60,85 = CANCEL_PCT line 143; flag at ratio > 2 = code line 216; 'none' for zero fills = line 211; cancel rule (own resting order, prob. CANCEL_PCT) = lines 252-254; identity and tally checks = lines 163-164, 170-178; 'does not decide lawfulness' is a docstring statement with no code claim.")
row("lab-L03-interpretation", "2.2 lab-claims", "course/modules/LX/LX2/L03.html line 345",
    "PASS", "Fill total 414 = 2 x 207 (printed line 6: True); largest ratio 21/37 below 2 (printed line 9 and table); 'ratios do not follow the cancel-rate column' (trader 1 rate 10 ratio 3/104 < trader 0 rate 5 ratio 6/97: 291 < 624). 'The proposition covers every run under A1' is discussed in row math-L03-prop22-time-index.")
row("lab-L04-hypothesis-and-interpretation", "2.2 lab-claims", "course/modules/LX/LX2/L04.html lines 148, 361",
    "PASS", "Hypothesis: bias 41/12 positive and not equal to 1 (Prop 4.4); Part B window changes both measures (1/4 vs 1/2; 11/3 vs 19/6); Part C bias 0 with large errors; Part D exact probability. Interpretation statements match printed lines.")
row("lab-L04-rounding-rule", "2.2 numbers / 2.5 labs", "course/modules/LX/LX2/L04.html lines 118, 167-169 (Def 4.1 and docstring); lab code lines 89-94",
    "PASS", "Rule floor(|x|*10^4+1/2)/10^4 with sign of x implemented by round_half_away (code line 93) and stated identically in Def 4.1 (line 118). recompute_l04.out reproduces every displayed value.")
row("lab-L04-docstring-partD-pair-order", "2.2 lab-claims / 2.4 notation", "tests/labs/LX2/lab-LX2-L04-1.py lines 27 and 140; course/modules/LX/LX2/L04.html lines 175 and 288",
    "FAIL", "The docstring says 'all 9 x 13 equally likely pairs (U, V)'. In the lesson U_t is the realised draw (13 values, -6..6, line 8 of the docstring and page line 123) and V_t the forecast draw (9 values). The code enumerates u over the forecast range (9 values) and v over the realised range (13 values), i.e. (V, U); the printed line 'pairs = 117 (9 forecast draws times 13 realised draws)' and Prop 4.4 (line 142) use (V_t, U_t). Ordering in the docstring contradicts the stated convention.",
    "Change '(U, V)' to '(V, U)' in tests/labs/LX2/lab-LX2-L04-1.py lines 27 and 140 (V = forecast draw, U = realised draw), run .venv/bin/python tools/embed_labs.py course/modules/LX/LX2/L04.html --refresh lab-LX2-L04-1, then run_labs --unit LX2. Optionally rename the loop variables in part_d so that u is the realised draw.")

# ---- gates
row("gate-run-labs-LX2", "gate", "tests/labs/LX2/, course/modules/LX/LX2/",
    "PASS", "run_labs.py --unit LX2 -> 'run_labs LX2: PASS (7/7)' exit 0 (" + S + "run_labs.out).")
row("gate-pytest-lab-twins-L03-L04", "gate", "tests/test_labs.py -k 'LX2-L03 or LX2-L04'",
    "PASS", "pytest -q: '..' 2 passed, exit 0 (" + S + "pytest_labs.out).")
row("gate-ruff-mypy-twins", "gate", "tests/labs/LX2/lab-LX2-L03-1.py, lab-LX2-L04-1.py",
    "PASS", "ruff check: 'All checks passed!'; ruff format --check: '2 files already formatted'; mypy --no-incremental: 'Success: no issues found in 2 source files' (" + S + "mypy.out).")
row("gate-check-pages-LX2", "gate", "course/modules/LX/LX2/*.html",
    "PASS", "check_pages.py --unit LX2 -> 'check_pages LX2: PASS' exit 0 (" + S + "check_pages.out).")
row("gate-check-dag-LX2", "2.9 DAG", "course/modules/LX/LX2/",
    "PASS", "check_dag.py --unit LX2 -> 'check_dag LX2: PASS' exit 0 (" + S + "check_dag.out).")
row("gate-page-smoke-L03-L04", "2.9 / 2.5", "course/modules/LX/LX2/L03.html, L04.html",
    "PASS", "page_smoke.py --unit LX2 --pages L03 L04 (run alone) -> 'page_smoke modules/LX/LX2/L03.html: PASS', '...L04.html: PASS', 'page_smoke LX2: PASS' (labs run in Pyodide, zero console errors, no horizontal scroll at 360 px, math renders) (" + S + "page_smoke_L03_L04.out).")
row("gate-verify-refs-LX2", "2.1 citations", "references/references.json (LX2 entries used by L04: cfandcode line 4946, frb2026fed line 9185)",
    "PASS", "verify_refs.py --unit LX2 -> 'live re-verification of LX2: 6 of 560 entries, 0 problems' exit 0 (" + S + "verify_refs_unit.out).")

# ---- math
row("math-L03-prop22-time-index", "2.4 mathematics (statement omits a hypothesis)", "course/modules/LX/LX2/L03.html lines 81-84 (statement), 88 (proof), 103 (hypothesis), 345 (interpretation)",
    "FAIL", "Proposition 2.2 is graded T and reads 'Under A1, let G be the shares of all orders at their arrival ... Then G = R + 2X + C_m + C_t' with no time index. Its proof (line 88) fixes the time as the end: 'resting at the end', 'A share that is none of these is still resting at the end'. The lab hypothesis (line 103) and interpretation (line 345) use the identity after every event ('should hold after every event', 'holds after every event of this flow'), and the code checks it after each of 400 events (lab lines 263-267). The statement does not cover intermediate times, and the proof as written does not establish them. recompute_l03.py confirms 0 failures after every event, so the claim is true for this flow, but the proposition as stated does not license it.",
    "Restate Proposition 2.2 with the time index: 'At every moment of a run under A1, with each quantity counted over the orders and executions up to that moment, G = R + 2X + C_m + C_t.' In the proof, change 'resting at the end' and 'still resting at the end' to 'resting at that moment', and say that the sums are taken over orders that have arrived by that moment. Keep the 'at the end' version only in Misconception 2 (line 385), which already says 'when the run ends'.")
row("math-L03-prop22-proof-end-of-run", "2.4 mathematics", "course/modules/LX/LX2/L03.html line 88",
    "PASS", "Read the proof step by step: routes (filled, market-cancelled, trader-cancelled, resting) are disjoint under A1; executions add q to exactly two distinct orders (A1), so sum f_o = 2X; cancelled shares split into C_m and C_t; the identity follows at the end of the run. Correct for the end-of-run reading; the time gap is FAIL row math-L03-prop22-time-index.")
row("math-L03-problems", "2.4 / 2.2 numbers", "course/modules/LX/LX2/L03.html lines 402-493",
    "PASS", "M1 fills 4+2=6, ratio 1/2; M2 fills 2, ratio 0; M3 C_t = 1000-120-600-40 = 240; P1 integer flag equivalence (f>=1); P2 disjointness; P3 c(f2-f1)/(f1 f2) >= 0; E1 21/37 > 17/50 (1050 > 629); E2 threshold 1 (every trader has >=3 cancels, minimum 3; max ratio 21/37<1); E3 59/986 (recomputed: 6/29-5/34 = 59/986); R1, R2, R3 consistent with the table (recompute_l03.out).")
row("math-L04-thm42-thm43", "2.4 mathematics", "course/modules/LX/LX2/L04.html lines 127-136",
    "PASS", "Thm 4.2 proof (indicator monotone in band) valid for 0<=b1<=b2 and states the only hypothesis used. Thm 4.3: |sum e| <= sum |e| (triangle inequality); equality case: |P-N| = P+N iff min(P,N)=0 iff one sign group is empty (checked line by line).")
row("math-L04-prop44", "2.4 mathematics", "course/modules/LX/LX2/L04.html lines 139-142",
    "PASS", "E[e]=1 from E[V]=E[U]=0 (symmetric ranges). Hit event |e|<=2 equals -3 <= V-U <= 1; for v in -4..3 the admissible u are v-1..v+3 (5 values inside [-6,6]), for v=4 they are 3..6 (4 values); 8*5+4=44; 44/117. Enumeration (recompute_l04.out): 117 pairs, 44 hits, E=1. Assumption A1 is stated (line 123) and used.")
row("math-L04-def41-rounding-proof", "2.2 numbers / 2.4", "course/modules/LX/LX2/L04.html line 118; course/modules/LX/LX2/L04.html problems P2 (line 396), M2 (line 388), M3 (line 390)",
    "PASS", "P2 proof: n = floor(y+1/2) gives |n-y| <= 1/2, hence |r(x)-x| <= 1/20000; M2: -7/3 -> -2.3333; M3: 44/12 = 11/3 -> 3.6667 (36667.17 floor 36667). Verified in recompute_l04.out.")
row("math-L04-problems-M-P-E-R", "2.4 / 2.2 numbers", "course/modules/LX/LX2/L04.html lines 385-414",
    "PASS", "M1 hit rate 1/2, bias 1/2; P1 errors 2,2,0,0 give hit rate 1 and bias 1; P3 windows 0,0,0,0 and +3,-3,+3,-3 both bias 0, hit rates 1 and 0; E1 hits 13,15,18,20,23,24 = 6 of 12 = 1/2 (table rows checked against the printed Part A); E2 errors 1-12 sum 44, bias 11/3 (3.6667); E3 Var(V)=20/3, Var(U)=14, Var(e)=62/3, se=sqrt(62/72)=0.9280, gap 29/12=2.4167, z=2.60 (recompute_l04.out); R1 44 pairs by counting; R2 counts 9, 27, 44, 60, first b with prob >= 1/2 is b=3 with 60/117 = 20/39 = 0.5128; R3 n=2 (+1,-1).")

# ---- notation
row("notation-L03", "2.4 notation", "course/modules/LX/LX2/L03.html; tests/labs/LX2/lab-LX2-L03-1.py",
    "PASS", "Macros used on the page: \\ge, \\le, \\cdot, \\times, \\sum, \\blacksquare, only standard LaTeX (grep count). Symbols G, R, X, C_m, C_t, g_o, f_o, k_o, r_o, f, c, D, f_1, f_2 are local and do not collide with notation/notation.json symbols (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}). No \\mathbb{R}, no T used.")
row("notation-L04", "2.4 notation", "course/modules/LX/LX2/L04.html; tests/labs/LX2/lab-LX2-L04-1.py",
    "PASS", "Registered macros used: \\E (5), \\Var (4), \\indic (3), \\se (1) (all in notation/notation.json macros). Other macros are standard LaTeX (\\operatorname, \\hat, \\frac, \\sum, \\lfloor, \\rfloor, \\tfrac, \\min, \\cap, \\approx, \\ldots, \\dots). No registered symbol is re-used: H is the horizon (BUILDER rule for LX2), T absent. \\R and \\mathbb{R} absent.")

# ---- grades and cards
row("grade-L03", "2.3 grades", "course/modules/LX/LX2/L03.html (data-grade attributes, key-results table)",
    "PASS", "Only Proposition 2.2 is graded T (proved on the page, subject to the time-index FAIL row). Lab results are 'not graded (SIMULATED output)' or 'not graded (demonstration value)' (key results lines 505-506), consistent with rule (9).")
row("grade-L04-keyresults-simulated-T", "2.3 grades (rule 9: SIMULATED lab values are C)", "course/modules/LX/LX2/L04.html line 429 (key-results table)",
    "FAIL", "Row 'Exact hit rate 3/8 and bias 41/12 on the SIMULATED path of Lab 1, Part A' is graded T with source 'Lab 1, Part A (computed)'. The values are read off a SIMULATED lab output (lab Part A, lines 340-343 of the page). Verifier rule (9) grades such values C, naming the lab. L03 handles the same kind of result as 'not graded (SIMULATED output)'. The T grade on the Part C hand-built path (line 430) and on Prop 4.4 (line 432) is correct because those are proved on the page.",
    "Change the grade in line 429 to C and the source to 'Lab 1, Part A (SIMULATED seed 20261103; computed from the printed output)'. Alternatively mark it 'not graded (SIMULATED output)' as L03 does.")
row("cards-L04-c085-grade", "2.7 retrieval cards", "course/modules/LX/LX2/cards.json, id LX2-c085",
    "FAIL", "Card LX2-c085 asks for the exact hit rate and bias on 'the 24-period SIMULATED path of Lab 1, Part A (seed 20261103)' with grade T and basis 'Lab 1, Part A (computed)'. Same defect as L04 line 429: a value read off a SIMULATED lab is C naming the lab (verifier rule 9); the basis also omits SIMULATED as BUILDER_RULES 7 and the plan §9 require for SIMULATED results.",
    "Set \"grade\" to \"C\" and \"basis\" to \"Lab 1, Part A (SIMULATED, seed 20261103)\". Card content unchanged.")
row("cards-L03", "2.7 retrieval cards", "course/modules/LX/LX2/cards.json LX2-c044 to LX2-c063",
    "PASS", "All 20 L03 cards read in full against L03 text: each atomic, back checkable against the lesson (Defs 1.1, 1.3, Remark 1.2, A1, Prop 2.2 with T, Remarks 2.3-2.4, Defs 3.1-3.2, Lab 1 printed values 69, 207, 2020, 21/37, 3/104 vs 6/97). Lab-derived cards are C or 'not graded' with basis naming Lab 1 (LX2-c053, c058, c059).")
row("cards-L04-except-c085", "2.7 retrieval cards", "course/modules/LX/LX2/cards.json LX2-c064 to LX2-c089 except c085",
    "PASS", "All 26 L04 cards read in full against the L04 text and the source quotes: definitions (c064-c065), SR 26-2 definitions and locators (c066-c069, c082-c084), A1/A2 (c074-c075), Theorems 4.2, 4.3 with hypotheses (c076-c077), Prop 4.4 with 'Assuming A1' (c078-c079), CFA quotes (c080-c081, c087-c088), SR enforceability (c089), Part C (c086). Card numbers 44/117, 0.3761, 3.4167, 0.3750 each appear in the lesson.")
row("cards-duplicates", "2.7 retrieval cards", "course/modules/LX/LX2/cards.json",
    "PASS", "No duplicate ids across the 89 cards (python check). No two L03/L04 cards state the same fact (c064/c080 and c087/c088 cover different Code statements).")

# ---- citations and attribution
row("cite-L04-cfa-quotes", "2.1 attribution (45 quotes)", "course/modules/LX/LX2/L04.html lines 56-82, 87-90 (all CFA quotes), key results 423-425, quiz 441-456",
    "PASS", "Fetched with plain curl: https://www.cfainstitute.org/standards/professionals/code-ethics-standards/standards-of-practice-iii-a, -vi-a, -vi-b (scripts: fetch_sources.sh, extract_sources.py). quote_check.py: all CFA quotes FOUND (III(A) The Standard; III(A) Guidance paragraphs 1, 2 and the 'however' paragraph; VI(A) The Standard, Guidance first and second paragraphs; VI(A) Application Example 3 Outcome; VI(B) The Standard). Example 3 facts (Fargmon, wife inherits Kincaid stock) match. Locators 'Guidance, paragraph 2' etc. match the page structure. (quote_check.out)")
row("cite-L04-sr26-2-quotes", "2.1 attribution (SR 26-2)", "course/modules/LX/LX2/L04.html lines 85-111, key results 426-428, quiz 459-483",
    "PASS", "Fetched: sr2602.htm (letter body, Applicability line, 'supersedes and replaces SR letter 11-7 ... and SR letter 21-8', Supersedes list at sr2602.txt line 301) and SR2602a1.pdf (attachment, printed pages 1-12, read in full). Verified each quote and locator: p.1-2 Sec I (definition of responsibility, spans pp. 1-2), p.2 Sec I 'does not set forth enforceable standards' and footnote 1, p.3 Sec II model definition and Sec III model risk, p.7 Sec IV 'Effective model use ... limitations' and Sec V 'Model validation evaluates ...', p.8 Conceptual Soundness and Sec V paragraph before Components, p.9 Outcomes Analysis paragraphs 1-2 (incl. 'persistent deviations...'), p.9 Ongoing Model Monitoring. Component list on p.8 (Conceptual Soundness) and p.9 (Outcomes Analysis, Ongoing Model Monitoring) correct. No heading 'Limitations' (grep -i limitation hits are body text only). The 'responsible for adopting ...' quote spans the p.1 and p.2 footer and is present in the text. (quote_check.out, plain.txt).")
row("cite-L04-hit-bias-search", "2.1 attribution (negative claim)", "course/modules/LX/LX2/L04.html line 111; card LX2-c084",
    "PASS", "Search of the full attachment text (pdftotext, both layout and plain modes) and the letter page for 'hit' and 'bias' (case-insensitive): zero matches (grep returned no line). The claim 'returns no match' is true.")
row("cite-L04-registry-keys", "2.1 citations / registry", "references/references.json lines 4946 (cfandcode), 9185 (frb2026fed); course/modules/LX/LX2/L04.html data-cite attributes",
    "PASS", "Only cfandcode and frb2026fed are cited (grep data-cite). Both keys exist (references.json 4946, 9185) and verify_refs --unit LX2 passes live (" + S + "verify_refs_unit.out). No SR 11-7 or 21-8 record exists (grep returns no line) and the page does not cite them.")
row("cite-L03-fc1-claim", "2.1 attribution (cross-lesson)", "course/modules/LX/LX2/L03.html lines 73, 107 (FC1 order-book rules); tests/labs/LX2/lab-LX2-L03-1.py lines 4-6",
    "PASS", "FC1 course/modules/FC/FC1/L04.html text: price-time priority; fill at the resting order's price; 'A market order never rests in the limit order book'; market-order remainder cancelled; 'The model has no cancellations or modifications of resting orders. Proposition 2.3 has no term for shares removed from the book by withdrawal'. So L03 line 73 ('has no trader cancels, so its share identity has no term for them') and the lab docstring's rule list are accurate. FC1 is not PASS (N3); the LX2 merge waits for it (plan Q11), which is not a defect of this slice.")
row("attr-L04-why-it-matters-scope-uncited", "2.1 attribution / BUILDER 2.3 (cite every requirement)", "course/modules/LX/LX2/L04.html line 51 (why-it-matters paragraph)",
    "FAIL", "'An investment professional owes clients a duty of loyalty and care whether or not a statute imposes further duties, and an interest that could impair objectivity must be avoided or disclosed.' (a) Scope: Standard III(A) applies to 'all CFA Institute members and candidates' (standards-of-practice-iii-a.txt, Guidance, paragraph 'The single standard of conduct ...'), and Standard VI(A) to 'Members and candidates'; the sentence states it for every investment professional. (b) No data-cite or data-locator, although BUILDER_RULES 2.1 and plan 2.3 require a requirement to carry both. The second half paraphrases VI(A) but drops 'could reasonably be expected' and the members-only scope.",
    "Rewrite as: 'A CFA Institute member or candidate owes clients a duty of loyalty, prudence and care under Standard III(A), whether or not a statute imposes further duties; a matter that could reasonably be expected to impair independence and objectivity must be avoided or disclosed under Standard VI(A).' Wrap each half in <span class=\"claim\" data-grade=\"C\" data-cite=\"cfandcode\" data-locator=\"Standard III(A), The Standard\"> and <span ... data-locator=\"Standard VI(A), The Standard\">.")
row("attr-L04-scope-note-and-section1", "2.1 attribution", "course/modules/LX/LX2/L04.html lines 53, 56, 69",
    "PASS", "Scope note states the Code is quoted, the letter is quoted from its attachment, and statutes or decisions are not read; line 69 says the Code's duty of loyalty is the only fiduciary-duty text quoted (true: no other fiduciary quote on the page). 'It is not a statute' (line 56) is a description of the Code, not a holding.")
row("attr-L03-dodd-mifid-characterisation", "2.1 attribution (unread description)", "course/modules/LX/LX2/L03.html lines 353 and 358 (Definitions 3.1 and 3.2)",
    "FAIL", "Definition 3.1 says the Dodd–Frank Act 'is the name the curriculum gives to one statute'; Definition 3.2 says MiFID II 'is the name the curriculum gives to one set of rules on financial markets'. Neither description is read from a source (registry grep: no Dodd, Frank or MiFID record; review_queue has only unrelated titles). Plan 0.3 B1 and 3 L03 allow only 'named, content not stated here'. The 'content not stated' sentence itself is correct.",
    "Delete the form descriptions: 'The Dodd–Frank Act is the name the curriculum gives to one of this unit's concepts.' and 'MiFID II is the name the curriculum gives to one of this unit's concepts.' Keep the sentences that say the provisions are not stated and that no key is cited.")
row("attr-L03-no-registry-keys", "2.1 citations", "course/modules/LX/LX2/L03.html line 54 and Section 9",
    "PASS", "L03 cites no registry key (no data-cite on the page) and says so (line 54, Section 9). No bibliographic data typed. The reference registry has no Dodd–Frank or MiFID II record (grep).")
row("prose-L03-misconception1-two-events", "2.9 prose accuracy", "course/modules/LX/LX2/L03.html line 381 (misconception 1)",
    "FAIL", "'The ratio counts two events, and it records neither intent nor any legal test.' The ratio divides two counts, cancels and fills (Definition 1.1); a fill is an execution counted once for each of the trader's orders in it, so 'two events' is not what the ratio counts. Remark 2.4 says the ratio counts cancel events.",
    "Replace 'The ratio counts two events' with 'The ratio divides two counts, cancels and fills,'.")
row("prose-banned-and-process-words", "2.9 banned strings / process words", "course/modules/LX/LX2/L03.html, L04.html and both twins",
    "PASS", "check_pages --unit LX2 PASS (BANNED tuple, lines 57-72 of tools/check_pages.py). grep for TODO, TBD, lorem, 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'experts agree', 'it is well known', 'obviously', 'clearly': no hits. Ellipses '...': only inside code blocks (L04 lines 156-158, the lab docstring). Unicode '…' only at L04 lines 509 and 513, and LaTeX \\ldots at lines 388 and 390; all are decimal repetends, not omitted content. Process words (build, builder, verifier, REQUESTS, unit report): no hits in learner text.")
row("prose-L03-quiz-fieldset", "2.9 / plan 2.1 item 9", "course/modules/LX/LX2/L03.html lines 518, 527, 536, 560, 574",
    "PASS", "All five multiple-choice fieldsets carry style=\"min-inline-size: 0\".")
row("html-L04-quiz-fieldset", "plan 2.1 item 9 (quiz fieldset)", "course/modules/LX/LX2/L04.html lines 442, 451, 460, 469, 478, 487, 496",
    "FAIL", "Plan 2.1 item 9 binds quiz options to use <fieldset style=\"min-inline-size:0\">. All seven L04 multiple-choice fieldsets are bare <fieldset>. course.css line 1468 (.quiz fieldset) sets no min-inline-size. page_smoke PASS at 360 px, so no overflow is observed, but the page does not meet the binding rule that L03 meets.",
    "Add style=\"min-inline-size: 0\" to the seven <fieldset> tags at lines 442, 451, 460, 469, 478, 487 and 496, matching L03.")
row("structure-L03", "2.9 structure", "course/modules/LX/LX2/L03.html",
    "PASS", "Order per BUILDER 4.2: why it matters; sections 1-3 with inline Lab 1; canon breaks (s4); misconceptions (3); problem set (3 per tier: mechanics M1-3, proof P1-3, empirical E1-3, research R1-3, each with details.solution); key results table; retrieval quiz (10 items, 8-15); references. data-hours=9.")
row("structure-L04", "2.9 structure", "course/modules/LX/LX2/L04.html",
    "PASS", "Same order: why it matters; sections 1-4 with inline Lab 1; canon breaks (s5); misconceptions (4); problem set (M1-3, P1-3, E1-3, R1-3); key results; quiz (11 items); references. data-hours=9. Assumptions A1, A2 numbered.")
row("hours", "2.6 / 2.9 hours", "course/modules/LX/LX2/index.html line 29 (data-hours-lessons=36, data-hours-project=14); L03.html and L04.html data-hours=9",
    "PASS", "Lessons 4 x 9 = 36 h = hub figure; project 14 h; total 50 = curriculum (curriculum/06-profession-capstone.yaml:53). Titles in the hub card and in the nav links match the L03 and L04 h1.")
row("data-and-simulated-labels", "2.8 data / 2.5 labels", "course/modules/LX/LX2/L03.html lines 103, 106, 345; L04.html lines 148, 151, 361; twins docstrings",
    "PASS", "No data-files attribute on either lab; no external data. L03 and L04 are labelled SIMULATED in the hypothesis, the twin docstring and the interpretation. The seed and generator are stated (L03 SEED 2026; L04 seed 20261103, draws in order U_1, V_1, ...).")
row("dag-L03", "2.9 DAG", "course/modules/LX/LX2/L03.html lines 37, 67-70, 102, 355-361",
    "PASS", "check_dag PASS. Only links are to concepts.html#limit-order-book and #order-types (FC1 concepts, in the closure). Market-manipulation defined here (def-market-manipulation); Dodd–Frank and MiFID II defined last (Defs 3.1, 3.2). No use of insider, tipping, misappropriation as a term (only the nav link to L02). 'market making' (line 491) is plain prose; the concept market-making-game is PC3 and is not used.")
row("dag-L04", "2.9 DAG (plain-prose out-of-closure terms)", "course/modules/LX/LX2/L04.html lines 56-111, 366-368, 406",
    "PASS", "Only LX2 concepts defined (fiduciary-duty, conflict-of-interest, model-risk-management). Out-of-closure term 'variance' (curriculum concept owner M4, curriculum.json concepts) and 'standard error' appear in plain prose in Problem E3 and Section 5, with no link and no dfn, which the architect default permits. No L03 concept used by link or definition. No D1-D9 concept (plan 4) used by name except plain prose already allowed.")
row("freshness", "2.1 freshness", "SR 26-2 (frb2026fed); CFA Code (cfandcode)",
    "PASS", "SR 26-2 page shows 'April 17, 2026' and 'Last Update April 17, 2026' (sr2602.txt). The CFA landing page shows the Code effective 1 January 2024 and Standards 'Updated April 2024' / 'January 2024' (cfa.txt, III(A), VI(A), VI(B) pages). No newer version was found in the fetched pages.")
row("grades-slice-L04-theorems-and-quotes", "2.3 grades", "course/modules/LX/LX2/L04.html claim spans lines 58-111, theorems 127-142",
    "PASS", "Quoted CFA and SR text graded C with cite and locator (rule 2.3). Theorems 4.2, 4.3 and Prop 4.4 graded T with proof on the page. Misconceptions and the Part C claims are not graded claims beyond T.")

fragment = {
    "unit": "LX2",
    "slice": "LX2-b",
    "round": 1,
    "verifier": "Claude Haiku 5.5, independent verifier for LX2 slice b (L03, L04 and lab twins), round 1; did not build LX2",
    "pin": "1c1645f3",
    "base": "none: first verification of this slice (base = pin 1c1645f3)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE1-LX2-b",
    "scratch": "/tmp/lx2b-src (fetched sources and extracted text; untracked)",
    "verified_at": "2026-11-04T04:40:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "cfandcode: record type 'primary' against the curriculum string '(practitioner)' (N2, known); the registry url is the Code landing page, which does not contain the Standards text. The quoted text is on the issuer's per-standard pages (standards-of-practice-iii-a, -vi-a, -vi-b, same domain). The architect may record those URLs as the locators' source.",
        "frb2026fed: the page verifies. The attachment is at https://www.federalreserve.gov/supervisionreg/srletters/SR2602a1.pdf and is cited by page only; the architect may add the attachment URL to the record.",
    ],
    "freshness_flags": [],
    "notes": (
        "Mutation testing is not applied: lab twins are demonstrations (architect ruling). Cross-unit: L03 relies on FC1 L04 text for the order-book rules; FC1 ledger is FAIL (N3), so the LX2 merge waits (plan Q11). "
        "Not checked: (1) the Dodd–Frank and MiFID II primary texts (no source admitted; nothing to verify); (2) the CFA Code PDF at code_of_ethics_and_standards_of_professional_conduct_2024.pdf is a 0-page stub with text, so only the per-standard pages were used for quotes; (3) SR 26-2 pages 10-12 were read in full but no L03/L04 quote cites them; (4) the 'Lab 1' outputs were checked by two independent scripts, not by the Pyodide runtime beyond page_smoke; (5) 'Part C ... mean absolute error is 3' is a computed fact, the lab does not print it (not treated as a lab claim); (6) cards for L01/L02 and the hub belong to other slices and were not read beyond the two lesson sets."
    ),
    "summary": "",
}
n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_fail = sum(1 for r in rows if r["status"] == "FAIL")
fragment["summary"] = f"rows {len(rows)}: PASS {n_pass}, FAIL {n_fail}, UNVERIFIABLE 0. Verdict FAIL on 8 defects (see FAIL rows)."
out = Path("/Users/billyribeiro/.fanout/wt/verifyE1-LX2-b/ledgers/LX2/LX2-b.json")
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, len(rows), n_pass, n_fail)
