"""SC1-a round 19: build ledgers/SC1/SC1-a.json from the round-18 fragment and this round's evidence.

Rows whose cited subject is byte-identical since the round-18 pin (50559266) are carried with the prefix the
verifier rules require. Rows whose subject changed (cards.json, the lab-mutant set, gate commands, historical deltas)
are re-verified and carry this round's evidence. Usage (from the checkout root):
    .venv/bin/python -I ledgers/SC1/scripts/SC1-a-r19/write_fragment_r19.py
"""

import datetime
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
OUT = os.path.join(ROOT, "ledgers", "SC1", "SC1-a.json")
R18 = "/Users/billyribeiro/.fanout/frags/E-SC1-a.round18.json"
O = "ledgers/SC1/scripts/SC1-a-r19/out"
PIN18 = "50559266"

prev = json.load(open(R18, encoding="utf-8"))
kill = open(os.path.join(ROOT, O, "kill_lab_mutants_r19.out"), encoding="utf-8").read().splitlines()
kill_lines = {}
for line in kill:
    m = re.match(r"(KILLED|SURVIVED) (\S+)", line)
    if m:
        kill_lines[os.path.basename(m.group(2))] = line
mutant_files = sorted(
    os.path.relpath(os.path.join(dp, f), ROOT)
    for dp, _, fs in os.walk(os.path.join(ROOT, "ledgers", "SC1", "lab-mutants"))
    for f in fs
    if f.endswith(".py")
)
assert len(mutant_files) == 38, len(mutant_files)
assert all(kill_lines[os.path.basename(p)].startswith("KILLED") for p in mutant_files)

ALL = "lab mutants killed 38/38; survivors 0 (" + O + "/kill_lab_mutants_r19.out)"
TWINS = (
    "run_labs / twin / page checks at cd4dd7df: run_labs SC1 PASS for L01, L02, L03; twin_L0n.rc=0 and empty stderr "
    "under python -I -W error; page_vs_twin_r19.out: page code == twin and expected == stdout for L01, L02, L03."
)
GATES = "gates_r19.sh outputs in " + O + "/"

RE = {}  # id -> (status, check, location, evidence, fix)


def re_row(rid, status, evidence, fix=None, check=None, location=None):
    RE[rid] = {"status": status, "evidence": evidence, "fix": fix, "check": check, "location": location}


re_row("SC1a-gate-check-pages", "PASS",
       "check_pages.py --unit SC1 at cd4dd7df: 'check_pages SC1: PASS', rc=0 (" + GATES + "check_pages_SC1.out). "
       "Covers index.html, L01-L03 and cards.json structure.")
re_row("SC1a-gate-check-dag", "PASS",
       "check_dag.py --unit SC1: 'check_dag SC1: PASS', rc=0 (check_dag_SC1.out).")
re_row("SC1a-gate-run-labs", "PASS", "run_labs.py --unit SC1 --page L01, L02, L03: each 'run_labs SC1: PASS (1/1)', rc=0 "
       "(run_labs_L01.out, run_labs_L02.out, run_labs_L03.out). " + TWINS)
re_row("SC1a-gate-page-smoke", "PASS",
       "page_smoke.py --unit SC1, run per page: index.html run 'page_smoke index.html: PASS' (also project, concepts, review "
       "pages), L01, L02, L03 each 'page_smoke ...: PASS', rc=0 (page_smoke_index.out, page_smoke_L01.out, "
       "page_smoke_L02.out, page_smoke_L03.out).")
re_row("SC1a-gate-lint-types-tests", "PASS",
       "ruff check . 'All checks passed!' rc=0; ruff format --check . '553 files already formatted' rc=0; mypy --no-incremental "
       "'Success: no issues found in 385 source files' rc=0; pytest -q -k SC1: eleven dots, rc=0; collect-only -k SC1: "
       "tests/test_labs.py: 11 (ruff_check.out, ruff_format.out, mypy.out, pytest_SC1.out, collect_SC1.out).")
re_row("SC1a-gate-verify-refs", "PASS",
       "verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' rc=0; verify_refs.py --unit SC1: 'live "
       "re-verification of SC1: 1 of 560 entries, 0 problems' rc=0 (verify_refs_offline.out, verify_refs_unit_SC1.out). "
       "The one SC1 entry is shreve2004stochastic (index.html:182).")
for rid, cmd, out in [
    ("SC1a-r10-cmd-check_pages", "check_pages.py --unit SC1", "check_pages_SC1.out: PASS, rc=0"),
    ("SC1a-r10-cmd-check_dag", "check_dag.py --unit SC1", "check_dag_SC1.out: PASS, rc=0"),
    ("SC1a-r10-cmd-check_projects", "check_projects.py --unit SC1", "check_projects_SC1.out: PASS, rc=0"),
    ("SC1a-r10-cmd-run_labs", "run_labs.py --unit SC1 --page L01/L02/L03", "run_labs_L01..L03.out: PASS, rc=0 each"),
    ("SC1a-r10-cmd-page_smoke", "page_smoke.py --unit SC1 --pages (per page)", "page_smoke_*.out: PASS, rc=0"),
    ("SC1a-r10-cmd-twins-python-I-W-error", "python -I -W error tests/labs/SC1/lab-SC1-L0n-1.py",
     "twin_L0n.rc = 0, twin_L0n.stderr empty (0 bytes), twin_L0n.stdout written"),
    ("SC1a-r10-cmd-verify_refs", "verify_refs.py --offline and --unit SC1", "560 entries 0 problems; 1 of 560, 0 problems"),
    ("SC1a-r10-cmd-ruff-mypy", "ruff check, ruff format --check, mypy --no-incremental", "All checks passed; 553 formatted; 385 files, no issues"),
    ("SC1a-r10-cmd-pytest-SC1", "pytest -q -k SC1", "11 passed (eleven dots), rc=0"),
]:
    re_row(rid, "PASS", f"Round 19 rerun of `{cmd}` at cd4dd7df: {out} (" + GATES + "). Command output recorded in the out/ file named.")
re_row("SC1a-r11-twins-venv-314", "PASS",
       "The verifier venv is CPython 3.14.8 (.venv/bin/python -V). The three L01-L03 twins run under python -I -W error with "
       "rc=0 and empty stderr (twin_L0n.rc, twin_L0n.stderr).")
re_row("SC1a-r15-gate-ruff-check", "PASS",
       "ruff check . passes (All checks passed!, rc=0). pyproject.toml:19 extend-exclude lists ledgers/*/lab-mutants, so the "
       "lab-mutant files, including SC1a-r13-lab-m1-L01-cov-max.py, are not linted (commit aeb512b6).")
re_row("SC1a-r7-gate-check-projects", "PASS", "check_projects.py --unit SC1 at cd4dd7df: 'check_projects SC1: PASS', rc=0 "
       "(check_projects_SC1.out).")
re_row("SC1a-r18-page-vs-twin", "PASS", TWINS + " (ledgers/SC1/scripts/SC1-a-r19/page_vs_twin_r19.py, out/page_vs_twin_r19.out).")
re_row("SC1a-r18-page-smoke-alone", "PASS",
       "page_smoke run alone for each slice page at cd4dd7df: index, L01, L02, L03 each PASS, rc=0 (page_smoke_*.out).")

for rid in ["SC1a-r8-lab-mutants", "SC1a-r16-mutants-list"]:
    re_row(rid, "PASS", "kill_lab_mutants_r19.py ran all 38 files under ledgers/SC1/lab-mutants/ under python -I -W error "
           "against the page expected blocks: " + ALL + ". The 35 older files plus SC1a-r16-lab-q1..q3 (recommitted in "
           "cd4dd7df).")
re_row("SC1a-r10-lab-mutants-4of4", "PASS",
       "ledgers/SC1/lab-mutants/SC1-a-r10/mut-L01-1.py, mut-L02-1.py, mut-L03-1.py, mut-L03-2.py: " + "; ".join(
           kill_lines[f].split(" (")[0] + " " + kill_lines[f].split("): ")[1] for f in
           ["mut-L01-1.py", "mut-L02-1.py", "mut-L03-1.py", "mut-L03-2.py"]) + " (kill_lab_mutants_r19.out).")
re_row("SC1a-r11-lab-mutants-6of6", "PASS",
       "ledgers/SC1/lab-mutants/SC1-a-r11/m1..m6 all KILLED in kill_lab_mutants_r19.out (m1 token 54, m2 token 16, m3 token "
       "34, m4 token 36, m5 token 224, m6 token 11).")
re_row("SC1a-r14-lab-mutants-new3", "PASS",
       "SC1a-r14-lab-n1, n2, n3 KILLED: n1 token 11 '1/2' vs '1'; n2 token 148 '0.252987;' vs '0.348139;'; n3 token 22 "
       "'1.4369,' vs '0.0718,' (kill_lab_mutants_r19.out).")
re_row("SC1a-r15-lab-mutants-p1-p3", "PASS",
       "SC1a-r15-lab-p1, p2, p3 KILLED: p1 token 11 '1/2' vs '1'; p2 token 148 '0.492342;' vs '0.348139;'; p3 token 31 "
       "'0.5644,' vs '1.1288,' (kill_lab_mutants_r19.out).")
re_row("SC1a-r16-lab-mutants-35", "PASS",
       "The lab-mutant set on disk is 38 files (35 older plus q1..q3). " + ALL + ". Each killed mutant differs from the "
       "page expected block (kill_lab_mutants_r19.out).")
re_row("SC1a-r16-lab-q1-q3-new", "PASS",
       "The three round-16 twins now exist, added by commit cd4dd7df (git log --diff-filter=A): ledgers/SC1/lab-mutants/"
       "SC1a-r16-lab-q1-L01-dyadic-drops-last-piece.py, SC1a-r16-lab-q2-L02-fixed-check-skips-own-level.py, "
       "SC1a-r16-lab-q3-L03-se-without-root-paths.py. Killed this round: q1 KILLED token 11 '15/16' vs '1'; "
       "q2 KILLED token 16 180 vs 216; q3 KILLED token 22 '1.4369,' vs '0.0718,' "
       "(kill_lab_mutants_r19.out). The r18 UNVERIFIABLE finding is resolved.")

# cards
CARDS_R19 = ("cards_L01_L03_r19.txt (full read of the 82 L01-L03 cards, dump_cards_r19.py) and cards_struct_r19.out "
             "(cards_struct_r19.py)")
re_row("SC1a-r10-cards-dup-hypotheses", "PASS",
       "Round 19 read of all 82 L01-L03 cards: " + CARDS_R19 + ". No two cards share a front (0 exact duplicate fronts over 227 "
       "cards). c011, c012 and c013 share one hypothesis block but ask three different questions (what B̃ satisfies, why it "
       "is discontinuous, whether continuity is determined by the laws).")
re_row("SC1a-r11-cards-scan", "PASS",
       "cards.json at cd4dd7df: 227 cards in total, 227 distinct ids, 82 for L01-L03 (25 L01, 33 L02, 24 L03; "
       "cards_struct_r19.out). L01-L03 was 81 at 56cc575a, 700bf33f and 50559266, and 82 at cd4dd7df after SC1-c243 was "
       "added; total 223, 227, 227, 227 at those pins. Earlier '221' and '79' figures are miscounts.")
re_row("SC1a-r13-cards-L01-L03-read", "PASS",
       "Round 19 read of all 82 L01-L03 cards (not 79; the round-13 figure was a miscount) in " + CARDS_R19 + ". Each card "
       "was read against its lesson statement. The per-card lesson agreement for the 81 records that are JSON-identical to "
       "50559266 is carried from round 18 (those records were checked there against the lesson text). The one new card, "
       "SC1-c243, is in SC1a-r19-card-c243 and SC1a-r19-c243-proposition-content.")
re_row("SC1a-r14-cards-L01-L03-changed", "PASS",
       "Records c011-c013, c029, c032, c034, c035, c054, c060, c207, c210, c220, c232-c234 compared with the 50559266 "
       "records by JSON equality (cards_pin_compare_r19.py -> out/cards_pin_compare_r19.out): all identical. The only L01-L03 record change since 50559266 is "
       "the addition of SC1-c243 (SC1a-r19-card-c243). Removed SC1-c217 (L06) and changed SC1-c110, c119, c122 (L06) are "
       "outside this slice.")
re_row("SC1a-r16-cards-L01-L03-full", "PASS",
       "Round 19 full read of the 82 L01-L03 cards (" + CARDS_R19 + "). The 81 records identical to 50559266 are carried "
       "from round 18 (each checked there against its lesson; JSON identity checked this round). SC1-c243 is the new "
       "record and fails: see SC1a-r19-card-c243.")
re_row("SC1a-r16-cards-grade-field", "FAIL",
       "cards_struct_r19.out: 27 of 82 L01-L03 cards carry no 'grade' key. Before SC1-c243, the 26 were definitions, "
       "assumption statements and misconception hypotheses (c001-c004, c006, c033, c060, c206-c213, c232-c234), which "
       "state no graded claim. SC1-c243 is not in that class: its back states Proposition 2.4's conclusion (L02.html:145-165, "
       "data-grade T) and carries no grade or basis. BUILDER_RULES §7 requires a graded theorem statement to carry its grade.",
       fix="Fix SC1-c243 as specified in SC1a-r19-card-c243; then this row is PASS.")
re_row("SC1a-r18-cards-full-scan", "FAIL",
       "Round 19 read of all 82 L01-L03 cards (" + CARDS_R19 + "). 81 records are unchanged since 50559266 and were checked "
       "there. SC1-c243 (new) breaks the one-fact rule of BUILDER_RULES §7 and the grade rule (SC1a-r19-card-c243). No "
       "duplicate ids (227 distinct) and no duplicate fronts. Every card number in the 81 carried cards appears in its lesson.",
       fix="Fix SC1-c243 as specified in SC1a-r19-card-c243; the other 81 cards need no change.")
re_row("SC1a-r16-banned-phrases", "PASS",
       "banned_scan_r19.sh over index.html, L01.html, L02.html, L03.html and cards.json (out/banned_scan_r19.out): no hit for "
       "TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is "
       "important to note, studies show, experts agree, it is well known, obviously, clearly, roughly, historically, Note "
       "that, As we saw, we will see, trivially, remarkably, surprisingly, as expected, it is easy. The only hits are "
       "the '…' math enumerations at cards.json:19, :20, :27 (t_1,…,t_r and (D3)).")
re_row("SC1a-r18-banned-scan", "PASS",
       "banned_scan_r19.sh (out/banned_scan_r19.out), same strings and files as above, run at cd4dd7df including SC1-c243: "
       "no banned hit. The only '…' hits are the cards.json math enumerations at :19, :20, :27.")
re_row("SC1a-r18-notation-macros", "PASS",
       "cards.json has no backslash macros (Unicode math). SC1-c243 uses Σ_M and Σ(t)=lim_M Σ_M(t); neither Σ nor lim is a "
       "registered symbol (notation/notation.json symbols: T, Φ, γ3, γ4, R*, R^{e*}, R_f, \\mathbb{Q}). The plain Q of the "
       "quadratic variation (L03 cards c042, c046-c048, c052-c054, c058-c059) is not the registered \\mathbb{Q}, which denotes "
       "a probability measure. Pages carried from round 18 (byte-identical since 50559266).")
re_row("SC1a-r15-counts", "PASS",
       "Round 19 re-derivation of the card count (cards_struct_r19.out): 227 cards total, 82 for L01-L03 (25/33/24). Other "
       "counts carried from round 18 (index.html, L01-L03.html and project.html byte-identical since 50559266, counts "
       "derived there): objectives, quiz and misconception counts, problem counts 3/3/3/3 per lesson, placement items. "
       "Re-run this round: every lesson data-hours value is 9 (grep over L01-L08.html).")

# historical delta rows: each row is superseded; the recorded range is re-derived where it can be
re_row("SC1a-r11-delta-read", "PASS",
       "Historical range e919577b..8e5751c9: both commits resolve; git diff --stat over the slice files reproduces the four "
       "changed files, index.html, L01.html, L02.html, cards.json (71 insertions, 41 deletions). The hunk-level claims are "
       "superseded for the current state by SC1a-r19-delta-read.")
re_row("SC1a-r15-delta-read", "PASS",
       "Historical row with no recorded commit range and no checkable hunk claim; it asserts only that it is superseded. "
       "It is superseded by SC1a-r19-delta-read for the current state. No current claim rests on it.")
re_row("SC1a-r16-delta-read", "PASS",
       "The round-16 delta is git diff d1e65a0 56cc575a (not 700bf33f): it changes exactly L01.html:434, L03.html:398, "
       "L03.html:502 and cards.json:433-434 (one hunk @@ -433,2 +433,2 @@), inside the row's cards.json:432-437 range. "
       "Re-derived this round.")
re_row("SC1a-r17-delta-read", "PASS",
       "Historical row with no recorded commit range and no checkable hunk claim; it asserts only that it is superseded by "
       "SC1a-r18-delta-read, which is itself superseded by SC1a-r19-delta-read.")
re_row("SC1a-r18-delta-read", "PASS",
       "git diff --stat 700bf33f 50559266 for the slice: L02.html 1 line (2 +-), L03.html 4 lines (8 +-), cards.json 2 lines (4 +-), "
       "re-derived this round. The row is superseded for the current state by SC1a-r19-delta-read.")

# new rows
NEW = []
NEW.append({
    "id": "SC1a-r19-delta-read", "check": "1-delta",
    "location": "git diff 50559266 cd4dd7df -- course/modules/SC/SC1 tests/labs/SC1 ledgers/SC1/lab-mutants notation references tools curriculum/03-markets.yaml plans/SC1-*",
    "status": "PASS",
    "evidence": "Delta from the round-18 pin 50559266 to cd4dd7df, read in full for the slice. (1) course/modules/SC/SC1/cards.json: hunks @@ -343,0 +344,7 @@ (SC1-c243 added, L02, lines 344-351), @@ -959 +966 @@ (c110, L06), @@ -1040,2 +1047,2 @@ (c119, L06), @@ -1065,3 +1072,5 @@ (c122, L06), @@ -1703,9 +1711,0 @@ (c217 removed, L06). Only c243 is in this slice; the L06 hunks are outside it and are not verified here. (2) ledgers/SC1/lab-mutants: three files added by cd4dd7df (SC1a-r16-lab-q1..q3). (3) index.html, L01.html, L02.html, L03.html, project.html, L04-L08.html, the lab twins tests/labs/SC1, the grader, notation/, references/, tools/, curriculum/03-markets.yaml, curriculum/curriculum.json and plans/SC1-* are byte-identical (git diff --stat empty). Out-of-slice hunks in the same commit range: tests/labs/E1/lab-E1-L03-1.py-e, tests/labs/LX1, plans/M5-open-items.md, plans/FINAL-ARCHITECT-RULINGS.md (not verified by this slice). Commands: git diff -U0 50559266 HEAD -- course/modules/SC/SC1/cards.json; cards_pin_compare_r19.py -> out/cards_pin_compare_r19.out (removed SC1-c217 L06, added SC1-c243 L02, changed c110/c119/c122 L06; 81 L01-L03 records JSON-identical at HEAD).",
})
NEW.append({
    "id": "SC1a-r19-card-c243", "check": "2.7-cards",
    "location": "course/modules/SC/SC1/cards.json:344-351 (SC1-c243, lesson L02)",
    "status": "FAIL",
    "evidence": "SC1-c243 front: 'In Lesson 2, what is the construction of Brownian motion?' back: 'The sequence of partial sums Σ_M, and its limit Σ(t)=lim_M Σ_M(t), which Proposition 2.4 shows exists on an event of probability one.' No grade, no basis, cite []. Two defects against BUILDER_RULES §7: (a) 'Each card tests one fact': the card asks for the construction (a definition) and also states the a.s. existence of the limit, a graded theorem conclusion (L02.html:145-165, Proposition 2.4, data-grade T; the same content is graded T at SC1-c032 and SC1-c220). (b) A card stating a theorem statement carries its grade and basis, which this card omits. The mathematics is correct (see SC1a-r19-c243-proposition-content).",
    "fix": "Split the card. Keep the definition only: front 'In Lesson 2, how is Σ(t) defined?' back 'Σ(t)=lim_M Σ_M(t), the pointwise limit of the partial sums, on the outcomes where the limit exists.' Put the probability-one statement on its own card with \"grade\": \"T\" and \"basis\": \"Proposition 2.4(a) and (b), Section 3\". Then rerun cards_struct_r19.py and check_pages.py --unit SC1.",
})
NEW.append({
    "id": "SC1a-r19-c243-proposition-content", "check": "2.4-math",
    "location": "course/modules/SC/SC1/L02.html:145-158 (Proposition 2.4 conclusion at :151, proof (a) at :156-158); cards.json:344-351",
    "status": "PASS",
    "evidence": "L02.html Proposition 2.4 conclusion: (a) P(Ω*)=1; (b) for every outcome in Ω*, Σ(t)=lim_M Σ_M(t) exists for every t in [0,1], the convergence is uniform, and Σ is continuous. Proof (a) at L02.html:156-158 gives P(Ω*)=lim P(A_m0) ≥ 1 by Assumption 2.1(c). So 'the limit exists on an event of probability one' is what Proposition 2.4 shows. The card's mathematical content is correct; its defect is the rule failure in SC1a-r19-card-c243.",
})
NEW.append({
    "id": "SC1a-r19-cards-struct", "check": "2.7-cards",
    "location": "course/modules/SC/SC1/cards.json (all 227 cards; 82 L01-L03)",
    "status": "PASS",
    "evidence": "ledgers/SC1/scripts/SC1-a-r19/cards_struct_r19.py -> out/cards_struct_r19.out: 227 distinct ids (no duplicate id); exact duplicate fronts: none; exact duplicate backs: 'They are independent.' (SC1-c208 and SC1-c210, with different fronts, not duplicate cards); grade values T 49, C 6, absent 27 among L01-L03; grade and basis are paired on every card; no card has a non-empty cite list among L01-L03. Numbered references in each card (Lemma, Proposition, Theorem, Remark, Example, Corollary, Definition, Problem, Assumption, Lab) occur in the lesson pages; the two 'Problem R1/R2/E3' tokens are the labelled problems R1, R2 and E3 of L03.html:354, :365, :372 (the checker's token form is stricter than the page's label form).",
})
NEW.append({
    "id": "SC1a-r19-lab-mutants-all-38", "check": "2.5-labs-mutants",
    "location": "ledgers/SC1/lab-mutants/** (38 files) vs L01.html, L02.html, L03.html expected blocks",
    "status": "PASS",
    "evidence": ALL + ". Every file is KILLED by a non-zero exit, a stderr write, or a token mismatch with the expected block (tolerance per the page's data-tolerance). Lab twins are demonstrations; this row is evidence hygiene.",
})

# carried rows and custom prefixes
CUSTOM_CARRY = {
    "SC1a-r17-card-c017-definition-fixes": "cards.json record SC1-c017 JSON-identical to 50559266 (cards_pin_compare_r19.py -> out/cards_pin_compare_r19.out) and L01.html byte-identical",
    "SC1a-r18-card-c017": "cards.json record SC1-c017 JSON-identical to 50559266 (cards_pin_compare_r19.py -> out/cards_pin_compare_r19.out) and L01.html byte-identical",
}

rows_out = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in RE:
        new = RE[rid]
        row = {
            "id": rid,
            "check": r["check"],
            "location": r["location"],
            "status": new["status"],
            "evidence": new["evidence"],
        }
        if new["status"] != "PASS":
            row["fix"] = new["fix"]
        rows_out.append(row)
        continue
    if rid in CUSTOM_CARRY:
        ev = f"Carried from round 18 ({CUSTOM_CARRY[rid]}): {r['evidence']}"
    else:
        ev = f"Carried from round 18 ({r['location']} byte-identical since the previous pin {PIN18}): {r['evidence']}"
    rows_out.append({"id": rid, "check": r["check"], "location": r["location"], "status": r["status"], "evidence": ev})

assert len({r["id"] for r in rows_out}) == len(rows_out)
rows_out += NEW

mutants = []
for p in mutant_files:
    name = os.path.basename(p)
    mutants.append({
        "id": p,
        "description": f"lab-twin mutant (demonstration, not a grader mutant): {name}",
        "killed_by": "kill_lab_mutants_r19.py: " + kill_lines[name],
    })

counts = {s: sum(1 for r in rows_out if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
verdict = "PASS" if counts["PASS"] == len(rows_out) else "FAIL"
fragment = {
    "unit": "SC1",
    "slice": "a",
    "round": 19,
    "verifier": "Haiku independent verifier, SC1-a round 19 (did not build SC1)",
    "pin": "cd4dd7df",
    "base": "50559266 (round-18 pin). Round-18 fragment /Users/billyribeiro/.fanout/frags/E-SC1-a.round18.json used as context: PASS rows carried only where the cited subject is byte-identical; non-PASS and changed-subject rows re-verified.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE19-SC1-a (detached at cd4dd7df; .venv symlinked; vendor copied)",
    "scratch": "none; cards.json at each pin is read with git show inside cards_pin_compare_r19.py (no temp files kept). All scripts under ledgers/SC1/scripts/SC1-a-r19/, outputs under ledgers/SC1/scripts/SC1-a-r19/out/",
    "verified_at": datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows_out,
    "mutants": mutants,
    "registry_flags": prev["registry_flags"],
    "freshness_flags": [],
    "notes": (
        "ROUND 19 at cd4dd7df. Delta from 50559266 for the slice: cards.json only (SC1-c243 added at L02, lines 344-351; L06 hunks "
        "c110, c119, c122, c217 are outside the slice); lab-mutants q1..q3 re-added by cd4dd7df. index.html, L01-L03.html, project.html, "
        "L04-L08.html, tests/labs/SC1 twins, notation, references, tools and curriculum are byte-identical to 50559266. Every hunk in the slice "
        "was read. The round-18 UNVERIFIABLE row SC1a-r16-lab-q1-q3-new is PASS: the three twins exist and are killed. "
        "New defect: SC1-c243 fails BUILDER_RULES §7 (two facts in one card; graded theorem content with no grade or basis). Fix in SC1a-r19-card-c243. "
        "Gates re-run at cd4dd7df: check_pages, check_dag, check_projects, run_labs (L01-L03), twins under python -I -W error (rc 0, empty stderr), "
        "page_vs_twin, page_smoke alone for index, L01, L02, L03, ruff check and format, mypy --no-incremental (385 files), pytest -k SC1 (11), "
        "verify_refs offline (560, 0 problems) and unit SC1 (1 of 560, 0 problems). Lab-twin mutants 38/38 killed. "
        "Not run: run_graders and mutate_graders (no grader in slice a), render_curriculum, build_site --check, fetch_data --check (outside slice a). "
        "Not re-read line by line this round: L04-L08 and project.html (carried by byte-identity, as in round 18). "
        "Historical delta rows SC1a-r15-delta-read and SC1a-r17-delta-read record no commit range and no hunk claim; they are PASS only as "
        "superseded history."
    ),
    "summary": {
        "text": f"SC1-a round 19 at cd4dd7df: verdict {verdict}. Non-PASS: SC1a-r16-cards-grade-field, SC1a-r18-cards-full-scan (FAIL, both from SC1-c243), SC1a-r19-card-c243 (FAIL).",
        "counts": counts,
        "mutants": "38 of 38 lab-twin mutants killed",
    },
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(fragment, f, ensure_ascii=False, indent=2)
    f.write("\n")
print("rows", len(rows_out), counts, "mutants", len(mutants), "verdict", verdict)
