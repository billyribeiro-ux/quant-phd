"""Writes ledgers/E3/E3-b.json for round 4 (E3 slice b: L04-L06 and twins). Rows are the verifier's own."""
import json
import sys

ROOT = sys.argv[1]
S = "ledgers/E3/scripts/E3-b-r4/"
CARRY = ("Carried from round 3 (course/modules/E/E3/L04.html, tests/labs/E3/lab-E3-L04-1.py and cards E3-c056..c077 "
         "byte-identical since the previous pin ccfdf4c; see " + S + "delta_and_cards.out): ")
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- gates and commands, all re-run in this round ----
row("E3b-cmd-run_labs", "2.5 labs", "tools/run_labs.py --unit E3; tests/labs/E3/",
    "PASS", "`.venv/bin/python tools/run_labs.py --unit E3` -> 'run_labs E3: PASS (11/11)', exit 0 (" + S + "run_labs_E3.out).")
for L in ("L04", "L05", "L06"):
    row(f"E3b-cmd-check_pages-{L}", "2.9 structure", f"course/modules/E/E3/{L}.html", "PASS",
        f"`tools/check_pages.py --unit E3 --page {L}` -> 'check_pages E3 {L}: PASS', exit 0 ({S}check_pages_{L}.out).")
row("E3b-cmd-check_dag", "2.9 DAG", "tools/check_dag.py --unit E3", "PASS",
    "'check_dag E3: PASS', exit 0 (" + S + "check_dag.out). Anchors re-grepped: def-expected-utility (L01), def-certainty-equivalent (L02), def-crra-utility (L03) each defined once; L05/L06 own anchors present.")
row("E3b-cmd-check_projects", "2.6 projects", "tools/check_projects.py --unit E3", "PASS",
    "'check_projects E3: PASS', exit 0 (" + S + "check_projects_E3.out). No project page is in slice b; the gate is recorded as run, not as slice evidence.")
row("E3b-cmd-build_site", "gate", "tools/build_site.py --check", "PASS",
    "'site data current: 6 outputs', exit 0 (" + S + "build_site.out).")
row("E3b-cmd-verify_refs-offline", "2.1 citations", "tools/verify_refs.py --offline", "PASS",
    "'offline integrity: 560 entries, 0 problems', exit 0 (" + S + "verify_refs_offline.out). The --unit live run was not repeated.")
row("E3b-cmd-page_smoke", "2.9 page_smoke", "tools/page_smoke.py --unit E3 --pages L04 L05 L06", "PASS",
    "'page_smoke E3: PASS', exit 0; lab run times reported, L06 lab 0.0 s (" + S + "page_smoke_L04-L06.out).")
row("E3b-cmd-ruff-mypy-pytest", "gate", "ruff, mypy --no-incremental, pytest tests/test_labs.py tests/test_page_checks.py -k 'E3 or lab'", "PASS",
    "ruff check 'All checks passed!'; ruff format --check '335 files already formatted'; mypy 'Success: no issues found in 229 source files'; pytest dots only, exit 0 (" + S + "ruff_check.out, ruff_format.out, mypy.out, pytest_labs.out).")

# ---- labs: twins in isolation and page = twin ----
for L in ("04", "05", "06"):
    row(f"E3b-lab-L{L}-twin-isolated", "2.5 labs", f"tests/labs/E3/lab-E3-L{L}-1.py", "PASS",
        f"`.venv/bin/python -I -W error tests/labs/E3/lab-E3-L{L}-1.py` exit 0 (" + S + f"twin_L{L}.out).")
    row(f"E3b-lab-L{L}-page-equals-twin-and-expected", "2.5 labs", f"course/modules/E/E3/L{L}.html (pre data-run; pre.expected)", "PASS",
        f"ledgers/E3/scripts/E3-b-r4/lab_compare.py (run with -I): 'embedded code == twin: True' and 'expected block == twin stdout: True' for L{L} (" + S + "lab_compare.out).")

# ---- references ----
row("E3b-refs-epstein1989", "2.1 citations", "references/references.json epstein1989substitution; course/modules/E/E3/L05.html:609", "PASS",
    "Plain curl to api.crossref.org/works/10.2307/1913778: title 'Substitution, Risk Aversion, and the Temporal Behavior of Consumption and Asset Returns: A Theoretical Framework', Epstein, Zin, Econometrica 57(4), p. 937, 1989; registry record matches (" + S + "crossref_two_keys.out). Lesson claim is grade D naming only, no locator.")
row("E3b-refs-kahneman1979", "2.1 citations", "references/references.json kahneman1979prospect; course/modules/E/E3/L06.html:531", "PASS",
    "Plain curl to api.crossref.org/works/10.2307/1914185: 'Prospect Theory: An Analysis of Decision under Risk', Kahneman, Tversky, Econometrica 47(2), p. 263, 1979; matches registry (" + S + "crossref_two_keys.out). Grade D naming only.")

# ---- notation and DAG ----
row("E3b-notation", "2.9 / notation", "notation/notation.json; course/modules/E/E3/L04.html, L05.html, L06.html", "PASS",
    "Registered symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} and \\Prob (macro) searched in the three pages: none used with another meaning; \\ast appears only as lambda^\\ast in L06; \\E and \\R macros used. notation.json byte-identical to ccfdf4c.")
row("E3b-DAG-closure", "2.9 DAG", "course/modules/E/E3/L04.html:37, L05.html:37, L06.html:37", "PASS",
    "Concepts used by name or link in L04-L06 are inside the closure {E1, M1, M2, M4, P0.1}: expected utility (L01), certainty equivalent (L02), CRRA (L03), discount factor and derivative (M1, M2), random variable and expectation (M4). Lesson-level forward reference 'Lesson L08' in L05 is plain text, not a concept link.")
row("E3b-hours-and-template", "2.9 structure", "course/modules/E/E3/L04.html:34, L05.html:34, L06.html:34", "PASS",
    CARRY + "L04 eyebrow '7 study hours' unchanged. L05 and L06 eyebrows '7 study hours' re-read this round, matching plan table lines 163-165. Template section order checked on L05 and L06 by reading each page in full. Hub hours split is not in this slice.")

# ---- L04 (carried; subject byte-identical) ----
row("E3b-L04-A1-A2-lemmas", "2.4 mathematics", "course/modules/E/E3/L04.html:55-126", "PASS",
    CARRY + "Lemma 1.2 identity, Lemma 1.6 and Proposition 1.8 re-derived in round 3 (ledgers/E3/scripts/E3-b-r3/recompute_L04_L06.py, output recompute_L04_L06.out).")
row("E3b-L04-thm1.5", "2.4 mathematics", "course/modules/E/E3/L04.html:88-99", "PASS",
    CARRY + "Identity E u(X)-E u(Y) = sum_j d_j (F_Y(s_{j-1}) - F_X(s_{j-1})) re-derived; 'if' witness checked.")
row("E3b-L04-thm2.3", "2.4 mathematics", "course/modules/E/E3/L04.html:133-160", "PASS",
    CARRY + "Chord-slope representation and c_j >= 0 re-derived; Remark 2.4 correct.")
row("E3b-L04-ex2.5-2.6-1.7", "2.4 / 2.2 numbers", "course/modules/E/E3/L04.html:112-173", "PASS",
    CARRY + "Exact Fractions recomputation in ledgers/E3/scripts/E3-b-r3/recompute_L04_L06.py (I_X, I_Y, F values) matches Examples 1.7, 2.5, 2.6.")
row("E3b-L04-problems-M-P-E-R", "2.4 / 2.2 numbers", "course/modules/E/E3/L04.html:521-616", "PASS",
    CARRY + "Problem numbers recomputed in round 3 (M1 means, M2/M3 values, E1 I_Y(4000)=500, E2 count 24, R3 argument).")
row("E3b-L04-lab-hypothesis-and-counts", "2.5 labs / 2.2 numbers", "course/modules/E/E3/L04.html:479-506; lab hypothesis at :438-482", "PASS",
    CARRY + "Expected block equals twin output this round (" + S + "lab_compare.out, L04 line). Counts 24/24, 8/8, 10 of 24, 2 of 8 match the output.")
row("E3b-L04-named-pairs-hypothesis", "2.5 labs", "course/modules/E/E3/L04.html:178", "PASS",
    CARRY + "Named pairs A, B, C verdicts match output lines in twin_L04.out.")
row("E3b-L04-grades-and-prose", "2.3 grades / 2.9 prose", "course/modules/E/E3/L04.html:51, 490-493, 510, 611, 626-631", "PASS",
    CARRY + "Theorems graded T, lab-derived counts graded C with the lab named; no banned phrase or process word on L04 (grep, this round).")
row("E3b-L04-cards", "2.7 cards", "course/modules/E/E3/cards.json E3-c056..E3-c077", "PASS",
    CARRY + "Cards E3-c056..c077 are byte-identical in cards.json per-card comparison (" + S + "delta_and_cards.out lists c081, c082, c084, c090, c091 and c113 as the only changed cards in L04-L06, none of them L04); each matches its L04 statement.")

# ---- L05 (re-verified in full: page changed) ----
row("E3b-L05-def-thm1.3-cor1.4", "2.4 mathematics", "course/modules/E/E3/L05.html:63-96", "PASS",
    "Read lines 63-96. Re-derived Theorem 1.3(a) by raising CE1^(1-gamma) to a/(1-gamma); (b) H(x)=(1-beta)c0^a+beta x^a monotone for either sign of a; Corollary 1.4 CE of sure k is k. No gap.")
row("E3b-L05-prop2.2", "2.4 mathematics", "course/modules/E/E3/L05.html:110-120", "PASS",
    "Re-derived dV0/dc0=(1-beta)c0^(a-1)K^(1/a-1), dV0/dc1=beta c1^(a-1)K^(1/a-1), MRS=((1-beta)/beta)(c1/c0)^(1-a) with 1-a=1/psi, so EIS=psi. Numeric check: closed form 0.4444444444 vs finite difference 0.4444444443 (" + S + "recompute_L05_L06.out).")
row("E3b-L05-remark2.3-gamma-claim", "2.5 labs / 2.2 numbers", "course/modules/E/E3/L05.html:124", "FAIL",
    "Remark 2.3 now says Lab 1 'estimates the EIS at one deterministic plan for three values of psi, with gamma not entering the estimate'. The twin hard-codes gamma: tests/labs/E3/lab-E3-L05-1.py line 233 `ez_value(x, [(1.0, y)], beta, 2.0, psi)` inside mrs_numeric, called by eis_numeric with no gamma argument; output prints EIS only (lines 347-349 of the expected block). The lab never varies gamma in the EIS, so it does not show that gamma leaves the estimate unchanged. The earlier wording 'at gamma = 2 only' was accurate and was removed.",
    "Restore the disclosure in L05.html:124: replace 'with gamma not entering the estimate' with 'at gamma = 2 only' (the earlier wording). Remark 2.3's mathematical claim can stay: it follows from CE1 = c1 for every gamma.")
row("E3b-L05-remark1.5-mean-regression", "2.4 / 2.1 scope", "course/modules/E/E3/L05.html:100", "PASS",
    "Round-3 FAIL row re-verified. The text now says the lottery 'enters only through CE1, which depends on the whole distribution of c1, not only on its mean'. Existence check run: lotteries (1,4) and (2,3) with probability 1/2 each have mean 5/2 at both, CE1 8/5 and 12/5 at gamma=2 (" + S + "recompute_L05_L06.out, last line), so 'can have different values' holds.")
row("E3b-L05-remark3.4-slope-sign", "2.4 mathematics", "course/modules/E/E3/L05.html:157", "PASS",
    "Round-3 FAIL row re-verified. Now reads 'where both have marginal rate of substitution (1-beta)/beta, so the curves have slope -(1-beta)/beta', at the diagonal. Since dc1/dc0 = -MRS on an indifference curve (Definition 2.1), the sign is right. Off the diagonal, r^gamma != r^(1/psi) for r != 1 when gamma != 1/psi, so the slopes differ.")
row("E3b-L05-cards-c078-c091", "2.7 cards", "course/modules/E/E3/cards.json E3-c078..E3-c091", "PASS",
    "All cards re-read against the current L05 text. c081 (A1 to A4 added, Corollary 1.4), c082 (round-3 FAIL, now matches Remark 1.5), c084 (round-3 FAIL, now 'A1 to A4 for deterministic plans', matches Proposition 2.2), c090 and c091 (match Remark 3.4 and Corollary 3.3). Others unchanged and checked.")
row("E3b-L05-cards-c092-c093-grade", "2.7 cards / 2.3 grades", "course/modules/E/E3/cards.json:627-638 (E3-c092, E3-c093) vs course/modules/E/E3/L05.html:500", "FAIL",
    "Card E3-c093 ('On the exact tree of Lab 1, what are V0, U, the mean of c1 and CE1?') has grade T and no basis. The key-results row for the same numbers, L05.html:500, grades them C with source 'Lab 1 (exact Fraction arithmetic on one tree); Problem E1 by hand'. E3-c092 gives the same mean and CE1 with grade T. Card and lesson disagree on grade.",
    "In cards.json set E3-c093 to grade C with basis 'Lab 1 (exact Fraction arithmetic on one tree); Problem E1 by hand', as key-results row 500 does. Set E3-c092 to the same grade and basis, or give the lesson's misconception 3 (L05.html:377-378) a grade and make both agree.")
row("E3b-L05-cards-c094-c097", "2.7 cards", "course/modules/E/E3/cards.json E3-c094..E3-c097", "PASS",
    "c094 EIS lines and step (lab lines 316-318, c1 in [0.999,1.001] times 4 at L05 lab line 243); c095 U and V0 values match expected block 343-346; c096 CE1 2.2500, 1.6000, 1.3720 re-derived (recompute_L05_L06.out); c097 D grade matches L05.html:609.")
row("E3b-L05-lab-numbers", "2.2 / 2.5 labs", "course/modules/E/E3/L05.html:162, 328-350, 351, 500-502", "PASS",
    "Expected block equals twin output (" + S + "lab_compare.out). Independent Fraction recomputation: CE1=8/5, mean 5/2, V0=80/49, U=-49/80, (1-gamma)U=49/80=V0^(1-gamma), theta=1. Floats: CE1 2.2500/1.6000/1.3720 (1.371989), V0(1,10)=4.3311, V0(4,4)=4.0000, U(4,4)=-0.2500, U(1,10)=-0.5500, EIS 0.5000/2.0000/0.2500 (" + S + "recompute_L05_L06.out).")
row("E3b-L05-problems", "2.4 / 2.2 numbers", "course/modules/E/E3/L05.html:389-483", "PASS",
    "M1 CE1=2 and mean 5/2; M2 V0=3/2; M3 theta=-2; E1 check; E2 CE1=16/7, V0=160/71 (2.2535, rise from 80/49=1.6327 because CE rises from 8/5 to 16/7), E3 EIS step; R2 identification argument; R3 MRS exponents 2 and 1/2 with r^2=r^(1/2) iff r=1. All recomputed (" + S + "recompute_L05_L06.out).")
row("E3b-L05-quiz-numeric", "2.9 quiz / 2.2 numbers", "course/modules/E/E3/L05.html:567-568 (item 8)", "FAIL",
    "Item 8 prompt asks for the value 'to six decimal places' (line 568), but data-answer=1.632653 with data-tolerance=0.0001 (line 567) accepts any answer within 0.0001 of 1.632653, so the four-decimal answers 1.6326 and 1.6327 are marked correct. Other numeric items (CE1=2, theta=-2, 1/psi=4) check out.",
    "Set data-tolerance to 0.0000005 on item 8 (answer 80/49 = 1.6326530612), or change the prompt to 'to four decimal places' and keep 0.0001.")
row("E3b-L05-quiz-mc", "2.9 quiz", "course/modules/E/E3/L05.html:508-605 (MC items and explanations)", "PASS",
    "Each correct option and explanation read against the lesson: Theorem 1.3(a), Proposition 2.2 and Remark 2.3, Theorem 3.2 and Remark 3.1, Corollary 3.3, Problem P3, Definition 2.1, Corollary 1.4, Lab 1 U and V0 values at (4,4) and (1,10).")
row("E3b-L05-canon-misconceptions", "2.9 prose", "course/modules/E/E3/L05.html:354-381", "PASS",
    "Section 4 bullets match Theorem 3.2, Corollary 3.3, Remark 3.4, Lesson L08 timing, Definition 2.1. Misconception 1 (ranking, ψ=2 outside restriction), 2 (EIS vs gamma, Lab 1 prints) and 3 (mean vs CE1, 80/49) match Lab 1 output.")
row("E3b-L05-key-results", "2.3 grades", "course/modules/E/E3/L05.html:494-502", "PASS",
    "Theorems T and proofs in §1-3; lab-derived rows C with lab named. Row 500 grade C vs card E3-c093 grade T is reported as E3b-L05-cards-c092-c093-grade.")
row("E3b-L05-references", "2.1 citations", "course/modules/E/E3/L05.html:607-611", "PASS",
    "The reference is grade D, names only the paper, cites no locator, and states the work-level attribution. Crossref confirms the record (E3b-refs-epstein1989).")

# ---- L06 (re-verified in full: page changed) ----
row("E3b-L06-def-prop1.4", "2.4 mathematics", "course/modules/E/E3/L06.html:55-90", "PASS",
    "Re-derived v'(x)=lambda delta(-x)^(delta-1)>0 and v''(x)=lambda delta(1-delta)(-x)^(delta-2)>0 for x<0; v''=alpha(alpha-1)x^(alpha-2)<0 for x>0; continuity at 0; Remark 1.5 ratio lambda; Definition 1.6 equivalence to lambda>1. Correct.")
row("E3b-L06-prop2.1-2.2-ex2.3", "2.4 / 2.2 numbers", "course/modules/E/E3/L06.html:96-119", "PASS",
    "W = p g - (1-p) lambda l re-derived; lambda*=5/3, W(1)=200, W(3/2)=50, W(2)=-100; power threshold p g^alpha/((1-p) l^delta) and W at lambda=2 with alpha=delta=1/2 = -8.6835091 (recompute_L05_L06.out).")
row("E3b-L06-remark2.4-2.5", "2.4 mathematics / 2.2 numbers", "course/modules/E/E3/L06.html:122-129", "PASS",
    "Remark 2.4 CE sign argument re-derived (v continuous, strictly increasing, v(0)=0, onto R). Remark 2.5 combined lottery 2000/400/-1200 with probabilities 1/4, 1/2, 1/4: value 700-300 lambda; separate 1000-600 lambda; at lambda=2, 100 and -200 (recompute_L05_L06.out).")
row("E3b-L06-remark3.1", "2.4 scope", "course/modules/E/E3/L06.html:282-288", "PASS",
    "Proposition 1.4 needs only lambda>0; Propositions 2.1 and 2.2 are linear in lambda for every lambda>0. 'the threshold ... is 5/3, which is above 1' matches Example 2.3.")
row("E3b-L06-remark3.2", "2.4 mathematics / 2.2 numbers", "course/modules/E/E3/L06.html:286-288", "PASS",
    "Round-3 FAIL row re-verified. Re-derived: alpha=1 gives p(g-EV)-(1-p)(l+EV)=EV-EV=0, lambda_R=1; Example 2.3 with EV=200 gives g-EV=l+EV=800 and value (1/2)800^alpha(1-lambda); p=1/3, g=1000, l=300 gives EV=400/3, ratio 2, lambda_R=sqrt(2)/2=0.7071 (recompute_L05_L06.out, 'R3.2' lines).")
row("E3b-L06-remark3.2-reference-scope", "2.4 scope / 2.9 prose", "course/modules/E/E3/L06.html:287 vs lines 296, 410-412, 495-501", "PASS",
    "Round-3 FAIL row re-verified. Remark 3.2 says the lesson uses its reference point 'only here, in Section 4, in Problem R2 and in retrieval quiz item 7'. grep of 'reference point' and 'Remark 3.2' in L06.html gives: 287 (the remark), 296 (Section 4 bullet 2), 410-412 (Problem R2), 495-501 (quiz item 7, the seventh li). No other use of the expected-value reference point. Statement holds.")
row("E3b-L06-lab-numbers", "2.5 labs / 2.2 numbers", "course/modules/E/E3/L06.html:133, 257-274, 275, 307-315, 438", "PASS",
    "Expected block equals twin output (" + S + "lab_compare.out). Independent recomputation matches every printed value. Interpretation line 275: grid of four gains (1,2,4,9) and four losses (-9,-4,-2,-1) matches the twin's grid. Hypothesis line 133 values match output.")
row("E3b-L06-problems", "2.4 / 2.2 numbers", "course/modules/E/E3/L06.html:326-416", "PASS",
    "M1 lambda*=3/2, W(2)=-100; M2 EV=0, W=-50, lambda*=1 < 2; M3 v(16)=4, v(-16)=-8, ratio 2; E1 values; E2 sqrt(5/3)=1.2910; E3 combined 250 and separate 100 at lambda=3/2, sign change on (5/3, 7/3) re-derived; R2 with Remark 3.2 values; R3 v(1)=1 vs v(2)+v(-1)=0 at lambda=2. All recomputed.")
row("E3b-L06-quiz-numeric", "2.9 quiz / 2.2 numbers", "course/modules/E/E3/L06.html:466-507", "PASS",
    "lambda* 1.6667 within 1e-4 of 5/3; W=-100 exact; 1.2910 within 1e-4 of sqrt(5/3)=1.29099; each explanation matches the lesson. MC items 1, 2, 5, 6, 7, 9, 10 read against Remark 1.5, Proposition 1.4, Example 2.3, Remark 3.1, Remark 3.2, Example 2.3 and Remark 2.4.")
row("E3b-L06-cards", "2.7 cards", "course/modules/E/E3/cards.json E3-c098..E3-c117", "PASS",
    "All 20 L06 cards re-read against the current text. c111 (Remark 3.2, lambda_R) and c113 (round-3 changed; lambda_R=sqrt(2)/2 about 0.7071, matches Remark 3.2) match. c115-c117 are grade C with a basis matching key-results rows 437-438. c112 and c114 section numbers match lines 306 and 314.")
row("E3b-L06-canon-breaks-misconceptions", "2.9 prose", "course/modules/E/E3/L06.html:291-318", "PASS",
    "Section 4 has four bullets; bullet 1 cites no magnitude; bullet 2 numbers 5/3 and 1 match Remark 3.2; misconception 3 gives 100 and -200 matching Remark 2.5.")
row("E3b-L06-prose-claims", "2.9 prose / process words", "course/modules/E/E3/L06.html (whole page); L05.html (whole page)", "PASS",
    "Full read of both pages. grep -i for builder, verifier, ledger, round, TODO, TBD, placeholder, lorem, obviously, clearly, studies show, ellipsis: no hits in L05 or L06 (also none in the L05 and L06 card text).")
row("E3b-L06-key-results", "2.3 grades", "course/modules/E/E3/L06.html:431-438", "PASS",
    "T for Proposition 1.4, Remark 1.5, Propositions 2.1-2.2, Remark 2.4, Remark 2.5; C for the lab-read rows 437-438 with lab named.")

# ---- delta bookkeeping ----
row("E3b-delta-round4", "delta", "ccfdf4c..b276325 for L04, L05, L06, both twins, cards.json, notation, references", "PASS",
    "Hashes (" + S + "delta_and_cards.out): L04.html, lab-E3-L04-1.py, lab-E3-L05-1.py, lab-E3-L06-1.py, notation.json, references.json SAME. L05.html, L06.html, cards.json CHANGED. Changed slice cards: E3-c081, c082, c084, c090, c091, c113. Every changed hunk in L05 and L06 read in context, and both pages read in full. pyproject.toml change (ruff exclude) does not touch the slice.")
row("E3b-previous-round-rows", "bookkeeping", "/Users/billyribeiro/.fanout/frags/C-E3-b.round3.json (round-3 FAIL rows)", "PASS",
    "All five round-3 FAIL rows were re-verified from scratch this round: E3b-L05-remark1.5-mean-regression, E3b-L05-card-E3-c082 and E3b-L05-card-E3-c084-assumptions (now PASS as rows E3b-L05-remark1.5-mean-regression and E3b-L05-cards-c078-c091), E3b-L05-remark3.4-slope-sign (PASS), E3b-L06-remark3.2-reference-scope (PASS).")

verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
fragment = {
    "unit": "E3",
    "slice": "E3-b",
    "round": 4,
    "verifier": "Haiku independent verifier, unit E3 slice b, round 4; did not build E3",
    "pin": "b276325",
    "base": "ccfdf4c (previous pin, round 3 fragment /Users/billyribeiro/.fanout/frags/C-E3-b.round3.json)",
    "checkout": ROOT,
    "scratch": S,
    "verified_at": "2026-10-29T02:30:00+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Mutation testing not applicable: slice b is lesson pages and lab twins only (VERIFIER_RULES 2.5 and the ruling: mutation testing applies to project graders). "
        "L04 subjects byte-identical to ccfdf4c, so L04 rows are carried from round 3 with the carry prefix; all other rows were re-verified from scratch. "
        "Not checked: the live Crossref/verify_refs --unit run for the whole registry (only the two cited keys were fetched by plain curl); "
        "hub course/modules/E/E3/index.html (changed in the delta, outside slice b); Pyodide-vs-CPython output identity beyond page_smoke PASS; "
        "the full pytest suite and render_curriculum gate (no generator input touched by the slice). Lab EIS values are finite-difference outputs, checked to 4 decimals against the exact value psi."
    ),
    "summary": (
        f"E3-b round 4: {sum(r['status']=='PASS' for r in rows)} PASS, {sum(r['status']!='PASS' for r in rows)} non-PASS of {len(rows)} rows. "
        "Non-PASS: E3b-L05-remark2.3-gamma-claim (lab-scope overreach), E3b-L05-cards-c092-c093-grade (card grade T vs lesson C), E3b-L05-quiz-numeric (six-decimal prompt with 1e-4 tolerance). "
        "All round-3 FAIL rows are fixed and re-verified."
    ),
}
json.dump(fragment, open(ROOT + "/ledgers/E3/E3-b.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(verdict, len(rows))
