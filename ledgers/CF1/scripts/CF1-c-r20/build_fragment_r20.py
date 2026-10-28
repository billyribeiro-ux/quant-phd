"""Round 20 fragment builder for CF1 slice c (L05, L06, lab twins). Reads the round-19 fragment, re-verified rows are
replaced, carried rows keep their id and get the carry prefix. Run with the checkout's .venv python -I."""
import json
import sys

ck = "/tmp/verify20-CF1-c"
prev = json.load(open("/tmp/fanout-frags/CF1-c.round19.json", encoding="utf-8"))
CARRY = ("Carried from round 19 (course/modules/CF/CF1/L05.html, cards.json, index.html, references/, tools/ and "
         "tests/labs/CF1/ byte-identical since the previous pin 51fa336; L06.html changed only at lines 211 and 447, "
         "which this row does not cite):")

R = {}
def put(i, check, location, status, evidence):
    R[i] = dict(id=i, check=check, location=location, status=status, evidence=evidence)

OUT = "ledgers/CF1/scripts/CF1-c-r20/out"
put("CF1-c-cmd-pin", "2.5-labs", "git rev-parse HEAD and git status in /tmp/verify20-CF1-c (detached)", "PASS",
    "git rev-parse HEAD = fd9a9b72f000e509f3af78babf970cd4c9a847e4; git status: only untracked .venv (symlink) and "
    "ledgers/CF1/scripts/CF1-c-r20/ (this round's scripts)")
put("CF1-c-cmd-check_pages", "2.9-structure", "tools/check_pages.py --all", "PASS",
    "Re-run: 'check_pages AC4: PASS', 'check_pages CF1: PASS', 'check_pages AP1: PASS', exit 0 (ledgers/CF1/scripts/CF1-c-r20/out/cmds_r20.out)")
put("CF1-c-cmd-check_dag", "DAG", "tools/check_dag.py --all", "PASS",
    "Re-run: 'check_dag CF1: PASS' (also AC2, AC4, AP1 PASS) (out/cmds_r20.out)")
put("CF1-c-cmd-run_labs", "2.5-labs", "tools/run_labs.py --unit CF1", "PASS",
    "Re-run: 'run_labs CF1: PASS (9/9)' (out/cmds_r20.out)")
put("CF1-c-cmd-page_smoke", "2.5-labs", "tools/page_smoke.py --unit CF1 --pages L05 L06", "PASS",
    "Re-run: 'page_smoke modules/CF/CF1/L05.html: PASS' (lab 0.0 s), 'page_smoke modules/CF/CF1/L06.html: PASS' (lab-CF1-L06-1 0.3 s), 'page_smoke CF1: PASS' (out/smoke_pytest_r20.out); under 10 s")
put("CF1-c-cmd-ruff-mypy-labs", "2.9-structure", "ruff check and ruff format --check on the two twins; mypy --no-incremental on the two twins", "PASS",
    "Re-run: 'All checks passed!' and '2 files already formatted' (out/cmds_r20.out); 'Success: no issues found in 2 source files' (out/mypy_labs_r20.out)")
put("CF1-c-cmd-pytest-labs", "2.5-labs", "pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_docs_figures.py", "PASS",
    "Re-run: exit 0, all dots, no failures (out/pytest_labs_r20.out)")
put("CF1-c-cmd-verify_refs", "2.1-citations", "tools/verify_refs.py --offline; tools/verify_refs.py --unit CF1", "PASS",
    "Re-run: 'offline integrity: 560 entries, 0 problems' (out/cmds_r20.out); 'live re-verification of CF1: 2 of 560 entries, 0 problems', exit 0 (out/verify_refs_live_CF1.out)")
put("CF1-c-cmd-twin-vs-page", "2.5-labs", "ledgers/CF1/scripts/CF1-c-r14/twin_vs_page.py /tmp/verify20-CF1-c (run under python -I)", "PASS",
    "Re-run: rc 0; both twins 'expected identical to twin output: True' and 'code identical (ignoring one trailing newline): True' (out/twin_vs_page_r20.out); strict byte identity False by one trailing newline, as in round 19")
put("CF1-c-twin-freshness", "2.5-labs", "tests/labs/CF1/lab-CF1-L05-1.py and lab-CF1-L06-1.py", "PASS",
    "Twins byte-identical to 51fa336 (git diff --quiet 51fa336 fd9a9b7 -- tests/labs/CF1 exit 0); twin_vs_page re-run PASS (CF1-c-cmd-twin-vs-page)")
put("CF1-c-lab-L05-1-run", "2.5-labs", "tests/labs/CF1/lab-CF1-L05-1.py under python -I -W error", "PASS",
    "Re-run: exit 0 (rc5=0)")
put("CF1-c-lab-L06-1-run", "2.5-labs", "tests/labs/CF1/lab-CF1-L06-1.py under python -I -W error", "PASS",
    "Re-run: exit 0 (rc6=0); output saved to ledgers/CF1/scripts/CF1-c-r20/out/recompute_l06_r20.out for comparison")
put("CF1-c-cmd-mutants-na-r13", "2.7-mutants", "ledgers/CF1/mutants/ (project-slice mutants)", "PASS",
    "Not slice c's subject: slice c has no project grader (architect ruling: mutation testing applies to project graders only). The ledgers/CF1/mutants/ directory changed in this delta (16 files, slice d's round); slice d re-checks it")
put("CF1-c-num-L06-s3-quantile-unrounded", "2.2-numbers", "L06.html Section 3 paragraph (line 211, changed) and misconception 2 (line 244, unchanged)", "PASS",
    "Re-verified this round against the changed sentence. Lab code (tests/labs/CF1/lab-CF1-L06-1.py) computes quantiles unrounded (quantile() returns float, lines 43-46) and prints .2f (line 76). Re-run recompute (ledgers/CF1/scripts/CF1-c-r20/recompute_l06_r20.py, out/recompute_l06_r20.out): q10 14896.623057, q90 143406.126569, difference 128509.503511 -> 128509.50 at two decimals; printed difference 143406.13 - 14896.62 = 128509.51; gap 0.0065 equals the sum of the two rounding errors (printed q10 is 0.003057 below unrounded, printed q90 is 0.003431 above). Printed output lines 202-204 contain no unrounded value. Sentence '(a re-run of the code of Lab 1, with the printing step left out, not a line of its output)' is accurate: the recompute uses the lab's own functions with print removed")
put("CF1-c-r19-L06-line211-twin-term", "2.9-structure", "L06.html line 211", "PASS",
    "Round-19 FAIL fixed: 'twin' now appears 0 times in L05.html and L06.html (grep -c -i twin = 0 for both); line 211 now reads 're-run of the code of Lab 1, with the printing step left out'. Re-verified numbers (CF1-c-num-L06-s3-quantile-unrounded)")
put("CF1-c-prose-process-path", "2.9-structure", "L05.html and L06.html learner text", "PASS",
    "ledgers/CF1/scripts/CF1-c-r16/banned_scan_r16.py run -I on both pages: 'L05.html hits 0', 'L06.html hits 0' (out/banned_scan_r20.out). 'twin' count 0 in both pages (grep). Round-19 FAIL was the term 'twin' at line 211, now removed")
put("CF1-c-delta-L06-line211-given-model", "2.9-structure", "L06.html line 211", "PASS",
    "grep -c 'given the model' L06.html = 0; line 211 contains no 'given the model' (re-verified after the wording change)")
put("CF1-c-r16-L06-line66-share-se-binomial", "2.2-numbers", "L06.html line 66 and Section 3 line 211; lab-CF1-L06-1.py line 78", "PASS",
    "Re-verified: lab line 78 'se_negative = math.sqrt(negative * (1.0 - negative) / N_MAX)' is the binomial formula at the estimated p; output 'share_npv_below_zero 0.0552 se 0.0010' (out/lab_L06 run, recompute_l06_r20.out: count 2761, p 0.05522, se 0.0010215 -> 0.0010). Line 211 SE sentence 'standard error of 0.0010 from the binomial formula at the estimated p' matches")
put("CF1-c-struct-L06", "2.9-structure", "course/modules/CF/CF1/L06.html whole page (changed lines 211 and 447 this round)", "PASS",
    "git diff 51fa336 fd9a9b7 -- L06.html: two hunks (line 211 paragraph; quiz item explain at line 447), no structural change. check_pages CF1 PASS, page_smoke L06 PASS (out/cmds_r20.out, out/smoke_pytest_r20.out); banned scan 0 hits")
put("CF1-c-delta-cross-slice-notes", "2.7-cards", "cards.json CF1-c054, c056, c058, c060, c094 (L04); project.html line 192 test count", "PASS",
    "Scoped to slice c. (a) cards.json and L04.html byte-identical since 51fa336 (git diff --stat empty), so the five L04 cards carry. (b) project.html line 192 says 'collects 157 checks'; re-run: copying grader/test_project.py as capbudget.py (reference.py) plus instance.py, pytest --collect-only gives '157 tests collected' (out/collect_project_r20.out). The project.html C2 annotation sentence (line 189-192 hunk) is in slice d's subject and is not verified here (see notes)")
put("CF1-c-r20-L06-line211-recompute", "2.2-numbers", "L06.html line 211 (changed this round)", "PASS",
    "Re-run recompute_l06_r20.py: quantiles 14896.623057 / 79457.938852 / 143406.126569; diff 128509.503511; printed diff 128509.51; gap 0.0065 = 0.003057 + 0.003431 rounding. Lab twin unchanged, exit 0")
put("CF1-c-r20-L06-quiz-se-explain", "2.2-numbers", "L06.html line 447 (explain of the numeric item for the SE of the negative share, data-answer 0.0010, changed this round)", "PASS",
    "Explain now: 'the lab prints se 0.0010 from sqrt(p(1-p)/n) at the estimated p, which is 2761/50000 = 0.05522 unrounded and which the lab prints as 0.0552 (E2)'. Recompute: negative-draw count 2761 of 50000 (recompute_l06_r20.out 'neg count 2761'), 2761/50000 = 0.05522; lab line 79 prints .4f -> 0.0552. sqrt(0.05522*0.94478/50000) = 0.0010215 -> 0.0010 (tolerance 0.00005 consistent). The count 2761 is not printed by the lab and the page does not claim it is")
put("CF1-c-r20-lab-mutants-rerun", "2.5-labs", "ledgers/CF1/scripts/CF1-c-r17/mutants/ (5) and ledgers/CF1/scripts/CF1-c-r18/mutants/ (12 incl. 3 alternatives), run by ledgers/CF1/scripts/CF1-c-r20/run_lab_mutants_r20.sh", "PASS",
    "All 17 re-run under python -I -W error against the current twins (out/lab_mutants_r20.out). 12 differ from baseline output (r18_L05_03 exits 1 with ZeroDivisionError; others exit 0 with different printed output). Equivalent on the printed output, both exit 0: c17_L06_04_share_counts_zero_npv_as_negative and r18_L06_10_share_uses_pstdev_style_se. Alternatives alt_r18_a/b/c identical output (not over-constrained). Per the architect ruling, a mutated twin that exits 0 is not a finding unless a lesson sentence claims the lab checks that property; no L05/L06 sentence claims the lab asserts or checks the SE or share implementation")
put("CF1-c-r20-project-count-157", "2.7-cards", "project.html line 192 'collects 157 checks'", "PASS",
    "pytest --collect-only on the reference-copied grader gives 157 tests (out/collect_project_r20.out); page says 157. Count matches. Subject is slice d's file, recorded here because the round-19 cross-slice row cited it")
put("CF1-c-r20-new-mutants-na", "2.7-mutants", "slice c mutation scope", "PASS",
    "Not required for slice c: the 'at least 3 new mutants' rule applies to project slices, and slice c holds lab twins, which are demonstrations and not mutation-tested (architect ruling on lab mutants). No new project grader in slice c. The 17 lab mutants and alternatives were all re-run (CF1-c-r20-lab-mutants-rerun)")

rows = []
for r in prev["rows"]:
    i = r["id"]
    if i in R:
        rows.append(R[i])
    elif r["status"] == "PASS":
        rows.append(dict(r, evidence=CARRY + " " + r["evidence"]))
    else:
        raise SystemExit("unhandled non-PASS row " + i)
seen = {r["id"] for r in rows}
for i, r in R.items():
    if i not in seen:
        rows.append(r)

mutants = []
for m in prev["mutants"]:
    mutants.append(m)
mutants.append({"id": "c17_L06_04_share_counts_zero_npv_as_negative", "file": "ledgers/CF1/scripts/CF1-c-r17/mutants/c17_L06_04_share_counts_zero_npv_as_negative.py",
                "description": "Share of negative NPVs counts zero as negative; EQUIVALENT on the printed output of seed 6 (no zero NPV draws), re-run round 20 'same-output'", "killed_by": "none on displayed output (equivalent, exits 0)"})
mutants.append({"id": "r18_L06_10_share_uses_pstdev_style_se", "file": "ledgers/CF1/scripts/CF1-c-r18/mutants/r18_L06_10_share_uses_pstdev_style_se.py",
                "description": "Share standard error uses a different constant; EQUIVALENT on the printed output (round 20 'same-output')", "killed_by": "none on displayed output (equivalent, exits 0)"})
seen_m = set(); uniq = []
for m in mutants:
    if m["id"] not in seen_m:
        seen_m.add(m["id"]); uniq.append(m)

verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
frag = {
    "unit": "CF1", "slice": "CF1-c", "round": 20, "verifier": "Haiku 5.5 independent verifier (round 20)",
    "pin": "fd9a9b72f000e509f3af78babf970cd4c9a847e4",
    "base": "51fa33616cf2a2ef40ec58634d40f67f78aa668c (round 19 pin; previous rows carried only where the cited subject is byte-identical)",
    "checkout": ck, "scratch": "/tmp/cf1-v/c20", "verified_at": "2026-10-28T12:00:00+00:00", "verdict": verdict,
    "rows": rows, "mutants": uniq, "registry_flags": [], "freshness_flags": [],
    "notes": [
        "Delta since 51fa336 for slice c: L06.html line 211 (wording: 'twin' replaced by 'the code of Lab 1, with the printing step left out') and the numeric quiz item explain at line 447 (adds 2761/50000 = 0.05522). L05.html, cards.json, index.html, references, tools, tests/labs/CF1 are byte-identical to 51fa336 (git diff --quiet).",
        "Round-19 FAIL rows CF1-c-prose-process-path and CF1-c-r19-L06-line211-twin-term are re-verified and PASS: 'twin' no longer appears in L05 or L06 learner text.",
        "Numbers in line 211 and line 447 recomputed independently from the lab code (recompute_l06_r20.py): quantiles, 128509.5035, gap 0.0065, count 2761, se 0.0010.",
        "Lab mutants: 17 re-run; 2 equivalent on displayed output (c17_L06_04, r18_L06_10); alternatives alt_r18_a/b/c identical output. No new lab mutants: slice c has no project grader, and lab twins are not mutation-tested (architect ruling).",
        "project.html C2 annotation sentence (line 189-192 hunk, 'each flow from year 1 includes the shield') and the new grader tests (test_project.py +29 lines) are slice d's subject and were not verified here. Only the collect count 157 was checked, because the cross-slice row cited it.",
        "Hours: data-hours=8 on L05 and L06 unchanged; not re-estimated (architect ruling).",
        "Repository-wide ruff/mypy runs and the full gate were not run: only the commands for slice c's pages and twins. Live verify_refs was run for CF1 (2 entries, 0 problems)."
    ],
    "summary": ("Slice c round 20: verdict " + verdict + ". Previous FAILs (twin wording at L06 line 211 and process-path) fixed and re-verified. "
                "Changed sentences: line 211 numbers and re-run claim verified; line 447 SE explain verified. All other rows carried by byte-identity or re-run. "
                "Lab twin mutants re-run: 12 differ, 2 equivalent, alternatives identical. Not verified in this slice: project.html C2 sentence and grader tests (slice d).")
}
json.dump(frag, open(f"{ck}/ledgers/CF1/CF1-c.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("rows", len(rows), "verdict", verdict, "nonpass", [r["id"] for r in rows if r["status"] != "PASS"])
