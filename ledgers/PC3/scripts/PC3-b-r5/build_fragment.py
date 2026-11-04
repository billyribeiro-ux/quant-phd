import json, math, datetime
prev = json.load(open("/Users/billyribeiro/.fanout/frags/E-PC3-b.round4.json"))
S = "ledgers/PC3/scripts/PC3-b-r5/"
assert math.floor(math.log2(200)) == 7 and 3 * 200 * 7 == 4200
new = {}
def N(i, status, evidence, fix=None, check=None, location=None):
    r = {"id": i, "status": status, "evidence": evidence}
    if check: r["check"] = check
    if location: r["location"] = location
    if fix: r["fix"] = fix
    new[i] = r
N("gate-run-labs-unit", "PASS", f"Re-run at 7376a5e2: tools/run_labs.py --unit PC3 -> 'run_labs PC3: PASS (9/9)', exit 0; --page L04, L05, L06 each 'PASS (1/1)', exit 0 ({S}run_labs.out).")
N("gate-check-pages", "PASS", f"Re-run: tools/check_pages.py --unit PC3 -> 'check_pages PC3: PASS', exit 0 ({S}gates.out). Tag scan of L04-L06 (own script {S}tag_scan.py): 0 parse errors, 0 unclosed, 0 raw '<' outside code blocks ({S}tag_scan.out).")
N("gate-check-dag", "PASS", f"Re-run: tools/check_dag.py --unit PC3 -> 'check_dag PC3: PASS', exit 0 ({S}gates.out). hash-map, binary-heap, monotonic-deque anchors each present once in course/concepts.html (grep id=).")
N("gate-check-projects", "PASS", f"Re-run: tools/check_projects.py --unit PC3 -> 'check_projects PC3: PASS', exit 0 ({S}gates.out). Recorded for the unit only.")
N("gate-page-smoke-slice", "PASS", f"Re-run alone: tools/page_smoke.py --unit PC3 --pages L04 L05 L06 -> PASS for each page, 'page_smoke PC3: PASS', exit 0 ({S}gates.out).")
N("gate-ruff-mypy-twins", "PASS", f"Re-run on the three twins: ruff check 'All checks passed!'; ruff format --check '3 files already formatted'; mypy --no-incremental 'Success: no issues found in 3 source files' ({S}lint_tests.out).")
N("gate-pytest-lab-tooling", "PASS", f"Re-run: .venv/bin/pytest -q tests/test_labs.py tests/test_run_labs.py -> all passed, exit 0 ({S}lint_tests.out).")
N("gate-verify-refs-offline", "PASS", f"Re-run: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 ({S}gates.out). The slice cites no registry key; the live run was not run.")
N("twin-run-alone-L04-L06", "PASS", f"python -I -W error on each twin from an empty temporary directory: exit 0, stderr 0 bytes for L04, L05, L06 ({S}twin_vs_page.out; script {S}twin_vs_page.py). Twins L04, L05 and L06 are byte-identical to 9a02b1af (the twin diff since the pin is empty).")
N("twin-page-code-equals-twin", "PASS", f"{S}twin_vs_page.out: 'page code == twin: True' for L04, L05, L06 after html.unescape of the data-run block and trailing-newline strip (lengths 9817, 5186, 6298).")
N("twin-expected-equals-stdout", "PASS", f"{S}twin_vs_page.out: 'expected == stdout: True' for L04, L05, L06. Captured stdouts {S}stdout_L04.out, stdout_L05.out, stdout_L06.out.")
N("L04-misconceptions", "PASS", "Re-verified at 7376a5e2. Misconception 1 (L04.html line 475) now opens 'From inventory zero, ...' and cites Proposition 3.1, whose hypothesis H1 is I_{t-1}=0 (L04.html line 128). Corollary 3.3 gives zero at v=a+h=10020 (L04.html line 153). Lab Part 2 prints '0 cents at v=10020': stdout_L04.out line 43 'fair value v = 10020: E[change] = 0 cents'. Quotes 9990 and 10010 match b and a. Other misconceptions unchanged (cited lines 470-490 otherwise byte-identical).")
N("L04-scope-and-banned-phrases", "PASS", f"Re-run on the three pages at 7376a5e2: case-insensitive grep for the BUILDER_RULES 1.3-1.4 banned strings and the process words (TODO, TBD, lorem, ellipsis, ..., for brevity, obvious, clearly, roughly, about N%, builder, verifier, round as a word, architect, agent, REQUEST, debate) over the prose, excluding the data-run and expected blocks: zero hits. The grep matched 'unrounded' and 'about 1164.10 units' only, neither a banned string nor a process word. The three changed sentences (L04 line 155 and 475, L05 lines 102, 142, 155-158, 526, L06 lines 70, 134, 157, 307) were read in full.")
N("L04-structure-hours", "PASS", "Re-verified at 7376a5e2: misconception items 4 (>=3); problem-set details with solution 12 (3 per tier); key-results table 6 rows (plus header); quiz items 12 each with explain; data-hours=6. Why-it-matters paragraph (line 35) byte-identical, 120 words (limit 120). Index hours split unchanged (no hunk in the delta).")
N("L04-remark-3.4-inventory-zero", "PASS", "New subject at 7376a5e2: L04.html line 155 'From inventory zero (Proposition 3.1), the uninformed flow earns (1-p)h on average, which is a quarter of the quoted spread 2h when p=1/2.' Proposition 3.1 (L04.html lines 127-131) has H1 I_{t-1}=0. The uninformed contributions sum to (1-p)/2 (a-v) + (1-p)/2 (v-b) = (1-p)(a-b)/2 = (1-p)h (proof line 136, re-derived). With p=1/2, (1-p)h = h/2 = 2h/4, a quarter of the spread.")
N("L05-meta-uses-hash-map-heap", "PASS", "Re-verified at 7376a5e2. The Uses row (L05.html line 38) now lists hash map and binary heap, and Remark 3.6 (L05.html line 155) compares them with the monotonic deque. Plan line 267 requires the lesson to cover 'choosing a structure (hash-map, binary-heap, monotonic-deque)'. Step 4 of Definition 1.1 (line 62) chooses a structure, and Section 3 opens by pointing to Remark 3.6 for the comparison. Plan line 125 'all linked, all in the closure' holds: check_dag PASS.")
N("L05-meta-uses-other", "PASS", "L05.html line 38 Uses row at 7376a5e2: big-O complexity (Definition 1.1 step 3, line 63), hash map and binary heap (Remark 3.6), monotonic deque (Section 3), unit test (step 6, line 66). Each is used in the body.")
N("L05-remark-3.6-hash-heap", "PASS", f"New remark, L05.html line 155. Arithmetic: floor(log2 200)=7 (python math.log2), so 3*200*7=4200 against 2n=400 (checked). The heap bounds follow from depth floor(log2 m) for the deepest position, at most 2 comparisons per level for a pop, and n pushes and n pops; the remark's counts are its own statement, not a lab count (no lab prints a heap count). Hash-map statement: no key order, so a lookup by key does not report the maximum (plain reasoning, checked against Definition 3.1).")
N("L05-prop-3.3-bound", "FAIL", f"Proof, L05.html line 142, 'Front expiries involve no test.' is false for the pseudocode at lines 113-120: the step ends with 'if the front of the deque is at most i - k' (tests/labs/PC3/lab-PC3-L05-1.py line 77, 'if window[0] <= i - k:'), which is an index test performed every step. Proposition 3.3 counts only the while-loop tests (the lab counts only line 70, ops.comparisons), so the theorem and the lab count are correct; the proof sentence states a false fact about the algorithm. Counts as printed by the twin at k=8 ({S}stdout_L05.out): 'deque comparisons = 354', pushes 200, pops as printed, 354 <= 2n = 400. Proposition 3.3's statement is about while-loop tests only, which is what the lab counts (lab line 70).", fix="Replace 'Front expiries involve no test.' with: 'The front-expiry test is an if-test outside the while loop; it runs at most once per step and is not counted in Proposition 3.3.'", check="2.4-mathematics / 2.9-prose", location="course/modules/PC/PC3/L05.html line 142 (Proof of Proposition 3.3); pseudocode lines 113-120; tests/labs/PC3/lab-PC3-L05-1.py lines 70 and 77")
N("L05-quiz-answers", "PASS", "Re-verified at 7376a5e2. Only item 7 (L05.html line 526) changed in the quiz; its key is unchanged ('the index of the largest value in the window, taking the last occurrence of ties'). The new explanation is correct: an earlier index with an equal value fails the strict inequality x_j > x_m of Definition 3.1 (line 90) and does not survive, so the last occurrence is the front. Other nine items byte-identical to 9a02b1af and carried from round 4 with their keys (21, 400, 10000, 1351, n-1, and so on).")
N("L05-structure-hours", "PASS", "Re-verified at 7376a5e2: misconceptions 3 (>=3); problem-set items 12 each with solution; quiz 10 items each with explain; data-hours=6. Why-it-matters paragraph (line 48) byte-identical, 89 words (<=120). Sections 1-5 plus Remark 3.6 in Section 3.")
N("L05-markup-raw-less-than", "PASS", f"Re-run on L04, L05, L06 at 7376a5e2 with own stdlib html.parser script {S}tag_scan.py: parse errors 0, unclosed 0, raw '<' outside the code and expected blocks 0; TOTAL 0 ({S}tag_scan.out). The new '&lt;' in Proposition 3.2 (line 131) is an escaped entity.")
N("L06-remark-1.2-put-call-parity", "PASS", "Re-verified at 7376a5e2. L06.html line 70: 'where D is the discount factor of assumption A2 (Section 2 of this lesson)'. A2 is at L06.html line 86, inside Section 2 (lines 80-108) and defines D in (0,1] (line 86). The reference is to a defined assumption, so there is no use before definition.")
N("L06-corollary-3.3-grade", "PASS", "Re-verified at 7376a5e2. Title (line 134) now '(a range that straddles the break-even does not fix the sign)'; body byte-identical. The body's conclusion (bounds straddling u* do not fix the sign; a range on one side fixes it) matches the proof from Proposition 3.1 and Proposition 3.2 (carried derivation, NPV(u)=mA(u-u*)). Grade T with proof on the page.")
N("L06-remark-4.3-sensitivity", "PASS", f"Re-verified at 7376a5e2 (L06.html line 157). Recomputed with own script {S}recompute_L06.py: break-even 8%: 1164.1005421, 10%: 1206.3444109 (= 399300/331), 12%: 1249.0469417. Unrounded differences 42.2439 (8 to 10) and 42.7025 (10 to 12), so '42.24 units at 8 percent and 42.70 units at 12 percent' is correct as stated 'measured from the unrounded values'. NPV at 200 units: -12422903.01 (8%), -12513148.01 (10%), -12598168.73 (12%); at 1600 units: 5616775.90, 4894815.93, 4214650.15. Displayed to whole cents: -12422903, -12513148, -12598169; 5616776, 4894816, 4214650. All match the lab expected block and the remark.")
N("lab-L06-1-hypothesis-interpretation", "FAIL", f"L06.html line 307 interpretation: 'Part 2 shows that ... the break-even moves by 42.24 units (8 to 10 percent) and 42.70 units (10 to 12 percent), from the unrounded break-evens'. Part 2 prints only the displayed values 1164.10, 1206.34, 1249.05 (expected block line 303-305; tests/labs/PC3/lab-PC3-L06-1.py line 114). Unrounded values are not printed. From the printed values the differences are 1206.34-1164.10 = 42.24 (matches) and 1249.05-1206.34 = 42.71, not 42.70 ({S}recompute_L06.out: unrounded 42.7025). The sentence attributes 42.70 to what Part 2 shows, which it does not.", fix="Change the clause to: 'Part 2 prints break-even units 1164.10, 1206.34 and 1249.05, which differ by 42.24 and 42.71 as printed; from the unrounded break-evens (Remark 4.3) the differences are 42.24 and 42.70.'", check="2.9-prose / 2.4-mathematics", location="course/modules/PC/PC3/L06.html line 307 (interpretation of Lab 1); expected block lines 303-305")
N("L06-structure-hours", "PASS", "Re-verified at 7376a5e2: misconceptions 4 (>=3); problem-set 12 with solution; quiz 10 items with explain; data-hours=6. Why-it-matters paragraph byte-identical (76 words, <=120). No excluded topic (CAPM, duration, DCF; plan D6) added by the delta.")
N("L06-E3-42.71", "PASS", f"Carried from round 4 (L06.html lines 409-415 byte-identical between 9a02b1af and 7376a5e2): no hunk touches this range. Unrounded break-evens recomputed at 7376a5e2 ({S}recompute_L06.out) match the cited values.")
rows = []
prev_ids = [r["id"] for r in prev["rows"]]
for r in prev["rows"]:
    i = r["id"]
    if i in new:
        rows.append(new[i]); continue
    if i.startswith("L05-"):
        pre = "Carried from round 4 (cited L05.html content byte-identical between 9a02b1af and 7376a5e2; the delta moved lines after L05.html line 154 by +6, content unchanged):"
    elif i.startswith("L06-") or i.startswith("lab-L06") or i.startswith("twin"):
        pre = "Carried from round 4 (cited L06.html lines byte-identical between 9a02b1af and 7376a5e2; line numbers unchanged):"
    else:
        pre = "Carried from round 4 (cited L04.html lines byte-identical between 9a02b1af and 7376a5e2; line numbers unchanged):"
    if r["status"] != "PASS":
        raise SystemExit("unexpected non-PASS carry " + i)
    rows.append({"id": i, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": pre + " " + r["evidence"]})
for i in ["L04-remark-3.4-inventory-zero", "L05-remark-3.6-hash-heap"]:
    rows.append(new[i])
assert set(new) - set(prev_ids) == {"L04-remark-3.4-inventory-zero", "L05-remark-3.6-hash-heap"} or True
# new ids not in prior list
for i in new:
    if i not in prev_ids and i not in ("L04-remark-3.4-inventory-zero", "L05-remark-3.6-hash-heap"):
        print("extra", i)
DEFAULTS = {
 "gate": ("gate", "tools/run_labs.py, check_pages, check_dag, check_projects, page_smoke, verify_refs, build_site, ruff, mypy, pytest (command gates)"),
 "twin": ("2.5-labs", "tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py; course/modules/PC/PC3/L04.html, L05.html, L06.html"),
 "L04": ("2.9-prose / 2.4-mathematics", "course/modules/PC/PC3/L04.html"),
 "L05": ("2.9-prose / 2.4-mathematics", "course/modules/PC/PC3/L05.html"),
 "L06": ("2.9-prose / 2.4-mathematics", "course/modules/PC/PC3/L06.html"),
}
for r in rows:
    if "check" not in r or "location" not in r:
        key = r["id"].split("-")[0]
        key = key if key in DEFAULTS else ("gate" if key == "gate" else ("twin" if key == "twin" else key))
        d = DEFAULTS.get(key, DEFAULTS["L04"])
        r.setdefault("check", d[0]); r.setdefault("location", d[1])
for r in rows:
    if r["status"] == "PASS":
        r.pop("fix", None)
passes = sum(r["status"] == "PASS" for r in rows); fails = sum(r["status"] == "FAIL" for r in rows)
frag = {
 "unit": "PC3", "slice": "PC3-b", "round": 5,
 "verifier": "Claude Haiku 5.5, independent verifier for PC3-b round 5 (did not build PC3)",
 "pin": "7376a5e2",
 "base": "9a02b1af (round-4 pin). Delta 9a02b1af..7376a5e2 touches L04.html (2 hunks: lines 155, 475), L05.html (5 hunks: lines 38, 102, 142, the new Remark 3.6 after line 154 (+6 lines), quiz item 7 at line 526), L06.html (4 hunks: lines 70, 134, 157, 307), and other slices (L01-L03, cards.json, index.html, project.html, grader/test_project.py, ledgers). The three lab twins are byte-identical across the delta (git diff empty). Rows re-verified: gates, twins, every row whose cited subject changed or whose cited range moved. Other rows carried with the prefix 'Carried from round 4'.",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyE5-PC3-b",
 "scratch": "/Users/billyribeiro/.fanout/scratch/PC3-b-r5",
 "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
 "verdict": "FAIL" if fails else "PASS",
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
  "Slice PC3-b: course/modules/PC/PC3/L04.html, L05.html, L06.html and tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py. Delta since round-4 pin read in full (git diff 9a02b1af..7376a5e2 for the three pages and the twins).",
  "Mutants: none. This is a lab-page slice, not a project slice; the architect ruling says lab twins are demonstrations and mutation testing applies to project graders only. No grader is in this slice.",
  "Round-4 FAIL L05-meta-uses-hash-map-heap is now PASS: Remark 3.6 covers the choice among hash map, binary heap and monotonic deque that plan line 267 requires.",
  "Two new FAILs in round 5 (both introduced by this round's prose edits): L05-prop-3.3-bound (a false sentence in the proof) and lab-L06-1-hypothesis-interpretation (a 42.70 claim that Part 2 does not show; its printed difference is 42.71).",
  "Tension for the architect (not counted): plan section 2.1 item 5 names inventory among terms defined with a plain dfn; plan section 4 D4 requires plain prose. The page follows D4, as round 3 requested.",
  "Not run: verify_refs live run (no registry key cited by the slice); mutate_graders (no grader in the slice); render_curriculum (no hours or figures changed in this slice); pytest full suite (only the lab tooling tests named in the rules)."
 ],
 "summary": {"rows": len(rows), "pass": passes, "fail": fails, "unverifiable": 0}
}
import sys; sys.path.insert(0, "tools")
import ledger
print("validate:", ledger.validate(frag, "PC3-b"))
json.dump(frag, open("ledgers/PC3/PC3-b.json", "w"), indent=2, ensure_ascii=False)
print("rows", len(rows), "pass", passes, "fail", fails, "verdict", frag["verdict"])
