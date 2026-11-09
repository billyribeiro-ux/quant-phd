"""Builds ledgers/E2/E2-a.json (round 1, pin 95f3f8cb) from the base round-8 fragment (pin f618cf1).

Re-verified rows get new evidence (see the scratch outputs in this directory). Every other base row is
carried with the carry prefix after a check that none of its cited files changed since f618cf1.
Run: python -I ledgers/E2/scripts/E2-a-r1/build_fragment_r1.py
"""

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
S = "ledgers/E2/scripts/E2-a-r1"
base = json.load(open("/Users/billyribeiro/.fanout/frags/C-E2-a.round8.json", encoding="utf-8"))
changed = set(
    subprocess.run(
        ["git", "diff", "--name-only", "f618cf1..HEAD"], capture_output=True, text=True, check=True, cwd=ROOT
    ).stdout.split()
)

REVERIFIED = {
    "E2a-r8-cards-L03-c034": (
        "Re-verified at 95f3f8cb (card changed since f618cf1). cards.json E2-c034 now reads front 'With alpha = 1/2, what is the market-consistent price?', "
        "back '6000 cents, the only market-consistent price, because alpha < 2/3 (Example 2.2; Proposition 2.1).' "
        "L03.html:72-78 (Proposition 2.1: the set is {6000 : alpha < 1} union {6000 + 6000 alpha : alpha >= 2/3}; for alpha < 2/3 the price 6000 is the only one) "
        "and L03.html:91-93 (Example 2.2: alpha = 1/2 gives {6000}). Run output " + S + "/twin_L03.stdout line 10: 'alpha = 1/2: market-consistent prices [6000]'. "
        "Grade T agrees with the Proposition's grade (L03.html:72). The card carries the proposition's specific hypothesis alpha < 2/3; Assumptions 1 to 3 "
        "of Proposition 2.1 are the lesson's model and are not restated on the card (observation, not a ruling-26 kind)."
    ),
    "E2a-r4-cmd-check_dag": "Re-run at 95f3f8cb: 'check_dag E2: PASS', rc 0 (" + S + "/check_dag.out). curriculum/*.yaml and course/concepts.html changed since f618cf1 (M3, CS3 entries only); E2 DAG result unchanged.",
    "E2a-r4-cmd-check_pages": "Re-run at 95f3f8cb: 'check_pages E2: PASS', rc 0 (" + S + "/check_pages.out). Covers cards.json (changed) and the banned-phrase scan of index and L01-L03.",
    "E2a-r4-cmd-check_projects": "Re-run at 95f3f8cb: 'check_projects E2: PASS', rc 0 (" + S + "/check_projects.out). E2 project.html changed (L05 and FC lines, not slice a); slice a has no project file.",
    "E2a-r4-cmd-run_labs": "Re-run at 95f3f8cb: 'run_labs E2: PASS (12/12)', rc 0 (" + S + "/run_labs.out). lab-E2-L05-1.py changed (slice b); L01-L03 twins byte-identical.",
    "E2a-r4-lab-isolated": "Re-run at 95f3f8cb: 'python -I -W error' on lab-E2-L01-1.py, L02-1.py, L03-1.py each rc 0, stderr 0 bytes (" + S + "/twins.out, twin_L0*.stderr).",
    "E2a-r4-lab-page-equals-twin-and-expected": "Re-run at 95f3f8cb with ledgers/E2/scripts/E2-a-r5/embed_and_expected_r3.py via python -I: L01, L02, L03 'page code == twin: True', 'expected == stdout: True', twin rc=0, stderr 0; 'ALL OK' (" + S + "/embed.out).",
    "E2a-r4-page-smoke": "Re-run at 95f3f8cb: 'page_smoke E2: PASS', rc 0, for index L01 L02 L03 (" + S + "/page_smoke.out).",
    "E2a-r4-pytest": "Re-run at 95f3f8cb: pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -q, all dots, rc 0 (" + S + "/pytest.out). Full suite not re-run: the closing delta touched no tooling.",
    "E2a-r4-ruff-mypy": "Re-run at 95f3f8cb: 'ruff check .' All checks passed, rc 0; 'ruff format --check .' 555 files already formatted, rc 0; '.venv/bin/mypy --no-incremental' 'Success: no issues found in 386 source files', rc 0 (" + S + "/ruff.out, " + S + "/mypy.out).",
    "E2a-r4-verify_refs": "Re-run at 95f3f8cb: 'tools/verify_refs.py --offline' 'offline integrity: 560 entries, 0 problems', rc 0 (" + S + "/verify_refs.out). references/references.json changed (generated_at, used_by for BK1/BK4, DV1/FC2, E9/LX1); no entry cited by E2-a changed (see E2a-r8-L01-76-registry-quote).",
    "E2a-r4-recompute": "Re-run at 95f3f8cb: ledgers/E2/scripts/E2-a-r5/recompute_e2a_r4.py via python -I: 'TOTAL 55 PASS 55 FAIL 0', rc 0 (" + S + "/recompute.out). New card numbers checked separately in E2a-r1-cards-numbers-and-lab-outputs.",
    "E2a-r4-banned-process-words": "Re-run at 95f3f8cb: check_pages banned-phrase scan PASS (E2a-r4-cmd-check_pages). Plus grep -i -E 'TODO|TBD|lorem|for brevity|beyond the scope|left as an exercise|round [0-9N]|verifier|builder|fixer|ruling' over course/modules/E/E2/cards.json: 0 hits (no output).",
    "E2a-r3-hub-cards-titles": "Re-verified at 95f3f8cb (" + S + "/hub_l06_delta.out): the card-title spans in index.html equal the h1 of each of L01-L09 exactly (L04 'Signaling', L05 'Screening', L06 'Moral hazard' unchanged). L04-L06 changed only in body text, not in h1.",
    "E2a-r8-index-115-L06-card-affine": "Re-verified at 95f3f8cb: index.html:115 says 'an affine contract'. L06.html:7 meta 'The affine contract', L06.html:86 Lemma 1.2 '(the contract is affine in output)', L06.html:95 'every contract ... is affine in output'. grep -i 'linear' gives only 'quasi-linear utility' (L06.html:119, :248). Agrees (" + S + "/hub_l06_delta.out).",
    "E2a-r8-index-128-stretch-card": "Re-verified at 95f3f8cb: index.html:128 'An open extension: asymmetric bidders, a third format, or a stated hypothesis...'. grep -rn 'no ceiling' course/modules/E/E2/ returns no line (rc 1), so no page keeps the old claim (" + S + "/hub_l06_delta.out).",
    "E2a-r3-DAG-forward-mentions": "Re-run at 95f3f8cb: check_dag E2 PASS (" + S + "/check_dag.out). L01.html, L02.html, L03.html and index.html are byte-identical to f618cf1 (git diff --quiet, " + S + "/hub_l06_delta.out), so the cited forward mentions are unchanged.",
}

registry_prefix = "Carried from round 8 (references/references.json entries for the keys cited here byte-identical since f618cf1: compared with json entries, nash1950equilibrium, fudenberg1991game, spence1973job, rothschild1976equilibrium, holmstrom1979moral identical at 95f3f8cb): "
card_prefix = "Carried from round 8 (course/modules/E/E2/cards.json entry byte-identical since f618cf1, " + S + "/card_delta.out): "

rows = []
carried = 0
for r in base["rows"]:
    rid = r["id"]
    if rid in REVERIFIED:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": REVERIFIED[rid]})
        continue
    if rid == "E2a-r8-L01-76-registry-quote" or rid == "E2a-r7-index-135-normalization-claim" or rid == "E2a-r3-hub-core-reading":
        prefix = registry_prefix
    elif rid.startswith("E2a-r8-cards-"):
        prefix = card_prefix
    else:
        files = sorted(set(re.findall(r"[A-Za-z0-9_./\-]+\.(?:html|py|json|yaml|md)", r["location"])))
        files = [f if "/" in f or f.startswith("tests") else f for f in files]
        full = []
        for f in files:
            if f.startswith(("L0", "index")):
                f = "course/modules/E/E2/" + f
            elif f.startswith("lab-"):
                f = "tests/labs/E2/" + f
            full.append(f)
        hit = [f for f in full if f in changed]
        assert not hit, (rid, hit)
        prefix = "Carried from round 8 (" + ", ".join(full) + " byte-identical since the previous pin f618cf1; git diff --name-only f618cf1..HEAD does not list them): "
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": prefix + r["evidence"]})
    carried += 1

new_rows = [
    {
        "id": "E2a-r1-cards-L01-changed",
        "check": "2.10 changed cards vs current L01 text (c002, c012, c013, c128, c129)",
        "location": "course/modules/E/E2/cards.json E2-c002, c012, c013, c128, c129 vs L01.html:56-62, :72, :107, :159-166, :271-274, :285, :294, :369-370, :392",
        "status": "PASS",
        "evidence": "c002 back 'Pure actions are chosen with certainty, with no randomization over actions (Definition 1.1)' agrees with L01.html:58 ('Pure actions are chosen with certainty. Mixed strategies ... are outside this lesson'). Locator note: the sentence sits in the paragraph after the Definition 1.1 block, not inside it (observation). c012 'three diagonal profiles (a, a), (b, b), (c, c)' and 'exactly one, (D, D)' agree with " + S + "/twin_L01.stdout lines 2, 8. c013 '(29, 31), (30, 30), (31, 29)', '8281 pairs' agree with twin_L01.stdout lines 10-11 and L01.html:271-272. c129 '(30, 30) alone' agrees with twin_L01.stdout line 13 (strict test uses '<', L01 lab code line 228). Grades C with lab basis match the lab-printed output.",
    },
    {
        "id": "E2a-r1-cards-L02-changed",
        "check": "2.10 changed cards vs current L02 text (c025, c127, c130)",
        "location": "course/modules/E/E2/cards.json E2-c025, c127, c130 vs L02.html:90-93, :97-102, :127-137",
        "status": "PASS",
        "evidence": "c025 '(n - 1)/(n + 1), under Assumptions 1 to 4 of Proposition 2.2 ... (Proposition 2.5)' agrees with L02.html:128 (Proposition 2.5 under Assumptions 1 to 4 of Proposition 2.2) and L02.html:102. c127 agrees with Example 2.1 (L02.html:92: n >= 2 bidders, value V_i, bid b_i >= 0, highest bid wins and pays own bid, earns V_i - b_i or 0; the lesson does not state a tie rule, which the card does not claim). c130 '(n - 1)/(n + 1)' for the second-highest mean agrees with L02.html:133-134 (density n(n-1)x^(n-2)(1-x)) and L02.html:137 (no second-price claim). Grade T agrees with L02.html:127 claim grade.",
    },
    {
        "id": "E2a-r1-cards-L03-changed",
        "check": "2.10 changed cards vs current L03 text (c040, c131; c034 re-verified above)",
        "location": "course/modules/E/E2/cards.json E2-c040, c131 vs L03.html:72-78, :112, :116, :184-197",
        "status": "PASS",
        "evidence": "c040 'One price, 6000 cents, for each share from 0 to 0.6 ... tests every whole-cent price from 0 to 15000' agrees with twin_L03.stdout lines 4-9 (alpha = 0 to 3/5 print [6000]) and L03.html:112. c131 '6000, and 10200, 10800 and 11400 cents for shares 0.7, 0.8 and 0.9' agrees with twin_L03.stdout lines 12-14 and the expected block L03.html:195-197; 6000 + 6000*0.9 = 11400 by Proposition 2.1 (L03.html:86). Grade C with exact-enumeration basis matches the printed lab output.",
    },
    {
        "id": "E2a-r1-cards-numbers-and-lab-outputs",
        "check": "2.10 every card number appears in its lesson; lab-cited outputs match the real twin run",
        "location": S + "/card_delta.out; " + S + "/twin_L01.stdout, twin_L03.stdout, twin_L02.stdout",
        "status": "PASS",
        "evidence": "card_delta.py (run with python -I) lists the numbers of each changed or new L01-L03 card; 'missing from lesson text' is empty for c002, c012, c013, c025, c034, c040, c127, c128, c129, c130, c131. Real twin runs (python -I -W error, rc 0) print the values the cards cite: L01 '8281', '[(29, 31), (30, 30), (31, 29)]', '[(30, 30)]', 3 diagonal profiles; L03 '15001 prices tested per share', alpha 0 to 3/5 -> [6000], alpha 7/10 -> [6000, 10200], 4/5 -> [6000, 10800], 9/10 -> [6000, 11400].",
    },
    {
        "id": "E2a-r1-scope-pages-twins-unchanged",
        "check": "scope: slice-a pages, twins and notation unchanged since the base pin",
        "location": "course/modules/E/E2/L01.html, L02.html, L03.html, index.html; tests/labs/E2/lab-E2-L01-1.py, L02-1.py, L03-1.py; notation/",
        "status": "PASS",
        "evidence": "git diff --quiet f618cf1..HEAD on these paths: exit 0 (" + S + "/hub_l06_delta.out). Changed files in E2 since f618cf1 are slice-b lessons L04-L06, project.html, tests/labs/E2/lab-E2-L05-1.py and cards.json; cards.json changes are checked per id above.",
    },
]
rows.extend(new_rows)

now = datetime.now(timezone.utc).isoformat(timespec="seconds")
frag = {
    "unit": "E2",
    "slice": "a",
    "round": 1,
    "round_note": "Round 1 independent closing delta verification (ruling 30) of E2-a at pin 95f3f8cb. Base: round-8 fragment C-E2-a.round8.json at f618cf1 (62 rows, all PASS). Delta f618cf1..95f3f8cb in slice a: cards.json entries E2-c002, c012, c013, c025, c034, c040 changed; E2-c127 to c131 added. Pages L01-L03, index.html, twins L01-L03 and notation are byte-identical. Shared files changed: references/references.json (generated_at and used_by only; no entry cited by E2-a changed), curriculum yaml and concepts/index (M3, CS3 and site generation only), slice-b lessons L04-L06, project.html and lab-E2-L05-1.py (not slice a).",
    "verifier": "Haiku independent verifier, E2-a closing delta round 1 (did not build E2)",
    "pin": "95f3f8cb",
    "base": "f618cf1",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyF11-E2-a",
    "scratch": "ledgers/E2/scripts/E2-a-r1/",
    "verified_at": now,
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": base["registry_flags"],
    "freshness_flags": [],
    "notes": (
        "Slice a has no project and no grader; no mutants were run or authored (ruling 37: closing round writes no new mutants; the standing set for slice a is empty). "
        "Observations (notes, not rows, per ruling 30): (1) E2-c002 cites '(Definition 1.1)' but its sentence is in the paragraph after the Definition 1.1 block (L01.html:58). "
        "(2) E2-c034 (grade T) restates alpha < 2/3 but not Assumptions 1 to 3 of Proposition 2.1; the lesson model is defined on the page and the card carries the proposition's specific hypothesis. "
        "(3) E2-c127 has no grade field; the convention for cards in this file allows that (38 cards without grade, check_pages PASS). "
        "Not checked: live Crossref (verify_refs --offline only); the hub-level gates for slice b (L04-L06, project) which belong to slice b; full pytest suite (relevant files only); mypy ran over the whole repository (386 files)."
    ),
    "summary": (
        "E2-a closing delta at 95f3f8cb: PASS. " + str(len(rows)) + " rows, all PASS: " + str(len(REVERIFIED)) + " re-verified from scratch (incl. E2a-r8-cards-L03-c034), "
        + str(carried) + " carried from base round 8 with the carry prefix (subjects byte-identical), " + str(len(new_rows)) + " new rows for the changed slice-a cards and scope. "
        "All gate commands re-run at 95f3f8cb pass: check_pages, check_dag, check_projects, run_labs, twins under python -I -W error, embed/expected, recompute, page_smoke, ruff, mypy, pytest (3 files), verify_refs --offline."
    ),
}
out = ROOT / "ledgers" / "E2" / "E2-a.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("rows", len(rows), "reverified", len(REVERIFIED), "carried", carried, "new", len(new_rows))
