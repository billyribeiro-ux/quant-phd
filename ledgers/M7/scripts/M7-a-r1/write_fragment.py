"""Verifier M7 slice a, closing delta round 1. Writes ledgers/M7/M7-a.json.

Row ids and order come from the round-2 base fragment. A row is either re-verified this round (new evidence
below, with the command output or script named) or carried from round 2 under the carry prefix because its cited
subject is byte-identical to 9294b914 (git diff --quiet, run in gate_commands.sh and card_bytes_delta.py).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, "tools")
import ledger  # noqa: E402

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyF21-M7-a")
BASE = json.loads(Path("/Users/billyribeiro/.fanout/frags/S-M7-a.round2.json").read_text(encoding="utf-8"))
S = "ledgers/M7/scripts/M7-a-r1/"

PFX = ("Carried from round 2 (course/modules/M/M7/L01.html, L02.html, L03.html and tests/labs/M7/lab-M7-L01-1.py, "
       "lab-M7-L02-1.py, lab-M7-L03-1.py byte-identical since the previous pin 9294b914; git diff --quiet "
       "9294b914..HEAD): ")
PFX_M2 = ("Carried from round 2 (course/modules/M/M7/L01.html, L02.html, L03.html, the three twins and "
          "course/modules/M/M2/L21.html byte-identical since 9294b914; git diff --quiet): ")
PFX_NOT = ("Carried from round 2 (course/modules/M/M7/L01.html, L02.html, L03.html, the three twins, notation/notation.json "
           "and references/ unchanged since 9294b914; git diff --quiet): ")

CARRY_PFX = {
    "M7a-L01-structure": PFX, "M7a-L01-math": PFX, "M7a-L01-problems": PFX, "M7a-L01-lab-prose": PFX,
    "M7a-L01-grades": PFX, "M7a-L01-quiz": PFX,
    "M7a-L02-structure": PFX, "M7a-L02-math": PFX, "M7a-L02-attribution-M2-L21": PFX_M2, "M7a-L02-problems": PFX,
    "M7a-L02-lab-prose": PFX, "M7a-L02-grades": PFX, "M7a-L02-quiz": PFX,
    "M7a-L03-structure": PFX, "M7a-L03-math": PFX, "M7a-L03-problems": PFX, "M7a-L03-lab-prose": PFX,
    "M7a-L03-grades": PFX, "M7a-L03-quiz": PFX, "M7a-L03-misconceptions": PFX,
    "M7a-notation-local-letters": PFX_NOT, "M7a-misconceptions-counts": PFX, "M7a-mutants": PFX,
}

NEW = {
"M7a-cmd-check_pages": (
    "Re-run at 95f3f8cb (index.html changed by one line): `.venv/bin/python tools/check_pages.py --unit M7` printed "
    "'check_pages M7: PASS' (exit 0); `--page L01`, `--page L02`, `--page L03` each printed 'check_pages M7 Lxx: PASS' "
    "(exit 0). Output: " + S + "out/check_pages_*.out."),
"M7a-cmd-check_dag": (
    "Re-run: `tools/check_dag.py --unit M7` printed 'check_dag M7: PASS' (exit 0; " + S + "out/check_dag_unit.out). "
    "The hub concept links (index.html line 64) and the L01-L03 dfn/links resolve; course/concepts.html is unchanged in the delta."),
"M7a-cmd-check_projects": (
    "Re-run because project.html changed in the delta (hub ladder and placement cite it): `tools/check_projects.py --unit M7` "
    "printed 'check_projects M7: PASS' (exit 0; " + S + "out/check_projects_unit.out). The project grader is not in this slice."),
"M7a-cmd-run_labs": (
    "Re-run: `tools/run_labs.py --unit M7 --page L01|L02|L03` printed 'run_labs M7: PASS (1/1)' for each (exit 0; " + S +
    "out/run_labs_L0*.out)."),
"M7a-lab-twin-direct": (
    "Re-run: each twin under `python -I -W error` exits 0 with empty stderr (" + S + "out/twin_L01.out, twin_L02.out, "
    "twin_L03.out). Deterministic exact-fraction or fixed-constant output; no network."),
"M7a-lab-code-equals-twin": (
    "Re-run with " + S + "delta_lab_check.py (output delta_lab_check.out): the first <code data-run> block of L01, L02 and L03 equals the "
    "twin text, the only difference being the single final newline the page omits (code==twin True for all three)."),
"M7a-lab-runtime-seed": (
    "Re-run: each twin exits 0 under -I -W error. page_smoke timings this round: runtime boot 1.1 s, lab 0.6 s max "
    "(" + S + "out/page_smoke_M7.out). L02 uses a fixed-constant generator (twin line 3); L01 and L03 are exact fractions."),
"M7a-cmd-page_smoke": (
    "Re-run (index.html changed): `tools/page_smoke.py --unit M7 --pages index L01 L02 L03` printed 'page_smoke M7: PASS' "
    "(exit 0; " + S + "out/page_smoke_M7.out). Lab timings 0.6 s max."),
"M7a-cmd-ruff-mypy": (
    "Re-run: `ruff check .` 'All checks passed!'; `ruff format --check .` '555 files already formatted'; ruff check and format "
    "check on the three twins clean; `mypy --no-incremental --strict` on the three twins 'Success: no issues found in 3 source "
    "files'; `mypy --no-incremental` on the repository 'Success: no issues found in 386 source files' (" + S + "out/)."),
"M7a-cmd-pytest-labs": (
    "Re-run: `pytest tests/test_labs.py -k M7 -q` passed 11 of 11 (exit 0; " + S + "out/pytest_labs_M7.out); "
    "`--collect-only` collects 11 (" + S + "out/pytest_collect_M7.out)."),
"M7a-cmd-verify_refs": (
    "Re-run: `tools/verify_refs.py --offline` printed 'offline integrity: 560 entries, 0 problems'; `tools/verify_refs.py --unit M7` "
    "printed 'live re-verification of M7: 2 of 560 entries, 0 problems' (both exit 0; " + S + "out/verify_refs_*.out). "
    "references/references.json is unchanged since 9294b914."),
"M7a-hub-hours": (
    "Re-verified (index.html changed at line 150 only): index.html line 29 data-hours-lessons=\"77\" data-hours-project=\"33\"; "
    "lesson cards L01 9 h, L02 9 h, L03 10 h, L04 10 h, L05 10 h, L06 10 h, L07 9 h, L08 10 h sum to 77; each lesson's data-hours "
    "attribute matches its card (grep); index line 141 'Lessons 1, 2, 7 ... 9 hours'; project.html line 35 '33 hours' and line 350 "
    "'110 hours.'; 33 / 110 = 30 percent, inside 10-40 percent; the hub split (line 39) reads 77 and 33."),
"M7a-hub-placement": (
    "Re-verified (index.html section#placement, lines 71-137): nine li.item questions (seven knowledge, two data-skill). Mastery "
    "0.8 of nine = eight; 7/9 = 77.8 percent, 8/9 = 88.9 percent (line 73). Answers recomputed: d/dx1 of x1^2+3x1x2 at (1,0) = 2; "
    "mixed partial = 3; identity is PSD, diag(1,-1) and [[0,1],[1,0]] are not; eigenvalues of [[2,1],[1,2]] are 3 and 1, smaller 1; "
    "negation = 'some asset has a negative weight'; real symmetric matrices have real eigenvalues; skill item Sigma w = lambda 1 "
    "matches L02 Proposition 3.2 (c) (L02.html line ~121-127); skill item Sigma = diag(1,2): u = (1, 1/2), s = 3/2, lambda = 2/3 = "
    "0.6667 to four places; derivative of x^2 at 3 = 6. The explanation cites M1 L01 Theorem 3.1 (negating one quantifier, "
    "course/modules/M/M1/L01.html line 79, read) and M3 spectral theorem (M3/index.html contains it, grep 5 hits; module pointer only)."),
"M7a-hub-objectives-ladder": (
    "Re-verified: objectives section (index.html line 45) lists eight objectives, each naming its lesson (1-6, 7-8 jointly) or the project (8); ladder "
    "(section#ladder, line 154) has four rungs in order: worked example, completion, independent, stretch. Rung text matches "
    "project.html lines 44-47 (Rung 1 Lab 1 three-asset long-only problem; Rung 2 Lab 2 blanks the stationarity line and two "
    "dual-sign lines; Rung 3 specification; Rung 4 stretch). 'Graded instantly in your browser' is the completion path in "
    "course/assets/js/labs.js lines 133-141. Stretch example (parametric frontier, budget multiplier vs value rate) matches "
    "L02 Problem R3 (L02.html line ~420)."),
"M7a-hub-prose-crossrefs": (
    "Re-verified from scratch: index.html read in full (182 lines). Changed hunk, line 150 (L08 hub card): 'value iteration on a "
    "finite-state problem with the change between successive iterates reported, and ... the infinite-horizon result'. L08 Lab 1 "
    "Part C prints 'n {n} change ...' (tests/labs/M7/lab-M7-L08-1.py line 129-130; L08.html expected block lines ~304-307) and "
    "L08 Remark 2.4 says 'The changes between successive iterates that Lab 1 prints'; L08 does not treat the infinite-horizon "
    "result (Remark 2.4). L07 card: backward recursion (Theorem 2.1) and brute-force enumeration (Lab 1). L04: weak duality, zero "
    "duality gap, grid bound, dual function present. L05: KKT linear system, enumeration present. L06: turnover, sector, "
    "short-sale, efficient frontier present. Presence checked by grep only for L04-L07 (their slices verify content)."),
"M7a-hub-naming": (
    "Re-verified: index.html uses 'M2 Calculus' (line 35, 64) and 'M3 Linear Algebra' (line 35). The M2 pages carry the title "
    "'M2 Single & Multivariable Calculus' (course/modules/M/M2/L21.html line 6); 'M2 Calculus' is the short label (non-blocking, "
    "as in round 2). No other naming change in the delta."),
"M7a-hub-covariance-B1": (
    "Re-verified: index.html line 167 is the only hub use of 'covariance' ('estimating a covariance matrix is outside M7'), with no "
    "link (grep). grep for 'covarian' over L01-L03 returns no hit. Other M7 pages (L06, project.html) carry the same disclaimer "
    "and are not in this slice."),
"M7a-hub-data-status": (
    "Re-verified: index.html section#data (line 165-167) 'No real data is used in M7'; no data-files attribute on any M7 page "
    "(grep count 0); L03 section 4 states the matrix and vector are given inputs, SIMULATED and not market data."),
"M7a-notation-x-ast": (
    "Re-counted: x^\\ast occurs 0 times in index.html, L01.html, L02.html, L03.html; R^\\ast occurs 0 times; the minimiser is "
    "written w^* or w^\\ast (index.html 6, L02 45, L03 32 occurrences of the starred form; L01 0)."),
"M7a-notation-ones-glyph": (
    "Re-counted \\mathbf{1}: index.html 5, L01 7, L02 42, L03 4 (same as round 2). notation/notation.json is unchanged; its "
    "macro \\indic has tex \\mathbf{1} and meaning 'indicator function' (grep). The collision is the open architect question in "
    "registry_flags. Ruling 26 does not list notation among its FAIL kinds, so the row stays PASS with that flag."),
"M7a-notation-diag-local": (
    "Re-counted: \\operatorname{diag} occurs index.html 3, L01 2, L02 6; \\diag occurs 0 times. notation/notation.json registers "
    "both forms (grep). Same rendering; minor, as flagged in round 2."),
"M7a-dag-closure": (
    "Re-verified: check_dag M7 PASS (" + S + "out/check_dag_unit.out). index.html line 64 links only M2 and M3 concepts "
    "(gradient, hessian, implicit-function-theorem, envelope-theorem, positive-semidefinite-matrix, eigendecomposition, "
    "spectral-theorem) through course/concepts.html, which is unchanged in the delta; no M7 page links a concept from outside the "
    "closure."),
"M7a-dfn-ownership": (
    "Re-verified by grep of <dfn> in L01-L08: convex-set, convex-function (L01); lagrange-multiplier (L02); kkt-conditions (L03); "
    "lagrangian-duality (L04); quadratic-programming (L05); mean-variance-optimization, linear-portfolio-constraints (L06); "
    "principle-of-optimality (L07); bellman-equation (L08). Ten concepts, each defined once, matching index.html line 68 'ten "
    "concepts'. check_dag PASS."),
"M7a-banned-phrases": (
    "Re-scanned with " + S + "scan_text.py (output scan_text.out) over index.html, L01-L03 and the three twins: zero banned "
    "strings in index.html and L03; L01 and L02 hits are 'fixed seed', 'fixed point', 'for fixed x and y' and the set range "
    "{-2, ..., 2} (a range, not omitted content). No TODO, TBD, lorem, 'for brevity', 'details omitted', 'beyond the scope', "
    "'left as an exercise', 'obviously', 'clearly', 'it can be shown', percentage guess or 'historically'."),
"M7a-process-words": (
    "Re-scanned with scan_text.py: no 'round', 'builder', 'verifier', 'fixer', 'agent' or 'we changed' in index.html, L01-L03 "
    "or the twins; the only 'fixed' hits are mathematical or seed wording (see M7a-banned-phrases)."),
"M7a-cards-scan": (
    "Re-run over the whole cards.json at 95f3f8cb with " + S + "delta_cards_check.py (output delta_cards_check.out): 203 cards (base 199). "
    "No duplicate ids and no duplicate fronts over the file; every card has id, lesson, front, back, grade; grades are T or C; "
    "every C card has a basis and no T card has one. L01-L03: 78 cards (L01 24, L02 25, L03 29; base 77 plus new M7-c229). "
    "card_bytes_delta.py (card_bytes_delta.out) compares each card object with 9294b914: changed or new in L01-L03 are c004, "
    "c018, c041, c050, c229; the rest are byte-identical. Outside L01-L03 the delta also changes c058, c103, c114, c123, c124, "
    "c136, c142, c150, c174 and adds c226 (L07), c227 (L08), c228 (L06); those belong to the L04-L08 slices and are not "
    "verified by this slice."),
"M7a-cards-numbers": (
    "Re-run over all 78 L01-L03 cards (delta_cards_check.py): every cited Definition, Proposition, Theorem, Lemma, Remark, Example, "
    "Assumption, Part and Lab number appears in the card's own lesson. The five 'Section N' citations (c011, c185 in L01/L02, "
    "c193, c225 in L02, c194 in L03) do not match the literal string because the pages write the section as an h2 with "
    "section-number N: L01 s3 'Quadratic forms', L02 s1 and s3, L03 s1 (checked in the h2 lines). No card number is missing."),
"M7a-cards-grades": (
    "Re-counted this round: L01-L03 cards T 64, C 14 (78 cards; base 64 and 13 over 77, plus new C card c229). Changed grades: "
    "c004 T (Proposition 1.3, data-grade T), c018 T (Theorem 2.2, data-grade T), c041 T (Lemma 1.5, T), c050 C and c229 C with "
    "basis 'Lab 1 (SIMULATED) ...' (lab printed lines, not proved). Other grades byte-identical and carried."),
}

# Rows re-verified this round that are also partly carried: the new evidence plus the round-2 evidence for the unchanged cards.
MIXED = {
"M7a-cards-L01": ("Changed card M7-c004 re-verified against L01.html Proposition 1.3 (lines 53-77): its hypotheses are a "
                  "nonempty family and each S_i convex, exactly as the card's back states; grade T matches the claim span. "
                  "The other 23 L01 cards are byte-identical to 9294b914 (card_bytes_delta.out) and L01.html is unchanged. "),
"M7a-cards-L02": ("Changed card M7-c018 re-verified against L02.html Assumption 1 and Theorem 2.2 (section 2): the card's "
                  "'M2 states the one-variable form' matches M2 L21 Theorem 1.3 (course/modules/M/M2/L21.html lines 68-70: "
                  "one independent real variable x, one dependent variable), and the hypotheses listed are those of Theorem 2.2. "
                  "The other 24 L02 cards are byte-identical to 9294b914 (card_bytes_delta.out) and L02.html is unchanged. "),
"M7a-cards-L03": ("Changed card M7-c041 re-verified against L03.html Lemma 1.5 (section 1): the answer 'Yes, for every c in R^n' "
                  "matches the lemma (Sigma symmetric with x'Sigma x >= 0; conclusion convexity for every c). Changed card "
                  "M7-c050 (grade C, 'Lab 1 (SIMULATED), exact arithmetic') re-derived: grad f(1/2,1/2) = (0, 3/2), residual = "
                  "(0,3/2) + (0,-3/10) + (-1/2)(1,1) = (-1/2, 1/2); the card matches the printed line 'off-solution point ... "
                  "stationarity residual (-1/2, 1/2)' in the expected block and the interpretation's 'two deliberate errors'. "
                  "New card M7-c229 (grade C) matches the printed 'flipped sign lambda2 = -3/10 ... dual residual 3/10' and the "
                  "(K3) definition in Definition 1.2. The other 26 L03 cards are byte-identical to 9294b914 (card_bytes_delta.out). "),
}

NOTES = [
    "Scope (base fragment notes, re-read): slice A = index.html, L01.html, L02.html, L03.html, their three twins, and the 77 "
    "L01-L03 cards in cards.json (now 78 with M7-c229). Delta 9294b914..95f3f8cb in slice A: index.html (one line, the L08 hub "
    "card, line 150); cards.json (L01-L03 changed: c004, c018, c041, c050; new c229). L01-L03 pages and the three twins are "
    "byte-identical to 9294b914 (git diff --quiet). Shared inputs unchanged: tools/, notation/, references/, curriculum/, "
    "course/assets/, course/concepts.html, M2/L21.html, M1 pages.",
    "Rulings applied: 30 (delta closing; every row whose subject changed re-verified from scratch, others carried under the "
    "carry prefix; observations are notes, not rows), 37 (no new mutants; the slice has none), 26 (only the FAIL kinds count; "
    "wording and card style are not FAIL here). Ruling 23 (blind exemplar scoring): slice A has no rubric exemplars and the base "
    "has no calibration rows, so none to cite or carry.",
    "Out-of-slice changes in the same cards.json (not verified by this slice; for the L04-L08 slices' delta rows): c058 (L04), "
    "c103, c114, c174 (L06), c123, c124, c136 (L07; c136 grade changed C to T), c142, c150 (L08); new c226 (L07), c227 (L08), "
    "c228 (L06). Also changed but outside slice A: L07.html, L08.html, project.html, grader/ and the M2 pages.",
    "Lab checks: page code equals twin (the page omits only the file's final newline); each page's expected block equals the "
    "twin's stdout exactly (delta_lab_check.out, ALL OK). The L03 printed lines are the source of c050 and c229 and were checked.",
    "Not checked, honestly: run_graders.py, mutate_graders.py and the alternative solvers (project and grader slices, not in A); "
    "L04-L08 pages and their cards beyond the presence-level greps in M7a-hub-prose-crossrefs; the full pytest suite (only "
    "-k M7 test_labs.py and collect-only); tools/build_site.py --check and tools/render_curriculum.py (generated outputs; no "
    "source changed in the delta, not run here); fetch_data.py --check ran and printed '3 datasets, 0 problems' (" + S + "out/fetch_data_check.out); "
    "page_smoke timing on a quiet machine (one run here). The M3 and M1 pointers in the placement explanations were read as module "
    "pointers only (M1 L01 Theorem 3.1 read; M3 spectral theorem located by grep).",
    "Registry flags (carried from round 2, still open for the architect): notation ones-glyph (\\mathbf{1} vs the registered macro "
    "\\indic) and diag spelling; plain gamma local letter in L02 line 83 and L03 line 140. Non-blocking for this slice.",
    "Judgement carried from round 2 (non-blocking): BUILDER 2.1 claim spans on theorem, proposition, lemma and example titles only.",
]

REGISTRY_FLAGS = [
    "boyd2004convex and stokey1989recursive: records unchanged; verify_refs offline 560 entries 0 problems; live M7 2 of 560 "
    "0 problems. Records read this round: Boyd & Vandenberghe (2004) and Stokey, Lucas & Prescott (1989), as index.html states.",
    "Notation (architect, not a slice defect): the bold-one glyph \\mathbf{1} is the ones vector on M7 pages, while "
    "notation/notation.json binds the macro \\indic to tex \\mathbf{1} with meaning 'indicator function'. A NOTATION_REQUEST "
    "is open; if the architect rules a collision, row M7a-notation-ones-glyph flips to FAIL.",
    "Notation (minor): the pages write \\operatorname{diag} where the registry macro \\diag would be used. Same rendering.",
    "Notation (local, for the architect): plain gamma is used in M7 for a curve (L02 line 83) and for risk aversion (L03 line 140), "
    "both defined locally.",
]

def build_rows():
    rows = []
    for base_row in BASE["rows"]:
        rid = base_row["id"]
        if rid in NEW:
            ev = NEW[rid]
        elif rid in MIXED:
            ev = MIXED[rid] + PFX + base_row["evidence"]
        elif rid in CARRY_PFX:
            assert not any(k in base_row["location"] for k in ("index.html", "cards.json", "project")), rid
            ev = CARRY_PFX[rid] + base_row["evidence"]
        else:
            raise SystemExit(f"row {rid} has no disposition")
        rows.append({"id": rid, "check": base_row["check"], "location": base_row["location"], "status": "PASS",
                     "evidence": ev})
    return rows

rows = build_rows()
assert [r["id"] for r in rows] == [r["id"] for r in BASE["rows"]], "row ids must be kept in order"
fragment = {
    "unit": "M7",
    "slice": "a",
    "round": 1,
    "verifier": "Haiku independent verifier, M7 slice a closing delta, round 1 (did not build M7; base = round-2 fragment)",
    "pin": "95f3f8cb",
    "base": "9294b914 (round-2 base fragment ~/.fanout/frags/S-M7-a.round2.json, verdict PASS)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyF21-M7-a (detached at 95f3f8cb; .venv symlinked)",
    "scratch": S,
    "verified_at": "2026-11-09",
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": REGISTRY_FLAGS,
    "freshness_flags": [],
    "notes": NOTES,
    "summary": {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows), "fail": 0, "unverifiable": 0},
}
out = ROOT / "ledgers/M7/M7-a.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
problems = ledger.validate(fragment, "M7-a")
print("validate:", problems)
print("rows:", len(rows), "re-verified:", sum(1 for r in rows if r["id"] in NEW or r["id"] in MIXED),
      "carried:", sum(1 for r in rows if r["id"] in CARRY_PFX))
