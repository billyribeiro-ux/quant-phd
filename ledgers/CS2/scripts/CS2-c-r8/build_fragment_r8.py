"""CS2-c-r8: assemble ledgers/CS2/CS2-c.json from the round-7 rows (carried or re-verified) and this round's rows."""

from __future__ import annotations

import datetime
import json
import sys

ROOT = sys.argv[1]
S = ROOT + "/ledgers/CS2/scripts/CS2-c-r8/"
r7 = json.load(open("/Users/billyribeiro/.fanout/frags/S-CS2-c.round7.json", encoding="utf-8"))
prev = {r["id"]: r for r in r7["rows"]}

PFX_LESSON = (
    "Carried from round 7 (L09.html, L10.html, L11.html, index.html, the CS2 lab twins, references/, notation/, "
    "tools/, course/modules/M/M1/ byte-identical since the previous pin aa659725; git diff --quiet aa659725 4540351d "
    "run this round):"
)
PFX_CARD = (
    "Carried from round 7 (cards.json entries {ids} JSON-equal between aa659725 and 4540351d; "
    "ledgers/CS2/scripts/CS2-c-r8/card_delta_r8.out):"
)

CARRY_LESSON = ["C-10", "C-11", "C-12", "C-13", "C-14"] + [f"C-{i}" for i in range(15, 27)] + \
    ["C-27", "C-28", "C-29", "C-30", "C-31", "C-32", "C-33", "C-34", "C-35", "C-36", "C-37", "C-38", "C-40",
     "C-41", "C-42", "C-43", "C-56", "C-58", "C-61", "C-62", "C-64", "C-69", "C-70", "C-71", "C-72", "C-73", "C-74"]
CARRY_CARD = {
    "C-44": "CS2-c116", "C-45": "CS2-c126", "C-46": "CS2-c135", "C-48": "CS2-c205", "C-50": "CS2-c151, CS2-c235, CS2-c217",
    "C-51": "CS2-c138", "C-57": "CS2-c236", "C-65": "CS2-c150", "C-66": "CS2-c151", "C-67": "CS2-c135",
    "C-78": "CS2-c125", "C-79": "CS2-c139", "C-80": "CS2-c194",
}

RERUN = {}

RERUN["C-01"] = (
    "Re-run on 4540351d: `.venv/bin/python tools/check_pages.py --all` printed every unit PASS, exit 0 "
    "(ledgers/CS2/scripts/CS2-c-r8/check_pages_all.txt); `tools/check_pages.py --unit CS2` printed "
    "'check_pages CS2: PASS', exit 0 (check_pages_unit.txt). Covers cards.json unique ids (198 of 198 unique), lesson "
    "existence, grades and cite keys."
)
RERUN["C-02"] = (
    "Re-run: `tools/check_dag.py --all` exit 0, 'check_dag CS2: PASS' among 27 PASS lines (check_dag_all.txt). "
    "L09, L10, L11 and index.html are byte-identical since aa659725."
)
RERUN["C-03"] = (
    "Re-run: `.venv/bin/python tools/run_labs.py --unit CS2` printed 'run_labs CS2: PASS (14/14)', exit 0 "
    "(ledgers/CS2/scripts/CS2-c-r8/run_labs_unit.txt)."
)
RERUN["C-04"] = (
    "Re-run alone: `env -i PATH=/usr/bin:/bin .venv/bin/python -I -W error tests/labs/CS2/lab-CS2-L09-1.py` (and L10, L11): "
    "exit 0 and stderr 0 bytes for each (twin_L09.err, twin_L10.err, twin_L11.err). L11 stdout equals the round-7 "
    "stdout line for line (the only difference is the appended exit line)."
)
RERUN["C-05"] = (
    "Re-run each page alone: `tools/page_smoke.py --unit CS2 --pages modules/CS/CS2/L09.html` (then L10, L11) each "
    "printed 'page_smoke CS2: PASS', exit 0 (page_smoke_L09.txt, page_smoke_L10.txt, page_smoke_L11.txt)."
)
RERUN["C-06"] = (
    "Re-run: `.venv/bin/ruff check .` 'All checks passed!' exit 0 (ruff_check.txt); `.venv/bin/ruff format --check .` "
    "'555 files already formatted' exit 0 (ruff_format.txt). No .py file in the slice changed since aa659725."
)
RERUN["C-07"] = (
    "Re-run: `.venv/bin/mypy --no-incremental` 'Success: no issues found in 386 source files', exit 0 (mypy.txt). "
    "The count is 386 where round 7 had 385 because tests/test_lx1_project_lab3.py was added elsewhere in the range."
)
RERUN["C-08"] = (
    "Re-run: `.venv/bin/python -m pytest -q tests/test_labs.py -k 'CS2 and (L09 or L10 or L11)'` exit 0 "
    "(pytest_labs_cs2_l09_l11.txt); `pytest -q tests/test_docs_figures.py tests/test_run_labs.py tests/test_page_smoke.py` "
    "exit 0 (pytest_misc.txt); `pytest -q tests/test_page_checks.py` exit 0 (pytest_page_checks.txt). Dot output; "
    "exit codes are the observed result. The -k filter was applied to each file separately, not to the whole list."
)
RERUN["C-09"] = (
    "Re-run: `.venv/bin/python tools/verify_refs.py --offline` 'offline integrity: 560 entries, 0 problems', exit 0 "
    "(verify_refs_offline.txt). references/ is byte-identical since aa659725; the live run was not repeated (network; no "
    "reference changed)."
)
RERUN["C-39"] = (
    "Lesson part carried (L09.html, L10.html, L11.html byte-identical since aa659725). Card part re-run: a case-sensitive scan "
    "of all 49 L09-L11 cards (front and back) for we, our, you, I, note, recall, round, verifier, builder, orchestrator, "
    "TODO, TBD, placeholder found no hit (ledgers/CS2/scripts/CS2-c-r8/process_words_r8.out). A case-insensitive scan "
    "matched only the index variable 'i' in math, not a process word."
)
RERUN["C-47"] = (
    "Re-verified because cards.json:1217 (CS2-c200) changed in this delta. The question is unchanged and asks the L11 "
    "Theorem 2.4 question. The new back states Theorem 2.4's hypotheses (L11.html:107-108) and the chain through Theorem "
    "2.2(b) (L11.html:86), Definition 2.1 (L11.html:76) and Lemma 2.3 (L11.html:96-104). See C-75, C-81 and C-95."
)
RERUN["C-49"] = (
    "Re-run: CS2-c207 absent from course/modules/CS/CS2/cards.json (card_delta_r8.out: 'absent CS2-c207 True')."
)
RERUN["C-52"] = (
    "Re-run: CS2-c225 absent (card_delta_r8.out: 'absent CS2-c225 True')."
)
RERUN["C-59"] = (
    "Re-run: CS2-c195 absent (card_delta_r8.out: 'absent CS2-c195 True')."
)
RERUN["C-60"] = (
    "Re-run: CS2-c199 absent (card_delta_r8.out: 'absent CS2-c199 True')."
)
RERUN["C-53"] = (
    "Re-run on 4540351d: cards.json has 198 entries and 198 unique ids (card_delta_r8.out). No two cards share the same "
    "front and back. Near-duplicates were reviewed by question and scope and are not duplicate cards: CS2-c200 and "
    "CS2-c147 both state E <= epsilon n (c200 asks why and gives the proof chain; c147 asks what bounds the error); "
    "CS2-c231 and CS2-c132 both state Theorem 2.4's 2n bound (c231 is the Lab 1 instance with N = 200); CS2-c245 and "
    "CS2-c148 both state the Theorem 2.5 guarantee (c245 is the Lab 1 instance). Observation only; no FAIL."
)
RERUN["C-54"] = (
    "Re-run: every numeric token (excluding 0 to 3) in the front and back of the 49 L09-L11 cards occurs in that card's own "
    "lesson text with tags stripped (card_delta_r8.out: missing list empty). Covers c231 (400, 200, 396, 399), c244 "
    "(9.258e-16, 8.852e-11, 7.449e-08, 1.269e-14, 10^6, 10^9) and c245 (0.0212, 0.0442, 1/20, 1/10, nine)."
)
RERUN["C-55"] = (
    "Re-verified against the current lesson text for the four changed cards: c200 vs L11.html:76, 86, 96-104, 107-108 and "
    "114; c231 vs L10.html:97-99 (Theorem 2.4) and 206-211 (printed totals and interpretation); c244 vs L09.html:207-216 "
    "and 322 (E3 solution); c245 vs L11.html:107-127, 144 and 257-259. The 45 other L09-L11 cards are JSON-equal to "
    "aa659725 (card_delta_r8.out) and their lessons are byte-identical."
)
RERUN["C-63"] = (
    "Re-verified: c194 (cards.json:1202) is JSON-equal to aa659725 and is a T card whose answer is Theorem 2.2's hypothesis 3 "
    "(L09.html:99) and the Section 3 canon break (L09.html:224). c200 (cards.json:1217) is a T card whose answer is the proof "
    "chain of Theorem 2.4 (L11.html:107-114). Neither is a printed reading. c244 and c245 are scored under C-76 and C-77."
)
RERUN["C-68"] = (
    "Re-run: CS2-c225 absent (card_delta_r8.out) and CS2-c118 (cards.json:799) JSON-equal to aa659725, so the duplicate "
    "check against the absent card stands."
)
RERUN["C-75"] = (
    "Re-verified: the back of CS2-c200 (cards.json:1217) now opens 'Assume the values are added in order, epsilon is fixed "
    "in (0, 1) with the capacities of Definition 2.1, arithmetic is exact, and n >= 1.' Theorem 2.4's hypotheses are "
    "'Those of Theorem 2.2, with n >= 1, and the capacities of Definition 2.1' (L11.html:108), and Theorem 2.2's are the "
    "three items (values added in order; epsilon in (0,1) with the Definition 2.1 capacities; exact arithmetic; "
    "L11.html:86). The preamble carries all four. It matches the sibling CS2-c147 (cards.json:982). The round-7 FAIL is "
    "resolved."
)
RERUN["C-76"] = (
    "Re-verified: CS2-c244 (cards.json:1412-1415) back now gives the reason: 'A candidate mechanism is that Welford's update "
    "rounds the running mean at each value, and those rounding errors enter the later deviations. The lesson states this as a "
    "hypothesis that Lab 1 does not test.' The second sentence is supported by L09.html:322 (E3 solution: 'This is a "
    "hypothesis about the mechanism ... Lab 1 shows the ordering on one stream and does not test the mechanism'). The card "
    "is no longer a bare printed reading. Grade C with basis 'Lab 1, offsets 0, 10^6 and 10^9 (SIMULATED stream, one seed)'. "
    "See C-91 and C-92. The round-7 FAIL is resolved."
)
RERUN["C-77"] = (
    "Re-verified: CS2-c245 (cards.json:1420-1423) back now states why the guarantee holds: the Theorem 2.4 hypotheses, then "
    "'The guarantee holds for every stream meeting these hypotheses by Theorem 2.5, which uses E <= epsilon n from Theorem 2.4, "
    "and Theorem 2.4 uses Lemma 2.3.' Theorem 2.5 (L11.html:118-119) and its proof (L11.html:122-127) use Theorem 2.4's "
    "E <= epsilon n, and Theorem 2.4's proof uses Lemma 2.3 (L11.html:114). Lab 1 remains the example (L11.html:259). The "
    "round-7 FAIL is resolved. See C-93 and C-94."
)
RERUN["C-81"] = (
    "Chain re-derived for CS2-c200. Theorem 2.2(b): C_h k_h 2^h <= n (L11.html:86), so C_h 2^h <= n/k_h. Definition 2.1: "
    "k_h >= (h+1)(h+2)/epsilon (L11.html:76), so n/k_h <= epsilon n/((h+1)(h+2)). Lemma 2.3 (L11.html:96-104) bounds the "
    "sum by 1. Independent check (ledgers/CS2/scripts/CS2-c-r8/c245_c200_recheck.out): k_h >= (h+1)(h+2)/epsilon for h = 0 "
    "to 199 with Fraction arithmetic at both epsilons, and the Lemma 2.3 identity and bound for H = 0 to 199, all True. "
    "E = sum C_h 2^h is Theorem 2.4's definition (L11.html:108)."
)
RERUN["C-82"] = (
    "Re-verified: 9.258e-16, 8.852e-11 and 7.449e-08 match the L09 expected block (L09.html:207, 211, 215) and "
    "twin_L09.out. The two-pass values 2.819e-17, 4.357e-17 and 1.269e-14 are all at or below 1.269e-14 (L09.html:208, "
    "212, 216). In this round, welford_mechanism_c244.py run under python -I -W error (welford_mechanism_c244.out) prints "
    "'welford as lab' relative errors 9.258e-16, 8.852e-11 and 7.449e-08 at offsets 0, 10^6 and 10^9, so the card's "
    "numbers reproduce. Basis 'Lab 1, offsets 0, 10^6 and 10^9 (SIMULATED stream, one seed)' is named and the grade is C."
)
RERUN["C-83"] = (
    "Re-verified: 0.0212 N and 0.0442 N match the L11 expected block (L11.html:257-258), the interpretation (L11.html:259), "
    "and this round's fresh recheck (c245_c200_recheck.out: excess/N 0.0212 at epsilon 1/20 and 0.0442 at 1/10, all nine "
    "probes pass both inequalities, deficit 0). Basis 'Lab 1 (SIMULATED stream, one seed)' is correct for grade C."
)
RERUN["C-84"] = (
    "Re-run of the delta from aa659725 to 4540351d (card_delta_r8.out): added none, removed none, changed CS2-c200, "
    "CS2-c231, CS2-c244, CS2-c245. The file has 198 entries, 198 unique ids. The diff is 5 insertions and 5 deletions, all "
    "one-for-one line replacements, so line numbers are unchanged. L09-L11 cards: 49 (43 T, 6 C); every C card has a basis "
    "and no T card does. No other CS2 card changed in this range."
)
RERUN["C-85"] = (
    "Notation of the four changed cards against notation/notation.json (8 registered symbols, 8 macros). The new text uses "
    "n, epsilon, E, C_h, k_h, h, w, q, v, R(v), R^-(v), #{x < v}, qN and N. N is conventionally local (the notation.json "
    "header says so). c231 defines N = 200 in its front; c245 uses the lesson's N = 5000 stream (L11.html:144). E is the plain-text compaction error "
    "total defined at L11.html:108; the registered \\E macro is the expectation operator and cards are plain text, so there "
    "is no clash. No registered symbol is used with another meaning."
)
RERUN["C-86"] = (
    "Process and hedge words in the four changed cards (process_words_r8.out, case-sensitive). No 'we', 'our', 'you', "
    "'note', 'recall', 'round', 'verifier' or 'builder'. 'candidate' in c244 hedges a mechanism that the lesson labels as "
    "a hypothesis (L09.html:322). 'Assume' preambles in c200 and c245 are mathematical hypotheses."
)
RERUN["C-87"] = (
    "Scope words in the changed cards (scope_words_r8.out, this round). c200 'all levels h': the sum is finite because only "
    "finitely many C_h are nonzero (L11.html:114). c245 'all nine probes' is the lab's assertion (L11.html:259); 'every "
    "stream meeting these hypotheses' is Theorem 2.5 with its hypotheses (L11.html:118-119). c244 'each value' is the "
    "mechanism step at each of the 2000 steps (L09.html:322); 'same three offsets' is the lab's printed offsets. c231 "
    "'each' refers to both printed deques (L10.html:206-210). Each scope word has a computation or a named hypothesis."
)

NEW = []
NEW.append({
    "id": "C-88",
    "check": "2.7 hypotheses rule (verifier item 10): Theorem 2.4 hypotheses carried by every card that states it, applied to CS2-c231",
    "location": "course/modules/CS/CS2/cards.json:1330-1333 (CS2-c231); L10.html:97-98 (Theorem 2.4 hypotheses)",
    "status": "FAIL",
    "evidence": (
        "The back states Theorem 2.4's conclusion ('Theorem 2.4 bounds the appends and removals of n insertions by 2n') and "
        "omits its hypotheses (L10.html:98): (1) w >= 1 is fixed; (2) the series has n >= 1 values inserted at positions "
        "0 to n-1; (3) the values are real numbers and comparisons are exact. Sibling CS2-c132 (cards.json:884, L10 T card "
        "on the same theorem) states them. C-75 required the same for CS2-c200 in round 7; the builder fixed c200 in this "
        "delta but not c231. Severity LOW. The lab's w values (1, 2, 5, 13, 30) and n = 200 satisfy the hypotheses, so the "
        "numbers are not affected."
    ),
    "fix": (
        "Prefix the back with: 'Assume w >= 1 is fixed, the series has n >= 1 values inserted at positions 0 to n - 1, and "
        "the values are real with exact comparisons.' (as CS2-c132 does), then keep the sentence about N = 200 and the lab."
    ),
})
NEW.append({
    "id": "C-89",
    "check": "2.2/2.4 CS2-c231 printed totals vs the L10 lab output",
    "location": "course/modules/CS/CS2/cards.json:1332 (back); L10.html:206-211; tests/labs/CS2/lab-CS2-L10-1.py",
    "status": "PASS",
    "evidence": (
        "Re-run under python -I -W error (twin_L10.out, stderr 0 bytes): per window the operation totals are min/max 399/399 "
        "(w=1), 398/399 (w=2), 398/398 (w=5), 397/398 (w=13), 396/397 (w=30), so the card's 'from 396 to 399 across the five "
        "window sizes, for both deques' is exact. The bound printed is 2N = 400, matching the expected block (L10.html:206-210) "
        "and the interpretation (L10.html:211). Basis 'Lab 1 (SIMULATED series, one seed)' is correct for grade C."
    ),
})
NEW.append({
    "id": "C-90",
    "check": "2.4 CS2-c231 front: N = 200 and the 2N bound against the lab's N and Theorem 2.4",
    "location": "course/modules/CS/CS2/cards.json:1332 (front); tests/labs/CS2/lab-CS2-L10-1.py:3,16; L10.html:97-103",
    "status": "PASS",
    "evidence": (
        "The lab defines N = 200 (lab-CS2-L10-1.py:16) and its claim line (line 3) says 'a seeded integer series of N = 200 "
        "values'. The card's 2N = 400 is 2n at n = 200. Theorem 2.4's conclusion ('the number of appends and removals ... is "
        "at most 2n') is stated the same way in L10.html:97-103 and its proof counts n appends and at most n removals. "
        "The card's claim matches; the hypothesis gap is C-88."
    ),
})
NEW.append({
    "id": "C-91",
    "check": "2.5 CS2-c244 attribution: 'the lesson states this as a hypothesis that Lab 1 does not test'",
    "location": "course/modules/CS/CS2/L09.html:322 (E3 solution); cards.json:1415 (CS2-c244 back)",
    "status": "PASS",
    "evidence": (
        "L09.html:322 (E3 solution): 'One candidate mechanism: ... Welford's update does update a running mean at each of the "
        "2000 steps, and those rounding errors can enter the later deviations. This is a hypothesis about the mechanism. Lab 1 "
        "shows the ordering on one stream and does not test the mechanism.' The card's sentence is the same claim in shorter "
        "form, so the attribution is accurate."
    ),
})
NEW.append({
    "id": "C-92",
    "check": "2.5 CS2-c244 candidate mechanism: independent check of the hedged claim",
    "location": "ledgers/CS2/scripts/CS2-c-r8/welford_mechanism_c244.py (tracked, not modified; run this round)",
    "status": "PASS",
    "evidence": (
        "welford_mechanism_c244.py run under python -I -W error (welford_mechanism_c244.out). At offsets 10^6 and 10^9, "
        "rounding the mean at each step while keeping the sum of squared deviations exact reproduces the lab's Welford error "
        "exactly (8.852e-11 and 7.449e-08). Keeping the mean exact instead gives 6.796e-16 and 5.028e-16. So the rounded "
        "running mean is the source at these offsets, which is consistent with the card's hedged candidate. The card does not "
        "claim it is verified, and the lesson says Lab 1 does not test it; no FAIL."
    ),
})
NEW.append({
    "id": "C-93",
    "check": "2.2/2.5 CS2-c245 numbers re-derived by an independent implementation",
    "location": "ledgers/CS2/scripts/CS2-c-r8/c245_c200_recheck.py and .out; cards.json:1423 (CS2-c245 back)",
    "status": "PASS",
    "evidence": (
        "Own implementation of Definition 2.1 (in-order recursive push, as the twin lines 58-63 do) with exact Fraction counts "
        "by linear scan instead of bisect. Output: eps 1/20: 151 compactions, excess/N 0.0212, deficit 0, all 9 probes pass; "
        "eps 1/10: 305 compactions, excess/N 0.0442, deficit 0, all 9 probes pass. These match the card and L11.html:257-258. "
        "My first draft compacted with a LIFO stack, which pushed kept items out of order and printed 0.0454 at eps 1/10; the "
        "error was in my script, not the card, and the reported output is from the corrected script."
    ),
})
NEW.append({
    "id": "C-94",
    "check": "2.4 CS2-c245 proof chain attribution: Theorem 2.5 uses Theorem 2.4, which uses Lemma 2.3",
    "location": "course/modules/CS/CS2/L11.html:98-104, 107-114, 118-127; cards.json:1423",
    "status": "PASS",
    "evidence": (
        "Theorem 2.5's hypotheses are 'Those of Theorem 2.4' (L11.html:119). Its upper and lower counts use Theorem 2.4's "
        "R^- and R bounds and 'E <= epsilon n' (L11.html:125-126). Theorem 2.4's bound on E uses Lemma 2.3 (L11.html:114). "
        "The card's chain matches, and the guarantee 'for every stream meeting these hypotheses' is a T claim with its "
        "hypotheses listed in the same back."
    ),
})
NEW.append({
    "id": "C-95",
    "check": "2.4 CS2-c200 hypotheses equal Theorem 2.4's hypotheses (Theorem 2.2's plus n >= 1 and Definition 2.1)",
    "location": "course/modules/CS/CS2/L11.html:86, 107-108; cards.json:1220 (CS2-c200 back)",
    "status": "PASS",
    "evidence": (
        "Theorem 2.2 hypotheses (L11.html:86): values added in order; epsilon fixed with 0 < epsilon < 1 and the Definition 2.1 "
        "capacities; exact arithmetic on weights and capacities. Theorem 2.4 (L11.html:108): those of Theorem 2.2, with n >= 1, "
        "and the capacities of Definition 2.1. The card's preamble lists the same four items in the same order."
    ),
})
NEW.append({
    "id": "C-96",
    "check": "2.2 CS2-c200 scope word 'all levels h' against the finiteness argument",
    "location": "course/modules/CS/CS2/L11.html:114; cards.json:1220 (CS2-c200 back)",
    "status": "PASS",
    "evidence": (
        "The card sums C_h 2^h 'over all levels h'. L11.html:114 proves that only finitely many C_h are nonzero (if C_h >= 1 "
        "then 2^h <= n), so the sum is finite and the 'all' is correct."
    ),
})

rows = []
for rid in [f"C-{i:02d}" for i in range(1, 88)]:
    if rid in RERUN:
        rows.append({
            "id": rid,
            "check": prev[rid]["check"],
            "location": prev[rid]["location"],
            "status": "PASS",
            "evidence": RERUN[rid],
        })
    elif rid in CARRY_LESSON:
        rows.append({
            "id": rid,
            "check": prev[rid]["check"],
            "location": prev[rid]["location"],
            "status": "PASS",
            "evidence": PFX_LESSON + " " + prev[rid]["evidence"],
        })
    elif rid in CARRY_CARD:
        rows.append({
            "id": rid,
            "check": prev[rid]["check"],
            "location": prev[rid]["location"],
            "status": "PASS",
            "evidence": PFX_CARD.format(ids=CARRY_CARD[rid]) + " " + prev[rid]["evidence"],
        })
    else:
        raise SystemExit(f"row {rid} has no disposition")
rows.extend(NEW)

# every round-7 PASS row must be carried or re-run, and round-7 FAIL rows must be re-decided
for rid in ("C-75", "C-76", "C-77"):
    assert rid in RERUN, rid
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"

now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL")}
verdict = "PASS" if counts["FAIL"] == 0 else "FAIL"

fragment = {
    "unit": "CS2",
    "slice": "c",
    "round": 8,
    "verifier": "Haiku independent verifier, CS2-c round 8 (closing delta verification; did not build CS2; no builder context)",
    "pin": "4540351dc664559cdfd371b908f2b4e644cf4297",
    "base": "aa6597255304919b9c4e5e5ca07763ae3e13d45c (round-7 pin; round-7 fragment /Users/billyribeiro/.fanout/frags/S-CS2-c.round7.json read as context only; its PASS rows were not trusted, and every round-7 FAIL was re-decided)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS8-CS2-c (detached at 4540351d; .venv symlinked)",
    "scratch": "ledgers/CS2/scripts/CS2-c-r8/ (every script and output that backs a row is kept there)",
    "verified_at": now,
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [
        "ledgers/CS2/scripts/CS2-c-r8/ already held a tracked file welford_mechanism_c244.py (committed in 4540351d). This verifier did not modify it; it ran it and wrote welford_mechanism_c244.out beside it.",
        "ledgers/CS2/CS2-c.json was overwritten by this round's fragment, as the protocol requires; the round-7 fragment in /Users/billyribeiro/.fanout/frags/ was read as context only.",
    ],
    "notes": (
        "Delta from aa659725 to 4540351d for the slice: only course/modules/CS/CS2/cards.json changed in CS2 (card_delta_r8.out: "
        "CS2-c200, c231, c244, c245 changed; none added or removed). L09.html, L10.html, L11.html, index.html, the three lab "
        "twins, tests/labs/CS2, references/, notation/, tools/ and course/modules/M/M1/ are byte-identical to aa659725 "
        "(git diff --quiet). Every hunk in the slice was read: c200 (preamble added), c231 (N = 200 added to the front; "
        "no Theorem 2.4 preamble was added to c231), c244 (mechanism sentence added), c245 (preamble and Theorem 2.5 chain added). "
        "Round-7 FAIL rows C-75, C-76 and C-77 are resolved by the c200, c244 and c245 edits and are PASS here; the new "
        "FAIL is C-88 (c231 omits Theorem 2.4's hypotheses, the same defect C-75 recorded for c200). "
        "Observations, not FAILs: near-duplicate pairs c200/c147, c231/c132 and c245/c148 are different questions "
        "(why vs what, lab instance vs general statement) and are recorded under C-53. The round-7 cards count of 204 "
        "was a count error in round 6 and is not used here. Outside the slice and not checked this round: CS2-c008 and "
        "CS2-c241 (L01 cards changed or removed in the round-7 range), other CS2 slices, other units. Mutants: none; this is a lesson slice with no "
        "project grader, so mutation testing does not apply (the rule that lab twins are demonstrations)."
    ),
    "summary": (
        f"CS2 slice c, round 8 (closing delta verification from aa659725 to 4540351d). {len(rows)} rows: "
        f"PASS {counts['PASS']}, FAIL {counts['FAIL']} (C-88 LOW: c231 omits Theorem 2.4's hypotheses). "
        "The round-7 FAILs C-75, C-76 and C-77 are resolved and re-verified. The four changed cards were re-derived: c200 "
        "chain and hypotheses correct; c244 reason and E3 attribution correct; c245 numbers re-derived independently (0.0212, "
        "0.0442); c231 printed totals correct. Gates re-run on 4540351d: check_pages --all and CS2, check_dag --all, "
        "check_projects --all, run_labs CS2 14/14, page_smoke L09/L10/L11 alone, twins under python -I -W error, ruff check "
        "and format, mypy 386 files, verify_refs --offline 560/0, pytest subsets. Mutants: none (lesson slice)."
    ),
}

out = ROOT + "/ledgers/CS2/CS2-c.json"
with open(out, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
print("wrote", out, "rows", len(rows), counts, "verdict", verdict)
