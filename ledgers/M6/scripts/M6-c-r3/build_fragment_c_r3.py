import json
from datetime import UTC, datetime

P = "PASS"
F = "FAIL"
ROOT = "/Users/billyribeiro/.fanout/wt/verifyC3-M6-c"
rows = []

def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix
    rows.append(r)

# ---- commands and structure
row("c-cmd-run-labs", "run_labs for M6 (all 15 labs; slice labs L09-L12 included)", "tests/labs/M6/lab-M6-L09-1.py .. lab-M6-L12-1.py",
    P, "`.venv/bin/python tools/run_labs.py --unit M6` printed `run_labs M6: PASS (15/15)`, exit 0.")
row("c-cmd-twins-alone", "each slice twin run alone as python -I -W error", "tests/labs/M6/lab-M6-L09-1.py .. L12-1.py",
    P, "Four runs exit 0, empty stderr. Script ledgers/M6/scripts/M6-c-r3/compare_labs.py: page lab code == twin (True x4); page expected block == twin output (True x4).")
row("c-cmd-check-pages", "check_pages (unit M6, includes L09-L12 static rules, word counts, banned strings, section order)",
    "course/modules/M/M6/L09.html .. L12.html", P, "`tools/check_pages.py --unit M6` -> `check_pages M6: PASS`.")
row("c-cmd-page-smoke", "page_smoke for the four slice pages alone (light/dark, 360 px, console, KaTeX, lab run)",
    "course/modules/M/M6/L09.html .. L12.html", P, "`tools/page_smoke.py --unit M6 --pages L09 L10 L11 L12` -> PASS for each page and `page_smoke M6: PASS`, exit 0.")
row("c-cmd-check-dag", "check_dag (prerequisite closure and concept links)", "course/modules/M/M6/*.html",
    P, "`tools/check_dag.py --all` -> `check_dag M6: PASS`. cauchy-sequence and completeness-of-reals are defined in M5 (curriculum/01-foundations.yaml:239-240), inside the M6 closure; expectation is M4.")
row("c-cmd-ruff-mypy-pytest", "ruff, mypy strict, lab pytest for the slice twins", "tests/labs/M6/lab-M6-L09-1.py .. L12-1.py",
    P, "`ruff check tests/labs/M6` All checks passed; `ruff format --check` 15 files formatted; `mypy --no-incremental` on the four twins: no issues; `pytest tests/test_labs.py -k M6`: 15 passed.")
row("c-cmd-verify-refs", "verify_refs --offline (slice cites no registry key; registry integrity)", "references/references.json",
    P, "`tools/verify_refs.py --offline` -> `offline integrity: 560 entries, 0 problems`. The four pages state 'This lesson cites no outside source' and contain no data-key citation.")
row("c-structure-sections", "lesson section order, minimum counts (3 misconceptions, 3 problems x 4 tiers with solutions, quiz 8-15, key-results, references), 9 h",
    "course/modules/M/M6/L09.html .. L12.html", P,
    "Counted by hand: each page has 3 misconceptions; 3 problems in each of mechanics/proof/empirical/research, each with details.solution; quiz items L09=9, L10=9, L11=10, L12=9; data-hours=9 on each page; check_pages passes.")
row("c-why-words", "why-it-matters <= 120 words and no banned strings or process words", "why-it-matters paragraph of each page",
    P, "check_pages PASS (word limit and banned strings). grep for round/builder/verifier/REQUESTS/TODO/planning words in the four pages and twins: no hits. Ellipses appear only inside code blocks.")
row("c-notation", "notation: every symbol vs notation/notation.json (no collision)", "L09-L12 prose and math",
    P, "Registry macros used: \\E, \\Prob, \\indic (all registered). Registered symbols R^\\ast, \\gamma_3/4, \\Phi, \\mathbb{Q}, T (number of observations) do not occur in the slice. L12 uses L^\\ast, not R^\\ast; no collision.")
row("c-cards-L09", "cards M6-c085..c093 agree with current L09 text, carry hypotheses, numbers appear in the lesson",
    "course/modules/M/M6/cards.json", P,
    "Each card checked against Definition 9.1, Prop 9.5 (3 assumptions), Prop 9.6, Lemma 9.7, Problem R2, the 186/256 and 0.7265625 values (Part A), look-ahead failure k=0..7, and the 2m+1 example (recomputed: tau = 1,3,5,7 for m=0..3).")
row("c-cards-L10", "cards M6-c094..c105 agree with current L10 text and numbers", "course/modules/M/M6/cards.json", P,
    "Definition 10.1, Lemma 10.2, Theorem 10.3, Definition 10.5, Lemma 10.6, Prop 10.7 (K=1000: m=9, 0.9980468750, 0.0019531250, 1001, 489), Prop 10.9 and misconceptions 1-3 all agree with the page (values recomputed).")
row("c-cards-L11", "cards M6-c106..c113 agree with current L11 text and numbers", "course/modules/M/M6/cards.json", P,
    "Definition 11.1, Lemma 11.2 hypotheses, Theorem 11.3 assumptions, Corollary 11.4, signed-walk values 1/2 and 0 (recomputed), attained ratio 1.000000 at N=1,2,4 (recomputed exactly) all agree.")
row("c-cards-L12-c114", "card M6-c114 lists the hypotheses of Lemma 12.1 (carry the proposition's hypotheses)", "course/modules/M/M6/cards.json id M6-c114; L12.html Lemma 12.1 assumptions (lines 60-64)", F,
    "Card lists three assumptions and says 'The first identity uses the orthogonality of increments stated in Section 1'. That orthogonality is not an assumption on the page and is attributed to L07, which is stated for finite Omega only (L07.html line 56 'Let Omega be finite', line 135 'The finite proof does not cover that case').",
    "Add the general orthogonality of a square-integrable martingale's increments as a numbered Assumption (not proved here, no grade) in Lemma 12.1 and in this card; see row c-L12-orthogonality-general.")
row("c-cards-L12-others", "cards M6-c115..c124 and c128 agree with L12 text and numbers", "course/modules/M/M6/cards.json", P,
    "Lemma 12.3, Theorem 12.4, Result 12.6 (not graded), Prop 12.8 (1/(12*4^n), 2^-(n+1)), Example 12.9 / Prop 12.10, and the 1/2048 and 1/12582912 values (recomputed) agree. Card ids c109, c125-c127 are absent; no lesson text is affected.")
row("c-cards-dup", "no duplicate cards for L09-L12", "course/modules/M/M6/cards.json", P,
    "Card questions for L09-L12 are distinct (checked by reading all 40 slice cards).")

# ---- labs: claims about printed output
row("c-lab-L09-claims", "L09 lab: each sentence about what the lab prints/checks matches code and output",
    "course/modules/M/M6/L09.html lines 101, 223; tests/labs/M6/lab-M6-L09-1.py",
    P, "depends_on_first flags (known_by_first_k) and hitting_time_is_stopping_time print True; lookahead_failing_k [0..7] printed (recomputed independently); Part C sum_equals_P_tau_at_most_N True. Interpretation text (k=8 pass, 0.7265625) matches.")
row("c-lab-L10-claims-partB", "L10 Part B hypothesis: 'the lab checks this (stopped expectation 0) for n in {1,2,3,5,10}'",
    "course/modules/M/M6/L10.html line 171 (hypothesis); tests/labs/M6/lab-M6-L10-1.py part_b() lines 250-273",
    F, "part_b() prints expected_stopped_value but has no equality flag or assertion on it. Only win_part_is_one_minus_2_to_minus_n is a flag. Mutant ledgers/M6/mutants/M6-c-r3/m_c_L10_wins_pay_zero.py prints expected_stopped_value -1/2, -1, -3/2, -5/2, -5 and exits 0; ledgers/M6/mutants/M6-c-r3/m_c_L10_no_stop_on_win.py prints -1,-3,-7,-31,-1023 and exits 0. The zero mean is printed, not checked.",
    "Reword line 171 to 'the lab prints this expectation for each n' (or add an equality flag such as expected_stopped_is_zero to part_b, and update the page code and expected block with tools/embed_labs.py).")
row("c-lab-L10-claims-partA", "L10 Part A: 'equals_start', 'ruin_is_one_over_2_to_bets' flags match the sentences that cite them", "course/modules/M/M6/L10.html lines 171, 300, 390-398",
    P, "Printed flags True for all five capitals; numbers recomputed from the closed forms (m, 2^-m, K+1, K+1-2^m, expectation K) for K=1,6,10,100,1000 all agree.")
row("c-lab-L11-claims", "L11 lab: hypothesis and interpretation claims (Part A all_bounds_hold, Part B atoms, Part C bound_holds) match code and output",
    "course/modules/M/M6/L11.html lines 130, 254, 260-263", P,
    "all_bounds_hold True for N=1..12 (recomputed exact ratio and bounds agree); Part B atoms_checked 4095 = 2^12-1 (code loops k in range(12)); Part C bound_holds False for N=1,2 (recomputed).")
row("c-lab-L12-claims", "L12 lab: Part A flags and Part B flags match the sentences that cite them", "course/modules/M/M6/L12.html lines 183, 307",
    P, "Part A formula_matches, E_M_squared_matches_one_third_minus, equals_half_over_2_to_n True for n=0..10 (recomputed); Part B one_step_martingale_on_every_atom True, E_M_n 1, P 2^-n for n=0..10 (recomputed).")

# ---- numbers in prose
row("c-num-L09", "L09 numbers in prose: 1/2, 1/8, 5/8, 70/256, 0.7265625, 0.625, 0.125", "L09.html M1 (line 295), E1 (345), E2 (352), quiz (419, 442, 465)",
    P, "Recomputed: P(tau=1)=1/2, P(tau=3)=1/8, P(tau<=2)=1/2, P(tau<=3)=5/8, P(tau<=8)=93/128=0.7265625, 256-186=70 (70/256=0.2734375 exact). All rounding-free.")
row("c-num-L10", "L10 numbers: K=1000 (m=9, 1/512 = 0.001953125 with ten-place 0.0019531250, 1001, 489, 0.9980468750); K=6 (7, 3, 6); K=10 (3, 3); K=100 (6, 37); E1 decimal reasoning", "L10.html lines 298-300, 318, 341, 348, 391",
    P, "Recomputed closed forms; 0.001953125 has nine decimals so ten-place display is exact; 1-1/512=0.998046875 displayed as 0.9980468750 exact.")
row("c-num-L11-E2-rounding", "L11 E2: '=2343/2772=0.845238' written with equality to a rounded decimal, rounding not stated",
    "course/modules/M/M6/L11.html line 352 (E2 solution); also line 254 interpretation '0.845238'",
    F, "2343/2772 = 0.84523809... (recomputed). The page writes an equality with the six-place printed value and does not say the value is rounded. Other values on the same page are exact (693/768=231/256=0.90234375; 781/1024=0.7626953125 exact).",
    "Write '2343/2772 = 0.8452380952... (printed as 0.845238, rounded to six places, as the lab prints)' or use '\\approx'; state the rounding as the plan's precedent requires.")
row("c-num-L11-other", "L11 numbers: N=1,2,4 ratios 1; N=3 2/3; E|S_12|=693/256; 781/1024; E|S_2|=1; P(max|S_k|>=2)=1/2 for N=3; 4095", "L11.html lines 239-255, 295, 302, 343-358, quiz",
    P, "Recomputed exact ratios for N=1..12 (N=12 maximum 71/84 = 0.845238 at lambda=3); E|S_12|=693/256; M2 event = {X1=X2} gives 1/2 and E|S_3|=3/2 (bound 3/4 at lambda=2).")
row("c-num-L11-signed", "L11 Part C values 1/2 and 0 (N=1,2) and 'bound fails'", "L11.html lines 252-253, 276, 357-359", P, "Recomputed: P(max S_k >= 1)=1/2 and E[S_N]=0 for N=1,2; 1/2 <= 0 false.")
row("c-num-L12", "L12 numbers: 1/(12*4^n), 1/3-1/(12*4^n), 2^-(n+1), 1/2048, 1/12582912, 4097 grid points, 21/64, 1/192 (0.00520833 to eight places), 1/8, 2^-n", "L12.html lines 149-158, 183, 283-307, 344-355, quiz",
    P, "Recomputed for n=0..10 with independent script ledgers/M6/scripts/M6-c-r3/recompute_l12_grid.py (largest grid error 2^-(n+1) at all n; E[M_n^2] identity true for all n; E error = 1/(12*4^n) true for all n). 1/192 = 0.005208333..., so 0.00520833 is correct to eight places.")
row("c-num-L12-E1", "L12 E1 and E2 solutions: 4^10 = 1048576, 12*4^10 = 12582912, grid j/4096 contains endpoints since 4096/1024 = 4", "L12.html lines 398-405", P, "Arithmetic re-derived; endpoint error 2^-11 attained on the grid.")

# ---- mathematics
row("c-math-L09", "L09 Prop 9.5, Prop 9.6, Lemma 9.7, Remark 9.2, Ex 9.3, misconceptions, canon-break 2 and 3, problems P1-P3, R1-R3",
    "L09.html lines 58-96, 228-256, 258-283, 285-387", P,
    "Re-derived each proof; assumptions complete; Remark 9.2 equivalence holds (Lemma 9.7 gives the converse); trivial-filtration counterexample {tau<=1}={X1=1} correct; R2 constant-time proof correct; 2m+1 example correct.")
row("c-math-L10", "L10 Lemma 10.2, Thm 10.3, Remark 10.4, Lemma 10.6, Prop 10.7, Ex 10.8, Prop 10.9 (a)-(c), problems P1-P3, R1-R3",
    "L10.html lines 63-167, 306-326, 414-430", P,
    "Telescoping identity and integrability re-derived; affordability threshold 2^k <= K+1 and tau = min(w,m) re-derived; wealth after win K+1 and after ruin K+1-2^m; expectation (1-2^-m)(K+1)+2^-m(K+1-2^m)=K; Prop 10.9 proof steps (a),(b),(c) valid; R1 counterexample valid.")
row("c-math-L11", "L11 Lemma 11.2, Thm 11.3 (Steps 1-3), Cor 11.4, M2, P1-P3, R1-R3",
    "L11.html lines 63-126, 285-387", P,
    "Identity max(1,|s|) = (|s+1|+|s-1|)/2 re-derived; Doob chain Step 1-3 valid (nonnegativity used only in Step 3); R3 second-moment bound valid (E[S_N^2]=N); R1 constant 1 optimal.")
row("c-math-L12-orthogonality-general", "L12 orthogonality of increments on a general probability space (Section 1 claim; Lemma 12.1 (T); Lemma 12.3 (T); Theorem 12.4 (T) steps)",
    "L12.html line 56 (Section 1 'orthogonal projection (L07)'), lines 58-66 Lemma 12.1, lines 92 Lemma 12.3 proof, line 110-112 Theorem 12.4 Step 1; L07.html lines 52, 56, 135", F,
    "The statement is true, but its only cited source L07 is stated and proved for a finite Omega with a partition-generated sigma-algebra (L07.html line 52 'This lesson defines it on a finite probability space'; line 135 'On a general space ... the finite proof does not cover that case'; the general definition is Assumption CE). L12 applies the property on a general (Omega, F, P) (Theorem 12.4 assumption 1). The step is therefore an unproved fact cited as T, which the plan's Architect default forbids (infinite-sample-space results without a proof are numbered Assumptions, no grade).",
    "Make the orthogonality of a square-integrable martingale's increments (E[Y(M_n-M_m)]=0 for F_m-measurable square-integrable Y) a numbered Assumption, 'not proved here', with no grade, and list it in the assumptions of Lemma 12.1, Lemma 12.3 and Theorem 12.4; or prove it from L07 Assumption CE with the approximation step written out. Then re-grade Lemma 12.1/12.3/Theorem 12.4 accordingly.")
row("c-math-L12-prop12.8b", "L12 Prop 12.8(b) proof: orthogonality on [0,1] cited to 'the L07 orthogonality'",
    "L12.html line 155", F,
    "Prop 12.8 is on [0,1] with the length measure. The cited L07 result is for finite Omega (L07.html line 52, 56). The step E[(Y-M_n)M_n]=0 is not shown. The identity itself is true: E[(Y-M_n)M_n] = sum over cells of c*int_cell (x-c)dx = 0 (recomputed), so this is a citation gap, not a false claim.",
    "Show the one-line computation sum_cells c * int_cell (x - c) dx = 0 in the proof of (b), or state the orthogonality as the numbered Assumption from row c-math-L12-orthogonality-general.")
row("c-math-L12-prop12.8ac-prop12.10", "L12 Prop 12.8(a),(c), Example 12.7 martingale property, Prop 12.10, Result 12.6 (ungraded), Thm 12.4 Steps 2-3",
    "L12.html lines 138-179, 81-119, 134", P,
    "Cell integral h^3/12 re-derived; midpoints c +- h/4 re-derived; |M_n(x)-x| <= 2^-(n+1) valid; all-heads probability bound and a.s. limit valid; Theorem 12.4 Steps 2-3 (continuity from below, countable union, 1/(2j) scale) valid given Lemma 12.1; Result 12.6 is labelled not proved and ungraded.")
row("c-math-L12-R-problems", "L12 problems M1-M3, P1-P3, R1-R3 (solutions re-derived)", "L12.html lines 344-439", P,
    "M1 1/48, M2 21/64, M3 1/8 and E=1; P2 cell identity ch; P3 Cauchy argument; R1 endpoint attainment; R2 biased coin p^-n martingale (checked); R3 second-moment role (qualitative, consistent).")

# ---- prose defects
row("c-defn-before-use", "define before use: no plain-words definition of a concept precedes its <dfn> (plan 2.1 rule 5)",
    "L09.html line 52 (why-it-matters 'A stopping time is a random time ...') before dfn at line 60; L10.html line 52 ('The doubling strategy is the classic attempt ...') before dfn at line 108; L11.html line 52 ('Doob's maximal inequality bounds the chance ...') before dfn at line 87",
    F, "The why-it-matters paragraphs give the concept's meaning in plain words before the <dfn data-concept> sentence. The plan says each concept is defined 'never before it'. Checked by reading each page top to bottom.",
    "Rewrite the three why-it-matters sentences to name the concept without defining it (e.g. 'Lesson L09 defines the stopping time') or move the definition into the why-it-matters with the dfn.")
row("c-process-words-and-scope", "no process words; scope words (every, all, always, any, almost surely) backed by computation",
    "L09-L12 prose", P, "grep for process words: none. Scope claims checked: 'every path of an 8-step walk' (lab enumerates 256), 'every atom' (L11 Part B, L12 Part B), 'almost surely' only where Prop 10.9(a), Prop 12.10 or Result 12.6 (ungraded) supply it.")
row("c-dag-links", "no link or dfn to a concept outside the prerequisite closure", "L09-L12 meta rows and links", P,
    "Links used: sigma-algebra, probability-space (L01/L02), filtration, martingale, conditional-expectation-l2, doob-maximal-inequality, stopping-time (M6 earlier lessons), expectation (M4), cauchy-sequence and completeness-of-reals (M5, in closure). check_dag PASS.")
row("c-attribution", "no bibliographic data or locator typed from memory; L08 and L07 citations read", "L09 line 55, L10 line 56, L11 line 56, L12 line 56", P,
    "The slice cites L08 Definition 1.1 (filtration with adaptedness inside; read at L08.html line 59-60) and Definition 2.2 (martingale; read at L08.html line 88-89), L09 Definition 9.1, L07 conditional expectation (read at L07.html line 79), L02 continuity from below (read at L02.html line 83). L08 is finite-horizon with finite Omega, which the L10 sentence on integrability relies on (L08.html line 56). No outside source is cited.")
row("c-quiz-explain", "quiz answers and explanations agree with the lesson (9-10 items each)", "L09.html 405-478, L10.html 451-521, L11.html 404-478, L12.html 459-528", P,
    "Checked each correct option and explanation: Definition 9.1, Example 9.3, Problem R2, M1 value 1/8; Theorem 10.3 hypothesis tau<=N; 489, 1000, 0; Theorem 11.3 tail probability; Step 3 for nonnegativity; L12 Result 12.6 ungraded. Numeric data-answers match recomputed values.")
row("c-ddg-grades", "evidence grades: T for proved claims; lab output carries no grade; Result 12.6 ungraded", "key-results tables and references of L09-L12", P,
    "Key-results rows are T only where the page proves them; references paragraphs state lab output carries no grade. The T grade on Lemma 12.1/12.3/Thm 12.4 is affected by row c-math-L12-orthogonality-general.")
row("c-hours", "hours arithmetic for the slice (9 h per lesson)", "data-hours on L09-L12", P, "Each page has data-hours=9 and 'N study hours' = 9; plan §3 lesson hours 9 each.")

mutants = [
    {"id": "m_c_L10_wins_pay_zero", "description": "L10 part_b: win branch returns net (wins pay 0). Mutant file ledgers/M6/mutants/M6-c-r3/m_c_L10_wins_pay_zero.py.",
     "killed_by": "printed flag win_part_is_one_minus_2_to_minus_n False only; exit code 0; no check on expected_stopped_value (see row c-lab-L10-claims-partB)"},
    {"id": "m_c_L10_no_stop_on_win", "description": "L10 run_unlimited: a win never stops the strategy. Mutant file ledgers/M6/mutants/M6-c-r3/m_c_L10_no_stop_on_win.py.",
     "killed_by": "printed flag win_part_is_one_minus_2_to_minus_n False only; exit code 0; expected_stopped_value -1, -3, -7, -31, -1023 printed unchecked"},
]

frag = {
    "unit": "M6",
    "slice": "c",
    "round": 3,
    "verifier": "Claude Haiku 5.5, independent verifier for M6-c, round 3 (did not build M6; no shared context with the builders)",
    "pin": "ccfdf4c18f5ae9d86e6fe1ca9141382fd6055f83",
    "base": "unknown: the round-2 fragment /Users/billyribeiro/.fanout/frags/C-M6-c.round2.json does not exist; every row was re-derived from scratch rather than carried",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyC3-M6-c",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyC3-M6-c/ledgers/M6/scripts/M6-c-r3/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Scope: course/modules/M/M6/L09.html, L10.html, L11.html, L12.html; cards.json entries for those lessons; tests/labs/M6/lab-M6-L09-1.py .. lab-M6-L12-1.py.",
        "Lab twins are demonstrations; mutation grading was applied only as evidence for the lab-claim row (ruling).",
        "Card id gaps: M6-c109, M6-c125, M6-c126, M6-c127 are absent from cards.json. Not a row failure; reported for the builder.",
        "Not checked: L07, L08 and L02 pages beyond the cited anchors (read only as cited); the hub and project pages; the grader; check_projects/run_graders (project slice); mutation of project graders (not applicable to lab twins).",
        "Not checked: verify_refs per unit (the slice cites no registry key); Crossref or live access (not needed; offline integrity only).",
        "Previous round fragment was absent, so no PASS row was carried; all rows were re-derived.",
    ],
    "summary": "",
}
frag["summary"] = (
    f"{sum(1 for r in rows if r['status']=='PASS')} PASS, {sum(1 for r in rows if r['status']!='PASS')} non-PASS "
    f"of {len(rows)} rows; 2 mutants, both printed-flag-only (exit 0)."
)
out = f"{ROOT}/ledgers/M6/M6-c.json"
with open(out, "w", encoding="utf-8") as fh:
    json.dump(frag, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("wrote", out, len(rows), "rows")
