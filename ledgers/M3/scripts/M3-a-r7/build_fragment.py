"""Build the round-7 fragment for M3 slice a from the round-6 rows (ids kept; overrides re-verified this round)."""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
prev = json.load(open("/Users/billyribeiro/.fanout/frags/B-M3-a.round6.json", encoding="utf-8"))
CARRY = "Carried from round 6 (cited locator bytes unchanged since 44f1eb6; hunk list 44f1eb6..7aa909e checked, no hunk inside the cited lines): "
# subjects whose cited lines overlap a changed hunk in 44f1eb6..7aa909e, re-verified this round
FRESH = {
    "a6-hub-structure": ("PASS", "course/modules/M/M3/index.html:29-182 (hunk at line 37 only)",
        "check_pages.py --unit M3 -> 'check_pages M3: PASS' on 7aa909e. Hub objectives, prerequisites, 9-item placement, 9-card lesson map unchanged except line 37, read in full in round 6 and checked against the one changed line here."),
    "a6-hub-data-claims": ("PASS", "course/modules/M/M3/index.html:37,173; course/modules/M/M3/project.html:53,60,103,185,289,292",
        "Line 37 now says 'The project's three worked labs use hand-set matrices labelled SIMULATED'. project.html has three labs (lines 55, 141, 287); SIMULATED labels at project.html:53,60,103,185,289,292; hand-set wording at 53,289. Line 173 unchanged and still matches MANIFEST (two series). Claim holds."),
    "a6-L01-span-prop": ("PASS", "course/modules/M/M3/L01.html:96-109 (hunk line 108)",
        "Line 108 now defines e_1 = (1,0,0), e_2 = (0,1,0) before use; span(e_1,e_2) = {(a,b,0)} re-derived. Previous FAIL a6-L01-defuse-e-i resolved."),
    "a6-L01-problems": ("PASS", "course/modules/M/M3/L01.html:408-503 (hunks at 435, 437)",
        "Problem P1 renamed U,W -> X,W at 435 and 437; proof at 437 uses X and W consistently ('Both X and W contain 0 ... X cap W is a subspace'). Other problems unchanged and carried from round 6."),
    "a6-L01-quiz-keyresults": ("PASS", "course/modules/M/M3/L01.html:527-610 (hunk at 566)",
        "Line 566 explanation now cites 'the proof of Lemma 3.4'. Lemma 3.4 is at L01.html:131 ('more columns than pivots gives a non-zero solution'), and its pivot-count argument is used at 147. Reference is correct."),
    "a6-L01-structure-prose": ("PASS", "course/modules/M/M3/L01.html (whole page; hunk at line 51)",
        "why-it-matters at line 51 re-counted: 99 words (<=120). New sentence 'Over one period, the return of a portfolio ...' contains no banned phrase or process word. Other structure elements unchanged."),
    "a6-L01-lab-twin-page": ("PASS", "tests/labs/M3/lab-M3-L01-1.py; course/modules/M/M3/L01.html:195-355",
        "ledgers/M3/scripts/M3-a-r7/twin_vs_page.py: 'L01 page code == twin: True | code lines 147'; 'L01 twin exit 0 | expected == output: True' under python -I -W error. run_labs --unit M3 --page L01: PASS (1/1)."),
    "a6-L01-lab-numbers": ("PASS", "ledgers/M3/scripts/M3-a-r7/recount.py; L01.html:355",
        "numpy recount: 'L01 numpy recount: 188 0 198 0 | planted dep 100 indep triples 100 rank3 100' (matches printed counts; 188/200, 0/200, 198/200, 0/200)."),
    "a6-L01-lab-claims": ("PASS", "course/modules/M/M3/L01.html:194,355; tests/labs/M3/lab-M3-L01-1.py:6-8",
        "Docstring claim (b) now reads 'the 4-vector lists in R^3 and the 5-vector lists in R^4 are all dependent'. Recount gives 0/200 independent in both, so the claim is true of the code's draws. Page text at 194 says 0 for both counts out of 200, matching."),
    "a6-L01-defuse-e-i": ("PASS", "course/modules/M/M3/L01.html:108",
        "Example 2.3 defines e_1, e_2 at 108 before use; the e_i definition at Example 3.9 (line 184) is now a harmless repeat."),
    "a6-L01-dag-simple-return": ("PASS", "course/modules/M/M3/L01.html:51; index.html; L02.html; L03.html",
        "Line 51 no longer contains 'simple return'; grep for 'simple return|simple-return' over index, L01, L02, L03 returns 0 hits. check_dag.py --unit M3: PASS."),
    "a6-L01-lab-docstring-claim-b": ("PASS", "tests/labs/M3/lab-M3-L01-1.py:7-9; course/modules/M/M3/L01.html:195-201",
        "Docstring (b) narrowed to the drawn n+1-vector lists and the 'every list' claim is attributed to Corollary 3.6, which the page states as a proved result; the lab's drawn lists are exactly those (4-vectors in R^3, 5-vectors in R^4). Previous FAIL resolved."),
    "a6-L01-lab-generated-inputs-label": ("PASS", "course/modules/M/M3/L01.html:193-194; course/modules/M/M3/L02.html:181-182",
        "L01 line 194 'drawn by a fixed generator' and L02 hypothesis 'seeded' both still present; generated-input labelling correct."),
    "a6-L02-change-of-basis": ("PASS", "course/modules/M/M3/L02.html:151-178 (hunks 167, 172)",
        "Line 167 'put \\widetilde{A} = P^{-1} A P. Then A = P \\widetilde{A} P^{-1}'; line 172 proof '(P P^{-1}) A (P P^{-1}) = I A I = A' re-derived. Theorem 4.1 at 157 and its proof unchanged; Ex 4.3 unchanged."),
    "a6-L02-lab-twin-page": ("PASS", "tests/labs/M3/lab-M3-L02-1.py; course/modules/M/M3/L02.html:183-357",
        "twin_vs_page.py: 'L02 page code == twin: True | code lines 166'; 'L02 twin exit 0 | expected == output: True'. run_labs --unit M3 --page L02: PASS (1/1). Renamed S->P, C->M in code and expected block consistently; no leftover S/C/B in twin."),
    "a6-L02-lab-numbers": ("PASS", "ledgers/M3/scripts/M3-a-r7/recount.py; course/modules/M/M3/L02.html:349-357",
        "numpy recount: 'L02 numpy recount: rejected 7 formula 50 composition 50 first [[3.0, -17.5, 12.333333], [0.0, 5.0, -1.666667], [-2.0, 8.0, -6.0]]'. Matches the printed 7, 50, 50 and first-pair matrix."),
    "a6-L02-lab-claims": ("PASS", "course/modules/M/M3/L02.html:182,358",
        "Hypothesis at 182 predicts 50 of 50 and the rejection count is not predicted; interpretation at 358 says 'row 1 is 3, -35/2, 37/3' which matches the recount row 1 (3, -17.5, 12.333). 'The 7 rejected draws' matches."),
    "a6-L02-misconceptions-problems": ("PASS", "course/modules/M/M3/L02.html:372-493 (hunks 431-464)",
        "Renamed B->widetilde A at 431-433, S->P at 448-465. Solutions re-checked: A = P widetilde{A} P^{-1} and the rejected-draw answer are consistent with Theorem 4.1 and the code. Other problems carried."),
    "a6-L02-quiz-keyresults": ("PASS", "course/modules/M/M3/L02.html:495-596 (hunks 542-548, 583)",
        "Q4 options renamed; correct option 'P widetilde{A} P^{-1}' is the right expression (Cor 4.2). Explanation at 548 consistent. Q9 option renamed to 'every P in the run is invertible by construction' and remains the correct distractor-free statement of the lab."),
    "a6-L02-structure-prose": ("PASS", "course/modules/M/M3/L02.html (whole page; hunks at 167-596)",
        "why-it-matters at line 51 re-counted: 112 words (<=120). Renamed text adds no banned phrase or process word. Meta description issue is a separate row (a7-L02-meta-description-B)."),
    "a6-L02-notation-S": ("PASS", "course/modules/M/M3/L02.html:138,143,148,382,474-476,594; L02.html:182,359,368",
        "S now appears only as the linear map S : W -> Z (lines 138-594). grep for S^{-1}/S^-1 and for S as a matrix returns 0 hits; the invertible matrix is P (line 182) in the hypothesis, the lab docstring and expected block."),
    "a6-L03-ex25-independence": ("PASS", "course/modules/M/M3/L03.html:144",
        "Now: columns (1,0,0),(1,1,0),(1,3,6) are independent 'once known'; det P = 6 (re-derived: upper triangular [[1,1,1],[0,1,3],[0,0,6]], det 6) is nonzero, so under F1 P is invertible, and Px=0 forces x=0. Chain is valid; the step is no longer missing."),
    "a6-L03-example-numbers": ("PASS", "course/modules/M/M3/L03.html:97,101-103,144",
        "Line 144 hunk checked: det P = 6 correct. Other numbers in 97-103 unchanged and re-derived in round 6."),
    "a6-L03-decomp-props": ("PASS", "course/modules/M/M3/L03.html:107-155 (hunk at 144)",
        "Only the Example 2.5 sentence at 144 changed (checked above); Prop 2.2-2.6 text unchanged and carried from round 6."),
    "a6-L03-lab-twin-page": ("PASS", "tests/labs/M3/lab-M3-L03-1.py; course/modules/M/M3/L03.html:157-253",
        "twin_vs_page.py: 'L03 page code == twin: True | code lines 82'; 'L03 twin exit 0 | expected == output: True'. run_labs --page L03: PASS (1/1)."),
    "a6-L03-lab-claims": ("PASS", "course/modules/M/M3/L03.html:159,252,402",
        "Re-ran twin: printed lines match the claims (AP=PD True; det 6; eigenvalues 2,3,5; defective B rank 1). Unchanged text."),
    "a6-L03-structure-prose": ("PASS", "course/modules/M/M3/L03.html (whole page; hunk at 144)",
        "Only line 144 changed; why-it-matters word count unchanged (77). No banned phrase or process word in the changed sentence."),
    "a6-dag-concepts": ("PASS", "course/modules/M/M3/{index,L01,L02,L03}.html",
        "check_dag.py --unit M3: PASS on 7aa909e (run this round)."),
    "a6-notation-registry": ("PASS", "notation/notation.json; course/modules/M/M3/L02.html (P, M, widetilde A, S)",
        "Registry holds 8 program-wide symbols; P, M, \\widetilde and S are local (not registered), used with one meaning each inside L02 (S only a map; P only the invertible change-of-basis matrix; M second integer matrix in the lab). The meta-description reuse of B is a separate FAIL row."),
    "a6-gates-lint-types": ("PASS", "tests/labs/M3/*.py; tests/test_labs.py -k M3",
        "ruff check tests/labs/M3: All checks passed; ruff format --check tests/labs/M3: 12 files formatted; mypy --no-incremental on the three L01-L03 twins: Success, no issues; pytest tests/test_labs.py -k M3: 12 passed."),
    "a6-render-page-smoke": ("PASS", "tools/page_smoke.py --unit M3",
        "This round: 'page_smoke M3: PASS' (index, concepts, review and M3 pages; exit 0). Round 6 could not run it (no Chromium); the run here succeeded."),
}
ADDED = [
    {"id": "a7-L02-card-M3-c036", "check": "cards agree with current lesson text and notation (cards.json vs L02.html:167-172)",
     "location": "course/modules/M/M3/cards.json:243-246 (card M3-c036, lesson L02)",
     "status": "FAIL",
     "evidence": "Card front 'If B = P^{-1} A P with P invertible, what is A in terms of B?' and back 'A = P B P^{-1} (Corollary 4.2)'. The lesson at L02.html:167 and :172 now defines widetilde{A} = P^{-1} A P and proves A = P widetilde{A} P^{-1}; on the same lesson B is the basis symbol (L02.html:153, 157). The card still uses B as the matrix, so it disagrees with the current lesson text and reuses B with a second meaning. Not changed in the 44f1eb6..7aa909e delta, so it was stale before this round too. Fix: change the card to widetilde{A} = P^{-1}AP and A = P widetilde{A} P^{-1} (edit cards.json source, then regenerate per the project rules if it is generated).",
     "fix": "Rewrite M3-c036 front to 'If widetilde{A} = P^{-1} A P with P invertible, what is A in terms of widetilde{A}?' and back to 'A = P widetilde{A} P^{-1} (Corollary 4.2).'"},
    {"id": "a7-L02-meta-description-B", "check": "notation: a symbol keeps one meaning on the page (B = basis in L02, Sec 2-4)",
     "location": "course/modules/M/M3/L02.html:7 (meta description)",
     "status": "FAIL",
     "evidence": "Meta description: 'and the change-of-basis formula B = P^-1 A P proved'. On the same page B denotes a basis (L02.html:111, 116, 121, 153, 157 'columns form a basis B'), and the theorem text now uses widetilde{A}, so the description reuses B with a second meaning and is inconsistent with the current statement. Fix: 'the change-of-basis formula P^-1 A P proved' (no symbol for the matrix)."
     , "fix": "Replace 'B = P^-1 A P' with 'P^-1 A P' in the meta description at L02.html:7."},
]

rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in FRESH:
        st, loc, ev = FRESH[rid]
        rows.append({"id": rid, "check": r["check"], "location": loc, "status": st, "evidence": ev})
    elif r["status"] == "PASS":
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": CARRY + r["evidence"]})
    else:
        raise SystemExit("unhandled non-PASS previous row: " + rid)
rows.extend(ADDED)

counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
frag = {
    "unit": "M3", "slice": "a", "round": 7,
    "verifier": "independent Haiku verifier (round 7), not a builder of M3",
    "pin": "7aa909e", "base": "44f1eb6 (round-6 pin; delta 44f1eb6..7aa909e read for slice a: index.html:37, L01.html:51,108,435,437,566, L02.html 7,138-596 renames, L03.html:144, L01 and L02 twins, cards.json M3-c0xx L02 and L03 hunks)",
    "checkout": str(root), "scratch": str(root / "ledgers/M3/scripts/M3-a-r7"),
    "verified_at": "2026-10-29T01:50:00+00:00", "verdict": verdict, "rows": rows,
    "mutants": [], "registry_flags": [], "freshness_flags": [],
    "notes": "Slice a = hub index.html, L01-L03 and their lab twins. Lesson slice: mutants not required (VERIFIER_RULES 2.6 applies to project slices). Fresh this round: twin_vs_page.py, recount.py, run_labs (index, L01-L03), check_pages, check_dag, page_smoke --unit M3, ruff, mypy, pytest -k M3, verify_refs --offline (560 entries, 0 problems). Carried rows cite locator ranges not inside any changed hunk; they were not re-read line by line this round (honest gap). Not checked: verify_refs live run; full-page line-by-line re-read of unchanged regions of L01-L03 (carried); project slices untouched.",
    "summary": f"{len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. FAIL: a7-L02-card-M3-c036 (card still uses B = P^-1AP, stale after the widetilde rename, B is basis symbol); a7-L02-meta-description-B (L02.html:7 meta description reuses B as the matrix). All round-6 FAIL rows (e_i before definition, 'simple return', L01 docstring claim (b), S as map and matrix, Example 2.5 independence) are fixed and re-verified PASS.",
}
out = root / "ledgers/M3/M3-a.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, counts, verdict)
