"""Assemble the round-11 fragment for M4 slice d from this round's script outputs (counts are read, not typed)."""
import json, re, pathlib, datetime

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB11-M4-d")
S = "ledgers/M4/scripts/M4-d-r11/"
mut_out = (ROOT / S / "mutate_M4.out").read_text(encoding="utf-8").splitlines()

# ---- mutants: every line of the tool's output, with dispositions for the accepted survivors
ACCEPTED = {
    "m11_loss_sign_flipped.py": "SURVIVES; accepted: project.html:204 and :228 exclude the loss sign from grading",
    "m17_student_t_second_seed.py": "SURVIVES; accepted: project.html:198 requires only that every run is reproducible from its seed, which this mutant meets",
    "r9_03_student_t_chi_square_reused_every_second_draw.py": "SURVIVES; accepted: project.html:228 states that a family reusing one chi-square on alternate draws passes the suite at seeds 0 to 9",
    "v4_m02_matched_factor_skipped_for_small_nu.py": "SURVIVES; accepted: project.html:204 and :228 exclude the matched factor inside simulate_losses at nu of 3 and 4",
}
NEW_FAIL = {
    "r11_02_debug_print_quantile_single_loss.py": "SURVIVES seeds 0-49 (per_seed.py: fails on 0 of 50); project.html:204 and :206 apply: FAIL (G-24)",
    "r11_03_debug_print_draw_count_multiple_of_100.py": "SURVIVES seeds 0-49 (per_seed.py: fails on 0 of 50); project.html:204 and :206 apply: FAIL (G-25)",
}
mutants = []
for line in mut_out:
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, kb = m.groups()
    killed_by = None if kb.strip() == "None" else kb.strip()
    if name in ACCEPTED:
        killed_by = None
        desc += " [" + ACCEPTED[name] + "]"
    if name in NEW_FAIL:
        desc += " [" + NEW_FAIL[name] + "]"
    mutants.append({"id": name, "description": desc, "killed_by": killed_by})
summary_line = [l for l in mut_out if l.startswith("mutate_graders M4:")]
assert len(mutants) == 101, len(mutants)

def mstatus(name):
    for x in mutants:
        if x["id"].startswith(name):
            return x
    raise KeyError(name)

rows = []
def row(i, check, location, status, evidence, fix=None):
    r = {"id": i, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

PASS, FAIL = "PASS", "FAIL"
ALT = "ledgers/M4/scripts/"
# ---------------- project page
row("P-01", "Lab 1 hypothesis numbers and expected block", "course/modules/M/M4/project.html:57, 136-143", PASS,
    S + "labs_check.out 'lab 1: output == expected: True' and run_labs.out 'run_labs M4: PASS (13/13)'; 8.4e9 = 3.6e9 + 1.2e9 + 3.6e9 by hand; ceil(0.99*20000)=19800; (nu-2)/nu = 0.6 at nu = 5; lines 57 and 136-143 byte-identical since the round-10 pin.")
row("P-02", "Lab 2 completion problem and expected block", "course/modules/M/M4/project.html:147-192", PASS,
    S + "labs_check.out: page code differs from the twin only at the two blanks; 'lab 2: output == expected: True'.")
row("P-03", "Lab 3 closed-form numbers and expected block", "course/modules/M/M4/project.html:266-314", PASS,
    S + "labs_check.out 'lab 3: output == expected: True', page-vs-twin differing lines 0; sqrt(8.4e9) = 91651.514; z = 2.326348; round(z*sd) = 213213; 0.99*19987 = 19787.13 (ceil 19788, floor 19787).")
row("P-04", "Lab 1 page code equals twin and runs under -I -W error", "course/modules/M/M4/project.html:58-135; tests/labs/M4/lab-M4-project-1.py", PASS,
    S + "labs_check.out: 0 differing lines (length 78 vs 78; the only difference is the final newline); 'lab 1: twin exit 0 stderr ''' under python -I -W error.")
row("P-05", "Appendix A1 to A3 formulas and divergence claims", "course/modules/M/M4/project.html:325, 429", PASS,
    "Re-derived by hand: E[W^-1] = Gamma(nu/2-1)/(2 Gamma(nu/2)) = 1/(nu-2); E[W^-2] = 1/((nu-2)(nu-4)); integrand exponents nu/2-2 (not integrable at 0 iff nu <= 2) and nu/2-3 (iff nu <= 4); Var(t) = nu E[W^-1]; E[RR^T] = Sigma. Line 429 unchanged since the pin of round 10 (the round-10 delta changed only line 359 on this page).")
row("P-06", "Conventions items 1, 2 and 4 (formulas)", "course/modules/M/M4/project.html:209-217", PASS,
    S + "anchors_and_identity.out: (99n+99)//100 == ceil(0.99 n) for every n in 1..20000 (0 mismatches). Items 1 and 2 match grader/reference.py lines 51-91 (round(-total), scale sqrt((nu-2)/W) for the Student-t family).")
row("P-07", "Conventions item 1 notation and the Reading section", "course/modules/M/M4/project.html:211, 214, 482", PASS,
    S + "notation/notation.json (8 symbols, macros list): the page uses \\E (registered as expectation), and \\nu, \\Sigma, \\Gamma, \\ell, W, Z, L, R, s, F_n, Q, which are local symbols; no registered symbol (\\Phi, \\gamma_3, \\gamma_4, R^\\ast, R_f, \\mathbb{Q}) appears on the page (grep of TeX macros in project.html).")
row("P-08", "What the suite does not test: completeness of disclosures", "course/modules/M/M4/project.html:228", PASS,
    "Each claim checked: nu of 3 and 4 skipped (test_project.py:157-158); cross term at nu 5, 100000 draws, tolerance 0.05, correlation 0.8 (test_project.py:43-48, 167-180); sign not tested (m11 survives, " + S + "mutate_M4.out); one chi-square per draw not tested (r9_03 survives on seeds 0-49).")
row("P-09", "Grading-mode count 133 equals real collect-only count", "course/modules/M/M4/project.html:206", PASS,
    S + "collect.out: '133 tests collected' for grader/test_project.py run against grader/reference.py copied as tail_risk.py in a temp directory.")
row("P-10", "Rubric table and brief", "course/modules/M/M4/project.html:316-343", PASS,
    "Five criteria, four levels each; the brief (lines 319-326) states Summary at most 80 words, body 300 to 700 words, appendix A1 to A4, and the rubric C5 level 3 repeats the same bounds. Consistent on re-read.")
row("P-11", "Numbers in exemplar A and B passages", "course/modules/M/M4/project.html:348-462", PASS,
    S + "exemplar_words.out: exemplar A body 90 words (line 359 now says 90); exemplar B body 671 words, Summary 70 words (within the 300-700 bar and at most 80). Exemplar B: 243004/210946 = 1.15197 (quoted 1.152, line 144); 213213-210946 = 2267; 243004-210946 = 32058 = 15.2 % of 210946; 1.0447 - 1 = 0.0447 = about 4.5 %.")
row("P-12", "Exemplar scores and annotation consistency", "course/modules/M/M4/project.html:348-462", PASS,
    "Exemplar A data-scores 2,2,2,2,2: each criterion's annotations stop at level 2 (C4 and C5 misses at level 3 at lines 358, 383, 394; C1 and C3 meets at level 2). Exemplar B data-scores 4,4,4,4,3: C5 has the only level-4 miss (line 458). Each 'Meets ... level 4' claim matches the level-4 cell text in lines 339 and 336.")
row("P-13", "Time budget and hub split", "course/modules/M/M4/project.html:33, 237-243; course/modules/M/M4/index.html:31, 39, 42, 147", PASS,
    "Hours 2 + 2 + 12 + 8 + 4 + 2 = 30 (lines 237-243); data-hours-project=30 (line 33); index.html:31 says 120 hours, :39 says 90 lesson and 30 project hours, :147 says ten lessons of nine hours; each lesson's data-hours is 9 (grep), 10 x 9 = 90; 90 + 30 = 120.")
row("P-14", "Anchors and relative links", "course/modules/M/M4/project.html (href targets)", PASS,
    S + "anchors_and_identity.out: no in-page #anchor missing; every relative href target exists on disk.")
row("P-15", "File names and ids named on the page", "course/modules/M/M4/project.html; cards.json; grader/*.py", PASS,
    "tail_risk.py, report/run_report.py, report/report.md, report/self_assessment.md (lines 202, 241, 464); grader/test_project.py, instance.py, starter.py exist; data-suite, data-support, data-solution and data-starter match these names (line 252).")
row("P-16", "Required signatures", "course/modules/M/M4/project.html:202; grader/starter.py:15-34", PASS,
    "starter.py defines matched_scale(nu: int) -> float, simulate_losses(position_cents, cov, n_draws, seed, family, nu) -> list[int] and quantile_99(losses_cents: list[int]) -> int, the same as line 202. starter.py is byte-identical since the round-10 pin.")
row("P-17", "Named conditions vs tests", "course/modules/M/M4/project.html:220-224", PASS,
    "Each named condition has a test in test_project.py: matched_scale nu <= 2 and non-int (lines 118-129); simulate_losses family, nu None rules, nu <= 2, draw count, non-int draws, positions, empty positions, cov shape, symmetry, positive definiteness (lines 200-432); quantile_99 empty and non-int (lines 505-511). Accepted inputs: lines 210, 238, 292-294, 396-398, 435-448.")
row("P-18", "Stream order and one chi-square per draw vs suite", "course/modules/M/M4/project.html:204, 215, 228", PASS,
    "The page says the stream order is not graded and the suite checks neither the order nor one chi-square per draw; test_project.py has no stream-order check (grep), and the cross term (line 167) is the only dependence check. Consistent with mutate_M4.out (n02 killed by the cross term; r9_03 survives).")
row("P-19", "Local run command and flags", "course/modules/M/M4/project.html:258-259", PASS,
    "Page: QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py; test_project.py:5 gives the same command and flags.")
row("P-20", "Autograder section attributes", "course/modules/M/M4/project.html:249-253", PASS,
    "data-unit=M4, data-grader=grader/, data-suite=test_project.py, data-support=instance.py, data-solution=tail_risk.py, data-starter=starter.py; all named files exist in grader/.")
row("P-21", "Lede and Lab 1 framing", "course/modules/M/M4/project.html:37, 57", PASS,
    "Lede says every input is SIMULATED; Lab 1 says positions 3,000,000 and 2,000,000 cents and covariance 0.0004/0.0001/0.0009 (line 69-70 of the twin), consistent with line 53 (volatilities 2 % and 3 %, correlation 1/6: 0.0001 = (1/6) x 0.02 x 0.03).")
row("P-22", "Limitations: tolerance and nu scope", "course/modules/M/M4/project.html:453", PASS,
    "Exemplar B limitations state tolerance 0.30 (test_project.py:41, TOL_T_VARIANCE) and the variance check at nu of 5 or more (test_project.py:42, MIN_NU_FOR_T_VARIANCE_CHECK). The sign-by-hand statement matches the convention at line 212.")
# ---------------- grader
row("G-01", "Suite conforms to the page's named conditions", "course/modules/M/M4/grader/test_project.py:89-517", PASS,
    "Read in full (517 lines). Every named condition on page lines 220-224 has a test; the new test_no_function_prints (278-289) calls every function, but see G-23-G-25 for the print checks. Comment-level overclaim is G-23.")
row("G-02", "Starter file", "course/modules/M/M4/grader/starter.py:15-34", PASS,
    "Read in full: three functions raising NotImplementedError, signatures complete, and no print or warning in the file.")
row("G-03", "Five-plus alternative correct implementations pass", "ledgers/M4/scripts/alt_1.py..alt_5.py; M4-d-r9/alt_stream_order_tail_risk.py; M4-d-r10/alt_r10_a_stream_order_fraction_index.py", PASS,
    S + "alternatives_seeds0-49_r11.txt: reference and alt_1 to alt_5 each PASS 50/50 seeds; " + S + "alt_extra_seeds0-49_r11.log: the two stream-order alternatives fail on 0 of 50 seeds.")
row("G-04", "matched_scale tests vs page", "course/modules/M/M4/grader/test_project.py:105-130", PASS,
    "test_matched_scale_is_nu_minus_two_over_nu covers nu 3 to 8; nu = 3 boundary (line 114-115); nu <= 2 and non-whole values rejected (118-129); matches page line 222.")
row("G-05", "Tolerance constants and comment numbers", "course/modules/M/M4/grader/test_project.py:31-48", PASS,
    "Carried from round 10 (course/modules/M/M4/grader/test_project.py:31-48 byte-identical since the round-10 pin; the round-10 sweep of seeds 0-1999 is ledgers/M4/scripts/M4-d-r10/sweep_grader_comment_0-1999.txt).")
for gid, mname, text in [
    ("G-06", "r6_01_three_asset_last_factor_column_dropped.py", "Mutant: three-asset last factor column dropped"),
    ("G-07", "r6_02_student_t_chi_square_twice_the_degrees.py", "Mutant: Student-t chi-square twice the degrees"),
    ("G-08", "r6_03_pivot_tolerance_rejects_small_positive_variance.py", "Mutant: pivot tolerance rejects small positive variance"),
    ("G-11", "n02_one_chi_square_per_asset.py", "Mutant: one chi-square per asset"),
    ("G-15", "r7_01_student_t_seed_fixed.py", "Mutant: Student-t seed fixed"),
    ("G-16", "r8_03_student_t_matched_scale_on_first_asset_only.py", "Mutant: matched scale on first asset only"),
    ("G-17", "r8_01_student_t_chi_square_drawn_once_per_run.py", "Mutants: chi-square drawn once per run (r8_01) and index one low at multiples of 100 (r8_02)"),
    ("G-19", "r9_01_student_t_cross_term_sign_flipped_for_second_asset.py", "Mutant: Student-t cross-term sign flipped for second asset"),
]:
    if gid == "G-17":
        a, b = mstatus("r8_01"), mstatus("r8_02")
        ok = bool(a["killed_by"]) and bool(b["killed_by"])
        row(gid, "Mutants: chi-square drawn once per run / index one low at multiples of 100", "ledgers/M4/mutants/r8_01_*.py; ledgers/M4/mutants/r8_02_*.py", PASS if ok else FAIL,
            S + f"mutate_M4.out: r8_01 -> {a['killed_by']}; r8_02 -> {b['killed_by']}.",
            None if ok else "see mutate_M4.out")
        continue
    x = mstatus(mname[:8] if mname[:3] != "n02" else "n02_one")
    row(gid, text, "ledgers/M4/mutants/" + mname, PASS if x["killed_by"] else FAIL,
        S + f"mutate_M4.out: {x['id']} -> {x['killed_by']}.",
        None if x["killed_by"] else "see G-22")
row("G-09", "Mutant: loss sign flipped", "ledgers/M4/mutants/m11_loss_sign_flipped.py; course/modules/M/M4/project.html:204, 212, 228", PASS,
    S + "mutate_M4.out: m11 SURVIVES all seeds 0-49; the loss sign is excluded from grading by project.html:204 ('the sign of the loss (item 2)') and stated at :228, so the survivor is not a violated grader claim.")
row("G-10", "Mutant: Student-t second seed", "ledgers/M4/mutants/m17_student_t_second_seed.py", PASS,
    S + "mutate_M4.out: m17 SURVIVES seeds 0-49. project.html:198 requires only reproducibility from the seed, which this mutant meets; the stream order is not graded (:215).")
row("G-12", "Mutant: matched factor skipped for small nu", "ledgers/M4/mutants/v4_m02_matched_factor_skipped_for_small_nu.py; course/modules/M/M4/project.html:204, 228", PASS,
    S + "mutate_M4.out: v4_m02 SURVIVES seeds 0-49; project.html:204 excludes 'the matched factor inside simulate_losses at nu of 3 and 4 (item 1)' and :228 states that the suite does not check it there.")
row("G-13", "Test count and rules", "course/modules/M/M4/grader/test_project.py:89-517", PASS,
    S + "collect.out: 133 tests collected, equal to project.html:206 (see P-09). No new test function was added in the round-10 to round-11 delta.")
row("G-14", "Instance generator", "course/modules/M/M4/grader/instance.py:1-48", PASS,
    "Read in full. Draws are from _DRAWS = (6003, 8001, 9997, 12011, 15013, 19987), none a multiple of 100 and none above 19987 (matches the docstring and test_instance_is_simulated_and_in_range). nu from randrange(3, 9) gives 3 to 8. " + S + "seed_table_0-49.txt lists nu and n_draws for seeds 0 to 49.")
row("G-18", "Mutant: chi-square reused every second draw", "ledgers/M4/mutants/r9_03_student_t_chi_square_reused_every_second_draw.py; course/modules/M/M4/project.html:228", PASS,
    S + "mutate_M4.out: r9_03 SURVIVES seeds 0-49, consistent with project.html:228 ('passes the whole suite at seeds 0 to 9').")
row("G-20", "Mutant: debug print in simulate_losses for long runs (round-10 FAIL, repaired)", "ledgers/M4/mutants/r10_01_debug_print_on_long_runs.py; course/modules/M/M4/grader/test_project.py:278-289", PASS,
    S + "mutate_M4.out: r10_01 KILLED by " + mstatus("r10_01")["killed_by"] + ". Re-verified from scratch this round. The new loop (test_project.py:281-287) calls simulate_losses at the instance's draw count for both families.")
row("G-21", "Mutant: debug print in matched_scale at nu = 3 (round-10 FAIL, repaired)", "ledgers/M4/mutants/r10_03_matched_scale_debug_print_at_boundary.py; course/modules/M/M4/grader/test_project.py:281-282", PASS,
    S + "mutate_M4.out: r10_03 KILLED by " + mstatus("r10_03")["killed_by"] + " (the loop over nu 3 to 8 at test_project.py:281-282).")
row("G-22", "mutate_graders --unit M4: every mutant killed except accepted survivors", "ledgers/M4/mutants/ (101 files); " + S + "mutate_M4.out", FAIL,
    S + "mutate_M4.out last line: '" + summary_line[-1].strip() + "'. Survivors: m11, m17, r9_03, v4_m02 (accepted, see G-09, G-10, G-18, G-12); r11_02 and r11_03 (FAIL, see G-24 and G-25).",
    "Make test_no_function_prints call quantile_99 on a one-loss list and on a list of 100 (or 1000) losses, and call simulate_losses with n_draws = 100 (a multiple of 100) at least once, under capsys; then re-run tools/mutate_graders.py --unit M4 --seeds 0-49 until only the four accepted survivors remain.")
row("G-23", "Test comment overclaims what the print test covers", "course/modules/M/M4/grader/test_project.py:279-280", FAIL,
    "Comment: 'every nu of 3 to 8, so a print that shows only on long runs or at one nu is caught as well'. The loop (281-282) runs matched_scale at every nu, but simulate_losses runs only at the instance's own nu (284). " + S + "per_seed_r11.log: ledgers/M4/mutants/r11_01 (a debug print in simulate_losses when the Student-t nu is 3) fails on 11 of 50 seeds (1, 2, 9, 11, 24, 32, 37, 42, 44, 46, 48) and passes the other 39, so a student whose instance has nu of 4 to 8 can print at nu = 3 undetected; the mutate tool counts it killed only because the window contains seed 1.",
    "Call simulate_losses(POSITIONS, COV, 50, SEED, 'student_t', nu) for each nu in range(3, 9) under capsys (in addition to the instance's N_DRAWS call), so the comment is true of simulate_losses as well as matched_scale.")
row("G-24", "Print in quantile_99 for a one-loss list survives", "ledgers/M4/mutants/r11_02_debug_print_quantile_single_loss.py; course/modules/M/M4/project.html:204, 206", FAIL,
    S + "mutate_M4.out: r11_02 SURVIVES seeds 0-49; " + S + "per_seed_r11.log: fails on 0 of 50 seeds. project.html:204 says 'No function prints or warns' and :206 grades 'the absence of printed output'; test_project.py:278-289 calls quantile_99 only on [3, 1, 2] under capsys, and test_quantile_99_of_one_loss_is_that_loss (501-502) does not capture output.",
    "Add quantile_99([7]) and a 100-loss list (and one with n = 101) inside test_no_function_prints, under the same capsys check.")
row("G-25", "Print in simulate_losses for a draw count that is a multiple of 100 survives", "ledgers/M4/mutants/r11_03_debug_print_draw_count_multiple_of_100.py; course/modules/M/M4/project.html:204, 206", FAIL,
    S + "mutate_M4.out: r11_03 SURVIVES seeds 0-49; " + S + "per_seed_r11.log: fails on 0 of 50 seeds. The instance never draws a multiple of 100 (instance.py docstring and _DRAWS), and test_no_function_prints uses the instance draw count and 50, so no call in the suite reaches the print. project.html:204 and :206 apply.",
    "Add one call with n_draws = 100 (or 1000) for each family inside test_no_function_prints, under capsys.")
# ---------------- labs
row("L-01", "Project labs: run output, twins, page code", "tests/labs/M4/lab-M4-project-1.py, -2.py, -3.py", PASS,
    S + "labs_check.out: 'output == expected: True' for labs 1, 2 and 3; each twin exit 0 under python -I -W error; " + S + "run_labs.out: PASS 13/13.")
row("L-02", "Project lab page code vs twins (line level)", "course/modules/M/M4/project.html:58-135, 147-184, 269-301", PASS,
    S + "labs_check.out: lab 1 0 differing lines (final newline only), lab 2 2 differing lines (the two blanks, intended), lab 3 0 differing lines.")
row("L-03", "All M4 labs run", "tests/labs/M4/lab-M4-*.py", PASS,
    S + "run_labs.out: 'run_labs M4: PASS (13/13)', exit 0.")
row("L-04", "Carried from round 9 (tests/labs/M4/lab-M4-L10-1.py:60-65; course/modules/M/M4/L10.html:234-236)", "tests/labs/M4/lab-M4-L10-1.py:60-65; course/modules/M/M4/L10.html:234-236", PASS,
    "Carried from round 10 (tests/labs/M4/lab-M4-L10-1.py and course/modules/M/M4/L10.html:234-236 byte-identical since the round-10 pin; the round-10 delta does not touch tests/labs/M4 or L10.html; run_labs.out covers the lab).")
# ---------------- cards
row("C-01", "cards.json structure", "course/modules/M/M4/cards.json", PASS,
    "191 cards (round 10 had 192: M4-c123 removed, see C-06); ids unique (check_pages.out PASS); grades only T (170) and C (21); every C card has a basis, no T card has one (python check); no duplicate front or back text.")
row("C-02", "Cards agree with the CURRENT lesson text and carry a proposition's hypotheses", "course/modules/M/M4/cards.json (M4-c118, M4-c124); course/modules/M/M4/L08.html:74, 86", FAIL,
    "M4-c118 back: 'AQ ... gives the same mean and covariance (Remark 1.4)', but L08.html:86 now says this holds 'Assuming Lesson 6's Assumption 1' (the Proposition 1.3 hypothesis, L08.html:74). M4-c124 back: 'The covariance of AZ is AA^T (Proposition 1.3)' omits the hypothesis that L08.html:74 states ('Assuming Lesson 6's Assumption 1'). M4-c117 and M4-c115 carry it; c124 and c118 do not. Re-verified from scratch because L08.html changed since the round-10 pin.",
    "M4-c118: 'Under Lesson 6's Assumption 1, if QQ^T = I then AQ is also a factor of AA^T and gives the same mean and covariance (Remark 1.4).' M4-c124: 'Under Lesson 6's Assumption 1, the covariance of AZ is AA^T (Proposition 1.3).'")
row("C-03", "Cards with specific checks: c014, c019, c119, c132, c137, c191", "course/modules/M/M4/cards.json", PASS,
    "M4-c119 re-checked against L08.html Example 1.5 (AA^T = [[4,2],[2,2]], A^T A = [[5,1],[1,1]], B = AQ = [[0,-2],[1,-1]], BB^T = Sigma) and against the Example text, which is unchanged in substance; c014, c019, c132, c137 and c191: Carried from round 10 (course/modules/M/M4/cards.json entries byte-identical since the round-10 pin, and the lesson sections they cite not changed in the delta).")
row("C-04", "Grade C cards name a lab and its basis", "course/modules/M/M4/cards.json (grade C entries)", PASS,
    "21 grade C cards; each has a 'basis' naming Lab 1 (or Lab 1 Part), SIMULATED, the seed and the replication count; checked programmatically (C-01).")
row("C-05", "Cards quoting lab numbers (c098, c112, c191)", "course/modules/M/M4/cards.json c098, c112, c191", PASS,
    "Carried from round 10 (cards c098, c112, c191 byte-identical since the round-10 pin; their lab outputs and lesson sections are unchanged).")
row("C-06", "Changed cards, individually", "course/modules/M/M4/cards.json (M4-c006, c023, c035, c078, c123 removed, c125, c140, c163)", FAIL,
    "c006 (Proposition 2.2(d): L01 hypotheses 'positive weights and distinct values x_1 < ... < x_m', L01 Proposition 2.2 statement: PASS); c023 (L02 Proposition 2.3, positive weights, PASS); c035 (L03 Proposition 1.1, PASS); c078 (L05 Proposition 2.4 'finitely many values', PASS); c123 removed (the L08 Section 4 text it summarised still exists; no card cites c123; PASS, with the loss of one misconception card noted); c125 (Problem P3, L08.html:307-313, does evaluate A^T w for the factor of Example 1.5, PASS); c140 (L09 Proposition 2.3(b) under Assumption 1 of Section 2, PASS); c163 FAIL: the back says 'Parts B and C print one seeded run per law or size', but L10.html:183 says Part C 'runs 400 seeded replications at n', and L10.html:182-183 places the midpoint integral in Part A alone (the back also says Parts A and D evaluate a midpoint integral).",
    "M4-c163 back: 'No. Part A evaluates closed forms and a midpoint integral at fixed points, Part D evaluates closed forms, Part B prints one seeded path per law, and Part C runs 400 seeded replications per size (both graded C). The lab proves no limit, and Remark 2.2 is cited from Lesson 6 rather than proved.'")
row("C-07", "Card numbers appear in their lesson", "course/modules/M/M4/cards.json (changed cards)", PASS,
    "Proposition 2.2(d) (L01), Proposition 2.3 (L02), Proposition 1.1 (L03), Proposition 2.4 (L05), Remark 1.4 and Example 1.5 and Problem P3 (L08.html:85, 92, 307), Proposition 2.3(b) and Assumption 1 of Section 2 (L09), Remark 2.2 and Parts A to D (L10.html:182-186) all appear in their lessons.")
row("N-01", "Notation vs notation/notation.json", "notation/notation.json; course/modules/M/M4/project.html; cards.json", PASS,
    "notation.json lists 8 symbols; none of the registered meanings (\\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) is used with another meaning on the page or in the changed cards; \\E is used as expectation (registered macro). The new text uses only the same local symbols (nu, W, Z, L, R, s, Sigma).")
row("D-01", "DAG and concept closure, process words", "course/modules/M/M4/; check_dag", PASS,
    S + "check_dag.out: 'check_dag M4: PASS'. The project cites Lesson 1 (quantile), Lesson 6 (Definitions 2.1 and 2.5, checked at L06.html) and Lesson 6's Assumption 1 only; no new concept is introduced by the round-10 to round-11 delta (the new prose cites Assumption 1 and Proposition 1.3, both already in L08).")
row("T-01", "Relevant pytest files", "tests/test_memo_exemplars.py, tests/test_page_checks.py, tests/test_curriculum.py", PASS,
    S + "pytest_relevant.out: exit 0 (all tests in the three files pass).")
row("GATE-01", "Gates: check_pages, check_dag, check_projects, page_smoke (project)", "course/modules/M/M4/", PASS,
    S + "check_pages.out 'check_pages M4: PASS'; check_dag.out PASS; check_projects.out PASS; page_smoke_project.out 'page_smoke M4: PASS'.")
row("GATE-02", "Gates: ruff check, ruff format, mypy", "repository", PASS,
    S + "ruff.out: 'All checks passed!' and '362 files already formatted', exit 0; mypy.out: 'Success: no issues found in 255 source files', exit 0 (mypy --no-incremental).")
row("GATE-03", "Gates: run_graders M4 (seeds 0-49) and verify_refs --offline", "course/modules/M/M4/grader; references/", PASS,
    S + "run_graders.out: 'run_graders M4: PASS (reference 50/50 seeds ...)'; verify_refs.out: 'offline integrity: 560 entries, 0 problems', exit 0.")

ledger = {
    "unit": "M4", "slice": "d", "round": 11,
    "verifier": "independent verifier (Haiku), not a builder of M4",
    "pin": "f42f432",
    "base": "e8b10b8 (round-10 pin; previous fragment /Users/billyribeiro/.fanout/frags/B-M4-d.round10.json)",
    "checkout": str(ROOT),
    "scratch": "/tmp/M4-d-r11-scratch",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta e8b10b8..f42f432 for slice d: project.html (line 359 only: 'body is 90 words'), grader/test_project.py (lines 278-289: test_no_function_prints extended), cards.json (c006, c023, c035, c078 hypotheses added; c123 removed; c125, c140, c163 reworded), L08.html and L09.html (cited by cards; read in full around the changed hunks). instance.py, starter.py, reference.py, labs and notation unchanged.",
        "Round-10 FAIL rows G-20 and G-21 are repaired (both mutants now KILLED) and re-verified; not carried.",
        "Full project.html (502 lines) and test_project.py (517 lines) read line by line this round; instance.py and starter.py read in full; cards.json checked entry by entry for the changed cards and by script for the rest.",
        "Alternatives: reference, alt_1..alt_5 pass 50/50 seeds (run_alternatives.py --seeds 0-49); the two stream-order alternatives pass 50/50 seeds.",
        "Observation, not a FAIL: project.html:325 (A2) lists only 'assuming Assumption 1'; the hypothesis nu > 2 is in A1 and Conventions item 3. The page could list it in A2 (carried observation from round 10).",
        "Observation, not a FAIL: M4-c123 was removed without replacement; no lesson cites it.",
        "Gate note: a first collect-only run from the checkout failed to import tail_risk (no solution file in grader/); the collection was redone in a temp directory with reference.py as tail_risk.py (collect.out, 133 tests).",
    ],
    "summary": {},
    "gate_scope": "check_pages, check_dag, check_projects, page_smoke (project), run_graders (seeds 0-49), run_labs, verify_refs --offline, ruff, mypy, collect-only, mutate_graders --unit M4 (seeds 0-49), run_alternatives (seeds 0-49), per-seed runs of the new mutants, relevant pytest files (test_memo_exemplars, test_page_checks, test_curriculum). Repo-wide suites outside M4 were not run.",
}
counts = {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows), "fail": sum(r["status"] == "FAIL" for r in rows), "unverifiable": 0,
          "mutants_total": len(mutants), "mutants_killed": sum(1 for m in mutants if m["killed_by"])}
ledger["summary"] = counts
out = ROOT / "ledgers/M4/M4-d.json"
out.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(counts))
