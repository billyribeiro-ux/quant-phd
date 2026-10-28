"""Write ledgers/AC4/AC4-e.json (round 11) from the mutate-gate output and the round-11 check results."""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
GATE = pathlib.Path(sys.argv[2]).read_text(encoding="utf-8").splitlines()
PREV = json.loads(pathlib.Path("/tmp/fanout-frags/AC4-e.round10.json").read_text(encoding="utf-8"))
MUT = ROOT / "ledgers/AC4/mutants"

killed = {}
for line in GATE:
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*?) -> (.*)$", line)
    if m:
        status, name, desc, where = m.groups()
        killed[name] = (status, where.strip())
mutants = []
for path in sorted(MUT.glob("*.py")):
    text = path.read_text(encoding="utf-8")
    first = text.splitlines()[0].strip('"').strip()
    status, where = killed.get(path.name, ("MISSING", ""))
    entry = {"id": path.stem, "file": f"ledgers/AC4/mutants/{path.name}", "description": first}
    if status == "KILLED":
        entry["killed_by"] = where
    mutants.append(entry)

prev_rows = {r["id"]: r for r in PREV["rows"]}
CARRY = "Carried from round 10 (course/modules/AC/AC4/{files} byte-identical since the previous pin af08ad1): "
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix:
        r["fix"] = fix
    rows.append(r)


def carry(rid, files, note=None):
    prev = prev_rows[rid]
    assert prev["status"] == "PASS", rid
    ev = CARRY.format(files=files) + prev["evidence"] + ((" " + note) if note else "")
    row(rid, prev["check"], prev["location"], "PASS", ev)


# --- command and gate rows, re-run on 91946cf
row("proj-autograder-reference", "Reference solution passes the whole suite on the learner-facing grader files",
    "course/modules/AC/AC4/grader/reference.py; course/modules/AC/AC4/grader/test_project.py",
    "PASS", "Re-run round 11: pytest of the reference copied to a scratch dir, QF_SEED=0..49, each '360 passed' "
    "(loop output: 0 deviations; /tmp/ac4-v/e11/ref); tools/run_graders.py --unit AC4 --seeds 0-49 -> "
    "'run_graders AC4: PASS (reference 50/50 seeds, slowest 0.2 s)' (/tmp/ac4-v/e11/graders.txt).")
row("proj-collect-count", "The page's test count equals the real collect-only count",
    "course/modules/AC/AC4/project.html line 265 (Grading mode); course/modules/AC/AC4/grader/test_project.py",
    "PASS", "Line 265 now says 360 checks (was 296). pytest --collect-only with the reference on each of seeds 0-49: "
    "'360 tests collected' on all 50 seeds (scratch /tmp/ac4-v/e11/collect). Page line 265 matches.")
row("proj-autograder-alternatives",
    "Alternative correct implementations pass the suite (over-constraint check)",
    "course/modules/AC/AC4/grader/test_project.py; ledgers/AC4/scripts/AC4-e-r8/alt_a..alt_j.py, alternatives_r4.py, "
    "AC4-e-r9/alt_k.py, AC4-e-r10/alt_l.py",
    "PASS", "ledgers/AC4/scripts/AC4-e-r11/run_alts_r11.py on seeds 0-9 and 25: alt_a, alt_b, alt_c, alt_e, alt_f, "
    "alt_h, alt_i, alt_j, alt_k, alt_l each '360 passed' on all 11 seeds (/tmp/ac4-v/e11/alts). alt_g fails 12 tests "
    "(case None, products as a mapping or text, a product given as a list) with TypeError or AttributeError where the "
    "page's Constraints line (line 263) requires ValueError; alt_g is therefore not a correct implementation under the "
    "current page and the new refusal tests catch it. No correct alternative is over-constrained.")
row("proj-alt-l-extra-keys", "proj-alt-l-extra-keys",
    "ledgers/AC4/scripts/AC4-e-r10/alt_l.py; course/modules/AC/AC4/grader/test_project.py",
    "PASS", "alt_l (reference plus informational extra keys) passes 360/360 on all 11 seeds in the run_alts_r11 run.")
row("proj-autograder-alt-decimal", "A Decimal half-up implementation (different valid algorithm) passes the suite",
    "ledgers/AC4/scripts/AC4-e-r9/alt_k.py; course/modules/AC/AC4/grader/test_project.py",
    "PASS", "alt_k (Decimal half-up rounding) passes 360/360 on all 11 seeds (run_alts_r11).")
row("proj-autograder-rerun-mutants-m01-m37", "Full mutant set killed on seeds 0-9",
    "ledgers/AC4/mutants (m01-m55 and fx10_*)", "PASS",
    "Round 11 re-run of every committed mutant on seeds 0, 1, 25 (ledgers/AC4/scripts/AC4-e-r11/run_mutants.py; "
    "/tmp/ac4-v/e11/mutants_r11.txt): 60 of 60 KILLED. tools/mutate_graders.py --unit AC4 --seeds 0-9 (final, 64 "
    "mutants): 63 killed, m52 survives (see proj-mutant-m52-dict-only-case).")
row("proj-mutant-descriptions", "Mutant docstrings describe each error",
    "ledgers/AC4/mutants/ (first docstring line of every mutant)", "PASS",
    "Every mutant file opens with a one-line docstring naming its error (checked in the mutate_graders output, "
    "/tmp/ac4-v/e11/mutate_gate_final.txt, which prints each description).")
for rid in ("proj-mutants-m01-m06", "proj-mutant-m07-empty-name", "proj-mutants-m08-m11", "proj-mutant-m12-duplicate-names",
            "proj-mutants-m13-m20", "proj-mutants-m15-m19", "proj-mutants-m21-m24", "proj-mutants-m21-m24-equivalence",
            "proj-mutants-m25-m29", "proj-mutants-r6-new", "proj-mutants-r7-new", "proj-mutants-r8-new",
            "proj-mutants-r9-new", "proj-mutants-r10-new"):
    row(rid, prev_rows[rid]["check"], prev_rows[rid]["location"], "PASS",
        "Re-run round 11 on seeds 0, 1, 25: each named mutant KILLED (/tmp/ac4-v/e11/mutants_r11.txt).")
row("proj-check-pages", "check_pages --all passes for AC4", "course/modules/AC/AC4/*.html and cards.json", "PASS",
    "Re-run round 11: 'check_pages AC4: PASS' (/tmp/ac4-v/e11/gates1.txt).")
row("proj-check-dag", "check_dag --all passes for AC4", "course/modules/AC/AC4", "PASS",
    "Re-run round 11: 'check_dag AC4: PASS' (/tmp/ac4-v/e11/gates1.txt).")
row("proj-check-projects", "check_projects --all passes for AC4", "course/modules/AC/AC4/project.html", "PASS",
    "Re-run round 11: 'check_projects AC4: PASS' (/tmp/ac4-v/e11/gates1.txt).")
row("proj-page-smoke", "page_smoke passes for the project page in Chromium, light and dark, at 360 px",
    "course/modules/AC/AC4/project.html", "PASS",
    "Re-run round 11: tools/page_smoke.py --unit AC4 --pages project -> 'page_smoke modules/AC/AC4/project.html: PASS', "
    "'page_smoke AC4: PASS', in-browser grader 'All 360 tests pass on seed 343313797' (/tmp/ac4-v/e11/page_smoke.txt).")
row("proj-ruff-mypy", "ruff and mypy (repo-wide strict) pass for the grader, labs and pages",
    "course/modules/AC/AC4/grader; tests/labs/AC4; repository mypy configuration", "PASS",
    "Re-run round 11: 'ruff check .' -> 'All checks passed!'; 'ruff format --check' on grader and labs -> 14 files "
    "already formatted; 'mypy --no-incremental' -> 'Success: no issues found in 153 source files'.")
row("proj-run-labs-ac4", "run_labs passes for every AC4 lab (10 labs)", "tests/labs/AC4", "PASS",
    "Re-run round 11: tools/run_labs.py --unit AC4 -> 'run_labs AC4: PASS (10/10)' (/tmp/ac4-v/e11/labs.txt).")
row("proj-banned-phrases", "Banned phrases and process words absent from the project page and cards",
    "course/modules/AC/AC4/project.html; course/modules/AC/AC4/cards.json", "PASS",
    "Re-run round 11 on the changed text: regex scan of project.html and every cards.json front/back/basis for "
    "roughly, about N, historically, typically, usually, generally, often, ellipses, builder, verifier, round, "
    "REQUEST, unit report: no card hit; project.html hits are the ordinary word 'rounded' or 'rounding' only "
    "(lines 146, 258, 260, 279, 365).")
carry("proj-memo-structure-length", "project.html (exemplar memo blocks, lines 330-340 and 361-373)")
carry("proj-exemplar-intro-universal-claim", "project.html line 324 (exemplars intro)")
carry("proj-exemplar-overall-level", "project.html lines 324, 327 and 357 (exemplar levels)")
row("proj-cards-structure", "cards.json structure: unique ids, lesson exists, required fields, grade set",
    "course/modules/AC/AC4/cards.json (129 cards)", "PASS",
    "Re-run round 11: 129 cards (was 119 in round 10 and 128 at 96dd532-af08ad1 delta), ids unique and sorted, every "
    "lesson in L01-L08, every card has id, lesson, front, back; grade optional (T 48, C 48, no grade 33); every C "
    "card has a basis and no non-C card does; tools/check_pages.py --all -> PASS.")
row("proj-cards-duplicates", "No duplicate card fronts, backs or ids", "course/modules/AC/AC4/cards.json", "PASS",
    "Re-run round 11: 129 unique ids, 0 duplicate fronts, 0 duplicate backs.")
carry("proj-cards-sample", "cards.json (c010-c080 sampled cards)")
row("proj-card-c126-basis", "AC4-c126 basis cites the lab output, not Proposition 2.2",
    "course/modules/AC/AC4/cards.json (AC4-c126, basis); course/modules/AC/AC4/L03.html lines 292-300 (lab output)",
    "PASS", "Round 10 FAIL is fixed. The basis is now 'Lab 1 (SIMULATED), make-or-buy lines (full-cost comparison, "
    "11.10 per unit against 10.50)'. The lab output (L03.html lines 294 'full make cost per unit ...: 11.10', 295 "
    "'buy price per unit: 10.50', 300 'full-cost decision: buy') carries each figure, and the back text matches it.")
row("proj-card-c102", "AC4-c102 back matches the L08 lesson after the edit",
    "course/modules/AC/AC4/cards.json line 718-721 (AC4-c102, T; back at line 721); course/modules/AC/AC4/L08.html line 306", "PASS",
    "The new back ('False as a general rule ... RI = (OI/C - r)C ... depends on the question asked') restates "
    "L08.html line 306 (same return above the rate gives the larger RI, because RI = (OI/C - r)C) and line 306's "
    "closing sentence. It states no figure, so it cannot disagree with the lesson's numbers. The X and Y figures "
    "it dropped are now on card AC4-c129.")
row("proj-card-c129", "AC4-c129 numbers match L08 Section 5 and their arithmetic",
    "course/modules/AC/AC4/cards.json line 914 (AC4-c129, T); course/modules/AC/AC4/L08.html line 128 (§5)",
    "PASS", "L08.html line 128 gives C=500, OI=60, r=9% for X and C=2,000, OI=200, r=9% for Y. Recomputed: RI_X = 60 - "
    "0.09 x 500 = 15; RI_Y = 200 - 0.09 x 2000 = 20. The card's 15 SCU and 20 SCU match, and the unit SCU matches "
    "L08.html line 306.")
for rid, files in (("proj-cards-r10-L01", "cards.json AC4-c003, c012, c014, c120, c127, c128 and their lesson"),
                   ("proj-cards-r10-L02", "cards.json AC4-c029, c125"),
                   ("proj-cards-r10-L03", "cards.json AC4-c038, c040, c042, c043, c122, c123, c124"),
                   ("proj-cards-r10-L04", "cards.json AC4-c045, c121")):
    carry(rid, files)
carry("proj-cards-changed-lessons-r10", "cards.json AC4-c059..c068 and the L05/L06 lessons (unchanged)")
carry("proj-instances", "grader/instance.py")
row("proj-alt-instance-coverage", "Starter fails the suite; instances cover the seed range",
    "course/modules/AC/AC4/grader/instance.py; course/modules/AC/AC4/grader/starter.py", "PASS",
    "Re-run round 11: the starter on seed 0 -> '354 failed, 6 passed'; the page's line 254 says the suite fails on the "
    "starter. Instance coverage: round 10 evidence carried (instance.py byte-identical since af08ad1); all 50 seeds "
    "give 3 products (/tmp/ac4-v/e11/seed_checks, ledgers/AC4/scripts/AC4-e-r11/seed_checks.py).")
row("proj-spec-empty-name-claim", "Constraint: a product name that is empty is refused",
    "course/modules/AC/AC4/project.html line 263 (Constraints); course/modules/AC/AC4/grader/test_project.py "
    "test_empty_product_name_raises_value_error", "PASS",
    "Line 263 names 'a product name that is not text, is empty or appears twice'; test_empty_product_name_raises_value_error "
    "checks all three functions; the empty-name mutant m07 is killed.")
row("proj-spec-fresh-objects-claim", "master_budget returns a fresh object on each call",
    "course/modules/AC/AC4/project.html line 263; course/modules/AC/AC4/grader/test_project.py "
    "test_master_returns_fresh_objects", "PASS", "Line 263 claim; test_master_returns_fresh_objects asserts "
    "first is not second and clearing first leaves the next call intact; mutant m27 is killed.")
row("proj-spec-clarity-and-errors", "Constraints line lists every ValueError the tests enforce",
    "course/modules/AC/AC4/project.html line 263 (Constraints); course/modules/AC/AC4/grader/test_project.py",
    "PASS", "Each condition on line 263 has a test: not a mapping (test_case_that_is_not_a_mapping); products not a "
    "list (test_products_that_are_not_a_list, dict and text only; see proj-spec-products-list-tuple); product not a "
    "mapping; name not text, empty, duplicate; text, float and boolean numbers (case, product and unit argument); "
    "negative count or amount; empty product list; no budgeted units; negative or non-integer unit argument. "
    "Each test asserts ValueError. The tuple case is the only listed item with no test of its own.")
row("proj-spec-coverage-claims", "Project line 265 claims the suite covers each named ValueError, purity and silence",
    "course/modules/AC/AC4/project.html line 265; course/modules/AC/AC4/grader/test_project.py", "PASS",
    "Line 265 items map to tests: each named ValueError (above), purity (test_functions_do_not_change_their_arguments, "
    "test_functions_do_not_reorder_their_products), silence (test_functions_are_silent); the 360 count equals the "
    "collect-only count (proj-collect-count).")
row("proj-spec-sign-both-directions", "Line 265: the sign of each variance is tested in both directions",
    "course/modules/AC/AC4/project.html line 265; test_project.py lines 393-430, 463-510, 559-575",
    "PASS", "Price: test_price_variance_is_favourable_when_price_rises and ..._unfavourable_when_every_price_falls. "
    "Volume: ..._favourable_when_more_units_are_sold and ..._unfavourable_when_fewer_units_are_sold. Mix: "
    "test_two_product_shift_to_higher_margin_is_favourable (explicit cents, >0) and test_two_product_shift_to_lower_margin_"
    "is_unfavourable (<0; seed-based but the equal-margin branch is never taken: the first two budgeted margins differ on "
    "all seeds 0-49, checked in seed_checks). Efficiency: positive and negative tests at lines 414-428.")
row("proj-spec-reconcile-seeds", "Line 265: reconciliation on seeds 0 to 49",
    "course/modules/AC/AC4/grader/test_project.py lines 694-699", "PASS",
    "test_every_grader_seed_reconciles_exactly is parametrized over range(50); the reference passes all 50 seeds.")
row("proj-messages-no-leak", "Assertion messages do not reveal reference values (grader docstring: 'it never prints the expected value')",
    "course/modules/AC/AC4/grader/test_project.py lines 343 and 612 (messages), module docstring (line 11)",
    "FAIL", "The module docstring says a failure 'never prints the expected value'. Two assert messages print an expected "
    "value: line 343 'a half cent rounds up, to 501.' and line 612 'a third of a cent rounds down to 0 cents.' Both "
    "are constant messages for fixed hand-built fixtures (the answers are also in the test's own comments at lines "
    "323 and 592), not seed-case values, so no seed value leaks; but the docstring's stated guarantee is violated "
    "literally. Lines 343 and 612 were the only messages inspected for this; all other messages were read and carry no "
    "number.",
    fix="Either drop the numeral from the two messages (line 343: 'a half cent must round up'; line 612: 'a third of "
        "a cent must round down') or reword the module docstring to 'it never prints a seed-case expected value'.")
row("proj-messages-bare-asserts", "Every assert in the grader carries a message", "course/modules/AC/AC4/grader/test_project.py",
    "PASS", "AST scan of test_project.py: no ast.Assert node without a msg (the new asserts at lines 486-510, 513-544, "
    "547-575, 577-614 and 739-1001 all carry messages).")
row("proj-grader-comments", "Grader comments are accurate (PRISTINE comment and the new comments)",
    "course/modules/AC/AC4/grader/test_project.py lines 43-44, 475-477, 486, 514, 592, 740, 796, 819",
    "PASS", "Re-read each new comment against the code: margins 5400 and 8000 cents (line 486: 6000-3*200 and 9000-5*200); "
    "equal margins of 1000 cents (line 514: 1400-400, 1600-600, 1800-800); 1/3 cent (line 592: budget revenue 3 over 9 "
    "units); the equal-margin proof (lines 475-477) holds because AT*m is an integer. Line 796's 'as the page states' is "
    "supported by page line 263 listing floats as refused.")
row("proj-mutant-m52-dict-only-case", "A case that is a non-dict Mapping is accepted (page line 252: 'One case, a mapping')",
    "ledgers/AC4/mutants/m52_case_must_be_a_dict.py; course/modules/AC/AC4/grader/test_project.py (no test feeds a "
    "non-dict Mapping); course/modules/AC/AC4/project.html line 252", "FAIL",
    "m52 (the case is refused unless isinstance(case, dict)) passes 360/360 on seeds 0, 1, 25 and survives "
    "mutate_graders --seeds 0-9. The page says the case is 'a mapping' (line 252). The reference accepts any "
    "collections.abc.Mapping (witness: types.MappingProxyType(case) accepted by master_budget and "
    "variance_decomposition, /tmp/ac4-v/e11/witness_tuple_mapping.py), so a valid input is refused by m52 and no test "
    "catches it.",
    fix="Add a test: master_budget(types.MappingProxyType(CASE)) and variance_decomposition of the same mapping equal "
        "the dict results (the page's 'a mapping' is what the test must check).")
row("proj-spec-products-list-tuple", "Constraints line: products that are not a list of mappings raise ValueError",
    "course/modules/AC/AC4/project.html line 263 (Constraints) and line 252 ('a list of mappings'); "
    "course/modules/AC/AC4/grader/reference.py (_case: isinstance(raw, list | tuple)); test_project.py "
    "test_products_that_are_not_a_list_raise_value_error", "FAIL",
    "The reference accepts a tuple of mappings: master_budget and variance_decomposition on a case whose products is "
    "tuple(CASE['products']) return results with no ValueError (witness /tmp/ac4-v/e11/witness_tuple_mapping.py). "
    "A tuple is not a list, and page line 263 says products that are not a list raise ValueError. The suite tests "
    "only a dict and a string as products, so the claim is wider than the test. No mutant covers this (m51 was "
    "considered and dropped: it equals the reference).",
    fix="Either make the reference raise for tuples (isinstance(raw, list) in reference.py) and add a test with "
        "tuple(PRODUCTS) for each function, or change page line 263 to 'products that are not a list or tuple'.")
row("proj-mutants-r11-m53-m55", "Round-11 student-error mutants m53-m55 are killed",
    "ledgers/AC4/mutants/m53_variable_cost_rounds_half_down.py; m54_any_zero_budget_product_refused.py; "
    "m55_mix_sign_flipped.py", "PASS",
    "m53 killed on seeds 0, 1, 25 (137 failed each; test_every_grader_seed_reconciles_exactly[34] first); "
    "m54 killed by test_product_with_no_budgeted_units (1 failed); m55 killed (66 failed). "
    "Writer: ledgers/AC4/scripts/AC4-e-r11/make_mutants_r11.py.")
row("proj-alt-g-student-error", "Alternative g is not an over-constraint",
    "ledgers/AC4/scripts/AC4-e-r8/alt_g.py (run in /tmp/ac4-v/e11/alts/alt_g); course/modules/AC/AC4/project.html line 263",
    "PASS", "alt_g fails 12 new refusal tests (case None; products as a mapping or as text; a product given as a list). "
    "Each is a condition page line 263 says must raise ValueError; alt_g raises TypeError or AttributeError. The tests "
    "are not over-constraining; they catch a real violation of the page.")
carry("proj-cards-targeted", "cards.json AC4-c062, c063, c064, c066, c067, c075, c076")
carry("proj-cards-number-format", "cards.json (c101, c102, c109)")
carry("proj-cards-changed-lessons", "cards.json AC4-c059..c068 and c069..c081; L05 and L06 unchanged")
carry("proj-inputs-every-number-int", "project.html lines 252 and 260")
carry("proj-stretch-two-inputs-scope", "project.html line 399")
carry("proj-conventions-no-spending-claim", "project.html line 260 and line 398")
carry("proj-lab-1-interpretation-second-clause", "project.html line 146")
carry("proj-lab-1-run-line146-untouched", "project.html lines 53-145")
carry("proj-lab-1", "project.html lines 53-147 and tests/labs/AC4/lab-AC4-project-1.py")
carry("proj-lab-2", "project.html lines 149-243 and tests/labs/AC4/lab-AC4-project-2.py")
carry("proj-lab-1-interpretation", "project.html line 146")
carry("proj-purity-order-dependence", "grader/test_project.py lines 950-994 (purity section)")
carry("proj-card-c020", "cards.json lines 134-138 (AC4-c020) and L02.html")
carry("proj-card-c078", "cards.json lines 553-557 (AC4-c078) and L06.html")
carry("proj-card-c091", "cards.json line 641 (AC4-c091) and L07.html")
carry("proj-card-c061", "cards.json line 436 (AC4-c061) and L05.html")
carry("proj-rubric-exhaustive", "project.html lines 314-318")
carry("proj-rubric-scoring-rule", "project.html line 308")
carry("proj-rubric-C4-observation", "project.html lines 306, 316, 373")
carry("proj-rubric-C2-terms", "project.html lines 308 and 315")
carry("proj-calib-A-scores", "project.html line 326 and exemplar A memo lines 330-340")
carry("proj-calib-A-annotation", "project.html lines 343-351")
carry("proj-calib-B-scores", "project.html line 357 and exemplar B line 363")
carry("proj-calib-B-annotation", "project.html lines 377-382")
carry("proj-exemplar-B-consequences", "project.html line 370")
carry("proj-exemplar-B-threshold", "project.html line 373")
carry("proj-exemplar-B-verdict", "project.html line 359")
carry("proj-reading-list-sentence", "project.html line 267 (Reading list)")
carry("proj-ladder-lede", "project.html line 42 and index.html lines 70 and following")
carry("proj-simulated-and-data", "project.html lines 53-56 and 252; tests/labs/AC4/lab-AC4-project-1.py")
carry("proj-citations-reading", "project.html reading list; references/references.json")
carry("proj-equal-margin-branch", "grader/test_project.py lines 463-480 (the test is unchanged; it still runs its equal-margin branch)")
carry("proj-grader-equal-margin-comment", "grader/test_project.py lines 472-474")
carry("proj-stretch-two-inputs", "project.html line 399")
carry("proj-stretch-spending", "project.html line 398")
carry("proj-stretch-list-intact", "project.html lines 396-401")
carry("proj-hours", "project.html lines 277-285 and index.html line 29")

notes = [
    "Delta af08ad1..91946cf (the round-10 pin to the round-11 pin) for this slice: project.html lines 263 and 265 "
    "(Constraints, Grading mode); cards.json (AC4-c102 back, AC4-c126 basis, new AC4-c129; 128 -> 129 cards); "
    "grader/test_project.py (new tests from line 485 to 691 and 897 to 947; a type-ignore comment removed at lines "
    "789 and 894); ledgers/AC4/mutants (fx10_* and m47-m50 from round 10; m52-m55 new this round, m51 dropped); "
    "scripts. Lesson pages, labs, reference.py, instance.py and starter.py are byte-identical to af08ad1.",
    "Mutants: all 64 mutants (60 committed plus m52-m55) re-run on seeds 0, 1, 25: 63 killed; m52 (dict-only case) "
    "survives and is a FAIL. Alternatives: 10 correct alternatives (alt_a-f, h-l) pass 11/11 seeds; alt_g is incorrect "
    "under the current page and the new tests kill it.",
    "Reference: passes 360/360 on each of seeds 0-49. The reference accepts a tuple of products and any Mapping, and "
    "the page line 263 says a non-list product set raises ValueError: FAIL proj-spec-products-list-tuple.",
    "Hours: unchanged in the delta; the round-10 split is carried (declared 20 vs hub 50 + 20 = 70). Per-component pace "
    "not judged (architect ruling).",
    "Not checked: a live tools/verify_refs.py run (no reference row changed; references.json byte-identical since "
    "96dd532); the full repository pytest suite (only the AC4 labs and the project checks were run); every one of the "
    "129 cards line by line (cards whose text and lesson are unchanged are carried by round-10 evidence).",
    "Round-10 FAIL proj-card-c126-basis is fixed and re-verified (PASS).",
]
summary_rows = len(rows)
frag = {
    "unit": "AC4",
    "slice": "AC4-e",
    "round": 11,
    "verifier": "Claude Haiku 5.5 (independent verifier, round 11, slice AC4-e; did not build AC4)",
    "pin": "91946cf",
    "base": "af08ad1 (round-10 pin; previous fragment /tmp/fanout-frags/AC4-e.round10.json used as context only)",
    "checkout": str(ROOT),
    "scratch": "/tmp/ac4-v/e11",
    "verified_at": "2026-10-28T18:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": {
        "rows": summary_rows,
        "pass": sum(1 for r in rows if r["status"] == "PASS"),
        "fail": sum(1 for r in rows if r["status"] == "FAIL"),
        "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
        "mutants": len(mutants),
        "mutants_killed": sum(1 for m in mutants if m.get("killed_by")),
    },
}
ids = [r["id"] for r in rows]
missing_prev = [i for i in prev_rows if i not in ids]
print("previous ids missing:", missing_prev)
out = ROOT / "ledgers/AC4/AC4-e.json"
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "mutants", len(mutants), "summary", frag["summary"])
