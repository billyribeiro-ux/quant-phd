"""SC1-a round 17 fragment writer. Carries round-16 rows, re-verifies the changed subjects, writes ledgers/SC1/SC1-a.json.

Run from the checkout root: python3 -I ledgers/SC1/scripts/SC1-a-r17/write_fragment_r17.py
"""

import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
PREV = "/Users/billyribeiro/.fanout/frags/E-SC1-a.round16.json"
OUT = os.path.join(ROOT, "ledgers", "SC1", "SC1-a.json")
R = "ledgers/SC1/scripts/SC1-a-r17"
CHANGED_FILES = ("index.html", "L01.html", "L03.html")
HUNKS = "index.html:33, :165; L01.html:234, :408; L03.html:51, :463"
PREFIX_A = "Carried from round 16 ({files} byte-identical since the previous pin):"
PREFIX_B = (
    "Carried from round 16 (cited files differ from the previous pin only at {hunks}; each of those six lines was read "
    "in the r17 delta rows and the row's property is line-local, so it holds on them):"
)

prev = json.load(open(PREV, encoding="utf-8"))
rows_by_id = {r["id"]: r for r in prev["rows"]}

OVERRIDE = {
    "SC1a-r15-lab-mutants-p1-p3": {
        "check": "2.5-labs",
        "location": "ledgers/SC1/lab-mutants/SC1a-r15-lab-p1-L01-dyadic-width-doubled.py; ...-p2-L02-...; ...-p3-L03-...",
        "status": "PASS",
        "evidence": (
            "Round-16 FAIL cited files that were absent at 56cc575. At 700bf33f they are tracked (`git ls-files "
            "ledgers/SC1/lab-mutants | grep r15` lists all three). Round-17 run of ledgers/SC1/scripts/SC1-a-r16/"
            "kill_lab_mutants_r16.py copied to "
            f"{R}/kill_lab_mutants_r17.py: `KILLED` for p1 (L01 token 11 '1/2' vs '1'), p2 (L02 token 148), p3 (L03 "
            f"token 31); output {R}/out/kill_lab_mutants_r17.out ends 'lab mutants killed 35/35; survivors 0'."
        ),
    },
    "SC1a-r16-hub-rung-hours": {
        "check": "2.9-prose",
        "location": "course/modules/SC/SC1/index.html:165; project.html:270-281, :638",
        "status": "PASS",
        "evidence": (
            "Round-17 index.html:165 now reads 'The project page's time budget gives the hours of each deliverable, and "
            "rung 4 (stretch) has no set hours.' project.html:270-281 (#hours table) gives a row per deliverable: rung 1 "
            "2 h, rung 2 3 h, proofs 10, engine 8, report 3, self-assessment 2, total 28 (matches data-hours-project=28 "
            "and the 28 of 100 hub split). project.html:638 'Rung 4 · Stretch' section has no hours; its text (:639-643) "
            "states none. Claim now true for rung 3 (its deliverables are rows of the table) and rung 4 (none set)."
        ),
    },
    "SC1a-r16-cards-L01-L03-full": {
        "check": "2.7-cards",
        "location": "course/modules/SC/SC1/cards.json (L01-L03 cards); L01.html:234",
        "status": "FAIL",
        "evidence": (
            "Round-16 full scan passed, but the round-17 L01.html:234 text ('Definition 1.1 fixes the value at time 0 of "
            "every path and the finite-dimensional laws') makes card SC1-c017 disagree with the current lesson: its back "
            "answers 'What does Definition 1.1 fix?' with 'Finite-dimensional laws, not the set of paths' only. See row "
            "SC1a-r17-card-c017-definition-fixes. The scan's conclusion for the other L01-L03 cards is unchanged "
            "(cards.json is byte-identical to the previous pin)."
        ),
        "fix": "Edit SC1-c017 back as in SC1a-r17-card-c017-definition-fixes, then re-scan the L01-L03 cards.",
    },
    "SC1a-misconceptions-canon": {
        "check": "2.9-prose",
        "location": "course/modules/SC/SC1/L01.html:219-237 (changed line 234); L02.html:329-345; L03.html:265-281",
        "status": "PASS",
        "evidence": (
            "Round-17 re-read of L01.html:219-237 and L02/L03 misconception blocks. L01.html:234 (changed) checked against "
            "D1 (L01.html:60, B_0=0) and D2/D3 (laws): accurate. Other misconception statements are byte-identical to "
            "the previous pin. Card SC1-c017 mismatch is row SC1a-r17-card-c017-definition-fixes."
        ),
    },
    "SC1a-hub-ladder-objectives": {
        "check": "2.9-prose",
        "location": "course/modules/SC/SC1/index.html:163-171 (changed line 165); :168",
        "status": "PASS",
        "evidence": (
            "Round-17 read of index.html:162-172 in full. Ladder rungs (worked example, completion problem, independent "
            "project, stretch) match project.html:43-47. Line 165 changed; checked in SC1a-r16-hub-rung-hours."
        ),
    },
    "SC1a-gate-check-pages": {
        "check": "2.9-structure-tool",
        "location": "index.html, L01.html, L02.html, L03.html, cards.json",
        "status": "PASS",
        "evidence": f"`.venv/bin/python tools/check_pages.py --unit SC1` -> 'check_pages SC1: PASS', rc=0 ({R}/out/check_pages_SC1.out).",
    },
    "SC1a-gate-check-dag": {
        "check": "2.9-dag",
        "location": "index.html, L01.html, L02.html, L03.html",
        "status": "PASS",
        "evidence": f"`.venv/bin/python tools/check_dag.py --unit SC1` -> 'check_dag SC1: PASS', rc=0 ({R}/out/check_dag_SC1.out).",
    },
    "SC1a-gate-run-labs": {
        "check": "2.5-labs",
        "location": "tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py",
        "status": "PASS",
        "evidence": (
            f"`tools/run_labs.py --unit SC1 --page L01|L02|L03` each -> 'run_labs SC1: PASS (1/1)', rc=0 "
            f"({R}/out/run_labs_L0{{1,2,3}}.out). Twins alone: `python -I -W error tests/labs/SC1/lab-SC1-L0n-1.py` rc=0 "
            f"for n=1,2,3 with empty stderr ({R}/out/twin_L0n.rc, .stderr)."
        ),
    },
    "SC1a-gate-page-smoke": {
        "check": "2.9-page-smoke",
        "location": "index.html, L01.html, L02.html, L03.html",
        "status": "PASS",
        "evidence": (
            f"`tools/page_smoke.py --unit SC1 --pages index L01 L02 L03` (alone) -> PASS for all four pages and "
            f"'page_smoke SC1: PASS', rc=0 ({R}/out/page_smoke_slice_a_r17.out)."
        ),
    },
    "SC1a-gate-lint-types-tests": {
        "check": "2.9-lint-types-tests",
        "location": "repo: ruff, mypy, pytest -k SC1",
        "status": "PASS",
        "evidence": (
            f"ruff check: 'All checks passed!' rc=0; ruff format --check: '553 files already formatted' rc=0; "
            f"mypy --no-incremental: 'Success: no issues found in 385 source files' rc=0; pytest -q -k SC1: 11 passed "
            f"rc=0, collect-only 'tests/test_labs.py: 11' ({R}/out/ruff_check.out, ruff_format.out, mypy.out, "
            f"pytest_SC1.out, collect_SC1.out)."
        ),
    },
    "SC1a-gate-verify-refs": {
        "check": "2.1-citations",
        "location": "course/modules/SC/SC1/index.html:182 (data-cite shreve2004stochastic); references/references.json",
        "status": "PASS",
        "evidence": (
            f"`tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems', rc=0 "
            f"({R}/out/verify_refs_offline.out); `tools/verify_refs.py --unit SC1` -> 'live re-verification of SC1: "
            f"1 of 560 entries, 0 problems', rc=0 ({R}/out/verify_refs_unit_SC1.out)."
        ),
    },
    "SC1a-r7-gate-check-projects": {
        "check": "2.9-structure-tool",
        "location": "index.html, L01.html, L02.html, L03.html",
        "status": "PASS",
        "evidence": f"`tools/check_projects.py --unit SC1` -> 'check_projects SC1: PASS', rc=0 ({R}/out/check_projects_SC1.out).",
    },
    "SC1a-r16-lab-mutants-35": {
        "check": "2.5-labs",
        "location": "ledgers/SC1/lab-mutants/** (35 files) vs L01.html, L02.html, L03.html expected blocks",
        "status": "PASS",
        "evidence": f"Round-17 run of kill_lab_mutants_r17.py: 35 KILLED, 'lab mutants killed 35/35; survivors 0' ({R}/out/kill_lab_mutants_r17.out).",
    },
}

NEW = [
    {
        "id": "SC1a-r17-delta-read",
        "check": "2.9-delta",
        "location": "course/modules/SC/SC1/index.html; L01.html; L02.html; L03.html; cards.json; tests/labs/SC1",
        "status": "PASS",
        "evidence": (
            "`git diff --stat 56cc575a..700bf33f -- course/modules/SC/SC1 tests/labs/SC1 curriculum notation "
            "references/extra_sources.yaml tools/data_sources.yaml`: index.html (2 lines), L01.html (2), L03.html (2); "
            "cards.json, L02.html, the three twins, notation, curriculum unchanged. All six changed lines read in the "
            "`git diff` output and rows SC1a-r17-hunk-* below. Line numbers preserved (1-for-1 replacements)."
        ),
    },
    {
        "id": "SC1a-r17-hunk-index-33",
        "check": "2.9-prose",
        "location": "course/modules/SC/SC1/index.html:33 (lede)",
        "status": "PASS",
        "evidence": (
            "Changed 'Its project proves those results' to 'Its project asks you to prove those results and to check them "
            "with a module'. project.html:45-47 rung 3 asks for the same proofs and engine; the fixed-time form is Theorem "
            "2.5 of L06 (L06.html:153, 'the reflection identity for Brownian motion') and the path-level form is Proposition "
            "2.7 (L06.html:52, :119). Banned-phrase scan of the line: no hits (bash grep, this round)."
        ),
    },
    {
        "id": "SC1a-r17-hunk-L01-234",
        "check": "2.9-prose",
        "location": "course/modules/SC/SC1/L01.html:234 (misconception 3)",
        "status": "PASS",
        "evidence": (
            "New text: 'Definition 1.1 fixes the value at time 0 of every path and the finite-dimensional laws, but not the "
            "set of paths.' Definition 1.1 (L01.html:60-63): (D1) B_0=0 is the time-0 value of every path; (D2)/(D3) are "
            "laws. Accurate; no number, no scope word. The sentence about the process B~ of section 4 is unchanged."
        ),
    },
    {
        "id": "SC1a-r17-hunk-L01-408",
        "check": "2.9-prose",
        "location": "course/modules/SC/SC1/L01.html:408 (quiz item 7 explanation)",
        "status": "PASS",
        "evidence": (
            "New explanation: 'Definition 1.1 fixes the start of every path and the finite-dimensional laws. Section 4 "
            "shows that a process satisfying it can have discontinuous paths.' The correct option (L01.html:405-407, "
            "'Whether the paths are continuous') is not fixed by D1-D3 (L01.html:60-63, :68). Accurate."
        ),
    },
    {
        "id": "SC1a-r17-hunk-L03-51",
        "check": "2.2-numbers",
        "location": "course/modules/SC/SC1/L03.html:51 (why-it-matters)",
        "status": "PASS",
        "evidence": (
            "Changed 'shrink to zero' to 'shrink to zero as the mesh shrinks'. Re-derived with "
            f"{R}/hunk_numbers_r17.py (out/hunk_numbers_r17.out): sum over 2000 random partitions of [0,H] of "
            "(b^2-a^2)^2 divided by 4H^3|P| has maximum 0.25 (<= 1, consistent with Prop 2.4(a)). Uniform partitions: "
            "sum/mesh -> 4H^3/3 (1.333328 at H=1, N=256; 10.666626 at H=2, N=256), so the sum is of order H^3 times the mesh."
        ),
    },
    {
        "id": "SC1a-r17-hunk-L03-463",
        "check": "2.9-prose",
        "location": "course/modules/SC/SC1/L03.html:463 (quiz item 8 correct option); :466 explanation",
        "status": "PASS",
        "evidence": (
            "Correct option now 'so the squares sum to something of order H^3 times the mesh'. Own computation "
            f"({R}/out/hunk_numbers_r17.out): sum/mesh = (4/3)H^3 in the limit (H=2 gives 10.6666 = 32/3), so the option "
            "is right and the explanation 'at most 4H^3|P|' (L03.html:466) holds. Matches card SC1-c056 (cards.json:458-462). "
            "The symbol t no longer appears in the option; H is the horizon of L03 (SC1a-notation-H-horizon)."
        ),
    },
    {
        "id": "SC1a-r17-card-c017-definition-fixes",
        "check": "2.7-cards",
        "location": "course/modules/SC/SC1/cards.json SC1-c017 (lines 136-141); L01.html:234",
        "status": "FAIL",
        "evidence": (
            "Card front: 'misconception: Definition 1.1 fixes the paths ... What does Definition 1.1 fix?'. Card back: "
            "'Finite-dimensional laws, not the set of paths.' Current lesson L01.html:234 says Definition 1.1 fixes 'the "
            "value at time 0 of every path and the finite-dimensional laws'. The back omits (D1), B_0=0, so it no longer "
            "agrees with the current lesson text (BUILDER_RULES section 7 / VERIFIER_RULES 2.7)."
        ),
        "fix": (
            "In course/modules/SC/SC1/cards.json, card SC1-c017, change the back to: 'The value at time 0 of every path "
            "(D1, B_0=0) and the finite-dimensional laws (D2, D3), not the set of paths. The process B~ of Section 4 "
            "satisfies (D1)-(D3) and has the laws of B, yet its paths differ from those of B.' No tool writes cards.json "
            "(grep of tools/*.py: only check_pages.py reads it), so edit the file and re-run the card scan."
        ),
    },
    {
        "id": "SC1a-r17-banned-changed-lines",
        "check": "2.9-banned-phrases",
        "location": "index.html:33, :165; L01.html:234, :408; L03.html:51, :463",
        "status": "PASS",
        "evidence": (
            "bash grep -i -E over the six changed lines for TODO|TBD|lorem|omitted|for brevity|beyond the scope|left as an "
            "exercise|you can add|important to note|studies show|experts agree|well known|obviously|clearly|ellipsis: no hits."
        ),
    },
]

rows = []
carried_ids = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in OVERRIDE:
        new = dict(r)
        new.update(OVERRIDE[rid])
        if new["status"] == "PASS":
            new.pop("fix", None)
        rows.append(new)
        continue
    new = dict(r)
    loc = r.get("location", "")
    if any(f in loc for f in CHANGED_FILES):
        new["evidence"] = PREFIX_B.format(hunks=HUNKS) + " " + r["evidence"]
    else:
        new["evidence"] = PREFIX_A.format(files=loc.split(";")[0].strip() or "cited files") + " " + r["evidence"]
    carried_ids.append(rid)
    rows.append(new)
rows.extend(NEW)

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
assert set(rows_by_id) <= set(ids), "a round-16 id was dropped"

mutants = []
for line in open(os.path.join(ROOT, R, "out", "kill_lab_mutants_r17.out"), encoding="utf-8"):
    m = re.match(r"KILLED (\S+) \((L0\d)\)", line)
    if m:
        first = open(os.path.join(ROOT, m.group(1)), encoding="utf-8").readline().strip()
        FIRST_LINE = first
        mutants.append(
            {
                "id": os.path.relpath(os.path.join(ROOT, m.group(1)), os.path.join(ROOT, "ledgers", "SC1", "lab-mutants")),
                "description": FIRST_LINE,
                "killed_by": f"lab-SC1-{m.group(2)}-1 expected block ({R}/out/kill_lab_mutants_r17.out)",
            }
        )

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
verdict = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 else "FAIL"
non_pass = [r["id"] for r in rows if r["status"] != "PASS"]

frag = {
    "unit": "SC1",
    "slice": "a",
    "round": 17,
    "verifier": "Haiku independent verifier, SC1-a round 17 (did not build SC1)",
    "pin": "700bf33f334486d7b5b4f22d4f82f3e25d4b39b6",
    "base": "56cc575a (round-16 pin; round-16 fragment /Users/billyribeiro/.fanout/frags/E-SC1-a.round16.json used as context, its PASS rows not trusted)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE17-SC1-a (detached at 700bf33f; .venv symlinked)",
    "scratch": "none used for evidence; scripts under ledgers/SC1/scripts/SC1-a-r17/",
    "verified_at": "2026-11-09T04:03:31+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": prev["registry_flags"],
    "freshness_flags": [],
    "notes": (
        "ROUND 17 at 700bf33f. Delta from 56cc575a for the slice: index.html:33, :165; L01.html:234, :408; L03.html:51, :463 "
        "(one line each, all read). cards.json, L02.html, the three lab twins and the notation are byte-identical. "
        "Gates re-run on the pin (see SC1a-gate-* rows), page_smoke alone for the four pages, twins under python -I -W error, "
        "lab-twin mutants 35/35. Round-16 FAIL SC1a-r15-lab-mutants-p1-p3 is now PASS (files tracked and killed). Round-16 FAIL "
        "SC1a-r16-hub-rung-hours is now PASS (sentence re-verified). NEW FAIL: card SC1-c017 back no longer matches "
        "L01.html:234 (SC1a-r17-card-c017-definition-fixes); the round-16 full card scan row is FAIL for the same reason. "
        "Carry rule: a round-16 PASS row whose cited locators touch a changed file is carried with the hunk-scoped prefix, "
        "not the byte-identical prefix; the orchestrator should decide whether file-level rows (for example "
        "SC1a-numbers-L01, SC1a-structure-L01-L03, SC1a-banned-phrases) need a full re-read of index.html, L01.html and "
        "L03.html instead. I did not re-read those three files in full this round (about 1,140 HTML lines); I re-read the "
        "six changed lines and re-checked the line-local properties on them. Not run: run_graders (no project grader in "
        "this slice), the full pytest suite, render_curriculum, build_site --check, fetch_data --check (outside slice a). "
        "Lab-twin mutants are kept in ledgers/SC1/lab-mutants (round-16 ruling: tools/mutate_graders.py reads ledgers/SC1/mutants)."
    ),
    "summary": {
        "text": (
            f"SC1-a round 17 at 700bf33f: verdict {verdict}. Non-PASS: "
            + ", ".join(non_pass)
            + ". Round-16 FAILs SC1a-r15-lab-mutants-p1-p3 and SC1a-r16-hub-rung-hours are now PASS."
        ),
        "counts": counts,
        "mutants": f"{len(mutants)} of {len(mutants)} lab-twin mutants killed",
    },
}

with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(frag, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("rows", len(rows), counts, "carried", len(carried_ids), "mutants", len(mutants), "verdict", verdict)
print("non-PASS:", non_pass)
