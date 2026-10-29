"""Adds the round-3 rows to ledgers/M5/M5-b.json (run with python -I from the checkout root)."""

import json

PATH = "ledgers/M5/M5-b.json"
P = "PASS"
F = "FAIL"

rows = [
    {"id": "M5-b-html-L05-math-lt", "check": "2.9-structure", "location": "course/modules/M/M5/L05.html:215, :220, :315", "status": P,
     "evidence": "page_checks_r3.py (ledgers/M5/scripts/M5-b-r3/): 'L05 unknown tag names: []'; no raw '<' followed by a letter remains. Math '0&lt;a&lt;1' escaped at :215."},
    {"id": "M5-b-html-L06-math-lt", "check": "2.9-structure", "location": "course/modules/M/M5/L06.html:56, :70, :234, :282", "status": P,
     "evidence": "page_checks_r3.py: 'L06 unknown tag names: []'."},
    {"id": "M5-b-L06-partB-lower-bound-claim", "check": "2.4-math / 2.5-lab", "location": "course/modules/M/M5/L06.html:221; tests/labs/M5/lab-M5-L06-1.py Part B", "status": P,
     "evidence": "Re-derived: x(1-x)=1/4-(x-1/2)^2 <= 1/4 on [0,1]; grid maximum equals 1/4 only if 1/2 is on the grid (unique maximiser). Lab output: grid_tenths argmax 1/2 maximum 1/4; grid_sevenths argmax 3/7 maximum 12/49 lower_bound_for_true True (python -I -W error run, rc 0)."},
    {"id": "M5-b-L06-partC-proposition-number", "check": "2.4-math / 2.7-cards", "location": "course/modules/M/M5/L06.html:221 and :325", "status": F,
     "evidence": "Proposition 3.4 (L06.html:276-277) is stated for e_n, n in N = {1,2,...}, in B(N) with d_inf. Part C (lab-M5-L06-1.py lines 95-96 build the vectors) checks e_0..e_9 truncated to length 20. The page at :221 says 'Proposition 3.4 proves the statement for all of them'. Index 0 and the length-20 truncation are outside Proposition 3.4 as stated. The proposition number itself is right; the scope claim is not.",
     "fix": "Replace 'Proposition 3.4 proves the statement for all of them' at L06.html:221 with: 'the proof of Proposition 3.4 applies verbatim to the truncations, because any two distinct unit vectors differ by 1 in two positions and both entries lie in [0,1]'. Same wording change at :325 ('as in Proposition 3.4')."},
    {"id": "M5-b-L06-mech2-citation", "check": "2.4-math", "location": "course/modules/M/M5/L06.html:307", "status": P,
     "evidence": "Re-derived: f(x)=x^3-3x; f(-2)=-2, f(-1)=2, f(1)=-2, f(2)=2; maximum 2 at x=-1 and x=2, minimum -2 at x=-2 and x=1. Existence cited to Corollary 2.2 (L06.html:239-240), which is stated for [a,b]; [-2,2] is a closed bounded interval."},
    {"id": "M5-b-L06-mech2-typo", "check": "2.9-structure", "location": "course/modules/M/M5/L06.html:307", "status": P,
     "evidence": "Round-2 FAIL re-checked: grep -c -w 'is is' on L06.html = 0; the sentence now reads 'the maximum is \\(2\\)'. Defect fixed."},
    {"id": "M5-b-L06-ex1.5-subsequence-citation", "check": "2.4-math", "location": "course/modules/M/M5/L06.html:96 (Example 1.5)", "status": P,
     "evidence": "grep -c 'Example 3.6' L06.html = 0. Replacement proof: n_k >= k, so 0 < 1/n_k <= 1/k -> 0 (re-derived). Correct."},
    {"id": "M5-b-L07-partC-no-fixed-point-claim", "check": "2.5-lab / 2.4-math", "location": "tests/labs/M5/lab-M5-L07-1.py part_c; course/modules/M/M5/L07.html:186, :193, :296", "status": P,
     "evidence": "Lab output part C lines: min of f(x)-x = 0.099020 on [-5,5] and 0.009999 on [-50,50] (recomputed: sqrt(26)-5 = 0.0990195, sqrt(2501)-50 = 0.0099990). Page at :296 says the grid check does not show that f has no fixed point; Section 4 item 2 proves it (re-derived: sqrt(x^2+1) > |x| >= x)."},
    {"id": "M5-b-L07-tolerance-claim", "check": "2.5-lab", "location": "tests/labs/M5/lab-M5-L07-1.py lines 83-85 and docstring; course/modules/M/M5/L07.html:186", "status": P,
     "evidence": "Round-2 FAIL re-checked: part_c() tests 'if gap <= 0.0' with no tolerance, and the docstring (lab lines 9-10) and page (:186, :196) now say 'Part C tests the sign of f(x) - x in floating point with no tolerance'. Claim matches code. Parts A and B use TOL = 1e-12 (lines 41, 58), which the page states. Fixed."},
    {"id": "M5-b-L07-M1-general-linear-map", "check": "2.4-math", "location": "course/modules/M/M5/L07.html Problem M1 solution (line 336)", "status": P,
     "evidence": "Re-derived: phi x = x/2 + 1, beta 1/2, x* = 2, x1 = 1, x2 = 1.5; bound at n=2 = (1/2)^2 * 1/(1/2) = 0.5 = |x2 - x*|. Example 2.3 and Problem R1 cited for the equality cases; both re-derived."},
    {"id": "M5-b-L07-completeness-attribution", "check": "2.1-citations / 2.4-math", "location": "course/modules/M/M5/L07.html:67 (Def 1.2), :136 (Prop 2.4 hyp 4)", "status": P,
     "evidence": "Read course/modules/M/M5/L02.html:125-127 (Theorem 2.5, H1 Cauchy, H2 every nonempty bounded-above subset of R has a supremum; 'Lesson 1, Definition 1.1') and L02.html:81 (Definition 2.1 Cauchy sequence). Lesson 1 Definition 1.1 is at course/modules/M/M5/L01.html:59 (completeness of R). Both references match."},
    {"id": "M5-b-L07-most-maps-scope", "check": "2.4-math / scope", "location": "course/modules/M/M5/L07.html:52", "status": P,
     "evidence": "Counterexample x -> -x: iterates from 1 are 1, -1, 1, -1, ..., which do not converge (direct computation). The word 'Not every map guarantees' is backed by this counterexample."},
    {"id": "M5-b-L07-bellman-term-before-definition", "check": "2.9-structure / DAG", "location": "course/modules/M/M5/L07.html:52", "status": P,
     "evidence": "grep -c -i bellman L07.html = 1; the one hit is the sentence 'The operator defined by formula in Lesson 8 needs the same theorem' (plan Architect Q1: operator defined by formula, no concept name)."},
    {"id": "M5-b-L07-R1-general-condition", "check": "2.4-math", "location": "course/modules/M/M5/L07.html R1 (line 411)", "status": P,
     "evidence": "Re-derived: x_n = beta^n, x* = 0, d(x0,x1) = 1 - beta, bound = beta^n = error. Sentence 'This page does not state a general condition' is accurate (no general condition appears in the page)."},
    {"id": "M5-b-L07-E3-strict-monotonicity", "check": "2.4-math / 2.2-numbers", "location": "course/modules/M/M5/L07.html Assumption 2(a) (line 159) and E3 solution (line 400)", "status": P,
     "evidence": "Round-2 FAIL re-checked: Assumption 2(a) now says 'sin is strictly increasing on [0,1]' (line 159); grep -c nondecreasing L07.html = 0. E3 quotient for (0.995, 1) = 0.840116725732577... (mpmath-free Decimal computation, numbers_L05_L07.py), gap sin1 - quotient = 0.00135425907531889..., matching the page's 0.0013542591. Fixed."},
    {"id": "M5-b-L05-why-it-matters-prop13", "check": "2.1-citations / 2.4-math", "location": "course/modules/M/M5/L05.html:52", "status": P,
     "evidence": "Round-2 FAIL re-checked: the why-it-matters line now cites only Proposition 2.1 and Example 2.3 (line 52); the Proposition 1.3 claim is removed. Fixed."},
    {"id": "M5-b-L05-interpretation-prop13a", "check": "2.4-math / 2.5-lab", "location": "course/modules/M/M5/L05.html:174", "status": P,
     "evidence": "Proposition 1.3(a) is an iff (L05.html:69-70). Lab output: 'order n sup_distance 1' for n in (1,2,5,10,50). The sentence 'stays at 1 ... not uniform, by Proposition 1.3(a)' is correct. 'On the grid of [0,1/2] ... (1/2)^n ... Proposition 2.5 with a=1/2 ... uniform on all of [0,1/2]' matches Prop 2.5 (a<1, S=[0,a])."},
    {"id": "M5-b-L05-lab-partC-label", "check": "2.5-lab", "location": "tests/labs/M5/lab-M5-L05-1.py docstring lines 98-99 and main() Part C", "status": P,
     "evidence": "The docstring now says 'a check prints True when f_n(1) = 1 for n = 1, 10, 100 and 1000'; the code checks exactly (1, 10, 100, 1000) (main, last print line). Run output last line: value_at_one_for_every_order True (python -I -W error, rc 0)."},
    {"id": "M5-b-L05-lab-run", "check": "2.5-lab", "location": "tests/labs/M5/lab-M5-L05-1.py; course/modules/M/M5/L05.html:156-173", "status": P,
     "evidence": "page_checks_r3.py: 'L05 lab rc 0', 'output lines 18 expected lines 18', 'output == expected block: True'. Values re-derived: 0.99^10 = 0.9043820750, 0.99^100 = 0.3660323413, 0.99^1000 = 0.0000431712, (1/2)^10 < 1/1000 < (1/2)^9, least order 10."},
    {"id": "M5-b-L06-lab-run", "check": "2.5-lab", "location": "tests/labs/M5/lab-M5-L06-1.py; course/modules/M/M5/L06.html:204-220", "status": P,
     "evidence": "page_checks_r3.py: 'L06 lab rc 0', 'output == expected block: True' (17 lines). Part A chosen indices 1 2 3 4 5 32 45 55 are increasing; step 8 interval [3/128, 7/256] has width 1/256."},
    {"id": "M5-b-L07-lab-run", "check": "2.5-lab", "location": "tests/labs/M5/lab-M5-L07-1.py; course/modules/M/M5/L07.html:282-295", "status": P,
     "evidence": "page_checks_r3.py: 'L07 lab rc 0', 'output == expected block: True' (14 lines). Re-derived: x* = 0.739085; a priori bound holds for n = 0..30 (checked by the run's AssertionError path); grid max 0.840116725732564 at (0.995, 1) (numbers_L05_L07.py grid-max section)."},
    {"id": "M5-b-cmd-run_labs-check_pages-dag-smoke", "check": "2.5-lab / 2.9-structure / DAG", "location": "tools/run_labs.py --unit M5; tools/check_pages.py --unit M5; tools/check_dag.py --all; tools/page_smoke.py --unit M5 --pages L05 L06 L07 --skip-sweep", "status": P,
     "evidence": "run_labs --unit M5: 'PASS (13/13)'. check_pages --unit M5: 'PASS'. check_dag --all: 'check_dag M5: PASS'. page_smoke --pages L05 L06 L07 --skip-sweep: 'page_smoke L05 PASS', 'L06 PASS', 'L07 PASS', 'page_smoke M5: PASS'. Sweep skipped (not run)."},
    {"id": "M5-b-hours", "check": "hours (arithmetic only)", "location": "course/modules/M/M5/L05.html, L06.html, L07.html data-hours; course/modules/M/M5/index.html:29, :131", "status": P,
     "evidence": "data-hours: L05=10, L06=10, L07=11 (grep). Hub data-hours-lessons=104 and text 'Six declare 10 ... four declare 11 (Lessons 7 to 10)' = 6*10 + 4*11 = 104 (L01-L04 and L08-L10 also checked by grep: 10, 10, 10, 10, 11, 11, 11). Pace not judged (architect ruling)."},
    {"id": "M5-b-numbers-prose", "check": "2.2-numbers", "location": "L05 Empirical 3 and interpretation; L06 Empirical 2; L07 E1, E2, E3, R2, M2, Misconception 3, Example 3.3", "status": P,
     "evidence": "numbers_L05_L07.py output: 0.99^100 = 0.366032 (page '0.366'); 1/196 = 0.005102 ('about 0.0051'); 2.661258/0.05439523 = 48.9245 ('about 48.9' and '48.92'); f'(5) = 5/sqrt26 = 0.980581, f'(50) = 0.999800; window gaps 0.099020 and 0.009999; M2 bound at n=13 = 1.8817e-6, n=14 = 6.2723e-7; R2 n* = 90.7126, smallest n = 91 (bound 9.516e-7; n=90 gives 1.131e-6); sin 1 = 0.8414709848; E3 quotient 0.8401167257."},
    {"id": "M5-b-grades-and-theorems", "check": "2.3-grades / 2.4-math", "location": "course/modules/M/M5/L05.html:181 (Prop 2.1 hyp 2); L05 Props 1.3, 2.4, 2.5, 3.1, 3.2; L06 Props 1.3, 1.4, 2.1, 3.1, 3.4; L07 Props 1.4, 2.4, 3.1, Cor 3.2", "status": F,
     "evidence": "Re-derived all listed proofs; the proof bodies are correct. Defect: the hypothesis of Proposition 2.1 (L05.html:181) reads 'each f_n: X -> R is continuous, in the epsilon-delta sense of L03', but L03 Definition 1.1 (course/modules/M/M5/L03.html:58-59) is for a function on D in R with |x - x0|, while X is a general metric space. See row M5-b-r3-L05-prop21-continuity-definition.",
     "fix": "Change the hypothesis at L05.html:181 to 'continuous in the sense of L04, Definition 4.1 at each point of X'. See the linked row for the other locations."},
    {"id": "M5-b-l07-canon-breaks-and-misconceptions", "check": "2.4-math / 2.7-cards", "location": "course/modules/M/M5/L07.html:302-304, :313-321", "status": P,
     "evidence": "Re-derived canon-breaks item 1 (x/2 on (0,1]: only candidate 0 not in X), item 2 (identity |phi x - phi y| = |x+y||x-y|/(phi x + phi y); ratio -> 1 along x = y + h, y -> infinity), item 3 (f(I) subset I by Assumption 2(b)). Misconceptions 1-3 re-derived; 48.92 ratio confirmed."},
    {"id": "M5-b-scope-and-process-words", "check": "2.9-structure / scope / process words", "location": "course/modules/M/M5/L05.html, L06.html, L07.html (scope words grepped)", "status": F,
     "evidence": "Grep of always/only/every/all/same/drives/as much as: every hit in L05 checked (computation or proof behind it). Process words (build, builder, round, verifier, REQUESTS, unit report) absent: grep. Ellipses in 'k = 0, ..., 100' are mathematical notation, not omitted content. Two scope claims fail: L07.html:52 'every pair of points strictly closer' (false for x = y, see M5-b-r3-L07-strictly-closer) and L06.html:221 'Proposition 3.4 proves ... for all of them' (see M5-b-L06-partC-proposition-number). Also L06.html:101 'the half with more prefix indices' (see M5-b-r3-L06-lab-pool-wording).",
     "fix": "Apply the fixes in the linked rows."},
    {"id": "M5-b-citations-registry", "check": "2.1-citations", "location": "course/modules/M/M5/L05.html:389-392, L06.html:421-424, L07.html:512-516 (References sections)", "status": P,
     "evidence": "L05 and L06 references lists are empty (<ol data-references></ol>); L07 says 'This page cites no source'. grep 'data-ref|references.json|doi.org' finds one element per page, the empty <ol data-references></ol>. tools/verify_refs.py --offline: '560 entries, 0 problems'. No registry key is cited on these pages. Live verify_refs not needed (no citation to check)."},
    {"id": "M5-b-l07-input-facts", "check": "2.4-math / 2.1-citations", "location": "course/modules/M/M5/L07.html Assumption 1 (line 154), Assumption 2 (lines 159-160)", "status": P,
     "evidence": "Assumption 1 (FTC and integral bound) and Assumption 2 (sin strictly increasing on [0,1], sin 0 = 0, 0 < cos t <= 1 on [0,1], derivatives of sin and cos) are standard and correct. grep -n -i 'integral\|derivative\|sin' course/modules/M/M5/L01.html course/modules/M/M5/L02.html returns no lines, so the claim 'Lesson 1 and Lesson 2 do not cover' these facts is supported by that grep (scope of the claim checked by grep only)."},
    {"id": "M5-b-mutants-not-applicable", "check": "mutation (project grader only)", "location": "M5-b slice (no project grader)", "status": P,
     "evidence": "Slice M5-b has no grader; mutation testing applies to project graders only (architect ruling). mutants: []."},
    {"id": "M5-b-r3-L05-prop21-continuity-definition", "check": "2.4-math / 2.1-citations (definition used)", "location": "course/modules/M/M5/L05.html:181 (Prop 2.1 hyp 2); also L05.html:38, L06.html:38, L07.html:38 ('Uses: continuity (epsilon-delta)' pointing to L03)", "status": F,
     "evidence": "L03.html:58-59 Definition 1.1 defines continuity for f on D with |x - x0| < delta, i.e. a subset of R. Proposition 2.1 has a general metric space (X, d) (L05.html:181, hyp 1) and its proof uses d(x0, z) < delta (L05.html:186). The definition for a general metric space is L04.html:302 Definition 4.1. The 'Uses' lines link continuity to L03, which is the R-only definition.",
     "fix": "At L05.html:181 replace 'in the epsilon-delta sense of L03' with 'in the sense of L04, Definition 4.1'. In the Uses lines, point the metric-space continuity to L04 Definition 4.1 (course/modules/M/M5/L04.html:302; the block has no anchor id, so link to the lesson or name it in prose); keep the L03 link only where the page works on R."},
    {"id": "M5-b-r3-L06-partC-scope", "check": "2.4-math / scope", "location": "course/modules/M/M5/L06.html:221 (Part C interpretation); tests/labs/M5/lab-M5-L06-1.py lines 95-96 (main, Part C)", "status": F,
     "evidence": "Lab Part C builds unit_vector(i, TRUNCATION) for i = 0..9, i.e. e_0 ... e_9 truncated to length 20 (lab line 96), with positions 0..19. Proposition 3.4 (L06.html:276-277) is stated for e_n with n in N = {1,2,...} on B(N), with no truncation. The page's sentence 'Proposition 3.4 proves the statement for all of them' therefore claims more than Proposition 3.4 states.",
     "fix": "Replace the sentence at L06.html:221 with: 'Proposition 3.4 proves the same statement for the unit vectors of B(N); the argument applies verbatim to these truncations, since any two distinct unit vectors differ by 1 in two positions.' Also reword L06.html:325 ('as in Proposition 3.4') to match."},
    {"id": "M5-b-r3-L06-lab-pool-wording", "check": "2.5-lab (what the lab does)", "location": "course/modules/M/M5/L06.html:101 (lab hypothesis); tests/labs/M5/lab-M5-L06-1.py line 56 (pool) and lines 57-65 (the half kept)", "status": F,
     "evidence": "The hypothesis says the lab keeps 'the half with more prefix indices'. The code (lab line 56) builds pool = indices n in range(last_index + 1, PREFIX + 1) whose term lies in the current interval, i.e. only the indices after the last chosen index. The lab docstring (lab file lines 7-8 of the bisect description, and page :108) says 'remaining prefix indices', so the hypothesis line is less precise than the code and the docstring.",
     "fix": "Change L06.html:101 to 'keeping the half that contains more of the remaining prefix indices (those after the last chosen index) inside the current interval'."},
    {"id": "M5-b-r3-L07-strictly-closer", "check": "2.4-math / scope", "location": "course/modules/M/M5/L07.html:52 (why-it-matters)", "status": F,
     "evidence": "'A contraction is a map that pulls every pair of points strictly closer together by a fixed factor.' Definition 1.1 (L07.html:61) gives d(phi x, phi y) <= beta d(x, y). For x = y both sides are 0, so the pair is not strictly closer. Strictness holds only for distinct points (beta d < d when d > 0).",
     "fix": "Replace 'pulls every pair of points strictly closer together' with 'pulls every pair of distinct points strictly closer together, by a fixed factor beta < 1'."}
]

with open(PATH, encoding="utf-8") as fh:
    fragment = json.load(fh)
fragment["rows"] = rows
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
fragment["summary"] = (
    f"M5-b round 3: {len(rows)} rows, {sum(1 for r in rows if r['status'] == 'FAIL')} non-PASS (FAIL). "
    "Round-2 defects fixed and re-verified: duplicated word, Prop 1.3 cite, E3 monotonicity, tolerance claim, raw less-than. "
    "Open: L05 Prop 2.1 hypothesis cites the R-only L03 definition for a general metric space; L06 Part C claims Proposition 3.4 for length-20 truncations and e_0; "
    "L06 lab hypothesis wording of the kept half; L07 'every pair of points strictly closer' fails for x = y."
)
with open(PATH, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("rows", len(rows), "fail", sum(1 for r in rows if r["status"] == "FAIL"))
