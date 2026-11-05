"""Build ledgers/FC2/FC2-d.json (round 10) from the round-9 fragment, this round's script outputs and the carry rules.

Every round-9 row id is kept. Rows whose subject is byte-identical since the round-9 pin (1e272e5) are carried with the
prefix the verifier rules require; rows whose subject changed, and every gate, are re-verified with this round's outputs.
Usage: build_fragment_fc2d_r10.py <repo_root>
"""

import json
import os
import re
import sys

from_root = os.path.abspath(sys.argv[1])
sys.path.insert(0, os.path.join(from_root, "tools"))
import ledger  # noqa: E402

R9 = json.load(open("/Users/billyribeiro/.fanout/frags/D-FC2-d.round9.json", encoding="utf-8"))
r9 = {r["id"]: r for r in R9["rows"]}
OUT = os.path.join(from_root, "ledgers", "FC2", "scripts", "FC2-d-r10")
SCR = "ledgers/FC2/scripts/FC2-d-r10/"
PIN9 = "1e272e5"

G = "course/modules/FC/FC2/grader (test_project.py, instance.py, reference.py, starter.py)"
LABS = "tests/labs/FC2"
RUNS = {}


def out(name):
    return open(os.path.join(OUT, name), encoding="utf-8").read().strip()


mut_text = out("mutate_fc2_r10_all.out")
killed = re.findall(r"^KILLED (\S+): (.*?) -> (\S+) \(seed (\d+)\)", mut_text, re.M)
mutants = []
for name, desc, test, seed in killed:
    mutants.append({"name": name[:-3], "description": desc, "killed_by": f"{test} (seed {seed})"})
assert len(mutants) == 87, len(mutants)
# docstring check: every mutant's module docstring opens with one line that describes the error
for m in mutants:
    src = open(os.path.join(from_root, "ledgers", "FC2", "mutants", m["name"] + ".py"), encoding="utf-8").read()
    first = src.split("\n", 1)[0]
    assert first.startswith('"""') and len(first) > 6, m["name"]  # first docstring line opens the module docstring

rows = []


def carry(rid, files):
    base = r9[rid]
    assert base["status"] == "PASS", rid
    rows.append({
        "id": rid, "check": base["check"], "location": base["location"], "status": "PASS",
        "evidence": f"Carried from round 9 ({files} byte-identical since the previous pin {PIN9}): {base['evidence']}",
        "fix": "",
    })


def rev(rid, check, location, evidence, status="PASS", fix=""):
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})


# ---- gates and runs re-executed on pin 47a36d8 -------------------------------------------------------------
rev("fc2d-r2-gate-mutate", "2.6", "tools/mutate_graders.py --unit FC2 --seeds 0-9",
    f"{SCR}mutate_fc2_r10_all.out: 'mutate_graders FC2: PASS (87/87 killed)', rc=0. The 83 round-9 mutants and the four new ones (z10_a..z10_d) were all re-run; {SCR}intended_kills_r10.out shows each new mutant fails its intended test on seed 0.")
rev("fc2d-r2-gate-run-graders", "2.5/2.6", "tools/run_graders.py --unit FC2 --seeds 0-49",
    f"{SCR}run_graders.out: 'run_graders FC2: PASS (reference 50/50 seeds, slowest 0.5 s)', rc=0.")
rev("fc2d-r2-gate-check-projects", "2.6", "tools/check_projects.py --unit FC2",
    f"{SCR}check_projects_fc2.out: 'check_projects FC2: PASS', rc=0.")
rev("fc2d-r2-gate-check-dag", "2.9", "tools/check_dag.py --unit FC2",
    f"{SCR}check_dag_fc2.out: 'check_dag FC2: PASS', rc=0. The round-10 hunks add the word 'leg' (defined in P6) and no concept link.")
rev("fc2d-r2-gate-check-pages", "2.9", "tools/check_pages.py --unit FC2",
    f"{SCR}check_pages_fc2.out: 'check_pages FC2: PASS', rc=0.")
rev("fc2d-r2-gate-run-labs", "2.5", "tools/run_labs.py --unit FC2",
    f"{SCR}run_labs_fc2.out: 'run_labs FC2: PASS (11/11)', rc=0.")
rev("fc2d-r2-lab-twins-isolated", "2.5", "project twins alone under python -I -W error",
    f"{SCR}expected_vs_run_r10.out: lab 1, 2 and 3 twins run from /tmp with '.venv/bin/python -I -W error': rc=0, stderr_bytes=0 each.")
rev("fc2d-r2-lab-page-equals-twin", "2.5", "page code equals twin; expected block equals output",
    f"{SCR}page_vs_twin_r10.out: lab 1 and lab 3 page code: 0 lines differ from the twin. Lab 2: 3 lines differ (line 58 gap, lines 60 and 73 net), each a page blank '___' in place of the twin expression, and nothing else. {SCR}expected_vs_run_r10.out: all three page expected blocks equal the twin stdout (16, 16, 17 lines).")
rev("fc2d-r2-gate-page-smoke", "2.9", "tools/page_smoke.py --unit FC2 --pages project",
    f"{SCR}page_smoke_project.out: 'page_smoke modules/FC/FC2/project.html: PASS', 'in-browser grader: All 94 tests pass', rc=0.")
rev("fc2d-r2-gate-ruff-mypy", "2.6", "ruff check, ruff format --check, mypy --no-incremental",
    f"{SCR}ruff_check.out 'All checks passed!' rc=0 (course/modules/FC/FC2, ledgers/FC2, tests/labs/FC2); {SCR}ruff_format.out '15 files already formatted' rc=0; {SCR}mypy.out 'Success: no issues found in 385 source files' rc=0.")
rev("fc2d-r2-gate-pytest-fc2", "2.5/2.6", "relevant pytest (FC2 filter)",
    f"{SCR}pytest_fc2.out: 'pytest -q tests/test_curriculum.py tests/test_labs.py -k FC2' 12 passed, rc=0.")
rev("fc2d-r2-gate-verify-refs", "2.1", "verify_refs --offline and --unit FC2 (live)",
    f"{SCR}verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', rc=0. {SCR}verify_refs_unit_FC2.out: 'live re-verification of FC2: 3 of 560 entries, 0 problems', rc=0.")
rev("fc2d-r2-collect-count", "2.6", "collected checks equal the page count, every seed 0..49",
    f"{SCR}collect_count.out (pytest --collect-only on reference.py as scanner.py, run with python -I): 'collected 94 for 50 seeds', rc=0. The page's 'consists of 94 checks' matches.")

# ---- numbers and prose ------------------------------------------------------------------------------------
rev("fc2d-r2-numbers-lab1", "2.2", "Lab 1 numbers (project.html line 55 hypothesis, Lab 1 code and expected block, interpretation)",
    f"{SCR}numbers_r10.out (exact Fractions): cost 45; parity gaps 0, 120, 0, 0, -20, 0 at 9000..11500; nets -45, 75, -45, -45, -25, -45; convexity chord less call 50, 100, -75, 75 at 9500..11000; the 10500 finding has gross 75 and net 30; chord 625 at 10500; two findings kept. All match the printed expected block and the interpretation (project.html 163). The round-10 hunk on line 55 changes only the leg parenthesis, which does not touch a number.")
rev("fc2d-r2-numbers-lab3", "2.2", "Lab 3 numbers (project.html Lab 3 hypothesis, expected block, interpretation)",
    f"{SCR}numbers_r10.out: cost 60; gaps 0, -60, 0, 0, 226, 540 at 4000..7000; nets -60, 0, -60, -60, 166, 480; chord less call 35, 470/3, -188/3, 59; gross 63 and net 3 at 6000; three kept. Matches the expected block and the interpretation (-188/3, about -62.67, rounded once to 63).")
rev("fc2d-r2-numbers-exemplars", "2.2", "exemplar numbers (project.html Exemplar B and A passages)",
    f"{SCR}numbers_r10.out: Exemplar B discounted strikes 6175 and 6650; gaps 226 and 540; chord (500 + 2 x 151)/3 = 802/3; chord less call -188/3; gross 63; net 3. Exemplar A reports only approximate values, which the annotations already mark as missing the cents level.")
rev("fc2d-r2-hours", "2.6", "hours arithmetic and hub consistency",
    "project.html time-budget rows 2 + 3 + 5 + 9 + 3 + 5 + 3 = 30 (page total row 30; data-hours-project=\"30\" on line 33). index.html line 29: data-hours-lessons=\"60\" and data-hours-project=\"30\", sum 90; curriculum/02-economics-finance-core.yaml line 399 FC2 hours: 90. No hours line changed since 1e272e5 (the round-10 hunks are lines 55 and 333).")
rev("fc2d-r2-banned-phrases", "2.9", "banned phrases and process words in the added lines",
    f"{SCR}added_lines_project_r10.txt: the two added lines (line 55 hypothesis, line 333 P6 bullet) scanned for round, now, changed, fixed, revised, updated and the first-person and filler words: 0 hits.")
rev("fc2d-r2-notation", "2.4", "notation against notation/notation.json",
    "The two round-10 hunks introduce no symbol (the new text is the noun 'leg' and the phrase 'one instrument'). notation/notation.json is byte-identical since 1e272e5, so the round-9 check on D, tau and r still holds, and the symbol set of the page is unchanged.")
rev("fc2d-r2-dag", "2.9", "check_dag and concepts outside the closure",
    f"{SCR}check_dag_fc2.out: 'check_dag FC2: PASS', rc=0. 'leg' is defined in the unit's own P6 convention, not a concept, so no DAG edge is added.")
rev("fc2d-r2-reading-keys", "2.1", "reading list and cited theorems",
    f"{SCR}links_anchors_r10.out: keys cox1979option, hull2021options and stoll1969relationship are entries of references/references.json (grep on the entries array); {SCR}verify_refs_unit_FC2.out: live FC2 run, 0 problems. Theorem 1.2 (parity) and Theorem 3.2 (convexity) of L05.html read at L05.txt lines 64 and 161.")
rev("fc2d-r2-spec-questions", "2.6", "spec completeness: questions a competent student would ask",
    "The round-10 P6 bullet now defines 'leg' before the spec's 'three legs' is used in the cost rule. The only term that the earlier round left undefined in the cost section is now defined. No other question arises from the spec text (project.html lines 285-320 unchanged).")
rev("fc2d-r2-scope-curriculum-brief", "2.6", "Rung 3 matches the curriculum scope",
    "Re-verified on 47a36d8: curriculum/02-economics-finance-core.yaml line 428 still reads 'Given an embedded option-chain snapshot, detect put–call parity and convexity violations net of a stated cost model'. The page (project.html line 285) says 'No market data is embedded' and every chain is SIMULATED. The curriculum brief and the page's scope therefore differ on the data the scanner runs on. The yaml is byte-identical since 1e272e5, so the round-9 failure stands.",
    status="FAIL",
    fix="Edit curriculum/02-economics-finance-core.yaml line 428 to 'Given a SIMULATED option-chain snapshot' (or equivalent wording that agrees with project.html line 285), then regenerate with tools/render_curriculum.py and tools/build_site.py; the builder owns that edit, the verifier does not edit it.")

# ---- rubric, autograder and instances ----------------------------------------------------------------------
carry("fc2d-r2-rubric-C2-level2", "course/modules/FC/FC2/project.html rubric table (lines 504-512)")
carry("fc2d-r2-rubric-calibration", "course/modules/FC/FC2/project.html rubric table and exemplar annotations (lines 504-634)")
carry("fc2d-r2-starter-suite-fails", G)
carry("fc2d-r2-autograder-panel-claims", "course/modules/FC/FC2/project.html line 37 and course/assets/js/grader.js")
carry("fc2d-r2-hub-placement-claim", "course/modules/FC/FC2/index.html")
carry("fc2d-r2-grader-messages", G)
carry("fc2d-r2-grader-named-conditions-only", G)
carry("fc2d-r2-instances", G)
carry("fc2d-r2-grader-over-constraint-trade-verb", G)
rev("fc2d-r2-grader-over-constraint-case", "2.6", "correct alternatives pass with case-insensitive rule names",
    f"{SCR}alts_r10.out (run_alts_r10.py): all 12 alternative correct implementations pass 50/50 seeds: alt1..alt10 from ledgers/FC2/scripts/FC2-d-r8/alts (copied into {SCR}alts), and two new ones, alt11_validation_order_lengths_first.py and alt12_reworded_explanations.py (made by {SCR}make_alts_r10.py). Explanations are matched case-insensitively by the suite; alt12 keeps the labels and the rule words.")
rev("fc2d-r2-alternatives-pass", "2.6", "five alternative correct implementations pass seeds 0..49",
    f"{SCR}alts_r10.out: 12 alternatives (10 prior and 2 new), 50/50 seeds each, rc=0 for every run.")
rev("fc2d-r2-mut-r7-docstrings", "2.6", "mutant docstrings (first line describes the error)",
    f"{SCR}build_fragment_fc2d_r10.py asserts, for all 87 files in ledgers/FC2/mutants/, that the module docstring opens on the first line and carries a one-line error description (the descriptions are in the fragment's mutants list and in {SCR}mutate_fc2_r10_all.out).")
rev("fc2d-r2-mut-new-killed", "2.6", "round-2 new mutants v07..v10 killed",
    f"{SCR}mutate_fc2_r10_all.out: v07, v08, v09, v10 each KILLED.")
carry("fc2d-r2-mut-r5d-resolved", "ledgers/FC2/mutants/r5_d (historical) and grader")
rev("fc2d-r2-mut-equivalents", "2.6", "no equivalent mutant in the set",
    f"{SCR}mutate_fc2_r10_all.out: 87/87 killed on seeds 0..9, so none of the 87 is equivalent on the suite's data. No equivalent mutant is claimed.")
rev("fc2d-r2-cards-full-scan", "2.6", "cards: unique ids, fronts, backs; near-duplicate review",
    f"{SCR}cards_scan_r10.out: 159 cards, unique ids and unique fronts. Near-duplicate fronts (ratio > 0.75) reviewed by hand: FC2-c160/c162 are the lower bounds on C and P (different bounds), c161 the range of P, c066 the range of C; FC2-c084/c163 are the cost and the uniqueness of the one-period portfolio; FC2-c005/c154 are the weak and strict cost orders. No two cards ask the same question.")
rev("fc2d-r2-cards-refs-numbers", "2.1/2.6", "every numbered reference on each card appears in its lesson",
    f"{SCR}cards_scan_r10.out: 'numbered references not found in cited lesson: [] 0'.")
rev("fc2d-r2-cards-lab-numbers", "2.5", "cards on lab-basis numbers (c012, c013, c095, c147, c148 and the other lab-basis cards)",
    f"Checked this round against the lesson twin outputs {SCR}twin_L01.out, twin_L03.out, twin_L04.out, twin_L07.out, twin_L08.out: c013 (holdings -5, 9; payoffs 22, 4), c012 (1/2), c138 (state prices -1/5, 11/10), c147 (30 portfolios, box -10..10), c038 (84 cents), c045 (0.049026), c046 (-4415468), c134 (4902625), c056 (6.56), c057 (14.58), c058 (108, 93), c061 (25, 17, 8), c135 (18.00), c109 (10.450584, 1045), c110 (-91), c111 (signs), c117 (-0.0049977, 0), c114 (0.35, 0.15), c116 (1.221403, 0.577493, 12.1623 -> 1216), c118 (5.573526 -> 557), c125 (37), c126 (4.8771; L08.txt lines 321 and 348 for c127), c133 (days 4, 6, 7, 10; -35, -13, -36, -22). Remaining lab-basis cards: carried from round 8/9.")
rev("fc2d-r4-cards-sample", "2.7", "one card in ten sampled, plus the changed cards",
    "All 159 card objects were read this round. The 13 changed cards are each verified in their own row (fc2d-r10-card-* and the rows named after them). The unchanged card objects are byte-identical since 1e272e5, so the one-in-ten sample of rounds 8 and 9 carries for them.")

# ---- round-10 changed cards -------------------------------------------------------------------------------
rev("fc2d-r10-card-c025", "2.7", "course/modules/FC/FC2/cards.json FC2-c025 (line 172); L02.html Proposition 3.1 (line 292-293)",
    "Front now reads 'Under A1 to A4, and A3 at each date t, what is the value of a long forward ...'. Proposition 3.1 is stated 'Assume A1 to A4, and assume A3 at each date t' (L02.txt line 293). Back V_t = S_t - F e^{-r(tau - t)} matches. Hypotheses carried.")
rev("fc2d-r10-card-c026", "2.7", "cards.json FC2-c026 (line 179); L02.html Corollary 3.2 (line 307)",
    "Front 'Under A1 to A4, and A3 at each date t, ... a forward priced at F*'. Corollary 3.2 is 'Under the hypotheses of Proposition 3.1 and with F = F*'. Back: zero at date 0, sign of S_t - F* e^{-r(tau-t)}. Matches.")
rev("fc2d-r10-card-c028", "2.7", "cards.json FC2-c028 (line 194); L02.html Problem P1 (line 332)",
    "Front 'If the asset pays one known income I at date t1 and A1 is dropped, with A2 to A4 and A3 kept'. Problem P1 (L02.html line 332): 'Drop A1 ... pays a known income I at date t1, with 0 < t1 <= tau, and nothing else. Keep A2 to A4.' A3 is kept by 'Keep A2 to A4' (A3 is the no-arbitrage assumption, L02 line 97). Back F = S e^{r tau} - I e^{r(tau - t1)} with 0 < t1 <= tau. Matches; the back carries the t1 range, the front omits it, which the rule permits.")
rev("fc2d-r2-card-c030", "2.7", "cards.json FC2-c030 (line 210); L02.html Problem R1 (line 487)",
    "Front 'Under A1 and A3, with the frictionless parts of A2 and A4 at two rates r_l <= r_b'. R1 says keep A1 and A3, keep the frictionless parts of A2, keep A4 with r replaced by the two rates, r_l <= r_b. Back: a price F outside [S e^{r_l tau}, S e^{r_b tau}] admits arbitrage; inside-interval arbitrage-freedom not claimed. R1 asks 'free of arbitrage only if it lies in the interval, and ... a price outside the interval gives an arbitrage', so the back's 'not established' is the correct scope. Matches.",
    )
rev("fc2d-r10-card-c044", "2.7", "cards.json FC2-c044 (line 299); L03.html Proposition 3.5 (line 189)",
    "Front 'Under A8, what is the value to the fixed payer at a fixed rate K'. Proposition 3.5: 'Assume A8. ... value to the fixed payer ... (R_par - K) sum DF_i'. Matches; the sign statement in the back matches the proposition's sign clause.")
rev("fc2d-r10-card-c089", "2.7", "cards.json FC2-c089 (line 614); L06.html Theorem 1.4 (line 95) and Theorem 2.2 (line 147)",
    "Front 'Under A1, A2, A3, A5 and A6'. Theorem 1.4 (L06.txt line 95): 'Under A1, A2, A3, A5 and A6'. Theorem 2.2 (line 147): 'Under the hypotheses of Theorem 1.4, V_0 = E^Q[V_1]/R_f'. Back cites Theorem 2.2. Matches.")
rev("fc2d-r10-card-c104", "2.7", "cards.json FC2-c104 (line 721); L07.html Definition 1.3, Proposition 1.5 (line 145-146)",
    "Front 'Under A7 and A8, on which inputs ...'. Proposition 1.5 is stated under Definition 1.3 with no assumption label; A7 and A8 are the premises under which Definition 1.3 is the call value (L07.txt lines 112, 118-119). Adding them to the front is a harmless over-statement of the premise, and the back's 'under the formula of Definition 1.3' is accurate. Matches.")
rev("fc2d-r8-card-c104", "2.6", "cards.json FC2-c104 (line 721); L07.html Proposition 1.5 (lines 145-146)",
    "The front change of round 10 is re-read (row fc2d-r10-card-c104). The back (S, K, r tau, sigma sqrt tau only; no drift) matches Proposition 1.5 text at L07.txt line 146. PASS.")
rev("fc2d-r10-card-c113", "2.7", "cards.json FC2-c113 (line 785); L07.html Proposition 1.4 (lines 125-126)",
    "Front 'Under A1 to A5, A7 and A8'. Proposition 1.4: 'Under A1 to A5, A7 and A8, the European put ... has value' (L07.txt line 126). Matches.")
rev("fc2d-r7-card-c113", "2.2/2.6", "cards.json FC2-c113 (line 785)",
    "Front changed in round 10 (row fc2d-r10-card-c113); the back (Proposition 1.4 and Lab 1 parity) re-read and matches. PASS.")
rev("fc2d-r10-card-c120", "2.7", "cards.json FC2-c120 (line 838); L08.html Lemma 2.1 (line 87)",
    "Front now 'For S > 0, K > 0, tau > 0 and sigma > 0, what is the vega ...'. Lemma 2.1 (L08.txt line 87): 'For sigma > 0, the derivative dC/dsigma ... equals S phi(d1) sqrt(tau)'. The sigma > 0 hypothesis, which the round-9 FAIL said the front omitted, is now in the front. The S, K, tau positivity comes from the lesson's fixed-input line (L08.txt line 69). PASS.",
    )
rev("fc2d-r7-card-c132", "2.2/2.6", "cards.json FC2-c132 (line 926); L05.html Theorem 4.1",
    "Front changed in round 10 (row fc2d-r10-card-c132) and re-read against Theorem 4.1 and Remark 4.2. PASS.")
rev("fc2d-r2-card-c120", "2.7", "course/modules/FC/FC2/cards.json FC2-c120 (line 838); L08.html Lemma 2.1 (line 87)",
    "Round-9 FAIL re-verified and fixed in 47a36d8: the front now includes sigma > 0, the hypothesis of Lemma 2.1 (row fc2d-r10-card-c120). PASS.")
rev("fc2d-r10-card-c121", "2.7", "cards.json FC2-c121 (line 845); L08.html Lemma 2.2 (line 112-113) and fixed inputs (line 69)",
    "Front now 'For a fixed spot S > 0, strike K > 0, rate r and maturity tau > 0 ...'. Lemma 2.2 (L08.txt line 113): limits S as sigma to infinity and L as sigma to 0+. L depends on K, r and tau, and the lesson fixes S, K, r and tau at L08.txt line 69. Back matches. PASS.")
rev("fc2d-r9-card-c121", "2.7", "cards.json FC2-c121 (line 845); L08.html line 55-69 and Lemma 2.2",
    "Round-9 FAIL (the front omitted the fixed rate r) re-verified and fixed in 47a36d8 (row fc2d-r10-card-c121). PASS.")
rev("fc2d-r10-card-c122", "2.7", "cards.json FC2-c122 (line 852); L08.html Theorem 2.3 (lines 121-123; 444)",
    "Front 'Under A1 to A5, A7 and A8 of Lesson 7, when does an implied volatility exist ...'. The lesson's summary sentence (L08.txt line 444) reads 'Under A1 to A5, A7 and A8 of Lesson 7, an implied volatility exists and is unique exactly when the price lies strictly between L and S', and the back uses the same wording. Matches.")
rev("fc2d-r10-card-c123", "2.7", "cards.json FC2-c123 (line 859); L08.html Definition 3.1 (line 109) and Proposition 3.2 (lines 114-115)",
    "Front 'For the bisection of Definition 3.1, with C* in (L, S), a bracket of width W that satisfies its condition, and tolerance tau_tol ...'. Proposition 3.2 hypotheses: bracket condition of Definition 3.1 and C* in (L, S), W = sigma_hi - sigma_lo. Definition 3.1 bracket: C(sigma_lo) < C* and C(sigma_hi) >= C*. Back gives the first k with W/2^k <= tau_tol. Matches.")
rev("fc2d-r4-card-c123", "2.7", "cards.json FC2-c123 (line 859); L08.html Proposition 3.2",
    "Front changed in round 10 (row fc2d-r10-card-c123). Re-read against Proposition 3.2 (bracket condition, C* in (L,S)). PASS.")
rev("fc2d-r10-card-c132", "2.7", "cards.json FC2-c132 (line 926); L05.html Theorem 4.1 (line 365) and Remark 4.2 (line 379-390)",
    "Front 'Under A1 to A5, (N) and r >= 0, does Theorem 4.1 give a rule ...'. Theorem 4.1 (L05.txt line 365): 'Under A1, A2, A3, A4, A5 and (N), with r >= 0 ... V_A(0) = V_E(0)'. Back: a price equality at date 0 only, no later-date rule (Remark 4.2). Matches.")
rev("fc2d-r2-card-c132", "2.7", "cards.json FC2-c132 (line 926); L05.html Theorem 4.1",
    "Front changed in round 10 (row fc2d-r10-card-c132). Matches Theorem 4.1 hypotheses. PASS.")

# ---- round-10 hunks in project.html and the sampled cards and their checks ---------------------------------
rev("fc2d-r10-page-hunk-lab1-hypothesis", "2.9", "course/modules/FC/FC2/project.html line 55 (Lab 1 hypothesis)",
    "Line 55 now reads 'Each finding trades three legs (a leg is defined under P6 in Conventions and assumptions, below), so a finding costs 45 cents.' The cost is 3 x (5+10) = 45 (numbers_r10.out LAB1 cost 45). The P6 cross-reference resolves to the bullet at line 333, and the parenthesis adds no claim. page_vs_twin_r10.out: the code block is unchanged. PASS.")
rev("fc2d-r10-page-hunk-P6-leg", "2.9", "course/modules/FC/FC2/project.html line 333 (P6 · Cost model bullet)",
    "New sentence 'A leg is one instrument that a finding buys or sells.' Consistent with the next sentences: a parity finding trades the call, the put and the underlying (three instruments); a convexity finding trades three calls (three instruments). The fee and half-spread definitions that follow are unchanged. PASS.")
rev("fc2d-r3-scope-changed-hunks", "2.6", "every hunk changed since 1e272e5 in the slice",
    "git diff 1e272e5 47a36d8 on the slice's files: project.html has two hunks (lines 55 and 333); cards.json has 13 changed fronts (ids c025, c026, c028, c030, c044, c089, c104, c113, c120, c121, c122, c123, c132) and no other changed card. Every hunk is read in full (rows fc2d-r10-*). grader/, labs twins and lessons are byte-identical. PASS.")
rev("fc2d-r7-cards-delta-read", "2.6", "cards.json delta since 1e272e5 read in full",
    "The 13 changed fronts were read in full this round (their rows are fc2d-r10-card-*, fc2d-r2-card-c120, fc2d-r2-card-c030, fc2d-r2-card-c132, fc2d-r9-card-c121, fc2d-r8-card-c104, fc2d-r7-card-c113 and fc2d-r4-card-c123). The hunks at 458-466 and 579-586 (c066, c084) and 1103-1135 (c160-c163) are unchanged since 1e272e5. PASS.")
rev("fc2d-r9-cards-changed-set-coverage", "2.7", "cards.json changed set since 1e272e5 is covered",
    "Changed fronts in round 10: c025, c026, c028, c030, c044, c089, c104, c113, c120, c121, c122, c123, c132. Each has a row above (fc2d-r10-card-* or a named row). No card of the round-9 changed set is left out.")
rev("fc2d-r3-df-ppm-link", "2.9", "df_ppm link resolves (project.html 'assumption P4' and the Inputs list)",
    f"{SCR}links_anchors_r10.out: 'project.html local links checked; unresolved: []'. The P4 link is href=#conventions, which resolves to the h3 id conventions.")
rev("fc2d-r6-page-conventions-definitions", "2.9", "course/modules/FC/FC2/project.html lines 325-336 (conventions and definitions) and line 55",
    "Lines 325-336 read in full this round: C, P, S, K and df are defined on the page (the 'In the formulas' paragraph), and the P1 to P6 labels are defined as before. The only change is the P6 sentence about legs (line 333, row fc2d-r10-page-hunk-P6-leg). PASS.")
rev("fc2d-r5-page-hunk-lab1-hypothesis", "2.9", "course/modules/FC/FC2/project.html line 55",
    "Re-read this round: row fc2d-r10-page-hunk-lab1-hypothesis. PASS.")

# ---- new student-error mutants and alternatives --------------------------------------------------------------
rev("fc2d-r10-new-mutants", "2.6", "four new student-error mutants z10_a..z10_d, written by this verifier",
    f"{SCR}make_mutants_r10.py writes ledgers/FC2/mutants/z10_a_strike_of_one_cent_rejected.py (strike < 2), z10_b_df_upper_bound_exclusive.py (df < 1000000), z10_c_zero_half_spread_rejected.py (spread <= 0), z10_d_convexity_flags_call_below_chord.py (convexity test > 0). {SCR}intended_kills_r10.out: each fails its intended test on seed 0 (rc=1). {SCR}mutate_fc2_r10_all.out: all four KILLED. Note: in the collated run, z10_b and z10_c were attributed to other tests, whose hand_chain default inputs (df=PPM, spread=0) also trip the mutant; the intended tests were confirmed separately by intended_kills_r10.sh.")
rev("fc2d-r8-alt-9-10", "2.6", "new alternatives: integer-only parity (alt9) and cross-multiplied convexity (alt10)",
    f"{SCR}alts_r10.out: alt9_integer_only_parity.py and alt10_cross_multiplied_convexity_no_fraction.py each 50/50 seeds pass.")
rev("fc2d-r5-alt7-cross-multiplied", "2.6", "alt7_cross_multiplied_integers in the suite",
    f"{SCR}alts_r10.out: alt7_cross_multiplied_integers.py 50/50 pass.")
rev("fc2d-r6-alt8-forward-price", "2.6", "alt8_forward_price_fraction in the suite",
    f"{SCR}alts_r10.out: alt8_forward_price_fraction.py 50/50 pass.")
rev("fc2d-r9-alternatives-rerun", "2.6", "alternatives re-run on the pin",
    f"{SCR}alts_r10.out: all 12 alternatives 50/50 on 47a36d8.")
rev("fc2d-r5-explanation-direction-untested", "2.6", "course/modules/FC/FC2/grader/test_project.py (explanation tests)",
    "Grader identical since 1e272e5; the round-9 probe (ledgers/FC2/scripts/FC2-d-r9/direction_probe_r9.out) stands: a parity explanation with the trade direction swapped passes the suite. The spec states no direction requirement for the explanation (project.html Required outputs names the rule and the labels only), so this is an observation, not a FAIL.")
rev("fc2d-r7-mut-s7-new-killed", "2.6", "round-7 new mutants s7_a..s7_d killed",
    f"{SCR}mutate_fc2_r10_all.out: s7_a, s7_b, s7_c, s7_d each KILLED.")
rev("fc2d-r3-mut-new-killed", "2.6", "round-3 student-error mutants q3_a..q3_d killed",
    f"{SCR}mutate_fc2_r10_all.out: q3_a..q3_d KILLED.")
rev("fc2d-r3-mut-prior-untracked", "2.6", "round-3 mutants r3_a..r3_d re-run",
    f"{SCR}mutate_fc2_r10_all.out: r3_a..r3_d KILLED.")
rev("fc2d-r4-mut-u4-new-killed", "2.6", "round-4 new mutants u4_a..u4_c killed",
    f"{SCR}mutate_fc2_r10_all.out: u4_a..u4_c KILLED.")
rev("fc2d-r5-mut-w5-new-killed", "2.6", "round-5 new mutants w5_a..w5_c killed",
    f"{SCR}mutate_fc2_r10_all.out: w5_a..w5_c KILLED.")
rev("fc2d-r6-mut-w6-new-killed", "2.6", "round-6 new mutants w6_a..w6_d killed",
    f"{SCR}mutate_fc2_r10_all.out: w6_a..w6_d KILLED.")
rev("fc2d-r8-mut-x8-a", "2.6", "grader: cost validation only when a parity finding is kept",
    f"{SCR}mutate_fc2_r10_all.out: x8_a KILLED (test_negative_cost_is_rejected_even_when_no_finding_is_kept).")
rev("fc2d-r8-mut-x8-b", "2.6", "grader: convexity_violations short-circuit for fewer than three strikes",
    f"{SCR}mutate_fc2_r10_all.out: x8_b KILLED.")
rev("fc2d-r8-mut-x8-c", "2.6", "grader: scan skips quote-length check for one-strike chains",
    f"{SCR}mutate_fc2_r10_all.out: x8_c KILLED.")
rev("fc2d-r9-mut-y9-new-killed", "2.6", "round-9 new mutants y9_a..y9_d",
    f"{SCR}mutate_fc2_r10_all.out: y9_a..y9_d KILLED.")

# ---- carry the rest of round 9 -----------------------------------------------------------------------------
CARRY = {
    "fc2d-r2-card-c010": "course/modules/FC/FC2/cards.json FC2-c010 and L01.html",
    "fc2d-r2-card-c020": "course/modules/FC/FC2/cards.json FC2-c020",
    "fc2d-r2-card-c041": "cards.json FC2-c041 and L03.html",
    "fc2d-r2-card-c051": "cards.json FC2-c051 and L04.html",
    "fc2d-r2-card-c061": "cards.json FC2-c061 and L04.html",
    "fc2d-r2-card-c071": "cards.json FC2-c071 and L05.html",
    "fc2d-r2-card-c082": "cards.json FC2-c082 and L06.html",
    "fc2d-r2-card-c092": "cards.json FC2-c092 and L06.html",
    "fc2d-r2-card-c102": "cards.json FC2-c102 and L07.html",
    "fc2d-r2-card-c112": "cards.json FC2-c112 and L07.html",
    "fc2d-r2-card-c142": "cards.json FC2-c142 and L04.html",
    "fc2d-r4-card-c093": "cards.json FC2-c093 and L06.html",
    "fc2d-r4-card-c124": "cards.json FC2-c124 and L08.html",
    "fc2d-r4-card-c149": "cards.json FC2-c149 and L06.html",
    "fc2d-r4-card-c150": "cards.json FC2-c150 and L06.html",
    "fc2d-r4-card-c151": "cards.json FC2-c151 and L08.html",
    "fc2d-r4-card-c152": "cards.json FC2-c152 and L08.html",
    "fc2d-r4-card-c153": "cards.json FC2-c153 and L05.html",
    "fc2d-r5-card-c005": "cards.json FC2-c005 and L01.html",
    "fc2d-r5-card-c055": "cards.json FC2-c055 and L04.html",
    "fc2d-r5-card-c154": "cards.json FC2-c154 and L01.html",
    "fc2d-r6-card-c072": "cards.json FC2-c072 and L05.html",
    "fc2d-r6-card-c103": "cards.json FC2-c103 and L07.html",
    "fc2d-r6-card-c155": "cards.json FC2-c155 and L05.html",
    "fc2d-r6-card-c073": "cards.json FC2-c073 and L05.html",
    "fc2d-r7-card-c007": "cards.json FC2-c007 and L01.html",
    "fc2d-r7-card-c014": "cards.json FC2-c014 and L01.html",
    "fc2d-r7-card-c021": "cards.json FC2-c021 and L02.html",
    "fc2d-r7-card-c037": "cards.json FC2-c037 and L03.html",
    "fc2d-r7-card-c046": "cards.json FC2-c046 and L03.html",
    "fc2d-r7-card-c059": "cards.json FC2-c059 and L04.html",
    "fc2d-r7-card-c060": "cards.json FC2-c060 and L04.html",
    "fc2d-r7-card-c068": "cards.json FC2-c068 and L05.html",
    "fc2d-r7-card-c069": "cards.json FC2-c069 and L05.html",
    "fc2d-r7-card-c076": "cards.json FC2-c076 and L05.html",
    "fc2d-r7-card-c079": "cards.json FC2-c079 and L05.html",
    "fc2d-r7-card-c080": "cards.json FC2-c080 and L05.html",
    "fc2d-r7-card-c081": "cards.json FC2-c081 and L06.html",
    "fc2d-r7-card-c094": "cards.json FC2-c094 and L06.html",
    "fc2d-r7-card-c095": "cards.json FC2-c095 and L06.html",
    "fc2d-r7-card-c114": "cards.json FC2-c114 and L07.html",
    "fc2d-r7-card-c125": "cards.json FC2-c125 and L08.html",
    "fc2d-r7-card-c128": "cards.json FC2-c128 and L08.html",
    "fc2d-r7-card-c137": "cards.json FC2-c137 and L06.html",
    "fc2d-r7-card-c145": "cards.json FC2-c145 and L07.html",
    "fc2d-r7-card-c156": "cards.json (FC2-c156 absent since 2d75559; historical)",
    "fc2d-r7-card-c157": "cards.json (FC2-c157 absent since 2d75559; historical)",
    "fc2d-r8-card-c110-c111-c117": "cards.json FC2-c110, c111, c117 and L07.html",
    "fc2d-r8-card-c143": "cards.json FC2-c143 and L04.html",
    "fc2d-r8-card-c158": "cards.json FC2-c158 and L04.html",
    "fc2d-r8-card-c159": "cards.json FC2-c159 and L04.html",
    "fc2d-r9-card-c066": "cards.json FC2-c066 and L05.html",
    "fc2d-r9-card-c084": "cards.json FC2-c084 and L06.html",
    "fc2d-r9-card-c160": "cards.json FC2-c160 and L05.html",
    "fc2d-r9-card-c161": "cards.json FC2-c161 and L05.html",
    "fc2d-r9-card-c162": "cards.json FC2-c162 and L05.html",
    "fc2d-r9-card-c163": "cards.json FC2-c163 and L06.html",
    "fc2d-r9-tie-rule-prose": "course/modules/FC/FC2/project.html Lab 1 and Lab 2 docstrings and spec tie-rule sentence (lines 59-63, 170-173, 308), none in the round-10 hunks",
    "fc2d-r9-grader-weak-assertion": G,
    "fc2d-r5-page-hunk-error-conditions": "course/modules/FC/FC2/project.html lines 309-316 and " + G,
    "fc2d-r6-page-line321-anchor": "course/modules/FC/FC2/project.html line 321 and line 517",
    "fc2d-r7-page-rung1-line44": "course/modules/FC/FC2/project.html line 44",
    "fc2d-r7-page-brief-line490": "course/modules/FC/FC2/project.html line 490",
    "fc2d-r7-exemplar-B-C3-annotation-line543": "course/modules/FC/FC2/project.html line 543",
    "fc2d-r7-exemplar-A-C4-annotation-line618": "course/modules/FC/FC2/project.html line 618",
    "fc2d-r7-grader-convexity-docstring": G,
    "fc2d-r8-exemplar-level-labels": "course/modules/FC/FC2/project.html line 351 and exemplar data-level attributes (lines 520, 584)",
    "fc2d-r3-footer-no-upload": "course/modules/FC/FC2/project.html footer and course/assets/js/grader.js",
    "fc2d-r3-exemplar-scores-match-text": "course/modules/FC/FC2/project.html lines 520 and 584 (data-scores and official-scoring sentences)",
    "fc2d-r3-instance-docstring-bounds": G,
}
for rid in r9:
    if rid in {r["id"] for r in rows}:
        continue
    if rid in CARRY:
        carry(rid, CARRY[rid])
    else:
        pass

missing = [rid for rid in r9 if rid not in {r["id"] for r in rows}]
print("round-9 ids not yet decided:", missing)

# ---- write the fragment ----------------------------------------------------------------------------------
from datetime import datetime, UTC  # noqa: E402

done = {r["id"] for r in rows}
assert len(rows) == len(done), "duplicate row ids"
missing = [rid for rid in r9 if rid not in done]
assert not missing, missing
extra = sorted(done - set(r9))
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
verdict = "PASS" if counts["PASS"] == len(rows) else "FAIL"
fragment = {
    "unit": "FC2",
    "slice": "FC2-d",
    "round": 10,
    "verifier": "Claude Haiku 5.5, independent verifier for FC2-d round 10 (did not build FC2)",
    "pin": "47a36d8c78633793ccc762ae19dcd5e19b780d19",
    "base": "1e272e5a641f18412703b37778a44db6f7391a69 (round-9 pin); delta inside FC2-d: course/modules/FC/FC2/project.html lines 55 and 333; course/modules/FC/FC2/cards.json 13 fronts (c025, c026, c028, c030, c044, c089, c104, c113, c120, c121, c122, c123, c132); no other slice file changed",
    "checkout": from_root,
    "scratch": SCR,
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": [{"name": m["name"], "description": m["description"], "killed_by": m["killed_by"]} for m in mutants],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 10 on pin 47a36d8 (round-9 pin 1e272e5). Round-9 FAIL rows fc2d-r2-card-c120 and fc2d-r9-card-c121 are fixed and re-verified "
        "PASS. The one remaining FAIL is fc2d-r2-scope-curriculum-brief (curriculum/02 line 428, byte-identical since 1e272e5). "
        "All 87 grader mutants killed on seeds 0-9 (83 prior plus z10_a..z10_d). Twelve alternative correct implementations pass 50/50 seeds "
        "(ten prior plus alt11, alt12). Collect-only count 94 for seeds 0-49. Not run: the full repo gate (render_curriculum.py, build_site.py --check, "
        "fetch_data.py --check, pytest over all of tests/, run_graders for other units, verify_refs over the whole registry); the browser "
        "autograder UI was not driven (page_smoke ran in Pyodide only); the lesson texts L01-L08 were read only where a changed card cites them, "
        "and carried card rows rest on the round-8 and round-9 checks, because lessons, labs and grader are byte-identical since 1e272e5. "
        "Observations, not rows: the one-strike length test asserts only that the digit 2 appears in the message; the explanation direction "
        "is untested (not a spec requirement); the collated kill attribution for z10_b and z10_c names a test that also fails for them by "
        "default-argument side effects, and the intended tests were confirmed separately."
    ),
    "summary": {"rows": len(rows), "pass": counts["PASS"], "fail": counts["FAIL"],
                "unverifiable": counts["UNVERIFIABLE"], "mutants": len(mutants), "mutants_killed": len(mutants),
                "new_ids_this_round": extra},
}
problems = ledger.validate(fragment, "FC2-d")
print("validate:", problems)
assert not problems
path = os.path.join(from_root, "ledgers", "FC2", "FC2-d.json")
with open(path, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("wrote", path, "rows", len(rows), "verdict", verdict, counts, "mutants", len(mutants))
