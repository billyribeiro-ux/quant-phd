# Builds ledgers/E4/E4-b.json (round 1, verifier F31) from the round-13 base fragment and this round's evidence.
import json, datetime
ROOT = "/Users/billyribeiro/.fanout/wt/verifyF31-E4-b"
BASE = "/Users/billyribeiro/.fanout/frags/E-E4-b.round13.json"
OUT = ROOT + "/ledgers/E4/E4-b.json"
S = "ledgers/E4/scripts/E4-b-r1/outputs/"
base = json.load(open(BASE, encoding="utf-8"))
brows = {r["id"]: r for r in base["rows"]}
PREV = "e919577b"

def carry(files, rid):
    return f"Carried from round 13 ({files} byte-identical since the previous pin {PREV}): " + brows[rid]["evidence"]

# ---- re-run command rows (this round, on 95f3f8cb)
RERUN = {
 "E4b11-cmd-check_pages": f"Re-run: check_pages.py --unit E4 -> 'check_pages E4: PASS'; check_pages.py --unit E4 --page L04 / L05 / L06 -> PASS each ({S}check_pages_E4.txt, check_pages_L04.txt, check_pages_L05.txt, check_pages_L06.txt).",
 "E4b11-cmd-check_dag": f"Re-run: check_dag.py --unit E4 -> 'check_dag E4: PASS' ({S}check_dag_E4.txt); check_dag.py --all -> 28 lines, all PASS, exit 0 ({S}check_dag_all.txt). Data-concept link sets of L04, L05 and L06 are md5-identical at e919577b and HEAD.",
 "E4b11-cmd-check_projects": f"Re-run: check_projects.py --unit E4 -> 'check_projects E4: PASS', exit 0 ({S}check_projects_E4.txt). Context only; slice b has no project.",
 "E4b11-cmd-run_labs": f"Re-run: run_labs.py --unit E4 -> 'run_labs E4: PASS (12/12)', exit 0 ({S}run_labs_E4.txt).",
 "E4b11-cmd-twins-isolated": f"Re-run: .venv/bin/python -I -W error tests/labs/E4/lab-E4-L04-1.py, lab-E4-L05-1.py and lab-E4-L06-1.py: exit 0 each, stderr empty ({S}twin_L04.out, twin_L05.out, twin_L06.out, *.err).",
 "E4b11-cmd-page-code-equals-twin": f"Re-run: twin_page_check_r1.py (outputs/twin_page_check_r1.txt): the code block of L04.html, L05.html and L06.html equals the twin file, ignoring the final newline the embed omits (L04 121 lines, L05 131, L06 219). The changed L06 hunks (lines 62, 86, 143, 157, 202, 552, 663, 722) lie outside L06.html:241-460.",
 "E4b11-cmd-expected-equals-output": f"Re-run: twin_page_check_r1.py: the expected block of each page equals the twin's stdout (rstrip) for L04 (942 chars), L05 (1611) and L06 (809) ({S}twin_page_check_r1.txt).",
 "E4b11-cmd-ruff": f"Re-run: ruff check and ruff format --check on the three twins ('All checks passed!', '3 files already formatted', {S}ruff_twins.txt); ruff check . ('All checks passed!') and ruff format --check . ('555 files already formatted'), exit 0 ({S}ruff_repo.txt).",
 "E4b11-cmd-mypy": f"Re-run: mypy --no-incremental on the three twins: 'Success: no issues found in 3 source files' ({S}mypy_twins.txt); on the repository: 'Success: no issues found in 386 source files', exit 0 ({S}mypy_repo.txt).",
 "E4b11-cmd-pytest-labs": f"Re-run: pytest tests/test_labs.py tests/test_run_labs.py -q: all dots, exit 0 ({S}pytest_labs.txt).",
 "E4b11-cmd-pytest-page": f"Re-run: pytest tests/test_page_checks.py tests/test_page_smoke.py -q: all dots, exit 0 ({S}pytest_page.txt).",
 "E4b11-cmd-page_smoke": f"Re-run: page_smoke.py --unit E4 --pages L04 L05 L06 -> 'page_smoke E4: PASS', exit 0 ({S}page_smoke_E4_L04-L06.txt).",
 "E4b11-cmd-verify_refs-offline": f"Re-run: verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 ({S}verify_refs_offline.txt).",
 "E4b11-cmd-verify_refs-live": f"Re-run: verify_refs.py --unit E4 (plain tool requests, live) -> 'live re-verification of E4: 3 of 560 entries, 0 problems', exit 0 ({S}verify_refs_live_E4.txt). No bot check, login or paywall touched.",
 "E4b11-cmd-render-diff": f"Re-run: render_curriculum.py regenerates CURRICULUM.md and curriculum/curriculum.json with exit 0 and no working-tree change; git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json exit 0 ({S}render_curriculum.txt, render_diff.txt). The M3 brief edit in curriculum/01-foundations.yaml is reflected in both committed files.",
}

RE_VERIFIED = {
 "E4b11-no-B1-B3-attribution": f"Re-verified: prose_scans_r1.txt gives 'B1/B3 hits: 0' for L04, L05 and L06 visible text. Cards: the B1/B3 matches in cards.json (E4-c189, c191, c196-c199, c209, c210) are all lesson L09, outside slice b; no L04-L06 card matches.",
 "E4b11-rederive-numbers": f"Re-derived with exact Fractions (rederive_r1.py, {S}rederive_r1.txt): 400 random exact trials of the L06 model (Lemma 6.3, 6.4, Prop 6.7 Step 3, Cor 6.8) with 0 failures; Example 6.9 gives kappa 2, sigma_eta^2 2, tau_eta 1/2, tau_bar 3/4, theta_s 3/7, theta_u 6/7, Var(p) 27/49, b 7/9, V_U 2/3, x_I(1,0) 1/7, x_U(1,0) -1/7, residual 0, and residual -9/85 at theta_s 1/2.",
 "E4b11-L06-part-e-replica": "Re-verified: L06.html:478-479 read in the expected block: 'p_on_s slope 0.426617 population 0.428571 tolerance 0.006497 within True' and 'v_on_p slope 0.761928 population 0.777778 tolerance 0.023538 within True'; the same lines are printed by the unchanged twin (twin_L06.out). L06.html:240 and 480 label Part E SIMULATED (seed 6, 20000 draws); no data read.",
 "E4b11-structure-scan": f"Re-verified: structure_scan_r1.txt versus the round-11 output: identical for L04 and L05; for L06 only the solution word counts differ (the changed P1 solution). Tag skeletons of L04, L05 and L06 are identical at e919577b and HEAD (skeleton_diff_r1.txt: 852, 752 and 922 tags).",
 "E4b11-structure-order": f"Re-verified: tag skeletons identical (skeleton_diff_r1.txt), so section order, ids, classes and block sequence are unchanged in L04, L05 and L06; only text inside existing blocks changed (L06 only).",
 "E4b11-solutions-length": f"Re-verified: no length limit in BUILDER_RULES (grep 'solution' finds none). Word counts from prose_scans_r1.txt: L04 min 13 / max 91, L05 33 / 99, L06 50 / 136 (12 solutions per page); the changed L06 P1 solution is inside these bounds.",
 "E4b11-dag-closure": f"Re-verified: check_dag E4 PASS (outputs/check_dag_E4.txt); data-concept link sets of L04, L05 and L06 are md5-identical at e919577b and HEAD; the new text adds no concept link (L06 has 15 links before and after).",
 "E4b11-notation": f"Re-verified: prose_scans_r1.txt 'registered-symbol hits in math: []' for L04, L05, L06. The new symbols G(i) and G(ii) are the two parts of the assumption labelled G (L06.html:90-92), and G is not a notation.json entry. Observation (not a ruling-26 kind): G also names the gain G(lambda) of L08 (L08.html:234); see notes.",
 "E4b11-define-before-use": "Re-verified: V_U is defined by '=:' in the Lemma 6.4 statement at L06.html:152 and first used at 157 (proof) and later; b is defined at L06.html:150 before use at 152. New forward pointer at L06.html:62 ('by the linear-image fact G(i) stated below', Assumption G at 90-92) is an explicit pointer, not a ruling-26 kind; see E4b-r1-A1-forward-G-pointer.",
 "E4b11-scope-words": "Re-verified: scope-word counts unchanged from round 13 (prose_scans_r1.txt: L04 61, L05 50, L06 48). The changed L06 scope phrases ('every pair (s, u)' in A4, 'every real theta_s' in P1, 'at each pair') are quantified statements under A4 or Proposition 6.7 and were read in context.",
 "E4b11-grades": "Re-verified: grades of Lemma 6.3, Lemma 6.4, Proposition 6.7 and Corollary 6.8 (T, L06.html:129, 146, 174, 210 region) and the key-results table rows L06.html:628-632 are unchanged; the new citations of G(i)/G(ii) in the proofs (lines 143 and 157) support the stated 'assuming A1 and G' hypotheses.",
 "E4b11-lab-twin-structure": "Re-verified: the three twins are byte-identical at e919577b and HEAD (git diff --quiet, exit 0 each); the lab sections of L04, L05 and L06 have identical tag skeletons (skeleton_diff_r1.txt).",
 "E4b11-L06-model": "Re-verified (L06.html:56-92): changed line 62 (A1 now says '(v, s, u) is jointly normal, by the linear-image fact G(i) stated below'; correct, since (v, s, u) is a linear image of (v, eps, u)) and changed line 86 (A4 proof: residual evaluated at (1,0) and (0,1); the residual is a linear function with no constant term, checked in rederive_r1.txt). Definition 6.1 and A2 read in full; no defect.",
 "E4b11-L06-lemma63-proof": "Re-verified (L06.html:129-144): changed line 143 'The vector (e, s, u) is jointly normal by A1 and G(i)' is correct ((e,s,u) is a linear image of (v, eps, u)); pairwise zero covariances Cov(e,s)=0, Cov(e,u)=0, Cov(s,u)=0 give independence by G(ii); Var(e) = sigma_v^2(1 - omega) = V_I is re-derived (rederive_r1.py, 'lemma 6.3' check, 0 failures).",
 "E4b11-L06-lemma64": "Re-verified (L06.html:146-158): changed line 157 'jointly normal by A1 and G(i)' is correct ((e,p) is a linear image of (v, s, u)); G(ii) gives e independent of p; V_U = sigma_v^2 - b Cov(v,p) equals sigma_v^2 (theta_s^2 sigma_eps^2 + theta_u^2 sigma_u^2)/Var(p) since sigma_v^2 Var(p) - theta_s^2 sigma_v^4 = sigma_v^2 (theta_s^2 sigma_eps^2 + theta_u^2 sigma_u^2).",
 "E4b11-L06-prop67": f"Re-verified (L06.html:172-209): changed line 202 (Step 3) now evaluates the residual at (1,0) and (0,1) to get Q theta_s = lambda tau_eps and Q theta_u = a. The residual (lambda tau_eps - Q theta_s) s + (Q theta_u - a) u is correct; the Step 4 solving is unchanged and consistent. rederive_r1.py: Step 3 identities hold at the closed form in 400 exact trials, 0 failures.",
 "E4b11-L06-problems": "Re-verified (L06.html:521-594): changed P1 solution at line 552 is correct (Lemma 6.3 uses A1 and G(i) for joint normality, G(ii) for independence; no other use); M, E and R problems are on unchanged lines and carried by byte identity of their lines (no hunk outside 552).",
 "E4b11-L06-key-results-quiz": "Re-verified (L06.html:622-725): changed quiz option L06q4 at line 663 ('so by G it is independent of (s, p), and it has mean zero') is the single correct option and the distractors stay wrong; changed explanation at line 722 (Step 3 evaluates at two points) agrees with L06.html:202. Key-results rows 628-632 unchanged.",
 "E4b11-cards-L04": "Re-verified against the unchanged L04.html text: changed E4-c058 (Theorem 1.4, L04.html:81-82: complete iff rank(A) = S), E4-c227 (pivot = first nonzero entry of a nonzero row, Lemma 2.1, L04.html:107), E4-c228 (closed under nonnegative combinations, Proposition 4.2, L04.html:296-297); new E4-c261 (strictly increasing pivot columns, Lemma 2.1) and E4-c268 (complete market, Definition 1.3, L04.html:76-77). Other 30 L04 cards byte-identical (card_delta_r1.txt). L04 has 35 cards.",
 "E4b11-cards-L05": "Re-verified against the unchanged L05.html text: E4-c076 (A2 affine family, L05.html:59); E4-c090 (c0* = 4, c1* = -3/10 = alpha/(beta+varsigma), -delta/(beta+varsigma); Lab Part A prints 'fixed_point c0 4 c1 -3/10'); E4-c097 (Proposition 3.2: varsigma >= beta and a start off the fixed point gives an error that does not go to zero; L05.html:109-111); E4-c251 (Lemma 2.1 proof: p_m = g(z) + (u - upsilon)/beta, independent normal shocks, A3). New E4-c263 (Lab Part A 'residual_c0 0 residual_c1 0'). Other 30 L05 cards byte-identical. L05 has 34 cards.",
 "E4b11-cards-L06": "FAIL. E4-c127 (cards.json:950-955) basis changed from 'Definition 6.1 and A1' to 'Definition 6.1 and A2'. Its back claims (T) that a noise trader is 'a random supply u that is independent of the payoff'; that independence is Assumption A1 ('mutually independent', L06.html:62). Assumption A2 (L06.html:71-72) is about the informed fraction and what each investor observes, and supports only the second sentence. So the basis no longer cites the hypothesis that supports the claim. Other changed L06 cards checked and correct: E4-c100 (Definition 6.1, L06.html:56-60), E4-c107 (basis now G(i); front names A1, A4 and G; the residual argument holds), E4-c115 (Step 3 fixes both coefficients), E4-c122 (lab output 'grid_points 16 zero_residuals 16', L06.html:478), E4-c231 (posterior, L06.html:96-97), new E4-c271 (2/3 = 1/(tau_v + tau_eta) = Var(v|p), Corollary 6.8; Lab Part B prints posterior_var_uninformed 2/3). Removed E4-c247 has no remaining reference. Other 35 L06 cards byte-identical.",
 "E4b11-cards-numbers-in-lesson": "Re-verified: E4-c122 numbers 16 and 16 appear in the L06 lab expected block (L06.html:475-476 'grid_points 16 zero_residuals 16'); E4-c090 (4, -3/10) in L05 lab Part A; E4-c263 (0, 0) in L05 Part A; E4-c271 (2/3) in L06.html Example 6.9 and lab Part B. Other listed cards (c092-c094, c118, c123-c125, c243) byte-identical and their numbers unchanged in the lab outputs.",
 "E4b11-cards-duplicate-scan": f"Re-verified: cards_scan_r1.txt: 259 cards, 259 unique ids, 0 duplicate fronts, 0 duplicate backs; slice cards (L04, L05, L06) 105. Near-overlaps read: E4-c271 and E4-c129 both give 2/3 but ask different questions (numeric value vs misconception); E4-c268 and E4-c060 are different questions.",
 "E4b11-cards-process-words": f"Re-verified: process-word regex over the 105 slice cards and the visible text of L04, L05, L06 gives 0 hits (prose_scans_r1.txt); the changed L06 and card text also scanned for ruling, round, verif, builder, fixed and similar words: 0 hits.",
 "E4b12-card-c076": "Re-verified: E4-c076 back now reads 'A2 restricts the forecast to this family' (cards.json:575-578); L05.html:59 A2 says the forecast is 'restricted to the family of affine functions', so the card agrees with the lesson.",
 "E4b12-L06-VU-use-before-definition": "Re-verified: V_U is defined at L06.html:152 ('=: V_U' in the Lemma 6.4 statement) before its first use in the proof at line 157; the changed line 157 keeps the sentence 'Here V_U = sigma_v^2(...)/Var(p) > 0', which is correct (rederive_r1.py). Ordering fixed in e919577b and unchanged here.",
 "E4b12-cards-split-review": "Re-verified (cards_scan_r1.txt, 0 duplicate fronts or backs): E4-c254 and E4-c255 are absent, so the pairs c116/c254 and c119/c255 no longer exist; E4-c081/c251, E4-c083/c252 and E4-c113/c253 are distinct questions (E[p_m|z] vs conditional law; fixed point vs price; E[v|p] vs Var(v|p)). E4-c116 and E4-c119 are single questions.",
 "E4b13-delta-removed-cards": f"Re-verified: E4-c121, E4-c254 and E4-c255 are absent; E4-c247 (L06) is removed in e919577b..HEAD (card_delta_r1.txt 'REMOVED: E4-c247'). grep for E4-c121, E4-c247, E4-c254 and E4-c255 over course/, tools/ and tests/ finds no reference ({S}card_delta_r1.txt).",
 "E4b13-delta-L06-hunk": "Re-verified: L06.html:149-152 (Lemma 6.4 statement, with the '=: V_U' definition at 152) is byte-identical in e919577b..HEAD (no hunk in 149-152). The base note 'the only hunk in slice b' no longer holds; the current hunks at L06.html lines 62, 86, 143, 157, 202, 552, 663 and 722 are each read above.",
 "E4b13-twins-unchanged": f"Re-verified: tests/labs/E4/lab-E4-L04-1.py, lab-E4-L05-1.py and lab-E4-L06-1.py are byte-identical at e919577b and HEAD (git diff --quiet exit 0 each) and re-run identical ({S}twin_L0x.out).",
}

CARRY_FILES = {
 "E4b11-muth-attribution": "course/modules/E/E4/L05.html:296 and the references/references.json entry muth1961rational (only black1973pricing and generated_at changed in that file)",
 "E4b11-simulated-labels": "course/modules/E/E4/L06.html:240, 255, 480, 633-634 and cards E4-c124, E4-c125",
 "E4b11-lab-l06-docstring": "tests/labs/E4/lab-E4-L06-1.py",
 "E4b11-lab-l05-docstring": "tests/labs/E4/lab-E4-L05-1.py",
 "E4b11-lab-l04-docstring": "tests/labs/E4/lab-E4-L04-1.py",
 "E4b11-L04-lemma21-assumptions": "course/modules/E/E4/L04.html:100-108",
 "E4b11-L04-lemma21-proof": "course/modules/E/E4/L04.html:108",
 "E4b11-L04-sec1-statements": "course/modules/E/E4/L04.html:62-96",
 "E4b11-L04-examples": "course/modules/E/E4/L04.html:111-115",
 "E4b11-L04-lab-1": "course/modules/E/E4/L04.html:117-265",
 "E4b11-L04-remarks": "course/modules/E/E4/L04.html:269-277",
 "E4b11-L04-canon-breaks": "course/modules/E/E4/L04.html:279-300",
 "E4b11-L04-misconceptions": "course/modules/E/E4/L04.html:302-321",
 "E4b11-L04-problems": "course/modules/E/E4/L04.html:324-427",
 "E4b11-L04-key-results": "course/modules/E/E4/L04.html:288-289 and 440",
 "E4b11-L04-quiz": "course/modules/E/E4/L04.html:446-514",
 "E4b11-L04-why-it-matters": "course/modules/E/E4/L04.html:51",
 "E4b11-L04-references": "course/modules/E/E4/L04.html:516-520",
 "E4b11-L05-why-it-matters": "course/modules/E/E4/L05.html:51",
 "E4b11-L05-model": "course/modules/E/E4/L05.html:58-74",
 "E4b11-L05-lemma21-prop22-cor23": "course/modules/E/E4/L05.html:78-98",
 "E4b11-L05-lemma31-proof": "course/modules/E/E4/L05.html:102-106",
 "E4b11-L05-lemma31-hypothesis": "course/modules/E/E4/L05.html:103-104",
 "E4b11-L05-prop32-33": "course/modules/E/E4/L05.html:108-118",
 "E4b11-L05-psi0-notation": "course/modules/E/E4/L05.html:402",
 "E4b11-L05-lab-1": "course/modules/E/E4/L05.html:120-282",
 "E4b11-L05-remark-canon-muth": "course/modules/E/E4/L05.html:292-296",
 "E4b11-L05-misconceptions": "course/modules/E/E4/L05.html:299-315",
 "E4b11-L05-problems": "course/modules/E/E4/L05.html:317-420",
 "E4b11-L05-key-results-quiz": "course/modules/E/E4/L05.html:422-502",
 "E4b11-L05-references": "course/modules/E/E4/L05.html:504-507",
 "E4b11-L06-why-it-matters": "course/modules/E/E4/L06.html:51",
 "E4b11-L06-lemma62-proof": "course/modules/E/E4/L06.html:99-125",
 "E4b11-L06-lemma62-hypotheses": "course/modules/E/E4/L06.html:98-104",
 "E4b11-L06-remark-65-610": "course/modules/E/E4/L06.html:160-163 and 233-236",
 "E4b11-L06-cor68-slope-step": "course/modules/E/E4/L06.html:211-226",
 "E4b11-L06-example69": "course/modules/E/E4/L06.html:228-231",
 "E4b11-L06-lab-1": "course/modules/E/E4/L06.html:238-481 and tests/labs/E4/lab-E4-L06-1.py",
 "E4b11-L06-canon-breaks": "course/modules/E/E4/L06.html:483-493",
 "E4b11-L06-misconceptions": "course/modules/E/E4/L06.html:495-515",
 "E4b11-L06-R1-corr-identity": "course/modules/E/E4/L06.html:598-602",
 "E4b11-L06-references": "course/modules/E/E4/L06.html:727-731",
 "E4b11-L06-part-d-alt": "course/modules/E/E4/L06.html:474-475 and tests/labs/E4/lab-E4-L06-1.py part_d",
 "E4b11-cards-c120-basis": "cards E4-c120 and E4-c220",
 "E4b12-card-c106": "course/modules/E/E4/cards.json:796-799 (E4-c106) and course/modules/E/E4/L06.html:80-81",
 "E4b12-L06-research-R2-R3": "course/modules/E/E4/L06.html:606-616",
 "E4b13-delta-c065-grade": "cards E4-c065",
 "E4b13-delta-card-basis-edits": "cards E4-c118 and E4-c129",
}

# Notes and the single FAIL row
NEW_ROWS = [
 {"id": "E4b-r1-A1-forward-G-pointer", "check": "2.4 / BUILDER 1.x define-before-use (forward pointer)",
  "location": "course/modules/E/E4/L06.html:62 (A1) and 90-92 (Assumption G)",
  "status": "PASS",
  "evidence": "A1 now reads 'Hence (v, s, u) is jointly normal, by the linear-image fact G(i) stated below'. The fact is stated 28 lines later in Assumption G (L06.html:90-92) and is correct. The lesson already points forward explicitly elsewhere (A4 cites 'the CARA demands of Remark 6.5 in §2', L06.html:82). This is a forward pointer to a numbered assumption, not a false, unproved, missing-hypothesis or wrong-number statement, so it is not a ruling-26 FAIL kind. Observation for the fixer (LOW): move Assumption G above A1, or drop 'stated below'."},
 {"id": "E4b-r1-L06-prop67-step3-residual", "check": "2.4 mathematics",
  "location": "course/modules/E/E4/L06.html:194-199 (Proposition 6.7 Step 3, changed line 202)",
  "status": "PASS",
  "evidence": f"With p = theta_s s - theta_u u the residual is (lambda tau_eps - Q theta_s) s + (Q theta_u - a) u with no constant term; evaluating at (1,0) and (0,1) gives Q theta_s = lambda tau_eps and Q theta_u = a, which Step 4 then uses. Checked exactly in rederive_r1.py ({S}rederive_r1.txt): linearity and zero constant term, Step 3 identities at the closed form, and clearing on a 6x6 grid, 400 random exact trials, 0 failures."},
 {"id": "E4b-r1-card-c268-ungraded-definition", "check": "2.7 cards (definition card)",
  "location": "course/modules/E/E4/cards.json:1902-1905 (E4-c268)",
  "status": "PASS",
  "evidence": "New card E4-c268 'What is a complete market (Definition 1.3)?' has no grade or basis field. It is a definition card with no graded claim; the back matches Definition 1.3 (L04.html:76-77: M(A) = R^S, every payoff attainable; 'otherwise incomplete'). Other ungraded definition cards exist in L04-L06 (for example E4-c231). Not a defect; no duplicate (E4-c060 asks about Corollary 1.6)."},
 {"id": "E4b-r1-card-c271-hypothesis-front", "check": "2.7 cards (hypotheses carried)",
  "location": "course/modules/E/E4/cards.json:1924-1928 (E4-c271)",
  "status": "PASS",
  "evidence": "New E4-c271 gives 2/3 = 1/(tau_v + tau_eta) = Var(v|p) at the Example 6.9 base instance. The value is right (rederive_r1.txt: V_U 2/3) and the basis is Corollary 6.8 and Lab Part B (outputs print posterior_var_uninformed 2/3). The front does not restate 'Assuming A1 to A4 and G' as E4-c118 does. The model of the page is in force for the whole Example, and the base round already accepted E4-c119 with the same wording. Observation (LOW, not a ruling-26 kind): add the hypotheses to the front."},
]

rows = []
for r in base["rows"]:
    rid = r["id"]
    row = {"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": None}
    if rid == "E4b11-cards-L06":
        row["status"] = "FAIL"
        row["evidence"] = RE_VERIFIED[rid]
        row["fix"] = ("Restore the basis of E4-c127 to cite the hypothesis that gives the independence claim, and keep A2 for the second sentence: "
                      "cards.json E4-c127 basis 'Definition 6.1, A1 and A2' (the round-13 value was 'Definition 6.1 and A1'). "
                      "Then re-run cards_scan and the card row.")
    elif rid in RERUN:
        row["evidence"] = RERUN[rid]
    elif rid in RE_VERIFIED:
        row["evidence"] = RE_VERIFIED[rid]
    elif rid == "E4b11-cards-L06":
        row["status"] = "FAIL"
        row["evidence"] = RE_VERIFIED.get(rid) or ""
        row["fix"] = ("Restore the basis of E4-c127 to cite the hypothesis that gives the independence claim, and keep A2 for the second sentence: "
                      "cards.json E4-c127 basis 'Definition 6.1, A1 and A2' (the round-13 value was 'Definition 6.1 and A1'). "
                      "Then re-run cards_scan and the card row.")
    elif rid in CARRY_FILES:
        row["evidence"] = carry(CARRY_FILES[rid], rid)
    else:
        raise SystemExit("unclassified base row " + rid)
    rows.append(row)
for n in NEW_ROWS:
    n = dict(n); n["evidence"] = n["evidence"]
    rows.append(n)
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids))
for r in rows:
    if r["id"] == "E4b11-cards-L06":
        assert r["status"] == "FAIL"
    if not r.get("evidence"):
        raise SystemExit("empty evidence " + r["id"])

notes = [
 "Delta e919577b..95f3f8cb for slice b (L04, L05, L06 pages, the three L04-L06 twins, cards for L04-L06). Changed in slice b: L06.html (hunks at lines 62, 86, 143, 157, 202, 552, 663, 722); cards.json (cards E4-c058, c076, c090, c097, c100, c107, c115, c122, c127, c227, c228, c231, c251 changed; c247 removed; c261, c263, c268, c271 added). L04.html, L05.html and the three twins are byte-identical in that range. Other changes in the range that touch E4 slice b inputs: references/references.json (generated_at and one unrelated used_by entry; the E4 entries are unchanged), curriculum/01-foundations.yaml and CURRICULUM.md / curriculum.json (the M3 brief only). Cards of L01-L03, L07-L09 (for example E4-c011, c047, c214, c225, c237, c260, c262, c264-c266, c269, c270) and L03.html and the project files are outside slice b and were not verified here (they belong to slices a, c and d).",
 "Ruling 30: rows re-verified from scratch are the base non-PASS row (E4b11-cards-L06, now FAIL) and every row whose cited lines or card objects changed; other rows are carried with the carry prefix only where the cited lines or card objects are byte-identical. Command gates were re-run on 95f3f8cb (not carried). Ruling 37: no new mutants; slice b has no grader; the standing mutant set for slice b is empty (mutants: []).",
 "Ruling 26: only FAIL kinds are reported. The single FAIL is a missing-hypothesis / wrong-basis defect on a T-graded card (E4-c127). Observations that are not ruling-26 kinds are recorded here, not as FAIL: (a) forward pointer 'G(i) stated below' at L06.html:62; (b) the letter G names the labelled Assumption G in L06 and the gain G(lambda) in L08 (L08.html:234), and G is not a notation.json entry (LOW, for the notation owner); (c) E4-c271 front does not restate 'A1 to A4 and G' (LOW).",
 "Exemplar calibration: not applicable (slice b has no rubric exemplars; ruling 23 blind scoring applies to rubric slices only).",
 "Base-row evidence cited as 'carried' is the round-13 evidence text; its own sources are in /Users/billyribeiro/.fanout/frags/E-E4-b.round13.json and in ledgers/E4/scripts/E4-b-r13/.",
]

frag = {
 "unit": "E4",
 "slice": "b",
 "round": 1,
 "verifier": "Haiku independent verifier F31, E4-b closing delta round 1 (did not build E4; no shared context with builders)",
 "pin": "95f3f8cb (detached) in /Users/billyribeiro/.fanout/wt/verifyF31-E4-b",
 "base": "e919577b (round-13 pin; base fragment /Users/billyribeiro/.fanout/frags/E-E4-b.round13.json, verdict PASS with 93 rows)",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyF31-E4-b",
 "scratch": "ledgers/E4/scripts/E4-b-r1/ (twin_page_check_r1.py, rederive_r1.py, card_delta_r1.py, skeleton_diff_r1.py, structure_scan_r1.py, solutions_len_r1.py, prose_scans_r1.py, cards_scan_r1.py, write_fragment_r1.py; outputs/ holds every command output)",
 "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
 "verdict": "FAIL",
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": notes,
 "summary": None,
}
c = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows: c[r["status"]] += 1
carried = sum(1 for r in rows if r["evidence"].startswith("Carried from round 13"))
frag["summary"] = (f"E4-b closing delta round 1 at 95f3f8cb: rows={len(rows)} (pass={c['PASS']} fail={c['FAIL']} unverifiable={c['UNVERIFIABLE']}; "
                   f"carried from round 13={carried}). All command gates exit 0 on the pin. One FAIL: E4b11-cards-L06 (E4-c127 basis cites A2, which does not support the independence of u; fix: 'Definition 6.1, A1 and A2'). "
                   "Everything else in the changed hunks of L06.html and the changed or new cards of L04-L06 is re-verified PASS.")
json.dump(frag, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(OUT, "a", encoding="utf-8").write("\n")
print("wrote", OUT, "rows", len(rows), c, "carried", carried)
