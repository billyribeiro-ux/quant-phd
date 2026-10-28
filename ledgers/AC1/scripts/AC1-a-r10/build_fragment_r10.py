"""Builds ledgers/AC1/AC1-a.json (round 10, AC1-a) from the round 9 fragment and round 10 re-checks.

Run: <checkout>/.venv/bin/python -I <this file>  (reads /tmp/fanout-frags/AC1-a.round9.json; writes the fragment).
"""

import json
import sys
from pathlib import Path

CHECKOUT = Path("/tmp/verify10-AC1-a")
R9 = json.loads(Path("/tmp/fanout-frags/AC1-a.round9.json").read_text(encoding="utf-8"))
S = "/tmp/ac1-v/a-r10"
SCRIPT = "ledgers/AC1/scripts/AC1-a-r10/witness_r10.py"

FRESH: dict[str, tuple[str, str]] = {
    "AC1a-cmd-check_pages": ("PASS", f"Re-run at af08ad1: 'check_pages AC1: PASS', exit 0 ({S}/check_pages.out)."),
    "AC1a-cmd-check_dag": ("PASS", f"Re-run at af08ad1: 'check_dag AC1: PASS', exit 0 ({S}/check_dag.out)."),
    "AC1a-cmd-run_labs": ("PASS", f"Re-run at af08ad1: 'run_labs AC1: PASS (11/11)', exit 0 ({S}/run_labs.out)."),
    "AC1a-cmd-page_smoke": ("PASS", f"Re-run at af08ad1: 'page_smoke AC1: PASS', exit 0; lab-AC1-L03-1 0.0 s ({S}/page_smoke.out)."),
    "AC1a-cmd-verify_refs": ("PASS", f"Re-run at af08ad1: live '2 of 560 entries, 0 problems' and offline '560 entries, 0 problems', both exit 0 ({S}/verify_live.out, verify_off.out). references/references.json not in the 96dd532..af08ad1 diff."),
    "AC1a-cmd-ruff-mypy": ("PASS", f"Re-run at af08ad1: ruff check 'All checks passed!'; ruff format --check '212 files already formatted'; mypy --no-incremental tests/labs/AC1 'Success: no issues found in 11 source files'; all exit 0 ({S}/ruff.out, mypy.out)."),
    "AC1a-cmd-twin-run": ("PASS", f"Re-run at af08ad1 under python -I -W error: L01 exit 0, L02 exit 0, L03 exit 0, stderr 0 bytes each ({S}/L01.out, L02.out, L03.out). L03 final line 'all articulation identities hold in every year: True'."),
    "AC1a-cmd-pytest-AC1": ("PASS", f"Re-run at af08ad1: pytest -q tests -k 'AC1 or lab' 143 dots, exit 0 ({S}/pytest.out). Collect-only per-file counts sum to 143 (test_labs 127, test_run_labs 6, test_page_checks 4, test_page_smoke 2, test_memo_exemplars 2, test_fetch_data 1, test_figure_kernels 1) ({S}/collect.out)."),
    "AC1a-cmd-build-site": ("PASS", f"Re-run at af08ad1: 'site data current: 6 outputs', exit 0 ({S}/build_site.out)."),
    "AC1a-cmd-scope-witness": ("PASS", f"Re-run of ledgers/AC1/scripts/AC1-a-r9/witness_r9.py under python -I at af08ad1: W4 write-off 30 on sales 100 with no collections gives R=100, K=0, dA=70, identity holds: False (output {S}/witness_r9_rerun.out). Hypothesis (i) of Proposition 3.2 (L01.html line 387) excludes write-offs."),
    "AC1a-twin-matches-page": ("PASS", f"Re-run in {SCRIPT} (W6): data-run block of L01.html, L02.html and L03.html equals tests/labs/AC1 twin after html.unescape, all True ({S}/witness_r10.out)."),
    "AC1a-cite-none": ("PASS", "Re-checked at af08ad1: no data-cite or cite-class markup in index.html, L01-L03.html; the word 'registry' occurs only in prose (index.html lines 63, 122, 175)."),
    "AC1a-lab-seeded-offline": ("PASS", "Re-checked at af08ad1: the L01-L03 twins import only __future__, random and dataclasses (grep of import lines); seeded with SEED = 20261027."),
    "AC1a-banned-phrases": ("PASS", "Re-grepped at af08ad1 in index.html, L01-L03.html for 'roughly half', 'about 6%', 'historically', ellipsis characters, 'builder', 'verifier', 'unit report', 'REQUESTS', 'as much as', 'round N': no hit. Three-dot matches are Python annotations (tuple[Line, ...] at L01 line 151, L02 line 200 and 152, L03 lines 178, 226, 498), not omitted content."),
    "AC1a-L01-key-scope": ("PASS", "Fixed at af08ad1. L01.html line 559 now reads 'balance, integer non-negative cents and at most one side per line (Remark 2.2); a line with neither side passes it'. Lab check_entry (tests/labs/AC1/lab-AC1-L01-1.py lines 56-57) rejects a line with both sides and accepts a line with neither; W1 prints 'accepted' for Line('cash') with debit 0 and credit 0, W2 rejects both sides ({S}/witness_r10.out). The table scope now matches the code."),
    "AC1a-r9-L01-remark22-one-side": ("PASS", "Fixed at af08ad1. L01.html line 103 now says the posting checks test 'that no line carries both a debit and a credit' and that 'the check does not refuse a line that carries neither'. Matches check_entry lines 56-57 and W1/W2 in witness_r10.out."),
    "AC1a-grade-T-L02": ("PASS", "Re-checked at af08ad1: Proposition 3.2 (L02.html line 97) now carries the hypothesis 'its only revenue and expense accounts are the four of Definition 2.1', which its proof (line 102, via Proposition 2.2 with hypothesis at line 78) needs. Proof algebra re-derived: A - L - C + H - N = 0 gives A = L + C + (N - H). Lab 2 TYPES (tests/labs/AC1/lab-AC1-L02-1.py lines 21-34) has revenue 'sales' and expenses cost_of_sales, operating_expense, depreciation_expense only. T grade supported."),
    "AC1a-r9-L02-prop32-hypothesis": ("PASS", "Fixed at af08ad1: L02.html line 97 adds the four-account hypothesis to Proposition 3.2 (the only change to its hypotheses). Card AC1-c029 and Remark 3.3 (line 107) carry the same hypothesis. W3 shows the failure mode without it (1000-cent gap for an interest-income entry in the Definition 2.1 identity)."),
    "AC1a-L02-q10-explain-causal": ("PASS", "Fixed at af08ad1: L02.html line 775 now says the hypothesis of Proposition 3.2 excludes a ledger with an interest or tax account, and 'Lab 2's ledger has neither'. Confirmed: the TYPES dict of the L02 twin has no interest or tax account (W4 in witness_r10.out). Option 'No; the proof needs only ... the four income accounts of Definition 2.1 and dividends' (line 773) is the data-correct option."),
    "AC1a-r6-L02-remark33-scope": ("PASS", "Fixed at af08ad1: L02.html line 107 'uses only' list now includes 'the revenue and expense accounts are the four of Definition 2.1', matching Proposition 2.2 and Proposition 3.2 hypotheses."),
    "AC1a-grade-T-L03": ("PASS", "Fixed at af08ad1: L03.html line 76 hypothesis (iv) now reads 'Depreciation and cost of sales are the only expenses that carry no cash line when posted.' Re-derived from the generators: in both twins the expense accounts posted without a cash line are cost_of_sales and depreciation_expense only, and operating_expense is always in a cash entry (W5 in witness_r10.out). Proof algebra for Proposition 2.2 re-derived: N + D - dA + dL = S_k + Q - O - V."),
    "AC1a-r9-L03-theorem-hyp": ("PASS", "Fixed at af08ad1: L03.html line 127 hypotheses now include 'Proposition 4.2 of Lesson 2 with its hypothesis that every cash line of the ledger carries one of the three activities' and the Lesson 2 four-account hypothesis; 'fiscal year: the' now has a space (grep 'fiscal year:the' count 0). The proof's third claim uses L02 Proposition 4.2 (line 121 hypothesis, verified)."),
    "cards-L02-rest": ("PASS", f"Fixed at af08ad1: AC1-c028 (cards.json line 186) now reads 'Yes, with only the four income accounts of Definition 2.1' and AC1-c029 (line 193) carries the four-account hypothesis; both match L02.html lines 78 and 97. Cards AC1-c017 to AC1-c027, c030, c031 carried from round 9 (cards.json lines outside the 96dd532..af08ad1 hunks at 184-193, 213, 271, 862; their L02 numbers 1,003,421.14; 803,421.14; 3,000,000.00; 4,454,305.29 re-read in {S}/L02.out)."),
    "cards-L02-c032": ("PASS", "Fixed at af08ad1: AC1-c032 (cards.json line 216) now opens 'The lesson does not say.' and keeps 'It is a convention set by the generator in Lab 2 (Definition 4.1)'. L02.html line 689 says 'what any reporting framework requires for this split is not stated here'. Grade C with basis retained."),
    "cards-L03-all": ("PASS", "Re-checked at af08ad1: AC1-c040 (cards.json line 274) and AC1-c124 (line 865) now carry 'In the lab's ledger, under the hypotheses of Proposition 3.1' and match Proposition 3.1 (L03.html line 93, hypotheses (i) to (iv)). Other L03 cards (c033-c039, c041-c045, c123, c126) carried from round 9; their cards.json lines are outside the hunks."),
    "AC1a-dag-concepts": ("PASS", f"Re-checked at af08ad1: check_dag AC1 PASS ({S}/check_dag.out). The dfn for statement-articulation is still at L03.html line 57 (Definition 1.1, text changed, id and data-concept unchanged); def-depreciation-and-amortization at line 62 unchanged."),
    "AC1a-num-L03": ("PASS", "Re-checked at af08ad1: misconception 1 (L03.html line 684) now says the indirect method adds the charge back 'because no cash line carries it'; the number 1,500,000.00 is equipment B's 2026 investing line (lab 3 output, Check 4 2026 investing -1,500,000.00 in {S}/L03.out; lab 2 output 'equipment B bought for cash -1,500,000.00'). Interpretation and remaining misconception numbers unchanged."),
    "AC1a-quiz-keys": ("PASS", "Re-checked at af08ad1: L02 quiz item q10 (L02.html lines 768-776) re-verified (see AC1a-L02-q10-explain-causal). L01 quiz and L03 quiz items (L03 q4 explanation line 854) unchanged in the delta; carried from round 9."),
    "AC1a-hours-L01": ("PASS", "Re-checked at af08ad1: L01.html data-hours='11'; hub card 'L01 · 11 h' (index.html line 150)."),
    "AC1a-hours-L02": ("PASS", "Re-checked at af08ad1: L02.html data-hours='12'; hub card 'L02 · 12 h' (index.html line 151)."),
    "AC1a-hours-L03": ("PASS", "Re-checked at af08ad1: L03.html data-hours='11'; hub card 'L03 · 11 h' (index.html line 152)."),
    "AC1a-r10-r9-delta": ("PASS", "placeholder"),
}
del FRESH["AC1a-r10-r9-delta"]

NEW_ROWS = [
    {
        "id": "AC1a-r10-hub-rung2-explain-scope",
        "check": "hub skill check rung 2 explanation states the Proposition 3.2 identity without its hypotheses",
        "location": "course/modules/AC/AC1/index.html line 141 (skill check rung 2 explain); L01.html Proposition 3.2 line 387",
        "status": "FAIL",
        "evidence": "The explain reads 'Revenue less cash received equals the change in receivables: 2,500 less 1,900 is 600 (L01, Proposition 3.2).' The arithmetic (2,500 - 1,900 = 600) is right. But Proposition 3.2 (L01.html line 387, hypothesis (i)) states the identity only when there are no write-offs, returns or allowances, and the question states no such condition. Witness W4 in ledgers/AC1/scripts/AC1-a-r9/witness_r9.py (rerun, output in /tmp/ac1-v/a-r10/witness_r9_rerun.out) shows a write-off of 30 on sales 100 breaks the identity (R-K = 100, dA = 70). The hub states an unconditional identity that the cited proposition does not give. Fix: 'Under Proposition 3.2 with no write-offs, returns or allowances, revenue less cash received equals the change in receivables: 2,500 less 1,900 is 600 (L01, Proposition 3.2).'",
    },
    {
        "id": "AC1a-r10-witness-w1-w6",
        "check": "round 10 witnesses for the changed scope sentences (L01 posting check, L02 and L03 charts, L03 expense postings, twin-page equality)",
        "location": f"{SCRIPT}; tests/labs/AC1/lab-AC1-L01-1.py lines 46-61; lab-AC1-L02-1.py TYPES lines 21-34; lab-AC1-L03-1.py TYPES",
        "status": "PASS",
        "evidence": f"Run under python -I at af08ad1; output {S}/witness_r10.out: W1 a line with neither side is accepted; W2 a line with both sides raises ValueError; W3 an unknown account raises; W3b a balanced entry on a valid wrong account is accepted; W4 the L02 and L03 charts have revenue and expense accounts sales, cost_of_sales, operating_expense, depreciation_expense and no interest or tax account; W5 expense accounts in entries with no cash line are cost_of_sales and depreciation_expense in both labs; W6 the three data-run blocks equal their twins.",
    },
]

ROW_FILES = {
    "course/modules/AC/AC1/index.html": "index.html",
}


def carry(row: dict) -> dict:
    loc = row["location"]
    files = []
    for name in ("index.html", "L01.html", "L02.html", "L03.html", "cards.json", "tests/labs/AC1", "concepts.html"):
        if name in loc:
            files.append(name)
    if not files:
        files = ["course/modules/AC/AC1 (see location)"]
    prefix = (
        "Carried from round 9 (" + ", ".join(files)
        + " cited lines byte-identical since the previous pin; hunks of 96dd532..af08ad1 checked against the cited lines):"
    )
    return {**row, "evidence": prefix + " " + row["evidence"]}


rows = []
for r in R9["rows"]:
    rid = r["id"]
    if rid in FRESH:
        status, ev = FRESH[rid]
        rows.append({**r, "status": status, "evidence": ev})
    elif r["status"] == "FAIL":
        raise SystemExit(f"round 9 FAIL row {rid} has no round 10 re-check")
    else:
        rows.append(carry(r))
rows.extend(NEW_ROWS)

n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_fail = sum(1 for r in rows if r["status"] == "FAIL")
frag = {
    "unit": "AC1",
    "slice": "AC1-a",
    "round": 10,
    "round_note": "round 10 independent verification of AC1-a at af08ad1. Previous pin 96dd532 (AC1-a.round9.json, verdict FAIL, 10 FAIL rows). Delta 96dd532..af08ad1 for this slice: index.html line 31 (eyebrow), L01.html lines 103, 138, 559, L02.html lines 73, 97, 107, 185, 549, 552, 686, 773, 775, L03.html lines 57, 76, 127, 211, 684, 808-811, cards.json c028, c029, c032, c040, c124, tests/labs/AC1 twins L01-L03 docstring line 30/52/211. L07.html, L08.html, tests/labs/AC1 L07 twin and the footers are outside this slice.",
    "verifier": "Haiku independent verifier, AC1-a round 10 (did not build AC1)",
    "pin": "af08ad1",
    "base": "96dd532 (previous verified pin; round 9 fragment ledgers and rows carried per the delta)",
    "checkout": "/tmp/verify10-AC1-a (detached worktree at af08ad1, .venv symlinked)",
    "scratch": "/tmp/ac1-v/a-r10",
    "verified_at": "2026-10-28",
    "registry_flags": [
        "references/references.json: unchanged in 96dd532..af08ad1 (git diff empty); live verify_refs --unit AC1 '2 of 560 entries, 0 problems'; offline '560 entries, 0 problems'."
    ],
    "freshness_flags": [],
    "notes": [
        "Slice: course/modules/AC/AC1/index.html, L01.html, L02.html, L03.html, the three lab twins, and the L01-L03 cards of cards.json. Witness scripts: " + SCRIPT + " (W1-W6, python -I) and build_fragment_r10.py (this fragment), in ledgers/AC1/scripts/AC1-a-r10/.",
        "Not a project slice: no grader, no project.html; the 57 mutants in ledgers/AC1/mutants/ mutate grader/reference.py of the AC1-d project (their header says so) and are not re-run here. mutants: [] with that reason. Alternative correct implementations do not apply to lesson pages.",
        "Hours: hub split 90 lesson hours and 30 project hours; lesson hours L01 11, L02 12, L03 11 (34 h); L04-L08 11, 12, 12, 11, 10 (56 h); 34 + 56 = 90, matching the hub. Pace is a design target and was not graded.",
        "Full line-by-line re-read was limited to the round 10 delta, the changed sentences and every row that cites a changed line; the unchanged remainder of L01-L03 was carried from round 9 under the byte-identical rule. Not re-read in this round: the full lab output beyond the printed sections used by the rows, and the L04-L08 pages (other slices).",
        "The W3 interest-income witness of round 9 is re-expressed in the hypothesis of Proposition 3.2; no new mutant was written because the slice contains no grader.",
    ],
    "mutants": [],
    "summary": {"rows": len(rows), "pass": n_pass, "fail": n_fail, "unverifiable": 0},
    "verdict": "FAIL" if n_fail else "PASS",
    "rows": rows,
}
out = CHECKOUT / "ledgers/AC1/AC1-a.json"
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "pass", n_pass, "fail", n_fail)
