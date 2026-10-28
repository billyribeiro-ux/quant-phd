"""Round 17 (AC1-c): build ledgers/AC1/AC1-c.json from the previous fragment and this round's re-runs.

Usage: python -I build_fragment_r17.py <checkout> <previous fragment>
Rows re-run in round 17 take the new evidence below. Every other previous row is carried: its status stays
PASS and its evidence gets the carry prefix, because the subject it cites is byte-identical since af08ad1.
"""

import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

root = Path(sys.argv[1])
prev = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
CARRY = (
    "Carried from round 16 (course/modules/AC/AC1/L07.html, course/modules/AC/AC1/L08.html, "
    "tests/labs/AC1/lab-AC1-L07-1.py and tests/labs/AC1/lab-AC1-L08-1.py byte-identical since the previous pin af08ad1;"
    " card objects cited are unchanged per ledgers/AC1/scripts/AC1-c-r17/card_delta_r17.py):"
)
RERUN = {
    "AC1-c-cmd-run_labs": "tools/run_labs.py --unit AC1 (round 17): PASS (11/11).",
    "AC1-c-lab-twin-run": "python -I -W error tests/labs/AC1/lab-AC1-L07-1.py rc=0 (output: SIMULATED grants, 4/4 schedules, 6/6 for each of 4 identities); lab-AC1-L08-1.py rc=0 (5/5 for three identities; deferred balance at end of year 5 0.00 SCU). Outputs saved in /tmp/AC1-v/AC1-c-r17/L07.out and L08.out.",
    "AC1-c-lab-embed-equals-twin": "ledgers/AC1/scripts/AC1-c-r9/embed_and_expected_check.py <checkout> re-run: L07 embedded code == twin True; L08 embedded code == twin True.",
    "AC1-c-lab-expected-output": "embed_and_expected_check.py re-run: L07 expected == run output True (18 lines); L08 True (13 lines).",
    "AC1-c-lab-seed-sweep": "ledgers/AC1/scripts/AC1-c-r9/seed_sweep_r9.py re-run: lab-AC1-L07-1 seeds 0-199 passing 200, failing none; lab-AC1-L08-1 seeds 0-199 passing 200, failing none.",
    "AC1-c-cmd-page_smoke": "tools/page_smoke.py --unit AC1 --pages L07 L08 (round 17): PASS for modules/AC/AC1/L07.html and L08.html (PASS for AC1).",
    "AC1-c-cmd-check_pages_dag": "tools/check_pages.py --unit AC1: PASS; tools/check_dag.py --unit AC1: PASS (round 17).",
    "AC1-c-dag-concepts": "tools/check_dag.py --unit AC1: PASS (round 17); L07.html:59 defines def-stock-based-compensation (one dfn); The concept-level reading (definitions and first uses) is carried from the previous fragment; its lesson text is byte-identical.",
    "AC1-c-lesson-structure": "tools/check_pages.py --unit AC1: PASS (round 17); section order and lab blocks of L07.html and L08.html unchanged (files byte-identical since af08ad1).",
    "AC1-c-cmd-pytest_ruff_mypy": "tests/test_labs.py and tests/test_page_checks.py: rc=0 (24 dots, all passed); pytest -k 'notation or macro or banned': rc=0; ruff check . 'All checks passed!'; ruff format --check . '212 files already formatted'; mypy --no-incremental 'Success: no issues found in 153 source files'.",
    "AC1-c-notation": "pytest -k 'notation or macro or banned' rc=0 (round 17). The L08.html:216 sentence uses \\(L\\), which notation/notation.json lists only as a letter defined locally in each lesson, as before.",
    "AC1-c-banned-phrases": "grep -n -i -E 'roughly|about [0-9]|historically|typically|most firms|half of|\\.\\.\\.|…|usually|generally' L07.html L08.html: one hit, L07.html:412, 'awards are typically forfeited at a stated rate', a distractor option in quiz L07q8 that the explanation at L07.html:416 rejects; no learner claim uses a banned phrase.",
    "AC1-c-figures-none": "grep -c '<img|<svg|<canvas|data-figure' over L07.html and L08.html = 0 each (round 17).",
    "AC1-c-cit-verify_refs": "tools/verify_refs.py --unit AC1 (live): 2 of 560 entries, 0 problems, rc=0; tools/verify_refs.py --offline: 560 entries, 0 problems (round 17). Slice cites no registry key (AC1-c-registry-absence).",
    "AC1-c-cards-dup-scan": "ledgers/AC1/scripts/AC1-c-r17/cards_lh_r17.py: 139 cards in cards.json, no duplicate ids, no duplicate fronts; L07 18 cards (c091-c104, c135-c138), L08 22 cards (c105-c121, c125, c129-c131, c139).",
    "AC1-c-r7-lab-student-mutants": "ledgers/AC1/scripts/AC1-c-r7/seed_sweep_and_mutants.sh re-run via path-substituted copy ledgers/AC1/scripts/AC1-c-r17/run_r7.sh: m8a, m7a, m7b each rc=1 (AssertionError) as expected; seed sweep 20 runs.",
    "AC1-c-r8-lab-student-mutants": "ledgers/AC1/scripts/AC1-c-r8/new_mutants.sh and mutants_and_sweep.sh re-run via ledgers/AC1/scripts/AC1-c-r17/run_r8b.sh and run_r8a.sh: n2life, n3sign, n4te rc=1 (killed); n1ceil and n1b rc=0 (survivors, same class as AC1-c-r10-m10c-survivor); 20 sweep runs rc=0.",
    "AC1-c-r9-new-mutants": "ledgers/AC1/scripts/AC1-c-r9/mutants_r9.py re-run: m9a-m9g each exit=1 (AssertionError), as expected.",
    "AC1-c-r9-alt-implementations-seeds": "mutants_r9.py alt9a, alt9b, alt9c exit=0; seed_sweep_r9.py 200/200 for both twins (round 17).",
    "AC1-c-r7-alt-implementations": "tests/labs/AC1/lab-AC1-L07-1.py and lab-AC1-L08-1.py re-run with alt9a, alt9b, alt9c, alt10a, alt10b (mutants_r9.py, mutants_r10.py): all rc=0.",
    "AC1-c-r10-alt-correct-implementations": "mutants_r9.py alt9a-c and mutants_r10.py alt10a, alt10b re-run: all exit=0. Round 17 adds alt17a (L08 current tax as (r*P - r*difference)//100): exit=0.",
    "AC1-c-r10-mutants-killed": "mutants_r10.py re-run: m10b, m10d, m10e exit=1 (AssertionError); m10a and m10c exit=0 (survivors, see their rows). Round 17 mutants m17b-m17e killed: see AC1-c-r17-mutants-killed.",
    "AC1-c-r10-m10a-survivor": "mutants_r10.py re-run: m10a exit=0 observed=PASS (survives). Expense starts one year late; every shifted schedule still sums to the total inside the six-year horizon, and every identity still holds (the lab checks identities, see L07.html:126 and :327). Classified as out of the lab's stated checks, the same class as AC1-c-r17-m17a-survivor, which is a FAIL under the rule applied there; see the notes.",
    "AC1-c-r10-m10c-survivor": "mutants_r10.py re-run: m10c exit=0 (survives): the base uses vest_years+1; the last year takes the remainder, so the sums stay exact and the identities hold. Same class as n1ceil and n1b (exit 0); see the notes on the class.",
    "AC1-c-r10-hours-sum": "course/modules/AC/AC1/index.html card-kicker hours: L01 11, L02 12, L03 11, L04 11, L05 12, L06 12, L07 11, L08 10; sum 90 equals data-hours-lessons=\"90\" (index.html:29) and plans/AC1-build-plan.md:124 split (L07 11, L08 10 match L07.html:2 and L08.html:2). Hours are not failed on a pace estimate (architect ruling).",
    "AC1-c-r9-embed-expected": "embed_and_expected_check.py re-run (round 17): L07 embedded == twin and expected == run output True; L08 True and True.",
    "AC1-c-r9-prose-recompute": "ledgers/AC1/scripts/AC1-c-r9/recompute_prose_r9.py re-run (round 17): all worked figures reproduced; L08 DTL 21% of 14010 = 2942.1 (K/cost = 0.3); L08 E2 yr1 10131.24 = 0.21 x 48244; L07 lab table figures unchanged since the lab is byte-identical.",
    "AC1-c-r5-delta-scope": "git diff --stat d57df1e de53f7e -- course/modules/AC/AC1/L07.html L08.html cards.json tests/labs/AC1 (round 17): 4 files changed, 21 insertions(+), 21 deletions(-); historic delta, no change to the current slice.",
    "AC1-c-r7-delta-scope": "same command, pins d57df1e..de53f7e (round 17): 4 files changed, 21 insertions(+), 21 deletions(-); historic.",
    "AC1-c-r8-delta-scope": "git diff --stat de53f7e 2c8162b -- course/modules/AC/AC1/L07.html L08.html cards.json tests/labs/AC1 (round 17): 3 files changed, 28 insertions(+), 20 deletions(-); historic.",
    "AC1-c-r9-delta-read": "git diff --stat 2c8162b 96dd532 (round 17): 3 files changed, 9 insertions(+), 9 deletions(-); historic. Labs and twins unchanged since 2c8162b.",
    "AC1-c-r10-delta-read": "git diff --stat 96dd532 af08ad1 -- course/modules/AC/AC1 tests/labs/AC1 (round 17): 7 files changed, 13 insertions(+), 13 deletions(-); historic; the slice hunks listed in the previous fragment are the ones at L07.html:140, :452 and L08.html:216, :394.",
    "AC1-c-cards-L07-L08": "cards.json: card objects changed since af08ad1 are c095, c108, c111 (L07/L08); added L07/L08 cards are c129, c130, c131, c135-c139. Each is re-verified in its own AC1-c-r17 row. The other L07/L08 cards (c091-c094, c096-c107, c109, c110, c112-c121, c125) are unchanged (card_delta_r17.py).",
}
CARRY_ONLY = {"AC1-c-cards-L07-L08"}  # re-verified above, not carried
NEW = [
    {"id": "AC1-c-r17-delta-read", "check": "delta since af08ad1: slice files byte-identical; changed slice cards read",
     "location": "git diff --stat af08ad1 fefbf8b -- course/modules/AC/AC1/L07.html L08.html tests/labs/AC1/lab-AC1-L07-1.py lab-AC1-L08-1.py (empty); card_delta_r17.py",
     "status": "PASS",
     "evidence": "The four slice files are byte-identical (empty stat). In cards.json the slice objects that changed are c095, c108, c111 and the added ones are c129-c131 and c135-c139; each is read in its own row. Outside the slice, and not verified here: cards c007, c015, c027, c033, c039, c042, c050, c051, c059 (L01-L04), c127-c128 (L03), c132-c134 (L04), tests/labs/AC1/lab-AC1-L03-1.py, tests/labs/CF1/lab-CF1-L05-1.py and index.html:141 (L01 skill check)."},
    {"id": "AC1-c-r17-card-c095", "check": "card c095 answer matches L07 Definition 1.2 (i)", "location": "course/modules/AC/AC1/cards.json:662-664; course/modules/AC/AC1/L07.html:73",
     "status": "PASS", "evidence": "Answer 'Yes. The total cost is fixed on the grant date (Definition 1.2 (i))' matches L07.html:73 '(i) The total cost C_g is fixed on the grant date.' Grade C with basis 'Model choices (Definition 1.2)' matches a model convention."},
    {"id": "AC1-c-r17-card-c108", "check": "card c108 answer matches L08 Definition 1.1 (asset constraints)", "location": "course/modules/AC/AC1/cards.json:752-756; course/modules/AC/AC1/L08.html:59",
     "status": "PASS", "evidence": "L08.html:59: 'cost C, a multiple of 10,000 cents, and a book life of L years, where C / L is a multiple of 100 cents'. The card states exactly these three constraints. Tax percentages and the flat rate are constraints on the tax schedule, not on the asset, and are stated by c130 and c131. Not an error."},
    {"id": "AC1-c-r17-card-c111", "check": "card c111 deferred tax expense definition", "location": "course/modules/AC/AC1/cards.json:770-773; course/modules/AC/AC1/L08.html:88",
     "status": "PASS", "evidence": "L08.html:86-88 defines DE_t = DTL_t - DTL_(t-1) and DTL_0 = 0. The card matches."},
    {"id": "AC1-c-r17-card-c129", "check": "card c129 book depreciation", "location": "course/modules/AC/AC1/cards.json:900-903; course/modules/AC/AC1/L08.html:59",
     "status": "PASS", "evidence": "L08.html:59 'Book depreciation is straight-line, b = C / L in each year t = 1, ..., L'. The card matches (the ellipsis is the lesson's own mathematical range notation, not a learner-text omission)."},
    {"id": "AC1-c-r17-card-c130", "check": "card c130 tax depreciation", "location": "course/modules/AC/AC1/cards.json:906-909; course/modules/AC/AC1/L08.html:59",
     "status": "PASS", "evidence": "L08.html:59 'Tax depreciation in year t is tau_t = C p_t / 100, where the integers p_1, ..., p_L are the tax percentages and sum to 100'. The card matches."},
    {"id": "AC1-c-r17-card-c131", "check": "card c131 flat rate in every year", "location": "course/modules/AC/AC1/cards.json:912-915; course/modules/AC/AC1/L08.html:59",
     "status": "PASS", "evidence": "L08.html:59 'The model's flat tax rate is a whole number of percent, r, the same in every year'. The card matches."},
    {"id": "AC1-c-r17-card-c135", "check": "card c135 no forfeiture", "location": "course/modules/AC/AC1/cards.json:942-946; course/modules/AC/AC1/L07.html:73",
     "status": "PASS", "evidence": "L07.html:73 '(ii) No award is forfeited, that is, lost by the employee before it vests.' The card says 'No. No award is forfeited (Definition 1.2 (ii))'. Matches; grade C basis is a model choice."},
    {"id": "AC1-c-r17-card-c136", "check": "card c136 no performance or market conditions", "location": "course/modules/AC/AC1/cards.json:950-954; course/modules/AC/AC1/L07.html:73",
     "status": "PASS", "evidence": "L07.html:73 '(iii) Vesting has no performance or market conditions, meaning no vesting test tied to a company target or to a share price.' The card repeats that gloss verbatim."},
    {"id": "AC1-c-r17-card-c137", "check": "card c137 no income tax on grants", "location": "course/modules/AC/AC1/cards.json:958-962; course/modules/AC/AC1/L07.html:73",
     "status": "PASS", "evidence": "L07.html:73 '(iv) Income tax is ignored in this lesson; L08 models tax on depreciation differences, not on these grants.' The card matches."},
    {"id": "AC1-c-r17-card-c138", "check": "card c138 no dilution count", "location": "course/modules/AC/AC1/cards.json:966-970; course/modules/AC/AC1/L07.html:73, :274",
     "status": "PASS", "evidence": "L07.html:73 '(v) Shares issued at vesting are not counted, so the model says nothing about dilution'; L07.html:274 repeats it. The card matches."},
    {"id": "AC1-c-r17-card-c139", "check": "card c139 total tax expense definition", "location": "course/modules/AC/AC1/cards.json:974-977; course/modules/AC/AC1/L08.html:88",
     "status": "PASS", "evidence": "L08.html:88 defines TE_t = CT_t + DE_t and says CT_t is the current tax and DE_t the deferred tax expense. The card says TE_t = CT_t + DE_t, the sum of the current tax and the deferred tax expense. Matches."},
    {"id": "AC1-c-r17-mutants-killed", "check": "round-17 student-error mutants m17b-m17e are killed; alternative alt17a passes",
     "location": "ledgers/AC1/scripts/AC1-c-r17/mutants_r17.py; tests/labs/AC1/lab-AC1-L07-1.py; tests/labs/AC1/lab-AC1-L08-1.py",
     "status": "PASS", "evidence": "mutants_r17.py re-run: m17b (vesting window one year long) exit=1; m17c (last year takes the base) exit=1; m17d (tax depreciation uses the first percent every year) exit=1; m17e (cumulative difference not accumulated) exit=1; all AssertionError. alt17a (current tax from pretax minus difference) exit=0."},
    {"id": "AC1-c-r17-m17a-survivor", "check": "student-error mutant m17a (SBC row labelled one year early) must be caught",
     "location": "ledgers/AC1/scripts/AC1-c-r17/mutants_r17.py (m17a); tests/labs/AC1/lab-AC1-L07-1.py:43 (sbc row); course/modules/AC/AC1/L07.html:268, :331",
     "status": "FAIL",
     "evidence": "m17a builds the printed sbc list over range(0, HORIZON), so the row labelled year 6 shows 20,933.34 (the year-5 expense) instead of 0.00. Exit 0: all four assertions pass (schedule sums 4/4, identities 6/6). The page states the table's shape: L07.html:268 'The expense in the table rises, peaks in year 3, and falls to zero in year 6', and L07.html:331 'In year 6 the expense is 0.00 SCU'. The mutant falsifies both, and nothing in the lab checks the SBC row against the year labels.",
     "fix": "Make the lab check the printed SBC row against the year labels: for example compare the row with an expected per-year vector for the seed, or assert that the year-6 value is 0 and that the year-3 value is the largest. Then re-run mutants_r17.py; m17a must exit non-zero. Do not change the page wording until the check exists."},
]
rows = []
seen = set()
for row in prev["rows"]:
    rid = row["id"]
    seen.add(rid)
    if rid in RERUN:
        new = dict(row)
        new["evidence"] = RERUN[rid]
        if rid == "AC1-c-cards-L07-L08":
            new["evidence"] += " Re-verified as rows AC1-c-r17-card-c095 ... c139."
        rows.append(new)
        continue
    original = row["evidence"]
    m = re.match(r"^Carried from round \d+ \(.*?\): ", original)
    body = original[m.end():] if m else original
    new = dict(row)
    new["status"] = "PASS"
    new["evidence"] = CARRY + " " + body
    rows.append(new)
rows.extend(NEW)
missing = sorted(set(RERUN) - seen)
assert not missing, missing
mutants = []
for mid, desc, killer in [
    ("r9-m9a", "L07 last vesting year takes the base, dropping the remainder", "AssertionError in lab-AC1-L07-1 (r9)"),
    ("r9-m9b", "L07 vesting window off by one (index > vest_years)", "AssertionError in lab-AC1-L07-1 (r9)"),
    ("r9-m9c", "L07 APIC change sign reversed", "AssertionError in lab-AC1-L07-1 (r9)"),
    ("r9-m9d", "L07 cash-flow statement without the SBC add-back", "AssertionError in lab-AC1-L07-1 (r9)"),
    ("r9-m9e", "L08 current tax ignores the temporary difference", "AssertionError in lab-AC1-L08-1 (r9)"),
    ("r9-m9f", "L08 deferred tax balance sign flipped", "AssertionError in lab-AC1-L08-1 (r9)"),
    ("r9-m9g", "L08 deferred tax balance without the tax rate", "AssertionError in lab-AC1-L08-1 (r9)"),
    ("r7-m8a", "L08 deferred expense from taxable income, not the balance change", "AssertionError in lab-AC1-L08-1 (r17 re-run)"),
    ("r7-m7a", "L07 last-year branch disabled", "AssertionError in lab-AC1-L07-1 (r17 re-run)"),
    ("r7-m7b", "L07 base amount plus one cent", "AssertionError in lab-AC1-L07-1 (r17 re-run)"),
    ("r8-n2life", "L08 book depreciation over LIFE minus one", "AssertionError in lab-AC1-L08-1 (r17 re-run)"),
    ("r8-n3sign", "L08 deferred expense sign reversed", "AssertionError in lab-AC1-L08-1 (r17 re-run)"),
    ("r8-n4te", "L08 total tax expense omits the deferred part", "AssertionError in lab-AC1-L08-1 (r17 re-run)"),
    ("r10-m10b", "L07 APIC change one cent short of the SBC expense", "AssertionError in lab-AC1-L07-1 (r10, re-run r17)"),
    ("r10-m10d", "L08 deferred expense equals the balance, not its change", "AssertionError in lab-AC1-L08-1 (r10, re-run r17)"),
    ("r10-m10e", "L08 current tax computed on pretax plus the difference", "AssertionError in lab-AC1-L08-1 (r10, re-run r17)"),
    ("r17-m17b", "L07 vesting window one year long (index > vest_years)", "AssertionError in lab-AC1-L07-1 (r17)"),
    ("r17-m17c", "L07 last vesting year takes the base", "AssertionError in lab-AC1-L07-1 (r17)"),
    ("r17-m17d", "L08 tax depreciation uses the first percent every year", "AssertionError in lab-AC1-L08-1 (r17)"),
    ("r17-m17e", "L08 cumulative temporary difference not accumulated", "AssertionError in lab-AC1-L08-1 (r17)"),
]:
    mutants.append({"id": mid, "description": desc, "killed_by": killer})
fragment = {
    "unit": "AC1",
    "slice": "AC1-c",
    "round": 17,
    "round_note": "round 17 (independent re-verification of AC1-c after the pin af08ad1, to fefbf8b). Delta: cards c095, c108, c111 changed; cards c129-c131 and c135-c139 added (L07/L08). Slice pages and lab twins byte-identical since af08ad1. The previous fragment (AC1-c.round16.json) is labelled round 10 internally with pin af08ad1; it is treated as the previous round.",
    "verifier": "independent verifier (Haiku 5.5), slice AC1-c round 17; did not build AC1 and shares no context with its builders or earlier verifiers",
    "pin": "fefbf8b",
    "base": "af08ad1 (previous pin, for the delta)",
    "checkout": "/tmp/verify17-AC1-c",
    "scratch": "/tmp/AC1-v/AC1-c-r17",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "scripts": [
        "ledgers/AC1/scripts/AC1-c-r17/mutants_r17.py",
        "ledgers/AC1/scripts/AC1-c-r17/cards_lh_r17.py",
        "ledgers/AC1/scripts/AC1-c-r17/card_delta_r17.py",
        "ledgers/AC1/scripts/AC1-c-r17/build_fragment_r17.py",
        "ledgers/AC1/scripts/AC1-c-r17/run_r7.sh",
        "ledgers/AC1/scripts/AC1-c-r17/run_r8a.sh",
        "ledgers/AC1/scripts/AC1-c-r17/run_r8b.sh",
        "ledgers/AC1/scripts/AC1-c-r9/mutants_r9.py",
        "ledgers/AC1/scripts/AC1-c-r9/seed_sweep_r9.py",
        "ledgers/AC1/scripts/AC1-c-r9/embed_and_expected_check.py",
        "ledgers/AC1/scripts/AC1-c-r9/recompute_prose_r9.py",
        "ledgers/AC1/scripts/AC1-c-r10/mutants_r10.py",
    ],
    "notes": (
        "Verdict FAIL: one row, AC1-c-r17-m17a-survivor. Notes: (1) m17a survives because the lab's assertions test identities only (L07.html:126, :327); "
        "the page's own table statements (:268, :331) are falsified by it, so it is recorded FAIL under the new-survivor rule. "
        "(2) The same class (the printed row is not pinned by any assertion) gives the carried PASS survivors m10a, m10c, n1ceil and n1b. "
        "Those are kept PASS because their subjects are byte-identical and the carry rule applies, but the architect should rule on the class: "
        "by the rule applied to m17a, they fail as well. (3) Card c108 names the asset constraints only; the tax-schedule constraints are on c130 and c131. "
        "(4) Not checked here: the L03/L04 cards and twins changed in the same range, belonging to other slices; the project and grader files; "
        "any live Crossref or web source (the slice cites no registry key, so verify_refs live reports 2 of 560 entries, outside this slice)."
    ),
    "summary": "",
}
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
fragment["summary"] = (
    f"FAIL: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE rows of "
    f"{len(rows)}. The slice's delta is the changed cards c095, c108, c111 and added cards c129-c131, c135-c139, "
    "all verified; the lab and page checks re-ran PASS. One FAIL: m17a survives and the page's year-by-year statements "
    "(L07.html:268, :331) are falsified. Mutants: 20 killed, 2 carried survivors (m10a, m10c) and 2 (n1ceil, n1b) out of this list."
)
out = root / "ledgers/AC1/AC1-c.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), counts)
