"""Write ledgers/E3/E3-e.json (round 1, closing delta 4540351d..2a805c83) from the round-18 base fragment."""
import json, re, pathlib, sys
from datetime import date

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyG1-E3-e")
BASE = json.load(open("/Users/billyribeiro/.fanout/frags/D-E3-e.round18.json", encoding="utf-8"))
OUT = "/tmp/e3e_r1/rows_out.json"
CARRY = "Carried from round 18 (cited subject byte-identical since 4540351d; the subject is named in the next clause): "
OUTD = "ledgers/E3/scripts/E3-e-r1/out/"


def base_ev(rid):
    ev = next(r["evidence"] for r in BASE["rows"] if r["id"] == rid)
    return re.sub(r"^Carried from round \d+ \(.*?\):\s*", "", ev)


def base_row(rid):
    return next(r for r in BASE["rows"] if r["id"] == rid)


CARRY_IDS = {
    "E3e-r14-twins-L05-L08-lint": "tests/labs/E3/ twins (git diff 4540351d..HEAD empty for tests/labs/E3); ruff and mypy on the twins not re-run this round",
    "E3e-r14-registry-crossref-live": "references/references.json, notation/notation.json (git diff empty); live Crossref not re-run",
    "E3e-r14-hub-structure": "course/modules/E/E3/index.html (git diff empty)",
    "E3e-r14-hub-placement-arithmetic": "course/modules/E/E3/index.html (git diff empty)",
    "E3e-r14-hub-data-and-labs-claims": "course/modules/E/E3/index.html and the L01, L03 twins (git diff empty)",
    "E3e-r14-hub-unlocks-and-titles": "course/modules/E/E3/index.html (git diff empty); h1 tags of L01-L08 unchanged (structure_compare.out h1_same True)",
    "E3e-r14-hub-reading-list": "course/modules/E/E3/index.html and L02.html (git diff empty)",
    "E3e-r14-hub-ladder-rungs-3-4": "course/modules/E/E3/index.html (git diff empty); project.html changed only at line 648, outside the ladder",
    "E3e-r14-hub-lesson-titles-match": "course/modules/E/E3/index.html (git diff empty); h1 tags of L01-L08 unchanged (structure_compare.out)",
    "E3e-r14-hub-E1-M4-released-claim": "course/modules/E/E3/index.html (git diff empty)",
    "E3e-r14-hub-rung1-generated-participant": "course/modules/E/E3/index.html (git diff empty); project.html:44 outside the hunk at line 648",
    "E3e-r14-why-it-matters": "why-it-matters paragraphs of L01-L08 (line 51 in L04; hunks at L05 496-502, 617-622, L06 542-547, L07 44-50, 77-83, 460-465, 567-572, L08 44-50, 64-70, 130-136, 476-482, 617-622, 720-725 do not touch them)",
    "E3e-r14-quiz-and-explanations": "L01 quiz lines, L05 lines 538 and 547, L06 lines 495, 518, 521-527, L08 line 586 (outside the hunks)",
    "E3e-r14-plan-rulings-6-8": "plans/E3-build-plan.md (git diff empty); the new rulings 37-39 are checked in E3e-r19-* rows",
    "E3e-r14-L04-theorems": "course/modules/E/E3/L04.html (git diff empty)",
    "E3e-r14-plan-lesson-guidance": "plans/E3-build-plan.md section 5 (git diff empty); the Ellsberg and Gilboa guidance at plans/E3-build-plan.md:273-275 ('cited by key only') is superseded by ruling 39 (no registry key on the page), recorded in notes",
    "E3e-r14-L05-math": "L05.html:64-86, :116-119, :130-131, :141-142 (outside hunks 496-502 and 617-622)",
    "E3e-r14-L05-lab-claims": "L05 lab section and tests/labs/E3/lab-E3-L05-1.py (twin unchanged; lab section outside the hunks; lab_exact.out re-run)",
    "E3e-r14-L06-math": "L06.html:63-69, :93-123, :127-131, :284-290 (the only L06 hunk is at 542-547, the footer)",
    "E3e-r14-L06-lab-claims": "L06 lab section and tests/labs/E3/lab-E3-L06-1.py (only the footer changed in L06)",
    "E3e-r14-L07-prop-and-examples": "L07.html Remark 1.3 (line 71), Proposition 2.2 (line 123) and the examples, outside the hunks at 44-50, 77-83, 460-465, 567-572",
    "E3e-r14-L08-math": "L08.html:141-160 and :585-587 (outside hunks at 130-136, 476-482, 617-622, 720-725)",
    "E3e-r14-L01-numbers": "course/modules/E/E3/L01.html (git diff empty); tests/labs/E3/lab-E3-L01-1.py",
    "E3e-r14-L02-numbers": "course/modules/E/E3/L02.html (git diff empty)",
    "E3e-r14-L02-lab-claims": "course/modules/E/E3/L02.html and its lab (git diff empty)",
    "E3e-r14-L02-prop3.1-undefined-q": "course/modules/E/E3/L02.html:195-199 (git diff empty)",
    "E3e-r14-notation-v": "L01.html:148, L02.html:149 (git diff empty), L03.html:174, :184, :432 (outside hunks 75-86, 323-329), L06-L08 value function lines (outside hunks)",
    "E3e-r14-notation-eps": "L02.html:164-217 and L05.html EIS lines (outside hunks)",
    "E3e-r14-DAG-convexity-term": "L06.html:74, :133, :247, :272, :431, :438, :460 (outside hunk 542-547)",
    "E3e-r14-contested-counter-side": "L06.html:298; L07.html:52 and :324 (outside hunks 44-50, 77-83, 460-465, 567-572)",
    "E3e-r15-notation-a": "L01.html:133-153, :326, :397, :470, :503, :512; L02.html:149, :407, :525, :582, :586; L07.html:323, :429-431 (outside hunks)",
    "E3e-r15-notation-W": "L02.html (git diff empty); L06.html:69-133 (outside hunk 542-547)",
    "E3e-r18-L01-prose": "course/modules/E/E3/L01.html (git diff empty); L06.html:56-58 (outside hunk 542-547)",
}

RE_VERIFIED = {
    "E3e-r14-gate-check-pages": ("PASS", "tools/check_pages.py --unit E3; course/modules/E/E3/index.html, L01-L08.html, project.html",
        "Re-run this round on pin 2a805c83: ledgers/E3/scripts/E3-e-r1/out/check_pages_E3.out = 'check_pages E3: PASS', exit 0. The gate does not test footer wording or grade attributes; those are rows E3e-r18-footers-L05-L06, E3e-r19-footers-L07-L08."),
    "E3e-r14-gate-check-dag": ("PASS", "tools/check_dag.py --unit E3; course/modules/E/E3",
        "Re-run this round: ledgers/E3/scripts/E3-e-r1/out/check_dag_E3.out = 'check_dag E3: PASS', exit 0."),
    "E3e-r14-gate-check-projects": ("PASS", "tools/check_projects.py --unit E3",
        "Re-run this round: ledgers/E3/scripts/E3-e-r1/out/check_projects_E3.out = 'check_projects E3: PASS', exit 0. The project slice itself is not judged here."),
    "E3e-r14-gate-run-labs-L05-L08": ("PASS", "tools/run_labs.py --unit E3; lab sections in L01-L08.html",
        "Re-run this round: ledgers/E3/scripts/E3-e-r1/out/run_labs_E3.out = 'run_labs E3: PASS (11/11)', exit 0."),
    "E3e-r14-gate-page-smoke": ("PASS", "tools/page_smoke.py --unit E3 --skip-sweep; index.html, L01-L08.html, project.html",
        "Re-run this round: ledgers/E3/scripts/E3-e-r1/out/page_smoke_E3.out, every page 'PASS', 'page_smoke E3: PASS', exit 0 (the figure sweep is skipped; E3 has no live figure)."),
    "E3e-r14-twins-L05-L08-run": ("PASS", "tests/labs/E3/lab-E3-L01-1.py, lab-E3-L03-1.py, lab-E3-L05-1.py, lab-E3-L06-1.py, lab-E3-L08-1.py",
        "Re-run this round with lab_exact.py (ledgers/E3/scripts/E3-e-r1/out/lab_exact.out): each twin runs under python -I -W error, exit 0, stderr_bytes 0; page code == twin True for L01, L03, L05, L06, L08. The twins are byte-identical to 4540351d (git diff empty)."),
    "E3e-r14-verify-refs-offline": ("PASS", "references/references.json; tools/verify_refs.py --offline",
        "Re-run this round: ledgers/E3/scripts/E3-e-r1/out/verify_refs_offline.out = 'offline integrity: 560 entries, 0 problems', exit 0."),
    "E3e-r14-pytest-relevant": ("PASS", "tests/test_labs.py, test_run_labs.py, test_page_checks.py, test_build_site.py, test_docs_figures.py, test_page_smoke.py, test_curriculum.py (-k 'E3 or L0 or lab or page or docs or site or curriculum')",
        "Re-run this round: ledgers/E3/scripts/E3-e-r1/out/pytest_relevant_full.out = '474 passed in 50.78s', exit 0. build_site --check re-run: build_site_check.out 'site data current: 6 outputs', exit 0."),
    "E3e-r14-lesson-hours": ("PASS", "L01-L08.html data-hours; course/modules/E/E3/index.html",
        "Re-run this round: structure_compare.out data_hours_same True for index.html and L01-L08.html (pins 4540351d and HEAD); 8 x 7 = 56 unchanged."),
    "E3e-r14-lesson-structure": ("PASS", "index.html and L01-L08.html; tags, h1, data-hours, dfn ids",
        "Re-run this round: structure_compare.out shows h1_same, data_hours_same and dfn_ids_same True for all nine files, and tags_same True for index, L01-L06. L07 and L08 tag multisets differ only by the removed registry rows, their <code> and <span> elements (diff of tag counts: L07 minus 1 code, 2 span, 3 td, 1 tr; L08 minus 2 code, 4 span, 6 td, 2 tr): the intended deletions of E3e-r15 ruling 39."),
    "E3e-r14-banned-strings": ("PASS", "index.html, L01-L08.html, project.html",
        "check_pages E3 PASS this round (check_pages_E3.out) applies the BUILDER_RULES banned-string scan to every E3 page, including the new sentences."),
    "E3e-r14-process-words": ("PASS", "added lines of course/modules/E/E3 in 4540351d..HEAD",
        "Regex scan of the added lines this round for round, verifier, builder, batch, todo, placeholder, reviewer, agent, ruling, fixer, architect, ledger: the only hit is the substring 'rounded' in the L03 interpretation line (ordinary English, not a process word)."),
    "E3e-r14-filler-and-rhetoric": ("PASS", "added lines of course/modules/E/E3 in 4540351d..HEAD (slice_delta.diff)",
        "All added lines read this round (ledgers/E3/scripts/E3-e-r1/slice_delta.diff). No filler or rhetoric added. The two sentences that overreach are graded in E3e-r19-L03-interp-scope and E3e-r18-footers-L05-L06 / E3e-r19-footers-L07-L08."),
    "E3e-r14-concept-dfn-and-links": ("PASS", "L01-L08.html; check_dag --all",
        "check_dag E3 PASS this round (check_dag_E3.out); structure_compare.out dfn_ids_same True for all nine files."),
    "E3e-r14-DAG-unlinked-names": ("PASS", "index.html, L01-L08.html",
        "check_dag E3 PASS this round (check_dag_E3.out). The delta adds no concept name; the added names (Kahneman and Tversky, Ellsberg, Gilboa and Schmeidler) are plain text, not concepts."),
    "E3e-r14-forward-pointers-allowed": ("PASS", "added lines of the delta",
        "The added lines add no forward pointer: L03 interpretation cites Remark 2.8 (L03.html:183), Proposition 2.6 (L03.html:163) and Proposition 1.2 as backward references; L07 and L08 registry sentences point nowhere forward."),
    "E3e-r14-grades": ("PASS", "L01-L08.html data-grade spans; key-results tables",
        "Re-verified: L07 has one C-graded result (L07.html:462, Observation 1.5 and Lab 1 part A) and no registry-title C claim; L08 has no C-graded result after the delta (grep data-grade over L08.html: T claims only); L08 T claims (Proposition 1.3 at L08.html:71, Theorem 2.2 at :98, Proposition 2.4 at :117, Proposition 3.2 at :148) each have a following Proof block. Grade attributes changed only by deletion (ruling 39)."),
    "E3e-r14-scope-words": ("PASS", "L01.html:334 and :403; L04.html:51; L05.html:131; L06.html:123; L08.html:67 and :479",
        "Re-verified this round: L08.html:67 'states no axiom or result from that paper' and L08.html:479 'used for their titles only' are checked by grep: Kahneman appears only in the naming sentence at L07.html:80, Gilboa at L08.html:67, Ellsberg at L08.html:133, and L08 names exactly two sources. Other cited lines are unchanged."),
    "E3e-r14-notation-registry": ("PASS", "notation/notation.json vs index.html, L01-L08.html",
        "symbol_sweep.out (this round): no hit for T, Phi, Q, R_f, gamma_3, gamma_4 in any E3 page; notation/notation.json byte-identical (git diff empty). The new symbols Lambda (L03), Xi (L01), Omega (L05, L08) are not registered and do not collide with a registered symbol."),
    "E3e-r14-cross-lesson-anchors": ("PASS", "L01-L08.html def-ids; check_dag --all",
        "structure_compare.out (this round): dfn_ids_same True for L01-L08; check_dag E3 PASS."),
    "E3e-r14-L03-numbers": ("PASS", "course/modules/E/E3/L03.html; tests/labs/E3/lab-E3-L03-1.py",
        "numeric_delta.out (this round): no number added or removed in L03.html. lab_exact.out: L03 expected block == stdout (len 1319 vs 1319). The interpretation paragraph's numbers (11250, 10000, 80000/9, 8888.8889, 1e-12, 0.1 percent, (k+1)/2) match the printed lines; its scope claim is graded in E3e-r19-L03-interp-scope."),
    "E3e-r14-L03-proofs-and-citations": ("PASS", "L03.html:66-67, :72-73, :77-83 (Proposition 1.2 with Lambda), :121-122, :133-134, :183-184",
        "Re-derived this round: Proposition 1.2 (L03.html:77-78) and its proof (L03.html:83): (w^iota)^Lambda = e^{Lambda ln(w^iota)} = e^{iota Lambda ln w} = w^{iota Lambda}, from ln(e^y)=y and ln(w^iota)=iota ln w; the second claim is unchanged. Other citations are outside the hunks."),
    "E3e-r14-L07-numbers": ("PASS", "course/modules/E/E3/L07.html",
        "numeric_delta.out (this round): the only numeric tokens removed from L07 are the years 1979 of the deleted registry-title claim and its table row; none added. The L07 C-graded lab result (L07.html:462) is unchanged."),
    "E3e-r14-L07-lab-claims": ("PASS", "course/modules/E/E3/L07.html lab; tests/labs/E3/lab-E3-L07-1.py",
        "run_labs.out (this round): E3 11/11 PASS. The lab-backed C row (L07.html:462, 'Observation 1.5; Lab 1, part A') is unchanged."),
    "E3e-r14-L08-numbers": ("PASS", "course/modules/E/E3/L08.html; tests/labs/E3/lab-E3-L08-1.py",
        "numeric_delta.out (this round): removed tokens are the years 1961 and 1989 of the deleted registry-title claims; none added. lab_exact.out: L08 expected block == stdout (len 1987 vs 1987)."),
    "E3e-r14-L08-lab-claims": ("PASS", "course/modules/E/E3/L08.html lab; tests/labs/E3/lab-E3-L08-1.py",
        "lab_exact.out (this round): page code == twin True; exit 0; stderr 0 bytes; expected == stdout."),
    "E3e-r15-footers-registry-claim": ("PASS", "course/modules/E/E3/L07.html:80, :463 (removed); L08.html:67, :133, :620-621 (removed); cards E3-c134, c157, c158",
        "Ruling 39 items re-checked: the three registry-title claims are now ungraded naming sentences with the words 'this page has not read the paper and cites it for no result' (L07.html:80, L08.html:67, L08.html:133); their data-grade and data-cite are gone (grep data-cite: 0 in L05-L08); the C rows of the L07 and L08 grade tables are deleted; cards E3-c134, E3-c157 and E3-c158 lost their grade and cite. What remains of the C-graded results on L07 and L08 is one lab result (L07.html:462). The footer wording on L07 and L08 no longer matches ruling 39 and is graded in E3e-r19-footers-L07-L08."),
    "E3e-r18-lab-exact": ("PASS", "course/modules/E/E3/L01.html, L03.html, L05.html, L06.html, L08.html; tests/labs/E3/lab-E3-L01-1.py, L03, L05, L06, L08",
        "Re-run this round: ledgers/E3/scripts/E3-e-r1/out/lab_exact.out: page code == twin True, exit 0, stderr 0 bytes, expected[0] == stdout True for L01 (1479), L03 (1319), L05 (1222), L06 (1050), L08 (1987)."),
    "E3e-r18-numeric-delta": ("PASS", "course/modules/E/E3/L03, L05, L06, L07, L08 .html, cards.json; project.html (observed)",
        "numeric_delta.out (this round): no numeric token added in any E3 page or card. Removed-only tokens: years 1961, 1979, 1989 of deleted registry-title claims. project.html is outside this slice; its changed number is in the notes."),
    "E3e-r18-symbol-sweep": ("PASS", "index.html and L01-L08.html math segments (symbol_sweep.out, greek_sweep.out this round)",
        "Re-run this round: Lambda occurs only in L03 (Proposition 1.2 and its proof); lambda (lowercase) is the loss-aversion coefficient in L06-L08 and project (see E3e-r19-notation-Lambda); Xi only in L01 (one meaning: mixture weight); Omega only in L05 and L08 (one meaning: 1 - 1/psi); the affine coefficient b occurs in L01, L02, L03:90 (cross-reference to L02 Proposition 2.2), L04 b_0, b_1 and L07 a + b, always the affine coefficient."),
    "E3e-r18-katex-render": ("PASS", "ledgers/E3/scripts/E3-e-r1/out/page_smoke_E3.out",
        "page_smoke E3 PASS this round (every page, including L03 with \\Lambda and L05 with \\Omega): zero unrendered math, no .katex-error."),
    "E3e-r18-footers-L01-L04": ("PASS", "course/modules/E/E3/L01.html:576, L02.html:627, L03.html:575, L04.html:728",
        "Re-verified: footers unchanged (grep this round: 'Each graded result carries a proof or a lab result labelled C.'). L03 C-graded results at L03.html:326 and :476 are lab results (Lab 1)."),
    "E3e-r18-index-carry-basis": ("PASS", "course/modules/E/E3/index.html",
        "git diff --stat 4540351d..HEAD -- course/modules/E/E3/index.html: empty (byte-identical); structure_compare.out index.html rows True."),
    "E3e-r18-notation-b": ("PASS", "L01.html:133-153, :397-399; L02.html:149-159, :407; L03.html:78, :83, :90; L04.html:153-154, :609, :616; L07.html:323, :429-431",
        "Re-verified after the L03 rename: b is the affine coefficient everywhere (u = a + b x, tilde u = a + b u, b_0 and b_1 as intercept and slope of the piecewise-linear L in L04.html:153, L07 omega(p) = a + bp). L03.html:90 'with b = 1' cites the L02 Proposition 2.2 affine slope. No b remains as the L03 exponent. The letter chosen for the exponent is judged under E3e-r19-notation-Lambda."),
    "E3e-r18-notation-ruling33-letters": ("PASS", "plans/FINAL-ARCHITECT-RULINGS.md:137-140 (ruling 38); L01.html Xi; L05.html and L08.html Omega; L02.html xi; L07.html omega",
        "Ruling 38 (plans/FINAL-ARCHITECT-RULINGS.md line 137) decides this row: Xi and Omega stay because upper and lower case are different symbols. Re-checked this round: Xi has one meaning (L01 mixture weight, symbol_sweep/greek_sweep), Omega has one meaning (1 - 1/psi, L05.html:65 and L08.html:142), xi (L02.html:113) and omega (L07.html:60-84) are different glyphs. The exponent rename, which ruling 38 also asks for, is judged in E3e-r19-notation-Lambda."),
}

NEW_ROWS = [
    {"id": "E3e-r18-footers-L05-L06", "check": "Footers of L05 and L06 read the sentence of ruling 39 ('Each graded result carries a proof or a lab result labelled C.') and the sentence is true",
     "location": "course/modules/E/E3/L05.html:620, L06.html:545; wording also at L07.html:570, L08.html:723",
     "status": "FAIL",
     "evidence": "Delta 4540351d..HEAD replaced the footer on L05 (L05.html:620), L06 (L06.html:545), L07 (L07.html:570) and L08 (L08.html:723) with 'Every substantive claim carries an evidence grade and at least one citation key from the verified registry.' Ruling 39 (plans/FINAL-ARCHITECT-RULINGS.md line 141-144) says the footers of L05 to L08 read 'Each graded result carries a proof or a lab result labelled C.' The new sentence is also false on these pages: grep -c data-cite over L05.html, L06.html, L07.html, L08.html returns 0 for each, so no substantive claim on them carries a registry citation key; the T claims (for example Remark 3.1, Theorem 3.2, Proposition 1.4, Proposition 2.2 of L07) have no key. The sentence was not in the ruling. Evidence file: ledgers/E3/scripts/E3-e-r1/out/ (grep commands listed in notes).",
     "fix": "Restore the footer text on L05, L06, L07 and L08 to the ruling 39 sentence 'E3 · Decision Theory Under Risk &amp; Ambiguity · Each graded result carries a proof or a lab result labelled C.' (the L01-L04 wording). Re-run check_pages --unit E3 and page_smoke --unit E3."},
    {"id": "E3e-r19-footers-L07-L08", "check": "Footers of L07 and L08 read the ruling 39 sentence and the sentence is true for them",
     "location": "course/modules/E/E3/L07.html:570; L08.html:723",
     "status": "FAIL",
     "evidence": "Same defect as E3e-r18-footers-L05-L06, on the two pages ruling 39 names. L07.html:570 and L08.html:723 read 'Every substantive claim carries an evidence grade and at least one citation key from the verified registry.' grep -c data-cite on L07.html and L08.html is 0, and the only registry-key mention is in naming sentences (L07.html:80, L08.html:67, :133), which ruling 39 makes ungraded. The footer the ruling requires is 'Each graded result carries a proof or a lab result labelled C.' For L07 and L08 that statement is true (L07 has one C result, a lab result at L07.html:462; L08 has no C result; the T results have proofs), so the required wording needs no other change.",
     "fix": "Replace the L07.html:570 and L08.html:723 footer sentence with the ruling 39 wording ('Each graded result carries a proof or a lab result labelled C.'). Re-run check_pages --unit E3 and page_smoke --unit E3 for L07 and L08."},
    {"id": "E3e-r19-notation-Lambda", "check": "Ruling 38: the exponent b of L03 Proposition 1.2 is renamed to a letter absent in E3 in either case (upper and lower)",
     "location": "course/modules/E/E3/L03.html:78, :83 (Lambda); lowercase lambda at L06.html:62-64, :74, :98, :113 and L08.html:441, :460, :479, :684, :699, and project.html:53 and :668",
     "status": "FAIL",
     "evidence": "Ruling 38 (plans/FINAL-ARCHITECT-RULINGS.md lines 137-140) says the remaining rename is the exponent b of L03 Proposition 1.2 'to a letter absent in E3 in either case'. The delta renamed it to Lambda (L03.html:78, :83; cards E3-c037). Uppercase Lambda is absent from E3 pages except L03 (grep this round), but lowercase lambda is used throughout E3 as the loss-aversion coefficient (L06.html:62-64, L08.html:441, project.html:53), so the letter is not absent in either case. Ruling 38 treats upper and lower case as different symbols for Xi and Omega, but for the rename it states the stricter condition 'absent in either case'; the Lambda choice does not meet it. Judgment: this follows the ruling wording; if the architect accepts glyph-level distinctness for Lambda as for Xi and Omega, the row is PASS.",
     "fix": "Choose a letter whose upper- and lower-case forms both occur zero times in E3 pages, cards and twins: by macro count, mu and Mu are 0 and 0 (rho is banned by plan 4, and Sigma, Theta, Pi, Upsilon are each used in lower case). Rename Lambda in L03.html:78 and :83 and card E3-c037 to that letter, and re-run check_pages --unit E3 and page_smoke --unit E3 for L03. Or record the architect's glyph-level acceptance in plans/FINAL-ARCHITECT-RULINGS.md."},
    {"id": "E3e-r19-L03-interp-scope", "check": "L03 interpretation paragraph: its scope sentence describes only what the lab computes (no 'every' claim the code does not support)",
     "location": "course/modules/E/E3/L03.html:326 (interpretation paragraph after the lab)",
     "status": "FAIL",
     "evidence": "The delta changed 'every number is computed from the fixed lottery' to 'every computed value comes from the fixed lottery and the stated gamma grid' (L03.html:326). tests/labs/E3/lab-E3-L03-1.py computes further values from other inputs: step sizes h in (1e-3, 1e-6) at line 86, the offset gamma = 1 +/- 1e-6 at line 83, wealth values w in (0.5, 2.0, 10000.0) at line 96, and scales k in (2, 3, 10) at line 103. None of these is the fixed lottery or the stated gamma grid of six values. The sentence is therefore false for the printed lines of the lab (its 'every' scope word is not supported). The other sentences of the paragraph are supported: the printed values match (lab_exact.out, L03 expected block == stdout).",
     "fix": "Replace the sentence with one that names the inputs: 'Every line is printed by the code above, and every computed value comes from the fixed lottery, the stated gamma grid, and the step sizes, offsets, wealth values and scales that the lab states.' Re-run lab_exact and page_smoke for L03."},
    {"id": "E3e-r19-L05-remark34-row", "check": "L05 grade-table row for Remark 3.4 states the MRS difference with the hypothesis Remark 3.4 proves",
     "location": "course/modules/E/E3/L05.html:499 (table row, graded T); Remark 3.4 at L05.html:156-158; R3 solution at L05.html:482",
     "status": "FAIL",
     "evidence": "The delta changed the row to 'so their marginal rates of substitution differ off psi = 1/gamma (Remark 3.4)'. Remark 3.4 (L05.html:157) proves the difference only 'at every plan with c1 != c0', and states that on the diagonal c1 = c0 both marginal rates equal (1-beta)/beta for every psi and gamma; the R3 solution (L05.html:482) says the same. The unqualified row therefore reads as a pointwise claim that is false on the diagonal (for example psi = 2, gamma = 2, c0 = c1 = 4: both MRS equal (1-beta)/beta). Graded T, so the omitted hypothesis matters (ruling 26: a T row needs its hypothesis).",
     "fix": "Change the row to 'so their marginal rates of substitution differ at every plan with c1 != c0 when psi != 1/gamma (Remark 3.4)'. Re-run check_pages --unit E3, page_smoke --unit E3 for L05."},
    {"id": "E3e-r14-open-items-deviations", "check": "plans/E3-open-items.md (the record of deviations for the architect) describes the L07 and L08 registry claims as the pages now state them",
     "location": "plans/E3-open-items.md:28-30 (section 2.1), :53-56 (section 3); pages L07.html:80, L08.html:67, :133",
     "status": "FAIL",
     "evidence": "Ruling 39 removed the data-cite and the C grade from the three registry-title claims. plans/E3-open-items.md section 2.1 still says L07 'cites the registry title only' and section 3 says each key is 'in one grade-C claim span (data-cite, data-locator = registry record: title only; paper not read)' and in the key-results table, which is no longer true (grep data-cite on L07 and L08 is 0; the C rows are deleted). The file is a plan record for the architect, not a page; it is stale against the pages.",
     "fix": "Update plans/E3-open-items.md section 2.1 and section 3 to say the three registry-title claims are ungraded naming sentences under ruling 39 (L07.html:80, L08.html:67, L08.html:133) with no registry key on the page, and that cards E3-c134, c157, c158 are ungraded. This is a plan file, not a course file; it is outside the verifier's write set."},
    {"id": "E3e-r19-ruling37-no-mutants", "check": "Ruling 37 (closing round writes no new mutants) and ruling 30 (delta closes the slice; no new-defect hunting outside the rows)",
     "location": "plans/FINAL-ARCHITECT-RULINGS.md:133-136 (ruling 37), :97-101 (ruling 30); this fragment's mutants field",
     "status": "PASS",
     "evidence": "No mutant was authored this round; the fragment's mutants list is empty, as slice e has no grader (base fragment notes). The round checked the rows of the base and the rows whose subject changed (ruling 30); the new rows E3e-r19-* are the defects those rows exposed in the changed hunks, not new-defect hunting. Notes list observations outside the rows without grading them."},
]


def main():
    rows_out = []
    seen = set()
    NEW_IDS = {nr["id"] for nr in NEW_ROWS}
    for r in BASE["rows"]:
        rid = r["id"]
        seen.add(rid)
        if rid in NEW_IDS:
            continue
        if rid in RE_VERIFIED:
            status, loc, ev = RE_VERIFIED[rid]
            row = {"id": rid, "check": r["check"], "location": loc, "status": status, "evidence": ev}
            if status != "PASS":
                row["fix"] = "see notes"
            rows_out.append(row)
            continue
        if rid in CARRY_IDS:
            rows_out.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                             "evidence": CARRY + CARRY_IDS[rid] + ". Prior evidence: " + base_ev(rid)})
            continue
        # every remaining base row is re-verified above or carried; list any leftover explicitly
        raise SystemExit(f"row {rid} has no disposition")
    # FAIL rows from the base that stay FAIL and changed-subject rows
    for nr in NEW_ROWS:
        rows_out.append(nr)
    ids = [r["id"] for r in rows_out]
    assert len(ids) == len(set(ids)), "duplicate ids"
    missing = [i for i in seen if i not in ids]
    assert not missing, missing
    json.dump(rows_out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(rows_out), "rows;", sum(r["status"] == "FAIL" for r in rows_out), "FAIL")


if __name__ == "__main__":
    main()
