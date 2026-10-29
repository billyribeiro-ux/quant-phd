import json, datetime
P = "PASS"; F = "FAIL"
rows = []
def r(id_, check, location, status, evidence, fix=None):
    row = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        row["fix"] = fix
    rows.append(row)

# ---- commands (2.9 / 2.5 / 2.1) ----
r("M2-a-cmd-pin", "2.9-structure", "repository HEAD; course/modules/M/M2/{index,L01-L06}.html; tests/labs/M2/lab-M2-L01..06-1.py", P,
  "git -C /tmp/verifyB1-M2-a rev-parse --short HEAD -> c11ae01 (the task's pin; the brief's b4590f6 is not the checkout). git status --short: only the .venv link and vendor copy; no commit made.")
r("M2-a-cmd-check_pages", "2.9-structure", "tools/check_pages.py --unit M2", P,
  "`.venv/bin/python tools/check_pages.py --unit M2` -> 'check_pages M2: PASS', exit 0 (log /tmp/M2-v/a/check_pages.txt).")
r("M2-a-cmd-check_dag", "2.9-structure", "tools/check_dag.py --all", P,
  "`.venv/bin/python tools/check_dag.py --all` exit 0; line 'check_dag M2: PASS' (log /tmp/M2-v/a/dag.txt).")
r("M2-a-cmd-run_labs", "2.5-lab", "tools/run_labs.py --unit M2; tests/labs/M2/lab-M2-L01..L06-1.py", P,
  "`.venv/bin/python tools/run_labs.py --unit M2` -> 'run_labs M2: PASS (27/27)', exit 0 (log /tmp/M2-v/a/labs.txt). Covers the six slice twins.")
r("M2-a-cmd-page_smoke", "2.9-structure", "tools/page_smoke.py --unit M2 --pages index L01 L02 L03 L04 L05 L06", P,
  "`.venv/bin/python tools/page_smoke.py --unit M2 --pages index L01 L02 L03 L04 L05 L06`: 'page_smoke modules/M/M2/index.html: PASS' and PASS for L01-L06, 'page_smoke M2: PASS', exit 0; lab timings 0.0 s each, boot 1.1 s (log /tmp/M2-v/a/smoke.txt).")
r("M2-a-cmd-ruff", "2.5-lab", "tests/labs/M2 (ruff check, ruff format --check)", P,
  "`.venv/bin/python -m ruff check tests/labs/M2` -> 'All checks passed!' exit 0; `ruff format --check` -> '27 files already formatted' exit 0.")
r("M2-a-cmd-mypy", "2.5-lab", "tests/labs/M2 (mypy strict, pyproject.toml [tool.mypy])", P,
  "`.venv/bin/python -m mypy --no-incremental tests/labs/M2` -> 'Success: no issues found in 27 source files', exit 0.")
r("M2-a-cmd-refs", "2.1-citations", "tools/verify_refs.py --unit M2; tools/verify_refs.py --offline; references/references.json", P,
  "live `tools/verify_refs.py --unit M2`: 'live re-verification of M2: 2 of 560 entries, 0 problems', exit 0; offline `tools/verify_refs.py --offline`: 'offline integrity: 560 entries, 0 problems', exit 0 (logs /tmp/M2-v/a/refs_live.txt, refs_offline.txt).")
r("M2-a-lab-twins-match", "2.5-lab", "tests/labs/M2/lab-M2-L01-1.py .. lab-M2-L06-1.py; L01..L06.html <code class=language-python> and <pre class=expected>", P,
  "ledgers/M2/scripts/M2-a-r1/twin_compare.py: for L01-L06 the embedded code equals the twin byte-for-byte after strip (True x6); each twin run with `python -I -W error` exits 0 and its stdout equals the embedded expected block (True x6).")

# ---- labs: one row per lab (2.5) ----
for n, desc in [("01", "tabulated limit, exact threshold 1000, search to 5000"),
                ("02", "limit-law closed forms at n=1,10,100,1000,10000"),
                ("03", "one-sided values at h=0.1..0.0001; grid check for delta=eps/3 at 38 points"),
                ("04", "difference quotient of x^3 at a=1, h=10^-1..10^-6"),
                ("05", "product, quotient, chain rules vs central difference at x=1.5, h=1e-4"),
                ("06", "sign of f'=3x^2-3 vs monotone intervals on a grid of step 1/4")]:
    r(f"M2-a-lab-L{n}", "2.5-lab", f"tests/labs/M2/lab-M2-L{n}-1.py; course/modules/M/M2/L{n}.html", P,
      f"run_labs M2 PASS; twin run under -I -W error exit 0 and output equals embedded expected block. Lab shows {desc}. Standard library only, no randomness, no network; Pyodide smoke PASS with lab time 0.0 s. Hypothesis/prediction text checked against the printed output.")

# ---- numbers (2.2) ----
r("M2-a-num-hub", "2.2-numbers", "course/modules/M/M2/index.html, placement paragraph (line 41 of the text render)", P,
  "Recomputed: 80% of 8 items = 6.4, so at least 7 correct; 6/8 = 75%, 7/8 = 87.5% (ledgers/M2/scripts/M2-a-r1/recompute.py). Class (c).")
r("M2-a-num-hub-hours", "2.9-structure", "course/modules/M/M2/index.html data-hours-lessons=240 data-hours-project=60; L01-L06 'N study hours'", P,
  "24 lessons x 10 h = 240; 240 + 60 = 300 = curriculum; 60/300 = 20% (inside the 10-40% band). All six slice pages declare 10 study hours. Pace not judged (architect ruling).")
r("M2-a-num-L01", "2.2-numbers", "L01.html Lab 1 hypothesis (line 49), Example 2.3, Problems E1-E3, quiz", P,
  "Recomputed exactly: a_1000 = 2001/1001 = 1.999000999..., error 1/1001 = 9.990010e-4 after rounding; 1/(n+1) < 10^-3 first holds for n >= 1000; error at 999 = 1e-3 exactly; 302/10100 n/a here; 1/10 for a_9; N=10000 for 10^-4; mech-1 N=1297 for eps=0.01 (13/(n+4) < 0.01 iff n > 1296). All match.")
r("M2-a-num-L02", "2.2-numbers", "L02.html Lab 1 hypothesis (line 46), Problems E1-E3, quiz, key-results row", P,
  "Recomputed: sum error (n+2)/(n(n+1)) at n=10 = 12/110 = 6/55 = 0.109091; product error (3n+2)/(n(n+1)) at n=100 = 302/10100 = 0.02990099...; quotient error (5n+4)/((n+1)(n+2)) at n=1 = 3/2; at n=10 = 54/132 = 0.409091; n=1000 quotient 4.989023e-3; all printed values match.")
r("M2-a-num-L03", "2.2-numbers", "L03.html Lab 1 hypothesis (line 64), interpretation (line 106), E1-E2, key row", P,
  "Recomputed: f(1-h)=(1-h)^2, f(1+h)=2+2h, gap 1+4h-h^2: h=0.1 gap 1.39; h=0.01 gap 1.0399; h=0.001 left 0.998001, right 2.002, gap 1.003999; h=1e-4 left 0.999800, right 2.000200, gap 1.000400. Grid count 38 = 2*19 points (k in -19..19, k != 0).")
r("M2-a-num-L04", "2.2-numbers", "L04.html Lab 1 hypothesis (line 37), canon (line 97), E1-E3, misconception 3 (line 109)", P,
  "Recomputed exactly: Q(h)=3+3h+h^2; Q(0.1)=3.31, error 0.31; Q(0.001)=3.003001; error at 1e-5 = 3.00001e-5 (prints 3.000010e-05); error/h at 1e-6 = 3.000001. All match the printed table.")
r("M2-a-num-L05", "2.2-numbers", "L05.html Lab 1 hypothesis (line 52), interpretation (line 102), E1-E3, Example 2.2 (line 114), key row", P,
  "Recomputed: p'(1.5)=32.0625, q'(1.5)=29/49=0.5918367346..., c'(1.5)=95.0625; E1: h^2 p'''(1.5)/6 = 1e-8*141/6 = 2.35e-7 matches the printed 2.350e-07; E2 printed 0.591836735 rounds 29/49 correctly. (The lab-size sentence in misconception 3 is a separate FAIL row.)")
r("M2-a-num-L06", "2.2-numbers", "L06.html Lab 1 hypothesis (line 64), interpretation (line 112), M2, misconception 3 (line 129), quiz", P,
  "Recomputed: 8 of 16 intervals increasing (4 in [-2,-1], 4 in [1,2]); f(-1)=2, f(1)=-2; f(-2)=-2; 1/sqrt(3)=0.5774 (text says 0.577, correct to 3 places); 2/sqrt(3)=1.1547005 matches 1.1547. Midpoints are odd multiples of 1/8.")
r("M2-a-num-L05-lab-size", "2.2-numbers", "course/modules/M/M2/L05.html:210 (misconception 3, 'which is the size of the central-difference error in Lab 1')", F,
  "The sentence says the error h^2 = 1e-8 is 'the size of the central-difference error in Lab 1'. Lab 1 prints 2.350e-07, 3.328e-10 and 8.550e-07 (L05.html lab output); none is 1e-8. The lab uses p, q and c, not x^3. Recomputed in recompute.py: h^2 = 1e-8 vs printed 2.35e-7 and 8.55e-7.",
  "Replace with: 'For x^3 the error is exactly h^2 (1e-8 at h = 1e-4). Lab 1's errors (2.35e-7, 3.3e-10, 8.55e-7) are h^2 p'''/6 for each function, not h^2.' Or drop the Lab 1 comparison.")

# ---- math (2.4) ----
r("M2-a-math-L01", "2.4-math", "L01.html Def 2.1, Prop 2.2, Prop 3.1, Ex 2.3, Ex 4.1, Problems M1-M3, P1-P3, R1-R3", P,
  "Re-derived each proof line by line: Prop 2.2 (eps/2 thresholds, triangle inequality), Prop 3.1 (N' = max(N,M)), Ex 2.3 (N > 1/eps), Ex 4.1 (contradiction 2 < 2), P3 shift N' = max(1, N-5), R2 floor bound 0 <= x - t_n < 10^-n, R3 square/nonsquare contradiction. No gap found in these.")
r("M2-a-math-L02", "2.4-math", "L02.html Prop 1.1 (i)-(iii) and proof, Corollary 2.2, Ex 2.3, Remark 3.1, Problems", P,
  "Re-derived (ii): a_n b_n - ab = a_n(b_n-b) + b(a_n-a) bound; (iii): identity (b(a_n-a) - a(b_n-b))/(b b_n), bound 2/|b|^2 times the bracket, thresholds eps|b|/4 and eps|b|^2/(4(|a|+1)) give < eps. Closed-form errors for Lab 1 re-derived (see num-L02). No gap.")
r("M2-a-math-L03", "2.4-math", "L03.html Def 1.1, Prop 1.3, Cor 1.4, Prop 2.2 (both directions), Ex 1.2, 2.3, 2.4, Problems P1-P3, R1-R3", P,
  "Re-derived: Ex 2.3 left delta=min(1,eps/2) gives |x^2-1|<2 delta <= eps; Prop 2.2 'if' direction with min(delta+,delta-); P2 delta=min(1, eps/(1+2|a|)); P3 uniqueness; R1 |f(x)| <= x^2; R2 bounded factor. Statement of Cor 1.4 proof does not use Prop 1.3 (see xref row).")
r("M2-a-math-L04", "2.4-math", "L04.html Def 1.1, Prop 2.1 (proof lines 84-86), Ex 1.2, Ex 3.1, Problems P1-P3, R1-R3", P,
  "Re-derived Prop 2.1: delta = min(delta1, eps/(|f'(a)|+1)) gives |f(x)-f(a)| = |x-a||Q| < delta(|f'|+1) <= eps. P1 cube derivative delta=min(1, eps/(3|a|+1)). Ex 3.1 one-sided quotients +1/-1. R1 x|x| quotient |h|. No gap.")
r("M2-a-math-L05", "2.4-math", "L05.html Lemma 1.1 proof (line 62, 'the same estimates close the argument'); Prop 2.1 proof (line 175, 'Define G on J')", F,
  "Lemma 1.1 (c) is used by Prop 1.3 for the final quotient limit, but its proof is not written: the text says only that 'the same estimates close the argument'. The displayed estimates cover (a) and (b). Also Prop 2.1 says 'Define G on J by G(k) = (g(b+k)-g(b))/k', but G(k) is defined only for b+k in J, so its domain is J minus b, not J. Products (a), (b), the quotient in Prop 1.3 and the chain rule were re-derived and are correct.",
  "Write the (c) estimate out: |G(h)| > |M|/2 gives |F/G - L/M| <= (2/|M|^2)(|M||F-L| + |L||G-M|) < eps with thresholds for F-L and G-M. Change 'Define G on J' to 'Define G on J - b = {k : b + k in J}'.")
r("M2-a-math-L06", "2.4-math", "L06.html Prop 1.1 (line 34), Fact 2.1, Thm 2.2, Thm 2.3, Cor 3.1 (i)-(iii), Problems P1-P3", P,
  "Re-derived: Prop 1.1 one-sided Q bounds and contradiction; Rolle picks a maximum off the endpoints when f(a)=f(b) and f non-constant; MVT via g(x)=f(x)-f(a)-s(x-a) with g(a)=g(b)=0; Cor 3.1 by MVT on [x,y]. Fact 2.1 is assumed and labelled ungraded, honestly. No gap in the proofs.")

# ---- grades (2.3) ----
r("M2-a-grade-labs", "2.3-grades", "L01-L06 key-results tables; lab interpretation paragraphs", P,
  "Every lab-derived row is graded C with basis naming Lab 1 (L01 line ~ key row, L02-L06 likewise). Every proved row is T with a locator to its proof (Prop 1.1 L02, Prop 2.2 L03, Prop 2.1 L04, Thm 2.3 L06 etc.). Fact 2.1 (EVT) is marked 'not graded' and listed as a hypothesis, consistent with its status.")

# ---- prose / scope / overclaims (2.9, 2.4) ----
r("M2-a-prose-L01-lab-would-print", "2.2-numbers", "course/modules/M/M2/L01.html:277 (Problem E3 solution)", F,
  "E3 says 'The lab would print 1.000000 x 10^-4 for the error at n = 9999.' Lab 1 (tests/labs/M2/lab-M2-L01-1.py, main()) prints the error only at n = 999 and n = 1000 and tests tolerance 1/1000, never n = 9999 or tolerance 1e-4. The sentence is false about the lab as shipped.",
  "Replace 'The lab would print' with 'A run of the same formula at n = 9999 would give 1.000000e-4' and drop 'the lab' as the source.")
r("M2-a-prose-L05-misc-h2", "2.9-structure", "course/modules/M/M2/L05.html:210", F,
  "Misconception 3 says the error h^2 'is the size of the central-difference error in Lab 1'. Lab 1 errors are 2.350e-07, 3.328e-10 and 8.550e-07 at h=1e-4 (L05.html lab output); h^2 = 1e-8 matches none. Same root as num-L05-lab-size.",
  "Use the wording in num-L05-lab-size: the exact error for x^3 is h^2; Lab 1's errors are h^2 p'''/6 etc.")
r("M2-a-prose-L06-exactly", "2.9-structure", "course/modules/M/M2/L06.html:51 (why it matters); L06.html:323 (key-results row 'controls monotonicity')", F,
  "'This lesson states exactly when that works' overclaims: the lesson proves only a necessary condition (Prop 1.1, stated at L06.html 'gives a necessary condition') and a sufficient condition for strict monotonicity (Cor 3.1 (ii)); it gives no sufficient condition for an extremum. Also 'The sign of the derivative controls monotonicity' overstates Cor 3.1, which gives one-way implications (sufficient, and not necessary by the x^3 example).",
  "Change to: 'This lesson states when a derivative test gives a necessary condition for an extremum, and a sufficient condition for increase.' Change the key-results row to 'The sign of the derivative gives sufficient conditions for monotonicity (Corollary 3.1)'.")
r("M2-a-prose-L06-each-hypothesis", "2.4-math", "course/modules/M/M2/L06.html:183 (canon-breaks: 'each hypothesis is needed')", F,
  "'The theorems above are sharp, and each hypothesis is needed. Three cases show...' Only two hypothesis drops are shown (continuity at the endpoint, differentiability on the open interval). The third case is about a zero derivative not implying an extremum, which concerns the converse of Prop 1.1, not a dropped hypothesis. Hypotheses of Prop 1.1 (local extremum), Rolle (f(a)=f(b)) and Cor 3.1 are not shown needed.",
  "Either give a counterexample for each dropped hypothesis, or change to 'Two hypotheses are shown to be needed: continuity on the closed interval and differentiability on the open interval.'")
r("M2-a-prose-L04-only-meaning", "2.9-structure", "course/modules/M/M2/L04.html:60 (Definition 1.1 paragraph, 'This is the only meaning of derivative used in the unit.')", F,
  "A universal scope claim about the whole unit. Only L01-L06 were read (and L16 partial derivatives is outside this slice); no computation or witness is given in this lesson that every later use of 'derivative' reduces to this definition.",
  "Change to 'This is the meaning of derivative used in this lesson.' or verify and cite the later uses.")
r("M2-a-prose-frequency-claims", "2.9-structure", "index.html:33 ('Much of finance concerns rates of change'); L01.html:179 ('A limit is rarely attained.'); L02.html:51 ('a frequent error comes from using a quotient law when its denominator has limit zero')", F,
  "Frequency claims with no computation or source: 'Much of finance', 'rarely attained', 'a frequent error'. The example in L01 shows only that one sequence never equals its limit. None is supported by a count, a citation, or a stated hypothesis.",
  "Remove the frequency word or support it: e.g. 'A limit is not attained by the terms of (2n+1)/(n+1), which never equal 2.' Replace 'a frequent error' with the Remark 3.1 example as the illustration.")
r("M2-a-prose-unproved-claims", "2.4-math", "L01.html:198 ('Boundedness is a necessary condition for a limit'); L02.html:206 ('b_n is a sign change of a_n, so it diverges too'); card M2-c012", F,
  "Two assertions used as facts with neither a proof nor a grade. (1) That a convergent sequence is bounded is not proved in L01 (Prop 2.2, 3.1 and Ex 4.1 do not prove it) and is not in the key-results table. (2) In L02 Misconception 2, 'b_n is a sign change of a_n, so it diverges too' needs 'if -a_n converges then a_n converges', which the lesson does not state. Card M2-c012 repeats (1).",
  "Prove (1) in two lines (|a_n| <= |L| + 1 for n >= N from the definition, then finitely many terms) and grade it T in the key-results table; for (2) cite the sign-change step by the product law with the constant -1 from Prop 1.1 (ii).")
r("M2-a-xref-L03-keyrow", "2.4-math", "course/modules/M/M2/L03.html:320 (key-results row 'A limit of a function gives the limit along every sequence that avoids the point'); L03.html:321 ('Proved in §1 from Proposition 1.3 and Lesson 2, §2' for Corollary 1.4); L03.html 'Uses:' line (limit laws, Lesson 2 Prop 1.1)", F,
  "The T-graded key row drops Prop 1.3's hypotheses: the sequence must lie in I and converge to a (the row says only 'avoids the point'). The Cor 1.4 row cites Prop 1.3, but the Cor 1.4 proof (L03.html ~line 46) is direct and does not use it. The 'Uses' line lists the limit laws (Lesson 2 Prop 1.1), which no L03 statement or proof uses.",
  "Key row: 'If x_n is in I, x_n != a and x_n -> a, then f(x_n) -> L along that sequence (Proposition 1.3)'. Cor 1.4 row: 'Proved in §1 directly, using Definition 1.1 and Lesson 2 §2'. Remove the limit-laws entry from 'Uses'.")

# ---- DAG / concepts (2.9) ----
r("M2-a-dag-slice", "2.9-structure", "tools/check_dag.py --all; slice data-concept links; <dfn> anchors; course/concepts.html", P,
  "check_dag M2: PASS. Concept links in the slice: quantifiers, direct-proof, proof-by-contradiction, mathematical-induction, exponential-and-logarithm (M1, each anchor present in concepts.html), evidence-grade, notation-conventions, project-ladder (P0.1, each reads 'not yet released' in concepts.html), and limit (L01 dfn id=def-limit), derivative (L04 dfn id=def-derivative). Each dfn appears once. No slice page links or names a later-module concept (grep: Riemann, Lebesgue, Fubini, matrix, Jacobian, Hessian appear only as M2 lesson titles or the M2 course's own sections).")
r("M2-a-xref-M1-locators", "2.9-structure", "index.html lines for placement explanations; L01.html (Theorem 3.2 (a), M1 Lesson 2), L03 uses, L06 uses", P,
  "Read course/modules/M/M1/L01.html Theorem 3.2 (a): not(for all x exists y R) iff exists x for all y not R, matching the hub explanation and L01's quiz. M1 L02 is 'Direct Proof and Proof by Contradiction' (√2 corollary 2.6). M1 L06 is 'Geometric Series and Proof by Induction'. M1 L03 defines the natural logarithm as the inverse of exp. All hub and lesson cross-references to M1 match.")
r("M2-a-hub-structure", "2.9-structure", "course/modules/M/M2/index.html", P,
  "Objectives: 7 (4-8 required). Prerequisites M1 and P0.1 linked. Placement: 8 items (6 M1/P0.1, 2 skill checks with data-skill and data-answer 2 and 3.01); data-mastery 0.8; data-unit M2. Lesson map: 24 cards L01-L24 each with its hours. Project ladder: four rung titles in order. Data status states 'No real data is used'. Core reading lists only the registry keys, with no locator.")
r("M2-a-cards-L01-L06", "2.7-cards", "course/modules/M/M2/cards.json (ids M2-c001..M2-c074, lesson L01-L06)", P,
  "All 74 cards read and compared with the lesson text: definitions, propositions, examples, misconceptions and Lab 1 values (e.g. c006 N=1000, c025 6/55, c035 gap 1.000400, c056-c058 central differences, c069 8 of 16). Each number appears in its lesson. Card c012 repeats the unproved boundedness claim (see M2-a-prose-unproved-claims).")
r("M2-a-cards-dup-scan", "2.7-cards", "course/modules/M/M2/cards.json: full scan of 375 cards for duplicate or near-duplicate fronts", F,
  "Full scan (difflib ratio > 0.85 on fronts): M2-c043 (L04, 'Proposition 2.1: does differentiability at a imply continuity at a?') and M2-c268 (L18, 'Proposition 3.3: does differentiability at a imply continuity at a?') have near-identical fronts for two different statements (scalar case vs map R^2 -> R^2). M2-c065 (L06 Rolle) and M2-c099 (L08 Rolle) restate the same theorem. Outside this slice: M2-c342 and M2-c343 (L23) have identical fronts, which the L23 verifier must catch.",
  "Give each card a front that names the setting: 'For a map F: R^2 -> R^2, ...' for c268, and 'Rolle's theorem on [p, q] (the special case of the MVT)' for c099, with c065 kept as the canonical card. Fix c342/c343 fronts in the L23 round.")
r("M2-a-refs-spivak-hubbard", "2.1-citations", "references/references.json keys spivak2008calculus, hubbard2015vector; L01-L06 'References' sections", P,
  "Registry entries read: spivak2008calculus (Calculus, Spivak, 2008, status verified, used_by M2); hubbard2015vector (Vector Calculus, Linear Algebra, and Differential Forms, Hubbard & Hubbard, 2015, status verified, used_by M2). Every slice reference section states that no passage locator is confirmed and attributes no statement to either source. Attribution check: nothing to check on the page; scope: none. Source text not read (no locator is claimed).")
r("M2-a-hub-banned", "2.9-structure", "index.html and L01-L06 visible prose; tools/check_pages.py banned-string scan", P,
  "check_pages M2: PASS (banned-string scan included). Manual scan of the rendered text: no 'roughly', 'about', 'historically', 'typically', no process words ('builder', 'verifier', 'round', 'REQUEST'). The only ellipsis is list notation inside a lab docstring (L06 lab line 'lo, lo + step, ..., hi'), which is code, not learner prose. Scope-word hits are logged in the rows above, not passed.")
r("M2-a-hours", "2.9-structure", "L01..L06 headers; index.html hours split", P,
  "Declared 10 h each (6-12 band), hub 240 + 60 = 300, 20% project share. Arithmetic consistent (see num-hub-hours). Pace not judged.")

fragment = {
    "unit": "M2",
    "slice": "M2-a",
    "round": 1,
    "verifier": "round-1 independent verifier (Haiku), slice M2-a (hub index.html, L01-L06 and their lab twins); did not build M2 and shares no context with the builders",
    "pin": "c11ae01",
    "base": "none",
    "checkout": "/tmp/verifyB1-M2-a (detached, pinned at c11ae01; .venv symlinked; vendor copied)",
    "scratch": "/tmp/M2-v/a",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Scope: index.html, L01-L06, tests/labs/M2/lab-M2-L01-1..L06-1.py. Cards for L01-L06 (cards.json) were checked as part of the slice; the rest of cards.json and L07-L24 were not read.",
        "Mutation: the architect ruling makes mutation testing a project-grader requirement only. This lab slice has no grader, so mutants is empty and no mutant was written. The three labs' outputs were compared with embedded expected blocks; no mutant is needed.",
        "Brief said pin b4590f6; the task text and the checkout are at c11ae01. The fragment records c11ae01.",
        "Not read: the Spivak and Hubbard sources (no locator is claimed, and the brief's access rules were not tested). No attempt was made to reach publisher pages.",
        "Hours pace not judged (architect ruling). Hub split and lesson hours checked for arithmetic only.",
        "Outside this slice, noted by the full cards.json duplicate scan: M2-c342 and M2-c343 (L23) have identical fronts.",
    ],
    "summary": {},
}
fragment["summary"] = {
    "rows": len(rows),
    "pass": sum(1 for x in rows if x["status"] == "PASS"),
    "fail": sum(1 for x in rows if x["status"] == "FAIL"),
    "unverifiable": sum(1 for x in rows if x["status"] == "UNVERIFIABLE"),
}
out = "/tmp/verifyB1-M2-a/ledgers/M2/M2-a.json"
json.dump(fragment, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(fragment["summary"])
