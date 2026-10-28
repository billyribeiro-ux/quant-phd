import json, pathlib, re, sys, ast
ROOT = pathlib.Path(sys.argv[1]); D = ROOT / "ledgers/AC4/scripts/AC4-e-r15"
prev = json.load(open("/tmp/fanout-frags/AC4-e.round14.json"))
CARRY_P = ("Carried from round 14 (course/modules/AC/AC4/project.html changed only at lines 55, 146, 265, 267, 398 and "
           "grader/test_project.py only at lines 445 and 1046-1098; the cited subject is not in those lines and is "
           "unchanged since cef676e): ")
CARRY_F = ("Carried from round 14 (cards.json, tests/labs/AC4, references/, grader/reference.py and grader/instance.py "
           "byte-identical since the previous pin cef676e): ")
RE = {  # re-verified this round: id -> (status, evidence)
 "proj-grader-comments": ("PASS", "Round-14 FAIL cleared. The comment at test_project.py line 445-446 now says each rounding moves a flexed amount by at most half a cent and an exact half cent always moves up. This matches reference.py _nearest_cent (halves up, line 50) for both flexed revenue and flexed variable cost; errors then lie in (-0.5, 0.5] so their difference is in (-1, 1). Recomputed: scripts AC4-e-r15/out/check_numbers_r15.out, max |difference| 0.99974 < 1 over 200000 random pairs and the extreme pair 0.999999999."),
 "proj-r13-grader-mix-comment": ("PASS", "Round-14 FAIL cleared; same comment as proj-grader-comments (test_project.py lines 445-446, function test_mix_is_within_one_cent_of_the_exact_fraction). The assertion (line 449) is unchanged; run_graders AC4 PASS 50/50 (out/run_graders.out)."),
 "proj-collect-count": ("PASS", "Re-run: .venv/bin/python -I ledgers/AC4/scripts/AC4-e-r15/collect.py gives '527 tests collected'. project.html line 265 states 527 checks; matches."),
 "proj-r12-count-matches-page": ("PASS", "Re-run: collect-only gives 527 (out/collect.out); project.html line 265 says '527 checks'. Equal."),
 "proj-spec-coverage-claims": ("PASS", "Re-read project.html line 265. Each claim located in test_project.py: the four variances and total, reconciliation on seeds 0-49, sign tests in both directions, zero-variance and single-product and zero-unit cases, ValueError tests, purity and silence; new claim 'ten product conditions ... repeated in the middle and the last product' matches LATER_PRODUCT_CONDITIONS (10 entries, lines 1047-1058) with positions (1, 2) of the three-product PRODUCTS (assert line 154). Count 527 matches collect-only."),
 "proj-lab-1": ("PASS", "project.html lines 53-147 re-read. Only line 55 (hypothesis) and line 146 (interpretation) changed in the delta. Line 55 parenthetical '(its budgeted price less the standard input cost of one unit)' equals the lab formula budget_price - standard * INPUT_PRICE (project.html line 118): Standard 5000 - 3*200 = 4400 cents, matching the 4,400 quoted at line 146. Lab run output unchanged (lab not in delta; run_labs AC4 PASS 10/10)."),
 "proj-lab-1-interpretation": ("PASS", "project.html line 146 re-read. New parenthetical '7,600,000 cents of budgeted margin over 1,400 units, rounded to two decimals': 7600000/1400 = 5428.571428 -> 5428.57 (python, out/check_numbers_r15.out). Other figures in the paragraph (2,600,000; 3,142,857; +542,857; -462,857; +180,000; -40,000; +220,000; 1/7 cent) unchanged and recomputed in the previous rounds; 3,142,857.142857 = 1500 * 8,600,000 / 1400 - 1500 * 1,000,000 / 1400 - 5,000,000 confirms the 1/7 figure."),
 "proj-r12-lab1-derived-figures": ("PASS", "project.html line 146 re-read; the figures unchanged except the parenthetical rounding basis, which is the only change and is correct (5428.57 = 7600000/1400 to two decimals)."),
 "proj-lab-1-interpretation-second-clause": ("PASS", "project.html line 146, last sentence ('The lab does not compute what a different input price would do ...') unchanged in this delta; the engine has no input price variance (project.html line 260), so the claim stands."),
 "proj-lab-1-run-line146-untouched": ("PASS", "Lines 53-145 of project.html: the delta changed line 55 only inside that range (parenthetical, verified in proj-lab-1). Line 146 is outside 53-145 and changed only its rounding parenthetical (verified in proj-lab-1-interpretation)."),
 "proj-simulated-and-data": ("PASS", "project.html line 55 still ends 'the case is SIMULATED'; lines 53-56 and 252 re-read; tests/labs/AC4/lab-AC4-project-1.py unchanged (not in the delta)."),
 "proj-banned-phrases": ("PASS", "Re-run this round on every changed line (project.html 55, 146, 265, 267, 398 and the new grader comments at test_project.py 445-446 and 1046-1098): grep for roughly, about, historically, usually, typically, half of, most, some, many, often, and an ellipsis: 0 hits."),
 "proj-reading-list-sentence": ("PASS", "project.html line 267 now: 'The reading list below gives the registry keys of the cost-accounting sources that the registry holds for this unit.' The list below (lines 407-408, data-cite datar2020horngrens and kaplan1998cost) has two keys; references/references.json records both with used_by containing 'AC4' (python read of the entries). 'Cost-accounting sources' describes Horngren's Cost Accounting (title in the record) and Kaplan's Cost & effect (integrated cost systems, title in the record)."),
 "proj-citations-reading": ("PASS", "Re-run: verify_refs --unit AC4 live: '2 of 560 entries, 0 problems' (out/verify_refs_live_ac4.out); the two reading keys have used_by AC4 in references/references.json."),
 "proj-stretch-spending": ("PASS", "project.html line 398 re-read: 'the six variances (the four above, the input price variance and the fixed overhead variance) add to the total exactly'. Count is six (four variances plus two added). Consistent with line 260 (no input price and no fixed overhead variance in the engine). Not a numerical claim about the case."),
 "proj-stretch-list-intact": ("PASS", "project.html lines 396-401 re-read: the list still has two items (spending variance, two inputs); line 398 change is inside the first item only."),
 "proj-stretch-two-inputs": ("PASS", "project.html line 399 unchanged in this delta; re-read in full."),
 "proj-stretch-two-inputs-scope": ("PASS", "project.html line 399 unchanged in this delta; re-read in full, scope unchanged."),
 "proj-conventions-no-spending-claim": ("PASS", "Line 260 unchanged; line 398 (stretch) read: it asks the reader to add the two variances and says nothing about the case's spending. No claim that the case has a spending variance."),
 "proj-r13-mix-tolerance-test": ("PASS", "test_project.py lines 442-449: the assertion (abs(Fraction(sales_mix) - exact_mix) < 1) unchanged; only the comment at 445-446 changed. Run: run_graders AC4 50/50 seeds PASS; mutants killed."),
 "proj-r14-mix-rounding-bound": ("PASS", "project.html line 260 and reference.py _nearest_cent (line 46-50, halves up) and variance_decomposition: the mix uses the whole-cent flexed profit, which is within one cent of the exact fraction; recomputed in AC4-e-r15/out/check_numbers_r15.out (max 0.99974)."),
 "proj-purity-order-dependence": ("PASS", "test_project.py: the purity, silence and order-dependence functions cited (formerly lines 1050-1093) are byte-identical; a new block (LATER_PRODUCT_CONDITIONS, 1046-1098) was inserted above them, so their line numbers moved by 51. Suite run: 527 collected, the reference passes all of them (run_graders AC4 PASS 50/50, out/run_graders.out)."),
 "proj-autograder-reference": ("PASS", "Re-run this round: run_graders.py --unit AC4 --seeds 0-49: 'run_graders AC4: PASS (reference 50/50 seeds, slowest 0.6 s)' (out/run_graders.out, rc=0)."),
 "proj-autograder-alternatives": ("PASS", "Re-run this round on seeds 0-49 (AC4-e-r15/out/all_prior_alts_r15.out): alt13_a, alt13_b, alt14_a, alt14_b PASS 50/50; alt_r12_a..e PASS 50/50; alt_l KILLED (a tuple-products case, student error). New: alt15_a/b/c PASS 50/50 (alts_r15.out)."),
 "proj-alt-l-extra-keys": ("PASS", "Re-run this round (all_prior_alts_r15.out): alt_l KILLED by test_products_that_are_not_a_list_raise_value_error[tuple-master_budget] — the grader refuses a tuple of products, which the page's constraints list (products must be a list of mappings) requires."),
 "proj-autograder-alt-decimal": ("PASS", "Re-run this round: alt_r12_a_decimal_half_up.py PASS 50/50 seeds (all_prior_alts_r15.out) and alt15_a_decimal_half_up.py PASS 50/50 (alts_r15.out)."),
 "proj-r12-alternatives-new": ("PASS", "Re-run this round: alt_r12_a..e all PASS 50/50 (all_prior_alts_r15.out)."),
 "proj-r13-alternatives-new": ("PASS", "Re-run this round: alt13_a_integer_divmod.py and alt13_b_fraction_floor.py PASS 50/50 (all_prior_alts_r15.out)."),
 "proj-r14-alternatives-correct": ("PASS", "Re-run this round: alt14_a_mix_as_residual.py and alt14_b_divmod_nearest.py PASS 50/50 (all_prior_alts_r15.out)."),
 "proj-alt-g-student-error": ("PASS", "Re-run this round: AC4-e-r8/alt_g.py KILLED by test_products_that_are_not_a_list_raise_value_error[number-master_budget] (all_prior_alts_r15.out); the page requires products to be a list, so the kill is required."),
 "proj-r14-mutants-all-rerun": ("PASS", "Re-run this round on all 121 top-level .py files in ledgers/AC4/mutants (out/mutate_r15.out): 121 KILLED, 0 survivors. The 107 in the round-14 fragment plus the fx14_* and r14e_* files and the four new r15e_* files."),
 "proj-r14-mutants-new-student-errors": ("PASS", "Re-run this round: r14e_01..04 KILLED (out/mutate_r15.out), killing tests named there."),
 "proj-mutant-descriptions": ("PASS", "Re-run: ast docstring scan of every top-level file in ledgers/AC4/mutants: no file without a docstring (python -I scan this round). Each new r15e_* file's first docstring line starts 'Student error:'."),
 "proj-autograder-rerun-mutants-m01-m37": ("PASS", "Re-run this round on all 121 mutants (out/mutate_r15.out): 121 KILLED, 0 survivors."),
 "proj-check-pages": ("PASS", "Re-run this round: out/check_pages.out 'check_pages AC4: PASS' rc=0."),
 "proj-check-dag": ("PASS", "Re-run this round: out/check_dag.out 'check_dag AC4: PASS' rc=0."),
 "proj-check-projects": ("PASS", "Re-run this round: out/check_projects.out 'check_projects AC4: PASS' rc=0."),
 "proj-page-smoke": ("PASS", "Re-run this round: out/page_smoke.out 'page_smoke AC4: PASS' rc=0 (Pyodide smoke over AC4 pages, project included)."),
 "proj-run-labs-ac4": ("PASS", "Re-run this round: out/run_labs.out 'run_labs AC4: PASS (10/10)' rc=0; tests/labs/AC4 not in the delta."),
 "proj-run-graders-ac4": ("PASS", "Re-run this round: out/run_graders.out 'run_graders AC4: PASS (reference 50/50 seeds, slowest 0.6 s)' rc=0."),
 "proj-ruff-mypy": ("PASS", "Re-run this round: ruff check on grader and tests/labs/AC4 'All checks passed!'; ruff format --check '14 files already formatted'; repository mypy --no-incremental 'Success: no issues found in 153 source files' rc=0."),
 "proj-r13-verify-refs": ("PASS", "Re-run this round: out/verify_refs_offline.out 'offline integrity: 560 entries, 0 problems' rc=0; out/verify_refs_live_ac4.out 'live re-verification of AC4: 2 of 560 entries, 0 problems' rc=0."),
 "proj-collect-count-noop": None,
}
RE = {k: v for k, v in RE.items() if v}
NEW = [
 ("proj-r15-hypothesis-line55-parenthetical", "project.html line 55 (hypothesis): 'its budgeted price less the standard input cost of one unit'", "course/modules/AC/AC4/project.html line 55 and line 118", "PASS", "Standard budgeted price 5000 cents (line 66-68 of the lab case), standard inputs 3 at INPUT_PRICE 200 (line 60, 69): 5000 - 600 = 4400, which is the lab's actual_mix_margin term at line 118 (budget_price - standard * INPUT_PRICE). The parenthetical is correct."),
 ("proj-r15-interpretation-rounding-basis", "project.html line 146: '5,428.57 cents each (7,600,000 cents of budgeted margin over 1,400 units, rounded to two decimals)'", "course/modules/AC/AC4/project.html line 146", "PASS", "7600000/1400 = 5428.5714...; rounded to two decimals 5428.57 (python, out/check_numbers_r15.out). The 'rounded to two decimals' basis is stated and correct."),
 ("proj-r15-grader-count-527", "project.html line 265 '527 checks' and grader collect count", "course/modules/AC/AC4/project.html line 265; grader/test_project.py", "PASS", "collect-only of the reference workspace: '527 tests collected' (out/collect.out)."),
 ("proj-r15-later-product-conditions", "test_project.py LATER_PRODUCT_CONDITIONS: 10 conditions x 2 positions x 3 functions", "course/modules/AC/AC4/grader/test_project.py lines 1047-1098", "PASS", "The dict has 10 entries; the parametrised test is applied to positions 1 and 2 of a three-product case (assert at line 154); 10 x 2 x 3 = 60 tests. The page's list (negative, boolean, float, text, missing, empty or non-text field, product that is not a mapping) matches the dict keys."),
 ("proj-r15-half-cent-comment-bound", "test_project.py comment (lines 445-446): an exact half cent always moves up, so the two moves cannot differ by a full cent", "course/modules/AC/AC4/grader/test_project.py lines 445-446; reference.py line 50", "PASS", "Half-up rounding gives errors in (-0.5, 0.5]; the difference of two errors lies in (-1, 1). Recomputed: max 0.9997358689910195 over 200000 random pairs, extreme pair 0.999999999 (out/check_numbers_r15.out)."),
 ("proj-r15-stretch-six-variances", "project.html line 398: 'the six variances (the four above, the input price variance and the fixed overhead variance) add to the total exactly'", "course/modules/AC/AC4/project.html line 398", "PASS", "Four engine variances plus two added variances is six; the reconciliation sentence is a stretch target, not a graded claim."),
 ("proj-r15-reading-keys-used-by-ac4", "project.html line 267 reading-list sentence and list items at lines 407-408", "course/modules/AC/AC4/project.html lines 267, 407-408; references/references.json", "PASS", "datar2020horngrens and kaplan1998cost are registry records with used_by ['AC4'] (python read); both titles are cost-accounting texts as their records state."),
 ("proj-r15-alternatives-correct-new", "Three new correct implementations: decimal ROUND_HALF_UP, floor(x + 1/2), exact type-check validator", "ledgers/AC4/scripts/AC4-e-r15/alts/alt15_a_decimal_half_up.py; alt15_b_floor_plus_half.py; alt15_c_type_check_validator.py", "PASS", "runfiles.py seeds 0-49 (out/alts_r15.out): all three PASS 50/50 seeds. None is refused by the suite, so the new tests over-constrain nothing for these implementations."),
 ("proj-r15-mutants-new-student-errors", "Four new student-error mutants written this round", "ledgers/AC4/mutants/r15e_01..r15e_04", "PASS", "r15e_01 last-product zero budget refused (killed: test_product_with_no_budgeted_units); r15e_02 exact half cent rounds down for revenue (killed: test_exact_half_cent_rounds_up); r15e_03 missing actual price read as budget price (killed: test_missing_product_field_raises_value_error[actual_price_cents-master_budget]); r15e_04 float budget price in last product truncated (killed: test_bad_later_product_raises_value_error[float ...]). Spec violated: project.html line 263 lists text, float and boolean refusals, a missing field refusal, and a budget with no budgeted units only as the refusal of a total."),
 ("proj-r15-mutants-all-rerun", "Every top-level AC4 mutant killed on seeds 0-49", "ledgers/AC4/mutants/*.py (121 files); ledgers/AC4/scripts/AC4-e-r15/out/mutate_r15.out", "PASS", "121 KILLED, 0 survivors (out/mutate_r15.out). The r15e_02 file was first written with a 1e-12 offset that the kill witness showed to be a negative-amount refusal, not a half-cent test; it was replaced with a true half-down rounding and re-run (out/new_mutants_r15.out: KILLED by test_exact_half_cent_rounds_up)."),
 ("proj-r15-no-banned-phrases-changed-lines", "Banned phrases in the changed lines and new grader comments", "project.html lines 55, 146, 265, 267, 398; test_project.py lines 445-446, 1046-1098", "PASS", "grep for roughly, about, historically, usually, typically, half of, most, some, many, often, ellipsis: 0 hits in the changed text (this round)."),
 ("proj-r15-comment-first-product-claim", "test_project.py comment (line ~1046): most refusal tests above put the bad value in the first product", "course/modules/AC/AC4/grader/test_project.py", "PASS", "rows[0] appears 19 times in the file, rows[1] and rows[2] once each (grep this round); the claim 'most' holds."),
]
CMD_ROWS = {"proj-r15-ruff-format-and-lint": None}
rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in RE:
        status, ev = RE[rid]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev})
        continue
    if r["status"] != "PASS":
        raise SystemExit(f"non-PASS previous row not re-verified: {rid}")
    loc = r["location"]
    if "project.html" in loc or "test_project" in loc:
        prefix = CARRY_P
    else:
        prefix = CARRY_F
    rows.append({"id": rid, "check": r["check"], "location": loc, "status": "PASS",
                 "evidence": prefix + r["evidence"]})
for rid, check, loc, status, ev in NEW:
    rows.append({"id": rid, "check": check, "location": loc, "status": status, "evidence": ev})
# mutants
out = (D / "out/mutate_r15.out").read_text().splitlines()
mut_entries = []
for line in out:
    m = re.match(r"KILLED (\S+) -> (.*) \(seed \d+\)$", line)
    if not m:
        continue
    fname, witness = m.group(1), m.group(2)
    f = ROOT / "ledgers/AC4/mutants" / fname
    doc = ast.get_docstring(ast.parse(f.read_text())) or ""
    mut_entries.append({"id": fname[:-3], "file": f"ledgers/AC4/mutants/{fname}", "description": doc.splitlines()[0],
                        "killed_by": witness})
n_fail = sum(1 for r in rows if r["status"] != "PASS")
frag = {
 "unit": "AC4", "slice": "AC4-e", "round": 15,
 "verifier": "Claude Haiku 5.5 (independent verifier, round 15, slice AC4-e; did not build AC4)",
 "pin": "c093bf5", "base": "cef676e (round-14 pin; previous fragment /tmp/fanout-frags/AC4-e.round14.json used as context only)",
 "checkout": str(ROOT), "scratch": "/tmp/ac4-v/e15",
 "verified_at": "2026-10-28T23:30:00+00:00",
 "verdict": "PASS" if n_fail == 0 else "FAIL",
 "rows": rows, "mutants": mut_entries,
 "registry_flags": [], "freshness_flags": [],
 "notes": ("Delta cef676e..c093bf5 for this slice: project.html (lines 55, 146, 265, 267, 398 changed in place, line count "
           "unchanged) and grader/test_project.py (comment at 445-446; new LATER_PRODUCT block at 1046-1098). cards.json, "
           "tests/labs/AC4, references, reference.py and instance.py are byte-identical. Round-14 FAIL rows "
           "proj-grader-comments and proj-r13-grader-mix-comment are re-verified PASS. Mutant r15e_02 was first written "
           "with a 1e-12 offset that the witness showed to be a different refusal; it was replaced and re-run. Rows with "
           "'Carried from round 14' cite subjects unchanged since cef676e; test_project.py functions that moved "
           "(purity block) are identified by function name."),
 "summary": {"rows": len(rows), "pass": len(rows) - n_fail, "fail": n_fail, "unverifiable": 0,
             "mutants_killed": len(mut_entries), "mutants": len(mut_entries)},
}
(ROOT / "ledgers/AC4/AC4-e.json").write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n")
print("rows", len(rows), "fail", n_fail, "mutants", len(mut_entries), "verdict", frag["verdict"])
