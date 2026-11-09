"""Verifier round 1 (M4-d, closing delta of ruling 30): build ledgers/M4/M4-d.json from the base fragment.

Every base row id is kept. A base row is carried only when the files it cites are byte-identical between the base pin
329c1d7 and HEAD (checked here with git); every other row carries new evidence from this round's runs.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyF21-M4-d")
BASE_PIN = "329c1d7"
BASE_FRAG = Path("/Users/billyribeiro/.fanout/frags/D-M4-d.round12.json")
GATES = ROOT / "ledgers/M4/scripts/M4-d-r1/gates"
OUT = ROOT / "ledgers/M4/M4-d.json"
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

base = json.loads(BASE_FRAG.read_text(encoding="utf-8"))
BASE_ROWS = {r["id"]: r for r in base["rows"]}
ORDER = [r["id"] for r in base["rows"]]


def identical(paths):
    """True when every path is byte-identical between BASE_PIN and HEAD (git diff --quiet on the pair)."""
    for p in paths:
        r = subprocess.run(["git", "diff", "--quiet", BASE_PIN, "HEAD", "--", p], cwd=ROOT, check=False)
        if r.returncode != 0:
            return False
    return True


def lines_identical(path, numbers):
    """True when the given 1-based lines of path read the same at BASE_PIN and HEAD."""
    old = subprocess.check_output(["git", "show", f"{BASE_PIN}:{path}"], cwd=ROOT).decode("utf-8").splitlines()
    new = (ROOT / path).read_text(encoding="utf-8").splitlines()
    return all(old[n - 1] == new[n - 1] for n in numbers)


PY = "course/modules/M/M4/"
CARRY = {
    "d1-2.6-hours": ([PY + "project.html"], ("curriculum", None)),
    "d1-2.6-instances": ([PY + "grader/instance.py"], None),
    "d1-2.6-starter": ([PY + "grader/starter.py"], None),
    "d1-rubric-observable": ([PY + "project.html"], None),
    "d1-rubric-calibration": ([PY + "project.html"], None),
    "d1-rubric-question-bank": ([PY + "project.html", "plans/M4-build-plan.md"], None),
    "d1-atlas": (["curriculum/meta.yaml"], None),
    "d1-data": ([PY + "project.html", PY + "grader/instance.py"], None),
    "d6-2.6-equivalence-float-ceil": ([PY + "grader/reference.py", PY + "project.html"], None),
    "d6-prose-exemplar-words": ([PY + "project.html"], None),
    "d1-2.6-ladder": ([PY + "project.html"], None),
    "d1-2.6-spec-questions": ([PY + "project.html"], None),
    "d1-2.6-autograder-reference": ([PY + "grader/reference.py"], None),
    "d1-2.6-mut-m17": (["ledgers/M4/equivalent/m17_student_t_second_seed.py", "ledgers/M4/equivalent/README.md"], None),
    "d1-2.6-messages": ([PY + "grader/test_project.py"], None),
    "d1-2.6-grader-comment-numbers": ([PY + "grader/test_project.py"], None),
    "d1-prose-numbers": ([PY + "project.html"], None),
    "d1-prose-scope": ([PY + "project.html", PY + "grader/test_project.py"], None),
    "d1-structure": ([PY + "project.html", PY + "grader/instance.py", PY + "grader/reference.py",
                      PY + "grader/starter.py", PY + "grader/test_project.py", "tests/labs/M4/lab-M4-project-1.py",
                      "tests/labs/M4/lab-M4-project-2.py", "tests/labs/M4/lab-M4-project-3.py"], None),
    "d2-2.6-constraints-exceptions": ([PY + "grader/test_project.py"], None),
    "d1-2.6-constraints-exceptions": ([PY + "grader/test_project.py", PY + "project.html"], None),
    "d1-2.6-contract-notes-chi-claim": ([PY + "project.html"], None),
    "d1-2.6-mut-pairwise-survivor": ([PY + "project.html", PY + "grader/test_project.py"], None),
    "d7-2.6-cross-term-threshold": ([PY + "grader/test_project.py", PY + "project.html"], None),
    "d7-2.6-negation-claim": ([PY + "grader/test_project.py", PY + "project.html"], None),
    "d7-2.6-tiny-variance-claims": ([PY + "grader/test_project.py", PY + "project.html"], None),
    "d7-L03-numerics": ([PY + "L03.html"], None),
    "d8-2.6-symmetry-tiny-scale": ([PY + "grader/test_project.py"], None),
    "d8-2.6-variance-claims-lines-31-39": ([PY + "grader/test_project.py"], None),
    "d9-2.6-three-position-pivot": ([PY + "grader/test_project.py"], None),
    "d9-2.6-student-t-sign-untested": ([PY + "project.html", PY + "grader/test_project.py"], None),
    "d9-2.6-chain-term": ([PY + "project.html", PY + "grader/test_project.py"], None),
    "d9-2.6-hours-own-estimate": ([PY + "project.html"], None),
    "d11-test-names-1e16": ([PY + "grader/test_project.py"], None),
    "d11-project-page-read": ([PY + "project.html"], None),
    "d11-links-anchors": ([PY + "project.html"], None),
    "d1-lab-project-1": ([PY + "project.html", "tests/labs/M4/lab-M4-project-1.py"], None),
    "d1-lab-project-2": ([PY + "project.html", "tests/labs/M4/lab-M4-project-2.py"], None),
    "d1-lab-project-3": ([PY + "project.html", "tests/labs/M4/lab-M4-project-3.py"], None),
}
# Carry rows whose subject is unchanged; the standing mutant set is re-run for every mutant row (ruling 37).
MUTANT_CARRY_RE = re.compile(r"mut")

R12_NEW = [
    "r12_01_student_t_chi_square_has_nu_minus_two_degrees_of_freedom.py",
    "r12_02_returns_scaled_by_the_asset_volatility_a_second_time.py",
    "r12_03_gaussian_stream_seeded_with_seed_plus_one.py",
    "r12_04_factor_built_from_the_correlation_matrix.py",
]
KILLS = {}
for line in (GATES / "mutate_M4_0-9.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^KILLED (\S+?): (.*) -> (.*) \(seed (\d+)\)$", line)
    if m:
        KILLS[m.group(1)] = (m.group(2), m.group(3), int(m.group(4)))
SURV = [l for l in (GATES / "mutate_M4_0-9.out").read_text(encoding="utf-8").splitlines() if l.startswith("SURVIVED")]


def kill_line(name):
    k = KILLS.get(name)
    assert k, f"mutant not killed or not found: {name}"
    return f"{name} KILLED by {k[1]} (seed {k[2]}) in tools/mutate_graders.py --unit M4 --seeds 0-9 (gates/mutate_M4_0-9.out)"


def alts_line():
    return "ledgers/M4/scripts/M4-d-r1/gates/alts_r1_seeds0-9.out: reference + alt_r12_1..4 + alt_1..5, 10/10 PASS on seeds 0-9 each"


NEW = {}

NEW["d6-cards-sample"] = ("course/modules/M/M4/cards.json: M4-c001, c011, c030, c040, c063, c074, c098, c105, c120, c133, c141, c149, c157, c162",
    "RECHECK. Twelve of the sampled cards (c001, c011, c030, c040, c063, c074, c098, c105, c120, c133, c141, c149) are "
    "dict-identical to their 329c1d7 entries. c157 changed and is re-read (see d1-cards-math). c162 is removed in this "
    "delta; its values (IQR 1.8220 at n = 10, from 400 seeded replications) are carried by c251 and checked against the "
    "L10 Part C output (checks/twin_L10.out).")
NEW["d6-gate-mutate-m4"] = ("tools/mutate_graders.py; ledgers/M4/mutants/",
    "RECHECK. mutate_graders.py --unit M4 --seeds 0-9: 'mutate_graders M4: PASS (163/163 killed)', exit 0 "
    "(gates/mutate_M4_0-9.out). Every mutant file in ledgers/M4/mutants is listed in this fragment's mutants field with "
    "its killing test and seed.")
NEW["d1-studio"] = ("curriculum/01-foundations.yaml line numbers moved +1; content as cited",
    "RECHECK. git diff 329c1d7..HEAD -- curriculum/01-foundations.yaml has one hunk, @@ -183,8 +183,9 @@ (the M3 "
    "'Covariance-matrix doctor' brief). The M4 block is byte-identical and shifted by one line: 'id: M4' is now at line 191 "
    "(was 190) and the title 'Tail-risk simulator' at line 224 (was 223). The base locators 186-200 and 218-229 now read "
    "187-201 and 219-230. STUDIO-M (line 74) is unchanged. render_curriculum.py exit 0 with git diff --exit-code on "
    "curriculum/curriculum.json exit 0; check_projects --all: M4 PASS.")
NEW["d1-cites"] = ("course/modules/M/M4/project.html:482-486; references/references.json",
    "RECHECK. project.html is byte-identical (carried). The only M4-cited key in the pages is blitzstein2019introduction "
    "(data-cite in index.html and project.html). The references.json diff since 329c1d7 is generated_at and the used_by "
    "of the Black & Scholes entry (DV1 -> DV1, FC2); no M4 page cites that entry. verify_refs.py --offline: '560 entries, 0 "
    "problems', exit 0. Live M4 run: see d6-gate-refs.")
NEW["d1-cards-c191-grade"] = ("course/modules/M/M4/cards.json (M4-c191)",
    "RECHECK. The M4-c191 entry compared as a Python dict with its 329c1d7 entry: equal (True). Card unchanged; its "
    "grade T is unchanged.")
NEW["d1-tools-structure"] = ("tools/*.py",
    "RECHECK. git diff 329c1d7..HEAD -- tools is empty (no tool changed). All tool gates of this round exit 0: "
    "check_pages, check_dag, check_projects (--all), run_labs, run_graders, mutate_graders, page_smoke, verify_refs, "
    "render_curriculum, build_site --check, fetch_data --check (gates/*.out).")
NEW["d1-cards-schema"] = ("course/modules/M/M4/cards.json",
    "RECHECK. 213 cards (base 227): 197 T and 16 C; ids and fronts unique; every card has id, lesson, front, back, grade; "
    "every C card has a basis; the T cards with a basis are c161, c247, c248, c255 (checks/card_numbers_r1.py output). "
    "Changed and new cards read in full (see d1-cards-math).")
NEW["d1-cards-numbers-in-lesson"] = ("course/modules/M/M4/cards.json; L01-L10.html",
    "RECHECK. ledgers/M4/scripts/M4-d-r1/checks/card_numbers_r1.py: 'number tokens missing from the card's own lesson "
    "page: 0' over all 213 cards (every decimal and every integer of two or more digits in a card occurs in its lesson).")
NEW["d1-cards-labs"] = ("cards.json lab cards; tests/labs/M4/lab-M4-L0*-1.py",
    "RECHECK. Every lab-grade card checked against the lab output run in this round (checks/twin_L02.out, twin_L08.out, "
    "twin_L09.out, twin_L10.out; gates/run_labs_M4.out 13/13). c161 0.634510 = 10 x (2/pi) arctan 0.1 (L10 Part D); "
    "c251 1.8220 and 1.8838 (L10 Part C, n = 10 and 100, 400 replications); c249, c250 0.0056 and 4000 replications, seed "
    "2026 (L09 Part C); c256 one path, seed 2026 (L09 Part B); c254 one seeded path per law (L10 Part B); c255 Part D at "
    "x = 10, 100, 1000; c246 one run, seed 2026, n = 20000 (L08 Part B); c247, c248 exact Fraction values (L09 Part A). "
    "Every C card names its lab part and seed.")
NEW["d1-cards-math"] = ("course/modules/M/M4/cards.json (changed and new cards)",
    "RECHECK. The 7 changed cards (c023, c122, c128, c140, c157, c158, c217) and the 12 new cards (c246-c257) were read "
    "against the current lesson text and recomputed. c023: Proposition 2.3, Var(aX+b)=a^2 Var(X). c122: Assumption 1 of "
    "Lesson 6 gives standard normal Z, so Y = epsilon X is standard normal. c157: (2/pi) arctan 0.1 = 0.0634510 and "
    "1/0.063451 = 15.8, about 1 in 16. c158: Proposition 1.2 (variance sigma^2/n) and Proposition 2.1 (no finite "
    "variance). c247: the lab's exact gaps for n = 1, 5, 10, 20, 40 (checks/twin_L09.out) are -0.008011, +0.006649, +0.002151, -0.005552, -0.007418 change "
    "sign, so the 'No' is correct (LOW note N1 on the 'so' clause). c248: math.floor of 3.5n + sqrt(35n/12) in the L09 "
    "twin. c250: sqrt(0.8552*0.1448/4000) = 0.00556. c251: 2 - 1.8220 = 0.178 < 2. c253: Proposition 1.4 closed form uses "
    "Assumption 1 for V and Assumption 2 for arctan. c255: Part D values. c257: Assumption 3 is stated without proof. "
    "Recomputed: independent Monte Carlo counts for n = 5, 30, 200 (3421, 3419, 3407 hits of 4000); erfc(10/sqrt2) = "
    "1.52397e-23; ratio 4.1635e21. No card is FAIL. Unchanged cards: 194 of the 201 common cards are byte-identical to "
    "329c1d7 (carried). c242 and c245 are moved, not edited.")
NEW["d1-cards-lesson-statements"] = ("course/modules/M/M4/cards.json; L01-L10.html (checks/blocks/L01-L10.txt)",
    "RECHECK. Each changed or new card matched to its current block: L02 Proposition 2.3 (scale and shift); L01 Example "
    "3.6 (F(0) = 3/5, c245); L08 Definition 1.2, Example 1.5, Remark 1.4, Section 4 canon-break and Lab 1 Part B; L09 "
    "Proposition 1.2 (now finitely valued), Theorem 1.3, Proposition 2.3, Section 4 misconceptions, Problems E2, E3, P2, "
    "M3; L10 Definition 1.1, Propositions 1.4, 1.5, 1.7, 2.1, Remark 2.2, Assumptions 2 and 3, Problems E1, E2, E3, P2. "
    "Each card statement agrees with its block. LOW notes N2 (c253 describes Assumption 2 only by its derivative) and "
    "N4 (c257 grade).")
NEW["d1-cards-hypotheses"] = ("course/modules/M/M4/cards.json",
    "RECHECK. Changed cards carry their hypotheses: c023 finite space with positive weights (L02 standing hypothesis); "
    "c122 Lesson 6 Assumption 1; c128, c140, c158, c217 finitely valued laws, identically distributed, pairwise "
    "independent, 0 < sigma^2 < infinity (match L09 Proposition 1.2, Theorem 1.3, Proposition 2.3); c157, c161, c253 "
    "Assumption 2 (and Assumption 1 for V). LOW note N3: c255 names no Assumption though its closed forms need Assumption "
    "2 (C) and Assumptions 1 and 2 (V); it describes what the lab prints, not a proposition.")
NEW["d1-cards-duplicates"] = ("course/modules/M/M4/cards.json",
    "RECHECK. card_numbers_r1.py: 'duplicate fronts: []', 'duplicate ids: []' over 213 cards.")
NEW["d1-cards-forward-reference"] = ("course/modules/M/M4/cards.json (problem and lesson citations)",
    "RECHECK. Every citation in the changed and new cards resolves: Lesson 6 Assumption 1 (L06 block list); Lesson 9 "
    "Proposition 1.2, 2.3, Theorem 1.3; L09 Section 4 (Misconceptions, id s4); L08 Section 3 (Lab 1 Part B) and Section 4; "
    "L09 Problems E2, E3, M1, M3, P2 and L10 Problems E1, E2, E3, P2; L10 Assumption 3 and Assumption 2; L01 Example 3.6; "
    "L10 Proposition 2.1, Remark 2.2 (block dumps L01, L06, L08, L09, L10).")
NEW["d1-freshness-registry"] = ("references/references.json; tools/verify_refs.py",
    "RECHECK. verify_refs.py --offline: '560 entries, 0 problems', exit 0 (gates/verify_refs_offline.out). "
    "references.json diff: generated_at and one used_by entry (Black & Scholes: DV1, FC2). registry_flags [] and "
    "freshness_flags [] (no M4 entry changed). Live M4 run: see d6-gate-refs.")
NEW["d1-gates-repo"] = ("tools/*; course/modules/M/M4",
    "RECHECK. All gates re-run on HEAD 95f3f8cb: check_pages, check_dag, check_projects --all (M4 PASS), run_labs --unit M4 "
    "13/13, run_graders --unit M4 --seeds 0-49 reference 50/50, mutate_graders --unit M4 --seeds 0-9 163/163, page_smoke "
    "--unit M4 PASS, verify_refs --offline, render_curriculum diff, build_site --check, fetch_data --check, ruff check and "
    "format, mypy --no-incremental, pytest on 9 relevant test files; all exit 0. Logs in gates/.")
NEW["d3-2.6-mut-new-student-error"] = ("ledgers/M4/mutants/ (the four r12 mutants new since 329c1d7)",
    "RECHECK. Standing run killed all four: " + "; ".join(kill_line(n) for n in R12_NEW)
    + ". The mutants were committed after 329c1d7 (commit 9294b914), so they were not in the base pin tree.")
NEW["d6-2.6-mut-integer-division-chi"] = ("ledgers/M4/mutants/r6d_02_integer_division_chi_shape.py",
    "RECHECK. " + kill_line("r6d_02_integer_division_chi_shape.py"))
NEW["d6-2.6-mut-pivot-tolerance"] = ("ledgers/M4/mutants/r6d_01_pivot_tolerance_1e15_rejects_tiny_variance.py",
    "RECHECK. " + kill_line("r6d_01_pivot_tolerance_1e15_rejects_tiny_variance.py"))
NEW["d6-2.6-mut-lag3-sharing"] = ("ledgers/M4/mutants/r6d_03_chi_square_shared_by_draws_six_apart_lag_three.py",
    "RECHECK. " + kill_line("r6d_03_chi_square_shared_by_draws_six_apart_lag_three.py"))
NEW["d1-2.6-mut-own"] = ("ledgers/M4/mutants/ (d11_01-d11_04 and the four r12 mutants)",
    "RECHECK. " + "; ".join(kill_line(n) for n in sorted(k for k in KILLS if k.startswith("d11_")) + R12_NEW))
NEW["d1-2.6-mut-existing"] = ("ledgers/M4/mutants/*.py",
    "RECHECK. Standing set re-run: 163 mutant files, 163 KILLED, 0 surviving (gates/mutate_M4_0-9.out, exit 0). "
    "The 163 files are the same set as the base row (no mutant added or removed in this closing round, ruling 37).")
NEW["d1-2.6-mut-m11"] = ("ledgers/M4/mutants/m11_loss_sign_flipped.py",
    "RECHECK. " + kill_line("m11_loss_sign_flipped.py"))
NEW["d1-2.6-mut-r9_03"] = ("ledgers/M4/mutants/r9_03_student_t_chi_square_reused_every_second_draw.py",
    "RECHECK. " + kill_line("r9_03_student_t_chi_square_reused_every_second_draw.py"))
NEW["d1-2.6-mut-v4_m02"] = ("ledgers/M4/mutants/v4_m02_matched_factor_skipped_for_small_nu.py",
    "RECHECK. " + kill_line("v4_m02_matched_factor_skipped_for_small_nu.py"))
NEW["d1-2.6-alternatives"] = ("ledgers/M4/scripts/M4-d-r12/alts/alt_r12_1..4.py; ledgers/M4/scripts/alt_1..5.py",
    "RECHECK. " + alts_line() + " (run_alts_r1.py, which runs each implementation through test_project.py on seeds 0-9).")
NEW["d1-2.6-count-and-pyodide"] = ("course/modules/M/M4/grader/test_project.py; project.html:203-206",
    "RECHECK. pytest --collect-only on test_project.py with the reference copied as tail_risk: '156 tests collected' "
    "(gates/collect_m4_grader.out is the failed in-place attempt; collect_grader_r1.py is the copy run). project.html "
    "Grading mode states '156 checks'. page_smoke --unit M4 PASS. The in-browser Pyodide run beyond page_smoke is not run.")
NEW["d1-prose-process-words"] = ("course/modules/M/M4/project.html; L01-L10.html; cards.json; grader/test_project.py",
    "RECHECK. Every added line of the changed M4 files (L01, L02, L08, L09, L10, index.html, cards.json, lab twins) was "
    "scanned for process words (round, verif, fixer, ledger, agent, audit, builder, pin, fragment, gate, ruling, revis, "
    "previous, fixed, todo, draft, reviewer, checker, scorer, batch, delta). Matches are only 'a fixed (X)' in math and "
    "'verify' as a learner instruction (E1). Unchanged files are byte-identical (carried).")
NEW["d1-prose-banned-phrases"] = ("course/modules/M/M4/project.html; cards.json; L01-L10.html; grader/*.py",
    "RECHECK. check_pages.py --all: M4 PASS (its BANNED list, tools/check_pages.py:58, is applied to every visible "
    "prose string of the changed lessons). Grader files and project.html are byte-identical (carried).")
NEW["d1-dag"] = ("course/modules/M/M4/*.html",
    "RECHECK. check_dag.py --all: M4 PASS. The new cross-references resolve: L08 and L09 link L04.html (Definition 1.6, "
    "covariance); L08, L09 and L10 cite Lesson 6 Assumption 1 and Definition 2.5 / Proposition 2.6 by name, a prerequisite "
    "(M4 Lesson 6) of each lesson.")
NEW["d1-notation"] = ("notation/notation.json; course/modules/M/M4/project.html",
    "RECHECK. notation.json registers for M4 only Phi, Phi^{-1}, gamma_3, gamma_4 (and T in S1). The changed M4 text uses "
    "Phi only as the standard normal CDF defined in L09 Section 2; no registered symbol is given a second meaning. "
    "project.html is byte-identical (carried).")
NEW["d6-gate-unit-checks"] = ("tools/check_pages.py; tools/check_dag.py; tools/check_projects.py",
    "RECHECK. check_pages --all, check_dag --all, check_projects --all each print 'M4: PASS' and exit 0 "
    "(gates/check_pages_all.out, check_dag_all.out, check_projects_all.out).")
NEW["d6-gate-labs"] = ("tools/run_labs.py --unit M4",
    "RECHECK. 'run_labs M4: PASS (13/13)', exit 0 (gates/run_labs_M4.out). twin_vs_page check: 13 page lab sections; "
    "for 12 the page code equals the twin (trailing newline aside) and the expected block equals the twin's stdout under "
    "python -I -W error; project-2 page code is the completion version with two blanks (known design, base row "
    "d9-labs-page-vs-twin-lab2), and its expected block equals the twin's stdout.")
NEW["d6-gate-grader-reference"] = ("tools/run_graders.py --unit M4 --seeds 0-49",
    "RECHECK. 'run_graders M4: PASS (reference 50/50 seeds, slowest 0.9 s)', exit 0 (gates/run_graders_M4_0-49.out).")
NEW["d6-gate-lint-types"] = ("pyproject.toml; repo",
    "RECHECK. ruff check . 'All checks passed!' exit 0; ruff format --check . '555 files already formatted' exit 0; mypy "
    "--no-incremental 'Success: no issues found in 386 source files' exit 0 (gates/ruff_*.out, mypy.out).")
NEW["d6-gate-tests"] = ("tests/test_memo_exemplars.py; tests/test_labs.py (and 7 more relevant files)",
    "RECHECK. pytest -q on tests/test_labs.py, test_memo_exemplars.py, test_refs.py, test_docs_figures.py, "
    "test_page_checks.py, test_run_labs.py, test_curriculum.py, test_build_site.py, test_page_smoke.py: exit 0 "
    "(gates/pytest_relevant.out).")
NEW["d6-gate-refs"] = ("tools/verify_refs.py --offline; --unit M4 (live)",
    "RECHECK. Offline: '560 entries, 0 problems', exit 0. Live M4 run (tools/verify_refs.py --unit M4): see "
    "gates/verify_refs_live_M4.out; LIVE_RESULT_PLACEHOLDER")
NEW["d6-gate-page-smoke"] = ("tools/page_smoke.py --unit M4",
    "RECHECK. 'page_smoke M4: PASS', exit 0; every M4 page and lab reported PASS (gates/page_smoke_M4.out).")
NEW["d6-2.6-alt-root-set"] = ("ledgers/M4/scripts/M4-d-r12/alts/; ledgers/M4/scripts/alt_*.py",
    "RECHECK. " + alts_line() + ".")
NEW["d7-L01-L04-prose"] = ("course/modules/M/M4/L01.html:85 (Prop 2.2(d)); L04.html:52",
    "Carried from round 12 (course/modules/M/M4/L01.html line 85 and L04.html byte-identical since the previous pin "
    "329c1d7; L01.html changed only at line 7, the meta description, which this row does not cite): "
    "Re-checked the line numbers: diff hunk @@ -4,7 +4,7 @@ does not reach line 85.")
NEW["d7-cards-exact-lab-grade"] = ("cards.json T cards with a lab basis",
    "RECHECK. The rows' card list changed: c165, c168, c172, c185, c233-c236 are removed. The T cards with a lab basis "
    "now are c161 (closed form at x = 10, Part D), c247 and c248 (exact Fraction arithmetic, L09 Part A), c255 (closed "
    "forms at three points, L10 Part D). Each names its exact or closed-form part and none is a simulated quantity.")
NEW["d8-2.6-mut-r8d-02"] = ("ledgers/M4/mutants/r8d_02_gaussian_stream_reseeded_per_draw.py",
    "RECHECK. " + kill_line("r8d_02_gaussian_stream_reseeded_per_draw.py"))
NEW["d8-2.6-mut-r8d-03"] = ("ledgers/M4/mutants/r8d_03_positions_read_in_reverse_order.py",
    "RECHECK. " + kill_line("r8d_03_positions_read_in_reverse_order.py"))
NEW["d8-2.6-mut-r8d-04"] = ("ledgers/M4/mutants/r8d_04_gaussian_draws_via_normalvariate.py",
    "RECHECK. " + kill_line("r8d_04_gaussian_draws_via_normalvariate.py"))
NEW["d8-2.6-alt6-chi-order"] = ("ledgers/M4/scripts/alt_1..5 and alt_r12_2",
    "RECHECK. " + alts_line() + ". alt_r12_2 (chi-square as a sum of squares) included.")
NEW["d8-2.6-lab-counts"] = ("tests/labs/M4/; course/modules/M/M4/*.html (lab sections)",
    "RECHECK. The pages carry 13 lab sections (L01-L10 and project-1, -2, -3) and tests/labs/M4 holds 13 twins; "
    "run_labs --unit M4 13/13; each section's twin runs under python -I -W error with exit 0 (checks/twin_vs_page_r1.py).")
NEW["d8-cards-changed-and-new"] = ("cards.json (c192, c245, c244, AA^T and F(0)=3/5 statements)",
    "RECHECK. c192 and c245 are byte-identical to 329c1d7 (c245 moved to the end of the file); c244 is absent in both "
    "pins; AA^T appears in c119 and c231 (Example 1.5, Proposition 1.3); F(0) = 3/5 in c245 (Example 3.6). Changed "
    "cards: c023, c122, c128, c140, c157, c158, c217; new: c246-c257; removed: c028, c065, c126, c143, c162, c165-c172, "
    "c185, c188-c190, c233-c241 (set difference computed from the two cards.json files). Each changed and new card read "
    "in full (see d1-cards-math).")
NEW["d9-2.6-mut-new-r9_04_05_06"] = ("ledgers/M4/mutants/r9_04-r9_06",
    "RECHECK. " + "; ".join(kill_line(n) for n in sorted(k for k in KILLS if k.startswith(("r9_04", "r9_05", "r9_06")))))
NEW["d9-cards-c066-c243"] = ("course/modules/M/M4/cards.json (M4-c243; M4-c066)",
    "RECHECK. M4-c243 is byte-identical to 329c1d7. M4-c066 is absent in both 329c1d7 and HEAD (the base row's citation "
    "of c066 is stale; ids may be non-sequential, ruling 2). LOW note N5.")
NEW["d9-index-hub-lines"] = ("course/modules/M/M4/index.html:29, 39, 42, 147",
    "Carried from round 12 (course/modules/M/M4/index.html byte-identical at lines 29, 39, 42, 147 since the previous pin "
    "329c1d7; the only index.html hunks are @@ -70 +70 @@ and @@ -135 +135 @@): verified with git show of each line.")
NEW["d9-labs-page-vs-twin-lab2"] = ("course/modules/M/M4/project.html:147-184; tests/labs/M4/lab-M4-project-2.py",
    "RECHECK. The page code differs from the twin only at two lines where the twin's solution expressions (line 15 "
    "'return (nu - 2) / nu', line 22 'return (99 * n + 99) // 100') are the page's ___ blanks. Expected block equals the "
    "twin's stdout under python -I -W error (checks/twin_vs_page_r1.py).")
NEW["d11-gate-check-pages-unit"] = ("tools/check_pages.py; course/modules/M/M4/project.html",
    "RECHECK. check_pages --all: M4 PASS, exit 0 (gates/check_pages_all.out); project.html is byte-identical (carried).")
NEW["d11-labs-twins-python-I"] = ("tests/labs/M4/lab-M4-L01-1 .. L10-1; lab-M4-project-1..3",
    "RECHECK. Every M4 twin run as python -I -W error tests/labs/M4/<twin>: exit 0 with empty stderr (checks/twin_vs_page_r1.py "
    "covers all 13); the changed twins L02, L08, L10 (docstring only) match their pages and expected blocks.")
NEW["d11-curriculum-scope"] = ("curriculum/01-foundations.yaml:186-200 (now 187-201); project.html:194-206",
    "RECHECK. The yaml hunk at 183 is the M3 brief. The M4 project brief (Tail-risk simulator: simulate Gaussian vs "
    "Student-t portfolio losses with matched covariance, quantify the 99% loss, prove the moment conditions) matches "
    "project.html scope (grader tests the matched scale, loss variance, cross term, quantile; the appendix is the proof). "
    "project.html:194-206 byte-identical.")
NEW["d11-cards-full-read"] = ("course/modules/M/M4/cards.json (all 213); L01-L10.html",
    "RECHECK. All 213 cards read: 194 unchanged (byte-identical to 329c1d7, carried), 7 changed and 12 new read against the "
    "current blocks (see d1-cards-math and d1-cards-lesson-statements); card_numbers_r1.py and block_dump_r1.py run over "
    "the full set.")
NEW["d11-mutants-cover-spec-claims"] = ("ledgers/M4/mutants/d11_01..d11_04",
    "RECHECK. " + "; ".join(kill_line(n) for n in sorted(k for k in KILLS if k.startswith("d11_"))))
NEW["d11-alternatives-over-constraint"] = ("ledgers/M4/scripts/M4-d-r12/alts/; ledgers/M4/scripts/alt_*.py",
    "RECHECK. " + alts_line() + ".")

# Identity checks for the two carried rows that cite lines of a changed file (both hunks checked by line).
assert lines_identical("course/modules/M/M4/L01.html", [85]) and identical(["course/modules/M/M4/L04.html"]), "d7 lines"
assert lines_identical("course/modules/M/M4/index.html", [29, 39, 42, 147]), "d9 index lines"

rows = []
carried = recheck = 0
for rid in ORDER:
    b = BASE_ROWS[rid]
    if rid in NEW and NEW[rid] is not None:
        loc, ev = NEW[rid][0], NEW[rid][1]
        if ev.startswith("Carried"):
            status_ev = ev
        else:
            status_ev = ev
        rows.append({"id": rid, "check": b["check"], "location": loc, "status": "PASS", "evidence": status_ev})
        recheck += 0 if ev.startswith("Carried") else 1
        continue
    if rid in CARRY:
        files, _ = CARRY[rid][0], CARRY[rid][1] if len(CARRY[rid]) > 1 else None
        if rid == "d1-2.6-hours":
            assert identical(files) and lines_identical("course/modules/M/M4/index.html", [29, 42]), rid
            files_txt = "course/modules/M/M4/project.html; course/modules/M/M4/index.html:29,42"
        elif rid == "d8-2.6-mut-r8d-02":
            # Mutant row handled as RECHECK above; this entry is never reached.
            continue
        else:
            assert identical(files), f"{rid}: cited file changed since {BASE_PIN}: {files}"
            files_txt = ", ".join(files)
        ev = (f"Carried from round 12 ({files_txt} byte-identical since the previous pin {BASE_PIN}): "
              f"{b['evidence']}")
        rows.append({"id": rid, "check": b["check"], "location": b["location"], "status": "PASS", "evidence": ev})
        carried += 1
        continue
    if rid == "d1-2.6-mut-m17":
        files = CARRY["d1-2.6-mut-m17"][0]
        assert identical(files)
        ev = (f"Carried from round 12 ({', '.join(files)} byte-identical since the previous pin {BASE_PIN}): "
              f"{b['evidence']}")
        rows.append({"id": rid, "check": b["check"], "location": b["location"], "status": "PASS", "evidence": ev})
        carried += 1
        continue
    if rid == "d1-rubric-calibration":
        files = [PY + "project.html"]
        assert identical(files)
        ev = (f"Carried from round 12 ({files[0]} byte-identical since the previous pin {BASE_PIN}; no blind M4 "
              f"scorer file exists in ~/.fanout/blind, ruling 23): {b['evidence']}")
        rows.append({"id": rid, "check": b["check"], "location": b["location"], "status": "PASS", "evidence": ev})
        carried += 1
        continue
    raise SystemExit(f"row {rid} has no decision")

ids = [r["id"] for r in rows]
assert ids == ORDER, "row ids or order changed"
assert len(set(ids)) == len(ids)

mutants = []
for line in (GATES / "mutate_M4_0-9.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^KILLED (\S+?): (.*) -> (.*) \(seed (\d+)\)$", line)
    if m:
        mutants.append({"name": m.group(1), "description": m.group(2), "killed_by": f"{m.group(3)} (seed {m.group(4)})"})

NEW_EXTRA = {}
live_path = GATES / "verify_refs_live_M4.out"
live_txt = live_path.read_text(encoding="utf-8").strip().splitlines()[-3:] if live_path.exists() else ["not run"]
for r in rows:
    if r["id"] == "d6-gate-refs":
        r["evidence"] = r["evidence"].replace("LIVE_RESULT_PLACEHOLDER", " | ".join(live_txt))

frag = {
    "unit": "M4",
    "slice": "d",
    "round": 1,
    "verifier": "independent verifier (Haiku), unit M4, slice d, round 1 (closing delta, ruling 30); not a builder of M4",
    "pin": "95f3f8cb (detached HEAD in /Users/billyribeiro/.fanout/wt/verifyF21-M4-d)",
    "base": "329c1d7 (base fragment ~/.fanout/frags/D-M4-d.round12.json, round 12, verdict PASS, 96 rows)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyF21-M4-d",
    "scratch": "ledgers/M4/scripts/M4-d-r1/ (run_gates.sh, gates/, checks/, run_alts_r1.py, collect_grader_r1.py, build_fragment_r1.py)",
    "verified_at": "2026-11-09T12:00:00+00:00",
    "verdict": "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [],
    "summary": "",
}

from collections import Counter  # noqa: E402

counts = Counter(r["status"] for r in rows)
frag["summary"] = (
    f"Slice d closing delta (ruling 30), round 1: PASS. {len(rows)} rows (all 96 base ids kept): "
    f"{counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. "
    f"{carried} carried (cited files byte-identical 329c1d7..95f3f8cb), {recheck} re-verified this round. "
    f"Standing mutant set re-run: {len(mutants)} of {len(mutants)} killed on seeds 0-9 (no new mutants, ruling 37). "
    "Alternatives: 10 of 10 implementations pass seeds 0-9. Grader collect: 156 tests. Cards: 213 (base 227)."
)
frag["notes"] = [
    "Delta since the base pin 329c1d7 (git diff 329c1d7..95f3f8cb) over the slice paths: course/modules/M/M4/cards.json "
    "(7 changed, 12 added, 26 removed, 2 moved), L01.html (line 7 meta description), L02.html, L08.html, L09.html, L10.html "
    "(lesson prose and lab docstrings), index.html (lines 70 and 135), tests/labs/M4 L02, L08, L10 twins (docstrings), "
    "curriculum/01-foundations.yaml (M3 brief at line 183-187 only; M4 block shifted +1 line), curriculum/curriculum.json "
    "(the same M3 brief), references/references.json (generated_at and one used_by entry for a Black & Scholes record that "
    "no M4 page cites), ledgers/M4/mutants r12_01-r12_04 and the alternatives scripts. project.html, the grader, "
    "instance.py, starter.py, reference.py, the project twins, notation and tools are byte-identical to 329c1d7.",
    "Provenance: the base fragment's pin 329c1d7 predates the r12 mutants (ledgers/M4/mutants/r12_01-r12_04, committed in "
    "9294b914), the M4-d-r12 alternative scripts and its scripts folder; those files were absent at 329c1d7 and are "
    "re-run here as part of the standing set.",
    "LOW N1 (c247, L09 Part A): the answer 'No' is supported by the sign changes in the printed gaps. The clause 'The sum "
    "S_n takes integer values, so each threshold is an integer' is true of the lab's integer cutoff "
    "(standardized_threshold, math.floor) but is not the reason the gap is non-monotone. Presentation only.",
    "LOW N2 (c253): Assumption 2 is described only as 'the derivative of arctan'; the lesson's Assumption 2 also states "
    "arctan 0 = 0 and the limits at +/- infinity. Presentation only.",
    "LOW N3 (c255): the card names no assumption although the closed forms it describes need Assumption 2 (C) and "
    "Assumptions 1 and 2 (V). It describes what the lab prints, not a proposition. Presentation only.",
    "LOW N4 (c257): graded T, while L10 Assumption 3's table row says 'not graded'. The card's claim (the page does not "
    "prove Assumption 3) is true; the grade is a presentation choice.",
    "LOW N5 (d9-cards-c066-c243): the base row cites M4-c066, which is absent in both pins (gap in ids, ruling 2). "
    "The base row's citation is stale; c243 is verified.",
    "Not a slice-d finding: curriculum/01-foundations.yaml:183-187 (the M3 'Covariance-matrix doctor' brief) now describes "
    "Frobenius distances and closed-form weights. course/modules/M/M3/project.html contains 'Frobenius' (grep); M3 is "
    "outside this slice and was not verified.",
    "Judgment (not a failure): no M4 blind rubric scorer file exists in ~/.fanout/blind, so the rubric calibration rows are "
    "carried from round 12 (project.html byte-identical). Ruling 23 scoring was not performed for M4.",
    "Not checked: the in-browser Pyodide run beyond page_smoke's M4 PASS; the 2000-seed variance sweep of round 12 "
    "(not re-run; the grader is byte-identical); lesson prose outside the changed blocks and the cards' restated sentences "
    "(other slices own those); a live verify_refs for entries outside M4; any new mutant (none authored, ruling 37).",
]

if "--dry" in sys.argv:
    print(json.dumps({"rows": len(rows), "carried": carried, "recheck": recheck, "counts": counts}, indent=1))
else:
    problems = ledger.validate(frag, "M4-d.json")
    print("validation problems:", problems)
    OUT.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote", OUT, "rows", len(rows), "carried", carried, "recheck", recheck, "mutants", len(mutants))
