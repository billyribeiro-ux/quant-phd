"""Build ledgers/SC1/SC1-b.json: closing delta round 1 for SC1 slice b (95f3f8cb..2a805c83).

Re-verified rows carry new evidence written from this round's commands and reads.
Every other base row is carried with the carry prefix (its cited lines and cards are
outside the delta hunks, see delta_carry_r1.py output in out/delta_carry_r1.txt).
"""
import datetime
import json

BASE = "/Users/billyribeiro/.fanout/frags/F3-SC1-b.round1.json"
OUT = "/Users/billyribeiro/.fanout/wt/verifyG1-SC1-b/ledgers/SC1/SC1-b.json"
PREFIX = ("Carried from round 1 (F3-SC1-b.round1, pin 95f3f8cb; cited lines and card ids byte-identical since that "
          "pin; the delta changes only L05.html:375, index.html:33 and card SC1-c238, none cited by this row): ")
O = "out/d_"  # outputs of this round in ledgers/SC1/scripts/SC1-b-r1/out/

RE = {
    "b-r1-index-lede-finite": ("PASS",
        "Re-verified at 2a805c83. index.html:33 now reads 'that the first-passage time is finite with probability one is "
        "proved in Lesson 8 (Corollary 1.4) under Assumptions A3 and A4 of Lesson 5 and the path conditions of Lesson 8, "
        "Proposition 1.2.' L08.html:87-88 is Corollary 1.4 '(finite with probability one)': 'Assuming A3 and A4 of Lesson 5, "
        "and under H1 and H2 of Proposition 1.2, P(tau_a<infinity)=1.' L08.html:65 is H1 (continuity, B_0=0) and L08.html:66 "
        "is H2 (a>0, H>=0). The proof at L08.html:93 is a limit of probabilities, so 'with probability one' is exact. The "
        "clause names the Proposition 1.2 hypotheses as 'the path conditions' (H1 and H2 together); it omits nothing "
        "Corollary 1.4 uses. Observation (note, not a row): H2 is a level and time condition, so 'the hypotheses H1 and H2 of "
        "Lesson 8, Proposition 1.2' would be the exact wording. Changed line scanned: no banned phrase, no process word "
        "(out/d_scan_changed.txt; out/d_check_pages.txt; delta_carry_r1.py)."),
    "b-r1-card-c238-bound": ("PASS",
        "Re-verified at 2a805c83. cards.json:1879 SC1-c238 back now reads 'An absolute error of at most 5x10^(-11). They do "
        "not show the size or the sign of the error below that.' L05.html:263 says 'The printed digits show no error larger "
        "than 5x10^-11', and L05.html:375 (E2) says 'support an error of at most 5x10^-11'. The bound is exact: the printed "
        "1.0000000000 means the unrounded value lies in [0.99999999995, 1.00000000005] (L05.html:375); recomputed with "
        "Decimal, both endpoints print 1.0000000000 under round-half-even, and under round-half-up the set is half-open. Either "
        "way |error| <= 5x10^-11, so 'at most' is correct and the former strict 'below' was not. Card front and basis (Lab 1, "
        "grade C) unchanged. Card text scanned: no banned, process or scope word beyond the existing ones (out/d_scan_changed.txt)."),
    "b-r1-index-lede-reflection": ("PASS",
        "Re-verified at 2a805c83. index.html:33 reflection clause is byte-identical to the round-1 text (the delta changes "
        "only the finite clause in the same line). L06.html:153-171 is Theorem 2.5 (reflection identity under A3 and A4, "
        "Assumptions list at 155-160); L06.html:185-194 is Proposition 2.7 whose assumptions are A3 (applied to tau_a wedge t) "
        "and A4(b),(c),(g),(h), a subset of A4, so 'under Assumptions A3 and A4 stated in Lesson 5' is not an overstatement. "
        "L06 unchanged in the delta (git diff --stat empty)."),
    "b-lab-L05-gap-carry": ("PASS",
        "Re-verified at 2a805c83. L05.html:256-262 lab output (1.0000000000 at line 261; gaps 5.55e-16 and 3.81e-29 at 256-262); "
        "263 interpretation ('at most 5.55e-16', '2.5 times the epsilon 2.2e-16' = 2.52, checked); 367-368 E1 (ratio "
        "5.55e-16/3.81e-29 = 1.457e13, stated 1.5e13 to two significant figures, checked); 375 E2 now 'an error of at most "
        "5x10^-11' (matches row b-r1-card-c238-bound); 382 E3 unchanged (3.05e-16/2.2e-16 = 1.39, 'about 1.4', checked). "
        "The gap-carry claims are unchanged and consistent."),
    "b-math-L05-E1-E3": ("PASS",
        "Re-verified at 2a805c83. L05.html:364-384: E1 solution (ratio 1.457e13 -> 1.5e13 to 2 s.f., checked with python), "
        "E2 solution at 375 (changed: 'an error of at most 5x10^-11'; the interval [0.99999999995, 1.00000000005] and the "
        "non-identifiable 1e-16 vs 1e-12 remark are unchanged and correct), E3 solution at 382 (3.05e-16 / 2.2e-16 = 1.386, "
        "'about 1.4' correct). Line 368 and 382 unchanged. Solution text consistent with the card SC1-c238 at 2a805c83."),
    "b-num-L05": ("PASS",
        "Re-verified at 2a805c83. Numbers at L05.html:255-263 (lab output at 255-262), 263 (prose), 365-368 (E1), 372-375 "
        "(E2, changed wording, same numbers 5x10^-11 and 1.0000000000), 379-382 (E3), 456-458 and 497-499 (quiz, unchanged). "
        "Independent recomputation: ledgers/SC1/scripts/SC1-b-r1/out/d_recompute_b_r14.txt is byte-identical to the stored "
        "round-14 output (ledgers/SC1/scripts/SC1-b-r14/out/recompute_b_r14.txt), including 'E2: unrounded interval "
        "[0.99999999995, 1.00000000005] width/2 = 5e-11' and integrals 1.00000000000000."),
    "b-r1-hunk-intersection": ("PASS",
        "Re-verified at 2a805c83 with ledgers/SC1/scripts/SC1-b-r1/delta_carry_r1.py over git diff -U0 95f3f8cb..2a805c83. "
        "New-side hunks in the SC1 slice paths: L05.html [375], index.html [33], cards.json SC1-c238 (line 1879). No hunk in "
        "L01-L04, L06-L08, project.html, notation/, references/references.json, tools/ or course/assets/. Intersection with "
        "every slice-b cited line: only L05:375 (rows b-lab-L05-gap-carry, b-math-L05-E1-E3, b-num-L05), index:33 (rows "
        "b-r1-index-lede-finite, b-r1-index-lede-reflection) and SC1-c238 (row b-r1-card-c238-bound), all re-verified above."),
    "b-check-pages": ("PASS",
        "Re-run at 2a805c83: .venv/bin/python tools/check_pages.py --unit SC1 -> 'check_pages SC1: PASS', exit 0 "
        "(out/d_check_pages.txt). The BANNED pattern list (tools/check_pages.py:58-74) applied to L05.html:375 and "
        "index.html:33 gives no hit."),
    "b-check-dag": ("PASS",
        "Re-run at 2a805c83: tools/check_dag.py --unit SC1 -> 'check_dag SC1: PASS', exit 0 (out/d_check_dag.txt). The changed "
        "lines add no concept link or new concept name (L05.html:375 and index.html:33 are plain text; c238 text has none)."),
    "b-page-smoke": ("PASS",
        "Re-run at 2a805c83: tools/page_smoke.py --unit SC1 --pages index L05 -> both PASS, 'page_smoke SC1: PASS' "
        "(out/d_page_smoke_index_L05.txt); --pages L04 L06 -> both PASS, 'page_smoke SC1: PASS' (out/d_page_smoke_L04_L06.txt). "
        "Shared assets (course/assets, tools) are unchanged in the delta."),
    "b-run-labs": ("PASS",
        "Re-run at 2a805c83: tools/run_labs.py --unit SC1 -> 'run_labs SC1: PASS (11/11)', exit 0 (out/d_run_labs_unit.txt); "
        "--page L05 -> PASS (out/d_run_labs_L05.txt). The three slice-b twins are byte-identical since the pin."),
    "b-pytest-tooling": ("PASS",
        "Re-run at 2a805c83: pytest tests/test_labs.py tests/test_page_checks.py -k SC1 -> exit 0 (out/d_pytest_sc1.txt); "
        "pytest tests/test_run_labs.py -> exit 0 (out/d_pytest_run_labs.txt)."),
    "b-lab-lint": ("PASS",
        "Re-run at 2a805c83: .venv/bin/ruff check . -> 'All checks passed!' exit 0 (out/d_ruff_check.txt); .venv/bin/ruff "
        "format --check . -> '555 files already formatted' exit 0 (out/d_ruff_format.txt). mypy not re-run: no .py file in "
        "the SC1 slice paths changed in the delta."),
    "b-verify-refs-r14-offline": ("PASS",
        "Re-run at 2a805c83: .venv/bin/python tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', "
        "exit 0 (out/d_verify_refs_offline.txt). references/references.json unchanged in the delta. The live run was not "
        "repeated (no network call in a closing delta)."),
    "b-recompute-r11": ("PASS",
        "Re-run at 2a805c83: ledgers/SC1/scripts/SC1-b-r14/recompute_b_r14.py via python -I; output byte-identical to the "
        "stored round-14 output (out/d_recompute_b_r14.txt vs ledgers/SC1/scripts/SC1-b-r14/out/recompute_b_r14.txt)."),
    "b-recompute-r5": ("PASS",
        "Re-run at 2a805c83: recompute_b_r14.py output byte-identical to the stored round-14 output (out/d_recompute_b_r14.txt)."),
    "b-r13-numeric-recompute-script": ("PASS",
        "Re-run at 2a805c83: recompute_b_r14.py exit 0, output identical to the stored output (out/d_recompute_b_r14.txt)."),
    "b-r1-cards-numbered-refs": ("PASS",
        "Re-run at 2a805c83 with ledgers/SC1/scripts/SC1-b-r1/cards_check_b_r1.py (python -I, ROOT argument): 92 slice cards, "
        "the same seven literal flags as round 1 (c074, c195, c198, c199, c200, c214, c222), all adjudicated false positives "
        "(list labels and span-numbered headings), no new flag, SC1-c238 not flagged (out/d_cards_check.txt)."),
    "b-cards-duplicates": ("PASS",
        "Re-run at 2a805c83 over the whole cards.json: 'duplicate fronts: []', 'duplicate backs: []', 'duplicate ids: []', "
        "total cards 227 (out/d_cards_check.txt). The one changed card (c238) shares no front or back with another card."),
    "b-r1-build-site": ("PASS",
        "Re-run at 2a805c83: tools/build_site.py --check -> 'site data current: 6 outputs', exit 0 (out/d_build_site_check.txt)."),
    "b-r13-delta-changed-hunks": ("PASS",
        "Re-verified at 2a805c83: cited lines L05.html:331-335 and index.html:184 are outside the delta hunks (delta_carry_r1.py); "
        "the changed-card ids of the earlier deltas (c099, c105, c119, c122, c197, c200, c214) are byte-identical to pin "
        "95f3f8cb (per-card JSON compare; only SC1-c238 differs in the delta)."),
    "b-banned-phrases": ("PASS",
        "Re-verified at 2a805c83: whole-page BANNED scan by tools/check_pages.py (out/d_check_pages.txt, PASS); the only "
        "changed page lines (L05.html:375, index.html:33) and the changed card (c238) were scanned with the same pattern list: "
        "no hit (out/d_scan_changed.txt). Whole-file results can change only on the changed lines, since the rest of each file is byte-identical."),
    "b-process-words": ("PASS",
        "Re-verified at 2a805c83 on the changed lines only (the rest of each file is byte-identical): L05.html:375 and "
        "index.html:33 and cards.json SC1-c238 contain no process word (round, verifier, ledger, fragment, fixer, ruling, delta, "
        "'earlier', 'corrected'); 'round' at L05.html:375 is the verb 'rounds to ten decimal places' and 'fixed' at index.html:33 "
        "is 'fixed-time form' of Theorem 2.5 (out/d_scan_changed.txt, scan_changed_r1.py)."),
    "b-scope-words-r5": ("PASS",
        "Re-verified at 2a805c83 on the changed lines: L05.html:375 changes 'below' to 'of at most' and keeps the existing "
        "'only' in the conclusion sentence (unchanged claim, no new scope word); index.html:33 adds no scope word from the list "
        "(only, all, always, every, any, same, drives, exactly). The rest of each file is byte-identical."),
    "b-scope-words-r11": ("PASS",
        "Re-verified at 2a805c83 on the changed lines, as in b-scope-words-r5: no new scope word in L05.html:375, index.html:33 "
        "or SC1-c238."),
    "b-notation-r5": ("PASS",
        "Re-verified at 2a805c83 on the changed lines: L05.html:375 changes words only and keeps \\(5\\times10^{-11}\\); the "
        "index.html:33 clause and card SC1-c238 introduce no symbol. The rest of each file is byte-identical."),
    "b-notation-r11": ("PASS",
        "Re-verified at 2a805c83 on the changed lines, as in b-notation-r5; notation/notation.json unchanged in the delta."),
    "b-dag-D1-D9": ("PASS",
        "Re-verified at 2a805c83: check_dag SC1 PASS (out/d_check_dag.txt); the changed lines add no concept link and no name "
        "of a concept outside the closure."),
}

NEW = [
    {"id": "b-delta-inventory-95f3f8cb-2a805c83", "check": "2.9 delta inventory (ruling 30)",
     "location": "git diff --stat 95f3f8cb..2a805c83 over the slice paths",
     "status": "PASS",
     "evidence": "course/modules/SC/SC1: L05.html 1 line (375), index.html 1 line (33), cards.json 1 line (SC1-c238 back, "
                 "line 1879). No change to L04.html, L06.html, L01-L03, L07, L08, project.html, notation/, references/, "
                 "tests/labs/SC1, tools/, course/assets/. Outside the slice: plans/FINAL-ARCHITECT-RULINGS.md (rulings 38-39 "
                 "appended at lines 137-147), tests/labs/E4, tests/labs/M3, tests/test_lx1_project_lab3.py, other units' pages, "
                 "ledgers/. Command: git diff --stat 95f3f8cb..2a805c83 -- course/modules/SC/SC1 tests/labs/SC1 notation "
                 "references/references.json plans/SC1-build-plan.md plans/SC1-open-items.md (3 files changed, 3 insertions, 3 "
                 "deletions)."},
    {"id": "b-ruling-38-39-scope", "check": "2.9 rulings 38 and 39 applicability to slice b",
     "location": "plans/FINAL-ARCHITECT-RULINGS.md:137-147; plans/FINAL-ARCHITECT-RULINGS.md:114-117 (ruling 33)",
     "status": "PASS",
     "evidence": "Rulings 38 (E3 glyph-level notation: Xi, Omega, exponent b of L03) and 39 (E3 L07, L08 title-only registry "
                 "records) name E3 pages, and ruling 33 (its footer sentence) is written for E3. None of them names an SC1 "
                 "page, symbol or card, so no SC1 slice-b row changes. The SC1 footers carry no 'Each graded result carries' "
                 "sentence (grep over L04-L06 empty), and the rulings do not require one for SC1."},
]

def main():
    base = json.load(open(BASE, encoding="utf-8"))
    rows = []
    for r in base["rows"]:
        if r["id"] in RE:
            status, ev = RE[r["id"]]
            rows.append({"id": r["id"], "check": r["check"], "location": r["location"], "status": status, "evidence": ev})
        else:
            rows.append({"id": r["id"], "check": r["check"], "location": r["location"], "status": "PASS",
                         "evidence": PREFIX + r["evidence"]})
    rows += NEW
    assert len({r["id"] for r in rows}) == len(rows)
    assert {r["id"] for r in base["rows"]} <= {r["id"] for r in rows}
    fails = [r["id"] for r in rows if r["status"] != "PASS"]
    re_count = sum(1 for r in base["rows"] if r["id"] in RE)
    frag = {
        "unit": "SC1",
        "slice": "b",
        "round": 1,
        "verifier": "Claude Haiku 5.5, independent verifier (closing delta, ruling 30), slice SC1-b round 1",
        "pin": "2a805c831410ab77c38c227f7e121e8537193ce9",
        "base": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672 (base fragment ~/.fanout/frags/F3-SC1-b.round1.json, FAIL with 2 rows); "
                "delta 95f3f8cb..2a805c83",
        "checkout": "/Users/billyribeiro/.fanout/wt/verifyG1-SC1-b",
        "scratch": "/Users/billyribeiro/.fanout/wt/verifyG1-SC1-b/ledgers/SC1/scripts/SC1-b-r1",
        "verified_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "verdict": "PASS" if not fails else "FAIL",
        "rows": rows,
        "mutants": [],
        "registry_flags": base["registry_flags"],
        "freshness_flags": [],
        "notes": (
            "Closing delta round 1 for SC1-b, base pin 95f3f8cb (F3 round-1 fragment, FAIL with two rows: b-r1-index-lede-finite "
            "and b-r1-card-c238-bound). The delta 95f3f8cb..2a805c83 changes three slice-b lines: L05.html:375 (E2 wording "
            "'an error of at most 5x10^-11'), index.html:33 (lede: 'finite with probability one ... Corollary 1.4 ... path "
            "conditions of Lesson 8, Proposition 1.2') and cards.json SC1-c238 back (same wording as L05:375). Both base FAIL "
            "rows are re-verified and now PASS: the lede matches L08 Corollary 1.4 and its hypotheses H1/H2, and 'at most' is the "
            "exact bound (the printed 1.0000000000 gives |error| <= 5x10^-11). Every row whose cited lines or cards touch the "
            "delta was re-verified (L05:364-384, L05:255-263, index:33, SC1-c238, the whole-page and whole-file scans on the "
            "changed lines). Every other row is carried with the carry prefix; its cited lines and cards are byte-identical. "
            "Gates re-run at 2a805c83 (out/d_*.txt): check_pages SC1, check_dag SC1, build_site --check, verify_refs --offline, "
            "page_smoke SC1 pages index/L04/L05/L06, run_labs SC1 (11/11), pytest SC1 label and page-check tests and test_run_labs, "
            "ruff check and format repo-wide, recompute script (identical to round 14), cards check script. Mutants: none "
            "(ruling 37, and slice b has no grader or project). Observations (notes, not rows): (1) the index.html:33 clause calls "
            "H1 and H2 'the path conditions', but H2 (a>0, H>=0) is a level and time condition; the exact wording is 'the "
            "hypotheses H1 and H2 of Lesson 8, Proposition 1.2'. (2) L05:375 and L05:263 state the bound for round-to-nearest "
            "with ties to even; under round-half-up the set is half-open, and the bound |error| <= 5x10^-11 holds either way. "
            "(3) The seven literal card-reference flags of cards_check_b_r1.py remain false positives (list labels, span "
            "headings). (4) Rulings 38 and 39 are E3-scoped; no SC1 row depends on them. Not checked: the full line-by-line reading "
            "of L04, L05 and L06 (byte-identical to the pin, carried as before); live verify_refs (no network); mypy "
            "(no Python in slice b changed); the other units' delta (outside slice b)."
        ),
        "summary": (f"{len(rows)} rows: {sum(1 for r in rows if r['status']=='PASS')} PASS, {len(fails)} non-PASS; "
                    f"{re_count} base rows re-verified from scratch (2 base FAIL rows now PASS, "
                    f"{re_count - 2} base PASS rows re-verified because their subject changed or was re-run), "
                    f"{len(base['rows']) - re_count} base rows carried, {len(NEW)} new inventory rows, 0 mutants."),
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(frag, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("wrote", OUT, "rows", len(rows), "non-PASS", fails, "re-verified", re_count)

if __name__ == "__main__":
    main()
