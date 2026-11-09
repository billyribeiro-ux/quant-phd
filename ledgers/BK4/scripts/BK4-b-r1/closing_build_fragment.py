"""Build ledgers/BK4/BK4-b.json (closing delta round 1, slice b) from the round-1 base fragment.

Run: .venv/bin/python -I ledgers/BK4/scripts/BK4-b-r1/closing_build_fragment.py
Every base row id is kept. Rows whose cited subject changed in git diff 95f3f8cb..2a805c83 are
re-verified in this round (evidence written here, with the command output file). Every other row is
carried with the carry prefix, and the script checks that no carried row cites a changed line.
"""
import datetime
import json
import re
import pathlib

REPO = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyG1-BK4-b")
BASE_FRAG = pathlib.Path("/Users/billyribeiro/.fanout/frags/F3-BK4-b.round1.json")
OUT = REPO / "ledgers/BK4/BK4-b.json"
S = "ledgers/BK4/scripts/BK4-b-r1/"

CHANGED = {
    "course/modules/BK/BK4/L04.html": {52, 69, 391},
    "course/modules/BK/BK4/L05.html": {51, 153, 466, 482, 485},
    "course/modules/BK/BK4/cards.json": {117, 687},
}
CHANGED_CARDS = {"BK4-c014", "BK4-c088"}
DELTA_TXT = "L04.html:52,69,391; L05.html:51,153,466,482,485; cards.json:117,687"

base = json.loads(BASE_FRAG.read_text(encoding="utf-8"))
base_rows = {r["id"]: r for r in base["rows"]}

REV = {
    "BK4b-cards-L04-L05-scan": (
        "Re-verified from scratch at 2a805c83 and the base FAIL is resolved. cards.json:687 (BK4-c088) front again reads "
        "'Assuming the finite probability space, A1 and A2, with A3 for independent failures and A4 for comonotone failures, "
        "do dependent failures cost more on average than independent failures (Proposition 2.4)?' The back cites Proposition 2.2 "
        "(L05.html:94-95, hypotheses: finite space, A1, A2, A3) and Proposition 2.4 (L05.html:113-114, hypotheses: finite space, A1, A2, A4); "
        "the front now carries all of them. Basis field 'Proposition 2.4 (proof in Section 2); Proposition 2.2 and Proposition 2.1' is consistent. "
        "Scan (" + S + "closing_cards_delta.txt): 100 objects, 100 unique ids, no duplicate front or back, 14 L05 cards, "
        "every number in the L04/L05 cards appears in its own lesson text (missing: none). Cards changed in the delta: BK4-c088 and BK4-c014 (L01, slice a)."),
    "BK4b-gate-check-pages": (
        "Re-run at 2a805c83: .venv/bin/python tools/check_pages.py --unit BK4 -> 'check_pages BK4: PASS', exit 0 (" + S + "closing_check_pages.txt). "
        "Covers the changed L04.html and L05.html, including the banned-word and structure scans."),
    "BK4b-gate-check-dag": (
        "Re-run: .venv/bin/python tools/check_dag.py --unit BK4 -> 'check_dag BK4: PASS', exit 0 (" + S + "closing_check_dag.txt). "
        "The delta adds no concept anchor (" + S + "closing_delta_scan.txt: the only 'concept' substring match is the word 'misconception')."),
    "BK4b-gate-check-projects": (
        "Re-run: .venv/bin/python tools/check_projects.py --unit BK4 -> 'check_projects BK4: PASS', exit 0 (" + S + "closing_check_projects.txt). "
        "project.html and the BK4 grader are not in the 95f3f8cb..2a805c83 delta."),
    "BK4b-run-labs": (
        "Re-run: .venv/bin/python tools/run_labs.py --unit BK4 -> 'run_labs BK4: PASS (8/8)', exit 0 (" + S + "closing_run_labs.txt). "
        "Lab blocks L04.html:155-357 and L05.html:160-337 are outside the changed lines (" + DELTA_TXT + ")."),
    "BK4b-twin-isolated-run": (
        "Re-run: .venv/bin/python -I -W error tests/labs/BK4/lab-BK4-L04-1.py and lab-BK4-L05-1.py, both exit 0 (" + S + "closing_twin_L04.txt, closing_twin_L05.txt). "
        "tests/labs/BK4 is not in the delta (git diff --stat empty); stderr 0 bytes per " + S + "closing_twin_vs_page.txt."),
    "BK4b-twin-lint": (
        "ruff check . -> 'All checks passed!' (" + S + "closing_ruff_check.txt); ruff format --check . -> '555 files already formatted' (" + S + "closing_ruff_format.txt); "
        "mypy --no-incremental on both slice twins -> 'Success: no issues found in 2 source files' (" + S + "closing_mypy_labs.txt). The twins are unchanged in the delta."),
    "BK4b-pytest-labs": (
        ".venv/bin/python -m pytest tests/test_labs.py -k BK4 -q -> 8 passed, exit 0 (" + S + "closing_pytest_labs.txt). tests/test_labs.py is not in the delta."),
    "BK4b-page-smoke": (
        "tools/page_smoke.py --unit BK4 --pages modules/BK/BK4/L04.html modules/BK/BK4/L05.html -> 'page_smoke BK4: PASS', exit 0 (" + S + "closing_page_smoke.txt)."),
    "BK4b-verify-refs": (
        "tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 (" + S + "closing_verify_refs_offline.txt). "
        "references/references.json has no change in 95f3f8cb..2a805c83 (git diff -U0 empty)."),
    "BK4b-verify-refs-unit-scope": (
        "tools/verify_refs.py --unit BK4 -> 'live re-verification of BK4: 3 of 560 entries, 0 problems', exit 0 (" + S + "closing_verify_refs_unit.txt). "
        "This is the repo tool's own run; no extra request was made by this verifier."),
    "BK4b-citation-bisndbasel": (
        "Re-read at 2a805c83. L05.html:348 says 'The Basel III framework is named in the registry at index level, as <span data-cite=\"bisndbasel\" "
        "data-locator=\"index page: title and issuer\">Basel III: international regulatory framework for banks</span>. The lesson does not state what that "
        "framework says about operational risk'. L05.html:580 says the same at index level. references/references.json bisndbasel entry: title "
        "'Basel III: international regulatory framework for banks | Bank for International Settlements', url https://www.bis.org/committees/bcbs/standards, "
        "verified_by 'issuer'. Both the citation sentence and the registry entry match the locator. No operational-risk claim is made from the source."),
    "BK4b-build-site-check": (
        "tools/build_site.py --check -> 'site data current: 6 outputs', exit 0 (" + S + "closing_build_site_check.txt)."),
    "BK4b-render-curriculum": (
        "tools/render_curriculum.py exit 0 (" + S + "closing_render_curriculum.txt; it rewrote the files to identical content). "
        "git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json exit 0 (" + S + "closing_render_diff.txt). BK4 hours unchanged."),
    "BK4b-cmd-recompute": (
        "Re-run of ledgers/BK4/scripts/BK4-b-r11/recompute_r11.py with python -I at 2a805c83 -> 60 checks, ALL OK (" + S + "closing_recompute_r11_rerun.txt). "
        "New independent script " + S + "closing_recompute.py -> 17 OK, 0 FAIL (" + S + "closing_recompute.txt): Example 2.8 mean 4375/2 under A3 and A4 by enumeration; "
        "2187.5 rounds half up to 2188; 2188 cents = 21.88 dollars; Example 2.7 1-(7/8)^3 = 169/512, p = 64/512, 3p = 192/512; Prop 2.5 difference "
        "19140625 equals 2 kappa^2 p(1-p) sum_{i<j} l_i l_j at the Example 2.8 parameters; Prop 2.5 identity and Prop 2.4 mean equality on exact grids; "
        "misconception 1 at rho = 1 with h > 0 (2519 grid points) and h = 0; Remark 4.1 threshold 20/19; Remark 2.3 sign; R3 monotone spot grid."),
    "BK4b-numbers-L04-prose": (
        "L04.html:69 changed, and its new sentence contains no number except the basis-point floor of Definition 1.2 (10000 rho), which matches Definition 2.1 "
        "(L04.html:90). The other cited L04 numbers (:74, :152, :356, :376, :392-393, :405-406, :419-424) are not in the delta and are re-derived by the "
        "recompute_r11.py re-run (" + S + "closing_recompute_r11_rerun.txt: 9416 at 113/120, pair counts 15 and 21, E1-E3 values, quiz 9416.67 floor, "
        "reserves 1900000 and 2100000 printed in ledgers/BK4/scripts/BK4-b-r11/L04_lab_stdout.txt lines 3 and 17)."),
    "BK4b-numbers-L04-lab-table": (
        "L04.html:318-356 is unchanged in the delta. Re-run recompute_r11.py (" + S + "closing_recompute_r11_rerun.txt: 'L04 table rho=19/20 pair count 15', 'rho=21/20 pair count 21') "
        "and the twin-vs-page check (" + S + "closing_twin_vs_page.txt: L04 page expected == twin stdout True, 38 lines)."),
    "BK4b-numbers-L05-prose": (
        "L05.html:153 (Example 2.8) and :482, :485 changed. Re-derived in " + S + "closing_recompute.txt: 2187.5 = 17500/8 = 4375/2, half-up rounding gives 2188, "
        "21.88 dollars; 169/512, 64/512, 192/512; Prop 2.5 difference 19140625. Lines L05.html:84-152, :335-337, :384-386, :393, :429-436 and :486 are "
        "unchanged in the delta and are covered by recompute_r11.py (60 checks ALL OK) and the twin-vs-page check (L05 expected == stdout True, 31 lines)."),
    "BK4b-lab-table-L05": None,
    "BK4b-math-L04-props": None,
    "BK4b-r10-L04-A1-3-scope": None,
    "BK4b-math-L05-props": None,
    "BK4b-r10-L05-proposition-assumption-list": None,
    "BK4b-r10-L04-prop-2.7-form": None,
    "BK4b-math-L04-R-problems": None,
    "BK4b-math-L05-R-problems": (
        "L05.html:466 (R3 statement) and its solution changed in the delta; re-verified. R3 now reads 'Under A1, with 0<p<1, and with the cost of A2 for real "
        "parameters kappa >= 0 and ell_i >= 0 (not only whole numbers), show that E[C] = p kappa sum ell_i is nondecreasing in p, in kappa, and in each ell_i'. "
        "The solution's claim holds: the proof of Proposition 2.1 (L05.html:84-90) uses the finite space, A1 and the constants kappa ell_i, and linearity, with no "
        "integrality step. Each factor is nonnegative on the stated domain, so the product is nondecreasing in each factor. Grid check " + S + "closing_recompute.txt "
        "'R3 monotone spot grid' OK. R1 (L05.html:450-456) and R2 (L05.html:457-463) are unchanged; recompute_r11 re-run gives 'L05 R1 equal delays' OK and "
        "'L05 R2 bounds 5/8 and 7/8' OK."),
    "BK4b-problems-L04-M-P-E": None,
    "BK4b-problems-L05-P-E": None,
    "BK4b-lab-L04-statements": None,
    "BK4b-lab-L05-statements": None,
    "BK4b-lab-docstrings-L04-other": None,
    "BK4b-lab-docstrings-L05": None,
    "BK4b-misconceptions-L04-1-2": (
        "L04.html:391 (misconception 1) changed; re-verified. New belief: 'A stablecoin whose reserves equal its claims keeps its coverage at 1 whatever the reserve "
        "assets are worth.' Under Assumptions 1 to 3, Proposition 2.4 (L04.html:111-116) gives theta - 1 = (rho - 1)/(1 - x) = 0 at every admissible share when "
        "rho = 1, and the text says so. With h > 0 the measured ratio is 1 - h < 1, and Remark 4.1 (L04.html:375-378) gives measured coverage below 1 at every "
        "admissible share for 1 - h. Checked exactly in " + S + "closing_recompute.txt ('Misconception 1' rows, 2519 grid points, and the h = 0 case). "
        "Misconception 2 (L04.html:392): halving gives rho/2 = 19/40, coverage 9/10 = 9000 bps at x = 1/2 (Remark 2.8), unchanged and correct."),
    "BK4b-misconceptions-L05": None,
    "BK4b-quiz-L04": None,
    "BK4b-quiz-L05": None,
    "BK4b-key-results-L04": None,
    "BK4b-key-results-L05": (
        "L05.html:482 (A4 mean row) and :485 (Example 2.7 row) changed; both re-verified. Row 482 (T): 'Under A4 the mean is the same as under A3 (Proposition 2.4)', "
        "basis 'Proposition 2.4 under A1, A2 and A4; the A3 value is Proposition 2.2 under A1 to A3'. Prop 2.4 (L05.html:113-114) needs the finite space, A1, A2, A4, "
        "and Prop 2.2 (L05.html:94-95) needs the finite space and A1 to A3; both are proved on the page, so T is right. Row 485 (T): '169/512 under A3 and 64/512 "
        "under A4, and 3/8 is neither (Example 2.7)', basis 'Example 2.7 (arithmetic on the page)', re-derived exactly (" + S + "closing_recompute.txt). "
        "Mirror cards: BK4-c088 (T, cards.json:687), BK4-c089 (T, basis Example 2.7). Rows 486 (Example 2.8, T) and 487 (C, Lab 1 Part D) are unchanged."),
    "BK4b-grades-claim-spans": (
        "The delta changes L04.html:52, :69, :391 and L05.html:51, :153, :466, :482, :485. Re-checked the grade-span claim: L05.html:147-153 (Examples 2.7 and 2.8) "
        "contain no data-grade attribute (grep count 0), so the examples carry no span grade; Remark 2.8 (L04.html:152) carries none. Spans in L04.html:94-153 "
        "(Propositions 2.2 to 2.7) and L04.html:367-376 (Remark 4.1 claim span) and L05.html:84-152 (Propositions 2.1, 2.2, 2.4, 2.5, 2.6) are unchanged. "
        "The C grades remain only on the Lab 1 key row (L05.html:487) and card BK4-c087."),
    "BK4b-why-length": (
        "Re-counted at 2a805c83 from the HTML text (" + S + "closing_delta_scan.txt): L04 why-it-matters 117 words (was 119), L05 119 words (was 117). Both are at most 120, "
        "the BUILDER_RULES 4.2 item 1 limit stated in the base evidence."),
    "BK4b-L05-why-overreach": (
        "L05.html:51 changed. The new sentence 'Proposition 2.5 shows that, for a failure probability strictly between 0 and 1 and a positive cost per day, the variance "
        "when all three fail together is at least the variance under independence (under Assumption 1.3 and A1 to A4)' matches Proposition 2.5 (L05.html:123-124): "
        "hypotheses finite space, A1 and A2, A3 for Var_3, A4 for Var_4, 0 < p < 1, kappa > 0; conclusion Var_4 - Var_3 = 2 kappa^2 p(1-p) sum_{i<j} l_i l_j >= 0. "
        "'Proposition 2.4 gives the same mean when all three trades fail together' matches Proposition 2.4 (hypotheses A1, A2, A4). No overreach."),
    "BK4b-L05-why-terms": (
        "L05.html:51 changed. The why paragraph names Assumption 1.3 (L05.html:68-73), A1 to A4 (defined there), Definitions 1.2 and 2.1 (L05.html:63, :79) and "
        "Lab 1; each is defined in the lesson. Naming a term before its definition in the preview is the same accepted pattern as in round 10 (a note, not a ruling-26 kind)."),
    "BK4b-L05-why-ungraded-claim": (
        "L05.html:51 changed. The why paragraph makes no empirical or graded claim: it names propositions, the modelled loss and Lab 1 only. PASS."),
    "BK4b-L05-M2-citation": None,
    "BK4b-r2-L05-numbering": None,
    "BK4b-r2-L05-why-dependence-attribution": (
        "L05.html:51 changed. The why paragraph attributes nothing to an outside source; it names the lesson's own propositions, Assumption 1.3, A1 to A4, and Lab 1."),
    "BK4b-r2-L05-M1-model": None,
    "BK4b-r2-title-casing": None,
    "BK4b-r3-L05-uses-metadata": None,
    "BK4b-grade-legend-L04": None,
    "BK4b-L04-bps-convention-note": (
        "L04.html:69 changed in its last sentence only (the Assumption 4 pointer). The basis-point sentence 'Its value in basis points is floor(10000 rho), the floor "
        "of 10000 rho, as in L04, Definition 2.1' is unchanged. Definition 2.1 (L04.html:90) computes floor(10000 theta) exactly. Consistent."),
    "BK4b-L05-quiz-prop21-scope": None,
    "BK4b-L04-amounts-integer-cents-scope": (
        "L04.html:69 changed (last sentence, Assumption 4 pointer). Definition 1.2 (L04.html:65) still says the reserves and claims are 'in integer cents at face value'; "
        "Remark 4.1 (L04.html:375-378) measures reserves at (1 - h) of face value, which the page says is not a whole-cent amount (:56). Scope unchanged. PASS."),
    "BK4b-L04-assumption1-face-value-conflict": None,
    "BK4b-L04-path-increasing-order": None,
    "BK4b-twin-page-exact": (
        "Re-run at 2a805c83: python -I -W error ledgers/BK4/scripts/BK4-b-r11/twin_vs_page_r11.py <checkout> /tmp/bk4b_r1d_scratch -> L04 page code == twin True "
        "(7676 vs 7677 chars); L04 twin exit 0, stderr 0 bytes; L04 page expected == twin stdout True (38 lines); L05 page code == twin True (7442 vs 7443 chars); "
        "L05 twin exit 0, stderr 0 bytes; L05 page expected == twin stdout True (31 lines); RESULT: PASS (" + S + "closing_twin_vs_page.txt)."),
    "BK4b-slice-delta": (
        "git diff --stat 95f3f8cb..2a805c83 over the BK4 slice paths (course/modules/BK/BK4, tests/labs/BK4, tests/test_labs.py, tests/test_refs.py, references, notation, "
        "curriculum, tools, course/assets, course/concepts.html, CURRICULUM.md): only course/modules/BK/BK4/L04.html (3 lines), L05.html (5 lines) and cards.json "
        "(2 lines) change; 10 insertions, 10 deletions. Hunks: " + DELTA_TXT + "."),
    "BK4b-r8-card-c074": (
        "BK4-c074 object unchanged, but it cites L04.html:391, which changed. Re-read against the new misconception: the card says for rho = 1 under Assumptions 1 to 3 the "
        "coverage is exactly 1 at every admissible share (Proposition 2.4), and with the Assumption 4 valuation (h > 0) the measured coverage is below 1 at every "
        "share admissible for 1 - h (Remark 4.1). Matches L04.html:376 and :391. Grade T, basis 'Proposition 2.4 and Remark 4.1 (Assumption 4)' correct."),
    "BK4b-r8-card-c075": None,
    "BK4b-r8-scope-words": (
        "Scope words in every added line of L04.html and L05.html traced (" + S + "closing_delta_scan.txt): 'only while x <= rho' (L04.html:52) is the necessity direction "
        "of Remark 2.3 (L04.html:106-108: x > rho makes the reserves negative); 'compares face values only' (L04.html:69) is the definition of rho; 'exactly when' "
        "(L04.html:52) is Proposition 2.4; 'every share admissible' (L04.html:391) follows from theta - 1 = (rho - 1)/(1 - x); 'the same mean' (L05.html:482) is "
        "Propositions 2.2 and 2.4; 'not only whole numbers' (L05.html:466) is an explicit extension. No unsupported scope claim. Tests and twins contain no change."),
    "BK4b-r9-card-c072": None,
    "BK4b-r9-L05-no-source-claim": None,
    "BK4b-r10-scope-no-T1": (
        "grep -c T1 over L04.html, L05.html, tests/labs/BK4/lab-BK4-L04-1.py, tests/labs/BK4/lab-BK4-L05-1.py and cards.json at 2a805c83: 0 matches in each."),
    "BK4b-r9-terms-before-definition": (
        "L04.html:52 and :69 changed. Both are forward pointers that name Section 2 explicitly ('In the model of Section 2' at :52; 'Assumption 4, stated in Section 2' at :69, "
        "stated at :85 under the Section 2 heading at :77). 'Admissible' is defined at :90 before first use at :94. Pointer use, accepted as in round 10; "
        "term order is a note and not a ruling-26 kind."),
    "BK4b-r9-build-site": (
        "tools/build_site.py --check -> 'site data current: 6 outputs', exit 0 (" + S + "closing_build_site_check.txt)."),
    "BK4b-r9-curriculum-render": (
        "tools/render_curriculum.py exit 0 and git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json exit 0 (" + S + "closing_render_curriculum.txt, closing_render_diff.txt)."),
    "BK4b-cards-duplicates": (
        "cards.json at 2a805c83: 100 objects, 100 unique ids; no duplicate front and no duplicate back across all 100 cards (" + S + "closing_cards_delta.txt). "
        "Changed objects BK4-c014 (L01, slice a) and BK4-c088; the total stays 100."),
    "BK4b-cards-grades-basis": (
        "Changed card BK4-c088 (grade T, basis 'Proposition 2.4 (proof in Section 2); Proposition 2.2 and Proposition 2.1') mirrors key row L05.html:482 (T, same propositions). "
        "BK4-c089 (T, basis 'Example 2.7') mirrors row :485 (T, 'Example 2.7 (arithmetic on the page)'). BK4-c086 and BK4-c094 (T, basis Example 2.8) mirror row :486. "
        "BK4-c087 (C, Lab 1 Part D) mirrors row :487 (C). All grades and bases agree."),
    "BK4b-banned-and-process-words": (
        "check_pages.py --unit BK4 PASS (its banned-word scan, " + S + "closing_check_pages.txt). Scan of added lines (" + S + "closing_delta_scan.txt): no process words "
        "(we, this section, the lab shows, paragraph, let us); cards c088 and c014 read as learner text."),
    "BK4b-notation": (
        "Changed text uses p, kappa, ell_i, rho, theta, h, x, E, Prob, Var, indicator with their lesson meanings. notation/notation.json (unchanged in the delta) defines the "
        "macros \\E, \\Prob, \\Var, \\indic and the symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}; it has no kappa, ell, rho, theta or x entry, so no "
        "reuse conflict. R3 (L05.html:466) keeps kappa as cost per day and ell_i as delay."),
    "BK4b-hours": None,
    "BK4b-dag-prose-terms": (
        "check_dag.py --unit BK4 PASS (" + S + "closing_check_dag.txt). Added lines carry no concept anchor (" + S + "closing_delta_scan.txt). New terms 'par redemption', "
        "'Assumption 4', 'Remark 4.1', 'Example 2.8', 'Lab 1' are unit-local and defined in the unit; no prerequisite outside the closure is named."),
    "BK4b-r10-dag-prose-terms": None,
    "BK4b-registry-citation-consistency": (
        "L05.html:348 and :580 unchanged; references/references.json has no change in the delta (git diff -U0 empty), so the bisndbasel entry (lines 2815-2842) and the BK4 "
        "entries are byte-identical. Re-read as in BK4b-citation-bisndbasel; verify_refs --unit BK4 PASS (3 of 560, 0 problems)."),
    "BK4b-L04-assumption4-scope": (
        "L04.html:69 (pointer) and :391 (misconception 1) changed. Assumption 4 is stated at :85 (under the Section 2 heading at :77), so 'stated in Section 2' is correct. "
        "Its listed uses remain true: Assumption 1 (:82), Definition 1.2 (:69), Remark 4.1 (:375-378), Problem R1 (:428), Misconception 1 (:391, now via the measured "
        "reserves at (1 - h)), key-results row (:447), quiz items 8 and 9 (:505-520), and the Lab 1 haircut check. The constant haircut 0 <= h < 1 matches "
        "Assumption 4 (:85)."),
    "BK4b-L04-seeded_path-docstring": None,
    "BK4b-L04-haircut-docstring": None,
    "BK4b-L04-misconception3": None,
    "BK4b-cards-c076": None,
    "BK4b-L04-admissible-undefined": None,
    "BK4b-L04-remark3.2-FC1-paraphrase": (
        "L04.html:368 is unchanged. FC1 L01.html:73 (inside Assumption 2.0, FC1 Section 2) changed: 'defined in Section 2' was dropped from the S_n sentence and "
        "'Assumptions A1 to A3 below hold.' was added. The FC1 lines the paraphrase quotes are unchanged in the delta: FC1 L01.html:67 (Section 2 heading), :71 (deposits "
        "are the bank's liabilities), :79-81 (Definition 2.1 'the increase in total deposits that results when the bank makes a loan and the proceeds are deposited back "
        "at the same bank'). The FC1 hunks are at lines 51, 73 and 320 only (git diff -U0). The L04 paraphrase still matches."),
    "BK4b-L04-def1.2-section4-claim": (
        "L04.html:69 changed. Its claim 'Section 4 treats a constant haircut to face value (Assumption 4)' is correct: Section 4 (L04.html:372-386) contains Remark 4.1 "
        "(:375-378) on the haircut and its consequences."),
    "BK4b-L05-M2-hunk-lines": None,
    "BK4b-r11-face-value-term": None,
    "BK4b-r11-scope-notes-L05-P3": None,
    "BK4b-r11-pytest-refs": (
        ".venv/bin/python -m pytest tests/test_refs.py -q -> all passed, exit 0 (" + S + "closing_pytest_refs.txt). tests/test_refs.py is not in the delta."),
    "BK4b-r1-ruling13-regrade-L05-486": (
        "Example 2.8 (L05.html:152-153) changed by adding 'Under A1 and A2' before Proposition 2.1; the derivation is unchanged (2187.5 = 17500/8 = 4375/2, half-up 2188). "
        "Ruling 13: a value derived on the page in a numbered Example is T with the Example as basis. Key row :486 (T, basis Example 2.8) and cards BK4-c086 and BK4-c094 "
        "(T, basis Example 2.8) are unchanged and consistent."),
    "BK4b-r1-card-count-L05": (
        "L05 cards at 2a805c83: 14 (BK4-c077, c078, c079, c080, c081, c083, c084, c086, c087, c088, c089, c090, c094, c098), per " + S + "closing_cards_delta.txt. "
        "No L05 card is added or removed in this delta; no key row or lesson sentence cites a removed id."),
    "BK4b-r1-delta-scope-ruling30": (
        "Ruling 30 delta for slice b: git diff -U0 95f3f8cb..2a805c83 over the slice paths gives " + DELTA_TXT + ". Every row whose subject changed is re-verified in this file; "
        "every other row is carried with the carry prefix and was checked not to cite a changed line. Outside slice b and not verified here: BK4-c014 (cards.json:117, L01, "
        "slice a), FC1 L01.html:51, :73, :320, FC1 L02, L03, index and cards.json, tests/labs/E4, tests/labs/M3, tests/test_lx1_project_lab3.py, plans/FINAL-ARCHITECT-RULINGS.md."),
    "BK4b-cards-c076-placeholder": None,
}
REV = {k: v for k, v in REV.items() if v is not None and not k.endswith("placeholder")}

CARRY_NOTE = ("Carried from round 1 (cited lines byte-identical since the previous pin 95f3f8cb; the round-1 delta " + DELTA_TXT +
              " is not among them):")
CARRY = [k for k in base_rows if k not in REV]

def strip_prefix(text):
    return re.sub(r"^Carried from round \d+ \(.*?\):\s*", "", text, count=1)

rows = []
for rid, brow in base_rows.items():
    if rid in REV:
        rows.append({"id": rid, "check": brow["check"], "location": brow["location"], "status": "PASS",
                     "evidence": REV[rid]})
    else:
        rows.append({"id": rid, "check": brow["check"], "location": brow["location"], "status": brow["status"],
                     "evidence": CARRY_NOTE + " " + strip_prefix(brow["evidence"])})
assert len(rows) == len(base_rows) == 90
assert all(r["status"] == "PASS" for r in rows), "base FAIL row must be re-verified and PASS"

# Guard: a carried row must not cite a changed line of L04/L05/cards.json (location numbers) or a changed card id.
flags = []
for r in rows:
    if r["id"] in REV:
        continue
    loc = r["location"]
    for path, lines in CHANGED.items():
        short = path.split("/")[-1]
        for m in re.finditer(re.escape(short) + r":([0-9][0-9,\- :]*)", loc):
            nums = set()
            for part in re.split(r"[,; ]+", m.group(1)):
                part = part.lstrip(":")
                if re.fullmatch(r"\d+-\d+", part):
                    a, b = map(int, part.split("-"))
                    nums |= set(range(a, b + 1))
                elif part.isdigit():
                    nums.add(int(part))
            hit = sorted(nums & lines)
            if hit:
                flags.append((r["id"], short, hit))
    for cid in CHANGED_CARDS:
        if cid in loc:
            flags.append((r["id"], cid, "card"))
print("carry-guard flags (should be empty):", flags)
assert not flags, flags

fragment = {
    "unit": "BK4",
    "slice": "b",
    "round": 1,
    "verifier": "Haiku independent verifier, BK4-b closing delta round 1 (did not build BK4; ruling 30 delta from the round-1 base; ruling 37: no new mutants)",
    "pin": "2a805c831410ab77c38c227f7e121e8537193ce9",
    "base": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672 (base fragment /Users/billyribeiro/.fanout/frags/F3-BK4-b.round1.json, verdict FAIL on BK4b-cards-L04-L05-scan, which is resolved here)",
    "checkout": str(REPO),
    "scratch": "/tmp/bk4b_r1d_scratch (twin-vs-page scratch); copies of every command output are in ledgers/BK4/scripts/BK4-b-r1/closing_*.txt",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": base.get("registry_flags", []),
    "freshness_flags": base.get("freshness_flags", []),
    "notes": [
        "Delta since the base pin 95f3f8cb in slice b (git diff -U0): L04.html:52, :69, :391; L05.html:51, :153, :466, :482, :485; cards.json:687 (BK4-c088 front) and :117 (BK4-c014, L01, slice a).",
        "The base FAIL (BK4-c088 front dropped A3 while the back cites Proposition 2.2, which needs A3) is fixed: the front again assumes A3 (cards.json:687). Re-verified from scratch.",
        "Ruling-26 kinds checked on every changed hunk: no false or unproved statement, no missing hypothesis, no wrong number, no over-grade, no failing gate, no unsupported lab statement. R3 (L05.html:466) explicitly extends A2 to real parameters; its solution's claim that the Proposition 2.1 proof does not use integrality is accurate.",
        "Observation (not a FAIL): L04.html:52 uses 'par redemption' and 'coverage' before their definitions (L04.html:82, :90), with a forward pointer 'In the model of Section 2'. Same pointer pattern accepted in round 10.",
        "Observation (not a FAIL): key row L05.html:487 stays C although Proposition 2.5 gives the sign of Var_4 - Var_3 for every parameter set; the C grade is conservative, and the row says 'for the SIMULATED parameters'.",
        "Observation (not a FAIL): key row L05.html:486 and card BK4-c094 use the Example 2.8 value; Lab 1 Part B prints the same value as a check, per ruling 13.",
        "Out of slice and not verified here: BK4-c014 (cards.json:117, L01 back now says 'Bank A in Lab 1 (SIMULATED day)'; slice a), FC1 L01.html:51, :73, :320, FC1 L02/L03/index/cards.json, tests/labs/E4, tests/labs/M3, tests/test_lx1_project_lab3.py, plans/FINAL-ARCHITECT-RULINGS.md.",
        "Mutants: none written (ruling 37). Slice b has no grader and no project; the lab twins are demonstrations (ruling 26/Rulings note). The standing mutant set for slice b is empty.",
    ],
    "summary": (
        "BK4-b closing delta round 1 (95f3f8cb..2a805c83, rulings 30 and 37): verdict PASS. 90 rows, all PASS: "
        + str(len(REV)) + " re-verified from scratch this round (the base FAIL BK4b-cards-L04-L05-scan, every row whose cited subject changed, and every gate), "
        + str(len(CARRY)) + " carried with the carry prefix (cited subjects byte-identical; guard script found no carried row citing a changed line). "
        "Gates re-run at 2a805c83 and PASS: check_pages, check_dag, check_projects, run_labs 8/8, twins under python -I -W error, twin-vs-page, page_smoke alone, "
        "pytest test_labs -k BK4 (8), pytest test_refs, ruff check, ruff format --check, mypy --no-incremental on the twins, verify_refs --offline (560, 0) and --unit BK4 (3, 0), "
        "build_site --check, render_curriculum with an empty git diff, recompute_r11 (60 ALL OK), and a new exact-fraction recompute (17 OK, 0 FAIL)."
    ),
}

problems = []
for r in rows:
    if not r["evidence"].strip():
        problems.append(r["id"])
assert not problems, problems
OUT.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", OUT, "rows", len(rows), "re-verified", len(REV), "carried", len(CARRY))
