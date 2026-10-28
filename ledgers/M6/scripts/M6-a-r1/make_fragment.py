"""Writes the M6 slice-a round-1 verification fragment (verifier-authored; standard library only)."""
import json
import sys

ROWS = []


def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    ROWS.append(r)


CMD = "tools/"
# ---- commands and tooling
row("M6-a-cmd-pin", "2.9-structure", "repository HEAD of /tmp/verifyC1-M6-a", "PASS",
    "git rev-parse --short HEAD -> 55b5634 (detached, the pin named in the brief); the only untracked paths are .venv (symlink) and ledgers/M6/scripts/M6-a-r1/.")
row("M6-a-cmd-check-pages", "2.9-structure", "tools/check_pages.py --unit M6", "PASS",
    "stdout: 'check_pages M6: PASS' (all 12 lessons and the hub; includes the 6-12 h and 10-40 % project-share rules).")
row("M6-a-cmd-check-dag", "DAG", "tools/check_dag.py --unit M6", "PASS",
    "stdout: 'check_dag M6: PASS'. Concept links used by the slice (quantifiers, direct-proof, mathematical-induction, limit, definite-integral, multiple-integral, expectation, conditional-expectation-elementary, metric-space, cauchy-sequence, completeness-of-reals, evidence-grade, project-ladder) are all in the M1, M2, M4, M5, P0.1 closure (plan section 0.1).")
row("M6-a-cmd-run-labs", "2.5-labs", "tools/run_labs.py --unit M6 --page L01 (and L02, L03, L04)", "PASS",
    "each run: 'run_labs M6: PASS (1/1)', exit 0; twin text byte-identical to the embedded block and stdout matches the page's expected output.")
row("M6-a-cmd-twins-isolated", "2.5-labs", "python -I -W error tests/labs/M6/lab-M6-L01-1.py ... L04-1.py", "PASS",
    "all four exit 0, empty stderr, wall time 0.01-0.04 s; outputs in /tmp/M6-v/M6-a/run/out-L0n-1.txt.")
row("M6-a-cmd-page-smoke", "2.5-labs", "tools/page_smoke.py --unit M6 --pages index L01 L02 L03 L04 --skip-sweep", "PASS",
    "'page_smoke M6: PASS'; per-lab times 0.0-0.1 s in the Pyodide-backed run; the sweep was skipped because the slice has no live figures (BUILDER/plan: no figures). Log: /tmp/M6-v/M6-a/smoke.txt.")
row("M6-a-cmd-ruff-mypy", "2.9-structure", "ruff check and ruff format --check on tests/labs/M6/lab-M6-L01..L04-1.py; mypy --no-incremental on the same four files", "PASS",
    "'All checks passed!', '4 files already formatted', 'Success: no issues found in 4 source files'.")
row("M6-a-cmd-verify-refs", "2.1-citations", "tools/verify_refs.py --offline; tools/verify_refs.py --unit M6 (live)", "PASS",
    "offline: '560 entries, 0 problems'; live --unit M6: '2 of 560 entries, 0 problems' (billingsley2012probability, williams1991probability).")
row("M6-a-cmd-collect", "2.5-labs", "tests/labs/M6 twins as written and their page embedding", "PASS",
    "twins read no file and use no network (grep of data-files in L01-L04: none); the lab docstrings say so and the code confirms it.")

# ---- citations
row("M6-a-cite-keys", "2.1-citations", "course/modules/M/M6/L01.html:470, L03.html:499, L04.html:484; index.html:177-178", "PASS",
    "the pages cite only the two M6 keys (billingsley2012probability, williams1991probability); both verified live (see M6-a-cmd-verify-refs). No edition string is repeated on the pages.")
row("M6-a-cite-no-locator", "2.1-citations", "course/modules/M/M6/L01.html:470, L03.html:499, L04.html:484", "PASS",
    "grep of the four lesson pages for theorem/page/equation locators attributed to Billingsley or Williams: none. Each references section states that no passage was read.")
row("M6-a-cite-no-curriculum-attribution", "2.1-citations", "course/modules/M/M6/L03.html:499, L04.html:484", "PASS",
    "both pages say 'the curriculum names Billingsley ... as a source for measure and integration'. The curriculum (curriculum/01-foundations.yaml:286-288) lists the title without a topic; the phrase 'for measure and integration' is the title's own wording, not a curriculum claim about content. Pass on the title reading; the hub's lesson mapping is a separate row (M6-a-prose-hub-core-reading).")

# ---- numbers
row("M6-a-num-L03-table", "2.2-numbers", "course/modules/M/M6/L03.html lab Part B printed table (lines 257-266) and interpretation (line 268)", "PASS",
    "recomputed with 50-digit Decimal in ledgers/M6/scripts/M6-a-r1/recompute_L01_L04.py: all ten I_n, all errors 1/3 - I_n and bounds 2^-n agree to 10 decimals; all rows inside the bracket; I_n nondecreasing. Printed error at n=10 0.0004819768 and bound 0.0009765625 match.")
row("M6-a-num-L03-I1", "2.2-numbers", "L03.html:171 (I_1 about 0.1464), :291 (gap 0.1869 and about 0.3333), :324 (problem M3 solution)", "PASS",
    "I_1 = (1/2)(1 - sqrt(1/2)) = 0.14644660940672624; 1/3 - I_1 = 0.1868867; displayed 0.1869 consistent with displayed 0.3333 - 0.1464 = 0.1869.")
row("M6-a-num-L03-E3-rounding", "2.2-numbers", "course/modules/M/M6/L03.html:374 (problem E3, solution)", "FAIL",
    "The page gives the terms as about 0.0518, 0.0795 and 0.1005 'with sum 0.2317'. The displayed terms add to 0.2318 (0.0518+0.0795+0.1005). The unrounded terms are 0.0517767, 0.0794593, 0.1004809 with sum 0.2317169 (recomputed in recompute_L01_L04.py), so 0.2317 is right only on the unrounded basis, which the page does not state.",
    "State the basis: 'sum 0.231717 from unrounded terms (the three rounded terms add to 0.2318)'.")
row("M6-a-num-L04-partial-sums", "2.2-numbers", "L04.html:152 (about 2.019877, about 4.197279), :248-249 (lab printed lines), :358 (E3 solution), :450 (quiz)", "PASS",
    "sum_{n=1}^{10} 1/(n+1) = 2.0198773449 -> 2.019877; sum_{n=1}^{100} 1/(n+1) = 4.1972785077 -> 4.197279 (6 decimals, rounded from the exact value, as the lab line says).")
row("M6-a-num-L02-602", "2.2-numbers", "L02.html:148 (602 of 729), :276, :318, :389-391, :446", "PASS",
    "3^6 = 729 ordered disjoint pairs; pairs with an empty member 64+64-1 = 127; 729-127 = 602; brute force over all 64 subsets gives 602 failing disjoint pairs and 602 pairs with both members non-empty. Printed 'disjoint pairs where additivity fails: 602 of 729' matches.")
row("M6-a-num-L02-values", "2.2-numbers", "L02.html:112, :136, :141, :148 (3/20 sum), :322, :348, :355, :361-373", "PASS",
    "fair die P({2,4,6}) = 1/2; biased P({1,2}) = 3/4 and P(odd) = 21/32; 6 * 3/20 = 9/10; (2/6+2/6)=2/3 vs P({1,2,3})=1/2; subtract P({2})=1/6 (Prop 3.1); nu example 4/36 vs 2/36. All recomputed.")
row("M6-a-num-L01-counts", "2.2-numbers", "L01.html:116 (Example 2.2), :227-236 (printed lines), :291 (M1 solution), :305 (M3 solution), :341 (E1 solution), :355 (E3 solution), :414-455 (quiz numeric items)", "PASS",
    "2^2=4, 2^4=16, 2^3=8, 2^5=32 (Prop 2.1(b)); brute-force closure enumeration gives 4, 16, 8 members and candidate failing complement closure only; M1 family has 8 members as listed.")
row("M6-a-num-L03-misc", "2.2-numbers", "L03.html:171 (I_1), :310 (M1 solution, 4), :317 (M2 solution, 3/4), :324 (M3 solution), :360 (E1 solution, 1)", "PASS",
    "0 * 1/2 + 1 * 1/4 + 3 * 1/4 = 1; 2*(1/3)+5*(2/3) = 4; 1/2 + 1/4 = 3/4; 0.14644660940672624 -> 0.1464.")
row("M6-a-num-L04-misc", "2.2-numbers", "L04.html:138, :301, :306-308, :344, :374-376, :294", "PASS",
    "n*(1/n)=1; n/(n+1)->1; min(2,x^-1/2) integral 2*(1/4)+[2sqrt x]_{1/4}^1 = 3/2; g=floor(x^-1/2) level-set length (2n+1)/(n^2(n+1)^2) identity and term bound (2n+1)/(n(n+1)^2) <= 3/n^2 checked for n<50.")
row("M6-a-num-hub-placement", "2.2-numbers", "index.html:73 (77.8 %, 88.9 %, bar 80 % of 9 items)", "PASS",
    "7/9 = 77.78 %, 8/9 = 88.89 %, 0.8*9 = 7.2 so eight correct is the bar. Consistent.")
row("M6-a-num-hub-hours", "2.2-numbers", "index.html:29, :40, :42 (108/42, 72 %/28 %); L01-L12 data-hours 9", "PASS",
    "12 x 9 = 108; 108 + 42 = 150 = curriculum/01-foundations.yaml:264; 108/150 = 72 %, 42/150 = 28 %. Pace is not judged (architect ruling).")

# ---- grades
row("M6-a-grade-L01", "2.3-grades", "L01.html:75 (Prop 1.3 T), :97 (Prop 2.1 T), :245 (Example 3.1 T)", "PASS",
    "each T claim has a complete proof on the page: Prop 1.3 (a)-(c) (L01 :83-88), Prop 2.1 (a)-(c) (:107-112), Example 3.1 (:247). Lab result in Key results row (:395) graded C with basis.")
row("M6-a-grade-L02", "2.3-grades", "L02.html:73, :100, :120, :289 (T claims)", "PASS",
    "Prop 1.3(a)-(d), Prop 1.5, Prop 2.1, Prop 3.1 each proved on the page (L02 :88-92, :107, :125-132, :297). Remark 1.4 is a remark, not graded. Lab results graded C with basis (:446).")
row("M6-a-grade-L03", "2.3-grades", "L03.html:77, :105, :121, :147 (T claims), :415 (C row)", "PASS",
    "Prop 2.2, 3.2, 3.3 proved (L03 :88-92, :116-117, :132); Prop 4.1 proved under the stated Assumption L (:158-159), and its grade is stated as under Assumption L (:413-414). Lab numerical row graded C (:415).")
row("M6-a-grade-L04-thm31-ungraded", "2.3-grades", "L04.html:92-102 (Theorem 3.1 DCT, stated, not proved); key results :399", "PASS",
    "Theorem 3.1 has no data-grade attribute and is listed 'not graded, stated with its assumptions, not proved here'. Consistent with BUILDER_RULES (a stated result is not graded T).")
row("M6-a-grade-L04-ex32-T", "2.3-grades", "L04.html:105-107 (Example 3.2 graded T), :398 (key row T), :262 (canon bullet), :279 (misconception), :308 (problem M3)", "FAIL",
    "Example 3.2 is graded T and computes int_0^1 x^(-1/2) dx = 2 'by the antiderivative 2 sqrt(x)' (L04 :106), then int f_n = 2 - 1/n from the antiderivative on (1/n^2, 1] (L04 :107). L03.html:164 states 'The page does not prove that this calculus value is the Lebesgue integral.' So the lambda-integral identity is used without proof while graded T. Lesson 4 says the calculus route is a consistency check only (:262), but the grade T is on the calculus value itself.",
    "Either prove int x^(-1/2) d(lambda) = 2 on the page (for example, by MCT applied to dyadic simple functions, the Prop 4.1 construction), or add the identity as a numbered Assumption and grade the example C (or 'T given Assumption X'). Change the key-results row at :398 to match; the problem M3 and misconception at :279 inherit the same basis.")

# ---- math
row("M6-a-math-L01-props", "2.4-math", "L01.html:80-111 (Def 1.1, Prop 1.3, Prop 2.1)", "PASS",
    "re-derived: (S2) from (S1) and complement identity; (S3) finite unions via empty sets; Prop 2.1(a) closure via U_J^c = U_{J^c}; (b) injectivity via non-empty blocks; (c) minimality. No gap found.")
row("M6-a-math-L01-ex31", "2.4-math", "L01.html:246-247 (Example 3.1)", "PASS",
    "finite unions of finite/cofinite sets stay cofinite or finite (complement inside a finite set); the even-integer union is neither finite nor cofinite. Hypotheses (N, cofinite) stated.")
row("M6-a-math-L02-props", "2.4-math", "L02.html:86-92 (Prop 1.3), :107 (Prop 1.5), :125-132 (Prop 2.1), :297 (Prop 3.1)", "PASS",
    "re-derived each step; Prop 2.1(a) finite-support argument valid (disjoint non-empty subsets of a finite set are finitely many); Remark 1.4 correctly locates the countable step in (c) and (d).")
row("M6-a-math-L02-finite-hypothesis", "2.4-math", "L02.html:51 (why-it-matters), :306 (canon bullet 1), :444 (key results row)", "FAIL",
    "The prose says 'every probability on a finite space is a sum of point weights'. Counterexample: Omega = {1,2}, F = {empty set, Omega}, P(empty)=0, P(Omega)=1 is a probability space on which no point weight exists (since {1} is not in F). Proposition 2.1 needs F = all subsets (its Assumption 1, L02 :123). The canon bullet and the key-results row drop that hypothesis.",
    "Add 'with every subset of Omega an event' at :51, 'when F is the power set' at :306, and the same condition at :444.")
row("M6-a-math-L03-props", "2.4-math", "L03.html:88-92, :116-117, :132, :158-159", "PASS",
    "re-derived: Prop 2.2 (monotone) via common refinement A_i ∩ B_j; Prop 3.2(a),(b) via sup definition; Prop 3.3 level-set measure argument (uses mu({x0})=0 as its Assumption 1); Prop 4.1(a) level sets are half-open intervals; (b) bracket with level set of value 1 of length 0. Numbers checked.")
row("M6-a-math-L03-level-set", "2.4-math", "L03.html:132 (Prop 3.3 proof 'level sets'), :158 (Prop 4.1 proof)", "FAIL",
    "'Level set' is used from Prop 3.3 onward but is not defined anywhere in the lesson; Definition 1.1 gives A_i = {s = a_i} without naming it.",
    "Define the level set {f = a} (or {f > t} as already used) in Definition 1.1 or the paragraph before Definition 2.1, then use the term.")
row("M6-a-math-L03-most-functions", "2.4-math", "L03.html:275 (canon bullet 1 'needed for most functions')", "FAIL",
    "'most functions' is a scope claim with no computation; the page only shows that x^2 is not simple (uncountable range, L03 :287).",
    "Replace with 'needed for functions that are not simple, such as x^2 (Misconceptions, first item)'.")
row("M6-a-math-L04-props", "2.4-math", "L04.html:64-82 (Thm 2.1 proof), :119-128 (Prop 4.1), :138-140 (Prop 4.2), :145 (Remark 4.3)", "PASS",
    "re-derived: MCT upper bound and lower bound via E_n = {f_n >= c s} increasing to Omega, continuity from below; Prop 4.1 disjoint intervals (1/(n+1),1/n], harmonic grouping bound m/2 for N=2^m-1; Prop 4.2 zero pattern. Remark 4.3 'neither hypothesis can be dropped' is witnessed by this same sequence (not monotone; no integrable bound), so it holds.")
row("M6-a-math-L04-dcT-hypothesis", "2.4-math", "L04.html:93-100 (Theorem 3.1 assumptions)", "PASS",
    "assumptions include measurability of f_n and f, pointwise convergence everywhere, measurable g with finite integral dominating |f_n| everywhere: the standard set of hypotheses; the statement f integrable with convergence is consistent with them. Stated without proof, so no proof row is needed.")
row("M6-a-math-L04-each-hypothesis", "2.4-math", "L04.html:257 ('each has a specific failure in this lesson'), :261 (pointwise and everywhere bullet)", "FAIL",
    "The sentence says each hypothesis has a specific failure in this lesson. The bullet on pointwise-everywhere convergence (:261) shows no failing example; it only says a.e. convergence is not used.",
    "Change to 'The first two hypotheses have a failure shown in this lesson; the pointwise-everywhere convention is only stated, not tested'.")
row("M6-a-math-L04-res-problems", "2.4-math", "L04.html:374-377 (R2 g-dominated example), :367-371 (R1), :379-385 (R3)", "PASS",
    "R2: f_n = n 1{(0,1/n^2]} has integral 1/n; g = floor(x^-1/2) dominates; level set length (2n+1)/(n^2(n+1)^2) identity verified; term bound 3/n^2 verified; finite integral. R3 argument uses only g >= f_n on I_n. Both solutions valid.")
row("M6-a-math-problems-L01-L03", "2.4-math", "L01.html:289-375 (problems), L02.html:339-405, L03.html:308-392", "PASS",
    "every worked solution re-derived: L01 M1 eight members, M2 {2,3}, M3 32, P1-P3, E1-E3, R1-R3; L02 M1-M3, P1-P3, E1-E3, R1-R3 (R3 is Prop 3.1); L03 M1-M3, P1-P3, E1-E3, R1-R3 (R3 gives infinity). No wrong answer found.")

# ---- labs
row("M6-a-lab-L01", "2.5-labs", "L01.html:121-238; tests/labs/M6/lab-M6-L01-1.py", "PASS",
    "hypothesis numbers (4, 16, 8; candidate fails complement closure; overlap rejected) match the printed output; interpretation (finite check only, three families only) does not overreach; code matches output. Runtime 0.01 s.")
row("M6-a-lab-L02", "2.5-labs", "L02.html:146-283; tests/labs/M6/lab-M6-L02-1.py", "PASS",
    "hypothesis 729/602 pairs, 3/20 weights failing total mass only, nu failing additivity: all printed lines match; interpretation says 'these three families only' / 'six-point space only', matching the code. Runtime 0.04 s.")
row("M6-a-lab-L03", "2.5-labs", "L03.html:169-269; tests/labs/M6/lab-M6-L03-1.py", "PASS",
    "all printed values recomputed. Note (not a FAIL): Part A's 'same function with the value at 1/2 set to 5' is built by adding a zero-length piece, so the equality is arithmetic, not a test of Prop 3.3's hypothesis mu({1/2})=0; the page states only what the output shows ('the value 1 both before and after') and does not claim the lab tests Prop 3.3.")
row("M6-a-lab-L04", "2.5-labs", "L04.html:148-252; tests/labs/M6/lab-M6-L04-1.py", "PASS",
    "printed 1..8 pattern, first zero 6 and 51, contributions 1/2..1/6, partial sums 2.019877 and 4.197279, grouping True match my recomputation; interpretation says the general claims are the proofs, not the lab. Docstring 'every value is exact except the rounded line' matches the code (float only in the partial-sum print).")
row("M6-a-lab-labels-and-grades", "2.3-grades", "L02.html:282, L03.html:268, L04.html:252; key results C rows L01 :395, L02 :446, L03 :415, L04 :400", "PASS",
    "each lab-derived row is C with the lab named as basis; Part B of L03 labelled numerical; no lab result is labelled T.")

# ---- prose / structure / DAG / hours / notation
row("M6-a-prose-hub-data-every", "2.9-prose", "course/modules/M/M6/index.html:37", "FAIL",
    "'Every result is proved on a page, computed by a lab on a finite or explicitly stated space, or generated as a SIMULATED instance.' Theorem 3.1 (DCT, L04.html:93, :101) is stated and not proved, and is not computed by a lab; Assumption L (L03.html:140) is an assumption, not a result. The 'every' claim is false for the stated theorem.",
    "Write: 'Every proved result is proved on a page; the dominated convergence theorem and the other stated theorems are stated with their assumptions and not proved here; labs compute exact or numerical checks on finite or explicitly stated spaces.'")
row("M6-a-prose-hub-core-reading", "2.9-prose", "course/modules/M/M6/index.html:180; course/modules/M/M6/L03.html:499; L04.html:484", "FAIL",
    "Hub: 'The curriculum names both texts as sources for this unit: Billingsley for measure and integration (Lessons 1 to 6) and Williams for the martingale results (Lessons 8 to 12).' curriculum/01-foundations.yaml:286-288 lists the two titles with no lesson mapping, so the lesson ranges are attributed to the curriculum without a source.",
    "Replace with: 'The curriculum names both texts as sources for this unit (curriculum/01-foundations.yaml:286-288), without a lesson mapping. No lesson attributes a result to either text.' Also drop 'as a source for measure and integration' on L03.html:499 and L04.html:484 or say 'as listed in the curriculum'.")
row("M6-a-prose-hub-lede-scope", "2.9-prose", "course/modules/M/M6/index.html:33", "FAIL",
    "'the results that finance uses, such as ... are stated and proved in that language': a universal claim about finance results, with no computation or citation behind it.",
    "Replace 'the results that finance uses' with 'results such as the expectation of a payoff ... are stated and proved in that language'.")
row("M6-a-prose-hub-prereq", "2.9-prose", "course/modules/M/M6/index.html:60; curriculum.json prereqs", "PASS",
    "'Those modules assume M1 and M2, and M1 assumes P0.1': curriculum.json gives M4 prereqs [M2], M5 prereqs [M2], M2 prereqs [M1], M1 prereqs [P0.1]. M1 is reached transitively; the closure {M1, M2, M4, M5, P0.1} is correct.")
row("M6-a-prose-hub-extends-L07", "2.9-prose", "index.html:64 ('M6 extends the second to a general sigma-algebra in Lesson 7'); L07.html dfn line", "PASS",
    "L07 defines conditional expectation given a general sub-sigma-algebra G in L2 (the dfn with 'G-measurable Y minimizing E[(X-Y)^2]'); the lesson read only for this claim (L07 is outside this slice).")
row("M6-a-prose-hub-cards-L01-L04", "2.9-prose", "index.html:143-146 (cards L01-L04) against the H1 and text of L01-L04", "PASS",
    "card titles and descriptions match the lesson H1s and sections (L01 axioms, partitions, countable unions; L02 monotonicity, additivity, continuity; L03 simple integral, sup, dyadic bracket; L04 MCT with proof, DCT with hypotheses, zero limit example). Cards L05-L12: titles match H1s (case style only differs); card text for those lessons is outside this slice.")
row("M6-a-prose-hub-objectives-ladder-placement", "2.9-prose", "index.html:46-166 (6 objectives, 9-item placement, 4 ladder rungs)", "PASS",
    "6 objectives (plan target six, range 4-8); placement 9 items: 7 prerequisite + 2 skill checks; answer keys verified (0.5, 3.5, 1.5, 0 for E[S_tau] by the stated walk, 7 for 1+2+4, Cauchy 1/n, completeness); ladder order Worked example, Completion, Independent, Stretch with rung-title spans.")
row("M6-a-prose-quiz-keys", "2.9-prose", "quiz items: index.html:94-134; L01.html:414-431; L02.html:465-500; L03.html:434-478; L04.html:419-460", "PASS",
    "every numeric data-answer re-derived (L01 32, 8, 16; L02 0.5, 0.6666666667 within 1e-6; L03 0.5, 0.1464, 4; L04 1, 1.5, 2.019877); every data-correct option is the true one; explain texts agree with the key result numbers.")
row("M6-a-prose-banned-process-words", "2.9-prose", "index.html, L01-L04 (grep for 'roughly half', 'about [digits]', 'historically', ellipsis, builder, verifier, round, unit report, REQUESTS)", "PASS",
    "no banned phrase; the two 'about' uses (L03.html:171, L04.html:152) are followed by a computed printed value (0.1464466094; 2.019877); no process words in learner text.")
row("M6-a-prose-structure", "2.9-prose", "all five slice pages", "PASS",
    "each lesson has why-it-matters, sections, canon-breaks, misconceptions, problem-set (mechanics, proof, empirical, research), key-results table with grades, quiz, references, lesson-nav; check_pages PASS. Grade legend present.")
row("M6-a-dag-dfn-once", "DAG", "dfn anchors in L01-L04 (def-sigma-algebra, def-probability-space, def-lebesgue-integral, def-monotone-convergence-theorem, def-dominated-convergence-theorem)", "PASS",
    "each slice concept defined once, in the lesson the curriculum assigns (curriculum/01-foundations.yaml:270-285); each dfn id appears once; unit-wide count of dfn elements across L01-L12 is 15 (L04, L08, L10 carry two each; L01-L03, L05-L07, L09, L11, L12 one each).")
row("M6-a-dag-links", "DAG", "concept links in index.html and L01-L04", "PASS",
    "all links target concepts.html anchors in the closure; prose-only terms (measurable function, Lebesgue measure, Borel, almost surely, Hilbert space) are not linked (plan section 12, Architect defaults).")
row("M6-a-notation", "2.4-math", "macros and symbols in index.html and L01-L04 vs notation/notation.json", "PASS",
    "macros used: \\Prob, \\indic, \\N, \\E (all registered with the same meaning); no use of registered symbols T, Phi, gamma_3, gamma_4, R^ast, R_f, \\mathbb{Q}. Local letters (mu, nu, lambda, tau, mathcal F, L, E_n, N) are not registered and are defined where used. Plan section 5 is respected.")

out = {
    "unit": "M6",
    "slice": "M6-a",
    "round": 1,
    "verifier": "round-1 independent verifier (Haiku), M6 slice a; did not build M6 and shares no context with the builders",
    "pin": "55b5634",
    "base": None,
    "checkout": "/tmp/verifyC1-M6-a",
    "scratch": "/tmp/M6-v/M6-a",
    "verified_at": sys.argv[1],
    "verdict": "FAIL" if any(r["status"] != "PASS" for r in ROWS) else "PASS",
    "rows": ROWS,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Slice: hub index.html, L01-L04 pages and tests/labs/M6/lab-M6-L01..L04-1.py. Architect ruling applied: no student-error "
        "mutants (lab twins are demonstrations; mutation testing applies to project graders only). Hours not judged on pace. "
        "Cards L05-L12, L05-L12 pages and project are outside this slice and were not verified."
    ),
    "summary": {},
}
n_fail = sum(1 for r in ROWS if r["status"] == "FAIL")
out["summary"] = {
    "rows": len(ROWS),
    "pass": sum(1 for r in ROWS if r["status"] == "PASS"),
    "fail": n_fail,
    "unverifiable": sum(1 for r in ROWS if r["status"] == "UNVERIFIABLE"),
    "mutants": 0,
    "fail_ids": [r["id"] for r in ROWS if r["status"] == "FAIL"],
}
with open("/tmp/verifyC1-M6-a/ledgers/M6/M6-a.json", "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print(json.dumps(out["summary"], indent=1))
