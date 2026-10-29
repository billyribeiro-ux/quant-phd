"""Writes ledgers/CS2/CS2-a.json (round 3) from the verifier's row list. Pure data; no network."""
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
P = "PASS"
F = "FAIL"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix
    rows.append(r)


CARRY = ("Carried from round 2 (course/modules/CS/CS2/L01.html and tests/labs/CS2/lab-CS2-L01-1.py, "
         "and the other subjects named, byte-identical since the previous pin 1817191; git diff --quiet): ")

# ---- commands and reproductions (fresh at aa3c26c)
row("CS2-a-cmd-check_dag", "2.8-dag", "tools/check_dag.py --unit CS2", P,
    "Round 3 at aa3c26c: `.venv/bin/python tools/check_dag.py --unit CS2` printed 'check_dag CS2: PASS'. Content of the DAG use is judged in CS2-a-dag.")
row("CS2-a-cmd-check_pages", "2.9-structure", "tools/check_pages.py --unit CS2; cards.json", P,
    "Round 3: `.venv/bin/python tools/check_pages.py --unit CS2` printed 'check_pages CS2: PASS'.")
row("CS2-a-cmd-page_smoke", "2.5-lab", "tools/page_smoke.py --unit CS2 --pages index L01 L02 L03 L04", P,
    "Round 3: PASS for index, L01, L02, L03, L04 (log /tmp/CS2-v/a3/page_smoke.out); 'page_smoke CS2: PASS'. Lab run times 0.0 to 0.6 s in Pyodide.")
row("CS2-a-cmd-run_labs", "2.5-lab", "tools/run_labs.py --unit CS2", P,
    "Round 3: 'run_labs CS2: PASS (14/14)'. The four CS2-a twins are also run in CS2-a-cmd-cmp_labs.")
row("CS2-a-cmd-lint-types-labs", "2.9-structure", "tests/labs/CS2/lab-CS2-L01-1.py..L04-1.py", P,
    "Round 3: `.venv/bin/ruff check tests/labs/CS2` -> All checks passed; `ruff format --check tests/labs/CS2` -> 14 files already formatted; `.venv/bin/mypy --no-incremental tests/labs/CS2` -> Success: no issues found in 14 source files.")
row("CS2-a-cmd-verify_refs", "2.1-citations", "tools/verify_refs.py --offline; tools/verify_refs.py --unit CS2", P,
    "Round 3: offline 'integrity: 560 entries, 0 problems'; live `verify_refs.py --unit CS2` '1 of 560 entries, 0 problems' (only cormen2022introduction is cited by CS2-a).")
row("CS2-a-cmd-cmp_labs", "2.5-lab", "course/modules/CS/CS2/L01.html..L04.html data-run and expected blocks; tests/labs/CS2/lab-CS2-L01-1.py..L04-1.py", P,
    "Round 3: scripts/CS2-a-r3/twin_vs_page.py ran each twin under `python -I -W error`: L01..L04 code_identical_to_twin=True, rc=0, stdout_equals_expected=True; 'ALL_OK'.")
row("CS2-a-lab-L01-twin", "2.5-lab", "tests/labs/CS2/lab-CS2-L01-1.py; L01.html data-run block", P,
    "Round 3 twin_vs_page.py: code identical and stdout equals the expected block (L01 block line 190-212). Twin unchanged since 1817191.")
row("CS2-a-lab-L02-twin", "2.5-lab", "tests/labs/CS2/lab-CS2-L02-1.py (docstring changed); L02.html lines 130-240", P,
    "Round 3 twin_vs_page.py: L02 code identical to the page data-run block and stdout equals the expected block (228-240). The only change since 1817191 is a docstring sentence (line 139), which states that the output prints both values; the output does print both.")
row("CS2-a-lab-L03-twin", "2.5-lab", "tests/labs/CS2/lab-CS2-L03-1.py; L03.html data-run block", P,
    "Round 3 twin_vs_page.py: code identical; stdout equals the expected block (258-286) for N = 16..4096.")
row("CS2-a-lab-L04-twin", "2.5-lab", "tests/labs/CS2/lab-CS2-L04-1.py; L04.html data-run block", P,
    "Round 3 twin_vs_page.py: code identical; stdout equals the expected block (342-386). The docstring overclaim is a separate row (CS2-a-lab-L04-docstring-partB).")

# ---- hypotheses and numbers
row("CS2-a-lab-L01-hypothesis", "2.5-lab", "L01.html line 119 hypothesis", P,
    CARRY + "L01.html and lab-CS2-L01-1.py. Predictions checked: 1001 = first n with n*n > 1000n; ratio (2^k-1)/(2^(k-1)-1) = 2 + 1/(2^(k-1)-1); 4^k pair steps.")
row("CS2-a-lab-L02-hypothesis", "2.5-lab", "L02.html line 129 hypothesis; lab output lines 228-240", P,
    "Round 3 recomputation (scripts/CS2-a-r3/recompute_numbers.py): 1+(n-1)/128 at n=16,32,64,128,256 = 1.1171875, 1.2421875, 1.4921875, 1.9921875, 2.9921875, which round to the stated 1.1172, 1.2422, 1.4922, 1.9922, 2.9922; alpha = 0.25, 0.5, 1, 2, 4; colliding total 50*51/2 = 1275; unsuccessful probe count for 3264 = 50 (recomputed chain length 50).")
row("CS2-a-lab-L03-hypothesis", "2.5-lab", "L03.html line 92 hypothesis", P,
    CARRY + "L03.html and lab-CS2-L03-1.py. Stated bounds 6N floor(log2 N) and 2 floor(log2 s) are the code's bounds (lines 234, 171 of the twin); growth predictions (about 4 and about 2 per doubling) match printed ratios 3.7-4.5 and 2.0-2.4 within the stated 'about'.")
row("CS2-a-lab-L04-hypothesis", "2.5-lab", "L04.html line 155 hypothesis", P,
    "Round 3: Part A sizes 8, 64, 256, 1024 and sorted 1024 (twin lines 251-266); Part B 'every permutation of 2 to 7' (lines 272-291) with insertion max n(n-1)/2 and merge max in [ceil log2 n!, n ceil log2 n] (output 352-364); Part C 2..1000 (line 300); Part D 1..1000 (line 319). Every clause matches the code and printed lines.")
row("CS2-a-num-L01", "2.2-numbers", "L01.html interpretation line 213, E1 line 327, key-results line 384", P,
    CARRY + "L01.html. Recomputed in round 3: 1023/511 = 2.0019569 -> 2.0020; pair-step ratio 4.0000 at every doubling (exact n^2 counts); 1000 of 1000; first failure 1001.")
row("CS2-a-num-L02-exact", "2.2-numbers", "L02.html interpretation line 241; E1 solution line 333; misconception 3 line 268", P,
    "Round 3 scripts/CS2-a-r3/recompute_numbers.py from an independent hash and key set: successful totals 16, 37, 97, 257, 772 (exact averages 1, 37/32, 97/64, 257/128, 193/64); successful gaps -15/128, -11/128, 3/128, 1/64, 3/128 = -0.1171875, -0.0859375, 0.0234375, 0.015625, 0.0234375; unsuccessful totals 134, 270, 548, 1016, 2014 over 500 absent keys, giving the exact gaps 0.018, 0.04, 0.096, 0.032, 0.028 (all exact, so the statement that the gaps use exact quotients holds). E1 claim that each total is the only integer in the printed interval holds for n <= 256 (half-width 0.00005 n <= 0.0128). Misconception 3: model increase 255/128 - 127/128 = 1; measured 193/64 - 257/128 = 129/128 = 1.0078125; printed 3.0156 - 2.0078 = 1.0078.")
row("CS2-a-num-L03", "2.2-numbers", "L03.html interpretation line 287; misconceptions lines 337, 341; E2-E3 lines 421, 428; Remark 1.7 line 314; canon line 324", P,
    CARRY + "L03.html. Recomputed in round 3: 6*4096*12 = 294912 and margin 128000; 2*4096*4097 = 33562624; 4378444/33562624 = 0.1305; 107+98 = 205, 241+361 = 602; 1617+4514 = 6131, 3802+4933 = 8735; 3742+17663 = 21405, 8517+10623 = 19140; 92609/8192 = 11.30; printed ratio ranges reproduced from the printed rows (sorted 3.5282..4.5050 in rows 64..4096; heap 1.9858..2.3778 in rows 64..4096).")
row("CS2-a-num-hub", "2.2-numbers", "index.html lines 31, 42, 71, 143", P,
    CARRY + "index.html. 7/9 = 77.8 percent and 8/9 = 88.9 percent (line 71); 100/130 = 76.9 -> 77 and 30/130 = 23.1 -> 23 (lines 40, 42).")
row("CS2-a-num-L04", "2.2-numbers", "L04.html interpretation line 387; E1 478; E2 485; E3 492; Remark 2.3 line 124; Part C line 309", P,
    "Round 3 recomputation: smallest integer c with 2^c >= 1024! is 8770 (log2(1024!) = 8769.006); 5120 = 10*2^9; 5120/8770 = 0.58381 -> 0.58; 262431/8886 = 29.5331 -> 29.53 (8886*29 = 257694, remainder 4737); log2(1000!) = 8529.3980 and 500*log2 500 = 4482.8921; smallest margin over n = 2..1000 is 1.0 at n = 2; sum over n = 1..1000 of (n+1) = 501500; Part B n=7 lower bound ceil(log2 5040) = 13, merge maximum 14, bound 21, insertion maximum 21.")
row("CS2-a-math-L01", "2.4-math", "L01.html Definition 1.1, Propositions 1.2, 1.3, 1.4, 1.6, 1.7, 2.3, Remark 2.2, Examples", P,
    CARRY + "L01.html. Re-derived in round 3: Prop 1.2 witness a+b+1; Prop 1.3 N = max(n0, floor(c)+1); Prop 1.4 induction; Prop 2.3 equivalence 1000n > n^2 iff n < 1000; R3 bound (n-1)/2 > c.")
row("CS2-a-math-L01-prop17-domain", "2.4-math", "L01.html Proposition 1.7 (line 109)", P,
    CARRY + "L01.html line 109; Proposition 1.7 hypothesis n >= 1 and the step model are stated.")
row("CS2-a-math-L02", "2.4-math", "L02.html Definitions 1.1-1.2, Propositions 1.3, 1.4, 2.2, Corollary 2.3, Remarks 1.5, 2.4, Example 2.5", P,
    "Round 3 full re-derivation of the changed subject. Prop 1.4: 64jM = q*2^32 + 64r with 0 <= 64r < 2^32, so h(64j) = 0 for all j >= 0 (checked for j <= 2000 by script). Prop 2.2(a),(b),(c) and Cor 2.3 re-derived; (c) sum rewritten as (n-1)/(2m) correctly. Example 2.5: 64*(1/64)^50 = 64^-49 (exact check in script). Scope: 'every stored key' computed.")
row("CS2-a-L02-R3-boundary", "2.4-math", "L02.html R3 solution line 372", P,
    "Re-derived: alpha - 1 - (n-1)/(2m) = (n - 2m + 1)/(2m). For integers n it is positive iff n >= 2m (iff alpha >= 2), zero at n = 2m-1, negative below. The page now says exactly this, including the tie at n = 2m-1. The round-2 wording error is fixed.",
    None)
row("CS2-a-math-L03", "2.4-math", "L03.html Propositions 1.2, 1.3, 1.5, 1.6, Remark 1.7, problems M1-M3, P1, P3, R1-R3", P,
    CARRY + "L03.html. Re-derived in round 3: Prop 1.2 level formula; Prop 1.3(b) h = floor(log2(s-1)) <= floor(log2 s); Prop 1.5 total 2N*L + 2N*2L = 6NL; Prop 1.6 per-push L-p+1 <= L+1 <= N+1 (list never holds more than N keys in the hold run).")
row("CS2-a-math-L03-P2", "2.4-math", "L03.html Problem P2 solution, lines 388-396", F,
    "The three-part invariant (a), (b), (c) is correct and the base, step and stop cases are right. But the step introduces the sibling sigma of i and uses sigma twice ('By (a), y = a[p] < a[sigma]'; '(c) at p: x < y < a[sigma]'). When i has no sibling (for example i = 2 in a 3-key heap, whose parent p = 0 has only the child i), sigma does not exist and the solution never says so. The case is harmless (the claims about sigma are vacuous) but it is not covered, so the proof has a gap.",
    "State the case: 'If i has no sibling, every claim about sigma is vacuous and the step goes through with (b) and (c) alone for p.' Re-verify.")
row("CS2-a-math-L04", "2.4-math", "L04.html Lemma 1.2, Propositions 1.3, 2.1, Corollary 2.2, Remark 1.4", P,
    "Round 3 re-derivation. Lemma 1.2: a+b-1 bound (each comparison outputs one key; at stop one list empty). Prop 1.3: K = ceil(log2 n), a = ceil(n/2) <= 2^(K-1) < n, IH gives C(a) <= a(K-1), C(b) <= b(K-1), total nK - 1. Remark 1.4(a),(b),(c): counts n-1, n(n-1)/2 and k 2^(k-1) recomputed by script and printed in Lab 4 Part A (5120 at k=10). Cor 2.2: factors k >= n/2 counted as floor(n/2)+1 >= n/2 and checked numerically in Part C.")
row("CS2-a-math-L04-prop2.1", "2.4-math", "L04.html Proposition 2.1 statement line 98 and proof line 103", P,
    "Hypothesis (5) (the algorithm returns the keys in increasing order on every input) is now stated, and the proof uses it to say that the output at a leaf is the sorting permutation, so distinct orderings end at distinct leaves. The round-2 counterexample (an algorithm that is not required to sort) is excluded by (5). Re-derived: n! distinct leaves, 2^h leaves at depth h, so h >= log2 n!.")
row("CS2-a-math-L04-prop3.2-monotone", "2.4-math", "L04.html Proposition 3.2 proof line 143; R1 solution line 503", F,
    "The induction step ends 'the search continues over a range of at most floor(s/2) positions and makes at most beta(floor(s/2)) = beta(s) - 1 further probes'. The induction hypothesis gives at most beta(t) probes for a range of t <= floor(s/2) positions; to reach beta(floor(s/2)) the proof needs beta to be nondecreasing, which is not stated or shown. R1's solution ('the induction goes through unchanged') relies on the same unstated step. The fact is true (the number of binary digits never decreases), so this is a missing step, not a false claim.",
    "Add one sentence: 'beta is nondecreasing, because a larger integer has at least as many binary digits, so beta(t) <= beta(floor(s/2)) for t <= floor(s/2).'")
row("CS2-a-math-L04-R3-hypotheses", "2.4-math", "L04.html problem R3 statement line 515 and solution line 517", F,
    "The statement says 'Any comparison algorithm that reports the gap must make at least ceil(log2(n+1)) comparisons on some input'. The solution's argument is the decision-tree leaf count, which needs the algorithm to be deterministic, to halt on every input, and to use only two-outcome comparisons. None of these hypotheses is listed, although Proposition 2.1 lists them. The problem is not graded T, but the general claim is stated without the hypotheses its proof uses.",
    "List the hypotheses before the claim (deterministic, halts on every input, the only key operation is a two-outcome comparison, and every gap is a possible answer), in the form used by Proposition 2.1.")
row("CS2-a-L01-lab-docstring", "2.5-lab", "tests/labs/CS2/lab-CS2-L01-1.py docstring lines 1-6; L01.html lines 121-126", P,
    CARRY + "lab-CS2-L01-1.py and L01.html. Docstring says every count is an exact integer in a counting model and no wall-clock time is measured; the code (lines 131-186) counts comparisons and steps and measures no time.")
row("CS2-a-L01-quiz-Q8", "2.4-math", "L01.html quiz item L01q8 and explanation line 452", P,
    CARRY + "L01.html. 3n+7 <= 10n for n >= 1; c = 1 fails for every threshold since 3n+7 > n.")
row("CS2-a-L02-misc3-prose", "2.2-numbers", "L02.html misconception 3, line 268", P,
    "Round 3: (256-128)/128 = 1 equals the model increase 255/128 - 127/128; measured 193/64 - 257/128 = 129/128 = 1.0078125; printed 3.0156 - 2.0078 = 1.0078, as stated. 'Either way the average does not double' holds (increases of 1 and 1.0078 on a base near 2 to 3).")
row("CS2-a-L02-quiz-Q7", "2.4-math", "L02.html quiz item L02q7 (line 441) and explanation line 447", P,
    "Round 3: at fixed m, cost 1 + (n-1)/(2m) -> 1 + (2n-1)/(2m) adds n/(2m); 1 + (2n-1)/(2m) < 2(1 + (n-1)/(2m)) for all n, so the increase is less than a doubling. Option text matches.")
row("CS2-a-L02-printed-digits", "2.2-numbers", "L02.html interpretation line 241; misconception 3 line 268; card CS2-c025", P,
    "Round 3: printed values 2.0078 vs model 1.9922 at n=128 and 4.0280 vs 4.0000 at n=256 match the expected block (lines 235, 237). Card c025 contains no printed digits to check. The wording problem in the card basis of CS2-c155 is in the cards row.")
row("CS2-a-L02-lab-heading-four-loads", "2.9-structure", "L02.html line 128 lab heading", P,
    "Round 3: heading now reads 'Probe counts at five loads and on a colliding key set'; the lab runs n = 16, 32, 64, 128, 256 (twin line 193; output lines 229-238), five loads.")
row("CS2-a-L04-quiz-inputs", "2.9-structure", "L04.html quiz items lines 545-613", P,
    "Round 3: each multiple-choice item has exactly one data-correct option; numeric answers 1023, 5120, 4, 3, 10 are recomputed from the formulas and the printed Part A and Part D rows.")
row("CS2-a-L04-lab-numbering", "2.9-structure", "L04.html line 154 and in-page lab references", P,
    "Round 3: the single lab is 'Lab 4'; in-page references to Lab 4 Part A, B, C, D match the twin's Part letters (twin lines 163-168).")
row("CS2-a-L04-footer", "2.9-structure", "L04.html line 630 footer; line 619 references", F,
    "The footer reads 'Every claim carries an evidence grade.' Several claims carry no grade attribute: Remark 1.4 (three counts, lines 88-89), Remark 2.3 (lines 122-125), Remark 3.3 and the Definitions. Only the blocks with class 'claim' carry data-grade. The sentence is an absolute scope claim the page does not meet.",
    "Change to 'Every graded result carries an evidence grade', the wording used on L01-L03.")
row("CS2-a-hub-SIMULATED", "2.9-structure", "index.html lines 37, 172; L02.html line 129; L03.html lines 51, 92; L04.html line 155 and twin lines 158-159", P,
    "Round 3: each generated stream, key set and event log is labelled SIMULATED on the page that shows it (grep of the four pages and the index).")
row("CS2-a-define-before-use", "2.9-structure", "L02.html line 51 and 57; L03.html lines 51, 57, 92; L04.html lines 52, 94, 134, 138", P,
    "Round 3: L02 line 51 names probes in plain words and points to Definition 1.2 before the definition; L03 'hold run' is defined in the Lab 3 hypothesis (line 92) before Proposition 1.5 (line 293); 'gap' (L04 line 134) and 'probe' (Definition 3.1, line 131) precede Proposition 3.2 (line 137).")
row("CS2-a-quiz-markup", "2.9-structure", "L01.html..L04.html quiz sections; course/assets/js/quiz.js unchanged", P,
    "Round 3: scripted count of data-correct per multiple-choice item (every mc item has exactly one); numeric items carry data-answer; quiz.js unchanged since 1817191.")
row("CS2-a-grades", "2.3-grades", "L01-L04 key-results tables and every data-grade", P,
    "Round 3 re-read: L02 Propositions 1.3, 1.4, 2.2, Corollary 2.3 are T and the lab row is C; L03 Propositions 1.2, 1.3, 1.5, 1.6 are T and the lab row is C; L04 Lemma 1.2, Propositions 1.3, 2.1, 3.2, Corollary 2.2 are T; L01 Propositions and lab row as in its table. Each graded claim has a proof or a lab basis.")
row("CS2-a-cards-L01", "2.7-cards", "cards.json CS2-c001..c012 against L01.html", P,
    CARRY + "cards.json entries c001-c012 (lines 1-84; the git diff hunks begin at line 171) and L01.html. Each card checked against L01: c003, c004, c006, c007, c011, c012 are T and match Propositions 1.2, 1.3, 1.6, 1.7 and Example 2.1; c009 is C naming Lab 1.")
row("CS2-a-cards-L02", "2.7-cards", "cards.json CS2-c013..c025 and CS2-c155 against L02.html", F,
    "(1) CS2-c017 (cards.json line 110) is graded T and states the consequence of Proposition 1.4 without its hypothesis 'a table of 64 buckets that stores exactly the n keys 64..64n'. Without that hypothesis the chain of bucket 0 may hold other keys, so 'makes n probes' does not follow. (2) CS2-c155 (line 1067) has basis 'Lab 2, printed averages and integer totals'. Lab 2 prints 4-decimal averages only; the integer totals are computed in the code and are not printed. The card's 257/128 and 193/64 are correct recomputations from n times the printed average (a unique integer for n <= 256). Other cards (c013-c016, c018-c025) match L02.html.",
    "(1) Add to c017: 'Assume the table has 64 buckets with this hash and stores exactly the keys 64, ..., 64n.' (2) Change the basis of c155 to 'Lab 2, printed averages; the integer totals are recovered as n times the printed average'.")
row("CS2-a-cards-L03", "2.7-cards", "cards.json CS2-c026..c039 against L03.html", F,
    "CS2-c035 (cards.json line 236) says 'From N = 64 to N = 4096, each doubling multiplies the sorted list's moves by between 3.7118 and 4.5050, and the heap's moves by between 1.9858 and 2.2331.' The lesson text says, in the Lab 3 interpretation (L03.html line 287) and in Remark 1.7 (line 314), that the ratios in 'the rows from N = 64 to N = 4096' are 3.5282 to 4.5050 for the sorted list and 1.9858 to 2.3778 for the heap. The card's window (doublings that end at 128..4096) and the lesson's window (rows 64..4096) differ, and the card's bounds 3.7118 and 2.2331 appear nowhere in the lesson text. The other L03 cards (c026-c034, c036-c039) match L03.html; c034, c038, c039 match the printed rows.",
    "Make the card and the lesson use the same window. Either change c035 to 'rows from N = 64 to N = 4096: 3.5282 to 4.5050 and 1.9858 to 2.3778' or change L03.html line 287 and Remark 1.7 to the doubling window 'from N = 64 to N = 4096 (the doublings that end at N = 128 to N = 4096)' with the 3.7118 and 2.2331 bounds.")
row("CS2-a-cards-L04", "2.7-cards", "cards.json CS2-c040..c055 against L04.html", F,
    "CS2-c047 now states all hypotheses of Proposition 2.1 (line 320): correct. But CS2-c048 (line 327) and CS2-c055 (line 376) are graded T and state the consequence of Proposition 2.1 and Corollary 2.2 for 'any comparison sort that returns the keys in increasing order' and for 'algorithms whose only operation on keys is comparison and which return the keys in increasing order', without hypotheses (2) deterministic, (3) halts on every input, and (4) every one of the n! orderings is possible; c055 also omits distinct keys. Corollary 2.2 is stated 'under the hypotheses of Proposition 2.1' (L04.html line 110), so the cards drop them. The other L04 cards match the lesson (c040-c046, c049-c054 checked).",
    "Give c048 and c055 the full hypothesis list of Proposition 2.1 (n >= 2, distinct comparable keys, deterministic, only two-outcome comparisons on keys, halts on every input, all n! orderings possible, returns the keys in increasing order on every input), or cite 'the hypotheses of Proposition 2.1'.")
row("CS2-a-cards-L01-hunks-note", "2.7-cards", "cards.json diff hunks", P,
    CARRY + "cards.json git hunks begin at line 171, so entries c001-c024 except c025 are byte-identical; this row is informational.")
row("CS2-a-dag", "2.8-dag", "index.html lines 63-64, 148; L02.html lines 104, 137, 249; L04.html lines 94, 413, 457, 517; curriculum.json", F,
    "Closure of CS2 is {CS1, M1, P0.1} (curriculum.json prereqs CS2 = [CS1, M1]). Concepts used by name in the slice that belong to modules outside that closure: 'expected value' and 'expectation' (concept key expectation, module M4) at L02.html line 104 and line 137 ('exact expectations'); 'independence' (key independence, module M4) at L02.html line 249 ('The model needs independence and uniformity'); 'decision tree' (key decision-tree, module QR3) at L04.html lines 94, 413, 457, 517 and index.html line 148. The Architect decisions allow prose-only use only for variance and quantile-function (plan section 2, Q2). They do not cover these three names, and no DAG_DEFECT entry for them exists in ledgers or plans. The other concept links resolve inside the closure or to CS2 (check_dag passes).",
    "Either log each of expectation, independence and decision-tree as a DAG_DEFECT with a plain-words definition, as the plan does for variance (plan section 2), or obtain an Architect ruling. Without that, the pages use outside concepts by name.")
row("CS2-a-hub-cards-prereqs", "2.9-structure", "index.html lines 35, 59-67, 145-155, 178-180", P,
    CARRY + "index.html. Prerequisite titles match curriculum.json (CS1 'Programming in Python from Zero', M1 'Precalculus & Mathematical Reasoning'); the placement quiz has nine items with two data-skill items; the eleven card kickers match the lesson hours for L01-L04 (8, 9, 10, 10).")
row("CS2-a-scope-words", "2.4-math", "L01-L04 and index.html scope words (only, all, every, always, same, never, any)", F,
    "Each scope word in the slice is backed by a proof or lab computation, except the footer of L04 ('Every claim carries an evidence grade'; L04.html line 630), recorded in CS2-a-L04-footer.",
    "See CS2-a-L04-footer.")
row("CS2-a-banned-phrases", "2.9-structure", "index.html; L01-L04 learner prose", P,
    "Round 3 grep: no TODO, TBD, lorem, 'for brevity', 'left as an exercise', 'roughly', 'historically', or ellipsis standing for omitted content in the slice. 'about' appears only with a computed value (for example L02 misconception 2 'about 1 + alpha/2', L03 'about 11.3').")
row("CS2-a-attributions", "2.1-citations", "L01-L04 References sections; index.html Core reading lines 175-181", P,
    "Round 3 grep: Cormen is named only in the References sections and the hub's Core reading, each saying no passage or locator is cited; no statement is attributed to it. The registry record (cormen2022introduction) has no locator.")
row("CS2-a-hours", "2.9-structure", "data-hours on index.html and L01-L04; L01-L11 total", P,
    "Round 3: declared data-hours of L01..L11 are 8, 9, 10, 10, 9, 9, 10, 10, 10, 8, 7 (L10 and L11 read from their pages), summing to 100; hub data-hours-lessons=100 and data-hours-project=30; 100/130 = 77 percent and 30/130 = 23 percent (hub bar 77 and 23). Hour targets are design targets and are not judged on pace.")
row("CS2-a-lab-L04-docstring-partB", "2.5-lab", "tests/labs/CS2/lab-CS2-L04-1.py docstring line 164-165; L04.html data-run block (same text)", F,
    "The module docstring says Part B is 'checked against the lower bound ceil(log2 n!) for any comparison sort and the merge-sort bound n * ceil(log2 n)'. Part B checks only two sorts, insertion and merge (twin lines 276-287: max_mer >= lower, max_mer <= upper, max_ins == n(n-1)/2). It does not check the lower bound for any comparison sort. The printed checks are correct, so the output is right and the docstring overstates what is checked.",
    "Change the docstring to: 'Part B: the worst case over every permutation of n = 2 to 7 for insertion sort and merge sort, compared with the lower bound ceil(log2 n!) and the merge-sort bound n * ceil(log2 n).'")

frag = {
    "unit": "CS2",
    "slice": "CS2-a",
    "round": 3,
    "round_label": "round 3 (independent re-verification of CS2-a after the round-2 fixes; delta from the round-2 pin 1817191 to aa3c26c)",
    "verifier": "independent Haiku verifier, CS2 slice a (hub index.html, L01-L04 and lab twins lab-CS2-L01-1..L04-1); did not build CS2 and shares no context with its builders",
    "pin": "aa3c26c",
    "base": "1817191 (round-2 pin; delta via git diff 1817191 aa3c26c)",
    "checkout": "/tmp/verifyB3-CS2-a (detached at aa3c26c; .venv symlinked)",
    "scratch": "/tmp/CS2-v/a3",
    "verified_at": "2026-10-28",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice a is not a project slice: no grader or project file is in it, so the mutation rule (section g), the alternative-implementation rule and tools/mutate_graders.py --unit CS2 do not apply here (architect ruling: lab twins are demonstrations, mutation testing applies to graders only). No mutants were written.",
        "Carried rows (the prefix 'Carried from round 2') cite subjects that git diff 1817191 aa3c26c shows byte-identical: index.html, L01.html, L03.html, lab-CS2-L01-1.py, lab-CS2-L03-1.py, the L01-L11 cards c001-c024 entries (hunks start at line 171), and tools/ curriculum/ references/. The twins and page commands were re-run in round 3 regardless.",
        "Not checked: project.html, grader/ and the L05-L11 pages (other slices). Page-level L10/L11 hour agreement was checked only through the hub kickers and the summed data-hours.",
        "Not checked: a fresh live verify_refs of the registry beyond the CS2 entry (the registry has 560 entries; the live run covers the one CS2 key).",
        "Sandbox: the repo tools were run without -I (the -I flag hides tools/ from sys.path and fails on import of coursekit); the twins themselves were run with -I -W error.",
    ],
    "summary": "CS2 slice a round 3: 10 FAIL rows out of 55. Round-2 FAILs now fixed and PASS: CS2-a-L02-R3-boundary, CS2-a-math-L04-prop2.1, CS2-a-L02-lab-heading-four-loads. New or still-open FAILs: DAG use of expectation, independence and decision-tree without DAG_DEFECT logs (CS2-a-dag); card CS2-c017 drops the Prop 1.4 storage hypothesis and CS2-c155 mislabels printed totals (CS2-a-cards-L02); card CS2-c035 uses a different ratio window from L03 text (CS2-a-cards-L03); cards CS2-c048 and CS2-c055 drop Prop 2.1 hypotheses (CS2-a-cards-L04); L03 Problem P2 does not cover the no-sibling case (CS2-a-math-L03-P2); L04 Prop 3.2 uses unstated monotonicity of beta (CS2-a-math-L04-prop3.2-monotone); L04 R3 omits the hypotheses its proof uses (CS2-a-math-L04-R3-hypotheses); L04 footer and scope word 'Every claim' overclaim (CS2-a-L04-footer, CS2-a-scope-words); L04 twin docstring says Part B checks the bound for any comparison sort (CS2-a-lab-L04-docstring-partB). All numbers recomputed from unrounded values match the displayed digits; all four labs' output equals their page blocks.",
}
out = ROOT / "ledgers/CS2/CS2-a.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "fails", sum(1 for r in rows if r["status"] == F))
