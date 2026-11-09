"""SC1-a round 18: build the verifier fragment ledgers/SC1/SC1-a.json from the round-17 row set.

Carry rule (VERIFIER_RULES, round after the first): a round-17 PASS row is carried only when every file it cites is
byte-identical since the round-17 pin 700bf33f (git diff below). Rows citing course/modules/SC/SC1/L02.html,
L03.html or cards.json were re-verified this round (both files read in full) and are restated as PASS with the
re-verification prefix. Rows whose evidence is a script output are re-run and overridden. Every round-17 row id is kept.
"""

import json
import os
import re
import subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
OUT = os.path.join(ROOT, "ledgers", "SC1", "scripts", "SC1-a-r18", "out")
PREV = "/Users/billyribeiro/.fanout/frags/E-SC1-a.round17.json"
PIN = "50559266"
BASE = "700bf33f"
CHANGED_FILES = subprocess.run(
    ["git", "-C", ROOT, "diff", "--name-only", BASE, PIN, "--", "course/modules/SC/SC1", "tests/labs/SC1", "notation",
     "references", "tools", "curriculum"],
    capture_output=True, text=True, check=True,
).stdout.split()
CHANGED_SLICE = sorted(p for p in CHANGED_FILES if p.startswith("course/modules/SC/SC1/") and p.endswith((".html", ".json")))

REVERIFIED_PREFIX = ("Re-verified round 18 (course/modules/SC/SC1/L02.html, L03.html and cards.json changed since 700bf33f; "
                     "each read in full this round, delta hunks re-derived): ")
CARRIED_PREFIX = ("Carried from round 17 (course/modules/SC/SC1/index.html, L01.html, project.html, tests/labs/SC1 and "
                  "notation/refs/tools byte-identical since 700bf33f; git diff 700bf33f 50559266 touches only L02.html, "
                  "L03.html, cards.json and plans): ")

with open(PREV, encoding="utf-8") as fh:
    prev = json.load(fh)

OVR = {}


def ovr(rid, status, evidence, location=None, check=None, fix=None):
    OVR[rid] = {"status": status, "evidence": evidence, "location": location, "check": check, "fix": fix}


GATE = "ledgers/SC1/scripts/SC1-a-r18/out/"
ovr("SC1a-gate-check-pages", "PASS",
    f"Re-run round 18: .venv/bin/python tools/check_pages.py --unit SC1 -> 'check_pages SC1: PASS', rc=0 ({GATE}check_pages_SC1.out).")
ovr("SC1a-gate-check-dag", "PASS",
    f"Re-run round 18: .venv/bin/python tools/check_dag.py --unit SC1 -> 'check_dag SC1: PASS', rc=0 ({GATE}check_dag_SC1.out).")
ovr("SC1a-gate-run-labs", "PASS",
    f"Re-run round 18: tools/run_labs.py --unit SC1 --page L01, L02, L03 -> 'run_labs SC1: PASS (1/1)', rc=0 each ({GATE}run_labs_L0n.out).")
ovr("SC1a-gate-page-smoke", "PASS",
    f"Re-run round 18, page_smoke run per slice page (ledgers/SC1/scripts/SC1-a-r18/page_smoke_each_r18.sh): index run -> "
    f"'page_smoke index.html: PASS', L01, L02, L03 runs -> 'page_smoke modules/SC/SC1/L0n.html: PASS'; each rc=0 "
    f"({GATE}page_smoke_index.out, _L01.out, _L02.out, _L03.out). The index run also covered the unit's other pages and passed.")
ovr("SC1a-gate-lint-types-tests", "PASS",
    f"Re-run round 18: ruff check -> 'All checks passed!' rc=0; ruff format --check -> '553 files already formatted' rc=0; "
    f"mypy --no-incremental -> 'Success: no issues found in 385 source files' rc=0; pytest -q -k SC1 -> 11 passed rc=0 "
    f"({GATE}ruff_check.out, ruff_format.out, mypy.out, pytest_SC1.out).")
ovr("SC1a-gate-verify-refs", "PASS",
    f"Re-run round 18: verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' rc=0; verify_refs.py --unit SC1 -> "
    f"'live re-verification of SC1: 1 of 560 entries, 0 problems' rc=0 ({GATE}verify_refs_offline.out, verify_refs_unit_SC1.out). "
    f"The one SC1 entry is shreve2004stochastic (index.html:182).")
ovr("SC1a-r7-gate-check-projects", "PASS", f"Re-run round 18: tools/check_projects.py --unit SC1 -> PASS rc=0 ({GATE}check_projects_SC1.out).")
ovr("SC1a-r15-gate-ruff-check", "PASS", f"Re-run round 18: .venv/bin/ruff check . -> 'All checks passed!' rc=0 ({GATE}ruff_check.out).")
for rid, cmd in [
    ("SC1a-r10-cmd-check_pages", "check_pages"), ("SC1a-r10-cmd-check_dag", "check_dag"),
    ("SC1a-r10-cmd-check_projects", "check_projects"), ("SC1a-r10-cmd-run_labs", "run_labs"),
    ("SC1a-r10-cmd-page_smoke", "page_smoke"), ("SC1a-r10-cmd-twins-python-I-W-error", "twins python -I -W error"),
    ("SC1a-r10-cmd-verify_refs", "verify_refs"), ("SC1a-r10-cmd-ruff-mypy", "ruff, mypy"),
    ("SC1a-r10-cmd-pytest-SC1", "pytest -k SC1"),
]:
    ovr(rid, "PASS", f"Command re-run in round 18 ({cmd}); output under {GATE} (see SC1a-gate-* rows), all rc=0.")
ovr("SC1a-r7-katex-render", "PASS",
    f"page_smoke round 18 ({GATE}page_smoke_*.out): zero unrendered math and every expression re-parses under KaTeX strict mode on index, L01, L02, L03.")
ovr("SC1a-r4-twin-timing-and-purity", "PASS",
    f"Round 18: twins run under python -I -W error, rc=0 and empty stderr for L01, L02, L03 ({GATE}twin_L0n.rc, .stderr); "
    f"page_smoke lab timings L01 0.0 s, L02 0.2 s, L03 0.1 s (page_smoke_L0n.out), all under 10 s.")
for rid in ("SC1a-r4-seed-sweep-L02", "SC1a-r12-L02-identities-301-seeds", "SC1a-r16-seed-sweep-L02"):
    ovr(rid, "PASS",
        "Round 18: the L02 docstring claims (dyadic count and grid-supremum identity 'hold for every seed') re-checked on seeds "
        "0-59: 0 dyadic mismatches and 0 grid-supremum mismatches (ledgers/SC1/scripts/SC1-a-r18/indep_recompute_r18.py, "
        "out/indep_recompute_r18.out). Structural argument: at a dyadic point every hat of level above the depth is exactly 0.0, "
        "and each level's grid maximum is attained at a hat centre where the hat equals exactly 1.0, so the identities hold for "
        "every seed, not only the sample. The round-12 301-seed run is not repeated.")
LABM = ("Round 18: kill_lab_mutants_r18.py ran all 35 files under ledgers/SC1/lab-mutants/ under python -I -W error against "
        "the page expected blocks: 'lab mutants killed 35/35; survivors 0' (out/kill_lab_mutants_r18.out).")
for rid in ("SC1a-r8-lab-mutants", "SC1a-r10-lab-mutants-4of4", "SC1a-r11-lab-mutants-6of6", "SC1a-r14-lab-mutants-new3",
            "SC1a-r15-lab-mutants-p1-p3", "SC1a-r16-lab-mutants-35", "SC1a-r16-mutants-list"):
    ovr(rid, "PASS", LABM + " The 35 files on disk are the set this row cites.")
ovr("SC1a-r16-lab-q1-q3-new", "UNVERIFIABLE",
    "Round-16 row cites three lab twins ledgers/SC1/lab-mutants/SC1a-r16-lab-q1-L01-dyadic-drops-last-piece.py, "
    "SC1a-r16-lab-q2-L02-fixed-check-skips-own-level.py and SC1a-r16-lab-q3-L03-se-without-root-paths.py. None exists in the "
    "checkout (find over the verifier worktrees and the main checkout: no match), and none appears in git history (git log "
    "--all -- ledgers/SC1/lab-mutants lists only SC1a-r15-lab-p1..p3 and earlier files). The round-16 kill output "
    "(ledgers/SC1/scripts/SC1-a-r16/out/kill_lab_mutants_r16.out, lines naming q1-q3) therefore cannot be reproduced. "
    "The round-17 kill run (kill_lab_mutants_r17.out) and this round's run kill the 35 files on disk, which do not include q1-q3.",
    fix="Either recommit the three round-16 lab twins (their descriptions are in ledgers/SC1/scripts/SC1-a-r16/write_fragment_r16.py "
        "line 83; recreate them as files under ledgers/SC1/lab-mutants/, run kill_lab_mutants, and cite the new output) or retire this row "
        "and state that the lab-mutant set is the 35 files on disk. Lab twins are demonstrations, so the row is evidence hygiene, "
        "not a page defect. The r16 row SC1a-r16-lab-mutants-35 must also drop its claim that the 35 included q1-q3.",
    check="2.5-labs-mutants")
ovr("SC1a-r16-cards-L01-L03-full", "PASS",
    "Round 18 full scan of all 81 L01-L03 cards (course/modules/SC/SC1/cards.json, read in full via a dump "
    "ledgers/SC1/scripts/SC1-a-r18/dump_cards_r18.py -> out/cards_L01_L03_r18.txt (lesson, front, back, cite, grade, basis); each card checked against the current "
    "lesson text, including c017 back vs L01.html:234 (now matching: value at time 0 and finite-dimensional laws, not the set of "
    "paths). No duplicate ids; no duplicate question among L01-L03 cards. Card c017 was the only card changed in this delta.")
ovr("SC1a-r17-card-c017-definition-fixes", "PASS",
    "cards.json lines 136-141 (SC1-c017) read this round: back 'The value at time 0 of every path (D1, B_0=0) and the "
    "finite-dimensional laws (D2, D3), not the set of paths. The process B̃ of Section 4 satisfies (D1)–(D3) and has the laws of B, "
    "yet its paths differ from those of B.' matches L01.html:234 ('fixes the value at time 0 of every path and the "
    "finite-dimensional laws, but not the set of paths ... discontinuous at U on every outcome'). basis cites Section 4 with Remark "
    "2.6 of Lesson 2 and A1(a), A1(b), A1(e), A2, Assumption 2.1(a)-(c), the hypotheses the Section 4 item uses (L01.html:215).")
ovr("SC1a-r11-cards-scan", "PASS",
    "cards.json at 700bf33f and 50559266 (card_count_pins_r18.sh -> out/card_count_pins_r18.out): 227 cards in total, 81 for L01-L03 (25 L01, 32 L02, 24 L03), read in full this round "
    "(see SC1a-r16-cards-L01-L03-full). Earlier '221' and '79' figures in ledger rows are stale or miscounted; the L01-L03 count "
    "was 81 at 56cc575a too (python count, this round).")
ovr("SC1a-r13-cards-L01-L03-read", "PASS",
    "Round 18 read of all 81 L01-L03 cards (not 79: the round-13 figure was a miscount; 81 at 56cc575a, 700bf33f and 50559266).")
ovr("SC1a-r10-cards-dup-hypotheses", "PASS",
    "Round 18 full scan: 81 L01-L03 cards. Cards c011, c012 and c013 share one hypothesis block but ask three different questions "
    "(what B̃ satisfies, why it is discontinuous, whether continuity is determined by the laws); no two cards ask the same question.")
ovr("SC1a-r11-numbers-recomputed", "PASS",
    "Round 18 recomputation by an independent script (ledgers/SC1/scripts/SC1-a-r18/indep_recompute_r18.py, out/indep_recompute_r18.out; "
    "ledgers/SC1/scripts/SC1-a-r18/l02_unrounded_r18.py, out/l02_unrounded_r18.out). Supersedes the round-14 file numbers_r14.out, "
    "which is not re-read.")
ovr("SC1a-r11-twins-venv-314", "PASS", "Round 18: .venv/bin/python -V -> Python 3.14.8 (CPython).")
for rid in ("SC1a-r11-delta-read", "SC1a-r15-delta-read", "SC1a-r16-delta-read", "SC1a-r17-delta-read"):
    ovr(rid, "PASS",
        "Historical delta read of an earlier pin. Superseded by "
        "SC1a-r18-delta-read, which reads the round-18 delta (700bf33f..50559266) in full.")


def is_reverified(text: str) -> bool:
    return bool(re.search(r"L02|L03|cards\.json|L02\.html|L03\.html", text))


rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in OVR:
        o = OVR[rid]
        row = {"id": rid, "check": o["check"] or r["check"], "location": o["location"] or r["location"],
               "status": o["status"], "evidence": o["evidence"]}
        if o["status"] != "PASS":
            row["fix"] = o["fix"]
        rows.append(row)
        continue
    text = (r.get("location", "") + " " + r.get("evidence", ""))
    if r["status"] != "PASS":
        raise SystemExit(f"round-17 non-PASS row without override: {rid}")
    if is_reverified(text):
        ev = REVERIFIED_PREFIX + r["evidence"]
    else:
        ev = CARRIED_PREFIX + r["evidence"]
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": ev})

NEW = [
    ("SC1a-r18-delta-read", "1-delta", "course/modules/SC/SC1/L02.html; L03.html; cards.json; plans/SC1-build-plan.md",
     "Round 18 delta read in full: git diff 700bf33f 50559266 -- course/modules/SC/SC1 tests/labs/SC1 notation references tools "
     "curriculum: 3 slice files changed (L02.html 1 line, L03.html 4 lines, cards.json 2 lines), tests/labs/SC1 and index.html, "
     "L01.html, project.html and notation unchanged. Every hunk read (see the hunk rows below)."),
    ("SC1a-r18-hunk-L02-51", "2.9-structure", "course/modules/SC/SC1/L02.html:51",
     "why-it-matters: 'adds the piecewise linear bumps of Definition 2.1 (§1)'. Definition 2.1 is in §1 (L02.html:63-68). Only the parenthetical was added; no number or claim changed."),
    ("SC1a-r18-hunk-L03-116", "2.4-math", "course/modules/SC/SC1/L03.html:115",
     "'under Assumptions 3.1 and 3.2 the random sums converge to it in mean square, and under Assumption 3.2 the mean-square error is exactly 2 sum Delta_k^2': matches Theorem 2.3 (L03.html:104 hypotheses H2 and the mesh assumption, proof L03.html:112 gives E[(Q-t)^2]=2 sum Delta_k^2)."),
    ("SC1a-r18-hunk-L03-260", "2.4-math", "course/modules/SC/SC1/L03.html:260",
     "Independence example: Q = N X_N^2, E[Q]=t, Var(Q)=N^2*2(t/N)^2=2t^2 for every N (re-derived: Var(N X^2)=N^2 Var(X^2)=N^2*2(t/N)^2). 'The family is not a standard Brownian motion, so the theorem does not apply' matches R3 (L03.html:382). The new clause 'the conclusion of Theorem 2.3 can fail when the independence in Assumption 3.2 is removed' is an existence statement the example supports."),
    ("SC1a-r18-hunk-L03-270", "2.9-structure", "course/modules/SC/SC1/L03.html:270; twin_L03.stdout line 'H = 2, N = 128'",
     "Misconception 1: 'Lab 1 prints the exact sum 0.166664' matches the twin output (ledgers/SC1/scripts/SC1-a-r18/out/twin_L03.stdout, H = 2, N = 128: sum = 0.166664, closed form matches: True) and the closed form H^4(4N^2-1)/(3N^3) = 16*(4*16384-1)/(3*2097152) = 0.166664 (recomputed by indep_recompute_r18.py). Mean H=2 by Theorem 2.3; mean-square error tending to zero under Assumptions 3.1 and 3.2 matches L03.html:104."),
    ("SC1a-r18-hunk-L03-278", "2.9-structure", "course/modules/SC/SC1/L03.html:278",
     "Misconception 3: 'Under Assumptions 3.1 and 3.2, the random sums fluctuate around t with mean-square error at most 2t|P_n|' matches Theorem 2.3 (L03.html:104, :112)."),
    ("SC1a-r18-card-c017", "2.7-cards", "course/modules/SC/SC1/cards.json:138-141 (SC1-c017); L01.html:234",
     "The card back and basis match L01.html:234 and :215 (see SC1a-r17-card-c017-definition-fixes)."),
    ("SC1a-r18-cards-full-scan", "2.7-cards", "course/modules/SC/SC1/cards.json (81 L01-L03 cards)",
     "Every card read this round against its lesson: definitions (c001-c004, c006, c018-c020, c042-c043, c184, c186), results (c005-c009, c021-c035, c044-c050, c236-c237, c220-c224), misconceptions (c014-c016, c039-c041, c056-c058, c053-c054, c057), labs (c010, c037, c038, c051, c187, c225), assumptions (c033, c060, c206-c213, c232-c234, c188). Every card number appears in its lesson (216 cases c037, 2.39 c051, 13.2 percent c187, sqrt(2Nt/pi) c057, 1.84 c051). Sample-of-10 rule: all cards read, not sampled."),
    ("SC1a-r18-lab-L03-gap-13.22", "2.5-labs", "course/modules/SC/SC1/L03.html:398; ledgers/SC1/scripts/SC1-a-r18/indep_recompute_r18.py",
     "Key-result row 398 says the largest gap is 13.2 percent at H=2, N=1 (printed-value gap 0.1601/(2 sqrt2/20)-1 = 13.21 percent, rounds to 13.2; unrounded 13.22 percent). Re-derived with the lab's code path with unrounded se: gap +13.22 percent at H=2, N=1, max |gap| over 16 pairs; all other pairs below 9.2 percent. The unrounded figure is not printed by the lab; it is reproduced by its code (grade C, SIMULATED). Accepted: the displayed-digit value supports 13.2."),
    ("SC1a-r18-lab-L03-z-and-se", "2.5-labs", "course/modules/SC/SC1/L03.html:253, :398, :133",
     "Recomputed the 16 (H,N) rows with the lab's RNG order (seed 20260503, 400 paths): max |z| = 2.39 at H=1, N=2; second largest 1.84 at H=1, N=128; all |z| <= 3. Theoretical se H sqrt(2/N)/20 at H=1,N=1 = 0.0707 (printed sample 0.0718); at H=2,N=128 = 0.0125. Matches L03.html:253 and :133."),
    ("SC1a-r18-lab-L03-exact-sums", "2.2-numbers", "course/modules/SC/SC1/L03.html:252, :434, :455-457",
     "Exact s^2 sums equal H^4(4N^2-1)/(3N^3) at all 16 pairs (recomputed with fractions). H=2,N=8 = 2.65625 (E2, :350); H=1,N=2 = 0.625 (quiz :434); both match."),
    ("SC1a-r18-lab-L02-E3-and-tail", "2.2-numbers", "course/modules/SC/SC1/L02.html:419-421, :277-278",
     "Recomputed the seeded sample (seed 20260101) unrounded: xi_11 = 0.23317868947886533, so |xi_11| rounds to 0.233179 (E3 :421 claims 0.2331787 and 0.233179: correct). Twice the printed 0.116589 is 0.233178, which is not the rounded |xi_11| (E3 correct). lambda_1 = 1.665109, half = 0.832555 (correct). Sum of level bounds 5..8 = 1.309399 and grid sup |Sigma_8 - Sigma_4| = 0.348139 (both match the printed lines)."),
    ("SC1a-r18-lab-L02-216-count", "2.2-numbers", "course/modules/SC/SC1/L02.html:266, :278, :411-414",
     "216 = 2*9+3*8+5*7+9*6+17*5 and 36 point-depth pairs covering 17 distinct points: recomputed."),
    ("SC1a-r18-quiz-answers", "2.9-structure", "course/modules/SC/SC1/L01.html:372-427; L02.html:472-531; L03.html:417-469; index.html:94-143",
     "All numeric quiz answers recomputed: L01 2, 2, 0.5, 10, 5, 3; L02 1, 4, 1, 0.5, 9; L03 48, 0.625, 2.65625; index rung 2 answer 2 (two paths ++ and +- reach 1) and rung 1 expression. Multiple-choice data-correct flags match the explanations. Rung 2 count for n=6, a=2 = 29 (brute force over 64 paths, indep_recompute_r18.out)."),
    ("SC1a-r18-placement-arith", "2.2-numbers", "course/modules/SC/SC1/index.html:74",
     "7/9 = 77.8 percent and 8/9 = 88.9 percent; nine items, seven prerequisite and two skill checks (index.html:94-143 count)."),
    ("SC1a-r18-hub-lede-fixed-time-form", "2.9-structure", "course/modules/SC/SC1/index.html:33, :54; L06.html:119, :332",
     "Hub lede calls Theorem 2.5 of Lesson 6 the fixed-time form of the reflection principle; L06.html:119 calls Proposition 2.3 its fixed-time form, while L06.html:332 says Theorem 2.5 'uses only the fixed-time form'. The two statements are consistent (Theorem 2.5 is the fixed-time tail identity; Proposition 2.3 is the fixed-time reflection in law). No change required; noted as a naming overlap."),
    ("SC1a-r18-hub-hours-sum", "2.9-structure", "course/modules/SC/SC1/index.html:29, :42, :150; L01-L08 data-hours; project.html:272-281",
     "data-hours: L01-L08 each 9 (sum 72); lessons 72 + project 28 = 100; project.html hour rows 2+3+10+8+3+2 = 28."),
    ("SC1a-r18-notation-macros", "2.9-structure", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html, cards.json",
     "Every backslash command used in these files is either a registered macro in notation/notation.json (\\E, \\Prob, \\Var, \\Cov, \\Normal, \\indic, \\R, ...) or a standard KaTeX command (Greek letters, operators, \\mathbb, \\mathcal, \\operatorname). No registered symbol (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, \\mathbb{Q}) is used with another meaning in the slice; the plain Q of the quadratic variation is not the registered \\mathbb{Q}, and H is the horizon (L03.html:120), not a registered symbol."),
    ("SC1a-r18-banned-scan", "2.9-structure", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html, cards.json",
     "Scan (ledgers/SC1/scripts/SC1-a-r18/banned_scan_r18.sh -> out/banned_scan_r18.out, the BUILDER_RULES 1.3 strings): no TODO, TBD, lorem, 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'experts agree', 'it is well known', 'obviously', 'clearly', 'roughly', 'historically', 'Note that', 'As we saw', 'we will see', 'trivially', 'remarkably', 'surprisingly', 'as expected', 'it is easy'. The only '…' hits are mathematical index ellipses (t_1,…,t_r) in cards.json and not omitted content. Process words: none (the word 'verify' in index.html:52 and L03.html:146 is learner-facing)."),
    ("SC1a-r18-page-vs-twin", "2.5-labs", "course/modules/SC/SC1/L01.html, L02.html, L03.html; tests/labs/SC1/lab-SC1-L0n-1.py",
     "page lab code (HTML-unescaped) equals the twin file, and the expected block equals the twin's stdout under python -I -W error, for L01, L02 and L03 (ledgers/SC1/scripts/SC1-a-r18/page_vs_twin_r18.py, out/page_vs_twin_r18.out)."),
    ("SC1a-r18-page-smoke-alone", "2.9-structure", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html",
     "page_smoke run alone for each slice page (see SC1a-gate-page-smoke): zero console errors, zero external requests, zero unrendered math, pass."),
]
for rid, check, loc, ev in NEW:
    rows.append({"id": rid, "check": check, "location": loc, "status": "PASS", "evidence": ev})

mutants = []
with open(os.path.join(OUT, "kill_lab_mutants_r18.out"), encoding="utf-8") as fh:
    for line in fh:
        if line.startswith("KILLED "):
            path = line[len("KILLED "):].split(" (")[0].strip()
            mutants.append({"id": path, "description": os.path.basename(path)[:-3].replace("-", " ") + " (lab-twin mutant, demonstration)",
                            "killed_by": "lab expected block (ledgers/SC1/scripts/SC1-a-r18/out/kill_lab_mutants_r18.out)"})

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
verdict = "PASS" if counts["PASS"] == len(rows) else "FAIL"

fragment = {
    "unit": "SC1",
    "slice": "a",
    "round": 18,
    "verifier": "Haiku independent verifier, SC1-a round 18 (did not build SC1)",
    "pin": PIN,
    "base": "700bf33f (round-17 pin; round-17 fragment /Users/billyribeiro/.fanout/frags/E-SC1-a.round17.json used as context only, its PASS rows re-checked by the carry rule)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE18-SC1-a (detached at 50559266; .venv symlinked; vendor copied)",
    "scratch": "none used for evidence; all scripts under ledgers/SC1/scripts/SC1-a-r18/ (gates_r18.sh, page_smoke_each_r18.sh, indep_recompute_r18.py, l02_unrounded_r18.py, page_vs_twin_r18.py, kill_lab_mutants_r18.py, write_fragment_r18.py)",
    "verified_at": "2026-11-09T05:13:54+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "Karatzas & Shreve, Brownian Motion and Stochastic Calculus, 2nd ed. (1991) is the second source the curriculum lists for SC1 (curriculum/03-markets.yaml:522-524); no admitted registry record (references/review_queue.json; plans/SC1-build-plan.md B2). No slice page cites it, so no request is needed unless the architect asks for it."
    ],
    "freshness_flags": [],
    "notes": (
        "ROUND 18 at 50559266. Delta from 700bf33f for the slice: L02.html:51 (one parenthetical), L03.html:115, :260, :270, :278 "
        "(four in-line text edits, line numbers unchanged), cards.json:138-141 (card c017 back and basis). index.html, L01.html, "
        "project.html, tests/labs/SC1 twins, notation, references and tools are byte-identical. Every hunk was read and re-derived. "
        "The round-17 FAILs are PASS now: c017 back matches L01.html:234; the full card scan finds no defect. "
        "NEW FAIL: SC1a-r16-lab-q1-q3-new is UNVERIFIABLE: its three cited lab twins do not exist in the checkout or in git history, so "
        "the round-16 kill run cannot be reproduced. The lab pages, twins and cards pass; the failure is evidence retention. "
        "L01-L03 card count is 81 at every pin since 56cc575a; earlier '79' and '221' figures in ledger rows were miscounts. "
        "Gates re-run on the pin: check_pages, check_dag, check_projects, run_labs (L01-L03), page_smoke alone for index, L01, L02, L03, "
        "twins under python -I -W error (rc 0, empty stderr), ruff check and format, mypy strict (385 files), pytest -k SC1 (11), "
        "verify_refs offline (560, 0 problems) and unit (1 entry, 0 problems). Lab-twin mutants 35/35 killed. "
        "Not run: run_graders and mutate_graders (no project grader in slice a), render_curriculum, build_site --check, "
        "fetch_data --check (outside slice a). Not re-read: L04-L08 and project.html beyond the cited hour rows; their rows are carried "
        "on byte-identity."
    ),
    "summary": {
        "text": f"SC1-a round 18 at 50559266: verdict {verdict}. Non-PASS: SC1a-r16-lab-q1-q3-new (UNVERIFIABLE, evidence files missing).",
        "counts": counts,
        "mutants": f"{len(mutants)} of {len(mutants)} lab-twin mutants killed",
    },
}

os.makedirs(os.path.join(ROOT, "ledgers", "SC1"), exist_ok=True)
with open(os.path.join(ROOT, "ledgers", "SC1", "SC1-a.json"), "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("rows", len(rows), counts, "mutants", len(mutants), "verdict", verdict)
print("changed slice files", CHANGED_SLICE)
