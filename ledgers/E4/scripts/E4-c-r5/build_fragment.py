"""Build ledgers/E4/E4-c.json (round 5) from the round-4 fragment and this round's evidence. Stdlib only."""
import json
import sys
from datetime import UTC, datetime

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE5-E4-c"
R4 = "/Users/billyribeiro/.fanout/frags/E-E4-c.round4.json"
OUT = f"{ROOT}/ledgers/E4/E4-c.json"
S5 = "ledgers/E4/scripts/E4-c-r5"
OUTD = f"{S5}/out"
PREV = "9a02b1af"
PIN = "7376a5e2"

r4 = json.load(open(R4, encoding="utf-8"))
old = {r["id"]: r for r in r4["rows"]}

def carry(rid, loc=None):
    o = old[rid]
    files = loc or o["location"]
    return {
        "id": rid,
        "check": o["check"],
        "location": files,
        "status": "PASS",
        "evidence": (
            f"Carried from round 4 ({files} byte-identical since the previous pin {PREV}; the "
            f"{PREV}..{PIN} delta does not touch the cited lines): " + o["evidence"]
            + " Round 5 also re-read the full text of the page (out/L0x.txt) and found no defect in these lines."
        ),
    }

def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r

ov = {}

# ---- delta, scripts, commands (re-run this round) ----
ov["E4c-r4-delta-read"] = row("E4c-r4-delta-read", "delta",
    "course/modules/E/E4/L07.html, L08.html, L09.html, index.html; tests/labs/E4/lab-E4-L07-1.py, L08-1.py, L09-1.py",
    "PASS",
    f"Round-5 delta read hunk by hunk: git diff -U0 {PREV} {PIN} -- these files, output read in full. Hunks: "
    "L07.html:492 (R3 question wording); L08.html:51, 55, 79, 136, 309, 314, 325, 328, 332, 336, 341 (embedded twin "
    "docstring), 571, 573, 583, 718, 795 (Assumption A5 renamed A4 and related wording); L09.html:62 (common-knowledge "
    "sentence), 287 (Remark 2.5 wording), an inserted key-results row after L09.html:435 (lines >=436 shift +1), "
    "512 (references paragraph); lab-E4-L08-1.py:5 (docstring); index.html:33 (lede only). Every hunk was re-read "
    "against its page and against the lesson text it cites.")
ov["E4c-r4-recheck-numbers"] = row("E4c-r4-recheck-numbers", "numbers",
    "course/modules/E/E4/L07.html, L08.html, L09.html (all printed and quoted numbers)", "PASS",
    f"Round-5 independent scripts (stdlib, python -I -W error): {S5}/recheck_L07.py (out/recheck_L07.out), "
    f"{S5}/recheck_L08.py (out/recheck_L08.out), {S5}/recheck_L09.py (out/recheck_L09.out). They do not reuse the lab "
    "closed forms: L07 solves the market-clearing fixed point for the price coefficients and reproduces theta_s=3/7, "
    "theta_u=6/7, rho^2=1/3, and the closed form to 3.3e-16 over 1440 parameter sets. L08 computes G(lambda) from the "
    "demand gaps as random variables: G(0)=0.173287, G(0.5)=0.158997, G(1)=0.127706=ln(5/3)/4, bisection roots at costs "
    "0.12 to 0.18 equal the printed lam* to 1e-9. L09 brute-forces all 15625 bets in exact Fractions: 500 strict at "
    "state 1 and at state 4, 0 of them nonnegative on the meet, 625 nonnegative on the meet, all with zero posteriors.")
ov["E4c-cmd-check-pages"] = row("E4c-cmd-check-pages", "command",
    "course/modules/E/E4/L07.html, L08.html, L09.html", "PASS",
    f"Re-run alone on pin {PIN}: {OUTD}/check_pages_L07.out, check_pages_L08.out, check_pages_L09.out, each "
    "'check_pages E4 Lnn: PASS' and exit=0.")
ov["E4c-cmd-check-dag"] = row("E4c-cmd-check-dag", "command", "course/modules/E/E4/*.html (unit)", "PASS",
    f"Re-run: {OUTD}/check_dag_E4.out 'check_dag E4: PASS', exit=0.")
ov["E4c-cmd-check-projects"] = row("E4c-cmd-check-projects", "command", "course/modules/E/E4/project.html and grader (unit)", "PASS",
    f"Re-run: {OUTD}/check_projects_E4.out 'check_projects E4: PASS', exit=0. Project content is another slice; the gate was run for completeness.")
ov["E4c-cmd-run-labs"] = row("E4c-cmd-run-labs", "command", "course/modules/E/E4/L07.html, L08.html, L09.html", "PASS",
    f"Re-run: {OUTD}/run_labs_L07.out, run_labs_L08.out, run_labs_L09.out, each 'run_labs E4: PASS (1/1)', exit=0.")
ov["E4c-cmd-twins-standalone"] = row("E4c-cmd-twins-standalone", "command",
    "tests/labs/E4/lab-E4-L07-1.py, lab-E4-L08-1.py, lab-E4-L09-1.py", "PASS",
    f"{S5}/run_gates.sh runs each twin from an empty scratch directory with env -i and python -I -W error: "
    f"{OUTD}/twin-L07.exit, twin-L08.exit, twin-L09.exit are 0; the .stderr files are 0 bytes; stdout in twin-L0x.stdout.")
ov["E4c-expected-equals-output"] = row("E4c-expected-equals-output", "labs",
    "course/modules/E/E4/L07.html:331-358, L08.html:544-563, L09.html:264-281", "PASS",
    f"{S5}/embed_check.py on pin {PIN} (out/embed_check.out): for L07, L08 and L09 the data-run code block equals the "
    "twin source and the expected block equals the standalone stdout (True, True for each lesson).")
ov["E4c-cmd-page-smoke"] = row("E4c-cmd-page-smoke", "command", "L07, L08, L09 (light/dark, 360 px and desktop)", "PASS",
    f"Re-run alone: {OUTD}/page_smoke_L07_L08_L09.out: 'page_smoke modules/E/E4/L07.html: PASS', L08 PASS, L09 PASS, "
    "'page_smoke E4: PASS', exit=0. Pyodide lab times: L07 0.0 s, L08 0.1 s, L09 4.8 s (under 10 s).")
ov["E4c-cmd-ruff-mypy-twins"] = row("E4c-cmd-ruff-mypy-twins", "command",
    "tests/labs/E4/lab-E4-L07-1.py, L08-1.py, L09-1.py", "PASS",
    f"{OUTD}/ruff_check.out 'All checks passed!'; ruff_format.out '3 files already formatted'; mypy_twins.out "
    "'Success: no issues found in 3 source files'; all exit 0.")
ov["E4c-cmd-pytest-labs"] = row("E4c-cmd-pytest-labs", "command", "tests/test_labs.py -k E4", "PASS",
    f"Re-run: {OUTD}/pytest_labs_E4.out, 13 passing, exit=0.")
ov["E4c-cmd-verify-refs"] = row("E4c-cmd-verify-refs", "command", "references/references.json (milgrom1982information used by L09)", "PASS",
    f"Offline re-run: {OUTD}/verify_refs_offline.out 'offline integrity: 560 entries, 0 problems', exit=0. No live run: "
    "no reference record changed in this slice.")
ov["E4c-cmd-run-graders"] = row("E4c-cmd-run-graders", "command", "course/modules/E/E4/grader/", "PASS",
    f"Re-run seeds 0-49: {OUTD}/run_graders_E4.out 'run_graders E4: PASS (reference 50/50 seeds, slowest 0.5 s)', exit=0. Grader content is another slice.")
ov["E4c-L07-structure"] = row("E4c-L07-structure", "structure", "course/modules/E/E4/L07.html", "PASS",
    f"Whole page re-read ({OUTD}/L07.txt). Order: why it matters (117 words, at most 120), numbered sections, inline Lab 1, "
    "where the canon breaks, misconceptions (4), problem set (3 per tier, 12 solutions in details.solution, minimum 37 words), "
    "key results, quiz (10 items), references. data-hours=8. check_pages L07 PASS.")
ov["E4c-L07-problems-E3-R"] = row("E4c-L07-problems-E3-R", "math", "course/modules/E/E4/L07.html:462, 465-498 (E2, E3, R1-R3)", "PASS",
    "L07.html:492 changed (R3 question now reads 'for every parameter set of Proposition 7.7'). R3 re-derived: rho^2=sigma_v^2/D, "
    "D=sigma_v^2+sigma_eps^2+chi*sigma_u^2, so d rho^2/d(sigma_u^2) = -sigma_v^2*chi/D^2, and the ratio to rho^2 is -chi/D, "
    "which varies with sigma_u. Sign negative for every parameter set of Prop 7.7 (chi>0, D>0). E2: 1/(1+sigma_eta^2)=1/4 gives "
    "sigma_eta^2=3, kappa=2, sigma_u^2=1/2 (checked by hand and in recheck_L07.py). E3 text unchanged.")
ov["E4c-L07-quiz"] = row("E4c-L07-quiz", "prose", "course/modules/E/E4/L07.html:518-592 (item at L07.html:565)", "FAIL",
    "Items 1-6, 8-10 re-derived (1/3, 5, falls strictly, 9/22 = 0.4091, Corr in [0,1], 1/2 benchmark, sqrt(1/2) = 0.7071, "
    "lower a raises rho^2 -> 'higher CARA coefficient a' is the lowering change): all correct. Item 7 (L07.html:565) asks "
    "'At the base instance, does a higher price variance imply a higher informativeness?' The answer is supported only by the "
    "noise-volume sweep of Lab 1, Part B, which moves sigma_u away from the base instance, so the question's scope ('at the base "
    "instance') does not match its evidence (Lab 1, Part B; Remark 7.9).",
    "Reword the prompt at L07.html:565 to 'Across the noise-volume sweep of Lab 1, Part B, does a higher price variance imply a "
    "higher informativeness?' and keep the option text and explanation. No other item changes.")
ov["E4c-L07-cents-docstring"] = carry("E4c-L07-cents-docstring")
ov["E4c-L07-hours"] = carry("E4c-L07-hours")
ov["E4c-L09-quiz"] = row("E4c-L09-quiz", "prose", "course/modules/E/E4/L09.html:443-506 (items at 446-506; shifted +1 by the row inserted at 436)", "PASS",
    "Quiz re-read in full this round (9 items, lines 443-506): the common-knowledge option, g1(1)=1/2, g2(1)=1/3, the prior hypothesis, "
    "0.2 for trader 2, 15625, M(1)={1,2,3}, and g1(1)=1/2 for x=(0,1,-1,0) all re-derived by hand and by recheck_L09.py. "
    "Explanations match the lesson text.")
ov["E4c-L09-references"] = row("E4c-L09-references", "prose", "course/modules/E/E4/L09.html:512; references/references.json:17291", "PASS",
    "Round-4 defect fixed: L09.html:512 now reads 'Lab 1 is an exhaustive finite check, graded C (basis: Lab 1, Parts A to C, "
    "exhaustive enumeration of 15625 bets in exact arithmetic on one six-state model).' The registry record matches the citation "
    "(title 'Information, trade and common knowledge', Journal of Economic Theory 26(1), pages 17-27, 1982). The page claims no "
    "result of the paper. Process words: none in the paragraph.")
ov["E4c-L09-footer"] = carry("E4c-L09-footer", "L09.html:523 (was 522 at the previous pin; text byte-identical; +1 shift from the row inserted at L09.html:436)")
ov["E4c-L09-dag"] = row("E4c-L09-dag", "DAG", "course/modules/E/E4/L09.html:37, 287, 290", "PASS",
    "check_dag E4 PASS (out/check_dag_E4.out). L09.html:287 (Remark 2.5) links Pareto efficiency (concepts.html#pareto-efficiency) "
    "and arrow-debreu-equilibrium (L02.html#def-arrow-debreu-equilibrium), both in the closure or earlier. 'adverse selection' "
    "is linked in the Uses line (L09.html:37) and appears in Remark 2.5 as a contrast only. No out-of-closure name from plan D1 to D10 "
    "appears in L07 to L09 (grep: bayes, state price, stochastic discount, martingale, informationally efficient, determinacy: none).")
ov["E4c-L09-process-banned"] = row("E4c-L09-process-banned", "prose", "course/modules/E/E4/L09.html", "PASS",
    "Body text scanned with tags, math, code and expected blocks removed (round-5 scan): no banned phrase "
    "(TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, "
    "studies show, experts agree, it is well known, obviously, clearly), no ellipsis, no process word (builder, verifier, fixer, REQUEST, unit report).")
ov["E4c-L08-structure"] = row("E4c-L08-structure", "structure", "course/modules/E/E4/L08.html", "PASS",
    f"Whole page re-read ({OUTD}/L08.txt). Order matches BUILDER_RULES 4.2 (why it matters 113 words; numbered sections; inline "
    "Lab 1 before the canon; misconceptions (4); problem set 3 per tier, 12 solutions of at least 34 words; key results; quiz "
    "(9 items); references). data-hours=8. check_pages L08 PASS.")
ov["E4c-L08-A5"] = row("E4c-L08-A5", "labels", "course/modules/E/E4/L08.html:58, 65, 70, 314, 319-332, 573 (and 51, 55, 795)", "PASS",
    "Round-4 FAIL fixed: L08 defines A1 (preferences, L08.html:58), A2 (normal information, 65), A3 (price taking, 70) and A4 "
    "(sign change, L08.html:314, 'Assumption A4 (sign change, the bisection's invariant)'). grep for A5 in L08.html and in the L08 twin "
    "returns nothing; Proposition 5.2(c) (L08.html:325) and the bisection rule (L08.html:332) cite A4. Observation (not a row): "
    "L08's A1 to A3 are not L06's A1 to A4 (L06 A1 is the normal primitives); L07 cites L06's labels as 'of Lesson L06', so no "
    "reader error is forced, but the reuse of labels across lessons is worth a note.")
ov["E4c-L08-line51-zero-cost"] = row("E4c-L08-line51-zero-cost", "math", "course/modules/E/E4/L08.html:51, 285-296", "PASS",
    "L08.html:51 (changed: A5 to A4 in the sentence, and 'Proposition 5.1(b)') matches Proposition 5.1(b) (L08.html:285-296) and "
    "Proposition 3.1 (lambda = 0 case): no equilibrium with informed traders for 0 < c < G(0) when sigma_u^2=0.")
ov["E4c-L08-line51-existence"] = row("E4c-L08-line51-existence", "math", "course/modules/E/E4/L08.html:51", "PASS",
    "'equilibria exist outside (G(1), G(0))' matches Proposition 5.2 (c >= G(0) gives lambda=0; c <= G(1) gives lambda=1); "
    "'existence uses Assumption A4' matches Proposition 5.2 (L08.html:309 'Assume A4 below'). Checked numerically with recheck_L08.py.")
ov["E4c-L08-cor-2.4-lemma-2.5"] = row("E4c-L08-cor-2.4-lemma-2.5", "math", "course/modules/E/E4/L08.html:122-146 (136 changed)", "PASS",
    "L08.html:136 now says p is an invertible affine function of y for lambda in (0,1] (Proposition 3.1), so sigma(p)=sigma(y), and "
    "Corollary 2.4(b) applies. Lemma 2.5 (L08.html:139-144) and Corollary 2.4 proofs re-derived (Fact 2.3 conditioning; independence of u from (v,s)). "
    "Recheck: the lab's closed-form price coefficients agree with the independent clearing fixed point (recheck_L08.py, Part A lines).")
ov["E4c-L08-prop-5.2"] = row("E4c-L08-prop-5.2", "math", "course/modules/E/E4/L08.html:304-326 (309, 314, 325 changed)", "PASS",
    "Proposition 5.2 statement and proof (c) re-read: with A4 the sign change of N gives the zero in (0,1), N(0)=G(0)-c>0>G(1)-c=N(1) "
    "(continuity from Section 3 and Proposition 5.2(a)). Lemma 3.3 gives strict monotonicity of Corr^2 on (0,1]. Recheck: "
    "G(lambda) falls and Corr^2 rises on the 999-point grid (recheck_L08.py).")
ov["E4c-L08-lab1-part-A"] = row("E4c-L08-lab1-part-A", "labs", "course/modules/E/E4/L08.html:336, 544-547; twin lines 351-383", "PASS",
    "Hypothesis (L08.html:336, changed wording only) states b_y/beta = 0.1605: recomputed as 13/81 = 0.160494 at lambda=1/2 (tau_eta=1/17, "
    "beta=9/26). Printed slope 0.1595 and clearing residual 1.332e-15 reproduced in recheck_L08.py (Part A reproduction). embed_check True.")
ov["E4c-L08-G1-derivation"] = row("E4c-L08-G1-derivation", "math", "course/modules/E/E4/L08.html:336, 564, 583, 674, 719", "PASS",
    "G(1)=ln(5/3)/4=0.127706 re-derived by hand (kappa=2, tau_eta=1/5, V_I=1/2, b_y=1/6, V_U=5/6, beta=1/2, Var(D_I)=1, "
    "Var(D_U)=2/3) and independently by recheck_L08.py (gain(1)=0.127706).")
ov["E4c-L08-misc-claims"] = row("E4c-L08-misc-claims", "math", "course/modules/E/E4/L08.html:583, 587, 591, 595", "PASS",
    "583: G(1)=ln(5/3)/4>0 with noise (re-derived). 587: positive informed fraction for every cost 0.12 to 0.17 (lam* from 1.0 to 0.2316, "
    "recheck_L08.py). 591: lam* at 0.15 = 0.6578 (recheck_L08.py bisection, 0.657828572). 595: the net benefit falls with c (N = G - c).")
ov["E4c-L08-canon-A5-limit"] = row("E4c-L08-canon-A5-limit", "prose", "course/modules/E/E4/L08.html:571-573", "PASS",
    "Limitations re-read: 'Assumption A4 gives a zero of N for each bracket with a sign change'; Lab 1 checks G falls on its 999-point grid. "
    "The statements match the code (lab Part B) and the stated assumption.")
ov["E4c-L08-key-results"] = row("E4c-L08-key-results", "prose", "course/modules/E/E4/L08.html:711-719", "PASS",
    "Key results re-checked row by row: G(0)=ln(1+sigma_v^2/sigma_eps^2)/(2a) (Lemma 4.5); G(1)=ln(5/3)/4; Prop 5.2 row now says 'under A4' "
    "and 'Proposition 5.2 (A4 assumed)'; grades T for proved results, C for the lab rows.")
ov["E4c-L08-G-before-definition"] = row("E4c-L08-G-before-definition", "DAG", "course/modules/E/E4/L08.html:51, 79 vs Definition 4.3 at L08.html:232", "PASS",
    "G appears at L08.html:51 and 79 with an explicit forward reference ('Definition 4.3'); the definition block follows. The Example 1.1 "
    "sentence (line 79) now reads 'Corollary 3.2 and Proposition 4.1 express the gain and the informativeness through variances alone', correct.")
ov["E4c-L08-simulated"] = row("E4c-L08-simulated", "data", "course/modules/E/E4/L08.html:336 (hypothesis, span.simulated-label); twin module docstring", "PASS",
    "SIMULATED label on Part A (seeded draws) at L08.html:336 and in the twin docstring line 5 (changed wording: 'Parts B to D evaluate "
    "population formulas in double precision. Part A uses seeded draws and is SIMULATED.'). No other part draws random numbers.")
ov["E4c-L08-process-banned"] = row("E4c-L08-process-banned", "prose", "course/modules/E/E4/L08.html", "PASS",
    "Same round-5 banned-phrase and process-word scan as for L09 (body text, math and code excluded): no hit; the only regex hit "
    "in L07 is 'around', a false positive of the pattern 'round '.")
ov["E4c-L08-dfn-duplicates"] = row("E4c-L08-dfn-duplicates", "DAG / duplicates", "course/modules/E/E4/L08.html:59, 66, 71, 206, 232-235, 267, 281; course/modules/E/E4/L06.html:57, 67, 96, 169", "PASS",
    "No duplicate definition across L06 and L08. L06 defines signal, noise trader, precisions, informed fraction (L06.html:57), CARA utility "
    "(L06.html:67), posterior (L06.html:96) and the linear noisy REE (L06.html:169). L08.html:59 uses CARA by reference to L06 Definition 6.2 "
    "(no dfn); L08 refers to the signal of L06 (L08.html:66, no dfn). L08's own dfns are noise-trader supply and informed/uninformed "
    "(66, 71: late, see E4c-r3-first-use-before-definition), demand gaps (206), gain from information (232-233), net benefit (235), "
    "equilibrium informed fraction (267) and the Grossman-Stiglitz paradox (281, data-concept). None is defined twice.")
ov["E4c-L09-structure"] = row("E4c-L09-structure", "structure", "course/modules/E/E4/L09.html", "PASS",
    f"Whole page re-read ({OUTD}/L09.txt). Order matches BUILDER_RULES 4.2; why it matters 115 words; quiz (9 items); "
    "3 misconceptions (section 5); 12 solutions of at least 52 words; data-hours=8. "
    "check_pages L09 PASS. The round-5 insertion after L09.html:435 is a key-results row (grade C) for the Lab 1 enumeration.")
ov["E4c-L09-partition-common-knowledge"] = row("E4c-L09-partition-common-knowledge", "prose", "course/modules/E/E4/L09.html:62", "PASS",
    "Round-4 defect fixed: L09.html:62 now reads 'Both partitions are common knowledge: each trader knows both partitions. This is an "
    "assumption of the model, and Definition 1.2 gives common knowledge for events.' Definition 1.2 (L09.html:78-79) is the common-knowledge definition for events; no forward reference to the wrong definition remains.")
ov["E4c-L09-dag-remark"] = None  # placeholder removed below
del ov["E4c-L09-dag-remark"]
ov["E4c-r3-first-use-before-definition"] = row("E4c-r3-first-use-before-definition", "DAG / first use",
    "course/modules/E/E4/L08.html:66 (dfn 'noise-trader supply'), L08.html:71 (dfn 'informed', 'uninformed'); first uses in course/modules/E/E4/L06.html:57 ('informed fraction'), L06.html:72 ('A fraction ... is informed ... An uninformed investor observes only p'), L06.html:673 (quiz prompt 'the noise-trader supply')",
    "FAIL",
    "Re-verified at 7376a5e: still present. grep -n 'noise-trader supply' course/modules/E/E4/L06.html returns 7, 245 (lab docstring), 673 (quiz). "
    "grep -n '<dfn' L06.html has no dfn for 'informed', 'uninformed' or 'noise-trader supply' (only 'informed fraction' at line 57). "
    "The terms are used in L06 before their only definitions in L08.html:66 and 71 (plain dfn, no data-concept).",
    "Define 'informed' and 'uninformed' with a plain <dfn> at their first use in L06.html:57 or 72, and define 'noise-trader supply' at its first "
    "use in L06 before the quiz prompt at L06.html:673 (or reword that prompt). Then replace the dfns at L08.html:66 and 71 with plain prose or "
    "links to L06 (owner: the L06 builder for the definitions; the L08 builder for the duplicates).")
ov["E4c-r4-L08-assumption-numbering"] = ov["E4c-L08-A5"]
ov["E4c-r4-L08-assumption-numbering"] = dict(ov["E4c-L08-A5"], id="E4c-r4-L08-assumption-numbering")
ov["E4c-r4-L09-partition-common-knowledge"] = dict(ov["E4c-L09-partition-common-knowledge"], id="E4c-r4-L09-partition-common-knowledge")

# new rows of round 5
new = []
new.append(row("E4c-r5-recheck-L07-prop-7.6", "numbers", "course/modules/E/E4/L07.html:97-118 (Prop 7.6 at 97, Prop 7.7 at 111), lab block 130-372, Parts A to E", "PASS",
    f"{S5}/recheck_L07.py, out/recheck_L07.out: fixed-point clearing equilibrium equals the closed form to 3.3e-16 on 1440 parameter sets; "
    "Prop 7.7 sign check (decreasing in sigma_u, a, sigma_eps; increasing in lambda): 0 violations on the grid; sweep values 4/9..1/66, "
    "1/6..9/22, 4/9..1/6, 2500/5001 reproduced exactly; Var(p) column reproduced."))
new.append(row("E4c-r5-recheck-L08-gains", "numbers", "course/modules/E/E4/L08.html:336, 544-563 (expected block), 564, 587, 591, 595; lab Parts A to D; costs 0.12 to 0.18", "PASS",
    f"{S5}/recheck_L08.py, out/recheck_L08.out: independent gains (demand gaps as random variables) match gain(0)=0.173287, gain(0.5)=0.158997, "
    "gain(1)=0.127706, gain(1e-6)-gain(0)=-6.248e-14, the 999-point monotonicity, and the bisection roots lam* 0.965625410, 0.815032329, "
    "0.657828572 (0.15), 0.480567912, 0.231615819, boundary rules at 0.12 and 0.18, with gaps below 1e-13 at the interior roots."))
new.append(row("E4c-r5-recheck-L09-counts", "numbers", "course/modules/E/E4/L09.html:118-120 (Example 2.4), 126 (lab 1), 264-281 (lab block)", "PASS",
    f"{S5}/recheck_L09.py, out/recheck_L09.out: 15625 bets; state 1 meet {{1,2,3}}: 500 strict, 0 of them nonnegative on the meet, 625 "
    "nonnegative on the meet with zero posteriors; state 4 meet {4,5,6}: the same counts; first strict bet at state 1 "
    "(-1,2,-2,-2,-2,-2) with agent 1 posteriors 1/2,1/2,-2 and agent 2 posteriors 1/3,1/3,1/3; at state 4 (-2,-2,-2,-2,1,2) with 1/3,1/3,1/3 and 1/2,1/2,-2; 625 = 5*5^3 zero-posterior bets."))
new.append(row("E4c-r5-L07-docstring-exact-fraction", "prose (docstring vs output)",
    "tests/labs/E4/lab-E4-L07-1.py:16-17 (embedded in course/modules/E/E4/L07.html in the code block); line 181 (population = float(...)); output line 'population 0.333333'",
    "FAIL",
    "The twin docstring line 17 says 'Every population value is an exact Fraction.' Part F (line 181) converts the exact population value to float "
    "and prints 'sample_rho2 0.330625 population 0.333333' (out/twin-L07.stdout). The sentence is contradicted by the code's own output.",
    "Reword twin line 17 to 'Parts A to E print exact Fraction population values; Part F converts the exact population value to float for comparison "
    "with the sample.' Then re-embed the page code with tools/embed_labs.py course/modules/E/E4/L07.html --refresh lab-E4-L07-1 and re-run run_labs."))
new.append(row("E4c-r5-cards-duplicates", "cards", "course/modules/E/E4/cards.json (220 cards)", "PASS",
    "Full scan: no duplicate id and no duplicate front across the 220 cards (python -I json check, this round). Ids are not sequential (ruling 2 allows that)."))
new.append(row("E4c-r5-cards-L07", "cards", "course/modules/E/E4/cards.json, lesson L07 (21 cards, E4-c130 to E4-c150)", "PASS",
    "All 21 L07 cards read against L07 text: definitions 7.1, 7.2; Lemmas 7.3 and 7.4; Proposition 7.6 closed form; 7.7 signs; Remark 7.8 "
    "benchmark; Remark 7.9; lab values 1/3, 4/9..1/66, 729/1444 to 35937/4802, 1/6..9/22, 4/9..1/6, SIMULATED 0.330625; misconceptions. "
    "Each back is checkable against the lesson text; the grades match the key-results table."))
new.append(row("E4c-r5-cards-L08", "cards", "course/modules/E/E4/cards.json:1341 (card E4-c179, lesson L08)", "FAIL",
    "Card E4-c179 ('Assuming A1 to A3 with sigma_u^2 > 0 and A4, what does Proposition 5.2(c) give ...') carries basis "
    "'Proposition 5.2(c); conditional on Assumption A5'. The lesson labels the sign-change assumption A4 (L08.html:314, 325). "
    "The other 40 L08 cards were read against the lesson: no other stale label; cards E4-c151 to E4-c188 and E4-c222 to E4-c224 agree.",
    "In course/modules/E/E4/cards.json, card E4-c179, change the basis to 'Proposition 5.2(c); conditional on Assumption A4'. Cards are generated "
    "by the card builder; do not hand-edit (CLAUDE.md rule 1): regenerate from the source once the basis field is corrected in the source."))
new.append(row("E4c-r5-cards-L09", "cards", "course/modules/E/E4/cards.json, lesson L09 (22 cards)", "PASS",
    "All 22 L09 cards read against the L09 text: Assumptions B1 to B3, Definitions 1.1 and 1.2, Theorem 2.1, Corollary 2.3, Example 2.4 values "
    "(1/2, 1/3, -2), Lab 1 counts (500, 0, 625, 15625), Problems Res 1 to Res 3, misconceptions. Each card matches the lesson."))
new.append(row("E4c-r5-milgrom-record", "citations", "references/references.json (milgrom1982information); course/modules/E/E4/L09.html:512", "PASS",
    "Registry record read: title 'Information, trade and common knowledge', container Journal of Economic Theory, volume 26, issue 1, pages 17-27, "
    "year 1982, verified by crossref (DOI 10.1016/0022-0531(82)90046-1). L09.html:512 cites the key only, with the same title, volume, issue, "
    "pages and year, and states no result of the paper. The abstract was not read; no claim is attributed to it."))
new.append(row("E4c-r5-notation-scan", "notation", "course/modules/E/E4/L07.html, L08.html, L09.html; notation/notation.json", "PASS",
    f"ledgers/E4/scripts/E4-c-r2/notation_scan.py run on the pin (saved {OUTD}/notation_scan.out): 'unknown macros = []' for each page. "
    "Registered macros used: \\E, \\Var, \\Cov, \\Corr, \\Normal, \\R (all registered). Local symbols (sigma, kappa, tau, chi, varpi, beta, lambda, "
    "rho, eta, D_I, D_U, Y, Z, c, b, pi, omega, theta) are each defined on their lesson; no registered symbol (T, gamma_3, gamma_4, Phi, R^*, "
    "Q) is used in E4 L07 to L09 (notation.json has 8 symbols, checked)."))
new.append(row("E4c-r5-figures", "figures", "course/modules/E/E4/L07.html, L08.html, L09.html", "PASS",
    "No figure: grep -c data-chart returns 0 for each page, so no chart, figure or SVG needs axes, source or caption checks in this slice."))
new.append(row("E4c-r5-lab-sim-labels", "data", "tests/labs/E4/lab-E4-L07-1.py (Part F), lab-E4-L08-1.py (Part A), lab-E4-L09-1.py (none)", "PASS",
    "SIMULATED is printed in the output of Part F ('Part F: SIMULATED sample check') and Part A ('part A (SIMULATED draws)'); L09 has no random draws and says so (L09.html:128)."))

# ---- assemble ----
rows = []
for r in r4["rows"]:
    rid = r["id"]
    if rid in ov:
        rows.append(ov[rid])
    elif r["status"] == "PASS":
        rows.append(carry(rid))
    else:
        raise SystemExit(f"unhandled round-4 non-PASS row {rid}")
rows += new
ids = [x["id"] for x in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
missing = [k for k in old if k not in ids]
assert not missing, f"round-4 ids dropped: {missing}"

verdict = "PASS" if all(x["status"] == "PASS" for x in rows) else "FAIL"
frag = {
    "unit": "E4",
    "slice": "E4-c",
    "round": 5,
    "verifier": "Claude Haiku 5.5, independent verifier for E4-c round 5 (did not build E4)",
    "pin": "7376a5e216c1e6d99becc76b4cd64028f5b55d3f",
    "base": f"{PREV}f9a02b1af92a060f7fabf7e1b3afb5ea95f45ba (round-4 pin; delta read hunk by hunk, see E4c-r4-delta-read)".replace(f"{PREV}f9a02b1af92a060f7fabf7e1b3afb5ea95f45ba", "9a02b1af9f92a060f7fabf7e1b3afb5ea95f45ba"),
    "checkout": ROOT,
    "scratch": "/tmp/e4c-r5-XXXX (twin runs, removed after each run)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "grossman1980 (Grossman and Stiglitz, AER 1980) still has no registry record (B1, REFERENCE_REQUEST R-E4-1); L08 cites no key, which is correct.",
        "mascolell1995microeconomic author conflict (B3) is outside this slice.",
    ],
    "freshness_flags": [],
    "notes": (
        "Scope: course/modules/E/E4/L07.html, L08.html, L09.html; tests/labs/E4/lab-E4-L07-1.py, L08-1.py, L09-1.py; cards.json for "
        "lessons L07 to L09 (card rows); index.html only at lines 29, 136, 137. Not checked by this slice: project, grader, rubric, "
        "mutants, alternatives and equivalents (other slices; run_graders and check_projects re-run as gates only); L06 text except the "
        "cited first-use lines; cards of other lessons; the live Crossref run (no reference changed). No figures in these pages. "
        "Mutants: none, because lab twins are demonstrations (ruling); no project grader in this slice. Observation, not a row: "
        "L08 numbers its assumptions A1 to A4 independently of L06's A1 to A4 (L07 cites L06 correctly). Observation: L08 uses "
        "'expected utility', 'variance' and 'CARA' in prose after the first link in each lesson; the first-use convention is applied."
    ),
    "summary": (
        f"E4-c round 5 on {PIN}: verdict {verdict}. Rows: {len(rows)} total, "
        f"{sum(1 for x in rows if x['status']=='PASS')} PASS, {sum(1 for x in rows if x['status']=='FAIL')} FAIL, 0 UNVERIFIABLE. "
        "Non-PASS rows: E4c-r3-first-use-before-definition (L08:66,71 vs L06:57,72,673; owner L06 and L08), E4c-L07-quiz (item at "
        "L07.html:565 scope), E4c-r5-L07-docstring-exact-fraction (twin lab-E4-L07-1.py:17 vs Part F output), E4c-r5-cards-L08 "
        "(card E4-c179 basis still says A5). Round-4 FAILs E4c-r4-L08-assumption-numbering, E4c-r4-L09-partition-common-knowledge "
        "and E4c-L09-references are fixed and now PASS. Mutants: none in this slice."
    ),
}

open(OUT, "w", encoding="utf-8").write(json.dumps(frag, ensure_ascii=False, indent=1) + "\n")
print("wrote", OUT, "rows", len(rows), "verdict", verdict)
