"""Round-12 E4 slice b fragment writer. Starts from the round-11 fragment (row ids kept), updates each row's status and
evidence from the round-12 evidence, carries unchanged PASS rows with the carry prefix, and adds the new round-12 rows."""
import json
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE12-E4-b")
OUT = ROOT / "ledgers/E4/E4-b.json"
R11 = Path("/Users/billyribeiro/.fanout/frags/E-E4-b.round11.json")
S = "ledgers/E4/scripts/E4-b-r12"
prev = json.loads(R11.read_text(encoding="utf-8"))
rows_prev = {r["id"]: r for r in prev["rows"]}

CARRY = "Carried from round 11 ({files} byte-identical since the previous pin 11d7077): "

# id -> (status, evidence) for fresh rows; id -> (files, note) for carried rows
fresh = {
    "E4b11-cmd-check_pages": "tools/check_pages.py --unit E4 (and --page L04/L05/L06, --all): all PASS. Output: ledgers/E4/scripts/E4-b-r12/outputs/check_pages_*.txt (check_pages E4: PASS).",
    "E4b11-cmd-check_dag": "tools/check_dag.py --unit E4 and --all: PASS (outputs/check_dag_E4.txt, check_dag_all.txt).",
    "E4b11-cmd-check_projects": "tools/check_projects.py --unit E4: PASS (outputs/check_projects_E4.txt).",
    "E4b11-cmd-run_labs": "tools/run_labs.py --unit E4: run_labs E4: PASS (12/12) (outputs/run_labs_E4.txt).",
    "E4b11-cmd-twins-isolated": "python -I -W error on tests/labs/E4/lab-E4-L04-1.py, lab-E4-L05-1.py, lab-E4-L06-1.py run alone: exit 0 each, empty stderr (outputs/twin_L0x_isolated.txt).",
    "E4b11-cmd-page-code-equals-twin": "ledgers/E4/scripts/E4-b-r12/twin_page_check_r12.py (run with -I): page code equals twin modulo the trailing newline the HTML drops, for L04, L05, L06 (outputs/twin_page_check_r12.txt; code_equal_modulo_trailing_newline=True x3). Lab sections are byte-identical to round 11 (git diff 11d7077..5db69a9 has no hunk inside them).",
    "E4b11-cmd-expected-equals-output": "twin_page_check_r12.py: expected_equal_modulo_trailing_newline=True for L04, L05, L06 (outputs/twin_page_check_r12.txt).",
    "E4b11-cmd-ruff": "ruff check on the three twins and on the repository: All checks passed (outputs/ruff_twins.txt, ruff_repo.txt).",
    "E4b11-cmd-mypy": "mypy --no-incremental (repository: Success: no issues found in 385 source files; twins: 3 files) (outputs/mypy_full.txt, mypy_twins.txt).",
    "E4b11-cmd-pytest-labs": "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_page_smoke.py: exit 0, all PASSED (outputs/pytest_slice_summary_r12.txt; pytest_labs.txt, pytest_page.txt).",
    "E4b11-cmd-pytest-page": "same run as E4b11-cmd-pytest-labs (test_page_checks.py and test_page_smoke.py): exit 0 (outputs/pytest_slice_summary_r12.txt).",
    "E4b11-cmd-page_smoke": "tools/page_smoke.py --unit E4 --pages L04 L05 L06: page_smoke modules/E/E4/L04.html, L05.html, L06.html PASS; page_smoke E4: PASS (outputs/page_smoke_E4.txt).",
    "E4b11-cmd-verify_refs-offline": "tools/verify_refs.py --offline: offline integrity: 560 entries, 0 problems (outputs/verify_refs_offline.txt).",
    "E4b11-cmd-verify_refs-live": "tools/verify_refs.py --unit E4 (live Crossref): live re-verification of E4: 3 of 560 entries, 0 problems (outputs/verify_refs_unit_E4_live.txt).",
    "E4b11-cmd-render-diff": "tools/render_curriculum.py then git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json: both exit 0 (outputs/render_curriculum.txt, render_diff.txt; exit codes in outputs/_exit_codes.txt).",
    "E4b11-no-B1-B3-attribution": "grep -i 'grossman|stiglitz|muth' over L04.html, L05.html, L06.html: only L05.html:296 (muth, title only); no Grossman-Stiglitz citation or B1/B3 attribution. Cards L04-L06 read in full (cards_scan_r12.py): no such attribution.",
    "E4b11-rederive-numbers": "ledgers/E4/scripts/E4-b-r12/rederive_r12.py (exact Fractions, 3854 checks, 0 failures; outputs/rederive_r12.txt): Lemma 6.3 identities, Lemma 6.4 V_U closed form and positivity, Example 6.9 (kappa 2, sigma_eta^2 2, theta 3/7, 6/7, b 7/9, V_U 2/3, x_I 1/7, x_U -1/7), M1-M3 (theta 3/8, 3/2; Var(p) 27/32; b 4/9; V_U 5/6; corr^2 1/6; p -3/4; x_I 7/4; x_U 1/4), Prop 2.2 and Lemma 3.1 and Prop 3.3 identities, Lab L05 paths (E1 1025/256, E2 0,5 alternation, E3 35/4, 27/4), R1 limit identities, Prop 6.7 clearing identity at 4 points; E1/E2 decimal values of L06 against lab Part E (0.426617, 0.006497).",
    "E4b11-structure-scan": "L06.html:51 why-it-matters: 117 words (<=120, BUILDER 4.2; script: inline count). L04.html:51 and L05.html:51 unchanged since 11d7077. Section order of L04-L06 unchanged (check_pages PASS).",
    "E4b11-solutions-length": "ledgers/E4/scripts/E4-b-r12/solutions_len_r12.py -> outputs/solutions_len_r12.txt: L04 12 solutions 36-91 words; L05 12 solutions 33-99 words; L06 12 solutions 50-136 words (the R3 solution grew from 108 to 136 words). BUILDER_RULES sets no solution word limit (grep 'words' BUILDER_RULES.md: only the 120-word Why it matters rule), so this is a count, not a failure.",
    "E4b11-dag-closure": "tools/check_dag.py --unit E4 and --all: PASS (outputs/check_dag_E4.txt, check_dag_all.txt). The round-12 hunks add no data-concept link (git diff 11d7077..5db69a9 on L04-L06 shows no class=concept or data-concept change).",
    "E4b11-notation": "Macros used on L04-L06 are the registry macros (\\E \\Var \\Cov \\R \\Normal) or standard LaTeX/Greek letters; no registered symbol (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R_f, \\mathbb{Q}) appears on L04-L06 (grep); new round-12 symbols (V_U, V_I, Y, Psi, upsilon, kappa, eta) are already in use or defined in-lesson (Lemma 6.3, Remark 6.5, Prop 6.7 Step 2). notation/notation.json read in full (8 symbols, macros dict).",
    "E4b11-scope-words": "Re-read every round-12 hunk for scope words: L06.html:616 'all five follow from G' lists the five facts (checked against Lemmas 6.3 and 6.4 and Lemma 6.2's hypothesis); L06.html:81 'every pair (s, u)' is the A4 hypothesis; L05.html:59 'every trader observes' is the A2 text, consistent with Definition 1.1 (L05.html:66).",
    "E4b11-grades": "Re-graded every changed claim span: L05.html:427-429 (T, Lemma 2.1 / Prop 2.2 / Cor 2.3 proved on page); L06.html:628-634 (T, proved on page under stated hypotheses; the lab-based rows are C with basis named, 633 C finite check, 634 C SIMULATED). The T grade of the Lemma 6.3/6.4 and Prop 6.7 rows matches the proofs (checked line by line).",
    "E4b11-structure-order": "check_pages.py --unit E4: PASS; section order of L04, L05, L06 unchanged (no section added or moved in the round-12 hunks; diff hunks listed in notes).",
    "E4b11-L04-key-results": "Re-verified. L04.html:440 now reads 'Proposition 4.1, under A2 to A4', matching the statement 'Under A2 to A4' at L04.html:289 (A2 finitely many securities, A3 unrestricted holdings, A4 infinitely many states). The round-11 FAIL (A2 and A4) is fixed. Other rows 434-439, 441 re-read: Lemma 1.2, Thm 1.4, Prop 1.5, Cor 1.6, Examples 2.2/2.3 (lab Part A/B output: rank 2 incomplete, rank 3 complete), Prop 4.2.",
    "E4b11-L05-model": "L05.html:58-74 re-read. A2 renamed to '(affine forecasts)' (L05.html:59) and now matches the affine family of Lemma 2.1, Prop 2.2, Def 1.2. Definition 1.1 (L05.html:66-68): p_m = (alpha - varsigma m(z) - delta z + u - upsilon)/beta re-derived from clearing d(p)=q, with q = varsigma m(z)+delta z+upsilon: correct.",
    "E4b11-L05-lemma21-prop22-cor23": "L05.html:78-98 re-derived: Lemma 2.1 E[p_m|z]=(alpha-varsigma(c0+c1 z)-delta z)/beta and conditional variance (sigma_u^2+sigma_upsilon^2)/beta^2 (exact); Prop 2.2 fixed point c0*=alpha/(beta+varsigma), c1*=-delta/(beta+varsigma) (exact, rederive_r12.py); Cor 2.3 variances (proof step 'Var(p) = (c1*)^2 Var(z) + ...' correct under independence of z and (u-upsilon)/beta).",
    "E4b11-L05-problems": "L05.html:317-420 re-read, changed solution E2 (L05.html:384). M1 (alpha 12, beta 3, varsigma 1, delta 2: c0*=3, c1*=-1/2, Psi(c*)=c*), M2 (ratio -1/3 in both components), M3 (5/4), P1-P3 proofs, E1 (|e_5|=4/1024; 1025/256 sixth entry), E2 (0,5 alternation; 5/2 stays put; Psi(5/2)=5/2), E3 (c0*=2; e3=27/4; ratio -3/2), R1 (nu=1/2; damped step 5/2), R2 (c1*=0), R3 text: all re-derived in rederive_r12.py or by hand.",
    "E4b11-L05-key-results-quiz": "Table rows L05.html:427-429 re-verified (fresh, see E4b11-L05-model and E4b11-L05-problems). Quiz and remaining table rows (L05.html:430-432, 436-502) byte-identical since 11d7077: Carried from round 11 for those lines.",
    "E4b11-define-before-use": "Cited lines re-checked. L04.html:51, 66, 77 (unchanged); L05.html:59 (A2 'affine' defined inline, 'An affine function is a constant plus a multiple of z', line 59, and 'public signal' dfn); L05.html:73; L06.html:57, 67, 96, 169 (unchanged). The new V_U use-before-definition at L06.html:157 is a separate defect: E4b12-L06-VU-use-before-definition.",
    "E4b11-L06-why-it-matters": "L06.html:51 re-read: 'the price no longer reveals the signal exactly' (was 'payoff'); true under A1 (sigma_u^2>0 and the price p = theta_s s - theta_u u); word count 117 (<=120). Sections named exist (Definitions 6.1, 6.2; Assumptions A1 to A4 and G).",
    "E4b11-L06-model": "L06.html:56-92 re-read. A4 title now '(market clearing at every pair (s, u))' (L06.html:81) matches the hypothesis 'For every pair (s, u) in R^2' (L06.html:82). Clearing argument at L06.html:86 re-derived: residual linear in (s,u) with no constant term (CARA demands are linear in (s,p), E[v|s,p]=omega s, E[v|p]=bp); a nonzero linear form vanishes only on a line, which has probability zero under the nondegenerate normal law from A1.",
    "E4b11-L06-lemma63-proof": "L06.html:130 ('Assuming A1 and G') and the proof at L06.html:143 re-derived: Cov(e,s)=0, Cov(e,u)=0 by A1, e independent of (s,u) by G(ii), E[v|s,p]=omega s, Var(e)=sigma_v^2(1-omega)=V_I (exact); the appended sentence on conditional normality (V_I>0 from A1) is correct.",
    "E4b11-L06-lemma64": "L06.html:148 and proof at L06.html:157 re-derived: b=Cov(v,p)/Var(p)=theta_s sigma_v^2/Var(p); Var(v|p)=sigma_v^2 - b Cov(v,p); the appended V_U = sigma_v^2(theta_s^2 sigma_eps^2 + theta_u^2 sigma_u^2)/Var(p) > 0 is correct (rederive_r12.py, 300 random exact trials). The use-before-definition of the symbol V_U is a separate FAIL row (E4b12-L06-VU-use-before-definition).",
    "E4b11-L06-prop67": "L06.html:174 ('Assuming A1 to A4 and G') and the proof at L06.html:191-208 re-read: Steps 1-4 re-derived (theta_s != 0 via A4 at (1,0); Y=p/theta_s=s-kappa' u; Q theta_s=lambda tau_eps; Q theta_u=a; kappa'=kappa; existence check). Clearing identity checked exactly at 4 points for 100 random parameter sets (rederive_r12.py).",
    "E4b11-L06-cor68-slope-step": "L06.html:213 ('Assuming A1 to A4 and G') and proof at L06.html:225 re-read; E[v|p]=tau_eta p/(theta_s*(tau_v+tau_eta)), Var(v|p)=1/(tau_v+tau_eta)=sigma_v^2 sigma_eta^2/(sigma_v^2+sigma_eta^2); slope identity. Exact check in rederive_r12.py.",
    "E4b11-L06-example69": "L06.html:230 re-derived exactly: kappa=2, sigma_eta^2=2, tau_eta=1/2, tau_bar=3/4, theta_s=3/7, theta_u=6/7, b=7/9, V_U=2/3, x_I=1/7, x_U=-1/7, clearing 1/2*1/7+1/2*(-1/7)=0 (rederive_r12.py).",
    "E4b11-L06-problems": "L06.html:521-594 re-read and re-derived: M1 (kappa 4, sigma_eta^2 5, tau_eta 1/5, tau_bar 3/5, theta 3/8, 3/2), M2 (Var(p)=27/32, b=4/9, Var(v|p)=5/6, corr^2=1/6), M3 (p=-3/4, x_I=7/4, Y=-2, x_U=1/4, clears at u=1), P1-P3 proofs, E1 (0.44 SE), E2 (-0.30 tolerance, -0.90 SE from lab Part E values 0.426617 and 0.006497), E3 text. All numbers exact (rederive_r12.py).",
    "E4b11-L06-R1-corr-identity": "L06.html:598-602 (R1) re-derived: kappa -> infinity, tau_eta -> 0, theta_s* -> 0, Var(p)=theta_s^2(sigma_v^2+sigma_eta^2), Corr(v,p)^2=sigma_v^2/(sigma_v^2+sigma_eta^2) -> 0 (exact identity checked at 100 random parameter sets, rederive_r12.py).",
    "E4b11-L06-key-results-quiz": "Table rows L06.html:628-634 re-verified fresh: 628-629 (Lemmas 6.3/6.4, 'assuming A1 and G'), 630 (Prop 6.7, 'assuming A1 to A4 and G'), 631 (Cor 6.8, 'assuming A1 to A4 and G'), 632 (base-instance values 3/7, 6/7, 7/9, 2/3; lab Part A/B output: theta_s 3/7 theta_u 6/7 b 7/9 V_U 2/3), 633 (C; lab Part C grid_points 16 zero_residuals 16; Part D alternative slope 1/2 nonzero), 634 (C SIMULATED; lab Part E). Quiz and table text otherwise byte-identical since 11d7077 (carried).",
    "E4b11-cards-numbers-in-lesson": "ledgers/E4/scripts/E4-b-r12/cards_scan_r12.py: every number in a slice card's back appears in its lesson text (outputs/cards_scan_r12.txt; no NUMBER NOT IN LESSON lines).",
    "E4b11-cards-duplicate-scan": "cards_scan_r12.py over all 254 cards: 254 unique ids, no duplicate fronts, no duplicate backs (outputs/cards_scan_r12.txt). Slice cards: 105 (L04 33, L05 33, L06 39).",
    "E4b11-cards-process-words": "Regex scan (builder|verifier|round|agent|fragment|ledger|workflow|script|this slice) over L04-L06 cards and pages: only 'The lab checks' at L05.html (a description of Lab 1, not process language). PASS.",
}
carried = {
    "E4b11-muth-attribution": "course/modules/E/E4/L05.html:296 and references/references.json (muth1961rational)",
    "E4b11-L06-part-e-replica": "course/modules/E/E4/L06.html:478-479; tests/labs/E4/lab-E4-L06-1.py",
    "E4b11-L04-lemma21-assumptions": "course/modules/E/E4/L04.html:100-108",
    "E4b11-L04-lemma21-proof": "course/modules/E/E4/L04.html:108",
    "E4b11-L04-sec1-statements": "course/modules/E/E4/L04.html:62-96",
    "E4b11-L04-examples": "course/modules/E/E4/L04.html:111-115",
    "E4b11-L04-lab-1": "course/modules/E/E4/L04.html:117-265",
    "E4b11-L04-remarks": "course/modules/E/E4/L04.html:269-277",
    "E4b11-L04-canon-breaks": "course/modules/E/E4/L04.html:279-300",
    "E4b11-L04-misconceptions": "course/modules/E/E4/L04.html:302-321",
    "E4b11-L04-problems": "course/modules/E/E4/L04.html:324-427",
    "E4b11-L04-quiz": "course/modules/E/E4/L04.html:446-514",
    "E4b11-L04-why-it-matters": "course/modules/E/E4/L04.html:51",
    "E4b11-L04-references": "course/modules/E/E4/L04.html:516-520",
    "E4b11-L05-why-it-matters": "course/modules/E/E4/L05.html:51",
    "E4b11-L05-lemma31-proof": "course/modules/E/E4/L05.html:102-106",
    "E4b11-L05-lemma31-hypothesis": "course/modules/E/E4/L05.html:103-104",
    "E4b11-L05-prop32-33": "course/modules/E/E4/L05.html:108-118",
    "E4b11-L05-psi0-notation": "course/modules/E/E4/L05.html:402",
    "E4b11-L05-lab-1": "course/modules/E/E4/L05.html:120-282",
    "E4b11-L05-remark-canon-muth": "course/modules/E/E4/L05.html:292-296",
    "E4b11-L05-misconceptions": "course/modules/E/E4/L05.html:299-315",
    "E4b11-L05-references": "course/modules/E/E4/L05.html:504-507",
    "E4b11-L06-lemma62-proof": "course/modules/E/E4/L06.html:99-125",
    "E4b11-L06-lemma62-hypotheses": "course/modules/E/E4/L06.html:98-104",
    "E4b11-L06-remark-65-610": "course/modules/E/E4/L06.html:160-163; 233-236",
    "E4b11-L06-lab-1": "course/modules/E/E4/L06.html:238-481",
    "E4b11-L06-canon-breaks": "course/modules/E/E4/L06.html:483-493",
    "E4b11-L06-misconceptions": "course/modules/E/E4/L06.html:495-515",
    "E4b11-L06-references": "course/modules/E/E4/L06.html:727-731",
    "E4b11-L06-part-d-alt": "course/modules/E/E4/L06.html:474-475; tests/labs/E4/lab-E4-L06-1.py part_d",
    "E4b11-cards-L04": "course/modules/E/E4/cards.json: all 33 L04-lesson cards (object-identical to 11d7077)",
    "E4b11-cards-c120-basis": "course/modules/E/E4/cards.json E4-c120 and E4-c220 (object-identical)",
    "E4b11-lab-twin-structure": "tests/labs/E4/lab-E4-L04-1.py, L05-1, L06-1 (no change since 11d7077) and the page section ids",
    "E4b11-lab-l04-docstring": "tests/labs/E4/lab-E4-L04-1.py (module docstring, rank, attainable, main) and L04.html:119, 259",
    "E4b11-lab-l05-docstring": "tests/labs/E4/lab-E4-L05-1.py (module docstring, check_params, show, main)",
    "E4b11-lab-l06-docstring": "tests/labs/E4/lab-E4-L06-1.py (module docstring lines 1-23, part_d, main)",
    "E4b11-simulated-labels": "course/modules/E/E4/L06.html:240, 255, 480, 633-634; cards E4-c124, E4-c125",
}
mixed_carry_note = {
    "E4b11-L05-key-results-quiz",
    "E4b11-L06-key-results-quiz",
}
notes_for_carry = {"E4b11-muth-attribution": "L05.html:296 unchanged"}

fail_rows = {
    "E4b11-cards-L05": "FAIL. The L05 card set contains E4-c076, whose front still names the A2 title '(linear forecasts)' while L05.html:59 now titles A2 '(affine forecasts)'. See E4b12-card-c076.",
    "E4b11-cards-L06": "FAIL. The L06 card set contains E4-c106, whose front still names the A4 title '(market clearing in every state)' while L06.html:81 now titles A4 '(market clearing at every pair (s, u))'. See E4b12-card-c106.",
}
fix_for = {
    "E4b11-cards-L05": "Change the E4-c076 front to the current title (see E4b12-card-c076). Then this row is PASS.",
    "E4b11-cards-L06": "Change the E4-c106 front to the current title (see E4b12-card-c106). Then this row is PASS.",
}

out_rows = []
for rid, r in rows_prev.items():
    nr = {"id": rid, "check": r["check"], "location": r["location"]}
    if rid in fresh:
        nr["status"] = "PASS"
        nr["evidence"] = fresh[rid]
    elif rid in carried:
        nr["status"] = "PASS"
        nr["evidence"] = CARRY.format(files=carried[rid]) + "round-11 evidence: " + r["evidence"]
    elif rid in fail_rows:
        nr["status"] = "FAIL"
        nr["evidence"] = fail_rows[rid] + " Round-11 evidence was: " + r["evidence"]
        nr["fix"] = fix_for[rid]
    elif rid == "E4b11-define-before-use":
        nr["status"] = "PASS"
        nr["evidence"] = CARRY.format(files="course/modules/E/E4/L04.html:51,66,77; L05.html:73; L06.html:57,67,96,169") + "round-11 evidence: " + r["evidence"] + " L05.html:59 re-checked fresh (affine defined inline). The new V_U use at L06.html:157 is E4b12-L06-VU-use-before-definition (FAIL)."
    elif rid == "E4b11-L06-lemma62-hypotheses":
        raise SystemExit("unexpected")
    else:
        raise SystemExit(f"row without round-12 decision: {rid}")
    out_rows.append(nr)

# the L05/L06 mixed rows: the note is in evidence already
new_rows = [
    {
        "id": "E4b12-card-c076",
        "check": "2.7-cards / 2.9-prose (cards agree with current lesson text)",
        "location": "course/modules/E/E4/cards.json:575-578 (id E4-c076, front at line 577); lesson course/modules/E/E4/L05.html:59",
        "status": "FAIL",
        "evidence": "Card E4-c076 front: 'Assumption A2 (linear forecasts) of the L05 model: what family of forecasts is searched?' The current L05.html:59 reads '<strong>A2 (affine forecasts).</strong>' (changed in 5db69a9, ccaeeaf4 delta; diff 11d7077..5db69a9 on L05.html:58-59). Command: grep -n -i 'linear forecast' course/modules/E/E4/L05.html returns nothing; grep -n -i 'linear forecast' course/modules/E/E4/cards.json returns E4-c076 only. Its back ('The affine family ...') already uses affine. Mismatch of the assumption title with the lesson.",
        "fix": "In course/modules/E/E4/cards.json, change the E4-c076 front to: 'Assumption A2 (affine forecasts) of the L05 model: what family of forecasts is searched?' Regenerate nothing else; re-run tools/check_pages.py --unit E4 and the round-12 cards scan.",
    },
    {
        "id": "E4b12-card-c106",
        "check": "2.7-cards / 2.9-prose (cards agree with current lesson text)",
        "location": "course/modules/E/E4/cards.json:796-799 (id E4-c106, front at line 798); lesson course/modules/E/E4/L06.html:80-81",
        "status": "FAIL",
        "evidence": "Card E4-c106 front: 'Assumption A4 (market clearing in every state): what does it require?' The current L06.html:81 reads '<span class=\"name\">(market clearing at every pair \\((s, u)\\))</span>' (changed in the round-12 delta, diff 11d7077..5db69a9 at L06.html:81). The card back ('For every pair (s, u) in R^2 ...') agrees with L06.html:82; only the assumption title is stale.",
        "fix": "In course/modules/E/E4/cards.json, change the E4-c106 front to: 'Assumption A4 (market clearing at every pair (s, u)): what does it require?'",
    },
    {
        "id": "E4b12-L06-VU-use-before-definition",
        "check": "2.4-notation / 2.9-prose (terms used before definition; BUILDER define-before-use)",
        "location": "course/modules/E/E4/L06.html:157 (proof of Lemma 6.4, new sentence); first definition of V_U at L06.html:162 (Remark 6.5)",
        "status": "FAIL",
        "evidence": "The round-12 proof sentence 'the conditional law of v is normal with mean bp and variance V_U, as Lemma 6.2 requires. Here V_U = sigma_v^2(theta_s^2 sigma_eps^2 + theta_u^2 sigma_u^2)/Var(p) > 0' uses V_U before any definition: grep -n 'V_U' course/modules/E/E4/L06.html shows the first occurrence at line 157 and the Lemma 6.4 statement (L06.html:148-152) defines only Var(v|p) = sigma_v^2 - b Cov(v,p), without naming V_U. The closed form and the positivity are correct (rederive_r12.py, 300 random exact trials), so only the ordering is at fault.",
        "fix": "In L06.html:152, name the variance in the statement, for example 'and \\(\\Var(v \\mid p) = \\sigma_v^2 - b\\,\\Cov(v, p) =: V_U\\)', or move the 'Here V_U = ...' clause ahead of the first use in the paragraph at L06.html:157. Then re-run tools/check_pages.py --page L06 and tools/page_smoke.py --unit E4 --pages L06.",
    },
    {
        "id": "E4b12-cards-split-review",
        "check": "2.7-cards (atomic cards; no duplicates after the round-12 splits)",
        "location": "course/modules/E/E4/cards.json: pairs E4-c081/c251, E4-c083/c252, E4-c113/c253, E4-c116/c254, E4-c119/c255",
        "status": "PASS",
        "evidence": "Round-12 splits each compound card into two single-question cards. Each pair asks different questions (E[p_m|z] vs conditional law; fixed point vs price; E[v|p] vs Var(v|p); E[v|p] coefficient at equilibrium vs its numerical ask; base slope vs base posterior variance). Each back is checked against its lesson: L05.html:82, 90, L06.html:152, 215, 220, 230-231. Note, not a fail: E4-c254 ('b = tau_eta/(theta_s*(tau_v+tau_eta))') restates the coefficient in E4-c116's back as a separate question; the two fronts differ, so this is not a duplicate. cards_scan_r12.py: 254 unique ids, no duplicate fronts or backs.",
    },
    {
        "id": "E4b12-L06-research-R2-R3",
        "check": "2.4-mathematics / 2.9-problem-set (research problems R2 and R3, changed R3 solution)",
        "location": "course/modules/E/E4/L06.html:606-616 (R2 at 606-609, R3 at 613-616)",
        "status": "PASS",
        "evidence": "R2 (Var(v|p) strictly increasing in sigma_u^2): the chain sigma_u^2 -> sigma_eta^2 (kappa>0 independent of sigma_u) -> tau_eta strictly decreasing -> 1/(tau_v+tau_eta) strictly increasing is correct (rederive_r12.py cross-check of the closed form). R3 solution (L06.html:616, changed in round 12) names the steps of Lemmas 6.3 and 6.4 that use G, the four facts of Prop 6.7 and the fifth fact of Lemma 6.2; each fact follows from G with A1 (proofs at L06.html:143 and 157); no claim about other payoff laws.",
    },
]

frag = {
    "unit": "E4",
    "slice": "b",
    "round": 12,
    "verifier": "Haiku independent verifier, E4-b round 12 (did not build E4; no shared context with builders)",
    "pin": "5db69a9bee460736c318ebfacc7200ee5a6eb0f0 (detached; checkout /Users/billyribeiro/.fanout/wt/verifyE12-E4-b)",
    "base": "11d7077a290f7960b183d3a5a6631af4773888f9 (round-11 pin; round-11 fragment /Users/billyribeiro/.fanout/frags/E-E4-b.round11.json used as context: its PASS rows were carried only where the cited subject is byte-identical, otherwise re-verified; its FAIL row E4b11-L04-key-results is re-verified PASS)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE12-E4-b",
    "scratch": f"{S}/ (run_commands_r12.sh, twin_page_check_r12.py, rederive_r12.py, cards_scan_r12.py, solutions_len_r12.py, write_fragment_r12.py; outputs/ holds every command output)",
    "verified_at": "2026-11-05T12:00:00Z",
    "verdict": "FAIL",
    "rows": out_rows + new_rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Round-12 delta, git diff 11d7077a..5db69a9 for slice b: L04.html:440 (one table cell); L05.html:59 (A2 title), 384 (E2 solution sentence), 427-429 (key-results rows); L06.html:51 (why-it-matters word), 81 (A4 title), 130 and 143 (Lemma 6.3 'Assuming' and appended conditional-normality sentence), 148 and 157 (Lemma 6.4 'Assuming' and appended V_U paragraph), 174 (Prop 6.7 'Assuming'), 213 (Cor 6.8 'Assuming'), 616 (R3 solution), 631-632 (key-results rows); cards.json: changed E4-c081, c083, c113, c116, c119, c229 and added c251 to c255 (L05 and L06 slice cards; c256-c260 are L08, outside this slice). Twins lab-E4-L04-1, L05-1, L06-1: unchanged since 11d7077.",
        "Outside the slice but changed in the same delta (not checked here): curriculum/02-economics-finance-core.yaml and curriculum.json (Arbitrage scanner brief, 'embedded' -> 'SIMULATED'); course/assets/data/program.json (same brief); course/modules/E/E4/index.html:63 (hub concept paragraph); L01-L03, L07-L09, project.html, grader/*, tests/labs/E4/lab-E4-L01-1.py and lab-E4-project-3.py, and cards outside the slice.",
        "Not a row but recorded: the L05 E2 solution (L05.html:384) states that the c0 path 'stays put at 5/2'; read as the starting point the question asks for, consistent with Psi(5/2)=5/2 (rederive_r12.py). Non-blocking.",
        "Not a row but recorded: L06 Lemma 6.2 still says 'Assume A3'; Lemma 6.3/6.4/Prop 6.7/Cor 6.8 now say 'Assuming'. Style only; not a defect.",
        "Not a row but recorded: L06 R3 solution grew from 108 to 136 words (solutions_len_r12.txt). BUILDER_RULES sets no solution word limit.",
        "Not a row but recorded: the round-12 Lemma 6.4 proof (L06.html:157) also says 'Here V_U ...' with V_U = Var(v|p) by Remark 6.5's definition; the ordering defect is the only issue (row E4b12-L06-VU-use-before-definition).",
        "Not checked: lessons L01-L03, L07-L09 and the hub's other sentences; the project, grader and their mutants (outside slice b, ruled out by the slice assignment); the Muth (1961) article body (title only, per the page); a browser run of Pyodide (page_smoke was run, not a hand browser session); the MANIFEST and snapshot hashes (fetch_data --check passed, outputs/fetch_data_check.txt); the other slices' cards (only id uniqueness and duplicates were checked).",
        "Mutants: none. Slice b is lesson text and lab twins; per the ruling, lab twins are demonstrations and mutation testing applies to project graders only.",
        "Access: the live verify_refs run used the tool's own plain Crossref requests; no bot check, login or paywall was touched.",
    ],
    "summary": "FAIL E4-b round 12 at 5db69a9: rows=%d. Non-PASS: E4b11-cards-L05 and E4b11-cards-L06 (set rows, cite the two defective cards), E4b12-card-c076 (A2 title '(linear forecasts)' vs L05.html:59 '(affine forecasts)'), E4b12-card-c106 (A4 title '(market clearing in every state)' vs L06.html:81 '(market clearing at every pair (s, u))'), E4b12-L06-VU-use-before-definition (L06.html:157 uses V_U before its definition). Round-11 FAIL E4b11-L04-key-results is fixed (L04.html:440 'A2 to A4' matches Prop 4.1 at L04.html:289). Every command gate passes at 5db69a9.",
}
frag["summary"] = frag["summary"] % len(frag["rows"])
OUT.write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", len(frag["rows"]), "pass", sum(r["status"] == "PASS" for r in frag["rows"]), "fail", sum(r["status"] == "FAIL" for r in frag["rows"]))
