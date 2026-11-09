# Builds the round-4 fragment ledgers/M5/M5-a.json for M5 slice a. Carried rows are copied from the round-3 fragment
# (/Users/billyribeiro/.fanout/frags/S-M5-a.round3.json) only where the cited subject is byte-identical at edbb7aa8
# (checked with git diff --quiet 8196077d edbb7aa8 -- <file>, and card objects with card_delta_r4.py).
import json, datetime, sys
R3 = "/Users/billyribeiro/.fanout/frags/S-M5-a.round3.json"
OUT = "ledgers/M5/M5-a.json"
O = "ledgers/M5/scripts/M5-a-r4/"
prev = {r["id"]: r for r in json.load(open(R3, encoding="utf-8"))["rows"]}

def carry(rid, subject):
    r = prev[rid]
    assert r["status"] == "PASS", rid
    return {"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
            "evidence": f"Carried from round 3 ({subject} byte-identical since 8196077d): " + r["evidence"]}

def fresh(rid, check, location, evidence, status="PASS", fix=None):
    row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix
    return row

rows = []
# ---- hub (index.html unchanged since 8196077d) ----
rows.append(carry("A1-hub-structure", "index.html"))
rows.append(carry("A1-hub-hours", "index.html; curriculum/01-foundations.yaml unchanged"))
rows.append(fresh("A1-hub-objectives", "2.9 objectives",
    "index.html:45-56",
    "index.html is byte-identical to 8196077d (git diff --quiet). Each objective's lesson re-checked against that lesson's block titles at edbb7aa8 "
    "(grep of block-title in each page): L01 Theorem 1.2 and Corollary 1.4 (L01.html:67, 97); L02 Proposition 2.2, Theorem 2.5, Corollary 3.2 with "
    "'exactly when' conclusion (L02.html:85, 127, 157-162); L03 Proposition 1.4 and Proposition 3.1 (L03.html:80, 203); L04 metric axioms "
    "(L04.html:59-64) and Proposition 2.1 (L04.html:243); L05 Proposition 2.1 uniform limit continuous (block title); L07 Theorem 2.1 Banach with "
    "Lemma 2.2 and Corollary 3.2; L08 Theorem 2.2 (operator is a contraction); L09 Theorem 2.4 certified stopping rule; L10 Corollary 3.2 closed form. "
    "Round-4 delta touched L02.html (Proposition 3.3 hypothesis list, Remark 2.6, misconception 1) but no block title named in the objectives."))
rows.append(carry("A1-hub-prereqs", "index.html and course/concepts.html (generated; build_site --check PASS, r4_build_site_check.out)"))
rows.append(carry("A1-hub-placement-structure", "index.html"))
rows.append(carry("A1-hub-placement-answers", "index.html"))
rows.append(carry("A1-hub-placement-rung1-skill", "index.html; project.html lines 44 and 113-114 (project hunks at 53, 57, 235, 404-412, 439-475 only; git diff -U0)"))
rows.append(carry("A1-hub-placement-rung2-skill", "index.html; project.html line 45 (no hunk there)"))
rows.append(fresh("A1-hub-lesson-map", "2.9 lesson map and card text",
    "index.html:129-144",
    "index.html byte-identical to 8196077d. Ten links L01-L10 resolve. data-hours at edbb7aa8: L01-L06 = 10, L07-L10 = 11 (grep of data-hours in each page), "
    "matching the card hours; 6*10+4*11 = 104. Card text for each of L01-L04 names results whose block titles exist at edbb7aa8: L01 'Archimedean property and nested intervals' "
    "(Theorem 1.2, Theorem 1.3) and 'bisection that brackets a supremum' (Theorem 1.6, L01.html:67, 82, 128); L02 'Cauchy sequences', 'Cauchy criterion for series' "
    "(Definition 2.1, Theorem 2.5, Corollary 3.2, L02.html:80, 127, 157); L03 'sequential characterization', 'failure of uniform continuity for x^2' (Proposition 2.1, "
    "Proposition 3.1, L03.html:172, 203); L04 'metric axioms, open and closed sets, sup metric on bounded functions, completeness' (Definition 1.1, Proposition 2.1, "
    "Example 1.6, Definition 3.2, L04.html:59, 243, 213, 265). L05-L10 card text re-checked against their block titles at edbb7aa8 (L07 Theorem 2.1 and Corollary 3.2; "
    "L08 Theorem 2.2; L09 Theorem 2.4; L10 Corollary 3.2), all present."))
rows.append(carry("A1-hub-ladder", "index.html; project.html lines 44-47 (no hunk there)"))
rows.append(fresh("A1-hub-data-status", "2.8/2.9 data status",
    "index.html:157-160; L08.html:138; L09.html:132; L10.html:177",
    "grep at edbb7aa8: 'data-files' count 0 in index, L01-L04 (r4_slice_scans.out); SIMULATED label present at L08.html:138, L09.html:132, "
    "L10.html:177 (grep, r4 check). No currency value: grep -i for dollar, USD, EUR, cents over index.html and L01-L04.html at edbb7aa8 returned no line. index.html:159 claim holds."))
rows.append(fresh("A1-hub-reading", "2.1 citations and reading list",
    "index.html:162-169; references/references.json; tools/verify_refs.py",
    "r4_verify_refs_offline_all.out 'offline integrity: 560 entries, 0 problems' (exit 0); r4_verify_refs_M5_live.out 'live re-verification of M5: 2 of 560 "
    "entries, 0 problems' (exit 0). Hub line 168 claim about M1 results: M1 L02.html:132-133 (Corollary 2.6, no rational number has square 2) and M1 "
    "L06.html:90-99 (Definition 2.1 and Theorem 2.2 for q != 1); course/modules/M/M1 byte-identical since 8196077d. Abbott and Rudin not opened; no locator asserted from them."))
# ---- L01 (byte-identical since 8196077d) ----
for rid in ["A1-L01-structure", "A1-L01-math", "A1-L01-numbers", "A1-L01-problems", "A1-L01-quiz-keyresults"]:
    rows.append(carry(rid, "L01.html"))
rows.append(fresh("A1-lab-L01-1", "2.5 lab: run, twin, page equals twin, expected equals output",
    "tests/labs/M5/lab-M5-L01-1.py; L01.html:144-231",
    "r4_run_labs_L01.out 'run_labs M5: PASS (1/1)' exit 0. Twin alone: r4_twin_L01.exit 0, r4_twin_L01.err 0 bytes (python -I -W error). "
    "r4_lab_expected_vs_twin.out 'L01: expected==twin_stdout True | page code==twin file True'. Standard library only; exact rational arithmetic; no randomness."))
# ---- L02 (changed since 8196077d: fresh) ----
rows.append(fresh("A1-L02-structure", "2.9 structure and template order",
    "course/modules/M/M5/L02.html:1-548 (sections 1-9 at lines 53, 77, 149, 297, 307, 325, 430, 449, 539)",
    "Read in full at edbb7aa8 (L02.html:1-553). Order: header 33-40, grade legend 42-49, §1 53-75, §2 77-147, §3 149-209, lab 211-294 (pre 214-285, expected 286-292, interpretation 293), "
    "§4 canon breaks 296-304, §5 misconceptions 306-322, §6 problems 324-427, §7 key results 429-446, §8 quiz 448-536, §9 references 538-542, next-link 545-548. "
    "The round-3 delta removed one hypothesis line of Proposition 3.3, so every locator from line 176 on is one line higher than in round 3. "
    "check_pages M5 PASS (r4_check_pages_M5.out, exit 0).",
    ))
rows.append(fresh("A1-L02-math", "2.4 mathematics: hypotheses, proofs, grades (re-verified after round-3 FAIL)",
    "course/modules/M/M5/L02.html:145-147 (Remark 2.6), 170-181 (Proposition 3.3 block 170-176, proof 178-181), 308-311 (misconception 1)",
    "Round-3 FAIL is fixed. Proposition 3.3 now lists only (H1) (L02.html:172-174); the sentence 'Only the consequence on divergence uses it' is gone; the proof "
    "(L02.html:180) takes H_{2N}-H_N >= 1/2 from the N terms 1/(N+1)..1/(2N), then assumes convergence, applies Proposition 2.2 (convergent implies Cauchy, which "
    "uses no completeness: L02.html:93-94) with eps = 1/2, and takes n=N, m=2N to contradict the inequality. Re-derived: each step is valid, and the consequence "
    "uses no completeness. Remark 2.6 (L02.html:146) states: (H2) is used in Lemma 2.4 and Theorem 2.5, and so in the converse direction of Corollary 3.2, which is "
    "proved from Theorem 2.5 (L02.html:167: 'By Proposition 2.2 and Theorem 2.5'). Checked: Theorem 2.5 is used in Corollary 3.2 (line 167) and in canon break 1 (line 300); "
    "Lemma 2.4 uses (H2) at line 123; Theorem 2.5 uses (H2) on line 137 (suprema b_k) and through Lemma 2.4 for L on the same line. Misconception 1 (L02.html:311): taking m = n+1 in "
    "Cauchy with Proposition 2.2 gives |a_{n+1}| < eps, a valid necessity argument. Other propositions, lemmas and theorems re-derived this round (Prop 1.2, Prop 2.2, "
    "Lemma 2.3, Lemma 2.4, Thm 2.5, Cor 3.2, Lemma 3.4, Prop 3.5 both directions, R3 geometric decay with beta != 1). No defect. r4_l02_numbers.out 19/19 PASS."))
rows.append(fresh("A1-L02-numbers", "2.2 numbers in prose and lab output",
    "L02.html:213, 286-292 (expected), 293 (interpretation), 382-400 (E1-E3), 449-536 (quiz)",
    "r4_twin_L02.out equals the expected block at L02.html:286-292 line for line (r4_lab_expected_vs_twin.out True; stderr 0 bytes; exit 0). Independent exact "
    "recomputation in ledgers/M5/scripts/M5-a-r4/l02_numbers_r4.py (r4_l02_numbers.out, 19 of 19 PASS): H_2-H_1 = 1/2; H_4-H_2 = 7/12; min over N=1..200 of H_2N-H_N is "
    "1/2 at N=1; Prop 3.3 bound for N=1..400; sum_{j=1}^{60} j = 1830; G_3 = 7/8; G_3-G_1 = 3/8; Lemma 3.4 identity on 1830 pairs; threshold N=10 for m<=60, N=0..20; "
    "H_{2^k} >= 1+k/2 for k=0..10. Prose numbers in the changed text (E2, E3, R1, R2, Prop 3.3) all match."))
rows.append(fresh("A1-L02-problems", "2.4/2.9 problem set with worked solutions",
    "L02.html:324-427 (problem set; M1-M3 328-350, P1-P3 353-376, E1-E3 378-401, R1-R3 403-426)",
    "All twelve problems read at edbb7aa8 and re-derived: M1 Archimedean; M2 (-1)^n with eps=1; M3 G_3-G_1 = 3/8 <= 1/2; P1-P3 standard (P3 integer differences less than 1 vanish). "
    "E1 witness pair (N,2N); E2 H_4-H_2 = 7/12; E3 sum of 60-n = 1830; R1 Lemma 3.4 with 1/2^10; R2 H_{2^k} >= 1+k/2 by Proposition 3.3; R3 geometric decay, "
    "beta^N <= 1/(Nh) checked on 2000 random (h,N) (r4_l02_numbers.out). No defect."))
rows.append(fresh("A1-L02-quiz-keyresults", "2.9 quiz keys and key-results table",
    "L02.html:429-446 (key results), 448-536 (quiz)",
    "Quiz items keyed: L02q1 (Definition 2.1), L02q2 (Proposition 2.2), numeric H_2-H_1 = 0.5, L02q4 (1/n counterexample, Proposition 3.3), G_3 = 0.875, "
    "G_m-G_n = 1/2^n-1/2^m (Lemma 3.4), N = 10 (Proposition 3.5), sqrt(n) unbounded (Lemma 2.3), rational Cauchy limit (canon break 1), 1830 pairs, completeness "
    "axiom in Theorem 2.5. All keys and explanations checked against the page; the explanations do not cite the removed H2 item. Key-results rows are T and point to proofs on the page."))
rows.append(fresh("A1-lab-L02-1", "2.5 lab: run, twin, page equals twin, expected equals output (re-run at edbb7aa8)",
    "tests/labs/M5/lab-M5-L02-1.py; L02.html:211-294 (page code 214-285, expected 286-292)",
    "r4_run_labs_L02.out 'run_labs M5: PASS (1/1)' exit 0. Twin alone under python -I -W error: r4_twin_L02.exit 0, r4_twin_L02.err 0 bytes, r4_twin_L02.out equals the page's expected block "
    "(r4_lab_expected_vs_twin.out 'L02: expected==twin_stdout True | page code==twin file True'). Standard library only; exact Fraction sums; no randomness. Lab hypothesis (L02.html:213) "
    "numbers 200 of 200, the 1830 identities, the first index 10 and the failing indices 0 to 9 match the output; the lab's docstring claims (L02.html:216-221) match the code."))
rows.append(fresh("A1-L02-attribution", "2.1/2.4 attribution of the cited M1 result",
    "course/modules/M/M5/L02.html:540 (references paragraph); L02.html:300 (canon break 1 cites M1 Lesson 2 Corollary 2.6); L02.html:423 (R3 cites M1 Lesson 6 Theorem 2.2)",
    "M1 L02.html:132-133 states Corollary 2.6 (no rational number has square 2). M1 L06.html:90-93 defines S_n(q) and L06.html:97-99 states Theorem 2.2 for q != 1. "
    "The references paragraph says every theorem stated in this lesson is proved on the page, and that Theorem 2.2 is cited, not proved, in R3; R3 uses it with beta != 1 "
    "(hypothesis present at L02.html:421-423). Consistent. M1 byte-identical since 8196077d."))
# ---- L03 (byte-identical since 8196077d) ----
for rid in ["A1-L03-structure", "A1-L03-math", "A1-L03-numbers", "A1-L03-problems", "A1-L03-quiz-keyresults"]:
    rows.append(carry(rid, "L03.html"))
rows.append(fresh("A1-lab-L03-1", "2.5 lab",
    "tests/labs/M5/lab-M5-L03-1.py; L03.html:106-168",
    "r4_run_labs_L03.out 'run_labs M5: PASS (1/1)' exit 0. Twin alone: r4_twin_L03.exit 0, r4_twin_L03.err 0 bytes; r4_lab_expected_vs_twin.out True (expected block equals twin stdout; page code equals twin file). Exact Fraction arithmetic; no randomness."))
# ---- L04 ----
for rid in ["A1-L04-structure", "A1-L04-numbers", "A1-L04-problems", "A1-L04-quiz-keyresults"]:
    rows.append(carry(rid, "L04.html; the twin lab-M5-L04-1.py"))
rows.append(carry("A1-L04-math", "L04.html"))
rows[-1]["evidence"] += (" [Round-4 note: the mathematics of the source is unchanged and re-checked; the rendered text of the F6 proof, the open-set definition and the "
    "Proposition 2.1 proof is defective, see A1-L04-render-raw-less-than.]")
rows.append(fresh("A1-L04-render-raw-less-than", "2.9 learner-visible text: raw '<' parsed as a tag hides text (new this round; missed by round 3)",
    "course/modules/M/M5/L04.html:56 (F6 proof, '\\(c<c\\)'), :240 (open-ball and open-set definitions, '\\(d(x,y)<r\\)'), :249 (proof of Proposition 2.1, '\\(...<d(x,y)+s=r\\)')",
    "Each '<' followed by a letter is parsed as a start tag by the browser, so the tag swallows the text up to the next '>'. Evidence in Chromium (Playwright, file://, "
    "from the project venv): ledgers/M5/scripts/M5-a-r4/raw_lt_strings_r4.py -> r4_raw_lt_strings.out: 'and F3 gives' is in the source (line 56) and ABSENT from the rendered "
    "<main>; the source at line 240 reads 'is <em>open</em> when' and the probe phrase 'is open when' is ABSENT in the rendered text, the rendered text reads 'd(x,y)open when for each'; 'was arbitrary' "
    "is in the source (line 249) and ABSENT; the rendered text after 'By M3, d(x,z)<=d(x,y)+d(y,z)' jumps to 'Remark 2.2', so the conclusion of the Proposition 2.1 proof "
    "('so z in B(x,r). Hence B(y,s) subset B(x,r), and since y was arbitrary, B(x,r) is open') is not shown. Independent block-level probe "
    "ledgers/M5/scripts/M5-a-r4/block_text_probe_r4.py -> r4_block_text_probe.out: index 0 of 39 blocks missing, L01 0 of 104, L02 0 of 117, L03 0 of 94, "
    "L04 3 of 110 missing (exactly these three blocks). Scanner ledgers/M5/scripts/M5-a-r4/slice_scans_r4.py (r4_slice_scans.out) finds raw '<'+letter only at L04.html 56, 240 and 249 in the slice pages. "
    "The same defect is recorded as defect 1 in plans/M5-open-items.md (Builder F, lines 240 and 249) and is not fixed at edbb7aa8. check_pages and page_smoke PASS because neither checks rendered text.",
    status="FAIL",
    fix="Escape each '<' that is followed by a letter in these three math spans as '&lt;': L04.html:56 '\\(c<c\\)' becomes '\\(c&lt;c\\)'; L04.html:240 '\\(d(x,y)<r\\)' becomes '\\(d(x,y)&lt;r\\)'; "
        "L04.html:249 '\\(d(x,z)\\le d(x,y)+d(y,z)<d(x,y)+s=r\\)' becomes '...&lt;d(x,y)+s=r...'. No other edit. Then re-run raw_lt_strings_r4.py (every probe PRESENT) "
        "and block_text_probe_r4.py (0 missing) and the L04 gates."))
rows.append(fresh("A1-lab-L04-1", "2.5 lab",
    "tests/labs/M5/lab-M5-L04-1.py; L04.html:103-210",
    "r4_run_labs_L04.out 'run_labs M5: PASS (1/1)' exit 0. Twin alone: r4_twin_L04.exit 0, r4_twin_L04.err 0 bytes; r4_twin_L04.out prints Part C 'squared_triangle_failures 2' and 'd(0,2) 4 d(0,1)+d(1,2) 2' as the page's expected block (r4_lab_expected_vs_twin.out True). Standard library only; enumerated samples; no randomness."))
# ---- cards ----
rows.append(carry("A1-cards-L01", "cards.json objects M5-c001..c016, c191, c216 (card_delta_r4.py: only c063, c160, c161 changed in the file, all outside L01)"))
rows.append(fresh("A1-cards-L02", "2.7 cards for L02 (all 21 read; re-verified after round-3 FAIL on card M5-c026)",
    "course/modules/M/M5/cards.json: M5-c017..c034, c213, c214, c217 (c026 object at line 185)",
    "Card M5-c026 (line 185) now states the Proposition 3.3 hypothesis as H_n = sum of 1/k for k=1..n, n>=1, and the conclusion H_{2N}-H_N >= 1/2 so the series diverges; "
    "this matches the lesson's Proposition 3.3 (L02.html:172-175), which lists only (H1). The round-3 FAIL is fixed. Every other L02 card read against the page at edbb7aa8: "
    "c017/c019 (Definitions 1.1 and 2.1), c018 (Proposition 1.2), c020 (Proposition 2.2), c021 (Lemma 2.3), c022 (Lemma 2.4, hypotheses match L02.html:113-118), "
    "c023 (Theorem 2.5, hypotheses match L02.html:128-131), c024 (Definition 3.1), c025 (Corollary 3.2, hypotheses match L02.html:158-161), c027 (Lemma 3.4, match "
    "L02.html:185-188), c028 (Proposition 3.5, match L02.html:199-202), c029 (misconception 1), c030 (misconception 2), c031 (canon break 1), c032/c033/c034/c217 graded C "
    "with basis naming Lab 1 (values in L02.html:286-292), c213/c214 (bounded, bounded below; match Section 2). Card-to-page locators on c029 and c031 unchanged in meaning."))
rows.append(carry("A1-cards-L03", "cards.json objects M5-c035..c049, c218, c219 (not changed in the round-3 to round-4 delta)"))
rows.append(fresh("A1-cards-L04", "2.7 cards for L04 (25 read; c063 re-verified after the round-3 delta)",
    "course/modules/M/M5/cards.json: M5-c050..c068, c190, c192, c193, c201, c215, c220; changed card M5-c063 at lines 455-460",
    "Changed card M5-c063 now reads 'No. The triangle inequality (M3) is an extra requirement that M1 and M2 do not imply (Misconception 1).' This is consistent with "
    "L04.html:334 (misconception 1, the squared distance (x-y)^2 is symmetric and vanishes only on the diagonal but fails M3) and with the counterexample at L04.html:325 "
    "(q(0,2)=4 > q(0,1)+q(1,2)=2). Other L04 cards are byte-identical objects since 8196077d (card_delta_r4.py) and were checked in round 3 (c056 Proposition 1.7 hypotheses match "
    "L04.html:223 hypothesis (4)); their rows carry the round-3 evidence."))
rows.append(fresh("A1-cards-duplicates", "2.7 full scan for duplicates",
    "course/modules/M/M5/cards.json (235 cards, all lessons)",
    "ledgers/M5/scripts/M5-a-r4/cards_dup_scan_r4.py -> r4_cards_dup_scan.out: 235 cards; 0 duplicate ids; 0 duplicate fronts; 0 duplicate backs (case-folded). "
    "Keys used: back, basis, front, grade, id, lesson. Per lesson L01 18, L02 21, L03 17, L04 25 (slice a 81 cards). Grades T 109, C 54, absent 72. "
    "Delta from round 3: removed M5-c184 (L10) and M5-c205 (L08), added M5-c241 (L07), so the total is 236 - 2 + 1 = 235."))
rows.append(fresh("A1-dag-concepts", "2.9 DAG and concept use",
    "check_dag M5; L01.html:59, L02.html:81 and :37, L03.html:59, L04.html:39; index.html:62-64",
    "r4_check_dag_M5.out 'check_dag M5: PASS' exit 0. The round-4 changes in L02 add no concept use: Proposition 2.2, Lemma 2.3, Theorem 2.5 and Corollary 3.2 are "
    "lesson-internal results; no new term link. Concept uses in slice a unchanged from round 3 (limit, derivative, definite-integral, discount-factor, geometric-series "
    "from M1, M2 and P0.1 closure; cauchy-sequence, completeness-of-reals, epsilon-delta-continuity, metric-space defined in L02, L01, L03, L04). No bellman-equation, "
    "principle-of-optimality, dynamic-programming, expected-utility, crra-utility or utility-maximization appears in slice a (grep, r4_slice_scans.out)."))
rows.append(fresh("A1-notation", "3.1 notation registry (NOTATION)",
    "notation/notation.json; L01-L04.html; index.html",
    "notation.json (unchanged since 8196077d) registers symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} and macros including \\R and \\N. "
    "r4_slice_scans.out: no math span in index or L01-L04 contains \\Phi, \\gamma_3, \\gamma_4, \\ast, R_f, \\mathbb{Q}, \\Q or a bare T. Macros used in slice a: \\R (104) and \\N (30) "
    "(registered), plus built-ins. Locally defined letters (S, S_N, H_n, G_N, C, B, D, L, K, ell-infinity, d_infinity, B(x,r), psi, phi, kappa) each defined at its point of use "
    "(L02.html:79-143 and 297-300 for S and the local letters; L02.html:300 uses 'the set S of Lesson 1'). No registered meaning is reused."))
rows.append(fresh("A1-banned-phrases", "2.9 banned phrases (BUILDER_RULES 1.3-1.4)",
    "index.html; L01-L04.html; cards.json",
    "r4_slice_scans.out: no banned string (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, "
    "studies show, experts agree, it is well known, obviously, clearly, it can be shown, of course, note that, we will, in this section, verifier, builder, round N, draft, "
    "placeholder) in the five pages or in any card. Ellipses appear only in code (outside the rendered prose); no ellipsis stands for omitted content in prose."))
rows.append(fresh("A1-scope-words", "2.2/2.4 scope words (only, all, every, always, exactly, same)",
    "index.html; L01-L04.html; L02.html changed sentences 146, 170-181, 311",
    "Scope words in the changed L02 text were read: 'does not use (H2)' (Proposition 3.3, 174-176 and Remark 2.6) is a negative claim proved in the proof at line 180; "
    "'every integer N >= 1' (Proposition 3.3) is proved for all N; 'every theorem stated in this lesson is proved on the page' (L02.html:540) holds for Lemma 2.3, 2.4, Theorem 2.5, "
    "Corollary 3.2, Proposition 3.3, Lemma 3.4 and Proposition 3.5. 'all 200 of 200' and 'all 1830 pairs' (Lab 1) are computed (r4_twin_L02.out). Other scope words in the "
    "slice were read in round 3 on byte-identical pages and are carried in their rows."))
rows.append(fresh("A1-figures", "2.8 figures",
    "index.html; L01-L04.html",
    "r4_slice_scans.out: svg count 0 in index, L01, L02, L03, L04. No figure in the slice; module-level figure rules do not apply."))
# ---- gates (all re-run at edbb7aa8; see gates_r4.sh and r4_* outputs) ----
rows.append(fresh("A1-gate-check-pages", "2.9 gate: check_pages", "tools/check_pages.py --unit M5",
    "r4_check_pages_M5.out: 'check_pages M5: PASS', exit 0."))
rows.append(fresh("A1-gate-check-dag", "2.9 gate: check_dag", "tools/check_dag.py --unit M5",
    "r4_check_dag_M5.out: 'check_dag M5: PASS', exit 0."))
rows.append(fresh("A1-gate-check-projects", "2.6 gate: check_projects (project outside this slice; gate only)", "tools/check_projects.py --unit M5",
    "r4_check_projects_M5.out: 'check_projects M5: PASS', exit 0. The project and grader were not read by this slice; run_graders was not run for slice a."))
rows.append(fresh("A1-gate-run-labs", "2.5 gate: run_labs for hub and L01-L04", "tools/run_labs.py --unit M5 --page index|L01|L02|L03|L04",
    "r4_run_labs_index.out 'PASS (0/0)'; r4_run_labs_L01..L04.out 'PASS (1/1)' each; all exit 0."))
rows.append(fresh("A1-gate-page-smoke", "2.5/2.9 gate: page_smoke for hub and L01-L04 (alone)", "tools/page_smoke.py --unit M5 --pages index L01 L02 L03 L04",
    "r4_page_smoke_M5_a.out: 'page_smoke M5: PASS', exit 0; PASS for each of the five pages; lab runtimes 0.0 to 1.6 s. This gate does not detect hidden text (see A1-L04-render-raw-less-than)."))
rows.append(fresh("A1-gate-ruff-mypy-twins", "2.5 gate: ruff, mypy strict, twins", ".venv/bin/ruff check .; .venv/bin/ruff format --check .; mypy --no-incremental; python -I -W error on each twin",
    "r4_ruff_check.out 'All checks passed!' exit 0; r4_ruff_format.out '553 files already formatted' exit 0; r4_mypy.out 'Success: no issues found in 385 source files' exit 0; "
    "twins L01-L04 alone: r4_twin_L0k.exit 0, .err 0 bytes."))
rows.append(fresh("A1-gate-pytest", "2.5 gate: relevant pytest", "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -q",
    "r4_pytest_M5_relevant.out: 190 progress dots over three lines (72, 72, 46), exit 0. Full suite not run (no tool or test changed in the delta; slice a touches only lab and page tooling)."))
rows.append(fresh("A1-gate-verify-refs", "2.1 gate: verify_refs", "tools/verify_refs.py --offline; tools/verify_refs.py --unit M5",
    "r4_verify_refs_offline_all.out 'offline integrity: 560 entries, 0 problems'; r4_verify_refs_M5_live.out 'live re-verification of M5: 2 of 560 entries, 0 problems'. Both exit 0."))
rows.append(fresh("A1-gate-build-site", "2.9 gate: build_site --check", "tools/build_site.py --check",
    "r4_build_site_check.out 'site data current: 6 outputs', exit 0."))
rows.append(fresh("A1-gate-render-curriculum", "3.1 gate: render_curriculum and diff", "tools/render_curriculum.py; git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json",
    "r4_render_curriculum.out: 'curriculum valid: 25 parts, 134 modules, 157 projects, 13,715 h (6.35 FTE years)' and 'wrote ... CURRICULUM.md'; r4_render_curriculum_diff.out exit 0 (no change to the tracked files)."))

ids = [r["id"] for r in rows]
missing = [i for i in prev if i not in ids]
assert not missing, missing
frag = {
    "unit": "M5",
    "slice": "a",
    "round": 4,
    "verifier": "Haiku independent verifier, M5 slice a round 4 (did not build M5)",
    "pin": "edbb7aa8de20e6d2f3035c463a79a318c22623c4",
    "base": "8196077d5f56c3919d33e69888176d197d378ad4 (round-3 pin); delta by git diff 8196077d edbb7aa8",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS4-M5-a",
    "scratch": "ledgers/M5/scripts/M5-a-r4/ (scripts and outputs, repo paths); /tmp/m5a_r4_scratch",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta 8196077d..edbb7aa8 for slice a: course/modules/M/M5/L02.html (Remark 2.6 line 146; Proposition 3.3 hypothesis list and proof 170-181; misconception 1 line 311) and course/modules/M/M5/cards.json (M5-c063 back text, lines 455-460). index.html, L01.html, L03.html, L04.html, tests/labs/M5/lab-M5-L01-1.py..L04-1.py, tools/, notation/, references/, curriculum/ are byte-identical (git diff --quiet). Outside slice a and not read: L05-L10 pages (block titles only), project.html and grader, cards M5-c160, c161, c184, c205, c241.",
        "Round-3 FAIL A1-L02-math is fixed: Proposition 3.3 drops (H2), the proof now uses only convergent implies Cauchy. Re-verified PASS.",
        "Round-3 FAIL A1-cards-L02 is fixed: card M5-c026 matches the lesson. Re-verified PASS.",
        "New FAIL A1-L04-render-raw-less-than: three raw '<' in L04.html hide text in the browser; missed by rounds 1-3 and by page_smoke. It is a learner-visible loss of a definition sentence and of the conclusion of the Proposition 2.1 proof, so it is not a LOW presentation row under ruling 26; the orchestrator should treat it as blocking unless it decides otherwise.",
        "Carried rows (PASS, subject byte-identical) keep the round-3 evidence with the prefix 'Carried from round 3'; every row id of the round-3 fragment is kept.",
        "The file ledgers/M5/M5-a.json held an earlier fragment (round 10, pin e8b10b8) from another lineage; this round overwrote it at the path given in the task.",
        "Slice a has no grader and no project, so there are no mutants; mutation testing (VERIFIER_RULES 2.6) does not apply.",
        "Could not check: Abbott and Rudin (not opened, no locator asserted); L05-L10 mathematics (outside the slice; block titles only); the full pytest suite; run_graders for M5 (project slice); visual pixel comparison (page_smoke only; no figure in the slice); the rendering of Chromium on other browsers; the lost-text probe for math-adjacent sentences beyond the block-level check.",
    ],
    "summary": "Round 4, slice a (hub, L01-L04 pages, lab twins, slice cards). {} rows: {} PASS, {} FAIL. FAIL 1 (A1-L04-render-raw-less-than, presentation of hidden text at L04.html:56, :240, :249; fix: escape three '<' as '&lt;'). Round-3 FAILs A1-L02-math and A1-cards-L02 are fixed and re-verified PASS. All gates re-run at edbb7aa8 PASS (check_pages, check_dag, check_projects, run_labs, twins, page_smoke, ruff, mypy, relevant pytest, verify_refs, build_site, render_curriculum diff).",
}
n = len(rows); npass = sum(r["status"] == "PASS" for r in rows); nfail = n - npass
frag["summary"] = frag["summary"].format(n, npass, nfail)
json.dump(frag, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
open(OUT, "a", encoding="utf-8").write("\n")
print("rows", n, "pass", npass, "fail", nfail)
