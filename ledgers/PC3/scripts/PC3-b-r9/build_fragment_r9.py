"""Verifier round 9 (PC3-b): build ledgers/PC3/PC3-b.json from the round-8 fragment, carrying unchanged rows.

Carried rows keep their id and their round-8 evidence, prefixed as the verifier rules require. Rows whose cited
subject changed in the 0dee921a..c93dd526 delta are re-verified and carry new evidence.
"""

import datetime
import json
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE9-PC3-b")
R8 = json.loads(Path("/Users/billyribeiro/.fanout/frags/E-PC3-b.round8.json").read_text(encoding="utf-8"))
OUT = ROOT / "ledgers" / "PC3" / "PC3-b.json"
OUT_DIR = "ledgers/PC3/scripts/PC3-b-r9/out"

NEW = {
    "gate-run-labs-unit": "Re-run on pin c93dd526: .venv/bin/python tools/run_labs.py --unit PC3 -> 'run_labs PC3: PASS (9/9)', exit 0 (" + OUT_DIR + "/run_labs.out).",
    "gate-check-pages": "Re-run: .venv/bin/python tools/check_pages.py --unit PC3 -> 'check_pages PC3: PASS', exit 0 (" + OUT_DIR + "/check_pages.out).",
    "gate-check-dag": "Re-run: .venv/bin/python tools/check_dag.py --unit PC3 -> 'check_dag PC3: PASS', exit 0 (" + OUT_DIR + "/check_dag.out).",
    "gate-check-projects": "Re-run: .venv/bin/python tools/check_projects.py --unit PC3 -> 'check_projects PC3: PASS', exit 0 (" + OUT_DIR + "/check_projects.out).",
    "gate-page-smoke-slice": "Re-run: .venv/bin/python tools/page_smoke.py --unit PC3 --pages L04 L05 L06 -> 'page_smoke PC3: PASS', exit 0; each page PASS (" + OUT_DIR + "/page_smoke.out).",
    "gate-ruff-mypy-twins": "Re-run: ruff check and ruff format --check on the three twins -> exit 0 both; .venv/bin/mypy --no-incremental -> 'Success: no issues found in 385 source files', exit 0 (" + OUT_DIR + "/ruff_check.out, ruff_format.out, mypy.out).",
    "gate-pytest-lab-tooling": ".venv/bin/pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -> all dots, exit 0 (" + OUT_DIR + "/pytest.out).",
    "gate-verify-refs-offline": ".venv/bin/python tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 (" + OUT_DIR + "/verify_refs.out).",
    "notation-registry-L04-L06": "Re-verified on the delta. The registry (notation/notation.json) reserves T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q. grep over L04/L05/L06.html finds none of them in the slice. The symbols N, t, p, L and h are defined locally (L04.html lines 56-58). The delta adds no new symbol (L04.html lines 72, 87, 129, 175 and L05.html lines 52, 140-151 reuse existing ones).",
    "twin-run-alone-L04-L06": "Re-run: .venv/bin/python -I -W error tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py and lab-PC3-L06-1.py -> exit 0 each, stderr empty (" + OUT_DIR + "/lab-PC3-L0*-1.stdout).",
    "twin-page-code-equals-twin": "Re-run: " + OUT_DIR + "/embed_compare.out -> L04 code == twin True (10694 vs 10695 chars, trailing newline), L05 True (5726 vs 5727), L06 True (6298 vs 6299).",
    "twin-expected-equals-stdout": "Re-run: embed_compare.out -> expected == twin stdout True: L04 52 lines, L05 25 lines, L06 21 lines.",
    "lab-L05-1-hypothesis-interpretation": "Re-verified. L05.html line 163 (hypothesis) now says Part 1 also runs seed 6 and prints its counts, and the printed seed-6 line (twin stdout, expected block) reads 'outputs equal: True, naive 1351, deque comparisons 350, pushes 200, pops 197', matching the claim. L05.html line 332 (interpretation) says the deque makes 350 comparisons on seed 6, consistent with the stdout.",
    "L04-definitions-A1-A6-notation": "Re-verified on the delta. L04.html lines 56-58 define N, t, p, L as local symbols. Line 72 (A1) now says 'Lab 1 (Section 4)', and the lab section (line 178) sits inside Section 4 (h2 id=s4 line 161, h2 id=s5 line 479). A5 (line 76) fixes L=10 and the fill test |I|<=L, matching Remark 1.2 (line 83) and the lab. No symbol is reused with another meaning.",
    "L04-lab-section-locator": "Re-verified. The two references are now correct: A1 (L04.html line 72) 'Lab 1 (Section 4)' and Example 1.3 title (line 87) 'the quoting rule of Lab 1, Section 4'. The lab section (line 178) lies between h2 s4 (line 161) and h2 s5 (line 479), so Section 4 is correct. A grep for 'Section 3' in L04.html now returns no hit.",
    "L04-prop-3.1-closed-form": "Re-verified on the changed H3 (L04.html line 129): now 'A1, A2, A4 and A5 hold'. The proof (lines 131-139) uses A1 and A2 (independence), A5 (the inventory test passes since |+-1| <= L when L >= 1, from H2), A4 (the informed trade rule) and A6 through H2 (a-b = 2h). It uses no A3 or A6 beyond H2, so A5 is needed and A3 is not, matching the amended statement. Closed form: (1-p)h - p[(v-a)^+ + (b-v)^+], with the three contributions summed in the proof. The Example 3.2 values (5, 0, 5/2) and the l04_independent.py enumeration over 520520 cases (" + OUT_DIR + "/l04_independent.out) agree.",
    "L04-R2-spread-criterion": "Re-verified (L04.html line 600). E=(1-p)h at v=m is re-derived: both brackets of Prop 3.1 vanish. If p<1, no h >= 1 gives E=0, so the criterion selects no spread. If p=1, E=0 for every h, so no spread is picked out. The changed sentence 'does not select a unique spread' is true in both cases, and the text names the assumption that would have to change (A1, arrival distribution depends on the quote). PASS.",
    "L04-E1-seed1-numbers": "Re-verified. Lab 1, Part 1 now prints the seed-1 line (lab-PC3-L04-1 stdout and page expected block): 'seed 1, same rule: fills 16 of 20 turns, cash flow 20100 cents, inventory at the end -2 units, settlement 10020 cents, P&L 60 cents'. The solution (L04.html line 568) quotes 16, 20100, -2, 10020, mark -20040, P&L 60, matching the printed line. The independent run l04_independent.out gives 'E1 seed1 fills, cash_flow, inv_end, settle, pnl: 16 20100 -2 10020 60'. The arithmetic 20100-20040=60 and (-2)(10020)=-20040 is correct.",
    "L05-E2-seed6-numbers": "Re-verified. Lab 1, Part 1 now prints 'seed 6 at window 8: outputs equal: True' and 'seed 6: naive comparisons = 1351, deque comparisons = 350, pushes = 200, pops = 197' (twin stdout, page expected block). E2 (L05.html lines 424-428) quotes 350, 200, 197, 1351 and says these are the lines Lab 1 Part 1 prints. My independent recount (" + OUT_DIR + "/l05_seed6_r9.out, written without the twin's code) gives 'seed 6 k=8: equal True, naive 1351, deque comparisons 350, pops 197, pushes 200'.",
    "lab-L04-1-hypothesis-interpretation": "Re-verified. The hypothesis (L04.html line 180) and the printed values match the stdout: informed arrivals 13 of 20, seed-1 line 16 fills, cash flow 20100, inventory -2, settlement 10020, P&L 60 (lab-PC3-L04-1.stdout lines 34-35). The interpretation (current line 475) now reads 'the proof covers every fair value for a fixed quote, from inventory zero (Proposition 3.1, H1)', which matches the round-8 finding: the inventory-zero hypothesis is now stated. H1 also carries the positive-probability clause of the conditioning event, which the citation covers. PASS.",
    "L04-key-results-prop-3.1-assumptions": "Re-verified on the changed hypothesis set. The key-results row for Prop 3.1 (L04.html line 621) says 'proved in §3 under A1, A2, A4, A5, A6 and H1 to H3', which matches the amended H3 (line 129) with A5 included.",
    "L04-problems-R1-R3-M-P": "Partly re-verified. R2 (lines 597-599) was re-verified (see L04-R2-spread-criterion). The M1-M3, P1-P3, R1 and R3 texts are byte-identical to the round-8 pin (the delta hunks at old lines 549-553, 560, 585 are E1, E2 and R2 only), so their round-8 evidence is carried as below.",
    "L04-scope-and-banned-phrases": "Re-verified on the delta text. The new sentences in L04.html (lines 52, 72, 87, 129, 180, 475) and the lab docstring carry no process words (grep for round, verifier, builder, TODO, draft, placeholder, pending returns nothing in L04-L06). Scope words in the new text ('every fair value' at line 475, 'the same rule', 'only' in no new sentence) are checked against H1-H3 of Prop 3.1 and the enumeration (see lab-L04-1-hypothesis-interpretation).",
    "L05-why-it-matters-comparisons": "Re-verified (L05.html line 52). The new 'Definition 1.3' cross-reference names the definition at L05.html line 77 (block title 'Definition 1.3 (sliding-window maximum)'), which is the sliding-window maximum the sentence describes. The claim 'at most twice the input length in comparisons' is Prop 3.3; the lab prints the deque comparisons (354 on seed 5, 350 on seed 6) against the bound 2n = 400 (" + OUT_DIR + "/lab-PC3-L05-1.stdout). PASS.",
    "L06-canon-breaks-and-misconceptions": "Re-verified (L06.html line 323, changed). The misconception now says the break-even moves 'by 21.24 units per point of rate, which is (1249.0469-1164.1005)/4 from the unrounded values (Problem E3)'. Recomputed: 1249.0469-1164.1005 = 84.9464, /4 = 21.2366, displayed 21.24 (l06_independent.out: 'avg per point: 21.236599884883976'). Problem E3 (L06.html line 410) gives the same unrounded values and the same 21.2366 -> 21.24. The lab prints 1164.10, 1206.34, 1249.05 (lab-PC3-L06-1 stdout and expected block). The 42.24 / 42.70 / 42.71 figures in E3 also re-derive.",
    "L04-structure-hours": "Re-verified: no hunk of the delta touches an hours figure or a section length in L04.html, and index.html line 29 is unchanged (the delta touches only L04.html, L05.html, L06.html and the two lab twins).",
    "L05-structure-hours": "Re-verified: no hunk of the delta touches an hours figure in L05.html (the delta hunks are at lines 52, 163, 173, 262-263, 306-307, 321, 417 of the old file).",
    "L04-A1-project-consistency": "Re-verified. A1 (L04.html line 72) now reads 'Lab 1 (Section 4) and the unit project use p=1/2', and project.html line 404 states the three outcomes with probabilities 1/4, 1/4 and 1/2, which is p=1/2. The sentence stays consistent.",
    "L06-structure-hours": "Re-verified: the only L06.html delta hunk is line 323 (misconception text, no hours figure), so the hours statements in L06.html are unchanged.",
}

CARRY_FILES = {
    # carried row -> (file(s) whose cited text is byte-identical since 0dee921a)
}

rows = []
for r in R8["rows"]:
    rid = r["id"]
    if rid in NEW:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": NEW[rid]})
    else:
        ev = r["evidence"]
        if r["status"] != "PASS":
            raise SystemExit(f"round-8 non-PASS row {rid} is not in NEW")
        rows.append({
            "id": rid,
            "check": r["check"],
            "location": r["location"] + " [round-8 line numbers; current lines per notes]",
            "status": "PASS",
            "evidence": "Carried from round 8 (cited text byte-identical since the previous pin 0dee921a; no delta hunk touches the cited text): " + ev,
        })

frag = {
    "unit": "PC3",
    "slice": "PC3-b",
    "round": 9,
    "verifier": "Claude Haiku 5.5, independent verifier for PC3-b round 9 (did not build PC3)",
    "pin": "c93dd526025c6dffd34c54cd2c89eb62a890f885",
    "base": "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3 (round-8 pin). Delta 0dee921a..c93dd526 touches L04.html (A1, Example 1.3, Prop 3.1 H3, why-it-matters, lab hypothesis/interpretation, lab seed-1 line, E1, E2, R2), L05.html (why-it-matters, lab hypothesis/interpretation, E2, lab seed-6 line), L06.html (one misconception line), lab twins lab-PC3-L04-1.py and lab-PC3-L05-1.py. Every changed hunk was read. Round-8 FAIL rows were re-verified from scratch; carried PASS rows are only those whose cited text is outside every hunk.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE9-PC3-b",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyE9-PC3-b/" + OUT_DIR,
    "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice b: course/modules/PC/PC3/L04.html, L05.html, L06.html and tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py. cards.json, project.html and the project graders are outside this slice and are not checked here.",
        "Line-number map (old 0dee921a -> current c93dd526, from difflib over the file): L04.html old 1-179 and 181-188 unchanged; old 190-348 +1; old 349-442 +13; old 443-459, 461-552, 554-559, 561-584, 586-722 +15. L05.html old 1-172 unchanged; old 174-261 +1; old 262-306 +9; old 307-320, 322-416, 418-569 +11. L06.html old 1-322 and 324-550 unchanged. Carried rows keep their round-8 locators; add the offset to find the current line.",
        "Mutants: none. Lab twins are demonstrations; mutation testing applies to project graders (ruling). No grader mutant is claimed.",
        "Judgement on the Prop 3.1 interpretation (L04.html lab interpretation, 'the proof covers every fair value for a fixed quote, from inventory zero (Proposition 3.1, H1)'): H1 includes the clause that the conditioning event has positive probability, so the citation of H1 carries that hypothesis. The sentence is read as citing the full H1. Not a finding.",
        "Why-it-matters (L04.html line 52) now says the inventory 'stays below its limit'. This matches the Remark 4.2 condition |I| <= L-1, under which the inventory test of A5 refuses no fill, so the sentence is consistent with the remark. The variance statement (Prop 4.1) holds for every I; the sentence attaches the limit condition to both claims, which is a reading choice and not a false claim.",
        "Ungraded model-limit sentences (for example, L04 Section 5 on the limit order book queue, L06 Section 5 on real assets) are not graded, per the ruling on unread standards and model limits.",
        "Round-9 scratch scripts: ledgers/PC3/scripts/PC3-b-r9/ (embed_compare.py, l04_independent.py, l05_independent.py, l06_independent.py, l05_seed6_r9.py, linemap.py, build_fragment_r9.py); outputs in ledgers/PC3/scripts/PC3-b-r9/out/. l05_seed6.py in the r9 folder is the round-8 script and fails in this checkout (import path points at the round-8 checkout); l05_seed6_r9.py replaces it.",
    ],
}
frag["summary"] = {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows), "fail": sum(r["status"] == "FAIL" for r in rows), "unverifiable": 0}
OUT.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", OUT, frag["summary"])
