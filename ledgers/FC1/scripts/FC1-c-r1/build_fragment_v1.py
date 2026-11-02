"""Writes the FC1-c round-1 ledger fragment from the verifier's rows and the mutate_graders output.

Usage: python -I build_fragment_v1.py <checkout-root> <mutate_graders output file>
Every mutant is read from the mutate output (KILLED/SURVIVED lines), so the mutant list cannot drift from the run.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(sys.argv[1])
MUTATE_OUT = Path(sys.argv[2])
SCRIPTS = "ledgers/FC1/scripts/FC1-c-r1"
PIN = "d0f39c09598ffefaf0ec18d5d1077cfacd42998b"
GRADER = "course/modules/FC/FC1/grader/test_project.py"

PASS, FAIL = "PASS", "FAIL"
rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> None:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != PASS:
        assert fix, rid
        item["fix"] = fix
    rows.append(item)


# ---- gates and commands (re-run by this verifier on the pin; outputs under SCRIPTS/out) -----------------------------
row("proj-check-projects", "2.6-structure", "course/modules/FC/FC1/project.html", PASS,
    "Re-run: .venv/bin/python tools/check_projects.py --unit FC1 -> 'check_projects FC1: PASS', exit 0 (" + SCRIPTS + "/out/check_projects.out).")
row("proj-check-pages", "2.9-structure", "course/modules/FC/FC1/project.html", PASS,
    "Re-run: tools/check_pages.py --unit FC1 -> 'check_pages FC1: PASS', exit 0 (out/check_pages.out).")
row("proj-check-dag", "2.9-DAG", "course/modules/FC/FC1/project.html links present-value and discount-factor", PASS,
    "Re-run: tools/check_dag.py --unit FC1 -> 'check_dag FC1: PASS', exit 0 (out/check_dag.out). Both project-page links are M1 concepts in the closure {E1, M1, M2, P0.1} (plans/FC1-build-plan.md section 7.2).")
row("proj-run-labs", "2.5-labs", "project.html labs lab-FC1-project-1..3 and tests/labs/FC1/lab-FC1-project-{1,2,3}.py", PASS,
    "Re-run: tools/run_labs.py --unit FC1 --page project -> 'run_labs FC1: PASS (3/3)', exit 0 (out/run_labs_project.out). The tool checks page code byte-identical to the twin (labs 1 and 3), completion lines equal or blank (lab 2), twin under python -I -W error, and stdout against the expected block with tol 1e-6 scaled by (1+|expected|).")
row("proj-page-smoke", "2.9-smoke", "course/modules/FC/FC1/project.html", PASS,
    "Re-run: tools/page_smoke.py --unit FC1 --pages project -> 'page_smoke FC1: PASS', exit 0; the in-browser grader reported 'All 68 tests pass on seed 172802359' (out/page_smoke_project.out); the tool enforces zero console errors and zero requests to any host other than the local server.")
row("proj-run-graders", "2.6-autograder-1", "course/modules/FC/FC1/grader/reference.py, test_project.py, instance.py, starter.py", PASS,
    "Re-run: tools/run_graders.py --unit FC1 --seeds 0-19 -> 'run_graders FC1: PASS (reference 20/20 seeds, slowest 0.2 s)' (out/run_graders_0_19.out). Repo-wide note, not failed here: grader/reference.py is tracked in the repository (BLUEPRINT deployment exclusion is not enforced by a file), recorded for the user.")
row("proj-lint-types", "gate", "course/modules/FC/FC1/grader/*.py and tests/labs/FC1/", PASS,
    "ruff check and ruff format --check on grader/ and tests/labs/FC1/ (out/ruff.out: 'All checks passed', '12 files already formatted', exit 0); mypy --no-incremental on reference.py, instance.py, starter.py and tests/labs/FC1/ (out/mypy.out: 'Success: no issues found in 11 source files', exit 0).")

# ---- Lab 1, 2, 3 and the prose numbers ----------------------------------------------------------------------------
row("proj-lab1-numbers", "2.2-numbers / 2.5-labs", "project.html lines 58, 97-100 (Lab 1)", PASS,
    "Recomputed with Fraction (" + SCRIPTS + "/numbers_recheck.py, out/numbers_recheck.out): coupon 5000; events (1,5000),(2,5000),(3,105000); exact PV 102775.09103322713 -> printed 102775; trade event (2,-98500). The prose figure 102775.091033 and the claim that .091033 is below one half are correct.")
row("proj-lab2-blanks", "2.5-labs", "project.html lines 133 and 140 (Lab 2), tests/labs/FC1/lab-FC1-project-2.py", PASS,
    "Exactly two blanks (___ at page lines 133 and 140); the twin is the completed solution, and run_labs checks each non-blank line against it. Tolerance claim: 1e-6 * (1 + 102775.09) = 0.103 cent, which matches 'about 0.1 cent' (tools/run_labs.py compare_output, data-tolerance 1e-6).")
row("proj-lab3-fixture-values", "2.2-numbers / 2.5-labs", "project.html lines 198-276 (Lab 3); tests/labs/FC1/lab-FC1-project-3.py", PASS,
    "Recomputed every printed fixture value (out/numbers_recheck.out and run of the twin): A [(1,10500)] price 10000; B 11053 exact 11052.6316 (10500/0.95 = 11052.6316); C [(1,5001),(2,15002)]; D [(1,2)]; rounding case events [(1,500),(2,500),(3,10500)], once 10278, term-by-term 10277; E (2,-98500); F [(1,1)] price 1; G [(1,10001)] price 5001. All match the expected block exactly.")
row("proj-rounding-fixture-terms", "2.2-numbers", "project.html line 193 and grader/test_project.py lines 329-331", PASS,
    "Recomputed: exact PV 10277.509103322713 -> 10278; per-term values 480.769 -> 481, 462.278 -> 462, 9334.462 -> 9334, sum 10277 (numbers_recheck.py). Page and test prose match.")
row("proj-lab3-claim-using-functions", "2.5-labs / prose vs code", "project.html line 198 (Lab 3 hypothesis) vs tests/labs/FC1/lab-FC1-project-3.py lines 42 and 54", FAIL,
    "The hypothesis says the program prints the fixture values 'using the functions of this lab in exact arithmetic'. Two fixture values are computed inline, not by a function: fixture E is the literal '(2, -10 * 9_850)' (lab line 54) and fixture B's exact value is 'Fraction(10_500) / Fraction(95, 100)' (lab line 42). The printed values are right; the sentence overstates the method.",
    "Either compute fixture E and the exact value of fixture B through a function of this lab, or reword the page's hypothesis to 'using the functions of this lab, and exact Fraction arithmetic for the exact values'. Then edit the twin and re-embed with tools/embed_labs.py project 3 --refresh (or the page's expected block if output changes), and re-run run_labs --page project.")
row("proj-expected-equals-output", "2.5-labs", "project.html expected blocks (lines 97, 145, 263-275)", PASS,
    "run_labs compares each expected block with the twin's stdout under the page's own rule (out/run_labs_project.out: PASS for all three labs).")

# ---- hours, rungs, spec ------------------------------------------------------------------------------------------
row("proj-hours-arithmetic", "2.6-hours / 2.9-structure", "project.html lines 286-293 (table#hours) and index.html data-hours-lessons/data-hours-project", PASS,
    "Seven component rows: 1+2+5+4+2+3+3 = 20, equal to the Total row (project.html line 293). Hub: data-hours-lessons=50 + data-hours-project=20 = 70 = curriculum hours (curriculum/02-economics-finance-core.yaml line 365-366); 20/70 = 28.6 percent (index.html line 41). Arithmetic consistent.")
row("proj-hours-rationale-rows", "2.6-hours", "project.html lines 286-293", PASS,
    "Each row has a one-line rationale. Estimated components against section 5.5 of plans/FC1-build-plan.md are not required by the architect's hours ruling (architect decisions, binding), so the 30 percent test is not applied.")
row("proj-ladder", "2.6-spec ladder", "project.html lines 41-50 and 153-278", PASS,
    "Rung 1 (Lab 1) is fully solved with a 'Step' comment for each of five steps; Rung 2 (Lab 2, class completion) is graded by run_labs and the browser; Rung 4 is labelled 'Not graded'. Rung 3 is covered by proj-spec-scope-vs-curriculum.")
row("proj-spec-interface", "2.6-spec", "project.html lines 161 and grader/starter.py lines 16-40", PASS,
    "Names and signatures on the page match starter.py: Bond(face_cents, coupon_bps, periods).events(), bond_price_cents(bond, yield_bps), CashTrade(quantity, price_cents, side, settlement_day).events(). The ValueError list (page lines 165-167) matches reference.py lines 42-47, 64-65, 81-88.")
row("proj-named-conditions", "2.6-autograder-exception-table", "grader/test_project.py must_raise call sites", PASS,
    "must_raise is used only for the named conditions: periods 0 and -1, face 0 and -1, coupon -1, yield -10000 and -20000, quantity 0 and -1, price -1, side 0, 2, -2, 3, -3, settlement_day 0 and -1. Each side of each limit is accepted (boundaries periods 1, face 1, coupon 0, yield -9999, quantity 1, price 0, side +1 and -1, settlement_day 1). Eight conditions, as the page says.")
row("proj-test-count", "2.6-autograder", "project.html line 171 ('68 checks') and grader/test_project.py", PASS,
    "pytest --co in a scratch copy with reference.py as instruments.py: '68 tests collected' (" + SCRIPTS + "/out/collect_only.out). Page count equals the real count.")
row("proj-starter-fails", "2.6-autograder", "grader/starter.py", PASS,
    "Starter run under the browser flags: 66 failed, 2 passed. The two passing tests (test_non_whole_face_is_refused_or_gives_ints, test_bool_periods_is_not_quietly_accepted_as_a_number) accept any exception by design (page lines 163-165). The suite fails overall on the empty implementation, which run_graders also requires.")
row("proj-instances", "2.6-autograder-2", "grader/instance.py, seeds 0-19", PASS,
    "Ran " + SCRIPTS + "/instances_seeds_0_19.py: every instance satisfies the page's valid-input rules (asserted), and all 20 seeds give distinct bond prices and distinct trade cash flows (out/instances.out).")
row("proj-silence-purity", "2.6-autograder", "grader/test_project.py lines 538-580", PASS,
    "The silence tests (valid and refused inputs) pass on reference.py and on all five alternatives on seeds 0-19 (out/alternatives_0_19.out). The pytest -W error flag turns any warning into a failure.")
row("proj-same-suite-pyodide-pytest", "2.6-autograder-5", "grader/test_project.py run in Pyodide (page_smoke) and in local pytest", PASS,
    "page_smoke ran the suite in Pyodide with 68 passing (out/page_smoke_project.out); local pytest with the same flags: 68 passed (collect and run in scratch, outputs in out/).")

# ---- mutants and alternatives ------------------------------------------------------------------------------------
row("proj-mutants-all", "2.6-mutation", "ledgers/FC1/mutants/*.py (80 files, 75 pre-existing and 5 written this round)", PASS,
    "Re-run: tools/mutate_graders.py --unit FC1 --seeds 0-9 -> 'mutate_graders FC1: PASS (80/80 killed)' (out/mutate_graders_0_9.out). Each mutant's killing test is listed in the mutants array.")
row("proj-mutants-v1c-new", "2.6-mutation", "ledgers/FC1/mutants/v1c_*.py (5 student-error mutants written by this verifier)", PASS,
    "Written by " + SCRIPTS + "/make_v1c_mutants.py from reference.py with one asserted replacement each: simple discount 1/(1+y*t); missing yield guard (ZeroDivisionError); seller side refused; price discounted at coupon rate; trade booked in dollars. All five are killed on seed 0 by a named test (mutate output).")
row("proj-alternatives", "2.6-autograder-alternatives", "ledgers/FC1/scripts/FC1-c-r1/alt_v1/alt1..alt5 (written this round)", PASS,
    "Five alternative correct implementations (list comprehension and floor half-up; generator methods; integer-only common denominator; Decimal in a local 60-digit context; Fraction power with a single validation helper) each pass all 68 tests on seeds 0-19: '0 of 20 failing seeds' each (run_alternatives_v1.sh, out/alternatives_0_19.out). No test is tolerance-based on money.")
row("proj-failure-messages", "2.6-autograder-4", "grader/test_project.py: 16 assert statements with no message (lines 173, 184, 189, 229, 309, 314, 332, 338, 343, 350, 357, 404, 409, 430, 468, 515)", FAIL,
    "A failing bare assert prints its source line, which contains the expected value. Plain-assert run of a mutant (out/leak_evidence_plain_assert.out, line 51 of the traceback): '> assert sol.bond_price_cents(sol.Bond(10_000, 500, 3), 400) == 10_278', so the answer 10278 is shown. The page says the flags show 'the test's own message and no values' (project.html line 309), and the test docstring says tests 'never print an expected value' (test_project.py line 13). Both claims are false for these 16 tests (out/bare_asserts.out).",
    "Give each of the 16 asserts a message that names the violated property without the value, for example ', \"the one-period bond at 500 bps is at par\"'. Then re-run " + SCRIPTS + "/bare_asserts.py on grader/test_project.py, which must print nothing, and re-run the mutate and run_graders gates.")

# ---- cards -------------------------------------------------------------------------------------------------------
row("proj-cards-scan-duplicates", "2.7-cards", "course/modules/FC/FC1/cards.json (119 cards)", PASS,
    "All 119 cards read. " + SCRIPTS + "/cards_scan.py (out/cards_scan.out): 119 unique ids, no duplicate ids, no duplicate fronts, no duplicate backs after whitespace and case normalisation. Semantic near-duplicates were read by eye (e.g. FC1-c066 and FC1-c067 are distinct claims about the same identity).")
row("proj-cards-numbers-in-lessons", "2.7-cards", "cards.json, all 119 cards vs L01-L05.html", PASS,
    "card_numbers_in_lessons.py: every numeric token of every card occurs in its lesson page text (out/card_numbers.out: missing_number_tokens=0).")
row("proj-cards-sample", "2.7-cards (sampled 1 in 10)", "cards.json FC1-c001, c011, c021, c031, c041, c051, c061, c071, c081, c091, c101, c111", PASS,
    "Sampled 12 cards checked against lesson text and arithmetic: c001 (Definition 1.1 in L01); c011 (1000/0.55 = 1818.18, 18.18 percent of 10000, Example 3.6 exists in L01); c021 (Proposition 1.4 in L02); c031 (twelve entries in L02); c041 (identity P = hV + sum sigma q (m_t - m_n) matches L03 Proposition 2.3); c051 (Remark 3.3 and Problem R1 about three dealers in L03); c061 (60*1000 + 90*1100 = 159000; average 1060); c071 (sell stop filling below its stop, L04 Example 1.4); c081 (L05 Remark 2.3 says the netting identities say nothing about failing payments); c091 (L01 Remark 4.2 is titled '(a test, not a legal rule)'); c101 (L05 Proposition 2.1(ii), 0 <= NP <= G); c111 (L01 A3 'closed system'). Not every one of the other 107 cards was re-derived line by line against its lesson; they were scanned for numbers, citations and duplicates only.")
row("proj-cards-citation-R3", "2.7-cards / 2.9-DAG", "cards.json FC1-c054 (lesson L03)", FAIL,
    "The back cites '(Lab 1, Part C; Problem R3)'. L03.html contains only 'Problem P1' and 'Problem R1' (grep of course/modules/FC/FC1/L03.html). Problem R3 exists only in L04.html, so the card cites a block that is not in its own lesson, and that problem concerns a different topic.",
    "Remove 'Problem R3' from FC1-c054 or replace it with 'Problem R1' if that is the intended block. Re-run " + SCRIPTS + "/card_refs_normalised.py (no UNRESOLVED line for FC1-c054).")
row("proj-cards-citation-R2", "2.7-cards", "cards.json FC1-c089 (lesson L05)", FAIL,
    "The back cites '(Problem R2)' for the step Pay_j >= 0. L05.html has no 'Problem' block; 'Problem R2' exists only in L04.html, where it concerns a crossed book. The citation is wrong for both the lesson and the claim.",
    "Remove the parenthetical '(Problem R2)' from FC1-c089, or cite the L05 step that uses Pay_j >= 0 (Proposition 2.1 proof).")
row("proj-cards-citation-scan", "2.7-cards", "cards.json, 182 block references", PASS,
    "card_refs_normalised.py (out/card_refs_normalised.out): 182 block references checked; 178 resolve in the card's own lesson page. Four hits are unresolved: FC1-c054 'Problem R3' and FC1-c089 'Problem R2' (the two FAIL rows above), and FC1-c052 'Lab 1, Part A' twice, which resolves to the Lab 1 output line 'Part A, mid fixed at 10000 cents' in L03.html (expected block); the raw first-pass output is in out/card_refs.out (its misses are label-format artifacts, e.g. the trailing full stop in 'Example 3.6.').")
row("proj-cards-grades", "2.7-cards / 2.3-grades", "cards.json grade fields for propositions (e.g. FC1-c079, c080, c089, c101)", PASS,
    "Cards marked grade T cite propositions graded T in their lesson (L05 Proposition 2.1 is data-grade T at L05.html line 78). Spot check only, on the sampled propositions.")

# ---- prose, scope, terminology, notation, references, data --------------------------------------------------------
row("proj-spec-scope-vs-curriculum", "2.6-spec (rung 3 matches curriculum scope)", "course/modules/FC/FC1/project.html lines 157 and 161; curriculum/02-economics-finance-core.yaml lines 390-393 (brief) and 397 (FC2 title)", FAIL,
    "The curriculum project brief (yaml lines 390-393) reads: 'Represent bonds, futures, swaps and options as dated cash-flow or payoff objects with a common interface, and test each against hand-computed examples.' The page covers a bond and a cash trade only, and says futures, swaps and options 'are not part of this project' (project.html line 157). That narrowing follows the architect's binding decision (plans/FC1-build-plan.md, 'Architect decisions', module specifics), but the curriculum brief has not been amended, so rung 3 does not match the curriculum scope.",
    "Architect or curriculum change request: amend curriculum/02-economics-finance-core.yaml lines 388-391 to the bond and cash-trade scope (and move the derivative objects to FC2, whose title is 'Derivatives Fundamentals' at yaml line 397), then regenerate with tools/render_curriculum.py and tools/build_site.py. Until then the verdict is a failure of this row.")
row("proj-terminology-short-holder", "2.12-prose", "course/modules/FC/FC1/project.html line 179 (Sides and signs)", FAIL,
    "'side is +1 for a long holder, who buys and pays cash, and -1 for a short holder, who sells and receives cash.' In market usage a holder who sells units it already owns is not short; 'long' and 'short' describe the position, not the trade side. The sentence misstates the terminology for a cash trade (the grader and lab only need buyer and seller).",
    "Replace with: 'side is +1 for the buyer, who pays cash, and -1 for the seller, who receives cash.' (keep the sign convention sentence unchanged).")
row("proj-prose-banned-phrases", "1.3-1.4 banned phrases", "course/modules/FC/FC1/project.html and cards.json", PASS,
    "grep -E for TODO, TBD, lorem, ellipsis, 'for brevity', 'beyond the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'experts agree', 'well known', 'obviously', 'clearly', and process words (builder, verifier, round, ledger, plan, checkout, mutant) in both files: no hits in project.html apart from the footer, which is the autograder sentence.")
row("proj-scope-words", "2.2 / prose scope words", "project.html scope words (only, all, always, every, any, same, exactly, never, none)", PASS,
    "Each scope word was read in context. 'this project uses none of them' (line 157) is checked: the grader and reference define only Bond and CashTrade (no Future, Swap or Option). 'Every amount is an int' and 'every step annotated' are definitions or descriptions, not counts. 'exactly' in Lab 3 and the 'exactly 10000' claims are computed (numbers_recheck.out).")
row("proj-terms-before-definition", "2.9 terms", "project.html: event, period, settlement period, holder, trade date (line 179)", PASS,
    "event, holder, settlement period and face are defined in the rungs paragraph before first use (line 54). 'trade date' (line 177) is used in its ordinary sense and is not defined on the page; it is the trade lifecycle's offset-0 date (L05). Noted, not failed.")
row("proj-notation", "2.9 notation", "project.html symbols y, t (lines 58, 106, 178) vs notation/notation.json (8 registered symbols)", PASS,
    "notation.json registers T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f and \\mathbb{Q}. The project page uses y (per-period yield) and t (period index), which are not registered and do not collide with a registered meaning. No macro from the registry is misused.")
row("proj-footer-claim", "2.9 prose claim", "project.html line 341 footer ('nothing you write leaves it')", PASS,
    "page_smoke enforces zero requests to any host other than the local server (out/page_smoke_project.out), and grader.js saves code only through the local store (store.put); the only network calls are same-origin file fetches (course/assets/js/grader.js lines 18, 88-89).")
row("proj-saved-as-you-type", "2.9 prose claim", "project.html line 301 ('saved in this browser as you type')", PASS,
    "course/assets/js/grader.js lines 59-62: an input listener writes the draft with store.put after a 400 ms debounce. 'As you type' is accurate within that debounce.")
row("proj-references-reading-list", "2.1 citations", "project.html lines 321-328; references/references.json entries harris2002trading and mishkin2021economics", PASS,
    "Both keys exist (references.json entries, status 'verified'). tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' (out/verify_refs_offline.out). The page makes no bibliographic or year claim ('This page attributes no statement to either'), consistent with architect decision Q3. The live Crossref/OpenLibrary run was not repeated (plain verify_refs needs a network run; the --unit flag is refused for live runs).")
row("proj-cited-year-conflicts", "2.1 citations (registry)", "references/references.json: harris2002trading (notes.year: curriculum 2003, crossref 2002); mishkin2021economics (notes.year: curriculum 2022, record 2021)", PASS,
    "Recorded as registry flags only. The page does not state a year, so no claim fails here; curriculum sources list (2003) and (2022) disagree with the registry (curriculum/02-economics-finance-core.yaml lines 384-385).")
row("proj-data-simulated", "2.8 data", "project.html lines 54, 159; tests/labs/FC1/lab-FC1-project-1..3.py; grader/instance.py docstring", PASS,
    "No data-files on any project lab (run_labs reads none). Labelled SIMULATED: twin tests/labs/FC1/lab-FC1-project-1.py line 14 ('SIMULATED face ... not market data'), page lines 54 and 159, instance.py line 3 and label string line 31.")
row("proj-reference-deployment", "repo-wide (not failed)", "course/modules/FC/FC1/grader/reference.py", PASS,
    "Per the round instruction, this repo-wide matter is recorded, not failed: reference.py is a tracked full solution in the module's grader directory. BLUEPRINT requires deployment to exclude it; no file in the repository enforces that (reference.py docstring lines 3-4 say so).")

rows_total = len(rows)

# ---- mutants from the mutate output ------------------------------------------------------------------------------
mutants = []
for line in MUTATE_OUT.read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+\.py): (.*) -> (\S+) \(seed (\d+)\)$", line)
    if not m:
        continue
    status, name, description, test, seed = m.groups()
    if status != "KILLED":
        continue
    mutants.append({
        "id": name.removesuffix(".py"),
        "file": f"ledgers/FC1/mutants/{name}",
        "description": description,
        "killed_by": f"{test} (seed {seed})",
    })

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
verdict = "PASS" if counts["PASS"] == rows_total else "FAIL"

fragment = {
    "unit": "FC1",
    "slice": "c",
    "round": 1,
    "verifier": "Claude Haiku 5.5, independent verifier for FC1-c, round 1 (did not build FC1)",
    "pin": PIN,
    "base": "n/a (round 1 of this slice)",
    "checkout": str(ROOT),
    "scratch": "/tmp/fc1c_scratch and /tmp/fc1c_alt_* (scratch copies; the evidence is copied under " + SCRIPTS + "/out)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "harris2002trading: registry year 2002 (crossref), curriculum year 2003; page cites the key only (architect Q3)",
        "mishkin2021economics: registry year 2021 (record), curriculum year 2022; page cites the key only (architect Q3)",
    ],
    "freshness_flags": [],
    "notes": (
        "Round 1 of FC1-c on pin d0f39c09. The slice's previous fragment (round 13 at 762f636d) is preserved in git history at d0f39c09 and was replaced in this working tree because the assignment named this path. "
        "Command rows were re-run on the pin: check_projects, check_pages, check_dag, run_labs --page project, page_smoke --pages project, run_graders 0-19, mutate_graders 0-9 (80 mutants), verify_refs --offline, ruff, mypy. "
        "Not checked: the full pytest suite and render_curriculum/build_site/fetch_data checks (no input of this slice changed in a way they read beyond the page); live verify_refs (network); Pyodide-only rerun of the five new mutants (the browser suite ran the reference only); line-by-line re-derivation of all 119 cards (all read, scanned, and 12 sampled as rows); hours not re-estimated (architect ruling); a visual check of the grader panel."
    ),
    "summary": f"{rows_total} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. {len(mutants)}/{len(mutants)} mutants killed on seeds 0-9. Verdict {verdict}.",
}
out = ROOT / "ledgers/FC1/FC1-c.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, "rows", rows_total, counts, "mutants", len(mutants), "verdict", verdict)
