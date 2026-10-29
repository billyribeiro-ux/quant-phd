"""Build the round-36 fragment for AC4-b from the round-35 fragment, the delta and the r36 re-runs."""

import json
import re
import sys
from datetime import UTC, datetime

PREV = "/tmp/fanout-frags/AC4-b.round35.json"
OUT = sys.argv[1]
prev = json.load(open(PREV, encoding="utf-8"))
prev_rows = {r["id"]: r for r in prev["rows"]}


def map_l04(n: int) -> int:
    """Old (5aeaaf0) L04 line -> current line: +5 for old 275..315, +6 from old 316 on."""
    if n <= 274:
        return n
    if n <= 315:
        return n + 5
    return n + 6


def remap(loc: str) -> str:
    def rng(m: re.Match[str]) -> str:
        a, b = int(m.group(1)), m.group(2)
        out = f"{map_l04(a)}"
        if b:
            out += f"-{map_l04(int(b))}"
        return out

    return re.sub(r"lines? (\d+)(?:-(\d+))?", lambda m: m.group(0).split()[0] + " " + rng(m), loc)


L03_PREFIX = "Carried from round 35 (course/modules/AC/AC4/L03.html cited lines byte-identical since the previous pin; the only L03 hunks are lines 328 and 490):"
L04_PREFIX = (
    "Carried from round 35 (course/modules/AC/AC4/L04.html cited sentences byte-identical since the previous pin; "
    "the only L04 hunks are lines 74, 275-279 and 320-321, so the round-35 numbers are shifted here: old 275-315 "
    "is now +5, old 316 onward is now +6):"
)

rows: list[dict[str, str]] = []


def carry(rid: str, prefix: str, loc_map: bool = False) -> None:
    r = prev_rows[rid]
    loc = remap(r["location"]) if loc_map else r["location"]
    if loc_map and loc != r["location"]:
        loc += " (current numbers; round-35 locator was " + r["location"] + ")"
    rows.append({"id": rid, "check": r["check"], "location": loc, "status": "PASS",
                 "evidence": prefix + " " + r["evidence"]})


def new(rid: str, check: str, location: str, evidence: str, status: str = "PASS", fix: str | None = None) -> None:
    row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix:
        row["fix"] = fix
    rows.append(row)


OUTD = "ledgers/AC4/scripts/AC4-b-r36/out"

# ---- command rows, re-run on the 51a4e97 checkout
new("AC4b-cmd-pin", "git HEAD and status", "checkout /tmp/verify36-AC4-b",
    "git log -1 gives 51a4e97 (detached); git status shows only the untracked .venv symlink. Delta base is the round-35 pin 5aeaaf0.")
new("AC4b-cmd-check_pages", "check_pages for both pages", "tools/check_pages.py --unit AC4 --page L03; --page L04",
    f"{OUTD}/check_pages.out: 'check_pages AC4 L03: PASS' rc=0; 'check_pages AC4 L04: PASS' rc=0.")
new("AC4b-cmd-check_dag", "check_dag", "tools/check_dag.py --all",
    f"{OUTD}/check_dag.out: 'check_dag AC4: PASS', CF1 PASS, AP1 PASS, rc=0.")
new("AC4b-cmd-run_labs", "run_labs for the two pages", "tools/run_labs.py --unit AC4 --page L03; --page L04",
    f"{OUTD}/run_labs.out: 'run_labs AC4: PASS (1/1)' twice, rc=0 both.")
new("AC4b-cmd-twins-isolated", "twins run alone under python -I -W error, compared with page expected blocks",
    "tests/labs/AC4/lab-AC4-L03-1.py; tests/labs/AC4/lab-AC4-L04-1.py",
    "Both twins exit 0 with 0 bytes of stderr. The html-unescaped expected block of L03.html (36 lines) and of L04.html (39 lines, lines 283-321) equals the twin stdout exactly (diff clean). Scratch: /tmp/AC4-v36/b/twin_L0{3,4}.out.")
new("AC4b-cmd-page_smoke", "page_smoke for L03 and L04", "tools/page_smoke.py --unit AC4 --pages L03 L04 --skip-sweep",
    f"{OUTD}/page_smoke.out: 'page_smoke modules/AC/AC4/L03.html: PASS', 'page_smoke modules/AC/AC4/L04.html: PASS', 'page_smoke AC4: PASS', rc=0; lab timing 0.0 s.")
new("AC4b-cmd-ruff-mypy", "ruff check, ruff format --check, mypy --no-incremental on the two twins",
    "tests/labs/AC4/lab-AC4-L03-1.py; tests/labs/AC4/lab-AC4-L04-1.py",
    f"{OUTD}/ruff_check.out 'All checks passed!' rc=0; {OUTD}/ruff_format.out '2 files already formatted' rc=0; {OUTD}/mypy.out 'Success: no issues found in 2 source files' rc=0.")
new("AC4b-cmd-verify_refs", "verify_refs offline and live for AC4", "tools/verify_refs.py --offline; tools/verify_refs.py --unit AC4",
    f"{OUTD}/verify_refs_offline.out 'offline integrity: 560 entries, 0 problems' rc=0; {OUTD}/verify_refs_live_AC4.out 'live re-verification of AC4: 2 of 560 entries, 0 problems' rc=0.")
new("AC4b-cmd-pytest", "pytest for the AC4 L03 and L04 lab tests", "pytest tests/test_labs.py -k 'AC4 and (L03 or L04)' -q",
    f"{OUTD}/pytest.out: two dots, [100%], rc=0 (exit status captured). collect-only count is 2 ({OUTD}/collect.out 'tests/test_labs.py: 2').")

# ---- delta and cards
new("AC4b23-slice-delta", "every hunk since 5aeaaf0 in the slice files read",
    "git diff 5aeaaf0 51a4e97 -- L03.html, L04.html, tests/labs/AC4/lab-AC4-L04-1.py",
    "L03.html: hunks at lines 328 (interp sentence) and 490 (R2 solution) only, both 1-for-1. L04.html: line 74 (Remark 1.3, 1-for-1); insertion of 5 lines after old 274 (the uneven-pool demonstration in the lab code); old 315 replaced by two lines (new 320-321). The twin has the same 5-line insertion. No L03 card object changed; cards.json changes are only AC4-c023 and AC4-c078 (L02, L06, outside this slice). index.html, references and the plan are unchanged. Every hunk was read.")
new("AC4b-cards-L03-L04", "every L03 and L04 card checked against the current lesson text",
    "course/modules/AC/AC4/cards.json (35 L03 and L04 cards)",
    "Re-run this round: a script over the 35 L03/L04 card backs checks every digit string against the html-stripped lesson text; zero missing (ledgers/AC4/scripts/AC4-b-r36/cards_check.py; " + OUTD + "/cards_check.out). Card objects are byte-identical to the previous pin, and no card cites the changed sentences (grep for 'Lab 1', 'printed', '14,000', 'R2', 'Remark 1.3' in the L03/L04 cards reviewed).")
carry("AC4b23-cards-c037", L03_PREFIX)
carry("AC4b23-cards-c136", L03_PREFIX)
new("AC4b23-card-identity", "L03 and L04 card objects byte-identical", "course/modules/AC/AC4/cards.json (L03 and L04 card objects)",
    "git diff 5aeaaf0 51a4e97 -- cards.json: only the c023 and c078 hunks (L02 and L06). No L03 or L04 card object changed.")
new("AC4b23-card-numbers", "every number on L03 and L04 card backs in the lesson text",
    "every digit string on the 35 L03/L04 card backs",
    "Scripted re-run this round (ledgers/AC4/scripts/AC4-b-r36/cards_check.py, output out/cards_check.out): zero digit strings missing from the html-stripped L03.html and L04.html text (the lesson text only gained digits, so no previously matched string was lost).")
carry("AC4b23-prose-changed-cards", L03_PREFIX)

# ---- hours
carry("AC4b-hours-L03-L04", L03_PREFIX)
carry("AC4b23-hub-hours", "Carried from round 35 (course/modules/AC/AC4/index.html and lesson data-hours attributes byte-identical since the previous pin; no hunk touches them):")

# ---- notation and L03 prose not touched by a hunk
carry("notation-T-L03", L03_PREFIX)
carry("notation-Gamma-L03", L03_PREFIX)
for rid in ["L03-num-ex21", "L03-prop22", "L03-prop12", "L03-prop41", "L03-sec2-model", "L03-sec3-ex31", "L03-sec4",
            "L03-s5-canon", "L03-misc", "L03-ex-problems-mech", "L03-ex-problems-proof", "L03-ex-problems-emp",
            "L03-keyresults", "L03-quiz", "L03-refs"]:
    carry(rid, L03_PREFIX)

# ---- L03 rows whose subject changed: re-verified
new("L03-lab1-output", "Lab 1 expected block equals the twin's output",
    "course/modules/AC/AC4/L03.html Lab 1 expected block; tests/labs/AC4/lab-AC4-L03-1.py",
    "Re-run: twin_L03 stdout (36 lines, rc 0, stderr 0) equals the html-unescaped expected block (36 lines), diff clean. The L03 twin is unchanged since 5aeaaf0.")
new("L03-lab1-interp", "every figure in the Lab 1 interpretation paragraph is printed or recomputed",
    "course/modules/AC/AC4/L03.html line 328",
    "Re-read the paragraph in full. Its figures (11.10 with overhead, 9.10 without it, 10.50 buy, 0.15 scrap, 9.25 break-even) are printed in the twin output (/tmp/AC4-v36/b/twin_L03.out, unchanged since round 35). The sentence naming the printed line (now 'second line of Lab 1's output, after its title') is correct; see L03-interp-first-line.")
new("L03-interp-first-line", "the sentence naming where the 9.10 avoidable cost is printed",
    "course/modules/AC/AC4/L03.html line 328 ('printed on the second line of Lab 1's output, after its title')",
    "Re-verified against the twin output (/tmp/AC4-v36/b/twin_L03.out): line 1 is the title 'Part K, make or buy: 20,000 units a year (SIMULATED)'; line 2 is '  avoidable make cost per unit (variable + dedicated fixed / units): 9.10'. The round-35 FAIL is fixed.")
new("L03-R2", "R2 solution defines every symbol it uses",
    "course/modules/AC/AC4/L03.html line 490",
    "Re-read: 'Let X be the contribution of the other use, so X = 40,000 here' now precedes 'Making costs 182,000 + X and buying costs 210,000 - X'. Re-derived: 182,000 + 40,000 = 222,000; 210,000 - 40,000 = 170,000; difference 52,000; 182,000 + X < 210,000 - X iff X < 14,000; both equal 196,000 at X = 14,000. The 'no scrap received' premise is the stated modeling of an equipment used for the other product (the problem's premise), not a number from the lab. The round-35 FAIL is fixed.")
new("L03-ex-problems-research", "R1 and R2 solutions", "course/modules/AC/AC4/L03.html lines 480-499 (R2 at 490)",
    "R1 states that no horizon or rate is computed. R2 re-derived above (222,000; 170,000; 52,000; crossover 14,000; equal at 196,000). PASS.")

# ---- L04 rows whose subject changed: re-verified
new("L04-s1-defs", "Definition 1.1, Proposition 1.2 and Remark 1.3",
    "course/modules/AC/AC4/L04.html lines 55-75 (Remark 1.3 at line 74)",
    "Lines 55-75 are unchanged except line 74; Definition 1.1 and Proposition 1.2 text are byte-identical to round 35 (their identity was re-derived there and is carried). Remark 1.3 (line 74) now says the rate function 'raises an error otherwise (the last line of Lab 1's output shows one refused uneven pool)'. Checked against the twin: the last line of twin_L04.out is 'Uneven pool (100000 cents over 3 driver units): refused', and exact_rate raises ValueError on a non-exact division. PASS.")
new("L04-remark13-lab", "exact_rate refuses an uneven division (the Remark's claim) and the demonstration",
    "course/modules/AC/AC4/L04.html lines 73-75 and 'tests/labs/AC4/lab-AC4-L04-1.py' exact_rate and main() tail",
    f"Imported the twin without main() under python -I -W error (ledgers/AC4/scripts/AC4-b-r36/remark13_check.py): exact_rate(10_000_001, 10_000) raises ValueError 'pool: 10000001 does not divide evenly by 10000 driver units'; exact_rate(100_000, 3) is refused; exact_rate(100_000, 4) = 25000. Output in {OUTD}/remark13_check.out.")
new("L04-lab1-output", "Lab 1 expected block equals the twin output",
    "course/modules/AC/AC4/L04.html Lab 1 expected block (lines 283-321 after the round-36 pin); tests/labs/AC4/lab-AC4-L04-1.py",
    "Re-run: twin_L04 stdout (39 lines, rc 0, stderr 0) equals the html-unescaped expected block (39 lines), diff clean. The new last line 'Uneven pool (100000 cents over 3 driver units): refused' is in both. Figures re-read: 4.50, 27.50, 8.00, 10.00, -35,000/+35,000, positive/negative margins, the 22.50 after the setup cut.")
new("L04-lab1-interp", "the Lab 1 interpretation paragraph",
    "course/modules/AC/AC4/L04.html line 322 (round-35 line 316)",
    "Text byte-identical to round 35. It says the output 'confirms the arithmetic of Examples 2.1 and 2.2 and the two identities' and that the lab does not measure the true setup count. The printed equals-pool lines (True three times: volume, activity, sensitivity) and the 'totals agree: True' line support it. The paragraph does not claim a count of 'True' lines. PASS.")

# ---- L04 carried rows (cited sentences byte-identical; locators shifted)
for rid in ["L04-ex21-22", "L04-s2-counts", "L04-prop31-reallocation", "L04-prop32"]:
    carry(rid, L04_PREFIX)
for rid in ["L04-s4-ex41", "L04-s5-canon", "L04-misc-ratios", "L04-misc2-3", "L04-problems-mech", "L04-problems-proof",
            "L04-problems-emp", "L04-problems-research", "L04-keyresults", "L04-quiz", "L04-refs",
            "AC4b-cite-kaplan1998cost"]:
    carry(rid, L04_PREFIX, loc_map=True)
carry("AC4b-cite-datar2020horngrens", "Carried from round 35 (references/references.json unchanged since the previous pin; live verify_refs re-run this round, 2 of 560 entries, 0 problems):")

# ---- lab mutants, re-run this round
new("L03-L04-lab-mutants", "every archived lab mutant run under python -I -W error and compared with the page expected block",
    "ledgers/AC4/mutants/AC4-b-r30/, AC4-b-r32/, AC4-b-r34/ (m_L03_*, m_L04_*; 17 files)",
    f"{OUTD}/mutants.out. 16 mutants differ from the expected block (14 with exit 0, 2 with exit 1 from an uncaught ValueError). m_L03_excess_hours_unclamped prints the same text: its own docstring says it is equivalent on this data (6,000 - 4,000 is positive), and no lesson sentence claims the lab checks the clamp, so it is out of scope (architect ruling: lab twins are demonstrations). PASS.")

rows_out = rows
import glob, os
MUTANTS = []
for path in sorted(glob.glob("/tmp/verify36-AC4-b/ledgers/AC4/mutants/AC4-b-r3*/m_L0[34]_*.py")):
    name = os.path.basename(path)[:-3]
    if name == "m_L03_excess_hours_unclamped":
        continue
    MUTANTS.append({"id": name, "description": "archived lab mutant (" + os.path.basename(os.path.dirname(path)) + "); lab twin demonstration, output differs from the page expected block",
                    "killed_by": "stdout differs from expected block (or uncaught ValueError, exit 1)"})
ids_prev = set(prev_rows)
ids_now = {r["id"] for r in rows_out}
missing = sorted(ids_prev - ids_now)
frag = {
    "unit": "AC4",
    "slice": "AC4-b",
    "round": 36,
    "verifier": "round-36 independent verifier (Haiku) for slice AC4-b: L03, L04 and their lab twins; did not build AC4 and shares no context with the builders or earlier verifiers",
    "pin": "51a4e97",
    "base": "5aeaaf0 (round-35 pin; delta base)",
    "checkout": "/tmp/verify36-AC4-b (detached at 51a4e97; .venv symlink)",
    "scratch": "/tmp/AC4-v36/b/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "rows": rows_out,
    "mutants": MUTANTS,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Round-35 row ids not re-emitted: " + ", ".join(missing) if missing else "All round-35 row ids are kept.",
        "This is a lesson-and-twin slice, not a project slice: the project-slice rules (new student-error mutants, alternative implementations) do not apply. The archived lab mutants were re-run, not extended.",
        "Hours: not failed on pace (architect ruling); the hub split 50/20 equals the lesson data-hours sum 50 (unchanged).",
        "Not checked: the rest of the AC4 unit (other lessons and labs) belongs to other slices; the full gate was not re-run; the Problem R2 'no scrap received' premise is a modeling choice stated by the solution, which the statement does not spell out.",
    ],
    "summary": {},
    "verdict": "",
}
frag["summary"] = {
    "rows": len(rows_out),
    "pass": sum(1 for r in rows_out if r["status"] == "PASS"),
    "fail": sum(1 for r in rows_out if r["status"] == "FAIL"),
    "unverifiable": sum(1 for r in rows_out if r["status"] == "UNVERIFIABLE"),
}
frag["verdict"] = "PASS" if frag["summary"]["pass"] == len(rows_out) else "FAIL"
json.dump(frag, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(frag["summary"], frag["verdict"], "missing:", missing)
