"""Builds ledgers/AC2/L05-L06.json (round 8) from the round-7 fragment; run with -I from the checkout."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
R7 = Path("/tmp/ac2-frags/L05-L06.round7.json")
OUT = ROOT / "ledgers" / "AC2" / "L05-L06.json"
FILES = ("course/modules/AC/AC2/L05.html, course/modules/AC/AC2/L06.html, tests/labs/AC2/lab-AC2-L05-1.py, "
         "tests/labs/AC2/lab-AC2-L06-1.py, references/references.json")
CARDS_NOTE = "cards.json records byte-identical (the file changed only at AC2-c024, c072 and c107)"

# Re-verified this round: subject changed, or the subject names index.html / cards.json as a whole, or a command row.
REVERIFIED = {
    "L05-L06-cmd-pin": ("PASS", "Re-verified at e6788c2: L05.html, L06.html, both labs and references/references.json are byte-identical to 6adfd01 (git diff --quiet, empty); cards.json parses to 140 records, sequential ids AC2-c001..c140, no duplicate ids, fronts or backs (script recompute.py). Location: repository"),
    "L05-L06-cmd-check-pages": ("PASS", "Re-run this round: tools/check_pages.py --unit AC2 --page L05 -> 'check_pages AC2 L05: PASS' (exit 0); --page L06 -> 'check_pages AC2 L06: PASS' (exit 0)."),
    "L05-L06-cmd-check-dag": ("PASS", "Re-run this round: tools/check_dag.py --unit AC2 -> 'check_dag AC2: PASS' (exit 0)."),
    "L05-L06-cmd-run-labs": ("PASS", "Re-run this round: tools/run_labs.py --unit AC2 -> 'run_labs AC2: PASS (11/11)'; pytest tests/test_labs.py -k AC2 -> 11 passed."),
    "L05-L06-cmd-twins-isolated": ("PASS", "Re-run this round: .venv/bin/python -I -W error tests/labs/AC2/lab-AC2-L05-1.py -> exit 0, 19 output lines (scripts/L05-L06-r8/L05-1.out); lab-AC2-L06-1.py -> exit 0, 39 lines (scripts/L05-L06-r8/L06-1.out). Printed values match the page: mean spread 0.00219, expected_t_at_planted 2.164, null FP 0.060, power 0.590; L06 strong TPR 0.9850, weak TPR 0.3550, flags_only 6/6, se 0.2781 and 0.0489."),
    "L05-L06-cmd-page-smoke": ("PASS", "Re-run this round: tools/page_smoke.py --unit AC2 --pages L05 L06 -> 'page_smoke modules/AC/AC2/L05.html: PASS' (lab-AC2-L05-1 3.0 s), 'page_smoke modules/AC/AC2/L06.html: PASS' (lab-AC2-L06-1 0.1 s), 'page_smoke AC2: PASS'."),
    "L05-L06-cmd-verify-refs-unit": ("PASS", "Re-run this round: tools/verify_refs.py --unit AC2 -> 'live re-verification of AC2: 7 of 560 entries, 0 problems'."),
    "L05-L06-cmd-verify-refs-offline": ("PASS", "Re-run this round: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems'."),
    "L05-L06-cmd-lint": ("PASS", "Re-run this round: .venv/bin/python -m ruff check tests/labs/AC2/lab-AC2-L05-1.py tests/labs/AC2/lab-AC2-L06-1.py -> 'All checks passed!'; ruff format --check -> '2 files already formatted'."),
    "L05-L06-card-L05-lab": ("PASS", "Re-verified this round because the subject includes AC2-c072 (changed). c072 back now reads 'The lesson states no finding of Sloan (1996)': L05.html line 61 says 'The lesson states no finding of that paper', line 111 and the lab docstring say it 'does not reproduce Sloan (1996)'. c069 (0.00219 vs 0.00223, 200 seeds), c070 (0.060; SE sqrt(0.05*0.95/200)=0.0154), c071 (0.590), c073 (seed 0 spread 0.00075, t 0.676), c074, c122 (-2.7937), c123 (2.164; 0.00223495/(0.0113137/sqrt 120)=2.16398; displayed-SD quotient 2.1647) and c075 (201.13 months) all match scripts/L05-L06-r8/L05-1.out and recompute.out."),
    "L05-L06-cards-dup-scan": ("PASS", "Re-run this round on cards.json (changed file): 140 records, ids unique and sequential, 0 duplicate fronts, 0 duplicate backs (scripts/L05-L06-r8/recompute.py output)."),
    "L05-L06-cards-coverage": ("PASS", "Re-run this round: L05 cards c063-c075, c122, c123 (15 records); L06 cards c076-c088, c124, c125, c128, c138 (17 records); every slice card carries lesson L05 or L06. c138 matches L06 Definition 1.2 (line 64-65: TA/A(t-1) = NDA + DA). c128 matches L06.html line 61 (the Crossref-abstract claim about the paper) and states no power figure, as L06.html line 499 does."),
    "L05-L06-struct-hours": ("PASS", "Re-run this round: index.html data-hours-lessons=76 and data-hours-project=34 (sum 110 = tier U 110 h); hub card kickers 9+10+8+9+8+10+10+12 = 76; L05.html data-hours=8 and L06.html data-hours=10 match their hub cards. The +/-30% judgement of each lesson's hours is carried from round 7; the L05 and L06 bodies are byte-identical."),
    "L05-L06-prose-jargon": ("PASS", "Re-checked this round on the changed texts: the new L05 hub title 'The Accruals Anomaly and the Sloan (1996) Question' and the c072 back contain no banned string (BUILDER_RULES 1.2/1.3 list grepped: 'roughly half', 'about 6%', 'historically'). L05.html and L06.html prose is byte-identical and carried."),
    "L05-L06-r2-attribution-sweep": ("PASS", "Re-checked this round: the changed hub L05 card now names Sloan (1996) only as 'the question Sloan (1996) asks', which matches L05.html section 3 ('The question Sloan (1996) asks, in the form given in Section 1'). No card or hub text attributes the anomaly's label to Sloan. Other named sources unchanged and carried."),
    "L05-L06-r7-L06-s1-dechow-attribution": ("PASS", "Re-run this round: curl https://api.crossref.org/works/10.2308/tar-9505096112 -> HTTP 200, title 'Detecting Earnings Management.', abstract 'Evaluates alternative accrual-based models for detecting earnings management. Comparison of the specification and power of commonly used test statistics' (scripts/L05-L06-r8/10.2308_tar-9505096112.json). L06.html line 61 matches; the page names no authors; index.html L06 card line 149 byte-identical to 6adfd01."),
    "L05-L06-r7-hub-L05-title": ("PASS", "Previous FAIL re-verified and fixed in e6788c2. index.html line 148 now reads 'The Accruals Anomaly and the Sloan (1996) Question' (the old 'The Accruals Anomaly (Sloan 1996)' is gone). L05.html section 3 line 228 uses 'The question Sloan (1996) asks', and the title attributes no anomaly label. curl https://api.crossref.org/works/10.2308/tar-9608042309 -> HTTP 200, title 'Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?', abstract 'Investigates whether stock prices reflect information about future corporate earnings contained in accrual and cash flow components' (scripts/L05-L06-r8/10.2308_tar-9608042309.json). The L05 h1 is unchanged. Location: course/modules/AC/AC2/index.html line 148"),
}

NEW = [
    {
        "id": "L05-L06-r8-c072-sloan-claim",
        "check": "2.7-cards",
        "location": "course/modules/AC/AC2/cards.json AC2-c072 (changed in e6788c2); L05.html line 61, line 111, lab docstring",
        "status": "PASS",
        "evidence": "New subject. c072 front 'True or false: Lab 1 reproduces Sloan (1996).' and back 'False. ... The lesson states no finding of Sloan (1996).' The lesson contains no finding of Sloan: L05.html line 61 gives only the question Sloan asks (Crossref abstract wording) and states 'The lesson states no finding of that paper'; line 235 says 'states no finding from either'. The lab docstring (line 111 area) says the lab 'does not reproduce Sloan (1996)'. The c072 back's claim that the lab gives no evidence about real returns matches the docstring 'It says nothing about the size of the accruals effect in real stock returns'. Scripts: L05-L06-r8/recompute.out."
    },
    {
        "id": "L05-L06-r8-access-dechow-doi",
        "check": "2.1-citations",
        "location": "plans/AC2-open-items.md line 24 (dechow1995detecting access statement)",
        "status": "PASS",
        "evidence": "Access statement 'plain curl to the publisher page for DOI 10.2308/tar-9505096112 returned HTTP 403' reproduced with plain curl, no bypass: curl -s -o /dev/null -w '%{http_code}' https://doi.org/10.2308/tar-9505096112 -> HTTP 302 to https://publications.aaahq.org/accounting-review/article/70/2/193/18940/Detecting-Earnings-Management; curl of that landing URL -> HTTP 403. The statement is consistent with the reproduced status; the paper body is not read, which the open-items row says."
    },
    {
        "id": "L05-L06-r8-card-arithmetic",
        "check": "2.2-numbers",
        "location": "course/modules/AC/AC2/cards.json AC2-c070, c071, c073, c075, c082, c084, c085, c086, c122, c123, c124, c125; L05.html Prop 2.3 (quintile gap)",
        "status": "PASS",
        "evidence": "Recomputed this round in scripts/L05-L06-r8/recompute.py (output recompute.out): quotient 0.00223495/(0.0113137/sqrt(120)) = 2.16398 -> 2.164; displayed-SD quotient 2.1647; n for 80% power = 201.13 -> about 201; quintile gap -2*phi(q)/0.2 = -2.7996 -> -2.800; L06 flags 0.355*200 = 71 and 0.985*200 = 197; SE of a rate from 200 draws sqrt(0.05*0.95/200) = 0.0154; c125 0.2781*sqrt(1800/57600) = 0.0492 against the printed 0.0489, a 'roughly as the square root' remark that the card itself states."
    },
]

def main() -> int:
    frag = json.loads(R7.read_text(encoding="utf-8"))
    rows = []
    for r in frag["rows"]:
        rid = r["id"]
        if rid in REVERIFIED:
            status, ev = REVERIFIED[rid]
            rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev})
        else:
            if r["status"] != "PASS":
                raise SystemExit(f"unexpected non-PASS carried row {rid}")
            prior = r["evidence"].split("Location:")[0].replace("Round 7 re-verified at 6adfd01 (not carried): ", "").strip()
            files = FILES + ("; " + CARDS_NOTE if "cards.json" in r["location"] else "")
            rows.append({
                "id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                "evidence": f"Carried from round 7 ({files} byte-identical since 6adfd01): {prior}",
            })
    rows.extend(NEW)
    ids = [r["id"] for r in frag["rows"]]
    assert all(i in {r["id"] for r in rows} for i in ids), "a previous row id was dropped"
    counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
    for r in rows:
        counts[r["status"]] += 1
    verdict = "PASS" if counts["PASS"] == len(rows) else "FAIL"
    out = {
        "unit": "AC2",
        "slice": "L05-L06",
        "round": 8,
        "verifier": "AC2 independent verifier, round 8, slice L05-L06 (fresh verifier; did not build AC2; shares no context with the builders or the rounds 1-7 verifiers)",
        "pin": "e6788c2",
        "base": "6adfd01",
        "checkout": "/tmp/verify-ac2r8-l56",
        "scratch": "/tmp/ac2-v/L05-L06-r8",
        "verified_at": "2026-10-27T00:00:00+00:00",
        "verdict": verdict,
        "registry_flags": frag["registry_flags"],
        "freshness_flags": [],
        "rows": rows,
        "mutants": [],
        "notes": frag["notes"] + [
            "Round 8 delta for the slice: cards.json AC2-c072 (back rewritten), index.html L05 hub card title (line 148). L05.html, L06.html, both labs and references.json are byte-identical to 6adfd01 (git diff --quiet).",
            "The round-7 FAIL row L05-L06-r7-hub-L05-title is PASS in this round after the e6788c2 title change.",
            "Carried rows keep their round-7 ids and are marked 'Carried from round 7'; every command row was re-run this round (see REVERIFIED evidence).",
        ],
        "summary": {
            "rows": len(rows),
            "pass": counts["PASS"],
            "fail": counts["FAIL"],
            "unverifiable": counts["UNVERIFIABLE"],
            "fail_ids": [r["id"] for r in rows if r["status"] == "FAIL"],
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("rows", len(rows), counts, verdict)
    return 0

if __name__ == "__main__":
    sys.exit(main())
