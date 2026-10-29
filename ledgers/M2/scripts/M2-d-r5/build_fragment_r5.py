"""Builds the round-5 fragment for slice M2-d from the round-4 fragment and this round's re-verification.

Usage: python -I build_fragment_r5.py <output json path>
Every round-4 row id is re-decided here; carried PASS rows state the byte-identical subject.
"""
import json
import sys

R4 = "/tmp/fanout-frags/B-M2-d.round4.json"
OUT = sys.argv[1]
r4 = json.load(open(R4, encoding="utf-8"))
old = {r["id"]: r for r in r4["rows"]}
NEW: dict[str, dict] = {}


def new(rid, status, location, evidence, fix=None, check=None):
    row = {
        "id": rid,
        "check": check or (old[rid]["check"] if rid in old else "cards agree with the current lesson text (slice M2-d)"),
        "location": location,
        "status": status,
        "evidence": evidence,
    }
    if status != "PASS":
        row["fix"] = fix
    NEW[rid] = row


def carry(rid, subject, extra=""):
    prev = old[rid]
    NEW[rid] = {
        "id": rid,
        "check": prev["check"],
        "location": prev["location"],
        "status": "PASS",
        "evidence": "Carried from round 4 (" + subject + " byte-identical since the previous pin):" + " " + prev["evidence"] + extra,
    }


# ---- command rows: re-run this round on 09b8751 ----
new("M2-d-cmd-check-pages", "PASS", "course/modules/M/M2/L19.html ... L24.html",
    "Round 5: .venv/bin/python tools/check_pages.py --unit M2 -> 'check_pages M2: PASS'; per page "
    "tools/check_pages.py --unit M2 --page Lnn -> 'check_pages M2 Lnn: PASS' for L19..L24.")
new("M2-d-cmd-check-dag", "PASS", "course/modules/M/M2/ (slice links and dfn ids)",
    "Round 5: tools/check_dag.py --unit M2 -> 'check_dag M2: PASS'.")
new("M2-d-cmd-run-labs", "PASS", "tests/labs/M2/lab-M2-L19-1.py ... lab-M2-L24-1.py",
    "Round 5: tools/run_labs.py --unit M2 --page Lnn for L19..L24 -> 'run_labs M2: PASS (1/1)' six times.")
new("M2-d-cmd-twins-isolated", "PASS", "tests/labs/M2/lab-M2-L19-1.py ... lab-M2-L24-1.py",
    "Round 5: cd /tmp && /tmp/verifyB5-M2-d/.venv/bin/python -I -W error tests/labs/M2/lab-M2-Lnn-1.py for L19..L24: "
    "rc=0 and 0 bytes of stderr each; stdout saved in /tmp/M2-v/d-r5/Lnn.out.")
new("M2-d-cmd-expected-match", "PASS", "course/modules/M/M2/L19.html ... L24.html (pre.expected)",
    "Round 5: ledgers/M2/scripts/M2-d-r5/exp_match.py: the embedded pre.expected block equals the fresh twin stdout "
    "for L19..L24 (True six times). The L22 block now prints x_hat, matching the changed twin.")
new("M2-d-cmd-embed-match", "PASS", "course/modules/M/M2/L19.html ... L24.html (data-run block)",
    "Round 5: tools/run_labs.py --unit M2 (same run as M2-d-cmd-run-labs) reports each data-run block byte-identical "
    "to its tests/labs/M2 twin (PASS for each page).")
new("M2-d-cmd-page-smoke", "PASS", "tools/page_smoke.py --unit M2 --pages L19 L20 L21 L22 L23 L24 --skip-sweep",
    "Round 5: 'page_smoke M2: PASS'; each of L19..L24 reports PASS in the run.")
new("M2-d-cmd-ruff-mypy", "PASS", "tests/labs/M2/",
    "Round 5: ruff check tests/labs/M2/ -> 'All checks passed!'; ruff format --check -> '27 files already formatted'; "
    "mypy --no-incremental tests/labs/M2/ -> 'Success: no issues found in 27 source files'.")
new("M2-d-cmd-pytest-labs", "PASS", "tests/test_labs.py, tests/test_run_labs.py (-k M2)",
    "Round 5: .venv/bin/python -m pytest -k M2 tests/test_labs.py tests/test_run_labs.py -> '27 passed, 208 deselected'.")
new("M2-d-cmd-verify-refs", "PASS", "references/references.json (keys spivak2008calculus, hubbard2015vector)",
    "Round 5: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems'; "
    "tools/verify_refs.py --unit M2 -> 'live re-verification of M2: 2 of 560 entries, 0 problems'.")
carry("M2-d-2.1-keys-used", "the References sections of L19-L21, L23 and L24 (no hunk in git diff 2657ab5..09b8751); L22's References paragraph was re-read this round (line 458)")

# ---- numbers ----
new("M2-d-num-L19", "PASS", "course/modules/M/M2/L19.html Lab 1 interpretation; Misconception 2; Remark 3.2",
    "Round 5 recomputation (ledgers/M2/scripts/M2-d-r5/recheck_r5.py, from the printed errors): first-order ratios "
    "6.215110e-03/1.573092e-03 = 3.9509, 1.573092e-03/3.957416e-04 = 3.9750, 3.957416e-04/9.924735e-05 = 3.9874; second-order "
    "ratios 7.8836, 7.9429, 7.9717 (match the page). Hessian f_xx = e^0.5/4 = 0.412180, f_xy = e^0.5 + 0.5 = 2.148721, f_yy = 1 "
    "(recomputed). The printed 2.26e-11 and 1.94e-11 are from the lab run this round. Remark 3.2 coefficient of d1*d2 re-derived.")
new("M2-d-num-L20", "PASS", "course/modules/M/M2/L20.html Proposition 2.2 proof; Theorem 1.2; Proposition 2.4; Lab 1; E1 to E3",
    "Round 5: the changed Proposition 2.2 proof re-derived: int_0^2 (xy + x^2) dy = 2x + 2x^2 (x*2^2/2 = 2x, x^2*2 = 2x^2), "
    "int_0^1 (2x + 2x^2) dx = 1 + 2/3 = 5/3; int_0^1 (xy + x^2) dx = y/2 + 1/3, int_0^2 (y/2 + 1/3) dy = 1 + 2/3 = 5/3. "
    "Lab 1 output re-run this round equals the embedded block (M2-d-cmd-expected-match). Theorem 1.2 and Proposition 2.4 carried from round 4 "
    "(no hunk in those passages; the Theorem 1.2 proof sums 1/2*2 + 1/3*2 = 5/3 re-derived).")
new("M2-d-num-L21", "PASS", "course/modules/M/M2/L21.html Lab 1 interpretation; E2; Example 2.2",
    "Carried from round 4 (the Lab 1 interpretation, E2 and Example 2.2 passages of L21 byte-identical since the previous pin; the L21 hunks are at Definition 1.1 and Research R3 only): "
    + old["M2-d-num-L21"]["evidence"] + " Round 5: the lab output re-run equals the embedded expected block (M2-d-cmd-expected-match).")
new("M2-d-num-L22", "PASS", "course/modules/M/M2/L22.html Lab 1 interpretation; misconception 3; E1; E3",
    "Round 5 re-run of tests/labs/M2/lab-M2-L22-1.py (labels now x_hat): x_hat = 0.50000001 at a = 1.5; Part A central differences equal ln a to 8 printed decimals "
    "(0.40546511, 0.69314718, 1.09861229, 1.38629436); Part B max error 5.4e-12 (1.9e-13, 1.0e-12, 5.4e-12). f_xx = -a/(1+x)^2 = -0.666667 at a = 1.5; "
    "0.5*0.666667*1e-16 = 3.33e-17 (page 3.3e-17). sqrt(2.22e-16) = 1.49e-8 (page 'about 10^-8'). E1 'about 10^-16' for 3.3e-17 is the nearest power of ten (log10 = -16.5).")
new("M2-d-num-L23", "PASS", "course/modules/M/M2/L23.html Lab 1 interpretation; Abstract; E3",
    "Round 5: ledgers/M2/scripts/M2-d-r4/check_L23.py re-run (independent check): ratio1 3.9278538, 3.9634380; ratio2 7.8807039, 7.9396267 "
    "(page 3.9279, 3.9634, 7.8807, 7.9396); P(0.04) = 108110.895779 cents, integer 108111 (lab output re-run). Proposition 3.3 grid check True. "
    "Only the R2 solution changed; it states no number.")
carry("M2-d-num-L24", "the Lab 1 output and Remark 4.4 passages of L24 (the only L24 hunk is the why-it-matters paragraph)")

# ---- grades and math ----
new("M2-d-grade-L19-L20-L22-L23-L24", "PASS", "course/modules/M/M2/L19.html ... L24.html (grade spans, key-results tables)",
    "Round 5: key-results tables re-read: L19 (lines 391-394), L20 (348-351, unchanged), L22 (380-383), L23, L24. Each T row is a proof on the page "
    "or a computed example; the T rows of L22 (Lemma 1.2, Theorem 1.3, Proposition 2.1, Example 2.3) were re-derived this round.")
new("M2-d-grade-L21-assumed-result", "PASS", "course/modules/M/M2/L21.html Theorem 1.2 (data-grade T) and its proof",
    "Round 5: Theorem 1.2 statement and proof re-read (L21 lines 62-72). The statement gives 'a unique function g: I -> J'; the proof shows exactly one zero in J "
    "for each x (strict monotonicity in y), which is what the amended Definition 1.1 says. Grade T is supported by the page.")
new("M2-d-math-L19-thm2.1", "PASS", "course/modules/M/M2/L19.html Theorem 2.1 and proof; Example 2.2",
    "Round 5: Theorem 2.1 proof (Steps 1-3) and Example 2.2 re-read in full (L19 lines 72-95). Example 2.2: f_x(0,y) = -y and f_y(x,0) = x, so "
    "f_xy(0,0) = -1 and f_yx(0,0) = 1 (re-derived); the continuity of f_xy at the origin is the hypothesis that fails.")
new("M2-d-math-L19-thm3.1-prop3.3", "PASS", "course/modules/M/M2/L19.html Theorem 3.1, Remark 3.2, Proposition 3.3 and proof",
    "Round 5: Theorem 3.1 statement and proof re-read (lines 97-112): phi(1) = s1 * phi''(s2), so |phi(1)| <= sup|phi''|; "
    "|h^T M h| <= (|h1| + |h2|)^2 max|M_ij| <= 2|h|^2 max|M_ij| (re-derived). The hypotheses (twice differentiable on N, H continuous at p) are the ones the proof uses. "
    "Proposition 3.3: E(s)/E(s/2) = (g'''(0)s^3/6)/(g'''(0)s^3/48) -> 8 (re-derived).")
new("M2-d-math-L19-solutions", "PASS", "course/modules/M/M2/L19.html problem set M1-M3, P1-P3, E1-E3, R1-R3 and quiz answers",
    "Round 5: the changed R2 (three-variable) solution re-derived: |h^T M h| <= (sum|h_i|)^2 max|M_ij| <= 3|h|^2 max|M_ij| by Cauchy-Schwarz "
    "(sum|h_i| <= sqrt(3)|h|), so the constant is n = 3 and the mean value step is unchanged. Other solutions carried from round 4 (no hunk).")
carry("M2-d-math-L19-misconception2", "the Misconception 2 passage of L19")
new("M2-d-math-L20-thm1.2-prop2.2-2.4", "PASS", "course/modules/M/M2/L20.html Theorem 1.2, Proposition 2.2, Proposition 2.4",
    "Round 5: the changed Proposition 2.2 proof (y integrated first, then x) re-derived: 2x + 2x^2 then 5/3; y/2 + 1/3 then 5/3 (see M2-d-num-L20). "
    "Theorem 1.2 and Proposition 2.4 carried from round 4 (no hunk in those passages).")
carry("M2-d-math-L20-def-not-apply", "the Section 3 and Example 3.1 passages of L20 (file hunks are at Definition 1.1 and the Proposition 2.2 proof only)")
carry("M2-d-math-L20-scope", "the L20 introduction and Section 3 passages")
carry("M2-d-math-L21-thm2.1-ex3.2", "the Theorem 2.1 and Example 3.2 passages of L21 (no hunk); the Theorem 1.2 proof was re-read this round")
carry("M2-d-math-L21-R1-hypothesis", "the Research R1 statement and solution of L21")
new("M2-d-math-L22-lemma-thm1.3-ex1.5", "PASS", "course/modules/M/M2/L22.html Lemma 1.2, Theorem 1.3, Remark 1.4, Example 1.5",
    "Round 5: all re-read (lines 62-94; notation changed to x_hat only). Example 1.5: f_x = a/(1+x) - 1 zero at a - 1, f_xx = -a/(1+x)^2 < 0, "
    "V = a ln a - (a - 1), V' = ln a, f_a(x_hat) = ln a (re-derived). Remark 1.4 cites the L21 Theorem 1.2 statement, which gives the unique g: I -> J.")
new("M2-d-math-L22-proposition-2.1-ex2.2-2.3", "PASS", "course/modules/M/M2/L22.html Proposition 2.1, Example 2.2, Example 2.3, Problems M1-M3, P1-P3",
    "Round 5: re-read (lines 223-248, 276-320). Proposition 2.1 proof and Example 2.2 (V = a^2/4, V' = a/2, f_y c_a = a/2) re-derived. "
    "Example 2.3: V = max(a,0), one-sided derivatives 1 and 0 (re-derived). M1: V = a^2/2, V' = a. M2: V = 3a + 9/4, V' = 3. M3: y* = a/4, V = a^2/8, V' = a/4. P1-P3 re-checked.")
new("M2-d-math-L23-prop2.1-3.1-3.2-3.3", "PASS", "course/modules/M/M2/L23.html Proposition 2.1, Theorem 3.1, Proposition 3.2, Proposition 3.3 and proofs",
    "Round 5: re-read (lines 67-244). P'' = sum t(t+1) c_t (1+y)^(-t-2) and P''' = -sum t(t+1)(t+2) c_t (1+y)^(-t-3) re-derived; Theorem 3.1 remainder "
    "R = P'''(theta) Delta^3/6 gives |R| <= M|Delta|^3/6; Proposition 3.2 gives sign R = sign(-Delta); Proposition 3.3 gives P(y0+D) - P1(D) = P''(theta) D^2/2 >= 0.")
new("M2-d-math-L23-prop2.2", "PASS", "course/modules/M/M2/L23.html Proposition 2.2 statement and proof",
    "Round 5: statement (N >= 1, F > 0, y > -1, coupons yF, face F added to the last coupon: price F at yield y) and proof re-derived: "
    "v = 1/(1+y), 1 - v = yv, sum v^t = (1 - v^N)/y, so yF sum v^t + F v^N = F. The y > -1 hypothesis is the one that makes v defined.")
carry("M2-d-math-L23-quiz-essential", "the L23 quiz item L23q8 and its explanation")
carry("M2-d-math-L24-prop3.1-3.2-thm2.1", "the Theorem 2.1 and Propositions 3.1 and 3.2 passages of L24 (hunks at the why-it-matters paragraph only)")
new("M2-d-math-L24-prop4.2-4.3", "PASS", "course/modules/M/M2/L24.html Propositions 4.2 and 4.3 and their proofs",
    "Round 5: Proposition 4.2 statement and proof re-read (lines 105-114): |computed D+ - f'| <= (1/2) M2 h + 2 delta/h; minimiser h* = 2 sqrt(delta/M2) "
    "with value 2 sqrt(M2 delta), re-derived from g(h) = A h + B/h with A = M2/2, B = 2 delta. Proposition 4.3 carried from round 4 (no hunk).")
carry("M2-d-math-L24-derivative-def", "the Section 1 passage of L24 (no hunk in Section 1 in this delta)")
carry("M2-d-math-L24-R1-R2-solutions", "the Research R1 and R2 solutions of L24")
carry("M2-d-math-L20-def-not-apply-2", "the L20 Problems M1-M3, P1-P3 and R1-R3 passages")

# ---- labs ----
new("M2-d-lab-L19", "PASS", "course/modules/M/M2/L19.html Lab 1 hypothesis, interpretation; tests/labs/M2/lab-M2-L19-1.py",
    "Round 5: the hypothesis now says the printed ratios 'bear on that point only indirectly'; the code computes f, its gradient, Hessian and the Taylor errors and not g'''(0), as the page says. "
    "The predictions (0.41218, 2.14872, 1, Hessian to 1e-10) match the run (2.26e-11). Ratios recomputed (M2-d-num-L19).")
carry("M2-d-lab-L20-overreach", "the L20 Lab 1 interpretation and E2 passages (lab twin byte-identical)")
carry("M2-d-lab-L21", "the L21 Lab 1 hypothesis and interpretation passages (the L21 hunks are at Definition 1.1 and R3)")
new("M2-d-lab-L22-count", "PASS", "course/modules/M/M2/L22.html Lab 1 interpretation and last sentence; lab-M2-L22-1.py",
    "Round 5: 'Part A at four values of a and Part B at three' matches PARAMETERS_A (4 entries) and PARAMETERS_B (3 entries); "
    "'tests no other objectives' matches main() (two loops only).")
new("M2-d-lab-L22-naive-constant", "PASS", "course/modules/M/M2/L22.html Lab 1 hypothesis; lab-M2-L22-1.py line 198 naive_partial = 0.0",
    "Round 5: naive_partial is the literal 0.0 (twin line 198, with the comment 'x * y has no a in it'), so the printed 0.00000000 is a constant rather than a computed partial. "
    "The page states the naive partial is zero, which is the correct mathematics, and does not present the value as computed. Accepted as a demonstration.")
carry("M2-d-lab-L23", "the L23 Lab 1 hypothesis and interpretation passages (the only L23 hunk is R2)")
carry("M2-d-lab-L24", "the L24 Lab 1 hypothesis and interpretation passages and the twin")

# ---- prose ----
new("M2-d-prose-L19-schwarz", "PASS", "course/modules/M/M2/L19.html Misconception 3 heading; Section 4 bullets 1-2",
    "Round 5: Section 4 bullet 1 (now 'an arbitrary function whose second partials exist') is supported by Example 2.2, where f_xy(0,0) = -1 != 1 = f_yx(0,0) (re-derived). "
    "Bullet 2 and Misconception 3 re-read: symmetry needs the continuity hypothesis; a finite-difference table is not a proof.")
carry("M2-d-prose-L19-central-difference", "the Section 4 bullet 2 and the Lab 1 hypothesis passages of L19")
new("M2-d-prose-L19-hypothesis-count", "PASS", "course/modules/M/M2/L19.html Section 4 introduction and bullet 3",
    "Round 5: Section 4 introduction 'Theorem 2.1 has two hypotheses' and the statement lists exactly two (partials exist on N; f_xy continuous at p). "
    "Bullet 3 matches Theorem 3.1 as stated (twice differentiability on the disc plus continuity of H at p).")
carry("M2-d-prose-L20-thm1.2-cite", "the Theorem 1.2 proof and Section 1 passages of L20")
new("M2-d-prose-L21-process-word", "PASS", "course/modules/M/M2/L19.html ... L24.html; cards of c280-c377",
    "Round 5: case-insensitive grep for builder|verifier|build|round [0-9]|fragment|checkout|unit report|request over the six pages and the slice cards: no hits.")
carry("M2-d-prose-L21-assumed-name", "the L21 Lab 1 hypothesis and E3 passages")
new("M2-d-prose-L21-R1-forward-ref", "PASS", "course/modules/M/M2/L21.html Research R1 statement and solution",
    "Round 5: grep 'L23' over course/modules/M/M2/L21.html returns 0 matches (re-run). R1 has no forward reference.")
new("M2-d-prose-L21-R3-taylor-hypothesis", "PASS", "course/modules/M/M2/L21.html Research R3 solution",
    "Round 5: the new solution is conditional: 'If g is twice differentiable on the interval, then by Taylor's theorem (Lesson L08, Theorem 2.1) the error ... is at most 1/2 sup|g''| dx^2'. "
    "L08 Theorem 2.1 (L08.html line 90) requires (n+1) differentiability on the open interval I (n = 1 here) and gives the Lagrange remainder, so the bound holds (re-derived). "
    "The solution also says Theorem 1.2 does not state twice differentiability, which matches its statement (C^1 only). The round-4 FAIL is fixed.")
new("M2-d-prose-L22-uniqueness", "PASS", "course/modules/M/M2/L22.html Section 2 bullets and Misconception 2",
    "Round 5: re-read (lines 245-260). Bullet 2: f_a(1,a) = 1 = V'(a) for a > 0; f_a(1,0) = 1 and f_a(0,0) = 0 against V'(0+) = 1 and V'(0-) = 0 (Example 2.3, re-derived). "
    "Misconception 2 matches Example 2.3's one-sided derivatives.")
new("M2-d-prose-L22-misconception3", "PASS", "course/modules/M/M2/L22.html Misconception 3 (changed text)",
    "Round 5: re-read (line 264). x_hat = 0.5 at a = 1.5; f_xx = -0.666667 (Example 1.5); 0.5*0.666667*1e-16 = 3.33e-17 (page 3.3e-17). "
    "The 1/2 |f_xx| e^2 expression is stated 'to leading order' and is a calculation on the page.")
carry("M2-d-prose-L23-units", "the L23 Section 1 and Lab 1 interpretation passages")
carry("M2-d-prose-L23-exponentials", "the L23 Section 4 bullet 1 and Lab 1 hypothesis passages")
carry("M2-d-prose-L24-problem-ref", "the L24 Section 5 bullet 3 and Problem P3")
new("M2-d-scope-words-L21-L24", "PASS", "course/modules/M/M2/L19.html ... L24.html changed lines (git diff 2657ab5..09b8751)",
    "Round 5: scope words in every changed line checked. L19 'an arbitrary function whose second partials exist' (witness: Example 2.2); "
    "L19 R2 constant n (Cauchy-Schwarz); L20 'for every choice of tags' (the limit definition); L21 'unique among functions with values in an open interval J' (Theorem 1.2 proof); "
    "L22 'every x in [0,1]' (Example 2.3, computed) and 'tests no other objectives' (two loops in main()); L23 R2 'any shift with y0 + Delta > -1' (Theorem 3.1 hypothesis); L24 'depends on the step it uses' (no universal claim).")
new("M2-d-banned-phrases", "PASS", "course/modules/M/M2/L19.html ... L24.html",
    "Round 5: check_pages M2 PASS for each page (banned-string gate); an ellipsis grep over the six pages hits only Python annotations in code.")
carry("M2-d-dag-prose-names", "the L20 Remark 2.3 passage ('often called Fubini's theorem')")
new("M2-d-dag-links", "PASS", "course/modules/M/M2/L19.html ... L24.html concept links and dfn",
    "Round 5: tools/check_dag.py --unit M2 -> 'check_dag M2: PASS'. The changed text adds 'Lesson L08, Theorem 2.1' (L21 R3), 'Lesson L19' (L21 R3), 'Lesson L21' (L22 Remark 1.4), all backward references.")
new("M2-d-dag-closure", "PASS", "course/modules/M/M2/L19.html ... L24.html (concepts used by name)",
    "Round 5: concepts used in the changed text: Taylor's theorem and Lagrange remainder (L08, earlier in M2), Hessian (L19, earlier than L22), "
    "implicit-function theorem (L21, earlier than L22), geometric series (M1, listed prerequisite, index.html line 35). None is used before its defining lesson or outside the closure.")
new("M2-d-struct-hours", "PASS", "course/modules/M/M2/L19.html ... L24.html data-hours and header",
    "Round 5: data-hours=\"10\" on each of L19..L24 (grep). The hub index.html changes in this delta are the lede and the Lessons 1-6 paragraph; no hours change. Hours are design targets and are not judged on pace.")
new("M2-d-cards-duplicate-scan", "PASS", "course/modules/M/M2/cards.json (377 cards; slice c280-c377)",
    "Round 5: ledgers/M2/scripts/M2-d-r5/cards_scan_r5.py course/modules/M/M2/cards.json -> 'cards 377 dup ids 0 dup fronts 0 dup backs 0'. "
    "M2-c378 (new, Lesson L10) is outside this slice.")
new("M2-d-cards-L19-L20", "PASS", "course/modules/M/M2/cards.json M2-c280..c307 (c291 and c298 changed)",
    "Round 5: c291 now reads 'twice differentiability on the disc together with continuity of H at p', matching Theorem 3.1 (round-4 FAIL fixed). "
    "c298 back ('With y integrated first ... 2x + 2x^2; with x integrated first ... y/2 + 1/3 (Proposition 2.2)') matches the changed proof. "
    "c285, c293, c304 re-checked. c290 is in its own row (M2-d-cards-L19-c290).")
new("M2-d-cards-L19-c290", "FAIL", "course/modules/M/M2/cards.json M2-c290 (front: 'Do the mixed partials of a general twice-differentiated function agree?')",
    "The back still says 'Not without a hypothesis. Example 2.2 has both mixed partials exist near the origin and differ at it', but the current L19 Section 4 bullet 1 "
    "(L19.html line 256) was changed to 'an arbitrary function whose second partials exist'. The front's 'twice-differentiated' is a different class from the one the lesson's sentence uses: "
    "Section 3 takes 'twice differentiable on N' as the hypothesis of Theorem 3.1, and the page does not establish that Example 2.2's function is twice differentiable at the origin.",
    fix="Change the front of M2-c290 to 'a function whose second partials exist' to match L19 Section 4 bullet 1; the back's Example 2.2 witness and continuity hypothesis stay.")
new("M2-d-cards-L21", "FAIL", "course/modules/M/M2/cards.json M2-c308 (Definition 1.1) and M2-c309..c322",
    "M2-c308 back says the implicit-function theorem gives conditions under which g 'exists, is unique and is differentiable'. The current Definition 1.1 (L21.html line 59) says unique "
    "'among functions with values in an open interval J around y0'. The qualifier is needed: for F(x,y) = y(y - 1) at (0,0), F_y = -1 != 0, and g(0) = 0 with g(x) = 1 for x != 0 satisfies F(x, g(x)) = 0 "
    "and g(x0) = y0, so an unqualified 'unique' is false. c309-c322 re-checked against the current text (c309 names J; c310, c313, c314, c319, c322 agree).",
    fix="Add 'among functions with values in an open interval J around y0' to the back of M2-c308.")
new("M2-d-cards-L22", "FAIL", "course/modules/M/M2/cards.json M2-c323..c337 (x* notation; c336 printed label)",
    "The current L22 writes the maximizer as x_hat(a) throughout (Definition 1.1, Lemma 1.2, Theorem 1.3, Remark 1.4, Example 1.5, Proposition 2.1, Lab 1 output, L22.html line 208). "
    "Cards c323, c324, c325, c326, c327, c330, c331, c334 and c337 still write x*(a). c336 says 'Part A prints x* with an error of about 10^-8', but the lab now prints 'x_hat' (L22.html line 208). "
    "The mathematics of these cards matches the lesson; the symbol and the printed label disagree with the current text.",
    fix="On M2-c323, c324, c325, c326, c327, c330, c331, c334 and c337 replace x*(a) with x_hat(a); in M2-c336 replace 'prints x*' with 'prints x_hat'.")
new("M2-d-cards-L23", "FAIL", "course/modules/M/M2/cards.json M2-c338..c357 (c340)",
    "M2-c340 back lists the hypotheses as 'N >= 1, face F > 0, coupons yF at each year t < N for the rate y, and the face F added to the last coupon'. "
    "Proposition 2.2 (L23.html line 81) also requires 'a rate y > -1'; without it v = 1/(1+y) is undefined at y = -1, so the card drops a stated hypothesis. "
    "c338-c357 otherwise re-checked; c345, c346 and c352 numbers match the lab output.",
    fix="Insert 'a rate y > -1' into the hypotheses in the back of M2-c340.")
new("M2-d-cards-L24", "PASS", "course/modules/M/M2/cards.json M2-c358..c377 (c375 changed)",
    "Round 5: c375 back now reads 'Proposition 4.2 proof, Section 4; Section 5 bullet on cancellation'. The Proposition 4.2 proof is at L24.html line 112 (Section 4) and the cancellation bullet is at line 250 (Section 5). "
    "The round-off bound 2 delta/h follows from Definition 4.1 (re-derived). c360, c370 and c371 carried from round 4 (no change in those cards or their passages).")

# ---- assemble ----
rows = []
for r in r4["rows"]:
    if r["id"] not in NEW:
        raise SystemExit("row not re-decided: " + r["id"])
    rows.append(NEW[r["id"]])
for rid, row in NEW.items():
    if rid not in old:
        rows.append(row)

verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
fragment = {
    "unit": "M2",
    "slice": "M2-d",
    "round": 5,
    "verifier": "independent verifier (Haiku), round 5, slice M2-d (L19-L24 and their lab twins); did not build M2",
    "pin": "09b8751",
    "base": "2657ab5",
    "previous_ledger": "/tmp/fanout-frags/B-M2-d.round4.json",
    "checkout": "/tmp/verifyB5-M2-d (detached at 09b8751)",
    "scratch": "/tmp/M2-v/d-r5",
    "verified_at": "2026-10-28T20:00:00+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta since the round-4 pin 2657ab5: L19 (Remark 3.2, lab hypothesis, Section 4 bullet 1, R2 solution), L20 (Definition 1.1 wording, Proposition 2.2 proof order), "
        "L21 (Definition 1.1 J qualifier, R3 solution), L22 (notation x* renamed x_hat throughout, Section 2/3 wording, Example 2.3 and misconception text, lab twin labels), "
        "L23 (R2 question and solution), L24 (why-it-matters paragraph), cards.json (c291, c298, c334, c340, c375 changed; c378 added, an L10 card), lab twin L22 (labels, docstrings). "
        "Byte-identical in the slice: L20 Theorem 1.2 and Proposition 2.4 passages, the L21 Theorem 1.2 statement, the L23 Theorem 3.1 and Proposition 2.1 passages, L24 Propositions 3.1 to 4.3 passages, the L19 and L23 and L24 lab twins (L22 twin changed).",
        "The round-4 FAIL rows were re-verified: M2-d-cards-L19-L20 (c291 now PASS), M2-d-cards-L22 (c334 content now PASS, but notation FAIL), M2-d-cards-L23 (c340 changed, still FAIL on the dropped y > -1), "
        "M2-d-cards-L24 (c375 now PASS), M2-d-prose-L21-R3-taylor-hypothesis (now PASS).",
        "Mutants: none. The lab slice is a demonstration (ARCHITECT ruling); mutation testing applies to project graders (M2-e).",
        "Not checked: I did not read every unchanged sentence of L19-L24 line by line again; unchanged passages are carried from round 4 with their byte-identity stated. "
        "No live Crossref or registry access was run beyond verify_refs; no bibliographic claim was checked against an external source.",
    ],
    "summary": "",
}
fragment["summary"] = (
    "Round 5, slice M2-d: %d rows, PASS %d, FAIL %d. FAIL rows: M2-d-cards-L19-c290 (card still says 'twice-differentiated' after the lesson sentence changed); "
    "M2-d-cards-L21 (c308 drops the 'among functions with values in J' qualifier of Definition 1.1); "
    "M2-d-cards-L22 (cards use x*(a) where the lesson now uses x_hat(a), and c336 quotes the old printed label); "
    "M2-d-cards-L23 (c340 drops the y > -1 hypothesis of Proposition 2.2)."
    % (len(rows), sum(r["status"] == "PASS" for r in rows), sum(r["status"] == "FAIL" for r in rows))
)
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=1, ensure_ascii=False)
print(len(rows), verdict, sum(r["status"] == "PASS" for r in rows))
