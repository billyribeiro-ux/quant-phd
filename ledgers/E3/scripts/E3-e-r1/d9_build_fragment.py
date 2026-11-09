"""Build ledgers/E3/E3-e.json: closing delta of E3 slice e (round 1) at pin d9de2fe5.

Base: ~/.fanout/frags/G-E3-e.round1.json (pin 2a805c83). Every base row id is kept. Rows whose subject changed
between 2a805c83 and d9de2fe5 are re-verified (FRESH); the rest are carried with the carry prefix.
"""

import json
import sys
from pathlib import Path

BASE = Path("/Users/billyribeiro/.fanout/frags/G-E3-e.round1.json")
OUT = Path("ledgers/E3/E3-e.json")
PIN_OLD = "2a805c83"
CARRY = "Carried from round 1 ({files} byte-identical since the previous pin {pin}): "

base = json.loads(BASE.read_text(encoding="utf-8"))
base_rows = {r["id"]: r for r in base["rows"]}

FRESH: dict[str, tuple[str, str]] = {}  # id -> (status, evidence)
CARRY_FILES: dict[str, str] = {}  # id -> files that are byte-identical
FIX: dict[str, str] = {}
NOTE_CARRY: dict[str, str] = {}  # id -> extra note appended to the carry prefix

# ---- gates, re-run at d9de2fe5 (outputs in d9/) ----
FRESH["E3e-r14-gate-check-pages"] = (
    "PASS",
    "Re-run at d9de2fe5: `.venv/bin/python tools/check_pages.py --unit E3` printed 'check_pages E3: PASS', exit 0 "
    "(d9/check_pages.out). The gate does not test footer wording; that is checked in the footer rows.",
)
FRESH["E3e-r14-gate-check-dag"] = (
    "PASS",
    "Re-run at d9de2fe5: `tools/check_dag.py --unit E3` printed 'check_dag E3: PASS', exit 0 (d9/check_dag.out).",
)
FRESH["E3e-r14-gate-check-projects"] = (
    "PASS",
    "Re-run at d9de2fe5: `tools/check_projects.py --unit E3` printed 'check_projects E3: PASS', exit 0 "
    "(d9/check_projects.out). The project slice itself is not judged here.",
)
FRESH["E3e-r14-gate-run-labs-L05-L08"] = (
    "PASS",
    "Re-run at d9de2fe5: `tools/run_labs.py --unit E3` printed 'run_labs E3: PASS (11/11)', exit 0 (d9/run_labs.out). "
    "This covers the changed L02 twin and the L01, L03, L05, L06, L08 labs: each page code equals its twin, each twin "
    "runs under python -I -W error, and each expected block equals the output.",
)
FRESH["E3e-r14-gate-page-smoke"] = (
    "PASS",
    "Re-run at d9de2fe5: `tools/page_smoke.py --unit E3 --skip-sweep` printed 'page_smoke E3: PASS', exit 0 "
    "(d9/page_smoke.out) for index, L01-L08, project, concepts and review pages. The figure sweep is skipped: E3 has "
    "no live figure.",
)
FRESH["E3e-r14-twins-L05-L08-run"] = (
    "PASS",
    "run_labs (11/11, row E3e-r14-gate-run-labs-L05-L08) runs every E3 twin. Also `.venv/bin/python -I -W error "
    "tests/labs/E3/lab-E3-L02-1.py` exit 0 with empty stderr (d9/lab_L02_twin.out, .err); a script showed its stdout "
    "equals the page expected block of L02.html:365 exactly.",
)
FRESH["E3e-r14-twins-L05-L08-lint"] = (
    "PASS",
    "The changed twin is L02 only. `.venv/bin/ruff check tests/labs/E3/lab-E3-L02-1.py` 'All checks passed!', "
    "`ruff format --check` '1 file already formatted', `mypy --no-incremental` 'Success: no issues found in 1 source "
    "file' (d9/ruff_check_L02.out, ruff_format_L02.out, mypy_L02.out). The L01, L03, L05, L06 and L08 twins are "
    "byte-identical since 2a805c83 (git diff empty), so their lint carries from round 1.",
)
FRESH["E3e-r14-verify-refs-offline"] = (
    "PASS",
    "Re-run at d9de2fe5: `.venv/bin/python tools/verify_refs.py --offline` printed 'offline integrity: 560 entries, 0 "
    "problems', exit 0 (d9/verify_refs_offline.out). references/ and tools/ are unchanged since 2a805c83.",
)
CARRY_FILES["E3e-r14-registry-crossref-live"] = "references/references.json and tools/refs/"
NOTE_CARRY["E3e-r14-registry-crossref-live"] = (
    " Live Crossref was not re-run in this round; no registry record changed. The keys kahneman1979prospect, "
    "ellsberg1961risk, gilboa1989maxmin and epstein1989substitution still list used_by E3 in references/references.json."
)
FRESH["E3e-r14-pytest-relevant"] = (
    "PASS",
    "Re-run at d9de2fe5: `.venv/bin/pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -k E3` "
    "printed 15 dots, exit 0 (15 collected, d9/pytest_E3.out). `tools/build_site.py --check` printed 'site data "
    "current: 6 outputs', exit 0 (d9/build_site_check.out).",
)

# ---- hub and structure rows: index.html and titles are not in the delta ----
CARRY_FILES["E3e-r14-hub-structure"] = "course/modules/E/E3/index.html"
CARRY_FILES["E3e-r14-hub-placement-arithmetic"] = "course/modules/E/E3/index.html"
CARRY_FILES["E3e-r14-hub-data-and-labs-claims"] = (
    "course/modules/E/E3/index.html; tests/labs/E3/lab-E3-L01-1.py; tests/labs/E3/lab-E3-L03-1.py"
)
CARRY_FILES["E3e-r14-hub-unlocks-and-titles"] = "course/modules/E/E3/index.html"
CARRY_FILES["E3e-r14-hub-reading-list"] = (
    "course/modules/E/E3/index.html (the L02 change at L02.html:223 is in the Floating-point paragraph, not the references section)"
)
CARRY_FILES["E3e-r14-hub-ladder-rungs-3-4"] = "course/modules/E/E3/index.html and project.html"
CARRY_FILES["E3e-r14-hub-lesson-titles-match"] = "course/modules/E/E3/L01.html-L08.html h1 lines"
CARRY_FILES["E3e-r14-hub-E1-M4-released-claim"] = "course/modules/E/E3/index.html"
CARRY_FILES["E3e-r14-hub-rung1-generated-participant"] = "course/modules/E/E3/index.html and project.html"
CARRY_FILES["E3e-r14-lesson-hours"] = "course/modules/E/E3/L01.html-L08.html data-hours attributes"
NOTE_CARRY["E3e-r14-lesson-hours"] = " git diff over the slice shows no data-hours change."
FRESH["E3e-r14-lesson-structure"] = (
    "PASS",
    "Re-run at d9de2fe5: tools/check_pages.py --unit E3 PASS and tools/check_dag.py --unit E3 PASS (both above) cover "
    "the page structure, tags, h1, data-hours and dfn ids. The delta changes no dfn id, h1 or data-hours "
    "(git diff over the slice has no such line).",
)
CARRY_FILES["E3e-r14-why-it-matters"] = (
    "L01-L08 why-it-matters paragraphs and L04.html:51 (the delta's L04 hunks are at :53-56 and :687-690)"
)
FRESH["E3e-r14-banned-strings"] = (
    "PASS",
    "Re-run at d9de2fe5: check_pages E3 PASS (it enforces the BANNED phrase list of BUILDER_RULES 1.3-1.4 in visible "
    "prose, tools/check_pages.py:58-125). The added lines of the delta were also read: no banned phrase.",
)
FRESH["E3e-r14-process-words"] = (
    "PASS",
    "The 13 added lines of course/modules/E/E3 (git diff 2a805c83..HEAD -U0, saved in d9/slice_delta_2a805c83_d9de2fe5.diff) "
    "were searched for verifier, fixer, ruling, round, pin, delta, ledger, builder, slice, audit, architect, rubric, "
    "checker and previous: none found.",
)
FRESH["E3e-r14-filler-and-rhetoric"] = (
    "PASS",
    "The 13 added lines (d9/slice_delta_2a805c83_d9de2fe5.diff) were read. Scope words in them are 'Every line is "
    "printed by the code above' (L03.html:326, true: every line of the expected block comes from a print call in "
    "lab-E3-L03-1.py), 'holds on this grid only' (L03.html:326, the lab grid), 'at every plan with c1 != c0' (L05.html:499, "
    "proved in Remark 3.4) and 'for every psi > 0' (L08.html:479, Proposition 3.2). No rhetoric word is added.",
)
FRESH["E3e-r14-concept-dfn-and-links"] = (
    "PASS",
    "check_dag --unit E3 PASS at d9de2fe5 (d9/check_dag.out). git diff over the slice has no dfn, data-concept or "
    "concept link change.",
)
CARRY_FILES["E3e-r14-DAG-unlinked-names"] = "course/modules/E/E3/index.html and L01-L08.html"
NOTE_CARRY["E3e-r14-DAG-unlinked-names"] = (
    " The new prose of the delta (L03.html:326, L04.html:53-56 and :687-690, L08.html:165, :472, :479-480) uses no term "
    "that the same paragraph of the base pin did not already use (checked by reading the added lines); check_dag PASS "
    "at d9de2fe5."
)
CARRY_FILES["E3e-r14-forward-pointers-allowed"] = "added lines of the delta"
NOTE_CARRY["E3e-r14-forward-pointers-allowed"] = (
    " The one forward pointer the delta adds is Remark 3.3 (L08.html:165) naming Problem R1 (L08.html:584); it is a "
    "pointer, not a premise, and no unmet premise is used before its definition."
)
FRESH["E3e-r14-scope-words"] = (
    "PASS",
    "Re-read this round: L04.html:51 is unchanged; L08.html:479 (Section 5 bullet) changed and now says 'Remark 3.3 names "
    "the case ... where the lesson does not establish whether they enter; it does not compute it', which matches "
    "Remark 3.3 (L08.html:165). L08.html:67 unchanged. L01.html:334, :403, L05.html:131, L06.html:123 unchanged.",
)
CARRY_FILES["E3e-r14-plan-rulings-6-8"] = "plans/E3-build-plan.md sections 4 and 10"
FRESH["E3e-r14-notation-registry"] = (
    "PASS",
    "Re-run this round: ledgers/E3/scripts/E3-e-r1/symbol_sweep.py and greek_sweep.py over the pins (d9/symbol_sweep.out, "
    "greek_sweep.out). notation/notation.json has no entry for Lambda, lambda, Xi, xi, Omega or omega (grep). The changed "
    "math adds no symbol with a second meaning: the one new capital is Lambda in L03.html:78 and :83 (ruling 38a).",
)
FRESH["E3e-r14-cross-lesson-anchors"] = (
    "PASS",
    "check_dag --unit E3 PASS (d9/check_dag.out). git diff over the slice has no def-id or data-concept change, so every "
    "def-id anchor of the base pin is unchanged.",
)
CARRY_FILES["E3e-r14-plan-lesson-guidance"] = "plans/E3-build-plan.md section 5 and L01-L08.html"
CARRY_FILES["E3e-r14-L01-numbers"] = "course/modules/E/E3/L01.html and tests/labs/E3/lab-E3-L01-1.py"
CARRY_FILES["E3e-r14-L02-numbers"] = "course/modules/E/E3/L02.html numeric content"
NOTE_CARRY["E3e-r14-L02-numbers"] = (
    " The only L02.html change in the delta is the sentence at L02.html:223 (see E3e-r14-L02-lab-claims), which contains "
    "no number; git diff confirms no numeric token was added or removed."
)
FRESH["E3e-r14-L02-lab-claims"] = (
    "FAIL",
    "The L02 lab section changed in the delta (L02.html:222-223 and tests/labs/E3/lab-E3-L02-1.py:14, the same docstring). "
    "The new sentence says 'Other values are unrounded CU quantities, printed with six decimal places.' The printed output "
    "(d9/lab_L02_twin.out, exit 0) shows that this is not true of every non-cents value: variance_cu2 1800.000000 is in "
    "CU squared; r_A 0.005000 and linear_r_A are per CU; r_R 0.500000 is dimensionless; 'eps 1.0' and the True/False "
    "lines are not six-decimal numbers. The page expected block equals the output (checked), so the wrong claim is in the "
    "prose, not the output.",
)
FIX["E3e-r14-L02-lab-claims"] = (
    "In tests/labs/E3/lab-E3-L02-1.py lines 13-14 and the identical text in course/modules/E/E3/L02.html:222-223 (the "
    "docstring is inside the page code block at L02.html:210), replace 'Other values are unrounded CU quantities, printed "
    "with six decimal places.' with 'Other values are unrounded and printed with six decimal places, in the units the lab "
    "names (CU, CU squared or per CU); the scales and the True or False checks are printed as given.' Then run "
    "`.venv/bin/python tools/embed_labs.py course/modules/E/E3/L02.html --refresh lab-E3-L02-1` and `tools/run_labs.py "
    "--unit E3`. Re-run check_pages and page_smoke for E3."
)
FRESH["E3e-r14-L03-numbers"] = (
    "PASS",
    "The changed L03 hunk is the interpretation paragraph at L03.html:326. Its numbers were recomputed: the gamma grid is "
    "0, 0.25, 0.5, 1, 2, 4 (lab-E3-L03-1.py:18, six values); 'gamma 0 and gamma 1 ... 11250 and 10000 cents' (E[prize] = "
    "1/4*5000 + 1/2*10000 + 1/4*20000 = 11250; geometric mean sqrt(5000*20000) = 10000); the exact gamma 2 value "
    "1/(sum p/x) = 80000/9 (hand computation), printed float 8888.8889 (the page expected block, equal to the twin output per run_labs); the offsets gamma 1 +/- 1e-6 "
    "(line 83), +/- 1e-3 and +/- 1e-6 (line 86), gamma 1 - 1e-6 with wealths 0.5, 2, 10000 (lines 96-97), and k = 2, 3, 10 "
    "(line 103) match the code line by line. The paragraph follows the L03 expected block, which equals the twin output "
    "(run_labs PASS, d9/run_labs.out)."
)
CARRY_FILES["E3e-r14-L03-proofs-and-citations"] = "course/modules/E/E3/L03.html:66-67, :72-73, :77-83, :121-122, :133-134, :183-184"
NOTE_CARRY["E3e-r14-L03-proofs-and-citations"] = " The delta changes only L03.html:326 in this file."
FRESH["E3e-r14-L04-theorems"] = (
    "PASS",
    "Re-read this round: L04.html:56-59 (A1 and A2; A2 assumed from Definition 2.1 on) matches use: Section 1 (Definition "
    "1.1, Lemma 1.2, Definition 1.3, Definition 1.4, Theorem 1.5, Lemma 1.6, Example 1.7, Proposition 1.8 at :118 'This "
    "holds without A2') uses A1 only. Definition 2.1 and Theorem 2.3 (:129-155) assume A1 and A2. Example 2.5 (:164-169): "
    "X = 2000:1/2, 4000:1/2; Y = 1000:1/4, 3000:1/2, 5000:1/4; both means 3000; I_X = (0,0,500,1000,2000) and I_Y = "
    "(0,250,500,1250,2000) at the support points 1000..5000, recomputed by hand from E(t-X)^+, so I_X <= I_Y everywhere (matches the page expected block at L04.html:445-446); "
    "F_X(2000) = 1/2 > 1/4 = F_Y(2000) and F_Y(3000) = 3/4 > 1/2 = F_X(3000). Theorem 2.3 is correct as stated.",
)
CARRY_FILES["E3e-r14-L05-math"] = (
    "course/modules/E/E3/L05.html:64-86, :116-119, :130-131, :141-142 (the delta hunks are at :499 and :620)"
)
CARRY_FILES["E3e-r14-L05-lab-claims"] = "course/modules/E/E3/L05.html lab and tests/labs/E3/lab-E3-L05-1.py"
CARRY_FILES["E3e-r14-L06-math"] = "course/modules/E/E3/L06.html:63-69, :93-123, :127-131, :284-290 (the delta hunk is at :545)"
CARRY_FILES["E3e-r14-L06-lab-claims"] = "course/modules/E/E3/L06.html lab and tests/labs/E3/lab-E3-L06-1.py"
CARRY_FILES["E3e-r14-L07-numbers"] = "course/modules/E/E3/L07.html (the delta hunk is at :570)"
CARRY_FILES["E3e-r14-L07-prop-and-examples"] = "course/modules/E/E3/L07.html (the delta hunk is at :570)"
CARRY_FILES["E3e-r14-L07-lab-claims"] = "course/modules/E/E3/L07.html lab and tests/labs/E3/lab-E3-L07-1.py"
FRESH["E3e-r14-L08-numbers"] = (
    "PASS",
    "Recomputed with Python fractions: 4180000/41 = 101951.2195 (EU and EZ, L08.html:437, :447); 1/(1/3/110000 + 2/3/95000) "
    "= 99523.8095 (maxmin); 102500 - 101951.2195 = 548.7805 and 22500/41 = 548.7805 (premium); 100000 - 99523.8095 = "
    "476.1905 (L08.html:472); 1/(1/4/110000 + 3/4/95000) = 1672000/17 = 98352.9412; the full-set worst prior P(red)=0 "
    "gives CE = 95000 (L08.html:477). The L08 expected block (L08.html:403-424) equals the twin output (run_labs PASS). The "
    "Section 4 sentence changed at :472 only in wording; its numbers are unchanged.",
)
CARRY_FILES["E3e-r14-L08-math"] = "course/modules/E/E3/L08.html:141-160 and :585-587"
NOTE_CARRY["E3e-r14-L08-math"] = (
    " Remark 3.3 (L08.html:165) and the Section 5 bullet (:479) changed in the delta; they are re-verified in row "
    "E3d9-L08-remark33-section4-section5."
)
CARRY_FILES["E3e-r14-L08-lab-claims"] = "course/modules/E/E3/L08.html lab and tests/labs/E3/lab-E3-L08-1.py"
CARRY_FILES["E3e-r14-L02-prop3.1-undefined-q"] = "course/modules/E/E3/L02.html:195-199"
CARRY_FILES["E3e-r14-notation-v"] = (
    "course/modules/E/E3/L01.html:148, L02.html:149, L03.html:174, :184, :432, L06-L08 (the L02 hunk is at :223, no symbol)"
)
CARRY_FILES["E3e-r14-notation-eps"] = "course/modules/E/E3/L05.html and L02.html:164-217"
CARRY_FILES["E3e-r14-DAG-convexity-term"] = "course/modules/E/E3/L06.html:74, :133, :247, :272, :431, :438, :460"
CARRY_FILES["E3e-r14-contested-counter-side"] = "course/modules/E/E3/L06.html:298 and L07.html:52, :324"
FRESH["E3e-r15-footers-registry-claim"] = (
    "PASS",
    "Footers changed in the delta and are re-verified (rows E3e-r18-footers-L05-L06, E3e-r19-footers-L07-L08). The "
    "registry-title sentences of ruling 39 are ungraded: L07.html:80 (Kahneman and Tversky, 'cites it for no result'), "
    "L08.html:67 (Gilboa and Schmeidler) and L08.html:133 (Ellsberg) carry no data-grade and no data-cite (grep: 0 "
    "data-cite in L05-L08). Cards E3-c134 (cards.json:879-880), E3-c157 (:1028) and E3-c158 (:1034-1035) carry only "
    "id, lesson, front and back: no grade, no citation key.",
)
CARRY_FILES["E3e-r15-notation-a"] = (
    "course/modules/E/E3/L01.html:133-153, :326, :397, :470, :503, :512; L02.html:149, :407, :525, :582, :586; L07.html:323, :429-431"
)
CARRY_FILES["E3e-r15-notation-W"] = "course/modules/E/E3/L02.html:136, :164, :209, :214, :217, :319, :420-422, :558; L06.html:69-133"
FRESH["E3e-r18-lab-exact"] = (
    "PASS",
    "Re-run at d9de2fe5: run_labs E3 PASS (11/11): each expected block equals its twin's output under the page rule "
    "(d9/run_labs.out). The L03 expected block was checked against the output line by line (the new interpretation "
    "sentences at L03.html:326 name only lines that are printed).",
)
FRESH["E3e-r18-numeric-delta"] = (
    "PASS",
    "Every number in the delta's changed prose was recomputed: L03.html:326 (see E3e-r14-L03-numbers), L08.html:472 and "
    ":479 (see E3e-r14-L08-numbers), L04.html:690-696 (F values, see E3d9-L04-example25-quiz), L05.html:499 (no number). "
    "cards.json is byte-identical since 2a805c83; no card number changed.",
)
FRESH["E3e-r18-symbol-sweep"] = (
    "PASS",
    "Re-run: ledgers/E3/scripts/E3-e-r1/symbol_sweep.py over d9de2fe5 (d9/symbol_sweep.out). Single-letter hits in the changed "
    "prose are the same symbols as their meaning in the base pin: the math segments added by the delta are X, Y, c0, c1, psi, beta, gamma, P-bar, 10^-12 and numerals (none is W, a, b, v or eps); the only "
    "b outside its affine meaning is 'b = 1' at L03.html:90 (the affine slope of L02 Proposition 2.2), as before.",
)
FRESH["E3e-r18-katex-render"] = (
    "PASS",
    "Re-run: tools/page_smoke.py --unit E3 --skip-sweep PASS (d9/page_smoke.out). page_smoke checks zero .katex-error and "
    "re-parses every expression with throwOnError strict.",
)
CARRY_FILES["E3e-r18-footers-L01-L04"] = "course/modules/E/E3/L01.html:576, L02.html:627, L03.html:575, L04.html:728"
NOTE_CARRY["E3e-r18-footers-L01-L04"] = (
    " All eight footers now read 'Each graded result carries a proof or a lab result labelled C.' (grep of "
    "site-footer over L01-L08, this round)."
)
CARRY_FILES["E3e-r18-L01-prose"] = "course/modules/E/E3/L01.html:334, :58-60, :403-410; L06.html:56-58"
CARRY_FILES["E3e-r18-index-carry-basis"] = "course/modules/E/E3/index.html"
CARRY_FILES["E3e-r18-notation-b"] = (
    "course/modules/E/E3/L01.html:133-153, :397-399; L02.html:149-159, :407; L03.html:78-83 (Lambda, see E3e-r19-notation-Lambda), :90; L04.html:153-154, :609, :616; L07.html"
)
CARRY_FILES["E3e-r18-notation-ruling33-letters"] = (
    "plans/FINAL-ARCHITECT-RULINGS.md:137-140 (ruling 38, unchanged) and the L01, L02, L05, L08 letters"
)
NOTE_CARRY["E3e-r18-notation-ruling33-letters"] = (
    " Ruling 38a (plans/FINAL-ARCHITECT-RULINGS.md:146-150, added in the delta) confirms that Lambda/lambda are different "
    "symbols, so the Lambda of L03 Proposition 1.2 is accepted (E3e-r19-notation-Lambda)."
)
FRESH["E3e-r18-footers-L05-L06"] = (
    "PASS",
    "Footers changed in the delta and now read the ruling 39 sentence on L05.html:620 and L06.html:545: 'E3 · Decision "
    "Theory Under Risk &amp; Ambiguity · Each graded result carries a proof or a lab result labelled C.' (grep "
    "site-footer, d9). Ruling 39 (plans/FINAL-ARCHITECT-RULINGS.md:141-145) requires this text. The sentence is true on these "
    "pages: L05 has C results at :500-502 (labs, basis 'Lab 1'), L06 has C results at :441 and :278 (lab); every T claim "
    "either has a Proof block or an inline argument (L05 Remark 3.1 at :130; L06 Remarks 1.5, 2.4, 2.5, 3.1, 3.2 argue inline, "
    "as the base row E3e-r14-L06-math checked).",
)
FRESH["E3e-r19-footers-L07-L08"] = (
    "PASS",
    "L07.html:570 and L08.html:723 now read the ruling 39 sentence (grep site-footer, d9). The sentence is true on these "
    "pages: a scan this round (every block-title claim span followed by a Proof block before the next claim) finds no T claim "
    "without a Proof on L07 (2 T claims) or L08 (4 T claims). L07 has one C result, a lab result at L07.html:462 with basis "
    "'Observation 1.5; Lab 1, part A'; L08 has no C result. data-cite count on L07 and L08 is 0.",
)
FRESH["E3e-r19-notation-Lambda"] = (
    "PASS",
    "Ruling 38a (plans/FINAL-ARCHITECT-RULINGS.md:146-150) states that the glyph-level rule covers Lambda/lambda: 'they are "
    "different symbols and need no further renaming'. The Lambda of L03.html:78 and :83 (and cards.json:253) is the capital; "
    "the lowercase lambda of L06 and L08 is a different symbol. Greek sweep (d9/greek_sweep.out): Lambda occurs only in "
    "L03; no notation.json entry for either form. PASS under ruling 38a.",
)
FRESH["E3e-r19-L03-interp-scope"] = (
    "PASS",
    "L03.html:326 changed and now lists its inputs: 'the fixed lottery and the gamma grid 0, 0.25, 0.5, 1, 2, 4' (the "
    "falling-order and exact-value lines), 'the offsets gamma 1 +/- 1e-6' (gap line, lab :83), 'gamma 1 +/- 1e-3 and "
    "gamma 1 +/- 1e-6' (slope line, :86), 'gamma 1 - 1e-6 with the wealths 0.5, 2 and 10000' (limit line, :96-97), and "
    "'the lottery multiplied by k = 2, 3 and 10' (homogeneity line, :103). Each matches lab-E3-L03-1.py. 'Every line is "
    "printed by the code above' holds (d9/run_labs.out). The 'every' claim now has its inputs named.",
)
FRESH["E3e-r19-L05-remark34-row"] = (
    "PASS",
    "L05.html:499 now reads 'differ at every plan with c1 != c0 when psi != 1/gamma (Remark 3.4)', graded T, basis "
    "'Proved in §3 from Proposition 2.2'. Remark 3.4 (L05.html:156-158) proves exactly that: for r = c1/c0 != 1, agreement "
    "needs r^gamma = r^(1/psi), so gamma = 1/psi; and off that case the two MRS differ at every plan with c1 != c0. The "
    "diagonal c1 = c0 is excluded by the row's hypothesis and by Remark 3.4 (both equal (1-beta)/beta). The R3 solution "
    "(L05.html:482) says the same. The hypothesis is now stated in the row.",
)
FRESH["E3e-r14-open-items-deviations"] = (
    "PASS",
    "plans/E3-open-items.md changed in the delta (git diff, 13 lines). Section 2.1 (lines 28-30) now says the 1979 mention "
    "is 'an ungraded naming sentence under ruling 39 (L07.html:80)' with no data-grade and no data-cite: matches L07.html:80. "
    "Section 3 (lines 53-61) says the three registry records are used by E3 (references/references.json: kahneman1979prospect, "
    "ellsberg1961risk, gilboa1989maxmin each list used_by ['E3']), cites L07.html:80, L08.html:67 and L08.html:133 as naming "
    "sentences, and says cards E3-c134, c157, c158 carry no grade and no key: matches cards.json and the pages. Scope of "
    "this row only; other items of the plan record were not re-judged (plan file, not a course file).",
)
FRESH["E3e-r19-ruling37-no-mutants"] = (
    "PASS",
    "plans/FINAL-ARCHITECT-RULINGS.md lines 133-136 (ruling 37) and 97-101 (ruling 30) are unchanged by the delta (git diff "
    "adds only lines 146-155: rulings 38a and 40). No mutant is authored in this closing round; the mutants list is empty.",
)

FRESH["E3e-r14-grades"] = (
    "PASS",
    "git diff over the slice shows four changed lines carrying a data-grade attribute: L03.html:326 (interpretation, its "
    "C span is kept) and L05.html:499 (Remark 3.4 row, T kept). data-grade spans per page (legend included) read this "
    "round: C in L03 3, L05 5, L06 3, L07 2, L08 1; the grades of the changed rows are unchanged, and the key-results row "
    "L05.html:499 keeps basis 'Proved in §3 from Proposition 2.2'.",
)
CARRY_FILES["E3e-r14-quiz-and-explanations"] = (
    "course/modules/E/E3/L01.html (:422, :469), L05.html (:538, :547), L06.html (:495, :518, :521-527), L08.html (:586)"
)
NOTE_CARRY["E3e-r14-quiz-and-explanations"] = (
    " The L04 quiz item changed in the delta and is re-verified in row E3d9-L04-example25-quiz."
)

# ---- carried rows that are pure carries with no changed subject ----
CARRY_FILES.setdefault("E3e-r14-gate-run-labs-L05-L08", "")  # (fresh above)

rows = []
for bid, brow in base_rows.items():
    row = {"id": bid, "check": brow["check"], "location": brow["location"]}
    if bid in FRESH:
        status, ev = FRESH[bid]
        row["status"] = status
        row["evidence"] = ev
    elif bid in CARRY_FILES:
        row["status"] = "PASS"
        if brow["status"] != "PASS":
            raise SystemExit(f"base row {bid} is not PASS but is carried")
        files = CARRY_FILES[bid]
        note = NOTE_CARRY.get(bid, "")
        row["evidence"] = CARRY.format(files=files, pin=PIN_OLD) + brow["evidence"] + note
    else:
        raise SystemExit(f"no decision for base row {bid}")
    if bid in FRESH:
        row["check"] = row["check"].replace(" (carried)", "") + " [re-verified at d9de2fe5]"
    if row["status"] != "PASS":
        row["fix"] = FIX[bid]
    rows.append(row)

unknown = (set(FRESH) | set(CARRY_FILES)) - set(base_rows)
if unknown:
    raise SystemExit(f"decisions for unknown ids: {sorted(unknown)}")

NEW_ROWS = [
    {
        "id": "E3d9-delta-coverage",
        "check": "Every hunk of git diff 2a805c83..d9de2fe5 over the E3 slice paths is read and mapped to a row",
        "location": "course/modules/E/E3/{L02,L03,L04,L05,L06,L07,L08}.html; tests/labs/E3/lab-E3-L02-1.py; plans/E3-open-items.md; plans/FINAL-ARCHITECT-RULINGS.md",
        "status": "PASS",
        "evidence": "git diff --stat 2a805c83..d9de2fe5 over course/modules/E/E3, tests/labs/E3, cards.json: 8 files, 13 insertions, 13 deletions (d9/slice_delta_2a805c83_d9de2fe5.diff). Hunks: L02.html:223 (sentence) and lab-E3-L02-1.py:14 (same docstring text); L03.html:326 (interpretation); L04.html:53-56 (A1/A2 block name) and :687-690 (Example 2.5 quiz prompt); L05.html:499 (Remark 3.4 row) and :620 (footer); L06.html:545, L07.html:570, L08.html:723 (footers); L08.html:165 (Remark 3.3), :472 (Section 4 sentence), :479-480 (Section 5 bullet). cards.json, the lab twins other than L02, and index.html are unchanged. Non-slice files read: plans/E3-open-items.md (rows E3e-r14-open-items-deviations) and plans/FINAL-ARCHITECT-RULINGS.md (rulings 38a and 40 added).",
    },
    {
        "id": "E3d9-L04-section1-no-A2",
        "check": "L04 A2 is assumed only from Definition 2.1 on (the changed block title and bullet at L04.html:56-59)",
        "location": "course/modules/E/E3/L04.html:56-59, :118, :129-155",
        "status": "PASS",
        "evidence": "Read the whole of Section 1 (L04.html:60-128): Definition 1.1, Lemma 1.2, Definition 1.3-1.4, Theorem 1.5, Lemma 1.6, Example 1.7 (means 3000 and 3500, used only as an instance of Theorem 1.5), Proposition 1.8 ('This holds without A2', :118). None uses E X = E Y. Definition 2.1 (:129-130) and Theorem 2.3 (:144-145) state 'Under A1 and A2'. The title '(finite support; equal means, used from Section 2)' and the bullet 'A2 is assumed from Definition 2.1 on, in Section 2' are true.",
    },
    {
        "id": "E3d9-L04-example25-quiz",
        "check": "The changed quiz prompt L04.html:690 and its explanation at :696 describe Example 2.5 correctly",
        "location": "course/modules/E/E3/L04.html:689-697 (quiz item L04q7), Example 2.5 at :164-169",
        "status": "PASS",
        "evidence": "New prompt: 'In Example 2.5, X dominates the spread lottery Y in the second order, and the pair has no first-order ranking.' Example 2.5 (:165-168): X = 2000:1/2, 4000:1/2; Y = 1000:1/4, 3000:1/2, 5000:1/4; equal means 3000; X dominates Y in the second order (hand computation: I_X <= I_Y at all support points; page lab line L04.html:444 'SOSD verdict X dominates Y'). Correct option: F_X(2000) = 1/2 > 1/4 = F_Y(2000) and F_Y(3000) = 3/4 > 1/2 = F_X(3000) (hand computation). Distractors 'The means differ' (false: both 3000) and 'The support is infinite' (false: S finite). Explanation at :696 matches.",
    },
    {
        "id": "E3d9-L08-remark33-section4-section5",
        "check": "The changed prose of L08 Remark 3.3 (:165), Section 4 (:472) and Section 5 bullet (:479-480) is true and carries its hypotheses",
        "location": "course/modules/E/E3/L08.html:165, :472, :479-480; Problem R1 at :584",
        "status": "PASS",
        "evidence": "Remark 3.3: 'The lesson does not establish whether its certainty equivalent then depends on psi and beta; Problem R1 names the step that fails, and the lesson does not compute the number.' Problem R1 (:584) is titled 'The step that fails for an earlier-resolving gamble'; the sentence claims no result. Section 4 (:472): 'under that model the bet is worth less than the initial wealth held for sure' — the maxmin CE 99523.8095 is 476.1905 below w0 = 100000 (the new wording fixes the old 'worth less than nothing'). Section 5 (:479-480): 'Remark 3.3 names the case ... where the lesson does not establish whether they enter; it does not compute it' matches Remark 3.3. The Proposition 3.2 hypotheses listed (A1 to A5, gamma != 1, c0 > 0, positive outcomes) are unchanged.",
    },
]

fragment = {
    "unit": "E3",
    "slice": "e",
    "round": 1,
    "verifier": "Haiku independent verifier, E3-e closing delta round 1 at d9de2fe5 (did not build E3)",
    "pin": "d9de2fe5",
    "base": "2a805c83 (base fragment ~/.fanout/frags/G-E3-e.round1.json, verdict FAIL with 6 non-PASS rows)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyH1-E3-e",
    "scratch": "/tmp/e3e_d9/",
    "verified_at": "2026-11-09",
    "verdict": "FAIL",
    "rows": rows + NEW_ROWS,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta: git diff 2a805c83..d9de2fe5 over course/modules/E/E3, tests/labs/E3, plans/E3-open-items.md and plans/FINAL-ARCHITECT-RULINGS.md (13 insertions, 13 deletions in the slice). Hunk list in row E3d9-delta-coverage.",
        "Rulings applied: 30 (delta closes the slice: every non-PASS base row and every changed-subject row re-verified from scratch; the rest carried); 37 (no mutants; mutants empty); 38a (Lambda/lambda accepted, row E3e-r19-notation-Lambda PASS); 39 (footers of L05-L08 are the ruling wording; registry-title sentences ungraded, cards E3-c134, c157, c158 ungraded); 26 (FAIL only for a lab statement the code does not support: row E3e-r14-L02-lab-claims).",
        "The base's twins were byte-identical except the L02 twin; the L02 twin was re-run under .venv python 3.14 with -I -W error (the system python3 lacks itertools.pairwise and was not used for it).",
        "Scripts: ledgers/E3/scripts/E3-e-r1/d9_build_fragment.py builds this fragment; evidence outputs are in ledgers/E3/scripts/E3-e-r1/d9/.",
        "Not checked: live Crossref and verify_refs online (references unchanged); run_graders and mutate_graders (slice e has no grader); project.html and the grader (outside slice e); full pytest suite (relevant subset: 15 tests); the figure sweep of page_smoke (E3 has no live figure); the T-grade proofs not touched by the delta were carried, not re-read.",
    ],
    "summary": {},
}

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in fragment["rows"]:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
fragment["summary"] = {
    "rows": len(fragment["rows"]),
    "pass": counts["PASS"],
    "fail": counts["FAIL"],
    "unverifiable": counts["UNVERIFIABLE"],
    "mutants": 0,
    "mutants_killed": 0,
}
fragment["verdict"] = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 else "FAIL"

OUT.write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("rows", len(fragment["rows"]), counts, fragment["verdict"], file=sys.stdout)
