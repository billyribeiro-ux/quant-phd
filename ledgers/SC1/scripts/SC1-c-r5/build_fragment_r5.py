"""Build the round-5 SC1-c fragment (ledgers/SC1/SC1-c.json) from the round-5 evidence recorded by the verifier."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
S = "ledgers/SC1/scripts/SC1-c-r5/"
OUT = "ledgers/SC1/scripts/SC1-c-r5/out/"
L7 = "course/modules/SC/SC1/L07.html"
L8 = "course/modules/SC/SC1/L08.html"
TW7 = "tests/labs/SC1/lab-SC1-L07-1.py"
TW8 = "tests/labs/SC1/lab-SC1-L08-1.py"
CARDS = "course/modules/SC/SC1/cards.json"

rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> None:
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        assert fix, rid
        r["fix"] = fix
    rows.append(r)


# ---- gates (command rows, re-run this round) ----
row("gate-check-pages", "2.9 structure (check_pages)", f"{L7}, {L8}", "PASS",
    "Re-run at pin 7376a5e2: .venv/bin/python tools/check_pages.py --unit SC1 --page L07 -> 'check_pages SC1 L07: PASS'; "
    "--page L08 -> 'check_pages SC1 L08: PASS' (exit 0 each) (" + OUT + "gates_1.txt).")
row("gate-check-dag", "2.9 DAG (check_dag)", f"{L7}, {L8} links and anchors", "PASS",
    "Re-run: tools/check_dag.py --unit SC1 -> 'check_dag SC1: PASS', exit 0 (" + OUT + "gates_1.txt). Anchors read this round: "
    "def-running-maximum-distribution (L07 line 64), def-first-passage-time (L08 line 59); links to L07 and L01/L02/L06 resolve.")
row("gate-run-labs", "2.5 labs (run_labs)", "tests/labs/SC1/lab-SC1-L07-1.py, lab-SC1-L08-1.py", "PASS",
    "Re-run: tools/run_labs.py --unit SC1 --page L07 -> 'run_labs SC1: PASS (1/1)'; --page L08 -> 'run_labs SC1: PASS (1/1)' (" + OUT + "gates_1.txt).")
row("lab-L07-twin-isolated", "2.5 labs (python -I -W error)", TW7, "PASS",
    "ledgers/SC1/scripts/SC1-c-r5/check_embed_r5.py runs the twin as python -I -W error from /tmp: exit 0, stderr 0 chars "
    "(" + OUT + "check_embed_r5.out, 'L07: twin exit 0, stderr chars 0').")
row("lab-L08-twin-isolated", "2.5 labs (python -I -W error)", TW8, "PASS",
    "Same run: 'L08: twin exit 0, stderr chars 0' (" + OUT + "check_embed_r5.out).")
row("lab-L07-page-equals-twin", "2.5 labs (embed)", f"{L7} <code data-run> vs {TW7}", "PASS",
    "check_embed_r5.py: page code (HTML-unescaped) equals twin.rstrip('\\n') (True, both tests in the script); the only difference "
    "is the final newline, which tools/embed_labs.py strips by design (line 117 of tools/embed_labs.py) (" + OUT + "check_embed_r5.out).")
row("lab-L08-page-equals-twin", "2.5 labs (embed)", f"{L8} <code data-run> vs {TW8}", "PASS",
    "Same check: page code equals twin.rstrip('\\n') (True) (" + OUT + "check_embed_r5.out).")
row("lab-L07-expected-equals-output", "2.5 labs (expected block)", f"{L7} pre.expected", "PASS",
    "Byte check this round: expected block == stdout.rstrip('\\n') for L07 (True; exact after strip, True) and for L08 (True) "
    "(" + OUT + "check_embed_r5.out and the twin run output).")
row("lab-L08-expected-equals-output", "2.5 labs (expected block)", f"{L8} pre.expected", "PASS",
    "Same byte check for L08 (True); the expected block lines 345-363 equal the twin stdout after the new Part A labels.")
row("lab-L07-printed-numbers", "2.2 numbers (a) lab-computed", f"{L7} expected block (lines 353-375) and interpretation (line 376)", "PASS",
    "Independent DP recomputation (" + S + "recompute_r5.py, out " + OUT + "recompute_r5.out): walk identity 78 of 78 by "
    "state DP; exact tail N=16,m=4 = 10889/32768 = 0.332306; closed 2(1-Phi(1)) = 0.3173105079; 1-Phi(1) = 0.1586552539; "
    "E[M_1] = sqrt(2/pi) = 0.79788456; Part B proportions 0.2275/0.2675/0.2825/0.3025 with counts 91/107/113/121 and se "
    "0.0210/0.0222/0.0225/0.0230 (recomputed from the same seeded draws); Part C means 0.5546/0.6639/0.7232/0.7586 and "
    "gaps to sqrt(2/pi) (" + OUT + "recompute_r5.out). Nesting violations 0 recomputed (" + S + "sim_checks_r5.py, " + OUT + "sim_checks_r5.out). "
    "Every printed L07 figure in the expected block and prose reproduces.")
row("lab-L08-printed-numbers", "2.2 numbers (a) lab-computed", f"{L8} expected block (lines 344-363) and interpretation (line 364)", "PASS",
    "DP recomputation (" + OUT + "recompute_r5.out): 8190 step sequences, 90114 (sequence, level) pairs, first-passage counts "
    "[512,0,384,0,288,0,224,0,180,0] summing to 1588; P(nu_3<=12)=1588/4096=0.3876953125; P(S_12>=3)=0.19384765625; "
    "truncated means 5.480560303, 11.815731233, 24.557203397; Part C sample means/se/z reproduced by " + S + "sim_checks_r5.py "
    "(-1.0466, -0.6866, -0.7748); Part D densities 0.2419707245 and 0.1098478224, P(tau_1<=2)=erfc(1/2)=0.4795001222.")
row("lab-L07-hypothesis-interpretation", "2.5 lab statements", f"{L7} lab hypothesis (line 150) and interpretation (line 376)", "PASS",
    "Each claim re-read against the twin and output: exact tails decrease (0.375000 to 0.317547); counts 91, 107, 113, 121 do not "
    "decrease; pathwise violations 0; gap narrows 0.0898 to 0.0148; 'the lab does not check A3 and A4' true (no code path tests them).")
row("lab-L08-hypothesis-interpretation", "2.5 lab statements", f"{L8} lab hypothesis (line 142) and interpretation (line 364)", "PASS",
    "Round-4 FAIL fixed. Line 142 now says 'agree on each (sequence, level) pair'; line 364 says 'agree on all 90114 pairs' and "
    "8190 sequences = sum 2^n (n=1..12) and 90114 pairs = sum n 2^n, both recomputed (" + OUT + "recompute_r5.out). "
    "The twin Part A print lines (twin lines 88-94) match.")
row("lab-simulated-labels-seeds", "2.5 labs (seeds, SIMULATED labels)", f"{L7} and {L8} lab headings; twins SEED", "PASS",
    "L07 heading '(Parts B and C SIMULATED)', SEED = 20260507; L08 heading '(Part C SIMULATED)', SEED = 20260508 (twin line 37). Exact parts "
    "contain no RNG call (twin code: random.Random is used only in fine_path/simulate_maxima at twin lines 101 and 125 for L07, and in simulated_first_passage at twin line 123 for L08).")
row("lab-runtime", "2.5 labs (runtime)", "tests/labs/SC1 twins; page_smoke Pyodide timing", "PASS",
    "Re-run page_smoke (" + OUT + "page_smoke_L07_L08.txt): 'lab lab-SC1-L07-1: 0.1 s', 'lab lab-SC1-L08-1: 0.2 s'. "
    "Both are under 10 s.")
row("lint-mypy-twins", "code quality (ruff, mypy strict)", f"{TW7}, {TW8}", "PASS",
    "Re-run (" + OUT + "lint_mypy.txt): ruff check 'All checks passed!' (exit 0); ruff format --check '2 files already formatted' "
    "(exit 0); mypy --no-incremental: 'Success: no issues found in 2 source files' (exit 0).")
row("page-smoke-L07-L08", "2.9 page_smoke (console, math, 360 px, labs in Pyodide)", f"{L7}, {L8}", "PASS",
    "Re-run alone: tools/page_smoke.py --unit SC1 --pages L07 L08 -> 'page_smoke modules/SC/SC1/L07.html: PASS', "
    "'page_smoke modules/SC/SC1/L08.html: PASS', 'page_smoke SC1: PASS', exit 0 (" + OUT + "page_smoke_L07_L08.txt). No figures on these pages.")
row("pytest-lab-tools", "2.5 labs (pytest, tooling)", "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py", "PASS",
    ".venv/bin/python -m pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -q -> dots to [100%], exit 0 "
    "(" + OUT + "pytest_labs_r5.out). Full suite not run (outside this slice).")
row("verify-refs-offline", "2.1 citations (integrity, offline)", "references/references.json", "PASS",
    "tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems', exit 0 (" + OUT + "verify_refs_offline_r5.out).")
row("verify-refs-live-SC1", "2.1 citations (live, unit)", "references/references.json entry used by SC1 (shreve2004stochastic)", "PASS",
    "tools/verify_refs.py --unit SC1: 'live re-verification of SC1: 1 of 560 entries, 0 problems', exit 0 (" + OUT + "verify_refs_live_SC1_r5.out). "
    "Registry record read: references/references.json:20732-20744 (Shreve, 2004).")
row("refs-no-citation-markup", "2.1 attribution (no unread citation)", f"{L7}, {L8}", "PASS",
    "grep -c 'data-cite|data-locator' = 0 for both pages; no Karatzas, Billingsley, Williams, Kloeden, Oksendal or Magdonis-Ismail text "
    "on either page; every card has cite [] (" + CARDS + "). Both References sections say no passage is cited.")
row("claim-grades-L07", "2.3 grades (re-graded)", f"{L7} Theorem 1.3, Cor 1.5, Prop 2.2, Cor 2.3, Remarks 1.4 and 2.4, key-results table, lab rows", "PASS",
    "Re-graded against BLUEPRINT section 3: T for Theorem 1.3 (H2 = A3, A4), Cor 1.5(a) (T), Cor 1.5(b) (T, assumes labelled A5), "
    "Prop 2.2, Cor 2.3, Remarks 1.4 and 2.4 (T); C for the exact enumeration and the SIMULATED lab rows with basis named (lines 523-525).")
row("claim-grades-L08", "2.3 grades (re-graded)", f"{L8} Prop 1.2, Cor 1.3-1.5, Prop 2.2-2.3, key-results table", "PASS",
    "Prop 1.2 T (no probability assumption); Cor 1.3 T (assuming A3, A4 through L07 Theorem 1.3); Cor 1.4 T (a limit of probabilities, "
    "stated as such, line 93); Cor 1.5 T (assuming A3, A4); Prop 2.2 and 2.3 T (finite sums); the enumeration and the simulation are C with basis (lines 511-512).")
row("math-L07-thm-1.3", "2.4 mathematics (Theorem 1.3 and proof)", f"{L7} lines 67-80", "PASS",
    "Chain re-derived: L06 Theorem 2.5 (line 153) gives P(M_t>=a)=2P(B_t>=a) under A3, A4; L01 Definition 1.1 (D2) with s=0 gives "
    "B_H ~ N(0,H); no atoms gives P(Z>=x)=1-Phi(x); L06 Corollary 2.6 (line 174) gives 2P(B_t>a)=erfc(a/sqrt(2t)); "
    "2(1-Phi(a/sqrt H)) = erfc(a/sqrt(2H)) at a=1, H=1,2 by math.erfc (" + OUT + "recompute_r5.out).")
row("math-L07-cor-1.5b", "2.4 mathematics (Corollary 1.5(b))", f"{L7} lines 101-107", "PASS",
    "Integration by parts re-derived: int_0^R (1-Phi) = R(1-Phi(R)) + phi(0) - phi(R); 0 <= R(1-Phi(R)) <= phi(R) -> 0; int_0^inf (1-Phi) = phi(0) = 1/sqrt(2 pi); "
    "E[M_H] = 2 sqrt(H) phi(0) = sqrt(2H/pi); sqrt(2/pi) = 0.79788456 (" + OUT + "recompute_r5.out).")
row("math-L07-prop-2.2-cor-2.3-remark-2.4", "2.4 mathematics (Prop 2.2, Cor 2.3, Remark 2.4)", f"{L7} lines 120-146 (Prop 2.2 H2 at line 123)", "FAIL",
    "Prop 2.2 is stated for 'N and N' integers with N>=1, and N divides N'' (line 123, H2). Definition 2.1 (line 116) defines the grid "
    "maximum only for an integer N>=1, so M^(N') is undefined when N' <= 0; and N'=0 or N'=-N satisfy H2 (0 and -N are divisible by N). "
    "Conclusion (b) is therefore not well-posed for those N'. The proof (line 131) writes N'=cN 'with c a positive integer', which needs N'>=1, "
    "so the proof uses a hypothesis the statement omits. Corollary 2.3 and Remark 2.4 re-derived correctly. The same omission is in card SC1-c144 front "
    "(" + CARDS + ") and in Problem P3 (line 453).",
    "Line 123 (Proposition 2.2, H2): replace with 'N and N′ are integers with N ≥ 1 and N′ ≥ 1, and N divides N′.' "
    "Card SC1-c144 front: add 'with N′ ≥ 1' after 'If N divides N′'. Problem P3 (line 453): 'Let N and N′ ≥ 1 be integers with N dividing N′.' "
    "Then run tools/check_pages.py --unit SC1 --page L07 and tools/check_pages.py --unit SC1.")
row("math-L07-def-2.1-grid-times", "2.4 mathematics (notation and definition)", f"{L7} line 116 (Definition 2.1)", "PASS",
    "Round-4 FAIL fixed. Line 116 now reads M^(N)_H = max_{0<=k<=N} B_{s_k} with s_k = kH/N defined on the same line (grep: B_{H_k} absent). "
    "Proposition 2.2 (line 130) and card SC1-c142 use s_k consistently.")
row("math-L07-remark-1.4-phi0", "2.4 mathematics (Remark 1.4)", f"{L7} line 84", "PASS",
    "Round-3/4 defect fixed: the sentence reads 'These two events add to 1, because P(Z>=0)+P(Z<=0)=1+P(Z=0) and P(Z=0)=0'. "
    "Limits 0 (H->0) and 1 (H->inf) re-derived; Phi(0)=1/2 by evenness.")
row("math-L07-R1-R3-P2-P3-M-E", "2.4 mathematics (problem solutions)", f"{L7} lines 412-504", "FAIL",
    "Re-solved this round: M1 (2(1-Phi(1)) = erfc(2/sqrt8) = erfc(1/sqrt2), 0.3173105079), M2, M3 (1-Phi(1) = 0.1586552539, exactly half), "
    "P1 (hypotheses H1-H3 applied per level b>0), P2 (integration by parts), E1 (0.2275*400=91, 0.3025*400=121), E2 (14893+6885=21778, "
    "21778/65536=0.332306), E3 (sqrt(33759/63840000)=0.0229958, printed 0.0230), R1 (a<0 gives >1), R2 (no atoms), R3 (limit 0). "
    "P3 (line 453) states 'Let N divide N'' with no N'>=1 hypothesis, the same omission as row math-L07-prop-2.2-cor-2.3-remark-2.4.",
    "Problem P3, line 453: state 'Let N and N′ be integers with N ≥ 1 and N′ ≥ 1, and N dividing N′. Assuming H1 of Proposition 2.2.'")
row("math-L08-prop-1.2-cor-1.3-1.4", "2.4 mathematics (Prop 1.2, Cor 1.3, Cor 1.4)", f"{L8} lines 62-94", "PASS",
    "Prop 1.2 both inclusions re-derived (closed-set infimum; IVT on (0, s*]; B_0=0 used); Cor 1.3 chain (event identity, L07 Theorem 1.3, L06 Cor 2.6); "
    "Cor 1.4: union over integers n and lim 2(1-Phi(a/sqrt n)) = 1 by Phi(0)=1/2.")
row("math-L08-cor-1.5", "2.4 mathematics (Corollary 1.5, density)", f"{L8} lines 96-104", "PASS",
    "F'(H) = a H^{-3/2} phi(a/sqrt H) re-derived by the chain rule (g' = -(1/2) a H^{-3/2}); F(0+)=0; numeric check of density "
    "0.2419707245 and 0.1098478224 (" + OUT + "recompute_r5.out).")
row("math-L08-prop-2.2-2.3", "2.4 mathematics (Prop 2.2, Prop 2.3)", f"{L8} lines 120-138", "PASS",
    "Prop 2.2 both inclusions re-derived (S_{k*}=a since steps are +-1; k*-1 has S <= a-1); count identity from L06 Cor 1.4 (line 88-89). "
    "Brute force by DP: 8190 sequences, 90114 pairs, all agree (" + OUT + "recompute_r5.out). Prop 2.3: min(nu,N)=sum_k 1{nu>k}; "
    "P(nu>k) integer over 2^k.")
row("math-L08-R3", "2.4 mathematics (Problem R3)", f"{L8} lines 489-495", "PASS",
    "d/dH log f_a = (a^2-3H)/(2H^2) re-derived; mode a^2/3; f_1(0.30)=0.458568, f_1(1/3)=0.462541, f_1(0.36)=0.460542 "
    "(" + OUT + "recompute_r5.out).")
row("math-L08-R1-R2", "2.4 mathematics (Problems R1, R2)", f"{L8} lines 476-487", "PASS",
    "R1: #{nu<=N} = 2#{S_N>=a} - #{S_N=a} re-derived; #{S_12=3}=0 by parity; 1588 = 2 x 794 (DP). R2: min(nu,N+1)-min(nu,N)=1{nu>N} re-derived.")
row("prob-L08-all", "2.4 problems (all L08 problems, solutions)", f"{L8} lines 400-496", "PASS",
    "All nine problems read and recomputed: M1 0.3173105 (erfc form), M2 0.2419707, M3 5/8 by listing and by the walk identity 4+1; "
    "P1 hypotheses (continuity, B_0=0, a>0); P2 identity; P3 truncated-mean identity; E1 parity counts and sum 1588; E2 z values -1.05, -0.69, -0.77; "
    "E3 density 0.109848 (0.398942 x 0.353553 x 0.778801 = 0.109848); R1-R3 as above.")
row("prob-L07-remaining", "2.4 problems (other L07 problems)", f"{L7} problems M1-M3, P2, P3, E1-E3, R1-R3", "PASS",
    "Recomputed in math-L07-R1-R3-P2-P3-M-E (the P3 defect is recorded there and in math-L07-prop-2.2-cor-2.3-remark-2.4); P1 in prob-L07-P1-assumptions.")
row("misconceptions-L07-content", "2.4 misconceptions (content)", f"{L7} Misconceptions 1-3 (lines 391-402)", "PASS",
    "Misconception 1: 0.3173105 rounds to 0.3173 and 0.1586553 to 0.1587; P(M_1>=1)-P(B_1>=1) = P(M_1>=1, B_1<1) correct. "
    "Misconception 2: grid estimates 0.2275 and 0.3025 lie below 0.3173105. Misconception 3: no tail formula for B-tilde (L01 section 4 lines 212-234 confirm B-tilde satisfies D1-D3 and has the same finite-dimensional laws, with discontinuous paths).")
row("misconceptions-L08-content", "2.4 misconceptions (content)", f"{L8} Misconceptions 1-3 (lines 379-389)", "PASS",
    "Misconception 1: Corollary 1.4 is a probability statement; {tau=infinity} has probability zero, not empty. Misconception 2: P(tau_1<=1)=0.317311 vs "
    "P(B_1>=1)=0.1586552539 (line 385); the walk ratio 1588:794 is exactly two at n=12, a=3 (Problem R1). Misconception 3: density ~ const H^{-3/2}, no moment (correct).")
row("canon-breaks-L07-L08", "2.4 canon breaks", f"{L7} Section 3 (lines 379-386); {L8} Section 3 (lines 368-374)", "PASS",
    "L07: continuity needed (L06 Lemma 2.1 requires continuous paths, L06 line 105); closed form conditional on A3, A4 (sketch for A3 only, L05 line 280); grid vs continuous tail (Cor 2.3). "
    "L08: the jump example (0 on [0,1/2), 2 from 1/2 on) has M_1=2>=1 and never equals 1, so tau_1=infinity and {tau_1<=1} fails (checked by hand); "
    "Corollaries 1.3-1.5 assume A3, A4; finite does not mean integrable.")
row("key-results-L07", "2.4 key-results table", f"{L7} Section 6 table (lines 517-525)", "PASS",
    "Each row checked against its proof, the lab output (" + OUT + "recompute_r5.out) or its simulation status. Row 521 (nested grids nondecreasing) holds by Prop 2.2(b); "
    "row 524 range 0.2275 to 0.3025 matches the printed proportions.")
row("key-results-L08", "2.4 key-results table", f"{L8} Section 6 table (lines 505-512)", "PASS",
    "Round-4 FAIL fixed. Row 511 now reads '90114 (sequence, level) pairs for n<=12 and a<=n ... 78 of 78 (n,a) pairs'. Rows 505-510 re-checked against the "
    "propositions. Row 505 states 'on every continuous path with a>0'; the hypothesis B_0=0 is supplied by L01 Definition 1.1 (D1, which holds identically), "
    "so the row is correct as a statement about B.")
row("quiz-L07", "2.9 quiz (answers, tolerances, explanations)", f"{L7} Section 7 (ten items, lines 531-610)", "PASS",
    "Round-4 FAIL fixed. Item q10 (line 604) now reads 'for every a>0 its tail is half the continuous tail'. All ten items recomputed: q2 0.3173105 "
    "(diff 7.9e-9 <= 1e-6); q4 0.158655 (diff 2.5e-7 <= 1e-6); q6 0.797885 (diff 4.4e-7 <= 1e-6); q8 0.3173105 (diff 7.9e-9); keyed answers and explanations match "
    "(" + OUT + "recompute_r5.out).")
row("quiz-L08", "2.9 quiz (answers, tolerances, explanations)", f"{L8} Section 7 (lines 518-597)", "PASS",
    "Keyed numeric answers recomputed: q2 0.3173105079 (diff 7.9e-9 <= 1e-6); q3 5/8 exact (tolerance 1e-9); q5 5.480560302734 vs 5.48056 (diff 3.0e-7 <= 1e-5); "
    "q6 0.2419707245 vs 0.241971 (diff 2.8e-7 <= 1e-6). Multiple-choice keys: continuity and B_0=0; Cor 1.4 probability statement; Remark 1.6; "
    "Problem R1 parity; jump example; parity of S_k. Explanations match.")
row("structure-L07", "2.9 structure and prose (template sections)", f"{L7}", "PASS",
    "check_pages L07 PASS (this round). data-hours 9; why-it-matters within 120 words; Definitions 1.1-2.1, Theorem 1.3, Corollaries 1.5, 2.3, Remarks 1.4, 2.4, "
    "Propositions 2.2; inline Lab 1; canon-breaks; three misconceptions; problems M1-M3, P1-P3, E1-E3, R1-R3 each with details.solution; key-results table; "
    "ten quiz items with explanations; references.")
row("structure-L08", "2.9 structure and prose (template sections)", f"{L8}", "PASS",
    "check_pages L08 PASS (this round). data-hours 9; Definitions 1.1, 2.1; Propositions 1.2, 2.2, 2.3; Corollaries 1.3-1.5; Remark 1.6; inline Lab 1; "
    "canon-breaks; three misconceptions; problems M1-M3, P1-P3, E1-E3, R1-R3; key-results table; ten quiz items; references.")
row("banned-and-process-words", "2.9 banned phrases and process words", f"{L7}, {L8}", "PASS",
    "grep -i over both pages (this round) for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, "
    "important to note, studies show, experts agree, well known, obviously, clearly, builder, verif, fixer, architect, ruling, 'round ', 'plan ', REQUEST, "
    "unit report, and an ellipsis: no hits except the project title 'Reflection Principle Verified' (L08 footer nav), which is a curriculum title, not a process word.")
row("notation-macros", "2.4 notation (notation.json)", f"{L7}, {L8}", "PASS",
    "Registered macros used: \\E, \\Prob, \\indic (notation/notation.json macros). \\Phi is the registered standard normal CDF symbol (symbols array). "
    "\\varphi only for the Gaussian density (L07 lines 104-106; L08 line 103). No registered symbol takes another meaning; T appears only in the L07 Definition 1.1 "
    "sentence that reserves it (line 59), consistent with the S1 meaning.")
row("dag-defined-once-L07-L08", "2.9 DAG (defined once)", f"{L7} line 64; {L8} line 59", "PASS",
    "dfn def-running-maximum-distribution (L07 line 64) and def-first-passage-time (L08 line 59) each occur once; later uses are links. "
    "The discretely monitored maximum is a plain dfn with no data-concept (L07 line 116). check_dag PASS.")
row("dag-outside-closure", "2.9 DAG (outside the prerequisite closure)", f"{L7} and {L8} meta lines and prose", "PASS",
    "Linked concepts: normal-distribution, random-variable, expectation (M4/M6, in closure), brownian-motion, brownian-motion-construction, reflection-principle, "
    "running-maximum-distribution, first-passage-time (SC1 earlier lessons). No SC2/SC3 concept (ito, sde, girsanov) appears on either page (grep).")
row("xref-L01-L05-L06", "2.1 cross references (Lessons 1, 5, 6)", f"{L7} and {L8} cross-references", "PASS",
    "Re-read this round against current pages: L06 section 2 defines tau_a = inf{s>=0: B_s=a} (L06 line 102); L06 Lemma 2.1 (line 105) states (i) "
    "{M_t>=a}={tau_a<=t} under continuity and B_0=0; Theorem 2.5 (line 153) under A3, A4; Corollary 2.6 (line 174-176) the erfc form; Corollary 1.4 (line 88) the "
    "discrete tail identity; L01 Definition 1.1 (D1-D3, lines 56-62); L01 section 4 defines B-tilde; L05 Assumption A3 (line 270, sketch) and A4 (line 59, standard "
    "facts) match the 'Lesson 5' uses; L05 line 278 limits A3 to bounded stopping times, as L06 Prop 2.3 requires.")
row("cards-dup-and-numbers", "2.7 cards (duplicates; numbers appear in lesson)", f"{CARDS}, L07 and L08 cards", "PASS",
    "ledgers/SC1/scripts/SC1-c-r5/cards_check_r5.py: 196 cards, 196 unique ids, 0 duplicate fronts across the deck, ids all SC1-cNNN; every number "
    "(>=2 digits, excluding 10/12/16/64/256/1000) in an L07/L08 card back occurs in its own lesson text (" + OUT + "cards_check_r5.out).")
row("proof-L07-cor-1.5a-continuity-direction", "2.4 mathematics (continuity from below)", f"{L7} line 103 (Corollary 1.5(a) proof)", "PASS",
    "{M_H>=b} increases as b decreases to m; union over b>m is {M_H>m}; continuity from below and Theorem 1.3 give P(M_H>m) = 2(1-Phi(m/sqrt H)). "
    "The corollary's m=0 case uses levels b>0 only, so H3 is applied at each level b>0 and the statement's 'H3' reading is not a missing hypothesis.")
row("prob-L07-P1-continuity", "2.4 problems (P1 continuity step)", f"{L7} line 441", "PASS",
    "Solution to P1 uses the same continuity-from-below step and continuity of Phi; m=0 by the same limit. Re-derived.")
row("prob-L07-R2-continuity", "2.4 problems (R2 continuity step)", f"{L7} line 498", "PASS",
    "R2: {M_H>=b} increases as b decreases to a; union {M_H>a}; continuity from below and Theorem 1.3 give P(M_H=a)=0. Re-derived.")
row("num-rounding-0.3173105078", "2.2 numbers (rounding of the closed form)", f"{L7} lines 416, 547, 589, 393; {L8} lines 404, 411, 534", "PASS",
    "2 x 0.1586552539 = 0.3173105078 on the printed digits; unrounded 2(1-Phi(1)) = 0.31731050786 rounds to 0.3173105079 (" + OUT + "recompute_r5.out). "
    "The quoted values are consistent, and the rounding rule is stated where the figure is rounded (quiz 'to seven decimals'; L07 line 393 'rounded to four decimals').")
row("notation-T-first-passage-index", "2.4 notation (T and nu)", f"{L8} Definition 2.1 (line 117); both pages", "PASS",
    "grep: no T-horizon on L08 and only the reserved-T sentence on L07 line 59. The first-passage index is nu_a (Definition 2.1), a local symbol defined at first use. The walk length is N.")
row("dag-simple-random-walk-defined-twice", "2.9 DAG (no second definition of a term)", f"{L7} Lab 1 hypothesis (line 150); {L8} line 113", "PASS",
    "L07 defines the walk in words in the lab hypothesis without a dfn; L08 line 113 says the lab works with the walk of Lesson 6, and L06 line 56 defines S_k. No second dfn.")
row("prose-L08-same-events", "2.9 prose (events)", f"{L8} Proposition 1.2, intro and why-it-matters (lines 51, 63-68)", "PASS",
    "The events {tau_a<=H} and {M_H>=a} coincide on every continuous path with B_0=0 and a>0 (Proposition 1.2). B_0=0 holds identically for B by L01 D1, "
    "so 'every continuous path' of B is correctly scoped; the prose does not claim it for paths with B_0 != 0.")
row("prose-L08-first-passage-name", "2.9 prose (naming)", f"{L8} Definitions 1.1, 2.1", "PASS",
    "'first-passage time' tau_a (Brownian) and 'first-passage index' nu_a (walk) named consistently and defined once each.")
row("lab-L07-docstring-exact-fractions", "2.5 lab docstring vs code", f"{TW7} docstring lines 156-161", "PASS",
    "Docstring: exact integer counts divided by 2**N, computed as floats and printed to six decimals; code max_at_least(n, m)/2**n, output 6 decimals. Consistent.")
row("scope-L07-assumption-phrase", "2.4 scope (assumption phrasing)", f"{L7} lines 55, 67-75, 92, 135, 145, 518-522", "PASS",
    "Every result that uses the closed form says 'Assuming A3 and A4' or names H2 (Theorem 1.3); Cor 1.5(b) names A5; Cor 2.3 names H2 for the closed-form equality; "
    "the problem-set intro (line 408) covers the closed-form problems.")
row("scope-L08-everything-after", "2.4 scope (assumption phrasing)", f"{L8} lines 55, 78, 88, 98, 371", "PASS",
    "Corollaries 1.3-1.5 say they assume A3 and A4; Section 2 does not; Corollary 1.4 is stated as a probability statement; canon-breaks line 371 says so.")
row("notation-kappa-redefined", "2.4 notation (kappa)", f"{L7}, {L8}", "PASS",
    "No \\kappa symbol on either page (grep of macro list: none).")
row("math-L08-prop-2.3-denominator", "2.4 mathematics (Prop 2.3 denominator)", f"{L8} Proposition 2.3 (line 132)", "PASS",
    "P(nu_a > k) = (2^k - #{max_{j<=k} S_j >= a})/2^k, an integer over 2^k (k=0 gives 1 = 1/1). Re-derived.")
row("prob-L07-P1-assumptions", "2.4 problems (P1 assumptions)", f"{L7} line 441", "PASS",
    "P1 states H1, H2 and H3 of Theorem 1.3, with H3 applied at each level b>0 and H>0 fixed. Matches the proof at line 103.")
row("cards-L07-L08-full-read", "2.7 cards (full read of L07 and L08 cards)", f"{CARDS}: L07 cards SC1-c134 to c159, c191; L08 cards SC1-c161 to c183, c192, c201", "PASS",
    "Round-4 FAIL fixed. All 49 L07 and L08 cards read this round against the current lesson text (" + OUT + "cards_L07_L08_r5_raw.txt). The missing "
    "L08 misconception card now exists: SC1-c201 (front 'P(tau_a<=H)=P(B_H>=a)', back 'Corollary 1.3 gives 2P(B_H>=a)', grade T, basis Corollary 1.3 and Lab 1 Part D). "
    "Each card's back agrees with its lesson text, grade and basis.")
row("cards-basis-A3-dependence", "2.7 cards (basis names the A3/A4 dependence)", f"{CARDS}: SC1-c139, SC1-c140, SC1-c192", "PASS",
    "Round-4 FAIL fixed. SC1-c192 basis now reads 'Proposition 1.2 (no probability assumption); the closed form is Theorem 1.3 of Lesson 7, assuming A3 and A4 of "
    "Lesson 5' and its back names the A3/A4 dependence. SC1-c139 and c140 bases name A3 and A4 (and A5 for c140).")
row("notation-horizon-H", "2.4 notation (architect decision: H is the horizon symbol; page says so once)", f"{L7} Definition 1.1 (line 59)", "PASS",
    "Round-4 FAIL fixed. Line 59 now says 'Standard texts write the horizon as T; this unit reserves T for the number of return observations, a meaning fixed in module S1, "
    "so the horizon is H throughout.' The sentence matches notation/notation.json (T: number of return observations, module S1). L08 does not repeat it, as the plan requires.")
row("lab-L08-twin-docstring-PATHS", "2.5 lab docstring vs code", f"{TW8} line 3 and the module docstring", "PASS",
    "The docstring says 'draws SIM_PATHS seeded simple random walk paths'; SIM_PATHS = 1000 is defined (twin line 40) and is the only count used (grep PATHS).")
row("cards-L07-misconception-same-law", "2.7 cards (misconception coverage, L07)", f"{CARDS} SC1-c191; {L7} line 392", "PASS",
    "SC1-c191 back: P(M_H<=0)=2 Phi(0)-1 = 0 (Corollary 1.5(a), m=0) and P(B_H<=0)=Phi(0)=1/2, so the laws differ at 0; basis names Corollary 1.5(a), Remark 1.4 and Theorem 1.3 with A3, A4. Matches the misconception text.")
row("lab-L08-partA-printed-label", "2.5 lab output label (sequences vs pairs)", f"{TW8} Part A print lines (twin lines 88-94); {L8} expected block (page lines 344-347)", "PASS",
    "Round-4 FAIL fixed. The twin now prints 'step sequences of length 1 to 12: 8190' and '(sequence, level) pairs checked: 90114'; the expected block (line 345-347) and the page "
    "text match the twin output byte-for-byte (" + OUT + "check_embed_r5.out).")
row("rounding-rule-lab-printed-figures", "2.2 numbers (rounding rule stated for rounded lab figures; plan section 2.1 items 1 and 12)",
    f"{L7} Part B/C figures (lines 364-372, 376); {L8} Part A/C/D figures (lines 345-363, 364)", "FAIL",
    "Binding plan section 2.1 item 1 requires that a page showing a rounded figure states its rounding rule, and item 12 requires every probability and bias figure to "
    "state its rounding rule. The pages state rules for some figures (quiz 'to seven decimals'; L07 line 393 'rounded to four decimals'; L07 docstring 'printed to six "
    "decimals' for exact tails), but not for the 4-decimal simulated proportions, means, standard errors and z values of L07 Parts B and C (lines 376) and L08 Part C, "
    "nor for the 6-decimal exact probabilities of L08 Parts A and D (lines 350-351, 364). The printed digits are consistent with the unrounded values (recomputed in " + OUT + "recompute_r5.out), so this is a statement gap, not a numeric error. Raised for the first time in this round (not raised in rounds 2-4).",
    "Add one sentence to each lab's interpretation (L07 line 376; L08 line 364): 'Exact probabilities are printed to six decimals; simulated proportions, means and standard errors to four decimals, and z to two decimals; no further rounding is applied.' Keep the twin output unchanged.")
row("math-L07-cor-1.5a-H3-reading", "2.4 mathematics (Corollary 1.5(a), H3 reading)", f"{L7} lines 91, 103", "PASS",
    "Statement of Corollary 1.5(a) cites H3 (a>0) for m>=0; the proof applies Theorem 1.3 only at levels b>0 and handles m=0 by the limit b downarrow 0. The stated hypotheses are sufficient, so no omitted hypothesis. Read as in rounds 3-4.")

# ---- new independent-recomputation rows (this round) ----
row("recompute-walk-dp-L07-L08", "2.2 numbers (independent algorithm)", "ledgers/SC1/scripts/SC1-c-r5/recompute_r5.py", "PASS",
    "Dynamic programme over (position, running maximum) and over first-passage states, not the reflection or binomial formulas of the twins: 78 of 78 walk identities; "
    "1588, 8190, 90114, the first-passage counts, E[min(nu_1,N)] = 5.480560303, 11.815731233, 24.557203397 all reproduce (" + OUT + "recompute_r5.out).")
row("recompute-sim-L07-B-C-L08-C", "2.2 numbers (simulated figures, independent code)", "ledgers/SC1/scripts/SC1-c-r5/sim_checks_r5.py", "PASS",
    "Own implementation of the seeded draws: L07 nesting violations 0; counts 91, 107, 113, 121; L08 Part C sample means 5.2850, 11.3840, 23.1240, se 0.1868, 0.6288, 1.8497 "
    "and z -1.0466, -0.6866, -0.7748 against exact values from a fraction DP (" + OUT + "sim_checks_r5.out).")

fragment = {
    "unit": "SC1",
    "slice": "SC1-c",
    "round": 5,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-c (L07, L08 and lab twins), round 5; did not build SC1",
    "pin": "7376a5e216c1e6d99becc76b4cd64028f5b55d3f",
    "base": "9a02b1af9f92a060f7fabf7e1b3afb5ea95f45ba (round-4 pin; round-4 fragment /Users/billyribeiro/.fanout/frags/E-SC1-c.round4.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE5-SC1-c (detached at 7376a5e; .venv symlinked; vendor copied)",
    "scratch": "ledgers/SC1/scripts/SC1-c-r5/out/ (outputs of every command and script in this round)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice SC1-c: course/modules/SC/SC1/L07.html (52115 bytes), L08.html (49154 bytes), tests/labs/SC1/lab-SC1-L07-1.py and lab-SC1-L08-1.py, and the 49 L07/L08 cards of cards.json. Every line of both pages and both twins was read this round, and every card of L07 and L08 was read; no PASS row is carried from round 4 (each was re-verified).",
        "Delta since the round-4 pin 9a02b1af for the slice: L07.html (lines 59, 89, 116, 383, 604), L08.html (lines 51, 142, 143-363 twin block, 364, 505-511), lab-SC1-L08-1.py (docstring, Part A labels), cards.json (c147, c154, c170, c191, c192, new c201; L05 and L04 cards are outside this slice and were read only for cross-reference).",
        "Round-4 FAIL rows, all fixed and re-verified PASS: lab-L08-hypothesis-interpretation, math-L07-def-2.1-grid-times, key-results-L08, quiz-L07, cards-L07-L08-full-read, cards-basis-A3-dependence, notation-horizon-H, lab-L08-partA-printed-label.",
        "New FAIL rows this round: math-L07-prop-2.2-cor-2.3-remark-2.4 (Prop 2.2 H2 omits N' >= 1, which the proof uses and Definition 2.1 requires; the same omission is in card SC1-c144 and Problem P3); rounding-rule-lab-printed-figures (plan section 2.1 items 1 and 12; statement gap, not a numeric error). math-L07-R1-R3-P2-P3-M-E is FAIL only for Problem P3.",
        "Lab twins are demonstrations: mutation testing does not apply to them (architect ruling 9; plan section 2.2 item 11). No mutants are listed. Mutants are not required for a lesson-page slice.",
        "Not checked in this slice: index.html; L01-L06 content (other slices; read only for cross-references); the project, grader, rubric, project labs and cards of other lessons (run_graders, mutate_graders, check_projects, page_smoke for the project); render_curriculum.py, build_site.py --check, fetch_data.py --check; the full repository pytest and full ruff/mypy run (ruff and mypy were run on the two twins only); verify_refs live for the whole registry (only the SC1 entry, 1 of 560, was re-verified live).",
        "Plan deviation noted, not failed: the L08 lab's truncated mean is the simple-random-walk E[min(nu_1,N)] (exact) with a seeded walk sample, not the Brownian E[min(tau_a,n)] of plan section 3; the page labels it as a walk quantity (Remark 1.6, card SC1-c172), so the scope is correct.",
        "Card-level 'grade' is absent on some definition and misconception cards (c134, c136, c142, c151, c152, c154, c161, c166, c167, c178); BUILDER_RULES section 7 requires a grade only for graded key results, so noted, not failed.",
    ],
    "summary": {},
}
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
fragment["summary"] = {"rows": len(rows), "pass": counts["PASS"], "fail": counts["FAIL"], "unverifiable": counts["UNVERIFIABLE"], "mutants": 0, "mutants_killed": 0}
dest = ROOT / "ledgers/SC1/SC1-c.json"
dest.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", dest, fragment["summary"])
