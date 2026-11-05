"""Build ledgers/E3/E3-g.json for round 10: carry round-8 PASS rows whose subject is unchanged, re-verify the rest."""
import json
import subprocess
from datetime import UTC, datetime

R = "/Users/billyribeiro/.fanout/wt/verifyD10-E3-g"
PIN = subprocess.run(["git", "-C", R, "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
BASE = "2d755599d8d74df292e3e43025f0458c4053802e"
r8 = json.load(open("/Users/billyribeiro/.fanout/frags/D-E3-g.round8.json", encoding="utf-8"))

CARRY_FILES = ("course/modules/E/E3/L05.html, L06.html, L07.html, L08.html, tests/labs/E3/lab-E3-L05-1.py..L08-1.py "
               "and every cited card object (cards.json per-id diff against 2d755599 shows the only changed or added "
               "slice ids are E3-c131, E3-c184, E3-c185)")

OVERRIDE = {
    "E3g8-c131-basis": ("FAIL",
        "E3-c131 back and basis (round 10: both changed since 2d755599). Overclaim: 'the 40-digit values are Problem E2'",
        "cards.json E3-c131 back and basis (line ~866-868); L07.html Problem E2 (L07.txt line 253)",
        "Recomputed with python decimal at 60 digits (ledgers/E3/scripts/E3-g-r10/): Gamma(A)=150*omega(3/10)=42.8686327356757356..., "
        "Gamma(B)=100*omega(3/5)=39.1250770026808434..., difference 3.7435557329948922..., i.e. 3.7436 to four decimals and "
        "3.74355573 to eight. Eight-decimal roundings 42.86863274 - 39.12507700 = 3.74355574 (correct). Printed 42.8686 - 39.1251 = 3.7435 "
        "(lab line 202). The numbers are right. But Problem E2 prints only the eight-decimal values and the DIFFERENCE 3.74355573 of the "
        "40-digit values; it never prints the 40-digit values themselves, so 'the 40-digit values are Problem E2' is inaccurate.",
        "Rewrite the parenthetical and basis to point at the difference only, e.g. back '(Lab 1, part C; the difference of the 40-digit "
        "values is given in Problem E2)' and basis 'Lab 1, part C; Problem E2 (40-digit difference)'; or print the 40-digit values in Problem E2."),
    "E3g4-c131-unrounded": ("PASS",
        "E3-c131 unrounded difference, to four decimals (re-verified: card changed in basis wording only)",
        "cards.json E3-c131; L07.html Problem E2",
        "Recomputed Gamma(A)-Gamma(B) at alpha=1 to 40+ digits with python decimal (ledgers/E3/scripts/E3-g-r10/): 3.74355573299... "
        "-> 3.7436 to four decimals. Printed values 42.8686 and 39.1251 (lab line 202) differ by 3.7435. The answer 3.7436 is correct."),
    "E3g3-basis-wording": ("FAIL",
        "basis strings of the C cards (re-verified; E3-c131 basis changed in round 10)",
        "cards.json E3-c131 basis (line ~868)",
        "Every other C-card basis in the slice is byte-identical to 2d755599 and names its lab (carried). E3-c131 basis 'Lab 1, part C; Problem E2 (40-digit values)' "
        "names a source that does not print the 40-digit values (see E3g8-c131-basis).",
        "Basis 'Lab 1, part C; Problem E2 (40-digit difference)'."),
    "E3g-r2-L07-G6": ("FAIL",
        "L07 lab part C and cards E3-c127, c128, c131, c133, c135 (re-verified; c131 changed)",
        "cards.json E3-c127, c128, c131, c133, c135; L07.txt lines 202-203 (lab part C output)",
        "c127 matches lab lines 202-203 (42.8686, 39.1251, 4.8788, 3.9125, A above B at both alphas). c128, c133, c135 byte-identical to 2d755599 (carried). "
        "c131 fails: see E3g8-c131-basis.",
        "Fix E3-c131 as in E3g8-c131-basis."),
    "E3g-r2-hypotheses": ("FAIL",
        "2.4 cards carry the hypotheses of the proposition they cite (re-verified; E3-c184 is new)",
        "cards.json E3-c184 (new, line ~1222); L05.txt line 50 (Proposition 2.2: 'Assume A1 to A4 for deterministic plans')",
        "E3-c184 cites Proposition 2.2 but states neither A1 to A4 nor beta. Lab 1 checks the closed form only at beta = 0.9 "
        "(L05.txt line 197: analytic = ((1 - 0.9)/0.9)*(4/2)^(1/0.5); line 226 prints True). psi = 1/2 satisfies A2 but is not stated as such. "
        "The other cards that cite Proposition 2.2 (E3-c084) carry 'Under A1 to A4 for deterministic plans'. All other hypotheses in the slice "
        "carried and unchanged.",
        "Add the hypotheses: 'Under A1 to A4 for deterministic plans, and at beta = 9/10 (the value Lab 1 uses), (c0, c1) = (2, 4) and psi = 1/2, "
        "the closed form ... agrees with the MRS Lab 1 computes by central differences (Proposition 2.2).'"),
    "E3g4-lab-observations": ("FAIL",
        "2.7 lab-versus-theorem pairs (re-verified; E3-c184 is a new lab-versus-Proposition 2.2 pair)",
        "cards.json E3-c184; L05.txt lines 197-198, 226",
        "The pair E3-c184 / Lab 1 line 226 is a true observation at beta = 0.9, psi = 1/2, (c0, c1) = (2, 4), but the card states it without beta, "
        "so the lab-versus-theorem pair is not stated at the scope the lab checks. The other lab pairs in the slice are carried unchanged. "
        "E3-c185 pairs Remark 1.5's mean 5/2 with lab line 209 and is a true pair.",
        "Same fix as E3g-r2-hypotheses: state beta = 9/10 on E3-c184."),
    "E3g-dup-scan": ("PASS",
        "2.7 duplicates: full scan of all 178 unit cards (re-run this round; new cards E3-c183..c186)",
        "cards.json (whole unit)",
        "Python scan (ledgers/E3/scripts/E3-g-r10/): 178 cards, 178 unique ids, no duplicate front and no duplicate back. Front-prefix collisions "
        "(12 groups) were read: each pair asks a different question (e.g. E3-c169 'U' and E3-c170 'CE1' on the same tree; E3-c144 red and E3-c182 black urn). "
        "No slice card duplicates another card."),
    "E3g-r2-coverage": ("PASS",
        "2.9 / 2.7 retrieval: every key result, definition and misconception of L05-L08 has a card (re-run with the new L05 cards)",
        "cards.json L05 cards (22); L05.txt Definition 1.1, Theorem 1.3, Corollary 1.4, Remark 1.5, Definition 2.1, Proposition 2.2, Remark 2.3, "
        "Remark 3.1, Theorem 3.2, Corollary 3.3, Remark 3.4, Section 5 misconceptions",
        "Each key result has a card: Def 1.1 c078; Remark 1.2 c079; Thm 1.3 c080; Cor 1.4 c081; Remark 1.5 c082 and c185; Def 2.1 c083; "
        "Prop 2.2 c084 and c184; Remark 2.3 c085; Remark 3.1 c086; Thm 3.2 c087; Cor 3.3 c088; Remark 3.4 c089 and c091; "
        "Section 5 misconceptions: 1st c090, 2nd c085, 3rd c081 (with c082). No key result is left uncarded."),
    "E3g8-card-numbers": ("PASS",
        "every number on a slice card appears in its lesson; no duplicate cards (re-run on 87 slice cards)",
        "cards.json L05..L08 cards (87); L05.txt, L06.txt, L07.txt, L08.txt",
        "Script (ledgers/E3/scripts/E3-g-r10/): every numeric token of every slice card back is present in the lesson text; no absent token. "
        "E3-c184 numbers 2, 4, 1/2 and E3-c185 numbers 5/2, 1, 4, 1/2 appear in L05.txt (lines 197, 226, 209, 45)."),
    "E3g-r2-numbers": ("PASS",
        "2.2 numbers in prose and cards (re-run on the changed and new cards)",
        "cards.json E3-c131, c184, c185; L05.txt lines 45, 209, 226; L07.txt lines 202, 253",
        "Remark 1.5 mean 5/2 and CE1 8/5 and 12/5: recomputed (1/2 * 1 + 1/2 * 4 = 5/2; 1/CE = 1/2(1 + 1/4) = 5/8, CE = 8/5; "
        "1/CE = 1/2(1/2 + 1/3) = 5/12, CE = 12/5). Closed form (1/9)*4 = 0.4444 agrees with the lab's numeric MRS (line 226 True). "
        "E3-c131 numbers verified in E3g4-c131-unrounded."),
    "E3g-r2-grades": ("PASS",
        "2.3 grades: card grades against the lesson key-results grades (re-run on new cards)",
        "cards.json E3-c131 (C), E3-c184 (C), E3-c185 (C); L05.txt line 227 (lab grade convention)",
        "L05.txt line 227 states that results of Lab 1 are C ('Every result of this lab holds on the listed cases'). E3-c184 and E3-c185 are "
        "C with basis 'Lab 1', consistent with that convention and with carried E3-c093, c169, c170. E3-c185 is a one-line exact mean "
        "(also on the page in Remark 1.5); grading it C follows the lesson's own convention, so it is not a FAIL here. E3-c131 C is right."),
    "E3g-r2-refs-cross": ("PASS",
        "2.9 DAG / cross-lesson references used by the cards (re-run on new cards)",
        "cards.json E3-c184, E3-c185; L05.txt",
        "E3-c184 cites Proposition 2.2 and Lab 1 (both in L05); E3-c185 cites Remark 1.5 and Lab 1 (both in L05). Neither card cites another lesson. "
        "E3-c131 cites Lab 1 part C and Problem E2 (both in L07)."),
    "E3g-r2-registry": ("PASS",
        "2.1 citations (registry keys cited by L05-L08 cards): new cards cite no registry key",
        "cards.json E3-c184, E3-c185; references/references.json (unchanged since 2d755599)",
        "No registry key appears on the new cards; references/ has no delta since 2d755599. verify_refs --offline: 560 entries, 0 problems (see E3g6-verify-refs)."),
    "E3g-r2-scope-words": ("PASS",
        "2.4 / 2.9 scope words in the slice (re-run on the changed and new cards)",
        "cards.json E3-c131, c184, c185 (front and back); L05..L08 lessons (unchanged)",
        "Scope-word scan (only, all, always, every, any, same, exactly, drives) over the three changed cards: no hit. Lessons unchanged since 2d755599 (carried)."),
    "E3g-r2-process-words": ("PASS",
        "1.3 / 1.4 banned and process phrases (re-run on changed cards)",
        "cards.json E3-c131, c184, c185",
        "Scan for we/our/us, TODO/TBD/placeholder, 'this slice', builder, verifier, agent, round N: no hit in front or back of the three changed cards."),
    "E3g-r2-gates": ("PASS",
        "2.9 gates: check_pages (L05-L08 each), check_dag, check_projects, page_smoke, ruff, mypy, verify_refs (re-run on pin 47a36d8c)",
        "ledgers/E3/scripts/E3-g-r10/*.out",
        "check_pages --unit E3 --page L05/L06/L07/L08: PASS each. check_dag --unit E3: PASS. check_projects --unit E3: PASS. "
        "ruff check . : All checks passed; ruff format --check .: 553 files already formatted. mypy --no-incremental: no issues in 385 files. "
        "verify_refs --offline: 560 entries, 0 problems. run_graders was not run (no grader in this slice; E3 project graders are another slice)."),
    "E3g-r2-delta": ("PASS",
        "delta of the slice since the previous pin (round-8 pin 2d755599 to 47a36d8c)",
        "git diff 2d755599 47a36d8c -- course/modules/E/E3 tests/labs/E3 notation references tools course/assets course/templates",
        "Slice files: L05.html, L06.html, L07.html, L08.html byte-identical; tests/labs/E3/lab-E3-L05..L08-1.py byte-identical; cards.json changed "
        "for ids c004, c022, c050, c131, c159, c180 and added c183..c186; of those, slice-g ids are c131 (basis/back), c184 and c185 (new). "
        "Other delta touched E3 project files, curriculum/01-foundations.yaml, curriculum.json, program.json, glossary.json, labs of other units "
        "(out of scope). notation/, references/, tools/, course/assets/, templates unchanged for E3."),
    "E3g8-delta": ("PASS",
        "delta 2d755599..47a36d8c for every slice subject (re-read this round)",
        "git diff --stat and per-file diff (see E3g-r2-delta)",
        "Every slice subject re-read: the lesson pages and lab twins are identical; the changed card objects are c131 (fails, see E3g8-c131-basis), "
        "c184 and c185 (new, verified above). All other slice card objects are identical JSON to the round-8 pin."),
    "E3g3-delta-r3": ("PASS",
        "delta read (re-read on this pin, round 10)",
        "git diff 2d755599 47a36d8c -- course/modules/E/E3/cards.json",
        "Hunks of cards.json read in full. Slice-relevant hunks: E3-c131 (fails, E3g8-c131-basis), E3-c184 and E3-c185 (new). The hunks for "
        "E3-c004, c022, c050, c159, c180, c183, c186 are outside slice g (L01, L02, L03, L04) and are not graded here."),
    "E3g-r2-lab-twins": ("PASS",
        "2.5 labs: run_labs, twins under python -I -W error, page code equals twin, expected block equals output (L05..L08)",
        "tests/labs/E3/lab-E3-L05-1.py..L08-1.py; L05.html, L07.html code and output blocks",
        "run_labs --unit E3 --page L05, L06, L07, L08: PASS each. python -I -W error tests/labs/E3/lab-E3-L0x-1.py exit 0 for x = 5..8. "
        "L05 page code block equals the twin (7637 characters, identical) and the L05 output block equals the twin output line by line (23 lines). "
        "L07 page code equals the twin (6892 characters) and its output block equals the twin output."),
    "E3g8-lab-twins-run": ("PASS",
        "lab twins under python -I -W error; page code equals twin; expected block equals output (L07, L08 re-run)",
        "tests/labs/E3/lab-E3-L07-1.py, lab-E3-L08-1.py; L07.html, L08.html",
        "Re-run on pin 47a36d8c: L07 and L08 twins exit 0 under python -I -W error; L07 part A..D lines 186-204 match the twin output; "
        "L08 run_labs PASS (1/1)."),
    "E3g7-card-xrefs": ("PASS",
        "2.9 structure: every 'Remark x.y', 'Proposition x.y', 'Example x.y', 'Model', 'Problem', section and misconception reference in the slice cards resolves in its lesson (re-run on 87 cards)",
        "cards.json L05..L08 (87)",
        "Scan of Remark/Proposition/Theorem/Corollary/Example/Definition/Observation/Problem/Lab/Section/Model/Assumption/Step references in the 87 slice cards: "
        "every reference resolves in its lesson text except 'Problem E2', which the lesson labels 'E2 ·' under Problem set (L07.txt line 250), a labelling "
        "match, not a missing target."),
    "E3g3-gates-projects-ruff": ("PASS",
        "2.6 project gates and ruff for the slice's twins (re-run)",
        "tools/check_projects.py --unit E3; ruff check .",
        "check_projects --unit E3: PASS. ruff check . : All checks passed. ruff format --check .: 553 files already formatted."),
    "E3g6-pytest": ("PASS",
        "2.5 relevant pytest over the lab and page tooling (re-run)",
        "tests/test_labs.py, test_run_labs.py, test_page_checks.py, test_curriculum.py, test_docs_figures.py, test_build_site.py",
        "pytest -q on those six files: all dots, exit 0 (ledgers/E3/scripts/E3-g-r10/pytest_relevant.out)."),
    "E3g6-verify-refs": ("PASS",
        "2.1 citations: registry integrity (re-run offline)",
        "tools/verify_refs.py --offline",
        "offline integrity: 560 entries, 0 problems. (The live Crossref run was not executed: references/ has no delta since 2d755599.)"),
    "E3g3-page-smoke": ("PASS",
        "2.5 / 2.9 page_smoke for L05..L08 (re-run alone, pages L05 L06 L07 L08)",
        "tools/page_smoke.py --unit E3 --pages L05 L06 L07 L08",
        "page_smoke modules/E/E3/L05.html, L06.html, L07.html, L08.html: PASS each; page_smoke E3: PASS (ledgers/E3/scripts/E3-g-r10/page_smoke_L05-L08.out)."),
    "E3g3-notation-collisions": ("PASS",
        "3 notation: local letters reused with another meaning inside the slice (re-run on the new L05 cards)",
        "cards.json E3-c184, E3-c185; L05.txt Definitions 1.1, 2.1, Assumptions A1 to A4",
        "E3-c184 uses beta, psi, c0, c1 with the meanings of A1 (beta), A2 (psi), Section 1 (c0, c1) and Proposition 2.2. E3-c185 uses c1 with the meaning of "
        "Section 1. No letter changes meaning. notation.json registers only T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q; none is used on the new cards."),
    "E3g3-notation-registry": ("PASS",
        "3 notation: registered symbols and macros (T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q; macros \\E, \\Prob, \\R) against the slice (re-run)",
        "notation/notation.json (unchanged since 2d755599); cards.json E3-c184, c185",
        "No registered symbol appears on the new cards; the new cards use only the lesson-local letters beta, psi, gamma, c0, c1 and CE1 defined in L05."),
}


def carry_evidence(old: str) -> str:
    return f"Carried from round 8 ({CARRY_FILES}) byte-identical since the previous pin {BASE[:8]}: " + old


rows = []
for r in r8["rows"]:
    rid = r["id"]
    if rid in OVERRIDE:
        status, check, location, evidence, *rest = OVERRIDE[rid]
        row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
        if status != "PASS":
            row["fix"] = rest[0]
    else:
        row = {"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
               "evidence": carry_evidence(r["evidence"])}
    rows.append(row)

missing = [k for k in OVERRIDE if k not in {r["id"] for r in r8["rows"]}]
assert not missing, f"override ids not in round-8 rows: {missing}"

new_ids = ["E3g-r10-c184-c185-new", "E3g-r10-c131-C-cards"]
# Added row for the new cards' own closed checks is not needed: all new cards are covered by the rows above.

frag = {
    "unit": "E3",
    "slice": "g",
    "round": 10,
    "verifier": "Haiku 5.5 independent verifier, E3-g round 10 (did not build E3)",
    "pin": PIN,
    "base": BASE + " (round-8 pin, last PASS fragment D-E3-g.round8.json; no round-9 fragment exists under ~/.fanout/frags)",
    "checkout": R,
    "scratch": R + "/ledgers/E3/scripts/E3-g-r10",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": None,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [
        "Round-8 pin 2d755599 is an ancestor of 47a36d8c. Delta for the slice: cards.json only (c131 changed; c184, c185 added); lessons and lab twins identical.",
        "cards.json also changed for E3-c004, c022, c050, c159, c180, c183, c186 (other slices, not graded here).",
    ],
    "notes": [
        "Round-9 fragment D-E3-g.round9.json is not present under /Users/billyribeiro/.fanout/frags/ (the newest is round8), so the baseline is the round-8 fragment (all 85 rows PASS at pin 2d755599).",
        "Slice g after the delta: L05 22 cards (20 + c184, c185), L06 19, L07 18, L08 28 = 87 cards.",
        "Lesson pages L05..L08 and their lab twins are byte-identical to 2d755599; their PASS rows are carried with the prefix. L05 lesson text was read in full this round (ledgers/E3/scripts/E3-g-r10/L05.txt); L06, L07, L08 text was not re-read because no byte of them changed, except that L07 Problem E2 and Lab 1 part C were re-read for the c131 check.",
        "Lab 1 of L05 run under python -I -W error: exit 0; the expected output block equals the run output line by line.",
        "Mutants: none. This slice is lessons and retrieval cards, not a project grader; lab twins are demonstrations (VERIFIER rulings).",
    ],
    "summary": None,
}

fails = [r for r in rows if r["status"] != "PASS"]
frag["verdict"] = "PASS" if not fails else "FAIL"
frag["summary"] = {
    "rows": len(rows),
    "pass": sum(1 for r in rows if r["status"] == "PASS"),
    "fail": len(fails),
    "carried_from_round_8": sum(1 for r in rows if r["evidence"].startswith("Carried from round 8")),
    "reverified_this_round": sum(1 for r in rows if not r["evidence"].startswith("Carried from round 8")),
    "mutants": 0,
    "mutants_killed": 0,
}
out = R + "/ledgers/E3/E3-g.json"
json.dump(frag, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("wrote", out, frag["verdict"], frag["summary"])
