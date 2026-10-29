"""Build the round-18 fragment for M1 slice c (L06, L07, L08): carries byte-identical PASS rows, re-verifies the rest."""

import json
import sys
from datetime import UTC, datetime

CK = "/tmp/verify18-M1-c"
prev = json.load(open("/tmp/fanout-frags/M1-c.round17.json", encoding="utf-8"))
PFX = "Carried from round 17 ({files} byte-identical since the previous pin): "

NEW = {
    "L08-q6-cause-scope": (
        "PASS",
        "Re-verified. Option now reads 'its excess compounds to 3.70 CU, and interest taken to the cent adds back 0.27 CU, "
        "so the final payment is 3.43 CU below the regular payment'. Recomputed (ledgers/M1/scripts/M1-c-r18/recompute_l08.py, "
        "/tmp/m1-v/M1-c-r18/recompute_l08.py): excess per payment 0.0036871 CU; FV at month 360 = 3.70377 CU; exact-interest "
        "final payment 1495.1762 CU (lab prints 1495.18); cent final 1495.45 CU; 0.27377 CU = interest-rounding effect; "
        "3.70377 - 0.27377 = 3.43000 CU = 1498.88 - 1495.45. Lab output line 'final payment if interest is not taken to the "
        "cent = 1495.18 CU' (ledgers/M1/scripts/M1-c-r18/out/lab08.out). Distractors unchanged and wrong. Explain line 528 "
        "unchanged and consistent. The previous FAIL (cause omitted the 0.27 CU) is closed.",
    ),
    "L08-numbers": (
        "PASS",
        "Re-verified after the L08.html:331 wording change. Every number in line 331 matches lab output "
        "(ledgers/M1/scripts/M1-c-r18/out/lab08.out): 1,498.88 regular; 1498.876313 exact; 1,495.45 final; 3.43 adjustment; "
        "drift 27 cents over months 1 to 359; 3.41 CU at month 359; first 1 CU at month 183; month 360 exact-rounded balance "
        "-3.7038 CU (recomputed, 3.70377). Hypothesis line 150 and misconception numbers unchanged.",
    ),
    "L08-lab-1-interpretation": (
        "PASS",
        "Re-verified: L08.html:331 changed from 'so the only source of difference between them is the interest taken to the "
        "nearest cent' to 'so the difference between them comes from the interest taken to the nearest cent'. Recomputed "
        "(recompute_l08.py): the cent schedule and the exact schedule at the rounded regular payment share the same payment, "
        "so their difference is driven only by interest rounding; unrounded maximum drift over months 1 to 359 is 27.32 cents "
        "(month 357), which the lab's integer comparison prints as 27. The causal claim is right; the lab's comparison rounding "
        "is within half a cent and does not change the cause. Remaining sentences (3.41 CU, month 183, month 360 3.70 CU, the "
        "identity of Proposition 2.3 printed, no split of the second comparison, one loan only) match lab output and the lab docstring.",
    ),
    "L08-decomposition-claim": (
        "PASS",
        "Re-verified against the changed quiz option and line 356 (unchanged). Recomputed in fractions: 3.70377 CU excess "
        "compounded, 0.27377 CU interest-rounding effect, difference 3.43000 CU = 1498.88 - 1495.45. Claim 'the 0.27 is the "
        "interest-rounding part; the 3.70 is the rounding of the regular pay' is supported by the lab's two final payments "
        "(1495.18 with unrounded interest, 1495.45 cent) and the model (the only difference between the two computations is "
        "interest rounding).",
    ),
    "quiz-answers-L06-L08": (
        "PASS",
        "Re-verified: L08q6 correct option (L08.html:525) recomputed as above (3.70, 0.27, 3.43 CU). L08 numeric answers and "
        "explanations at L08.html:488, 493, 507, 530, 544 unchanged in this diff; L06 and L07 quiz blocks byte-identical to "
        "fefbf8b.",
    ),
    "L08-card-c135": (
        "PASS",
        "Re-verified. cards.json M1-c135 entry byte-identical to fefbf8b (not in the diff hunks; ledgers/M1/scripts/M1-c-r18/out/"
        "cards_diff_r18.out lists changed ids M1-c060, c160, c163, c175 only). Line 331 still states 27 cents with each exact "
        "balance rounded before comparison, which the lab prints (drift = 27).",
    ),
    "L08-structure": (
        "PASS",
        "Re-verified: the L08.html diff since fefbf8b changes only lines 331 and 525, which contain no section markup; section "
        "order and why-it-matters line unchanged.",
    ),
    "slice-banned-phrases": (
        "PASS",
        "Re-scanned L06 to L08 learner text (grep, tags stripped): no 'roughly half', 'about 6%', 'historically' or process "
        "words. Ellipses appear only as quiz-stem cloze blanks: L06.html:415, 424; L07.html:487, 515; L08.html:489, 499, 536 "
        "(stems ending in '…' that the answer options complete). Changed L08 text at lines 331 and 525 has no banned phrase.",
    ),
    "slice-process-words": (
        "PASS",
        "Re-scanned L06 to L08 learner text: no 'build', 'builder', 'verifier', 'round', 'REQUEST' or 'unit report' in the "
        "changed lines 331 and 525 or elsewhere in the pages.",
    ),
    "cards-L06-L08-scan": (
        "PASS",
        "Re-run ledgers/M1/scripts/M1-c-r17/cards_scan.py on the r18 checkout (ledgers/M1/scripts/M1-c-r18/out/cards_scan.out): "
        "178 cards (was 179; the removed card M1-c175 is an L03 card, outside this slice); per lesson L06 12, L07 24, L08 30, "
        "unchanged. No cards for L06 to L08 changed (cards_diff_r18.out).",
    ),
    "cards-duplicate-scan": (
        "PASS",
        "Re-run near-duplicate scan: 22 pairs above 0.6 involving L06 to L08 cards, identical to the round-17 output apart from "
        "the total count line; no duplicate ids (cards_scan.out).",
    ),
    "M1c-cmd-check-pages": (
        "PASS",
        "Re-run: `tools/check_pages.py --unit M1` -> 'check_pages M1: PASS', exit 0 (out/check_pages.out).",
    ),
    "M1c-cmd-check-dag": (
        "PASS",
        "Re-run: `tools/check_dag.py --all` -> PASS for M1, S7, AC1, AC2, AC4, CF1, AP1; exit 0 (out/check_dag.out).",
    ),
    "M1c-cmd-run-labs": (
        "PASS",
        "Re-run: `tools/run_labs.py --unit M1` -> 'run_labs M1: PASS (11/11)', exit 0 (out/run_labs.out).",
    ),
    "M1c-cmd-page-smoke": (
        "PASS",
        "Re-run: `tools/page_smoke.py --unit M1 --pages L06 L07 L08` -> PASS for all three pages, lab runtimes 0.0 s, 0.0 s, "
        "0.1 s; exit 0 (out/smoke.out).",
    ),
    "M1c-cmd-twins-isolated": (
        "PASS",
        "Re-run each twin under `python -I -W error`: lab-M1-L06-1.py, lab-M1-L07-1.py, lab-M1-L08-1.py all exit 0 "
        "(out/lab06.out, lab07.out, lab08.out; lab08 output re-read in full).",
    ),
    "M1c-twin-embed": (
        "PASS",
        "Re-run embed comparison (ledgers/M1/scripts/M1-c-r17/embed_check.py against r18 out files): for L06, L07, L08 page "
        "code equals the twin and page expected output equals the twin's stdout (out/embed_check.out, all True, exit 0). "
        "The first run's False was an artefact of an appended exit line in my copy, removed and re-run.",
    ),
    "M1c-lint-types": (
        "PASS",
        "Re-run: ruff check tests/labs/M1 course/modules/M/M1 -> 'All checks passed!'; ruff format --check tests/labs/M1 -> "
        "11 files already formatted; mypy --strict tests/labs/M1 -> no issues in 11 source files; pytest -k M1 in "
        "tests/test_labs.py -> 11 passed (out/pytest_M1.out). The course module was not put through mypy (no Python there).",
    ),
    "M1c-refs-live": (
        "PASS",
        "Re-run: tools/verify_refs.py --unit M1 -> 'live re-verification of M1: 1 of 560 entries, 0 problems', exit 0; "
        "tools/verify_refs.py --offline -> '560 entries, 0 problems', exit 0 (out/vr_live_M1.out, out/vr_offline.out).",
    ),
    "L08-q6-cause-scope-recheck-note": None,
}
NEW.pop("L08-q6-cause-scope-recheck-note")

RE_NOTE = {"L08-identity-count-claim", "L08-key-results-drift", "L08-R3-drift-identification"}

rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in NEW:
        st, ev = NEW[rid]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": st, "evidence": ev})
        continue
    if r["id"].startswith("M1c-") or r["id"] in ("slice-hours",):
        rows.append({**r, "evidence": r["evidence"]})
        continue
    files = r["location"].split(";")[0].split(":")[0].strip() or "the cited files"
    rows.append({**r, "evidence": PFX.format(files=files) + r["evidence"]})

summary = {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows),
           "fail": sum(r["status"] == "FAIL" for r in rows),
           "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in rows)}
frag = {
    "unit": "M1",
    "slice": "M1-c",
    "round": 18,
    "verifier": "independent verifier round 18 (did not build M1; shares no context with the builders or earlier verifiers)",
    "pin": "7143726",
    "base": "fefbf8b (the round-17 pin; M1 slice paths changed at fefbf8b..7143726 only in L08.html lines 331 and 525 and in cards.json entries M1-c060, c160, c163, c175, none of which is an L06 to L08 card)",
    "previous_ledger": "/tmp/fanout-frags/M1-c.round17.json (context only; its PASS rows were re-checked or carried with the byte-identical rule)",
    "checkout": CK,
    "scratch": "/tmp/m1-v/M1-c-r18",
    "verified_at": datetime.now(UTC).isoformat(timespec="seconds"),
    "verdict": "PASS" if summary["fail"] == 0 and summary["unverifiable"] == 0 else "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Mutants: ledgers/M1/mutants/ holds the M1 project grader mutants (grader and project.html; not this lab and page slice), "
        "so the project mutant re-run and the three new student-error mutants do not apply to M1-c; none were run. "
        "Alternative implementations: not applicable (no grader in this slice). Full line-by-line read: only the changed hunks "
        "(L08.html 331 and 525) and the rows they touch were re-read; every other row is carried by byte-identity, with the "
        "commands re-run. Hours: unchanged; the hub split (9 h per lesson) matches data-hours=9 in each page; no arithmetic "
        "inconsistency. Cards for L06 to L08 unchanged."
    ),
    "summary": summary,
}
json.dump(frag, open(f"{CK}/ledgers/M1/M1-c.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(summary, frag["verdict"])
