"""PC3-b round 16: assemble ledgers/PC3/PC3-b.json from the round-15 rows (row ids kept), this round's overrides and new rows.

Usage: python -I ledgers/PC3/scripts/PC3-b-r16/make_fragment.py
Every row carries evidence from this round's own reads or scripts (see out/ and the scripts in this directory).
"""
import json
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE16-PC3-b")
OUT = "ledgers/PC3/scripts/PC3-b-r16/out"
prev = json.loads(Path("/Users/billyribeiro/.fanout/frags/E-PC3-b.round15.json").read_text(encoding="utf-8"))

PREFIX = "Re-verified round 16 at 56cc575 (cited lines unchanged since d1e65a0): "

# rows whose cited subject changed since d1e65a0, or whose status changes; full new evidence text
OVR = {
    "gate-run-labs-unit": ("tools/run_labs.py --unit PC3", "run_labs PC3: PASS (9/9), exit 0 (" + OUT + "/run_labs_unit.out); includes lab-PC3-L04-1, L05-1, L06-1."),
    "gate-check-pages": ("tools/check_pages.py --unit PC3", "check_pages PC3: PASS, exit 0 (" + OUT + "/check_pages_unit.out)."),
    "gate-check-dag": ("tools/check_dag.py --unit PC3", "check_dag PC3: PASS, exit 0 (" + OUT + "/check_dag_unit.out); check_dag --all: LX1, LX2, PC3 PASS (" + OUT + "/check_dag_all.out)."),
    "gate-check-projects": ("tools/check_projects.py --unit PC3", "check_projects PC3: PASS, exit 0 (" + OUT + "/check_projects_unit.out). Run for the gate table; the project rows belong to slices c and d."),
    "gate-page-smoke-slice": ("tools/page_smoke.py --unit PC3 --pages L04 L05 L06 (run alone)", "page_smoke PC3: PASS for L04, L05, L06, exit 0 (" + OUT + "/page_smoke_slice.out); the tool's own PASS line; its internal checks (console errors, external requests) were not re-read this round, so this row rests on the tool's PASS."),
    "gate-ruff-mypy-twins": ("ruff check tests/labs/PC3; ruff format --check tests/labs/PC3; mypy --no-incremental", "ruff check tests/labs/PC3: All checks passed (" + OUT + "/ruff_check_twins.out); ruff format --check tests/labs/PC3: 9 files already formatted (" + OUT + "/ruff_format_twins.out); mypy --no-incremental: Success, 385 source files (" + OUT + "/mypy.out)."),
    "gate-pytest-lab-tooling": ("pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py", "pytest exit 0, all dots, no failures (" + OUT + "/pytest_labs_tooling.out)."),
    "gate-verify-refs-offline": ("tools/verify_refs.py --offline (whole registry)", "offline integrity: 560 entries, 0 problems, exit 0 (" + OUT + "/verify_refs_offline.out)."),
    "gate-run-graders-unit": ("tools/run_graders.py --unit PC3 --seeds 0-49", "run_graders PC3: PASS (reference 50/50 seeds), exit 0 (" + OUT + "/run_graders_unit.out). Run for the gate table; the grader rows belong to slices c and d."),
    "gate-fetch-data-check": ("tools/fetch_data.py --check", "fetch_data: 3 datasets, 0 problems, exit 0 (" + OUT + "/fetch_data_check.out)."),
    "gate-build-site-check": ("tools/build_site.py --check", "site data current: 6 outputs, exit 0 (" + OUT + "/build_site_check.out)."),
    "gate-render-curriculum-diff": ("tools/render_curriculum.py; git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json", "render_curriculum wrote the same files; git diff --exit-code exit 0 (" + OUT + "/render_curriculum.out, " + OUT + "/render_curriculum_diff.out)."),
    "notation-registry-L04-L06": ("course/modules/PC/PC3/L04.html, L05.html, L06.html math vs notation/notation.json", "Registered macros used on the pages: \\E and \\Var (L04 only), same meanings. No registered symbol (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) appears in math on L04-L06 (scripted scan, round 16). Local symbols N, t, p, L, v, a, b, h, q, I, C, W, sigma, eps, D, A, tau, ell are used only inside their lesson."),
    "twin-run-alone-L04-L06": ("tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py", "Run alone as python -I -W error <twin> (cwd /tmp): exit 0, stderr 0 bytes for all three (" + OUT + "/twin_check.out)."),
    "twin-page-code-equals-twin": ("L04.html, L05.html, L06.html data-run vs the three twins", "Page code equals twin after HTML unescape, except one trailing newline that the twin file has and the page omits (script compares rstrip('\\n')==twin.rstrip('\\n') equal for all three) (" + OUT + "/twin_check.out; ledgers/PC3/scripts/PC3-b-r16/twin_check.py)."),
    "twin-expected-equals-stdout": ("L04.html pre.expected vs stdout of lab-PC3-L04-1; L05.html vs lab-PC3-L05-1; L06.html vs lab-PC3-L06-1", "Run output equals the expected block line for line after rstrip: 52 = 52 lines (L04), 25 = 25 (L05), 21 = 21 (L06) (" + OUT + "/twin_check.out)."),
    "L04-misconceptions": ("L04.html lines 490-505 (four misconceptions)", "Re-read round 16. Line 492 changed to 'h/2 cents per turn when p=1/2, one quarter of the quoted spread 2h'; (1-p)h at p=1/2 is h/2 = 5 cents = (2h)/4 with h=10 (Prop 3.1). Lab 1 Part 2 prints 0 cents at v=10020 (verify_numbers.out grid check and run_labs output). Other three misconceptions re-derived: M1 (10010-10000=10), M2 (2 units short), variance 2500 at 10 units; quoting-rule misconception matches A3."),
    "L04-remark-3.4-inventory-zero": ("L04.html lines 157-158 (Remark 3.4)", "Re-read round 16. Line 158 now says (1-p)h cents per turn, h/2 at p=1/2, one quarter of 2h; each is correct from Prop 3.1 (verify_numbers.py 'closed form' and 'Example 3.2' checks, PASS)."),
    "L05-why-it-matters-comparisons": ("L05.html line 52 (why it matters) plus Definition 1.3 (line 77) and Definition 3.1 (line 105)", "Re-read round 16. Line 52 now cites 'Definition 3.1 of this lesson' for the monotonic deque; Definition 3.1 exists (L05.html line 105) and defines the deque; 'Definition 1.3' also exists (line 77). The 'at most twice the input length in comparisons' phrase matches Prop 3.3 (while-loop tests, 2n); see notes on what 'comparisons' counts."),
    "L06-why-it-matters-scope": ("L06.html line 52 (why it matters)", "Re-read round 16. Line 52 now cites 'a case (Definition 4.1 of this lesson)'; Definition 4.1 (case interview) exists (L06.html line 143) and Proposition 3.1 and Remark 4.3 are cited correctly. The remaining scope statements re-read in the scope scan (out/prose_scan.out) are computed or proved."),
    "L06-canon-breaks-and-misconceptions": ("L06.html lines 310-312 (canon breaks), 318-333 (misconceptions)", "Re-read round 16. Line 322 now says the break-even 'rises by 21.24 units per point of rate', (1249.0469-1164.1005)/4 = 21.2366 (verify_numbers.py L06 Remark 4.3 / E3 checks, PASS); other misconceptions re-derived (no-arbitrage payoff 0 at 10000 and 100 at 10100; sign at bounds same at 8, 10, 12 percent: -12422903/-12513148/-12598169 and 5616776/4894816/4214650; four grid points). Canon breaks: 'factor of 8' = 1600/200 (line 313), 'real assets' sentence (line 309) matches card PC3-c190."),
    "L06-corollary-3.3-grade": ("L06.html lines 130-137 (Corollary 3.3 statement at 132; proof at 137)", "Was FAIL in round 15. Line 132 now reads 'A range of positive width with an end exactly at u* does not fix the sign, because the NPV is zero at that end and nonzero at the other end.' The degenerate point range l = h = u* is excluded by 'positive width'. Proof (line 137) gives NPV(u) = mA(u-u*) (Prop 3.1), so for l < u* = h the NPV is zero at h and nonzero at l, and the sign is not fixed; for h < u* or l > u* it is fixed. Grade T and the hypotheses (Props 3.1, 3.2) match. Card PC3-c112 carries the same sentence (cards.json line 957)."),
    "card-PC3-c112-corollary-boundary": ("course/modules/PC/PC3/cards.json line 957 (PC3-c112 back)", "Was FAIL in round 15. Back now carries 'A range of positive width with an end exactly at u* does not fix the sign, because the NPV is zero at that end and nonzero at the other end', identical in substance to L06.html line 132. Checked against the lesson, not against the round-15 wording."),
    "card-full-scan-L04": ("cards.json: all 39 L04 cards (PC3-c062..c083, c137..c141, c153..c154, c162..c164, c168, c171, c174..c176, c185..c186)", "Re-scanned all 39 L04 cards in full (round 16). Changed card PC3-c186 checked (see row r16-card-c186). Every other card checked against lesson text and lab output: grades T/C as lesson states, basis fields present, cite [] for all. Seeded-run cards (c077, c137-c141) are graded C with basis naming the SIMULATED lab; they are accepted under the round 3-15 precedent and noted in notes."),
    "card-full-scan-L05": ("cards.json: all 30 L05 cards (PC3-c084..c101, c142..c146, c169..c170, c177, c180..c182, c188)", "Re-scanned all 30 L05 cards in full (round 16). Counts checked: 1351 = 193*7, 5239 = 169*31, 354/350/382/387 and pushes/pops against the L05 expected block (out/twin_check.out); 4200 = 3*200*7; 2n = 400. New card c188 checked (row r16-cards-c188-c190). No duplicates."),
    "card-full-scan-L06": ("cards.json: all 40 L06 cards (PC3-c102..c127 except c118, c147..c151, c165..c167, c178..c179, c183..c184, c187, c189..c190)", "Was FAIL in round 15 (on c112, now fixed). Re-scanned all 40 L06 cards in full (round 16). Numbers checked against lesson text and scripts: 3310/1331, 399300/331, 1164.1005, 1206.3444, 1249.0469, 2.5770970, 2.4018313, -16655000000/1331, 4894816, 500/121, 33275/331, 0.7540, 24.6 percent, 21.24. Card PC3-c124 (positive at 1200 units at 8 percent) is arithmetically correct (+462582 cents) and derivable from the lesson's 8 percent break-even; see row r16-card-c124."),
    "card-duplicate-scan": ("cards.json: all 109 L04-L06 cards and all 185 PC3 cards", "Programmatic scan (round 16): 109 slice cards, 0 duplicate ids, 0 duplicate fronts, 0 duplicate backs across all PC3 cards; every card has a valid grade field, cite [] and a basis when graded T or C."),
    "card-number-in-lesson": ("cards.json numbers vs own lesson text and lab output (L04-L06)", "Programmatic scan (round 16): every numeric token of length >= 2 digits in the 109 slice cards appears verbatim in the card's own lesson HTML (0 missing). Seeded-run numbers also match the expected blocks."),
    "card-cite-empty": ("cards.json L04-L06 'cite' fields", "Programmatic scan (round 16): cite is [] on all 109 slice cards."),
    "card-key-results-agreement": ("cards.json L04-L06 cards vs key-results tables L04.html 620-625, L05.html 472-477, L06.html 448-453", "Re-read the three key-results tables in round 16. Every card whose claim matches a key-results row agrees with it (for example PC3-c071 = row 'zero exactly at v=a+h'; PC3-c147 and key row 6 for 399300/331; PC3-c075 = nine-value grid row, grade C in both)."),
    "card-PC3-c187-articulation": ("cards.json PC3-c187 (L06) vs course/modules/AC/AC1/L03.html line 57", "AC1 L03 line 57 states 'the cash-flow statement ends at the balance-sheet cash' (read in round 16). Card and L06 Section 1 agree; card has cite []."),
    "card-PC3-c081-basis-H2": ("cards.json PC3-c081 basis vs L04 A3 and Prop 3.1 (H2)", "Re-read round 16: basis 'Assumption A3 and hypothesis (H2) of Proposition 3.1 (the quote is fixed)' matches L04.html A3 (line 74) and the Prop 3.1 hypotheses (line 128)."),
    "L04-A1-project-consistency": ("L04.html line 72 and line 83 vs project.html lines 53-57, 76-81", "project.html changed this round only at line 397 (diff d1e65a0..56cc575), outside lines 53-57 and 76-81; the lesson's constants (N=20, v_0=10000, 5-cent moves, q-bar=5, L=10, p=1/2) still match those project lines. Re-checked round 16."),
    "delta-r14-hunks-L04-L06-cards": ("round-15 delta cards c081, c112, c187 (kept id; re-verified this round)", "The round-15 card hunks are re-read at 56cc575: c081 unchanged (r16 basis check), c187 unchanged (AC1 line 57), c112 changed again this round and is re-verified (row card-PC3-c112-corollary-boundary)."),
    "delta-r14-twins-unchanged": ("git diff 8e5751c9..d1e65a0 -- tests/labs/PC3 and d1e65a0..56cc575 -- tests/labs/PC3", "Both diffs are empty (0 files): git diff --name-only 8e5751c9 d1e65a0 -- tests/labs/PC3 gives 0 files; git diff --name-only d1e65a0 56cc575 -- tests/labs/PC3 gives 0 files (round 16)."),
    "delta-r15-L05-unchanged": ("git diff 8e5751c9..d1e65a0 -- course/modules/PC/PC3/L05.html", "The round-15 delta claim holds: 0 files for 8e5751c9..d1e65a0. Separately, L05.html changed in d1e65a0..56cc575 (line 52 only), re-verified in row L05-why-it-matters-comparisons."),
    "L06-E2-first-negative": ("L06.html line 404 (E2 solution), against tests/labs/PC3/lab-PC3-L06-1.py lines 105-106 and the expected block", "Hand NPVs check (-105000000/1331 = -78888.05 at 1200; 1550000000/1331 = 1164537.94 at 1300); four grid points above break-even 1206.34 check (verify_numbers.py). But the sentence 'Lab 1, Part 2 checks that the NPV increases on the grid but prints no NPV at a grid point' is false: the lab prints 'NPV at the lower bound = -12513148 cents' (units 200) and 'NPV at the upper bound = 4894816 cents' (units 1600), and 200 and 1600 are grid points (twin lines 105-106; expected block lines 'NPV at the lower bound', 'NPV at the upper bound')."),
    "L06-E2-hand-npv": ("L06.html lines 401-405 (E2 hand values)", "Covered by row L06-E2-first-negative (the defect sentence is on line 404, in the same solution)."),
}
FAIL_FIX = {
    "L06-E2-first-negative": "On L06.html line 404 replace 'Lab 1, Part 2 checks that the NPV increases on the grid but prints no NPV at a grid point' with 'Lab 1, Part 2 checks that the NPV increases on the grid and prints NPVs only at the two bounds, 200 and 1600 units, which are grid points', so the two hand NPVs at 1200 and 1300 units are not printed by the lab.",
}

NEW = [
    ("r16-delta-scope", "2.10-delta", "git diff --name-only d1e65a0 56cc575 (PC3 slice)", "PASS",
     "Slice hunks: L04.html lines 158 and 492 (1 line each); L05.html line 52 (1 line); L06.html lines 52, 132, 305, 322, 324, 404 (1 line each, no line-count change); cards.json c112 (changed), c186 (changed), c188, c189, c190 (new). tests/labs/PC3 unchanged (0 files). project.html changed at line 397 only (other slice). Each slice hunk was read and re-derived this round (rows below)."),
    ("r16-L04-remark-3.4-hunk-158", "2.4-mathematics", "L04.html line 158 (Remark 3.4)", "PASS",
     "(1-p)h at p=1/2 is h/2 = (2h)/4, a quarter of 2h; 'cents per turn' is the Prop 3.1 expectation from inventory zero; the parenthetical ('a per-turn average set against a per-trade spread') is a wording note, not a numeric claim. Checked against verify_numbers.py (Prop 3.1 enumeration)."),
    ("r16-L04-misconception-1-hunk-492", "2.2-numbers", "L04.html line 492 (misconception 1)", "PASS",
     "h/2 = 5 cents at p=1/2, h=10; 'Lab 1, Part 2 prints 0 cents at v=10020' matches the lab output line 'fair value v = 10020: E[change] = 0 cents'."),
    ("r16-L04-canon-mid-induction", "2.4-mathematics", "L04.html line 484 (canon breaks): mid at turn t is 10000 - 10 I_{t-1}", "PASS",
     "Induction on the fills is valid for the Example 1.3 rule (a fill sets the mid to the fill price, which is the mid plus or minus 10). Independent simulation (out/sim_game_independent.out): the identity mid = 10000 - 10*I_{t-1} holds at every turn for seeds 0..499; largest |I| 8 over those seeds."),
    ("r16-L05-why-it-matters-forward-refs", "2.9-prose", "L05.html line 52 (why it matters) and its references Definition 1.3 (line 77), Definition 3.1 (line 105)", "PASS",
     "Both cross-references resolve to the right definitions (sliding-window maximum; the deque and its invariant). Proposition 3.3 bounds the while-loop comparisons at 2n, and the lab counts comparisons of stored values only; the expiry test (an index comparison) is excluded in the proof, see notes."),
    ("r16-L06-why-it-matters-def-4.1", "2.9-prose", "L06.html line 52 (why it matters); Definition 4.1 at line 143", "PASS",
     "'a case (Definition 4.1 of this lesson)' resolves to the case-interview definition (line 143); 'Proposition 3.1 of this lesson' and 'Remark 4.3 of this lesson' also resolve."),
    ("r16-L06-interpretation-hunk-305", "2.2-numbers", "L06.html line 305 (interpretation) vs expected block 'NPV at the lower bound = -12513148 cents (exact -16655000000/1331)'", "PASS",
     "The interpretation says the lower-bound NPV prints its exact fraction and whole cent, and the other NPVs print only the whole cent. Lab lines 105-106 and the expected block agree: the lower-bound line prints both, the upper-bound line only the whole cent; the sensitivity table prints whole cents only."),
    ("r16-L06-misconception-2-hunk-322", "2.2-numbers", "L06.html line 322 (misconception 2): 'the break-even rises by 21.24 units per point of rate'", "PASS",
     "(1249.0469-1164.1005)/4 = 21.2366, which displays as 21.24; 'rises' is correct because the break-even 3000/A increases as A falls with the rate (1164.10 at 8 percent, 1249.05 at 12 percent)."),
    ("r16-card-c186", "2.7-cards", "cards.json PC3-c186 (L04) vs L04.html line 484", "PASS",
     "Card back 'm_t = 10000 - 10 I_(t-1)' matches the canon-breaks claim and the independent simulation (r16-L04-canon-mid-induction). Grade T with basis 'Section 5 (induction on the fills...)' is consistent with the lesson."),
    ("r16-cards-c188-c190", "2.7-cards", "cards.json PC3-c188 (L05), PC3-c189 and PC3-c190 (L06) vs canon-breaks sections", "PASS",
     "c188 matches L05.html's amortised-bound paragraph (line 339: 'at most two comparisons per step', 'a single step can cost of order k', per-step bound false). c189 matches L06.html line 312 ('wide, by a factor of 8', three factors each varying by 2; 1600/200 = 8). c190 matches L06.html line 310 (model result under A1 to A5; real assets pay income). All grade T with basis fields; cite []."),
    ("r16-prose-scan", "2.9-prose", "scripted scan of visible prose of L04, L05, L06 (ledgers/PC3/scripts/PC3-b-r16/prose_scan.py)", "PASS",
     "0 banned phrases, 0 process words (build, builder, round, verifier, REQUESTS, unit report), 0 three-dot ellipses (out/prose_scan.out). 140 sentences with scope words (only, all, always, every, any, same, exactly, never) were each read: each is a definition, an explicit assumption, a proof step, a finite computation or a negative claim."),
    ("r16-twin-page-and-run", "2.5-labs", "tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py; the three pages", "PASS",
     "Each twin was read in full. Page code equals twin up to one trailing newline (out/twin_check.out). Each twin ends with an unconditional main() call and has no __main__ guard; run alone under python -I -W error exits 0 with empty stderr; stdout equals the expected block line for line. Lab runtimes are reported as 0.0 s by page_smoke."),
    ("r16-numbers-rederivation", "2.2-numbers", "all numbers in L04-L06 prose, quiz, key results and problems (ledgers/PC3/scripts/PC3-b-r16/verify_numbers.py)", "PASS",
     "58 of 58 independent checks pass (out/verify_numbers.out): Prop 3.1 closed form equal to exhaustive enumeration for p in {0,1/4,1/2,3/5,1} over v=9950..10050; the nine grid values; Remark 4.2 (5/2 at I=10); Cor 3.3 zero only at v=10020; R1 d=20/3; E2 z=1.34 < 1.959964 (z(0.975) = 1.9599639845 from statistics.NormalDist); L05 counts 1351, 5239, 5239/382=13.7, 4200, 400; deque equal to naive maxima on 300 random sequences; Prop 3.3 bounds; L06 M2 500/121, M3 33275/331, A(8/10/12%), Remark 4.3 break-evens and differences, E3 widths and rounding, R3 m*=3769.8 (0.7540, 24.6 percent), E2 hand NPVs, sign at bounds at three rates."),
    ("r16-sim-independent", "2.5-labs", "independent re-implementation of the L04 game rules (ledgers/PC3/scripts/PC3-b-r16/sim_game_independent.py)", "PASS",
     "Seed 0: 9 fills, cash flow -9950, inventory 1, settlement 9980, P&L 30, 13 informed arrivals, max |I| 3; seed 1: 16 fills, cash 20100, inventory -2, settlement 10020, P&L 60. All equal the lab's printed values (out/sim_game_independent.out). Draw order taken from the twin's docstring text and the lesson's Definition 1.1 order (move, then arrival)."),
    ("r16-card-c124", "2.7-cards", "cards.json PC3-c124 (L06): NPV at 1200 units and 8 percent is positive", "PASS",
     "Recomputed: -15000000 + 5000 * 1200 * 2.5770970 = +462582 cents, positive. The sign follows from the lesson's 8 percent break-even 1164.10 and monotonicity (Prop 3.1). Card number 1200 appears in the lesson (E2), and the 8 percent break-even appears in Remark 4.3; the combined claim is derived, not quoted."),
    ("r16-gates-ruff-format-repo", "2.9-prose", "ruff check . ; ruff format --check . (repo)", "PASS",
     "ruff check . : All checks passed; ruff format --check . : 553 files already formatted (" + OUT + "/ruff_check_repo.out, " + OUT + "/ruff_format_repo.out)."),
    ("r16-gate-check-dag-all", "2.9-DAG", "tools/check_dag.py --all", "PASS",
     "check_dag LX1, LX2, PC3: PASS (" + OUT + "/check_dag_all.out). Concepts used by L04-L06 and their defining modules, checked by hand: market-maker, bid-ask-spread, limit-order-book (FC1 L03/L04, in closure through FC2), expectation (M4), big-O (CS2), unit-test (CS1, in closure as CS2 prereq), hash-map, binary-heap, monotonic-deque (CS2), forward-contract, cost-of-carry-forward-price, put-call-parity (FC2), net-present-value (CF1), statement-articulation (AC1 L03; AC1 is in the closure per plan section 2.2), fermi-estimation (PC3 L01)."),
]

notes = list(prev.get("notes", []))
notes = [n for n in notes if not n.startswith("Checkout note") and not n.startswith("Carried rows") and not n.startswith("Defect class found")]
notes = [
    "Checkout note: the checkout is at 56cc575a774a66e9580d3182969eb7d6aa413731 (detached), base d1e65a0203e386e3246429ba1cf7e723eb6cfbfa (round-15 pin). .venv is a symlink to the main checkout's venv; vendor copied.",
    "Carried rows: none carried without re-check. Every row of the round-15 fragment was re-read and re-derived this round (row ids kept). The round-15 PASS rows were used only as the list of checks; their evidence was re-run or re-read at 56cc575.",
    "Defect class found this round: a sentence about what a lab prints (L06.html line 404, 'prints no NPV at a grid point') is false, because the lab prints NPVs at the two grid-point bounds 200 and 1600. Fix is one sentence (row L06-E2-first-negative). The round-15 T-graded Corollary 3.3 fix (degenerate range) is verified fixed in both places.",
    "Judgement (not a row): 'comparisons' in L05 why-it-matters and Prop 3.3 counts the while-loop tests of stored values (the lab counts exactly these, 'comparisons of stored values'). The expiry test 'front <= i-k' is an index comparison, excluded from Prop 3.3 by the proof ('not counted in Proposition 3.3'). Read as that, the 2n bound holds; if 'comparisons' included every <= test, the total would be at most 3n. The lesson defines its count in the proof, so no FAIL is given; the architect may want the why-it-matters sentence to say 'comparisons of stored values'.",
    "Judgement (not a row): the L06 lab prints 'initial outlay of the portfolio: -S for the asset plus S from the loan = 0 cents' from the literal expression -spot + spot. The lesson does not present this line as a check (zero cost is proved on the page, Prop 2.1(i)), so no row fails; the code line is a tautology and could be replaced by a computed cost.",
    "Judgement (not a row): seeded-run cards (PC3-c077, c137-c141, and the L05/L06 seeded counts) test the printed output of one SIMULATED path. They are graded C with the lab named in basis (rule 9). Under rule 2.7 ('not trivia') they are borderline; accepted under the round 3-15 precedent.",
    "Judgement (not a row): the Section 5 real-market sentences in L04 and L06 are model-limit prose with no grade or registry key, as in round 15; accepted for the same reason.",
    "Mutation testing: not applicable to this slice (lab twins and cards; graders belong to slices c and d). mutants is empty; no mutant was written or killed.",
    "Not checked: the Pyodide browser runtime beyond page_smoke's own run; the visual layout at 360 px (page_smoke's checks are the only evidence); the registry (no key is cited in this slice); project pages, graders and hub (other slices); tests/test_docs_figures.py (not in this slice's gates, run only by the full gate); the lesson-level 'CS1 unit-test' definition was checked only through the curriculum yaml owner (CS1) and check_dag, not by reading CS1 pages.",
]

rows = []
seen = set()
for r in prev["rows"]:
    rid = r["id"]
    seen.add(rid)
    if rid in OVR:
        loc, ev = OVR[rid]
        status = "FAIL" if rid in FAIL_FIX else "PASS"
        row = {"id": rid, "check": r["check"], "location": loc, "status": status, "evidence": ev}
        if status != "PASS":
            row["fix"] = FAIL_FIX[rid]
    else:
        status = "PASS"
        row = {"id": rid, "check": r["check"], "location": r["location"], "status": status,
               "evidence": PREFIX + r["evidence"]}
    rows.append(row)
for rid, check, loc, status, ev in NEW:
    if rid in seen:
        raise SystemExit("duplicate id " + rid)
    rows.append({"id": rid, "check": check, "location": loc, "status": status, "evidence": ev})

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
verdict = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 else "FAIL"

frag = {
    "unit": "PC3",
    "slice": "PC3-b",
    "round": 16,
    "verifier": "Claude Haiku 5.5, independent verifier for PC3-b round 16 (did not build PC3)",
    "pin": "56cc575a774a66e9580d3182969eb7d6aa413731",
    "base": "d1e65a0203e386e3246429ba1cf7e723eb6cfbfa (round-15 pin). Delta d1e65a0..56cc575 in this slice: L04.html lines 158, 492; L05.html line 52; L06.html lines 52, 132, 305, 322, 324, 404; cards.json c112, c186 (changed), c188, c189, c190 (new). Twins unchanged.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE16-PC3-b",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyE16-PC3-b/ledgers/PC3/scripts/PC3-b-r16/out",
    "verified_at": "2026-11-09T02:30:00+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": ("Slice b (L04-L06, twins, 109 cards), round 16. One FAIL row: L06.html line 404 (E2 solution) says Lab 1 Part 2 "
                "'prints no NPV at a grid point', but the lab prints NPVs at the grid-point bounds 200 and 1600 units. "
                "Fix: one sentence. Round-15 FAIL rows (Corollary 3.3 degenerate range, card PC3-c112) are verified fixed. "
                "All twins, expected blocks, numbers, cards, notation, prose scans and gates PASS."),
}
out_path = ROOT / "ledgers/PC3/PC3-b.json"
out_path.write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out_path, "rows", len(rows), counts, "verdict", verdict)
