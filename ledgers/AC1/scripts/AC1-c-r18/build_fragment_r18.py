"""Round 18 (AC1-c): builds ledgers/AC1/AC1-c.json from the round-17 fragment and this round's re-runs.

Usage: python -I build_fragment_r18.py <checkout> <round17_fragment.json>
Carry rule: a round-17 PASS row keeps its status only when its cited subject is byte-identical
(the git diff fefbf8b..7143726 touches only L07.html:51, :412 and L08.html:51, :209 in this slice);
every other row is re-verified this round and its evidence is replaced.
"""

import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
prev = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
CARRY = (
    "Carried from round 17 (cited subject byte-identical since the previous pin fefbf8b; the slice diff "
    "touches only L07.html:51, :412 and L08.html:51, :209): "
)
CARD_CARRY = (
    "Carried from round 17 (cited card entries byte-identical since the previous pin; cards.json changed only "
    "at c060, an L04 card outside this slice): "
)

fresh = {
    "AC1-c-cmd-run_labs": "Re-run in round 18: `.venv/bin/python tools/run_labs.py --unit AC1` exit 0, output 'run_labs AC1: PASS (11/11)' (scratch run_labs.txt).",
    "AC1-c-lab-twin-run": "Re-run in round 18: `python -I -W error` on tests/labs/AC1/lab-AC1-L07-1.py and lab-AC1-L08-1.py both exit 0 (scratch run-L07.txt, run-L08.txt).",
    "AC1-c-lab-embed-equals-twin": "Re-run in round 18 with ledgers/AC1/scripts/AC1-c-r18/embed_and_run_check_r18.py: embedded data-run code equals the twin byte for byte (True) for L07 and L08.",
    "AC1-c-lab-expected-output": "Re-run in round 18: the expected blocks (L07.html:250-267, L08.html:196-208) equal the twin run output after strip (True for both labs).",
    "AC1-c-lab-seed-sweep": "Re-run in round 18 with ledgers/AC1/scripts/AC1-c-r18/seed_sweep_r18.py: both twins exit 0 for seeds 0,1,2,3,7,42,999,123456789,20260701,20260702. Supports L07.html:327 (E2) and L08.html:273 (E3) 'pass for any seed'.",
    "AC1-c-lab-hypothesis-scope": "Re-run in round 18: L07.html:126 says 4 of 4 schedules and 6 of 6 years, matching the run lines 263-267; L07.html:268 matches; L08.html:107 (three checks at 5 of 5) matches run lines 206-208; L08.html:209 'current tax is below ... by the deferred expense in years 1 and 2' matches the table (year 1: 8,169.84 vs 10,131.24, DE 1,961.40; year 2: 16,677.15 vs 17,657.85, DE 980.70).",
    "AC1-c-cmd-page_smoke": "Re-run in round 18: tools/page_smoke.py --unit AC1 exit 0; 'page_smoke modules/AC/AC1/L07.html: PASS', 'page_smoke modules/AC/AC1/L08.html: PASS', lab-AC1-L07-1 0.0 s, lab-AC1-L08-1 0.0 s.",
    "AC1-c-cmd-check_pages_dag": "Re-run in round 18: tools/check_pages.py --unit AC1 exit 0 ('check_pages AC1: PASS'); tools/check_dag.py --unit AC1 exit 0 ('check_dag AC1: PASS').",
    "AC1-c-cmd-pytest_ruff_mypy": "Re-run in round 18: pytest tests/test_labs.py tests/test_page_checks.py exit 0 (all dots); mypy --no-incremental on both twins 'Success: no issues found in 2 source files'; ruff format --check tests/labs/AC1 exit 0. ruff check reports 11 findings only in my own scratch scripts under ledgers/AC1/scripts/AC1-c-r18 (excluded from the repo gate by pyproject extend-exclude ledgers/*/scripts).",
    "AC1-c-cit-verify_refs": "Re-run in round 18: tools/verify_refs.py --unit AC1: 'live re-verification of AC1: 2 of 560 entries, 0 problems'; tools/verify_refs.py --offline: '560 entries, 0 problems'. The slice cites no registry key (grep of L07/L08 for data-references and citations: none).",
    "AC1-c-num-L07-prose": "Recomputed in round 18 by hand: Example 1.4 (1,200,000/4=300,000; $12,000 total), M1 (400,000/3=133,333; 2x133,333; 133,334), M2 (100,000 x4), M3 (NI2 18,666.67; APIC2+RE2=20,000), E1 year 3 vesting grants, E3 (619,799.00 net income in year 6), Example 2.3 ($50,000 - $3,000 = $47,000). Matches run lines 250-267 and the solutions at L07.html:295-341.",
    "AC1-c-num-L07-table": "Re-run in round 18: the expected block at L07.html:250-267 equals the twin output (see AC1-c-lab-expected-output); key result L07.html:358 '57,822.92 SCU' equals the year-3 sbc_expense in the run output (line 259). Class note: the table values are not pinned by any assertion (see AC1-c-r17-m17a-survivor).",
    "AC1-c-num-L08-table": "Re-run in round 18: expected block L08.html:196-208 equals the twin output; year-1 DTL 1,961.40 = 0.21 x 9,340.00; K at years 2-3 14,010.00 = 0.30 x 46,700.00; key results :300-301 match the rows.",
    "AC1-c-num-L08-prose": "Recomputed in round 18: Example 1.4 (K = 20,000, 30,000, 30,000, 20,000, 0; DTL 4,200, 6,300, 6,300, 4,200, 0 at 21%); Example 2.2 (CT1 6,300, DE1 4,200, TE1 10,500; CT2 8,400, DE2 2,100, TE2 10,500); M1 (30,000 x 25% = 7,500); M2 (DTL 2,100, 1,680, 0; DE 2,100, -420, -1,680); M3 (CT 8,400, 10,920, 12,180; TE 10,500 each); E1 (K 14,010 = 30% of 46,700; 0.21 x 14,010 = 2,942.10); E2 (8,169.84 + 1,961.40 = 10,131.24 = 0.21 x 48,244); R2 (CT3 12,500, DTL3 7,500, DTL2 6,300, DE3 1,200, TE3 13,700; 4 x 30,000/100 = 1,200).",
    "AC1-c-grades": "Re-read in round 18: grade spans and claim grades at L07.html:43-48 legend, :77 (T), :102 (T), :110 (T), :355-358 (T, T, T, C, C); L08.html:68, :91, :297-301 (T, C); cards c119, c120 (C) match the lab-based and proof-based statements.",
    "AC1-c-math-L07": "Re-derived in round 18: Def 1.1 floor/remainder schedule sums to C_g (Theorem 1.3 proof at :81 is algebraically correct); Theorem 2.1 (a)-(d) and Corollary 2.2 proofs at :106, :114 check; the 'nonnegative' argument at :285 holds since remainder >= C/v.",
    "AC1-c-math-L08": "Re-derived in round 18: Theorem 1.3 proof at :72; Theorem 2.1 (a)-(d) at :95 (telescoping, (c) by sum tau = C = sum b); P3 at :259 algebra (the d_t terms cancel). Section 2 exactness sentence at :88 is conditional; see AC1-c-r18-L08-why-it-matters for the over-broad attribution at line 51.",
    "AC1-c-notation": "Re-checked in round 18: notation/notation.json defines only program-wide macros (\\E, \\Prob, \\Var, ...) and states that letters with local meaning are defined in each lesson; L07/L08 use none of \\E, \\Prob, \\Var; P_t, K_t, DTL_t, CT_t, DE_t, TE_t, S_t, OI_t are local and defined on the page (L08.html:82; L07.html:91).",
    "AC1-c-dag-concepts": "Re-run in round 18: check_dag AC1 PASS; dfn ids unique (L07.html:59 def-stock-based-compensation; L08.html:64 def-deferred-taxes); the data-concept links in L07 (7 distinct) and L08 (7 distinct) resolve to defined concepts (check_pages PASS; deferred-taxes defined at L08.html:64, stock-based-compensation at L07.html:59).",
    "AC1-c-banned-phrases": "Re-scanned in round 18 (grep -i for roughly, about N, historically, ellipsis, builder, verifier, round N, REQUEST, typically, usually, always, only, all, same, drives, offsets, raises): hits at L07 :68, :78, :81, :99, :111, :268, :273, :281, :309, :311, :315, :323, :327, :337, :341, :358, :370, :371, :380, :403, :425 and L08 :55, :59, :64, :215, :223, :226-227, :279, :330, :350; each was read in context and is a stated model fact or a shown calculation. No process words; no banned phrase.",
    "AC1-c-scope-words": "Re-read in round 18: L08.html:64 (Def 1.2 'a positive balance is a liability') and :215 ('neither has a negative balance and neither shows an asset') unchanged; the 'same tax percentages' claim is checked against Example 1.4 and the lab TAX_PERCENT (40, 30, 20, 10, 0) (lab-AC1-L08-1.py:17).",
    "AC1-c-cards-dup-scan": "Re-run in round 18: cards.json has 139 cards for the unit (all lessons); duplicate ids 0; duplicate fronts 0. L07/L08 cards: 40 (c091-c121, c125, c129-c131, c135-c139). The earlier '125 cards' figure is superseded.",
    "AC1-c-cards-L07-L08": "Re-run in round 18: 40 L07/L08 cards (c091-c121, c125, c129-c131, c135-c139), each read against its lesson text: unchanged cards are byte-identical; the cards whose lesson lines changed in this round (none of the 40 cite L07:51, :412 or L08:51, :209) need no change.",
    "AC1-c-registry-absence": "Re-run in round 18: tools/verify_refs.py --offline 560 entries, 0 problems; L07.html:441-442 and footer :452 state 'This page cites no registry key'; L08.html:383-384 and :394 likewise; no citation attribute in either page.",
    "AC1-c-quiz-L07": "Re-read in round 18: L07.html:363-437 quiz keys: q1 (vesting years), numeric 4000, 1333.33, 18666.67, q5, q6, numeric 3000 (1,000 shares x $12 = 12,000 / 4), q8 (new option text, see AC1-c-r18-L07-q8-option), q9 (year 6), q10; each explain line matches its key.",
    "AC1-c-quiz-L08-numeric": "Re-read in round 18: L08.html:306-378 numeric keys 4200 (0.21 x 20,000), 6300 (0.21 x 30,000), 8400 (M2 current tax), 10500 (Theorem 2.1 (b)), -420 (M2 DE2), 1961.40 (run line 198); mc keys q1, q4, q7, q9, q10 match their explain lines.",
    "AC1-c-lesson-structure": "Re-run in round 18: check_pages AC1 PASS; both pages have the template sections (why-it-matters, Sections 1-3, misconceptions, problem set M/P/E/R, key results, quiz, references, lesson navigation), data-hours 11 and 10.",
    "AC1-c-figures-none": "Re-run in round 18: grep for <img, <svg, <canvas and figures- in L07.html and L08.html: 0 matches each. No live figure is claimed.",
    "AC1-c-hours-L07": "Re-checked in round 18: L07.html data-hours=11 (line 2); hub split data-hours-lessons=90 equals the sum of lesson data-hours (11+12+11+11+12+12+11+10 = 90), see AC1-c-r10-hours-sum.",
    "AC1-c-hours-L08": "Re-checked in round 18: L08.html data-hours=10 (line 2); included in the 90-hour lesson sum above.",
    "AC1-c-r5-L07-line51-why": "Re-verified in round 18 against the CURRENT L07.html:51: 'no forfeitures (an award lost by the employee before it vests)' matches Definition 1.2 (ii) at L07.html:73 ('lost by the employee before it vests'); the gloss is given where the term first appears. PASS.",
    "AC1-c-r5-L08-interp-209": "Re-verified in round 18 against the CURRENT L08.html:209: 'current tax is below the total tax expense by the deferred expense, which is positive in those years because the printed balance rises' matches the run table (years 1-2: TE - CT = DE = 1,961.40 and 980.70; DTL 0 -> 1,961.40 -> 2,942.10). 'Above the expense' in years 4-5 refers to the total tax expense of the same sentence; years 4 and 5 check: CT 10,711.89 > TE 9,731.19; CT 14,356.65 > TE 12,395.25. PASS.",
    "AC1-c-r17-delta-read": "Re-run in round 18: git diff --stat fefbf8b 7143726 -- course/modules/AC/AC1 tests/labs/AC1: slice files changed are L07.html (2 hunks: :51, :412), L08.html (2 hunks: :51, :209); cards.json only at c060 (L04, outside this slice); tests/labs/AC1/lab-AC1-L07-1.py and lab-AC1-L08-1.py byte-identical (git diff --quiet exit 0). Every hunk was read.",
    "AC1-c-r17-mutants-killed": "Re-run in round 18 with ledgers/AC1/scripts/AC1-c-r18/mutants_r18.py: m17b, m17c, m17d, m17e killed (AssertionError); alt17a passes (exit 0).",
    "AC1-c-r10-hours-sum": "Re-run in round 18: index.html data-hours-lessons=90 and data-hours-project=30; sum of lesson data-hours 90; hub split and lesson hours agree (arithmetic only; hours are design targets per the architect ruling).",
    "AC1-c-r10-mutants-killed": "Re-run in round 18 (mutants_r18.py): m10b, m10d, m10e killed (AssertionError).",
    "AC1-c-r10-alt-correct-implementations": "Re-run in round 18 (mutants_r18.py): alt9a, alt9b, alt9c, alt10a, alt10b, alt17a, alt18a, alt18b, alt18c all exit 0 (PASS); the lab accepts ceiling, half-up, cumulative-rounding and first-year-remainder variants.",
    "AC1-c-r7-alt-implementations": "Re-run in round 18: the alternative implementations alt9a-c, alt10a-b, alt17a, alt18a-c all pass (exit 0), so the lab's assertions do not over-constrain correct implementations.",
    "AC1-c-r7-lab-student-mutants": "Re-run in round 18: m7a, m7b, m8a are killed (AssertionError) by mutants_r18.py entries r7-m7a, r7-m7b, r7-m8a-L08-deferred-from-taxable.",
    "AC1-c-r17-card-c095": "CARD_CARRY",
}

carried_defaults = {}
rows_out = []
mutants_killed = [
    ("r7-m8a", "L08 deferred expense from taxable income, not the balance change", "AssertionError in lab-AC1-L08-1 (r18 re-run)"),
    ("r7-m7a", "L07 last-year branch disabled", "AssertionError in lab-AC1-L07-1 (r18 re-run)"),
    ("r7-m7b", "L07 base amount plus one cent", "AssertionError in lab-AC1-L07-1 (r18 re-run)"),
    ("r8-n2life", "L08 book depreciation over LIFE minus one", "AssertionError in lab-AC1-L08-1 (r18 re-run)"),
    ("r8-n3sign", "L08 deferred expense sign reversed", "AssertionError in lab-AC1-L08-1 (r18 re-run)"),
    ("r8-n4te", "L08 total tax expense omits the deferred part", "AssertionError in lab-AC1-L08-1 (r18 re-run)"),
    ("r9-m9a", "L07 last vesting year takes the base, dropping the remainder", "AssertionError in lab-AC1-L07-1 (r9, r18 re-run)"),
    ("r9-m9b", "L07 vesting window off by one (index > vest_years)", "AssertionError in lab-AC1-L07-1 (r9, r18 re-run)"),
    ("r9-m9c", "L07 APIC change sign reversed", "AssertionError in lab-AC1-L07-1 (r9, r18 re-run)"),
    ("r9-m9d", "L07 cash-flow statement without the SBC add-back", "AssertionError in lab-AC1-L07-1 (r9, r18 re-run)"),
    ("r9-m9e", "L08 current tax ignores the temporary difference", "AssertionError in lab-AC1-L08-1 (r9, r18 re-run)"),
    ("r9-m9f", "L08 deferred tax balance sign flipped", "AssertionError in lab-AC1-L08-1 (r9, r18 re-run)"),
    ("r9-m9g", "L08 deferred tax balance without the tax rate", "AssertionError in lab-AC1-L08-1 (r9, r18 re-run)"),
    ("r10-m10b", "L07 APIC change one cent short of the SBC expense", "AssertionError in lab-AC1-L07-1 (r10, r18 re-run)"),
    ("r10-m10d", "L08 deferred expense equals the balance, not its change", "AssertionError in lab-AC1-L08-1 (r10, r18 re-run)"),
    ("r10-m10e", "L08 current tax computed on pretax plus the difference", "AssertionError in lab-AC1-L08-1 (r10, r18 re-run)"),
    ("r17-m17b", "L07 vesting window one year long (index > vest_years)", "AssertionError in lab-AC1-L07-1 (r17, r18 re-run)"),
    ("r17-m17c", "L07 last vesting year takes the base", "AssertionError in lab-AC1-L07-1 (r17, r18 re-run)"),
    ("r17-m17d", "L08 tax depreciation uses the first percent every year", "AssertionError in lab-AC1-L08-1 (r17, r18 re-run)"),
    ("r17-m17e", "L08 cumulative temporary difference not accumulated", "AssertionError in lab-AC1-L08-1 (r17, r18 re-run)"),
    ("r18-m18b", "L07 cash change equals the APIC change", "AssertionError in lab-AC1-L07-1 (r18)"),
    ("r18-m18e", "L08 deferred expense uses a stale balance (previous balance never updated)", "AssertionError in lab-AC1-L08-1 (r18)"),
    ("r18-m18f", "L08 total tax expense adds the balance instead of the deferred expense", "AssertionError in lab-AC1-L08-1 (r18)"),
    ("r18-m18a", "L07 schedule check sums years 1 to 5 only (seed-dependent)", "AssertionError in lab-AC1-L07-1 under seeds 2, 3, 42, 999, 123456789 (seed sweep r18); shipped seed 20260701 not killed"),
]

for r in prev["rows"]:
    rid = r["id"]
    if rid in fresh:
        ev = fresh[rid]
        if ev == "CARD_CARRY":
            ev = CARD_CARRY + r["evidence"]
        status = r["status"]
        if rid == "AC1-c-r17-m17a-survivor":
            status = "FAIL"
        rows_out.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev})
    else:
        rows_out.append({"id": rid, "check": r["check"], "location": r["location"], "status": r["status"],
                         "evidence": (CARRY + r["evidence"]) if r["status"] == "PASS" else r["evidence"]})

# rows whose status changes or that carry a fresh FAIL
override = {
    "AC1-c-r17-m17a-survivor": {
        "status": "FAIL",
        "evidence": "Re-run in round 18 (ledgers/AC1/scripts/AC1-c-r18/mutants_r18.py, entry r17-m17a): exit 0, the mutant survives. The lab twin is byte-identical to fefbf8b, so no assertion pins the printed SBC row. The mutant's printed table is: year 1 0.00, year 2 29,769.58, year 3 36,889.58, year 4 57,822.92, year 5 47,894.58, year 6 20,933.34. This falsifies the page statements L07.html:268 ('expense in the table rises, peaks in year 3, and falls to zero in year 6') and :331 (year 6 expense 0.00), and the key result L07.html:358 (peak in year 3 at 57,822.92). The page states the behaviour, so this is a FAIL. The round-17 page sentences at :268 and :358 are unchanged in 7143726, so the fix is not made.",
        "fix": "Add a lab assertion that pins the printed SBC row to the Definition 1.1 schedule (for example compare sbc[i] with the per-year sums of yearly_expense computed independently, and assert the year-3 value 57,822.92 for seed 20260701), or remove the table-shape claims at L07.html:268 and :358 and state only the identities. Then re-run run_labs and embed the new expected block with tools/embed_labs.py --refresh lab-AC1-L07-1.",
    },
    "AC1-c-r5-L08-line51-signed": {
        "status": "FAIL",
        "evidence": "Re-verified against the CURRENT L08.html:51 (changed in 7143726). The sentence says 'the tax expense, the current tax ... and the deferred balance are exact in integer cents when pretax book income (P_t, defined in Section 2) is a multiple of 100 cents'. The deferred balance DTL_t = r K_t / 100 is exact for every P_t: Definition 1.1 makes C a multiple of 10,000 cents and b = C/L a multiple of 100 cents, so tau_t = C p_t / 100 and b_t are multiples of 100, K_t is a multiple of 100, and r K_t / 100 is an integer (run output balances 1,961.40, 2,942.10, 0.00 for this seed are integers in cents). The P_t condition is therefore not the basis for the balance, a basis stated more broadly than the evidence supports. The same over-broad 'requires' appears in Section 2 (L08.html:88), where the requirement is stated for 'each amount above' (CT, DE, TE, DTL) although only CT and TE need P_t to be a multiple of 100. Recomputed: K=(9,340, 14,010, 14,010, 9,340, 0) and DTL at 21% = (1,961.40, 2,942.10, 2,942.10, 1,961.40, 0.00), all integral.",
        "fix": "Rewrite L08.html:51 to: 'the current tax and the total tax expense are exact in integer cents when pretax book income (P_t, defined in Section 2) is a multiple of 100 cents, while the deferred expense and the deferred balance are exact for every P_t, because Definition 1.1 makes every tax and book amount a multiple of 100 cents.' Make the same split in L08.html:88 ('the model requires P_t ...' applies to CT_t and TE_t only).",
    },
    "AC1-c-r9-delta-read": {
        "status": "FAIL",
        "evidence": "Re-verified against the CURRENT L08.html:51, which is in this row's cited subject. The sentence changed in 7143726 and still carries the over-broad basis described at AC1-c-r5-L08-line51-signed (the deferred balance is exact for every P_t; the P_t condition is not its basis). Cards c102 and c109 and L07.html:59, :73, :339, :341 are unchanged and were re-read.",
        "fix": "Apply the fix at AC1-c-r18-L08-why-it-matters (split the exactness claim between the current tax/total tax expense and the deferred expense/balance).",
    },
    "AC1-c-r18-L08-why-it-matters": None,
}
for rid, ov in override.items():
    if ov is None:
        continue
    for row in rows_out:
        if row["id"] == rid:
            row.update({k: v for k, v in ov.items()})
            break

new_rows = [
    {"id": "AC1-c-r18-delta-read", "check": "1-delta round-17 pin to round-18 pin (slice paths)",
     "location": "git diff --stat fefbf8b 7143726 -- course/modules/AC/AC1 tests/labs/AC1",
     "status": "PASS",
     "evidence": "Every hunk in the slice was read: L07.html:51 (why-it-matters: forfeiture gloss), L07.html:412 (quiz q8 distractor), L08.html:51 (why-it-matters: P_t reference and the exactness claim), L08.html:209 (interpretation). cards.json changed only at c060 (an L04 card, outside this slice). Lab twins byte-identical (git diff --quiet exit 0). The other slices' files are not verified here."},
    {"id": "AC1-c-r18-L07-why-it-matters", "check": "2.2-why-it-matters L07 (forfeiture gloss, changed)",
     "location": "course/modules/AC/AC1/L07.html:51",
     "status": "PASS",
     "evidence": "'no forfeitures (an award lost by the employee before it vests)' matches Definition 1.2 (ii) at L07.html:73 ('No award is forfeited, that is, lost by the employee before it vests'). The gloss is given where the term first appears, before Section 1 uses it. The sentence does not add a claim about firms. Nothing in the lab depends on it."},
    {"id": "AC1-c-r18-L07-q8-option", "check": "2.9-quiz L07 q8 distractor (changed)",
     "location": "course/modules/AC/AC1/L07.html:412-413, :416",
     "status": "PASS",
     "evidence": "The question asks which statement is a model assumption and not a finding about firms. The key 'no award is forfeited' is Definition 1.2 (ii) (L07.html:73). The distractor 'some awards are forfeited before they vest' is a claim about behaviour that the model does not assume, and the explain line at :416 says 'The other two are claims about behaviour, which this lesson does not make'. The distractor is not a model assumption, so the item has one key."},
    {"id": "AC1-c-r18-L08-why-it-matters", "check": "2.4-math and 2.2 basis: L08 exactness claim at why-it-matters (changed)",
     "location": "course/modules/AC/AC1/L08.html:51; :82-88 (Section 2 exactness sentences)",
     "status": "FAIL",
     "evidence": "L08.html:51 says the tax expense, the current tax and the deferred balance are exact in integer cents when P_t is a multiple of 100 cents. Only the current tax and the tax expense depend on P_t (CT_t = r(P_t - d_t)/100 and TE_t = rP_t/100). The deferred expense DE_t = r d_t/100 and the balance DTL_t = r K_t/100 are exact for every P_t, because Definition 1.1 makes C a multiple of 10,000 cents and C/L a multiple of 100 cents, so tau_t, b_t and K_t are multiples of 100. Computed: for the run's asset (cost 46,700.00, K = 9,340/14,010/14,010/9,340/0) the balances at 21% are integral for any pretax income. The sentence attributes the balance's exactness to a condition that is not its basis. Section 2 (:88) repeats the same over-broad 'requires'. Line 51 is changed in this round and is a FAIL.",
     "fix": "Rewrite L08.html:51 so the P_t condition applies only to the current tax and the total tax expense, and state that the deferred expense and balance are exact for every P_t by Definition 1.1; make the same split in L08.html:88.",
     },
    {"id": "AC1-c-r18-L08-interp-209", "check": "2.5-labs interpretation L08 (changed)",
     "location": "course/modules/AC/AC1/L08.html:209",
     "status": "PASS",
     "evidence": "Checked against the run output (scratch run-L08.txt): years 1-2 current tax below total tax expense by the deferred expense (1,961.40 and 980.70), the deferred expense positive because the balance rises (0 -> 1,961.40 -> 2,942.10); years 4-5 deferred expense -980.70 and -1,961.40, with current tax above the total expense (10,711.89 > 9,731.19; 14,356.65 > 12,395.25) because the balance unwinds (2,942.10 -> 1,961.40 -> 0). Causal direction matches DE_t = DTL_t - DTL_{t-1}."},
    {"id": "AC1-c-r18-m18a-survivor-check", "check": "2.5-labs student-error mutant m18a (schedule check skips year 6)",
     "location": "tests/labs/AC1/lab-AC1-L07-1.py:86 (schedule loop); course/modules/AC/AC1/L07.html:126, :325-327 (E2)",
     "status": "PASS",
     "evidence": "mutants_r18.py entry m18a: exit 0 with the shipped seed 20260701 (output identical, no printed row changes). seed_sweep_r18.py: m18a exits 1 (killed) for seeds 2, 3, 42, 999 and 123456789. The shipped run passes because no grant vests in year 6 for that seed. E2 asks the student to change the seed, and the page's 'pass for any seed' claim is about the correct lab, which passes all ten seeds. The mutant is detected under E2's own procedure, so it is not a survivor."},
    {"id": "AC1-c-r18-m18c-sbc-omits-last-grant", "check": "2.5-labs new student-error mutant m18c (SBC row omits the last grant)",
     "location": "tests/labs/AC1/lab-AC1-L07-1.py:89; course/modules/AC/AC1/L07.html:358, :359, :268, :331, E1 (:323)",
     "status": "FAIL",
     "evidence": "mutants_r18.py entry m18c: exit 0 (survives every assertion). Printed SBC row becomes 29,769.58, 36,889.58, 36,889.59, 26,961.25, 0.00 for years 1-5, so the year-3 figure is 36,889.59, not 57,822.92. The page states the year-3 peak of 57,822.92 at L07.html:358 (key result), :323 (E1 solution) and :268 ('falls to zero in year 6'; here zero from year 5). The mutant falsifies these, and no assertion catches it. It is a student-error mutant (dropping a grant from the statement sum), so FAIL under the new-survivor rule.",
     "fix": "Pin the printed SBC row: assert the per-year sum of all grants equals an independently computed schedule (or assert the peak 57,822.92 for seed 20260701), so that dropping a grant changes an assertion.",
     },
    {"id": "AC1-c-r18-m18d-tax-depreciation-shifted", "check": "2.5-labs new student-error mutant m18d (tax depreciation one year late)",
     "location": "tests/labs/AC1/lab-AC1-L08-1.py:54 (tax_dep); course/modules/AC/AC1/L08.html:209, :262-265 (E1), :300 (key result)",
     "status": "FAIL",
     "evidence": "mutants_r18.py entry m18d: exit 0. The printed table becomes tax_dep 0.00, 18,680.00, 14,010.00, 9,340.00, 4,670.00 and DTL -1,961.40, 0.00, 980.70, 980.70, 0.00 for years 1-5. The totals still equal the cost and the three identity checks still pass, so no assertion sees it. The page states the peak balance 2,942.10 in years 2 and 3 (E1 at :262-265, key result :300), the year-1 interpretation at :209 ('current tax is below ... because the printed balance rises') and the 'balance rises' mechanism; under m18d the balance is negative (-1,961.40) in year 1 and its largest value is 980.70 in years 3 and 4, not 2,942.10 in years 2 and 3. FAIL under the new-survivor rule.",
     "fix": "Pin the printed DTL and tax_dep columns: assert the year-1 tax depreciation equals cost * TAX_PERCENT[0] // 100 and the balance series equals the Example 1.4 values for the shipped asset, or drop the table-shape claims at :209, :262-265 and :300.",
     },
    {"id": "AC1-c-r18-m18g-base-from-share-count", "check": "2.5-labs new student-error mutant m18g (base amount floors the share count, not the cost)",
     "location": "tests/labs/AC1/lab-AC1-L07-1.py:45 (base); course/modules/AC/AC1/L07.html:63 (Def 1.1 base), :358, :268",
     "status": "FAIL",
     "evidence": "mutants_r18.py entry m18g: exit 0. The base becomes shares // v * fair value, which differs from floor(C_g / v) (Definition 1.1, L07.html:63) and changes the printed SBC row to 29,766.90, 36,885.12, 57,813.42, 47,885.06, 20,959.50. The printed year-3 peak becomes 57,813.42, so the statement 57,822.92 at L07.html:358 and :323 is falsified, and no assertion checks the base against Definition 1.1. FAIL under the new-survivor rule.",
     "fix": "Assert the base amount against floor(C_g / v_g) for each grant (the Definition 1.1 formula), and pin the peak value 57,822.92 for seed 20260701.",
     },
    {"id": "AC1-c-r18-alt-implementations", "check": "2.5-labs over-constraint: correct alternative implementations",
     "location": "tests/labs/AC1/lab-AC1-L07-1.py:45-48; tests/labs/AC1/lab-AC1-L08-1.py:53-62",
     "status": "PASS",
     "evidence": "mutants_r18.py alternatives all exit 0: alt18a (cumulative rounding schedule, a different algorithm: cost*(k)//v minus cost*(k-1)//v), alt18b (DTL by accumulated rate steps), alt18c (tax expense from rate times pretax), alt9a (half-up base), alt9b (remainder in first year), alt9c (deferred from difference), alt10a (ceiling base), alt10b, alt17a (current tax from pretax minus difference). The lab accepts these different correct algorithms. Note: alt9a, alt10a, alt18a change the printed table values, which no assertion pins (the class of AC1-c-r17-m17a-survivor); they are alternatives, not student errors."},
    {"id": "AC1-c-r18-seed-sweep", "check": "2.5-labs seed sweep for the pages' 'pass for any seed' claims (E2, E3)",
     "location": "tests/labs/AC1/lab-AC1-L07-1.py:15; tests/labs/AC1/lab-AC1-L08-1.py:122 (seed); course/modules/AC/AC1/L07.html:327; L08.html:273",
     "status": "PASS",
     "evidence": "ledgers/AC1/scripts/AC1-c-r18/seed_sweep_r18.py: both twins exit 0 for seeds 0, 1, 2, 3, 7, 42, 999, 123456789, 20260701 and 20260702. Structural argument checked: grant years 1-3 and 3 or 4 vesting years give last vesting year at most 6 (the horizon); L08 draws multiples of 10,000 cents and 100-cent pretax income."},
    {"id": "AC1-c-r18-twins-unchanged", "check": "2.5-labs lab twins byte-identical since the previous pin",
     "location": "tests/labs/AC1/lab-AC1-L07-1.py; tests/labs/AC1/lab-AC1-L08-1.py",
     "status": "PASS",
     "evidence": "git diff --quiet fefbf8b 7143726 -- tests/labs/AC1/lab-AC1-L07-1.py tests/labs/AC1/lab-AC1-L08-1.py: exit 0 (identical). The only tests/labs/AC1 change in the range is lab-AC1-L04-1.py, outside this slice."},
]
rows_out.extend(new_rows)

# carried-survivor notes and the mutant list
mutants = [{"id": mid, "description": desc, "killed_by": kb} for mid, desc, kb in mutants_killed]
out = {
    "unit": "AC1",
    "slice": "AC1-c",
    "round": 18,
    "round_note": "round 18 (independent re-verification of AC1-c after pin 7143726). Delta since fefbf8b: L07.html:51 and :412, L08.html:51 and :209 changed; lab twins and cards of this slice byte-identical. Round-17 FAIL m17a re-verified and still open.",
    "verifier": "independent verifier (Haiku 5.5), slice AC1-c round 18; did not build AC1 and shares no context with its builders or earlier verifiers",
    "pin": "7143726",
    "base": "fefbf8b (previous pin, for the delta)",
    "checkout": "/tmp/verify18-AC1-c",
    "scratch": "/tmp/AC1-v/AC1-c-r18",
    "verified_at": "2026-10-28T12:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows_out,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "scripts": [
        "ledgers/AC1/scripts/AC1-c-r18/mutants_r18.py",
        "ledgers/AC1/scripts/AC1-c-r18/seed_sweep_r18.py",
        "ledgers/AC1/scripts/AC1-c-r18/embed_and_run_check_r18.py",
        "ledgers/AC1/scripts/AC1-c-r18/build_fragment_r18.py",
        "ledgers/AC1/scripts/AC1-c-r17/mutants_r17.py",
        "ledgers/AC1/scripts/AC1-c-r10/mutants_r10.py",
        "ledgers/AC1/scripts/AC1-c-r9/mutants_r9.py",
    ],
    "notes": (
        "Verdict FAIL. FAIL rows: (1) AC1-c-r17-m17a-survivor (still open; the page's table statements at L07.html:268, :331 and :358 are falsified by the survivor); "
        "(2) AC1-c-r18-L08-why-it-matters (new in this round: L08.html:51 attributes the deferred balance's exactness to the P_t condition; the balance is exact for every P_t, the same over-broad 'requires' at :88); "
        "(3) AC1-c-r18-m18c-sbc-omits-last-grant, AC1-c-r18-m18d-tax-depreciation-shifted, AC1-c-r18-m18g-base-from-share-count (new survivors that falsify stated numbers); "
        "(4) AC1-c-r5-L08-line51-signed and AC1-c-r9-delta-read (cite the changed L08.html:51). "
        "Class note for the architect: carried PASS survivors AC1-c-r10-m10a-survivor and AC1-c-r10-m10c-survivor, and the non-ledgered survivors n1ceil (r8-n1ceil) and n1b (r8-n1b), produce the same falsification of the printed table or of 57,822.92 as m17a (m10a output is identical to m17a). They are carried PASS under the carry rule because their lab subject is byte-identical; the architect should rule on the class. "
        "m18a is killed by seeds 2, 3, 42, 999, 123456789 and is PASS. The verifier mutant files are not written under ledgers/AC1/mutants/ because tools/mutate_graders.py reads that directory as grader mutants; the lab mutants are generated by ledgers/AC1/scripts/AC1-c-r18/mutants_r18.py. "
        "Not checked: the project and grader files (other slices), the L03/L04 changes in the same range, any live web or registry source beyond verify_refs, the hours design targets (architect ruling: arithmetic only)."
    ),
    "summary": "",
}
counts = {"PASS": 0, "FAIL": 0}
for r in rows_out:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
out["summary"] = (
    f"FAIL: {counts['PASS']} PASS, {counts['FAIL']} FAIL, 0 UNVERIFIABLE rows of {len(rows_out)}. "
    f"Mutants killed: {len(mutants)} listed; survivors m17a, m18c, m18d, m18g are FAIL rows; m10a, m10c, n1ceil, n1b are carried PASS survivors (class note)."
)
Path(sys.argv[3]).write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(counts, len(rows_out))
