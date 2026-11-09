# Builds ledgers/FC1/FC1-a.json (round 1 closing delta, slice a) from the base fragment and this round's fresh checks.
import json
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
BASE = pathlib.Path("/Users/billyribeiro/.fanout/frags/F1-FC1-a.round1.json")
base = json.loads(BASE.read_text(encoding="utf-8"))
O = "ledgers/FC1/scripts/FC1-a-r1/out"
CARRY_PREFIX = ("Carried from round 1 (base fragment F1-FC1-a.round1.json, pin 95f3f8cb; cited lines byte-identical "
                "since 95f3f8cb, see " + O + "/delta_slice_a_r1.diff): ")

FRESH = {
    "a-r1-gate-check-pages": f"Re-run at 2a805c83: tools/check_pages.py --unit FC1 -> 'check_pages FC1: PASS' EXIT=0 ({O}/check_pages_unit.out); --all EXIT=0, all 27 unit lines PASS, no FAIL ({O}/check_pages_all.out).",
    "a-r1-gate-check-dag": f"Re-run at 2a805c83: tools/check_dag.py --unit FC1 -> 'check_dag FC1: PASS' EXIT=0 ({O}/check_dag_unit.out); --all EXIT=0, all unit lines PASS ({O}/check_dag_all.out).",
    "a-r1-gate-check-projects": f"Re-run at 2a805c83 (tool gate only): tools/check_projects.py --unit FC1 -> 'check_projects FC1: PASS' EXIT=0 ({O}/check_projects_unit.out); --all EXIT=0, all unit lines PASS ({O}/check_projects_all.out).",
    "a-r1-gate-run-labs": f"Re-run at 2a805c83: tools/run_labs.py --unit FC1 -> 'run_labs FC1: PASS (8/8)' EXIT=0 ({O}/run_labs_fc1.out).",
    "a-r1-twins-isolated": f"Re-run at 2a805c83: python -I -W error on tests/labs/FC1/lab-FC1-L01-1.py, L02-1.py, L03-1.py each EXIT=0 with no traceback or warning ({O}/twin_L01.out, twin_L02.out, twin_L03.out; summary.txt).",
    "a-r1-page-smoke": f"Re-run at 2a805c83: tools/page_smoke.py --unit FC1 --pages index L01 L02 L03 -> 'page_smoke FC1: PASS' EXIT=0; index, L01 and L03 modules PASS ({O}/page_smoke_fc1.out).",
    "a-r1-ruff-mypy-twins": f"Re-run at 2a805c83: ruff check . -> 'All checks passed!' EXIT=0; ruff format --check . -> '555 files already formatted' EXIT=0; mypy --no-incremental -> 'Success: no issues found in 386 source files' EXIT=0 ({O}/ruff_check.out, ruff_format.out, mypy_nocache.out).",
    "a-r1-pytest-relevant": f"Re-run at 2a805c83: pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_page_smoke.py tests/test_refs.py tests/test_docs_figures.py EXIT=0, every line dots only, no failure ({O}/pytest_slice.out).",
    "a-r1-verify-refs-offline": f"Re-run at 2a805c83: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' EXIT=0 ({O}/verify_refs_offline.out). references/ unchanged in the delta (git diff --stat 95f3f8cb..HEAD).",
    "a-r1-notation-scan": f"Changed math in the delta is only two sentences: L01 line 73 (Assumption 2.0: D_t, X_t, \\(\\ell_t\\), S_n, with 'defined in Section 2' removed) and L01 line 320 (\\(\\rho\\)). The added math segments are the same symbols as the removed ones, so no new symbol enters the slice ({O}/delta_slice_a_r1.diff). Local letters (S, D, X, \\(\\ell\\)) are defined in each lesson where used per notation/notation.json 'about'; no macro in notation.json has these symbols. The base scan of the rest of the slice's math is unchanged.",
    "a-r1-process-banned-scan": f"Added lines of the delta (34-line diff, {O}/delta_slice_a_r1.diff) scanned for process words (round, verif, fixer, ruling, audit, builder, architect, TODO, TBD, we, our, I) and external markup (http, img, svg, iframe, href): zero hits.",
    "a-r1-no-external-no-figures": f"Added lines of the delta scanned for http, <img, <svg, <iframe, href: zero hits ({O}/delta_slice_a_r1.diff). Slice has no figures.",
    "a-r1-hub-structure": f"index.html: the delta changes only line 137 (lessons intro: 'follow one trade' -> 'follow the path of a trade'); lines 1-176 otherwise byte-identical. Line 137 re-read: five lessons, 10 h each, match index lines 139-143 (L01-L05 '10 h'); the path names L01 bank, L02 instrument, L03 dealer, L04 order book, L05 settlement, matching the lesson titles. check_pages FC1 PASS ({O}/check_pages_unit.out).",
    "a-r1-define-before-use": f"Changed sentences re-read: L01 line 51 (no new term), L01 line 73 (S_n now defined inline in Assumption 2.0; first use is in that definition, Section 2 line 86 repeats it), L02 line 50 ('two kinds of trade' = Definition 1.1 exchange-traded/OTC, L02 line 57), L03 line 51 (Definition 1.2, Definition 2.1 and Proposition 2.3 cited by number; 'equilibrium ask (defined in Section 3)' is a flagged forward reference: Section 3 defines the equilibrium profile at L03 line 140), index line 137. No term used before its definition without a flagged forward pointer.",
    "a-r1-scope-words": f"Scope words in the changed sentences: 'Every lesson' (index line 137) checked: all five lessons have data-run labs, a problems section and a quiz (grep counts per lesson L01-L05: problems section 1, quiz 2 hits, data-run lab 2 hits); 'each share' (L03 line 51) matches Proposition 2.3's hV term; 'no claim about real banks' (L01 line 51) matches Section 5 (L01 line 318-319). Other scope words unchanged ({O}/delta_slice_a_r1.diff).",
    "a-r1-l01-misconceptions-canon": f"Canon bullet 3 (L01 line 320) re-derived: limit d/rho at rho = 1/10 is 10d and at rho = 1/2 is 2d (Proposition 3.1; {O}/c016_check_r1.out prints 1/rho = 10 and 2). Bullet 1 (line 318) claim re-derived from Proposition 3.5 limit d/(1-phi(1-rho)) < d/rho when phi < 1 and rho < 1 (L01 line 137). Misconceptions 328-339 unchanged and checked against L01 Proposition 3.1 and Section 2.",
    "a-r1-l01-cards-lab-T": f"Current cards.json (c125 is no longer in the file; the base row cited it, but the base notes say it was removed before 95f3f8cb, so the base citation was stale): FC1-c014 (C) 'Lab 1, Part A prints True' matches twin output line 'partial sums ... 0 to 10: True'; FC1-c092 (C) '181790 cents ... against 686189' matches twin Part C lines 'total deposits after stage 10 ... 181790' and '686189'; FC1-c093 (C) losses 50/100/150 leave equity 50, 0, -50 and sign test True/True/False, matching twin Part D. FC1-c015 and FC1-c103 are T cards with a 'Lab 1, Part A/B' corroboration clause, accepted in round 5 and noted as advisory below ({O}/cards_scan_r1.out).",
    "a-r1-l01-cards-other": f"FAIL re-verified and now PASS. Base FAIL: FC1-c016 back said 'No.' at rho = 1, which the card's own hypothesis 0 < rho <= 1 admits. Current back: 'No, unless rho = 1 ... When rho = 1 it equals 1 = 1/rho at every stage (Proposition 3.1; misconception 2).' Exact-arithmetic check at rho in {1/10, 1/2, 9/10, 99/100, 1} for n = 0..10: S_n/d equals the closed form, is smaller than 1/rho when rho < 1, and equals 1 = 1/rho when rho = 1 ({O}/c016_check_r1.out: 'c016 claims hold on tested grid: True'). Proposition 3.1 proof (L01 lines 110-112) covers rho = 1. Misconception 2 (L01 line 334) says the same for rho < 1. Near-duplicate scan: highest word-Jaccard with another card 0.366 (FC1-c007, a closed-form question), no duplicate ({O}/c016_neardup_r1.out). The other L01 cards are byte-identical (git diff 95f3f8cb..2a805c83, cards.json hunks at c016 and c056 only).",
    "a-r1-l01-why-it-matters": f"Changed line 51 re-read: 'The lesson makes no claim about real banks.' Consistent with Definition 2.1 (L01 line 81: 'Section 5 says what the lesson does not claim about real banks'), Section 5 (line 319: 'No source for real bank practice is cited') and the interpretation paragraph (line 310). Sentences about defining an intermediary and the equity loss match Definition 1.1 and Proposition 4.1.",
    "a-r1-l02-why-it-matters": f"Changed line 50 re-read: 'This lesson defines the two kinds of trade' matches Definition 1.1 (L02 line 57-59: exchange-traded and over-the-counter trade, the two kinds). The 'three-axis taxonomy' and 'counting rule (Proposition 2.5)' claims are unchanged text (lesson line 50 same as base otherwise).",
    "a-r1-l03-why-it-matters": f"Changed line 51 re-derived: (1) 'a dealer earns half the quoted spread on each share it trades, against that trade's mid': Proposition 2.3 first term hV with h = s/2 and p_t - m_t = sigma h (L03 Definition 2.1 at line 87; Definition 1.2 at line 61). (2) 'the mid can move between trades': A1 (L03 line 80). (3) 'These are the two terms of Proposition 2.3 in Section 2': spread capture hV and mid-move term. (4) 'equilibrium ask (defined in Section 3) can sit 0, 1 or 2 cents above cost': Proposition 3.2 equilibria (c,c),(c+1,c+1),(c+2,c+2) (L03 Proposition 3.2 at line 149 and its proof). (5) 'Lab 1 checks both identities in whole cents and enumerates the tick-game grid': lab-FC1-L03-1.py module docstring 'Part A and Part B check the identity of Proposition 2.3 and Corollary 2.4' and Part C grid; twin output shows 'mark-to-mid P&L equals spread capture plus mid-move term: True' and the grid pairs. Wording note only: the sentence before says 'proves an identity' (singular), so 'both identities' has no antecedent in the same sentence; not a ruling-26 kind, recorded as a note.",
    "a-r1-cards-grade-convention": f"Current cards.json: L01 34, L02 29, L03 41 (104 cards; {O}/cards_scan_r1.out). Only one L01-L03 card changed in this delta, FC1-c016 (grade T, Proposition 3.1 cited), re-verified above; the other 103 cards are byte-identical (cards.json hunks in the delta: c016 and c056 only).",
    "a-r1-cards-dup-gaps": f"Re-scan at 2a805c83: 169 cards, 169 unique ids, no duplicate ids, no duplicate fronts ({O}/cards_scan_r1.out).",
    "a-r2-lab-mutants": f"Standing lab-claim mutants re-run at 2a805c83 under python -I -W error: 5 of 5 KILLED ({O}/mutants_r1.out; diffs in {O}/mut_*.stdout vs twin_base_*.stdout). Mutants rebuilt as one-line edits of the twins by ledgers/FC1/scripts/FC1-a-r1/make_standing_mutants_r1.py (ruling 37: no new mutants).",
    "a-r2-cards-near-dup-scan": f"Near-duplicate scan for the changed card FC1-c016 against all other cards: highest word-Jaccard 0.366 (FC1-c007), no near-duplicate ({O}/c016_neardup_r1.out). Full-deck scan at 2a805c83 has no duplicate ids or fronts ({O}/cards_scan_r1.out).",
    "a-r2-numbers-recompute": f"Numbers in the delta: 'ten times' and 'twice the initial deposit' (L01 line 320) recomputed exactly: d/rho = 10d at rho = 1/10 and 2d at rho = 1/2 ({O}/c016_check_r1.out, printed 1/rho = 10 and 2). Other numbers in the slice are byte-identical to the base and were recomputed there (ledgers/FC1/scripts/FC1-a-r4/numbers_fc1a_r4.py, present in this checkout).",
    "a-r3-gates-full": f"Superseded by this round's full slice gate run at 2a805c83 (all commands EXIT=0; {O}/summary.txt, last line DONE).",
    "a-r1-hub-hours": None,
}
CARRY_NOTE = {}
rows = []
base_ids = [r["id"] for r in base["rows"]]
for r in base["rows"]:
    rid = r["id"]
    if rid in FRESH and FRESH[rid]:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": FRESH[rid]})
    elif rid == "a-r1-l01-cards-other":
        raise SystemExit("unreachable")
    else:
        if r["status"] != "PASS":
            raise SystemExit(f"non-PASS base row not re-verified: {rid}")
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": CARRY_PREFIX + r["evidence"]})
assert [r["id"] for r in rows] == base_ids, "row ids must be kept in order"
muts = []
for m in base["mutants"]:
    name = m["id"]
    muts.append({"id": name, "description": m["description"],
                 "killed_by": f"KILLED in the round-1 closing run at 2a805c83 (ledgers/FC1/scripts/FC1-a-r1/out/mutants_r1.out; mut_{name}__*.stdout differs from twin_base_*.stdout): the printed claim flips. " + m["killed_by"].split(":", 1)[-1].strip()})
frag = {
    "unit": "FC1",
    "slice": "FC1-a",
    "round": 1,
    "verifier": "Claude Haiku 5.5 independent verifier, FC1-a closing delta (ruling 30), round 1 of this verification; did not build FC1; read verifier-rules.md",
    "pin": "2a805c831410ab77c38c227f7e121e8537193ce9",
    "base": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672 (base fragment /Users/billyribeiro/.fanout/frags/F1-FC1-a.round1.json, FAIL on a-r1-l01-cards-other)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyG1-FC1-a",
    "scratch": "ledgers/FC1/scripts/FC1-a-r1/ (gates_r1.sh, out/, make_standing_mutants_r1.py, run_standing_r1.sh, cards_scan_r1.py, c016_check_r1.py, c016_neardup_r1.py, build_fragment_r1.py); mutants ledgers/FC1/mutants/fc1a-r1/",
    "verified_at": "2026-11-09T17:07:15+00:00",
    "verdict": "PASS",
    "rows": rows,
    "mutants": muts,
    "registry_flags": base["registry_flags"],
    "freshness_flags": base["freshness_flags"],
    "notes": [
        "Delta scope (ruling 30, 95f3f8cb..2a805c83, FC1 slice-a paths): L01.html lines 51, 73, 320; L02.html line 50; L03.html line 51; index.html line 137; cards.json FC1-c016 (slice a) and FC1-c056 (L04, other slice, not verified here). project.html, twins, references, curriculum and tools are unchanged in the delta.",
        "The base's one FAIL (FC1-c016, rho = 1 case) is fixed: the back now says 'No, unless rho = 1' and states the rho = 1 equality. Re-verified from scratch; no ruling-26 defect remains, so no further delta round is needed.",
        "Base row a-r1-l01-cards-lab-T cited FC1-c125, which the base's own notes say was removed before 95f3f8cb; this round re-verifies that row against the current cards (c014, c092, c093).",
        "Advisory (no row, as in the base): FC1-c103 (T) ends with 'Lab 1, Part B prints True', and FC1-c015 (T) carries 'Lab 1, Part A' as a corroboration. A stricter reading would grade the lab clause C. Not a ruling-26 kind in this round; left as the base left it.",
        "Advisory (no row): the L03 why-it-matters sentence 'Lab 1 checks both identities' follows 'proves an identity' (singular); the lab does check two identities (Proposition 2.3 and Corollary 2.4), so the claim is supported, only the antecedent is loose. Wording, not a ruling-26 kind.",
        "Ruling 37: no new mutants written. The five standing lab-claim mutants were rebuilt from the base's descriptions as one-line edits of the twins (make_standing_mutants_r1.py); all five are KILLED.",
        "Not run: run_graders.py and mutate_graders.py (no FC1-a grader); render_curriculum.py (curriculum unchanged in this delta); Chromium screenshots (no figures in the slice). Pre-existing ledgers/FC1/FC1-a.json in this checkout (an older round) is overwritten by this fragment, as the task directs; the base's gates_r1.sh and output files at the same scripts path were overwritten in this checkout only.",
    ],
    "summary": "FC1-a closing delta (round 1 of this verification) at 2a805c83: 80 rows (all base ids kept), 80 PASS, 0 FAIL, 0 UNVERIFIABLE. The base FAIL (FC1-c016 rho = 1 answer) is fixed and re-verified. All gates re-run EXIT=0 at 2a805c83; standing lab-claim mutants 5 of 5 KILLED. Verdict PASS.",
}
out = ROOT / "ledgers/FC1/FC1-a.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "mutants", len(muts))
