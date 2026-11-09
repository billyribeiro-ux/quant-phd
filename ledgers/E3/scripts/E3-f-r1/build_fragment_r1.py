import json, subprocess, sys
base = json.loads(open("/Users/billyribeiro/.fanout/frags/D-E3-f.round18.json", encoding="utf-8").read())
PIN = "2a805c831410ab77c38c227f7e121e8537193ce9"
BASE_PIN = "4540351dc664559cdfd371b908f2b4e644cf4297"

def carry(prefix, row):
    return prefix + " " + row["evidence"]

P = {
    "L01": "Carried from round 18 (course/modules/E/E3/L01.html and tests/labs/E3/lab-E3-L01-1.py byte-identical since the previous pin 4540351d):",
    "L02": "Carried from round 18 (course/modules/E/E3/L02.html, tests/labs/E3/lab-E3-L02-1.py, references/references.json byte-identical since the previous pin 4540351d):",
    "L04": "Carried from round 18 (course/modules/E/E3/L04.html and tests/labs/E3/lab-E3-L04-1.py byte-identical since the previous pin 4540351d):",
    "L03": "Carried from round 18 (course/modules/E/E3/L03.html outside its delta hunks at lines 78, 83 and 326, and course/modules/E/E3/cards.json entries outside E3-c037 byte-identical, since the previous pin 4540351d):",
    "CARDS": "Carried from round 18 (course/modules/E/E3/cards.json entry {id} byte-identical and its cited lesson blocks outside this delta's hunks, since the previous pin 4540351d):",
    "GRADER": "Carried from round 18 (course/modules/E/E3/grader/* and tests/labs/E3/lab-E3-project-*.py byte-identical since the previous pin 4540351d):",
}

NEW = {}
def new(rid, status, evidence, fix=None):
    NEW[rid] = (status, evidence, fix)

# Re-verified in this closing round (command outputs under ledgers/E3/scripts/E3-f-r1/out/)
new("E3f-cmd-check_pages", "PASS", "Closing round 1 at 2a805c83: .venv/bin/python tools/check_pages.py --unit E3 -> 'check_pages E3: PASS' rc 0 (out/check_pages_unit.out).")
new("E3f-cmd-check_dag", "PASS", "Closing round 1: tools/check_dag.py --unit E3 -> 'check_dag E3: PASS' rc 0 (out/check_dag_unit.out). The delta adds no class=\"concept\" link (git diff 4540351d..HEAD of L03.html has only hunks at lines 78, 83, 326).")
new("E3f-cmd-check_projects", "PASS", "Closing round 1: tools/check_projects.py --unit E3 -> 'check_projects E3: PASS' rc 0 (out/check_projects_unit.out). project.html changed in the delta (line 648, another slice) and this gate is re-run.")
new("E3f-cmd-page_smoke", "PASS", "Closing round 1, run alone after the other gates: tools/page_smoke.py --unit E3 --pages L01 L02 L03 L04 -> 'page_smoke E3: PASS' rc 0 (out/page_smoke.out).")
new("E3f-cmd-pytest-labs", "PASS", "Closing round 1: pytest -q tests -k E3 -> rc 0 (out/pytest_e3.out); pytest -q tests -k 'lab and not lx1' -> rc 0 (out/pytest_lab_not_lx1.out). The LX1 test file is not run in this slice.")
new("E3f-cmd-pytest-cards-notation", "PASS", "Closing round 1: pytest -q tests -k 'card or notation or review or concept' -> rc 0, 6 dots, no failures (out/pytest_cards.out).")
new("E3f-cmd-ruff-labs", "PASS", "Closing round 1: ruff check tests/labs/E3 course/modules/E/E3/grader -> 'All checks passed!'; ruff format --check tests/labs/E3 -> '11 files already formatted'; repo-wide ruff check . and ruff format --check . also rc 0 (out/ruff_labs.out, out/ruff_format_labs.out, out/ruff_repo.out, out/ruff_format_repo.out).")
new("E3f-cmd-mypy-twins", "PASS", "Closing round 1: .venv/bin/python -m mypy --no-incremental -> 'Success: no issues found in 386 source files' rc 0 (out/mypy.out).")
new("E3f-cmd-verify_refs", "PASS", "Closing round 1: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' rc 0 (out/verify_refs_offline.out).")
new("E3f-cmd-build_site-render", "PASS", "Closing round 1: tools/build_site.py --check -> 'site data current: 6 outputs' rc 0; tools/render_curriculum.py -> 'curriculum valid: 25 parts, 134 modules, 157 projects, 13,715 h (6.35 FTE years)' rc 0; git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json rc 0 (out/build_site_check.out, out/render_curriculum.out, out/render_diff.out).")
new("E3f-cmd-pytest-docs", "PASS", "Closing round 1: pytest -q tests/test_docs_figures.py tests/test_refs.py -> rc 0 (out/pytest_docs.out).")
new("E3f-cmd-run_labs-L01-L04", "PASS", "Closing round 1: tools/run_labs.py --unit E3 --page L01, L02, L03, L04 -> 'run_labs E3: PASS (1/1)' each, rc 0 (out/run_labs_L01..L04.out).")
new("E3f-cmd-fetch_data", "PASS", "Closing round 1: tools/fetch_data.py --check -> 'fetch_data: 3 datasets, 0 problems' rc 0 (out/fetch_data_check.out).")
new("E3f-lab-twin-equality", "PASS", "Closing round 1: ledgers/E3/scripts/E3-f-r1/twin_check_r1.py . -> L01..L04 each 'page_code_equals_twin=True expected_equals_stdout=True rc=0 stderr=''' (out/twin_check.out). Run under python -I -W error via the script.")
new("E3f-lab-L03", "FAIL",
    "Closing round 1 at 2a805c83. Lab code and expected block agree: tests/labs/E3/lab-E3-L03-1.py run with python -I -W error exits 0 and its stdout equals the pre-block at course/modules/E/E3/L03.html:307-325 (twin_check out); page code equals twin. Re-derived independently (ledgers/E3/scripts/E3-f-r1/out/rederive_r1.out): CE 11250.0000, 10931.7733, 10615.8009, 10000.0000, 8888.8889, 7337.6161 rounded 11250, 10932, 10616, 10000, 8889, 7338; exact 80000/9. DEFECT in the changed interpretation paragraph, course/modules/E/E3/L03.html:326: 'every computed value comes from the fixed lottery and the stated gamma grid'. The code computes values from inputs that are neither the lottery nor the grid GAMMAS (twin line 18 = 0, 0.25, 0.5, 1, 2, 4): the gap at gamma 1 +/- 1e-6 (twin line 83), the slopes at gamma 1 +/- 1e-3 and 1 +/- 1e-6 (twin lines 87-88), and the CRRA utility at gamma 1 - 1e-6 for wealths 0.5, 2 and 10000 (twin lines 96-97). The previous wording 'every number is computed from the fixed lottery' had the same over-claim. Ruling 26 kind: a lab statement the code does not support.",
    "Rewrite the sentence at course/modules/E/E3/L03.html:326 to name the sources that the code uses: the certainty equivalents, the exact value and the falling-order check use the fixed lottery and the grid 0, 0.25, 0.5, 1, 2, 4; the gap, the slope and the limit checks use the offsets 1 +/- 1e-6 and 1 +/- 1e-3 and the wealths 0.5, 2 and 10000 that the code states; the scaling checks use the lottery multiplied by k = 2, 3, 10. Keep the rest of the paragraph. Then re-run check_pages, page_smoke L03 and twin check.")
new("E3f-lesson-numbers-L03", "PASS", "Closing round 1: numbers in the changed text re-derived. Prop 1.2 (L03.html:78) and its proof (line 83) contain no new number. Interpretation paragraph (line 326): 11250 and 10000 cents (run output lines 'gamma 0' and 'gamma 1'), 80000/9 and 8888.8889 (output lines 'gamma 2 exact value' and 'gamma 2: certainty equivalent'), 10^{-12} (twin line 103-106 worst_rel <= 1e-12, output 'unrounded: True'), 0.1 percent (twin line 88-90), (k+1)/2 (twin line 111) all match the printed output and code. Other L03 numbers carried (out/rederive_r1.out).")
new("E3f-r14-L03-proofs", "PASS", "Closing round 1: Proposition 1.2 and its proof (course/modules/E/E3/L03.html:78 and :83) re-derived: ln(w^iota) = iota ln w; (w^iota)^Lambda = e^{Lambda ln(w^iota)} = e^{iota Lambda ln w} = w^{iota Lambda}. Independent check over 20000 random (w, iota, Lambda) gives max relative error 1.6e-14 (out/rederive_r1.out). Second claim (xy)^c = x^c y^c is text-identical. Other propositions and problems of L03 carried: " + "L03 lines outside the hunks are byte-identical since the previous pin 4540351d.")
new("E3f-notation", "PASS", "Closing round 1: notation/notation.json byte-identical since the pin (git diff empty). In L03 the renamed letters Lambda (exponent of Prop 1.2) and iota are introduced in the lesson (L03.html:78) and are not program-wide symbols (notation.json 'about': letters whose meaning is conventionally local are defined in each lesson). No registered symbol is given a second meaning by the delta.")
new("E3f-r14-notation-tau", "PASS", "Closing round 1: tau has one meaning in E3 pages. L08.html:65-67, 80, 186, 189 keep tau as the alpha-MEU weight in [0, 1]; the L08 hunk at line 67 changes only the name sentence, not V_tau(f). L01 no longer uses tau: L01 Definition 2.1 (L01.html:86) uses \\Xi for the mixture weight (50 uses, all in [0, 1], see E3f-r18-notation-ruling33-letters). The base text 'now rho' was stale and is corrected here: the L01 weight is Xi.")
new("E3f-r15-notation-cross-lesson", "PASS", "Closing round 1: grep over course/modules/E/E3 pages, cards.json, grader and tests/labs/E3 (python regex scan, ledgers/E3/scripts/E3-f-r1/out and this round's notes): \\Lambda occurs 7 times, all in course/modules/E/E3/L03.html; \\iota 21 times, all in L03.html (plus cards E3-c036, c037, c188); \\Xi 50 times in L01.html only (plus 13 card words). None of these letters has a second meaning in E3. Lowercase \\lambda and \\xi/\\omega are distinct symbols under ruling 38.")
new("E3f-r18-notation-ruling33-letters", "PASS", "Closing round 1: the base FAIL is resolved by ruling 38 (plans/FINAL-ARCHITECT-RULINGS.md:137-140, commit 892d74d5, inside this delta): 'Upper and lower case Greek letters are different symbols, so Xi (L01 mixture weight) and Omega (L05 and L08 Epstein-Zin exponent) stay'. Re-verified: \\Xi is the mixture weight in every one of its 50 uses in L01.html (lines 86, 91, 96, 98, 105, 107, 115, 119, 390, 392, 406, 422, 469), so it keeps one meaning. The remaining rename, the exponent b of Proposition 1.2 to Lambda (L03.html:78, 83; cards E3-c037 line 253), uses the letter absent elsewhere in E3 (grep above). Reading of ruling 38's 'absent in E3 in either case': taken as case-distinct, as its first sentence states; if it meant both cases, Lambda would fail because lowercase lambda occurs in E3 (L05, L06, L08, project). Flagged for architect confirmation in notes; not a row.")
new("E3f-dag-L02-crra-forward-use", "PASS", "Closing round 1: check_dag E3 PASS (out/check_dag_unit.out); the L03 hunks at lines 78, 83, 326 contain no concept link or dfn (git diff reviewed). The forward-use prose is unchanged.")
new("E3f-dag-other-links", "PASS", "Closing round 1: check_dag E3 PASS (out/check_dag_unit.out). The delta changes no 'Uses'/'Introduces' line and no concept link on L01-L04.")
new("E3f-banned-and-process", "PASS", "Closing round 1: changed visible prose (L03.html:78, 83, 326; cards E3-c037, c134, c157, c158) scanned for process words (round, ruling, verifier, fixer, ledger, TODO, placeholder); no hit. The word 'rounded' at L03.html:326 is the mathematical rounding, not a process word.")
new("E3f-banned-cards", "PASS", "Closing round 1: process-word scan over the four changed cards (E3-c037, c134, c157, c158): no hit (out/cards_closing_r1.out, banned_hits_changed []). The full-file banned-string grep of the base round is carried; the changed entries are the only new text.")
new("E3f-coverage-cards", "PASS", "Closing round 1: the labelled block of Proposition 1.2 (L03.html:77 block-title 'Proposition 1.2 (powers of powers)' and data-grade T) is unchanged; the hunk at line 78 changes only the statement sentence. Other labelled blocks of L01-L04 are carried (their lines are not in the delta hunks).")
new("E3f-cards-integrity", "PASS", "Closing round 1: ledgers/E3/scripts/E3-f-r1/cards_closing_r1.py over course/modules/E/E3/cards.json: 178 cards, 178 distinct ids, same order as 4540351d; no extra keys; every grade in {T, C}; every C card has a basis or a cite; every cite key is in references/references.json (out/cards_closing_r1.out, integrity_problems []). Changed entries: E3-c037 (back text), E3-c134, E3-c157, E3-c158 (grade and cite fields removed, ruling 39). 174 entries byte-identical (out/cards_entry_identity_r1.out).")
new("E3f-cards-near-duplicates", "PASS", "Closing round 1: difflib scan of the four changed cards against all 177 others (front ratio > 0.8 or back ratio > 0.85): no pair (out/cards_closing_r1.out, near_duplicate_pairs_changed_vs_all []). No duplicate card created.")
new("E3f-cards-xrefs", "PASS", "Closing round 1: every Definition, Proposition, Theorem, Lemma, Example, Remark, Corollary label cited in the text of all 178 cards exists in its lesson page (out/cards_closing_r1.out, xref_missing_all_cards []). Changed cards: E3-c037 cites Proposition 1.2 (L03.html:77); E3-c134 cites Definition 1.2 (L07.html:64); E3-c157 cites Example 2.5 (L08.html:131); E3-c158 cites Definition 1.2 (L08.html:64).")
new("E3f-cards-numbers", "PASS", "Closing round 1: every number in the four changed cards' fronts and backs appears in its lesson page (out/cards_closing_r1.out, numbers_in_changed_cards_not_in_lesson []): 1979 (L07.html:80), 1989 (L08.html:67), 1961 (L08.html:133), 1.2 and 2.5 (block labels at L07.html:64, L08.html:64 and L08.html:131), and the lottery and exponent numbers of E3-c037 (L03.html:78). Other L01-L04 card numbers carried.")
new("E3f-cards-grades", "PASS", "Closing round 1: E3-c106 entry byte-identical, grade T, basis 'Example 2.3' (carried observation). The three grade removals (E3-c134, c157, c158) match L07.html:80 and L08.html:67, 133: each sentence now states that the page has not read the paper and cites it for no result, and the C rows of the grade tables were removed (L07 grade-table row removed, L08 two rows removed). Consistent with ruling 39.")
new("E3f-cards-slice-scan", "PASS", "Closing round 1: the 91 L01-L04 cards re-scanned for the changes of this delta. Only E3-c037 changed among them (and E3-c188 cites its unchanged second claim); the rest are byte-identical (out/cards_entry_identity_r1.out). Card-level rows below.")
new("E3f-E3-c037", "PASS", "Closing round 1: course/modules/E/E3/cards.json E3-c037 back now reads 'For w > 0 and real iota and Lambda, (w^iota)^Lambda = w^(iota Lambda) (Proposition 1.2).' Matches the statement at L03.html:78 letter for letter and the proof at line 83. grade T unchanged.")
new("E3f-E3-c188", "PASS", "Closing round 1: E3-c188 entry byte-identical. Its cited claim, (xy)^c = x^c y^c (Proposition 1.2), is the second sentence of L03.html:78, which is text-identical to the pre-delta line (diff shows the change is confined to the first claim).")
new("E3f-r14-cards-unsampled", "PASS", "Closing round 1: the three cards of this list changed in this delta were re-verified against the changed L07 and L08 text: E3-c134 against L07.html:80 (title-only, no result, Definition 1.2 non-cumulative value at L07.html:64), E3-c157 against L08.html:133 (Example 2.5 block at 131), E3-c158 against L08.html:67 (Definition 1.2 at 64; V_tau formula unchanged). Their 'cite' and 'grade' fields are gone (cards.json) and the C rows of the grade tables are gone (L07, L08), as ruling 39 states. The other 26 cards of the list are carried: their entries are byte-identical and their cited blocks sit outside the L05, L06, L07 and L08 hunks.")
new("E3f-r15-delta", "PASS", "Closing round 1 delta 4540351d..2a805c83 read in full for the slice: course/modules/E/E3/L03.html three hunks (line 78 statement of Proposition 1.2 b -> Lambda; line 83 proof; line 326 interpretation sentence, see E3f-lab-L03); course/modules/E/E3/cards.json four entries (E3-c037 text; E3-c134, E3-c157, E3-c158 cite and grade fields removed). Byte-identical since the pin: L01.html, L02.html, L04.html, tests/labs/E3 twins, grader, index.html, notation/notation.json, references/references.json. L05.html (499, 620), L06.html (545), L07.html (47, 80, 463, 571), L08.html (47, 67, 133, 479, 620, 725) and project.html (648) changed in other slices: read for the cards that depend on them, observations in notes.")
new("E3f-cmd-grader-not-in-slice", "PASS", "Carried from round 18 (course/modules/E/E3/grader/* byte-identical since the previous pin 4540351d; git diff --quiet clean): the E3 project grader is outside this slice.")

changed_ids = {"E3-c037", "E3-c134", "E3-c157", "E3-c158", "E3-c188"}
rows = []
for r in base["rows"]:
    rid = r["id"]
    if rid in NEW:
        status, ev, fix = NEW[rid]
        row = {"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev}
        if fix:
            row["fix"] = fix
        rows.append(row)
        continue
    # carry: pick prefix
    if rid.startswith("E3f-E3-c") or rid.startswith("E3f-r18-changed-card-E3-c") or rid == "E3f-E3-r7-independent-rederivation":
        cid = rid.replace("E3f-", "").replace("r18-changed-card-", "")
        if rid == "E3f-E3-r7-independent-rederivation":
            prefix = "Carried from round 18 (ledgers/E3/scripts/E3-f-r15/*.py byte-identical since the previous pin 4540351d; L01-L04 numbers re-derived this round where changed):"
        else:
            prefix = P["CARDS"].format(id=cid)
    elif rid in ("E3f-lab-L01", "E3f-lesson-numbers-L01", "E3f-r14-L01-proofs", "E3f-notation-alpha"):
        prefix = P["L01"]
    elif rid in ("E3f-lab-L02", "E3f-lesson-numbers-L02", "E3f-r14-L02-prop31-proof", "E3f-r14-L02-prop31-limit", "E3f-r14-L02-proofs", "E3f-notation-kappa", "E3f-r14-notation-eps", "E3f-references"):
        prefix = P["L02"]
    elif rid in ("E3f-lab-L04", "E3f-lesson-numbers-L04", "E3f-r14-L04-theorems", "E3f-r14-L04-proofs"):
        prefix = P["L04"]
    elif rid in ("E3f-r15-notation-tilde-L03", "E3f-r14-notation-eta", "E3f-hours", "E3f-L03-references"):
        prefix = P["L03"]
    elif rid.startswith("E3f-r14-cards-sample-") or rid == "E3f-r15-cards-changed-L05-L08" or rid == "E3f-r14-cards-unsampled":
        prefix = ("Carried from round 18 (the cited cards.json entries byte-identical, and the cited blocks of L05, L06, L07 and L08 outside this delta's hunks, since the previous pin 4540351d; the cards E3-c134, c157, c158 of the list are re-verified above):")
    else:
        raise SystemExit("no carry prefix for " + rid)
    if r["status"] != "PASS":
        raise SystemExit("non-PASS base row not re-verified: " + rid)
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": carry(prefix, r)})

# every base id kept
assert [r["id"] for r in rows] == [r["id"] for r in base["rows"]], "ids/order differ"
from collections import Counter
cnt = Counter(r["status"] for r in rows)
verdict = "PASS" if cnt["PASS"] == len(rows) else "FAIL"
fragment = {
    "unit": "E3",
    "slice": "f",
    "round": 1,
    "verifier": "Claude Haiku 5.5, independent closing-delta verifier for E3-f, round 1 (did not build E3)",
    "pin": PIN,
    "base": BASE_PIN + " (round-18 base fragment ~/.fanout/frags/D-E3-f.round18.json; closing delta 4540351d..2a805c83)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyG1-E3-f",
    "scratch": "ledgers/E3/scripts/E3-f-r1/",
    "verified_at": "2026-11-09T17:20:00+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Ruling 30 closing delta: scope = rows of the base fragment whose subject changed in git diff 4540351d..2a805c83 for this slice (L03.html hunks at lines 78, 83, 326; cards.json entries E3-c037, c134, c157, c158) plus every base non-PASS row (E3f-r18-notation-ruling33-letters). Every other base row is carried with the carry prefix and its base evidence. Row ids are all kept (161 rows, same order).",
        "Ruling 37: no new mutants. mutants is []: slice f has no project grader, and the lab twins are demonstrations (ruling for project graders only).",
        "Base FAIL E3f-r18-notation-ruling33-letters is PASS: ruling 38 (plans/FINAL-ARCHITECT-RULINGS.md lines 137-140) keeps capital Xi and Omega and names the remaining rename, b to Lambda, in L03. Ambiguity for the architect: ruling 38 says 'a letter absent in E3 in either case'. This verifier read it case-distinct, as its first sentence does. If it means that both upper and lower case must be absent, Lambda fails (lowercase lambda occurs in L05, L06, L08 and project.html). Request: confirm the reading.",
        "Observation, outside slice f (route to the L05-L08 slice verifier, not a row here): the closing delta changed the footers of L05.html:620, L06.html:545, L07.html:570 and L08.html:723 from 'Each graded result carries a proof or a lab result labelled C.' to 'Every substantive claim carries an evidence grade and at least one citation key from the verified registry.' Ruling 39 (plans/FINAL-ARCHITECT-RULINGS.md lines 141-145) says the footers of L05 to L08 'then read Each graded result carries a proof or a lab result labelled C.' The L01-L04 footers still read the ruling text, so the change contradicts ruling 39.",
        "Observation, outside slice f: L05.html:499 (a grade-table row wording: 'their marginal rates of substitution differ') and L05.html:620 changed in this delta; the L05 row is not covered by ruling 39 and is routed to the L05 slice. The cards of slice f that cite L05 Definition 1.1, Theorem 1.3, Remark 3.4 and Corollary 3.3 are carried because their cited blocks are outside these hunks.",
        "Observation: the base notes described the L03 interpretation paragraph (L03.html:326) as covered; the defect found in it this round is in the sentence this delta introduced (see E3f-lab-L03).",
        "Correction to the base: row E3f-r14-notation-tau said 'mixture weight, now rho'. L01 Definition 2.1 uses \\Xi (L01.html:86), not rho; the row is re-verified on that basis.",
        "Not checked: tests/test_lx1_project_lab3.py (an LX1 test, outside this slice) was not run in this round; the E3 subset and the non-LX1 lab subset pass. Gate runs were not repeated for other units.",
        "Scripts: ledgers/E3/scripts/E3-f-r1/gates_r1.sh (gates), twin_check_r1.py, cards_closing_r1.py, rederive_r1.py, build_fragment_r1.py; outputs in ledgers/E3/scripts/E3-f-r1/out/.",
    ],
    "summary": {
        "rows": len(rows),
        "pass": cnt["PASS"],
        "fail": cnt["FAIL"],
        "unverifiable": cnt["UNVERIFIABLE"],
    },
}
json.dump(fragment, open("ledgers/E3/E3-f.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("rows", len(rows), dict(cnt), "verdict", verdict)
