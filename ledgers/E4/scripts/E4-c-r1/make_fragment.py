"""Build ledgers/E4/E4-c.json (round 1) from the base round-11 fragment and this round's checks."""

from __future__ import annotations

import json
import sys

BASE = "/Users/billyribeiro/.fanout/frags/E-E4-c.round11.json"
OUT = "/Users/billyribeiro/.fanout/wt/verifyF31-E4-c/ledgers/E4/E4-c.json"
OUT_DIR = "ledgers/E4/scripts/E4-c-r1/out/"

base = json.load(open(BASE, encoding="utf-8"))

CARRY_PAGES = (
    "Carried from round 11 (course/modules/E/E4/L07.html, L08.html, L09.html and tests/labs/E4/lab-E4-L07-1.py, "
    "lab-E4-L08-1.py, lab-E4-L09-1.py byte-identical since the previous pin 11d7077a):"
)
CARRY_HUB = (
    "Carried from round 11 (cited index.html lines byte-identical since the previous pin 11d7077a, re-checked this round; "
    "index.html changed only at line 63):"
)
CARRY_L06 = (
    "Carried from round 11 (cited L06.html lines byte-identical since the previous pin 11d7077a, re-checked this round; "
    "L06.html changed elsewhere and is outside this slice):"
)

# Rows whose subject changed in this delta, or that cite cards.json, the milgrom record, curriculum.json, L06
# statements, or a gate: re-verified this round with the evidence below.
REVERIFIED = {
    "E4c-r4-delta-read": (
        "Round 11 base row re-verified this round. git diff 11d7077a..HEAD over the slice paths: L07.html, L08.html, "
        "L09.html and the three twins are byte-identical (no hunk). cards.json changed (see E4c1-cards-changed-L07, "
        "-L08, -L09); index.html changed at line 63 only. Every cited page line is unchanged."
    ),
    "E4c-r4-recheck-numbers": (
        "Re-derived this round with ledgers/E4/scripts/E4-c-r1/indep_cards_L07_L09.py (out/indep_cards_L07_L09.out) "
        "and the twin outputs out/twin_L07-1.out, out/twin_L08-1.out, out/twin_L09-1.out. Pages unchanged, so the "
        "page-level numbers are the round-11 numbers; the card-level numbers were re-derived in E4c1-independent-numbers."
    ),
    "E4c-cmd-check-pages": (
        "Command: .venv/bin/python tools/check_pages.py --unit E4 -> out/check_pages_E4.out: 'check_pages E4: PASS' "
        "(covers cards.json: unique ids, lessons exist, grades and cites valid, 259 cards)."
    ),
    "E4c-cmd-check-dag": (
        "Command: .venv/bin/python tools/check_dag.py --unit E4 -> out/check_dag_E4.out: 'check_dag E4: PASS'."
    ),
    "E4c-cmd-check-projects": (
        "Command: .venv/bin/python tools/check_projects.py --unit E4 -> out/check_projects_E4.out: "
        "'check_projects E4: PASS'."
    ),
    "E4c-cmd-run-labs": (
        "Commands: tools/run_labs.py --unit E4 --page L07 / L08 / L09 -> out/run_labs_L07.out, run_labs_L08.out, "
        "run_labs_L09.out, each 'run_labs E4: PASS (1/1)'."
    ),
    "E4c-cmd-twins-standalone": (
        "Commands: env -i ... .venv/bin/python -I -W error tests/labs/E4/lab-E4-L0{7,8,9}-1.py from fresh mktemp "
        "directories -> exit 0 for all three; out/twin_L07-1.out, twin_L08-1.out, twin_L09-1.out; the .err files are 0 bytes."
    ),
    "E4c-expected-equals-output": (
        "Compared each page's expected <pre> block (the block containing 'Part A') with out/twin_L07-1.out, "
        "out/twin_L08-1.out, out/twin_L09-1.out after stripping blank lines and surrounding whitespace: equal for L07, L08 and L09."
    ),
    "E4c-cmd-page-smoke": (
        "Command: .venv/bin/python tools/page_smoke.py --unit E4 --pages L07 L08 L09 -> out/page_smoke_L07-9.out: "
        "'page_smoke modules/E/E4/L07.html: PASS', L08 and L09 PASS, 'page_smoke E4: PASS'."
    ),
    "E4c-cmd-ruff-mypy-twins": (
        "Commands: .venv/bin/ruff check tests/labs/E4 -> out/ruff_twins.out (exit 0); .venv/bin/mypy --no-incremental "
        "on the three twins -> out/mypy_twins.out 'Success: no issues found in 3 source files'; repo ruff check . "
        "-> out/ruff_check.out 'All checks passed!'."
    ),
    "E4c-cmd-pytest-labs": (
        "Command: .venv/bin/python -m pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -k E4 "
        "-> out/pytest_labs_E4.out: 13 tests, exit 0."
    ),
    "E4c-cmd-verify-refs": (
        "Commands: tools/verify_refs.py --offline -> out/verify_refs_offline_r1.out 'offline integrity: 560 entries, 0 "
        "problems'; tools/verify_refs.py --unit E4 -> out/verify_refs_unit_E4.out 'live re-verification of E4: 3 of 560 "
        "entries, 0 problems'."
    ),
    "E4c-cmd-run-graders": (
        "Command: .venv/bin/python tools/run_graders.py --unit E4 --seeds 0-49 -> out/run_graders_E4_r1.out: "
        "'run_graders E4: PASS (reference 50/50 seeds, slowest 0.2 s)'. Project grader is another slice; the gate was run "
        "because the base fragment listed it."
    ),
    "E4c-L09-references": (
        "L09.html:512 cites milgrom1982information. The record is identical by content between 11d7077a and HEAD "
        "(json comparison by key: identical). Its locator moved from references.json:17291 to :17293 because the "
        "black1973pricing used_by list gained FC2 above it (record unchanged)."
    ),
    "E4c-r5-milgrom-record": (
        "references/references.json key milgrom1982information compared by content with 11d7077a: identical. "
        "Only changes in the file: generated_at (line 3) and black1973pricing used_by (adds FC2). Locator now :17293."
    ),
    "E4c8-registry-milgrom": (
        "Re-checked this round: milgrom1982information record identical by content to 11d7077a (json comparison by key)."
    ),
    "E4c9-L09-milgrom-no-claim": (
        "Re-checked this round: L09.html:512 unchanged; milgrom1982information record identical by content (json "
        "comparison by key) to 11d7077a."
    ),
    "E4c10-milgrom-abstract": (
        "The Crossref output ledgers/E4/scripts/E4-c-r10/out/crossref_milgrom.json is a previous-round artifact; the record "
        "it checks is identical by content (json comparison by key), so the check still applies."
    ),
    "E4c8-delta-read": (
        "Re-read this round: L07.html and L08.html and L09.html byte-identical to 11d7077a; cards.json changed (re-verified "
        "in E4c1-cards-*); index.html lines 33 and 167 unchanged (re-checked)."
    ),
    "E4c9-delta-read": (
        "Re-read this round: L09.html:124, 402-405 and L08.html lines unchanged (byte-identical file); curriculum.json "
        "changes are only the M3 and FC2 project briefs (not E4, see E4c1-curriculum)."
    ),
    "E4c-r5-cards-duplicates": (
        "course/modules/E/E4/cards.json: 259 cards, unique ids, unique fronts and backs (script output in this round). "
        "Round 11 said 243 cards; this round added 18 and removed 3."
    ),
    "E4c-r5-cards-L07": (
        "Re-verified: L07 cards are 22 (E4c1-cards-changed-L07 lists the 9 changed and 1 added card). Card set checked "
        "against the unchanged L07.html text."
    ),
    "E4c-r5-cards-L08": (
        "Re-verified: L08 cards are 49 (E4c1-cards-changed-L08 lists the 14 changed and 7 added cards; E4-c224 removed)."
    ),
    "E4c-r5-cards-L09": (
        "Re-verified: L09 cards are 24 (E4c1-cards-changed-L09 lists E4-c200, c203, c206 changed and E4-c269 added)."
    ),
    "E4c8-cards-L07-L09": (
        "Re-verified: 95 cards with lesson L07, L08 or L09 (22, 49, 24), replacing the round-11 count of 87 "
        "(21, 43, 23) after the changes in E4c1-cards-*."
    ),
    "E4c10-cards-count-and-changed": (
        "Re-verified: 259 cards total; the changed set is listed in E4c1-cards-changed-L07/L08/L09 and the "
        "removed and added set in E4c1-cards-removed-added."
    ),
    "E4c11-cards-L07-L09-full-scan": (
        "Re-scanned this round: 95 cards with lesson L07, L08 or L09 (not 87); every changed and added card compared "
        "with the lesson text (E4c1-cards-changed-*); unchanged cards carry the round-11 check."
    ),
    "E4c10-banned-phrases": (
        "Re-checked this round: cards.json changed; no process word (round, ruling, verifier, fixed, changed, now, we, I) in "
        "any changed or added card; check_pages BANNED list passes (out/check_pages_E4.out)."
    ),
    "E4c10-notation-scan": (
        "Re-checked this round: notation/notation.json registers 8 symbols (T, Phi, gamma_3, gamma_4, R^*, R^e*, R_f, Q). "
        "No changed card uses one of them; the E4 symbols in the cards are lesson-local (L08.html:75 says so)."
    ),
    "E4c10-ruff-mypy-repo": (
        "Commands: .venv/bin/ruff check . -> 'All checks passed!'; .venv/bin/ruff format --check . -> '555 files already "
        "formatted'; .venv/bin/mypy --no-incremental -> 'Success: no issues found in 386 source files'."
    ),
    "E4c10-twin-equals-page": (
        "Re-run this round: page expected blocks equal twin stdout for L07, L08 and L09 (see E4c-expected-equals-output)."
    ),
    "E4c10-expected-equals-stdout": (
        "Re-run this round: L07.html, L08.html and L09.html expected blocks equal out/twin_L07-1.out, twin_L08-1.out, "
        "twin_L09-1.out (see E4c-expected-equals-output)."
    ),
    "E4c9-L06-statements-used": (
        "L06.html changed in this delta (Lemma 6.3 and 6.4 proofs cite G(i) and G(ii); A4 residual at two pairs; Step 3 of "
        "Proposition 6.7 evaluates at (1,0) and (0,1)). Re-read the used statements: Lemma 6.3 and 6.4 (proofs and "
        "statements), Proposition 6.7 Step 2 and Step 3, Corollary 6.8, Remark 6.10. The changes are hypothesis wording "
        "and an equivalent two-point evaluation (the (0,0) point gave no extra constraint); the formulas used by L07 to L09 "
        "are unchanged. Assumption G is at L06.html:90-91."
    ),
    "E4c10-L06-statements-used": (
        "Re-verified this round after the L06 change (see E4c9-L06-statements-used): the closed form of Proposition 6.7, "
        "Lemma 6.3 and 6.4 variances, and Corollary 6.8 are unchanged in formula; L06 lab outputs (tests/labs/E4/lab-E4-L06-1.py, "
        "run this round from a fresh temporary directory, python -I -W error, not saved to out/) print tau_eta 1/2, rho2 1/3, slope 7/9, Var(v|p) 2/3, all consistent with the L07 and L08 numbers."
    ),
    "E4c10-dag-closure": (
        "Re-checked: check_dag E4 PASS (out/check_dag_E4.out); curriculum.json changes are the M3 and FC2 project briefs "
        "only, so the E4 prerequisite entries (E2, E3, M7 and closure) are unchanged."
    ),
    "E4c11-cmd-check-pages-unit": (
        "Command: tools/check_pages.py --unit E4 -> 'check_pages E4: PASS' (out/check_pages_E4.out)."
    ),
    "E4c11-cmd-check-dag-unit": "Command: tools/check_dag.py --unit E4 -> 'check_dag E4: PASS' (out/check_dag_E4.out).",
    "E4c11-cmd-check-projects-unit": (
        "Command: tools/check_projects.py --unit E4 -> 'check_projects E4: PASS' (out/check_projects_E4.out)."
    ),
    "E4c11-cmd-run-labs-L07-L09": (
        "Commands: tools/run_labs.py --unit E4 --page L07 / L08 / L09 -> PASS (1/1) each (out/run_labs_L07.out, "
        "run_labs_L08.out, run_labs_L09.out)."
    ),
    "E4c11-cmd-twins-standalone": (
        "Re-run: python -I -W error on each twin in an isolated env -> exit 0, empty stderr (out/twin_L0{7,8,9}-1.*)."
    ),
    "E4c11-cmd-page-smoke-L07-L09": (
        "Command: tools/page_smoke.py --unit E4 --pages L07 L08 L09 -> 'page_smoke E4: PASS' (out/page_smoke_L07-9.out)."
    ),
    "E4c11-cmd-ruff-mypy-slice": (
        "Commands: ruff check tests/labs/E4 (exit 0) and mypy --no-incremental on the three twins ('Success: no issues "
        "found in 3 source files'), out/ruff_twins.out and out/mypy_twins.out."
    ),
    "E4c11-cmd-ruff-mypy-repo": (
        "Commands: ruff check . ('All checks passed!'), ruff format --check . ('555 files already formatted'), "
        "mypy --no-incremental ('Success: no issues found in 386 source files')."
    ),
    "E4c11-cmd-pytest-labs-subset": (
        "Command: pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -k E4 -> 13 tests, exit 0."
    ),
    "E4c11-cmd-verify-refs": (
        "Commands: tools/verify_refs.py --offline ('560 entries, 0 problems') and tools/verify_refs.py --unit E4 "
        "('3 of 560 entries, 0 problems'), out/verify_refs_offline_r1.out and out/verify_refs_unit_E4.out."
    ),
    "E4c11-cmd-run-graders": (
        "Command: tools/run_graders.py --unit E4 --seeds 0-49 -> 'run_graders E4: PASS (reference 50/50 seeds, slowest "
        "0.2 s)' (out/run_graders_E4_r1.out)."
    ),
}

# Rows whose cited subject is byte-identical (or whose cited lines are identical): carried with the prefix.
HUB_IDS = {
    "E4c-L07-hours", "E4c-L08-hours", "E4c-L09-hours", "E4c-L08-hub-title", "E4c-L09-hub-title",
    "E4c10-hub-data-arithmetic", "E4c11-hub-data-status-fixed", "E4c-r2-delta-read",
}
L06_IDS = {"E4c-L08-define-posterior", "E4c-r6-L08-definition-6.2-link", "E4c-L08-dfn-duplicates",
           "E4c-r3-first-use-before-definition"}

rows: list[dict[str, str]] = []
for r in base["rows"]:
    rid = r["id"]
    row = dict(r)
    if rid in REVERIFIED:
        row["evidence"] = REVERIFIED[rid]
        row["status"] = "PASS"
    else:
        if r["status"] != "PASS":
            raise SystemExit(f"base non-PASS row {rid} must be re-verified")
        if rid in HUB_IDS:
            prefix = CARRY_HUB
        elif rid in L06_IDS:
            prefix = CARRY_L06
        else:
            prefix = CARRY_PAGES
        row["evidence"] = f"{prefix} {r['evidence']}"
    rows.append(row)

NEW = [
    {
        "id": "E4c1-delta-read",
        "check": "delta",
        "location": "git diff 11d7077a..95f3f8cb over course/modules/E/E4 (L07, L08, L09, index, cards.json), tests/labs/E4, references, curriculum, notation",
        "status": "PASS",
        "evidence": (
            "git diff --stat: L07.html, L08.html, L09.html, lab-E4-L07-1.py, lab-E4-L08-1.py, lab-E4-L09-1.py and notation/ "
            "have no hunk. index.html: one hunk at line 60-63 (prerequisites paragraph: 'From E2 it uses adverse selection, "
            "which Lesson 9 lists among its uses'). cards.json: 70 changed cards, 18 added, 3 removed (id-level comparison "
            "of git show 11d7077a and HEAD: 244 old cards, 259 new, removed c121, c224, c247, added 18, changed 70). "
            "references.json: generated_at line and black1973pricing used_by (adds FC2). curriculum: M3 and FC2 briefs only. "
            "L06.html changed (outside this slice; its changes are checked in E4c9-L06-statements-used)."
        ),
    },
    {
        "id": "E4c1-cards-changed-L07",
        "check": "2.7-cards",
        "location": "course/modules/E/E4/cards.json E4-c132, c134, c139, c140, c142, c147, c148, c149, c150 (changed); E4-c264 (added)",
        "status": "PASS",
        "evidence": (
            "Each changed card checked against L07.html: c132 = Definition 7.2 (L07.html:61-65); c134 = Lemma 7.4 b (L07.html:80-81); "
            "c139 = Remark 7.8 rho2 < rho0^2 for sigma_u > 0 and limit (L07.html:122); c140 = Remark 7.9 Var(p) (L07.html:127); "
            "c142 = L07 lab Part B values 4/9, 1/3, 1/6, 1/18, 1/66 (out/twin_L07-1.out, rechecked exactly in out/indep_cards_L07_L09.out); "
            "c147 = Remark 7.9 and Proposition 7.7 (L07.html:127, 382); c148 = Proposition 7.6 equivalent form and base tau_eta = 1/2 "
            "(L07.html:102, 386; L06 lab Part A prints tau_eta 1/2, Part B rho2 1/3); c149 = Proposition 7.6 and 7.7 (L07.html:97-118, 390); "
            "c150 = Proposition 7.7 strictly increasing in lambda, values 1/6, 1/3, 9/22 (L07.html:112, 394; out/twin_L07-1.out Part C). "
            "c264 = Lemma 7.4 residual variance (L07.html:81). No number on a changed card missing from L07.html (grep)."
        ),
    },
    {
        "id": "E4c1-cards-changed-L08",
        "check": "2.7-cards",
        "location": "course/modules/E/E4/cards.json E4-c155, c159, c160, c162, c163, c167, c168, c176, c177, c181, c183, c184, c186, c187 (changed); E4-c256, c257, c258, c259, c260, c262, c270 (added)",
        "status": "PASS",
        "evidence": (
            "Checked against L08.html and the L08 twin output out/twin_L08-1.out: c155 = Assumption A4 (L08.html:314-318, part (ii) assumed); "
            "c159 and c160 = Corollary 2.4 posterior means (L08.html:125-126); c162 and c163 = Proposition 3.1 incl. uniqueness "
            "with beta_p nonzero (L08.html:151-169); c167 = Proposition 4.1 Var(D_I) (L08.html:207); c168 = Proposition 4.2 EU_I "
            "(L08.html:222); c176 = Proposition 5.1(c) (L08.html:290, 298); c177 = Proposition 5.2(a) limit of G (L08.html:307); "
            "c181 = Part A residual 1.332e-15, tolerance 1e-12, lam 0.5, seed 20261103, 20000 draws (out/twin_L08-1.out); "
            "c183 = Part C cost 0.12, lam* = 1, gap 7.71e-03 (out/twin_L08-1.out; G(1) - 0.12 by out/indep_cards_L07_L09.out prints 7.71e-03); "
            "c184 = Part D max |gain| 0.0e+00 (out/twin_L08-1.out); c186 = Definition 4.6 (i), Proposition 4.4, G(0) = ln(2)/4 (L08.html:267-275, 240); "
            "c187 = Lemma 3.3(a) and Proposition 5.1(a) (L08.html:191, 288); c256 = Corollary 2.4(a) V_I (L08.html:125, 132); c257 = Corollary 2.4(b) V_U (L08.html:126, 133); "
            "c258 = Proposition 4.1 Var(D_U) (L08.html:207); c259 = Proposition 4.2 EU_U (L08.html:222); c260 = Var(D_U) limit a^2 sigma_u^2 sigma_v^4 "
            "(L08.html:325-328), re-derived numerically in out/indep_cards_L07_L09.out (4.0000 and 26.998 vs predicted 4.0 and 27.0); "
            "c262 = Part C cost 0.18, lam* = 0, gap -6.71e-03 (out/twin_L08-1.out; G(0) - 0.18 prints -6.71e-03 in out/indep_cards_L07_L09.out); "
            "c270 = Part D: 0 interior fractions with gain = cost 0.15, G(0) = 0.173287 > 0.15, G(1) = 0 < 0.15 (out/twin_L08-1.out, out/indep_cards_L07_L09.out). "
            "Every number on these cards appears in L08.html (grep)."
        ),
    },
    {
        "id": "E4c1-cards-changed-L09",
        "check": "2.7-cards",
        "location": "course/modules/E/E4/cards.json E4-c200, c203, c206 (changed); E4-c269 (added)",
        "status": "PASS",
        "evidence": (
            "Checked against L09.html:118-120 (Example 2.4), L09.html:108-111 (Corollary 2.3, raw text 'g_1(omega) < 0 or g_2(omega) < 0'), "
            "L09.html:264-281 (Lab 1 block) and out/twin_L09-1.out: c200 M(1) = {1,2,3}, g_1(1) = 1/2 (out/indep_cards_L07_L09.out); "
            "c203 exactly x(3)=0 and x(2)=-x(1), 5*5^3 = 625 of 15625, enumerated (indep script: nonneg on meet 625, zero posteriors 625, "
            "strict at state 1 500) and printed by the lab (out/twin_L09-1.out part B); c206 = Corollary 2.3 with the raw inequality; "
            "c269 = g_2(1) = 1/3, g_1(3) = -2 (L09.html:119). Numbers appear in L09.html (grep)."
        ),
    },
    {
        "id": "E4c1-cards-removed-added",
        "check": "2.7-cards",
        "location": "course/modules/E/E4/cards.json: removed E4-c121 (L06), E4-c224 (L08), E4-c247 (L06); added E4-c251, c252, c253, c256 to c266, c268 to c271 (18 cards)",
        "status": "PASS",
        "evidence": (
            "Removed E4-c224 (L08) asked whether lambda = 0 or 1 is an equilibrium at cost 0.15 and printed G(0)=0.173287, G(1)=0.000000; "
            "its content is covered by the new E4-c262 and E4-c270 (both verified in E4c1-cards-changed-L08). "
            "E4-c121 and E4-c247 are L06 cards (outside this slice; their lesson is checked by the L06 verifier). "
            "Added L07, L08 and L09 cards are E4-c256, c257, c258, c259, c260, c262, c264, c269, c270 (verified above). The other added cards "
            "(E4-c251, c252, c253, c261, c263, c265, c266, c268, c271; lessons L01, L02, L04, L05, L06) belong to other slices and are not checked here."
        ),
    },
    {
        "id": "E4c1-cards-numbers-in-lessons",
        "check": "2.7-cards",
        "location": "course/modules/E/E4/cards.json changed and added L07, L08, L09 cards vs L07.html, L08.html, L09.html",
        "status": "PASS",
        "evidence": (
            "grep -F of each number on a changed or added card in its lesson text: 7.71e-03 (L08.html x2), 6.71e-03 (x2), 1.332e-15 (x1), "
            "0.0e+00 (x1), 1e-12 (x6), 999 (x5), 625 (L09.html x14), 15625 (x7), 0.173287 (x4), 0.127706 (x4), 9/22 (L07.html x6), "
            "1/66 (x5), 729/1444 (x3), 35937/4802 (x3), 2/3 (x1), 20000 (x3), 20261103 (x2), and the cost values 0.12, 0.15, 0.18 all occur "
            "in the lesson text. Each number occurs at least once in the lesson that the card cites."
        ),
    },
    {
        "id": "E4c1-cards-count-duplicates",
        "check": "2.7-cards",
        "location": "course/modules/E/E4/cards.json (259 cards; L07 22, L08 49, L09 24)",
        "status": "PASS",
        "evidence": (
            "Python json check (sandbox -I): 259 cards, no duplicate id, no duplicate front, no duplicate back; 95 cards with lesson L07, L08 or L09; "
            "check_pages cards check passes (out/check_pages_E4.out)."
        ),
    },
    {
        "id": "E4c1-independent-numbers",
        "check": "2.2-numbers",
        "location": "ledgers/E4/scripts/E4-c-r1/indep_cards_L07_L09.py; out/indep_cards_L07_L09.out",
        "status": "PASS",
        "evidence": (
            "Own exact-Fraction and float script written from the lesson formulas (not the lab code): rho2 sweep 4/9, 1/3, 1/6, 1/18, 1/66; "
            "Var(p) 729/1444, 27/49, 27/32, 729/338, 35937/4802; lambda sweep 1/6, 1/3, 9/22; rho2 < 1/2 for sigma_u^2 > 0 and -> 1/2; "
            "G(0) = ln2/4 = 0.173287, G(1) = ln(5/3)/4 = 0.127706 (gain(1.0) matches); cost gaps 7.71e-03 and -6.71e-03; "
            "0 interior fractions with gain = 0.15 at sigma_u^2 = 0; lim Var(D_U) = a^2 sigma_u^2 sigma_v^4 (4.0 and 27.0); "
            "Example 2.4 values and 625 of 15625 bets."
        ),
    },
    {
        "id": "E4c1-hub-prereq-adverse-selection",
        "check": "2.9-prose",
        "location": "course/modules/E/E4/index.html:63 (prerequisites paragraph, changed this delta) vs course/modules/E/E4/L09.html:37",
        "status": "PASS",
        "evidence": (
            "Hub text 'From E2 it uses adverse selection, which Lesson 9 lists among its uses' matches L09.html:37 'Uses: ... adverse "
            "selection (contrast only)'. The concept link is unchanged (concepts.html#adverse-selection). Hub hours and title lines "
            "(index.html:33, 38, 121, 147-149, 167) unchanged (re-checked by sha256 of each line)."
        ),
    },
    {
        "id": "E4c1-L06-changed-lines-used-by-L07-L09",
        "check": "2.4-mathematics",
        "location": "course/modules/E/E4/L06.html changed hunks (git diff 11d7077a..HEAD -- course/modules/E/E4/L06.html; Assumption A1, A4, Lemmas 6.3 and 6.4, Proposition 6.7, Corollary 6.8, Solution P1 and R3 of Lab text, L06.html:552 and 613-628); used by L07.html:98-107, 127; L08.html:126, 155-170, 207, 222-228, 325-328; L09.html:512",
        "status": "PASS",
        "evidence": (
            "L06 changes: A1 cites G(i); A4 residual evaluated at (1,0) and (0,1); Lemma 6.3/6.4 proofs cite G(i)/G(ii) and Lemma 6.2 "
            "conditional normality; Proposition 6.7 Step 3 evaluates at (1,0),(0,1) (the (0,0) point gave Q*theta_s = lambda*tau_eps "
            "and Q*theta_u = a from nothing more). The equations Q theta_s = lambda tau_eps and Q theta_u = a follow from the two "
            "points alone; the (0,0) point is redundant, so the change is correct. G(i)/G(ii) are stated at L06.html:90-91. The formulas used by L07 (Proposition 6.7 "
            "coefficients, Step 2, Remark 6.10 via Remark 7.9) and by L08 (Lemma 6.3 posterior variances) are unchanged in content."
        ),
    },
    {
        "id": "E4c1-process-words-cards",
        "check": "2.12-process",
        "location": "course/modules/E/E4/cards.json changed and added L07, L08, L09 cards",
        "status": "PASS",
        "evidence": (
            "Regex scan of front, back and basis of the 35 changed or added L07 to L09 cards for round, ruling, verif, changed, fixed, revis, "
            "previous, now, we, I, new, updat, obviously, clearly, ... and TODO/TBD: only '(i)' case labels matched. Banned phrases "
            "pass check_pages (out/check_pages_E4.out)."
        ),
    },
    {
        "id": "E4c1-cards-prop-hypotheses",
        "check": "2.9-structure",
        "location": "course/modules/E/E4/cards.json changed and added proposition cards (E4-c139, c162, c163, c167, c168, c176, c177, c256-c260, c264)",
        "status": "PASS",
        "evidence": (
            "Each proposition card states its hypotheses as in the lesson: c139 'A1 to A4 and G of L06, sigma_u > 0' (Proposition 7.6 "
            "and Remark 7.8); c162/c163 'sigma_u^2 > 0', lambda in (0,1]; c167/c168/c258/c259 'A1 to A3, lambda in (0,1]' (Propositions "
            "4.1, 4.2); c176 'sigma_u^2 = 0, c >= G(0)' (Proposition 5.1(c)); c177/c260 'sigma_u^2 > 0' (Proposition 5.2(a)); c256/c257 "
            "'A1 to A3' (Corollary 2.4); c264 'zero means, positive variances' (Lemma 7.4). No card drops a hypothesis the lesson states."
        ),
    },
    {
        "id": "E4c1-card-grades",
        "check": "2.3-grades",
        "location": "course/modules/E/E4/cards.json E4-c142, c181, c183, c184, c262, c270 (grade C); c260, c200, c203, c269 (grade T)",
        "status": "PASS",
        "evidence": (
            "Lab-derived values (c142, c181, c183, c184, c262, c270) are grade C with a basis naming the lab part (the check_pages cards check requires a cite or basis for graded results); "
            "c181 names SIMULATED Part A. Proof-derived or exact-enumeration values (c200, c203, c260, c269) are grade T; c203 is an exact "
            "enumeration reproduced by the lab (out/twin_L09-1.out part B) and c260 is a proof limit (L08.html:325-328). No changed grade-T card "
            "rests on the SIMULATED Part F or Part A (the T cards cite proofs or exact parts)."
        ),
    },
    {
        "id": "E4c1-milgrom-locator",
        "check": "2.1-citations",
        "location": "references/references.json (key milgrom1982information, now line 17293); course/modules/E/E4/L09.html:512",
        "status": "PASS",
        "evidence": (
            "Record compared by key with 11d7077a: identical. Registry check verify_refs offline and unit PASS (out/verify_refs_offline_r1.out, "
            "out/verify_refs_unit_E4.out). Only the locator moved (line 17291 to 17293) because a record above it gained FC2 in used_by."
        ),
    },
]

rows.extend(NEW)

fragment = {
    "unit": "E4",
    "slice": "c",
    "round": 1,
    "verifier": "Claude Haiku 5.5, independent verifier for E4-c round 1 (first independent verification of this slice; did not build E4)",
    "pin": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
    "base": "11d7077a290f7960b183d3a5a6631af4773888f9",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyF31-E4-c",
    "scratch": "fresh mktemp -d directories under $TMPDIR named e4c1_<lab>.XXXX for the twin runs (python -I -W error, env -i); indep script in ledgers/E4/scripts/E4-c-r1/",
    "verified_at": "2026-11-09T12:00:00+00:00",
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": base["registry_flags"]
    + [
        "milgrom1982information: record identical by content to 11d7077a; locator now references.json:17293 (black1973pricing used_by gained FC2 above it).",
        "black1973pricing: used_by gains FC2 (project slice; not checked here).",
    ],
    "freshness_flags": [],
    "notes": (
        "Round 1 of the closing delta for E4-c (base: round 11, pin 11d7077a). Scope: L07, L08, L09 pages, their twins, cards.json "
        "(L07 to L09 cards), and the hub prerequisites line. Pages and twins are byte-identical to the base pin, so their base rows "
        "are carried with the prefix. Re-verified from scratch: every card changed or added in L07 to L09 (26 changed, 9 added, 1 removed), "
        "every gate command in the slice, the milgrom registry record, and the L06 statements used by L07 to L09. "
        "Observation, not a FAIL: card E4-c167 back says 'Both gaps have mean zero' but the front defines only D_I (D_U is not on the card); "
        "the statement is correct (Proposition 4.1 gives E D_I = E D_U = 0). Observation, not a FAIL: E4-c184 and E4-c270 share the "
        "same Part D of the lab and differ in the question asked. No mutants: slice c is not a project slice (ruling 26 FAIL kinds only, "
        "no new mutants)."
    ),
    "summary": (
        "E4-c round 1: 181 base rows kept (ids unchanged) and 14 rows added; all PASS. 26 changed and 9 added L07 to L09 cards "
        "verified against the lesson text and re-derived numbers; pages and twins byte-identical to 11d7077a; all slice gates re-run and PASS."
    ),
    "could_not_check": [
        "Browser rendering of L07, L08 and L09 (no visual review; page_smoke is the check that ran).",
        "Grossman and Stiglitz (1980): no registry record (B1, REFERENCE_REQUEST R-E4-1); L08 cites no key, so no attributed claim is checked.",
        "Milgrom and Stokey and Milgrom (1982) abstract: not re-read in this round; L09 attributes only title, venue, volume, issue and pages, which are identical by content.",
        "Part F of L07 and Part A of L08 are SIMULATED; the independent recomputation reproduces the printed statistic with the same seed and draw order; it is not an independent statistical test.",
        "L06 proofs were not re-read line by line as a slice of their own (another slice); only the statements L07 to L09 use were checked.",
        "The full repository pytest suite was not run (only the E4 subset and repository ruff and mypy); mutate_graders was not run (not a project slice).",
        "Other-slice cards in cards.json (L01 to L06) changed in this delta and are not checked here.",
        "The verifier-rules exemplar calibration (blind scorers, ruling 23) does not apply to this slice; no calibration rows exist in the base.",
    ],
}

with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("rows", len(rows), "ids unique", len({r['id'] for r in rows}) == len(rows))
