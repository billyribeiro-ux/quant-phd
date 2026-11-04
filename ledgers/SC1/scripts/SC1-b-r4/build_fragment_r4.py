"""Round 4 verifier: writes the SC1 slice b fragment ledgers/SC1/SC1-b.json from the checks run in this round.

Every PASS row cites the command, script or locator it was checked with this round. Outputs are under
ledgers/SC1/scripts/SC1-b-r4/out/. Run from the checkout root: python -I ledgers/SC1/scripts/SC1-b-r4/build_fragment_r4.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
VERIFIED_AT = "2026-11-04T00:00:00+00:00"  # date of this round; time not recorded
OUT = "ledgers/SC1/scripts/SC1-b-r4/out"
SC = "course/modules/SC/SC1"

P = "PASS"
rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> None:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        item["fix"] = fix
    rows.append(item)


# ---- gates and tooling (commands run this round on pin 9a02b1af) ----
row("b-check-pages", "2.9 structure (check_pages, banned strings, section order, minimum counts)",
    f"{SC}/L04.html, L05.html, L06.html", P,
    f"tools/check_pages.py --unit SC1 (this round): 'check_pages SC1: PASS', exit 0 ({OUT}/check_pages.txt).")
row("b-check-dag", "2.9 DAG (check_dag, closure, definitions once)",
    f"{SC}/L04.html, L05.html, L06.html", P,
    f"tools/check_dag.py --unit SC1 (this round): 'check_dag SC1: PASS', exit 0 ({OUT}/check_dag.txt). "
    "Chapman-Kolmogorov is the only 'Kolmogorov' string in L05 (grep), so no outside-closure concept name is used.")
row("b-run-labs", "2.5 labs (run_labs)", f"tests/labs/SC1/lab-SC1-L04-1.py, lab-SC1-L05-1.py, lab-SC1-L06-1.py", P,
    f"tools/run_labs.py --unit SC1 --page L04 / L05 / L06 (this round): each 'run_labs SC1: PASS (1/1)', exit 0 "
    f"({OUT}/run_labs_L04.txt, run_labs_L05.txt, run_labs_L06.txt).")
row("b-twin-match", "2.5 labs: page code equals twin; twin runs under python -I -W error; expected equals stdout",
    f"{SC}/L04.html (lab-SC1-L04-1), L05.html (lab-SC1-L05-1), L06.html (lab-SC1-L06-1)", P,
    "ledgers/SC1/scripts/SC1-b-r4/twin_match.py run as python -I -W error (this round): for all three labs "
    "code_equals_twin=True, exit 0, stderr empty, expected_equals_output=True, 'ALL MATCH' "
    f"({OUT}/twin_match.txt).")
row("b-lab-lint", "2.5 labs (ruff check, ruff format, mypy strict)",
    "tests/labs/SC1/lab-SC1-L04-1.py, lab-SC1-L05-1.py, lab-SC1-L06-1.py", P,
    f".venv/bin/ruff check: 'All checks passed!'; ruff format --check: '3 files already formatted'; "
    f"mypy --no-incremental on the three twins: 'Success: no issues found in 3 source files' ({OUT}/ruff_check.txt, ruff_format.txt, mypy.txt).")
row("b-page-smoke", "2.9 page_smoke (run alone on the three pages)", f"{SC}/L04.html, L05.html, L06.html", P,
    f"tools/page_smoke.py --unit SC1 --pages L04 L05 L06, run alone (this round): each page PASS, "
    f"'page_smoke SC1: PASS'; lab runtimes 0.1 s, 1.3 s, 0.0 s ({OUT}/page_smoke.txt).")
row("b-pytest-tooling", "2.5 tooling pytest (labs and page checks)",
    "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py", P,
    f".venv/bin/python -m pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py: 100% dots, exit 0 ({OUT}/pytest.txt).")
row("b-verify-refs", "2.1 citations (live re-verification of the unit's registry entries)",
    "registry key shreve2004stochastic, named in the References sections of L04, L05, L06", P,
    f"tools/verify_refs.py --unit SC1 (live, plain HTTP, this round): 'live re-verification of SC1: 1 of 560 entries, 0 problems', "
    f"exit 0 ({OUT}/verify_refs_unit_live.txt). Full registry offline: 'offline integrity: 560 entries, 0 problems' "
    f"({OUT}/verify_refs_registry_offline.txt). Record at references/references.json:20732-20744 (Open Library, title, author, year 2004).")
row("b-attribution-references", "2.1 attribution: no passage, locator or theorem number attributed to a source not read",
    f"{SC}/L04.html:468, L05.html:514, L06.html:536", P,
    "grep of L04-L06 for shreve, karatzas, billingsley, williams, data-cite, data-locator (this round): the only hit is the "
    "shreve2004stochastic key inside each References section, and each section says no claim is attributed to it. "
    "Shreve (2004) was not read, so no locator is claimed and none is needed. No registry flag.")

# ---- cross-references and numbers ----
row("b-cross-L04", "2.9 cross-references into L01 and L03",
    f"{SC}/L04.html:37, 65, 82, 126 (checked against L01.html:61-63 and L03.html:70, 89, 99-112)", P,
    "Anchors L01.html#def-brownian-motion and L03.html#def-quadratic-variation exist (grep of id=). L01.html:61-63 gives (D1) B_0=0, (D2) "
    "Normal(0,t-s), (D3) independent increments, as cited at L04:65 and L04:103. L03.html:70 is Assumption 3.2 with parts (a) and (b), cited at L04:65. "
    "L03.html:89 is Lemma 2.2 with E[X^4]=3 Delta^2 (cited for E[B_t^4]=3t^2 at L04:119 and M1 at L04:264). L03.html:99-112 is Theorem 2.3 with its Mean paragraph "
    "(E[(Delta B_k)^2]=Delta_k, telescoped to E[Q]=t), cited by the remark at L04:126. The L03 edits (H1, H2 wording at L03.html:101-102, 133) do not change any cited statement.")
row("b-cross-L05-L06", "2.9 cross-references into L01, L02, L08, M6 and between L05 and L06",
    f"{SC}/L05.html:52-67, 278, 287, 333; L06.html:127-128, 305", P,
    "L05:333 cites Proposition 1.2 and A1(c) of Lesson 1: L01.html:84 is Proposition 1.2 (covariance), L01.html:72-80 lists A1(c) as two "
    "covariance-zero coordinates of a multivariate normal vector are independent. L05:287 'Lesson 8 ... finiteness is a result there' is true: "
    "L08 Corollary 1.4 (P(tau_a<inf)=1 under A3, A4) and Corollary 1.5 (density). L05:278 'defined in Lesson 6, Section 2' is true: L06.html:102 "
    "(Section 2 opens at L06:100). L06:305 'Lesson 8 does' (state the law) is true: L08 Corollary 1.5. L05:52 and L06:127-128 use of A3 and A4(c),(g),(h) of Lesson 5 is true (L05:63-68). "
    "The L06:102 Lesson 2 hypothesis list is a separate FAIL row (b-hyp-L06-102-lesson2-hypotheses).",
    "")
row("b-num-L04", "2.2 numbers in L04 prose and Lab 1",
    f"{SC}/L04.html:224 (interpretation), 314 (E1), 321 (E2), 328 (E3), 452 (Q10), 420 (Q6)", P,
    f"ledgers/SC1/scripts/SC1-b-r4/recompute_numbers_r4.py ({OUT}/recompute_numbers_r4.txt): e^(1/4)=1.284025417, e^1=2.718281828, "
    "e^4=54.598150033, e^8=2980.957987; |2.718281828-e|=4.6e-10 and |54.598150033-e^4|=1.4e-10, both inside 1e-9.")
row("b-num-L05", "2.2 numbers in L05 prose, Lab 1 and problems",
    f"{SC}/L05.html:262, 303-305 (interpretation and misconception 3), 319-320 (M1), 326 (M2), 350 (P2), 357 (P3), 367 (E1), 374 (E2), 381 (E3), 498 (Q9)", P,
    f"recompute_numbers_r4.py ({OUT}/recompute_numbers_r4.txt): 225 cases; 5.55e-16/2.22e-16=2.500; 5.55e-16/3.81e-29=1.457e13; "
    "3.05e-16/2.22e-16=1.374; 1/(2 sqrt pi)=p_2(0,0)=0.2820947918; Phi(-1/sqrt2)=0.2397500611 (Q9 tolerance 1e-5 holds); "
    "E[(x+Z)^3]=x^3+6x for Z~N(0,2). Lab expected block shows 5.55e-16, 3.81e-29, 1.0000000000 (L05:254-261).")
row("b-num-L06", "2.2 numbers in L06 prose, Lab 1 and quiz",
    f"{SC}/L06.html:186, 296, 316, 320, 384-400 (E1-E3), 414, 511 (Q8), 479 (Q4)", P,
    f"recompute_numbers_r4.py ({OUT}/recompute_numbers_r4.txt): #{{M12>=3}}=1588 of 4096; #{{M12>=3,S12=2}}=495=#{{S12=4}}; "
    "P(M10>=2)=281/512, 2P(S10>2)=11/32, P(S10=2)=105/512=C(10,6)/1024; #{M3>=1}=5 of 8; #{M2>=2}=1 of 4; "
    "erfc(1/sqrt2)=0.3173105079, half=0.15865525393 (prints 0.1586552539 after rounding); counts 1014 triples and 78 pairs.")

# ---- lab twins (L04, L05, L06) ----
row("b-lab-L04-hypothesis", "2.5 labs: hypothesis claims match code", f"{SC}/L04.html:147 (hypothesis of Lab 1)", P,
    "L04:147 predicts relative 1e-9 for the integral of e^(theta sqrt(t) z) against phi, equal to e^(theta^2 t/2) (Lemma 2.1 with h=t), and absolute 1e-9 "
    "for E[Z_t]=1. The twin's TOL=1e-9 with a relative test for the first and an absolute test for the second (tests/labs/SC1/lab-SC1-L04-1.py:169, 173, 207-208).")
row("b-lab-L04-interpretation", "2.5 labs: interpretation matches printed output", f"{SC}/L04.html:224", P,
    "L04:224 values 2.718281828, 1.284025417, 54.598150033 are e^1, e^(1/4), e^4 (recompute_numbers_r4.txt); E[Z_t]=1.000000000 as in L04:217-223.")
row("b-lab-L04-docstring", "2.5 labs: twin docstring claims match code and output",
    "tests/labs/SC1/lab-SC1-L04-1.py lines 1-14 and 150-161 on the page", P,
    "Docstring says numerical, no randomness, no file read, three theta at t=2, and 'the lab does not compute the mass beyond LIMIT'; the code has "
    "LIMIT=12, THETAS=(-1,0.5,2), TIME=2 and no random or file calls (twin_match.py: code equals twin).")
row("b-lab-L05-docstring-quadrature", "2.5 labs: twin docstring and card describe the gaps as quadrature errors, but output and interpretation say rounding",
    "tests/labs/SC1/lab-SC1-L05-1.py:7-8 (docstring, shown on page L05.html:170-177); course/modules/SC/SC1/cards.json SC1-c091",
    P, "Docstring lines 176-177 say the gaps 'are at the scale of double-precision rounding, not exact values', matching the interpretation at L05:262 "
    "(5.55e-16 is 2.5 machine epsilons, computed) and card SC1-c091 back text.")
row("b-lab-L05-hypothesis-interpretation", "2.5 labs: L05 hypothesis and interpretation match output",
    "L05.html:169 (hypothesis), 262 (interpretation), 254-261 (expected block)", P,
    "L05:169 says 225 cases, s,t in {0.5,1,2}, x,y in {-1,-0.25,0,0.5,1}, tolerance 1e-6 and a tail mass far below the gap: the twin has TIMES=(0.5,1.0,2.0), "
    "POINTS=(-1,-0.25,0,0.5,1), TOLERANCE=1e-6 and prints 225 cases, 3.81e-29 tail, largest gap 5.55e-16 (expected block).")
row("b-lab-L06-claims", "2.5 labs: hypothesis and interpretation claims match output", f"{SC}/L06.html:186 (hypothesis), 297 (interpretation)", P,
    "L06:186 (N=1..12, Parts A-E as printed) and L06:297 (495 = 495 for N=12, a=3; 281/512, 11/32, 105/512; Part E numerical) match the code "
    "and expected block (L06:280-296, twin_match.py).")
row("b-lab-L06-docstring-exact-fraction", "2.5 labs: twin docstring says every probability is an exact fraction; Part E prints floating point",
    "tests/labs/SC1/lab-SC1-L06-1.py:4-5, 189-191 (docstring, shown on page at L06.html:189-191)", P,
    "Docstring: 'every probability in Parts A to D is an exact fraction; Part E evaluates a closed form in floating point'. Parts A-C print counts, "
    "Part D prints Fraction objects, Part E uses math.erfc (code lines 226-276).")

# ---- mathematics ----
row("b-math-L04-lemma-2.1", "2.4 mathematics: Lemma 2.1 (MGF of a normal, h>0)", f"{SC}/L04.html:80-90", P,
    "Re-derived L04:87-89: theta*y - y^2/(2h) = theta^2 h/2 - (y - theta h)^2/(2h) (expanding the right side gives the left). The shifted density integrates to 1. h>0 is stated in the lemma.")
row("b-math-L04-prop-2.2", "2.4 mathematics: Proposition 2.2 (B is a martingale)", f"{SC}/L04.html:92-106", P,
    "Re-derived L04:103-105: E[B_t^2]=t by (D2); B_t=B_s+Y; 4.2(a),(c) with B_s F_s-measurable; Y independent of F_s (Assumption 4.1), so 4.2(d) gives E[Y|F_s]=E[Y]=0 by (D2).")
row("b-math-L04-prop-2.3", "2.4 mathematics: Proposition 2.3 (B_t^2 - t is a martingale)", f"{SC}/L04.html:108-124", P,
    "Re-derived L04:119-123: E[B_t^4]=3t^2 (L03 Lemma 2.2, checked at L03.html:89-95); E[(B_t^2-t)^2]=3t^2-2t^2+t^2=2t^2; "
    "E[B_t^2|F_s]=B_s^2+h with h=t-s; so E[B_t^2-t|F_s]=B_s^2-s.")
row("b-math-L04-prop-2.4", "2.4 mathematics: Proposition 2.4 (exponential martingale, second moment)", f"{SC}/L04.html:128-143", P,
    "Re-derived L04:139-142: E[e^{2 theta B_t}]=e^{2 theta^2 t} by Lemma 2.1 with 2 theta; E[Z_t^2]=e^{-theta^2 t} e^{2 theta^2 t}=e^{theta^2 t}; "
    "Z_t=Z_s W, E[W^2]=e^{theta^2 h}, E[W]=1 by Lemma 2.1 with variance h. The case s=t is handled separately (L04:140).")
row("b-math-L04-A4.1-sketch", "2.4 mathematics and labelling: sketch of Assumption 4.1 (natural filtration)", f"{SC}/L04.html:63-66", P,
    "L04:65 is now titled 'Sketch, not a proof, for the natural filtration of B' and names both skipped steps (the pi-system of cylinder sets, and the pi-lambda extension). "
    "Its cited facts: (D1) for the sum-of-increments representation, (D3) for independence of [0,s] and [s,t] increments, and Lesson 3 Assumption 3.2(a) for single-variable functions (L03.html:70), all checked. The sketch's title restricts it to the natural filtration, which is the only filtration it treats.")
row("b-math-L04-misconception-1", "2.4 mathematics: misconception 1 (mean-zero process is a martingale)", f"{SC}/L04.html:240", P,
    "Re-derived L04:241: (B_s+Y)^3=B_s^3+3B_s^2Y+3B_sY^2+Y^3; conditional mean B_s^3+3(t-s)B_s, which differs from B_s^3 for s<t exactly when B_s is nonzero.")
row("b-math-L04-R1-R3", "2.4 mathematics: research problems R1-R3 (solutions)", f"{SC}/L04.html:336-355", P,
    "R1 (L04:339): h(t)=t-g(t) constant forces g(t)=t+c. R2 (L04:346): Z_s e^{c^2h/2}=Z_s forces c^2h=0, so c=0 for h>0, with Z_s>0. R3 (L04:353): conditional variance t-s, a constant.")
row("b-prose-L04-R2-title", "2.9 prose: problem R2 title", f"{SC}/L04.html:343-346", P,
    "Title 'When the exponential exp(cB_t) is a martingale' matches the solution at L04:346 (c=0 only).")
row("b-prose-L04-remark-numbering", "2.9 prose: cross-references to remarks and propositions", f"{SC}/L04.html:37, 126", P,
    "L04:126 is an unnumbered 'Remark (the link with Lesson 3)' after Proposition 2.3, and L04:37 refers to it as 'the remark after Proposition 2.3'.")
row("b-scope-L04-footer", "2.9 scope words: footer claims", f"{SC}/L04.html:479 (footer)", P,
    "Footer: Propositions 2.2 to 2.4 are proved from Assumptions 4.1 and 4.2, stated and not proved; Lab 1 is labelled numerical. Matches L04:55-70, 129-143 and L04:147.")
row("b-math-L05-lemma-1.3", "2.4 mathematics: Lemma 1.3 (future increment independent of the past), for 0 <= s <= t",
    f"{SC}/L05.html:87-101", P,
    "Re-read L05:99-100. s=t: B_t-B_s=0 is constant. s=0: F_0 generated by the constant B_0=0. 0<s<t: (D3) applied to 0=r_0<...<r_k=s<t gives mutual "
    "independence of Delta_1..Delta_{k+1}; B_{r_j} is a sum of Delta_1..Delta_j; A4(f) groups; the pi-system of cylinder events generates F_s; A4(a) extends.")
row("b-math-degenerate-L04-lemma-2.1", "2.4 mathematics: Lemma 2.1 hypothesis h > 0 versus its use in Proposition 2.4 for 0 <= s <= t",
    f"{SC}/L04.html:82 (hypothesis), 140-142 (proof of Proposition 2.4)", P,
    "L04:140 now reads 'Let 0 <= s < t, Y = B_t - B_s and h = t - s > 0' and treats s=t separately (Z_t is F_t-measurable), so Lemma 2.1 with h>0 is applied only where h>0.")
row("b-math-L05-thm-1.4", "2.4 mathematics: Theorem 1.4 (Markov property at fixed times)", f"{SC}/L05.html:103-122", P,
    "Re-derived L05:119-120: psi(x)=int g(y) p_{t-s}(x,y) dy; A4(b) with Z=B_s, Y=B_t-B_s, f(z,y)=g(z+y) gives fbar(z)=E[g(z+B_t-B_s)]; "
    "the substitution y=z+w gives phi_u(y-z)=p_u(z,y) (L05:120). f is bounded and jointly measurable.")
row("b-math-L05-lemma-2.2-thm-2.1", "2.4 mathematics: Lemma 2.2 (completing the square) and Theorem 2.1 (Chapman-Kolmogorov)",
    f"{SC}/L05.html:133-165", P,
    "Re-derived Lemma 2.2 (L05:141): uv times both sides gives v(z-x)^2+u(y-z)^2 and (u+v)z^2-2(vx+uy)z+...; the constant identity reduces to "
    "(u+v)(vx^2+uy^2)-(vx+uy)^2=uv(y-x)^2. Theorem 2.1 (L05:155-164): c=(u+v)/(uv), A4(e) gives (2pi/c)^(1/2), prefactor (2pi)^(-1/2) and the uv powers cancel.")
row("b-math-L05-A3-sketch", "2.4 mathematics and labelling: sketch of A3 names every skipped step", f"{SC}/L05.html:280", P,
    "L05:280 names (i) extension of independence from finitely many increments to the path via A4(a), and (ii) the limit passage in E[f(X^(n)) 1_A] (A in F_rho). "
    "Dyadic approximation bounds from R3 (L05:405); stopping property of rho_n; continuity gives pointwise convergence (cited correctly).")
row("b-math-L05-R3", "2.4 mathematics: research problem R3 (dyadic approximation) with rho <= c", f"{SC}/L05.html:403-405", P,
    "L05:405: x <= ceil(x) < x+1 gives rho <= rho_n < rho+2^(-n); {rho_n<=r}={rho<=floor(2^n r)/2^n} lies in F_r (checked: rho_n<=r iff ceil(2^n rho)<=floor(2^n r)).")
row("b-math-L05-problems", "2.4 mathematics: problem set M1-M3, P1-P3, E1-E3, R1-R2 (worked solutions)", f"{SC}/L05.html:314-420", P,
    "Re-derived M1 (1/(2 sqrt pi) at both values), M2 (x^2+2 and x^3+6x for Z~N(0,2)), M3 (Cov=0, A1(c) of L01), P1 (u=1,v=3,x=0,y=1: both sides (4z^2-2z+1)/3), "
    "P2 (Phi((c-x)/sqrt(t-s)) from Theorem 1.4 with g=indicator), P3 (substitution gives 1), R1 (paths and A4(d) argument), R2 (A3 at a deterministic time). "
    "Mathematics PASS. The P3 title defect is tracked separately in b-prose-L05-P3-title (FAIL).")
row("b-math-L05-misconceptions", "2.4 mathematics: misconceptions 1-3", f"{SC}/L05.html:296-305", P,
    "L05:297 by P2: N(B_s,t-s), mean B_s, so not independent of the past. L05:301: p_{t-s}(x,.) equals p_t(0,.) iff x=0 and s=0 (Normal(x,t-s)=Normal(0,t) forces x=0 and t-s=t). "
    "L05:305: 225-point gap 5.55e-16 matches the lab expected block.")
row("b-scope-L05-D1D3", "2.9 scope words: which facts Sections 1 and 2 use", f"{SC}/L05.html:56", P,
    "L05:56 lists (D1)-(D3), A4(a), A4(b), A4(e), A4(f). Lemma 1.3 uses D1, D3, A4(a), A4(f); Theorem 1.4 uses A4(b); Lemma 2.2 and Theorem 2.1 use A4(e). Checked by reading the proofs at L05:97-101, 117-121 and 139-165.")
row("b-notation-L05-Phi-varphi", "3 notation: registered symbol Phi keeps its meaning; no other registered symbol misused",
    f"{SC}/L05.html:348, 350, 498; notation/notation.json (symbols, \\Phi)", P,
    f"notation_scan.py ({OUT}/notation_scan.txt): the 4 uses of \\Phi in L04-L06 are the standard normal CDF (P2 and Q9); registered symbols T, \\gamma_3, \\gamma_4, R^\\ast, R^{{e\\ast}}, R_f, \\mathbb{{Q}} do not appear in L04-L06 math (scan).")
row("b-notation-L05-X-n", "3 notation: local symbols defined before use", f"{SC}/L05.html:274, 279-280", P,
    "X_r and X^(n) are defined at L05:274-280 before their use; no registered macro or symbol uses X (notation_scan.txt).")
row("b-notation-M-clash", "3 notation: M_t meaning is not reused across the unit's lessons",
    f"{SC}/L04.html:75-147, L05.html (no M), L06.html:52, 56, 102, 107-114", P,
    "M_N (walk, L06:56) and M_t (Brownian, L06:52, L06:107) are both running maxima of two different processes, defined where used. No registered symbol M exists in notation.json.")
row("b-quiz-L05-Q7", "2.9 quiz item: sketch skipped step", f"{SC}/L05.html:478-484", P,
    "Q7 correct option names the extension of independence and the limit passage, the two steps named at L05:280; explanation at L05:484 matches.")
row("b-scope-L05-canonical", "2.4 mathematics: canonical-space choice in R1", f"{SC}/L05.html:389", P,
    "L05:389 states the path space is chosen for this problem only, and A4(d) is applied to paths on that space.")
row("b-term-almost-surely", "5 terms used before definition: almost surely", f"{SC}/L05.html:62 (first use), L05.html:75, L06.html:144", P,
    "'almost surely' first appears in A4(b) at L05:62 with 'that is, with probability one'; later uses are consistent. "
    "'stopping time' first appears in A4(c) at L05:63 before its definition in §3 at L05:267; it is an M6 concept listed in L05's Uses line (L05:38), so no FAIL.")
row("b-scope-L05-E1-tail", "2.2 numbers and 2.9 scope: the mass-beyond-truncation sentence", f"{SC}/L05.html:365-367 (E1)", P,
    "L05:367 restricts the comparison to 12<=|z|<=40 and says the mass for |z|>40 is not computed. Printed 5.55e-16/3.81e-29 = 1.457e13 (recompute_numbers_r4.txt).")
row("b-math-L06-facts-unnumbered", "2.4 mathematics: every fact used in Proposition 2.3 is proved or a numbered assumption; terms defined before use",
    f"{SC}/L06.html:102 (defs), 135-144 (Prop 2.3 proof)", P,
    "A4(h) (L05:68) gives X_rho and rho F_rho-measurable for rho<=c; L06:102 defines F_t and F_rho; L06:135 computes {rho<=r}={tau_a<=r} in F_r; "
    "A4(c) (L05:63) makes tau_a a stopping time; A4(g) (L05:67) gives joint measurability. Every fact used is proved on the page or stated as A3, A4(b), A4(c), A4(g), A4(h). The L06:102 hypothesis omission is a separate row.")
row("b-math-L06-prop-1.3-cor-1.4", "2.4 mathematics: Proposition 1.3 (discrete reflection) and Corollary 1.4 (tail identity)", f"{SC}/L06.html:76-98", P,
    "Re-derived L06:82-83 (bijection through Lemma 1.2; {kappa<=N, S_N=2a-b} equals {S_N=2a-b} because S_0=0<a<2a-b). Cor 1.4 (L06:97): sum over b<a of #{S_N=2a-b} = #{S_N>a}.")
row("b-math-L06-lemma-2.1", "2.4 mathematics: Lemma 2.1 (running maximum and first visit; B continuous)", f"{SC}/L06.html:104-115", P,
    "Re-derived L06:112-114: IVT on [0,t]; {s: B_s=a} closed so B_{tau_a}=a; (iii) t<tau_a gives B_t != a and B_s<=a, so B_t<a. P2 solution (L06:369) gives the same for (ii) and (iii).")
row("b-math-L06-prop-2.3-thm-2.5", "2.4 mathematics: Proposition 2.3 and Theorem 2.5 logic", f"{SC}/L06.html:122-171", P,
    "Re-derived L06:136-144: rho=tau_a^t bounded stopping time (A4(c)); W_t=B_rho-X_{t-rho}; freezing with Z=(B_rho,t-rho), Y=X (A4(b)); h_- = h_+ by symmetry of N(0,u). "
    "Theorem 2.5 (L06:167-170): E={tau_a<=t, B_t<a}={W_t>a}; P(W_t>a)=P(B_t>a); P(B_t=a)=0 by the normal density.")
row("b-math-L06-cor-2.6", "2.4 mathematics: Corollary 2.6 (closed form of the tail)", f"{SC}/L06.html:173-182", P,
    "Re-derived L06:181: z=sqrt2 w; lower limit a/sqrt(2t); prefactor sqrt2/sqrt(2 pi)=1/sqrt(pi); erfc definition gives one half erfc. Numerically 2P(B_1>1)=erfc(1/sqrt2)=0.3173105079 (recompute_numbers_r4.txt).")
row("b-math-L06-R1-R3", "2.4 mathematics: research problems R1-R3 (solutions)", f"{SC}/L06.html:406-426", P,
    "R1 (L06:410): parity of S_N; both sides vanish when b and N have different parity. R2 (L06:417): Theorem 2.5 applied to -B gives 2 P(B_t<-a). R3 (L06:424): 2x>x for x>0.")
row("b-math-L06-E1-E3", "2.4 mathematics and numbers: empirical problems E1-E3", f"{SC}/L06.html:384-400", P,
    "E1: 1+...+12=78 (L06:386). E2: 281/512 - 11/32 = 105/512 = 210/1024 (L06:393). E3: half of 0.3173105079 is 0.15865525393, as stated (L06:400).")
row("b-scope-L06-only-events", "2.9 scope words: what Section 2 needs of the path", f"{SC}/L06.html:102", P,
    "L06:102 'need the path only on [0,t]': the events of Lemma 2.1 and Theorem 2.5 and the random time rho=tau_a^t use the path on [0,t] only (proofs at L06:112-114, 135-144).")
row("b-scope-L06-N12-every-case", "2.2 and 2.9 scope words: every case with N <= 12", f"{SC}/L06.html:186, 194, 296, 441", P,
    "L06:186, 195, 297 scope (N<=12, 1<=a<=N, b>=-N) match the enumeration domain in the twin: range(1,13), range(1,n+1), range(-n,a) (L06 lab code lines 230-235).")
row("b-rounding-L06-misconception", "2.2 numbers: misconception 1 values and rounding", f"{SC}/L06.html:316", P,
    "L06:316 P(M_1>=1)=0.3173 and P(B_1>=1)=0.1587 at four decimals (recompute: 0.3173105079 and 0.1586552539); Part E prints ten decimals as stated (L06:295-296).")
row("b-plan-L06-pathlevel", "plan coverage: L06 must state the path-level reflection principle, assuming A3 (plans/SC1-build-plan.md section 3, L06)",
    f"{SC}/L06.html:119 (Definition 2.2), 149 (Remark 2.4); plans/SC1-open-items.md:3-8", P,
    "Recorded deviation, not a silent one: plans/SC1-open-items.md:3-8 records 'L06: path-level reflection principle not proved'. L06:119 and L06:149 "
    "state that the path-level statement is not proved. Stale wording to note: the open-items entry (line 6) says the claim is 'labelled as a conjecture', which L06:119 no longer uses.")
row("b-causal-L06-symmetry-last-step", "2.9 prose: causal and location claims about where the symmetry is used",
    f"{SC}/L06.html:306 (canon break), quiz Q10 at L06:523-529", P,
    "L06:306 locates the factor 2 in the two equal-probability events of Theorem 2.5 and the symmetry at h_- = h_+ in Proposition 2.3; Q10 explanation at L06:529 matches the proof at L06:142-144.")
row("b-quiz-L04-Q8-explain", "2.9 quiz explanation: Q8 (is B_t + t a martingale)", f"{SC}/L04.html:432-438", P,
    "L04:438 explanation: E[X_t|F_s]=B_s+t, which differs from X_s=B_s+s when s<t (matches P1 at L04:289).")
row("b-quiz-L04-L06", "2.9 retrieval quiz: item count, answers and explanations", f"{SC}/L04.html:376-464, L05.html:427-510, L06.html:449-532", P,
    "Item counts: L04 11, L05 10, L06 10 (8-15 rule). Every item has an explain block. Numeric answers: L04 Q3 3, Q4 27, Q6 2.718281828 (tolerance 1e-9, |e-2.718281828|=4.6e-10), "
    "Q10 54.598150033 (tolerance 1e-9, diff 1.4e-10); L05 Q2 3 (tolerance 1e-4), Q4 0.3989 (|0.398942-0.3989|=4.2e-5), Q9 0.23975 (tolerance 1e-5, diff 6.1e-8); "
    "L06 Q2 0.25, Q4 0.3173 (diff 1.1e-5), Q8 0.1587 (diff 4.5e-5). All within stated tolerance (recompute_numbers_r4.txt).")
row("b-plan-coverage-L04-L05", "plan coverage: L04 and L05 mandatory content (plans/SC1-build-plan.md section 3)", f"{SC}/L04.html, L05.html", P,
    "Plan section 3 (plans/SC1-build-plan.md lines 234-282) read for L04-L06: L04 has the filtration, martingale definition restated, B_t and B_t^2-t, the exponential martingale with derivations, "
    "and no optional stopping; L05 has the Markov property, Gaussian transition density, Chapman-Kolmogorov (derived), and A3 stated with a sketch naming its skipped step; L06 covers the reflection principle as a recorded deviation (b-plan-L06-pathlevel), the M_t tail, and the discrete identity.")
row("b-hours-L04-L06", "2.9 hours: declared study hours and split", f"{SC}/L04.html:2, L05.html:2, L06.html:2; {SC}/index.html:29", P,
    "data-hours=9 on L04, L05, L06 (grep); index.html data-hours-lessons=72 and data-hours-project=28 (grep); 8 x 9 = 72 and 72 + 28 = 100.")
row("b-dag-D1-D9", "2.9 DAG: plan section 4 concepts D1-D9 and NOT IN CURRICULUM terms used without links",
    f"{SC}/L04.html, L05.html, L06.html (full text grep)", P,
    "grep (this round) of L04-L06 for Ito, Itô, geometric Brownian, Ornstein, SDE, Euler, Milstein, Girsanov, Feynman, Donsker: 0 hits each. "
    "'Kolmogorov' occurs in L05 only inside 'Chapman-Kolmogorov'. check_dag.py PASS (check_dag.txt).")
row("b-process-words", "2.9 learner text: no process words", f"{SC}/L04.html, L05.html, L06.html, and the three twins", P,
    "grep (this round) of the text of L04-L06 for builder, verifier, fixer, architect, planner, plan, round N, open item, TODO, TBD, lorem: 0 hits.")

# ---- retrieval cards (cards.json, re-read this round) ----
row("b-cards-c061-c072", "2.7 retrieval cards (sampled and read): SC1-c061 to SC1-c072 against the L04 text",
    f"{SC}/cards.json (ids SC1-c061 to SC1-c072)", P,
    "All 12 cards read in full and checked against L04 text and numbers: c066 (Lemma 2.1), c068 (E[B_t^4]=3t^2, Lemma 2.2 of L03), c070 (E[W]=1), c072 (lab numbers 54.598150033, 1.000000000). "
    "cards_scan_r4.py: fronts unique; cited Problem/Proposition numbers present in L04.")
row("b-cards-c073-c085", "2.7 retrieval cards: SC1-c073 to SC1-c085 against the L04 and L05 text",
    f"{SC}/cards.json (ids SC1-c073 to SC1-c085)", P,
    "All 13 cards read: c073 (P1), c074 (Section 3), c076 (misconception 1), c079 (R1), c080 (R2), c081 (P2), c082 (P3); c085 lists A4(a) to A4(h) in the same order as L05:61-68. Cards cite L04 and L05 text as stated.")
row("b-cards-c086-c097", "2.7 retrieval cards: SC1-c086 to SC1-c097 against the L05 text",
    f"{SC}/cards.json:767-770 (SC1-c091), and cards c086-c097 generally", P,
    "Read in full. c091 back now reads 'gaps are at the scale of double-precision rounding ... not exact values' (matches L05:262, 5.55e-16 = 2.5 epsilon, recomputed). c093 states the A3 conclusion and 'assumed, not proved'. c095 (R2), c096 (R3), c097 (R1) match the solutions.")
row("b-cards-c098-c110", "2.7 retrieval cards: SC1-c098 to SC1-c110 against the L05 and L06 text",
    f"{SC}/cards.json (ids SC1-c098 to SC1-c110)", P,
    "Read in full. c098 (B-tilde, L05:286), c099 (unbounded tau, L05:287), c100-c102 (misconceptions, L05:297-305), c102 now names 'assuming Lemma 2.2 and A4(e)' (matches L05:146), c103 (M2 with Z~N(0,2)), c104 (P2 with Phi), c105 (M3, A1(c) of L01).")
row("b-cards-c111-c122", "2.7 retrieval cards: SC1-c111 to SC1-c122 against the L06 text and Lab 1 output",
    f"{SC}/cards.json (ids SC1-c111 to SC1-c122)", P,
    "Read in full. c111 (1014 triples, all equal, run_labs output), c112 (78 pairs), c113 (281/512, 11/32, 105/512), c114 (495 and 495, 2a-b=6-2=4), c115 (erfc(1/sqrt2)=0.3173), c116-c118 (Lemma 2.1), c119-c122 (Definition 2.2, Proposition 2.3). All match L06 and the lab output.")
row("b-cards-c123-c133", "2.7 retrieval cards: SC1-c123 to SC1-c133 against the L06 text",
    f"{SC}/cards.json (ids SC1-c123 to SC1-c133)", P,
    "Read in full. c123 (Theorem 2.5), c124 (Corollary 2.6), c125 (jump example, L06:304), c126 (0.3173 vs 0.1587), c127 (105/512), c128 (continuity and A3), c129 (5 of 8), c130 (parity), c131 (2P(B_t<-a)), c132 (strict inequality), c133 (A3 with c=t). All match.")
row("b-cards-duplicates", "2.7 retrieval cards: full scan for duplicates and coverage",
    f"{SC}/cards.json (all 187 cards)", P,
    f"cards_scan_r4.py ({OUT}/cards_scan_r4.txt): 187 cards, 187 unique ids, no duplicate fronts, no duplicate backs; 74 cards tagged L04 (22), L05 (24), L06 (28). "
    "cards_delta.py vs the round-3 pin (out/cards_delta.txt): changed in this slice SC1-c091, c102, c103, c104; SC1-c189 unchanged; c190 removed and c191-c192 added (L07/L08, outside this slice).")
row("b-math-L05-def-1.1-st-case", "2.4 mathematics: Definition 1.1 (Markov property for all 0<=s<=t) is covered by Theorem 1.4 and its conclusion",
    f"{SC}/L05.html:75 (Definition 1.1), :110 (Theorem 1.4 statement 'For 0<=s<t'), :114 ('So B has the Markov property'), :121 (new s=t paragraph)", P,
    "Round-3 FAIL closed. L05:121 now treats s=t: psi=g, g(B_t) is bounded and F_t-measurable (B_t is F_t-measurable by the definition of F_t), so E[g(B_t)|F_t]=g(B_t)=psi(B_t) a.s. "
    "Together with L05:110-120 (0<=s<t), Definition 1.1 holds for all 0<=s<=t. Read this round at pin 9a02b1af.")

# ---- new non-PASS rows found this round ----
row("b-hyp-L06-102-lesson2-hypotheses",
    "2.4 mathematics: Lesson 2 results cited at L06:102 with hypotheses that omit Assumption 2.1 of Lesson 2",
    f"{SC}/L06.html:102 (both sentences); course/modules/SC/SC1/L02.html:286-288 (Theorem 2.5 (H2)), 300-301 (Remark 2.6 (H2))",
    "FAIL",
    "L02.html Theorem 2.5 (H2) reads 'Assuming A2 and Assumption 2.1', and Remark 2.6 (H2) reads 'Assuming A1(a), A1(b), A1(e), A2 and Assumption 2.1'. "
    "L06.html:102 says the [0,1] process is given 'under Assumption A2 of Lesson 2 (Theorem 2.5 there)' and the [0,infinity) extension has 'a proof under Assumptions A1(a), A1(b) and A1(e) of Lesson 1 and Assumption A2 of Lesson 2'. "
    "Both omit Assumption 2.1, which the cited statements need (verified by reading L02.html:279-310).",
    "In L06.html:102 add Assumption 2.1 to both citations: 'under Assumption A2 and Assumption 2.1 of Lesson 2 (Theorem 2.5 there)' and "
    "'with a proof under Assumptions A1(a), A1(b) and A1(e) of Lesson 1, and Assumption A2 and Assumption 2.1 of Lesson 2'.")
row("b-prose-L05-P3-title", "2.9 prose: problem title matches its content",
    f"{SC}/L05.html:354 (title 'P3 · Uniqueness of the transition function'), :355-357 (problem and solution)",
    "FAIL",
    "The title promises uniqueness of the transition function. The problem (L05:355) and its solution (L05:357) show only that the integral of p_u(x,y) over y equals 1 (normalisation). "
    "No uniqueness is proved or asked.",
    "Retitle L05.html:354 to 'P3 · Normalisation of the transition density'.")
row("b-prose-L06-P2-title", "2.9 prose: problem title matches its content",
    f"{SC}/L06.html:366 (title 'P2 · The three inclusions of Lemma 2.1'), :367-369",
    "FAIL",
    "The problem (L06:367) asks only for Lemma 2.1 (ii) and (iii), and says 'without using part (i)'. Part (i) is an equality, not an inclusion, and the solution proves two parts, so 'three inclusions' is wrong.",
    "Retitle L06.html:366 to 'P2 · Parts (ii) and (iii) of Lemma 2.1 from continuity'.")
row("b-prose-L04-P3-title", "2.9 prose: problem title matches its content",
    f"{SC}/L04.html:300 (title 'P3 · Covariance of a martingale with itself at two times'), :301-303",
    "FAIL",
    "The problem asks E[Z_s Z_t] = E[Z_s^2] (L04:301). That is a product moment, not a covariance: no means are subtracted, and E[Z_s]E[Z_t] is not removed, so the title's word is incorrect.",
    "Retitle L04.html:300 to 'P3 · The product moment of a martingale at two times'.")

fragment = {
    "unit": "SC1",
    "slice": "b",
    "round": 4,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-b, round 4 (did not build SC1)",
    "pin": "9a02b1af",
    "base": "67a2d13e (round-3 pin). Delta read hunk by hunk: L04.html:65; L05.html:121, 278; L06.html:102, 119; "
    "L01.html and L02.html and L03.html and index.html hunks read for cross-references; cards.json per-id delta (cards_delta.py, out/cards_delta.txt).",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE4-SC1-b",
    "scratch": "ledgers/SC1/scripts/SC1-b-r4",
    "verified_at": VERIFIED_AT,
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Slice b is lessons L04-L06 and their three lab twins; no project grader, so no mutants are required (rulings). "
        "Every round-3 row id is kept. All round-3 PASS rows were re-verified this round from the pin's bytes; none is carried. "
        "Round-3 FAIL b-math-L05-def-1.1-st-case is closed (L05:121). "
        "Not checked: Shreve (2004) was not read (no access beyond the registry record); no locator or claim is attributed to it on these pages. "
        "Not in slice: hub index.html beyond hours, L01-L03 and L07-L08 content (only the statements cited from them were read), cards for L01-L03 and L07-L08, project and grader files. "
        "Observed, not a FAIL: L05:70 promises result statements say 'Assuming A4'; Lemma 1.3, Theorem 1.4 and Theorem 2.1 name A4 parts in an 'Assumptions' block instead. "
        "Observed, not a FAIL: plans/SC1-open-items.md:6 still calls the L06 path-level claim 'a conjecture'; L06.html:119 now says 'not proved'. "
        "Full repository gate not run: no dependency, build or CI change, so the targeted gates above were used."
    ),
    "summary": "",
}

counts = {"PASS": sum(1 for r in rows if r["status"] == P), "FAIL": sum(1 for r in rows if r["status"] == "FAIL")}
fragment["summary"] = (
    f"SC1-b round 4: verdict FAIL. Rows: pass={counts['PASS']} fail={counts['FAIL']} unverifiable=0 ({len(rows)} rows). "
    "Non-PASS: b-hyp-L06-102-lesson2-hypotheses (L06:102 omits Assumption 2.1), b-prose-L05-P3-title, b-prose-L06-P2-title, b-prose-L04-P3-title."
)

out = ROOT / "ledgers/SC1/SC1-b.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, counts, len(rows))
