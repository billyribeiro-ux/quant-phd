# Builds ledgers/CS2/CS2-c.json (round 9). Carried rows keep round-8 evidence under the carry prefix.
import json, subprocess
ROOT = "/Users/billyribeiro/.fanout/wt/verifyS9-CS2-c"
r8 = json.load(open("/Users/billyribeiro/.fanout/frags/S-CS2-c.round8.json"))
r8rows = {r["id"]: r for r in r8["rows"]}
P_LESSON = ("Carried from round 8 (L09.html, L10.html, L11.html, index.html, tests/labs/CS2, notation/, references/, "
            "tools/check_pages.py, tools/check_dag.py, tools/run_labs.py, tools/page_smoke.py, tools/refs and "
            "course/modules/M/M1 byte-identical since 4540351d; scripts/CS2-c-r9/byte_identity_r9.txt):")
P_CARD = ("Carried from round 8 (the cited CS2 card objects are JSON-identical to 4540351d, card_delta_r9.out lists only "
          "CS2-c231 as changed; cited lesson files byte-identical since 4540351d):")
carry_lesson = {"C-05", "C-10", "C-11", "C-12", "C-13", "C-14", "C-15", "C-16", "C-17", "C-18", "C-19", "C-20", "C-21",
                "C-22", "C-23", "C-24", "C-25", "C-26", "C-27", "C-28", "C-29", "C-30", "C-31", "C-32", "C-33", "C-34",
                "C-35", "C-36", "C-37", "C-38", "C-40", "C-41", "C-42", "C-43", "C-56", "C-58", "C-61", "C-62", "C-64",
                "C-69", "C-70", "C-71", "C-72", "C-73", "C-74"}
carry_card = {"C-44", "C-45", "C-46", "C-47", "C-48", "C-49", "C-50", "C-51", "C-52", "C-57", "C-59", "C-60", "C-63",
              "C-65", "C-66", "C-67", "C-68", "C-76", "C-77", "C-78", "C-79", "C-80", "C-81", "C-82", "C-83", "C-91",
              "C-93", "C-94", "C-95", "C-96"}
fresh = {}
def F(cid, status, ev):
    fresh[cid] = (status, ev)

F("C-01", "PASS", "Fresh on 95f3f8cb (cards.json changed since 4540351d, so re-run): `.venv/bin/python tools/check_pages.py --all` exit 0 with 27 'check_pages <UNIT>: PASS' lines and no FAIL (ledgers/CS2/scripts/CS2-c-r9/check_pages_all.txt); `tools/check_pages.py --unit CS2` printed 'check_pages CS2: PASS', exit 0 (check_pages_unit.txt). This covers cards.json: 198 entries, 198 unique ids, lesson existence, grades and cite keys. tools/ reads cards.json only in check_pages.py (grep).")
F("C-02", "PASS", "Fresh on 95f3f8cb: `.venv/bin/python tools/check_dag.py --all` exit 0, 27 PASS lines, 'check_dag CS2: PASS', no FAIL (ledgers/CS2/scripts/CS2-c-r9/check_dag_all.txt). L09, L10, L11 and index.html byte-identical since 4540351d (byte_identity_r9.txt).")
F("C-03", "PASS", "Fresh on 95f3f8cb: `.venv/bin/python tools/run_labs.py --unit CS2` printed 'run_labs CS2: PASS (14/14)', exit 0 (ledgers/CS2/scripts/CS2-c-r9/run_labs_unit.txt). The printed L10 block equals the expected block at L10.html:206-210 (twin_L10.out).")
F("C-04", "PASS", "Fresh: `.venv/bin/python -I -W error tests/labs/CS2/lab-CS2-L09-1.py`, L10 and L11 each exit 0 with 0 bytes on stderr (ledgers/CS2/scripts/CS2-c-r9/twin_L09.out/.err, twin_L10.out/.err, twin_L11.out/.err).")
F("C-06", "PASS", "Fresh: `.venv/bin/ruff check .` printed 'All checks passed!', exit 0 (ruff_check.txt); `.venv/bin/ruff check tests/labs/CS2` exit 0; `.venv/bin/ruff format --check .` printed '555 files already formatted', exit 0 (ruff_format.txt).")
F("C-07", "PASS", "Fresh: `.venv/bin/mypy --no-incremental` printed 'Success: no issues found in 386 source files', exit 0 (ledgers/CS2/scripts/CS2-c-r9/mypy.txt). The repository changed (FC2 twins, ruling 37), so the repository gate was re-run.")
F("C-08", "PASS", "Fresh: `.venv/bin/pytest -q tests/test_labs.py -k 'CS2 and (L09 or L10 or L11)'` exit 0 (pytest_labs_cs2_l09_l11.txt); `.venv/bin/pytest -q tests/test_page_checks.py tests/test_docs_figures.py` exit 0 (pytest_misc.txt).")
F("C-09", "PASS", "Fresh: `.venv/bin/python tools/verify_refs.py --offline` printed 'offline integrity: 560 entries, 0 problems', exit 0 (ledgers/CS2/scripts/CS2-c-r9/verify_refs_offline.txt). references/ and notation/ byte-identical since 4540351d.")
F("C-39", "PASS", "Fresh deck-wide card part: card_delta_r9.py scanned all 198 cards (front and back), case-sensitive, for we, our, you, I, note, recall, round, verifier, builder, orchestrator, TODO, TBD, placeholder: 'process-word hits []' (card_delta_r9.out). Lesson part carried: L09, L10, L11 byte-identical since 4540351d (byte_identity_r9.txt).")
F("C-53", "PASS", "Fresh: card_delta_r9.out: 198 entries, 198 unique ids; exact (front, back) duplicate pairs []; duplicate fronts []. Near-duplicate pairs are unchanged in kind and are observation only: CS2-c231 and CS2-c132 both state Theorem 2.4's 2n bound (c231 is the Lab 1 instance, N = 200). c231's new back now repeats c132's hypothesis sentence word for word, as the rules require; it is not a second card for the same question.")
F("C-54", "PASS", "Fresh: card_delta_r9.out 'L09-L11 cards 49 numeric tokens missing from lesson: []': every numeric token (excluding 0 to 3) in the front and back of the 49 L09-L11 cards occurs in that card's lesson with tags stripped. This is a substring presence check; the c231 values (400, 200, 396, 399) were also checked against the lab output (C-89).")
F("C-55", "PASS", "Fresh for CS2-c231, the only card changed since 4540351d (card_delta_r9.out 'changed [CS2-c231]'): its back's hypothesis sentence matches the Theorem 2.4 hypotheses at L10.html:98 and its 2n bound matches the claim at L10.html:98; its 400, 396 and 399 match the expected block (L10.html:206-210) and the interpretation (L10.html:211). The other cards changed in round 8 (CS2-c200, c244, c245) are JSON-identical to 4540351d and their lessons are byte-identical; carried from round 8 for those (see C-78 to C-83, C-93 to C-96).")
F("C-75", "PASS", "Fresh deck-wide re-check (the scope of this row is every card that states Theorem 2.4, and c231 changed). L10 deque Theorem 2.4 (L10.html:97-98: w >= 1 fixed; n >= 1 values at positions 0..n-1; real values, exact comparisons): CS2-c132 (cards.json:884-887) states all three; CS2-c231 (cards.json:1333) now states all three; CS2-c133, c134 and c137 cite Corollary 2.5, whose hypotheses are 'Those of Theorem 2.4' (L10.html:108), and each states the three. CS2-c135 (Corollary 2.5(c)) states w >= 1 and exact comparisons, and its series is concrete (w+1 values at positions 0..w), so the n >= 1 hypothesis holds by construction and is not omitted. L11 sketch Theorem 2.4 (L11.html:107-108: 'Those of Theorem 2.2, with n >= 1, and the capacities of Definition 2.1'): CS2-c147, c148, c200 and c245 state those hypotheses; CS2-c236 cites Theorem 2.4 only for the one-compaction parity identity proved in its proof (L11.html:113) and states that identity's own hypotheses (sorted buffer, even-numbered items kept), so it claims no Theorem 2.4 conclusion without its hypotheses.")
F("C-84", "PASS", "Fresh: card_delta_r9.out: added [], removed [], changed [CS2-c231], order preserved; `git diff --numstat 4540351d HEAD -- course/modules/CS/CS2/cards.json` = 1 insertion, 1 deletion (line 1333, the back of CS2-c231). 198 entries, 198 unique ids. No other CS2 card changed in this range.")
F("C-85", "PASS", "Fresh for CS2-c231: w (window size, L10.html:58 'Fix an integer w >= 1'), n (values inserted, Theorem 2.4 hypothesis (2)) and N (number of values, L10.html:120 'where N = 200 is the number of values') are used with their lesson meanings. notation/notation.json registers 8 program-wide symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q) and none of w, n, N; its 'about' field says N and other conventionally local letters are defined in each lesson where used. No registered symbol is reused.")
F("C-86", "PASS", "Fresh for CS2-c231 (front and back): no process word (C-39 scan), and no hedge word (case-insensitive scan for probabl, likely, seems, roughly, approximately, might, may, could, appears, suggest: no match in the card, card_delta_r9.py).")
F("C-87", "PASS", "Fresh for CS2-c231: scope scan (all, every, only, same, any, always, never, exact, exactly, stable, optimal) finds only 'exact' in the back, which names Theorem 2.4 hypothesis (3), 'comparisons are exact' (L10.html:98), an explicit hypothesis. 'each' in the front refers to the ten printed totals (5 windows x 2 deques, L10.html:206-210).")
F("C-88", "PASS", "Round-8 FAIL resolved. cards.json:1333 (CS2-c231 back) now begins 'Assume w >= 1 is fixed, the series has n >= 1 values inserted at positions 0 to n - 1, and the values are real with exact comparisons. Theorem 2.4 then bounds ...'. Each of Theorem 2.4's hypotheses (L10.html:98: (1) w >= 1 fixed, (2) n >= 1 values at positions 0..n-1, (3) real values with exact comparisons) is stated, in the same words CS2-c132 uses (cards.json:884-887). The lab's w values (1, 2, 5, 13, 30) and n = 200 satisfy them (twin_L10.out). Grade C with basis 'Lab 1 (SIMULATED series, one seed)' is not an over-grade: the 2n bound is T, the 396-399 totals are C naming the lab.")
F("C-89", "PASS", "Fresh: twin_L10.out (python -I -W error, exit 0, stderr 0 bytes): per-window operation totals min/max are 399/399 (w=1), 398/399 (w=2), 398/398 (w=5), 397/398 (w=13), 396/397 (w=30), so the card's 'from 396 to 399 across the five window sizes, for both deques' is exact. The bound printed is 2N = 400, matching the expected block (L10.html:206-210) and the interpretation (L10.html:211). Basis is correct for grade C.")
F("C-90", "PASS", "Fresh: lab-CS2-L10-1.py:3 'a seeded integer series of N = 200 values' and :16 'N = 200'; the card's 2N = 400 is 2n at n = 200. Theorem 2.4 (L10.html:97-103) concludes 'at most 2n' operations (appends plus removals), and the lab counts operations as 1 + removals per push (twin lines 48). The hypothesis gap is closed by C-88.")

rows = []
for r in r8["rows"]:
    cid = r["id"]
    if cid in fresh:
        status, ev = fresh[cid]
        rows.append({"id": cid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev})
        continue
    if cid in carry_lesson:
        prefix = P_LESSON
    elif cid in carry_card:
        prefix = P_CARD
    elif cid == "C-92":
        prefix = ("Carried from round 8 (ledgers/CS2/scripts/CS2-c-r8/welford_mechanism_c244.py byte-identical since "
                  "4540351d, byte_identity_r9.txt; card CS2-c244 JSON-identical):")
    else:
        raise SystemExit(f"unclassified row {cid}")
    assert r["status"] == "PASS", cid
    rows.append({"id": cid, "check": r["check"], "location": r["location"], "status": "PASS",
                 "evidence": prefix + " " + r["evidence"]})
assert [r["id"] for r in rows] == [r["id"] for r in r8["rows"]], "ids must be kept"
pin = subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
frag = {
    "unit": "CS2",
    "slice": "c",
    "round": 9,
    "verifier": "Haiku independent verifier, CS2-c round 9 (closing delta verification per ruling 30; did not build CS2; no builder context)",
    "pin": pin,
    "base": "4540351dc664559cdfd371b908f2b4e644cf4297 (round-8 pin; round-8 fragment /Users/billyribeiro/.fanout/frags/S-CS2-c.round8.json read as context; its PASS rows were not trusted and are carried only with byte or JSON identity; its FAIL C-88 was re-decided)",
    "checkout": ROOT + " (detached at 95f3f8cb; .venv symlinked)",
    "scratch": "ledgers/CS2/scripts/CS2-c-r9/",
    "verified_at": "2026-11-09T15:20:00+00:00",
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [
        "ledgers/CS2/CS2-c.json is overwritten by this round's fragment, as the protocol requires; the round-8 fragment in /Users/billyribeiro/.fanout/frags/ was read as context only.",
        "ledgers/CS2/scripts/CS2-c-r8/ (tracked since 4540351d) was not modified; its welford_mechanism_c244.py was not re-run this round (C-92 carried by byte identity).",
        "page_smoke (C-05) was not re-run this round: L09, L10, L11 and tools/page_smoke.py are byte-identical since 4540351d and page_smoke reads no cards.json (carried).",
    ],
    "notes": (
        "Delta 4540351d..95f3f8cb for the slice: only course/modules/CS/CS2/cards.json changed (one line, CS2-c231 back, line 1333). "
        "L09-L11 lessons, index, the three twins, notation/, references/ and the M1 lesson are byte-identical (byte_identity_r9.txt). "
        "Rows re-verified fresh (20): C-01, C-02, C-03, C-04, C-06, C-07, C-08, C-09, C-39, C-53, C-54, C-55, C-75, C-84, C-85, C-86, C-87, C-88, C-89, C-90 "
        "(all rows whose subject is cards.json as a whole, the c231 card, or a deck-wide scope, plus the commands re-run this round). "
        "Carried (76): every other row, with its round-8 evidence under the carry prefix, because its cited lesson, twin, notation, reference, tool or card object is byte- or JSON-identical to 4540351d. "
        "Ruling 37: no new mutants were written; the slice is a lesson slice with no project grader, so mutation testing does not apply (ruling 26 kinds only). "
        "Observations, not FAILs: (a) CS2-c231 and CS2-c132 are near-duplicates (both state Theorem 2.4's 2n bound; c231 is the Lab 1 instance); (b) CS2-c135's n >= 1 hypothesis holds by construction of its concrete series rather than being restated. "
        "Not checked this round: FC2 twins and ruling 37 text changed in the same range (other slices); other CS2 slices and other units; a fresh page_smoke run (carried, see freshness_flags)."
    ),
    "summary": (
        "CS2 slice c, round 9 (closing delta verification, ruling 30, 4540351d to 95f3f8cb). 96 rows: PASS 96, FAIL 0. "
        "The round-8 FAIL (C-88: CS2-c231 omitted Theorem 2.4's hypotheses) is resolved: the back now states all three hypotheses, matching L10.html:98 and CS2-c132. "
        "20 rows re-verified fresh with new commands (check_pages --all and --unit CS2, check_dag --all, run_labs CS2 14/14, the three twins under python -I -W error, ruff check and format, mypy 386 files, pytest subsets, verify_refs --offline 560/0) and deck-wide scans (duplicates, process words, numeric tokens, Theorem 2.4 hypotheses). "
        "76 rows carried under the carry prefix. Mutants: none (ruling 37)."
    ),
}
json.dump(frag, open(ROOT + "/ledgers/CS2/CS2-c.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(ROOT + "/ledgers/CS2/CS2-c.json", "a", encoding="utf-8").write("\n")
print("rows", len(rows), "fresh", len(fresh), "carried", len(rows) - len(fresh), "fail", sum(r["status"] != "PASS" for r in rows))
