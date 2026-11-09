import json, datetime, pathlib
BASE = pathlib.Path("/Users/billyribeiro/.fanout/frags/G-E3-g.round1.json")
base = json.loads(BASE.read_text(encoding="utf-8"))
base_rows = {r["id"]: r for r in base["rows"]}
CHECKOUT = "/Users/billyribeiro/.fanout/wt/verifyH1-E3-g"
OUT = "/Users/billyribeiro/.fanout/wt/verifyH1-E3-g/ledgers/E3/E3-g.json"
S = "ledgers/E3/scripts/E3-g-r1/out/"

NEW = {
"E3g19-delta-inventory": ("course/modules/E/E3/L05.html 499, 620; L06.html 545; L07.html 570; L08.html 165, 469, 479, 723; cards.json; tests/labs/E3; course/modules/E/E3/grader",
 "git diff 2a805c83..d9de2fe5 over slice g: L05.html 4 lines (499 key-results row; 620 footer), L06.html 2 (545 footer), L07.html 2 (570 footer), L08.html 8 (165 Remark 3.3; 469 'worth less than the initial wealth' sentence; 479 Epstein-Zin bullet; 723 footer). cards.json, tests/labs/E3/lab-E3-L05..L08-1.py, course/modules/E/E3/grader, references/references.json, notation/notation.json and course/modules/E/E3/index.html are byte-identical (git diff --quiet rc=0). Outside slice g and not rated: L02/L03/L04 pages (L03 interpretation line ~326 only; L04 Assumptions A1/A2 title and Example 2.5 quiz prompt) and tests/labs/E3/lab-E3-L02-1.py."),
"E3g19-L05-remark34-row": ("course/modules/E/E3/L05.html line 499 (row) against Remark 3.4 (block at line 156-157) and Proposition 2.2 (line 112)",
 "Row now reads 'differ at every plan with c1 != c0 when psi != 1/gamma'. Re-derived: for r = c1/c0 != 1 and beta in (0,1), r^gamma = r^(1/psi) iff gamma = 1/psi (ln r != 0), and the common prefactor (1-beta)/beta > 0 cancels, so the MRS differ iff the exponents differ. Grid check of the exponent equality over gamma in {0.5,1.5,2,3}, psi in {0.25,0.5,2,3}, r in {0.2,...,4} has zero mismatches (ledgers/E3/scripts/E3-g-r1/numbers_delta.py, out/numbers_delta.out). Remark 3.4 text (line 157) states the same claim. Grade T with basis 'Proved in §3 from Proposition 2.2' matches Remark 3.4 (T). Wording point, not a FAIL: 'psi != 1/gamma' is undefined at gamma = 0, where Remark 3.4 says the elasticity is undefined; the MRS claim still holds there (CRRA exponent 0 against 1/psi != 0), so the row is correct under any reading."),
"E3g18-grade-legend-footer": ("course/modules/E/E3/L05.html 620; L06.html 545; L07.html 570; L08.html 723 (footers); L05-L08 legend lines 46-47; L05.html 609, L06.html 534, L07.html 80, L08.html 67, 133, 479 (ungraded naming sentences)",
 "All four footers now read 'Each graded result carries a proof or a lab result labelled C.', the ruling 39 wording (ruling 33 also names it), identical to the L01-L04 footers (grep). Base FAIL asked for grades and keys on the title-only sentences; ruling 39 and 38a answer that by making them ungraded naming sentences, which is what the page now has. Footer claim checked against every grade span: ledgers/E3/scripts/E3-g-r1/grades.py -> out/grades.out: L05 12 spans (T 7, C 5), L06 11 (T 8, C 3), L07 8 (T 6, C 2), L08 9 (T 8, C 1). Every T basis cites a proof section, numbered Example, Proposition, Remark, Problem or 'Algebra in §n'; every C basis cites Lab 1 or a numbered lab part. Each of the four pages has claim spans 0 and data-cite 0, and no 'registry record ... title only' grade row remains (grep). Legend L05-L08 'C single study or lab result' is consistent with 'a lab result labelled C'. Out of slice, not rated: L01.html and L02.html legend still read 'single study' (line 46)."),
"E3g12-c134": ("course/modules/E/E3/cards.json E3-c134; course/modules/E/E3/L07.html line 80",
 "cards.json unchanged in the delta. E3-c134 carries no grade and no cite key, the ungraded form the other cards use (E3-c137 has no grade key either). Back text 'The name prospect theory appears in the title of the 1979 Kahneman and Tversky paper, which is used for its title only' agrees with L07.html line 80 ('title of the 1979 paper by Kahneman and Tversky; this page has not read the paper and cites it for no result'). Registry kahneman1979prospect (references/references.json): Kahneman, Tversky, 1979, 'Prospect Theory: An Analysis of Decision under Risk'. Ruling 39 aligns this card with the ungraded naming sentence; base FAIL answered."),
"E3g12-c157": ("course/modules/E/E3/cards.json E3-c157; course/modules/E/E3/L08.html line 133",
 "cards.json unchanged in the delta. E3-c157 has no grade or cite key. Back text 'Only its registry title, which contains the word ambiguity' agrees with L08.html line 133 ('The registry title of the 1961 paper by Ellsberg contains the word ambiguity; this page has not read the paper and cites it for no result'). Registry ellsberg1961risk: Ellsberg, 1961, 'Risk, Ambiguity, and the Savage Axioms' (contains 'ambiguity'). Ruling 39 answers the base FAIL."),
"E3g12-c158": ("course/modules/E/E3/cards.json E3-c158; course/modules/E/E3/L08.html line 67",
 "cards.json unchanged in the delta. E3-c158 has no grade or cite key. Back text 'Only the name: maxmin expected utility appears in the title of the 1989 Gilboa and Schmeidler paper' agrees with L08.html line 67 ('The name maxmin expected utility appears in the title of the 1989 Gilboa and Schmeidler paper; this page has not read the paper and cites it for no result'). Registry gilboa1989maxmin: Gilboa and Schmeidler, 1989, 'Maxmin expected utility with non-unique prior'. Ruling 39 answers the base FAIL."),
"E3g15-attributions": ("references/references.json kahneman1979prospect, ellsberg1961risk, gilboa1989maxmin; L07.html line 80; L08.html lines 67, 133, 479",
 "Registry records read directly: kahneman1979prospect (Kahneman and Tversky, 1979), ellsberg1961risk (Ellsberg, 1961), gilboa1989maxmin (Gilboa and Schmeidler, 1989); all three titles match the sentences. Each sentence names the title, states that the page has not read the paper, and states no result from it. None carries data-grade or data-cite (grep; check_pages PASS). Under ruling 39 they are ungraded naming sentences, so the base FAIL is answered."),
"E3g18-page-structure-footers": ("course/modules/E/E3/L05.html 620; L06.html 545; L07.html 570; L08.html 723; section order and Previous/Next links",
 "check_pages.py --unit E3: 'check_pages E3: PASS' (rc 0, out/check_pages_E3.out). page_smoke for L05-L08: 'page_smoke E3: PASS' (out/page_smoke.out). Section order and nav links are outside all slice-g hunks. The footers now read the ruling 39 sentence (see E3g18-grade-legend-footer)."),
"E3g12-L05-L08-key-results": ("course/modules/E/E3/L05.html line 499 (changed row) and grade tables L05 lines 489-507, L07 451-467, L08 607-624",
 "L05 changed row re-verified in E3g19-L05-remark34-row. Grade tables read in full from grades.out: every T row has a proof, algebra, Example or Proposition basis and every C row has a Lab 1 basis. No 'Registry record' row remains in the L07 or L08 key-results tables (grep). The rows removed in the earlier delta are not restored (ruling 39)."),
"E3g12-L05-prose-numbers": ("course/modules/E/E3/L05.html line 499 and the rest of L05 prose (Remark 1.5, Definition 2.1, Proposition 2.2 proof, Remark 2.3, Remark 3.4, P1-E3)",
 "git diff -U0 2a805c83..d9de2fe5 numeric-token multiset over L05: removed minus added = {} (no number removed); added minus removed = {'0':1,'1':1}, which come from the subscripts c_0, c_1 and the 1 in '1/gamma' in the row at 499, not new values. No number in the changed row needs recomputation beyond E3g19-L05-remark34-row."),
"E3g12-L06-prose-numbers": ("course/modules/E/E3/L06.html (only hunk is the footer, line 545)",
 "Numeric-token multiset over the L06 hunk: removed minus added = {}, added minus removed = {} (git diff -U0). The footer has no numeric value."),
"E3g12-L07-prose-numbers": ("course/modules/E/E3/L07.html lines 44, 80, 462-463, 570",
 "Numeric-token multiset over L07 hunks (footer 570 only in this delta): removed minus added = {}, added minus removed = {}. L07.html line 80 (year 1979, unchanged since 2a805c83) equals registry kahneman1979prospect year 1979."),
"E3g12-L08-prose-numbers": ("course/modules/E/E3/L08.html lines 165, 469, 479, 723 (changed in the delta)",
 "Numeric-token multiset over the four L08 hunks: removed minus added = {}, added minus removed = {}. Line 469 keeps 99523.8095, 101951.2195, 102500 and 548.7805 and the 476.1905 figure; ledgers/E3/scripts/E3-g-r1/numbers_delta.py recomputes them: maxmin CE at p = 1/3 = 99523.8095; EU CE at p = 1/2 = 101951.2195; 102500 - 101951.2195 = 548.7805; 100000 - 99523.8095 = 476.1905 (out/numbers_delta.out). Initial wealth w0 = 100000 cents (L08.html line 173, 433)."),
"E3g12-scope-words-cards": ("course/modules/E/E3/cards.json E3-c134, c157, c158; L05.html line 499 ('at every plan'); footers",
 "The footer 'every' scope word is gone from L05-L08. The new scope word in L05 line 499 ('differ at every plan with c1 != c0') is backed by Remark 3.4 (line 157: 'Off that case ... at every plan with c1 ≠ c0 ... because r^gamma ≠ r^(1/psi) for r ≠ 1') and by the grid check in numbers_delta.out. The card 'Only' phrases (c134, c157, c158) are backed by the registry titles and the L07/L08 naming sentences (E3g15-attributions)."),
"E3g12-process-words-cards": ("cards.json E3-c134, c157, c158; L05.html 499-620; L06.html 545; L07.html 570; L08.html 165, 469, 479, 723",
 "grep -o -i over the added lines of git diff -U0 2a805c83..d9de2fe5 (L05-L08 and cards) for ledger|verif|round|builder|agent|audit|fixed|revis|changed|correct|draft|reviewer|delta|now: zero matches. 'The lesson does not establish whether' (L08 165) is an evidence-basis disclosure, not process narration."),
"E3g12-notation": ("course/modules/E/E3/L05.html 499; L08.html 165, 469, 479; notation/notation.json",
 "notation/notation.json byte-identical (git diff --quiet rc 0). Added lines contain no Omega, Lambda or other new symbol (grep -o over added lines, empty for Omega/Lambda). The changed text uses psi, gamma, beta, c_0, c_1 and MRS with their existing meanings in L05 Definition 2.1 and Proposition 2.2."),
"E3g18-omega-notation": ("course/modules/E/E3/L05.html, L06.html, L08.html; cards.json E3-c078, c080, c145; tests/labs/E3 lab-E3-L05-1.py",
 "The delta hunks (L05 499 and 620, L06 545, L07 570, L08 165, 469, 479, 723) contain no Omega token in either the removed or the added line (grep -o 'Omega' over diff, empty). cards.json and the L05 twin are byte-identical. Omega is still local to E3 L05 and L08 and not registered."),
"E3g12-check-pages-dag-projects": ("tools/check_pages.py --unit E3; tools/check_dag.py --unit E3; tools/check_projects.py --unit E3",
 "Re-run at d9de2fe5 (ledgers/E3/scripts/E3-g-r1/gates_delta_r1.sh): 'check_pages E3: PASS' (rc 0), 'check_dag E3: PASS' (rc 0), 'check_projects E3: PASS' (rc 0); out/check_pages_E3.out, check_dag_E3.out, check_projects_E3.out. check_pages does not test the footer text (see E3g18-grade-legend-footer)."),
"E3g12-verify-refs": ("tools/verify_refs.py --offline; references/references.json",
 "Re-run at d9de2fe5: 'offline integrity: 560 entries, 0 problems' (rc 0, gates_delta_r1.sh verify_refs_offline). references/references.json byte-identical in the delta. Live Crossref not run; references unchanged."),
"E3g12-lab-twins-run": ("tests/labs/E3/lab-E3-L05-1.py, lab-E3-L06-1.py, lab-E3-L07-1.py, lab-E3-L08-1.py",
 "Each twin run alone under python -I -W error: exit 0 (out/twin_L05.out .. twin_L08.out). run_labs.py --unit E3 --page L05..L08: 'run_labs E3: PASS (1/1)' each (out/run_labs_L0x.out). Twins are byte-identical in the delta."),
"E3g18-twins-run": ("tests/labs/E3/lab-E3-L05-1.py .. lab-E3-L08-1.py; course/modules/E/E3/L05-L08.html lab blocks",
 "Same re-run as E3g12-lab-twins-run: twins exit 0 under python -I -W error; run_labs PASS for L05-L08; the lab blocks are outside the delta hunks."),
"E3g14-page-smoke": ("tools/page_smoke.py --unit E3 --pages L05 L06 L07 L08",
 "Re-run at d9de2fe5: 'page_smoke E3: PASS' (rc 0), with per-page PASS lines for L05-L08 (out/page_smoke.out)."),
"E3g14-ruff-mypy": ("ruff check .; ruff format --check .; mypy --no-incremental (strict config)",
 "Re-run at d9de2fe5: 'All checks passed!' (ruff check, rc 0); '555 files already formatted' (ruff format --check, rc 0); 'Success: no issues found in 386 source files' (mypy --no-incremental, rc 0). out/ruff_check_delta.out, ruff_format_delta.out, mypy_delta.out."),
"E3g14-pytest-relevant": ("tests/test_docs_figures.py; tests/test_refs.py; tests/test_page_checks.py; tests/test_labs.py; tests/test_run_labs.py; tests/test_build_site.py; tests/test_page_smoke.py",
 "pytest -q tests/test_docs_figures.py tests/test_refs.py: all pass (rc 0). pytest -q tests/test_page_checks.py tests/test_labs.py tests/test_run_labs.py tests/test_build_site.py tests/test_page_smoke.py -k 'E3 or e3 or page or lab or build': all pass (rc 0; out/pytest_relevant.out). The full 'pytest -k E3' over tests was not re-run."),
"E3g14-lab-L05-printed": ("tests/labs/E3/lab-E3-L05-1.py; course/modules/E/E3/L05.html expected block",
 "Re-run: run_labs.py --unit E3 --page L05 'run_labs E3: PASS (1/1)' (rc 0; out/run_labs_L05.out). Twin run alone under python -I -W error: exit 0 (out/twin_L05.out). The expected block is outside the delta hunks."),
"E3g14-lab-L06-printed": ("tests/labs/E3/lab-E3-L06-1.py; course/modules/E/E3/L06.html expected block",
 "Re-run: run_labs.py --unit E3 --page L06 'run_labs E3: PASS (1/1)' (rc 0; out/run_labs_L06.out). Twin exit 0 under -I -W error (out/twin_L06.out)."),
"E3g14-lab-L07-printed": ("tests/labs/E3/lab-E3-L07-1.py; course/modules/E/E3/L07.html expected block",
 "Re-run: run_labs.py --unit E3 --page L07 'run_labs E3: PASS (1/1)' (rc 0; out/run_labs_L07.out). Twin exit 0 under -I -W error (out/twin_L07.out)."),
"E3g14-lab-L08-printed": ("tests/labs/E3/lab-E3-L08-1.py; course/modules/E/E3/L08.html expected block",
 "Re-run: run_labs.py --unit E3 --page L08 'run_labs E3: PASS (1/1)' (rc 0; out/run_labs_L08.out). Twin exit 0 under -I -W error (out/twin_L08.out)."),
"E3g15-numbers": ("ledgers/E3/scripts/E3-g-r1/numbers_delta.py; out/numbers_delta.out; L05-L08 numeric tokens of the delta",
 "Re-derived at d9de2fe5 with numbers_delta.py (out/numbers_delta.out): 99523.8095, 101951.2195, 548.7805, 476.1905 and the MRS closed forms at (c0,c1)=(2,4), beta=0.9, psi=1/2, gamma=2 (both 0.444444). The base script numbers_L05_L08.py is not in this checkout and was not re-run; instead the numeric-token multiset of the delta is empty for removed numbers (see E3g12-L08-prose-numbers)."),
"E3g15-gate-check-and-build": ("tools/build_site.py --check; tools/render_curriculum.py; git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json",
 "Re-run at d9de2fe5: 'site data current: 6 outputs' (rc 0); render_curriculum.py rc 0; git diff --exit-code on CURRICULUM.md and curriculum/curriculum.json rc 0 (out/build_site_check.out, render_curriculum.out, curriculum_diff.out)."),
"E3g15-gate-run-labs": ("tools/run_labs.py --unit E3 --page L05..L08",
 "Re-run: 'run_labs E3: PASS (1/1)' for each of L05, L06, L07, L08 (rc 0)."),
"E3g12-c147": ("course/modules/E/E3/cards.json E3-c147; course/modules/E/E3/L08.html Remark 3.3 (line 165, changed)",
 "cards.json unchanged. Back text 'a dependence on psi and beta is an untested hypothesis (Remark 3.3)' agrees with the changed Remark 3.3 ('The lesson does not establish whether its certainty equivalent then depends on psi and beta; Problem R1 names the step that fails'). The phrase 'untested hypothesis' remains in L08 Problem R1 solution (line 586: 'the untested hypothesis of Remark 3.3'). Card agrees with the current lesson text."),
"E3g12-c152": ("course/modules/E/E3/cards.json E3-c152; course/modules/E/E3/L08.html line 472 (risk premium; changed sentence follows it)",
 "cards.json unchanged. 102500 - 101951.2195 = 548.7805 cents and 548.7805 / 100 = 5.487805, which rounds to 5.4878 CU (numbers_delta.out). The changed sentence on line 472 only concerns the maxmin CE and keeps the same figures; the card's figures agree."),
"E3g15-lab-twin-L06": ("tests/labs/E3/lab-E3-L06-1.py; course/modules/E/E3/L06.html section 3 Lab 1",
 "Twin byte-identical in the delta; run_labs L06 PASS and twin exit 0 under -I -W error (out/run_labs_L06.out, twin_L06.out)."),
}

CARD_FILES = "course/modules/E/E3/cards.json byte-identical since the previous pin 2a805c83"
PAGE_NOTE = "cited lesson block outside the d9de2fe5 hunks (L05 499/620, L06 545, L07 570, L08 165/469/479/723), so byte-identical since the previous pin"
CARRY_PREFIX = {
 "E3g19-c037": "course/modules/E/E3/cards.json byte-identical since the previous pin 2a805c83; L03.html Proposition 1.2 lines 77-83 outside the d9de2fe5 hunks (the L03 hunk is the interpretation text near line 326)",
 "E3g12-c137": "course/modules/E/E3/cards.json byte-identical since the previous pin 2a805c83; L08.html line 67 outside the d9de2fe5 hunks",
 "E3g12-c172": "course/modules/E/E3/cards.json byte-identical since the previous pin 2a805c83; L08.html line 67 outside the d9de2fe5 hunks",
 "E3g12-c144": "course/modules/E/E3/cards.json byte-identical since the previous pin 2a805c83; L08.html line 132 outside the d9de2fe5 hunks",
 "E3g12-c164": "course/modules/E/E3/cards.json byte-identical since the previous pin 2a805c83; L08.html line 132 outside the d9de2fe5 hunks",
 "E3g12-c165": "course/modules/E/E3/cards.json byte-identical since the previous pin 2a805c83; L08.html line 132 outside the d9de2fe5 hunks",
 "E3g12-c182": "course/modules/E/E3/cards.json byte-identical since the previous pin 2a805c83; L08.html line 132 outside the d9de2fe5 hunks",
 "E3g15-L07-changes": "course/modules/E/E3/L07.html Remark 1.6, section 4 misconceptions and the L07 section 6 key-results row outside the d9de2fe5 hunks (570 only); cards byte-identical",
 "E3g15-L05-changes": "course/modules/E/E3/L05.html Remark 1.5, Definition 2.1, Proposition 2.2 proof and quiz L05q9 outside the d9de2fe5 hunks (499, 620); cards byte-identical",
 "E3g15-L06-changes": "course/modules/E/E3/L06.html Proposition 1.4, Remark 3.2, section 4 and section 5 outside the d9de2fe5 hunks (545 only); cards byte-identical",
 "E3g15-L08-changes": "course/modules/E/E3/L08.html section 6 first misconception and cards.json E3-c154 outside the d9de2fe5 hunks (165, 469, 479, 723); cards byte-identical",
 "E3g12-L04-theorem-cross-lesson": "course/modules/E/E3/L04.html Theorem 1.5 and L07 section 0/Section 2 outside the d9de2fe5 hunks (L04 hunks are the A1/A2 title and the Example 2.5 quiz prompt); cards.json E3-c129 byte-identical",
 "E3g12-L05-L08-problem-solutions": "L05-L08 problem and solution blocks outside the d9de2fe5 hunks (the hunks touch only the rows, Remark 3.3, the 469 sentence, the 479 bullet and footers)",
 "E3g12-L05-L08-quiz-keys": "L05-L08 quiz items outside the d9de2fe5 hunks (quiz blocks not touched)",
 "E3g14-hours-arithmetic": "course/modules/E/E3/index.html byte-identical since the previous pin 2a805c83",
 "E3g12-card-numbers": "course/modules/E/E3/cards.json byte-identical since the previous pin 2a805c83; the numeric-token diff of L05-L08 removes no number (E3g12-L08-prose-numbers)",
 "E3g12-dup-scan": "course/modules/E/E3/cards.json byte-identical since the previous pin 2a805c83",
 "E3g18-rename-complete": "course/modules/E/E3/cards.json and tests/labs/E3 L05/L06/L08 twins byte-identical since the previous pin 2a805c83; the delta hunks touch none of the renamed lines (E3g18-omega-notation)",
 "E3g18-c106-basis": "course/modules/E/E3/cards.json byte-identical since the previous pin 2a805c83",
 "E3g12-c131-basis-note": "course/modules/E/E3/cards.json byte-identical since the previous pin 2a805c83 (E3-c131 still absent)",
 "E3g12-c131": "course/modules/E/E3/cards.json byte-identical since the previous pin 2a805c83 (E3-c131 still absent)",
 "E3g12-r11-c130-grade-resolved": "course/modules/E/E3/cards.json byte-identical since the previous pin 2a805c83",
 "E3g12-delta-round12": "history row (commit range ccaeeaf4..329c1d7f); the range is unchanged by this delta",
 "E3g14-delta-round14": "history row (commit range 329c1d7f..1431aa1d); the range is unchanged by this delta",
 "E3g15-delta": "history row for the earlier delta; the cited blocks are not touched by the 2a805c83..d9de2fe5 hunks except as listed in E3g19-delta-inventory",
 "E3g18-delta-inventory": "history row for the earlier delta (dde0486b..4540351d); the cited blocks are not touched by the 2a805c83..d9de2fe5 hunks",
}

rows = []
for rid, b in base_rows.items():
    if rid in NEW:
        loc, ev = NEW[rid]
        rows.append({"id": rid, "check": b["check"], "location": loc, "status": "PASS", "evidence": ev})
        continue
    if b["status"] != "PASS":
        raise SystemExit("unexpected non-PASS base row without new evidence: " + rid)
    prefix = CARRY_PREFIX.get(rid)
    if prefix is None:
        if rid.startswith("E3g12-c") or rid.startswith("E3g12-c0") or rid.startswith("E3g12-c1"):
            prefix = CARD_FILES
        else:
            prefix = PAGE_NOTE
    rows.append({"id": rid, "check": b["check"], "location": b["location"], "status": "PASS",
                 "evidence": f"Carried from round 1 ({prefix}): " + b["evidence"]})

now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
frag = {
  "unit": "E3", "slice": "g", "round": 1,
  "verifier": "Haiku 5.5 independent verifier, unit E3 slice g, closing delta round 1 (2a805c83..d9de2fe5, rulings 30, 37, 38a, 39, 40)",
  "pin": "d9de2fe5",
  "base": "2a805c831410ab77c38c227f7e121e8537193ce9 (base fragment ~/.fanout/frags/G-E3-g.round1.json, verdict FAIL with 6 FAIL rows)",
  "checkout": CHECKOUT,
  "scratch": "ledgers/E3/scripts/E3-g-r1/out",
  "verified_at": now,
  "verdict": "PASS",
  "rows": rows,
  "mutants": [],
  "registry_flags": [],
  "freshness_flags": [],
  "notes": [
    "Slice g scope: L05-L08 lesson pages, cards.json (178 cards), L05-L08 lab twins. No grader in slice g, so no mutants are authored or run (ruling 37, closing round). Ruling 30: delta verification only.",
    "Delta 2a805c83..d9de2fe5 inside slice g: L05 499 (key-results row) and 620 (footer); L06 545 (footer); L07 570 (footer); L08 165 (Remark 3.3), 469 (sentence), 479 (Epstein-Zin bullet), 723 (footer). cards.json, the twins, the grader, references.json and notation.json are byte-identical.",
    "The six base FAIL rows (E3g18-grade-legend-footer, E3g18-page-structure-footers, E3g12-c134, E3g12-c157, E3g12-c158, E3g15-attributions) are re-verified against ruling 39 and 38a: the title-only sentences are ungraded naming sentences with no key, the cards have no grade or cite key, and the footers read the ruling 39 wording, which every E3 page now carries (L01-L08). Each is PASS.",
    "Out-of-slice observations, not rated: L01.html and L02.html legend still read 'single study' (line 46) while L03-L08 read 'single study or lab result'; L03 interpretation text (line ~326), L04 Assumptions A1/A2 title and Example 2.5 quiz prompt, tests/labs/E3/lab-E3-L02-1.py and the L02 page line changed in d9de2fe5 belong to other slices.",
    "Command outputs are in ledgers/E3/scripts/E3-g-r1/out/: check_pages_E3, check_dag_E3, check_projects_E3, run_labs_L05..L08, verify_refs_offline, build_site_check, render_curriculum, curriculum_diff, ruff_check, ruff_format, mypy, pytest_docs_refs, page_smoke, twin_L05..L08, pytest_relevant, grades.out, numbers_delta.out.",
    "Could not check: run_graders and mutate_graders (no grader in slice g); live Crossref (verify_refs without --offline; references unchanged); browser screenshots beyond page_smoke; the base script numbers_L05_L08.py (absent from this checkout, so not re-run); the full pytest -k E3 over tests (targeted files run instead).",
  ],
  "summary": {},
}
counts = {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows), "fail": 0, "unverifiable": 0, "mutants": 0, "mutants_killed": 0}
frag["summary"] = counts
pathlib.Path(OUT).write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(counts)
