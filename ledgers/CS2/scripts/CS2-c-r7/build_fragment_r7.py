"""Builds the round-7 CS2-c fragment from the round-6 fragment (context) and this round's re-verification.

Carried rows keep their round-6 status and evidence only where the cited subject is byte-identical (lesson,
twin, reference and notation files by git diff --quiet e896b7a4 aa659725; card objects by JSON equality, see
card_delta.out). Every other row is re-verified this round and its evidence names the command or script.
"""

import json
import sys

ROOT = sys.argv[1]
PREV = "/Users/billyribeiro/.fanout/frags/S-CS2-c.round6.json"
OUT = f"{ROOT}/ledgers/CS2/CS2-c.json"
prev = json.load(open(PREV, encoding="utf-8"))
prev_rows = {r["id"]: r for r in prev["rows"]}

LESSON_FILES = (
    "course/modules/CS/CS2/L09.html, L10.html, L11.html, index.html, tests/labs/CS2/lab-CS2-L09-1.py, "
    "lab-CS2-L10-1.py, lab-CS2-L11-1.py, references/, notation/, tools/, course/modules/M/M1/"
)
CARD_NOTE = "cards.json objects {ids} JSON-equal between e896b7a4 and aa659725 (ledgers/CS2/scripts/CS2-c-r7/card_delta.out)"
SCR = "ledgers/CS2/scripts/CS2-c-r7/"

CARRY_LESSON = {"C-%02d" % i for i in list(range(10, 39)) + [40, 41, 42, 43, 56, 58, 61, 62, 64, 69, 70, 71, 72, 73, 74]}
CARRY_CARD = {
    "C-44": "CS2-c116", "C-45": "CS2-c126", "C-46": "CS2-c135", "C-48": "CS2-c205", "C-50": "CS2-c151, CS2-c235, CS2-c217",
    "C-51": "CS2-c138", "C-57": "CS2-c236", "C-65": "CS2-c150", "C-66": "CS2-c151", "C-67": "CS2-c135",
}

R = {}  # id -> (status, check, location, evidence)
def override(rid, status, location, evidence, check=None):
    R[rid] = (status, check or prev_rows[rid]["check"], location, evidence)

override("C-01", "PASS", prev_rows["C-01"]["location"],
         f"Re-run on aa659725: `.venv/bin/python tools/check_pages.py --unit CS2` printed 'check_pages CS2: PASS', exit 0 "
         f"({SCR}check_pages_unit.txt). Covers cards.json unique ids and lesson existence.")
override("C-02", "PASS", prev_rows["C-02"]["location"],
         f"Re-run: `tools/check_dag.py --all` exit 0, every line PASS including CS2 ({SCR}check_dag_all.txt). "
         "L09, L10, L11 and index.html byte-identical since e896b7a4.")
override("C-03", "PASS", prev_rows["C-03"]["location"],
         f"Re-run: `tools/run_labs.py --unit CS2` printed 'run_labs CS2: PASS (14/14)', exit 0 ({SCR}run_labs_unit.txt). "
         "Lab sections of L09-L11 and their twins are byte-identical since e896b7a4 (git diff --quiet).")
override("C-04", "PASS", prev_rows["C-04"]["location"],
         "Re-run alone under `env -i PATH=/usr/bin:/bin .venv/bin/python -I -W error tests/labs/CS2/lab-CS2-L09-1.py` "
         "(and L10, L11): exit 0, stderr 0 bytes for all three (twin_L09.err, twin_L10.err, twin_L11.err); "
         "stdout in twin_L09.out, twin_L10.out, twin_L11.out.")
override("C-05", "PASS", prev_rows["C-05"]["location"],
         "Re-run each page alone: `tools/page_smoke.py --unit CS2 --pages modules/CS/CS2/L09.html` (and L10, L11) "
         "printed 'page_smoke CS2: PASS', exit 0 (page_smoke_L09.txt, page_smoke_L10.txt, page_smoke_L11.txt).")
override("C-06", "PASS", prev_rows["C-06"]["location"],
         f"Re-run: `.venv/bin/ruff check .` 'All checks passed!' exit 0; `.venv/bin/ruff format --check .` "
         f"'554 files already formatted' exit 0 ({SCR}ruff.txt).")
override("C-07", "PASS", prev_rows["C-07"]["location"],
         f"Re-run: `.venv/bin/mypy --no-incremental` 'Success: no issues found in 385 source files', exit 0 ({SCR}mypy.txt).")
override("C-08", "PASS", prev_rows["C-08"]["location"],
         "Re-run: `.venv/bin/python -m pytest -q tests/test_labs.py -k 'CS2 and (L09 or L10 or L11)'` exit 0 "
         f"({SCR}pytest_labs_cs2_l09_l11.txt); `pytest -q tests/test_docs_figures.py tests/test_page_checks.py "
         f"tests/test_run_labs.py tests/test_page_smoke.py` exit 0 ({SCR}pytest_misc.txt). Dot output only; exit codes "
         "are the observed result.")
override("C-09", "PASS", prev_rows["C-09"]["location"],
         f"Re-run: `.venv/bin/python tools/verify_refs.py --offline` 'offline integrity: 560 entries, 0 problems', exit 0 "
         f"({SCR}verify_refs_offline.txt). references/ byte-identical since e896b7a4; the live run was not repeated "
         "(network; no reference changed).")
override("C-39", "PASS", prev_rows["C-39"]["location"],
         f"Re-run on the changed cards: {SCR}card_process_words.out scans all 49 L09-L11 cards for process and hedge words. "
         "The six changed cards (c125, c139, c194, c200, c244, c245) contain none; the only hits are mathematical uses "
         "('i' as an index, 'fixed' as in 'epsilon is fixed'). Lesson text is byte-identical since e896b7a4.")
override("C-47", "PASS", "course/modules/CS/CS2/cards.json:1217 (CS2-c200)",
         "Re-verified: CS2-c200 changed in this round and is now a T card on the Theorem 2.4 chain. Its content is correct "
         "against L11.html:84-115 (re-derived under C-81). It is atomic and not trivia. The missing hypotheses are recorded "
         "as C-75, not here.")
override("C-49", "PASS", "course/modules/CS/CS2/cards.json (CS2-c207 absent)",
         f"Re-verified at aa659725: CS2-c207 absent (card_delta.out); 198 cards with 0 duplicate ids (cards_r7_scan.out).")
override("C-52", "PASS", "course/modules/CS/CS2/cards.json (CS2-c225 absent)",
         "Re-verified at aa659725: CS2-c225 absent (card_delta.out).")
override("C-53", "PASS", "course/modules/CS/CS2/cards.json (whole deck, 198 cards)",
         f"Re-run of the whole-deck scan ({SCR}cards_r7_scan.py, .out): 198 cards, 0 duplicate ids; 11 near-duplicate pairs "
         "at difflib ratio >= 0.55 (c004/c005, c018/c019, c029/c219, c034/c175, c044/c045, c052/c176, c059/c178, "
         "c134/c137, c143/c226, c146/c149, c159/c175). Each pair asks a different fact, read from both cards. The six "
         "changed cards duplicate no other card. CS2-c225, the round-6 duplicate of c118, is absent.")
override("C-54", "PASS", "course/modules/CS/CS2/cards.json (all 49 L09-L11 cards)",
         f"Re-run ({SCR}cards_numbers_all_L09_L11.out): every numeric token in front or back of all 49 L09-L11 cards, "
         "other than the integers 0 to 20, appears in its lesson HTML ('absent: []'). Changed cards also in cards_r7_scan.out.")
override("C-55", "PASS", "course/modules/CS/CS2/cards.json (six changed cards vs current lessons)",
         "Re-verified against the current lesson text: c125 vs L09.html:218 and 235; c139 vs L10.html:67-73 and 85-92; "
         "c194 vs L09.html:98-99 and 224; c200 vs L11.html:84-115; c244 vs L09.html:207-217; c245 vs L11.html:144 and 257-259. "
         "The other L09-L11 cards are JSON-equal to e896b7a4 and their lessons are byte-identical.")
override("C-59", "PASS", "course/modules/CS/CS2/cards.json (CS2-c195 absent)",
         "Re-verified at aa659725: CS2-c195 absent (card_delta.out).")
override("C-60", "PASS", "course/modules/CS/CS2/cards.json (CS2-c199 absent)",
         "Re-verified at aa659725: CS2-c199 absent (card_delta.out).")
override("C-63", "PASS", "course/modules/CS/CS2/cards.json:1202 (CS2-c194), 1217 (CS2-c200)",
         "Round-6 FAIL is resolved. c194 is now a T card whose answer is Theorem 2.2's hypothesis 3 (exact arithmetic, "
         "L09.html:99) and L09 Section 3 (L09.html:224), not a printed reading; c200 is a T card whose answer is the proof "
         "chain of Theorem 2.4 (L11.html:107-115). Both were re-read in this round (cards_r7_scan.out). The new C cards "
         "c244 and c245 are scored under C-76 and C-77.")
override("C-68", "PASS", "course/modules/CS/CS2/cards.json:799 (CS2-c118); CS2-c225 absent",
         f"Re-verified: CS2-c225 absent; CS2-c118 JSON-equal to e896b7a4 (card_delta.out); the duplicate scan finds no "
         "pair sharing the Welford fact ({SCR}cards_r7_scan.out).".replace("{SCR}", SCR))

for rid, ids in CARRY_CARD.items():
    p = prev_rows[rid]
    assert p["status"] == "PASS", rid
    R[rid] = ("PASS", p["check"], p["location"],
              f"Carried from round 6 ({CARD_NOTE.format(ids=ids)}): " + p["evidence"])
for rid in sorted(CARRY_LESSON):
    p = prev_rows[rid]
    assert p["status"] == "PASS", rid
    R[rid] = ("PASS", p["check"], p["location"],
              f"Carried from round 6 ({LESSON_FILES} byte-identical since the previous pin, verified by git diff --quiet "
              f"e896b7a4 aa659725): " + p["evidence"])

# Non-PASS rows (round 7)
R["C-75"] = ("FAIL",
    "Theorem 2.4 hypotheses are carried by every card that states it (hypotheses rule, verifier item 10)",
    "course/modules/CS/CS2/cards.json:1217 (CS2-c200)",
    "The back states the Theorem 2.4 conclusion E <= epsilon n but omits Theorem 2.4's hypotheses: those of Theorem 2.2 "
    "(values added in order, epsilon fixed in (0, 1) with the capacities of Definition 2.1, exact arithmetic) and n >= 1 "
    "(L11.html:108). The sibling CS2-c147 (cards.json:982) states them, and round-2 precedent required them for c151, "
    "c235, c217. Severity LOW.")
R["C-76"] = ("FAIL",
    "Cards are not trivia: a card whose whole answer is one printed reading of Lab 1 is a FAIL (C-63 standard, BUILDER_RULES 7)",
    "course/modules/CS/CS2/cards.json:1412 (CS2-c244)",
    "The whole answer is printed readings of Lab 1 (three methods at three offsets, L09.html:207-216) with no stated reason. "
    "Its numbers are correct (C-82). This is the defect that C-63 recorded for the round-5 cards c194 and c200, which were "
    "fixed by rewriting them as T cards. Severity LOW. Fix: give the answer's reason (Welford's update rounds the running "
    "mean at each value, L09.html:224 and 239), with the Lab 1 figures as the C-graded example; or delete the card. "
    "If the orchestrator rules that printed-reading cards are allowed, record that ruling, because the same standard then "
    "applies to c194 and c200 in round 6.")
R["C-77"] = ("FAIL",
    "Cards are not trivia: a card whose whole answer is one printed reading of Lab 1 is a FAIL (C-63 standard, BUILDER_RULES 7)",
    "course/modules/CS/CS2/cards.json:1420 (CS2-c245)",
    "The whole answer is 'Yes' plus the printed excess values 0.0212 N and 0.0442 N and the lab's pass report "
    "(L11.html:257-259, key-results row L11.html:406). Numbers and basis are correct (C-83). Same standard as C-76. "
    "Severity LOW. Fix: state the reason the guarantee holds (Theorem 2.5, with E <= epsilon n from Theorem 2.4 and "
    "Lemma 2.3) and keep Lab 1 as the single-stream example; or delete the card. The same orchestrator ruling as C-76 applies.")

R["C-78"] = ("PASS", "CS2-c125 (changed): numbers, mechanism and grade",
    "course/modules/CS/CS2/cards.json:834 (CS2-c125, grade C, basis 'Lab 1, offset 10^9')",
    f"Re-derived in {SCR}recheck_r7_numbers.py/.out: 2e21 = n(1e9)^2 lies in [2^70, 2^71) (2^70 = 1.18e21, 2^71 = 2.36e21); "
    "the spacing there is 2^18 = 262144, so one rounding moves a value by at most 131072 (half-spacing), as L09.html:218 "
    "states; (n-1) s^2 = 1999 x 0.087281 = 174.47 (exact 174.4749), so 131072 exceeds it. 'Prints 0.000000e+00' matches "
    "L09.html:217 and twin_L09.out:line 9. Mechanism matches L09.html:218 and 235. C grade with a named basis is correct.")
R["C-79"] = ("PASS", "CS2-c139 (changed): T claim and 'not in general'",
    "course/modules/CS/CS2/cards.json:926 (CS2-c139, T)",
    f"Brute force {SCR}recheck_c139.py/.out: 3000 random series (n <= 30, w <= 8, ties included, 46328 positions) confirm "
    "that the front after position i equals i exactly when x_i <= every earlier value still in W_i, matching the card. "
    "'Not in general' holds: x = [1, 2], w = 2 gives fronts [0, 0]. Back matches Definition 2.1 step (2) (L10.html:67) and "
    "Theorem 2.3 (L10.html:85-92). Hypotheses (w >= 1, no NaN, exact comparisons) match Theorem 2.2 (L10.html:73-74).")
R["C-80"] = ("PASS", "CS2-c194 (changed): T claim with its hypothesis",
    "course/modules/CS/CS2/cards.json:1202 (CS2-c194, T)",
    "'Theorem 2.2 assumes exact arithmetic (hypothesis 3)' matches L09.html:99 (hypothesis (3)). 'Each subtraction, division "
    "and multiplication rounds' matches L09.html:224. The card does not say that only these operations round, and the "
    "lesson does not say so either. The conclusion 'the theorem does not bound the computed values' follows from the "
    "failed hypothesis (L09.html:224, 'this proof does not supply one'). Not a printed reading (see C-63).")
R["C-81"] = ("PASS", "CS2-c200 (changed): proof chain of Theorem 2.4 re-derived",
    "course/modules/CS/CS2/cards.json:1217 (CS2-c200, T)",
    "Chain checked against L11.html: Theorem 2.2(b) gives C_h k_h 2^h <= n (L11.html:86), so C_h 2^h <= n/k_h; Definition 2.1 "
    "gives k_h >= (h+1)(h+2)/epsilon (L11.html:76), so n/k_h <= epsilon n/((h+1)(h+2)); Lemma 2.3 (L11.html:98) bounds "
    f"the sum by 1, and the identity and k_h bounds were re-checked for H, h = 0..59 with Fractions "
    f"({SCR}recheck_r7_numbers.out). E = sum C_h 2^h is the definition in Theorem 2.4 (L11.html:108). The derivation is correct; "
    "the missing hypotheses are C-75.")
R["C-82"] = ("PASS", "CS2-c244 (new): printed numbers, two-pass bound and basis",
    "course/modules/CS/CS2/cards.json:1412 (CS2-c244, C, basis 'Lab 1, offsets 0, 10^6 and 10^9')",
    "9.258e-16, 8.852e-11, 7.449e-08 match L09.html:207, 211, 215 and twin_L09.out. The two-pass values 2.819e-17, "
    "4.357e-17, 1.269e-14 are all at or below 1.269e-14 (L09.html:208, 212, 216). An independent implementation (same seed "
    f"90, n = 2000) reproduces all printed values ({SCR}recheck_r7_numbers.out). The basis is named and the C grade is "
    "right. The card's form is the trivia issue in C-76.")
R["C-83"] = ("PASS", "CS2-c245 (new): claims against the lab code and output",
    "course/modules/CS/CS2/cards.json:1420 (CS2-c245, C, basis 'Lab 1 (SIMULATED stream, one seed)')",
    "twin_L11.out and L11.html:257: 'all 9 probes pass', excess 0.0212 N and 0.0442 N; 0.0212 < 0.05 and 0.0442 < 0.1. The twin "
    "(tests/labs/CS2/lab-CS2-L11-1.py, lines 241-246) counts #{x < v} and #{x <= v} exactly with bisect on the sorted stream "
    "and asserts both Definition 1.2 inequalities with Fraction arithmetic. An independent direct count reproduces 'True' for "
    f"all nine probes at both epsilons and the printed excess ({SCR}recheck_r7_numbers.out). The numbers and basis are right; "
    "the form is C-77.")
R["C-84"] = ("PASS", "cards.json delta since the previous pin: ids added, removed and changed",
    "course/modules/CS/CS2/cards.json",
    f"git show e896b7a4 and aa659725 cards.json compared by id ({SCR}card_delta.out): L09-L11 added c244, c245; changed c125, "
    "c139, c194, c200; removed none. Outside the slice: c008 changed and c241 removed (both L01), not checked. Deck: 198 "
    "entries at aa659725 (197 at e896b7a4). L09-L11: 49 cards (13, 13, 23); 43 T, 6 C; every C card has a basis and no T card "
    "does (cards_r7_scan.out).")
R["C-85"] = ("PASS", "Notation of the changed cards against notation/notation.json",
    "notation/notation.json; course/modules/CS/CS2/cards.json (changed cards)",
    "notation.json registers 8 program-wide symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q). The changed cards use "
    "n, N, q, epsilon, E, C_h, k_h, R(v), R^-(v), h, H, w, x_i, M_n and S_n, and none of these is registered or reused with "
    "another meaning (grep of the six changed cards). N, E, C_h, k_h and epsilon are defined locally in L11 (Definition 1.2, "
    "Definition 2.1, Theorem 2.4, and 'N = 5000' at L11.html:144).")
R["C-86"] = ("PASS", "Process and hedge words in the changed cards",
    f"course/modules/CS/CS2/cards.json (c125, c139, c194, c200, c244, c245)",
    f"{SCR}card_process_words.out: no round, verifier, builder, ruling, TODO, TBD, 'we' or 'our' in any L09-L11 card.")
R["C-87"] = ("PASS", "Scope words in the changed cards (all, every, only, same, any)",
    "course/modules/CS/CS2/cards.json:1217 (c200), 1412 (c244), 1420 (c245)",
    "c200's 'all compactions' is the definition of E (L11.html:108, 113). c244's 'the same three offsets' and c245's 'all nine "
    "probe quantiles' are the set the lab prints and asserts (L09.html:207-216; L11.html:257 'all 9 probes pass'). Each claim "
    "is computed for the printed set only, and the bases say 'one stream and one seed'.")

# assemble
rows = []
for rid in sorted(prev_rows, key=lambda x: int(x.split("-")[1])):
    if rid not in R:
        raise SystemExit(f"missing decision for {rid}")
    st, chk, loc, ev = R[rid]
    rows.append({"id": rid, "check": chk, "location": loc, "status": st, "evidence": ev})
FIXES = {
    "C-75": "Prefix the back with: 'Assume the values are added in order, epsilon is fixed in (0, 1) with the capacities of "
            "Definition 2.1, arithmetic is exact, and n >= 1.' (as CS2-c147 does).",
    "C-76": "Give the answer's reason (Welford's update rounds the running mean at each value, L09.html:224 and 239) and keep "
            "the Lab 1 figures as the C-graded example; or delete the card. Orchestrator to rule on printed-reading cards.",
    "C-77": "State why the guarantee holds (Theorem 2.5, with E <= epsilon n from Theorem 2.4 and Lemma 2.3) and keep Lab 1 as "
            "the single-stream example; or delete the card. Same ruling as C-76.",
}
for rid in ["C-75", "C-76", "C-77", "C-78", "C-79", "C-80", "C-81", "C-82", "C-83", "C-84", "C-85", "C-86", "C-87"]:
    st, chk, loc, ev = R[rid]
    row = {"id": rid, "check": chk, "location": loc, "status": st, "evidence": ev}
    if st != "PASS":
        row["fix"] = FIXES[rid]
    rows.append(row)
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)) == 87, len(ids)

counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
verdict = "PASS" if counts["PASS"] == len(rows) else "FAIL"
frag = {
    "unit": "CS2",
    "slice": "c",
    "round": 7,
    "verifier": "Haiku independent verifier, CS2-c round 7 (delta verification; did not build CS2; no builder context)",
    "pin": "aa6597255304919b9c4e5e5ca07763ae3e13d45c",
    "base": "e896b7a45344d1bc17ebfbf7fb05d87698ec9d6a (round-6 pin; round-6 fragment /Users/billyribeiro/.fanout/frags/S-CS2-c.round6.json, read as context only)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS7-CS2-c (detached at aa659725; .venv symlinked)",
    "scratch": "ledgers/CS2/scripts/CS2-c-r7/ (every script and output that backs a row is kept there)",
    "verified_at": sys.argv[2],
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [
        "ledgers/CS2/scripts/CS2-c-r7/ already held tracked files from an earlier pass (gates.sh, gates.log, html_notation_check.py, "
        "l09_claims.py, l10_claims.py, l11_claims.py, l11_property.py, lab_and_lt_check.py, numbers_l09.py). This verifier did not "
        "write or modify them (git status shows them unchanged), and wrote its own outputs beside them. The committed "
        "ledgers/CS2/CS2-c.json was overwritten by this round's fragment, as the protocol requires."
    ],
    "notes": (
        "Delta from e896b7a4 to aa659725 for the slice: only course/modules/CS/CS2/cards.json changed in the slice (c125, c139, "
        "c194, c200 changed; c244, c245 added). L09.html, L10.html, L11.html, index.html, the three twins, references/, notation/, "
        "tools/ and course/modules/M/M1/ are byte-identical to e896b7a4 (git diff --quiet). Every other change in the range (L04-L08, "
        "their twins, cards of L01, L04, L06, L07, L08, FINAL-ARCHITECT-RULINGS.md, KNOWN-ISSUES.md) is outside the slice and was not "
        "checked. Observation: the round-6 fragment states 204 cards for e896b7a4, but cards.json at e896b7a4 has 197 entries "
        "(git show count); this is a count error in round 6, and round 7 uses the 198 of aa659725. Observation: notation uses N for "
        "the number of values in L09's lab (n = 2000) and in L11's lab (N = 5000); each is defined locally, so no clash is recorded. "
        "Not checked: a live verify_refs run (network; no reference changed); render_curriculum.py --check (outside the slice's gate "
        "list); the full pytest suite (subsets only); visual screenshots (page_smoke geometry only, no figures on these pages); "
        "lessons L01-L08 and other slices; the statement 'the printed numbers are one run' is a lesson caveat and was read, not "
        "re-derived for other streams. No project grader in this slice, so no mutants were run."
    ),
    "summary": (
        f"CS2 slice c, round 7 (delta verification from e896b7a4 to aa659725). {len(rows)} rows: PASS {counts['PASS']}, "
        f"FAIL {counts['FAIL']} (C-75 LOW: c200 omits Theorem 2.4 hypotheses; C-76 LOW: c244 is a printed-reading card; "
        "C-77 LOW: c245 is a printed-reading card). The round-6 FAIL C-63 is resolved (c194 and c200 are T cards). The changed "
        "and new cards were re-derived: c125, c139, c194, c200 correct; c244 and c245 numbers correct. Gates re-run on aa659725 and "
        "all pass: check_pages CS2, check_dag --all, check_projects --all, build_site --check, run_labs CS2 14/14, page_smoke "
        "L09/L10/L11 alone, ruff check and format, mypy 385 files, pytest subsets, verify_refs --offline 560/0, and the twins under "
        "python -I -W error. Mutants: none (no project grader in this slice)."
    ),
}
json.dump(frag, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows", len(rows), counts, verdict)
