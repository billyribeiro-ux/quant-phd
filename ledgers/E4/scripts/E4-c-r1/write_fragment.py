"""Writes the E4-c round-1 verifier fragment (ledgers/E4/E4-c.json). Rows are the verifier's own findings."""

import json

S = "ledgers/E4/scripts/E4-c-r1"
OUT = f"{S}/out"

rows = []


def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- command rows ----
row("E4c-cmd-check-pages", "gate", "course/modules/E/E4/L07.html, L08.html, L09.html", "PASS",
    f"tools/check_pages.py --unit E4 --page L07|L08|L09 -> 'check_pages E4 L07: PASS', 'L08: PASS', 'L09: PASS' ({OUT}/check_pages_L0{{7,8,9}}.out, exit 0).")
row("E4c-cmd-check-dag", "gate", "course/modules/E/E4/*.html (unit)", "PASS",
    f"tools/check_dag.py --unit E4 -> 'check_dag E4: PASS' ({OUT}/check_dag.out). Unlinked out-of-closure names checked by grep in rows E4c-dag-unlinked.")
row("E4c-cmd-check-projects", "gate", "course/modules/E/E4/project.html and grader (unit)", "PASS",
    f"tools/check_projects.py --unit E4 -> 'check_projects E4: PASS' ({OUT}/check_projects.out). Project is not in this slice; run as the unit gate.")
row("E4c-cmd-run-labs", "2.5-labs", "course/modules/E/E4/L07.html, L08.html, L09.html", "PASS",
    f"tools/run_labs.py --unit E4 --page L07|L08|L09 -> 'run_labs E4: PASS (1/1)' three times ({OUT}/run_labs_L0*.out): page code byte-identical to its twin, stdout matches the expected block under the page rule.")
row("E4c-cmd-twins-standalone", "2.5-labs", "tests/labs/E4/lab-E4-L07-1.py, lab-E4-L08-1.py, lab-E4-L09-1.py", "PASS",
    f"ledgers/E4/scripts/E4-c-r1/run_twins.sh: 'python -I -W error' with an empty environment and a scratch cwd; exit 0 for all three; stderr 0 bytes ({OUT}/twins_exit.out, lab-E4-*.err).")
row("E4c-expected-equals-output", "2.5-labs", "course/modules/E/E4/L07.html:331-358, L08.html:544-563, L09.html:264-281", "PASS",
    f"Python check: each page's <pre class=\"expected\"> text (html.unescape) equals the standalone twin stdout exactly, for L07, L08 and L09 ({OUT}/lab-E4-L0*-1.out).")
row("E4c-cmd-page-smoke", "2.9-smoke", "L07, L08, L09 (light/dark, 360 px and desktop)", "PASS",
    f"tools/page_smoke.py --unit E4 --pages L07 L08 L09 (run alone) -> 'page_smoke modules/E/E4/L07.html: PASS', L08 PASS, L09 PASS, 'page_smoke E4: PASS'; lab timings L07 0.0 s, L08 0.1 s, L09 4.9 s (under 10 s) ({OUT}/page_smoke_L07_L08_L09.out).")
row("E4c-cmd-ruff-mypy-twins", "2.5-labs", "tests/labs/E4/lab-E4-L07-1.py, L08-1.py, L09-1.py", "PASS",
    f"ruff check: 'All checks passed!'; ruff format --check: '3 files already formatted'; mypy --no-incremental: 'Success: no issues found in 3 source files' ({OUT}/lint_twins.out).")
row("E4c-cmd-pytest-labs", "2.5-labs", "tests/test_labs.py -k E4", "PASS",
    f"pytest tests/test_labs.py -q -k E4 -> 13 tests, all passing (dot line, no failure lines), exit 0 ({OUT}/pytest_labs_E4_full.out).")
row("E4c-cmd-verify-refs", "2.1-citations", "references/references.json (milgrom1982information used by L09)", "PASS",
    f"tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 ({OUT}/verify_refs_offline.out). tools/verify_refs.py --unit E4 (live) -> 'live re-verification of E4: 3 of 560 entries, 0 problems', exit 0 ({OUT}/verify_refs_unit_E4_live.out).")
row("E4c-cmd-run-graders", "2.6-projects-context", "course/modules/E/E4/grader/", "PASS",
    f"tools/run_graders.py --unit E4 --seeds 0-49 -> 'run_graders E4: PASS (reference 50/50 seeds, slowest 0.2 s)', exit 0 ({OUT}/run_graders_E4.out). Project grader is not this slice; run as the unit gate.")

# ---- L07 ----
row("E4c-L07-structure", "2.9-structure", "course/modules/E/E4/L07.html", "PASS",
    "Read line by line (1-610). Sections in §4.2 order: why it matters (line 51), core sections 1-2 with Definitions, Lemmas, Propositions, Remarks, inline lab (lines 130-360) before 'Where the canon breaks' (362-371), four misconceptions (373-393), problem set with three problems in each of four tiers (395-498), key results (500-516), ten-item quiz (518-593), empty data-references with 'cites no registry source' (595-599). check_pages E4 L07: PASS.")
row("E4c-L07-hours", "2.9-hours", "L07.html:2, index.html:29", "PASS",
    "data-hours=\"8\" (L07.html:2) within 6-12; hub data-hours-lessons=72 and data-hours-project=28 (index.html:29) sum to 100 and the nine lessons sum to 72 (8 h each, L01-L09).")
row("E4c-L07-def-correlation-noise-volume", "2.4-math", "L07.html:55-67", "PASS",
    "Definition 7.1 and 7.2: Corr = Cov/sqrt(Var Var) and rho^2 = Cov(v,p)^2/(Var(v)Var(p)); both match the definitions used in Lemma 7.3-7.4 and in lab Part A (recheck_l07_l08.out: rho2_moments = 1/3 = closed form).")
row("E4c-L07-lemma-7.3-7.4", "2.4-math", "L07.html:70-87", "PASS",
    "Re-derived: q(t)=Var(X)+2t Cov+t^2 Var(Y) discriminant gives Cov^2<=VarVar (7.3); E(X-cY)^2 minimised at c=Cov/VarY, residual Var(X)-Cov^2/VarY, so explained share = Corr^2 (7.4). Zero-mean hypothesis stated (7.4). P1 and P2 solutions (L07.html:430, 437) re-derived and agree.")
row("E4c-L07-prop-7.6", "2.4-math", "L07.html:96-108", "PASS",
    "Re-derived: Y=p/theta_s = v+eta, eta=eps-kappa u, Var(eta)=sigma_eps^2+kappa^2 sigma_u^2; Cov(v,Y)=sigma_v^2, Var(Y)=sigma_v^2+sigma_eta^2; rho^2=sigma_v^2/(sigma_v^2+sigma_eta^2) (identical to L06 Prop 6.7 Step 2, L06.html ~line 201-233). Equivalent form tau_eta/(tau_v+tau_eta) checked. Hypotheses 'A1 to A4 and G of Lesson L06' exist (L06.html:61-90).")
row("E4c-L07-prop-7.7", "2.4-math", "L07.html:111-118", "PASS",
    f"Re-derived: rho^2=sigma_v^2/D, D=sigma_v^2+sigma_eps^2+a^2 sigma_eps^4 sigma_u^2/lam^2; signs in sigma_u, a, sigma_eps (D up) and lam (D down) are strict. Float grid 60x40x20 confirms signs ({OUT}/recheck_l07_l08.out: 'Prop 7.7 sign grid ... True').")
row("E4c-L07-remark-7.8", "2.4-math", "L07.html:121-123", "PASS",
    "rho_0^2 = sigma_v^2/(sigma_v^2+sigma_eps^2) = Corr(v,s)^2 (Cov(v,s)=sigma_v^2, Var(s)=sigma_v^2+sigma_eps^2); rho^2 < rho_0^2 for sigma_u>0 since D grows; 'does not treat sigma_u=0 as Prop 6.7' is correct because L06 A1 requires sigma_u^2>0 (L06.html:61-62).")
row("E4c-L07-remark-7.9-varp", "2.2-numbers", "L07.html:127; L07.html:378 (misconception 1)", "PASS",
    f"Var(p) values 729/1444, 27/49, 27/32, 729/338, 35937/4802 and rho^2 4/9, 1/3, 1/6, 1/18, 1/66 recomputed with Fractions; Var(p) increasing across the sweep ('L07 var_p increasing: True') ({OUT}/recheck_l07_l08.out).")
row("E4c-L07-lab1-values", "2.2-numbers", "L07.html:130-360 (lab 1 parts A-E)", "PASS",
    f"Independent Fraction recomputation reproduces every printed exact value: Part A 1/3 both ways; Part B rho^2 4/9,1/3,1/6,1/18,1/66; Part C 1/6,1/3,9/22; Part D 4/9,1/3,1/6; Part E benchmark 1/2 and 2500/5001 at sd=1/100 ({OUT}/recheck_l07_l08.out; twin run {OUT}/lab-E4-L07-1.out).")
row("E4c-L07-lab1-partF", "2.2-numbers", "L07.html:132, 358; tests/labs/E4/lab-E4-L07-1.py Part F", "PASS",
    "Part F is labelled SIMULATED in the hypothesis (L07.html:132), the docstring (twin line 146), the code print and the output. Seed 7, 20000 draws, tolerance 0.02; printed sample_rho2 0.330625 vs 0.333333, within True. The check is reproducible by the twin under -I -W error (run recorded).")
row("E4c-L07-hypothesis-scope", "2.9-prose", "L07.html:132 (hypothesis) and L07.html:359 (interpretation)", "PASS",
    "The hypothesis predicts exactly the printed signs and values (rho^2 falls, lam-rises, a-falls, every sweep value below 1/2). The interpretation says the lab 'checks the formulas at one parameter set and on finite grids' and 'does not show that the sign pattern holds at every parameter value', which matches the code (no sign check outside the grids).")
row("E4c-L07-misc-claims-1-3", "2.9-prose", "L07.html:378, 382, 386", "PASS",
    "Misconception 1: price variance 729/1444 -> 35937/4802 and rho^2 4/9 -> 1/66 (lab Part B). Misconception 2: tau_eta = 1/2 at base is L06 Lab 1 Part A output 'tau_eta 1/2' (L06.html line 456); rho^2 = tau_eta/(tau_v+tau_eta)=1/3 correct. Misconception 3: rho^2 = 1/66 > 0 at sigma_u = 4 (lab Part B).")
row("E4c-L07-misc-4", "2.9-prose", "L07.html:390", "PASS",
    "Misconception 4: kappa = a sigma_eps^2/lam falls with lam, so the uninformed noise falls; rho^2 at lam=1/4,1/2,3/4 is 1/6,1/3,9/22 (recomputed, Part C).")
row("E4c-L07-problems-M-P", "2.2-numbers", "L07.html:402-447", "PASS",
    "M1 kappa=2, sigma_eta^2=5, rho^2=1/6 (recomputed); M2 kappa=4/3, sigma_eta^2=13/9, rho^2=9/22; M3 rho^2=2/7 and x/(x+5) increasing. P1 (discriminant, Var(Y)=0 case: linear q forces Cov=0, correct), P2 (residual algebra), P3 (scaling) all re-derived.")
row("E4c-L07-problems-E1", "2.2-numbers", "L07.html:453-456", "PASS",
    "1/3 - 0.330625 = 0.0027083; divided by 0.02 = 0.1354 (prints '0.135'); check passes. Solution says 'labelled SIMULATED' (true).")
row("E4c-L07-problems-E3-R", "2.2-numbers", "L07.html:465-498", "PASS",
    "E3 claims re-checked: Part F detects only sampling error (the sample is drawn from the model, so misspecification cannot appear). R1 limit rho^2 -> 0 as a->infinity (D grows like a^2). R2: c=4 and sigma_u=1/sqrt(2) (recomputed). R3: d(rho^2)/d(sigma_u^2) = -sigma_v^2 c/D^2, ratio -c/D varies with sigma_u.")
row("E4c-L07-quiz", "2.9-quiz", "L07.html:522-592", "PASS",
    "Ten items; each numeric key recomputed: 0.3333 (1/3), 5 (sigma_eta^2 at sigma_u=1), 0.4091 (9/22), 0.5 (benchmark), 0.7071 (sigma_u=1/sqrt2), with tolerances consistent with the stated decimals. MC keys point to the correct options (Lemma 7.4, Prop 7.7, Lemma 7.3, Remark 7.9, Prop 7.7 for lam, a, sigma_eps).")
row("E4c-L07-key-results", "2.3-grades", "L07.html:506-512", "PASS",
    "T rows are Lemma 7.3, 7.4, Prop 7.6, 7.7, Remark 7.8, each proved on the page; C rows are the lab finite checks and the SIMULATED Part F, as BUILDER_RULES §2.2 and the plan §2.2 require.")
row("E4c-L07-canon-volume", "2.9-prose", "L07.html:369", "FAIL",
    "Sentence: 'A different definition of volume changes the numbers but not the sign of Proposition 7.7.' Proposition 7.7 is proved for sigma_u only. The sign is preserved for a strictly increasing reparametrisation of sigma_u (for example sigma_u^2), but no proof covers 'a different definition' in general (a volume measure that also moves with lambda or a would change the sign structure).",
    "Restrict the sentence to a strictly increasing reparametrisation of sigma_u (for example sigma_u^2), which keeps the sign of Proposition 7.7, and drop 'a different definition of volume'.")
row("E4c-L07-canon-linear-witness", "2.9-prose", "L07.html:365", "FAIL",
    "'A price that carries information through a nonlinear function of the payoff can be informative while rho^2 is small.' The sentence asserts an existence claim with no example on the page. A witness is v ~ N(0,1) and p = v^2: Corr(v,p)=0 by symmetry, while p determines |v|. The page gives none.",
    "Add the witness (v standard normal, p = v^2: Corr(v,p)^2 = 0 but p reveals |v|) or remove the existence claim.")
row("E4c-L07-cents-docstring", "2.5-labs", "tests/labs/E4/lab-E4-L07-1.py:16 (docstring 'Units')", "FAIL",
    "Twin docstring: 'Units: the payoff is in cents of value per unit of the asset.' The page never introduces a currency unit (Definition 7.1 says 'measured in units of the asset', L07.html:57). Plan §2.1 item 8 requires any introduced currency unit to be integer cents, stated on the page, and rounded once.",
    "Change the twin docstring to 'Units: the payoff is in units of the asset (the liquidation value v)'; the page text is unchanged; then run tools/embed_labs.py L07.html --refresh lab-E4-L07-1 (docstring is part of the embedded code).")
row("E4c-L07-notation-c", "2.4-math/notation", "L07.html:81, 117, 487 (c as coefficient) vs L08 (c = information cost)", "FAIL",
    "Plan §2.3 local symbol c means information cost, and §2.1 item 5 requires each local symbol be 'never redefined'. In L07, c is the forecast slope in Lemma 7.4 (L07.html:81) and c = a sigma_eps^4 / lam^2 in the proof of Prop 7.7 (L07.html:117) and in R2 (L07.html:487). Within E4 this reuses c for another meaning.",
    "Rename the L07 coefficients to unused local letters (for example chi for a sigma_eps^4/lam^2 and b for the forecast slope), and keep c for the information cost as in L08.")
row("E4c-L07-E2-population", "2.2-numbers/prose", "L07.html:462", "FAIL",
    "'By Lemma 7.4, the reported R^2 is the population rho^2.' Lemma 7.4 is a population identity. A regression R^2 that is reported from data is a sample quantity, and E3 (L07.html:467) says it can differ from rho^2. The solution treats a reported sample value as population without stating that assumption.",
    "Rewrite as: 'Treat the reported R^2 as the population rho^2 (an assumption; E3 explains why a sample R^2 can differ), so sigma_eta^2 = 3.'")
row("E4c-L07-simulated-labels", "2.8-data", "L07.html:132, 146 (twin), 290-291, 358, 512", "PASS",
    "SIMULATED is visible in the hypothesis text, the printed output and the key-results row for the one seeded check; no other draw is used.")
row("E4c-L07-dag", "2.9-dag", "L07.html:37-38 (links to L06.html#def-noisy-rational-expectations-equilibrium, concepts.html anchors)", "PASS",
    "check_dag PASS; the L06 anchor exists (L06.html:167). Concepts used are prerequisites (random-variable, expectation, variance, correlation, least-squares-projection) or defined earlier in E4 (L06).")
row("E4c-L07-define-before-use", "2.9-prose", "L07.html:57-62", "PASS",
    "correlation, noise volume and price informativeness are defined before use (L07.html:57, 57, 62); 'noise-trader supply' is defined in L06.")
row("E4c-L07-process-and-banned", "2.9-prose", "course/modules/E/E4/L07.html (whole file)", "PASS",
    "grep for build/builder/verifier/round/request and the banned list in BUILDER_RULES §1.3-1.4: no hits in learner text (only 'cents' in the lab docstring, separately flagged). check_pages banned-string rule PASS.")

# ---- L08 ----
row("E4c-L08-structure", "2.9-structure", "course/modules/E/E4/L08.html", "PASS",
    "Read line by line (1-808). Sections 1-5 with Assumptions A1-A3 and A5, Lemmas 2.1-2.5, Fact 2.3, Corollaries 2.4 and 3.2, Propositions 3.1, 4.1, 4.2, 4.4, 5.1, 5.2, Lemmas 3.3 and 4.5, Definitions 4.3, 4.6, inline lab (334-565), canon-breaks (567-576), four misconceptions (578-598), problems in four tiers with three each (600-703), key results (705-723), nine-item quiz (725-791), empty data-references (793-797). check_pages E4 L08: PASS.")
row("E4c-L08-hours", "2.9-hours", "L08.html:2", "PASS",
    "data-hours=\"8\" within 6-12; hub split in index.html:29 counts this lesson in the 72 h of lessons.")
row("E4c-L08-lemma-2.1-2.2-fact-2.3", "2.4-math", "L08.html:85-113", "PASS",
    "Re-derived: MGF of normal gives E[U|I] = -exp(-aW0') exp(f(x)), f quadratic, minimiser x*=(m-p)/(aV), value -exp(-aW0')exp(-(m-p)^2/(2V)) (2.1). Lemma 2.2: integral combining exponents gives (1+sigma^2/V)^(-1/2) (2.2, sigma^2=0 case also checked). Fact 2.3 standard normal conditioning, residual uncorrelated -> independent (2.3).")
row("E4c-L08-cor-2.4-lemma-2.5", "2.4-math", "L08.html:121-146", "PASS",
    "Cor 2.4(a) E[v|s], Var=1/(tau_v+tau_eps); (b) with kappa' in R, b_y=tau_eta/(tau_v+tau_eta), Var=1/(tau_v+tau_eta) (re-derived). Lemma 2.5 conditional law given sigma(s,p) (independence of r_v from (s,u) re-derived). Hypothesis beta_p != 0 is used only to write sigma(s,p) inside sigma(s,u); see E4c-L08-lambda0-citation.")
row("E4c-L08-prop-3.1", "2.4-math", "L08.html:151-170", "PASS",
    "Re-derived clearing identity (*) (L08.html:162-164) from Cor 2.4 and (tau_v+A')b=A' etc.; coefficient matching gives beta_p=A'/(tau_v+A'), alpha=(1-beta)vbar, gamma/beta_p=kappa' and kappa'(A'-(1-lam)tau_eta')=a with the bracket = lam tau_eps, so kappa'=kappa. Part (b) price clears (checked by substituting). Numerical check: Monte Carlo market-clearing residual 1.3e-15 in the lab (run output).")
row("E4c-L08-cor-3.2-lemma-3.3", "2.4-math", "L08.html:173-200", "PASS",
    "Cov(v,p*)=beta sigma_v^2, Var(p*)=beta^2(sigma_v^2+sigma_eta^2), Corr^2=sigma_v^2/(sigma_v^2+sigma_eta^2)=tau_eta/(tau_v+tau_eta) (re-derived). Lemma 3.3(b): t/(tau_v+t) strictly increasing; (c) noiseless case constant in lam. Recomputed Corr^2 at the printed Part C fractions matches the printed values to 6 decimals ({OUT}/recheck_l08_corr.out).")
row("E4c-L08-prop-4.1-4.2-4.4", "2.4-math", "L08.html:204-246", "PASS",
    "Re-derived D_I=(b_s-beta)(s-vbar)+kappa beta u and D_U=(b_y-beta)(y-vbar), variances, means zero (4.1); EU formulas (4.2) and the log-ratio algebra giving EU_I >= EU_U iff c <= G (4.4). Independent Monte Carlo (2e6 draws, lam=1/2, recheck_l07_l08.out): indifference cost 0.15903 vs closed-form G(1/2)=0.15900 (difference 3e-5, within MC error).")
row("E4c-L08-lambda0-citation", "2.4-math/hypotheses", "L08.html:221, 240, 275", "FAIL",
    "Line 275: 'Cases (i) and (ii) follow from Proposition 4.4 applied at lambda=0 and lambda=1'. Prop 4.2 and 4.4 are stated for lambda in (0,1] (L08.html:221, 240). At lambda=0 the price is p = vbar - a sigma_v^2 u (Lemma 4.5, L08.html:250), so beta_p = 0 and Lemma 2.5's hypothesis beta_p != 0 (L08.html:140) fails. The deviator's expected utility at lambda=0 is therefore not derived under the stated hypotheses. The argument can be completed (sigma(s,p*) = sigma(s,u) and u is independent of (v,s)) but the page does not say it.",
    "Either state Prop 4.2/4.4 for lambda=0 with the deviator conditioning on sigma(s,u) and prove it (drop the beta_p != 0 hypothesis from Lemma 2.5, whose proof does not use it), or cite Lemma 4.5 directly for case (i) and state case (ii) at lambda=1 only.")
row("E4c-L08-lemma-4.5", "2.4-math", "L08.html:249-261", "PASS",
    "Re-derived: p=vbar-a sigma_v^2 u; D_I, D_U, V_U=sigma_v^2, X_0=a^2 sigma_u^2 sigma_v^2, q=sigma_v^2/sigma_eps^2; (1+q)(1+X_0)/(1+X_0) gives G(0)=ln(1+q)/(2a). Numerically G(0)=ln2/4=0.17328679514 (recheck_l07_l08.out) matching the printed 0.173287.")
row("E4c-L08-prop-5.1", "2.4-math", "L08.html:284-301", "PASS",
    "(a) at sigma_u=0: tau_eta=tau_eps, A=tau_eps, beta=b_s, b_y=b_s, Var(D_I)=Var(D_U)=0, G=0 (recomputed in ledgers/E4/scripts/E4-c-r1/recheck_l08_extra.py: G = 0.0 at lam = 0.1, 0.5, 1 with var_u = 0, out/recheck_l08_extra.out); (b) 0<c<G(0): each case fails; (c) c>=G(0): lambda=0 holds, lambda=1 and interior fail. Hypotheses sigma_u^2=0 stated.")
row("E4c-L08-prop-5.2", "2.4-math", "L08.html:304-326", "PASS",
    "(a) limit re-derived: kappa*A -> a, kappa*beta -> a sigma_v^2, Var(D_I) and Var(D_U)/V_U limits give G(0) (checked; numerically G(1e-6)-G(0) = -6.25e-14, recheck_l07_l08.out). (b) case (i)/(ii) at the stated costs. (c) existence for G(1)<c<G(0) is conditional on A5 (L08.html:314-315) and is labelled as such.")
row("E4c-L08-A5", "2.9-prose", "L08.html:313-316, 573", "PASS",
    "A5 is a numbered Assumption that is explicitly assumed (not proved); it is used only in Prop 5.2(c) and the bisection (L08.html:332). The page says so (L08.html:315, 573).")
row("E4c-L08-line51-zero-cost", "2.9-prose/math", "L08.html:51, L08.html:301", "FAIL",
    "L08.html:51: 'no informed fraction is an equilibrium at any cost below the gain from information.' L08.html:301: 'at any cost between zero and G(0), no fraction works'. At c = 0 with sigma_u=0, G(1) = 0 >= c, so lambda=1 satisfies Definition 4.6(ii) (L08.html:270) and is an equilibrium (recheck: gain(1)=0 at var_u=0). Prop 5.1(b) (L08.html:289) correctly requires 0 < c < G(0). The two sentences overreach.",
    "Replace with 'at any positive cost below G(0)' (line 51) and 'for 0 < c < G(0)' (line 301).")
row("E4c-L08-line51-existence", "2.9-prose/scope", "L08.html:51", "FAIL",
    "'With noise, equilibria exist and the price stays partly informative.' The page proves existence without A5 only for c >= G(0) or c <= G(1) (Prop 5.2(b)). For G(1) < c < G(0) existence is assumed (A5, L08.html:314-315, 'This is assumed here'). The why-it-matters sentence states existence unconditionally, which BUILDER_RULES §2 and plan §2.1 item 4 forbid.",
    "Say: 'With noise, equilibria exist for costs outside (G(1), G(0)); for costs inside that interval the existence claim uses Assumption A5.'")
row("E4c-L08-G1-derivation", "2.3-grades/2.2-numbers", "L08.html:336, 564, 583, 674, 719", "FAIL",
    "G(1)=ln(5/3)/4 is graded T in the key-results table (L08.html:719, source 'Problem Emp 3'). Section 4 derives only G(0) (Lemma 4.5). The Emp 3 solution (L08.html:674) asserts kappa=2, tau_eta=1/5, beta=b_s=1/2, Var(D_I)=1, V_I=1/2, Var(D_U)=2/3, V_U=5/6 without showing the steps. The values are correct (recheck: G(1)=0.1277064059, printed 0.127706), but the T grade has no derivation on the page, and the lab-hypothesis closed form (L08.html:336) is asserted, not derived.",
    "Add a derivation of G(1) to Section 4 with each intermediate value shown, or regrade the row to C with basis 'Lab 1, Part B (exact printed value)' and say the closed form is not derived on this page.")
row("E4c-L08-lab1-part-A", "2.5-labs/2.2-numbers", "L08.html:336, 544-547; twin lines 351-383", "PASS",
    "Part A reproduces: residual 1.332e-15 (<1e-12) and sample slope 0.1595 against formula b_y/beta = 0.1605 (recheck: b_y/beta = 0.1604938, lam=1/2, kappa=4, tau_eta=1/17). Difference 0.0010 (at most 0.02). Labelled SIMULATED with span.simulated-label (L08.html:336).")
row("E4c-L08-lab1-part-B", "2.2-numbers", "L08.html:548-551", "PASS",
    "gain(0)=0.173287, gain(1)=0.127706 and gain(0.5)=0.158997 recomputed (recheck_l07_l08.out: 0.1589971917 for gain(0.5)); gain(1e-6)-gain(0) = -6.2e-14; monotone checks on the 999 interior grid points reproduced by the twin and by the independent recheck (recheck_l08_extra.out: 'G strictly decreasing ... True', 'Corr^2 strictly increasing ... True').")
row("E4c-L08-lab1-part-C", "2.2-numbers", "L08.html:552-558", "PASS",
    f"Independent bisection (recheck_l07_l08.py) reproduces every interior root to <=4.3e-10: cost 0.13 -> 0.965625410; 0.14 -> 0.815032329; 0.15 -> 0.657828572; 0.16 -> 0.480567912; 0.17 -> 0.231615819. Boundary rule: 0.12 -> lam=1 (gap 7.71e-03), 0.18 -> lam=0 (gap -6.71e-03). Gap magnitudes at interior roots are 1e-15 to 3e-14 as printed.")
row("E4c-L08-lab1-part-D-docstring", "2.5-labs/docstring", "tests/labs/E4/lab-E4-L08-1.py:181-182; L08.html:564", "FAIL",
    "Twin docstring of part_d: 'gain is zero at every interior fraction, so no fraction is an equilibrium at cost 0.15.' The code evaluates the gain only on the 999-point grid (line 182: grid = [k/(GRID+1) ...]), so the docstring describes a result the code does not check on every interior fraction. The interpretation (L08.html:564) says Part D 'checks Proposition 5.1 by computing the three cases', which is true only on the grid. Prop 5.1(a) proves the all-fraction statement on the page, but the lab does not.",
    "Change the docstring to 'gain is zero at every grid fraction; Proposition 5.1(a) gives zero at every interior fraction', and say in the interpretation that the interior case is checked on the 999-point grid.")
row("E4c-L08-misc-claims", "2.9-prose", "L08.html:583, 587, 591, 595", "PASS",
    "583: G(1)=ln(5/3)/4>0 with noise (printed 0.127706). 587: positive informed fraction for every printed cost 0.12-0.17 (all below G(0)=0.173287), lam* at 0.15 is 0.658 (printed 0.657828572). 591: Corr values 0.013 to 0.167 at costs with an informed trader (printed). 595: N=G-c falls with c; fraction falls on the grid, and the text says the grid does not show it for other costs.")
row("E4c-L08-canon-finite-traders", "2.9-prose/math", "L08.html:572", "FAIL",
    "'With a finite number of traders, each trader's demand moves the price, and the linear equilibrium of Proposition 3.1 is not the equilibrium of that game.' No derivation or citation on the page establishes what the finite-trader equilibrium is or that Prop 3.1 fails in it. It is an unproven claim.",
    "Replace with: 'Proposition 3.1 uses price taking (A3). With a finite number of traders the derivation does not apply, and the page does not derive the equilibrium of that game.'")
row("E4c-L08-canon-A5-limit", "2.9-prose", "L08.html:571-573", "PASS",
    "Statements 'the noise is what keeps an equilibrium with informed traders alive' (Prop 5.2 and 5.1 contrast), 'nothing on the page proves that G falls on (0,1)' and 'the cost is in wealth' are consistent with the proofs (L08.html:284-325).")
row("E4c-L08-emp-1-2", "2.2-numbers", "L08.html:658-667", "PASS",
    "Emp 1: printed gap 1.83e-15 at lam* 0.657828572 (matches output). Emp 2: 0.231615819 is at cost 0.17 (sixth of seven, output line 557) and Corr^2 0.013061 (printed); 0.480567912 at cost 0.16 (output line 556).")
row("E4c-L08-res-1", "2.4-math", "L08.html:683-687", "PASS",
    "Proof of Prop 5.1(b),(c) in the exercise; each case checked (G=0 for lam>0; lam=1 needs G(1)>=c, fails; lam=0 needs G(0)<=c, fails for c<G(0)); when c>=G(0) the price is vbar - a sigma_v^2 u, independent of v, so Corr=0 (correct).")
row("E4c-L08-res-2-crossref", "2.4-math/prose", "L08.html:690-692", "FAIL",
    "Exercise asks for the limit 'using only the formulas of Proposition 4.1 and Corollary 2.4', but the solution writes 'From Proposition 5.2(a), Var(D_U) = (b_y - beta)^2(sigma_v^2 + 1/tau_eta)'. The formula is in Proposition 4.1 (L08.html:207); Prop 5.2(a) is a limit statement. The algebra itself is correct.",
    "Change 'From Proposition 5.2(a)' to 'From Proposition 4.1'.")
row("E4c-L08-res-3", "2.4-math", "L08.html:697-699", "PASS",
    "Var(D_I) = kappa^2 b_s^2 sigma_u^2 at lam=1 (beta=b_s) -> 0; Var(D_U)/V_U = (b_y-b_s)^2(sigma_v^2+sigma_eta^2)/V_U -> 0 since tau_eta -> tau_eps; so G(1) -> 0 (re-derived).")
row("E4c-L08-mech-1-3", "2.2-numbers", "L08.html:607-624", "PASS",
    "Mech 1: kappa=4, tau_eta=1/17, sigma_eta^2=17 (recomputed). Mech 2: x*=1/12, maximal value -exp(-3W0)exp(-1/16) (Lemma 2.1 with m=1, V=2, p=1/2, a=3). Mech 3: 1/sqrt5 = 0.4472136 and Jensen bound exp(-2)=0.135 (correct).")
row("E4c-L08-proof-1-3", "2.4-math", "L08.html:632-651", "PASS",
    "Proof 1 coefficient of s gives beta_p = A'/(tau_v+A') (re-derived). Proof 2 monotone tau_eta (correct). Proof 3: N strictly decreasing in c; each interior fraction is an equilibrium at exactly one cost; the page says monotonicity of G in lam is not proved here (correct).")
row("E4c-L08-emp-3", "2.2-numbers", "L08.html:671-675", "PASS",
    "G(0)=ln(2)/4=0.173287 and G(1)=(1/4)ln((1+2)/(1+4/5))=(1/4)ln(5/3)=0.127706 with the listed intermediate values (values verified in recheck). The derivation of the intermediate values is the gap in E4c-L08-G1-derivation, not here.")
row("E4c-L08-quiz-items", "2.9-quiz", "L08.html:730-790", "PASS",
    "Nine items: V is the conditional variance (item 1 correct); kappa=4 (item 2); G(0)=0.1732868 (item 3); no fraction at 0<c<G(0) (item 4); Corr^2=1/18 at lam=1/2 (item 5, 0.0555556 recomputed); the 0.6578 rounding (item 7, printed 0.657828572); u lowers the price, coefficient -kappa beta (item 8); 0.4472136 (item 9). Explanations match the lesson text.")
row("E4c-L08-quiz-6-uniqueness", "2.9-quiz/math", "L08.html:762-770", "FAIL",
    "Keyed correct option: 'If c >= G(0), the equilibrium informed fraction is 0.' Prop 5.2(b) (L08.html:308) only says lambda=0 is an equilibrium; L08.html:328 says 'The interior equilibrium is not claimed to be unique', and L08.html:573 says monotonicity of G is not proved on (0,1). The keyed option asserts uniqueness the page does not establish. The explanation cites Definition 4.6(i) and Prop 5.2(b), which support existence only.",
    "Change the keyed option to 'If c >= G(0), the fraction 0 is an equilibrium informed fraction', and keep the explanation.")
row("E4c-L08-key-results", "2.3-grades", "L08.html:711-719", "PASS",
    "Rows: CARA demand T (Lemma 2.1); normal moment T (2.2); price T (3.1, unique when sigma_u>0); Corr T (3.2, 3.3); indifference T (4.4); G(0) T (4.5); noiseless T (5.1); Prop 5.2 T with A5 assumed; G(1) row see E4c-L08-G1-derivation.")
row("E4c-L08-footer", "2.9-prose", "L08.html:806", "FAIL",
    "Footer: 'Every claim carries an evidence grade and a registry citation.' The references section says 'This lesson cites no registry source' (L08.html:795) and the reference list is empty (L08.html:796). The footer is false on the page.",
    "Use the L07 footer wording: 'Each graded result carries a proof or a lab result.'")
row("E4c-L08-notation-gamma", "2.4-notation", "L08.html:140, 154, 161, 165, 168, 635", "FAIL",
    "Plain gamma is the coefficient of u in p = alpha + beta_p s - gamma u. Plan §2.3 (plans/E4-build-plan.md, notation table row \\gamma_3, \\gamma_4) states 'Plain \\gamma is not used either.' The registry keeps gamma local (notation/notation.json, 'about' field), so this is a plan rule rather than a registry collision.",
    "Rename the coefficient to an unused letter (for example varpi) throughout Prop 3.1, Lemma 2.5, Proof 1 of the problem set, and the proof text; or record a notation decision in the plan.")
row("E4c-L08-define-posterior", "2.9-define-before-use", "L08.html:122", "FAIL",
    "'posteriors of the two groups' is the first use of 'posterior' in E4 L08 (and the term recurs in Corollary 2.4 and Prop 4.1). The plan §2.1 item 5 requires 'the posterior' to be defined with a plain <dfn> at first use; no <dfn> for posterior appears in L08.",
    "Add a plain <dfn>posterior</dfn> (the conditional distribution of v given the information set) at the first use in Section 1 or 2.")
row("E4c-L08-hub-title", "2.9-structure", "index.html:136 vs L08.html:35", "FAIL",
    "Hub card title 'The Grossman–Stiglitz paradox' (index.html:136) does not match the lesson h1 'The Grossman–Stiglitz Paradox' (L08.html:35). Plan §2.2 requires hub titles to match the h1 at integration.",
    "Make the hub title and the h1 identical (capitalise 'Paradox' in both).")
row("E4c-L08-DAG", "2.9-dag", "L08.html:37-38", "PASS",
    "Links: price-informativeness -> L07.html#def-price-informativeness (exists, L07.html:62); other concepts link to concepts.html anchors of prerequisites (E1, E3, M2, M4). check_dag PASS.")
row("E4c-L08-simulated", "2.8-data", "L08.html:336, lab docstring", "PASS",
    "Part A is seeded and carries span.simulated-label (L08.html:336); parts B to D are exact or on fixed grids, labelled as such. Seed 20261103 is in the twin.")
row("E4c-L08-process-banned", "2.9-prose", "course/modules/E/E4/L08.html (whole file)", "PASS",
    "grep for process words and banned strings (BUILDER_RULES §1.3-1.4) on the page: no hits in learner text.")

# ---- L09 ----
row("E4c-L09-structure", "2.9-structure", "course/modules/E/E4/L09.html", "PASS",
    "Read line by line (1-524). Assumptions B1-B3, Definitions 1.1-1.2, Theorem 2.1 with proof, Definition 2.2, Corollary 2.3, Example 2.4, Remark 2.5, inline lab (126-283), canon-breaks (292-300), three misconceptions (302-318), problems in four tiers with three each (320-423), key results (425-439), nine-item quiz (441-507), empty data-references (509-513). check_pages E4 L09: PASS.")
row("E4c-L09-hours", "2.9-hours", "L09.html:2", "PASS",
    "data-hours=\"8\" within 6-12.")
row("E4c-L09-theorem-2.1", "2.4-math", "L09.html:86-100", "PASS",
    "Re-derived: S_1 = sum over P1-cells D inside M of pi(D) g_1(D) (M is a union of P1 cells); S_2 = -S_1 from the same argument with -x and P2 cells; nonnegativity forces S_1=0 and then each term zero. Hypothesis (nonnegative on all of M, B1-B3) stated. Proof complete.")
row("E4c-L09-cor-2.3-def-2.2", "2.4-math", "L09.html:102-115", "PASS",
    "Corollary 2.3 follows from Theorem 2.1 by contradiction at omega* in M(omega*) (omega* in M). Definition 2.2 'says nothing about prices' is consistent with the page.")
row("E4c-L09-example-2.4", "2.2-numbers", "L09.html:118-120", "PASS",
    "M(1)={1,2,3} (cells {1,2}, {1,2,3}, {3}); g_1(1)=(-1+2)/2=1/2; g_2(1)=(1-2+2)/3=1/3; g_1(3)=x(3)=-2<0. Printed by the lab (output lines 271-273); recomputed independently ({OUT}/recheck_l09.out: first strict bet [-1,2,-2,-2,-2,-2]).")
row("E4c-L09-meet-definition-canon", "2.9-prose", "L09.html:79 vs L09.html:298", "FAIL",
    "Definition 1.2 (L09.html:79) defines the meet as the smallest set containing omega that is a union of cells of both partitions. Canon-break bullet 4 (L09.html:298) says the meet is 'the largest set of states at which the acceptance must be common knowledge'. That contradicts the definition.",
    "Rewrite as: 'Theorem 2.1 uses the meet, the smallest set containing the state that is a union of cells of both partitions, on which acceptance must hold.'")
row("E4c-L09-misc-1-no-trade-overclaim", "2.9-prose", "L09.html:307", "FAIL",
    "'Different information alone does not produce trade.' Theorem 2.1 excludes only strict mutual acceptance when acceptance is common knowledge on the meet. Example 2.4 (L09.html:119) and L09.html:290 show two traders who accept a bet strictly on private information, which the page says the theorem does not rule out. The sentence overgeneralises the theorem.",
    "Replace with: 'With a common prior and common knowledge of acceptance on the meet, Theorem 2.1 rules out a bet that both traders accept strictly. Acceptance on private information is not ruled out (Example 2.4).'")
row("E4c-L09-misc-2-3", "2.9-prose", "L09.html:311, 315", "PASS",
    "Misconception 2: Omega={a,b,c}, P1={{a,b},{c}}, P2={{a},{b,c}}, E={a,b}: both traders know E at a, but M(a)={a,b,c} is not in E (re-derived). Misconception 3: posterior 1/2 at state 1 and receipt -2 at state 3 (Example 2.4) correct.")
row("E4c-L09-mech-1-3", "2.2-numbers", "L09.html:327-342", "PASS",
    "Mech 1: g_1 = 1 on {1,2}, 3/2 on {3,4} (recomputed). Mech 2: M(1)=Omega (reachable 1->2->3->4) (re-derived). Mech 3: trader 1 expects 0.4; trader 2 expects 0.2 (recomputed).")
row("E4c-L09-proof-1-2", "2.4-math", "L09.html:352-363", "PASS",
    "Proof 1 identity over a union of P1 cells: disjoint cells, pi(D)>0 (re-derived). Proof 2: M(omega') subset M(omega) subset E (re-derived).")
row("E4c-L09-proof-3-statement", "2.4-math", "L09.html:367-369", "FAIL",
    "Statement: 'Prove that the hypothesis of Theorem 2.1 implies g_1 = g_2 = E[x] on Omega.' The solution (L09.html:369) gives g_2 = E[-x] = -E[x], and then E[x]=0. The statement and the solution disagree on g_2 (equal only when E[x]=0).",
    "Change the statement to 'g_1 = E[x] and g_2 = -E[x] on Omega, and E[x] = 0 under the hypothesis'.")
row("E4c-L09-emp-1-3", "2.2-numbers", "L09.html:377-394", "PASS",
    "Emp 1: 500 strict and 625 nonneg on the meet, intersection 0 (printed; recomputed independently in recheck_l09.out). Emp 2: x=(-1,2,-2,-2,-2,-2), g_1 on meet 1/2,1/2,-2; g_2 1/3 (verified). Emp 3: the zero-posterior set on {1,2,3} equals {x3=0, x2=-x1}, count 625 (recheck_l09.out: 'equal sets True').")
row("E4c-L09-res-1", "2.4-math", "L09.html:403-405", "PASS",
    "Proof: S_1 >= 0 from g_1>=0 on M; sum over M of pi(-x-k) = -S_1 - k pi(M) >= 0 from g_2>=0 on M; sum gives -k pi(M) >= 0, contradicting k>0 and pi(M)>0. Correct.")
row("E4c-L09-res-2", "2.4-math", "L09.html:410-412", "FAIL",
    "Exercise: 'Show that there is a bet with strictly positive expected receipts for both traders' for any priors p != r. The solution (L09.html:412) says 'With 0 < r < p < 1, such a theta exists' and handles p < r by exchanging the labels H and L. Priors equal to 0 or 1 are not covered by the written argument (for example p = 1 or r = 0), although a theta strictly between r and p in (0,1) exists in every case. The stated proof therefore has a gap at the boundary.",
    "Replace the range condition with: 'choose theta strictly between r and p and inside (0,1), which is possible for every p != r in [0,1]; then t = theta/(1 - theta)'. Or state 0 < p, r < 1 as a hypothesis, as B1 does for state probabilities.")
row("E4c-L09-res-3", "2.4-math", "L09.html:416-419", "PASS",
    "Proof of Theorem 2.1 uses only that M is a union of cells of both partitions; the same argument holds for any such E (re-derived).")
row("E4c-L09-canon-prior-example", "2.2-numbers", "L09.html:295", "PASS",
    "Trader 1: 0.7*1 + 0.3*(-1) = 0.4; trader 2's receipt of -x: -(0.4 - 0.6) = 0.2 (both recomputed). Trivial partitions, so common knowledge holds and the common-prior hypothesis is the one that fails.")
row("E4c-L09-lab1-counts", "2.2-numbers/2.5-labs", "L09.html:264-281; tests/labs/E4/lab-E4-L09-1.py", "PASS",
    f"Independent numpy enumeration of 5^6=15625 bets ({OUT}/recheck_l09.out): state 1 strict-both 500, strict and nonnegative on meet 0, nonnegative on meet 625, nonneg but not zero 0; state 4 same counts; first strict bets [-1,2,-2,-2,-2,-2] and [-2,-2,-2,-2,1,2]; posteriors on the meets match the printed fractions.")
row("E4c-L09-lab1-hypothesis-interpretation", "2.5-labs", "L09.html:128, 282", "PASS",
    "Hypothesis (exactly 15625 bets; identity holds for every bet; state 1 and 4 counts) matches the printed output. Interpretation: 'the printed counts match the hypothesis', 'a finite check on one six-state model, so it illustrates Theorem 2.1 and does not prove it' (honest).")
row("E4c-L09-quiz", "2.9-quiz", "L09.html:445-505", "PASS",
    "Nine items: meet condition (item 1 correct, explanation Misconception 2); g_1(1)=0.5; g_2(1)=0.3333333; B1 correct (item 4); 0.2 (item 5); Lab 1 part B 0 nonnegative on the meet (item 6); 15625 (item 7); M(1)={1,2,3} (item 8); 0.5 (item 9). All keys recomputed.")
row("E4c-L09-key-results", "2.3-grades", "L09.html:431-435", "PASS",
    "T rows: identity (Proof 1), Theorem 2.1, Corollary 2.3, Misconception 2 example (checked); the two-priors row rests on Res 2, whose boundary gap is E4c-L09-res-2.")
row("E4c-L09-references", "2.1-citations", "L09.html:511; references/references.json:17291", "PASS",
    "Registry record milgrom1982information: Milgrom & Stokey, 'Information, trade and common knowledge', Journal of Economic Theory, volume 26, issue 1, pages 17-27, 1982 (references.json:17291 record). The page's title, container, volume, issue and pages match. The page states no result of the paper and says the abstract was not read. The span uses data-cite but the list is empty, which is consistent with 'no claim cited'.")
row("E4c-L09-footer", "2.9-prose", "L09.html:522", "FAIL",
    "Footer: 'Every claim carries an evidence grade and a registry citation.' The references section says the lesson cites only the topic key and states no result from it (L09.html:511); most claims carry no registry key. The footer overstates.",
    "Use wording that matches the page: 'Each graded result carries a proof or a lab result.'")
row("E4c-L09-hub-title", "2.9-structure", "index.html:137 vs L09.html:35", "FAIL",
    "Hub card title 'The no-trade theorem' (index.html:137) does not match the lesson h1 'The No-Trade Theorem' (L09.html:35). Plan §2.2 requires them to match.",
    "Make the hub title and the h1 identical.")
row("E4c-L09-dag", "2.9-dag", "L09.html:37, 287, 290", "PASS",
    "Links: arrow-debreu-equilibrium -> L02.html#def-arrow-debreu-equilibrium (exists, L02.html:89); pareto-efficiency and adverse-selection -> concepts.html (E1, E2 closure). check_dag PASS. Unlinked use of plan D-list names checked in E4c-dag-unlinked.")
row("E4c-L09-process-banned", "2.9-prose", "course/modules/E/E4/L09.html (whole file)", "PASS",
    "grep for process words and banned strings: no hits in learner text.")
row("E4c-L09-simulated", "2.8-data", "L09.html:128", "PASS",
    "No random draws and no data; the hypothesis states 'no SIMULATED label applies' (correct; the twin uses no RNG, only fractions and itertools).")

# ---- twins (lab-level) ----
row("E4c-twin-L07-1", "2.5-labs", "tests/labs/E4/lab-E4-L07-1.py", "PASS",
    f"Standalone python -I -W error run exit 0, stderr empty; ruff and mypy clean; page code byte-identical (run_labs); expected block exact match; top-level main() call and no __name__ guard (grep count 0); seeded (random.Random(7)); standard library only. Only the 'cents' docstring line is flagged (E4c-L07-cents-docstring).")
row("E4c-twin-L08-1", "2.5-labs", "tests/labs/E4/lab-E4-L08-1.py", "PASS",
    f"Standalone run exit 0, stderr empty; ruff/mypy clean; page code byte-identical; expected block exact; top-level main(); seed 20261103 (random.Random). Only part_d docstring is flagged (E4c-L08-lab1-part-D-docstring).")
row("E4c-twin-L09-1", "2.5-labs", "tests/labs/E4/lab-E4-L09-1.py", "PASS",
    f"Standalone run exit 0, stderr empty; ruff/mypy clean; page code byte-identical; expected block exact; top-level main(); no RNG, no data.")

# ---- cross-cutting ----
row("E4c-notation-registered", "2.4-notation", "course/modules/E/E4/L07.html, L08.html, L09.html", "PASS",
    "grep: no use of the registered symbols T (sample size), \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}, and no raw \\mathbb{E} or \\mathbb{R} (architect ruling 1: \\R used in L08.html:107 and L09.html:67). Expectation via \\E, correlation via \\Corr. Plain gamma (L08) and c (L07) are the two local-symbol findings, flagged separately.")
row("E4c-dag-unlinked", "2.9-dag", "L07, L08, L09 (plan §4 names D1-D10)", "PASS",
    "grep of the slice for bayes, state price, stochastic discount, law of one price, fundamental theorem, martingale, efficient markets, noise-trader risk, two-fund, diagnostic, determinacy, informed trading, walras, banach, intermediate value, Lagrangian, Bellman: no hits. 'posterior' and 'common knowledge' are defined in-page with plain dfn (L09.html:72, 104 for common knowledge is a dfn with data-concept of its own only for the theorem; the common-knowledge term at L09.html:79 is a plain dfn). CARA and noise traders are plain dfn (L08.html:59, 66).")
row("E4c-no-mutants-slice", "2.6-mutation", "lab twins (not project graders)", "PASS",
    "Not applicable: lab twins are demonstrations, and mutation testing applies to project graders only (architect ruling in plans/E4-build-plan.md §2.1 item 14 and the verifier rules). Recorded so the ledger's mutant list is intentionally empty for this slice.")

fragment = {
    "unit": "E4",
    "slice": "E4-c",
    "round": 1,
    "verifier": "Claude Haiku 5.5, independent verifier for E4-c round 1 (did not build E4; checkout pinned at 1c1645f)",
    "pin": "1c1645f3b00eada2fb54d39c86d5d949e15b4fbc",
    "base": "none: first verification of this slice (round 1)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE1-E4-c",
    "scratch": "/tmp/e4c-run.* (twin runs, removed after each run)",
    "verified_at": "2026-11-04T04:30:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Scope: course/modules/E/E4/L07.html, L08.html, L09.html and tests/labs/E4/lab-E4-L07-1.py, lab-E4-L08-1.py, lab-E4-L09-1.py. "
        "Every page was read line by line (L07 1-610, L08 1-808, L09 1-524), and every twin was read in full. "
        "Mechanical rows were run on this pin and their outputs are in ledgers/E4/scripts/E4-c-r1/out/ (scripts: run_gates.sh, run_twins.sh, "
        "recheck_l07_l08.py, recheck_l08_corr.py, recheck_l09.py, write_fragment.py). Independent recomputation of every printed lab number and every "
        "closed-form number in the slice is in recheck_l07_l08.out, recheck_l08_corr.out and recheck_l09.out. Monte Carlo of Prop 4.2/4.4 "
        "(2e6 draws) is in recheck_l07_l08.out. "
        "Not checked by this slice: the cards (E4 cards.json, builder F), the hub index.html and the project (slices a, b, d, e), mutation and "
        "alternative graders (project only), page_smoke for other pages, and the full unit ledger. Hub title mismatches are reported here "
        "because they sit between the hub and these lessons. The lesson-level verdict is FAIL because of the findings listed below; "
        "none of them invalidates a lab's output."
    ),
    "summary": "",
}

n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_fail = sum(1 for r in rows if r["status"] == "FAIL")
n_unv = sum(1 for r in rows if r["status"] == "UNVERIFIABLE")
fragment["summary"] = (
    f"E4-c round 1: verdict FAIL. {len(rows)} rows: {n_pass} PASS, {n_fail} FAIL, {n_unv} UNVERIFIABLE. "
    "Non-PASS rows are wording and proof-hypothesis defects in L07-L09, one quiz key, one docstring, one notation rule, and two hub title mismatches; "
    "no lab output or numeric claim failed."
)

with open("ledgers/E4/E4-c.json", "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("rows", len(rows), "pass", n_pass, "fail", n_fail, "unverifiable", n_unv)
