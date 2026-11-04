"""Builds ledgers/E4/E4-b.json for E4-b round 3 (rows, verdict, notes). Run with python -I from the checkout root."""
import json

OUT = "ledgers/E4/E4-b.json"
R3 = "ledgers/E4/scripts/E4-b-r3/outputs/"
CARRY = "Carried from round 2 (files byte-identical since the previous pin 67c47689): "


def row(rid, check, location, status, evidence, fix=""):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r


rows = [
    row("E4b-cmd-check_pages", "tools/check_pages.py --unit E4", "course/modules/E/E4/L04.html, L05.html, L06.html",
        "PASS", "Re-run at 67a2d13: 'check_pages E4: PASS', exit 0 (" + R3 + "check_pages_E4.txt)."),
    row("E4b-cmd-check_dag", "tools/check_dag.py --unit E4", "E4 DAG (L04-L06 links and definitions)",
        "PASS", "Re-run at 67a2d13: 'check_dag E4: PASS', exit 0 (" + R3 + "check_dag_E4.txt)."),
    row("E4b-cmd-check_projects", "tools/check_projects.py --unit E4", "E4 project (out of slice, unit gate)",
        "PASS", "Re-run at 67a2d13: 'check_projects E4: PASS', exit 0 (" + R3 + "check_projects_E4.txt)."),
    row("E4b-cmd-run_labs", "tools/run_labs.py --unit E4 (and --page L04, L05, L06)",
        "tests/labs/E4/lab-E4-L04-1.py, lab-E4-L05-1.py, lab-E4-L06-1.py", "PASS",
        "Re-run at 67a2d13: 'run_labs E4: PASS (12/12)'; per page L04, L05, L06 'PASS (1/1)' (" + R3 +
        "run_labs_E4.txt, run_labs_L04.txt, run_labs_L05.txt, run_labs_L06.txt)."),
    row("E4b-cmd-twins-isolated", "python -I -W error on each twin",
        "tests/labs/E4/lab-E4-L04-1.py, lab-E4-L05-1.py, lab-E4-L06-1.py", "PASS",
        "Re-run at 67a2d13 (" + R3 + "run_gates.sh twin_* lines): exit 0 for all three; stderr 0 bytes for each "
        "(checked again with 2> file: 0 bytes)."),
    row("E4b-cmd-page-code-equals-twin", "page lab code byte-identical to twin",
        "course/modules/E/E4/L04.html:120-240, L05.html:123-252, L06.html:241-~470", "PASS",
        "run_labs E4 PASS at 67a2d13 (byte identity is part of its check, " + R3 + "run_labs_E4.txt). The L06 twin "
        "docstring changed in this round and the embedded page code still matches."),
    row("E4b-cmd-expected-equals-output", "page expected block equals twin output",
        "course/modules/E/E4/L04.html:242-258, L05.html:254-279, L06.html:454-472", "PASS",
        "run_labs E4 PASS at 67a2d13 (" + R3 + "run_labs_E4.txt). Twin output of L06 printed and read: Parts A to E "
        "match the expected block (" + R3 + "../../../../../../ledgers is not used; see twin_L06 output in run_labs)."),
    row("E4b-cmd-ruff-mypy", "ruff check, ruff format --check, mypy --no-incremental on the three twins",
        "tests/labs/E4/lab-E4-L04-1.py, lab-E4-L05-1.py, lab-E4-L06-1.py", "PASS",
        "Re-run at 67a2d13: ruff check 'All checks passed!'; ruff format --check '3 files already formatted'; "
        "mypy --no-incremental 'Success: no issues found in 3 source files' (" + R3 + "ruff_check.txt, ruff_format.txt, "
        "mypy_twins.txt)."),
    row("E4b-cmd-pytest-labs", "pytest tests/test_labs.py tests/test_run_labs.py -k E4",
        "tests/test_labs.py, tests/test_run_labs.py", "PASS",
        "Re-run at 67a2d13 with -o addopts='' -v: 13 passed for -k E4 including lab-E4-L04-1, lab-E4-L05-1, "
        "lab-E4-L06-1 (" + R3 + "pytest_E4_only.txt); broader -k run 104 passed (" + R3 + "pytest_labs.txt)."),
    row("E4b-cmd-page_smoke", "tools/page_smoke.py --unit E4 --pages L04 L05 L06",
        "course/modules/E/E4/L04.html, L05.html, L06.html", "PASS",
        "Re-run at 67a2d13: 'page_smoke modules/E/E4/L04.html ... PASS', L05 PASS, L06 PASS; 'page_smoke E4: PASS', exit 0 ("
        + R3 + "page_smoke_L04_06.txt)."),
    row("E4b-cmd-verify_refs-live", "tools/verify_refs.py --unit E4 (live) and offline",
        "references/references.json (muth1961rational, mascolell1995microeconomic, milgrom1982information; used_by E4)",
        "PASS",
        "Live re-run this round: 'live re-verification of E4: 3 of 560 entries, 0 problems', exit 0 ("
        + R3 + "verify_refs_unit_E4_live.txt). Offline: 'offline integrity: 560 entries, 0 problems' (" + R3 +
        "verify_refs_offline.txt). git diff 67c47689..67a2d13 -- references notation tools is empty."),
    row("E4b-lab-L04-1", "Lab 1 of L04: twin reads, runs, output matches",
        "course/modules/E/E4/L04.html:117-260; tests/labs/E4/lab-E4-L04-1.py", "PASS",
        CARRY + "L04 lab section and twin are not in the delta; re-run now: run_labs PASS, twin exit 0, stderr 0 bytes (" +
        R3 + "run_labs_L04.txt, twin_lab-E4-L04-1.txt)."),
    row("E4b-lab-L05-1", "Lab 1 of L05: twin reads, runs, output matches, statements about it",
        "course/modules/E/E4/L05.html:120-281; tests/labs/E4/lab-E4-L05-1.py", "PASS",
        CARRY + "L05 lab section and twin are not in the delta; re-run now: run_labs PASS, twin exit 0, stderr 0 bytes ("
        + R3 + "run_labs_L05.txt)."),
    row("E4b-lab-L06-1-outputs", "Lab 1 of L06: printed outputs equal the expected block and the text about them",
        "course/modules/E/E4/L06.html:236-474; tests/labs/E4/lab-E4-L06-1.py", "PASS",
        "Re-verified at 67a2d13 (subject changed: docstring only). Twin output (" + R3 + "outputs; run "
        "'python -I -W error tests/labs/E4/lab-E4-L06-1.py') prints kappa 2, sig_eta2 2, tau_eta 1/2, tau_bar 3/4, theta_s 3/7, "
        "theta_u 6/7, var_p 27/49, cov 3/7, slope 7/9, posterior_var 2/3, rho2 1/3, 16/16 zero residuals, informed demand 1/7, "
        "alternative residual -9/85, sample slopes 0.426617 and 0.761928 within tolerance. run_labs PASS (expected block equal). "
        "Each value re-derived in exact arithmetic (" + R3 + "l06_checks.py, outputs/l06_checks.txt) and by hand from Example 6.9."),
    row("E4b-lab-L06-1-units", "L06 lab docstring units statement is dimensionally consistent with the model",
        "tests/labs/E4/lab-E4-L06-1.py:17-20; course/modules/E/E4/L06.html:257-260", "PASS",
        "Re-verified at 67a2d13. The docstring now says kappa and theta_u have units price per unit of the asset squared, "
        "because kappa*u and theta_u*u are prices per unit of the asset. Exponent check, money M and asset A, a has M^-1 "
        "(CARA on wealth in money), sig_e2 has (M/A)^2: kappa = a sig_e2 / lambda has (1,-2); theta_u*u has (1,-1), so "
        "theta_u has (1,-2); theta_s is (0,0). Output in " + R3 + "l06_checks.txt section 3. The round-2 FAIL is fixed."),
    row("E4b-lab-L06-1-residual-docstring", "residual() docstring matches its formulas",
        "tests/labs/E4/lab-E4-L06-1.py:88-89 (page L06.html:326-327)", "PASS",
        CARRY + "the residual() function and docstring (twin lines 74-106) are not in the delta. Recomputed the residual "
        "with exact arithmetic: additive and homogeneous in (s,u) with the price substituted (" + R3 + "l06_checks.txt section 1)."),
    row("E4b-lab-L06-1-hypothesis-xref", "hypothesis paragraph cross-references and values",
        "course/modules/E/E4/L06.html:238-240", "PASS",
        CARRY + "L06.html:240 is not in the delta. Its values were recomputed this round (Example 6.9 arithmetic and Part D "
        "residual -9/85 from twin output)."),
    row("E4b-L04-math-sec1", "Section 1 definitions, A1-A3, Definition 1.3, Lemma 1.2",
        "course/modules/E/E4/L04.html:64-96", "PASS",
        CARRY + "lines 64-96 are not in the delta (L04 delta hunks are at 349-352 and 524; " + R3 +
        "slice_delta_67c47689_67a2d13.diff)."),
    row("E4b-L04-math-lemma21", "Lemma 2.1 (elimination counts the rank)", "course/modules/E/E4/L04.html:100-104", "PASS",
        CARRY + "lines not in the delta; pivot argument re-read."),
    row("E4b-L04-math-examples", "Examples 2.2 and 2.3", "course/modules/E/E4/L04.html:106-115", "PASS",
        CARRY + "lines not in the delta; Example 2.2 and 2.3 re-derived."),
    row("E4b-L04-math-remark31", "Remark 3.1 (one security per state)", "course/modules/E/E4/L04.html:264-267", "PASS",
        CARRY + "lines not in the delta."),
    row("E4b-L04-math-remark32", "Remark 3.2 (redundancy and the kernel)", "course/modules/E/E4/L04.html:270-271", "PASS",
        CARRY + "lines not in the delta; kernel dimension 1 from rank-nullity (round-2 script independent_checks.py)."),
    row("E4b-L04-math-sec4", "Section 4: Assumption A4, Proposition 4.1, Proposition 4.2", "course/modules/E/E4/L04.html:278-294",
        "PASS", CARRY + "lines not in the delta."),
    row("E4b-L04-misconceptions", "Misconceptions section (L04)", "course/modules/E/E4/L04.html:297-317", "PASS",
        CARRY + "lines not in the delta."),
    row("E4b-L04-problems", "Problem set (L04), changed items re-verified", "course/modules/E/E4/L04.html:319-421", "PASS",
        "Re-verified at 67a2d13. P1 (L04.html:349-352) changed to 'using only Lemma 1.2 and Definition 1.3'. Its solution uses "
        "x = theta^T A so x in row(A) (Lemma 1.2), the row space of [A;x] equals row(A)+span(x) (Lemma 1.2 applied to [A;x]), and "
        "equal row spaces have equal dimension, which is rank (Definition 1.3). Only those are used: PASS. Other problems carried."),
    row("E4b-L04-quiz-q4", "Quiz item L04q4 (portfolios replicating (1,2,3))", "course/modules/E/E4/L04.html:467-475", "PASS",
        CARRY + "lines not in the delta; replicating family 1-t, 2-2t, 3-3t, t re-checked exactly (t = 0, 1, -3, 7/5)."),
    row("E4b-L04-quiz-rest", "Quiz items L04q1-q8", "course/modules/E/E4/L04.html:441-508", "PASS",
        CARRY + "lines not in the delta."),
    row("E4b-L04-why-empirical", "why-it-matters (L04) claims", "course/modules/E/E4/L04.html:51", "PASS",
        CARRY + "line 51 not in the delta."),
    row("E4b-grades-L04", "L04 grades and theorem titles", "course/modules/E/E4/L04.html:429-436 and 81-96", "PASS",
        CARRY + "grade spans not in the delta; every L04 T claim has a proof on the page (Theorem 1.4, Proposition 1.5, "
        "Corollary 1.6, Lemma 2.1, Proposition 4.1, 4.2 by grep of data-grade)."),
    row("E4b-struct-L04", "L04 structure, nav, header", "course/modules/E/E4/L04.html:2, 34-520", "PASS",
        CARRY + "header, sections and the Next nav (L04.html:520, text 'Rational-Expectations Equilibrium' equals L05 h1) "
        "unchanged. The footer is checked under E4b3-L04-footer; the nav label convention under E4b-nav-labels."),
    row("E4b-L05-math-sec1-2", "L05 Section 1-2: A1-A3, Definitions 1.1-1.2, Lemma 2.1, Proposition 2.2",
        "course/modules/E/E4/L05.html:64-98", "PASS", CARRY + "lines not in the delta."),
    row("E4b-L05-math-sec3", "L05 Section 3: Lemma 3.1 (error recursion)", "course/modules/E/E4/L05.html:102-118", "PASS",
        CARRY + "lines not in the delta."),
    row("E4b-L05-prop32", "Proposition 3.2 (when iteration converges)", "course/modules/E/E4/L05.html:108-112", "PASS",
        CARRY + "lines not in the delta."),
    row("E4b-L05-sec5-wording", "L05 Section 5 wording about convergence", "course/modules/E/E4/L05.html:293", "PASS",
        CARRY + "line 293 not in the delta (the changed Section 5 line is 294)."),
    row("E4b-L05-prop34-remark41", "Proposition 3.4 slot and Remark 4.1 wording", "course/modules/E/E4/L05.html:284-287",
        "PASS", CARRY + "lines not in the delta."),
    row("E4b-L05-notation-gamma", "gamma no longer used for supply response (notation)",
        "course/modules/E/E4/L05.html:66-68, 111 and tests/labs/E4/lab-E4-L05-1.py", "PASS",
        CARRY + "neither the cited lines nor the L05 twin are in the delta (grep for gamma/lambda in L05 finds none)."),
    row("E4b-L05-notation-s", "symbol s not reused with another meaning (L05 vs L06)",
        "course/modules/E/E4/L05.html:66; L06.html:57", "PASS", CARRY + "cited lines not in the delta."),
    row("E4b-L05-muth-markup", "attribution claim about Muth (1961) title", "course/modules/E/E4/L05.html:295", "PASS",
        CARRY + "line 295 not in the delta. Attribution checked: registry record muth1961rational title 'Rational Expectations "
        "and the Theory of Price Movements' (references/references.json), and the live verify_refs run re-resolved it "
        "(3 of 560 entries, 0 problems). The GRADE on this claim is a separate FAIL, E4b3-L05-footer-muth."),
    row("E4b-L05-math-muth-scope", "Muth claim scope ('used for the title only')", "course/modules/E/E4/L05.html:295", "PASS",
        CARRY + "line 295 not in the delta; the sentence states no Muth result. Muth (1961) itself not read (see notes)."),
    row("E4b-L05-misconceptions", "L05 misconceptions", "course/modules/E/E4/L05.html:299-315", "PASS",
        CARRY + "not in the delta."),
    row("E4b-L05-problems", "L05 problem set", "course/modules/E/E4/L05.html:317-420", "PASS", CARRY + "not in the delta."),
    row("E4b-L05-quiz", "L05 retrieval quiz", "course/modules/E/E4/L05.html:438-500", "PASS", CARRY + "not in the delta."),
    row("E4b-grades-L05", "L05 grades (key-results table and claim spans)", "course/modules/E/E4/L05.html:422-435 and 295",
        "FAIL",
        "The key-results table grades are consistent with the proofs, but the claim at L05.html:295 is graded T "
        "('The phrase rational expectations appears in the title of Muth (1961).'). BLUEPRINT §3 defines T as 'Theorem: proved "
        "on the page, or with a precisely cited proof'. A bibliographic title fact is neither a theorem nor a proof, so the "
        "grade does not fit (VERIFIER §2.3 re-grade: no BLUEPRINT grade matches a title fact).",
        "Remove the grade span from the Muth sentence at L05.html:295 and state it as a registry-backed fact with "
        "data-cite=muth1961rational and data-locator=title, or grade it as the BLUEPRINT grade that fits the evidence. "
        "Then fix the footer (E4b3-L05-footer-muth)."),
    row("E4b-struct-L05", "L05 structure", "course/modules/E/E4/L05.html:2, 34-505", "PASS",
        CARRY + "section order and nav (L05.html:510-511) unchanged; nav convention under E4b-nav-labels; footer under "
        "E4b3-L05-footer-muth."),
    row("E4b-L06-math-model", "Section 1 model: A1-A4, Assumption G, Definitions 6.1-6.2, Remark 6.5",
        "course/modules/E/E4/L06.html:55-92 and 160-163", "FAIL",
        "A4 paragraph (L06.html:86) changed this round. Its sentence 'For a fixed price, the residual is a linear function of "
        "(s, u) with no constant term' is false as written. In A4 the price is p = theta_s s - theta_u u, which varies with "
        "(s,u), so 'fixed price' has no referent. With the price held at a fixed p = 1 (base instance, theta fixed "
        "otherwise), the (s,u)-free part of the residual is -7/6, nonzero (" + R3 + "l06_checks.txt, line '2 (s,u)-free part "
        "of residual at fixed p=1: -7/6'). The substituted residual IS linear with no constant term (" + R3 +
        "l06_checks.txt section 1, additive and homogeneous; R(0,0)=0). The clearing argument is otherwise valid: a nonzero "
        "linear function vanishes on a line, a null set under the nondegenerate normal law of (s,u).",
        "Replace 'For a fixed price, the residual is a linear function of (s, u) with no constant term.' at L06.html:86 with "
        "'With the price rule p = theta_s s - theta_u u substituted (theta_s and theta_u fixed), the residual is a linear "
        "function of (s, u) with no constant term.' Edit with the same phrase in the quiz prompt at L06.html:715 (row "
        "E4b-L06-quiz-q12). No twin change is needed."),
    row("E4b-L06-lemma62", "Lemma 6.2 (CARA demand under normal beliefs)", "course/modules/E/E4/L06.html:96-124", "PASS",
        CARRY + "lines not in the delta; proof re-derived (MGF, g(x), unique minimiser)."),
    row("E4b-L06-lemma63", "Lemma 6.3 (informed beliefs)", "course/modules/E/E4/L06.html:128-143", "PASS",
        CARRY + "lines not in the delta. Also holds for any theta (the twin residual docstring relies on this, and the "
        "independence argument uses only that p is a function of (s,u))."),
    row("E4b-L06-lemma64", "Lemma 6.4 (uninformed beliefs are a linear projection)", "course/modules/E/E4/L06.html:146-157",
        "PASS", CARRY + "lines not in the delta."),
    row("E4b-L06-prop67-uniqueness", "Proposition 6.7 (b) uniqueness", "course/modules/E/E4/L06.html:190-204", "PASS",
        CARRY + "lines not in the delta; Steps 1-4 re-derived (Step 3 clearing identity and Q re-derived symbolically)."),
    row("E4b-L06-prop67-existence", "Proposition 6.7 (a) existence", "course/modules/E/E4/L06.html:206-209", "PASS",
        CARRY + "lines not in the delta."),
    row("E4b-L06-cor68", "Corollary 6.8", "course/modules/E/E4/L06.html:211-226", "PASS", CARRY + "lines not in the delta."),
    row("E4b-L06-example69-remark610", "Example 6.9 and Remark 6.10", "course/modules/E/E4/L06.html:228-236", "PASS",
        CARRY + "lines not in the delta; every Example 6.9 value re-derived this round (kappa 2, sig_eta2 2, tau_eta 1/2, "
        "tau_bar 3/4, theta 3/7 and 6/7, b 7/9, V_U 2/3, x_I 1/7, x_U -1/7)."),
    row("E4b-L06-misconceptions", "L06 misconceptions", "course/modules/E/E4/L06.html:~540-600", "PASS",
        CARRY + "not in the delta."),
    row("E4b-L06-problems-M", "L06 problem set, Mechanics", "course/modules/E/E4/L06.html", "PASS", CARRY + "not in the delta."),
    row("E4b-L06-problems-P", "L06 problem set, Proof", "course/modules/E/E4/L06.html", "PASS", CARRY + "not in the delta."),
    row("E4b-L06-problems-E", "L06 problem set, Empirical (E2 reads Lab 1 Part E)", "course/modules/E/E4/L06.html:580-588",
        "PASS", CARRY + "not in the delta; Part E is labelled SIMULATED."),
    row("E4b-L06-problems-R", "L06 problem set, Research", "course/modules/E/E4/L06.html", "PASS", CARRY + "not in the delta."),
    row("E4b-L06-quiz-q12", "Quiz item at L06.html:713-720 (the A4 question)", "course/modules/E/E4/L06.html:713-720", "FAIL",
        "The prompt at L06.html:715 reads 'For a fixed price, the clearing residual in A4 is a linear function of (s, u).' "
        "This premise is the same false statement as E4b-L06-math-model. The keyed option ('A nonzero linear function of (s,u) "
        "vanishes only on a line...') is correct, and the explanation (no constant term because demands and price are linear) "
        "is correct once the price rule is substituted. The prompt is wrong as written.",
        "Change the prompt at L06.html:715 to 'With the price rule p = theta_s s - theta_u u substituted, the clearing residual "
        "in A4 is a linear function of (s, u).' Keep the option and explanation as they are."),
    row("E4b-L06-A4-section3", "A4 pointer to Section 3 (dangling in round 2)", "course/modules/E/E4/L06.html:82-86", "PASS",
        "Re-verified at 67a2d13: the pointer '(Section 3, after Proposition 6.7)' is gone; L06.html:86 now gives the argument "
        "inline ('a line has probability zero because (s, u) has a nondegenerate normal law under A1'), and refers to "
        "Proposition 6.7 only for the coefficients, which is stated in Section 3. The round-2 FAIL is fixed. The wording defect "
        "in the same paragraph is E4b-L06-math-model."),
    row("E4b-L06-quiz-rest", "Quiz items L06q1-q10", "course/modules/E/E4/L06.html:644-709", "PASS",
        "Re-verified at 67a2d13 for items 1-10 (the A4 item is E4b-L06-quiz-q12): q1 3/7; q2 kappa = a sig_e2/lambda = 4 at a = 2 "
        "(a sig_e2 / lambda = 2/(1/2)); q3 sig_eta^2 2; q5 V_I 1/2; q6 sig_eta^2 rises with sig_u^2; q7 x_I = (1/2 - 3/7)/(1/2) "
        "= 1/7; q8 b = 7/9 vs p-on-s slope 3/7; q10 Var(v|p) = 2/3; the keyed answer 'Exactly one' is Proposition 6.7(b). "
        "Each value matches the twin output (" + R3 + "outputs/twin_lab-E4-L06-1.txt) and Example 6.9 arithmetic."),
    row("E4b-L06-why-uninformed-trading", "why-it-matters (L06) claims", "course/modules/E/E4/L06.html:51", "PASS",
        "Re-verified at 67a2d13 (line 51 changed: 'In this model a price can aggregate the information that investors hold'). "
        "Consistent with Remark 6.10 (uninformed observe v + eta, with eta noise) and Definition 6.1 (noise traders are a random "
        "net supply). The 'absorbs a supply of the asset that carries no payoff information' sentence is unchanged and matches "
        "Definition 6.1."),
    row("E4b-L06-dfn-informed-fraction-posterior", "first-use definitions (informed fraction, posterior)",
        "course/modules/E/E4/L06.html:57 and 96", "PASS", CARRY + "lines 57 and 96 not in the delta."),
    row("E4b-L06-grades", "L06 grades (key-results table)", "course/modules/E/E4/L06.html:621-627", "PASS",
        CARRY + "not in the delta. T rows are proved on the page (Lemma 6.2-6.4, Proposition 6.7, Corollary 6.8). C rows name "
        "Lab 1 Parts C-E and SIMULATED Part E."),
    row("E4b-struct-L06", "L06 structure, header, nav", "course/modules/E/E4/L06.html:2, 34-731", "PASS",
        "Re-verified at 67a2d13: header data-hours 8; h1 'Noisy rational-expectations equilibrium' equals the hub card and the "
        "L07 neighbour text; Previous 'Rational-Expectations Equilibrium' equals L05 h1. Next label convention is in E4b-nav-labels."),
    row("E4b-hub-titles", "hub card titles equal each lesson h1", "course/modules/E/E4/index.html:129-137 vs L01-L09 h1",
        "PASS",
        "Re-verified at 67a2d13. index.html:132 'Complete and Incomplete Markets' = L04.html:35 h1; index.html:133 "
        "'Rational-Expectations Equilibrium' = L05.html:35 h1; index.html:134 = L06 h1. Checked L01-L09 h1 against all nine "
        "card titles: all equal. The round-2 FAIL is fixed."),
    row("E4b-dag-closure", "DAG: no unlinked use before definition, links resolve", "L04-L06 text, math and labels", "PASS",
        "Re-run check_dag E4 PASS at 67a2d13 (" + R3 + "check_dag_E4.txt). The only concept link in the slice (crra-utility, "
        "L06.html:485) resolves."),
    row("E4b-concept-definitions", "concept definitions once, plain dfn terms",
        "course/modules/E/E4/L04.html:38,77; L05.html:73; L06.html:57-67, 96, 167", "PASS",
        CARRY + "cited lines not in the delta; check_dag E4 PASS at 67a2d13."),
    row("E4b-notation-registry", "notation registry: no reused registered symbol; new text adds no new symbol",
        "L04-L06 math segments; index.html:81-84", "PASS",
        "Re-verified at 67a2d13: grep finds no \\mathbb and no zeta in L04-L06; the A4 and nav edits add no symbol. "
        "notation/notation.json has no lambda, zeta or multiplier entry (grep), so the hub's Pq3 change from lambda to zeta "
        "(index.html:81-84) collides with nothing registered."),
    row("E4b-simulated-labels", "SIMULATED labels where seeded draws are used", "L06.html:238, 252, 469-473, 627", "PASS",
        "Re-verified at 67a2d13: Part E is labelled SIMULATED in the hypothesis, the twin docstring and the interpretation; "
        "grade C 'SIMULATED: Lab 1, Part E, one seed' at key-results. L04 and L05 use no random draws (grep)."),
    row("E4b-banned-process-words", "banned phrases and process words (learner-visible text)",
        "L04-L06 visible prose and docstrings", "PASS",
        "Re-verified at 67a2d13: check_pages E4 PASS (banned phrases). grep for builder, build, verifier, round, REQUESTS, unit report, "
        "TODO, TBD, obviously, clearly and the other BUILDER_RULES phrases over L04-L06 pages and twins: no hits."),
    row("E4b-page-width-360", "no horizontal scroll at 360 px", "L04.html, L05.html, L06.html", "PASS",
        "Re-run page_smoke L04-L06 at 67a2d13: PASS in light and dark, desktop and 360 px ("
        + R3 + "page_smoke_L04_06.txt)."),
    row("E4b-nav-labels", "lesson navigation labels follow one convention across the unit",
        "course/modules/E/E4/L04.html:519-520, L05.html:510-511, L06.html:734-735; L03.html:499; L07.html:604", "FAIL",
        "In L04-L06 the nav labels are the bare h1 text (L04.html:520 'Rational-Expectations Equilibrium', L05.html:510-511, "
        "L06.html:734-735 'Price informativeness'). Every other lesson uses 'Lnn · h1' (L01.html, L02.html, L03.html:499 "
        "'L04 · Complete and incomplete markets', L07.html:604 'L08 · The Grossman–Stiglitz paradox', L08.html, L09.html). "
        "So the unit has two conventions, and L03.html:499 differs from the L04 h1 in case ('Complete and incomplete markets' "
        "vs 'Complete and Incomplete Markets'). The round-2 fix (bare labels in L06) made the slice self-consistent, not the unit.",
        "Pick one convention for the unit. The majority is 'Lnn · h1' (L01-L03, L07-L09). Make the L04, L05 and L06 nav labels "
        "'Lnn · <h1 text>' and the L03.html:499 label 'L04 · Complete and Incomplete Markets' (out of slice). Re-run check_pages E4 "
        "and page_smoke E4 after the change."),
    # new rows (round 3)
    row("E4b3-L04-footer", "L04 footer claim matches its graded claims", "course/modules/E/E4/L04.html:524", "PASS",
        "Changed this round to 'Each graded result carries a proof or a lab result.' L04 has only T claims (grep data-grade), "
        "and each T claim has a proof on the page (Theorem 1.4, Proposition 1.5, Corollary 1.6, Lemma 2.1, Proposition 4.1, 4.2). "
        "True as written."),
    row("E4b3-L05-footer-muth", "L05 footer claim matches its graded claims", "course/modules/E/E4/L05.html:515 and 295", "FAIL",
        "The footer at L05.html:515 reads 'Each graded result carries a proof or a lab result.' The claim at L05.html:295 is "
        "graded T and carries a registry citation (data-cite=muth1961rational), but no proof and no lab result. So the footer is "
        "false for this page.",
        "Either re-grade or unmark the Muth claim (see E4b-grades-L05), or change the footer at L05.html:515 to 'Each graded "
        "result carries a proof, a lab result or a registry citation.' Do the same only where the page needs it (L04.html:524 "
        "and L06.html:739 can keep their wording)."),
    row("E4b3-L05-why-it-matters", "L05 why-it-matters (changed sentences)", "course/modules/E/E4/L05.html:51", "PASS",
        "Changed this round: 'Proposition 2.2 in Section 2' is correct (Proposition 2.2 is in Section 2, L05.html:87); "
        "'converges for every start only when varsigma < beta' is the statement of Proposition 3.2 (L05.html:109-112), which "
        "says convergence from every start holds when varsigma < beta and fails from some start when varsigma >= beta. "
        "The 'only when' is that converse. The lab checks the error ratio (Lemma 3.1, base ratio -1/4)."),
    row("E4b3-L05-definition12-traders", "L05 Section 5: 'traders in Definition 1.2 know the price rule...'",
        "course/modules/E/E4/L05.html:294", "PASS",
        "Changed this round from 'Lemma 2.1' to 'Definition 1.2'. Definition 1.2 (L05.html:72-74) requires m(z) = E[p_m | z] "
        "with p_m the price the market produces (Definition 1.1 gives p_m and the supply response varsigma), and A3 gives the "
        "shock law. Knowing the price rule, the shock distribution and the supply response is what the definition presupposes. "
        "PASS as a reading of the definition; the sentence does not claim more."),
    row("E4b3-L06-A4-linearity", "A4 residual: linear, homogeneous in (s,u) once the price rule is substituted",
        "course/modules/E/E4/L06.html:82-86; tests/labs/E4/lab-E4-L06-1.py:74-106 (residual)", "PASS",
        "Exact check (" + R3 + "l06_checks.py section 1, outputs/l06_checks.txt): residual(s1+s2,u1+u2) = residual(s1,u1) + "
        "residual(s2,u2) and residual(c s, c u) = c residual(s,u) for 200 random rational draws; residual(0,0) = 0. This is the "
        "mathematical content that the quiz and A4 need; the wording defect is E4b-L06-math-model."),
    row("E4b3-L06-A2-informed-observe", "A2 and the lab: informed investors observe s and p",
        "course/modules/E/E4/L06.html:72 (A2), :243-246 (page lab), tests/labs/E4/lab-E4-L06-1.py:5-7", "PASS",
        "Changed this round: the twin and the page both say 'A mass LAM of CARA investors ... observes s and the price p; the "
        "rest observe only the price p.' This matches A2 (L06.html:72) and the residual's informed demand E[v|s,p] = omega s "
        "(twin residual, Lemma 6.3). The round-2 wording ('observes s') was incomplete."),
    row("E4b3-hub-pq3", "hub question Pq3 (lambda renamed zeta)", "course/modules/E/E4/index.html:81-84", "PASS",
        "Changed this round from multiplier lambda to zeta, so the symbol lambda (informed fraction, E4 local) is not reused. "
        "The answer grad f = zeta grad g is the Lagrange condition of M7 (interior maximum, constraint gradient enters with a "
        "multiplier). No registry entry for zeta or lambda (notation/notation.json grep). PASS."),
]

frag = {
    "unit": "E4",
    "slice": "b",
    "round": 3,
    "round_note": "Round 3 of E4-b, independent verifier (did not build E4). Pin 67a2d13 (detached, full 67a2d13e7575608e95b2e34a9c7c2a82c61b117b). Previous pin 67c47689 (round-2 fragment /Users/billyribeiro/.fanout/frags/E-E4-b.round2.json, context only). Delta 67c47689..67a2d13 read hunk by hunk for L04, L05, L06, index.html and tests/labs/E4/lab-E4-L06-1.py (ledgers/E4/scripts/E4-b-r3/slice_delta_67c47689_67a2d13.diff, 170 lines). Round-2 rows re-verified where the subject changed or was previous non-PASS; others carried.",
    "verifier": "Haiku independent verifier, E4-b round 3",
    "pin": "67a2d13e",
    "base": "67c47689 (round-2 pin)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE3-E4-b",
    "scratch": "ledgers/E4/scripts/E4-b-r3/ (run_gates.sh, l06_checks.py, outputs/); /tmp copies of twin outputs only",
    "verified_at": "2026-11-04",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Mutants: none. Lab twins are demonstrations; mutation testing applies to project graders only (VERIFIER rules ruling; "
        "plans/E4-build-plan.md §2.1 item 14). No mutant files written for this slice.",
        "Commands run at 67a2d13 by ledgers/E4/scripts/E4-b-r3/run_gates.sh (outputs in ledgers/E4/scripts/E4-b-r3/outputs/). "
        "Live verify_refs --unit E4 run (3 of 560 entries, 0 problems). Round-2 'timeout' attempt failed (no timeout binary on this Mac) and was rerun with bash.",
        "Carried rows: the round-2 subjects of L04 (except P1 and footer), L05 (except line 51, 294, 515), and L06 (except lines 51, 86, 715, 735, twin docstring) are byte-identical since 67c47689 per the delta hunks. Round-2 scripts are in ledgers/E4/scripts/E4-b-r2 (slice_delta_1c1645f3_67c47689.diff, independent_checks.py).",
        "Round 2 non-PASS rows: E4b-lab-L06-1-units now PASS; E4b-L06-A4-section3 now PASS; E4b-hub-titles now PASS. New non-PASS in this round: E4b-L06-math-model, E4b-L06-quiz-q12 (the same 'fixed price' wording), E4b-grades-L05 and E4b3-L05-footer-muth (Muth claim graded T, footer contradicted). E4b-nav-labels stays FAIL, re-scoped to unit-level convention.",
        "Not checked: cards.json entries for L04-L06 (changed in the delta, 162 lines; assigned to the cards check in the plan, not this slice). L01-L03, L07-L09, index.html outside the card titles and Pq3, project and grader (changed in the delta; other slices). L03.html:499 and L07.html:604 nav text were read only to decide the convention; their fixes belong to their slices.",
        "Not checked: the Muth (1961) paper itself was not read (no abstract, no PDF); the claim is a title fact checked against the registry record and the live Crossref-based verify_refs run. Mas-Colell and Milgrom records are not cited in this slice's text beyond used_by.",
        "Observation (not a row): L05 uses varsigma (U+03C2, final sigma) for the supply response next to sigma_z, sigma_u and sigma_eta in the same equations. Glyphs are close. No registry or definition conflict exists (notation/notation.json has no varsigma). Consider a distinct symbol in a later round.",
        "Unit observation (not in this slice): the footer string 'Each graded result carries a proof or a lab result.' is written on every E4 lesson (L03.html:503, L07.html:608 too); the L05 instance is false because of the registry-cited T claim.",
    ],
    "summary": "E4-b round 3: FAIL. 79 rows: 74 PASS, 5 FAIL, 0 unverifiable. FAIL rows: E4b-L06-math-model and E4b-L06-quiz-q12 (A4 'for a fixed price' is false as written: the (s,u)-free part is -7/6 at p=1), E4b-grades-L05 and E4b3-L05-footer-muth (the Muth title claim is graded T with no proof or lab, and the footer says every graded result has one), E4b-nav-labels (two nav-label conventions across the unit). Round-2 FAILs fixed: units (L06 docstring), A4 section-3 pointer, hub titles.",
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(frag, f, indent=1, ensure_ascii=False)
    f.write("\n")
print("rows", len(rows), "fails", sum(1 for r in rows if r["status"] != "PASS"))
