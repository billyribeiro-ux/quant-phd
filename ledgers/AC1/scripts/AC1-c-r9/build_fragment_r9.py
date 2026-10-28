"""Build ledgers/AC1/AC1-c.json (round 9) from the round-8 row ids, re-verified and carried rows, and new rows."""
import json
import sys
from pathlib import Path

CHECKOUT = Path(sys.argv[1])
prev = json.load(open("/tmp/fanout-frags/AC1-c.round8.json", encoding="utf-8"))
CARRY = ("Carried from round 8 (course/modules/AC/AC1/L07.html and L08.html cited lines byte-identical since the "
         "previous pin 2c8162b; the only changed lines are L07 :59, :73, :339, :341, L08 :51 and cards c102, c109): ")

# Round-9 re-verification of previously non-PASS or subject-changed rows, and fresh re-runs.
FRESH = {
    "AC1-c-cmd-run_labs": ("tools/run_labs.py --unit AC1 (run this round): PASS (11/11); both twins run under "
                           "python -I -W error with rc=0 (see AC1-c-lab-twin-run)"),
    "AC1-c-lab-twin-run": ("python -I -W error tests/labs/AC1/lab-AC1-L07-1.py and lab-AC1-L08-1.py: rc=0 each; "
                           "outputs in /tmp/verify9-AC1-c/lab_L07.out and lab_L08.out"),
    "AC1-c-lab-embed-equals-twin": ("ledgers/AC1/scripts/AC1-c-r9/embed_and_expected_check.py: embedded code in "
                                    "L07.html and L08.html equals the twin file (True, True)"),
    "AC1-c-lab-expected-output": ("embed_and_expected_check.py: expected block equals fresh run output, L07 18/18 "
                                  "lines, L08 13/13 lines"),
    "AC1-c-lab-seed-sweep": ("ledgers/AC1/scripts/AC1-c-r9/seed_sweep_r9.py: both twins pass for all SEED 0-199 "
                             "(200/200 each); supports L07 E2 and L08 E3 'pass for any seed'"),
    "AC1-c-cmd-page_smoke": "tools/page_smoke.py --unit AC1 --pages L07 L08 (this round): PASS for both pages",
    "AC1-c-cmd-check_pages_dag": "tools/check_pages.py --unit AC1: PASS; tools/check_dag.py --unit AC1: PASS (this round)",
    "AC1-c-cmd-pytest_ruff_mypy": ("ruff check . PASS; ruff format --check . 212 files formatted; mypy --no-incremental "
                                   "Success 153 files; pytest tests/test_labs.py -k AC1 PASS; pytest "
                                   "tests/test_page_checks.py PASS (this round)"),
    "AC1-c-cit-verify_refs": ("tools/verify_refs.py --unit AC1 (live): 2 of 560 entries, 0 problems; "
                              "tools/verify_refs.py --offline: 560 entries, 0 problems (this round)"),
    "AC1-c-num-L07-prose": ("Recomputed in ledgers/AC1/scripts/AC1-c-r9/recompute_prose_r9.py and by hand: Example 1.4 "
                            "(1,200,000 cents, 300,000 base), M1 (133,333 / 133,334), M3 NI 18,666.67, Example 2.3; "
                            "lines L07:85-86, :292-305, :320-334 and :341 re-read; PASS"),
    "AC1-c-num-L07-table": ("Lab output (this round) year 3 SBC 57,822.92 = recomputed 5,782,292 cents; L07:358 "
                            "matches; PASS"),
    "AC1-c-num-L08-table": ("Lab output (this round) rows match; L08:262-265 and :300-301 read; PASS"),
    "AC1-c-num-L08-prose": ("recompute_prose_r9.py: Example 1.4 DTL 4,200/6,300/6,300/4,200/0; Example 2.2 CT 6,300, "
                            "DE 4,200, TE 10,500; M2 DTL 2,100/1,680/0, DE -420; M3 CT 10,920 and 12,180; R2 TE3 13,700 "
                            "gap 1,200; E1 14,010 = 30% of 46,700; E2 10,131.24; PASS"),
    "AC1-c-math-L07": ("L07:59 now reads 'a whole number of shares n_g >= 0' and L07:68 'exact in cents' follows from "
                       "integer n_g and integer-cent f_g (Def 1.1); Thm 1.3 proof (L07:77-81) and Thm 2.1 / Cor 2.2 "
                       "(L07:99-114) re-derived; PASS"),
    "AC1-c-notation": ("notation/notation.json: pages use only standard LaTeX macros (Delta, mathrm, frac, lfloor, "
                       "rfloor, sum, tau, phi), no registered macro is redefined and no registered symbol (Phi, gamma_3, "
                       "R_f, R^*, Q) is used with another meaning (script scan this round); PASS"),
    "AC1-c-dag-concepts": "tools/check_dag.py --unit AC1: PASS (this round); def-stock-based-compensation and def-deferred-taxes unique",
    "AC1-c-banned-phrases": ("grep -E over L07.html, L08.html, cards.json (this round): no 'roughly', 'about <n>', "
                             "'historically', 'typically' used as evidence, '...', 'builder', 'verifier', 'round N'; "
                             "L07:73 and L08:51 new text clean; PASS"),
    "AC1-c-cards-dup-scan": ("cards.json: 126 cards, ids AC1-c001 to AC1-c126, 0 duplicate ids (this round). Round 8 "
                             "said 125; the file holds 126 and the pin 2c8162b also holds 126"),
    "AC1-c-cards-L07-L08": ("cards c091-c104, c105-c121, c125 re-read against the current lesson text; c102 "
                            "('Holding operating income fixed') matches Corollary 2.2; c109 matches Definition 1.2; PASS"),
    "AC1-c-registry-absence": ("both pages: 'This page cites no registry key' (L07.html:441, L08.html:383); "
                               "L08.html:287 is the only other mention; grep for data-ref/doi/isbn: none; PASS. "
                               "Round-8 locator L07.html:442 was off by one (pin 2c8162b also has it at :441)"),
    "AC1-c-new-L07-R2-bonus": ("L07.html:338-341: the R2 question was rewritten to an equity-settled grant that vests in "
                               "year y, so the cash-bonus comparison the model cannot answer is gone; the solution "
                               "(:341) gives the cash, net income and APIC effects from Def 1.1 with v=1 (P1), Sec 2 "
                               "display, and Cor 2.2 and says the model computes no share count (Def 1.2 (v)); PASS"),
    "AC1-c-r4-L07-misc-R2-R3": ("L07.html:283 (misconception 2, P2 reference) and :285 (misconception 3 nonnegativity, "
                                "checked: floor(C/v) and remainder >= C/v) re-derived; :341 PASS (as AC1-c-new-L07-R2-bonus); "
                                "R3 solution :345 re-read: breaks Def 1.2 (i), Thm 1.3 no longer follows, no total stated; PASS"),
    "AC1-c-r5-L07-line341-R2": "L07.html:341 (R2 solution, rewritten): no bonus comparison; each claim re-derived; PASS",
    "AC1-c-r7-L07-R2-bonus-cash": ("L07.html:341: the cash effect of the grant is stated from Corollary 2.2 and "
                                   "Thm 2.1 (b): cash unchanged; no bonus cash effect is claimed; PASS"),
    "AC1-c-r5-L08-line51-signed": ("L08.html:51 rewritten: exact in integer cents when pretax income is a multiple of 100 "
                                   "cents; checked: C multiple of 10,000 and C/L multiple of 100 (Def 1.1), tau_t = C p_t/100 "
                                   "multiple of 100, r whole, so CT, DE, TE and DTL = rK/100 are integers; PASS"),
    "AC1-c-r7-lab-student-mutants": ("UNVERIFIABLE in this checkout: the round-7 mutant scripts (ledgers/AC1/scripts/"
                                     "AC1-c-r7/seed_sweep_and_mutants.sh) and the m8a, m7a, m7b definitions are not in "
                                     "/tmp/verify9-AC1-c, and this verifier did not read another round's checkout. "
                                     "Analogous student-error mutants were run this round (AC1-c-r9-new-mutants, m9a-m9g: "
                                     "all 7 killed)"),
    "AC1-c-r8-lab-student-mutants": ("UNVERIFIABLE in this checkout: the round-8 mutant set (ledgers/AC1/scripts/AC1-c-r8/"
                                     "mutants_and_sweep.sh, new_mutants.sh) is not in /tmp/verify9-AC1-c and its exact "
                                     "mutations are not recorded in the round-8 fragment. Analogous mutants m9a-m9g run this "
                                     "round, all killed"),
    "AC1-c-r7-alt-implementations": ("ledgers/AC1/scripts/AC1-c-r9/mutants_r9.py: alt9a (round-half-up base), alt9b "
                                     "(remainder in first vesting year, L07), alt9c (deferred from the difference, L08): "
                                     "all three exit 0; the assertions accept valid alternatives; PASS"),
    "AC1-c-figures-none": "grep for svg, img, figure, figures-L in L07.html and L08.html: no matches (this round); PASS",
    "AC1-c-hours-L07": "L07.html:2 data-hours=11; index.html:156 card 'L07 · 11 h'; PASS",
    "AC1-c-hours-L08": ("L08.html:2 data-hours=10; index.html:157 'L08 · 10 h'; lesson hours L01-L08 sum 11+12+11+11+12+12+11+10 = 90 "
                        "= index.html:39 split (computed this round); PASS"),
    "AC1-c-L08-sec2-integer-cents": ("L08.html:58, :82, :88 re-read; Def 1.1 and Sec 2 exactness sentence are consistent with "
                                     "the recomputed integer identities; PASS"),
    "AC1-c-L08-R1-sign-claim": "L08.html:279 (R1 solution) re-derived: K_1 = K_2 = -A, K_3 = 0; DE_t signs; identity (c) condition sum tau = sum b = A; PASS",
    "AC1-c-lesson-structure": ("L07.html and L08.html re-read in full: sections 1-8, Lab 1 with hypothesis / code / expected / "
                               "interpretation, misconceptions, problem set tiers, key results, quiz, references; PASS"),
    "AC1-c-quiz-L08-numeric": "L08.html quiz numeric keys re-derived this round (4200, 6300, 8400, 10500, -420, 1961.40); PASS",
    "AC1-c-quiz-L07": "L07.html quiz keys re-derived this round (4000, 1333.33, 18666.67, 3000); PASS",
    "AC1-c-r8-L07-line59-shares-integer": ("L07.html:59 now 'a whole number of shares n_g >= 0' (was 'a number of shares'); "
                                           "with integer f_g in cents, C_g is integer cents, so 'exact in cents' at :68 holds; PASS"),
    "AC1-c-r8-L07-line73-dilution-gloss": ("L07.html:73 now 'dilution, which is a fall in each existing holder's proportionate "
                                           "ownership when new shares are issued' (was 'a rise in the number of shares "
                                           "outstanding'); this is the standard meaning of dilution, given as a gloss and cited "
                                           "to no source; PASS"),
    "AC1-c-r8-L07-R2-unanswerable": ("L07.html:339 and :341: the question now asks for the grant's effect on cash, net income "
                                     "and APIC, and whether the model computes shares; answerable from Def 1.1, Thm 2.1, Cor 2.2 "
                                     "and Def 1.2 (v); PASS"),
}
NEW_FAIL = {
    "AC1-c-r7-L08-216-so-clause": (
        "FAIL",
        "course/modules/AC/AC1/L08.html:216 (Section 3, canon breaks, third paragraph)",
        "Re-verified from scratch this round, overriding round 7's PASS. The sentence 'its balance is zero at year L by "
        "Theorem 2.1 (c), so it cannot show how many temporary differences a real firm holds at once' gives a non-sequitur: "
        "the zero balance at year L (Theorem 2.1 (c), checked by the lab's assert previous_dtl == 0) does not limit how many "
        "differences a firm holds. The stated limit comes from the single asset and single schedule, the first clause only.",
        "Replace the sentence with: 'The model has one asset and one tax schedule, so it cannot show how many temporary "
        "differences a real firm holds at once. Its balance is zero at year L by Theorem 2.1 (c).'",
    ),
}
UNVERIFIABLE = {"AC1-c-r7-lab-student-mutants", "AC1-c-r8-lab-student-mutants"}
NEW_ROWS = [
    {"id": "AC1-c-r9-delta-read", "check": "1-delta round-8 pin 2c8162b to round-9 pin 96dd532 (slice paths)",
     "location": "course/modules/AC/AC1/L07.html:59,73,339,341; L08.html:51; cards.json c102, c109; tests/labs/AC1 unchanged",
     "status": "PASS",
     "evidence": "git diff 2c8162b 96dd532 -- course/modules/AC/AC1/L07.html L08.html cards.json tests/labs/AC1 (read in full, every hunk). "
                 "Labs and twins unchanged since 2c8162b (empty diff). The other AC1 hunks (L01-L03, project, grader) are outside this slice"},
    {"id": "AC1-c-r9-new-mutants", "check": "2.5-labs new student-error mutants m9a-m9g (all must FAIL)",
     "location": "tests/labs/AC1/lab-AC1-L07-1.py; tests/labs/AC1/lab-AC1-L08-1.py; ledgers/AC1/scripts/AC1-c-r9/mutants_r9.py",
     "status": "PASS",
     "evidence": "mutants_r9.py: m9a no remainder in last vesting year (AssertionError), m9b vesting off by one, m9c APIC sign, "
                 "m9d CFO without add-back (L07, all AssertionError); m9e current tax ignores the difference, m9f DTL sign flipped, "
                 "m9g DTL without the rate (L08, all AssertionError). 7 of 7 killed. Output in /tmp/AC1-v/AC1-c/mutants_r9.out"},
    {"id": "AC1-c-r9-alt-implementations-seeds", "check": "2.5-labs over-constraint and seed claims",
     "location": "ledgers/AC1/scripts/AC1-c-r9/mutants_r9.py (alt9a-c); ledgers/AC1/scripts/AC1-c-r9/seed_sweep_r9.py",
     "status": "PASS",
     "evidence": "Valid alternatives exit 0: round-half-up base (L07), remainder in first year (L07), deferred expense from the "
                 "difference (L08). Seeds 0-199: 200 of 200 pass for each lab"},
    {"id": "AC1-c-r9-prose-recompute", "check": "2.2-numbers: every worked figure recomputed independently this round",
     "location": "course/modules/AC/AC1/L07.html:85-86, :99, :118-119, :268, :292-305, :322-334; L08.html:77-78, :100, :234-246, :250-254, :262-268, :279, :283, :300-301",
     "status": "PASS",
     "evidence": "ledgers/AC1/scripts/AC1-c-r9/recompute_prose_r9.py (integer cents, Fraction): all worked figures reproduced; "
                 "lab table year 3 = 5,782,292 cents; L08 peak 2,942.10 = 0.21 x 14,010"},
    {"id": "AC1-c-r9-embed-expected", "check": "2.5-labs embed equals twin and expected block equals run",
     "location": "course/modules/AC/AC1/L07.html:127-267; L08.html:108-208; ledgers/AC1/scripts/AC1-c-r9/embed_and_expected_check.py",
     "status": "PASS",
     "evidence": "embedded code == twin (True, True); expected block == fresh run output (18/18 and 13/13 lines)"},
]

rows = []
carried_ids = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in NEW_FAIL:
        status, loc, ev, fix = NEW_FAIL[rid]
        rows.append({"id": rid, "check": r["check"], "location": loc, "status": status, "evidence": ev, "fix": fix})
    elif rid in UNVERIFIABLE:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "UNVERIFIABLE",
                     "evidence": FRESH[rid],
                     "fix": "Re-run the round-7/8 mutant definitions from a checkout that holds their scripts, or commit the "
                            "mutant list under ledgers/AC1/mutants/ so the next verifier can re-run them"})
    elif rid in FRESH:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": FRESH[rid]})
    else:
        carried_ids.append(rid)
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": CARRY + r["evidence"]})
rows += NEW_ROWS

mutants = [
    {"id": "m9a", "description": "L07 last vesting year takes the base, dropping the remainder", "killed_by": "AssertionError in lab-AC1-L07-1 (schedule_ok == N_GRANTS)"},
    {"id": "m9b", "description": "L07 vesting window off by one (index > vest_years)", "killed_by": "AssertionError in lab-AC1-L07-1"},
    {"id": "m9c", "description": "L07 APIC change sign reversed", "killed_by": "AssertionError in lab-AC1-L07-1 (apic_ok)"},
    {"id": "m9d", "description": "L07 cash-flow statement without the SBC add-back", "killed_by": "AssertionError in lab-AC1-L07-1 (cfo_ok)"},
    {"id": "m9e", "description": "L08 current tax computed on pretax income, ignoring the temporary difference", "killed_by": "AssertionError in lab-AC1-L08-1 (tax_ok)"},
    {"id": "m9f", "description": "L08 deferred tax balance sign flipped", "killed_by": "AssertionError in lab-AC1-L08-1 (deferred_ok)"},
    {"id": "m9g", "description": "L08 deferred tax balance without the tax rate", "killed_by": "AssertionError in lab-AC1-L08-1 (deferred_ok, tax_ok)"},
]

frag = {
    "unit": "AC1",
    "slice": "AC1-c",
    "round": 9,
    "round_note": ("round 9 (independent re-verification of AC1-c after the round-8 fixes at 96dd532). Delta read from 2c8162b "
                   "(round-8 pin) to 96dd532. All 75 round-8 ids are kept. Carried PASS rows carry the required prefix; rows whose "
                   "subject changed or whose status was non-PASS were re-verified. One new FAIL (L08:216 'so' clause) and two "
                   "UNVERIFIABLE rows (previous mutant sets not present in this checkout)."),
    "verifier": "independent verifier (Haiku 5.5), slice AC1-c round 9; did not build AC1 and shares no context with its builders or earlier verifiers",
    "pin": "96dd532",
    "base": "2c8162b (round-8 pin, for the delta)",
    "checkout": str(CHECKOUT),
    "scratch": "/tmp/AC1-v/AC1-c",
    "verified_at": "2026-10-28T00:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "scripts": [
        "ledgers/AC1/scripts/AC1-c-r9/embed_and_expected_check.py",
        "ledgers/AC1/scripts/AC1-c-r9/mutants_r9.py",
        "ledgers/AC1/scripts/AC1-c-r9/seed_sweep_r9.py",
        "ledgers/AC1/scripts/AC1-c-r9/recompute_prose_r9.py",
        "ledgers/AC1/scripts/AC1-c-r9/build_fragment_r9.py",
    ],
    "notes": [
        "Not checked: the Pyodide browser runtime; the 10 s bound was measured only in local Python via page_smoke.",
        "Not checked: other slices (L01-L06, project, grader, cards outside c091-c126 except the c102/c109 delta).",
        "Not checked: the round-7 and round-8 mutant definitions (scripts not in this checkout); marked UNVERIFIABLE, not guessed.",
        "Live verify_refs was run; the registry has no entry for these topics. Live check passed (2 of 560 entries, 0 problems).",
        "Round-8 evidence corrections: registry-absence locator is L07.html:441 (not :442); the card count is 126 (not 125).",
        "Hours: lesson-hour sum 90 equals the hub split; no per-hour pace estimate was used to fail a row (architect ruling).",
    ],
    "summary": "FAIL: L07 round-8 FAILs (line 59, line 73, R2 unanswerable) re-verified and now PASS; L08 line 51 PASS; one new FAIL "
                "(L08:216 causal 'so' clause); two previous mutant rows UNVERIFIABLE because their scripts are not in this checkout.",
}
out = CHECKOUT / "ledgers/AC1/AC1-c.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
ids_prev = [r["id"] for r in prev["rows"]]
print("previous ids:", len(ids_prev), "kept:", all(i in {r["id"] for r in rows} for i in ids_prev))
print("carried:", len(carried_ids), "total rows:", len(rows))
