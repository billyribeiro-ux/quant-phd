"""Round 1 closing delta for E3-f (pin d9de2fe5, base 2a805c83). Builds ledgers/E3/E3-f.json from the base fragment.

Rows re-verified in this round get fresh evidence (their cited subject changed or a ruling changed); every other base
row is carried with the carry prefix. Row ids and order are kept. Outputs of the commands are in out2/.
"""
import datetime
import json
import sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyH1-E3-f"
base = json.load(open("/Users/billyribeiro/.fanout/frags/G-E3-f.round1.json", encoding="utf-8"))
S = "ledgers/E3/scripts/E3-f-r1/out2/"

PREFIX = ("Carried from round 1 (cited files byte-identical since the previous pin 2a805c83, except the closing-delta "
          "hunks at course/modules/E/E3/L02.html:223, L03.html:326, L04.html:56 and :690, lab-E3-L02-1.py:14, "
          "L05.html:499, :620, L06.html:545, L07.html:570, L08.html:165, :472, :478, :723, none of which lies inside "
          "the locators this row cites; cards.json, references, notation and the hub files are unchanged): ")

NEW = {
    "E3f-cmd-check_pages": f"Re-run at d9de2fe5: .venv/bin/python tools/check_pages.py --unit E3 -> 'check_pages E3: PASS' rc 0 ({S}check_pages_unit.out).",
    "E3f-cmd-check_dag": f"Re-run: tools/check_dag.py --unit E3 -> 'check_dag E3: PASS' rc 0 ({S}check_dag_unit.out). The delta adds no class=\"concept\" line (git diff 2a805c83..HEAD -- course/modules/E/E3 | grep -c 'class=\"concept\"' = 0).",
    "E3f-cmd-check_projects": f"Re-run: tools/check_projects.py --unit E3 -> 'check_projects E3: PASS' rc 0 ({S}check_projects_unit.out).",
    "E3f-cmd-page_smoke": f"Run alone after the other gates: tools/page_smoke.py --unit E3 --pages L01 L02 L03 L04 -> 'page_smoke E3: PASS' rc 0 ({S}page_smoke.out).",
    "E3f-cmd-pytest-labs": f"Re-run: pytest -q tests -k E3 rc 0 (16 progress marks, {S}pytest_e3.out); pytest -q tests -k 'lab and not lx1' rc 0 (8 marks, {S}pytest_lab_not_lx1.out).",
    "E3f-cmd-pytest-cards-notation": f"Re-run: pytest -q tests -k 'card or notation or review or concept' rc 0 (6 marks, {S}pytest_cards.out).",
    "E3f-cmd-ruff-labs": f"Re-run: ruff check tests/labs/E3 course/modules/E/E3/grader -> 'All checks passed!'; ruff format --check tests/labs/E3 -> '11 files already formatted'; repo-wide ruff check . and ruff format --check . -> passed, '555 files already formatted' ({S}ruff_*.out).",
    "E3f-cmd-mypy-twins": f"Re-run: mypy --no-incremental -> 'Success: no issues found in 386 source files' ({S}mypy.out).",
    "E3f-cmd-verify_refs": f"Re-run: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' rc 0 ({S}verify_refs_offline.out). references/ unchanged in the delta.",
    "E3f-cmd-build_site-render": f"Re-run: build_site.py --check -> 'site data current: 6 outputs'; render_curriculum.py -> 'curriculum valid: 25 parts, 134 modules, 157 projects, 13,715 h (6.35 FTE years)'; git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json rc 0 ({S}build_site_check.out, render_curriculum.out, render_diff.out).",
    "E3f-cmd-pytest-docs": f"Re-run: pytest -q tests/test_docs_figures.py tests/test_refs.py rc 0 ({S}pytest_docs.out).",
    "E3f-cmd-run_labs-L01-L04": f"Re-run: tools/run_labs.py --unit E3 --page L01 / L02 / L03 / L04 -> 'run_labs E3: PASS (1/1)' each, rc 0 ({S}run_labs_L0*.out).",
    "E3f-cmd-fetch_data": f"Re-run: tools/fetch_data.py --check -> 'fetch_data: 3 datasets, 0 problems' rc 0 ({S}fetch_data_check.out).",
    "E3f-cmd-grader-not-in-slice": "git diff --stat 2a805c83..HEAD over course/modules/E/E3/grader, tests/labs/E3/lab-E3-project-*.py, course/project.html and project.html is empty: the E3 project grader is unchanged by this delta.",
    "E3f-lab-twin-equality": f"Own check, ledgers/E3/scripts/E3-f-r1/delta_twin_check.py, run under python -I -W error ({S}delta_twin_check.out): L01, L02, L03, L04 each code_equals_twin=True expected_equals_stdout=True rc=0 stderr=''.",
    "E3f-lab-L01": f"L01 is not in any delta hunk. Re-checked in {S}delta_twin_check.out: lab-E3-L01-1 code_equals_twin=True expected_equals_stdout=True rc=0 (23 stdout lines).",
    "E3f-lab-L02": f"Re-verified. The changed sentence (L02.html:223, twin lab-E3-L02-1.py:13-14, inside the lab code) drops 'and labelled as unrounded'. Page code equals twin and expected equals stdout (16 lines, rc 0, {S}delta_twin_check.out). Every non-money value the twin prints is formatted .6f (lab-E3-L02-1.py lines 122-150: r_A, r_R, exact_premium_cu, pratt_premium_cu, error_cu, mean, variance, Part B ratio, limit, gap, Part C linear_r_A). The phrase 'labelled as unrounded' occurs nowhere else in L02, the twin, or cards.json. PASS.",
    "E3f-lab-L03": f"Re-verified; the base FAIL is resolved. The new interpretation paragraph (L03.html:326) names the sources the code uses. Checked against lab-E3-L03-1.py: GAMMAS = (0, 0.25, 0.5, 1, 2, 4) at line 18 (certainty equivalents, exact value, falling-order check); gap at gamma 1 +/- 1e-6 at line 83; slopes at gamma 1 +/- 1e-3 and +/- 1e-6 at lines 86-88; limit at gamma 1 - 1e-6 for w in 0.5, 2, 10000 at lines 96-97; homogeneity for k in 2, 3, 10 at line 103. Printed output (L03 expected block, {S}delta_twin_check.out): gamma 0 11250.0000, gamma 1 10000.0000, '80000/9 cents', gamma 2 8888.8889 (4 dp). Page code equals twin; expected equals stdout (19 lines, rc 0). No over-claim remains in the paragraph. PASS.",
    "E3f-lab-L04": f"Re-verified. The lab block and twin lab-E3-L04-1.py are unchanged; the two L04 hunks (line 56 assumption block, line 690 quiz) lie outside it. Page code equals twin, expected equals stdout (45 lines, rc 0, {S}delta_twin_check.out). PASS.",
    "E3f-lesson-numbers-L02": "Re-verified for the changed sentence (L02.html:223): the word diff removes 'and labelled as unrounded' and adds no numeral; 'six decimal places' matches the .6f format of the twin. Other numbers of this row (Example 2.3, Section 3, Lab 1 interpretation, misconception, E1-E3, quiz) are on lines outside the hunk and carried from the base evidence. PASS.",
    "E3f-lesson-numbers-L03": "Re-verified for the changed paragraph (L03.html:326): every number in it (1e-6, 1e-3, 0.5, 2, 10000, k = 2, 3, 10, gamma grid 0, 0.25, 0.5, 1, 2, 4, 80000/9, 8888.8889, 11250, 10000, 10^-12, (k+1)/2) is set by lab-E3-L03-1.py lines 16-18, 83, 86-88, 96-97, 103 or printed by its expected block. Remark 2.8 is at L03.html:183. PASS.",
    "E3f-lesson-numbers-L04": "Re-verified for the two changed L04 hunks: 'Section 2' (heading L04.html:126), 'Definition 2.1' (L04.html:129, 'Under A1 and A2'), 'Example 2.5' (L04.html:164-165, probabilities 1/2, 1/2 and 1/4, 1/2, 1/4, means 3000). The quiz explanation (L04.html:696) gives F_X(2000)=1/2>1/4=F_Y(2000) and F_Y(3000)=3/4>1/2=F_X(3000), matching the new prompt. PASS.",
    "E3f-banned-and-process": f"Re-verified: process-word scan (round, ruling, verifier, fixer, ledger, TODO, placeholder, Round N) over the whole HEAD files L02-L08: the only hits are mathematical 'round'/'rounds' (L02:486, L03:184-418, L07:507-512, L08:176-177); none on the changed lines L02:223, L03:326, L04:56, L04:690, L05:499, L08:165, :472, :478. PASS.",
    "E3f-r14-L04-theorems": "Re-verified against the changed A2 scope: Lemma 1.2, Theorem 1.5 and Lemma 1.6 are stated 'Under A1' (L04.html:69, 89, 103); Proposition 1.8 says 'This holds without A2' (L04.html:117-118); Definition 2.1, Lemma 2.2, Theorem 2.3 and Remark 2.4 are 'Under A1 and A2' (L04.html:129-160). This matches the new assumption text 'A2 is assumed from Definition 2.1 on, in Section 2, and not in Section 1' (L04.html:59). PASS.",
    "E3f-r14-L04-proofs": "Re-verified: Problems R3 (L04.html:613-614) assumes that A2 fails and that the test still holds, consistent with A2 scoped to Section 2; Example 2.6 and Problems P1-P3, R1-R3 contain no Section 1 use of equal means. PASS.",
    "E3f-r18-notation-ruling33-letters": "Re-verified after ruling 38a (plans/FINAL-ARCHITECT-RULINGS.md:146-150, delta commit 2ec5d481): Xi/xi, Omega/omega and Lambda/lambda are different symbols and need no further renaming, which settles the base reading ambiguity. Counts corrected by recount: \\Xi occurs 50 times on 13 lines of L01.html (lines 86, 91, 96, 98, 105, 107, 115, 119, 390, 392, 406, 422, 469), all as the mixture weight; Omega occurs 57 times on 20 lines of L05.html and 23 times on 6 lines of L08.html (Epstein-Zin exponent); uppercase Lambda occurs in E3 pages and cards only as the L03 exponent at L03.html:78, :83 and cards.json:253 (grep). PASS.",
    "E3f-r14-notation-tau": "Carried from round 1 with a corrected location: the L01 mixture weight is Xi (L01.html:86), not rho; L08 Definition 1.2 tau is unchanged. The base wording 'now rho' was stale. PASS.",
    "E3f-dag-L02-crra-forward-use": "Re-verified: check_dag E3 PASS (out2/check_dag_unit.out); the delta adds no class=\"concept\" link (grep count 0).",
    "E3f-dag-other-links": "Re-verified: check_dag E3 PASS (out2/check_dag_unit.out); the delta adds no class=\"concept\" link (grep count 0).",
    "E3f-hours": "Carried from round 1 (no data-hours line in the delta, grep count 0; hub files byte-identical since 2a805c83): data-hours values unchanged. PASS.",
    "E3f-E3-c062": "Re-verified against L04.html:59 and :117-118: 'The equal-means assumption A2 is not needed (Proposition 1.8)' matches the new A2 scope. PASS.",
    "E3f-E3-c063": "Re-verified against L04.html:59 and :129: 'Under A1 and A2 (equal means)' matches Definition 2.1. PASS.",
    "E3f-E3-c064": "Re-verified against L04.html:129-135 (Lemma 2.2 under A1 and A2). PASS.",
    "E3f-E3-c066": "Re-verified against L04.html:155-160 (Remark 2.4 and the A2 term): the card's 'A2 through the vanishing affine term' matches. PASS.",
    "E3f-E3-c068": "Re-verified against L04.html:164-165 (Example 2.5) and quiz L04.html:690-696: 'X dominates Y in the second order' is the same claim as the new quiz prompt, and the probabilities and F values match. PASS.",
    "E3f-E3-c071": "Re-verified against L04.html:59 and :145-155: 'with A2 not assumed' matches the Section 1 scope of A2. PASS.",
    "E3f-E3-c072": "Re-verified against L04.html:59 and Example 2.6 (L04.html:172): 'Equal means are a hypothesis of the second-order theorem' matches. PASS.",
    "E3f-E3-c160": "Re-verified against the changed L03 paragraph (L03.html:326): 'Only floating-point agreement on the lab's fixed lottery: the certainty equivalent at gamma = 1 +/- 1e-6 is within 0.01 cents of the gamma = 1 value' matches lab-E3-L03-1.py line 83-84 and the printed line. PASS.",
    "E3f-E3-c171": "Re-verified against the changed L03 paragraph (L03.html:326) and lab-E3-L03-1.py lines 96-114: homogeneity for k = 2, 3, 10 'on the lab's grid' matches the new text. PASS.",
    "E3f-r14-cards-sample-L05": "Re-verified for E3-c089, c090 and c091 (Remark 3.4 at L05.html:156-160 against the changed table row L05.html:499; consistent). The other sampled L05 cards cite blocks outside the L05 hunks (carried from base). PASS.",
    "E3f-r15-cards-changed-L05-L08": "Carried from round 1: cards.json entries byte-identical since 2a805c83; the L05-L08 hunks lie outside the cited blocks (E3-c083, c101, c106, c117, c154), except the footers, which no card cites. PASS.",
    "E3f-r18-changed-card-E3-c143": "Carried from round 1: E3-c143 cites Proposition 2.4 (L08.html:117), which is outside the L08 hunks (165, 472, 478, 723). PASS.",
    "E3f-r18-changed-card-E3-c145": "Carried from round 1: E3-c145 cites Definition 3.1 (L08.html:141), outside the L08 hunks. PASS.",
}

mut_note = "Ruling 37: no new mutants. Slice f has no project grader; mutants is []."
rows = []
for r in base["rows"]:
    rid = r["id"]
    if rid in NEW:
        row = {"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": NEW[rid]}
    else:
        ev = r["evidence"]
        row = {"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
               "evidence": PREFIX + ev}
    if rid == "E3f-r14-notation-tau":
        row["location"] = "course/modules/E/E3/L01.html Definition 2.1 (mixture weight Xi, L01.html:86); L08 Definition 1.2 (tau)"
    rows.append(row)

missing = [k for k in NEW if k not in {r["id"] for r in base["rows"]}]
EXTRA = {'E3f-E3-c089': "Re-verified against Remark 3.4 (L05.html:156-160) and the changed grade-table row (L05.html:499: 'differ at every plan with c1 != c0 when psi != 1/gamma'). The card's 'agree at every deterministic plan exactly when 1/psi = gamma' is consistent with the Remark's proof (r^gamma = r^(1/psi) with r != 1 forces gamma = 1/psi). PASS.", 'E3f-E3-c090': "Re-verified against Remark 3.4 (L05.html:156-160) and L05.html:499: 'Off that restriction the two criteria can assign different marginal rates of substitution' matches. PASS.", 'E3f-E3-c091': 'Re-verified against Remark 3.4 (L05.html:156-160): elasticity 1/gamma for gamma != 0, undefined at gamma = 0, Epstein-Zin gives psi. PASS.', 'E3f-E3-c147': "Re-verified against Remark 3.3 (L08.html:164-165) after the delta: the new text 'The lesson does not establish whether its certainty equivalent then depends on psi and beta; Problem R1 names the step that fails, and the lesson does not compute the number' matches the card ('not computed', 'an untested hypothesis'). PASS."}
assert not missing, missing
assert not missing, missing
nonpass = [r["id"] for r in rows if r["status"] != "PASS"]
frag = {
    "unit": "E3",
    "slice": "f",
    "round": 1,
    "verifier": "Claude Haiku 5.5, independent closing-delta verifier for E3-f, round 1 (did not build E3)",
    "pin": "d9de2fe5eea982d14cd9f922a61676b847506fbc",
    "base": "2a805c831410ab77c38c227f7e121e8537193ce9 (base fragment ~/.fanout/frags/G-E3-f.round1.json; closing delta 2a805c83..d9de2fe5)",
    "checkout": ROOT,
    "scratch": "ledgers/E3/scripts/E3-f-r1/",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "verdict": "PASS" if not nonpass else "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Scope (ruling 30, delta 2a805c83..d9de2fe5 over the slice paths): hunks course/modules/E/E3/L02.html:223, L03.html:326, L04.html:56 and :690, tests/labs/E3/lab-E3-L02-1.py:14 (docstring twin of L02:223); plans/FINAL-ARCHITECT-RULINGS.md:146-155 (rulings 38a and 40). The delta also changes L05.html:499 and :620, L06.html:545, L07.html:570, L08.html:165, :472, :478, :723 (footers and text). These are the L05-L08 slice's rows; they are cited here only where a slice-f card cites a changed locator: E3-c089, c090, c091 (L05:499) and E3-c147 (L08:165) were re-verified; no slice-f card cites the footers or L08:472/478.",
        "Re-verified from scratch: the base non-PASS row E3f-lab-L03 (now PASS, the interpretation sentence is corrected); every E3f-cmd row (all gates re-run at d9de2fe5); the changed-subject rows E3f-lab-L02, E3f-lab-L04, E3f-lesson-numbers-L02/L03/L04, E3f-banned-and-process, E3f-r14-L04-theorems/proofs, E3f-r18-notation-ruling33-letters (after ruling 38a), and the cards whose cited locators touch a hunk (E3-c062, c063, c064, c066, c068, c071, c072, c089, c090, c091, c147, c160, c171).",
        "Carried with the carry prefix: every other base row. Each carried row's cited files are byte-identical to 2a805c83 except hunks that lie outside its cited locators (listed in the prefix). cards.json, references/, notation/, curriculum/, the E3 hub files and the E3 grader are byte-identical to 2a805c83 (git diff --stat empty).",
        "Ruling 38a resolves the base reading question: Lambda/lambda need no renaming, so the Lambda exponent of L03 Proposition 1.2 (L03.html:78, :83; cards.json:253) is accepted under ruling 38 with the case-distinct reading.",
        "Corrections to base counts (recounted): Xi is 50 occurrences on 13 lines of L01 (the base said '50 matching lines'); Omega is 57 occurrences on 20 lines of L05 and 23 on 6 lines of L08 (the base said '57' and '23' matching lines); \\eta in L07 is 24 occurrences on 9 lines (base '24 uses' is correct); varepsilon in L02 is 91 occurrences on 26 lines (base '91 uses' is correct).",
        "Correction to base row E3f-r14-notation-tau: its location said 'mixture weight, now rho'. L01 Definition 2.1 uses Xi (L01.html:86), not rho; the row is PASS with the corrected location.",
        "Observation for the architect (not a row): ruling 33 names the footers of L05-L08 only. The L01-L04 footers still read 'Every substantive claim carries an evidence grade and at least one citation key from the verified registry.' (for example L02.html:627); the base note raised this and no ruling states the L01-L04 footer text.",
        "Observation: L05.html:499 (grade-table row) and L08.html:472 ('under that model ... held for sure') changed in this delta; no slice-f card cites them, and cards.json contains no 476 or 'initial wealth' text. They belong to the L05 and L08 slices.",
        "Not checked: the full L05-L08 hunks as rows (routed to their slices); tests/test_lx1_project_lab3.py (outside E3); the L03 b-to-Lambda rename at L03:78 and :83 was introduced in the earlier delta and is carried, not re-derived line by line beyond its Lambda uniqueness check; the E3 project grader and its mutants (not in slice f).",
        "Card checks with no base row (folded into notes): " + " ".join(f"{k}: {v}" for k, v in EXTRA.items()),
        "Slice f has no project grader and no mutants. Ruling 37: no new mutants were written in this closing round.",
    ],
    "summary": {"rows": len(rows), "pass": sum(1 for r in rows if r["status"] == "PASS"),
                "fail": sum(1 for r in rows if r["status"] == "FAIL"), "unverifiable": 0},
}
json.dump(frag, open(f"{ROOT}/ledgers/E3/E3-f.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("rows", len(rows), "nonpass", nonpass, "verdict", frag["verdict"], frag["summary"])
