"""Build ledgers/PC3/PC3-c.json (round 1, closing delta of slice c) from the base round-18 fragment.

Rows re-verified this round carry fresh evidence (command outputs under ledgers/PC3/scripts/PC3-c-r1/out/).
Every other base row is carried with the carry prefix. Row ids are kept.
"""

import datetime
import json
import re
import sys
from pathlib import Path

REPO = Path("/Users/billyribeiro/.fanout/wt/verifyF31-PC3-c")
OUT = REPO / "ledgers/PC3/scripts/PC3-c-r1/out"
BASE = Path("/Users/billyribeiro/.fanout/frags/E-PC3-c.round18.json")
FRAG = REPO / "ledgers/PC3/PC3-c.json"

base = json.loads(BASE.read_text(encoding="utf-8"))
base_rows = {r["id"]: r for r in base["rows"]}

CARRY = (
    "Carried from round 18 (cited subject byte-identical since the previous pin 50559266: "
    "git diff --quiet 50559266 95f3f8cb is empty for course/modules/PC/PC3/project.html, grader/, "
    "tests/labs/PC3, plans/PC3-build-plan.md, course/modules/PC/PC3/index.html, ledgers/PC3/alternatives, "
    "ledgers/PC3/mutants except r18_01..03, tools/, notation/, references/, course/assets/; "
    "the evidence artifacts under ledgers/PC3/scripts/PC3-c-r18/out were committed after the pin and are cited as base evidence): "
)

# Parse the 92-mutant run.
mut_lines = (OUT / "mutate_pc3_0_49.out").read_text(encoding="utf-8").splitlines()
mutants = []
for line in mut_lines:
    m = re.match(r"^(KILLED|SURVIVED|ERROR) (\S+?): (.*) -> (.*)$", line)
    if m:
        mutants.append({
            "name": m.group(2),
            "description": m.group(3),
            "killed_by": m.group(4) + " (seeds 0-49, tools/mutate_graders.py --unit PC3)",
            "status": m.group(1),
        })
kill_map = {m["name"]: m for m in mutants}


def killed(prefix: str) -> list[str]:
    hits = [n for n in kill_map if n.startswith(prefix)]
    bad = [n for n in hits if kill_map[n]["status"] != "KILLED"]
    if bad:
        raise SystemExit(f"not killed: {bad}")
    return hits


m_all = killed("m")
v_all = [n for n in kill_map if re.match(r"^v\d\d_", n)]
assert len(mutants) == 92 and all(m["status"] == "KILLED" for m in mutants), len(mutants)
mut_m = [n for n in kill_map if re.match(r"^m\d\d_", n)]
mut_v = [n for n in kill_map if re.match(r"^v\d\d_", n) and not n.startswith("v17_")]
mut_r14 = [n for n in kill_map if n.startswith(("r13_", "r14_", "s14_"))]
assert len(mut_m) == 10 and len(mut_v) == 48 and len(mut_r14) == 12, (len(mut_m), len(mut_v), len(mut_r14))
r18 = [n for n in kill_map if n.startswith("r18_")]
assert len(r18) == 3

# Lesson-4 hrefs in project.html must resolve to ids present in L04.html at HEAD.
proj = (REPO / "course/modules/PC/PC3/project.html").read_text(encoding="utf-8")
l04 = (REPO / "course/modules/PC/PC3/L04.html").read_text(encoding="utf-8")
l04_ids = set(re.findall(r'\bid="([^"]+)"', l04))
l04_hrefs = sorted(set(re.findall(r'href="L04\.html(#[^"]*)?"', proj)))
frag_targets = [h for h in re.findall(r'href="L04\.html#([^"]+)"', proj)]
assert all(t in l04_ids for t in frag_targets), frag_targets
assert "def-market-making-game" in l04_ids

FRESH = {}

FRESH["proj-rubric-c4-real-form-undefined"] = dict(
    location=(
        "course/modules/PC/PC3/project.html line 626 (C4 level 4) against course/modules/PC/PC3/L04.html "
        "line 484 (the queue and learning sentence; the base locator 'line 482' is the section 5 heading at HEAD)"
    ),
    evidence=(
        "Fresh, round 1 (pin 95f3f8cb). project.html line 626 (C4 level 4) says the model leaves out 'the queue of "
        "resting orders and a trader who learns from the fills, both set aside in Lesson 4, latency, more than one "
        "asset'. L04.html line 484 reads 'this game does not model that queue' and 'Proposition 3.1 does not cover a "
        "trader who learns from the fills, and this lesson does not model learning'. L04.html line 482 is the "
        "section 5 heading (sed -n 482p), so the base locator was stale by two lines. Latency and more than one asset "
        "are not stated as set aside in Lesson 4 (grep -i 'latency|one asset' over L04.html: no match); the "
        "parenthesis attaches 'set aside in Lesson 4' to the queue and learning items only. The only L04 change in "
        "50559266..95f3f8cb is line 127 (git diff), which is outside the cited lines."
    ),
)

FRESH["proj-r14-l04-cited-sentences"] = dict(
    location=(
        "course/modules/PC/PC3/L04.html line 60 (anchor def-market-making-game), line 484 (the 'queue of resting "
        "orders' and 'this lesson does not model learning' sentences); project.html line 37 and rubric line 626"
    ),
    evidence=(
        "Fresh, round 1. sed -n 60p L04.html: <dfn id=\"def-market-making-game\" data-concept=\"market-making-game\">. "
        "sed -n 484p L04.html contains 'the queue of resting orders at each price, and this game does not model that "
        "queue' and 'this lesson does not model learning'. project.html line 626 cites Lesson 4 for the same two "
        "items. The cited lines are byte-identical to the pin (git diff 50559266..HEAD changes only L04.html line 127)."
    ),
)

FRESH["proj-dag-terms"] = dict(
    location="course/modules/PC/PC3/project.html line 37 (concept link market-making-game) against course/modules/PC/PC3/L04.html line 60",
    evidence=(
        "Fresh, round 1. check_dag PASS (out/check_dag_unit.out: 'check_dag PC3: PASS', EXIT=0). L04.html line 60 "
        "defines def-market-making-game (see proj-r14-l04-cited-sentences); project.html line 37 links "
        "L04.html#def-market-making-game (grep href), and the id is present in L04.html."
    ),
)

FRESH["proj-r16-mutants-76"] = dict(
    location=(
        "ledgers/PC3/mutants/ (92 files at HEAD 95f3f8cb; 89 committed at pin 50559266, the three r18_01..03 files "
        "were added in the delta); course/modules/PC/PC3/grader/test_project.py; out/mutate_pc3_0_49.out"
    ),
    evidence=(
        "Fresh, round 1. tools/mutate_graders.py --unit PC3 --seeds 0-49 over all 92 files at HEAD: 92 KILLED, 0 "
        "SURVIVED, 0 ERROR (out/mutate_pc3_0_49.out, last line 'mutate_graders PC3: PASS (92/92 killed)'). "
        "Locator correction: the base row said '92 files at 50559266', but git ls-tree shows 89 mutant files at pin "
        "50559266; ls ledgers/PC3/mutants gives 92 at HEAD."
    ),
)

for rid, fn, desc in [
    ("proj-r18-mutant-r18_01", "r18_01", "replay re-plays the game from log seed, ignoring logged fills"),
    ("proj-r18-mutant-r18_02", "r18_02", "replay books every informed fill as a purchase"),
    ("proj-r18-mutant-r18_03", "r18_03", "replay marks the ending inventory at settlement minus start value"),
]:
    name = next(n for n in kill_map if n.startswith(fn + "_"))
    FRESH[rid] = dict(
        location=f"ledgers/PC3/mutants/{name}; course/modules/PC/PC3/grader/test_project.py",
        evidence=(
            f"Fresh, round 1. Mutant file exists at HEAD and was not in the pin (git ls-tree 50559266 shows none). "
            f"Description ({desc}) matches its docstring (sed -n 1p). Full-suite run: 'KILLED {name}' with killed_by "
            f"'{kill_map[name]['killed_by'].split(' (seeds')[0]}' (out/mutate_pc3_0_49.out). Candidate runs of this "
            f"round (out/candidates_r18_seeds_r1.out): seed 0 and seed 77314143 both exit 1 "
            f"(see the failed-test counts there). Not survived."
        ),
    )

FRESH["proj-r18-alternatives-new"] = dict(
    location="ledgers/PC3/scripts/PC3-c-r18/alt_r18_1_skew_and_size.py, alt_r18_2_mean_of_last_three_fills.py, alt_r18_3_never_quotes.py",
    evidence=(
        "Fresh, round 1 (out/candidates_r18_seeds_r1.out, scratch copy of grader engine, instance, test_project and the "
        "candidate as market_maker.py, python -I -m pytest -W error): alt_r18_1, alt_r18_2 and alt_r18_3 exit 0 with "
        "489 passed on seed 0 and 498 passed on seed 77314143."
    ),
)

FRESH["proj-r18-fill-side-by-price-equivalence"] = dict(
    location="course/modules/PC/PC3/grader/reference.py replay side rule; course/modules/PC/PC3/project.html line 397 and Conventions; ledgers/PC3/scripts/PC3-c-r18/alt_r18_1_skew_and_size.py",
    evidence=(
        "Fresh, round 1. The side-from-price candidate alt_r18_1 passes seeds 0 and 77314143 (489 and 498 passed; "
        "out/candidates_r18_seeds_r1.out). The arrival-based replay r17_02 is KILLED by "
        "test_a_fill_takes_its_side_from_its_price_not_its_arrival[uninformed-buy-False] (out/mutate_pc3_0_49.out). "
        "reference.py exits 0 on both seeds (out/candidates_r18_seeds_r1.out)."
    ),
)

FRESH["proj-r16-alternatives-prior-52"] = dict(
    location="52 prior candidate modules listed in ledgers/PC3/scripts/PC3-c-r18/out/candidate_modules_r18.txt (ledgers/PC3/alternatives/alt1..alt6 and the round-16 and round-18 modules)",
    evidence=(
        "Fresh, round 1. Each of the 52 listed files was run against the grader suite on seed 0 and on seed 77314143 "
        "(ledgers/PC3/scripts/PC3-c-r1/run_prior52_r1.sh; out/prior52_seeds_r1.out): 104 of 104 runs exit 0."
    ),
)

gate_fresh = (
    "Fresh, round 1 (checkout 95f3f8cb, gates_r1.sh). "
)
FRESH["proj-check-tools"] = dict(
    location="tools/check_pages.py --unit PC3; tools/check_dag.py --unit PC3; tools/check_projects.py --unit PC3; tools/run_labs.py --unit PC3 --page project",
    evidence=gate_fresh + "check_pages PC3: PASS (out/check_pages_unit.out); check_dag PC3: PASS (out/check_dag_unit.out); check_projects PC3: PASS (out/check_projects_unit.out); run_labs PC3: PASS (3/3) (out/run_labs_project.out). Each EXIT=0. The project-only check_pages run is recorded under the notes (tool scope)."
)
FRESH["proj-r8-check-tools"] = dict(FRESH["proj-check-tools"])
FRESH["proj-r15-gates"] = dict(
    location=FRESH["proj-check-tools"]["location"] + "; tools/run_graders.py --unit PC3 --seeds 0-49",
    evidence=gate_fresh + "check_pages, check_dag, check_projects PASS and run_labs 3/3 PASS (out/*.out, EXIT=0); run_graders PC3: PASS, reference 50/50 seeds (out/run_graders_0_49.out).",
)
FRESH["proj-r17-gates"] = dict(
    location="ledgers/PC3/scripts/PC3-c-r1/gates_r1.sh (re-run of the round-18 gate set, plus run_candidates_r1.sh and mutate_graders)",
    evidence=gate_fresh + "The full slice gate set ran on this checkout: out/driver.log lists every command with its EXIT code; all EXIT=0 except check_pages --page project (tool scope, see notes) and verify_refs --unit (usage error, offline mode, see notes), which are not gates.",
)
FRESH["proj-run-labs-unit"] = dict(
    location="tools/run_labs.py --unit PC3 --page project",
    evidence=gate_fresh + "run_labs PC3: PASS (3/3) (out/run_labs_project.out, EXIT=0).",
)
FRESH["proj-r8-run-labs-page-smoke"] = dict(
    location="tools/run_labs.py --unit PC3 --page project; tools/page_smoke.py --unit PC3 --pages project",
    evidence=gate_fresh + "run_labs PC3: PASS (3/3); page_smoke PC3: PASS, with 'All 498 tests pass on seed 1097350607' in the in-browser grader line (out/page_smoke_project.out).",
)
FRESH["proj-page-smoke"] = dict(
    location="tools/page_smoke.py --unit PC3 --pages project (course/modules/PC/PC3/project.html)",
    evidence=gate_fresh + "page_smoke modules/PC/PC3/project.html: PASS; page_smoke PC3: PASS (out/page_smoke_project.out, EXIT=0).",
)
FRESH["proj-lint-ruff"] = dict(
    location="ruff check and ruff format --check on course/modules/PC/PC3, tests/labs/PC3, ledgers/PC3",
    evidence=gate_fresh + "ruff check: 'All checks passed!' (out/ruff_check_slice.out, EXIT=0); ruff format --check: '14 files already formatted' (out/ruff_format_slice.out, EXIT=0).",
)
FRESH["proj-r14-lint-mypy-pytest"] = dict(
    location="ruff; repo mypy; pytest on PC3 selections",
    evidence=gate_fresh + "ruff check PASS; mypy --no-incremental: 'Success: no issues found in 386 source files' (out/mypy_repo.out, EXIT=0); pytest tests/test_labs.py tests/test_page_checks.py tests/test_run_labs.py tests/test_page_smoke.py -k PC3: exit 0 (out/pytest_pc3.out).",
)
FRESH["proj-mypy-labs"] = dict(
    location="tests/labs/PC3 twins; repo mypy",
    evidence=gate_fresh + "mypy --no-incremental over the repo: 'Success: no issues found in 386 source files' (out/mypy_repo.out, EXIT=0).",
)
FRESH["proj-grader-mypy-strict"] = dict(
    location="course/modules/PC/PC3/grader/engine.py, instance.py, test_project.py, market_maker.py (= reference.py)",
    evidence=gate_fresh + "mypy --strict --no-incremental on engine.py, instance.py, market_maker.py (reference.py) and test_project.py in a scratch copy: 'Success: no issues found in 4 source files', EXIT=0 (out/mypy_grader_strict_r1.out, script mypy_grader_r1.sh).",
)
FRESH["proj-r15-mypy-strict-grader"] = dict(FRESH["proj-grader-mypy-strict"], location=FRESH["proj-grader-mypy-strict"]["location"])
FRESH["proj-r16-grader-mypy-note"] = dict(FRESH["proj-grader-mypy-strict"], location=FRESH["proj-grader-mypy-strict"]["location"])
FRESH["proj-r8-pytest-pc3"] = dict(
    location="tests/test_labs.py -k PC3; tests/test_page_checks.py -k PC3; tests/test_run_labs.py; tests/test_page_smoke.py",
    evidence=gate_fresh + "pytest over those four files: exit 0 (out/pytest_pc3.out).",
)
FRESH["proj-grader-reference"] = dict(
    location="course/modules/PC/PC3/grader/reference.py via tools/run_graders.py --unit PC3 --seeds 0-49",
    evidence=gate_fresh + "run_graders PC3: PASS, reference 50/50 seeds, slowest 0.6 s (out/run_graders_0_49.out, EXIT=0). reference.py also exits 0 on seeds 0 and 77314143 (out/candidates_r18_seeds_r1.out).",
)
FRESH["proj-grader-starter-fails"] = dict(
    location="course/modules/PC/PC3/grader/starter.py with test_project.py in a scratch copy (seeds 0 and 77314143)",
    evidence=gate_fresh + "starter.py exit 1 on seed 0 (423 failed, 66 passed) and on seed 77314143 (431 failed, 67 passed), with NotImplementedError in test_quotes_are_legal_on_every_turn (out/candidates_r18_seeds_r1.out).",
)
FRESH["proj-r15-starter-fails"] = dict(FRESH["proj-grader-starter-fails"])
FRESH["proj-r16-reference-collect-and-starter"] = dict(
    location="course/modules/PC/PC3/grader/test_project.py; grader/reference.py; grader/starter.py",
    evidence=gate_fresh + "collect-only: 489 tests on seed 0 and 498 on seed 77314143 (out/collect_only_r1.out); reference.py passes both (out/candidates_r18_seeds_r1.out); starter.py fails both.",
)
FRESH["proj-r8-collect-counts"] = dict(
    location="course/modules/PC/PC3/grader/test_project.py (collect-only, seeds 0 and 77314143)",
    evidence=gate_fresh + "pytest --collect-only: '489 tests collected' for seed 0 and '498 tests collected' for seed 77314143 (out/collect_only_r1.out).",
)
FRESH["proj-r8-verify-refs"] = dict(
    location="tools/verify_refs.py --offline (all entries); tools/verify_refs.py --unit PC3 (live, carried)",
    evidence=gate_fresh + "tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' (out/verify_refs_offline_all.out, EXIT=0). The live --unit PC3 run is not repeated: it needs network, and references/ is byte-identical since the pin, so its base output (ledgers/PC3/scripts/PC3-c-r18/out/verify_refs_live_pc3.out) is carried.",
)
FRESH["proj-builder-mutants"] = dict(
    location="ledgers/PC3/mutants/m01..m10",
    evidence=gate_fresh + "tools/mutate_graders.py --unit PC3 --seeds 0-49: " + ", ".join(sorted(mut_m)) + " all KILLED (out/mutate_pc3_0_49.out).",
)
FRESH["proj-verifier-mutants"] = dict(
    location="ledgers/PC3/mutants/v01..v16 and v18..v26 (v17 absent)",
    evidence=gate_fresh + "tools/mutate_graders.py --unit PC3 --seeds 0-49: the 48 v-files v01..v49 without v17 are all KILLED (out/mutate_pc3_0_49.out). v17 is absent from ledgers/PC3/mutants (ls).",
)
FRESH["proj-r14-mutants-aggregate"] = dict(
    location="ledgers/PC3/mutants/ (the 70 files that existed at pin d1e65a0: m01-m10, v01-v49 without v17, r13_01-05, r14_01-04, s14_01-03)",
    evidence=gate_fresh + "all 70 named files are KILLED in out/mutate_pc3_0_49.out (10 m, 48 v, 5 r13, 4 r14, 3 s14).",
)
FRESH["proj-r16-links-anchors"] = dict(
    location="course/modules/PC/PC3/project.html (href values); L04.html ids",
    evidence=(
        "Fresh, round 1. Targets of project.html hrefs to L04.html: " + ", ".join(l04_hrefs) + ". Every fragment "
        "target (" + ", ".join(sorted(set(frag_targets))) + ") is an id present in L04.html (checked by script, "
        "ledgers/PC3/scripts/PC3-c-r1/build_fragment_r1.py). L04.html has no id removed or renamed since the pin "
        "(git diff 50559266..HEAD changes one text line, 127). Other href targets are unchanged files."
    ),
)

# Carried rows keep their base evidence under the carry prefix.
rows = []
fresh_ids = []
for rid, r in base_rows.items():
    if rid in FRESH:
        fr = FRESH[rid]
        rows.append({
            "id": rid,
            "check": r["check"],
            "location": fr["location"],
            "status": "PASS",
            "evidence": fr["evidence"],
        })
        fresh_ids.append(rid)
    else:
        assert r["status"] == "PASS", rid
        rows.append({
            "id": rid,
            "check": r["check"],
            "location": r["location"],
            "status": "PASS",
            "evidence": CARRY + r["evidence"],
        })

assert len(rows) == len(base_rows) == 167
assert set(FRESH) <= set(base_rows), set(FRESH) - set(base_rows)

counts = {"PASS": sum(r["status"] == "PASS" for r in rows)}
verdict = "PASS" if counts["PASS"] == len(rows) and len(mutants) == 92 and all(m["status"] == "KILLED" for m in mutants) else "FAIL"

fragment = {
    "unit": "PC3",
    "slice": "c",
    "round": 1,
    "verifier": "independent verifier (Haiku 5.5), closing delta round 1, slice c; did not build PC3; exemplar scoring not performed here (ruling 23: dedicated blind scorer, ~/.fanout/blind/PC3-c.json cited)",
    "pin": "95f3f8cb",
    "base": "round 18 fragment /Users/billyribeiro/.fanout/frags/E-PC3-c.round18.json (pin 50559266); delta 50559266..95f3f8cb for this slice",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyF31-PC3-c (detached at 95f3f8cb; .venv symlinked to the repo venv; course/assets/vendor present)",
    "scratch": "ledgers/PC3/scripts/PC3-c-r1/ (gates_r1.sh, run_candidates_r1.sh, run_r18_cands_r1.sh, run_prior52_r1.sh, mypy_grader_r1.sh, build_fragment_r1.py, out/)",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "verdict": verdict,
    "rows": rows,
    "mutants": [{"name": m["name"], "description": m["description"], "killed_by": m["killed_by"]} for m in mutants],
    "registry_flags": [],
    "freshness_flags": [
        "course/modules/PC/PC3/L04.html: the base row proj-rubric-c4-real-form-undefined cites line 482; the queue sentence is at line 484 (482 is the section 5 heading). Corrected in this round.",
        "ledgers/PC3/mutants: the base row proj-r16-mutants-76 says '92 files at 50559266'; 89 were committed at 50559266 (r18_01..03 added in the delta). Corrected in this round.",
        "The base row proj-r8-verify-refs live part and the base scratch outputs under ledgers/PC3/scripts/PC3-c-r18/out were committed after the pin and are carried as base evidence, not regenerated.",
    ],
    "notes": [
        "Scope (ruling 30, closing delta): slice sources byte-identical 50559266..95f3f8cb (git diff --quiet): course/modules/PC/PC3/project.html, grader/ (engine, instance, reference, starter, test_project), tests/labs/PC3 (twins), plans/PC3-build-plan.md, course/modules/PC/PC3/index.html, ledgers/PC3/alternatives, ledgers/PC3/mutants except r18_01..03, and the shared tools/, notation/, references/, course/assets/, BUILDER_RULES.md, VERIFIER_RULES.md, BLUEPRINT.md. Changed in the delta and relevant to slice c: course/modules/PC/PC3/L04.html (one sentence, line 127, 'Proposition 3.1 and Example 3.2 use it') and ledgers/PC3/mutants/r18_01..03 (added in the delta). course/modules/PC/PC3/cards.json changed (cards PC3-c067 and PC3-c191); base notes place cards outside slice c, so they were not re-verified here.",
        "Re-verified from scratch: every row whose cited subject changed (L04-citing rows, the three r18 mutants, the r18 alternatives, the mutant-directory count row) and the gate rows (all re-run on 95f3f8cb). All other rows carried with the carry prefix. No non-PASS row existed in the base (167 PASS), so none needed re-verification as a non-PASS row.",
        "Ruling 37: no new mutants were written in this round. The standing set of 92 files was run (92/92 KILLED, seeds 0-49). The candidate runners only copy the existing files.",
        "Ruling 26 kinds checked on the changed subjects: false or unproved math, missing hypothesis, wrong number, over-graded claim, failing gate, surviving non-equivalent mutant, lab statement the code does not support. None found on the changed subjects.",
        "Observation (not a row; slice b scope): L04.html line 127 names Proposition 3.1 and Example 3.2 as using x^+. Both do (L04 lines 131-140 and 145). Corollary 3.3's proof (L04 line 155, (b-v)^+ = 0) also uses it; the sentence does not say 'only', so it is not false.",
        "Observation (tool scope): check_pages.py --unit PC3 --page project exits 1 with 11 lesson-rule problems (out/check_pages_project.out, identical to the base output). tools/check_pages.py line 25 says project pages are checked by check_projects.py, and the unit-wide check_pages run passes (out/check_pages_unit.out). Not counted as a FAIL.",
        "Observation (tool scope): tools/verify_refs.py --unit is a live-run flag; with --offline it exits 2 (out/verify_refs_offline_pc3.out is from the base; this round ran --offline with no unit, 560 entries, 0 problems).",
        "Exemplar calibration (ruling 23): not scored by this verifier and no exemplar rows are in this fragment. The dedicated blind scorer file is ~/.fanout/blind/PC3-c.json (A: C1..C5 = 4,4,4,3,4; B: 2,2,1,2,1; its notes say it was scored from /tmp/blind_PC3 outputs only). Comparison to the official exemplar scores was not made here: that needs the exemplar annotations (project.html lines 632-694), which this verifier did not read. PC3 has no entry in plans/KNOWN-ISSUES.md.",
        "Mutation: 92 of 92 KILLED on seeds 0-49 (out/mutate_pc3_0_49.out). Candidate tests this round: r18_01..03 exit 1 on seeds 0 and 77314143; alt_r18_1..3 exit 0; 52 prior candidates exit 0 on both seeds (104 of 104).",
        "Gates this round (all on 95f3f8cb): check_pages unit PASS; check_dag PASS; check_projects PASS; run_labs PC3 3/3 PASS; run_graders PC3 50/50 PASS; page_smoke project PASS; ruff check and format PASS; mypy --no-incremental PASS (386 files); pytest PC3 selections exit 0; verify_refs --offline 560 entries, 0 problems; mypy --strict on grader PASS; collect-only 489 (seed 0) and 498 (seed 77314143), matching the page line 397.",
        "Not checked: exemplar blind comparison to official scores (ruling 23); project.html exemplar lines 632-694; cards.json content (outside slice c); the live verify_refs run (network; references/ unchanged); browser UI claims (base also did not check them); Pyodide timings beyond page_smoke; the L04.html content beyond the cited lines.",
    ],
    "summary": (
        f"PC3-c closing delta round 1: verdict {verdict}. Rows {len(rows)}: PASS {counts['PASS']}, non-PASS 0. "
        f"Re-verified fresh {len(fresh_ids)}; carried {len(rows) - len(fresh_ids)}. Mutants {sum(m['status']=='KILLED' for m in mutants)}/92 killed "
        f"on seeds 0-49. No new mutants written (ruling 37). Source files of the slice unchanged since pin 50559266; "
        f"delta touching the slice: L04.html line 127, r18_01..03 mutants (added)."
    ),
}

FRAG.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "fresh", len(fresh_ids), "verdict", verdict, "mutants", len(mutants))
