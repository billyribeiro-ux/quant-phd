"""Round-5 fragment builder for AC2 slice L01-L02 (reads the round-4 fragment for ids; writes ledgers/AC2/L01-L02.json)."""
import json
import sys

R4 = "/tmp/ac2-frags/L01-L02.round4.json"
OUT = sys.argv[1]
r4 = json.load(open(R4))

CARRY_HUB = "Carried from round 4 (course/modules/AC/AC2/index.html, course/modules/AC/AC2/L01.html, tests/labs/AC2/lab-AC2-L01-1.py, plans/, references/, course/assets/, tools/ byte-identical since 2607c60): "
CARRY_L02 = "Carried from round 4 (course/modules/AC/AC2/L02.html differs from 2607c60 only in four hunks, lines 87, 509/593, 653, 882; the sentence below is outside them and byte-identical; lab output re-run this round, 26 of 26 lines match the page): "

R5 = {
 "L02-definition-4-1": ("PASS", "R5 re-verified. Line 653 now says 'Three of these ratios use year-end balances' and names current ratio, debt to assets and DSO; gross margin 'uses no balance'. Code: current_ratio, debt_to_assets, days_sales_outstanding take period-end items (tests/labs/AC2/lab-AC2-L02-1.py lines 362-385); gross_margin takes revenue and cogs only (line 370). Round-4 FAIL resolved."),
 "L02-definition-4-1-note": ("PASS", "R5 re-verified. cards.json AC2-c134 (DSO: 'Year-end receivables over the fiscal year's revenue, times 365') and AC2-c135 (current ratio and debt to assets on year-end balances) and AC2-c136 (gross margin, no balance) match Definition 4.1 and the code. Round-4 FAIL resolved."),
 "L02-lab-header-gross-margin-basis": ("PASS", "R5 re-verified. Hypothesis (L02.html line 87) and printed header 'other ratios (SIMULATED): year-end balances, except gross margin, which uses only the year's flows' (twin line 509; page line 593) match the code. Output re-run: rc 0 under python -I -W error; header line identical in page and output. Round-4 FAIL resolved."),
 "L02-lab-output-recomputed": ("PASS", "R5 re-run: tests/labs/AC2/lab-AC2-L02-1.py rc 0 (python -I -W error); 26 of 26 output lines occur verbatim in L02.html (/tmp/ac2-v/l12/r5/L02.out). Scratch: ledgers/AC2/scripts/L01-L02-r5/r5_l02_check.py."),
 "L02-prose-numbers": ("PASS", "R5 recomputed (ledgers/AC2/scripts/L01-L02-r5/r5_l02_prose_numbers.py): 0.1179*0.8701*1.6936=0.17374 (prose 0.1737 in last digit); gap 0.1925/0.1820 = 5.77% (5.8%); log shares -0.2993, -0.3400, -0.0221, -0.0184; shares 88.1, 6.5, 5.4; E3 0.12*365=43.80; 120/900*365=48.67; 120/900*360=48.00; DSO 2022 restated 43.28. Carried for the sentences not re-computed this round."),
 "L02-example-4-2": ("PASS", "R5 re-verified: DSO 2022 = 135826937/1145473837*365 = 43.28; at the originally filed 1131.9 it is 43.80; receivables equal 0.12 x 1131.89 (generator, twin line 230 and 'filed revenue' at line 296, restatement factor 1.012 at line 296 of make_filer). The receivables figure carries no restatement, as the sentence says."),
 "L02-cards": ("PASS", "R5: 18 L02 cards read; c017-c031 unchanged in cards.json diff; c134-c136 re-verified against Definition 4.1 (see L02-definition-4-1-note)."),
 "L01-L02-cards-changed": ("PASS", "R5 read c014, c026, c031, c120 in full: texts unchanged in the cards.json diff since 2607c60 (hunks touch c059, c065, c103, c107, c119, c123, c130, c134 only) and each matches its lesson (c026 receivables on the originally filed revenue, 0.12 x 1131.89 consistent with the twin)."),
 "L01-L02-cards-c134-c136": ("PASS", "R5 re-read in full. c134 back changed to 'Year-end receivables over the fiscal year's revenue, times 365 ...' matches Definition 4.1 and code (days_sales_outstanding uses period-end receivables and revenue); c135 and c136 unchanged and match."),
 "L01-L02-verify-refs": ("PASS", "R5 re-run: tools/verify_refs.py --unit AC2 (live) 7 of 560 entries, 0 problems; tools/verify_refs.py --offline 560 entries, 0 problems."),
 "L01-L02-run-graders": ("PASS", "R5 re-run: tools/run_graders.py --unit AC2: PASS (reference 50/50 seeds)."),
 "L01-L02-check-pages-dag": ("PASS", "R5 re-run: check_pages --unit AC2 PASS; check_dag --unit AC2 PASS; check_projects --unit AC2 PASS."),
 "L01-L02-pagesmoke": ("PASS", "R5 re-run: tools/page_smoke.py --unit AC2 --pages L01 L02 index: PASS (L02 lab 0.0 s)."),
 "L01-L02-run-labs": ("PASS", "R5 re-run: run_labs --unit AC2 --page L01 PASS; --page L02 PASS (1/1)."),
 "L01-L02-twins-isolated": ("PASS", "R5 re-run: python -I -W error on lab-AC2-L01-1.py rc 0 and lab-AC2-L02-1.py rc 0."),
 "L01-L02-ruff-mypy-pytest": ("PASS", "R5 re-run: ruff check tests/labs/AC2 rc 0; ruff format --check (11 files) rc 0; mypy --no-incremental: no issues in 112 files; pytest -q -k 'AC2 or lab' rc 0."),
 "L01-L02-notation": ("PASS", "R5: notation unchanged in the slice hunks (Definition 4.1 uses the same \\(\\mathrm{Rev}\\), \\(\\mathrm{COGS}\\) symbols as before)."),
 "L01-L02-cards-duplicates": ("PASS", "R5 duplicate scan: cards.json has 140 cards, ids unique, no duplicate fronts."),
 "L01-L02-companyfacts-fetch": ("PASS", "Carried from round 4 (the SEC companyfacts file and the slice's data sources are unchanged since 2607c60; not re-fetched this round)."),
}
ADD = [
 {"id": "L02-definition-4-1-title", "check": "2.4 definitions / category label", "location": "course/modules/AC/AC2/L02.html line 652 (Definition 4.1 block title)", "status": "FAIL",
  "evidence": "The block title reads '(solvency and liquidity ratios)', but the block now defines four ratios of which gross margin (line 653) is a profitability ratio, and it is a margin measure, not a solvency or liquidity one. The label does not match the content.",
  "fix": "Retitle the span to '(solvency, liquidity and margin ratios)' or '(balance and margin ratios)'. Learner text only; no test checks the title."},
]

rows = []
for r in r4["rows"]:
    rid = r["id"]
    if rid in ("L02-definition-4-1", "L02-definition-4-1-note", "L02-lab-header-gross-margin-basis"):
        status, ev = R5[rid]
    elif rid in R5:
        status, ev = R5[rid]
    elif rid.startswith("L02-") or rid.startswith("L01-L02-hub") or rid.startswith("L01-L02-sec") or rid.startswith("L01-L02-data") or rid.startswith("L01-L02-hub"):
        status = r["status"]
        ev = (CARRY_L02 if rid.startswith("L02-") and rid not in ("L02-hours",) else CARRY_HUB) + r["evidence"]
    else:
        status = r["status"]
        ev = CARRY_HUB + r["evidence"]
    if rid in R5:
        ev = R5[rid][1]
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev})
rows.extend(ADD)

frag = {
 "unit": "AC2",
 "slice": "L01-L02",
 "round": 5,
 "verifier": "independent round-5 verifier for AC2 slice L01-L02 (fresh context; round-4 fragment used as context only; every changed subject re-verified)",
 "pin": "11b3477",
 "base": "2607c60",
 "checkout": "/tmp/verify-ac2r5-l12 (detached at 11b3477)",
 "scratch": "/tmp/ac2-v/l12/r5",
 "verified_at": "2026-10-27T00:00:00+00:00",
 "verdict": "FAIL" if any(x["status"] != "PASS" for x in rows) else "PASS",
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
  "Round 5 delta 2607c60..11b3477 for this slice: L02.html (four hunks: hypothesis line 87, lab header line 509/593, Definition 4.1 line 653, quiz explanation line 882), tests/labs/AC2/lab-AC2-L02-1.py (one print line), cards.json (c134 changed; c059, c065, c103, c107, c119, c123, c130 are other lessons). index.html, L01.html and the L01 twin are byte-identical since 2607c60.",
  "All three round-4 FAIL rows (L02-definition-4-1, L02-definition-4-1-note, L02-lab-header-gross-margin-basis) are fixed and PASS; ids kept.",
  "New FAIL: L02-definition-4-1-title (block title '(solvency and liquidity ratios)' labels a block that includes gross margin). Minor, learner text only.",
  "Lab output re-run: 26 of 26 printed lines occur verbatim in L02.html. Ratios recomputed independently from the twin statements (ledgers/AC2/scripts/L01-L02-r5/r5_l02_check.py): helpers agree.",
  "Honest gap carried: the dechow1995detecting paper body was not read in any round; no paper-original row here depends on it.",
 ],
 "rows": rows,
 "summary": {"rows": len(rows), "pass": sum(1 for x in rows if x["status"] == "PASS"), "fail": sum(1 for x in rows if x["status"] == "FAIL"), "unverifiable": sum(1 for x in rows if x["status"] == "UNVERIFIABLE")},
}
json.dump(frag, open(OUT, "w"), indent=1, ensure_ascii=False)
print("rows", len(rows), frag["summary"], frag["verdict"])
