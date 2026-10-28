import json, re, sys
ROOT = "/tmp/verify22-M1-b"
sys.path.insert(0, ROOT + "/tools")
import ledger  # noqa: E402

prev = json.load(open("/tmp/fanout-frags/M1-b.round21.json"))
CARRY = ("Carried from round 21 (course/modules/M/M1/L04.html, L05.html and cards.json cited lines "
         "byte-identical since the previous pin f95243f; the round-22 delta changes only L04.html line 79 "
         "and cards.json lines 511 and 1133, none cited by this row): ")
STRIP = re.compile(r"^Carried from round \d+ \(.*?\): ", re.S)

FRESH = {}
def fresh(i, check, loc, ev, status="PASS"):
    FRESH[i] = dict(id=i, check=check, location=loc, status=status, evidence=ev)

fresh("M1-b-r22-delta", "round-22 delta for slice b (f95243f..d160ac3)",
      "course/modules/M/M1/L04.html:79; cards.json:511 (M1-c075), 1133 (M1-c163); L05.html; tests/labs/M1; tools; references",
      "git diff --stat f95243f d160ac3 -- course/modules/M/M1 tests/labs/M1 tools references: L04.html 2 lines (one hunk, line 79), cards.json 4 lines (hunks at 511 and 1133). L05.html, both twins, tools, references: no change (out/pin.txt). Every hunk read in full: L04.html:79 (Assumption E block) and the two card backs. Rows citing other lines are carried.")
fresh("M1-b-cmd-pin", "checkout pin and slice inventory",
      "repository HEAD; course/modules/M/M1/L04.html, L05.html, cards.json; tests/labs/M1/",
      "git rev-parse HEAD = d160ac3c73ebad41c3c3b0b53a492967fc2ef9af (detached, out/pin.txt). Slice inventory: L04.html, L05.html, cards.json, lab-M1-L04-1.py, lab-M1-L05-1.py. Round-21 pin f95243f.")
fresh("M1-b-cmd-run_labs", "run_labs for M1 (all 11 labs)",
      "tools/run_labs.py --unit M1; course/modules/M/M1/L04.html; L05.html",
      "Command: .venv/bin/python tools/run_labs.py --unit M1 (exit 0): 'run_labs M1: PASS (11/11)'. out/run_labs.txt.")
fresh("M1-b-cmd-twins", "lab twins alone under python -I -W error, output equal to the embedded expected block",
      "tests/labs/M1/lab-M1-L04-1.py; lab-M1-L05-1.py; course/modules/M/M1/L04.html <pre class=expected>; L05.html <pre class=expected>",
      "Each twin run from /tmp as .venv/bin/python -I -W error: exit 0, empty stderr (out/twin_L04.err, twin_L05.err). ledgers/M1/scripts/M1-b-r21/embed_cmp.py on the stdout (out/twin_L04.stdout, twin_L05.stdout): 'expected==twin: True 27 27' and 'expected==twin: True 13 13'. tests/labs/M1 unchanged in this delta.")
fresh("M1-b-cmd-page_smoke", "page_smoke for L04 and L05",
      "tools/page_smoke.py --unit M1 --pages L04 L05",
      "Exit 0: 'page_smoke modules/M/M1/L04.html: PASS' (lab-M1-L04-1 0.0 s), 'page_smoke modules/M/M1/L05.html: PASS' (lab-M1-L05-1 0.0 s), 'page_smoke M1: PASS'. out/page_smoke.txt.")
fresh("M1-b-cmd-check_pages_dag", "check_pages and check_dag for M1",
      "tools/check_pages.py --unit M1; tools/check_dag.py --unit M1",
      "'check_pages M1: PASS' (exit 0, out/check_pages.txt); 'check_dag M1: PASS' (exit 0, out/check_dag.txt).")
fresh("M1-b-cmd-lint-types", "ruff check, ruff format --check and mypy on the two twins",
      "tests/labs/M1/lab-M1-L04-1.py, lab-M1-L05-1.py",
      "ruff check: 'All checks passed!' (exit 0). ruff format --check: '2 files already formatted' (exit 0). mypy --no-incremental: 'Success: no issues found in 2 source files' (exit 0). out/ruff_check.txt, ruff_format.txt, mypy.txt.")
fresh("M1-b-cmd-refs", "verify_refs offline and live for M1; L04 and L05 cite no registry key",
      "references/references.json; tools/verify_refs.py; L04.html:459-462; L05.html:472-475",
      "verify_refs.py --offline (exit 0): 'offline integrity: 560 entries, 0 problems'. verify_refs.py --unit M1 (exit 0): 'live re-verification of M1: 1 of 560 entries, 0 problems'. The references paragraphs at L04.html:460 and L05.html:473 cite no registry key (out/vr_offline.txt, vr_live.txt).")
fresh("M1-b-cmd-pytest", "relevant pytest",
      "tests/test_run_labs.py; tests/test_page_checks.py; tests/test_labs.py",
      "pytest -q on the three files: exit 0, every progress line all dots, no F or E (out/pytest.txt).")
fresh("M1-b-2.9-structure-prose", "2.9 structure, banned phrases and process words, L04 and L05 (full pages)",
      "course/modules/M/M1/L04.html and L05.html (changed line 79 re-read in full; full-page grep)",
      "grep -i over both pages for roughly half, about 6%, historically, ellipsis, builder, verifier, round, REQUESTS, unit report, build, typically, usually, always, only, all: L04.html hits at 79 ('only through A1 to A3', pre-existing, not a scope claim) and 260 (a quoted misconception, 'always add value'); L05.html no hit. The new text of line 79 contains no banned phrase and no process word. Line 79 is the only changed sentence in this slice.")
fresh("M1-b-2.9-DAG", "2.9 DAG and concepts for L04 and L05",
      "tools/check_dag.py --unit M1 (re-run); L04.html:79 (changed line, no data-concept attribute)",
      "check_dag M1: PASS (exit 0, out/check_dag.txt). The changed L04.html:79 carries no data-concept attribute (grep -c data-concept on line 79 = 0). Concept definitions are unchanged.")
fresh("M1-b-r4-term-before-def-L04", "term before definition, L04 (Assumption E block and its first use)",
      "course/modules/M/M1/L04.html:75 (first mention), 78-80 (Assumption E block), 52, 54-56, 59",
      "Assumption E is first named at line 75 as 'stated as Assumption E in the next block', a signpost to the definition at 78-79, not a use before definition. Line 79 changed this round; its new text uses the names Proposition 2.2 (defined at 101), Remark 2.3 (111), Problem R2, Problem R3, sections 5, 7 and 9 as places to look, which are signposts, not undefined terms. PASS.")
fresh("M1-b-r20-E-scope-remarks", "scope of Assumption E in the remarks that cite Proposition 2.2 (Remark 2.3 entries)",
      "L04.html:79 (list, Remark 2.3 entry), 112 (Remark 2.3); L05.html:127",
      "L04.html:79 lists 'Remark 2.3'; L04.html:112 reads 'Under Assumption E, Proposition 2.2 says that they stay below e^r'; L05.html:127 reads 'Under Assumption E, Proposition 2.2 says that treating r as a continuous rate discounts more than ...'. Both remarks name Assumption E where they use Proposition 2.2. The list's completeness is a separate row (M1-b-r22-E-lab1-dropped).")
fresh("M1-b-r21-E-list-complete", "scope of the L04.html:79 list: round-21 omissions at lines 75 and 460",
      "course/modules/M/M1/L04.html:79 (list), 75 and 460",
      "Resolved: the round-22 list in line 79 names 'the section 2 introduction' (line 75) and 'the references paragraph in §9' (line 460). Their omission, which was the round-21 defect, is fixed. The list still has a new omission (Lab 1, line 117), recorded as M1-b-r22-E-lab1-dropped.")
fresh("M1-b-r22-E-lab1-dropped", "scope and completeness of the L04.html:79 list of places that name Proposition 2.2",
      "course/modules/M/M1/L04.html:79 (list; sentence 'It is used in Proposition 2.2 and in each other place on this page that names Proposition 2.2 ...'), 117 (Lab 1 hypothesis)",
      "Grep -n 'Proposition 2.2' and '2.2' over L04.html gives lines 75, 79, 101, 112, 117, 261, 358, 365, 378, 380, 425, 460. Line 117 is the Lab 1 hypothesis: 'Propositions 2.1 and 2.2 predict that the factor rises with m ...'. The new list at line 79 names the section 2 introduction (75), Remark 2.3 (112), the misconception in §5 (261), Problem R2 (358), the R3 solution (365), the key-results table (378, 380), quiz item 5 (425) and the references (460), but not line 117. The round-21 list had 'Lab 1' and the round-22 edit removed it, so the claim 'each other place on this page that names Proposition 2.2' is false as written.",
      status="FAIL")
FRESH["M1-b-r22-E-lab1-dropped"]["fix"] = "Restore 'Lab 1 (the hypothesis, line 117)' to the list in L04.html:79, so the list again covers every line that names Proposition 2.2 (lines 75, 112, 117, 261, 358, 365, 378, 380, 425, 460)."
fresh("M1-b-r21-cards-c075-credit", "card M1-c075 back (changed this round) against Proposition 2.1, Proposition 2.2 and L04.html:261",
      "course/modules/M/M1/cards.json:511 (M1-c075); L04.html:84-85 (Prop 2.1), 101-102 (Prop 2.2), 261 (misconception 3)",
      "Card back now: 'No. Under Assumption E, every F_m(r) is below e^r (Proposition 2.2), although each extra compounding period raises the factor (Proposition 2.1).' Prop 2.2 (L04.html:102) gives F_m(r) < e^r for every whole m >= 1 and r > 0. Prop 2.1 (L04.html:84-85) gives strict increase in m, so 'raises' is witnessed by the proposition. The sentence matches L04.html:261 word for word in its second clause. The term 'credit' no longer appears on the card. PASS.")
fresh("M1-b-r17-2.7-cards-c163-scope", "scope of M1-c163 (changed this round, line 1133) against Problem R3 (L04.html:365)",
      "course/modules/M/M1/cards.json:1133 (M1-c163); L04.html:365 (R3 solution)",
      "Card back now: 'Yes, r_m > r under Assumption E (Problem R3). The condition 1 + r_m/m > 0 selects the positive m-th root of e^r, which is e^(r/m) (Problem R3).' L04.html:365 says 'The hypothesis 1 + r_m/m > 0 selects the positive m-th root of e^r. That root is e^(r/m)' and derives r_m > r from Assumption E (e^x - 1 > x for x > 0). The card no longer states an even-m witness. The card's front (line 1131) asks for the whole m >= 1 case with 1 + r_m/m > 0, which is the scope R3 proves. PASS.")
fresh("M1-b-2.7-cards", "2.7 cards of the slice: every card checked against the current lesson text; full duplicate scan",
      "course/modules/M/M1/cards.json (full scan); M1-c075 (511), M1-c163 (1133) re-read; other L04/L05 cards carried",
      "Full scan of cards.json (out/cards_scan.txt): 180 entries, L04 16, L05 21, no duplicate id, no duplicate front. The delta changes two card backs only (511 M1-c075, 1133 M1-c163); both re-read against L04.html:84-85, 101-102, 261 and 365 (rows M1-b-r21-cards-c075-credit and M1-b-r17-2.7-cards-c163-scope). The other L04/L05 card texts are byte-identical to the previous pin; their rows are carried.")
fresh("M1-b-r19-cards-scan", "full card scan (cards.json)",
      "course/modules/M/M1/cards.json",
      "Full scan this round (out/cards_scan.txt): 180 entries, no duplicate id, no duplicate front.")
fresh("M1-b-r18-cards-scan", "full card scan after round-18 edits (superseded)",
      "course/modules/M/M1/cards.json",
      "Superseded by the full scan this round (out/cards_scan.txt): 180 entries, no duplicate id, no duplicate front.")

rows = []
for r in prev["rows"]:
    i = r["id"]
    if i in FRESH:
        rows.append(FRESH[i])
        continue
    ev = STRIP.sub("", r["evidence"], count=1)
    nr = dict(id=i, check=r["check"], location=r["location"], status=r["status"], evidence=CARRY + ev)
    if r["status"] != "PASS":
        nr["fix"] = r.get("fix", "")
    rows.append(nr)
known = {r["id"] for r in prev["rows"]}
for i, r in FRESH.items():
    if i not in known:
        rows.append(r)
# keep fix on FRESH FAIL rows; FRESH rows carry no stale 'fix'
for r in rows:
    if r["status"] == "PASS":
        r.pop("fix", None)

counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
frag = {
    "unit": "M1",
    "slice": "M1-b",
    "round": 22,
    "verifier": "independent verifier (Haiku), round 22",
    "pin": "d160ac3c73ebad41c3c3b0b53a492967fc2ef9af",
    "base": "f95243f (round 21 pin; delta: L04.html line 79; cards.json lines 511, 1133)",
    "previous_fragment": "/tmp/fanout-frags/M1-b.round21.json",
    "checkout": ROOT,
    "scratch": "/tmp/M1-v/M1-b-r22",
    "verified_at": "2026-10-28T12:00:00+00:00",
    "verdict": "FAIL" if counts["FAIL"] else "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice b is lessons L04 and L05 with their lab twins, not a project slice: no student-error mutants or alternative implementations apply (architect ruling, as in rounds 16-21). ledgers/M1/mutants/ holds the project mutants of slices a and c and is unchanged in this delta (out/pin.txt).",
        "Delta f95243f..d160ac3 for slice b: L04.html line 79 (Assumption E block, one sentence rewritten); cards.json lines 511 (M1-c075) and 1133 (M1-c163). L05.html, tests/labs/M1, tools and references are unchanged.",
        "Carried rows cite lines and files that are byte-identical to the previous pin; their cited lines are not in the delta. Every row citing L04.html:79 or cards.json 511/1133, and every whole-file card scan, was re-verified fresh.",
        "Not checked: a full line-by-line re-read of every unchanged line of L04.html and L05.html (carried by byte-identity of the cited lines, as in rounds 16-21). Every command row was re-run this round.",
        "No external source is cited or read in this slice; the registry check is a live sample (1 of 560 entries) plus the full offline integrity pass.",
        "Card M1-c181 (L05) and card M1-c180 (L07) are carried from round 21; M1-c180 belongs to L07, outside this slice.",
        "Round-21 row M1-b-r21-E-list-complete is resolved for lines 75 and 460, and its residual Lab 1 omission is the new FAIL row M1-b-r22-E-lab1-dropped (the round-22 edit dropped 'Lab 1' from the list).",
    ],
    "summary": {"rows": len(rows), "pass": counts["PASS"], "fail": counts["FAIL"], "unverifiable": counts["UNVERIFIABLE"]},
}
out = ROOT + "/ledgers/M1/M1-b.json"
json.dump(frag, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows", len(rows), counts, "verdict", frag["verdict"])
print("validate:", ledger.validate(json.load(open(out, encoding="utf-8")), "M1-b"))
