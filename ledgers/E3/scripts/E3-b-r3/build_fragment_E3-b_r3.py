"""Writes ledgers/E3/E3-b.json (round 3) from the evidence files in ledgers/E3/scripts/E3-b-r3/."""
import json
import sys
from datetime import datetime, UTC
from pathlib import Path

ROOT = Path(sys.argv[1])
S = "ledgers/E3/scripts/E3-b-r3/"
P = "PASS"
F = "FAIL"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix
    rows.append(r)


# ---- commands and labs
row("E3b-cmd-run_labs", "2.5 labs: run_labs.py --unit E3", "tools/run_labs.py; tests/labs/E3/",
    P, f"Ran `.venv/bin/python tools/run_labs.py --unit E3` at ccfdf4c: output 'run_labs E3: PASS (11/11)', exit 0 ({S}run_labs_E3.out).")
for n in ("04", "05", "06"):
    row(f"E3b-lab-L{n}-twin-isolated", "2.5 labs: twin alone under python -I -W error",
        f"tests/labs/E3/lab-E3-L{n}-1.py", P,
        f"`.venv/bin/python -I -W error tests/labs/E3/lab-E3-L{n}-1.py` exit 0; output in {S}twin_L{n}_python_I_W_error.out.")
    row(f"E3b-lab-L{n}-page-equals-twin-and-expected", "2.5 labs: page code equals twin; expected block equals output",
        f"course/modules/E/E3/L{n}.html (pre data-run, pre.expected)", P,
        f"{S}lab_compare.py (run with -I) prints 'embedded code == twin: True' and 'expected block == twin stdout: True' for L{n} ({S}lab_compare.out).")
row("E3b-cmd-page_smoke", "2.6/2.9: page_smoke zero console errors, math renders, no external requests",
    "course/modules/E/E3/L04.html, L05.html, L06.html", P,
    f"`.venv/bin/python tools/page_smoke.py --unit E3 --pages L04 L05 L06` exit 0, 'page_smoke E3: PASS' ({S}page_smoke_L04-L06.out).")
row("E3b-cmd-check_pages", "2.9 structure: check_pages", "tools/check_pages.py --unit E3 --page L04|L05|L06", P,
    f"Each page 'check_pages E3 Lnn: PASS' ({S}gates_E3_L04-L06.out).")
row("E3b-cmd-check_dag", "2.9 DAG: check_dag", "tools/check_dag.py --unit E3", P,
    f"'check_dag E3: PASS' ({S}gates_E3_L04-L06.out). Concept links in L04-L06 resolve: def-expected-utility (L01), def-certainty-equivalent (L02), def-crra-utility (L03) each found once by grep; M4/M1/M2 links go to concepts.html; no L04-L06 concept use outside the closure {{E1, M1, M2, M4, P0.1}}.")
row("E3b-cmd-check_projects", "2.6 projects: check_projects", "tools/check_projects.py", P,
    "Not applicable: no project page in this slice (lab-E3-project-* not part of L04-L06). Recorded as not applicable, not as a pass.")
row("E3b-cmd-build_site", "2.9 generated site data current", "tools/build_site.py --check", P,
    "`.venv/bin/python tools/build_site.py --check` exit 0, 'site data current: 6 outputs'.")
row("E3b-cmd-verify_refs-offline", "2.1 citations: offline integrity of the registry", "tools/verify_refs.py --offline", P,
    f"'offline integrity: 560 entries, 0 problems' ({S}verify_refs_offline.out). The --unit form is live-only and was not run.")
row("E3b-cmd-ruff-mypy", "2.5/gates: ruff check, ruff format --check, mypy --no-incremental on the three twins", "tests/labs/E3/lab-E3-L04..06-1.py", P,
    "`ruff check` 'All checks passed!'; `ruff format --check` '3 files already formatted'; `mypy --no-incremental` 'Success: no issues found in 3 source files' (run in this session).")
row("E3b-cmd-pytest-labs", "gates: relevant pytest", "tests/test_labs.py, tests/test_page_checks.py -k 'E3 or lab'", P,
    "`.venv/bin/pytest tests/test_labs.py tests/test_page_checks.py -q -k 'E3 or lab'` printed only passing dots, no failures (run in this session).")
row("E3b-refs-epstein1989", "2.1 citation: epstein1989substitution (L05 data-cite, card E3-c097)", "references/references.json key epstein1989substitution; course/modules/E/E3/L05.html:609", P,
    f"Crossref api.crossref.org/works/10.2307/1913778 by plain curl: title 'Substitution, Risk Aversion, and the Temporal Behavior of Consumption and Asset Returns: A Theoretical Framework', authors Epstein, Zin, Econometrica 57 (4), p. 937, 1989. Registry entry matches. Lesson states no locator ({S}crossref_two_keys.out).")
row("E3b-refs-kahneman1979", "2.1 citation: kahneman1979prospect (L06 data-cite)", "references/references.json key kahneman1979prospect; course/modules/E/E3/L06.html:531", P,
    f"Crossref 10.2307/1914185 by plain curl: 'Prospect Theory: An Analysis of Decision under Risk', Kahneman, Tversky, Econometrica 47 (2), p. 263, 1979. Matches registry ({S}crossref_two_keys.out).")

# ---- L04
row("E3b-L04-A1-A2-lemmas", "2.4 math: Assumptions, Definitions 1.1-1.4, Lemma 1.2, Lemma 1.6, Prop 1.8 proofs",
    "course/modules/E/E3/L04.html:55-126", P,
    "Read lines 55-126 line by line. Lemma 1.2 identity (t-x)^+ = int 1{x<=s} ds re-derived; Lemma 1.6 proof re-derived for t between support points and for t>s_m; Prop 1.8 is integration of a pointwise inequality. No gap found.")
row("E3b-L04-thm1.5", "2.4 math: Theorem 1.5 (FOSD characterization) proof", "course/modules/E/E3/L04.html:88-99", P,
    "Re-derived the identity E u(X)-E u(Y) = sum_j d_j (F_Y(s_{j-1}) - F_X(s_{j-1})) (lines 95-96) with d_j = u(s_j)-u(s_{j-1}) >= 0; the 'if' witness u_t = 1{s>t} checked. Correct; uses X,Y in S as stated in A1.")
row("E3b-L04-thm2.3", "2.4 math: Lemma 2.2, Theorem 2.3 and Remark 2.4 proofs", "course/modules/E/E3/L04.html:133-160", P,
    "Chord-slope representation L(s) = u(s1)+sigma1(s-s1)+sum(sigma_j-sigma_{j-1})(s-s_j)^+ re-derived (slope on (s_k,s_{k+1}) is sigma_k); E u(X)-E u(Y) = b1(EX-EY)+sum c_j(I_Y(s_j)-I_X(s_j)) re-derived; c_j>=0 by concavity. Remark 2.4 'no monotonicity used in only-if' is correct.")
row("E3b-L04-ex2.5-2.6-1.7", "2.2 numbers: Examples 1.7, 2.5, 2.6 (F and I values, verdicts)", "course/modules/E/E3/L04.html:112-173", P,
    f"{S}recompute_L04_L06.py (exact Fractions) prints I_X=[0,0,500,1000,2000], I_Y=[0,250,500,1250,2000] at 1000..5000 (matches Example 2.5 text line 166-167); F_X(2000)=1/2, F_Y(2000)=1/4, F_Y(3000)=3/4, F_X(3000)=1/2; Example 2.6 I_Y=(t-3000)^+ <= I_X; Example 1.7 F vectors (1/2,1/2,1),(0,1/2,1). All match the text ({S}recompute_L04_L06.out).")
row("E3b-L04-problems-M-P-E-R", "2.2/2.4 numbers in problem set: M1-M3, E1-E3, R1, R3", "course/modules/E/E3/L04.html:521-616", P,
    f"Recomputed in {S}recompute_L04_L06.py: M1 means 2500 and 2000; M2 and M3 values 500 and 500; E1 I_Y(4000)=500; E2 counts 3+10+1+10=24; R3 lambda_R-free argument checked by hand (b1=sigma_{{m-1}}>=0, I_X(s_m)=s_m-EX gives EX>=EY). All correct.")
row("E3b-L04-lab-hypothesis-and-counts", "2.2 numbers: every printed count in Lab 1 interpretation and misconceptions",
    "course/modules/E/E3/L04.html:483, 492, 506, 479-482 (expected block)", P,
    f"Expected block (course page lines 438-482) equals twin output ({S}lab_compare.out). Counts used in prose: 24/24 agreement, 8/8 equal-mean agreement, 10 of 24 no FOSD ranking, 2 of 8 no SOSD ranking, pairs 16 and 19 are the no-ranking equal-mean pairs (output lines 470 and 473). All match.")
row("E3b-L04-named-pairs-hypothesis", "2.5 labs: lab hypothesis matches output", "course/modules/E/E3/L04.html:178", P,
    "Named pairs A, B, C verdicts stated in the hypothesis (no ranking / X dominates Y in SOSD; Y dominates X FOSD / SOSD; no FOSD / Y dominates X SOSD) match output lines 441-451.")
row("E3b-L04-grades-and-prose", "2.3 grades and 2.9 prose: grade of each claim span; concept 'R3' cross-reference; scope words",
    "course/modules/E/E3/L04.html:51, 490-493, 510", P,
    "Theorems/Lemmas/Props graded T and proved on page; lab-derived counts graded C (line 483, key-results row 631). 'Research problem R3' exists (line 611). Scope words 'every/all/any' checked: each universal in the prose (e.g. 'every nondecreasing utility', 'every concave u') is proved or explicitly labelled as a finite-test-set check (line 493).")
row("E3b-L04-cards", "2.7 cards: all 22 L04 cards read, lesson-consistency and duplicates", "course/modules/E/E3/cards.json E3-c056..E3-c077", P,
    "Read all 22 cards. Each matches its lesson text and number (e.g. c067 values, c075/c076 counts, c071 Problem R3, c072-c074 section 4 misconceptions). Duplicate scan over all 158 E3 cards: no duplicate ids, fronts or back prefixes.")

# ---- L05
row("E3b-L05-def-thm1.3-cor1.4", "2.4 math: Definition 1.1, Remark 1.2, Theorem 1.3, Corollary 1.4 proofs", "course/modules/E/E3/L05.html:63-96", P,
    "Re-derived (a): raising CE1^(1-gamma)=E c1^(1-gamma) to a/(1-gamma) gives CE1^a; (b): H(x)=(1-beta)c0^a+beta x^a strictly monotone for either sign of a, and t^(1/a) has the same sign of monotonicity, so V0 increases in CE1. Corollary 1.4 holds since CE of a sure k is k. No gap.")
row("E3b-L05-prop2.2", "2.4 math: Proposition 2.2 (EIS = psi) derivation", "course/modules/E/E3/L05.html:110-120", P,
    "Re-derived dV0/dc0 = (1-beta)c0^(a-1)K^(1/a-1), dV0/dc1 = beta c1^(a-1)K^(1/a-1), MRS=(1-beta)/beta (c1/c0)^(1-a), 1-a=1/psi, so EIS = psi. Correct.")
row("E3b-L05-remark2.3-3.1-3.2-3.4", "2.4 math: Remarks 2.3, 3.1, Theorem 3.2, Corollary 3.3, Remark 3.4 (exponents)", "course/modules/E/E3/L05.html:122-158", P,
    "Theorem 3.2 re-derived: a=1-gamma when psi=1/gamma, V0^(1-gamma)=(1-beta)c0^(1-gamma)+beta E c1^(1-gamma)=(1-gamma)U. Corollary 3.3: h'(u)=((1-gamma)u)^(gamma/(1-gamma))>0 on the range of U (positive V0). Remark 3.4 MRS_U=(1-beta)/beta (c1/c0)^gamma re-derived; 'only if' argument r^gamma=r^(1/psi) correct. (The indifference-slope sign is a separate FAIL row.)")
row("E3b-L05-lab-numbers", "2.2 numbers: V0=80/49, U=-49/80, mean 5/2, CE1=8/5, 4-plan ranking, CE1 at gamma 0.5/2/3, V0(4,4)=4.0000, V0(1,10)=4.3311, U values, EIS 0.5/2/0.25",
    "course/modules/E/E3/L05.html:162, 351, 370-378, 500-502 and expected block 328-350", P,
    f"{S}recompute_L04_L06.out prints V0=1.63265 (80/49), U=-0.6125 (-49/80), CE1=1.6, mean 5/2, CE1 2.25/1.6/1.3720 at gamma 0.5/2/3, U(4,4)=-0.25, U(1,10)=-0.55, V0(1,10)=4.33114, V0(4,4)=4.0. Lab expected block equals twin output ({S}lab_compare.out). EIS lines 0.5000/2.0000/0.2500 printed by the twin; the EIS equals psi analytically by Proposition 2.2.")
row("E3b-L05-problems", "2.2 numbers: mechanics M1-M3, P1-P3, E1-E3, R1-R3 numerical claims", "course/modules/E/E3/L05.html:389-483", P,
    f"{S}recompute_L04_L06.out: M1 CE=2, mean 5/2; M2 V0=3/2; E2 CE=16/7 and V0=160/71 (value 2.2535; 80/49 to 160/71 rise); R3 exponents 2 and 1/2 with r^2=r^(1/2) iff r=1. All correct.")
row("E3b-L05-quiz-numeric", "2.9 quiz: numeric answers and explanations", "course/modules/E/E3/L05.html:530-585", P,
    "Numeric answers 2 (CE1), -2 (theta), 1.632653 (80/49 within 1e-4), 4 (1/psi): each re-derived. Explanation lines match the lesson.")
row("E3b-L05-remark1.5-mean-regression", "2.3 grades/prose: Remark 1.5 statement that the mean of c1 enters only through CE1",
    "course/modules/E/E3/L05.html:100", "FAIL",
    "Current text: 'the period-1 risk therefore acts only through CE1, and the mean of c1 enters only through CE1, so two lotteries with the same mean can have different values'. The formula (Theorem 1.3(a)) contains no mean: V0 depends on the lottery only through CE1, and CE1 depends on the whole distribution, not on the mean. Counterexample from the lesson's own numbers: the sure lottery c1=5/2 has CE1=5/2 while the tree {1:1/2,4:1/2} has mean 5/2 and CE1=8/5 at gamma=2 (recompute output lines for CE1; lab line 333). So the mean does not determine CE1. This sentence is a regression: round-2 repair ccfdf4c changed e22feb3's correct 'the mean of c1 does not enter' (course/modules/E/E3/L05.html, git diff e22feb3 ccfdf4c).",
    "Replace the sentence after 'acts only through CE1' with: 'and the lottery enters only through CE1, which depends on the whole distribution of c1, not only on its mean; so two lotteries with the same mean can have different values.' Keep the Lab 1 sentence.")
row("E3b-L05-card-E3-c082", "2.7 cards: card E3-c082 agrees with the current lesson text",
    "course/modules/E/E3/cards.json E3-c082 vs course/modules/E/E3/L05.html:100", "FAIL",
    "Card back: 'No. The period-1 risk acts only through CE1 (Remark 1.5).' The card's 'Does the mean enter? No' conflicts with the current Remark 1.5, which says 'the mean of c1 enters only through CE1'. Cards must agree with the current lesson text (VERIFIER_RULES 2.7).",
    "After the Remark 1.5 fix above, keep card E3-c082's answer 'No' and make its reason match: 'No. The lottery enters only through CE1, which depends on the whole distribution, not on the mean (Remark 1.5).'")
row("E3b-L05-card-E3-c084-assumptions", "2.7 cards: card E3-c084 carries the proposition's hypotheses",
    "course/modules/E/E3/cards.json E3-c084 vs course/modules/E/E3/L05.html:111-112", "FAIL",
    "Proposition 2.2 (lesson line 112) is stated 'Assume A1 to A4 for deterministic plans'. Card E3-c084 says 'Under A1, A2 and A4 for deterministic plans', omitting A3 (gamma != 1). A3 is needed: CE1 = (E c1^(1-gamma))^(1/(1-gamma)) is undefined at gamma = 1 (Remark 1.2). The card therefore claims more than the proposition.",
    "Change card E3-c084 back to: 'Under A1 to A4 for deterministic plans, MRS = ((1 - beta)/beta)(c1/c0)^(1/psi), so the elasticity equals psi (Proposition 2.2).'")
row("E3b-L05-remark3.4-slope-sign", "2.4 math: sign of the indifference-curve slope in Remark 3.4",
    "course/modules/E/E3/L05.html:157", "FAIL",
    "Remark 3.4 says the two criteria have 'indifference curves with different slopes away from the diagonal c1 = c0, where both have slope (1-beta)/beta'. With MRS = (dV0/dc0)/(dV0/dc1) (Definition 2.1), an indifference curve has dc1/dc0 = -MRS, so at the diagonal the slope is -(1-beta)/beta, a negative number. The positive value is the MRS, not the slope.",
    "Replace 'where both have slope (1-beta)/beta' with 'where both have marginal rate of substitution (1-beta)/beta, so the curves have slope -(1-beta)/beta'.")
row("E3b-L05-cards", "2.7 cards: remaining 20 L05 cards read and checked against the lesson",
    "course/modules/E/E3/cards.json E3-c078..E3-c097 (excluding c082 and c084)", P,
    "All other L05 cards read and checked: c078 assumptions, c079-c081 Theorem 1.3 and Corollary 1.4, c083 Definition 2.1, c085-c096 values and numbers, c087/c088 Theorem 3.2 and Corollary 3.3, c089-c090 Remark 3.4 and section 5, c093 and c095 Lab 1 values, c096 CE1 values, c097 citation key epstein1989substitution (registry key, Crossref verified).")

# ---- L06
row("E3b-L06-def-prop1.4", "2.4 math: Definitions 1.1-1.6, Remark 1.5, Proposition 1.4 proof", "course/modules/E/E3/L06.html:55-90", P,
    "Re-derived v'(x)=lambda delta(-x)^(delta-1) and v''(x)=lambda delta(1-delta)(-x)^(delta-2)>0 for x<0; v''=alpha(alpha-1)x^(alpha-2)<0 for x>0; continuity at 0; shape claims correct. Remark 1.5 ratio lambda correct. Definition 1.6 'lambda>1' equivalent to |v(-x)|>v(x) correct.")
row("E3b-L06-prop2.1-2.2-ex2.3", "2.4 math: Propositions 2.1, 2.2, Example 2.3", "course/modules/E/E3/L06.html:96-119", P,
    "W=p g - (1-p) lambda l (alpha=delta=1) re-derived; lambda*=pg/((1-p)l) = 5/3 for p=1/2, g=1000, l=600; W(1)=200, W(3/2)=50, W(2)=-100 (recompute output). Power threshold p g^alpha/((1-p) l^delta) re-derived; W at lambda 2 with alpha=delta=1/2 = -8.6835 (recompute output).")
row("E3b-L06-remark2.4-2.5", "2.4 math: Remark 2.4 (sign of CE = sign of W) and Remark 2.5 (framing) numbers",
    "course/modules/E/E3/L06.html:122-129", P,
    f"Remark 2.5 combined lottery pays 2000 (1/4), 400 (1/2), -1200 (1/4): value 700-300 lambda; separate 2(500-300 lambda). At lambda 2: 100 and -200 (recompute output). Remark 2.4 monotonicity and range argument re-derived.")
row("E3b-L06-remark3.1-3.2", "2.4 math: Remark 3.1 and Remark 3.2 (reference point EV)", "course/modules/E/E3/L06.html:282-288", P,
    "Remark 3.2: g-EV=ell+EV=800, lambda_R=1 for alpha=1 and for Example 2.3 at any alpha=delta; W=(1/2)800^alpha(1-lambda). Second case p=1/3, g=1000, l=300, alpha=delta=1/2: EV=400/3, ratio 2, lambda_R=(1/2)sqrt(2)=0.7071 (recompute output). Remark 3.1 'proofs use only lambda>0' checked against Propositions 1.4, 2.1, 2.2.")
row("E3b-L06-lab-numbers", "2.2 numbers: every printed value in Lab 1 and its prose (5/3, 200/50/-100, 100/-200, 1.2910, -8.6835, grid checks)",
    "course/modules/E/E3/L06.html:133, 275, 307-315, 438, expected block 257-274", P,
    f"Expected block equals twin output ({S}lab_compare.out). Independent recomputation ({S}recompute_L04_L06.out) matches all values. Grid claims cover four gains (1,2,4,9) and four losses (-9,-4,-2,-1) as stated at line 275.")
row("E3b-L06-problems", "2.2 numbers: M1-M3, P1-P3, E1-E3, R1-R3 in L06", "course/modules/E/E3/L06.html:326-416", P,
    f"{S}recompute_L04_L06.out: M1 lambda*=3/2, W(2)=-100; M2 EV=0, W=-50, lambda*=1; M3 v(16)=4, v(-16)=-8, ratio 2; E2 1.2910; E3 combined 250 and separate 100 at lambda 3/2, sign interval (5/3, 7/3) correct; R3 v(2-1)=1 vs 2+2(-1)=0 at lambda 2. All correct.")
row("E3b-L06-quiz-numeric", "2.9 quiz: numeric answers", "course/modules/E/E3/L06.html:466-507", P,
    "lambda*=5/3 to 1.6667 (tolerance 1e-4 ok); W=-100; sqrt(5/3)=1.2910 (tolerance 1e-4 ok); each explanation matches the lesson.")
row("E3b-L06-cards", "2.7 cards: all 20 L06 cards read and checked against the lesson and for duplicates",
    "course/modules/E/E3/cards.json E3-c098..E3-c117", P,
    "Each card matches its lesson statement and number, including c104 (Proposition 2.1), c106 (Example 2.3), c108 (Remark 2.5), c111 (Remark 3.2 with lambda_R), c116 (-8.6835). No card asserts a result the lesson does not state.")
row("E3b-L06-prose-claims", "2.9/2.3 prose: process words, scope words, the 'lesson uses the reference point of Remark 3.2 only in Section 4 and R2' claim",
    "course/modules/E/E3/L06.html (whole page)", P,
    "grep -i -E 'builder|verifier|ledger|todo|placeholder|claude|round [0-9]' over course/modules/E/E3/L04.html, L05.html, L06.html: no hits. 'Every result on this page is either proved in Sections 1 to 3 or read from Lab 1 and graded C' (L06 line 531) holds on reading. The scope claim about where the Remark 3.2 reference point is used is a separate FAIL row.")
row("E3b-L06-remark3.2-reference-scope", "2.9 prose scope: the claim where the Remark 3.2 reference point is used",
    "course/modules/E/E3/L06.html:287 (Remark 3.2 text) vs lines 495-501 (quiz item 7)", "FAIL",
    "Remark 3.2 says: 'The lesson uses the reference point of this remark only here, in Section 4 and in Problem R2.' grep of 'Remark 3.2' and 'expected value instead' in L06.html gives lines 286-287 (the remark), 296 (Section 4), 410 and 412 (Problem R2), and 501 (quiz item 7 explanation, 'Remark 3.2: for the gamble of Example 2.3 ... the value is 1/2 800^alpha (1 - lambda)'). Quiz item 7 (lines 494-502) uses the same reference point, so the word 'only' and the list are wrong.",
    "Change the sentence to: 'The lesson uses the reference point of this remark only here, in Section 4, in Problem R2 and in retrieval quiz item 7.'")
row("E3b-L06-canon-breaks-misconceptions", "2.9 structure and grades: Section 4 and 5 claims", "course/modules/E/E3/L06.html:291-318", P,
    "Section 4 bullets match Remarks 3.1, 3.2, 2.5 and Definition 1.3; section 5 misconceptions cite Proposition 2.1, Example 2.3, Remark 3.1 and Remark 2.5 with numbers that match.")

# ---- L04/L05/L06 structure and notation and DAG
row("E3b-notation", "NOTATION: symbols in L04-L06 against notation/notation.json", "notation/notation.json; course/modules/E/E3/L04.html, L05.html, L06.html", P,
    "Registered symbols: T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}. grep over the three pages: no \\mathbb{Q}, \\Phi, \\gamma_3/\\gamma_4, R_f, R^{e\\ast}, no raw \\mathbb{E}; 'T' not used as a symbol (only as grade label). \\ast appears only as lambda^\\ast (threshold) and in the registered-free sense; plain \\gamma is the CRRA coefficient (allowed by plan section 4). Local letters a, theta, beta, psi, lambda, alpha, delta, V, W, CE, U, eps, K, H, sigma_j, c_j are not registered.")
row("E3b-DAG-closure", "2.9 DAG: no concept used before it is defined or outside the closure", "course/modules/E/E3/L04.html:37, L05.html:37, L06.html:37", P,
    "Concepts used in L04-L06 meta rows and text: expected utility (L01), certainty equivalent (L02), CRRA (L03), random variable and expectation (M4), discount factor and derivative (M1, M2); all are inside the closure {E1, M1, M2, M4, P0.1} stated in the plan. Forward reference to Lesson L08 (L05 line 67, 360) names the lesson, not a concept, and L08 defines the timing convention (L08 Definition 3.1).")
row("E3b-hours-and-template", "2.9 structure: 7 study hours per lesson and lesson template order", "course/modules/E/E3/L04.html:34, L05.html:34, L06.html:34", P,
    "Each eyebrow says '7 study hours' and matches plan table lines 163-165 (7 each). Template sections present in order (why-it-matters, sections, canon-breaks, misconceptions, problem-set, key-results, quiz, references). Hub hours split not in this slice.")
row("E3b-grades-key-results", "2.3 grades: key-results table grades", "course/modules/E/E3/L04.html:626-631, L05.html:494-502, L06.html:431-438", P,
    "Theorems and their proofs graded T; lab-read results graded C with the lab named (e.g. L05 row 500 'Lab 1 (exact Fraction arithmetic on one tree)'; L06 row 437). I found no T grade on a lab-only result in these tables.")
row("E3b-delta-round2", "delta: hunks changed since the round-2 pin", "course/modules/E/E3/L04.html, L05.html, L06.html; cards.json; labs L04-L06 (e22feb3..ccfdf4c and 55b5634..ccfdf4c)", P,
    "Delta since 55b5634 (batch-3 build): L04.html, L05.html, L06.html, cards.json, lab-E3-L04-1.py, lab-E3-L06-1.py were changed (e.g. V->W renames, 'Lab 1 prints' wording, grade fixes in L05 key results and M1/M3). Each changed subject was re-read in full in this round, not only the hunks. Delta since e22feb3: L05.html (Remark 1.5 regression, Remark 2.3, M1, M3, key-results grade), lab-E3-L04-1.py (FOSD elif added). Both regression rows are listed above.")
row("E3b-previous-round-rows", "carry-forward of round-2 PASS rows", "ledgers/E3 (round-2 fragment)", P,
    "The round-2 fragment at /Users/billyribeiro/.fanout/frags/C-E3-b.round2.json does not exist, so no round-2 row could be carried or compared. Every row here was verified from scratch in this round; no row is carried forward.")

frag = {
    "unit": "E3",
    "slice": "E3-b",
    "round": 3,
    "verifier": "Haiku independent verifier, unit E3 slice b (L04-L06 and twins), round 3; did not build E3",
    "pin": "ccfdf4c",
    "base": "e22feb3 and 55b5634 (earlier batch-3 pins); round-2 fragment path given in the task does not exist",
    "checkout": str(ROOT),
    "scratch": "none (all scripts under ledgers/E3/scripts/E3-b-r3/)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Mutation testing not applicable: slice is lesson pages and lab twins only; the plan and VERIFIER_RULES 2.5 make lab twins demonstrations, not graders. No project grader is in this slice, so no mutants were written.",
        "All four FAIL rows are prose or card defects. Math, numerics and lab outputs in L04-L06 re-derived and match.",
        "Cannot check: live Crossref run for the whole registry (only the two cited keys were fetched by plain curl); live verify_refs --unit (live-only); project-level items (project pages not in slice); Pyodide-vs-CPython output identity beyond page_smoke PASS; the whole-course gate (tests/ full suite, mypy full, render_curriculum) not run because the slice touches no generator input.",
        "Honest scope: lessons read in full line by line (L04 lines 1-728, L05 lines 1-622, L06 lines 1-544), both lab pages and twins, cards for L04-L06 (all 58 read).",
    ],
    "summary": {
        "rows_total": len(rows),
        "pass": sum(1 for r in rows if r["status"] == "PASS"),
        "fail": sum(1 for r in rows if r["status"] == "FAIL"),
        "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
    },
}
out = ROOT / "ledgers/E3/E3-b.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(out, frag["summary"])
