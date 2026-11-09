"""Build ledgers/LX1/LX1-a.json for the LX1 slice a closing delta (round 1, pin 2a805c83, base 95f3f8cb).

Re-verified rows carry new evidence from this round; every other base row is carried with the carry prefix
because its cited lines are byte-identical since 95f3f8cb (git diff -U0 hunk list checked in this round).
"""
import json
import re
import sys
from datetime import datetime, timezone

CHECKOUT = "/Users/billyribeiro/.fanout/wt/verifyG1-LX1-a"
BASE_PATH = "/Users/billyribeiro/.fanout/frags/F3-LX1-a.round1.json"
OUT = CHECKOUT + "/ledgers/LX1/LX1-a.json"
S = "ledgers/LX1/scripts/LX1-a-r1/out-closing"
PREV = "95f3f8cb"

base = json.load(open(BASE_PATH, encoding="utf-8"))
base_rows = {r["id"]: r for r in base["rows"]}

fresh = {
    "LX1a-cmd-check_pages": f"Re-run at 2a805c83: 'check_pages LX1: PASS', exit 0 ({S}/check_pages.txt).",
    "LX1a-cmd-check_dag": f"Re-run at 2a805c83: 'check_dag LX1: PASS', exit 0 ({S}/check_dag.txt).",
    "LX1a-cmd-check_projects": f"Re-run at 2a805c83 (project.html changed at line 473, outside the slice pages): 'check_projects LX1: PASS', exit 0 ({S}/check_projects.txt).",
    "LX1a-cmd-run_labs": f"Re-run at 2a805c83: 'run_labs LX1: PASS (7/7)', exit 0 ({S}/run_labs_unit.txt).",
    "LX1a-cmd-twins-isolated": f"Re-run at 2a805c83: python -I -W error on lab-LX1-L01-1.py and lab-LX1-L02-1.py, exit 0 each, stderr empty ({S}/twin_L01.err, twin_L02.err).",
    "LX1a-cmd-page_smoke": f"Re-run at 2a805c83: 'page_smoke LX1: PASS' for index, L01, L02 ({S}/page_smoke.txt).",
    "LX1a-cmd-ruff-mypy": f"Re-run at 2a805c83 on the two twins: 'All checks passed!', '2 files already formatted', 'Success: no issues found in 2 source files' ({S}/ruff_twins.txt, mypy_twins.txt).",
    "LX1a-cmd-pytest": f"Re-run at 2a805c83: pytest -o addopts='' on test_labs.py, test_run_labs.py, test_page_checks.py, test_docs_figures.py: '420 passed in 49.47s' (420 collected); exit 0 ({S}/pytest_subset.txt).",
    "LX1a-cmd-verify_refs-offline": f"Re-run at 2a805c83: 'offline integrity: 560 entries, 0 problems' ({S}/verify_refs_offline.txt).",
    "LX1a-cmd-fetch_data-check": f"Re-run at 2a805c83: 'fetch_data: 3 datasets, 0 problems' ({S}/fetch_data_check.txt).",
    "LX1a-cmd-mutate_graders": f"Re-run at 2a805c83: mutate_graders --unit LX1 exit 0, no output; run_graders reports 'no autograder (grading: rubric)' ({S}/mutate_graders_LX1.txt, run_graders_LX1.txt). LX1 has no grader; no mutants (ruling 37).",
    "LX1a-lab-L02-1": f"Re-run at 2a805c83: page_twin_check.txt 'L02 page code == twin (trailing newline ignored): True', 'L02 expected block == twin output: True'; twin_L02 exit 0. Changed line L02.html 300 (interpretation) checked against the twin's Part D output: 'V_12 / V_0 = P_0 / P_12 holds exactly: True' (lines 293-296) and HORIZON = 12 (twin line 162), so 'Part D confirms Proposition 2.1(b) at the horizon H = 12' is supported; the 'whole horizon' wording removed in the delta was the only change.",
    "LX1a-num-L01-mechanics": f"Re-derived at 2a805c83 with exact Fractions ({S}/../closing_numbers.py, run with -I): Mech 1 F0 = 250/0.06 = 12500/3 = 4166.67, half-up 4167 (L01.html 334). Mech 2 1.04^3 = 17576/15625 = 1.124864, 250 x 1.124864 = 281.216, /0.06 = 4686.93, half-up 4687 (line 338, unchanged). Mech 3 q = 1, term d1/(1+r) = 2000/21, S_10 = 20000/21 = 952.38 = 1000/1.05 (line 342 new text: 'the partial sums equal N d1/(1+r)' = 10 x 100/1.05 = 952.38, consistent). Prop 1.4 hypotheses cited at 342 match L01.html line 91.",
    "LX1a-math-L01-thm1.3": "Re-derived at 2a805c83 from L01.html lines 55-85: (A0) r > g and 1+g > 0 gives r > g > -1, so 1+r > 0; q = (1+g)/(1+r), 1-q = (r-g)/(1+r) > 0, 0 < q < 1 since 1+r > 1+g > 0; S_N(t) = F_t(1-q^N) exactly; F_t = d1(1+g)^t/(r-g) = d_{t+1}/(r-g) by (A1) with s = t+1. Changed line 67 (Definition 1.2 remark, 'this lesson does not use it as a forecast of any price') is a benign prose change; grep for 'forecast' in L01 finds only line 387 (the dividend forecast in Research 3), not a forecast of a price by F_t.",
    "LX1a-math-L01-problems": "FAIL in base (Proof 2 solution divided by F_{t-1}, valid only for d1 != 0). Re-verified from scratch at 2a805c83, now PASS. Proof 2 (L01.html 353): F_t = d1(1+g)^t/(r-g) for every t >= 0 (Theorem 1.3); for t >= 1, (1+g)^t = (1+g)(1+g)^{t-1}, so F_t = (1+g) d1(1+g)^{t-1}/(r-g) = (1+g) F_{t-1}; no division. Python (closing_numbers.py): F_t = (1+g)F_{t-1} exact for d1 in {0, 400, -250, 1/3} and t = 1..14 at r = 9%, g = 3%: True. Proof 1 (349): strict monotonicity on -1 < g < r with reciprocals of a > b > 0 and d1 > 0; grid check True. Proof 3 (357): (A1) with d1 > 0, 1+g > 0, r > -1, g > r gives q > 1 and terms d1 q^{k-1}/(1+r) -> infinity. Mech 1-3 as in LX1a-num-L01-mechanics. Empirical 1 (364): 9 of 13 (lab line 265), share 0.6923 (python 9/13 = 0.692308). Empirical 2 (368): 13 - 9 = 4 (lab lines 265, 281). Empirical 3 (372): 2175/8698 = 0.250057 -> 25.01 percent; F_9 = 400 x 1.03^9 / 0.06 = 8698.49 (python), wedge +0.25 exact (twin wedge = randint/100), price 1.25 x F_9 rounds to 10873, 10873 - 8698 = 2175; unrounded gap 0.25 F_9 = 2174.62 rounds to 2175; exact 25.00 percent. Research 1 (379): g* = 0.09 - 400/6000 = 7/300 = 0.023333, benchmark at g* = 6000 (python). Research 2-3 (383, 387): qualitative, no numbers; consistent with Prop 2.2 and Definition 2.1. Quiz numerics (418-436) recomputed: F_0 = 6666.67, F_2 = 7072.67, q = 0.944954, g* = 0.023333.",
    "LX1a-math-L02-prop1.2": "Re-derived at 2a805c83 from L02.html 55-78: Definition 1.1 (55-58); changed line 60 ('the currency price of gold, and says nothing about the prices of goods') matches Remark 1.3 (line 77: 'It says nothing about the prices of goods'); Proposition 1.2 hypothesis (A1) line 65 (parity at every date); proof lines 71-72 give one gram costs 1/kappa; conclusion line 67. The argument uses only the parity, so the T grade is supported by the stated convertibility definition.",
    "LX1a-num-L02-counts": "Re-verified at 2a805c83 against the printed twin output (L02.html 259-299): Part C 'periods with a falling price index: 6 of 12' and 'rising real value: 6 of 12' (line 300 'twelve periods'; 319). Solutions 390-392: negative changes at t = 1, 5, 6, 8, 9, 12 (printed -1, -4, -1, -4, -3, -4), positive at t = 2, 3, 4, 7, 10, 11 (python recomputation: falls = [1, 5, 6, 8, 9, 12]). Line 443: 5/2 currency units per gram. Line 446: 100/94.70509914... = 1.0559093..., to six decimals 1.055909 (= printed V12/V0 1055909/10^6). Lines 494-496: six, t = 1, 5, 6, 8, 9, 12. Line 300 numbers: horizon 12 and twelve periods match the twin.",
    "LX1a-notation-L01": "Re-verified at 2a805c83: grep 'P_[{0-9t]' in L01.html = 0; A_0 x7, A_t x5, B_t x3, one meaning (observed price, gap, lines 105, 114, 119-120, 378). Symbols newly used in changed lines (g', a, b, q, N, d_1) are local to their lessons (notation.json 'about': N, S and similar letters are local). notation.json registers only T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}; grep of the L01 and L02 changed lines finds none of them. Macros used (\\ge, \\ast, \\cdot, \\kappa, \\mapsto, \\ne, \\sum) are standard TeX, none is a registry macro with another meaning.",
    "LX1a-dag-links": "Re-run at 2a805c83: data-concept and dfn-id sequence of L01 and of L02 identical to 95f3f8cb (closing_text_checks.txt 'L01 identical', 'L02 identical'); index.html unchanged in the delta; changed lines of L01 (67, 334-356) carry no concept link.",
    "LX1a-dag-outside-closure": "Re-run at 2a805c83: grep of the outside-closure names (bank run, fire sale, leverage cycle, ..., deposit insurance) over index, L01, L02: 0 hits (closing_text_checks.txt, 'hits=1' means no match).",
    "LX1a-dag-defined-once": "Re-run at 2a805c83: dfn ids of L01 (def-fundamental-value, def-speculative-bubble, def-financial-panic) and L02 (def-gold-standard, def-debt-deflation) identical to 95f3f8cb; no duplicate ids.",
    "LX1a-struct-L01-L02": "Re-counted at 2a805c83: L01 and L02 each have 12 problem blocks (3 per tier, 4 tiers), 10 quiz items, 3 misconception list items, one lab section with SIMULATED in its heading; section order unchanged (no h2 hunk in the delta).",
    "LX1a-prose-banned": "Re-run at 2a805c83 over index, L01, L02: 0 hits for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, it can be shown, roughly, historically, of course, and ellipses (closing_text_checks.txt).",
    "LX1a-prose-process-words": "Re-run at 2a805c83 over index, L01, L02: 0 hits for ruling, verifier, fixer, ledger, fragment, mutant, blind, architect, checkout, slice, round N (closing_text_checks.txt).",
    "LX1a-hub-historian-regulator": "Re-run at 2a805c83: grep -c historian|regulator = 0 in index.html, L01.html, L02.html.",
    "LX1a-data-figures": "Re-run at 2a805c83: grep -c svg|class=\"chart\"|data-figures|data-files = 0 in index.html, L01.html, L02.html; the lab sections carry data-runtime only.",
    "LX1a-L02-prop12-no-lab-check": "Re-verified at 2a805c83: L02.html 131 claims the lab checks Proposition 2.1, Corollary 3.2 and part (b) at H = 12, not Proposition 1.2. Line 300 (changed) says Part E confirms 1/kappa of Proposition 1.2 'at one illustrative parity' and that the lab 'does not test the assumption that the parity holds at every date, which is (A1)'; Part E (twin lines 251-255, expected 297-299) prints one parity only (2/5 gram). The claim is limited to one parity, so no over-claim.",
    "LX1a-L02-CU-undefined": "Re-verified at 2a805c83: grep '\\bCU\\b' in L02.html and lab-LX1-L02-1.py: 0 hits. The lab text uses 'currency unit' / 'currency units' (L02.html 135, 297-298, 443), defined by Definition 1.1 (line 57, 'one unit of the currency').",
    "LX1a-twin-page-equality": f"Re-run at 2a805c83: page_twin_check.py ({S}/page_twin_check.txt): L01 and L02 page code == twin (trailing newline ignored): True; expected block == twin output: True for both. Exact byte difference is the final newline only.",
    "LX1a-scope-words": "Re-run at 2a805c83 over the 9 added lines of the delta in L01, L02, index (closing_text_checks.txt): 'does not use it as a forecast of any price' (L01 67; 'forecast' in L01 only at line 387, a dividend forecast); 'needs only r != g' (L01 353; the algebra step uses only the closed form, which needs r != g); 'for every real d1, including d1 = 0' (L01 353; python check for d1 in {0, 400, -250, 1/3}); 'only under an explicit assumption' (L02 60; Proposition 1.2 has the single hypothesis (A1)); 'every count is an integer' (L02 300; counts are integers by construction, twin integer lists); 'does not test the assumption that the parity holds at every date' (L02 300; Part E has one parity); 'with no calendar length specified' (L02 300). No new unsupported universal.",
    "LX1a-r3-full-read": "This round: every changed hunk of the slice pages and twins was read with its line numbers (git diff -U0 95f3f8cb..HEAD): L01.html 67, 334, 342, 348, 353, 356; L02.html 60, 131, 300; lab-LX1-L01-1.py and lab-LX1-L02-1.py unchanged. Unchanged lines of L01.html and L02.html are byte-identical to 95f3f8cb (no other hunk), so the round-1 full read of them stands for the unchanged text; the changed hunks were re-read in full in this round (L01.html 36-130, 318-440 and L02.html 50-301 were read in this round).",
    "LX1a-r3-delta": "Current delta (git diff 95f3f8cb..2a805c83) over the slice paths, hunk by hunk: L01.html 67 (LX1a-math-L01-thm1.3, LX1a-scope-words); 334, 342 (LX1a-num-L01-mechanics, LX1a-math-L01-problems); 348, 353, 356 (LX1a-math-L01-problems, LX1a-scope-words); L02.html 60 (LX1a-math-L02-prop1.2, LX1a-scope-words); 131 (LX1a-lab-L02-1, LX1a-L02-prop12-no-lab-check); 300 (LX1a-lab-L02-1, LX1a-num-L02-counts, LX1a-L02-prop12-no-lab-check, LX1a-scope-words); twins unchanged. Outside the slice: project.html 473 (LX1a-cmd-check_projects re-run), cards.json (not in this slice's base scope, see notes), course/modules/E/E5/index.html and course/modules/FC/FC1/index.html (cited lines 6 and 32 unchanged, LX1a-hub-E5-title and LX1a-hub-fc1-title carried).",
}

carry_ids = [
    "LX1a-lab-L01-1", "LX1a-num-L01-closed-form-sums", "LX1a-num-L01-prop22-witness", "LX1a-num-L01-canon-breaks-367",
    "LX1a-num-L01-lab-counts", "LX1a-num-L01-empirical-shares", "LX1a-num-L01-quiz-numeric", "LX1a-num-L02-real-values",
    "LX1a-num-hub-placement", "LX1a-num-hub-hours", "LX1a-math-L01-prop1.4", "LX1a-math-L01-prop2.2",
    "LX1a-math-L02-prop2.1-cor3.2", "LX1a-math-L02-problems", "LX1a-notation-L02-T", "LX1a-notation-L02-Q",
    "LX1a-notation-hub", "LX1a-struct-hub", "LX1a-claim-E5-prop1.7", "LX1a-claim-registry-records",
    "LX1a-claim-attribution-readings", "LX1a-claim-fed-licence", "LX1a-claim-fx-note-blanks",
    "LX1a-claim-hub-no-other-series", "LX1a-claim-P0.1-not-released", "LX1a-claim-simulated-labels",
    "LX1a-claim-hub-math-prereqs", "LX1a-hub-L03-concept-claim", "LX1a-hub-fc1-title", "LX1a-hub-fx-one-lab",
    "LX1a-hub-derivative-claim", "LX1a-L01-usual-first-test", "LX1a-L01-gap-integer-cents",
    "LX1a-L01-prop22-unnumbered-assumptions", "LX1a-L01-only-quantitative-tool", "LX1a-L02-misconception-gold-price",
    "LX1a-hub-E5-title", "LX1a-hub-hours-rung1", "LX1a-hub-objective-panic", "LX1a-cmd-verify_refs-live",
]

def strip_carry(ev):
    return re.sub(r"^Carried from round \d+ \([^)]*\)[^:]*:\s*", "", ev)

rows = []
for r in base["rows"]:
    rid = r["id"]
    if rid in fresh:
        status = "PASS"
        ev = fresh[rid]
    elif rid in carry_ids:
        status = "PASS"
        ev = (f"Carried from round 1 (cited lines of {r['location']} byte-identical since the previous pin {PREV}, "
              f"checked by git diff -U0 at 2a805c83): " + strip_carry(r["evidence"]))
    else:
        raise SystemExit(f"row {rid} neither fresh nor carried")
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev})

ids_base = [r["id"] for r in base["rows"]]
assert [r["id"] for r in rows] == ids_base, "row ids must be kept"
assert set(fresh) <= set(ids_base) and set(carry_ids) <= set(ids_base)
assert len(set(fresh) & set(carry_ids)) == 0
assert set(fresh) | set(carry_ids) == set(ids_base), (set(ids_base) - set(fresh) - set(carry_ids))

counts = {"PASS": sum(1 for r in rows if r["status"] == "PASS"), "FAIL": sum(1 for r in rows if r["status"] == "FAIL")}
now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
frag = {
    "unit": "LX1",
    "slice": "LX1-a",
    "round": 1,
    "verifier": "Haiku independent verifier, LX1 slice a, closing delta round 1 (ruling 30); did not build LX1",
    "pin": "2a805c83",
    "base": "95f3f8cb (F3-LX1-a.round1.json, verdict FAIL, 72 rows, one FAIL: LX1a-math-L01-problems); delta = git diff 95f3f8cb..2a805c83 over the slice paths",
    "checkout": CHECKOUT,
    "scratch": CHECKOUT + "/ledgers/LX1/scripts/LX1-a-r1/out-closing",
    "verified_at": now,
    "verdict": "PASS" if counts["FAIL"] == 0 and counts["PASS"] == len(rows) else "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "references/references.json: byte-identical across 95f3f8cb..2a805c83 (git diff empty); the round-1 informational flag stands unchanged: reinhart2009this used_by gained LX1 and generated_at changed; the records for this slice's keys are unchanged (informational, outside the slice defect list)."
    ],
    "freshness_flags": [
        "course/modules/E/E5/index.html and course/modules/FC/FC1/index.html changed in the repo delta outside this slice; the cited lines of those files (E5 6 and 32, FC1 6 and 32) are unchanged, so LX1a-hub-E5-title and LX1a-hub-fc1-title are carried.",
        "course/modules/LX/LX1/cards.json changed in the delta (lines 6, 48, 173, 182, 739-740, 753-761); cards are not in this slice's base scope (base notes), so it is not verified here."
    ],
    "notes": [
        "Closing delta (ruling 30) against the round-1 fragment at 95f3f8cb. Ruling 26 FAIL kinds only: the single base FAIL (LX1a-math-L01-problems, a proof gap in Proof 2 for d1 = 0) is fixed in the delta (L01.html 353 now multiplies out with no division) and re-verified from scratch: PASS. No new FAIL row was found in the rows whose subject changed.",
        "Ruling 37: no new mutants written. LX1 has no grader; mutate_graders --unit LX1 exits 0 with no output; run_graders reports rubric grading, so the standing mutant set is empty and mutants is [].",
        "Observation for the cards slice (not a row of this slice): cards.json LX1-c092 (front 'Proposition 1.4 hypotheses: d_1 > 0, 1 + g > 0, r > -1 and g > r') states the strict inequality g > r, while L01.html line 91 (Proposition 1.4) states g >= r. The card's answer is correct for g > r, but its stated hypotheses differ from the lesson. Not checked as a row here because cards.json is outside this slice's base scope.",
        "Observation: the twin's Part B header and printed label say 'price' while the docstring says A_t; the page uses A_t (ruling 16), and the printed text is a label only (carried from round 1).",
        "Observation: symbol letter A is shared by the assumption labels (A0)-(A4) and the observed price A_t; they have distinct typographic roles and the registry holds no A symbol (carried from round 1).",
        "Working tree: ledgers/LX1/scripts/LX1-a-r1/ holds tracked artifacts from an earlier verifier. This round's files are closing_run_cmds.sh, closing_numbers.py, closing_text_checks.sh, closing_write_fragment.py, with outputs in out-closing/ (and this fragment's RUN.log).",
        "Not checked here: the verify_refs live (network) run, carried because references/ is byte-identical since 95f3f8cb; the cards.json delta (outside this slice's base scope); project.html changes beyond the command row (other slice); unchanged L01/L02 text was not re-read line by line this round, its evidence is carried by byte-identity of the cited lines (round-1 full read).",
    ],
    "summary": {
        "rows": len(rows),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": 0,
        "carried_rows": len(carry_ids),
        "fresh_rows": len(fresh),
        "commands_run": [
            "tools/check_pages.py --unit LX1", "tools/check_dag.py --unit LX1", "tools/check_projects.py --unit LX1",
            "tools/run_labs.py --unit LX1", "python -I -W error on lab-LX1-L01-1.py and lab-LX1-L02-1.py (alone)",
            "ledgers/LX1/scripts/LX1-a-r1/page_twin_check.py (python -I)", "ledgers/LX1/scripts/LX1-a-r1/closing_numbers.py (python -I)",
            "tools/page_smoke.py --unit LX1 --pages index L01 L02", "ruff check and ruff format --check on the two twins",
            "mypy --no-incremental on the two twins", "pytest -o addopts='' on test_labs, test_run_labs, test_page_checks, test_docs_figures (420 passed)",
            "tools/verify_refs.py --offline", "tools/fetch_data.py --check", "tools/mutate_graders.py --unit LX1", "tools/run_graders.py --unit LX1",
            "ledgers/LX1/scripts/LX1-a-r1/closing_text_checks.sh", "git diff -U0 95f3f8cb..HEAD over the slice paths",
        ],
        "scripts": [
            "ledgers/LX1/scripts/LX1-a-r1/closing_run_cmds.sh", "ledgers/LX1/scripts/LX1-a-r1/closing_numbers.py",
            "ledgers/LX1/scripts/LX1-a-r1/closing_text_checks.sh", "ledgers/LX1/scripts/LX1-a-r1/closing_write_fragment.py",
            "ledgers/LX1/scripts/LX1-a-r1/page_twin_check.py",
        ],
    },
}
json.dump(frag, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("rows", len(rows), "fresh", len(fresh), "carried", len(carry_ids), "verdict", frag["verdict"])
