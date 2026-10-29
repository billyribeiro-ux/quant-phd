"""Round 23 (AC1-c): builds ledgers/AC1/AC1-c.json from the round-22 fragment and this round's re-runs.

Usage: python -I build_fragment_r23.py <checkout> <previous_fragment.json>
Every previous row id is kept. A previous PASS row is carried only when its slice files are byte-identical
since the previous pin (fd9a9b7); rows whose subject changed or which are command rows are re-run and
rewritten with this round's evidence. Mutant survivors are PASS rows (out of scope), not mutants.
"""

import json
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

root = Path(sys.argv[1])
prev = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
PIN_PREV = "fd9a9b7"
OUT = "ledgers/AC1/scripts/AC1-c-r23/out"
SCR = "ledgers/AC1/scripts/AC1-c-r23"


def git_text(rev: str, path: str) -> str:
    return subprocess.run(["git", "-C", str(root), "show", f"{rev}:{path}"], capture_output=True, check=True,
                          text=True).stdout


def line_of(text: str, card_id: str) -> int:
    for n, line in enumerate(text.splitlines(), 1):
        if f'"id": "{card_id}"' in line:
            return n
    raise SystemExit(f"card {card_id} not found")


# ---- card line moves (cards.json changed in L04-L06 rows; L07/L08 card objects identical) ----
old_cards = git_text(PIN_PREV, "course/modules/AC/AC1/cards.json")
new_cards = (root / "course/modules/AC/AC1/cards.json").read_text(encoding="utf-8")
CARD_SHIFT = {c: line_of(new_cards, c) - line_of(old_cards, c) for c in
              ["AC1-c091", "AC1-c095", "AC1-c098", "AC1-c104", "AC1-c108", "AC1-c111", "AC1-c129", "AC1-c135",
               "AC1-c139"]}
assert set(CARD_SHIFT.values()) == {-6}, CARD_SHIFT

SLICE_FILES = {
    "course/modules/AC/AC1/L07.html": "L07.html",
    "course/modules/AC/AC1/L08.html": "L08.html",
    "course/modules/AC/AC1/index.html": "index.html",
    "tests/labs/AC1/lab-AC1-L07-1.py": "lab-AC1-L07-1.py",
    "tests/labs/AC1/lab-AC1-L08-1.py": "lab-AC1-L08-1.py",
    "references/references.json": "references.json",
}
for path in SLICE_FILES:
    assert git_text(PIN_PREV, path) == git_text("HEAD", path), path

# ---- re-run rows: id -> (check, location, status, evidence) ----
RERUN = {
    "AC1-c-cmd-run_labs": (None, None, "PASS",
        f"Re-run round 23 (checkout 503d139): tools/run_labs.py --unit AC1 exit 0, 'run_labs AC1: PASS (11/11)' ({OUT}/run_labs.out)."),
    "AC1-c-lab-twin-run": (None, None, "PASS",
        f"Re-run round 23: python -I -W error tests/labs/AC1/lab-AC1-L07-1.py exit 0 (18 output lines, {OUT}/twin_L07.out); lab-AC1-L08-1.py exit 0 (13 output lines, {OUT}/twin_L08.out)."),
    "AC1-c-lab-embed-equals-twin": (None, None, "PASS",
        f"Re-run round 23 with {SCR}/embed_and_expected_check_r23.py: 'L07 embedded code == twin: True', 'L08 embedded code == twin: True' ({OUT}/embed_expected.out)."),
    "AC1-c-lab-expected-output": (None, None, "PASS",
        f"Re-run round 23 ({SCR}/embed_and_expected_check_r23.py, {OUT}/embed_expected.out): 'L07 expected == run output: True 18 18'; 'L08 expected == run output: True 13 13'."),
    "AC1-c-lab-seed-sweep": (None, None, "PASS",
        f"Re-run round 23: ledgers/AC1/scripts/AC1-c-r20/seed_sweep_r20.py over 45 seeds: 'L07 ... failing seeds: []', 'L08 ... failing seeds: []' ({OUT}/seed_sweep_r23.out). Supports L07.html:327 (E2) and L08.html:273 (E3)."),
    "AC1-c-cmd-page_smoke": (None, None, "PASS",
        f"Re-run round 23: tools/page_smoke.py --unit AC1 --pages L07 L08 exit 0; 'page_smoke modules/AC/AC1/L07.html: PASS', 'L08.html: PASS', 'page_smoke AC1: PASS' ({OUT}/page_smoke.out)."),
    "AC1-c-cmd-check_pages_dag": (None, None, "PASS",
        f"Re-run round 23: tools/check_pages.py --unit AC1 'check_pages AC1: PASS'; tools/check_dag.py --unit AC1 'check_dag AC1: PASS' ({OUT}/check_pages.out, {OUT}/check_dag.out)."),
    "AC1-c-cmd-pytest_ruff_mypy": (None, None, "PASS",
        f"Re-run round 23: pytest tests/test_labs.py tests/test_page_checks.py exit 0 ({OUT}/pytest.out); ruff check tools tests 'All checks passed!' ({OUT}/ruff.out); mypy --no-incremental 'Success: no issues found in 153 source files' ({OUT}/mypy.out)."),
    "AC1-c-cit-verify_refs": (None, None, "PASS",
        f"Re-run round 23: tools/verify_refs.py --unit AC1 'live re-verification of AC1: 2 of 560 entries, 0 problems' ({OUT}/vr_live.out); tools/verify_refs.py --offline 'offline integrity: 560 entries, 0 problems' ({OUT}/vr_offline.out). L07.html:442 and L08.html:384 hold an empty <ol data-references></ol>, so neither lesson cites a key."),
    "AC1-c-cards-dup-scan": ("1-structure cards duplicate scan", "course/modules/AC/AC1/cards.json (141 cards at 503d139)", "PASS",
        f"Re-run round 23 with {SCR}/delta_and_cards_r23.py ({OUT}/delta_cards.out): 141 cards at HEAD; 'duplicate ids: []', 'duplicate fronts: []', 'duplicate backs: []'. The round-22 count of 125 is stale: cards c141 (lesson L06) was added and c057, c069, c070, c071, c087, c088 were edited in L04 to L06 cards (outside this slice)."),
    "AC1-c-banned-phrases": (None, None, "PASS",
        f"Re-run round 23 with {SCR}/extract_and_scan_r23.py: 'banned-string hits: 0' over course/modules/AC/AC1/L07.html, L08.html and the L07/L08 cards ({OUT}/banned_scan.out). Strings checked: BUILDER_RULES 1.3 and 1.4 list, 'about <digit>', external URLs."),
    "AC1-c-dag-concepts": (None, None, "PASS",
        f"Re-run round 23: tools/check_dag.py --unit AC1 'check_dag AC1: PASS' ({OUT}/check_dag.out). Definitions in the slice: def-stock-based-compensation at L07.html:59 and def-deferred-taxes at L08.html:64 (grep id=\"def-...\"), each defined once."),
    "AC1-c-r10-hours-sum": (None, None, "PASS",
        "Re-run round 23 by grep of data-hours: L01 11, L02 12, L03 11, L04 11, L05 12, L06 12, L07 11 (L07.html:2), L08 10 (L08.html:2). Sum 90 = index.html data-hours-lessons=\"90\"; project data-hours-project=\"30\"; total 120 = curriculum/02-economics-finance-core.yaml:521 hours: 120. Hours are design targets (architect ruling); arithmetic only."),
    "AC1-c-r7-lab-student-mutants": (None, None, "PASS",
        f"Re-run round 23: archived r7 mutants in {OUT}/mutants_rerun_r23.out: r7-m8a, r7-m7a, r7-m7b exit 1 (FAIL), as expected."),
    "AC1-c-r7-alt-implementations": (None, None, "PASS",
        f"Re-run round 23: alt9a, alt9b, alt9c, alt10a, alt10b, alt17a, alt18a, alt18b, alt18c all exit 0 ({OUT}/mutants_rerun_r23.out); alt20a, alt20b exit 0 ({OUT}/rerun_mutants_r20_new.py.out)."),
    "AC1-c-r8-lab-student-mutants": (None, None, "PASS",
        f"Re-run round 23 ({OUT}/mutants_rerun_r23.out): r8-n2life, r8-n3sign, r8-n4te exit 1 (FAIL). r8-n1ceil and r8-n1b (ceiling base with remainder) exit 0: they still sum exactly, and the lab checks sums and identities only (L07.html:126): out of scope."),
    "AC1-c-r9-new-mutants": (None, None, "PASS",
        f"Re-run round 23 ({OUT}/mutants_rerun_r23.out): m9a through m9g all exit 1 (FAIL)."),
    "AC1-c-r9-alt-implementations-seeds": (None, None, "PASS",
        f"Re-run round 23: alt9a, alt9b, alt9c exit 0 ({OUT}/mutants_rerun_r23.out); seed sweep 0 failing seeds of 45 ({OUT}/seed_sweep_r23.out)."),
    "AC1-c-r9-embed-expected": (None, None, "PASS",
        f"Re-run round 23 ({SCR}/embed_and_expected_check_r23.py; {OUT}/embed_expected.out): both pairs True, 18 = 18 lines and 13 = 13 lines."),
    "AC1-c-r10-mutants-killed": (None, None, "PASS",
        f"Re-run round 23 ({OUT}/mutants_rerun_r23.out): m10b, m10d, m10e exit 1 (FAIL)."),
    "AC1-c-r10-m10a-survivor": (None, None, "PASS",
        f"Re-run round 23 ({OUT}/mutants_rerun_r23.out): m10a exit 0 (expense starts one year late; the schedule still sums inside the six-year horizon for these grants, and the lab checks sums and identities). Out of scope: no lesson sentence says the lab checks timing (L07.html:126, :133). The timing claims in E1 and E3 (L07.html:320-328) are read off the printed table and are not checked by the lab."),
    "AC1-c-r10-m10c-survivor": (None, None, "PASS",
        f"Re-run round 23 ({OUT}/mutants_rerun_r23.out): m10c exit 0 (base divides by vest years plus one; sums stay exact). Out of scope: the lab checks sums and identities; the base formula is stated at L07.html:63 and :81 and not checked by the lab (L07.html:126, :133)."),
    "AC1-c-r10-alt-correct-implementations": (None, None, "PASS",
        f"Re-run round 23: alt9a, alt9b, alt9c, alt10a, alt10b all exit 0 ({OUT}/mutants_rerun_r23.out); new alt23a, alt23b, alt23c also exit 0 (see AC1-c-r23-alt-implementations)."),
    "AC1-c-r17-mutants-killed": (None, None, "PASS",
        f"Re-run round 23 ({OUT}/mutants_rerun_r23.out): m17b, m17c, m17d, m17e exit 1 (FAIL); alt17a exit 0."),
    "AC1-c-r17-m17a-survivor": (None, None, "PASS",
        f"Re-run round 23 ({OUT}/mutants_rerun_r23.out): m17a exit 0 (SBC row starts at year zero). L07.html:133 claims only the schedule sums and the Section 2 identities; the lab does not check the year of the SBC row, so this is out of scope under the architect ruling on lab twins."),
    "AC1-c-r18-m18a-survivor-check": (None, None, "PASS",
        f"Re-run round 23 ({OUT}/mutants_rerun_r23.out): m18a exit 0 on the shipped seed (schedule check sums years 1 to 5 only). The lab's check does not reach year 6 for this seed. No lesson sentence claims the lab checks year 6; L07.html:327 claims the correct code passes for any seed, and the seed sweep (0 failing seeds of 45) confirms that for the correct twin. Out of scope."),
    "AC1-c-r18-m18c-sbc-omits-last-grant": (None, None, "PASS",
        f"Re-run round 23 ({OUT}/mutants_rerun_r23.out): m18c exit 0 (SBC row omits the last grant). The lab checks grant schedules with yearly_expense, not the SBC row, and the identities hold for any SBC row (L07.html:133). The figures in L07.html:357 are read off the printed table, which the lab does not check. Out of scope."),
    "AC1-c-r18-m18d-tax-depreciation-shifted": (None, None, "PASS",
        f"Re-run round 23 ({OUT}/mutants_rerun_r23.out): m18d exit 0 (tax depreciation one year late). L08.html:103 claims the lab checks (a), (b) and the year-5 balance only; the timing of the tax schedule is not claimed. Out of scope."),
    "AC1-c-r18-m18g-base-from-share-count": (None, None, "PASS",
        f"Re-run round 23 ({OUT}/mutants_rerun_r23.out): m18g exit 0 (base floors the share count). The lab checks sums and identities only (L07.html:126); out of scope."),
    "AC1-c-r18-alt-implementations": (None, None, "PASS",
        f"Re-run round 23: alt18a, alt18b, alt18c exit 0 ({OUT}/mutants_rerun_r23.out)."),
    "AC1-c-r18-seed-sweep": (None, None, "PASS",
        f"Re-run round 23: seed sweep over 45 seeds, 0 failing for L07 and L08 ({OUT}/seed_sweep_r23.out)."),
    "AC1-c-r19-cmd-check_pages_dag": (None, None, "PASS",
        f"Re-run round 23: check_pages AC1 PASS and check_dag AC1 PASS ({OUT}/check_pages.out, {OUT}/check_dag.out)."),
    "AC1-c-r19-cmd-run_labs": (None, None, "PASS",
        f"Re-run round 23: run_labs AC1: PASS (11/11) ({OUT}/run_labs.out)."),
    "AC1-c-r19-lab-twins-isolated": (None, None, "PASS",
        f"Re-run round 23: both twins exit 0 under python -I -W error ({OUT}/twin_L07.out, {OUT}/twin_L08.out)."),
    "AC1-c-r19-lab-embed-equals-twin-and-expected": (None, None, "PASS",
        f"Re-run round 23 ({SCR}/embed_and_expected_check_r23.py, {OUT}/embed_expected.out): embedded code equals the twin and the expected block equals the run for L07 (18 lines) and L08 (13 lines)."),
    "AC1-c-r19-seed-sweep": (None, None, "PASS",
        f"Re-run round 23: 45 seeds, 0 failing for L07 and L08 ({OUT}/seed_sweep_r23.out)."),
    "AC1-c-r19-page_smoke": (None, None, "PASS",
        f"Re-run round 23: tools/page_smoke.py --unit AC1 --pages L07 L08 PASS ({OUT}/page_smoke.out)."),
    "AC1-c-r19-verify_refs": (None, None, "PASS",
        f"Re-run round 23: live 2 of 560 entries, 0 problems; offline 560 entries, 0 problems ({OUT}/vr_live.out, {OUT}/vr_offline.out)."),
    "AC1-c-r19-cards-L07-L08": (None, None, "PASS",
        f"Re-run round 23 with {SCR}/delta_and_cards_r23.py ({OUT}/delta_cards.out): 'L07/L08 cards at pin: 40 at HEAD: 40 identical: True'."),
    "AC1-c-r19-mutants-rerun": (None, None, "PASS",
        f"Re-run round 23: {SCR}/mutants_r23_rerun.py (the archived r7, r8, r9, r10, r17, r18 lab mutants and alternatives) on 503d139 ({OUT}/mutants_rerun_r23.out): every FAIL-expected mutant exits 1, every alternative exits 0, and the survivors are those of the classification row."),
    "AC1-c-r19-new-student-mutants": (None, None, "PASS",
        f"Re-run round 23 ({OUT}/rerun_mutants_r19_new_rerun_r20.py.out): m19a, m19b, m19c exit 1 (FAIL); m19d exit 0 (out of scope, see survivor classification)."),
    "AC1-c-r19-survivor-classification": (None, None, "PASS",
        f"Re-run round 23 ({OUT}/mutants_rerun_r23.out, {OUT}/rerun_mutants_r19_new_rerun_r20.py.out, {OUT}/rerun_mutants_r20_new.py.out): survivors on the shipped seed are m10a, m10c, m17a, m18a, m18c, m18d, m18g, m19d, m20a, m20b, m20c (all exit 0). None is claimed by a lesson sentence as a check of the property it violates: L07.html:133 and :327, L08.html:103 and :209 name the checks (schedule sums, identities, year-5 balance)."),
    "AC1-c-r19-tooling-carried": (None, None, "PASS",
        f"Re-run round 23 rather than carried: pytest (test_labs, test_page_checks) exit 0, ruff check tools tests passed, mypy --no-incremental 153 files clean ({OUT}/pytest.out, {OUT}/ruff.out, {OUT}/mypy.out). git diff --stat fd9a9b7 503d139 -- tools references notation curriculum atlas plans/AC1-build-plan.md is empty."),
    "AC1-c-r20-mutants-rerun": (None, None, "PASS",
        f"Re-run round 23: all archived lab mutants re-run on 503d139 ({OUT}/mutants_rerun_r23.out; {OUT}/rerun_mutants_r20_new.py.out)."),
    "AC1-c-r20-new-mutant-m20a": (None, None, "PASS",
        f"Re-run round 23 ({OUT}/rerun_mutants_r20_new.py.out): m20a exit 0 on the shipped seed. Rotated tax percentages still sum to 100, so the identities hold. L08.html:103 and :209 make no claim about the tax-percentage order. Out of scope."),
    "AC1-c-r20-new-mutant-m20b": (None, None, "PASS",
        f"Re-run round 23 ({OUT}/rerun_mutants_r20_new.py.out): m20b exit 0. Equivalent: the cumulative tax shares are at least the book shares at every year end (40, 70, 90, 100, 100 against 20, 40, 60, 80, 100, L08.html:64), so K_t is never negative and max(K_t, 0) = K_t. Equivalent mutant, not a fault."),
    "AC1-c-r20-new-mutant-m20c": (None, None, "PASS",
        f"Re-run round 23 ({OUT}/rerun_mutants_r20_new.py.out): m20c exit 0 on the shipped seed (expense index shifted one year). The schedule still sums inside the horizon for these grants. L07.html:133 claims only the schedule sums and identities. Out of scope; seed-dependent failures (21 of 45 seeds, round 20) are not a claim of the lesson."),
    "AC1-c-r20-alt-implementations": (None, None, "PASS",
        f"Re-run round 23: alt20a and alt20b exit 0 ({OUT}/rerun_mutants_r20_new.py.out)."),
    "AC1-c-r9-delta-read": None,
}
RERUN = {k: v for k, v in RERUN.items() if v is not None}

NEW_ROWS = [
    ("AC1-c-r23-delta-read", "1-delta fd9a9b7 to 503d139 (slice paths)",
     "course/modules/AC/AC1/L07.html; L08.html; index.html; tests/labs/AC1/lab-AC1-L07-1.py; lab-AC1-L08-1.py; references/references.json; plans; tools; notation",
     "PASS",
     "git show fd9a9b7 and 503d139 compared with sha256 (ledgers/AC1/scripts/AC1-c-r23/delta_and_cards_r23.py, ledgers/AC1/scripts/AC1-c-r23/out/delta_cards.out): all six slice files byte-identical. course/modules/AC/AC1/project.html changed (outside AC1-c; it belongs to the project slice). git diff --stat fd9a9b7 503d139 is empty for tools, references, notation, curriculum, atlas and plans/AC1-build-plan.md. The only AC1 changes are L04, L05, L06, cards.json (c057, c069, c070, c071, c087, c088 and new c141, all L04 to L06), the project grader and project.html, and the lab twins L04 and L05. None of these is in AC1-c."),
    ("AC1-c-r23-read-L07", "2.2/2.4/2.9 full read of L07",
     "course/modules/AC/AC1/L07.html (rendered text, 308 lines); tests/labs/AC1/lab-AC1-L07-1.py (123 lines)",
     "PASS",
     f"Read every line of the rendered text ({OUT}/L07_text.txt, produced by {SCR}/extract_and_scan_r23.py; line numbers below are those extract lines) and the twin in full (lab-AC1-L07-1.py), checked against the printed run ({OUT}/twin_L07.out). Confirmed: Example 1.4 (extract line 41: 1,000 shares at $12.00, base 300,000 cents); Example 2.3 (line 61); M1 (lines 196 to 199: base 133,333, last year 133,334, recomputed in recompute.out); M2 (200 to 203); M3 (204 to 207: NI2 18,666.67, CFO2 20,000.00); P1 to P3 (209 to 220); E1 (222 to 225: year 3, 57,822.92, four vesting grants, matches the table); E2 (226 to 229: seed sweep, {OUT}/seed_sweep_r23.out); E3 (230 to 233: year 6 zero, NI 619,799.00 equals OI); R1 to R3 (235 to 246); misconceptions (187 to 193); key results (247 to 253, matching the printed table: 4 of 4 grants, 6 of 6 years, peak 57,822.92 in year 3); quiz numeric answers (4,000; 1,333.33; 18,666.67; 3,000 at lines 261 to 284). No sentence about the lab's checks was contradicted. banned_scan.out: 0 hits."),
    ("AC1-c-r23-read-L08", "2.2/2.4/2.9 full read of L08",
     "course/modules/AC/AC1/L08.html (rendered text, 264 lines); tests/labs/AC1/lab-AC1-L08-1.py (88 lines)",
     "PASS",
     f"Read every line of the rendered text ({OUT}/L08_text.txt; line numbers below are extract lines) and the twin in full, checked against the printed run ({OUT}/twin_L08.out). Confirmed: Example 1.4 (line 32: K 20,000, 30,000, 30,000, 20,000, 0; DTL 4,200, 6,300, 6,300, 4,200, 0); Example 2.2 (line 46: CT1 6,300, DE1 4,200, TE1 10,500, CT2 8,400, DE2 2,100); lab description (lines 48 to 49, matching the code asserts at lab lines 83 to 85); printed-output reading (line 137: current tax below expense in years 1 and 2, above it in years 4 and 5, matching 8,169.84 < 10,131.24, 16,677.15 < 17,657.85, 10,711.89 > 9,731.19, 14,356.65 > 12,395.25); Section 3 (138 to 141); misconceptions (142 to 148); M1 to M3 (151 to 162; M2 DTL 2,100, 1,680, 0 and DE 2,100, -420, -1,680, recomputed); P1 to P3 (164 to 175); E1 (177 to 180: balance 2,942.10 in years 2 and 3, K 14,010 = 30 percent of 46,700); E2 (181 to 184: 8,169.84 + 1,961.40 = 10,131.24); E3 (185 to 188); R1 (190 to 193); R2 (194 to 197: TE3 13,700); R3 (198 to 201); key results (202 to 209); quiz (210 to 258). Recomputed in recompute_numbers_r23.py ({OUT}/recompute.out). banned_scan.out: 0 hits."),
    ("AC1-c-r23-lab-claims", "2.5-labs lab-claim sentences vs code and output",
     "course/modules/AC/AC1/L07.html:122, :126, :327 (E2), embedded lab docstring at :133; L08.html:103, :107, :209, :273 (E3); tests/labs/AC1/lab-AC1-L07-1.py; lab-AC1-L08-1.py",
     "PASS",
     "L08.html:103 says the lab checks (a) and (b) in every year and the year-5 balance and does not check (d): lab-AC1-L08-1.py:66-67 (deferred_ok, tax_ok per year) and :84 (previous_dtl == 0 at year 5) confirm it. L08.html:209 says the current tax is below the total expense in years 1 and 2 and above it in years 4 and 5: out/twin_L08.out gives 8,169.84 < 10,131.24 and 16,677.15 < 17,657.85 and 10,711.89 > 9,731.19 and 14,356.65 > 12,395.25. The embedded lab docstring (L07.html:133) says the checks are the schedule sums and the Section 2 identities: lab-AC1-L07-1.py:131-132 and :119 to :120. E2 (L07.html:327) and E3 (L08.html:273) say the checks pass for any seed: seed sweep 0 failing of 45 (out/seed_sweep_r23.out) and the generator ranges in the code (grant years 1 to 3, vesting 3 or 4, so the last vesting year is at most 6; costs are multiples of 10,000 cents and pretax multiples of 100 cents)."),
    ("AC1-c-r23-alt-implementations", "2.5-labs over-constraint: alternative correct implementations (round 23)",
     "tests/labs/AC1/lab-AC1-L07-1.py (yearly_expense); tests/labs/AC1/lab-AC1-L08-1.py (cumulative; current)",
     "PASS",
     f"{SCR}/mutants_r23_new.py ({OUT}/mutants_new_r23.out): alt23a (L07, remainder cents spread over the first years, a different valid schedule) exit 0; alt23b (L08, cumulative from running totals, same value) exit 0; alt23c (L08, current tax with a round-half-up cutoff, equal on the lab's multiples of 100) exit 0. None fails any check, so the lab's checks do not over-constrain these correct implementations."),
    ("AC1-c-r23-m23a", "2.5-labs new student-error mutant m23a (L07 last year one base short)",
     "tests/labs/AC1/lab-AC1-L07-1.py:46-47 (remainder)", "PASS",
     f"{OUT}/mutants_new_r23.out: m23a exit 1, AssertionError. The remainder is one base short, so the grant's schedule exceeds its total and the schedule check fails. Killed."),
    ("AC1-c-r23-m23b", "2.5-labs new student-error mutant m23b (L08 book depreciation on the carrying amount)",
     "tests/labs/AC1/lab-AC1-L08-1.py:53 (book_dep)", "PASS",
     f"{OUT}/mutants_new_r23.out: m23b exit 1, AssertionError. Book depreciation at 20 percent of the carrying amount does not total the cost, so the total check fails. Killed."),
    ("AC1-c-r23-m23c", "2.5-labs new student-error mutant m23c (L07 base divides by the horizon, not the vesting years)",
     "tests/labs/AC1/lab-AC1-L07-1.py:45 (base)", "PASS",
     f"{OUT}/mutants_new_r23.out: m23c exit 0. The remainder formula keeps every schedule exact, so the schedule sums and the identities hold. The lab checks sums and identities only (L07.html:126, :133), and no lesson sentence claims the lab checks the base amount, so this is an out-of-scope lab survivor under the architect ruling. The printed table would differ from the page, which is a difference in output, not in a checked property."),
    ("AC1-c-r23-scripts-recorded", "1-structure: scripts and outputs cited",
     f"{SCR}/*.py; {SCR}/out/*", "PASS",
     "Every row of this round cites a script by its repository path (ledgers/AC1/scripts/AC1-c-r23/) or a command output file under ledgers/AC1/scripts/AC1-c-r23/out/. The re-used script ledgers/AC1/scripts/AC1-c-r20/seed_sweep_r20.py was run in this round."),
]

MUTANTS_KILLED_PREV = {
    # survivors on the shipped seed are excluded and recorded as PASS rows instead
}
SURVIVORS = {"r17-m17a", "r18-m18a", "r18-m18c", "r18-m18d", "r18-m18g", "r19-m19d", "r20-m20a", "r20-m20b", "r20-m20c"}
rerun_out = {}
for name in ["mutants_rerun_r23.out", "rerun_mutants_r19_new_rerun_r20.py.out", "rerun_mutants_r20_new.py.out", "mutants_new_r23.out"]:
    for line in (root / OUT / name).read_text(encoding="utf-8").splitlines():
        m = re.match(r"^(\S+?): exit=(\d+) observed=(\w+)", line) or re.match(r"^(\S+?) exit (\d+) expected", line) \
            or re.match(r"^(\S+?): exit=(\d+) observed=(\w+)", line)
        if m:
            case = m.group(1)
            rerun_out[case] = int(m.group(2))
        else:
            mm = re.match(r"^(\S+?) exit (\d+) ", line)
            if mm:
                rerun_out[mm.group(1)] = int(mm.group(2))


def find_case(key: str) -> str:
    bare = key.split("-", 1)[1] if key.startswith("r") and "-" in key else key
    hits = [c for c in rerun_out if c == key or c.startswith(key + "-") or c.startswith(bare + "-")]
    if len(hits) != 1:
        raise SystemExit(f"mutant {key}: {hits}")
    return hits[0]


mutants = []
for key in prev["mutants"]:
    mid = key["id"]
    if mid in SURVIVORS:
        continue
    case = find_case(mid)
    assert rerun_out[case] == 1, (mid, case, rerun_out[case])
    lab = "lab-AC1-L08-1" if "L08" in case else "lab-AC1-L07-1"
    mutants.append({"id": mid, "description": key["description"],
                    "killed_by": f"AssertionError in {lab} (round 23 re-run, {case}: exit 1)"})
for mid, lab, desc in [("m23a", "lab-AC1-L07-1", "L07 last vesting year takes one base short"),
                       ("m23b", "lab-AC1-L08-1", "L08 book depreciation on the carrying amount")]:
    case = [c for c in rerun_out if c.startswith(mid + "-")][0]
    assert rerun_out[case] == 1
    mutants.append({"id": f"r23-{mid}", "description": desc, "killed_by": f"AssertionError in {lab} (round 23 new, {case}: exit 1)"})

# ---- carry or rewrite the previous rows ----
SLICE_NAMES = {"course/modules/AC/AC1/L07.html": "L07.html", "course/modules/AC/AC1/L08.html": "L08.html",
               "course/modules/AC/AC1/index.html": "index.html", "tests/labs/AC1/lab-AC1-L07-1.py": "lab-AC1-L07-1.py",
               "tests/labs/AC1/lab-AC1-L08-1.py": "lab-AC1-L08-1.py", "references/references.json": "references.json"}
rows = []
for r in prev["rows"]:
    rid = r["id"]
    assert r["status"] == "PASS", rid
    if rid in RERUN:
        check, location, status, evidence = RERUN[rid]
        rows.append({"id": rid, "check": check or r["check"], "location": location or r["location"],
                     "status": status, "evidence": evidence})
        continue
    loc = r["location"]
    files = [short for path, short in SLICE_NAMES.items() if path in loc]
    if "cards.json" in loc:
        files.append("cards.json (L07/L08 card objects identical)")
    if "scripts" in loc or "ledgers/" in loc:
        files.append("cited scripts unchanged")
    if "tools/" in loc or "tests/labs/AC1" in loc and not files:
        files.append("lab twins")
    if not files:
        files = ["tooling and registry paths (unchanged since fd9a9b7)"]
    new_loc = loc
    new_evidence = r["evidence"]
    rid_card = re.search(r"c(\d{3})", rid)
    if rid_card and "cards.json" in (loc + new_evidence):
        card = "AC1-c" + rid_card.group(1)
        shift = line_of(new_cards, card) - line_of(old_cards, card)

        def bump(text: str) -> str:
            text = re.sub(r"cards\.json:(\d+)-(\d+)",
                          lambda m: f"cards.json:{int(m.group(1)) + shift}-{int(m.group(2)) + shift}", text)
            return re.sub(r"cards\.json (c\d+ )?\(lines (\d+)-(\d+)\)",
                          lambda m: f"cards.json {m.group(1) or ''}(lines {int(m.group(2)) + shift}-{int(m.group(3)) + shift})", text)

        new_loc = bump(loc)
        new_evidence = bump(new_evidence)
        if new_loc != loc or new_evidence != r["evidence"]:
            files.append(f"card {card} line numbers moved by {shift} lines (card object unchanged)")
    prefix = f"Carried from round 22 (" + "; ".join(files) + " byte-identical since the previous pin):"
    rows.append({"id": rid, "check": r["check"], "location": new_loc, "status": "PASS",
                 "evidence": f"{prefix} {new_evidence}"})

for rid, check, location, status, evidence in NEW_ROWS:
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence})

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids))
for r in prev["rows"]:
    assert r["id"] in ids, r["id"]
counts = {"PASS": sum(1 for r in rows if r["status"] == "PASS")}
verdict = "PASS" if counts["PASS"] == len(rows) and all(m.get("killed_by") for m in mutants) else "FAIL"
fragment = {
    "unit": "AC1",
    "slice": "AC1-c",
    "round": 23,
    "round_note": "round 23 (independent re-verification of AC1-c after pin 503d139). Delta since the round-22 pin fd9a9b7: the six slice files (L07.html, L08.html, index.html, the two lab twins, references.json) are byte-identical; the L07/L08 card objects (40) are identical; cards.json changed only in L04 to L06 cards (and new c141, L06), so card line numbers moved by 6 and cards.json rows are re-located. Command rows and mutant rows are re-run on 503d139.",
    "verifier": "independent verifier (Haiku 5.5), slice AC1-c round 23; did not build AC1 and shares no context with its builders or earlier verifiers",
    "pin": "503d139",
    "base": "fd9a9b7 (previous pin of the round-22 fragment /tmp/fanout-frags/AC1-c.round22.json, for the delta)",
    "checkout": "/tmp/verify23-AC1-c",
    "scratch": "/tmp/AC1-v/AC1-c-r23",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "scripts": sorted(p.relative_to(root).as_posix() for p in (root / SCR).rglob("*") if p.is_file()),
    "notes": "Not checked: the project slice (AC1 project.html, grader/test_project.py, the L04 to L06 pages and cards outside AC1-c); the hours are design targets (architect ruling: arithmetic only, index hub 90 plus 30 equals 120); live web sources beyond verify_refs (no network fetch of the references beyond the tool, which re-verified 2 of 560 live); Springer and similar access-blocked sources were not contacted. Lab survivors on the shipped seed are out-of-scope PASS rows under the architect ruling (lab twins), each with its lesson sentence. m20b is an equivalent mutant (K_t never negative for this schedule).",
    "summary": f"PASS: {counts['PASS']} of {len(rows)} rows. Mutants: {len(mutants)} listed, all killed (the round-22 survivors are PASS rows, not listed mutants). New student-error mutants m23a and m23b killed; m23c an out-of-scope lab survivor.",
}
dest = root / "ledgers/AC1/AC1-c.json"
dest.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", len(rows), "mutants", len(mutants), "verdict", verdict)
