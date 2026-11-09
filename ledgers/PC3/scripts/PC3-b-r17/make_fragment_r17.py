"""Round 17 PC3-b fragment builder. Carries round-16 rows by id (byte-identical subjects) and adds round-17 evidence."""
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
PREV = Path("/Users/billyribeiro/.fanout/frags/E-PC3-b.round16.json")
prev = json.loads(PREV.read_text(encoding="utf-8"))
O = "ledgers/PC3/scripts/PC3-b-r17/out/"
S = "ledgers/PC3/scripts/PC3-b-r17/"

BASE_NOTE = "carried from round 16 (pin 56cc575): "
L04F = "course/modules/PC/PC3/L04.html and tests/labs/PC3/lab-PC3-L04-1.py"
L05F = "course/modules/PC/PC3/L05.html (the only L05 hunk since 56cc575 is line 52)"
L06F = ("course/modules/PC/PC3/L06.html (the hunks since 56cc575 are at lines 172-173, 312, 405 and 453; "
        "every cited passage outside them is byte-identical, and line numbers after line 172 are +1 relative to round 16)")
CARDF = "course/modules/PC/PC3/cards.json (the only changed entry since 56cc575 is PC3-c178)"


def carry(rid, files):
    old = next(r for r in prev["rows"] if r["id"] == rid)
    assert old["status"] == "PASS", rid
    return {
        "id": rid, "check": old["check"], "location": old["location"], "status": "PASS",
        "evidence": f"Carried from round 16 ({files} byte-identical since the previous pin 56cc575): " + old["evidence"],
    }


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r


rows = []
# ---- gate and command rows, re-run this round
rows += [
    row("gate-run-labs-unit", "2.5-labs", "tools/run_labs.py --unit PC3", "PASS",
        f"Re-run at 700bf33f: run_labs PC3: PASS (9/9), exit 0 ({O}run_labs_unit.out)."),
    row("gate-check-pages", "2.9-prose", "tools/check_pages.py --unit PC3", "PASS",
        f"Re-run: check_pages PC3: PASS, exit 0 ({O}check_pages_unit.out)."),
    row("gate-check-dag", "2.9-DAG", "tools/check_dag.py --unit PC3", "PASS",
        f"Re-run: check_dag PC3: PASS, exit 0 ({O}check_dag_unit.out)."),
    row("gate-check-projects", "2.6-structure", "tools/check_projects.py --unit PC3", "PASS",
        f"Re-run: check_projects PC3: PASS, exit 0 ({O}check_projects_unit.out). The project rows belong to slices c and d."),
    row("gate-page-smoke-slice", "2.9-prose", "tools/page_smoke.py --unit PC3 --pages L04 L05 L06 (run alone)", "PASS",
        f"Re-run alone: page_smoke PC3: PASS for L04, L05, L06, exit 0; lab runtimes 0.0 s each, boot 1.1-1.2 s ({O}page_smoke_slice.out). "
        "Its internal console-error and external-request checks were not re-read; this row rests on the tool's PASS line."),
    row("gate-ruff-mypy-twins", "2.5-labs", "ruff check tests/labs/PC3; ruff format --check tests/labs/PC3; mypy --no-incremental", "PASS",
        f"Re-run: ruff check tests/labs/PC3 'All checks passed!' ({O}ruff_check_twins.out); ruff format --check: '9 files already formatted' ({O}ruff_format_twins.out); mypy --no-incremental: 'Success: no issues found in 385 source files' ({O}mypy.out)."),
    row("gate-pytest-lab-tooling", "2.5-labs", "pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py", "PASS",
        f"Re-run: progress line only dots and the 100% marker, no F or E, exit 0 ({O}pytest_labs_tooling.out)."),
    row("gate-verify-refs-offline", "2.1-citations", "tools/verify_refs.py --offline (whole registry); tools/verify_refs.py --unit PC3", "PASS",
        f"Re-run: 'offline integrity: 560 entries, 0 problems' ({O}verify_refs_offline.out); live 'live re-verification of PC3: 2 of 560 entries, 0 problems' ({O}verify_refs_unit_PC3.out). The L04-L06 pages carry empty data-references lists and cite no registry key."),
    row("gate-run-graders-unit", "2.6-structure", "tools/run_graders.py --unit PC3 --seeds 0-49", "PASS",
        f"Re-run: 'run_graders PC3: PASS (reference 50/50 seeds)', exit 0 ({O}run_graders_unit.out). The grader rows belong to slices c and d."),
    row("gate-fetch-data-check", "2.8-data", "tools/fetch_data.py --check", "PASS",
        f"Re-run: 'fetch_data: 3 datasets, 0 problems', exit 0 ({O}fetch_data_check.out)."),
    row("gate-build-site-check", "2.9-prose", "tools/build_site.py --check", "PASS",
        f"Re-run: 'site data current: 6 outputs', exit 0 ({O}build_site_check.out)."),
    row("gate-render-curriculum-diff", "2.9-prose", "tools/render_curriculum.py; git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json", "PASS",
        f"Re-run: 'curriculum valid: 25 parts, 134 modules, 157 projects, 13,715 h'; git diff --exit-code exit 0 ({O}render_curriculum.out, {O}render_curriculum_diff.out)."),
    row("r16-gates-ruff-format-repo", "2.5-labs", "ruff check . ; ruff format --check . (repo)", "PASS",
        f"Re-run: 'All checks passed!' ({O}ruff_check_repo.out); '553 files already formatted' ({O}ruff_format_repo.out)."),
    row("r16-gate-check-dag-all", "2.9-DAG", "tools/check_dag.py --all", "PASS",
        f"Re-run: check_dag LX1, LX2, PC3: PASS ({O}check_dag_all.out)."),
]
# ---- labs and twins, re-run this round
rows += [
    row("notation-registry-L04-L06", "2.4-notation", "course/modules/PC/PC3/L04.html, L05.html, L06.html math vs notation/notation.json", "PASS",
        f"Re-run scripted scan ledgers/PC3/scripts/PC3-b-r15/notation_scan.py at 700bf33f: 'registered symbol mentions: []' for L04, L05 and L06 ({O}notation_scan.out). The round-17 L06 hunks add no symbol to any math span; the new 'S_T' appears only in the lab's printed text (L06 twin lines 64-69, page lines 223-228; expected block lines 288-290), which is not page math."),
    row("twin-run-alone-L04-L06", "2.5-labs", "tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py", "PASS",
        f"Re-run alone: python -I -W error <twin> from cwd /tmp: exit 0, stderr 0 bytes for all three ({O}twin_check.out; script ledgers/PC3/scripts/PC3-b-r17/twin_check.py)."),
    row("twin-page-code-equals-twin", "2.5-labs", "L04.html, L05.html, L06.html data-run vs the three twins", "PASS",
        f"Re-run: page code equals twin after html.unescape and rstrip('\\n') for all three ({O}twin_check.out); independent comparison ledgers/PC3/scripts/PC3-b-r15/twin_page_compare.py: ALL_EQUAL ({O}twin_page_compare.out). L06 now equal after the round-17 docstring hunk (twin lines 13-14 = page)."),
    row("twin-expected-equals-stdout", "2.5-labs", "L04.html pre.expected vs stdout of lab-PC3-L04-1; L05.html vs lab-PC3-L05-1; L06.html vs lab-PC3-L06-1", "PASS",
        f"Re-run: expected equals stdout line for line after rstrip: 52 = 52 (L04), 25 = 25 (L05), 21 = 21 (L06) ({O}twin_check.out)."),
    row("lab-L05-1-hypothesis-interpretation", "2.5-labs", "L05.html line 163 (hypothesis), 332 (interpretation), code 164-306", "PASS",
        f"Re-verified round 17 by an independent deque implementation (ledgers/PC3/scripts/PC3-b-r17/verify_numbers_r17.py, output {O}verify_numbers_r17.out): seed 5 naive comparisons 1351 = (200-8+1)(8-1), deque while-tests 354 <= 400, pops 173+26 = 199; seed 6 deque tests 350, pops 178+19 = 197. The expected block lines 312-317 of L05.html equal the run output. The hypothesis and interpretation passages are byte-identical to round 16."),
    row("lab-L06-1-hypothesis-interpretation", "2.5-labs", "L06.html line 159 (hypothesis), 306 (interpretation), code 160-283", "PASS",
        f"Re-verified round 17 at 700bf33f: the twin code changed only in its docstring (lines 13-14); the printed values (lower NPV -12513148 cents, exact -16655000000/1331; upper 4894816; rates 8/10/12 lower -12422903/-12513148/-12598169, upper 5616776/4894816/4214650; break-evens 1164.10/1206.34/1249.05) equal the independent recomputation in {O}verify_numbers_r17.out. Hypothesis line 159 and interpretation line 306 match the output."),
    row("r16-L06-interpretation-hunk-305", "2.5-labs", "L06.html interpretation (now line 306) vs expected block 'NPV at the lower bound = -12513148 cents (exact -16655000000/1331)'", "PASS",
        f"Re-verified round 17: the expected block line 299 equals the run output; -16655000000/1331 = -12513148.009 rounds (floor(x+1/2)) to -12513148 (exact check in {O}verify_numbers_r17.out)."),
    row("r16-L06-misconception-2-hunk-322", "2.3-grades", "L06.html misconception 2 (now line 323): 'the break-even rises by 21.24 units per point of rate'", "PASS",
        f"Re-verified round 17: (1249.0469-1164.1005)/4 = 21.2366, displays as 21.24 ({O}verify_numbers_r17.out 'width 12-8'); Problem E3 gives the same derivation. The sentence is unchanged since round 16."),
    row("L06-E2-first-negative", "2.5-labs", "L06.html line 405 (E2 solution), against tests/labs/PC3/lab-PC3-L06-1.py lines 100-117 and the expected block lines 292-304", "PASS",
        f"Round-16 FAIL is fixed at 700bf33f. The sentence now reads 'Lab 1, Part 2 checks that the NPV increases on the grid and prints NPVs only at the two bounds, 200 and 1600 units, which are grid points'. Checked against the twin: NPV-valued prints are only the lower and upper bounds (lines 105-107 and the rate loop 110-117); line 100 prints a boolean for the break-even and line 103-104 a boolean for the increase. Hand values: NPV(1200) = -105000000/1331 = -78888.054 and NPV(1300) = 1550000000/1331 = 1164537.941 ({O}verify_numbers_r17.out). Grid positives 1300, 1400, 1500, 1600 (count 4); largest negative 1200 ({O}verify_numbers_r17.out)."),
    row("r17-L06-part1-prose-five-spot-values", "2.4-mathematics", "L06.html lines 172-173 (Part 1 prose) and twin lines 13-14", "PASS",
        f"'The lab checks this at five spot values': twin line 63 loops over 8000, 9000, 10000, 11000, 12000, and the run prints the check for each (expected lines 288-290). 'Proposition 2.1 covers every spot state': Prop 2.1(i) proof, L06.html line 97: 'This does not depend on S_tau'; the portfolio payoff F'-S/D is re-derived exactly for F' in {{10000, 10100}} at the five spots ({O}verify_numbers_r17.out line 2)."),
    row("r17-L06-canon-case-answer-sentence", "2.9-prose", "L06.html line 312 ('The case answer depends on its assumptions.')", "PASS",
        "The following sentences list the omitted items and the fixed inputs: margin 5000 cents and the rate fixed over three years match Example 4.2 (line 149: 'the contribution is the same in each year'; 'the rate is 10 percent'); 'no tax' and 'no salvage value' match Example 4.2 (line 149). The clause 'the lesson measures none of them' is a claim about this lesson's own content (no tax, depreciation or salvage is computed on the page). Banned phrases: none (scan in " + O + "prose_scan.out: banned=0 for L06)."),
    row("r17-L06-key-results-prop-3.2", "2.3-grades", "L06.html line 453 (key results row for Prop 3.2)", "PASS",
        "'A product of positive factor ranges lies between the products of their lower and upper ends' matches Prop 3.2 hypotheses (H1: 0 < l_j <= h_j, line 122) and conclusion (both ends attained); grade T with the induction proof on the page (lines 124-127). Card PC3-c111 states the same hypotheses."),
    row("r17-card-PC3-c178", "2.7-cards", "cards.json PC3-c178 (cards.json lines 1467-1468), L06", "PASS",
        f"Answer 'No' is right: [200, 1600] contains the break-even 399300/331 = 1206.344 (Prop 3.1 with A = 3310/1331). NPV(200) = -12513148.01 and NPV(1600) = 4894815.93 at 10 percent ({O}verify_numbers_r17.out), so negative at 200 and positive at 1600. Numbers 200, 1600, 1206.34 appear in L06.html (Example 4.2 line 149; misconception 3 line 329). Grade T: the sign follows from Prop 3.1 on the page; Lab 1 Part 2 is exact arithmetic, not SIMULATED, so citing it is a demonstration. Basis cites Example 4.2 and Corollary 3.3, both on the page."),
    row("r17-delta-scope", "2.9-prose", "git diff --name-only 56cc575 700bf33f (PC3 slice files)", "PASS",
        "Changed in this slice since 56cc575: L05.html line 52; L06.html lines 172-173, 312, 405, 453; cards.json PC3-c178 (lines 1467-1468); tests/labs/PC3/lab-PC3-L06-1.py lines 13-14 (docstring). Not changed: L04.html, lab-PC3-L04-1.py, lab-PC3-L05-1.py. Other changes in the commit (project grader and project.html, references/references.json, other units) are outside this slice. The references.json diff adds FC2 to black1973pricing used_by; no L04-L06 page cites that key."),
]
# ---- the one new FAIL
rows += [
    row("r17-L05-meta-description-comparisons", "2.9-prose", "course/modules/PC/PC3/L05.html line 7 (meta name=\"description\")", "FAIL",
        "The description says the deque's 'comparisons number at most twice the number of inputs', with no qualifier. Proposition 3.3 (L05.html line 137) counts the while-loop tests, which compare stored values, and the body (line 52, changed this round) now says 'comparisons of stored values'. The literal reading also counts the front-expiry test 'window[0] <= i-k' (lab twin line 78), which Prop 3.3 excludes (L05.html line 142: 'not counted in Proposition 3.3'). Under that literal reading the claim is false: xs = [5,4,3,2,1,6,7,8,9,10], k = 3 gives 11 while-tests plus 10 expiry tests = 21 > 2n = 20 (ledgers/PC3/scripts/PC3-b-r17/out/meta_expiry_count.out; max (tests+n)/2n = 1.462 over 20000 random cases). The while-test reading holds (max tests/2n <= 1).",
        "Change line 7 to: 'a monotonic deque whose correctness is proved and whose comparisons of stored values number at most twice the number of inputs.' Keep the wording identical to line 52 and Proposition 3.3."),
]
# ---- carried rows: L04 (unchanged file)
L04_IDS = [
    "L04-definitions-A1-A6-notation", "L04-lab-section-locator", "L04-prop-2.2-2.3-identity", "L04-example-3.2-values",
    "L04-proposition-4.1-remark-4.2-sd", "L04-remark-4.2-inventory-independence", "L04-remark-3.4-inventory-zero",
    "L04-canon-breaks-tick", "L04-canon-breaks-quote-rule", "L04-R2-spread-criterion", "L04-E1-seed1-numbers",
    "L04-E2-binomial-z", "L04-E3-mid-vs-settlement", "L04-problems-R1-R3-M-P", "L04-M3-inventory-hypothesis",
    "L04-quiz-q11-citation", "L04-quiz-answers", "L04-key-results-prop-3.1-assumptions", "L04-prop-3.1-closed-form",
    "L04-corollary-3.3", "L04-misconceptions", "L04-key-results-table-other", "L04-scope-and-banned-phrases",
    "L04-structure-hours", "L04-DAG-D-terms", "L04-A1-project-consistency", "L04-footer-registry-claim",
    "L04-lab-docstring-money-integer", "lab-L04-1-hypothesis-interpretation", "r16-L04-remark-3.4-hunk-158",
    "r16-L04-misconception-1-hunk-492", "r16-L04-canon-mid-induction", "r16-sim-independent",
]
for rid in L04_IDS:
    rows.append(carry(rid, L04F))
# ---- carried rows: L05 (only line 52 changed)
L05_IDS = [
    "L05-def-3.1-markup", "L05-prop-2.1-2.2-remark", "L05-prop-3.2-correctness", "L05-prop-3.3-bound",
    "L05-remark-3.4-k-range", "L05-example-3.5-trace", "L05-problems-M-P", "L05-E1-E3-numbers", "L05-E2-seed6-numbers",
    "L05-R1-scope-sentence", "L05-R2-R3", "L05-key-results-grades", "L05-quiz-answers",
    "L05-misconceptions-canon-breaks", "L05-structure-hours", "L05-meta-uses-hash-map-heap", "L05-meta-uses-other",
    "L05-footer-registry-claim", "L05-DAG-links", "L05-card-PC3-c092", "L05-card-PC3-c096-grade", "L05-card-PC3-c097-grade",
    "r16-L05-why-it-matters-forward-refs",
]
for rid in L05_IDS:
    if rid == "r16-L05-why-it-matters-forward-refs":
        continue
    rows.append(carry(rid, L05F))
rows.append(row("L05-why-it-matters-comparisons", "2.4-mathematics",
    "L05.html line 52 (why it matters) plus Definition 1.3 (line 77), Definition 3.1 (line 105), Proposition 3.3 (line 137)", "PASS",
    "Re-verified round 17. The new phrase 'comparisons of stored values' matches the lesson's count: Prop 3.3 counts the while-loop tests (L05.html line 137 and its proof, lines 141-142), and the lab's counter increments once per while test (tests/labs/PC3/lab-PC3-L05-1.py line 71) and not for the expiry test (line 78). Checked by brute force over 3000 random cases with ties: the while-test count never exceeds 2n, max ratio 0.966 ({O}verify_numbers_r17.out; {S}meta_expiry_count.py). Definitions 1.3 (line 77) and 3.1 (line 105) exist. 'Exactly' (naive count) and 'the same answers' (Prop 2.1; Prop 3.2 Step B) are backed by proofs."))
rows.append(row("r16-L05-why-it-matters-forward-refs", "2.9-prose", "L05.html line 52 and Definition 1.3 (line 77), Definition 3.1 (line 105)", "PASS",
    "Re-verified round 17: both 'of this lesson' references resolve (L05.html lines 77 and 105, the block-title Definition 1.3 and Definition 3.1); line 52 is the only changed L05 line."))
rows.append(row("L05-markup-raw-less-than", "2.9-prose", "L05.html prose outside pre and script (line 52 included)", "PASS",
    f"Re-verified round 17: line 52 contains no raw '<' or '&' apart from its own closing </p> ({O}twin_page_compare.out is unaffected); the L05 page run through page_smoke (gate-page-smoke-slice) passes."))
# ---- carried rows: L06 (line-shifted, cited passages byte-identical)
L06_CARRY = [
    "L06-prop-1.1-payoff-identity", "L06-remark-1.2-put-call-parity", "L06-definition-1.3-NPV-and-prop-3.1",
    "L06-prop-2.1-forward", "L06-remark-2.2-continuous-convention", "L06-corollary-3.3-grade", "L06-prop-3.2-fermi-bounds",
    "L06-M1-M3-numbers", "L06-P1-P3-proofs", "L06-R1-R3", "L06-quiz-answers", "L06-articulation-claim-linked", "L06-footer-registry-claim",
    "L06-structure-hours", "L06-DAG-and-cross-links", "L06-why-it-matters-scope", "L06-card-PC3-c148-grade",
    "L06-card-PC3-c151", "r16-L06-why-it-matters-def-4.1", "r16-card-c124", "r16-cards-c188-c190", "r16-card-c186",
    "card-PC3-c187-articulation", "card-PC3-c081-basis-H2", "card-PC3-c112-corollary-boundary",
]
for rid in L06_CARRY:
    files = CARDF if ("card" in rid and "card-full" not in rid) and rid not in ("L06-card-PC3-c148-grade",) else L06F
    if rid in ("r16-card-c124", "r16-cards-c188-c190", "r16-card-c186", "card-PC3-c187-articulation", "card-PC3-c081-basis-H2",
               "card-PC3-c112-corollary-boundary", "L06-card-PC3-c148-grade", "L06-card-PC3-c151"):
        files = CARDF
    rows.append(carry(rid, files))
# re-verified L06 rows with changed subject or re-derived numbers
rows.append(row("L06-canon-breaks-and-misconceptions", "2.9-prose", "L06.html lines 312-313 (canon breaks), 318-333 (misconceptions; now +1)", "PASS",
    "Re-verified round 17. Canon line 312 changed to 'depends on its assumptions' (checked above); the factor-of-8 sentence (line 313) equals 1600/200 = 8 and three factors each doubled (Example 4.2 ranges). Misconception 2 numbers: " + O + "verify_numbers_r17.out. Misconception 3 matches Example 4.2 and Corollary 3.3. Misconception 4: the sign at the bounds is negative at 200 and positive at 1600 at all three rates (verify_numbers_r17.out)."))
rows.append(row("L06-E1-12pct", "2.2-numbers", "L06.html lines 394-399 (E1)", "PASS",
    f"Re-verified round 17: A(12%) = 1/1.12 + 1/1.2544 + 1/1.404928 = 52725/21952 = 2.4018313; 3000/A = 1249.0469 = 1249.05 ({O}verify_numbers_r17.out)."))
rows.append(row("L06-E3-42.71", "2.2-numbers", "L06.html lines 408-414 (E3)", "PASS",
    f"Re-verified round 17: width 1249.0469-1164.1005 = 84.9464 -> 84.95; /4 = 21.2366 -> 21.24; 8->10: 42.2439 -> 42.24; 10->12: 42.7025 -> 42.70; printed-value difference 1249.05-1206.34 = 42.71 ({O}verify_numbers_r17.out). The solution's statement that 42.71 is not the answer is correct."))
rows.append(row("L06-E3-rest-and-quiz-q9", "2.2-numbers", "L06.html E3 (line 411 region) and quiz item 9", "PASS",
    f"Re-verified round 17: break-even units at 8, 10 and 12 percent (1164.10, 1206.34, 1249.05) and the per-point rate (21.24) recomputed ({O}verify_numbers_r17.out). Quiz item 9 answer 1249.05 matches Remark 4.3."))
rows.append(row("L06-remark-4.3-sensitivity", "2.2-numbers", "L06.html Remark 4.3", "PASS",
    f"Re-verified round 17: A(8) = 50725/19683 = 2.5770970, A(10) = 3310/1331 = 2.4868520, A(12) = 52725/21952 = 2.4018313; unrounded break-evens 1164.1005, 1206.3444, 1249.0469 (4 dp); differences 42.24 (8 to 10) and 42.70 (10 to 12); NPV at 200 negative and at 1600 positive at all three rates ({O}verify_numbers_r17.out)."))
rows.append(row("L06-example-4.2-numbers", "2.4-mathematics", "L06.html Example 4.2 (lines 148-149)", "PASS",
    f"Re-verified round 17: Fermi bounds [200, 1600] (2000*1*1/10 and 4000*2*1/5, ratio 8); A = 3310/1331; break-even 399300/331 = 1206.344; straddle, so Corollary 3.3 applies ({O}verify_numbers_r17.out)."))
rows.append(row("L06-lab-docstring-money-integer", "2.5-labs", "tests/labs/PC3/lab-PC3-L06-1.py docstring 1-19 (changed lines 13-14), code 21-125", "PASS",
    "Re-verified round 17: the docstring's stated facts hold: standard library only (imports itertools, math, collections.abc, fractions); no randomness and no network; integer cents constants (SPOT_CENTS, QUOTED_CENTS, OUTLAY_CENTS, MARGIN_CENTS); every value a fractions.Fraction; half_up is used only in display (lines 38-47, 98, 106-117). The Part 1 sentence matches lines 63 and 70-71 (five spot values; payoffs exact)."))
rows.append(row("card-full-scan-L06", "2.7-cards", "cards.json: all 40 L06 cards (PC3-c102..c127 except c118, c147..c151, c165..c167, c178..c179, c183..c184, c187, c189..c190)", "PASS",
    f"Re-read round 17: all 40 L06 entries printed and read (fronts, backs, grades, basis). Each card's numbers appear in its lesson or lab output; the answers match the lesson (e.g. c126 33275/331 = 100.5287; c125 500/121 = 4.1322; c127 margin ratio 0.753965, fall 24.6 percent; c121 and c123 break-evens 1164.10, 1206.34, 1249.05). c178 re-verified (row r17-card-PC3-c178). Scripted: ledgers/PC3/scripts/PC3-b-r15/cards_check.py -> {O}cards_check.out: 'card numbers not found verbatim in own lesson page: count 0'."))
# ---- L04, L05 card full-scan rows are carried; cards.json other entries unchanged
rows.append(carry("card-full-scan-L04", CARDF))
rows.append(carry("card-full-scan-L05", CARDF))
rows.append(row("card-duplicate-scan", "2.7-cards", "cards.json: 109 L04-L06 cards; 185 PC3 cards", "PASS",
    f"Re-run: ledgers/PC3/scripts/PC3-b-r15/cards_check.py at 700bf33f: 'unique ids: True count: 185'; near-duplicate fronts (difflib >= 0.85) are PC3-c096/c142, c097/c145, c110/c183, c110/c184, c116/c148, c117/c150, c138/c140, c181/c182. Each pair asks a different value or property (e.g. c116 asks the break-even at 8 percent and c148 at 12 percent; c110 asks NPV(u), c183 asks monotonicity), so none is a duplicate ({O}cards_check.out)."))
rows.append(row("card-key-results-agreement", "2.7-cards", "cards.json L04-L06 cards vs key-results tables L04.html 620-625, L05.html 472-477, L06.html 448-454", "PASS",
    "Re-verified round 17: the changed key-results row (L06.html line 453, Prop 3.2) agrees with card PC3-c111 (hypotheses 0 < l_j <= h_j; both ends attained) and with the remaining L06 cards. Other key-results rows are unchanged."))
rows.append(row("card-number-in-lesson", "2.7-cards", "cards.json numbers vs own lesson text and lab output (L04-L06)", "PASS",
    f"Re-run: cards_check.py -> 'card numbers not found verbatim in own lesson page: count 0' ({O}cards_check.out)."))
rows.append(row("card-cite-empty", "2.7-cards", "cards.json L04-L06 'cite' fields", "PASS",
    "Re-run (python): no L04, L05 or L06 card has a non-empty 'cite' list; the c178 cite is []."))
rows.append(row("card-PC3-c112-corollary-boundary", "2.7-cards", "cards.json PC3-c112 (unchanged)", "PASS",
    "Carried from round 16 (cards.json entry PC3-c112 byte-identical since 56cc575): " + next(r for r in prev["rows"] if r["id"] == "card-PC3-c112-corollary-boundary")["evidence"]))
# ---- historic delta rows, carried: their ranges are unchanged
for rid in ["delta-r14-hunks-L04-L06-cards", "delta-r14-twins-unchanged", "delta-r15-L05-unchanged"]:
    rows.append(carry(rid, "the historic range named in the row (no change in it since)"))
rows.append(carry("r16-delta-scope", "the round-16 range d1e65a0..56cc575"))
rows.append(carry("r16-prose-scan", "L04.html, L05.html and L06.html visible prose outside the round-17 hunks; the scripted prose scan was re-run this round (" + O + "prose_scan.out) and agrees"))
rows.append(row("r16-numbers-rederivation", "2.2-numbers", "all numbers in L04-L06 prose, quiz, key results and problems", "PASS",
    f"Re-run this round: ledgers/PC3/scripts/PC3-b-r17/verify_numbers_r17.py -> {O}verify_numbers_r17.out (all L06 hunk numbers, Remark 4.3, E1-E3, M2, M3, R3, c124-c127, L05 counts 1351/354/350/400, Remark 3.4 k). L04 numbers are carried (file unchanged)."))
rows.append(row("r16-twin-page-and-run", "2.5-labs", "tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py; the three pages", "PASS",
    f"Re-run this round: twin_check.out (ALL OK), twin_page_compare.out (ALL_EQUAL)."))
rows.append(row("r16-card-c124", "2.7-cards", "cards.json PC3-c124 (L06): NPV at 1200 units and 8 percent is positive", "PASS",
    f"Re-verified round 17: at 8 percent the break-even is 1164.1005 < 1200, and NPV is increasing (Prop 3.1), so the NPV is positive ({O}verify_numbers_r17.out 'NPV r=8' gives the bounds; 1200 is between the break-even and the upper bound)."))

# ---- sanity: every round-16 row id present
ids_prev = [r["id"] for r in prev["rows"]]
ids_now = {r["id"] for r in rows}
missing = [i for i in ids_prev if i not in ids_now]
extra = [i for i in ids_now if i not in ids_prev]
print("missing from round 17:", missing)
print("new in round 17:", extra)
# the L04-prose carried row 'L04-lab-docstring-money-integer' etc. are kept; L05 'r16' carried rows handled above
# remove duplicates by id, keep first
seen = set()
final = []
for r in rows:
    if r["id"] in seen:
        continue
    seen.add(r["id"])
    final.append(r)
rows = final

n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_fail = sum(1 for r in rows if r["status"] == "FAIL")
n_unv = sum(1 for r in rows if r["status"] == "UNVERIFIABLE")
verdict = "PASS" if n_fail == 0 and n_unv == 0 and all(r["status"] == "PASS" for r in rows) else "FAIL"

frag = {
    "unit": "PC3",
    "slice": "PC3-b",
    "round": 17,
    "verifier": "Claude Haiku 5.5, independent verifier for PC3-b round 17 (did not build PC3)",
    "pin": "700bf33f334486d7b5b4f22d4f82f3e25d4b39b6",
    "base": "56cc575a774a66e9580d3182969eb7d6aa413731 (round-16 pin). Delta 56cc575..700bf33f in this slice: L05.html line 52; L06.html lines 172-173, 312, 405, 453; cards.json PC3-c178; tests/labs/PC3/lab-PC3-L06-1.py lines 13-14. L04.html, lab-PC3-L04-1.py and lab-PC3-L05-1.py unchanged.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE17-PC3-b (detached at 700bf33f; .venv symlinked)",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyE17-PC3-b/ledgers/PC3/scripts/PC3-b-r17/out",
    "verified_at": "2026-11-09T04:10:00+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Scope: slice b = L04, L05, L06 lesson pages, their lab twins tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py, and the L04-L06 cards of course/modules/PC/PC3/cards.json. Project files, graders, hub and slice a/c/d items are not judged here.",
        "Round-17 method: delta computed from 56cc575 with git diff; every hunk in the slice read; every round-16 non-PASS row re-verified (L06-E2-first-negative is now PASS); every round-16 PASS row whose cited passage is byte-identical is carried by id with the prefix 'Carried from round 16'; rows whose subject changed were re-verified with new evidence. All command rows were re-run at 700bf33f with outputs in ledgers/PC3/scripts/PC3-b-r17/out/.",
        "Line numbers: L06.html line numbers after line 172 are +1 relative to the round-16 fragment (the Part 1 prose hunk added one line). Carried rows keep their round-16 location text; the carry note states this.",
        "The one FAIL: the page description (L05.html line 7) is the only place the deque bound is stated without the 'of stored values' qualifier that the body now uses. The fix is one attribute value. Lines L05.html 339 ('at most two comparisons') and 348 ('at most 2n comparisons by Proposition 3.3') use the same word but are attributed to Proposition 3.3, whose statement names the while-loop tests; they are judged PASS with this note, not failed.",
        "Judgement (not a row): the Remark 4.3 and E3 'per point' figures are exact to the displayed digits; no rounding conflict found (verify_numbers_r17.out).",
        "Judgement (not a row): the L06 lab's exact-fraction NPV prints are deterministic, not SIMULATED; cards that cite them with grade C or T (c117, c119, c121, c123, c149, c150) name the lab as the basis, as the earlier rounds accepted.",
        "Judgement (not a row): the lab prints the tautology 'initial outlay ... -S ... plus S ... = 0 cents' (twin line 72); the lesson proves zero cost in Prop 2.1(i), so no row fails.",
        "Mutation testing: not applicable to this slice (lab twins, cards, prose). mutants is empty.",
        "Registry: references/references.json changed in the delta (generated_at; black1973pricing used_by gained FC2). No L04-L06 page or card cites that key (pages' data-references lists are empty). No registry flag.",
        "Could not check: the Pyodide browser runtime beyond page_smoke's PASS line (its console-error and external-request internals were not re-read); the 360 px layout of the three pages (page_smoke is the only evidence); CS1-level prerequisite pages (DAG was checked by check_dag, not by reading the prerequisite pages); the full pytest suite (only the three lab-tooling modules, as in round 16); the live verify_refs for the whole registry (only the offline whole-registry run and the live PC3 run).",
    ],
    "summary": (
        f"Slice b (L04-L06, twins, L04-L06 cards), round 17 at 700bf33f. {len(rows)} rows: {n_pass} PASS, {n_fail} FAIL, {n_unv} UNVERIFIABLE. "
        "The round-16 FAIL (L06-E2-first-negative) is fixed and verified. One new FAIL: L05.html line 7 meta description says the deque's comparisons are at most twice n without the 'of stored values' qualifier the body now uses; the literal reading gives 21 > 20 on a 10-value example. All gates and twins PASS."
    ),
}
out = ROOT / "ledgers/PC3/PC3-b.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "pass", n_pass, "fail", n_fail, "verdict", verdict)
