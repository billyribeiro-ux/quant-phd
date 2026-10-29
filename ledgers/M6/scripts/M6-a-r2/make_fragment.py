"""Writes the M6 slice-a round-2 verification fragment (verifier-authored; standard library only).

Run: .venv/bin/python -I ledgers/M6/scripts/M6-a-r2/make_fragment.py  (from the checkout root)
"""

import json

ROWS = []


def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    ROWS.append(r)


CARRY = "Carried from round 1 (cited passage byte-identical since the previous pin 55b5634): "
RE = "Re-verified at e22feb3: "

# ---- commands and tooling (all re-run on the round-2 pin)
row("M6-a-cmd-pin", "2.9-structure", "repository HEAD of /tmp/verifyC2-M6-a", "PASS",
    RE + "git rev-parse --short HEAD -> e22feb3 (detached); git diff 55b5634..e22feb3 touches the M6 pages, twins L05-L12, cards.json and grader; twins L01-L04 are byte-identical across the two pins (git diff --quiet).")
row("M6-a-cmd-check-pages", "2.9-structure", "tools/check_pages.py --unit M6", "PASS",
    RE + "stdout 'check_pages M6: PASS', exit 0.")
row("M6-a-cmd-check-dag", "DAG", "tools/check_dag.py --unit M6", "PASS",
    RE + "stdout 'check_dag M6: PASS'. The new text adds no concept link (the only added match for 'concept' is the word Misconceptions).")
row("M6-a-cmd-run-labs", "2.5-labs", "tools/run_labs.py --unit M6 --page L01 (and L02, L03, L04)", "PASS",
    RE + "four runs, each 'run_labs M6: PASS (1/1)'.")
row("M6-a-cmd-twins-isolated", "2.5-labs", "python -I -W error tests/labs/M6/lab-M6-L01-1.py ... L04-1.py", "PASS",
    RE + "all four exit 0 with 0 bytes of stderr (/tmp/M6-v/a-r2 captures).")
row("M6-a-cmd-page-smoke", "2.5-labs", "tools/page_smoke.py --unit M6 --pages index L01 L02 L03 L04 --skip-sweep", "PASS",
    RE + "'page_smoke M6: PASS'; each lab 0.0 s. Log of the run: this round's stdout (tail shows PASS for index and L04).")
row("M6-a-cmd-ruff-mypy", "2.9-structure", "ruff check, ruff format --check, mypy --no-incremental on tests/labs/M6/lab-M6-L01..L04-1.py", "PASS",
    RE + "'All checks passed!', '4 files already formatted', 'Success: no issues found in 4 source files'.")
row("M6-a-cmd-verify-refs", "2.1-citations", "tools/verify_refs.py --offline; tools/verify_refs.py --unit M6 (live)", "PASS",
    RE + "offline '560 entries, 0 problems'; live 'M6: 2 of 560 entries, 0 problems'.")
row("M6-a-cmd-collect", "2.5-labs", "tests/labs/M6 twins as written and their page embedding", "PASS",
    RE + "twins byte-identical to the previous pin; run_labs confirms that the embedded expected output equals the twin's stdout for L01-L04.")

# ---- citations
row("M6-a-cite-keys", "2.1-citations", "course/modules/M/M6/L01.html:470, L03.html:499, L04.html:484; index.html:177-178", "PASS",
    RE + "L03.html:499 and L04.html:484 re-read: both cite Billingsley by registry key billingsley2012probability without an edition string; the keys are in references/references.json (verify_refs live 2 of 560 for M6). L01.html:470 and index.html:177-178 carried from round 1 (lines unchanged).")
row("M6-a-cite-no-locator", "2.1-citations", "course/modules/M/M6/L01.html:470, L03.html:499, L04.html:484", "PASS",
    RE + "the changed sentences at L03.html:499 and L04.html:484 name no theorem, page or equation number from Billingsley; L04 states that no passage was read.")
row("M6-a-cite-no-curriculum-attribution", "2.1-citations", "course/modules/M/M6/L03.html:499, L04.html:484; index.html:180", "PASS",
    RE + "round-1 wording 'as a source for measure and integration' is removed; the pages now say 'as a source for this unit, without a lesson mapping'. curriculum/01-foundations.yaml:286-288 lists the two titles under sources with no lesson mapping (read), so the new wording matches the curriculum.")

# ---- numbers
row("M6-a-num-L03-table", "2.2-numbers", "course/modules/M/M6/L03.html lab Part B printed table (lines 257-266) and interpretation (line 268)", "PASS",
    RE + "ledgers/M6/scripts/M6-a-r2/recompute_a_r2.py (exact Decimal, 60 digits) reproduces all ten I_n, 1/3 - I_n and 2^-n to 10 decimals; every row satisfies 0 <= 1/3 - I_n <= 2^-n; I_n nondecreasing. At n = 10 the error is 0.0004819768 and the bound 0.0009765625 (recompute.txt).")
row("M6-a-num-L03-I1", "2.2-numbers", "L03.html:291 (gap 0.1869 and about 0.3333), :171 (I_1 about 0.1464)", "PASS",
    RE + "I_1 = (1/2)(1 - sqrt(1/2)) = 0.1464466094; 1/3 - I_1 = 0.1868867239, displayed 0.1869; 1/3 displayed 0.3333; 0.3333 - 0.1464 = 0.1869 on displayed digits, consistent.")
row("M6-a-num-L03-E3-rounding", "2.2-numbers", "course/modules/M/M6/L03.html:374 (problem E3, solution)", "PASS",
    RE + "unrounded terms 0.0517767, 0.0794593, 0.1004809 sum to 0.2317169 (recompute.txt); the page now says the sum is 0.231717 from the unrounded terms and that the three rounded values add to 0.2318, which is the displayed-digit sum 0.0518+0.0795+0.1005 = 0.2318 (checked). I_2 = 0.2317169538 printed by the lab agrees.")
row("M6-a-num-L04-partial-sums", "2.2-numbers", "L04.html:152, :248-249 (lab printed lines), :358, :450", "PASS",
    RE + "partial sums of 1/(n+1): N=10 gives 2.019877 and N=100 gives 4.197279 (exact Fraction, recompute.txt). Page lines carried from round 1 (unchanged); the L04 lab output lines are unchanged.")
row("M6-a-num-L02-602", "2.2-numbers", "L02.html:148 (602 of 729), :276, :318, :389-391, :446", "PASS",
    RE + "729 ordered disjoint pairs; 602 fail additivity for nu(A) = (|A|/6)^2 (exact enumeration, recompute.txt). Lines 148 and 446 unchanged; the quiz explanation at :511-514 region unchanged for this figure.")
row("M6-a-num-L02-values", "2.2-numbers", "L02.html:112, :136, :141, :148, :322, :348, :355, :361-373", "PASS",
    RE + "fair die: P({1,2}) + P({2,3}) = 2/3, P({1,2,3}) = 1/2, P({2}) = 1/6 (line 322, changed sentence, verified exact). Biased weights 1/2, 1/4, 1/8, 1/16, 1/32, 1/32 sum to 1 (line 136). 3/20 on six faces sums to 9/10 (line 148). Odd faces {1,3,5}: 21/32 (line 348). Carried for the unchanged lines.")
row("M6-a-num-L01-counts", "2.2-numbers", "L01.html:116, :227-236 (printed lines), :291, :305, :341", "PASS",
    CARRY + "L01.html:116, :227-236, :291, :305, :341 (none of these lines is in the round-2 diff; the diff of L01 touches only :51, :108, :246, :257-258, :260, :373, :412). Lab 1 counts 4, 16, 8 match the card text c007 (2^2, 2^4, 2^3).")
row("M6-a-num-L03-misc", "2.2-numbers", "L03.html:171, :310, :317, :324, :360", "PASS",
    CARRY + "none of these lines changed (L03 diff: :59, :275, :291, :374, :499). I_1 at :171 re-derived above.")
row("M6-a-num-L04-misc", "2.2-numbers", "L04.html:138, :294, :301, :306-308, :344, :374-376", "PASS",
    RE + "L04.html:308 (problem M3 solution, changed sentence) re-derived: 2*(1/4) + int_{1/4}^1 x^(-1/2) dx = 1/2 + 1 = 3/2 (recompute.txt). Other lines carried (not in the L04 diff: :51, :105-107, :257, :261-262, :279, :308, :398, :484).")
row("M6-a-num-hub-placement", "2.2-numbers", "index.html:73 (77.8 %, 88.9 %, bar 80 % of 9 items)", "PASS",
    CARRY + "index.html:73 unchanged; 7/9 = 77.8 %, 8/9 = 88.9 %, as before.")
row("M6-a-num-hub-hours", "2.2-numbers", "index.html:29, :40, :42, :141 (108 hours, 12 x 9)", "PASS",
    RE + "12 lessons x 9 h = 108 h (index.html:141, changed sentence re-checked); 108 + 42 = 150 h; 108/150 = 72 %, 42/150 = 28 % (index.html:29, :40, :42 unchanged). Hours are design targets; no pace judgement (architect ruling).")

# ---- grades
row("M6-a-grade-L01", "2.3-grades", "L01.html:75 (Prop 1.3 T), :97 (Prop 2.1 T), :245 (Example 3.1 T)", "PASS",
    CARRY + "heading lines unchanged; Example 3.1 proof re-read at :246-247 and verified (A_n = {2n}, union = even numbers, neither finite nor cofinite).")
row("M6-a-grade-L02", "2.3-grades", "L02.html:73, :100, :120, :289 (T claims)", "PASS",
    CARRY + "none of these lines changed; the T-graded Proposition 2.1 hypotheses are now stated with all subsets (L02.html:120-123, :444), and the T claim is restricted accordingly.")
row("M6-a-grade-L03", "2.3-grades", "L03.html:77, :105, :121, :147 (T claims), :415 (C row)", "PASS",
    CARRY + "none of these lines changed. The dyadic bracket (Proposition 4.1) is re-derived in this round (part (a) and (b) proofs read at :158-159).")
row("M6-a-grade-L04-thm31-ungraded", "2.3-grades", "L04.html:92-102 (Theorem 3.1 DCT, stated, not proved); key results :399", "PASS",
    CARRY + "Theorem 3.1 carries 'stated, not proved' in its title (L04.html:93) and the references paragraph (L04.html:484, changed) says it is not proved here; the key-results table has no T grade for it.")
row("M6-a-grade-L04-ex32-T", "2.3-grades", "L04.html:105-107 (Example 3.2), :398 (key row), :262, :279, :308", "PASS",
    RE + "Example 3.2 title now says the Lebesgue identity is assumed; the key row at :398 is graded C with basis 'Calculus antiderivative, §3; the identity with the Lebesgue integral is assumed'. The T grade is gone; the calculus values 2 and 2 - 1/n are re-derived (recompute.txt). The canon bullet (:262), the misconception (:279) and problem M3 (:308) state the same assumption.")

# ---- mathematics
row("M6-a-math-L01-props", "2.4-math", "L01.html:80-111 (Def 1.1, Prop 1.3, Prop 2.1); changed sentence :108", "PASS",
    RE + "Proposition 2.1 (:98-111) re-proved: (a) S1-S3 from the index rule x in U_J iff i(x) in J; (b) J -> U_J injective via a non-empty block; (c) minimality via countable unions with the j-th term B_j or empty. The sentence at :108 now says the rule is used in (a) and (b), which matches the proof (c uses only Proposition 1.3(a) and (S3)). Proposition 1.3 at :80-96 not in the changed set and carried.")
row("M6-a-math-L01-ex31", "2.4-math", "L01.html:246-247 (Example 3.1)", "PASS",
    RE + "parenthetical 'the cofinite sets' added at :246 (no mathematical change). Proof re-read: complements, finite unions (finite union of cofinite set with finite set is cofinite), counterexample A_n = {2n} with union the evens, infinite and co-infinite, so not in the family.")
row("M6-a-math-L02-props", "2.4-math", "L02.html:86-92 (Prop 1.3), :96 (changed), :107 (Prop 1.5), :125-132 (Prop 2.1), :297 (Prop 3.1)", "PASS",
    RE + "Proposition 1.3 (a)-(d) re-proved from (M1), (M2): (a) padding with empty sets gives finite additivity, (b) uses only (a), (c) disjointification with (b), (d) telescoping with (a). Changed :96 wording matches. Proposition 3.1 at :297 re-proved: P(A u B) = P(A) + P(B \\ A) and P(B) = P(B \\ A) + P(A cap B) use only finite additivity. Proposition 1.5 and 2.1 statements carried (unchanged lines).")
row("M6-a-math-L02-finite-hypothesis", "2.4-math", "L02.html:51 (why-it-matters), :120-123 (Prop 2.1 hypotheses), :306 (canon bullet), :444 (key results row)", "PASS",
    RE + "every use of Proposition 2.1 now carries 'finite and every subset an event' (:51, :117, :123, :306, :444). The round-1 counterexample (Omega = {1,2}, F = {empty, Omega}) does not contradict any statement: no unqualified finite-space claim remains (grep of 'finite space' and 'Proposition 2.1' in L02 and index).")
row("M6-a-math-L03-props", "2.4-math", "L03.html:88-92 (Prop 2.2), :116-117 (Prop 3.2 area), :132 (Prop 3.3 proof), :158-159 (Prop 4.1 proof)", "PASS",
    RE + "Proposition 4.1 (a) and (b) re-proved: s_n takes values k/2^n, 0 <= s_n <= x^2 <= s_n + 2^-n; I_n = sum of k/2^n (sqrt((k+1)/2^n) - sqrt(k/2^n)) is the simple integral; adding 2^-n to a simple function adds 2^-n to its integral. Proposition 3.3 proof at :132 uses the zero-measure point and monotonicity, which is correct. Lines :88-92 and :116-117 carried (unchanged).")
row("M6-a-math-L03-level-set", "2.4-math", "L03.html:59 (definition added), :132, :158, and the terminology at L03.html:446 (quiz explanation)", "FAIL",
    "The round-1 defect is closed: 'level set' of s at a is {s = a} (L03.html:59) before its first use at :132 and :158. But L03.html:446 (quiz explanation) now says 'Measurability is defined through the level sets {f > t}', which uses the just-defined term for the set {f > t}. Under the page's own definition {f > t} is not a level set of a value a.",
    "At L03.html:446 replace 'the level sets \\(\\{f > t\\}\\)' with 'the sets \\(\\{f > t\\}\\)'. Keep the term 'level set' for {s = a} only.")
row("M6-a-math-L03-most-functions", "2.4-math", "L03.html:275 (canon bullet)", "PASS",
    RE + "reworded to 'needed for functions that are not simple, such as x^2' with the reason (uncountably many values, so not simple). The scope word 'most' is gone; the claim is a direct consequence of Definition 2.1's domain.")
row("M6-a-math-L04-props", "2.4-math", "L04.html:64-82 (Thm 2.1 proof), :119-128 (Prop 4.1), :138-140 (Prop 4.2), :145 (Remark 4.3)", "PASS",
    RE + "Theorem 2.1 proof re-read: measurability via {f > t} = union of {f_n > t}; upper bound via monotone integrals; lower bound via simple s and E_n increasing to Omega (continuity from below, Lesson 2, Proposition 1.3(d)). Proposition 4.1 proof re-derived: I_n = (1/(n+1), 1/n], h_N <= g, sum 1/(n+1) >= m/2 by dyadic blocks (checked). Proposition 4.2 values 1 and 0 re-derived. Remark 4.3 carried (unchanged).")
row("M6-a-math-L04-dcT-hypothesis", "2.4-math", "L04.html:93-100 (Theorem 3.1 assumptions)", "PASS",
    CARRY + "L04.html:93-100 unchanged; the assumptions match the statement and the Remark 4.3 use.")
row("M6-a-math-L04-each-hypothesis", "2.4-math", "L04.html:257 ('Each hypothesis above does real work'), :261-262 (pointwise and everywhere, DCT not proved)", "FAIL",
    "The sentence at :257 says each hypothesis does real work and then says the 'pointwise-everywhere convention is only stated, not tested' (:261). The two hypotheses shown to be non-removable are monotonicity (Example 2.2 with Proposition 4.2) and domination (Proposition 4.1). The other hypotheses of Theorem 2.1 (measure space, measurability, non-negativity) and Theorem 3.1 (measurability, real-valued, measure space) have no failing example. So 'each hypothesis does real work' is an unsupported universal claim, and it contradicts the next bullet.",
    "Replace the :257 sentence with: 'Two hypotheses are shown to be needed: monotonicity (Example 2.2 with Proposition 4.2) and an integrable bound (Proposition 4.1). The other hypotheses are stated, and are not tested here.' Remove 'does real work' for the untested ones.")
row("M6-a-math-L04-res-problems", "2.4-math", "L04.html:367-371 (R1), :374-377 (R2), :379-385 (R3)", "PASS",
    CARRY + "none of these lines changed; R1 (limit of integrals vs integral of limit) matches Proposition 4.2; the problem solutions were checked in round 1 and the cited statements (Example 2.2, Proposition 4.2) are unchanged.")
row("M6-a-math-problems-L01-L03", "2.4-math", "L01.html:289-375 (problems; changed line :373), L02.html:339-405 (changed :364), L03.html:308-392 (changed :374)", "PASS",
    RE + "L02 P1 exercise (:364) now asks for Proposition 1.3(b) using only (a); its solution uses finite additivity only (checked). L03 E3 solution (:374) re-derived (see M6-a-num-L03-E3-rounding). L01 :373 states Lab 1 checks finite families only, which matches the twin docstring (tests/labs/M6/lab-M6-L01-1.py, lines 1-8). Other problem solutions carried from round 1 (unchanged lines).")

# ---- labs
row("M6-a-lab-L01", "2.5-labs", "L01.html:121-238; tests/labs/M6/lab-M6-L01-1.py", "PASS",
    RE + "twin unchanged; run_labs PASS; docstring says every check is over a finite family, matching the page's :373 bullet.")
row("M6-a-lab-L02", "2.5-labs", "L02.html:146-283; tests/labs/M6/lab-M6-L02-1.py", "PASS",
    RE + "twin unchanged; run_labs PASS; the claims at :148 and :282 (five set functions, 602 of 729) match the output.")
row("M6-a-lab-L03", "2.5-labs", "L03.html:169-269; tests/labs/M6/lab-M6-L03-1.py", "PASS",
    RE + "twin unchanged; run_labs PASS; the printed table reproduced by recompute_a_r2.py; the sentence at :268 about Part A and Part B matches the output.")
row("M6-a-lab-L04", "2.5-labs", "L04.html:148-252; tests/labs/M6/lab-M6-L04-1.py", "PASS",
    RE + "twin unchanged; run_labs PASS; the output lines (integrals 1, zero patterns 1/5 and 1/50, partial sums) match the recomputation and the docstring.")
row("M6-a-lab-labels-and-grades", "2.3-grades", "L02.html:282, L03.html:268, L04.html:252; key-results C rows L01 :395, L02 :446, L03 :415, L04 :400", "PASS",
    RE + "C rows for labs present; L04 key row for Example 3.2 changed to C (see M6-a-grade-L04-ex32-T).")

# ---- hub and prose
row("M6-a-prose-hub-data-every", "2.9-structure", "course/modules/M/M6/index.html:37", "PASS",
    RE + "the new sentence ('Each proved result is proved on its lesson page. A theorem that a lesson states without proof is marked as stated, not proved') is true for slice a: Theorem 3.1 (L04.html:93) is marked 'stated, not proved', and the grades in L01-L04 carry proofs or labs. Proofs of cross-lesson results (for example Lemma 10.2 in L10) are on their lesson page.")
row("M6-a-prose-hub-core-reading", "2.1-citations", "course/modules/M/M6/index.html:180; course/modules/M/M6/L03.html:499; L04.html:484", "PASS",
    RE + "index.html:180 now says 'named ... as sources for this unit, without a lesson mapping'; curriculum/01-foundations.yaml:286-288 lists the two titles with no lesson mapping (read). The round-1 lesson ranges are removed, so the attribution matches the curriculum.")
row("M6-a-prose-hub-lede-scope", "2.9-structure", "course/modules/M/M6/index.html:33 (lede)", "PASS",
    RE + "the lede now names three specific results (expectation of a payoff, conditional expectation given partial information, expected final wealth of a fair game under a bounded stopping rule). The last is Theorem 10.3 (L10.html:81-95, proof read: telescoping with Lemma 10.2). Conditional expectation is proved in L07 (other slice, not read here: an honest gap for this round).")
row("M6-a-prose-hub-prereq", "DAG", "course/modules/M/M6/index.html:60; curriculum.json prereqs", "PASS",
    CARRY + "index.html:60 unchanged; prerequisites M4, M5 and their closure as in round 1.")
row("M6-a-prose-hub-extends-L07", "DAG", "index.html:64; L07.html dfn line", "PASS",
    CARRY + "index.html:64 unchanged.")
row("M6-a-prose-hub-cards-L01-L04", "2.7-cards", "index.html:143-146 (cards L01-L04); course/modules/M/M6/cards.json cards c001-c042 for L01-L04", "PASS",
    RE + "index card names match H1s of L01-L04. cards.json L01-L04 cards re-read against the current lesson text: c006, c007, c010, c016, c017, c018, c030, c032, c036, c037, c039, c040 checked against the changed sentences and the lab outputs; c037 now carries the assumption and grade C, as the L04 key row does. Cards c009, c019, c033, c041 are removed in round 2 and do not leave a dangling reference (no id references in pages).")
row("M6-a-prose-hub-objectives-ladder-placement", "2.9-structure", "index.html:46-166 (objectives, placement, ladder)", "PASS",
    CARRY + "index.html:46-166 unchanged except lines 141 and 180 (re-checked above).")
row("M6-a-prose-quiz-keys", "2.9-structure", "quiz items: index.html:94-134; L01.html:414-431; L02.html:465-516 (L02q8 changed); L03.html:434-478; L04.html:419-460", "PASS",
    RE + "L02q8 (question: which proposition uses the countable form of (M2)) keyed to Proposition 1.3(d); distractors Proposition 3.1 and Proposition 1.5(a) use only finite additivity (verified). L01 quiz key: the σ-algebra on {1,2,3} is the middle option, checked against S2 and S3. Other quiz items carried.")
row("M6-a-prose-banned-process-words", "2.9-structure", "index.html, L01-L04 (grep for banned phrases, ellipses, process words)", "PASS",
    RE + "grep of index.html and L01-L04 for 'roughly half', 'historically', 'builder', 'verifier', 'round N', 'REQUEST', 'unit report', ellipses: no match. Scope words (only, all, every, any, always, same) are checked in the rows above where they bear a claim.")
row("M6-a-prose-structure", "2.9-structure", "all five slice pages", "PASS",
    RE + "section and card structure unchanged (checked by check_pages PASS).")
row("M6-a-dag-dfn-once", "DAG", "dfn anchors in L01-L04 (def-sigma-algebra, def-probability-space, def-lebesgue-integral, def-monotone-convergence-theorem ...)", "PASS",
    RE + "the new 'level set' text at L03.html:59 uses <em> and no <dfn>, so no concept is defined twice; anchors unchanged.")
row("M6-a-dag-links", "DAG", "concept links in index.html and L01-L04", "PASS",
    RE + "check_dag M6 PASS; no concept link added or removed in the round-2 delta.")
row("M6-a-notation", "2.4-math", "macros and symbols in index.html and L01-L04 vs notation/notation.json", "PASS",
    RE + "notation.json registers \\E, \\Prob, \\indic, \\N (all used with their registered meaning in the slice); the symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f and \\mathbb{Q} do not occur in L01-L04 or index.html (grep). The script letters \\mathcal F, G, L, C are local names, not registered symbols, and carry one meaning each within a page.")

frag = {
    "unit": "M6",
    "slice": "M6-a",
    "round": 2,
    "verifier": "round-2 independent verifier (Haiku), M6 slice a; did not build M6 and shares no context with the builders",
    "pin": "e22feb3",
    "base": "55b5634",
    "checkout": "/tmp/verifyC2-M6-a",
    "scratch": "/tmp/M6-v/a-r2",
    "verified_at": "2026-10-28T00:00:00+00:00",
    "verdict": "FAIL",
    "rows": ROWS,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Slice: hub index.html, L01-L04 pages and tests/labs/M6/lab-M6-L01..L04-1.py. Delta 55b5634..e22feb3 touches "
        "index.html (lines 33, 37, 141, 180), L01 (51, 108, 246, 257-258, 260, 373, 412), L02 (51, 96, 287, 306, 322, 364, 444, 510, 514), "
        "L03 (59, 275, 291, 374, 499), L04 (51, 105-107, 257, 261-262, 279, 308, 398, 484). Twins L01-L04 are byte-identical. "
        "Carry convention used: a round-1 PASS row is carried only when every line it cites is outside the round-2 diff, "
        "with the prefix 'Carried from round 1'; rows touching a changed line are re-verified ('Re-verified at e22feb3'). "
        "Architect ruling applied: no student-error mutants (lab twins are demonstrations; mutation testing applies to project graders only). "
        "Hours are design targets and not judged on pace. Cross-slice pages (L05-L12, project, grader) are outside this slice and not verified here. "
        "Not checked in this round: the Proposition 1.3 text at L01.html:80-96 beyond the changed sentence; conditional expectation proof in L07 (for the hub lede)."
    ),
    "summary": {},
}
n_fail = sum(1 for r in ROWS if r["status"] != "PASS")
frag["summary"] = {
    "rows": len(ROWS),
    "pass": len(ROWS) - n_fail,
    "fail": n_fail,
    "unverifiable": 0,
    "mutants": 0,
    "fail_ids": [r["id"] for r in ROWS if r["status"] != "PASS"],
}
with open("ledgers/M6/M6-a.json", "w", encoding="utf-8") as fh:
    json.dump(frag, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("wrote ledgers/M6/M6-a.json rows", len(ROWS), "fail", n_fail)
