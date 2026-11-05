"""Build ledgers/SC1/SC1-c.json (round 12) from the evidence rows below. Run with -I from the checkout root."""
import json
import sys

O = "ledgers/SC1/scripts/SC1-c-r12/out/"
S = "ledgers/SC1/scripts/SC1-c-r12/"
rows = []

def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

P = "PASS"
# ---- gates and runs
row("gate-check-pages", "2.9 structure (check_pages)", "course/modules/SC/SC1/L07.html, L08.html", P,
    f"`.venv/bin/python tools/check_pages.py --unit SC1` -> 'check_pages SC1: PASS', exit 0 ({O}check_pages.txt).")
row("gate-check-dag", "2.9 DAG (check_dag)", "course/modules/SC/SC1/L07.html, L08.html", P,
    f"`.venv/bin/python tools/check_dag.py --unit SC1` -> 'check_dag SC1: PASS', exit 0 ({O}check_dag.txt).")
row("gate-run-labs", "2.5 labs (run_labs)", "tests/labs/SC1/lab-SC1-L07-1.py, lab-SC1-L08-1.py", P,
    f"`.venv/bin/python tools/run_labs.py --unit SC1` -> 'run_labs SC1: PASS (11/11)', exit 0 ({O}run_labs.txt).")
row("lab-L07-twin-isolated", "2.5 labs (twin under python -I -W error)", "tests/labs/SC1/lab-SC1-L07-1.py", P,
    f"`python -I -W error lab-SC1-L07-1.py` run alone: exit 0, stderr 0 bytes, stdout saved ({O}lab_L07.stdout, {O}lab_L07.stderr).")
row("lab-L08-twin-isolated", "2.5 labs (twin under python -I -W error)", "tests/labs/SC1/lab-SC1-L08-1.py", P,
    f"`python -I -W error lab-SC1-L08-1.py` run alone: exit 0, stderr 0 bytes ({O}lab_L08.stdout, {O}lab_L08.stderr).")
row("lab-L07-page-equals-twin", "2.5 labs (embed: page code equals twin)", "course/modules/SC/SC1/L07.html:151-356 vs tests/labs/SC1/lab-SC1-L07-1.py", P,
    f"{S}page_twin_check.py: 'L07 page code equals twin: True' ({O}page_twin_check.txt).")
row("lab-L08-page-equals-twin", "2.5 labs (embed: page code equals twin)", "course/modules/SC/SC1/L08.html:143-343 vs tests/labs/SC1/lab-SC1-L08-1.py", P,
    f"{S}page_twin_check.py: 'L08 page code equals twin: True' ({O}page_twin_check.txt).")
row("lab-L07-expected-equals-output", "2.5 labs (expected block equals output)", "course/modules/SC/SC1/L07.html:357-379 (pre.expected)", P,
    f"{S}page_twin_check.py: 'L07 expected equals twin stdout: True' ({O}page_twin_check.txt).")
row("lab-L08-expected-equals-output", "2.5 labs (expected block equals output)", "course/modules/SC/SC1/L08.html:344-363 (pre.expected)", P,
    f"{S}page_twin_check.py: 'L08 expected equals twin stdout: True' ({O}page_twin_check.txt).")
row("lab-L07-printed-numbers", "2.2 numbers (a) lab-computed, recomputed independently", "course/modules/SC/SC1/L07.html:357-379 and :380", P,
    f"{S}indep_r12.py (DP and explicit-loop code, no lab helpers) reproduces every printed Part A/B/C/D figure: tails 0.375000, 0.332306 (21778/65536), identity 78 of 78; Part B counts 91,107,113,121 and SE 0.0210/0.0222/0.0225/0.0230; Part C means and SE; violations 0 ({O}indep_r12.txt).")
row("lab-L08-printed-numbers", "2.2 numbers (a) lab-computed, recomputed independently", "course/modules/SC/SC1/L08.html:344-363 and :364", P,
    f"{S}indep_r12.py: absorbing-DP truncated means 5.480560, 11.815731, 24.557203 (exact 179587/32768 for N=16); DP counts 1588/4096 and 794/4096; Part C mean/SE/z (-1.0466, -0.6866, -0.7748); Part D 0.3173105079 and density 0.2419707245 (H=1), 0.4795001222 and 0.1098478224 (H=2) ({O}indep_r12.txt).")
row("lab-L07-hypothesis-interpretation", "2.5 lab statements (hypothesis and interpretation match output)", "course/modules/SC/SC1/L07.html:150 (hypothesis) and :380 (interpretation)", P,
    "Hypothesis predicts decrease across five N (printed 0.375000..0.317547 decrease), nondecrease of level-1 counts (91,107,113,121), and cites 0.317311 (2(1-Phi(1)) rounded). Interpretation sentences ('78 of 78', '0.0898, 0.0498, 0.0348, 0.0148', '1.24 printed standard errors', 'Part D ... agree') match the printed output and indep_r12.txt. Rounding rule paragraph matches the format strings in the twin (.6f, .4f, .10f).")
row("lab-L08-hypothesis-interpretation", "2.5 lab statements (hypothesis and interpretation match output)", "course/modules/SC/SC1/L08.html:142 (hypothesis) and :364 (interpretation)", P,
    "Hypothesis lists the printed items (counts for n=12, a=3; P(nu_3<=12) and P(S_12>=3); truncated means for N=16,64,256; 1000 walks of length 256; Part D). Interpretation: 8190 sequences, 90114 pairs (sum n 2^n), 78 of 78, counts 512,0,384,0,288,0,224,0,180,0 sum 1588, z = -1.05,-0.69,-0.77 (computed z -1.0466,-0.6866,-0.7748), densities 0.241971 and 0.109848 all match output.")
row("lab-simulated-labels-seeds", "2.5 labs (seeds; SIMULATED labels)", "course/modules/SC/SC1/L07.html:148-149; L08.html:141-142; tests/labs/SC1/lab-SC1-L07-1.py:32; lab-SC1-L08-1.py:37", P,
    "L07 section title says 'Parts B and C SIMULATED' and the twin seeds random.Random(SEED) with SEED=20260507; L08 title says 'Part C SIMULATED' with SEED=20260508. Exact parts (A, D; L08 B) carry no SIMULATED label and use no randomness (twin module docstrings; grep of random use).")
row("lab-runtime", "2.5 labs (runtime under 10 s)", "tests/labs/SC1/lab-SC1-L07-1.py, lab-SC1-L08-1.py", P,
    f"Wall time of the twins under python -I -W error: 0.05 s (L07) and 0.10 s (L08) ({O}time_L07.txt, {O}time_L08.txt); page_smoke lab timings 0.1 s and 0.2 s ({O}page_smoke_L07_L08.txt).")
row("lint-mypy-twins", "code quality (ruff, mypy strict)", "tests/labs/SC1/lab-SC1-L07-1.py, lab-SC1-L08-1.py", P,
    f"ruff check tests/labs/SC1: 'All checks passed!'; ruff format --check: '11 files already formatted'; mypy --no-incremental on both twins: 'Success: no issues found in 2 source files' ({O}ruff.txt, {O}mypy.txt).")
row("page-smoke-L07-L08", "2.9 page_smoke (console, math, 360 px, labs in Pyodide)", "course/modules/SC/SC1/L07.html, L08.html", P,
    f"`.venv/bin/python tools/page_smoke.py --unit SC1 --pages L07 L08` run alone: 'page_smoke modules/SC/SC1/L07.html: PASS', 'L08.html: PASS', 'page_smoke SC1: PASS', exit 0 ({O}page_smoke_L07_L08.txt).")
row("pytest-lab-tools", "2.5 labs (pytest, tooling)", "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py", P,
    f"`.venv/bin/python -m pytest -q` on the three files: all tests passed, exit 0 ({O}pytest_lab_tools.txt).")
row("verify-refs-offline", "2.1 citations (integrity, offline)", "references/references.json", P,
    f"`.venv/bin/python tools/verify_refs.py --offline`: 'offline integrity: 560 entries, 0 problems', exit 0 ({O}verify_refs_offline.txt).")
row("verify-refs-live-SC1", "2.1 citations (live, unit SC1)", "references/references.json entry shreve2004stochastic", P,
    f"`.venv/bin/python tools/verify_refs.py --unit SC1` (live): 'live re-verification of SC1: 1 of 560 entries, 0 problems', exit 0 ({O}verify_refs_SC1_live.txt).")
row("refs-no-citation-markup", "2.1 attribution (no unread citation)", "course/modules/SC/SC1/L07.html:618 and L08.html references section", P,
    "Both references sections cite no passage or locator. The only key named is shreve2004stochastic; the registry record (references/references.json) has title 'Stochastic Calculus for Finance II', author Shreve, year 2004, used_by SC1, identical at the round-10 pin, and the page text matches that title. No theorem, page or equation number is attributed to it.")
row("claim-grades-L07", "2.3 grades (re-graded against BLUEPRINT section 3)", "course/modules/SC/SC1/L07.html (claims, key-results table)", P,
    "Theorem 1.3, Corollary 1.5(a)/(b), Proposition 2.2, Remark 2.4 and Corollary 2.3 graded T with proofs on the page (re-derived in rows math-L07-*). Lab-derived results (Part A count identity, Part B grid estimates, Part C mean) graded C naming Lab 1 and SIMULATED where generated. No B/C claim omits counter-evidence on this page.")
row("claim-grades-L08", "2.3 grades (re-graded against BLUEPRINT section 3)", "course/modules/SC/SC1/L08.html (claims, key-results table)", P,
    "Proposition 1.2, Corollaries 1.3, 1.4, 1.5 and Proposition 2.2, 2.3 graded T with proofs (re-derived). Lab Part A (90114 pairs, 78 of 78) and Part C (SIMULATED seeded walks) graded C naming Lab 1. Remark 1.6 says the mean is not evaluated, so no unsupported grade.")
# ---- mathematics
row("math-L07-thm-1.3", "2.4 mathematics (Theorem 1.3 and proof)", "course/modules/SC/SC1/L07.html:67-80", P,
    "Closed form 2(1-Phi(a/sqrt H)) = erfc(a/sqrt(2H)) re-derived (erfc(x)=2/sqrt(pi) int_x^inf e^-w^2; Phi(x)=erfc(-x/sqrt2)/2) and checked numerically at a=1,H=1: 0.3173105079 both ways ({O}indep_r12.txt). Proof chain checked against L06 Theorem 2.5 (L06.html:153-171, hypotheses continuous B, a>0, t>0, A3 and A4), L01 Definition 1.1 D2 (L01.html:58-64, s=0), no-atoms step, and L06 Corollary 2.6 (L06.html:174-181, hypotheses t>0, a>0 only).")
row("math-L07-cor-1.5b", "2.4 mathematics (Corollary 1.5(b))", "course/modules/SC/SC1/L07.html:87-108", P,
    "Integration by parts R(1-Phi(R))+phi(0)-phi(R) and bound R(1-Phi(R)) <= phi(R) checked (phi' = -u phi). Integral of (1-Phi) over [0,inf) = 1/sqrt(2 pi) = 0.398942 (numerical check in indep_r12 not separately printed; closed-form algebra re-derived). Substitution m = sqrt(H) u gives 2 sqrt(H)/sqrt(2 pi) = sqrt(2H/pi): checked at H=1 (0.797885 = sqrt(2/pi) to 6 d.p.). Assumption A5 stated (L07.html:96-99) and invoked in the statement.")
row("math-L07-prop-2.2-cor-2.3-remark-2.4", "2.4 mathematics (Prop 2.2, Cor 2.3, Remark 2.4)", "course/modules/SC/SC1/L07.html:119-146", P,
    "Prop 2.2(a): grid times are points of [0,H], so grid max <= running max, needs only continuity (H1). Prop 2.2(b): s_k=kH/N=(kc)H/N' for N'=cN, so the subset argument holds. Cor 2.3 inclusion and monotonicity re-derived. Remark 2.4: M^(1)_H=max(0,B_H), so P(M^(1)>=a)=P(B_H>=a)= half of P(M_H>=a) under H2 (factor 2 from L06 Theorem 2.5).")
row("math-L07-def-2.1-grid-times", "2.4 mathematics (notation and definition)", "course/modules/SC/SC1/L07.html:116", P,
    "Grid times s_k=kH/N, k=0..N and M^(N)_H=max_k B_{s_k}; the twin grid_maximum uses stride FINE//n over the fine path, the same grid (indep_r12.py uses walk[j] for j in range(0, FINE+1, FINE//g)).")
row("math-L07-remark-1.4-phi0", "2.4 mathematics (Remark 1.4)", "course/modules/SC/SC1/L07.html:83-86", P,
    "Limits 0 as H->0 and 1 as H->inf follow from the closed form (a/sqrt H -> inf, 0); Phi(0)=1/2 by evenness of the normal density; P(Z=0)=0 since the normal law has no atoms (re-derived).")
row("math-L07-R1-R3-P2-P3-M-E", "2.4 mathematics (problem solutions)", "course/modules/SC/SC1/L07.html:417-512", P,
    "All problems read in full: M1 (H=4,a=2 -> 2(1-Phi(1)) = 0.3173105079, erfc(2/sqrt8)=erfc(1/sqrt2)); M2; M3 (0.1586552539 vs 0.3173105079, half); P1 (Cor 1.5(a) proof, assumptions H1-H3 and A3/A4 listed; m=0 case OK); P2 (integral 1/sqrt(2pi)); P3 (nested events, H1 and divisibility stated); E1 (0.2275*400=91, 0.3025*400=121); E2 (binomials 8008,4368,1820,560,120,16,1 sum 14893; 6885; 21778/65536=0.332306 - recomputed); E3 (sqrt(33759/63840000)=0.022996 -> 0.0230); R1 (a<0 gives >1); R2 (no atoms); R3 (tau_a<=H = M_H>=a, limit 0). All re-derived; no error found.")
row("math-L08-prop-1.2-cor-1.3-1.4", "2.4 mathematics (Prop 1.2, Cor 1.3, Cor 1.4)", "course/modules/SC/SC1/L08.html:62-94", P,
    "Prop 1.2 both directions re-derived (closedness of {B=a}; IVT on [0,s*] with B_0=0<a<=B_{s*}); Cor 1.3 chain (Prop 1.2 needs no probability assumption; Theorem 1.3 L07; erfc form L06 Cor 2.6). Cor 1.4: union of increasing {tau<=n}, limit 2(1-Phi(0))=1 (continuity from below). Checked numerically: P(tau_1<=1)=0.3173105079, P(tau_1<=2)=0.4795001222 (indep_r12.txt).")
row("math-L08-cor-1.5", "2.4 mathematics (Corollary 1.5, density)", "course/modules/SC/SC1/L08.html:96-104", P,
    "F(H)=2(1-Phi(a H^-1/2)); F'(H)=-2 phi(.) * (-a/2 H^-3/2)= a H^-3/2 e^(-a^2/(2H))/sqrt(2 pi) re-derived; F(eps)->0 as eps->0 since a/sqrt(eps)->inf; FTC on (0,inf) gives F(H)=int_0^H f. Numerically: central difference equals closed form to 1e-8 (lab Part D printed True; indep dens 0.2419707245, 0.1098478224).")
row("math-L08-prop-2.2-2.3", "2.4 mathematics (Prop 2.2, 2.3)", "course/modules/SC/SC1/L08.html:120-138", P,
    "Prop 2.2: nu_a<=N iff max_{k<=N} S_k>=a (first-hit argument: S_{k*-1}<=a-1 and +-1 steps give S_{k*}=a); count identity via L06 Cor 1.4 (L06.html:87-94). Prop 2.3: min(nu,N)=sum_{k<N} 1{nu>k} re-derived; P(nu>k)=1-P(max_{j<=k} S_j>=a) integer over 2^k; k=0 gives 1. Numerically: E[min(nu_1,16)]=179587/32768 exact by DP (indep_r12.txt).")
row("math-L08-R3", "2.4 mathematics (Problem R3)", "course/modules/SC/SC1/L08.html:490-497 (R3)", P,
    "d/dH log f_a = (a^2 - 3H)/(2H^2); positive below a^2/3, negative above; mode H=a^2/3 correct (re-derived by hand).")
row("math-L08-R1-R2", "2.4 mathematics (Problems R1, R2)", "course/modules/SC/SC1/L08.html:476-489", P,
    "R1: #{nu<=N} = #{S_N>=a}+#{S_N>a} = 2#{S_N>=a} - #{S_N=a}; parity of S_12 even so #{S_12=3}=0; 2*794=1588 (indep_r12.txt). R2: min(nu,N+1)-min(nu,N)=1{nu>N} re-derived.")
row("prob-L08-all", "2.4 problems (all L08 problems, solutions)", "course/modules/SC/SC1/L08.html:392-497", P,
    "Every L08 problem read in full (M1-M3, P1-P3, E1-E3, R1-R3). M3 count 5/8 by listing (4 from +1 starts, (-1,+1,+1) from -1 start) and identity 4+1=5 re-verified; E1 odd counts sum to 1588 re-verified; E2 z-values and E3 density 0.1098478224 (rounded-factor product 0.109848) re-verified.")
row("prob-L07-remaining", "2.4 problems (other L07 problems)", "course/modules/SC/SC1/L07.html:411-512", P,
    "All L07 problems read in full and re-derived (see math-L07-R1-R3-P2-P3-M-E).")
row("misconceptions-L07-content", "2.4 misconceptions (content)", "course/modules/SC/SC1/L07.html:392-408", P,
    "Misconception 1: 0.3173105 vs 0.1586553 (7 d.p.) and 0.3173 vs 0.1587 (4 d.p.) checked; difference equals P(path reaches 1, ends below 1) (consistent with L06 Theorem 2.5). Misconception 2: printed grid estimates 0.2275 and 0.3025 both below 0.3173105. Misconception 3: B-tilde of L01 Section 4 (L01.html:211-235) discontinuous and same one-time laws.")
row("misconceptions-L08-content", "2.4 misconceptions (content)", "course/modules/SC/SC1/L08.html:379-391", P,
    "Misconception 1: P(tau<infty)=1 is probability, not an empty event (Cor 1.4 proof). Misconception 2: 0.317311 vs B_1 tail 0.1586552539 (Lesson 7); walk ratio 1588/794=2 exact. Misconception 3: finiteness does not bound a mean (Remark 1.6). No error found.")
row("canon-breaks-L07-L08", "2.4 canon breaks", "course/modules/SC/SC1/L07.html:383-390; course/modules/SC/SC1/L08.html:365-372", P,
    "L07 bullets: continuity (Lemma 2.1 L06), conditional closed form (A3 sketch only, A4 standard facts, L05 A3 at L05.html:271-289), grid tail one-step exactly half. L08 bullets: jump path 0 on [0,1/2), 2 after: M_1=2 and never equals 1, tau_1=infty; Cor 1.4 probability statement; finite does not mean integrable. Each example checked.")
row("key-results-L07", "2.4 key-results table", "course/modules/SC/SC1/L07.html:515-531", P,
    "Each row checked against its proof or lab output: E[M_H] row assumes A5 (matches Cor 1.5(b)); grid-maximum row correct (Prop 2.2(b)); lab numeric rows 0.332306 (C), 0.2275..0.3025 (C), 0.7586 and 0.0317 (C) match output.")
row("key-results-L08", "2.4 key-results table", "course/modules/SC/SC1/L08.html:499-517", P,
    "Rows match the proofs (Prop 1.2, Cor 1.3-1.5, Prop 2.2, 2.3) and the lab (90114 pairs; z-values within 1.1 SE below). Grades T for proofs, C for lab outputs with SIMULATED labels where generated.")
row("quiz-L07", "2.9 quiz (keys, tolerances, explanations)", "course/modules/SC/SC1/L07.html:535-614", P,
    "All 10 items checked: numeric keys 0.3173105 (tol 1e-6; true 0.31731051), 0.158655 (true 0.15865525, |diff| 2.5e-7 < 1e-6), 0.797885 (true 0.79788456, |diff| 4.4e-7 < 1e-6), 0.3173105 (M4 case); MC keys correct (factor 2, grid max <= running max, P(M<=0)=0, nested counts, a<0 formula > 1, single-step grid); explanations cite the right results.")
row("quiz-L08", "2.9 quiz (keys, tolerances, explanations)", "course/modules/SC/SC1/L08.html:518-597", P,
    "All 10 items checked: numeric 0.3173105 (tol 1e-6), 0.625 exact (5/8, tol 1e-9), 5.48056 (exact 179587/32768 = 5.4805603, tol 1e-5, |diff| 3e-7), 0.241971 (true 0.2419707, tol 1e-6); MC keys correct (hypothesis continuity, finite w.p.1, E[tau] not evaluated, parity, jump example). Explanations re-derived.")
row("structure-L07", "2.9 structure and prose (template sections)", "course/modules/SC/SC1/L07.html", P,
    f"check_pages PASS ({O}check_pages.txt); section order why-it-matters, s1 core, lab, s3 canon-breaks, s4 misconceptions, s5 problems (mechanics, proof, empirical, research), s6 key results, s7 quiz (10 items), s8 references; data-hours 9; no svg, img or data-files.")
row("structure-L08", "2.9 structure and prose (template sections)", "course/modules/SC/SC1/L08.html", P,
    f"check_pages PASS ({O}check_pages.txt); section order matches template; quiz 10 items; no svg, img or data-files; data-hours 9.")
row("banned-and-process-words", "2.9 banned phrases and process words", "course/modules/SC/SC1/L07.html, L08.html; tests/labs/SC1/lab-SC1-L07-1.py, lab-SC1-L08-1.py", P,
    "check_pages banned-string check PASS; manual grep for process words (build, builder, round, verifier, REQUESTS, unit report) in pages and twins: none. 'almost surely' used only as a stated scope limit.")
row("notation-macros", "2.4 notation (notation.json)", "course/modules/SC/SC1/L07.html, L08.html", P,
    f"{S}notation_scan.py: macros used are \\E, \\Prob, \\Phi, \\indic (registered); \\tau, \\nu, \\ast, \\min, \\log, \\sum not registered in notation.json (its macro list: \\E \\Prob \\Var \\Cov \\Corr \\R \\N \\indic \\Normal \\iid \\dto \\pto \\se ...). No registered symbol reused with another meaning ({O}notation_scan.txt).")
row("dag-defined-once-L07-L08", "2.9 DAG (defined once)", "course/modules/SC/SC1/L07.html:64, :116; course/modules/SC/SC1/L08.html:59", P,
    "dfn ids: def-running-maximum-distribution (L07:64, data-concept), plain dfn discretely monitored maximum (L07:116, no data-concept), def-first-passage-time (L08:59, data-concept). No term defined twice in L07/L08 (check_dag PASS).")
row("dag-outside-closure", "2.9 DAG (outside the prerequisite closure)", "course/modules/SC/SC1/L07.html:37, L08.html:37 and bodies", P,
    "check_dag PASS. Grep of both pages for SC2/SC3 terms (Itô, Girsanov, SDE, Ornstein, geometric Brownian motion, Feynman-Kac, Donsker, Gaussian process) and for martingale, stopping time, filtration, sigma: no hit, so no closure-outside concept is used by name. 'integrable' and 'moment' appear only as plain words (L08 canon-breaks, misconceptions) with no link.")
row("dag-reflection-link-L07-L08", "2.9 DAG and prose (concept link names the result the sentence cites)", "course/modules/SC/SC1/L07.html:37 and course/modules/SC/SC1/L08.html:3 (line 37)", P,
    "L07 'Uses' links L06.html#s2 (Theorem 2.5 of Lesson 6) and L08 'Uses' links the same anchor; the anchor s2 exists in L06.html (link-check of all hrefs and fragments: none missing).")
row("xref-L01-L05-L06", "2.1 cross references (Lessons 1, 5, 6)", "course/modules/SC/SC1/L07.html, L08.html; L01.html Def 1.1 (L01.html:58-64) and Section 4 (211-235); L05.html A3 (271-289), A4 (59-71); L06.html Cor 1.4 (87-94), Lemma 2.1 (105-115), Thm 2.5 (153-171), Cor 2.6 (174-181), tau_a definition (102)", P,
    "Every cross reference in L07/L08 re-read against the current text: Lesson 6 Cor 1.4 is the discrete tail identity; Lemma 2.1 gives {M_t>=a}={tau_a<=t} with continuous paths; Thm 2.5 is the reflection identity under A3, A4; Cor 2.6 is the erfc form with t>0, a>0 only; tau_a = inf{s>=0: B_s=a} is in L06 Section 2 (L06.html:102); L01 Def 1.1 (D1-D3) and Section 4 (B-tilde discontinuous); L05 A3 is stated for bounded stopping times with a sketch naming skipped steps; A4 is standard facts without proof.")
row("cards-dup-and-numbers", "2.7 cards (duplicates; numbers appear in lesson)", "course/modules/SC/SC1/cards.json (216 cards)", P,
    f"{S}dup_scan_r12.py over all 216 cards: no exact duplicate fronts; near-duplicate pairs (Jaccard >= 0.5) are distinct questions (e.g. SC1-c123 Thm 2.5 vs SC1-c139 Cor 1.5(a); SC1-c137 Thm 1.3 vs SC1-c205 Cor 1.3 on tau) ({O}dup_scan_r12.txt). Every L07/L08 card number appears in its lesson or its expected block.")
row("cards-L07-L08-full-read", "2.7 cards (full read of all L07 and L08 cards)", "course/modules/SC/SC1/cards.json (27 L07 cards, 23 L08 cards)", P,
    "All 27 L07 cards (SC1-c134 to c159 without c147, c151, c158; c191, c215, c229, c230) and all 23 L08 cards (SC1-c161, c162, c164, c165, c167 to c176, c178 to c183, c201, c205, c218) read in full against the current lessons and lab output; each card is PASS (see the cards rows).")
row("cards-c140-substitution", "2.7 cards / 2.4 mathematics (substitution in SC1-c140)", "course/modules/SC/SC1/cards.json SC1-c140 (back); course/modules/SC/SC1/L07.html:104-107", P,
    "Card c140 (changed since round 10): substitution m=sqrt(H) u gives 2 sqrt(H) int(1-Phi) du and 2 sqrt(H)/sqrt(2 pi) = sqrt(2H/pi), matching L07:107. Round-9 FAIL carried for this card is fixed (the card states the factor 2 sqrt(H) and the constant).")
row("cards-c150-gap", "2.2 numbers (card c150 gap in SE units)", "cards.json SC1-c150 (back); course/modules/SC/SC1/L07.html interpretation (:380)", P,
    "Card c150: mean 0.7586 with SE 0.0317 (matches output and indep_r12.txt: 0.7586, 0.0317). The 1.24-SE gap sentence moved to card c229, re-checked: 0.0393/0.0317 = 1.24 (unrounded 1.2398).")
row("num-L08-z-values", "2.2 numbers (z values and SE units)", "course/modules/SC/SC1/L08.html interpretation and E2; cards SC1-c173", P,
    "z printed -1.05, -0.69, -0.77 (recomputed -1.0466, -0.6866, -0.7748, indep_r12.txt); E2 '1.1 standard errors' bound and c173 'less than 1.1' consistent.")
row("num-L08-E3-factors", "2.2 numbers (rounded-factor product in E3 and M2)", "course/modules/SC/SC1/L08.html E3 and M2 solutions", P,
    "E3: 0.398942*0.353553*0.778801 = 0.1098477 -> 0.109848 (printed); unrounded 0.1098478224. M2: 0.398942*0.606531 = 0.2419707 -> 0.241971 (unrounded 0.2419707245). Both match the stated 'unrounded' values.")
row("num-rounding-0.3173105078", "2.2 numbers (rounding of the closed form)", "course/modules/SC/SC1/L07.html (interpretation, M1, quiz, misconceptions)", P,
    "2(1-Phi(1)) unrounded 0.3173105079 (0.31731050786); 2 x 0.1586552539 = 0.3173105078 on printed digits; 7-d.p. 0.3173105 and 0.1586553 (from 0.15865525393) all consistent with the statements.")
row("notation-T-first-passage-index", "2.4 notation (T and nu)", "course/modules/SC/SC1/L07.html:59; course/modules/SC/SC1/L08.html; notation/notation.json symbol T (module S1)", P,
    "T is not used as a horizon (the only bare T in math is the L07:59 remark that the unit reserves T for return observations, matching notation.json). Horizon is H throughout. nu_a is not in notation.json and collides with no registered symbol.")
row("notation-kappa-redefined", "2.4 notation (kappa)", "course/modules/SC/SC1/L07.html, L08.html", P,
    "grep 'kappa' in both pages: 0 hits. Nothing to redefine.")
row("notation-star-superscript-L08", "2.4 notation (superscript star in L08)", "course/modules/SC/SC1/L08.html (s^\\ast in Prop 1.2 proof; k^\\ast in Prop 2.2 proof)", P,
    "\\ast is used only as a local maximiser or first-index marker (s^\\ast, k^\\ast). notation.json registers R^\\ast and x^\\ast (AP1) and no generic \\ast; no R^\\ast use in SC1-L07/L08. No collision.")
row("notation-horizon-H", "2.4 notation (H is the horizon symbol)", "course/modules/SC/SC1/L07.html:59", P,
    "Horizon H used throughout L07 and L08, with the reason stated once (L07:59).")
row("notation-n-steps-L08", "2.4 notation (local convention, plan section 2.3)", "course/modules/SC/SC1/L08.html section 2 and lab; tests/labs/SC1/lab-SC1-L08-1.py", P,
    "Observation, not a fail: the plan (section 2.3) asks for N for a step count and n for a grid index, and L08 uses n as the walk length (Part A and the lab, e.g. 'n = 12'), with N in Props 2.2-2.3. notation.json has no conflicting meaning for n, so no notation.json row fails. Carried as an observation from earlier rounds.")
row("dag-simple-random-walk-defined-twice", "2.9 DAG (no second definition of a term)", "course/modules/SC/SC1/L07.html:150; course/modules/SC/SC1/L08.html:113", P,
    "'simple random walk' is defined in L06 (dfn at L06.html:56) and only referred to in L07 (lab hypothesis) and L08 (line 113) as 'the simple random walk of Lesson 6'. No second definition.")
row("dag-plain-bias-L08", "2.9 DAG (plain-English 'bias' in L08)", "course/modules/SC/SC1/L08.html:461", P,
    "The word 'bias' appears once in plain prose ('it cannot show a bias either way', E2 solution), with no link and no dfn; not a concept use (grep).")
row("prose-L08-same-events", "2.9 prose (events)", "course/modules/SC/SC1/L08.html:51, :63-70", P,
    "Why-it-matters and Prop 1.2 use the same events {tau_a<=H} and {M_H>=a} with the same meaning; re-read.")
row("prose-L08-first-passage-name", "2.9 prose (naming)", "course/modules/SC/SC1/L08.html:59, :116-121", P,
    "'first-passage time' (continuous, tau_a, Def 1.1) and 'first passage of the walk' (nu_a, Def 2.1) are distinct and named distinctly; Prop 2.2 title 'walk identity for first passage' is consistent with its statement.")
row("lab-L07-docstring-exact-fractions", "2.5 lab docstring vs code", "tests/labs/SC1/lab-SC1-L07-1.py:1-23 (module docstring) and :96, :125", P,
    "Docstring claims: Parts A and D use no randomness (no random call in part_a or part_d: checked in code); exact integer counts with math.comb for N=4..1024 (code line 96); composite Simpson on [1,13] with SIMPSON_INTERVALS=2000 (code line 192); sample divisor PATHS-1 (code line 125). All match.")
row("lab-L08-twin-docstring-PATHS", "2.5 lab docstring vs code", "tests/labs/SC1/lab-SC1-L08-1.py:1-28 (docstring) and :37-42 (constants)", P,
    "Docstring: Parts A, B, D without randomness (none in code), Part C with SIM_PATHS=1000 walks of SIM_STEPS=256 seeded by random.Random(SEED); D is erfc and density formula as in code lines 168-175. All match.")
row("lab-L08-partA-printed-label", "2.5 lab output label (sequences vs pairs)", "tests/labs/SC1/lab-SC1-L08-1.py:88-102; course/modules/SC/SC1/L08.html", P,
    "Label 'step sequences of length 1 to 12: 8190' equals sum_{n=1}^{12} 2^n (code variable 'distinct' is set for a==1, i.e. summed over n); label '(sequence, level) pairs checked: 90114' equals sum n 2^n. Labels correct.")
row("lab-L07-partA-label", "2.5 lab output label (identity)", "tests/labs/SC1/lab-SC1-L07-1.py:54, :74, :88; course/modules/SC/SC1/L07.html", P,
    "Label 'discrete tail identity of Lesson 6 (maximum >= a) = (endpoint >= a) + (endpoint > a)' matches the computed identity (code lines 231-235) and the page text.")
row("rounding-rule-lab-printed-figures", "2.2 numbers (rounding rule stated for rounded lab figures)", "course/modules/SC/SC1/L07.html (interpretation); course/modules/SC/SC1/L08.html (interpretation)", P,
    "Both interpretation paragraphs state a rounding rule matching the format strings in the twins (L07: .6f, .4f, .10f; L08: .6f, .4f, z .2f). Each difference computed from unrounded values (indep_r12 check).")
row("math-L07-cor-1.5a-H3-reading", "2.4 mathematics (Corollary 1.5(a), H3 reading)", "course/modules/SC/SC1/L07.html:91, :103", P,
    "Cor 1.5(a) hypotheses: H1 and H3 of Theorem 1.3 plus H2; the proof applies Theorem 1.3 only at levels b>m>=0, so b>0 (H3) holds at each level used. Re-derived.")
row("recompute-walk-dp-L07-L08", "2.2 numbers (independent algorithm)", "ledgers/SC1/scripts/SC1-c-r12/indep_r12.py", P,
    f"{S}indep_r12.py: DP over positions (absorbing for L08 first passage; running-max-capped DP for L07) reproduces 0.375000, 0.332306 (21778/65536), 78 of 78 identity pairs, 1588/4096, 794/4096, 5.480560, 11.815731, 24.557203 ({O}indep_r12.txt).")
row("recompute-sim-L07-B-C-L08-C", "2.2 numbers (simulated figures, independent code)", "ledgers/SC1/scripts/SC1-c-r12/indep_r12.py", P,
    f"Same seeds (20260507, 20260508), explicit loops: L07 counts 91,107,113,121; SE 0.0210,0.0222,0.0225,0.0230; means 0.5546,0.6639,0.7232,0.7586 with SE 0.0315-0.0317; L08 means 5.2850, 11.3840, 23.1240, SE 0.1868, 0.6288, 1.8497, z -1.0466/-0.6866/-0.7748 ({O}indep_r12.txt).")
row("remark-1.4-title-L07", "2.4 mathematics / 2.9 prose (title claim)", "course/modules/SC/SC1/L07.html:83-84", P,
    "Title 'limits in the horizon' matches the content (limits of P(M_H>=a) as H->0 and H->inf).")
row("term-walk-identity-L07", "2.4 notation/terms (term used before definition; attribution to Lesson 6)", "course/modules/SC/SC1/L07.html:150, :357, :380; tests/labs/SC1/lab-SC1-L07-1.py", P,
    "'Discrete tail identity of Lesson 6' is attributed to Corollary 1.4 of Lesson 6 (L06.html:87-94) wherever used; the hypothesis at L07:150 says 'Corollary 1.4' with the Lesson 6 attribution. No term used before its definition.")
row("term-walk-identity-L08", "2.4 terms (consistency of 'walk identity' within L08)", "course/modules/SC/SC1/L08.html:121 (Prop 2.2 title), :142, :364, :418", P,
    "'walk identity' in L08 means the first-passage/maximum count identity of Prop 2.2, which is the Lesson 6 identity specialised; the proof cites Corollary 1.4 of Lesson 6 for the count. Consistent.")
row("cards-no-A5-L05-lesson-scope", "2.7 cards (assumption labels cite the right lesson)", "cards.json SC1-c149, c150, c174, c215; c137, c139, c140", P,
    "Cards cite A3/A4 of Lesson 5 (the Lesson 5 assumptions), and A5 of Lesson 7 (c140, c215). Lab-only numbers cite Lab 1 of the correct lesson (c149/c150 in L07, c173/c174 in L08). No card mislabels an assumption's lesson.")
row("freshness-L07-L08", "2.1 freshness (2025-2026 work for a debate brief)", "course/modules/SC/SC1 (L07, L08)", P,
    "No debate key on SC1 (curriculum/03-markets.yaml:505-532 has none) and the pages cite no published work, so no 2025-2026 freshness item applies. No freshness_flags.")
row("cards-basis-A3-dependence", "2.7 cards (closed-form cards name the A3/A4 dependence)", "cards.json: SC1-c137, c139, c140, c145, c149, c150, c164, c165", P,
    "Each of these cards names the A3/A4 (or A5) dependence in its hypotheses or back; c149, c150 state the lab basis; c164 and c165 name A3 and A4 of Lesson 5 (checked in the full read).")
row("cards-c205-new", "2.7 cards (new card SC1-c205)", "cards.json SC1-c205 (L08); course/modules/SC/SC1/L08.html:81-84", P,
    "Card c205 states P(tau<=H)=P(M_H>=a)=2(1-Phi)=erfc with hypotheses H1, H2 of Prop 1.2 and A3, A4; matches Corollary 1.3 and its proof (which names Prop 1.2, Theorem 1.3 L07 and Cor 2.6 L06).")
row("cards-c215-A5-card", "2.7 cards (Lesson 7 Assumption A5 card)", "cards.json SC1-c215; course/modules/SC/SC1/L07.html:96-99", P,
    "Card c215 states A5 as E[X]=int P(X>m) dm for X>=0, value in [0,inf]; matches the page's Assumption A5 text exactly in substance.")
row("cards-c218-new", "2.7 cards (new L08 card SC1-c218)", "cards.json SC1-c218; course/modules/SC/SC1/L08.html:511 and :344-363", P,
    "Card c218 'All 78 pairs' matches the lab (78 pairs n<=12, a<=n; expected block line 'counts agree ... 78 of 78').")
row("cards-c151-removed-coverage", "2.7 cards (removal of SC1-c151 keeps coverage)", "cards.json (SC1-c151 absent)", P,
    "SC1-c151 is absent in the current file; its content (grid maximum property) is covered by SC1-c143 and c144 (Prop 2.2(a),(b)), and no lesson content is uncovered.")
row("cards-c150-c170-changed-text", "2.7 cards (changed backs: SC1-c150, SC1-c170)", "cards.json SC1-c150, SC1-c170", P,
    "c150 back: 0.7586, SE 0.0317 (matches output). c170 back: 'All 90114 pairs' (matches the lab's 90114 and n<=12, a<=n). Both re-verified against the current lesson and lab output.")
row("assume-A3-A4-additions", "2.4 scope/assumptions (round-9 'Assuming A3 and A4' phrasing additions)", "course/modules/SC/SC1/L07.html:443 (P1), :470 (E1); course/modules/SC/SC1/L07.html Lab 1 hypothesis (:150)", P,
    "Problems P1 and E1 and the Lab 1 interpretation carry 'assuming A3 and A4' where the closed form is used; the Remark 1.4 and Corollary 1.5 uses carry A3/A4 or A5 correctly.")
row("delta-round10-hunks", "1 inventory (delta 00a84795..5db69a9 for slice c)", "ledgers/SC1/scripts/SC1-c-r12/out/delta_slice_c_r12.txt", P,
    "git diff 00a84795..5db69a9: L07.html, L08.html and both twins byte-identical (no stat lines). cards.json changed: c140, c149, c150, c162, c165, c171, c201 (L07/L08) and new c229, c230 (L07), c220 to c228 belong to L02 to L05 (other slices), c229 and c230 are L07 (own row), c219 (L01) removed (L01). references.json changed only for other keys (shreve entry identical). curriculum.json changed for another unit. All changed slice-c subjects re-verified in rows above.")
row("cards-changed-r11-L07-L08", "2.7 cards (changed or new L07/L08 cards at 5db69a9)", "cards.json SC1-c149, c150, c162, c165, c171, c201, c229, c230", P,
    f"{S}cards_delta.py (round-10 vs current): changed L07 cards c140, c149, c150; changed L08 cards c162, c165, c171, c201; new L07 cards c229, c230. Each changed text re-checked against the current lesson and lab output (rows above and cards-L07-L08-full-read).")
row("cards-c229-c230-new", "2.7 cards / 2.2 numbers (new L07 cards)", "cards.json SC1-c229, SC1-c230; course/modules/SC/SC1/L07.html:357-380", P,
    "c229: gap 0.0393 is 1.24 SE (0.0393/0.0317 = 1.2398; unrounded 1.2398 in indep_r12) and 'does not separate discrete bias from sampling error' is supported by the one-seed sample. c230: 0 nesting violations (printed 0; recomputed 0 in indep_r12).")
row("delta-round9-carried-fail-fixed", "1 inventory (round-9 FAIL carried forward)", "ledgers/SC1 (round-9 fragment cards-c140-substitution)", P,
    "Round-9 FAIL on cards-c140-substitution is fixed at this pin (see the cards-c140-substitution row, re-checked).")
row("proof-L07-cor-1.5a-continuity-direction", "2.4 mathematics (continuity from below)", "course/modules/SC/SC1/L07.html:103", P,
    "The events {M_H>=b} increase as b decreases to m; their union over b>m is {M_H>m}; continuity from below applies. Re-derived.")
row("prob-L07-P1-continuity", "2.4 problems (P1 continuity step)", "course/modules/SC/SC1/L07.html:445", P,
    "Same argument as the page proof; the m=0 case handled. Re-derived.")
row("prob-L07-R2-continuity", "2.4 problems (R2 continuity step)", "course/modules/SC/SC1/L07.html:502", P,
    "{M_H>=b} increase as b decreases to a, union {M_H>a}; P(M_H=a)=0 by subtraction. Re-derived.")
row("scope-L07-assumption-phrase", "2.4 scope (assumption phrasing)", "course/modules/SC/SC1/L07.html:55, :68-82, :83-86, :91-92, :103, :134-", P,
    "Scope words ('every', 'all', 'any', 'for every real x', 'every grid') each attach to a computed or proved statement or a named hypothesis; simulated parts disclaimed (L07:380). Re-read.")
row("scope-L08-everything-after", "2.4 scope (assumption phrasing)", "course/modules/SC/SC1/L08.html:55, :63-81, :87-90, :97-106, :367-374", P,
    "'every continuous path' (Prop 1.2) and 'every step sequence' (Prop 2.2) are proved; 'finite with probability one' is a probability statement (Cor 1.4 remark). Re-read.")
row("math-L08-prop-2.3-denominator", "2.4 mathematics (Prop 2.3 denominator)", "course/modules/SC/SC1/L08.html:132", P,
    "P(nu>k)=1 - (integer)/2^k is an integer over 2^k for every k (k=0 gives 1 = 2^0/2^0). Re-derived.")
row("prob-L07-P1-assumptions", "2.4 problems (P1 assumptions)", "course/modules/SC/SC1/L07.html:443-445", P,
    "P1 lists H1, H2, H3 of Theorem 1.3 and states the level-wise use of H3. Matches the proof.")
row("cards-L07-misconception-same-law", "2.7 cards (misconception coverage, L07)", "cards.json SC1-c191; course/modules/SC/SC1/L07.html:397", P,
    "Card c191: P(M_H<=0)=0 and P(B_H<=0)=1/2 (Phi(0)=1/2); matches misconception 1 and Cor 1.5(a) with m=0.")
row("structure-why-it-matters-word-cap", "2.9 structure (why it matters: at most 120 words, BUILDER_RULES 4.2 item 1)", "course/modules/SC/SC1/L07.html:51; course/modules/SC/SC1/L08.html:51", P,
    "Word count of the why-it-matters paragraph (HTML stripped): L07 117 words, L08 117 words; both at most 120.")
row("delta-round8-hunks", "1 inventory (historic: round-8 to round-9 delta)", "ledgers/SC1/scripts/SC1-c-r12/out/delta_slice_c_r12.txt", P,
    "Historic inventory only. The hunks it named (Remark 1.4 wording, Corollary 1.5 assumption lists, Lab 1 hypothesis, card c149-c151 wording) are present at the current pin with the current text, re-read in this round; c151 is absent (see cards-c151-removed-coverage). No defect at this pin.")
row("defs-numbering-L08", "2.9 structure (numbering of definitions, propositions, corollaries)", "course/modules/SC/SC1/L08.html:58, :63, :77, :87, :97, :107, :116, :121", P,
    "Definition 1.1, Proposition 1.2, Corollary 1.3, 1.4, 1.5, Remark 1.6, Definition 2.1, Proposition 2.2, 2.3 numbered in order; references in text (e.g. 'Corollary 1.4 of Lesson 6', 'Proposition 2.3 of this lesson') resolve.")
row("scope-words-full-scan-r8", "2.4 scope (every, all, always, never, any, surely, exactly, only) full sentence scan", "course/modules/SC/SC1/L07.html, L08.html (prose, outside pre blocks)", P,
    "Re-scanned in this round with grep: 47 whole-file hits in L07 and 48 in L08 (code and expected blocks included); the prose hits were reviewed line by line. Each universal claim is a proved statement (per-path, per-sequence) or a disclaimed simulation/one-seed statement. No unsupported universal claim.")
row("terms-used-before-defined-L07-L08", "2.4 terms used before definition (full scan)", "course/modules/SC/SC1/L07.html, L08.html", P,
    "Only forward references are the 'discretely monitored maximum' (defined L07:116, used earlier with 'Definition 2.1 of this lesson' pointer at L07:51) and 'Proposition 2.3 of this lesson' (L08:51, pointer). Both are explicit forward pointers. 'integrable' and 'moment' are plain words.")
row("delta-round9-hunks", "1 inventory (delta 0dee921..c93dd52 for the slice)", "ledgers/SC1/scripts/SC1-c-r12/out/delta_slice_c_r12.txt", P,
    "Historic inventory. The round-9 hunks (L07, L08 wording; lab twins; cards) are present at this pin; the L07 and L08 twins are byte-identical since the round-10 pin, and the round-9 text is what the current rows re-verify.")
row("twin-docstring-identity-rename", "2.5 lab docstrings and print lines vs the expected block (rename)", "tests/labs/SC1/lab-SC1-L07-1.py:54, :74, :88; course/modules/SC/SC1/L07.html", P,
    "Docstring and print lines of L07 twin match the expected block line for line (page_twin_check.py: expected block equals twin stdout).")

# ---- new rows at this round
row("meta-description-L07-mean-hypothesis", "2.9 prose (learner-visible description states a result under fewer hypotheses than the proof uses)", "course/modules/SC/SC1/L07.html:7 (meta description)", "FAIL",
    "The meta description says 'P(M_H >= a) = 2(1 - Phi(a/sqrt H)) under Assumptions A3 and A4, its mean sqrt(2H/pi), ...'. The mean needs Assumption A5 as well (Corollary 1.5(b), L07.html:88-92; key-results row L07.html:524 and quiz item L07.html:577 both say 'assuming A5'). A reader of the description sees the mean stated under A3 and A4 only.",
    "In L07.html line 7, change 'under Assumptions A3 and A4, its mean' to 'under Assumptions A3 and A4, and its mean, under Assumption A5 as well,' (or 'and, for its mean, Assumption A5'), then re-run check_pages --unit SC1.")
row("grader-and-mutants-not-applicable", "2.6 projects (autograder, mutants)", "course/modules/SC/SC1/ (no grader for slice c)", P,
    "Slice c is lessons L07, L08 and their lab twins; it has no autograder. The project grader belongs to slice e. Lab twins are demonstrations and are not mutation-tested (FINAL-ARCHITECT-RULINGS 9; verifier ruling). No mutants are listed for slice c.")

fragment = {
    "unit": "SC1",
    "slice": "c",
    "round": 12,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-c (L07, L08, lab twins), round 12; did not build SC1",
    "pin": "5db69a9bee460736c318ebfacc7200ee5a6eb0f0 (detached, /Users/billyribeiro/.fanout/wt/verifyE12-SC1-c)",
    "base": "00a84795 (round-10 pin; round-10 fragment /Users/billyribeiro/.fanout/frags/E-SC1-c.round10.json). The round-11 fragment named in the task, E-SC1-c.round11.json, does not exist in /Users/billyribeiro/.fanout/frags; the latest slice-c fragment is round 10.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE12-SC1-c (detached at 5db69a9; .venv symlinked)",
    "scratch": "ledgers/SC1/scripts/SC1-c-r12/out/",
    "verified_at": "2026-11-05T12:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta since the round-10 pin: L07.html, L08.html and both lab twins are byte-identical. Cards changed for L07/L08 (c140, c149, c150, c162, c165, c171, c201) and new L07 cards c229, c230; all were re-verified from scratch. Every L07/L08 claim, number, cross-reference and card was re-read, not carried.",
        "Carried-forward rows: none. Every row has fresh evidence at this pin; the round-10 row ids are kept.",
        "Previous-round rule: the round-10 fragment is the base because the round-11 fragment named in the task is absent.",
        "Observation (not a fail): L08 uses n for the walk length where the plan (section 2.3) asks for N for steps; notation.json has no conflicting meaning. Carried from earlier rounds.",
        "Gates run at this pin: check_pages, check_dag, run_labs (11/11), ruff check and format, mypy --no-incremental on both twins, page_smoke for L07 and L08 alone (PASS), pytest on the three lab/page tool test files (exit 0), verify_refs --offline (560 entries, 0 problems), verify_refs --unit SC1 live (1 of 560, 0 problems).",
        "Could not check in this slice: render_curriculum, build_site, fetch_data, check_projects and run_graders (other slices); the full pytest suite (only the three lab and page tool files were run); lesson proofs of L01, L02, L04 and L05 beyond the statements L07 and L08 cite (other slices; the cited statements were re-read); the Pyodide runtime beyond page_smoke; the contents of Shreve (no access; no locator is cited, so none is checked); figures (none exist in L07 or L08).",
    ],
    "summary": {},
}
fragment["summary"] = {
    "rows": len(rows),
    "pass": sum(1 for r in rows if r["status"] == "PASS"),
    "fail": sum(1 for r in rows if r["status"] == "FAIL"),
    "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
    "mutants_killed": 0,
    "mutants": 0,
}
out = sys.argv[1]
json.dump(fragment, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("wrote", out, fragment["summary"])
