"""Builds the round-3 fragment ledgers/M5/M5-a.json for slice a (hub, L01-L04, twins, cards). Data only; no checks run here."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyS3-M5-a")
S = "ledgers/M5/scripts/M5-a-r3/"
PASS, FAIL = "PASS", "FAIL"


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != PASS:
        r["fix"] = fix
    return r


rows = [
    # ---- hub
    row("A1-hub-structure", "2.9 structure", "course/modules/M/M5/index.html:1-174", PASS,
        "Read in full this round. Order: header 30-43, objectives 45-56, prerequisites 58-67, placement 69-127, lessons 129-144, ladder 146-155, data 157-160, reading 162-169. " + S + "check_pages_M5.out: 'check_pages M5: PASS'."),
    row("A1-hub-hours", "2.9 hours arithmetic", "index.html:29, 31, 42; L01-L10 data-hours", PASS,
        "index.html:29 data-hours-lessons=104, data-hours-project=26; 104+26=130 = curriculum hours (curriculum/01-foundations.yaml:233). Per-lesson data-hours (grep): L01-L06=10, L07-L10=11, so 6*10+4*11=104 (" + S + "recompute_a_r3.out). 26/130=20.0% (inside 10-40%). Eyebrow index.html:42 '104 h lessons · 26 h project (20% of the 130 module hours)' matches. check_pages M5 PASS."),
    row("A1-hub-objectives", "2.9 objectives", "index.html:45-56", PASS,
        "Six objectives, each with a verb and a named lesson. Claims checked: L01 Thm 1.2 and Cor 1.4; L02 Prop 2.2, Thm 2.5, Cor 3.2 ('exactly when'); L03 Prop 1.4 and Prop 3.1; L04 metric axioms and L05 Prop 2.1 (uniform limit continuous, block title grep of L05.html); L07 Banach with a priori bound (block-title grep of L07.html: Theorem 2.1, Corollary 3.2); L08 contraction and L09 certified bound (block-title grep of L08/L09.html); L10 Corollary 3.2 closed form (block-title grep of L10.html). L05-L10 bodies belong to other slices; only block titles were read here."),
    row("A1-hub-prereqs", "2.9 prerequisites and concept links", "index.html:58-67; course/concepts.html anchors", PASS,
        "M2 and M1 titles as in round 2 (not re-read). Concept anchors present in course/concepts.html (grep id= count 1 each): limit, derivative, definite-integral, discount-factor, geometric-series, evidence-grade, project-ladder, cauchy-sequence, completeness-of-reals, epsilon-delta-continuity, metric-space. evidence-grade (concepts.html:39) and project-ladder (concepts.html:40) read 'not yet released'. L10 Darboux definition at L10.html:80 (within section 2 at L10.html:78)."),
    row("A1-hub-placement-structure", "2.9 placement diagnostic", "index.html:69-127", PASS,
        "data-mastery=0.8 (index.html:69). Nine items with prompts at lines 74, 83, 92, 97, 102, 107, 112, 117, 122: seven prerequisite items and two data-skill items (117, 122). 0.8*9=7.2, so 8 correct needed; 7/9=77.8% and 8/9=88.9% (" + S + "recompute_a_r3.out, PASS rows)."),
    row("A1-hub-placement-answers", "2.2 numbers in prose and answer keys", "index.html:73-124", PASS,
        "Every answer key recomputed in " + S + "recompute_a_r3.py (71 checks, all PASS, " + S + "recompute_a_r3.out): negation (x^2<0 exists); contradiction; ln(e^2)=2; 1/1.05 to six places = 0.952381 (|diff|=4.8e-8 < 5e-7); sum_{k=0}^3 2^k=15; lim_{x->2} x^2=4; d/dx x^3 at 1 = 3; skill 1 = (0.9/0.1)*0.2=1.8; skill 2 = 0.5*4=2."),
    row("A1-hub-placement-rung1-skill", "5.1 placement item tests rung-1 skill", "index.html:116-119; course/modules/M/M5/project.html:44, 113-114", PASS,
        "index.html:116-119 asks beta/(1-beta) times the largest change, 0.9/0.1*0.2=1.8. project.html:44 names 'the certified error of the iteration'; project.html:113-114 (Lab 1 step 5) prints beta/(1-beta) times that change. project.html line count unchanged by the round-2 to round-3 delta, so these locators still hold."),
    row("A1-hub-placement-rung2-skill", "5.1 placement item tests rung-2 skill", "index.html:121-124; project.html:45", PASS,
        "index.html:121-124: d(Gv,Gw) <= beta*d(v,w), beta=1/2, d=4 gives 2 (recomputed). project.html:45 asks the reader to fill in 'the two lines that carry the observed contraction ratio and the bound'; index.html:151 says the same removed step."),
    row("A1-hub-lesson-map", "2.9 lesson map and card text", "index.html:129-144", PASS,
        "Ten links L01-L10 resolve (ls course/modules/M/M5). Card hours 10 h (L01-L06) and 11 h (L07-L10) match data-hours. Card text for L01-L04 matches each lesson's block titles (L01 Def 1.1, Thm 1.2-1.6, Cor 1.4, Lemma 1.5; L02 Def 1.1, Def 2.1, Lemma 2.3, Thm 2.5, Cor 3.2; L03 Def 1.1, Prop 1.4, Prop 3.1; L04 Def 1.1, Prop 2.1, Prop 3.3, Example 1.6). L05-L10 card text matches their block titles (grep), not a body read."),
    row("A1-hub-ladder", "2.9 ladder and rung titles", "index.html:146-155; project.html:44-47", PASS,
        "Four rung titles in order (index.html:150-153). project.html:44-47 carry 'Rung 1 · Worked example', 'Rung 2 · Completion problem', 'Rung 3 · Independent project', 'Rung 4 · Stretch'."),
    row("A1-hub-data-status", "2.8/2.9 data status", "index.html:157-160; L08.html:138; L09.html:132; L10.html:177", PASS,
        "No lab reads a data file: grep 'data-files' in M5 pages returns no match. SIMULATED labels present in L08 (line 138), L09 (132), L10 (177). No currency value in M5 pages (grep for dollar, USD, EUR, cents returned none). index.html:159 claim holds."),
    row("A1-hub-reading", "2.1 citations and reading list", "index.html:162-169; references/references.json; tools/verify_refs.py", PASS,
        "data-cite keys abbott2015understanding and rudin1976principles: " + S + "verify_refs_offline_all.out 'offline integrity: 560 entries, 0 problems'; " + S + "verify_refs_M5_live.out 'live re-verification of M5: 2 of 560 entries, 0 problems'. Hub line 168 claim: the two results cited from M1 are M1 Lesson 2 Corollary 2.6 ('no rational number has square 2', M1 L02.html:132-133) and M1 Lesson 6 Theorem 2.2 (closed form of S_n(q) for q != 1, M1 L06.html:97-99 with S_n(q) of Definition 2.1 at M1 L06.html:90-93). Abbott and Rudin were not opened; no locator is asserted from them."),
    # ---- L01
    row("A1-L01-structure", "2.9 structure and template order", "course/modules/M/M5/L01.html:1-495", PASS,
        "Read in full this round. Header, why-it-matters, §1 to §3 (lab inside §3, L01.html:144-231), §4 canon breaks (L01.html:250), §5 misconceptions (260), §6 problems (278), §7 key results (383), §8 quiz (400), §9 references (481), next-link. check_pages M5 PASS (" + S + "check_pages_M5.out)."),
    row("A1-L01-math", "2.4 mathematics: theorems, proofs, notation", "L01.html:55-137 (Def 1.1 at 57, Thm 1.2 at 66, Thm 1.3 at 81, Cor 1.4 at 96, Lemma 1.5 at 114, Thm 1.6 at 127); L01.html:233-245 (Prop 1.7 at 233, proof at 241)", PASS,
        "Read every proof. Thm 1.2 uses (H3) for n+1 in N. Thm 1.3 nested-interval proof checked both orders (n<=m and m<n). Cor 1.4 uses H4. Lemma 1.5 uses m>=0 (x>=m>=0 gives x^2>=m^2). Thm 1.6 induction checked for both branches (m_n in S0 or not) and the width (b0-a0)/2^n. Prop 1.7 both cases re-derived: s^2<2 witness eps=min{1,(2-s^2)/(2s+2)} gives (s+eps)^2<2; s^2>2 witness delta=(s^2-2)/(4s), t=s-delta gives t^2>2 (random-s check in recompute_a_r3.out). Canon breaks L01.html:250-259 re-derived (rational lub gives q^2=2). Misconceptions L01.html:260-277 correct. Hypotheses of every T result are complete."),
    row("A1-L01-numbers", "2.2 numbers in prose and lab output", "L01.html:146, 213-230, 338, 345, 352, 425, 439, 444, 456", PASS,
        "Lab output (L01.html:213-229) re-run by the twin (" + S + "twin_L01.out): steps 0-12 widths 2/2^n, step 12 bracket [181/128, 2897/2048], 13 of 13, first width below 1/1000 at step 11 (1/1024). Prose numbers recomputed in recompute_a_r3.out: E1 181^2=32761 < 32768=2*128^2 and 2897^2=8392609 >= 8388608=2*2048^2; width 2897/2048-181/128=1/2048; E2 2^9=512, 2^10=1024; E3 steps 4 and 5 brackets; M3 steps 1 and 2; quiz q5 (7/5)^2<2, (141/100)^2<2, (3/2)^2>=2; q6 least natural above 1000.5 is 1001."),
    row("A1-L01-problems", "2.4/2.9 problem set with worked solutions", "L01.html:278-381 (problem set at 278; mechanics 284, proof 309, empirical 334, research 359)", PASS,
        "All twelve problems read (M1-M3, P1-P3, E1-E3, R1-R3). Solutions re-derived: M1 sup(0,1)=1 witness (1+max(y,0))/2; M2 maximum equals supremum and sup{1-1/n}=1; M3 bisection steps 1-2 [1,2] and [1,3/2]; P1 Cor 1.4 proof; P2 approximation; P3 iff with H3; E1-E3 numbers as above; R1 cubic set (cube monotone); R2 endpoints rational; R3 infimum via -B. No defects."),
    row("A1-L01-quiz-keyresults", "2.9 quiz keys and key-results table", "L01.html:383-399 (key results), 400-480 (quiz)", PASS,
        "Quiz items L01q1-L01q10: correct options and explanations re-checked (Def 1.1; S has no largest element; q3 width 2/8=1/4; q4 step 11; q5 upper bound 3/2 with 7/5 and 141/100 not upper bounds; q6 1001; q7 rational lub; q8 s^2=2; q9 Archimedean; q10 supremum in bracket, width (b0-a0)/2^n). Key-results table rows all grade T and match proofs on the page."),
    row("A1-lab-L01-1", "2.5 lab: run, twin, page equals twin, expected equals output", "tests/labs/M5/lab-M5-L01-1.py; L01.html:144-231", PASS,
        "run_labs M5 --page L01: 'run_labs M5: PASS (1/1)' (" + S + "run_labs_M5_L01.out). Twin alone under python -I -W error: exit 0, stderr 0 bytes, output in " + S + "twin_L01.out. Lab is standard library only, seeded not needed (no randomness). Hypothesis numbers match output (13 of 13; step 11)."),
    row("A1-lab-L02-1", "2.5 lab: run, twin, page equals twin, expected equals output", "tests/labs/M5/lab-M5-L02-1.py; L02.html:212-296", PASS,
        "run_labs M5 --page L02: 'run_labs M5: PASS (1/1)' (" + S + "run_labs_M5_L02.out). Twin alone under python -I -W error: exit 0, stderr 0 bytes (" + S + "twin_L02.out/.err); twin output equals the expected block at L02.html:287-293 line for line. Standard library only; exact Fraction sums; no randomness. Lab hypothesis (L02.html:214) numbers 200 of 200, 1830, first index 10 match the output."),
    # ---- L02
    row("A1-L02-structure", "2.9 structure and template order", "course/modules/M/M5/L02.html:1-554", PASS,
        "Read in full this round. Sections §1 to §9 in order, lab at L02.html:212-296, canon breaks at 297, misconceptions at 307, problem set at 325, key results at 430, quiz at 449, references at 539, next-link. check_pages M5 PASS (" + S + "check_pages_M5.out)."),
    row("A1-L02-math", "2.4 mathematics: hypotheses, proofs, grades", "course/modules/M/M5/L02.html:170-181 (Proposition 3.3 block at 170; H2 at 174; proof at 179-181)", FAIL,
        "Read every theorem and proof on the page. Proposition 3.3 now lists (H2) completeness (L02.html:174) and says 'Only the consequence on divergence uses it, through Corollary 3.2.' The proof at L02.html:181 gives H_{2N}-H_N >= 1/2 (no completeness used) and then 'suppose the series converged. Then by Corollary 3.2 ... there would be N with |H_m-H_n|<1/2'. That invokes only the direction 'convergent implies Cauchy', which Proposition 2.2 proves without completeness (L02.html:84-94). Formally Corollary 3.2 is stated with (H2), so invoking it presupposes (H2), which holds; but the implication actually used (converges implies Cauchy) does not depend on (H2). So the divergence consequence does not use completeness, and the sentence at L02.html:174 states a dependency the proof does not have; (H2) is an unused hypothesis. Proposition 3.3 remains true without it. Other propositions checked: Prop 2.2, Lemma 2.3, Lemma 2.4, Thm 2.5 (H1,H2 both used), Cor 3.2, Lemma 3.4, Prop 3.5 (both directions re-derived), R3 geometric-decay argument (beta != 1 hypothesis used, Archimedean N). Remark 2.6 accurate.",
        fix="Either delete the (H2) item at L02.html:174 and the sentence 'Only the consequence on divergence uses it, through Corollary 3.2.', since the statement and proof hold without completeness; or keep (H2) and replace the sentence with an accurate statement that the proof does not use it. Card M5-c026 then matches (see A1-cards-L02)."),
    row("A1-L02-numbers", "2.2 numbers in prose and lab output", "L02.html:214, 287-293, 294, 379-403 (empirical problems E1-E3), 449-537 (quiz)", PASS,
        "Twin output (" + S + "twin_L02.out) matches the expected block (L02.html:287-293): 200 of 200; min gap 1/2 at N=1; 200 of 200 failing; 1830 of 1830 identities; first index 10; fails 0 to 9. recompute_a_r3.out: H_4-H_2=7/12; sum_{j=1}^{60} j = 1830; G3-G1=3/8; threshold check for N=0..20 (fails 0-9, passes 10-20); H_{2^k}>=1+k/2 for k<=10."),
    row("A1-L02-problems", "2.4/2.9 problem set with worked solutions", "L02.html:325-429", PASS,
        "All twelve problems read (M1-M3, P1-P3, E1-E3, R1-R3). Solutions re-derived: M1 1/n->0; M2 (-1)^n not Cauchy with eps=1; M3 G3-G1=3/8; P1-P3 standard; E1 witness pair (N,2N); E2 H_4-H_2=7/12; E3 sum of 60-n; R1 Lemma 3.4 role; R2 H_{2^k} bound; R3 Cauchy from geometric decay (beta^N<=1/(Nh), Archimedean N). No defects."),
    row("A1-L02-quiz-keyresults", "2.9 quiz keys and key-results table", "L02.html:430-448 (key results), 449-537 (quiz)", PASS,
        "Quiz items L02q1-L02q11: keys and explanations re-checked (Definition 2.1; Prop 2.2 yes; H2-H1 = 1/2; q4 1/n counterexample; G3 = 7/8; G_m-G_n = 1/2^n - 1/2^m; threshold N=10; sqrt(n) unbounded; rational Cauchy has no rational limit; 1830 pairs; completeness axiom used). Key-results rows are T and point to proofs on the page."),
    row("A1-L02-attribution", "2.1/2.4 attribution of the cited M1 result", "L02.html:541 (references paragraph); L02.html:421-424 (Research R3 problem and solution)", PASS,
        "Re-verified after the round-2 FAIL. The paragraph now says every theorem stated in this lesson is proved on the page, and that the finite geometric-sum formula (M1, Lesson 6, Theorem 2.2, which needs the ratio not equal to 1) is cited, not proved, in the solution to R3. M1 course/modules/M/M1/L06.html:97-99 states Theorem 2.2 as S_n(q) = (1-q^n)/(1-q) for q != 1, and L06.html:90-93 defines S_n(q) = sum_{k=0}^{n-1} q^k. R3 uses it with m-n >= 1, consistent."),
    # ---- L03
    row("A1-L03-structure", "2.9 structure and template order", "course/modules/M/M5/L03.html:1-460", PASS,
        "Read in full this round (L03.html:30-460). Sections §1 to §9 in order; lab L03.html:106-167; canon breaks, misconceptions, problems, key results, quiz, references. check_pages M5 PASS."),
    row("A1-L03-math", "2.4 mathematics", "L03.html:57-93 (Def 1.1 at 57, Lemma 1.3 at 66, Prop 1.4 at 79, Prop 1.5 at 92), L03.html:171-196 (Prop 2.1 at 171, Prop 2.2 at 185), L03.html:202-213 (Prop 3.1 at 202)", PASS,
        "Lemma 1.3 (|x+2| <= |x-2|+4 <= 5); Prop 1.4 with delta=min{1,eps/5}; Prop 1.5; Prop 2.1 both directions (negation to a sequence with 1/n); Prop 2.2; Prop 3.1 with x=1/delta, y=x+delta/2 gives f(y)-f(x)=x*delta+delta^2/4 >= 1. Definitions, hypotheses and canon-break examples re-derived (delta at 10 with eps=1; f(1)=5 with x=1+min(delta,1)/2 gives |x-5|>=3.5; y_n=2/(2n+1) not of the form 1/k and tends to 0)."),
    row("A1-L03-numbers", "2.2 numbers in prose and lab output", "L03.html:108, 161-165 (expected), 166 (interpretation), 298-320 (empirical problems E1-E3)", PASS,
        "Twin output (" + S + "twin_L03.out) matches expected block: 401 of 401; 7 points for delta=1/50; 7 of 7; first failing point 381/200 with |x^2-4|=14839/40000=0.370975; 29 failing points. recompute_a_r3.out confirms each, plus 5|x-2|=95/200 at 381/200, 15 positive-side and 14 negative-side failing k (E3), x=3 sharp constant R1, 2+1/400 not a grid point (R2), 1/19<1/10 (M3), 2/(2n+1)<=1/n (misconception 3)."),
    row("A1-L03-problems", "2.4/2.9 problem set", "L03.html:242-346 (problem set at 242)", PASS,
        "All twelve problems read and re-derived: M1 (3x+1, delta=eps/3); M2 delta=1/50; M3 1/x at 1; P1 |x|; P2 |f|; P3 x^2 with delta=min{1,eps/(1+2|x0|)}; E1 bound at 381/200 (|x-2|=19/200, 5|x-2|=95/200); E2 seven points 397/200 ... 403/200; E3 counts; R1 sharp constant 5; R2 grid check with g = x^2+1 off grid (x=2+h, 0<h<1/200, |g(x)-g(2)|>=1); R3 max inequality re-derived by cases."),
    row("A1-L03-quiz-keyresults", "2.9 quiz keys and key-results table", "L03.html:347-363 (key results), 364-444 (quiz)", PASS,
        "Quiz items L03q1-L03q10 re-checked (Def 1.1; delta 0.02; delta depends on eps; f(1)=5 not continuous; least c=5; Prop 2.1 quantifies over every sequence; x^2 not uniformly continuous; 29; 401; |x+2|<=5). Key-results rows T and match the page."),
    row("A1-lab-L03-1", "2.5 lab", "tests/labs/M5/lab-M5-L03-1.py; L03.html:106-168", PASS,
        "run_labs M5 --page L03: PASS (1/1) (" + S + "run_labs_M5_L03.out). Twin alone under python -I -W error: exit 0, stderr 0 bytes (" + S + "twin_L03.out/.err). Exact Fraction arithmetic; no randomness."),
    # ---- L04
    row("A1-L04-structure", "2.9 structure and template order", "course/modules/M/M5/L04.html:1-480", PASS,
        "Read in full this round (L04.html:1-480). Sections §1 to §10 in order (metric axioms and facts F1-F6 §1; open sets §2; completeness §3; continuity §4; canon breaks §5; misconceptions §6; problem set §7; key results §8; quiz §9; references §10). Lab L04.html:103-210. check_pages M5 PASS."),
    row("A1-L04-math", "2.4 mathematics (changed subject: Prop 1.7 hypothesis (4), Prop 1.7 still re-derived)", "L04.html:78-83 (Prop 1.4 at 78), 221-237 (Prop 1.7 at 221, hypothesis at 223, proof at 226), 242-251 (Prop 2.1), 252-256 (Remark 2.2), 259-298 (Section 3, Prop 3.3 at 270, Prop 3.4 at 280, Example 3.6 at 295), 307-321 (Prop 4.2 at 307), 322-330 (canon breaks)", PASS,
        "Prop 1.7 hypothesis (4) (L04.html:223) is used in the finiteness step (supremum of {|f-g|} bounded by 2M); the proof's M1-M3 re-checked. Prop 1.4 Lagrange identity re-expanded symbolically (u1^2 v2^2 + u2^2 v1^2 - 2 u1 v1 u2 v2) and checked on all 7^4 integer samples in [-3,3] (recompute_a_r3.out). Prop 2.1 (open balls), Prop 3.3, Prop 3.4 (coordinatewise Cauchy, eps/2 choice), Prop 4.2, Example 3.6 (F4, F5, F6 chain) and Example 4.3 re-derived. Canon breaks (q(x,y)=(x-y)^2; |x^2-y^2| pseudometric; unbounded f on R; completeness depends on space) verified. Misconceptions verified (closed/open (0,1] with min(r/2,1))."),
    row("A1-L04-numbers", "2.2 numbers in prose and lab output", "L04.html:105, 198-208 (expected), 209 (interpretation), 340-372 (problem set), 393-464 (quiz)", PASS,
        "Twin output (" + S + "twin_L04.out) matches expected block (L04.html:198-208): Part A 25/625/15625 with 0 failures; Part B 27/729/19683 with 0 failures; Part C 3/9/27 with 2 triangle failures and d(0,2)=4, d(0,1)+d(1,2)=2. recompute_a_r3.out re-counts each independently (grid 5x5, vectors (0,1,2)^3, squared distance) and finds the same counts and the same two triples (0,1,2),(2,1,0). Mech1 d2=5; Mech3 d_inf=1/4 at x=1/2; Research1 psi monotone and subadditive; Proof2 min(|x-y|,1) triangle checked over a grid."),
    row("A1-L04-problems", "2.4/2.9 problem set", "L04.html:340-372 (problem set; L04-proof-1 at 351, L04-res-3 at 371)", PASS,
        "All mechanics, proof, empirical and research problems read. Solutions re-derived: Mech2 finite metric (recompute_a_r3.out checks all triples); Proof1 pseudometric d(1,-1)=0; Proof2 truncated metric; Proof3 uniform closeness implies pointwise; Emp1 25^3=15625; Emp2 the two failing triples (0,1,2),(2,1,0), other pairs not failing (re-enumerated); Emp3 27^3=19683 and sup distance 2; Research1 psi argument; Research2 closed subsets of complete spaces; Research3 constants preserve distance. No defects."),
    row("A1-L04-quiz-keyresults", "2.9 quiz keys (re-verified after round-2 FAIL) and key-results table", "L04.html:429 (L04q5 explanation); L04.html:393-464 (quiz); L04.html:376-391 (key results)", PASS,
        "Re-verified after the round-2 FAIL. L04q5 explanation (L04.html:429) now lists three separate triples: (0,0,1) reads 1<=1, (0,1,0) reads 0<=2, (0,1,1) reads 1<=1; each is re-checked and each holds (recompute_a_r3.out, row 'L04 Q5 explanation triples'). Option 1 (x=y=0, z=1) and option 3 (x=y=z) repeat a point and violate nothing. Other items L04q1-L04q9 keys re-checked (three axioms; 5; (0,1] not open; 19683; Prop 3.3 hypothesis; closed set definition)."),
    row("A1-lab-L04-1", "2.5 lab", "tests/labs/M5/lab-M5-L04-1.py; L04.html:103-210", PASS,
        "run_labs M5 --page L04: PASS (1/1) (" + S + "run_labs_M5_L04.out). Twin alone under python -I -W error: exit 0, stderr 0 bytes (" + S + "twin_L04.out/.err). Standard library only; enumerated samples; no randomness."),
    # ---- cards
    row("A1-cards-L01", "2.7 cards for L01 (one per 10 sampled, all read)", "course/modules/M/M5/cards.json: M5-c001-c016, c191, c216", PASS,
        "All 18 L01 cards read against L01.html (" + S + "cards_L01-L04_dump.out). Changed card M5-c006 (cards.json:37-41) now carries the Corollary 1.4 hypotheses (H1-H4, L01.html:97-101) and its answer matches. Numbers on cards (12 steps and [181/128, 2897/2048], width 1/2048; step 11; 13 of 13; rational lub has square 2) match L01.html and the lab output."),
    row("A1-cards-L02", "2.7 cards for L02 (all read)", "course/modules/M/M5/cards.json: M5-c017-c034, c213, c214, c217; card M5-c026 at cards.json:185-189", FAIL,
        "Card M5-c026 states the Proposition 3.3 hypothesis as only H_n = sum of 1/k. The lesson's Proposition 3.3 (L02.html:174) also lists (H2) completeness. A card must carry its proposition's hypotheses (VERIFIER_RULES 2.7, round rule 10). Other L02 cards read and correct (c017-c034, c213, c214, c217; c032/c033/c034/c217 labelled C and naming Lab 1; c031 matches L02.html section 4). Full-scan duplicate check A1-cards-duplicates passes.",
        fix="Make card M5-c026 agree with the lesson. If the lesson drops (H2) as recommended in A1-L02-math, the card is already correct. If the lesson keeps (H2), add 'every nonempty subset of R bounded above has a supremum' to the card front."),
    row("A1-cards-L03", "2.7 cards for L03 (all read)", "course/modules/M/M5/cards.json: M5-c035-c049, c218, c219", PASS,
        "All 17 L03 cards read against L03.html. c040 Prop 2.1 hypotheses match L03.html:171-177; c042 Prop 3.1 with eps=1; c043 least constant 5 and x=3; c044 point 10 with delta=1/5 and 10.1 gives 2.01; c046 y_n=2/(2n+1) example matches L03.html:224-241 (misconceptions); c047/c048/c049 numbers match lab output and E3; c219 first failing point 381/200 matches lab output."),
    row("A1-cards-L04", "2.7 cards for L04 (all read)", "course/modules/M/M5/cards.json: M5-c050-c068, c190, c192, c193, c201, c215, c220; changed card M5-c056 at cards.json:399-403", PASS,
        "All 26 L04 cards read against L04.html. Changed card M5-c056 (Prop 1.7) now lists hypothesis (4) completeness, matching L04.html:223. c062 (M3 fails at (0,1,2), q(0,2)=4 > 2) and c066/c067/c068 match the lab output; c061 (1/n in (0,1]) matches Example 3.6; c192 matches Proof 1; c220 (0 failures) matches Part A."),
    row("A1-cards-duplicates", "2.7 full scan for duplicates", "course/modules/M/M5/cards.json (236 cards, all lessons)", PASS,
        "Scripted scan (" + S + "cards_dump.py, output " + S + "cards_L01-L04_dump.out head): 236 cards, 0 duplicate ids, 0 duplicate fronts, 0 duplicate backs (case-folded). Keys used: back, basis, front, grade, id, lesson. Grades T 108, C 56, absent 72 (definitional cards carry no grade)."),
    # ---- cross-cutting
    row("A1-dag-concepts", "2.9 DAG and concept use", "check_dag M5; L01.html:59, L02.html:81, L03.html:59, L04.html:39; index.html:62-64", PASS,
        "check_dag M5 PASS (" + S + "check_dag_M5.out). Each concept used in slice a is in the M5 closure (M1, M2, P0.1) or defined earlier in the module: limit, derivative, definite-integral (M2); discount-factor, geometric-series (M1); evidence-grade, project-ladder (P0.1, 'not yet released'); completeness-of-reals (L01), cauchy-sequence (L02), epsilon-delta-continuity (L03), metric-space (L04). No bellman-equation, principle-of-optimality, dynamic-programming, expected-utility, crra-utility or utility-maximization appears in slice a (grep). 'Bellman operator' appears only as M5's own operator (index.html:33, 53, 140, 150, 152)."),
    row("A1-notation", "3.1 notation registry (NOTATION)", "notation/notation.json; L01-L04.html; index.html", PASS,
        "Registered symbols (notation.json symbols): T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q. None appear in slice a (grep over math spans). Registered macros used in slice a: \\R, \\N only. Locally defined letters (S, S_N, H_n, G_n, I_n, C, L, B, D, K, M, N, ell^infty, d_2, d_infty, B(x,r), rho, phi, psi, kappa) each defined at point of use (L01.html:55-112 for S; L02.html:79-143 for C, H_n, G_N, S_N; L04.html:212-216 for ell^infty(S)). No collision with a registered meaning."),
    row("A1-banned-phrases", "2.9 banned phrases (BUILDER_RULES 1.3-1.4)", "index.html; L01-L04.html; cards.json (slice-a cards)", PASS,
        "grep -i -E for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, it can be shown, of course, note that, we will, in this section, verifier, builder, round N, draft, placeholder: no matches in slice-a pages or cards. Ellipses appear only inside code (L01.html:170, L02.html:238, 243; L04.html:130) and in \\dots (math)."),
    row("A1-scope-words", "2.2/2.4 scope words (only, all, every, always, exactly, same)", "index.html; L01-L04.html", PASS,
        "Each use of 'every', 'all', 'only', 'exactly', 'always' in slice-a prose was read: 'all 401 points' (L03 lab) and 'all 200 of 200' (L02 lab) are computed; 'every theorem ... is proved on the page' (L02.html:541, L03 references, L04 references) holds for all T results in the slice, with the M1 result cited and not claimed proved; L01 footer 'Each theorem is proved on the page' holds for the theorems stated on L01; 'No lab reads a data file' holds (no data-files); 'exactly when' statements (Cor 3.2, Prop 3.5, Prop 2.1) are two-directional and proved."),
    row("A1-figures", "2.8 figures", "index.html; L01-L04.html", PASS,
        "No svg and no chart in index.html and L01-L04.html (grep '<svg' returns 0 for each). Figures are not in this slice; the module-level figure rules (2.8) therefore do not apply here."),
    # ---- gates (all re-run this round)
    row("A1-gate-check-pages", "2.9 gate: check_pages", "tools/check_pages.py --unit M5", PASS,
        "'check_pages M5: PASS' (" + S + "check_pages_M5.out, exit 0)."),
    row("A1-gate-check-dag", "2.9 gate: check_dag", "tools/check_dag.py --unit M5", PASS,
        "'check_dag M5: PASS' (" + S + "check_dag_M5.out, exit 0)."),
    row("A1-gate-check-projects", "2.6 gate: check_projects (project is outside this slice; gate run only)", "tools/check_projects.py --unit M5", PASS,
        "'check_projects M5: PASS' (" + S + "check_projects_M5.out, exit 0). The project and grader were not read by this slice."),
    row("A1-gate-run-labs", "2.5 gate: run_labs for hub and L01-L04", "tools/run_labs.py --unit M5 --page index|L01|L02|L03|L04", PASS,
        "run_labs M5 --page index: PASS (0/0). --page L01: PASS (1/1). L02: PASS (1/1). L03: PASS (1/1). L04: PASS (1/1). Files " + S + "run_labs_M5_index.out, run_labs_M5_L01.out ... L04.out, each with exit 0. Page code equals twin and expected equals output for all four labs."),
    row("A1-gate-page-smoke", "2.5/2.9 gate: page_smoke for hub and L01-L04 (alone)", "tools/page_smoke.py --unit M5 --pages index L01 L02 L03 L04", PASS,
        "'page_smoke M5: PASS', exit 0, light and dark, desktop and 360 px, figure sweep (no figures in slice). Output in " + S + "page_smoke_M5_a.out. Lab runtimes 0.0 to 1.5 s."),
    row("A1-gate-ruff-mypy-twins", "2.5 gate: ruff, mypy strict, twins", "ruff check . ; ruff format --check . ; mypy --no-incremental; python -I -W error on each twin", PASS,
        "ruff check: 'All checks passed!' (" + S + "ruff_check.out). ruff format --check: '553 files already formatted' (" + S + "ruff_format.out). mypy --no-incremental: 'Success: no issues found in 385 source files' (" + S + "mypy.out). Twins L01-L04 alone under python -I -W error: exit 0, stderr empty (" + S + "twin_L0*.out/.err)."),
    row("A1-gate-pytest", "2.5 gate: relevant pytest", "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py", PASS,
        "Exit 0, all tests passed (" + S + "pytest_M5_relevant.out). Not run: full suite (not in scope of slice a; only lab and page tooling touched)."),
    row("A1-gate-verify-refs", "2.1 gate: verify_refs", "tools/verify_refs.py --offline; tools/verify_refs.py --unit M5", PASS,
        "offline integrity: 560 entries, 0 problems (" + S + "verify_refs_offline_all.out). M5 live run: 2 of 560 entries, 0 problems (" + S + "verify_refs_M5_live.out). Both exit 0."),
    row("A1-gate-build-site", "2.9 gate: build_site --check (added this round; hub and lesson pages are generated-data inputs only indirectly)", "tools/build_site.py --check", PASS,
        "'site data current: 6 outputs', exit 0 (" + S + "build_site_check.out)."),
    row("A1-gate-render-curriculum", "3.1 gate: render_curriculum and diff (added this round)", "tools/render_curriculum.py; git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json", PASS,
        "Render ran; the diff of CURRICULUM.md and curriculum/curriculum.json is empty, exit 0 (" + S + "render_curriculum_diff.out). git status shows no tracked-file modification in the checkout."),
]

fragment = {
    "unit": "M5",
    "slice": "a",
    "round": 3,
    "verifier": "Haiku independent verifier, M5 slice a round 3 (did not build M5)",
    "pin": "8196077d5f56c3919d33e69888176d197d378ad4",
    "base": "9294b914a51647c66d2dee62c4a112c76ba04900 (round-2 pin; delta computed for M5 paths)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS3-M5-a",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyS3-M5-a/ledgers/M5/scripts/M5-a-r3",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta from 9294b914 to 8196077d for slice a: index.html (lede line 33, eyebrow 42, references 168); L02.html (Prop 3.3 H2 line 174; references 541); L04.html (Prop 1.7 hypothesis 223; L04q5 explanation 429); cards.json (c006 at 37-41, c056 at 399-403, plus L05-L10 cards not in slice); project.html (lede 34 and 232-235; in-place edits, line count unchanged, so hub locators 44-47, 113-114 still hold); L06-L10 pages and tests/labs/M5/lab-M5-L06-1.py, grader/test_project.py, plans/M5-open-items.md are outside slice a. L01.html, L03.html, lab twins for L01, L02, L03, L04 are byte-identical to 9294b914 (git diff shows no change), so their rows were re-verified in full this round rather than carried.",
        "Round-2 FAIL A1-L04-quiz-keyresults is fixed and re-verified PASS. Round-2 FAIL A1-L02-attribution is fixed and re-verified PASS. Round-2 PASS rows were all re-verified this round because index.html, L02.html, L04.html and cards.json changed as files.",
        "Two new non-PASS rows: A1-L02-math (Prop 3.3 states that completeness is used through Corollary 3.2 for the divergence consequence, but the proof uses only the direction convergent implies Cauchy, which needs no completeness) and A1-cards-L02 (card M5-c026 omits the (H2) hypothesis the lesson lists). Both are minor and have one-line fixes. No other defect found in slice a.",
        "No mutants: slice a contains no grader or project. Lab twins are demonstrations; mutation testing applies to project graders only (VERIFIER_RULES 2.6 and the rulings). mutate_graders.py and run_graders.py were not run for this slice; they belong to the project slice.",
        "Forward pointers (Section 3 of L02 'defined in Section 3', L04 'Section 1 facts', 'Section 5') are explicit section references, not undefined terms.",
        "Could not check: Abbott and Rudin locators (not opened; no lesson asserts a locator from either); L05-L10 mathematics beyond block-title grep for hub card text and hub objectives; project.html and grader contents beyond the lines the hub cites; P0.1 concept bodies (not released); live URL access was limited to the tools/verify_refs.py run (no plain curl to any publisher page); page_smoke timing on hardware other than this Mac.",
        "Scripts backing rows are in ledgers/M5/scripts/M5-a-r3/: gates_a_r3.sh (commands), recompute_a_r3.py (71 checks), cards_dump.py, build_fragment_a_r3.py (this fragment), and each *.out. The twins were run with the commands recorded in gates_a_r3.sh, using scratch copies under /tmp/m5a_r3_scratch.",
    ],
    "summary": "",
}
n = len(rows)
np_ = sum(1 for r in rows if r["status"] == PASS)
nf = n - np_
fragment["summary"] = (
    f"Round 3, slice a (hub, L01-L04 pages, lab twins, cards for L01-L04). {n} rows: {np_} PASS, {nf} FAIL. "
    "FAIL 1 (minor, A1-L02-math): Proposition 3.3 says completeness is used through Corollary 3.2 for divergence, "
    "but its proof uses only convergent implies Cauchy (no completeness). FAIL 2 (minor, A1-cards-L02): card M5-c026 omits "
    "the (H2) hypothesis the lesson lists. Round-2 FAILs (A1-L04-quiz-keyresults, A1-L02-attribution) are fixed. "
    "All gates pass (check_pages, check_dag, check_projects, run_labs, page_smoke, ruff, mypy strict, pytest subset, verify_refs, build_site, render_curriculum diff). "
    "Recomputation: 71 of 71 PASS."
)
out = ROOT / "ledgers/M5/M5-a.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, "rows", n, "pass", np_, "fail", nf)
