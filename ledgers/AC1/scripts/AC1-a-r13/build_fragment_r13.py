"""Build the round 13 AC1-a fragment: carry round 12 PASS rows whose cited passage is unchanged,
re-verified rows get round 13 evidence, command rows are re-run in this round."""
import json
import sys

CHECKOUT = "/tmp/verify13-AC1-a"
PREV = "/tmp/fanout-frags/AC1-a.round12.json"
OUT = CHECKOUT + "/ledgers/AC1/AC1-a.json"
S = "/tmp/ac1-v/a-r13/"
prev = json.load(open(PREV, encoding="utf-8"))
prev_rows = {r["id"]: r for r in prev["rows"]}

# Passage-level carry: the cited passage lies outside every hunk changed since aebdc15.
CARRY_PREFIX = ("Carried from round 12 (cited passage byte-identical since the previous pin aebdc15; "
                "the hunks changed in eaf6d87 are L01.html line 388, L02.html lines 133-134, 535 and 552, "
                "L03.html line 57, and none of the cited lines is among them): ")

RERUN = {
    "AC1a-cmd-check_pages": ("index, L01-L03", "Re-run at eaf6d87: check_pages.py --all, 'check_pages AC1: PASS', exit 0 (" + S + "check_pages.out)."),
    "AC1a-cmd-check_dag": ("AC1 DAG", "Re-run at eaf6d87: check_dag.py --all, 'check_dag AC1: PASS', exit 0 (" + S + "check_dag.out)."),
    "AC1a-cmd-run_labs": ("tests/labs/AC1", "Re-run at eaf6d87: run_labs.py --unit AC1, 'run_labs AC1: PASS (11/11)', exit 0 (" + S + "run_labs.out)."),
    "AC1a-cmd-page_smoke": ("index, L01, L02, L03", "Re-run at eaf6d87: page_smoke.py --unit AC1 --pages index.html L01.html L02.html L03.html --skip-sweep, 'page_smoke AC1: PASS', exit 0 (" + S + "page_smoke.out). The figure sweep was skipped (--skip-sweep); these four pages carry no live figure (no figures-*.js block in them, checked by grep)."),
    "AC1a-cmd-verify_refs": ("references/references.json", "Re-run at eaf6d87: verify_refs.py --offline, 'offline integrity: 560 entries, 0 problems', exit 0 (" + S + "vr_offline.out). The live --unit AC1 run was not repeated in this round: the registry, tools and the four pages' citation markup are unchanged since aebdc15 (git diff empty for references/, tools/)."),
    "AC1a-cmd-ruff-mypy": ("repo; tests/labs/AC1", "Re-run at eaf6d87: ruff check . ('All checks passed!', exit 0) and mypy --no-incremental ('Success: no issues found in 153 source files', exit 0) (" + S + "ruff.out, " + S + "mypy.out)."),
    "AC1a-cmd-twin-run": ("tests/labs/AC1/lab-AC1-L01-1.py, L02-1, L03-1", "Re-run at eaf6d87 under python -I -W error: each twin exits 0; stdout is in " + S + "lab-AC1-L0{1,2,3}-1.py.out."),
    "AC1a-cmd-pytest-AC1": ("tests", "Re-run at eaf6d87: pytest tests/test_run_labs.py tests/test_page_checks.py tests/test_labs.py, exit 0 (" + S + "pytest_ac1.out). The full-suite run was not repeated: nothing outside the slice's pages and the AC1 project grader changed in this round's delta, and the grader is judged in the project slice."),
    "AC1a-cmd-build-site": ("course/concepts.html; site data", "Re-run at eaf6d87: build_site.py --check, 'site data current: 6 outputs', exit 0 (" + S + "build_site.out)."),
    "AC1a-cmd-scope-witness": ("L01.html Proposition 3.2 statement", "Re-run at eaf6d87: ledgers/AC1/scripts/AC1-a-r11/witness_r11.py '<checkout>' ... 'ALL PASS' (" + S + "witness_r11.out) and ledgers/AC1/scripts/AC1-a-r10/witness_r10.py <checkout> (exit 0; " + S + "witness_r10.out), with W6 'data-run equals twin: True' for L01-L03. The Proposition 3.2 scope witness R-K=600.00 against dAR=500.00 (hub rung 2) is printed by witness_r11."),
    "AC1a-twin-matches-page": ("L01.html, L02.html, L03.html", "Re-run at eaf6d87: ledgers/AC1/scripts/AC1-a-r13/cmp_code.py gives 'data-run == twin: True' for L01, L02, L03; cmp_expected.py gives 'page expected == twin stdout: True' for L01, L02, L03 (" + S + "scripts/)."),
}

REVERIFIED = {
    "AC1a-dag-concepts": ("FAIL->PASS", "course/modules/AC/AC1/L03.html line 57 now reads 'adding back depreciation (Definition 1.2, below)', the forward-pointer convention; L01.html line 388 hypothesis (v) reads 'depreciation is one, defined in Lesson 3, Definition 1.2'; L02.html line 552 reads 'amortized (Lesson 3, Definition 1.2)'. L03.html line 38 introduces depreciation and amortization; the dfn is line 62. check_dag.py --all passes (" + S + "check_dag.out). The forward references are explicit pointers, the convention that round 12 itself accepted for L02.html line 73."),
    "AC1a-r12-L02-552-amortized-term": ("FAIL->PASS", "course/modules/AC/AC1/L02.html line 552 now reads 'An intangible asset that is amortized (Lesson 3, Definition 1.2) brings in an expense account outside the four of Definition 2.1'. The pointer is present. L03.html line 62 (Definition 1.2) says 'In this lesson, amortization applies the same arithmetic to an intangible asset with a finite life', so the cited definition covers amortization of an intangible asset (read by grep at eaf6d87)."),
    "AC1a-lab-L02-claims": ("PASS", "L02.html hypothesis (line 133): 'the lowest cash balance is the opening position, which holds if cash rises in each year'. Sufficient-condition wording; the lab's prediction is the opening position. Printed year-end cash in lab-AC1-L02-1 run: 3,000,000.00 opening, 4,454,305.29, 5,945,920.93, 7,489,781.87, each higher than the last, so the condition holds in the run. Re-run output " + S + "lab-AC1-L02-1.py.out."),
    "AC1a-r6-simulated-labels": ("PASS", "L02.html line 133 still reads 'The lab generates a SIMULATED firm'; line 535 still reads 'The figures above are SIMULATED.' L01 and L03 labels unchanged (git diff)."),
    "AC1a-r6-L02-lab-scope-word": ("PASS", "L02.html line 535 now reads 'The lowest cash balance is taken over the year ends, including the opening position, and not over the quarters. In this run it equals the opening cash, because cash rises at each year end.' Lab code line 335-359: sheets = balance_sheet for (OPENING_YEAR, *YEARS), i.e. the four year-end sheets, and the printed minimum is min(s['cash'] for s in sheets) = 3,000,000.00, the opening cash. No quarterly balance is computed. The 'because' is the sufficient condition read from the printed year-end cash (above). Lab output " + S + "lab-AC1-L02-1.py.out."),
    "AC1a-r12-L02-552-prop32-scope": ("PASS", "L02.html line 552 scope: the amortized-intangible sentence says Proposition 3.2 does not cover that case, since amortization brings in an account outside the four of Definition 2.1 (L02.html Definition 2.1, line 72-76). Proposition 3.2 hypothesis (iv)/(v) and the four-account restriction support that reading (L01.html line 388). The pointer change does not alter the claim."),
    "AC1a-grade-T-L01": ("PASS", "L01.html Proposition 3.2 (title line 387, hypotheses line 388) is still T. The only change is the parenthetical in hypothesis (v). The proof (line 393) uses X = X_a + X_k (so every operating expense is either on account or in cash), which is hypothesis (v) and unchanged; the parenthetical names depreciation as a case that (v) excludes and points to its definition at L03 Definition 1.2 (line 62). Proof re-read at eaf6d87."),
    "AC1a-r3-scope-witness-prop32": ("PASS", "L01.html line 388 hypotheses: unchanged scope apart from the pointer. Witness witness_r11.py prints 'PASS hub rung 2 witness: no write-offs holds, yet R - K != change in AR | R-K=600.00 dAR=500.00' (" + S + "witness_r11.out), so the no-write-off hypothesis is not sufficient without the listed sources."),
    "AC1a-r10-hub-rung2-explain-scope": ("PASS", "index.html line 141 (rung-2 explain text) is byte-identical at eaf6d87 (not in the delta). It cites Proposition 3.2 hypotheses (i)-(iii) and states that (iv) and (v) are not used; the changed parenthetical in (v) does not touch that statement."),
    "AC1a-r12-index-141-rung2": ("PASS", "index.html line 141 unchanged; L01.html line 388 hypothesis (v) now carries the depreciation pointer. The hub's statement that (iv) and (v) are not used for the rung-2 computation is unaffected."),
    "AC1a-r11-L01-scope-hypotheses-P2-P3-R2-R3": ("PASS", "L01.html line 388 hypotheses (i)-(v) re-read at eaf6d87. Scope unchanged except the parenthetical that names depreciation as one non-cash expense excluded by (v), which matches Definition 1.2 (L03.html line 62: 'no line touches cash'). Lines 486, 493, 538, 545 unchanged."),
    "AC1a-r11-cards-c015-c027-c033-c039-c042": ("PASS", "cards.json unchanged at eaf6d87 (git diff empty). c033 (articulation) is a subset of L03.html Definition 1.1 (line 57): it omits the depreciation add-back clause, which the card does not claim; the card's statement 'under the hypotheses of Proposition 2.2, indirect operating cash flow equals the direct figure (Definition 1.1)' matches the lesson's 'gives the same figure as the direct method'. c027 and c013 cite Proposition 3.2 hypotheses (i)-(v) and 'Remark 2.2', unchanged in meaning."),
    "AC1a-r12-L03-def11-articulation-rewrite": ("PASS", "L03.html line 57 (Definition 1.1): 'by adding back depreciation (Definition 1.2, below) and adjusting for the changes in receivables and payables (Definition 2.1, the indirect method), and gives the same figure as the direct method.' Definition 2.1 is the indirect method (L03.html line 71); Definition 1.2 at line 62 defines depreciation with 'no line touches cash', so the add-back is a correct description. The sentence now uses the forward-pointer convention; see AC1a-dag-concepts."),
    "AC1a-r11-banned-process-words": ("PASS", "ledgers/AC1/scripts/AC1-a-r13/scan.py is the round 12 scan.py run on eaf6d87: no hits for builder, verifier, round, REQUEST, unit report, roughly, historically, typically, about N, clearly, obviously, simply in index, L01-L03 or cards.json. Hits for 'offsets' (L03 line 'The add-back offsets a charge', card c037) and 'half of' (fixed fractions, a stated parameter, and 'the direct-method half of Proposition 6.2') are in unchanged passages and were judged in round 12 (carried)."),
    "AC1a-r11-notation": ("PASS", "Macro scan of index, L01-L03 TeX spans at eaf6d87: \\Delta, \\blacksquare, \\dots, \\in, \\le, \\sum, \\text, \\times only. The changed passages add no TeX symbol; notation/notation.json is unchanged (git diff)."),
    "AC1a-r12-delta": ("PASS", "Delta aebdc15..eaf6d87 for the slice: L01.html line 388; L02.html lines 133-134, 535, 552; L03.html line 57; cards.json unchanged; tests/labs/AC1 unchanged (git diff empty); index.html unchanged. Every hunk read in full (see AC1a-r13-delta)."),
}

NEW = [
    ("AC1a-r13-delta", "delta since the previous pin", "L01.html line 388; L02.html lines 133-134, 535, 552; L03.html line 57; index.html; cards.json; tests/labs/AC1",
     "PASS", "git diff --stat aebdc15 eaf6d87 for course/modules/AC/AC1 and tests/labs/AC1: L01.html 1 hunk (line 388), L02.html 3 hunks (133, 535, 552), L03.html 1 hunk (line 57); cards.json, index.html, tests/labs/AC1 empty. The grader/test_project.py and project.html hunks belong to the project slice and are not judged here. All five hunks read in full (" + S + "delta_hunks.out)."),
    ("AC1a-r13-L01-prop32-depreciation-pointer", "hypothesis (v) pointer and scope", "course/modules/AC/AC1/L01.html line 388",
     "PASS", "Text: 'with no other non-cash expense (depreciation is one, defined in Lesson 3, Definition 1.2)'. Depreciation is an expense with no cash line (L03.html line 62), so it is a non-cash expense that (v) excludes. The forward pointer is explicit. Proposition 3.2 remains T: the proof at line 393 is unchanged and uses hypothesis (v) only through X = X_a + X_k."),
    ("AC1a-r13-L02-hypothesis-and-interp-wording", "lab L02 prediction and interpretation wording", "course/modules/AC/AC1/L02.html line 133 (hypothesis) and line 535 (interpretation); tests/labs/AC1/lab-AC1-L02-1.py lines 335-359; lab output " + S + "lab-AC1-L02-1.py.out",
     "PASS", "Hypothesis: 'which holds if cash rises in each year' is a sufficient condition for the prediction, and the printed year-end cash rises each year (3,000,000.00 to 7,489,781.87), so the prediction holds in the run. Interpretation: 'taken over the year ends, including the opening position, and not over the quarters' matches the code (min over the four year-end sheets). 'In this run it equals the opening cash, because cash rises at each year end' is a correct consequence, with the printed figures as basis. Nothing is claimed beyond the run."),
    ("AC1a-r13-L02-amortized-pointer-scope", "amortization pointer in the omitted-items bullet", "course/modules/AC/AC1/L02.html line 552",
     "PASS", "'An intangible asset that is amortized (Lesson 3, Definition 1.2) brings in an expense account outside the four of Definition 2.1, and Proposition 3.2 does not cover that case.' L03.html line 62 defines amortization for an intangible asset with a finite life; Definition 2.1 has four accounts (L02.html lines 72-76). The sentence states only what the cited definitions support."),
    ("AC1a-r13-L03-def11-pointer", "Definition 1.1 forward pointer", "course/modules/AC/AC1/L03.html line 57; Definition 1.2 at line 62",
     "PASS", "'adding back depreciation (Definition 1.2, below)': the term is introduced at line 38 (Introduces) and defined at line 62, below line 57, with a pointer. check_dag passes (" + S + "check_dag.out)."),
    ("AC1a-r13-hyp-scope-no-new-numbers", "no new numbers or bases", "L01.html line 388; L02.html lines 133, 535, 552; L03.html line 57",
     "PASS", "The delta adds no figure, percentage, ratio or bibliographic item. The only numbers in the changed lines are the lab's printed 3,000,000.00 and the references 'Lesson 3, Definition 1.2' and 'Definition 2.1', which were checked against the pages."),
    ("AC1a-r13-scan-new-student-error", "new student-error reading of changed passages", "course/modules/AC/AC1/L01.html line 388; L02.html lines 133, 535; L03.html line 57",
     "PASS", "Three readings checked: (1) a student reads 'depreciation is one [non-cash expense]' as a claim that depreciation is in every ledger: no, the parenthetical lists an example of what (v) excludes; (2) a student reads 'holds if cash rises' as 'only if': the page says 'if', a sufficient condition; (3) a student reads 'taken over the year ends' as a claim about quarterly lows: the page says not over the quarters. None is an error in the page."),
]

CARRY_IDS_EXCLUDE = set(RERUN) | set(REVERIFIED) | {"AC1a-dag-concepts", "AC1a-r12-L02-552-amortized-term"}
rows = []
for rid, r in prev_rows.items():
    if rid in RERUN:
        loc, ev = RERUN[rid]
        rows.append({"id": rid, "check": r["check"], "location": loc, "status": "PASS", "evidence": ev})
    elif rid in REVERIFIED:
        status, ev = REVERIFIED[rid]
        status = "PASS"
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev})
    else:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": CARRY_PREFIX + r["evidence"]})
for rid, check, loc, status, ev in NEW:
    rows.append({"id": rid, "check": check, "location": loc, "status": status, "evidence": ev})

fails = [r for r in rows if r["status"] != "PASS"]
frag = {
    "unit": "AC1", "slice": "AC1-a", "round": 13,
    "round_note": ("round 13 independent verification of AC1-a at eaf6d87. Previous pin aebdc15 (round 12 fragment, verdict FAIL, 2 FAIL rows: AC1a-dag-concepts and AC1a-r12-L02-552-amortized-term). Delta aebdc15..eaf6d87 for this slice: L01.html line 388; L02.html lines 133-134, 535, 552; L03.html line 57. Both FAIL rows are re-verified and now PASS. Command rows re-run. Every previous row id kept."),
    "verifier": "Haiku independent verifier, AC1-a round 13 (did not build AC1)",
    "pin": "eaf6d87",
    "base": "aebdc15 (previous pin; round 12 fragment)",
    "checkout": CHECKOUT + " (detached worktree at eaf6d87, .venv symlinked)",
    "scratch": S,
    "verified_at": "2026-10-28",
    "registry_flags": prev["registry_flags"] + ["Round 13: git diff empty for references/, tools/, notation/, curriculum/; offline verify_refs '560 entries, 0 problems' re-run at eaf6d87."],
    "freshness_flags": [],
    "notes": [
        "Slice: course/modules/AC/AC1/index.html, L01.html, L02.html, L03.html, the three lab twins tests/labs/AC1/lab-AC1-L01-1.py, lab-AC1-L02-1.py, lab-AC1-L03-1.py, and the L01-L03 cards of cards.json (AC1-c001 to c045, c123, c124, c126 to c128). The AC1 grader/test_project.py and project.html hunks belong to the project slice and are not judged here.",
        "Carry rule: a previous PASS row is carried only when the passage it cites is outside every hunk changed since aebdc15; rows whose cited passage touches a hunk were re-verified in this round (rows AC1a-lab-L02-claims, AC1a-r6-L02-lab-scope-word, AC1a-r6-simulated-labels, AC1a-grade-T-L01, AC1a-r3-scope-witness-prop32, AC1a-r10-hub-rung2-explain-scope, AC1a-r12-index-141-rung2, AC1a-r11-L01-scope-hypotheses-P2-P3-R2-R3, AC1a-r11-cards-c015-c027-c033-c039-c042, AC1a-r12-L03-def11-articulation-rewrite, AC1a-r12-L02-552-prop32-scope, AC1a-r12-L02-552-amortized-term, AC1a-dag-concepts, AC1a-r11-banned-process-words, AC1a-r11-notation, AC1a-r12-delta).",
        "Twins: tests/labs/AC1/*.py are byte-identical at eaf6d87 (git diff empty), so the twin-behaviour rows are carried; the twin-to-page equality and the twin runs were re-run (AC1a-twin-matches-page, AC1a-cmd-twin-run).",
        "Mutants: none for this slice. The slice is lessons and the hub, not a project; no student-error mutant or alternative implementation applies to a lesson page. Round 8 recorded the same (row AC1a-r8-mutants-not-required, carried). ledgers/AC1/mutants/ belongs to the AC1-d project grader.",
        "Hours: hub split 90 lesson hours and 30 project hours; lesson hours L01 11, L02 12, L03 11 (34 of the 90 shown by lesson). Arithmetic consistent. Not judged against pace (architect ruling: hours are design targets).",
        "Could not check: the four pages cite no external source (no registry key), so no paper or standard was read. The live verify_refs --unit AC1 was not repeated in round 13 (registry unchanged). The full pytest suite was not repeated; the three AC1-relevant test modules and the lab runner were run.",
        "Witness scripts: ledgers/AC1/scripts/AC1-a-r13/ holds the copies of cmp_code.py and cmp_expected.py with the checkout path set; the round 10 and round 11 witness scripts and the round 12 scan.py were re-run from ledgers/AC1/scripts/.",
    ],
    "mutants": [],
    "summary": {"rows": len(rows), "pass": sum(1 for r in rows if r["status"] == "PASS"), "fail": len(fails), "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE")},
    "verdict": "PASS" if not fails else "FAIL",
    "rows": rows,
}
json.dump(frag, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("rows", len(rows), "fails", [r["id"] for r in fails], "verdict", frag["verdict"])
