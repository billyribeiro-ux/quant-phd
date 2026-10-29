import json
C = "Carried from round 13 (cited lines byte-identical since the previous pin fca6bb1; no hunk of fca6bb1..d2b4a87 touches them):"
S = "/Users/billyribeiro/.fanout/wt/verifyB14-M3-c/ledgers/M3/scripts/M3-c-r14/"
rows = []
def row(i, check, loc, status, ev):
    rows.append({"id": i, "check": check, "location": loc, "status": status, "evidence": ev})
def carry(i, check, loc, ev):
    row(i, check, loc, "PASS", C + " " + ev)

row("GATE-01", "tools/check_pages.py", "tools/check_pages.py", "PASS", "Fresh run on d2b4a87: 'check_pages M3: PASS' (log ledgers/M3/scripts/M3-c-r14/check_pages.log, exit 0).")
row("GATE-02", "tools/check_dag.py", "tools/check_dag.py", "PASS", "Fresh run: exit 0, check_dag log ledgers/M3/scripts/M3-c-r14/check_dag.log ends 'AP1: PASS'.")
row("GATE-03", "tools/build_site.py --check", "tools/build_site.py", "PASS", "Fresh run: 'site data current: 6 outputs', exit 0 (build_site_check.log).")
row("GATE-04", "tools/render_curriculum.py and git diff --exit-code", "tools/render_curriculum.py", "PASS", "Fresh run: 'curriculum valid: 25 parts, 134 modules, 157 projects, 13,715 h'; git diff --exit-code on CURRICULUM.md and curriculum/curriculum.json exit 0 (render_diff.log).")
row("GATE-05", "tools/run_labs.py --unit M3", "tools/run_labs.py", "PASS", "Fresh run: 'run_labs M3: PASS (12/12)' (run_labs_M3.log, exit 0). A --page filter run returned 0/0 and was discarded.")
row("GATE-06", "tools/page_smoke.py --unit M3 --pages L07 L08 L09", "tools/page_smoke.py", "PASS", "Fresh run: L07, L08, L09 each PASS, 'page_smoke M3: PASS' (page_smoke_L07-09.log, exit 0).")
row("GATE-07", "pyproject.toml ruff config", "pyproject.toml", "PASS", "Fresh: ruff check tests/labs/M3 exit 0; ruff format --check 12 files already formatted (ruff.log).")
row("GATE-08", "pyproject.toml mypy config", "pyproject.toml", "PASS", "Fresh: .venv/bin/python -m mypy --no-incremental 'Success: no issues found in 255 source files' (mypy.log).")
row("GATE-09", "tests/ M3-selected", "tests/", "PASS", "Fresh: pytest --collect-only -k M3 gives 12 (tests/test_labs.py); pytest -k M3 exit 0, 12 passed (pytest_M3.log).")
row("GATE-10", "tools/verify_refs.py --offline", "tools/verify_refs.py", "PASS", "Fresh: 'offline integrity: 560 entries, 0 problems', exit 0 (verify_refs_offline.log).")
row("GATE-11", "tools/fetch_data.py --check", "tools/fetch_data.py", "PASS", "Fresh: 'fetch_data: 3 datasets, 0 problems', exit 0 (fetch_data_check.log).")
row("TWIN-01", "Each twin runs under python -I -W error", "tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py", "PASS", "Fresh: python -I -W error exit 0 for all three (twin_L07/L08/L09.out); run_labs M3 12/12 checks stdout against expected blocks.")
row("TWIN-02", "Page code equals twin; expected block equals output", "course/modules/M/M3/L07.html, L08.html, L09.html", "PASS", "Fresh: run_labs M3 12/12 includes byte-identity of page code to twin and expected-block match (run_labs_M3.log).")
carry("MATH-L07-01", "Theorem 1.2 to 1.3 proofs and Remark 1.4", "course/modules/M/M3/L07.html:63-96", "L07.html:63-96 contains no hunk.")
row("MATH-L07-02", "Theorem 2.2 and Section 1 consequences", "course/modules/M/M3/L07.html:107-121, 319-331", "PASS", "Hunks at L07.html:321 and 328 re-read this round: R2 solution (L07:323) linearity and R3 solution (L07:330) Q=I-P algebra correct. Lines 107-121 carried from round 13 (no hunk touches them).")
row("MATH-L07-03", "Problem set M1-M3, P1-P3, E1-E3, R1 numbers and proofs", "course/modules/M/M3/L07.html:231-308 and 312-318", "PASS", "Re-derived this round: M1 P=(1/2)[[1,1],[1,1]], p=(1,1), residual (1,-1) inner 0; M2 normal eqs give beta1=1/2, beta0=7/6, fitted 7/6,5/3,13/6, residuals -1/6,1/3,-1/6, inner with x = 0; M3 P=diag(1,0), 25=9+16. Hunks at L07:264 and 271 change prompt text only (marker added); solutions P1, P2, P3 re-read and correct.")
carry("NUM-L07-01", "Lab 1 printed values and interpretation", "course/modules/M/M3/L07.html:190-199, 200", "Card M3-c126 (cards.json:883) changed text only (marker added); its number 0.8951 still matches L07.html:218 and the lab printout.")
carry("NUM-L07-02", "E2 solution A^T y numbers", "course/modules/M/M3/L07.html:298", "L07.html:298 carries no hunk.")
carry("NUM-L07-03", "E3 intercept numbers and generator", "course/modules/M/M3/L07.html:303-305; tests/labs/M3/lab-M3-L07-1.py lines 149-154", "L07.html:303-305 no hunk; twin unchanged.")
carry("MATH-L08-01", "Lesson 2 PCA definitions and Theorem 1.4 / 2.1 proofs", "course/modules/M/M3/L08.html:56-133", "L08.html:52 hunk is outside the cited range; no hunk in 56-133.")
row("MATH-L08-02", "Problem set E1-E3, P1-P3, R1-R3 (numbers and proofs)", "course/modules/M/M3/L08.html:323-416", "PASS", "Re-derived this round: M1 X~ rows (-2,-3),(0,-1),(2,4), X~'X~=[[8,14],[14,26]], M=[[4,7],[7,13]], trace 17 = (13+1+20)/2, det 3, eigenvalues (17 +- sqrt277)/2; M2 shares 2/3,1/6,1/6; M3 eigenvalues 18, 9, shares 2/3, 1/3; E1 bound 100*13.6818/(88.2028+99*13.6818)=0.9483; E3 75.9+18.1+5.2=99.2 with bound 0.15. Hunks at L08.html:339, 357, 375, 382, 406, 414 re-read: prompt markers only, and R2 title now matches its statement (was mismatched). R2 and R3 solutions verified algebraically.")
carry("NUM-L08-01", "Lab 1 share numbers and E1 solution", "course/modules/M/M3/L08.html:270-285, 377", "No hunk in 270-285 or 377.")
carry("NUM-L08-02", "Lab 1 cosines and interpretation", "course/modules/M/M3/L08.html:277-280, 284", "No hunk in cited lines.")
carry("NUM-L08-03", "E3 rounding bound", "course/modules/M/M3/L08.html:389-391", "No hunk in cited lines; re-derived 3 x 0.05 = 0.15 this round.")
carry("MATH-L09-01", "Lemma 1.3 to Proposition 3.5 proofs", "course/modules/M/M3/L09.html:73-181", "No hunk in 73-181 (hunks at 193, 350, 360, 390, 445).")
carry("NUM-L09-01", "Example 2.3 and lab numbers", "course/modules/M/M3/L09.html:104-107, 329-331", "No hunk in cited lines.")
carry("NUM-L09-02", "Lab 1 distances and interpretation", "course/modules/M/M3/L09.html:334-338, 342", "L09.html:342 unchanged this round (hunk at 350 is outside).")
carry("NUM-L09-03", "Quiz and sum of squared negative eigenvalues", "course/modules/M/M3/L09.html:438-440; L09.html:559-562", "No hunk in cited lines.")
carry("NUM-L09-04", "Lab 1 interpretation numbers", "course/modules/M/M3/L09.html:341, 342", "No hunk in cited lines.")
carry("NUM-L09-05", "Example 3.6 numbers", "course/modules/M/M3/L09.html:177-180", "No hunk in cited lines; re-derived 0.04 and 1.1 this round.")
row("NUM-L09-06", "E3 and Frobenius-norm solutions (numbers)", "course/modules/M/M3/L09.html:387-449", "PASS", "Re-derived this round: sum of squared entries 1+1.44+1.44+1=4.88; 2.2^2+(-0.2)^2=4.88; E3 eigenvalues of A0 are 2, 0.5, 0, ||A-A0||_F=0.5 (0.25 under the root). Hunks at L09.html:390 and 445 re-read (marker and prose only).")
row("NOTATION-01", "Every symbol vs notation/notation.json", "notation/notation.json; course/modules/M/M3/L07.html, L08.html, L09.html", "PASS", "notation/notation.json unchanged since fca6bb1 (not in diff). Delta hunks add only the words 'Assuming F1 to F4 of Lesson 4' and prose; no new symbol introduced.")
row("NOTATION-02", "Symbols used with one meaning", "course/modules/M/M3/L07.html, L08.html, L09.html", "PASS", "Hunk re-read: symbols in changed sentences (A, y, P, Q, M, c, B, D, C_0) keep their meanings from earlier in each lesson.")
row("STRUCT-L07-01", "L07 structure and tiers", "course/modules/M/M3/L07.html", "PASS", "check_pages L07 PASS and page_smoke L07 PASS fresh (page_smoke_L07-09.log).")
row("STRUCT-L08-01", "L08 structure and tiers", "course/modules/M/M3/L08.html", "PASS", "check_pages and page_smoke L08 PASS fresh.")
row("STRUCT-L09-01", "L09 structure and tiers", "course/modules/M/M3/L09.html", "PASS", "check_pages and page_smoke L09 PASS fresh.")
carry("DATA-L08-01", "Canon-breaks bullet 2 (data claim)", "course/modules/M/M3/L08.html:291", "No hunk at 291 (hunks at 293, 295).")
row("SIM-LABEL-01", "Labs state SIMULATED data", "tests/labs/M3/lab-M3-L07-1.py, L08-1.py, L09-1.py; page prose", "PASS", "Twin docstrings read this round: L07 'SIMULATED: the 12 observations ... seed 7'; L09 item 4 'SIMULATED: off-diagonal entries 0.5'. L08 lab interpretation says 'SIMULATED panel'.")
row("DAG-01", "Prerequisite closure and meta-row links", "tools/check_dag.py; L07-L09 meta-row links", "PASS", "Fresh check_dag --all: CF1 PASS, AP1 PASS (check_dag.log).")
row("CROSSREF-01", "Cross-lesson citations resolve", "course/modules/M/M3/L07, L08, L09 cross-citations", "PASS", "check_pages --all PASS fresh; new cross-citations this delta are to Lesson 4 Assumptions F1-F4 (L04.html:56-62, which exist). Limited: I did not re-read every Lesson 1/3 citation this round.")
carry("HOURS-01", "Hours on the meta rows and hub split", "course/modules/M/M3/L07.html:2,35; L08.html:2,35; L09.html:2,35; index.html:154-156", "No hunk at lines 2 or 35; index.html not changed.")
row("PROSE-01", "Prose numbers vs displayed values", "course/modules/M/M3/L07.html:125-200; L08.html:146-284; L09.html:193-342", "PASS", "Hunk re-read: L09.html:193 hypothesis block changed (marker added); its numbers -2.4, 0.64, 40 seeds are unchanged. Other cited lines carried (no hunks in 125-200, 146-284 and 194-342 except 193 and 350 which lies outside).")
carry("GRADE-01", "Grade tags and cards grade consistency", "course/modules/M/M3/L07.html:342-346; L08.html:428-434; L09.html:484-493; cards.json", "Cards.json changed only at line 883 (M3-c126 text); cards carry no grade field, so grades are unaffected.")
row("ASSUME-01", "Restating sentences of an F1-F4 result must carry the marker (round-13 rule: why-it-matters, canon-breaks, misconceptions, problem statements, interpretations)", "course/modules/M/M3/L07.html:208, 291, 298; course/modules/M/M3/L08.html:290", "FAIL", "Fixed in this delta and PASS: L07.html:52, 218, 264, 271, 321, 328; L08.html:52, 293, 295, 304, 308, 312, 339, 357, 375, 382, 414; L09.html:193, 350, 360, 390, 445 now carry 'Assuming F1 to F4 of Lesson 4'. Still unmarked: L07.html:208 (misconception: 'Theorem 2.2(c) holds for every response vector y'); L07.html:291 (E1 solution: 'That holds for every response, by Theorem 2.2(c)'); L07.html:298 (E2 solution: 'by Theorem 2.2 that identifies the least-squares solution'); L08.html:290 (misconception: 'Proposition 2.3 covers a common factor on all entries'; Proposition 2.3 needs F1-F4 by its proof at L08.html:359). Fix: prefix each sentence with 'Assuming F1 to F4 of Lesson 4,' as the sibling sentences do.")
carry("ASSUME-02", "Definitions and methods named as assuming F1-F4", "course/modules/M/M3/L08.html:140-141; course/modules/M/M3/L09.html:98, 116, 123, 139, 185, 187, 342, 447", "No hunk at these lines.")
row("ASSUME-03", "Problem R3 and P2 statements carry the marker", "course/modules/M/M3/L08.html:357, 414-416", "PASS", "Re-read this round: P2 statement (L08:357) now opens 'Assuming F1 to F4 of Lesson 4' and supplies the orthonormal eigenbasis hypothesis; R3 statement (L08:414) opens with the marker and its solution (L08:416) uses F3 and F1 only under it.")
carry("ASSUME-04", "Lesson 4 facts used in R1 and E3 solutions", "course/modules/M/M3/L07.html:316 (R1); course/modules/M/M3/L09.html:447 (E3)", "No hunk at these lines; E3 solution marker unchanged.")
carry("CARD-HYP-01", "Hypothesis-bearing cards carry F1-F4 markers", "course/modules/M/M3/cards.json ids M3-c117 to c123, c134 to c137, c143 to c145, c153 to c157, c161, c165, c168, c183", "Card changed by this delta is M3-c126 only (not in this list). Re-read c143, c144, c165, c183: each marker matches the current lesson sentence (L08:304, 308; L09:360; L09:180 vs card).")
carry("CARD-HYP-02", "Cards that quote a proposition's hypotheses", "course/modules/M/M3/cards.json ids M3-c142, M3-c153, M3-c158", "Not touched by the delta.")
carry("CARD-C183", "Card M3-c183 numbers", "course/modules/M/M3/cards.json id M3-c183", "Not touched; 0.04 matches L09.html:180.")
carry("CARD-C161", "Card M3-c161", "course/modules/M/M3/cards.json id M3-c161", "Not touched by the delta.")
carry("CARD-C130", "Card M3-c130", "course/modules/M/M3/cards.json id M3-c130", "Not touched by the delta.")
carry("CARD-C138", "Card M3-c138 vs Remark 2.4", "course/modules/M/M3/cards.json id M3-c138; course/modules/M/M3/L08.html Remark 2.4 (lines 131-133)", "No hunk at 131-133.")
row("CARD-OK-01", "Every card's lesson-bearing claim agrees with current text; no unmarked F1-F4 result in a card", "course/modules/M/M3/cards.json", "PASS", "Scanned all 60 slice cards (L07-L09) fresh: text search for Theorem/Proposition/spectral/eigen/projection/orthonormal/PSD/Lemma/Corollary/clip without 'Assum'. Hits (c116, c124, c128, c129, c131, c132, c139, c149, c158, c159, c160, c163, c164, c166, c167, c174, c175, c181) are definitions, lab outputs, or results needing no F1-F4. c126 now carries the marker and matches L07.html:218.")
row("CARD-DUP-01", "No duplicate cards", "course/modules/M/M3/cards.json", "PASS", "Fresh: 184 cards overall, no duplicate ids and no duplicate fronts.")
carry("CLAIM-L07-01", "Claim at L07.html:206", "course/modules/M/M3/L07.html:206", "No hunk at 206.")
carry("CLAIM-L07-02", "Claim cross-references", "course/modules/M/M3/L07.html:206; L07.html:90; L07.html:316", "No hunk at these lines.")
carry("CLAIM-L07-03", "Problem R1 existence sentence", "course/modules/M/M3/L07.html:206", "No hunk at 206; the 'Assuming F1 to F4' wording is at L07.html:206 (unchanged since round 13).")
carry("REMARK-L08-01", "Remark 2.4 claim 1", "course/modules/M/M3/L08.html:131-133", "No hunk in cited lines.")
carry("REMARK-L08-02", "Remark 2.4 claim 2", "course/modules/M/M3/L08.html:131-133", "No hunk in cited lines.")
carry("REMARK-L08-03", "Remark 2.4 claim 3", "course/modules/M/M3/L08.html:131-133", "No hunk in cited lines.")
carry("PROSE-02", "Cross-references and prose", "course/modules/M/M3/L07.html:206, 316; L08.html:132, 137, 282-284; L09.html:98, 118, 147, 349", "No hunk at these lines (L09 hunks are at 350, 360).")
row("PROCESS-01", "No process words in learner text", "course/modules/M/M3/L07.html, L08.html, L09.html", "PASS", "Fresh grep (case-insensitive) for round, builder, verifier, fragment, audit, agent, workflow, batch N in the three pages: no hits.")
row("REG-01", "Registry and notation register unchanged", "notation/notation.json; course/modules/M/M3/L07.html, L08.html, L09.html", "PASS", "notation/notation.json unchanged; verify_refs offline 0 problems (GATE-10); no citation added or changed by the delta.")

frag = {
 "unit": "M3", "slice": "c", "round": 14,
 "verifier": "independent Haiku verifier, checkout verifyB14-M3-c",
 "pin": "d2b4a874a8deeeb77ce4e2ec8bab7479eaf4f00c", "base": "fca6bb104984c6a724fc214d8073158e610e995a",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyB14-M3-c", "scratch": S.rstrip('/'),
 "verified_at": "2026-10-29", "verdict": "FAIL", "rows": rows, "mutants": [],
 "registry_flags": [], "freshness_flags": [],
 "notes": "Delta since round 13 (fca6bb1..d2b4a87) read hunk by hunk: L07.html 52, 218, 264, 271, 321, 328; L08.html 52, 293, 295, 304, 308, 312, 339, 357, 375, 382, 406, 414; L09.html 193, 350, 360, 390, 445; cards.json 883 (M3-c126). Round-13 ASSUME-03 is fixed. Round-13 ASSUME-01 is fixed for every listed hunk but four unmarked restatements remain (L07.html:208, 291, 298; L08.html:290). The lab twin docstring at tests/labs/M3/lab-M3-L09-1.py lines 6-8 cites Propositions 3.3 and 3.4 without the marker; it is a lab-check claim (numerical), so it is not counted as a finding. Lab twins are demonstrations; no project grader in this slice, so no mutation run (ruling). Carried rows cite only line ranges with no hunk, verified with ledgers/M3/scripts/M3-c-r14/carry_check.py.",
 "summary": "M3-c round 14 FAIL: 1 non-PASS row (ASSUME-01, four unmarked F1-F4 restatements at L07.html:208, 291, 298 and L08.html:290). All gates PASS on d2b4a87 (check_pages, check_dag, check_projects, build_site --check, render diff, run_labs M3 12/12, page_smoke L07-L09, ruff, mypy, pytest -k M3 12, verify_refs offline, fetch_data --check)."
}
json.dump(frag, open('/Users/billyribeiro/.fanout/wt/verifyB14-M3-c/ledgers/M3/M3-c.json', 'w'), indent=1, ensure_ascii=False)
from collections import Counter
print(Counter(r['status'] for r in rows), len(rows))
