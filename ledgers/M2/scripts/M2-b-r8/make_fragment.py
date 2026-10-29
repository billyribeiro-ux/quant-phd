import json, sys
sys.path.insert(0, "tools")
R = []
def row(i, check, loc, status, ev):
    R.append({"id": i, "check": check, "location": loc, "status": status, "evidence": ev})
C7 = "Carried from round 7 (file byte-identical since the previous pin 7aa909e): "
TW = ("twin alone: .venv/bin/python -I -W error tests/labs/M2/lab-M2-L{n}-1.py exit 0, stderr 0 bytes, stdout {l} lines "
      "(ledgers/M2/scripts/M2-b-r8/twin_L{n}.out); run_labs --unit M2 --page L{n} -> 'run_labs M2: PASS (1/1)'; "
      "page_smoke --pages L07..L12 PASS; pytest tests/test_labs.py tests/test_run_labs.py -k M2: 27 passed; "
      "ruff check + ruff format --check clean; mypy --no-incremental on the six twins: no issues")
lines = {"07": 43, "08": 17, "09": 22, "10": 26, "11": 10, "12": 21}
for n in ["07", "08", "09", "10", "11", "12"]:
    row(f"LAB-L{n}", "2.5 labs", f"course/modules/M/M2/L{n}.html lab section; tests/labs/M2/lab-M2-L{n}-1.py",
        "PASS", TW.format(n=n, l=lines[n]) + "; page code equals twin and expected block equals output (run_labs PASS)")
row("NUM-L07", "2.2 numbers", "course/modules/M/M2/L07.html lines 204-205, 271-279, 282-288, 157 (POINTS_A), 460-470 (E2)", "PASS",
    C7 + "L07.html; re-read the cited lines in round 7 (ledgers/M2/scripts/M2-b-r7/recheck_numbers.py) and the printed lab output (L07.html 266-273, 287) matches the twin output this round.")
row("NUM-L08", "2.2 numbers", "course/modules/M/M2/L08.html lines 165-169, 185-195, 208, lab part C table", "PASS",
    "Re-derived this round in ledgers/M2/scripts/M2-b-r8/recheck_r8.py (out: recheck_r8.out): Example 2.4 bound 2^(n+2)x^(n+1) holds at 70 pairs; ratio bound/exact = 2^(n+2)(1-x) in [2^(n+1),2^(n+2)); M3 128/27, bound 4/27, exact 1/12; xi E1 0.1294494, E2 0.0496772, M2 0.0693951; E3 bounds 5.625, 8.4375, 12.65625, 18.984375 and remainders 0.9, 0.54, 0.324, 0.1944; R3 bound 2 at x=1/2 for each n. Only L08 hunk: lab docstring lines 136-139 (no number changed).")
row("NUM-L09", "2.2 numbers", "course/modules/M/M2/L09.html lines 166-169, 202-210, 215-221, 88-93 (Remark 1.4 edit)", "PASS",
    C7 + "L09.html (round-7 re-derivation in ledgers/M2/scripts/M2-b-r7/recheck_numbers.py).")
row("NUM-L10", "2.2 numbers", "course/modules/M/M2/L10.html line ~347 (Problem L10-E3 solution), lines 370-372 (E1, E2)", "PASS",
    C7 + "L10.html (round-7 re-derivation); L10.html changed nowhere in the delta 7aa909e..ce7b382 (the lab twins and cards for L10 changed only by the new card M2-c389, which states Theorem 1.2 and is checked under CARDS-L07-L12).")
row("NUM-L11", "2.2 numbers", "course/modules/M/M2/L11.html lines 300-330 (E1, E2, E3), Lab part A/B expected block", "PASS",
    "Re-derived this round (recheck_r8.out): E1 smallest N with 2/(3N^2) <= 1e-6 is 817 (816 gives 1.0012e-6, 817 gives 9.988e-7); E2 residual 2.6666666667-2.6666666663 = 4e-10; E3 1/2 * 1/30 = 1/60 = 0.0166666667; part A/B/C expected values equal the twin output. Cited lines 300-330 are byte-identical since the previous pin; the delta hunks in L11 (lines 132-135, 226-229, 243-247, 416-420) do not touch them.")
row("NUM-L12", "2.2 numbers", "course/modules/M/M2/L12.html lines 164, 186, 190, 192-194, 296-330 (P1, E1-E3), Lab part C", "PASS",
    C7 + "the cited lines 164-194 and 296-330; the only L12 hunk since the previous pin is line 364 (R3 solution, notation L(f,P) only), re-derived under MATH-L12; lab part C output matches the twin.")
row("MATH-L07", "2.3 math", "course/modules/M/M2/L07.html Prop 1.4, Lemma 1.6, Prop 2.3, Lemma 3.1, Thm 3.2, Ex 4.1, Prop 4.2, Remark 4.3, R1, R3, quiz", "PASS",
    C7 + "L07.html; Lemma 3.1 proof (L07.html 319-328) read this round and supplies the Bernoulli inequality (1+h)^m >= 1+mh that L08 R2 cites.")
row("MATH-L08", "2.3 math", "course/modules/M/M2/L08.html Lemma 1.1, Thm 1.2, Thm 2.1 proof, Cor 2.2, Ex 2.3, Ex 2.4, Remarks 3.1-3.3, R1, R2, R3, Misconceptions, quiz", "PASS",
    "Whole L08.html read this round (lines 30-487). Re-verified: Thm 1.2 = Rolle with h(p)=h(q) (Lesson 6 Thm 2.2 cited; L06.html line 77); Thm 2.1 proof steps (g(x)=0, g(x0)=0, Rolle chain, K = f^(n+1)(xi)/(n+1)!); Cor 2.2; Ex 2.3 (xi=1-(1-x)^(1/(n+2)) in (0,x)); Ex 2.4 M=(n+1)!2^(n+2) gives 2^(n+2)x^(n+1) on [0,1/2]; Remark 3.3 numbers; M1 (x^4 at 1: P3 and remainder (x-1)^4); M2 P_2(1/4)=21/16, R=1/48, xi=0.0693951; M3 4/27 vs 1/12; P2 c^(1/m) in (c,1); R1 Bernoulli; R2 r=x/(1-x), threshold x<1/2 (uses L07 Lemma 3.1 proof); R3. Lesson 7 Definition 2.1 and Prop 2.3 cited as used (L07.html 106, 118).")
row("MATH-L09", "2.3 math", "course/modules/M/M2/L09.html Lemmas 1.1-1.2, Def 1.3, Thm 2.2 proof, Cor 2.3, Ex 3.2 (lines ~110-130), Misc 2 (line ~260), R1-R3", "PASS",
    C7 + "L09.html (Thm 2.2 monotone integrands at L09.html 99-112 re-read this round; it is the citation used by L11 Example 3.3).")
row("MATH-L10", "2.3 math", "course/modules/M/M2/L10.html Thm 2.1 proof, Ex 2.2, Cor 3.1 (lines ~80-100), Prop 4.1, Misc 2 G(x)=x/(1+x)+5, R1-R3", "PASS",
    C7 + "L10.html; Thm 1.2 (MVT, L10.html 62-63) re-read this round and matches card M2-c389.")
row("MATH-L11", "2.3 math", "course/modules/M/M2/L11.html line 134 (Example 3.3 integrability of f on [1,2]); Corollary 1.2 line 73 (integrable on [0,b], b>0); Examples 2.2, 2.3, 3.2, 3.3; Problems P1-P3, M1-M3, R1-R3", "PASS",
    "Previous FAIL (Example 3.3 cited Corollary 1.2 for [1,2]) is fixed: L11.html line 134 now cites Lesson 9, Theorem 2.2 (monotone integrands, L09.html 99-101: monotone on [a,b] implies integrable), which applies to f=x on [1,2]. Re-derived: Ex 2.2 u'v=-x(1-x)^4/2, uv'=x^2(1-x)^3, boundary 0, int = 1/60 (1/30 via 1/2-4/3+3/2-4/5+1/6); Ex 2.3 boundary term 1, int x = 1/2; Ex 3.2 integrand 3t^8+7t^6+5t^4+t^2, int 8/3; Ex 3.3 int_1^2 x = 3/2, integrand 2t+2t^3 int_0^1 = 3/2; M1 1/12; M2 7/3; M3 3/2*1/30 = 1/20; P2 linear substitution; P3; R1 Beta recursion I(m,n+1)=(n+1)/(m+1) I(m+1,n) checked by script on 25 pairs; R2 scaling; R3 composite 2t^3, int 1/2 both sides. Remark: Corollary 1.2 wording (b>0) matches its use.")
row("MATH-L12", "2.3 math", "course/modules/M/M2/L12.html Lemma 2.1 proof (lines ~140-146), Problem L12-P1 solution (line ~364 changed: L(f, P) notation), Thm 2.2 proof, Thm 3.3, Lemma 3.1-3.2, R1-R3", "PASS",
    "Only L12 hunk since the previous pin is line 364 (solution of the series problem): it now writes L(f, P) for the lower sum of the unit partition. Re-derived: sum_{k=2}^N k^-p <= int_1^N x^-p dx <= 1/(p-1) (decreasing f, lower sum below integral); printed check ledgers/M2/scripts/M2-b-r8/recheck_r8.out gives partial sums 0.644434 (p=2) and 0.202057 (p=3) below 1/(p-1). Remaining L12 cited lines are byte-identical to 7aa909e and carried from round 7 (C7 prefix: L12.html lines 140-146, 296-330, 164-194, 216, 242, 27, 460 unchanged).")
row("PROSE-L09-monotone", "2.1 prose", "course/modules/M/M2/L09.html Remark 1.4 (line ~45-47 and 88-93)", "PASS",
    C7 + "L09.html.")
row("ASSUME-L12-monotone-convergence", "2.1 assumption", "course/modules/M/M2/L12.html why-it-matters (line ~27), Problem L12-R3 statement (line ~362), references (line ~460), key-results row", "PASS",
    C7 + "the cited lines are byte-identical; the only L12 hunk (line 364, R3 solution) does not touch them. The assumption is stated as a named assumption (Assumption 2.2) and is not used as a proved fact elsewhere in the slice.")
row("SCOPE-L12-integer-exponents", "2.1 scope", "course/modules/M/M2/L12.html Section 4 bullet 2 (line ~242), Remark 3.4 (line ~216)", "PASS",
    C7 + "the cited lines are byte-identical; the only L12 hunk is at line 364.")
row("NOTATION-L07-L12", "2.4 notation", "course/modules/M/M2/L07-L12.html math spans; notation/notation.json (symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}; macros \\E, \\Prob, \\R, ...)", "PASS",
    "Re-run this round: scan of all math spans in L07-L12 found no use of T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}, \\E, \\Prob, \\Var, \\Cov, \\Corr, \\N, \\indic, \\Normal, \\iid, \\dto, \\pto, \\argmax, \\argmin, \\tr, \\diag, \\SR, \\se, \\emgamma. Plain R (Riemann sums, L09 and L11) and plain Q (partitions, L09) are not registered symbols (\\mathbb{Q} is registered; plain Q is not). Lesson-local L(f,P), U(f,P), R_n, P_n, I(m,n) are defined in-lesson (L09 Def 1.3; L11 Thm 2.1 proof) and are not registered letters. The new L12 notation L(f, P) (line 364) matches L09 usage.")
row("DAG-L07-L12", "2.4 DAG", "tools/check_dag.py --unit M2; concept links in L07-L12", "PASS",
    "Run this round: check_dag --unit M2 -> 'check_dag M2: PASS'. The delta adds no new concept link or def; new Example 2.4 wording (L08 docstring) and L11 'Lesson 9, Theorem 2.2' are prose references to lesson-prerequisite results already in the closure (L09 is in L11's closure).")
row("CARDS-L07-L12", "2.6 cards", "course/modules/M/M2/cards.json: cards with lesson L07..L12 (107 cards: L07 22, L08 19, L09 18, L10 16, L11 16, L12 16); M2-c093 (L07), M2-c388 (L08), M2-c389 (L10), M2-c163 (L11)", "FAIL",
    "Changed cards re-read against lessons: M2-c093 now 'x = 3/10, -1/2 and 9/10 ... (27 checks)' matches L07.html line 157 POINTS_A (three points, 9 values of k = 27 checks) and printed 'part A: formula equals recursion at all 27 checks (x in 3/10, -1/2, 9/10; k = 0 to 8)' (L07.html 196, 266) -> PASS. M2-c388 (Rolle, Assumption 1.1, p<q, h(p)=h(q), h'(c)=0, p<c<q) matches L08.html Theorem 1.2 (line 76-77) -> PASS. M2-c389 (MVT, Assumption 2.1 of L06, p<q, continuous/differentiable, h(q)-h(p)=h'(c)(q-p)) matches L10.html Theorem 1.2 (line 62-63) -> PASS; no duplicate of M2-c134 or M2-c099 (different content). M2-c163 back (cards.json line 1166): 'The worked examples check it: polynomials on [0, b] with b > 0 (Corollary 1.2), monotone functions (Lesson 9, Theorem 2.2), and sums and scalar multiples of integrable functions (Lemma 1.1)'. The Lemma 1.1 clause is false for the worked examples: Examples 2.2, 2.3, 3.2 and 3.3 (L11.html 95-135) cite Corollary 1.2 or Lesson 9 Thm 2.2 only; Lemma 1.1 is cited in the Theorem 2.1 proof (line 92), P2 and P3 solutions, not in a worked example. FAIL. Other 104 slice cards were not changed since 7aa909e (cards.json diff hunks listed in notes) and were re-checked against their lessons where the lesson changed (L08 docstring and L11 lines 134, 226-228, 245, 418 do not alter any card statement except c163).")
row("STRUCT-L07-L12", "2.6 structure", "L07-L12 headers, Misconceptions, Problem set (tiers mechanics/proof/empirical/research), Retrieval quiz, Key results, References", "PASS",
    "Whole L08 and L11 read this round; section numbering 1-9 consistent; misconception list present (3 items in L08 and L11); problem tiers present; quiz sections present with data-correct markers; key-results tables present; references sections present; data-hours=\"10\" once per page in L07-L12 (grep). L11 quiz prompt L11q7 reworded to 'in the worked examples' with explain text 'Misconception 3' still correct.")
row("SMOKE-L07-L12", "2.6 smoke", "tools/page_smoke.py --unit M2 --pages L07 L08 L09 L10 L11 L12 (run alone)", "PASS",
    "Run this round: page_smoke modules/M/M2/L07..L12.html each PASS; 'page_smoke M2: PASS'.")
row("GRADE-L07-L12", "2.6 grades", "data-grade markers in L07-L12 bodies", "PASS",
    "Changed hunks contain no data-grade markup (checked in the diff: L08 line 136-139 docstring; L11 lines 134, 226-228, 245, 418). L08 and L11 grade markers read in full this round: Lemma 1.1, Theorem 1.2, Theorem 2.1, Corollary 2.2, Example rows and key-results T grades match the body.")
row("CROSSREF-L07-L12", "2.4 cross-reference", "lesson-number and theorem-number citations in L07-L12 (see DAG row)", "PASS",
    "Changed citations checked: L08 'Example 2.4 of this lesson (Corollary 2.2 with M = (n+1)! 2^(n+2))' -> L08.html 123-124 exists and states it; L11 'Lesson 9, Theorem 2.2' -> L09.html 99 (monotone integrands) PASS; L11 'Lesson 9 Theorem 2.2' and 'Lesson 10 Corollary 3.1' remain as before; L08 Remark 1.3 'Theorem 2.3 of Lesson 6' (L06.html 87 MVT) PASS; L08 Assumption 1.1 'Assumption 2.1 of Lesson 6' (L06.html 70-71 EVT) PASS.")
row("BANNED-L07-L12", "2.6 filler", "BUILDER_RULES 1.3-1.4 phrase list and filler words, L07-L12 bodies", "PASS",
    "Added lines of the delta (git diff 7aa909e..ce7b382 for L08, L11, L12, cards, lab-M2-L08) grepped for process words (round, fix, verif, updated, previous, revis, now, corrected, earlier): no hit in learner text; the L11 new prose is read in full (lines 134, 228, 245, 418).")
row("CLAIM-L11-each-application-checks", "2.3 claim vs proof", "course/modules/M/M2/L11.html Misconception 3 (line 245) and quiz prompt (line 418); cards.json M2-c163 back", "FAIL",
    "The round-7 defect ('Each application checks it', unchecked in Problems L11-M1, M3, R1 and M2) is removed: the text now says 'The worked examples check it', and the four worked examples do check integrability (polynomials by Corollary 1.2 and monotone f=x by Lesson 9 Thm 2.2). The remaining sentence, 'using ... sums and scalar multiples of integrable functions (Lemma 1.1)', is not supported by any worked example: Example 2.2 (L11.html 97), Example 2.3 (104), Example 3.2 (129) and Example 3.3 (134) cite only polynomial integrability and monotonicity. Lemma 1.1 appears in the Theorem 2.1 proof (line 92), Problem P2 and P3 solutions, not in an Example. Fix: delete the clause '(Lemma 1.1)' phrase 'and sums and scalar multiples of integrable functions (Lemma 1.1)' from L11.html line 245 and from cards.json M2-c163 back (or state that the proofs, not the worked examples, use Lemma 1.1), then re-run the card check.")
FIX = {
 "CARDS-L07-L12": "Delete the Lemma 1.1 clause ('and sums and scalar multiples of integrable functions (Lemma 1.1)') from cards.json M2-c163 back, or reword it to say the proofs (not the worked examples) use Lemma 1.1; then re-run the card check.",
 "CLAIM-L11-each-application-checks": "Delete the Lemma 1.1 clause ('and sums and scalar multiples of integrable functions (Lemma 1.1)') from course/modules/M/M2/L11.html Misconception 3 (line 245), or reword it to say the proofs use Lemma 1.1; then re-run check_pages and the cards check.",
}
for r in R:
    if r["status"] != "PASS":
        r["fix"] = FIX[r["id"]]
frag = {
    "unit": "M2", "slice": "b", "round": 8,
    "verifier": "independent Haiku verifier, M2 slice b (L07-L12 and lab twins), round 8; fresh context",
    "pin": "ce7b3821c288da3dbba5dd4c90fb87dfd6d30089",
    "base": "7aa909e95b757b1abf7b75186d5fa1ed7d1945a4 (round-7 pin, fragment B-M2-b.round7.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyB8-M2-b",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyB8-M2-b/ledgers/M2/scripts/M2-b-r8",
    "verified_at": "2026-10-28T00:00:00Z",
    "verdict": "FAIL",
    "rows": R,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [
        "cards.json: slice now holds 107 cards with lesson L07..L12 (round-7 said 105): two new cards M2-c388 (L08) and M2-c389 (L10) were added since the round-7 pin; M2-c290 (L19), M2-c344 and M2-c356 (L23) were removed (outside the slice). Round-7 PASS rows that cited 105 are superseded.",
        "L12.html changed at line 364 (R3 solution: L(f,P) notation); L08.html changed at lab docstring lines 136-139; L11.html changed at lines 134, 226-228, 245, 418; project.html, L13, L16, L17, L19, L20, L22, L23 and lab-M2-L13 changed outside the slice and were not read."
    ],
    "notes": [
        "Scope: slice b, L07-L12 pages and twins tests/labs/M2/lab-M2-L07-1.py..lab-M2-L12-1.py at pin ce7b382. Round delta since 7aa909e read in full: L08.html (1 hunk), L11.html (4 hunks), L12.html (1 hunk), cards.json (M2-c093, M2-c163 changed; M2-c388, M2-c389 added), lab-M2-L08-1.py (docstring). L08.html and L11.html were re-read entirely (not only the hunks) because they changed; L07, L09, L10 pages and L12 except line 364 are byte-identical since 7aa909e and their PASS rows are carried with the round-7 evidence.",
        "Commands run on ce7b382 (outputs under ledgers/M2/scripts/M2-b-r8/): check_pages --unit M2 PASS; check_dag --unit M2 PASS; run_labs --unit M2 --page L07..L12 each PASS (1/1); twins alone under python -I -W error: exit 0, stderr 0 bytes, stdout 43/17/22/26/10/21 lines; page_smoke --unit M2 --pages L07..L12 PASS; ruff check and ruff format --check on tests/labs/M2 clean; mypy --no-incremental on the six twins: no issues; pytest tests/test_labs.py tests/test_run_labs.py -k M2: 27 passed; verify_refs --offline: 560 entries, 0 problems; check_projects --unit M2 PASS.",
        "Not a grader slice: no project grader is in this slice, so no student-error mutants or alternative implementations were run; mutants list empty by design (the lab ruling in verifier-rules). Lab twins were not mutated.",
        "Could not check: the M2 hub and project pages and the M2 graders (other slices); the BLUEPRINT grade-definition text beyond the legend; the L06, L07 and L10 statements cited from other lessons were checked only at the cited theorem line, not re-proved (they are not in this slice). No published source is cited in the slice.",
        "Fix list for the two FAIL rows: drop the Lemma 1.1 clause from L11.html line 245 and cards.json M2-c163 back (or reword it to say the proofs use Lemma 1.1). No other change is required by this round."
    ],
    "summary": "M2-b round 8 on pin ce7b382: 30 rows, 28 PASS, 2 FAIL (CLAIM-L11-each-application-checks and CARDS-L07-L12, both the same Lemma 1.1 clause in L11 Misconception 3 and card M2-c163); verdict FAIL. Round-7 MATH-L11 and c093 defects are fixed and re-verified."
}
import ledger
probs = ledger.validate(frag, "M2-b")
print("validate:", probs)
json.dump(frag, open("ledgers/M2/M2-b.json", "w"), indent=1, ensure_ascii=False)
from collections import Counter
print(Counter(r["status"] for r in R), len(R))
