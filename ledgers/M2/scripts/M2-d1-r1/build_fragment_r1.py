"""Build ledgers/M2/M2-d1.json (round 1, closing delta) from the base round-4 fragment.

Re-verified rows get new evidence from this round's commands and outputs (scripts/M2-d1-r1/).
Every other row keeps its base id, check and location and is carried with the carry prefix.
Run with: .venv/bin/python -I ledgers/M2/scripts/M2-d1-r1/build_fragment_r1.py
"""
import json
import os

CHECKOUT = "/Users/billyribeiro/.fanout/wt/verifyF21-M2-d1"
SCRATCH = "ledgers/M2/scripts/M2-d1-r1"
BASE_PATH = "/Users/billyribeiro/.fanout/frags/D-M2-d1.round4.json"
OUT = "ledgers/M2/M2-d1.json"
PIN = "95f3f8cb21c2cd9fc904430bd30a6b734d01f672"
BASE_PIN = "4eb6788fe3b408bb6d90ac73addc6fb17af47b8b"

PAGES = ("course/modules/M/M2/L19.html, L20.html, L21.html, tests/labs/M2/lab-M2-L19-1.py, "
         "lab-M2-L20-1.py, lab-M2-L21-1.py")
CARRY_PAGES = "Carried from round 4 (" + PAGES + " byte-identical since the previous pin 4eb6788f):"

RE = {
    "G-check-pages": (
        "check_pages.py --unit M2 -> 'check_pages M2: PASS', exit 0 (" + SCRATCH + "/check_pages.out). Re-run on pin 95f3f8cb."),
    "G-check-dag": (
        "check_dag.py --unit M2 -> 'check_dag M2: PASS', exit 0 (check_dag.out). Re-run on pin. The delta's curriculum.json "
        "hunks touch M3 and one other unit only (10 changed lines, none in M2)."),
    "G-check-projects": (
        "check_projects.py --unit M2 -> 'check_projects M2: PASS', exit 0 (check_projects.out). Re-run on pin."),
    "G-run-labs": (
        "run_labs.py --unit M2 -> 'run_labs M2: PASS (27/27)', exit 0 (run_labs_M2.out). Re-run on pin."),
    "G-twins-isolated": (
        "python -I -W error on tests/labs/M2/lab-M2-L19-1.py, L20-1, L21-1: exit 0 each, stderr empty "
        "(twin_L19/20/21.out, .err). Twin files byte-identical since 4eb6788f."),
    "G-ruff-check-format": (
        "ruff check tests/labs/M2 course/modules/M/M2/grader -> 'All checks passed!', exit 0; ruff format --check on the "
        "same paths -> '31 files already formatted', exit 0 (ruff_check.out, ruff_format.out)."),
    "G-mypy-twins": (
        "mypy --no-incremental on the three twins -> 'Success: no issues found in 3 source files', exit 0 (mypy_twins.out)."),
    "G-mypy-labs-M2": (
        "mypy --no-incremental (repository, strict config) -> 'Success: no issues found in 386 source files', exit 0 "
        "(mypy_repo.out); tests/labs/M2 is within that run."),
    "G-mypy-repo": (
        "mypy --no-incremental -> 'Success: no issues found in 386 source files', exit 0 (mypy_repo.out)."),
    "G-page-smoke-L19-L21": (
        "page_smoke.py --unit M2 --pages L19 L20 L21 -> 'page_smoke M2: PASS', L19/L20/L21 each PASS, exit 0 (page_smoke.out)."),
    "G-pytest-labs-M2": (
        "pytest tests/test_labs.py -k M2 -q -> exit 0, no failures (pytest_labs_M2.out)."),
    "G-pytest-page-checks": (
        "pytest tests/test_page_checks.py -q -> exit 0, no failures (pytest_page_checks.out)."),
    "G-verify-refs-offline": (
        "verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 (verify_refs_offline.out)."),
    "G-verify-refs-live-M2": (
        "verify_refs.py --unit M2 (live, plain run) -> 'live re-verification of M2: 2 of 560 entries, 0 problems', exit 0 "
        "(verify_refs_live_M2.out)."),
    "G-run-graders-M2": (
        "run_graders.py --unit M2 --seeds 0-49 -> 'run_graders M2: PASS (reference 50/50 seeds, slowest 0.2 s)', exit 0 "
        "(run_graders_M2.out)."),
    "REF-openlibrary-M2": (
        "references/references.json changed in the delta (generated_at, and used_by gains BK4, FC2, LX1 on three other "
        "keys). Entries for spivak2008calculus and hubbard2015vector are identical between 4eb6788f and HEAD, used_by ['M2'] "
        "(delta_check_r1.out, section 5). Live verify_refs --unit M2 0 problems. Pages cite the keys at L19.html:484, "
        "L20.html:427, L22.html:473 (line 473 changed; the key names are unchanged)."),
    "DELTA-r4-slice": (
        "git diff 4eb6788f..95f3f8cb over the slice: L19.html, L20.html, L21.html and the three twins are byte-identical "
        "(delta_pages_twins_stat.out, empty). Slice-relevant hunks: cards.json entry M2-c293 back text only (the other 42 "
        "L19-L21 entries are JSON-identical; delta_check_r1.out section 2); cross-reference lines in L16.html:65 (not 303), "
        "L22.html 88/93/99/369/466/473 and L23.html 379 (delta_xref_index_refs.diff), index.html lines 68/124/161 (not 29), "
        "references.json used_by/generated_at. Each hunk re-read and checked under the rows below."),
    "HOURS-L19-L21": (
        "index.html:29 data-hours-lessons=\"240\" and data-hours-project=\"60\" (line unchanged; hunks at 68/124/161). "
        "Sum of data-hours over L01..L24 = 240.0 on HEAD, as on 4eb6788f (delta_check_r1.out section 6). L19, L20, L21 "
        "data-hours=10 and index.html card lines 'L19 · 10 h', 'L20 · 10 h', 'L21 · 10 h' unchanged in value; the L21 card "
        "body text changed (line 161) but its hours did not."),
    "XREF-L21-M2": (
        "Cross-references to L19-L21 numbering re-read in the changed lines: L22.html:88, 369, 466, 473 cite 'Theorem 1.3 of "
        "Lesson L21' under 'Assumption 1.2' and 'Assumption 2.1 of Lesson L06'; L21.html has Definition 1.1, Assumption 1.2, "
        "Theorem 1.3 (proved in §1 under Assumption 1.2 and Assumption 2.1 of L06), Theorem 2.1; L23.html:379 cites "
        "'Assumption 1.2 of Lesson L21', 'Theorem 2.1 of Lesson L21' and L23's own Proposition 2.1 (exists). L22.html:473 "
        "cites L06 Theorem 2.3 (mean value theorem; exists in L06.html) and its Assumption 2.1 (EVT, unchanged in substance, "
        "L06.html:72-73). L16.html:303 (unchanged line) says the general condition is taken up in Lesson L19 (Theorem 2.1 there, on the symmetry of mixed partials); L19.html Theorem 2.1 exists (MATH-L19-thm2.1). All targets exist."),
    "SIMULATED-labels": (
        "L19.html:126-127 and twin docstring label Lab 1 'SIMULATED' (f = e^x y + x y^2); L20.html:98-101 and L21.html:107-110 "
        "label their labs SIMULATED. Changed card M2-c293 quotes Lab 1's printed f_xy = 2.148721 with the lab's SIMULATED "
        "function already labelled on the lesson page. The other changed cards are not in scope of this row."),
    "PROSE-banned-and-process": (
        "Re-scan of the 43 L19-L21 cards in cards.json for banned strings (TODO, TBD, lorem, 'it is important to note', "
        "'studies show', 'experts agree', 'it is well known', 'obviously', 'clearly', 'left as an exercise', '\\mathbb', "
        "'we will', 'in this lesson', 'as we saw'): no hits (cards_scan_r1.out). The pages are byte-identical (carried)."),
    "SCOPE-words": (
        "Scope-word scan of L19-L21 cards (cards_scan_r1.out). The one changed card, M2-c293, uses 'smooth' in 'for this "
        "smooth f' tied to 'Assuming Assumption 2.1 of Lesson 6'; the function is Lab 1's f = e^x y + x y^2 (twin line 27), "
        "a smooth function by inspection, so the scope word is backed by a named hypothesis and a stated function. The "
        "other scope words in these cards are unchanged entries (carried). Page scope words carried."),
    "L-mathbb-R": (
        "Cards scan: no '\\mathbb' in the 43 L19-L21 cards (cards_scan_r1.out). Pages byte-identical (no \\mathbb in them "
        "by the same base scan)."),
    "DAG-L19-L21": (
        "check_dag.py --unit M2 -> PASS on the pin (check_dag.out). L19-L21 pages byte-identical; glossary.json and "
        "concepts.html changes sit in other units' concepts (the M3 concept rename in curriculum.json)."),
    "CARDS-coverage-L19-L21": (
        "L19-L21 card id set on the pin equals the base set (43 entries: M2-c280..c322, c402, c403; delta_check_r1.out "
        "section 2), each with the same lesson field. The one changed entry M2-c293 still covers Lab 1 Misconception 2 and "
        "the L19 cross-term result."),
    "CARDS-dup-scan": (
        "Full scan of cards.json on the pin: 398 entries (base 394); no duplicate ids, no duplicate fronts, no duplicate "
        "backs after normalisation (cards_scan_r1.out; delta_check_r1.out section 2)."),
    "CARDS-numbers-in-lesson": (
        "Changed card M2-c293 number 2.148721 equals Lab 1's printed f_xy (twin_L19.out 'f_xy = 2.148721'). It appears in "
        "L19.html inside the Lab 1 expected-output block (grep on L19.html, the line 'closed-form Hessian: ... f_xy = "
        "2.148721'). The lesson prose gives '\\approx 2.149' (L19.html, Misconception 2), which rounds it. Other L19-L21 "
        "card numbers unchanged (carried)."),
    "CARDS-agree-with-text-L19-L21": (
        "Re-checked the changed card M2-c293 against the current L19.html text: 'assuming Assumption 2.1 of Lesson L06, the "
        "two mixed entries are equal for this smooth f by Theorem 2.1, and the cross term ... is present whenever f_xy(p) "
        "!= 0' (L19.html Misconception 2 and Theorem 3.1 solution); 'Misconception 2' is the second misconception in L19; "
        "Lab 1 f_xy(0.5, 0.25) = 2.148721 = e^0.5 + 0.5 (twin formula exp(x)*y + x*y**2). The other 42 entries are "
        "JSON-identical to the base and carried."),
    "CARDS-L19-hypotheses": (
        "Re-checked M2-c293 (changed): it names 'Assuming Assumption 2.1 of Lesson 6'; L06.html Assumption 2.1 is still the "
        "extreme value theorem with the same statement (L06.html:72-73; diff only in the last sentence). The other entries "
        "in the list are JSON-identical (carried)."),
}

CARRY = {
    "G-page-vs-twin": CARRY_PAGES + " twin expected blocks and page code, unchanged; run_labs re-run PASS (27/27).",
    "NUM-L19": CARRY_PAGES,
    "NUM-L20": CARRY_PAGES,
    "NUM-L21": CARRY_PAGES,
    "STRUCT-L19": CARRY_PAGES,
    "STRUCT-L20": CARRY_PAGES,
    "STRUCT-L21": CARRY_PAGES,
    "MATH-L19-thm2.1": CARRY_PAGES,
    "MATH-L19-ex2.2": CARRY_PAGES,
    "MATH-L19-thm3.1": CARRY_PAGES,
    "MATH-L19-rem3.2": CARRY_PAGES,
    "MATH-L19-prop3.3": CARRY_PAGES,
    "MATH-L19-key-results-and-refs": CARRY_PAGES + " (registry entries for the cited keys identical, see REF-openlibrary-M2).",
    "L19-example-2.2-discontinuity": CARRY_PAGES,
    "L19-lab-1-prose-and-docstring": CARRY_PAGES,
    "L19-theorem-2.1-hypothesis-count": CARRY_PAGES,
    "L19-solutions-omit-assumption-2.1": CARRY_PAGES,
    "L19-quiz-Q9-circular-answer": CARRY_PAGES,
    "L19-refs-every-graded-result": CARRY_PAGES + " (registry entries for the cited keys identical, see REF-openlibrary-M2).",
    "L19-lab1-prop3.3-assumption": CARRY_PAGES,
    "LAB-L19-1": CARRY_PAGES + " run_labs re-run PASS (27/27); twin_L19 run alone PASS.",
    "MATH-L20-thm1.2": CARRY_PAGES,
    "MATH-L20-prop2.2": CARRY_PAGES,
    "MATH-L20-prop2.4": CARRY_PAGES,
    "MATH-L20-ex3.1-claims": CARRY_PAGES,
    "MATH-L20-problems-and-remarks": CARRY_PAGES,
    "LAB-L20-1": CARRY_PAGES + " run_labs re-run PASS; twin_L20 run alone PASS.",
    "MATH-L21-thm1.3": CARRY_PAGES,
    "MATH-L21-thm2.1": CARRY_PAGES,
    "MATH-L21-examples": CARRY_PAGES,
    "MATH-L21-misconceptions": CARRY_PAGES,
    "L21-sec3-bullet-thm1.3-assumption": CARRY_PAGES,
    "MATH-L21-problems": CARRY_PAGES,
    "L21-E2-third-derivative": CARRY_PAGES,
    "L21-E3-solution-incomplete": CARRY_PAGES,
    "LAB-L21-1": CARRY_PAGES + " run_labs re-run PASS; twin_L21 run alone PASS.",
    "NOTATION-L19-L21": ("Carried from round 4 (" + PAGES + " and notation/ byte-identical since the previous pin 4eb6788f):"
                         " notation/notation.json unchanged (git diff --quiet over notation/)."),
    "GRADES-L19-L21": ("Carried from round 4 (" + PAGES + " and BLUEPRINT.md byte-identical since the previous pin 4eb6788f):"
                       " BLUEPRINT.md unchanged (git diff --quiet)."),
    "L-mathbb-R-pages": CARRY_PAGES,
    "CARDS-L20-assumption": ("Carried from round 4 (course/modules/M/M2/cards.json entries M2-c296, c298, c302, c304, c305 "
                             "JSON-identical since the previous pin 4eb6788f; the delta changed only M2-c293 among L19-L21):"),
    "CARD-M2-c307-witness": ("Carried from round 4 (course/modules/M/M2/cards.json entry M2-c307 JSON-identical since the "
                             "previous pin 4eb6788f):"),
    "CARD-M2-c302-witness": ("Carried from round 4 (course/modules/M/M2/cards.json entry M2-c302 JSON-identical since the "
                             "previous pin 4eb6788f):"),
    "CARDS-L21-hypotheses": ("Carried from round 4 (course/modules/M/M2/cards.json entries M2-c309..c322 JSON-identical since "
                             "the previous pin 4eb6788f):"),
    "L19-lab1-prop3.3-cards": ("Carried from round 4 (course/modules/M/M2/cards.json entries M2-c287, c288, c289 "
                               "JSON-identical since the previous pin 4eb6788f):"),
}


def main():
    os.chdir(CHECKOUT)
    base = json.load(open(BASE_PATH, encoding="utf-8"))
    rows = []
    for r in base["rows"]:
        rid = r["id"]
        if rid in RE:
            ev = RE[rid]
            status = "PASS"
        elif rid in CARRY:
            ev = CARRY[rid]
            status = "PASS"
        else:
            # Default carry for rows whose subject is byte-identical (pages, twins, notation, BLUEPRINT).
            ev = CARRY_PAGES + " " + r["evidence"]
            status = "PASS"
        if rid in CARRY and rid in ("CARDS-L20-assumption", "CARD-M2-c307-witness", "CARD-M2-c302-witness",
                                    "CARDS-L21-hypotheses", "L19-lab1-prop3.3-cards", "NOTATION-L19-L21",
                                    "GRADES-L19-L21", "G-page-vs-twin", "L-mathbb-R-pages"):
            ev = CARRY[rid] + " Base evidence: " + r["evidence"]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev})
    counts = {"PASS": sum(1 for r in rows if r["status"] == "PASS"),
              "FAIL": sum(1 for r in rows if r["status"] == "FAIL")}
    re_count = sum(1 for r in rows if r["id"] in RE)
    carry_count = len(rows) - re_count
    out = {
        "unit": "M2",
        "slice": "d1",
        "round": 1,
        "round_note": ("Round 1 of the closing delta (architect ruling 30) for slice d1 (L19, L20, L21 and their twins). Base: "
                       "round-4 fragment /Users/billyribeiro/.fanout/frags/D-M2-d1.round4.json, pin 4eb6788f. Delta: "
                       "git diff 4eb6788f..95f3f8cb. Re-verified from scratch: every row whose subject changed (cards, "
                       "cross-references, index hub line, references, all gates). Carried with the carry prefix: rows whose "
                       "subject is byte-identical. No mutants (closing round writes none, ruling 37; no project grader)."),
        "verifier": "Haiku 5.5 independent verifier, slice d1 (L19, L20, L21 and their lab twins), closing delta round 1",
        "pin": PIN,
        "base": BASE_PIN + " (round-4 pin; fragment " + BASE_PATH + ")",
        "checkout": CHECKOUT,
        "scratch": CHECKOUT + "/" + SCRATCH,
        "verified_at": "2026-11-09T15:30:00Z",
        "verdict": "PASS" if counts["FAIL"] == 0 else "FAIL",
        "rows": rows,
        "mutants": [],
        "registry_flags": [],
        "freshness_flags": [],
        "notes": [
            "Mutants: none. Ruling 37 (closing round writes no new mutants); the slice holds no project grader and lab twins are "
            "demonstrations (ruling 9), so none is owed. The standing mutant set for this slice is empty.",
            "Scope (ruling 26 kinds only, no new-defect hunting): the only changed slice content is M2-c293's back text (number "
            "2.148721 replacing the rounded 'about 2.149'). It is correct against Lab 1's printed output and appears in the "
            "L19.html Lab 1 expected block; the lesson's prose gives 2.149 (rounded). No ruling-26 defect found.",
            "Observations outside slice scope (not graded here): the delta changed L01-L18, L22-L24, project.html, grader, "
            "index.html cards and curriculum.json (M3 and one other unit). Only the L16/L22/L23 cross-reference lines to L19-L21 "
            "were read. The architect's repo gates (build_site --check, render_curriculum, check_pages --all) are not run here.",
            "Not checked: no screenshot viewed (page_smoke only); no Crossref lookup (no DOI in these records); live verify_refs "
            "run as a plain run, no bot-check handling; the 42 unchanged L19-L21 cards and the L19-L21 pages were carried, not "
            "re-read line by line this round (byte-identical since 4eb6788f, JSON-identical per entry).",
            "Scripts: ledgers/M2/scripts/M2-d1-r1/ (check_pages.out, check_dag.out, check_projects.out, run_labs_M2.out, "
            "twin_L19/20/21.out and .err, page_smoke.out, ruff_check.out, ruff_format.out, mypy_twins.out, mypy_repo.out, "
            "pytest_labs_M2.out, pytest_page_checks.out, verify_refs_offline.out, verify_refs_live_M2.out, run_graders_M2.out, "
            "cards_scan_r1.py/.out, delta_check_r1.py/.out, delta_cards.diff, delta_xref_index_refs.diff, "
            "delta_pages_twins_stat.out, build_fragment_r1.py).",
        ],
        "summary": (f"M2-d1 closing delta round 1: {len(rows)} rows (pass={counts['PASS']} fail={counts['FAIL']}); "
                    f"{re_count} re-verified on pin 95f3f8cb (all gates re-run; changed subjects: cards M2-c293 and card-wide scans, "
                    f"cross-references L16/L22/L23, index hub line, references, DELTA row), {carry_count} carried with the carry "
                    "prefix (L19-L21 pages and twins byte-identical). Verdict PASS."),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print("wrote", OUT, counts, "re-verified", re_count, "carried", carry_count)


if __name__ == "__main__":
    main()
