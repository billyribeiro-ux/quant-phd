"""Builds ledgers/FC2/FC2-d.json (round 11) from the round-10 fragment and this round's evidence.

Every round-10 row id is kept. A row is either re-verified this round (fresh evidence, citing the scripts in this
folder) or carried: its subject is byte-identical since the round-10 pin 47a36d8 and the carry prefix names it.
Usage: python3 -I build_fragment_r11.py <repo_root> <prev_fragment.json> <mutate_out> <out.json>
"""
import datetime
import json
import re
import sys

root, prev_path, mutate_out, out_path = sys.argv[1:5]
prev = json.load(open(prev_path, encoding="utf-8"))
S = "ledgers/FC2/scripts/FC2-d-r11/"
PIN = "ccaeeaf44bea94b37d912ec1da3c660bb2c55d87"
BASE = "47a36d8c78633793ccc762ae19dcd5e19b780d19"
GRADER = "course/modules/FC/FC2/grader/ (starter.py, reference.py, instance.py, test_project.py)"
LESSONS = "course/modules/FC/FC2/L01.html to L08.html and index.html"
PROJ_NO289 = "course/modules/FC/FC2/project.html (its only hunk since {} is at line 289; lines {} are byte-identical)"


def card(cid):
    return (f"course/modules/FC/FC2/cards.json object FC2-{cid} (object-equal to {BASE[:7]}, cards_delta_r11.out) "
            "and its lesson file (byte-identical)")


CARRY_FILES = {
    "fc2d-r2-grader-messages": GRADER,
    "fc2d-r2-grader-named-conditions-only": GRADER + " and project.html lines 309-316 (outside the hunk)",
    "fc2d-r2-grader-over-constraint-trade-verb": GRADER,
    "fc2d-r2-grader-over-constraint-case": GRADER,
    "fc2d-r5-explanation-direction-untested": GRADER,
    "fc2d-r7-grader-convexity-docstring": GRADER,
    "fc2d-r9-grader-weak-assertion": GRADER,
    "fc2d-r2-autograder-panel-claims": "course/modules/FC/FC2/project.html lines 285, 360-368 and 672 (outside the hunk)",
    "fc2d-r2-hub-placement-claim": "course/modules/FC/FC2/project.html line 42 and course/modules/FC/FC2/index.html",
    "fc2d-r3-footer-no-upload": "course/modules/FC/FC2/project.html lines 285, 360 and 672 (outside the hunk)",
    "fc2d-r3-exemplar-scores-match-text": "course/modules/FC/FC2/project.html lines 520-635 (outside the hunk)",
    "fc2d-r5-page-hunk-lab1-hypothesis": "course/modules/FC/FC2/project.html line 55 (outside the hunk)",
    "fc2d-r10-page-hunk-lab1-hypothesis": "course/modules/FC/FC2/project.html line 55 (outside the hunk)",
    "fc2d-r10-page-hunk-P6-leg": "course/modules/FC/FC2/project.html line 333 (outside the hunk)",
    "fc2d-r5-page-hunk-error-conditions": "course/modules/FC/FC2/project.html lines 309-316 (outside the hunk)",
    "fc2d-r6-page-conventions-definitions": "course/modules/FC/FC2/project.html lines 325-336 (outside the hunk)",
    "fc2d-r6-page-line321-anchor": "course/modules/FC/FC2/project.html lines 321 and 517 (outside the hunk)",
    "fc2d-r7-page-rung1-line44": "course/modules/FC/FC2/project.html line 44 (outside the hunk)",
    "fc2d-r7-page-brief-line490": "course/modules/FC/FC2/project.html line 490 (outside the hunk)",
    "fc2d-r7-exemplar-B-C3-annotation-line543": "course/modules/FC/FC2/project.html line 543 (outside the hunk)",
    "fc2d-r7-exemplar-A-C4-annotation-line618": "course/modules/FC/FC2/project.html line 618 (outside the hunk)",
    "fc2d-r8-exemplar-level-labels": "course/modules/FC/FC2/project.html lines 351, 520 and 584 (outside the hunk)",
    "fc2d-r9-tie-rule-prose": "course/modules/FC/FC2/project.html lines 59-63, 170-173 and 308 (outside the hunk)",
    "fc2d-r2-cards-refs-numbers": "every course/modules/FC/FC2/cards.json object except FC2-c007, c016, c047, c082, c124 and c164-c167 (object-equal to " + BASE[:7] + ", cards_delta_r11.out) and the lesson files",
    "fc2d-r2-cards-lab-numbers": "every lab-basis card object except FC2-c047 and FC2-c045 (verified fresh), and tests/labs/FC2 (byte-identical)",
    "fc2d-r4-cards-sample": "the sampled card objects (object-equal to " + BASE[:7] + ") and the lesson files",
    "fc2d-r7-card-c156": "no subject: FC2-c156 is absent from cards.json at both pins",
    "fc2d-r7-card-c157": "no subject: FC2-c157 is absent from cards.json at both pins",
    "fc2d-r6-card-c073": card("c073"),
}
for cid in ["c010", "c020", "c041", "c051", "c061", "c071", "c092", "c102", "c112", "c142", "c093", "c149", "c150",
            "c152", "c153", "c151", "c005", "c055", "c154", "c072", "c103", "c155", "c014", "c021", "c037", "c046",
            "c059", "c060", "c068", "c069", "c076", "c079", "c080", "c081", "c094", "c095", "c114", "c125", "c128",
            "c137", "c145", "c113", "c132", "c120", "c121", "c122", "c123", "c025", "c026", "c028", "c030", "c044",
            "c089", "c104", "c110", "c111", "c117", "c143", "c158", "c159", "c066", "c084", "c160", "c161", "c162",
            "c163", "c122"]:
    CARRY_FILES.setdefault(f"fc2d-r2-card-{cid}", card(cid))
    CARRY_FILES.setdefault(f"fc2d-r4-card-{cid}", card(cid))
    CARRY_FILES.setdefault(f"fc2d-r5-card-{cid}", card(cid))
    CARRY_FILES.setdefault(f"fc2d-r6-card-{cid}", card(cid))
    CARRY_FILES.setdefault(f"fc2d-r7-card-{cid}", card(cid))
    CARRY_FILES.setdefault(f"fc2d-r8-card-{cid}", card(cid))
    CARRY_FILES.setdefault(f"fc2d-r9-card-{cid}", card(cid))
    CARRY_FILES.setdefault(f"fc2d-r10-card-{cid}", card(cid))
CARRY_FILES["fc2d-r8-card-c110-c111-c117"] = card("c110") + "; " + card("c111") + "; " + card("c117")
CARRY_FILES["fc2d-r8-card-c143"] = card("c143")
CARRY_FILES["fc2d-r2-card-c120"] = card("c120")
CARRY_FILES["fc2d-r2-card-c030"] = card("c030")

# Rows re-verified this round, with fresh evidence.
FRESH = {
    "fc2d-r2-gate-mutate": ("tools/mutate_graders.py --unit FC2 --seeds 0-9", "PASS",
        f"{S}mutate_fc2_r11_all.out: 'mutate_graders FC2: PASS (91/91 killed)', rc=0. Re-run on this pin with the 4 new "
        "round-11 mutants (a11_a..a11_d) added to ledgers/FC2/mutants/."),
    "fc2d-r2-gate-run-graders": ("tools/run_graders.py --unit FC2 --seeds 0-49", "PASS",
        f"{S}run_graders.out: 'run_graders FC2: PASS (reference 50/50 seeds, slowest 0.8 s)', rc=0."),
    "fc2d-r2-gate-check-projects": ("tools/check_projects.py --unit FC2", "PASS",
        f"{S}check_projects_fc2.out: 'check_projects FC2: PASS', rc=0."),
    "fc2d-r2-gate-check-dag": ("tools/check_dag.py --unit FC2", "PASS",
        f"{S}check_dag_fc2.out: 'check_dag FC2: PASS', rc=0."),
    "fc2d-r2-gate-check-pages": ("tools/check_pages.py --unit FC2", "PASS",
        f"{S}check_pages_fc2.out: 'check_pages FC2: PASS', rc=0."),
    "fc2d-r2-gate-run-labs": ("tools/run_labs.py --unit FC2", "PASS",
        f"{S}run_labs_fc2.out: 'run_labs FC2: PASS (11/11)', rc=0."),
    "fc2d-r2-lab-twins-isolated": ("project twins alone under python -I -W error", "PASS",
        f"{S}page_vs_twin_r11.out and {S}expected_vs_run_r11.out (scripts page_vs_twin_r10.py and expected_vs_run_r10.py "
        "copied into the r11 folder): twins of labs 1, 2 and 3 run with '.venv/bin/python -I -W error' from /tmp, rc=0, "
        "stderr_bytes=0 each."),
    "fc2d-r2-lab-page-equals-twin": ("page code equals twin; expected block equals output", "PASS",
        f"{S}page_vs_twin_r11.out: lab 1 and lab 3 page code, 0 lines differ from the twin; lab 2 differs on lines 58, 60 "
        f"and 73 only, each a page blank '___' (project.html lines 226, 228, 241). {S}expected_vs_run_r11.out: "
        "expected_equals_output=True for labs 1, 2, 3 (16, 16, 17 lines)."),
    "fc2d-r2-gate-page-smoke": ("tools/page_smoke.py --unit FC2 --pages project", "PASS",
        f"{S}page_smoke_project.out: 'page_smoke modules/FC/FC2/project.html: PASS', 'in-browser grader: All 94 tests "
        "pass', page_smoke FC2: PASS, rc=0."),
    "fc2d-r2-gate-ruff-mypy": ("ruff check, ruff format --check, mypy --no-incremental", "PASS",
        f"{S}ruff_check.out 'All checks passed!' rc=0; {S}ruff_format.out '15 files already formatted' rc=0; "
        f"{S}mypy.out 'Success: no issues found in 385 source files' rc=0."),
    "fc2d-r2-gate-pytest-fc2": ("relevant pytest (FC2 filter)", "PASS",
        f"{S}pytest_fc2.out: pytest -q tests/test_curriculum.py tests/test_labs.py -k FC2, rc=0."),
    "fc2d-r2-gate-verify-refs": ("verify_refs --offline and --unit FC2 (live)", "PASS",
        f"{S}verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', rc=0. {S}verify_refs_unit_FC2.out: "
        "'live re-verification of FC2: 3 of 560 entries, 0 problems', rc=0. references.json changed only in BK1, BK4, "
        "E9 and LX1 used_by lists (git diff 47a36d8..ccaeeaf); the FC2 entries are unchanged."),
    "fc2d-r2-collect-count": ("collected checks equal the page count, every seed 0..49", "PASS",
        f"{S}collect_count_r11.out: 'collected 94 for 50 seeds', rc=0 (collect_count_r10.py copied into the r11 folder, "
        "run with -I and an absolute repo root). project.html line 320 states 94."),
    "fc2d-r2-numbers-lab1": ("project.html line 55 and Lab 1 (lines 147-163)", "PASS",
        f"{S}numbers_r11.out (numbers_r10.py, exact Fractions): cost 45; parity gaps 0, 120, 0, 0, -20, 0 at strikes "
        "9000..11500; nets -45, 75, -45, -45, -25, -45; chord-less-call 50, 100, -75, 75; kept 2 (strikes 9500 parity, "
        "10500 convexity). Hand recomputation agrees with the printed expected block and the line 163 interpretation."),
    "fc2d-r2-numbers-lab3": ("project.html Lab 3 (lines 377-486)", "PASS",
        f"{S}numbers_r11.out: gaps 0, -60, 0, 0, 226, 540 at 4000..7000; nets; chord-less-call 35, 470/3, -188/3 "
        "(gross 63, net 3), 59; kept 3. Hand recomputation (Kdf = 4275, 6175, 6650) agrees with lines 475-485 and 486 "
        "(188/3 = 62.67, rounded to 63)."),
    "fc2d-r2-numbers-exemplars": ("project.html Exemplar B passage (line 538) and Exemplar A (lines 590, 602)", "PASS",
        f"{S}numbers_r11.out: discounted strike 6500 -> 6175, gap 226; 7000 -> 6650, gap 540; chord at 6000 = 802/3, "
        "less call -188/3. Exemplar A quotes only about-values that match 226, 540 and 63."),
    "fc2d-r2-hours": ("project.html lines 339-356 and hub index.html line 41", "PASS",
        "Time budget rows 2+3+5+9+3+5+3 = 30 (project.html line 352 states 30); data-hours-project=30 (line 33); the hub "
        "states '60 h lessons · 30 h project' (index.html line 41); lesson eyebrows L01..L08 read 6, 8, 9, 7, 8, 8, 8, 6 "
        "= 60, and 60 + 30 = 90. The estimates are the verifier's own; none is more than 30% from its declared hours."),
    "fc2d-r2-banned-phrases": ("project.html and cards.json against BUILDER_RULES 1.3-1.4 and the process-word list", "PASS",
        "A grep of project.html and cards.json for TODO, TBD, lorem, an ellipsis, 'for brevity', 'details omitted', 'beyond "
        "the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'experts agree', "
        "'it is well known', 'obviously', 'clearly' gives no hit; a word scan of project.html text for round, builder, "
        "verifier, agent, ledger, fragment, pin, slice, checkout, reviewer, we, I gives no hit. Re-run on the line-289 hunk: "
        "no banned phrase."),
    "fc2d-r2-notation": ("project.html and cards.json against notation/notation.json (8 registered symbols)", "PASS",
        "notation/notation.json lists T, Phi, gamma_3, gamma_4, R*, R^{e*}, R_f, Q. project.html uses none of them (no "
        "Phi, gamma, R_f, Q, T; C, P, S, K, df, D are unregistered and used with one meaning). cards.json uses Phi (the "
        "standard normal CDF, M4 meaning), R_f (gross one-period return, AP1 meaning) and Q (risk-neutral measure, AP1 "
        "meaning); no collision. The line-289 sentence introduces no symbol."),
    "fc2d-r2-dag": ("tools/check_dag.py --unit FC2 and concept links on project.html", "PASS",
        f"{S}check_dag_fc2.out: 'check_dag FC2: PASS', rc=0. project.html links arbitrage-opportunity (L01), put-call-parity "
        "and option-arbitrage-bounds (L05), all defined inside FC2 (L01 and L05 are FC2 lessons), so no concept is used "
        "before definition."),
    "fc2d-r2-reading-keys": ("project.html lines 652-660 and the reading keys", "PASS",
        "Keys hull2021options, stoll1969relationship, cox1979option (project.html lines 655-657): their records are unchanged "
        "(references.json diff 47a36d8..ccaeeaf does not touch them). Line 659 cites Theorem 1.2 (L05 line 63, put-call "
        "parity) and Theorem 3.2 (L05 line 115, convexity in strike), both present and graded T in L05.html; line 659 "
        "says the listed reading assigns no chapter, which is consistent with the three entries having no locator."),
    "fc2d-r2-spec-questions": ("project.html lines 278-317 (Rung 3 spec)", "PASS",
        "Re-read in full this round, including the reworded df_ppm bullet (line 289). A competent student needs no "
        "question about the three signatures, the record keys, the tie rules (lines 308), the named conditions (lines "
        "309-316), the cost model (P6, line 333) or the chord (line 336). One inference, not a blocking question: for a "
        "convexity finding strike_cents is the middle strike; Lab 1's expected output (line 162: 'convexity at strike "
        "10500') and the grader (test_convexity_finding_..., line 792) show it, though the spec sentence does not name it."),
    "fc2d-r2-scope-curriculum-brief": ("Rung 3 matches the curriculum scope (curriculum/02 line 428 vs project.html line 285)", "PASS",
        "Re-verified on ccaeeaf. curriculum/02-economics-finance-core.yaml line 428 now reads 'Given a SIMULATED option-chain "
        "snapshot' (diff 47a36d8..ccaeeaf). curriculum/curriculum.json line 7797 matches. "
        f"{S}render_curriculum.out and {S}curriculum_diff.out: rendering reproduces CURRICULUM.md and curriculum.json "
        f"byte-identically (git diff --exit-code rc=0). {S}build_site_check.out: site data current. program.json line 1910 and "
        "CURRICULUM.md line 441 carry the same brief. project.html line 285: 'No market data is embedded ... every chain on "
        "this page and in the autograder is a simulation, labelled SIMULATED'; tools/data_sources.yaml lists no option-quote "
        "source."),
    "fc2d-r2-rubric-C2-level2": ("project.html rubric row C2 (lines 508-513)", "PASS",
        "Read this round. Level 2 'States the cost model, but does not say, for each finding, whether it survives the cost, "
        "or reports gross amounts without the cost' names observable elements; level 4 'states ... the net amount after the "
        "cost and the gap between the net and zero' is observable."),
    "fc2d-r2-rubric-calibration": ("project.html exemplars A and B (lines 517-635) against the rubric (lines 502-515)", "PASS",
        "Blind scoring from the rubric descriptors and the passages, before reading the data-scores: B = 4, 4, 3, 3, 3 and A = "
        "2, 1, 2, 2, 1 (C1..C5), both within one level of data-scores (lines 520, 584) on every criterion."),
    "fc2d-r2-starter-suite-fails": ("grader/starter.py with test_project.py", "PASS",
        f"{S}starter_suite.out: starter.py copied as scanner.py, pytest with QF_SEED=0 --assert=plain -W error: '86 failed, "
        "8 passed', so the suite fails on the starter (NotImplementedError)."),
    "fc2d-r2-instances": ("grader/instance.py, 20 seeds", "PASS",
        f"{S}instances_r11.py and {S}instances_r11.out: seeds 0, 3, 7, ..., 71, 97 (20 seeds) are valid: spot 8000..20000, "
        "df 930000..999000, fee 0..40, half-spread 1..150, six increasing strikes, every quote within the Theorem 2.2 bounds "
        "to half a cent, no half-cent parity gap. Kinds: parity, convexity and none; 20 distinct spots, 20 distinct df, 13 "
        "distinct planted amounts."),
    "fc2d-r2-alternatives-pass": ("five-plus alternative correct scanners, seeds 0..49 (alternatives 1-14)", "PASS",
        f"{S}alts_r11.out (run_alts_r11.py): alt1..alt14 each 50/50 seeds pass the suite. alt13 (divided-difference convexity) "
        "and alt14 (net rounded once) were written this round. The correct alternative alt15 (shared empty result) passes "
        "28/50 seeds and fails 22: see fc2d-r11-grader-identity-over-constraint."),
    "fc2d-r2-mut-r7-docstrings": ("ledgers/FC2/mutants/*.py docstring first lines", "PASS",
        f"{S}mutate_fc2_r11_all.out prints the first docstring line of all 91 mutants (KILLED lines); each first line "
        "describes the error."),
    "fc2d-r2-mut-new-killed": ("round-2 mutants v07..v10", "PASS",
        f"{S}mutate_fc2_r11_all.out: KILLED v07 (seed 0, test_convexity_matches_oracle_on_an_uneven_grid), v08, v09, v10."),
    "fc2d-r2-mut-r5d-resolved": ("round-1 survivor r5_d (historical)", "PASS",
        "No r5_d file exists in ledgers/FC2/mutants/ (ls count 0), and the 91-mutant run has no SURVIVED line. The "
        "historical survivor is not in the set."),
    "fc2d-r2-mut-equivalents": ("the 91 mutants against the reference", "PASS",
        f"{S}mutate_fc2_r11_all.out: 91/91 KILLED on seeds 0-9. A killed mutant is distinguishable from the reference, so "
        "no listed mutant is equivalent."),
    "fc2d-r2-cards-full-scan": ("course/modules/FC/FC2/cards.json, all 163 cards", "PASS",
        f"{S}cards_scan_r11.py / cards_scan_r11.out: 163 cards, 163 unique ids, no duplicate front or back, every lesson in L01..L08, "
        "grades in {T, C, None}. 14 near-duplicate pairs (front or back ratio >= 0.75) reviewed: each pair asks distinct "
        "facts (for example c160/c161/c162 are Theorem 2.2 parts (b), (c), (d); c124 and c167 ask the step and the stop of "
        "Definition 3.1; c042 is the general par-rate formula, c045 the Lab 3 number)."),
    "fc2d-r4-cards-sample": ("sampled cards plus the changed cards", "PASS",
        "Carried from round 10 (sampled unchanged card objects byte-identical since 47a36d8, by cards_delta_r11.out): the "
        "changed cards (FC2-c007, c016, c047, c082, c124) and the new cards (FC2-c164..c167) are verified in their own "
        "fc2d-r11-card-* and fc2d-r2-card-c082, fc2d-r4-card-c124, fc2d-r7-card-c007 rows."),
    "fc2d-r2-card-c082": ("cards.json FC2-c082 (line 569-570 of the file) against L06 Definition 1.2 (line 64)", "PASS",
        "Re-verified on the changed text. Front 'What are the stock's possible values in the one-period binomial model, and "
        "what does A6 require?'; back 'The stock is worth S_0 today and uS_0 or dS_0 ... A6 requires 0 < d < R_f < u "
        "(Definition 1.2).' L06.html line 64 gives S_0 > 0, uS_0 or dS_0, and 'Assumption A6 is 0 < d < R_f < u'. Correct."),
    "fc2d-r4-card-c124": ("cards.json FC2-c124 against L08 Definition 3.1 (line 110)", "PASS",
        "Re-verified on the changed text. Back 'It tests the midpoint m against C* and keeps the half that still brackets C* "
        "(Definition 3.1).' L08.html line 110: 'set m = (sigma_lo + sigma_hi)/2; if C(m) < C*, set sigma_lo = m, and "
        "otherwise set sigma_hi = m.' Correct; the stop rule moved to FC2-c167."),
    "fc2d-r7-card-c007": ("cards.json FC2-c007 against L01 (Proposition 3.2 and Remark 3.3, line 123-124)", "PASS",
        "Re-verified on the changed text. Back 'Not claimed. Proposition 3.2 runs one way, and Remark 3.3 states that the "
        "converse is not claimed.' L01.html line 124: 'Proposition 3.2 runs one way. This lesson does not claim that a market "
        "without arbitrage has strictly positive state prices.' Correct; the uniqueness sentence moved to FC2-c164."),
    "fc2d-r7-card-c156": ("cards.json FC2-c156 (retired)", "PASS",
        "Carried from round 10 (historical row; no subject): FC2-c156 is absent from cards.json at 47a36d8 and at ccaeeaf "
        "(removed in commit 2d755599). It is not a live claim, and the ledger asserts nothing about the card. The verifier "
        "flags the retired row to the orchestrator in the notes."),
    "fc2d-r7-card-c157": ("cards.json FC2-c157 (retired)", "PASS",
        "Carried from round 10 (historical row; no subject): FC2-c157 is absent from cards.json at 47a36d8 and at ccaeeaf "
        "(removed in commit 2d755599). It is not a live claim. Flagged in the notes."),
    "fc2d-r3-scope-changed-hunks": ("every hunk changed since 47a36d8 in the slice", "PASS",
        f"git diff 47a36d8 ccaeeaf: course/modules/FC/FC2/project.html has one hunk (line 289, df_ppm bullet); cards.json has "
        "five changed objects (c007, c016, c047, c082, c124) and four added objects (c164..c167); the grader, tests/labs/FC2 "
        "and L01..L08 and index.html are empty in the diff. Outside the slice: curriculum yaml line 428 and curriculum.json "
        "line 7797 (brief), references.json used_by entries (BK1, BK4, E9, LX1), tests/labs of other units, and the "
        "round-10 z10 mutants and alts scripts."),
    "fc2d-r7-cards-delta-read": ("cards.json delta since 47a36d8", "PASS",
        f"{S}cards_delta_r11.out: changed ['FC2-c007','FC2-c016','FC2-c047','FC2-c082','FC2-c124'], added ['FC2-c164'..'FC2-c167'], "
        "removed []. Every changed field and every added object was read in full and verified in its own row."),
    "fc2d-r9-cards-changed-set-coverage": ("changed and added cards since 47a36d8", "PASS",
        "Covered: FC2-c007 (fc2d-r7-card-c007), c016 (fc2d-r11-card-c016), c047 (fc2d-r11-card-c047), c082 "
        "(fc2d-r2-card-c082), c124 (fc2d-r4-card-c124), and c164..c167 (fc2d-r11-card-c164..c167)."),
    "fc2d-r3-df-ppm-link": ("project.html line 289 and the 'assumption P4' link", "PASS",
        "The reworded df_ppm bullet links to #conventions, whose h3 is at line 325 (id='conventions'); P4 is defined at line "
        "331. The claim 'so every parity gap is an exact rational number' holds: with an integer df_ppm, df = df_ppm/10^6 is "
        "rational, and the reference computes the gap with Fraction (grader/reference.py line 55)."),
    "fc2d-r10-new-mutants": ("ledgers/FC2/mutants/z10_a..z10_d", "PASS",
        f"{S}mutate_fc2_r11_all.out: KILLED z10_a (test_parity_gap_rejects_a_nonpositive_strike_and_accepts_one, seed 0), "
        "z10_b, z10_c, z10_d."),
    "fc2d-r8-alt-9-10": ("alt9 and alt10", "PASS", f"{S}alts_r11.out: alt9_integer_only_parity.py and alt10_cross_multiplied_convexity_no_fraction.py each 50/50 seeds pass."),
    "fc2d-r5-alt7-cross-multiplied": ("alt7_cross_multiplied_integers", "PASS", f"{S}alts_r11.out: 50/50 seeds pass."),
    "fc2d-r6-alt8-forward-price": ("alt8_forward_price_fraction", "PASS", f"{S}alts_r11.out: 50/50 seeds pass."),
    "fc2d-r9-alternatives-rerun": ("alternatives re-run on the pin", "PASS", f"{S}alts_r11.out: all 14 alternatives 50/50 seeds pass."),
    "fc2d-r3-mut-new-killed": ("round-3 mutants q3_a..q3_d", "PASS",
        f"{S}mutate_fc2_r11_all.out: KILLED q3_a (test_parity_gap_matches_exact_rounding_second_chain[1]), q3_b "
        "(test_half_cent_gross_rounds_once_up), q3_c (test_scan_matches_exhaustive_oracle_second_chain), q3_d."),
    "fc2d-r3-mut-prior-untracked": ("round-3 mutants r3_a..r3_d", "PASS",
        f"{S}mutate_fc2_r11_all.out: KILLED r3_a, r3_b (test_puts_longer_than_strikes_is_rejected), r3_c, r3_d."),
    "fc2d-r4-mut-u4-new-killed": ("round-4 mutants u4_a..u4_c", "PASS", f"{S}mutate_fc2_r11_all.out: KILLED u4_a, u4_b, u4_c."),
    "fc2d-r5-mut-w5-new-killed": ("round-5 mutants w5_a..w5_c", "PASS", f"{S}mutate_fc2_r11_all.out: KILLED w5_a, w5_b, w5_c (seed 4 for w5_c)."),
    "fc2d-r6-mut-w6-new-killed": ("round-6 mutants w6_a..w6_d", "PASS", f"{S}mutate_fc2_r11_all.out: KILLED w6_a, w6_b, w6_c, w6_d."),
    "fc2d-r7-mut-s7-new-killed": ("round-7 mutants s7_a..s7_d", "PASS", f"{S}mutate_fc2_r11_all.out: KILLED s7_a, s7_b, s7_c, s7_d."),
    "fc2d-r8-mut-x8-a": ("mutant x8_a", "PASS", f"{S}mutate_fc2_r11_all.out: KILLED x8_a (test_negative_cost_is_rejected_even_when_no_finding_is_kept, seed 0)."),
    "fc2d-r8-mut-x8-b": ("mutant x8_b", "PASS", f"{S}mutate_fc2_r11_all.out: KILLED x8_b (test_two_strike_chain_still_checks_df_and_strikes_for_convexity, seed 0)."),
    "fc2d-r8-mut-x8-c": ("mutant x8_c", "PASS", f"{S}mutate_fc2_r11_all.out: KILLED x8_c (test_one_strike_chain_checks_the_quote_lengths, seed 0)."),
    "fc2d-r9-mut-y9-new-killed": ("round-9 mutants y9_a..y9_d", "PASS", f"{S}mutate_fc2_r11_all.out: KILLED y9_a, y9_b, y9_c, y9_d."),
    "fc2d-r3-instance-docstring-bounds": ("grader/instance.py docstring (lines 1-21) against _within_bounds and _draw", "PASS",
        "Read in full this round. The docstring's ranges (spot 80.00-200.00, df 0.930000-0.999000, fee 0-40, half-spread 1-150, "
        "half-cent rule for ties, half-cent Theorem 2.2 bounds) match lines 75-81 and 47-60; the Theorem 2.2 bounds match "
        "L05.html lines 84-96."),
}

NEW = [
    {"id": "fc2d-r11-grader-identity-over-constraint", "check": "2.6 (rule 11: alternatives must pass; tests demand only stated behaviour)",
     "location": "course/modules/FC/FC2/grader/test_project.py lines 188-194 (test_scan_returns_a_new_list_each_call)",
     "status": "FAIL",
     "evidence": (f"The test asserts 'first is not second' (line 193): scan must return a NEW list object on each call. The page "
                  "(project.html lines 301-307) states no identity requirement; the only purity rule is that the functions do not "
                  "change their arguments. A correct scanner that returns a shared empty list for the no-finding case ("
                  f"{S}alts/alt15_shared_empty_result.py) passes every "
                  "other test but fails test_scan_returns_a_new_list_each_call on seeds 0 and 1 (clean chains; "
                  "'1 failed, 93 passed' on seed 0 and on seed 1, the only failure being test_scan_returns_a_new_list_each_call). "
                  f"{S}alts_r11.out: alt15_shared_empty_result.py 28/50 seeds pass the suite, so 22 seeds fail. Seed 2 gives 94 passed."),
     "fix": ("Delete the identity assertion 'assert first is not second' (test_project.py line 193, keep the equality check on the "
             "rows on line 194), or state the requirement on project.html if it is wanted. Then rerun "
             "tools/run_graders.py --unit FC2 --seeds 0-49 and tools/mutate_graders.py --unit FC2 --seeds 0-9.")},
    {"id": "fc2d-r11-card-c016", "check": "2.7", "location": "course/modules/FC/FC2/cards.json FC2-c016 (line 111); L02.html Definition 1.1 (line 58)",
     "status": "PASS",
     "evidence": "Front 'What is the payoff at expiry of the long party to a forward contract?'; back 'The long party pays the forward price F and receives one unit, so its payoff at expiry is S_tau - F. The short party's payoff is F - S_tau (Definition 1.1).' L02.html line 58: 'the long party's payoff at expiry is S_tau - F, and the short party's is F - S_tau.' Correct; no duplicate front."},
    {"id": "fc2d-r11-card-c047", "check": "2.7", "location": "course/modules/FC/FC2/cards.json FC2-c047 (line 325 area); L03.html Problem P3 (line 357) and key table (line 427)",
     "status": "PASS",
     "evidence": "Back 'B_n = sum_{i=1}^{n} Delta_i (1 + rho)^{n-i} (Problem P3).' L03.html Problem P3 (lines 357-365): B_i = (1 + rho) B_{i-1} + Delta_i gives this sum (solution by induction). Basis 'Problem P3 (exact)' follows the deck's convention. The removed sentence about A8' moved to FC2-c165."},
    {"id": "fc2d-r11-card-c164", "check": "2.7", "location": "course/modules/FC/FC2/cards.json FC2-c164 (line 1134 area); L01.html line 124 (Remark 3.3) and Example 3.4 (line 129)",
     "status": "PASS",
     "evidence": "Back 'Yes. The two state-price equations have a nonzero determinant, -2, so there is one set of state prices. The lesson does not state uniqueness for other markets (Remark 3.3).' L01.html line 124: 'In the market of Example 3.4 they are unique, because the two state-price equations have a nonzero determinant, -2. The lesson does not state uniqueness for other markets.' Determinant of [[1,1],[3,1]] is 1 - 3 = -2 (Example 3.4 equations, line 129). Correct."},
    {"id": "fc2d-r11-card-c165", "check": "2.7", "location": "course/modules/FC/FC2/cards.json FC2-c165; L03.html Problem P3 (lines 357-365) and Proposition 1.3 (line 72)",
     "status": "PASS",
     "evidence": "Back 'For n >= 2 the identity holds for every price path only when rho = 0, so A8' is needed for Proposition 1.3 (Problem P3).' L03.html Problem P3 solution: path Delta_1 = 1, others 0 gives B_n = (1+rho)^{n-1}, which is 1 only when rho = 0 for n >= 2; 'So the identity of Proposition 1.3 needs A8'.' Correct; Proposition 1.3 says 'Assume A8'' (line 72)."},
    {"id": "fc2d-r11-card-c166", "check": "2.7", "location": "course/modules/FC/FC2/cards.json FC2-c166; L06.html Definition 1.2 (line 64)",
     "status": "PASS",
     "evidence": "Back 'max(uS_0 - K, 0) after an up move and max(dS_0 - K, 0) after a down move (Definition 1.2).' L06.html line 64: 'A claim pays V_1(u) = max(uS_0 - K, 0) if the stock goes up and V_1(d) = max(dS_0 - K, 0) if it goes down.' Correct."},
    {"id": "fc2d-r11-card-c167", "check": "2.7", "location": "course/modules/FC/FC2/cards.json FC2-c167; L08.html Definition 3.1 (line 110)",
     "status": "PASS",
     "evidence": "Back 'It stops when the bracket width is at most tau_tol, and it reports the midpoint of the final bracket (Definition 3.1).' L08.html line 110: 'While sigma_hi - sigma_lo > tau_tol, repeat ... When the loop ends, report sigma-hat = (sigma_lo + sigma_hi)/2.' Correct."},
    {"id": "fc2d-r11-mut-new-student-errors", "check": "2.6 (rule 3: at least three new student-error mutants)",
     "location": "ledgers/FC2/mutants/a11_a..a11_d (written this round by the verifier)",
     "status": "PASS",
     "evidence": f"Four new student-error mutants, each a one-change edit of reference.py (make_r11.py asserts each replacement matches once): a11_a convexity explanation omits P2; a11_b parity explanation omits P4; a11_c parity_gap_cents returns float; a11_d scan runs the convexity test on puts. {S}mutate_fc2_r11_all.out: all four KILLED (a11_a and a11_b by test_scan_explanations_are_nonempty_and_name_the_rule; a11_c by test_parity_gap_returns_an_integer_not_a_bool; a11_d by test_convexity_half_cent_tie_rounds_once_up_at_any_discount_factor, seed 0)."},
]

NOTES = (
    "Round 11 on pin ccaeeaf (round-10 pin 47a36d8). Delta inside this slice: project.html line 289 (df_ppm bullet, "
    "reworded, no new symbol or number); cards.json: FC2-c007, c016, c047, c082, c124 changed, FC2-c164..c167 added. "
    "The round-10 FAIL (fc2d-r2-scope-curriculum-brief) is fixed upstream (curriculum/02 line 428 now says SIMULATED; "
    "render_curriculum and build_site --check reproduce byte-identically) and is re-verified PASS. One new FAIL: "
    "fc2d-r11-grader-identity-over-constraint (test_scan_returns_a_new_list_each_call demands object identity the page "
    "does not state; alt15, a correct scanner returning a shared empty list, fails seeds 0 and 1). Mutants: 91, all "
    "killed on seeds 0-9 (87 prior plus a11_a..a11_d). Alternatives: 14 pass 50/50 seeds (alt1..alt14); alt15 fails as above. "
    "Collect-only count 94 for every seed 0..49. "
    "Observations, not rows: (1) failure messages for hand-built tie tests state the expected value (test_project.py lines "
    "264, 270, 277, 279, 760, 769); the expected values are also in the public test comments, so no secret answer is "
    "revealed, but the builder may prefer to name only the property. (2) Explanation direction is untested (ruled non-finding "
    "since round 5: spec line 301 requires the rule and labels, not the trade direction). (3) Retired historical rows "
    "fc2d-r7-card-c156 and fc2d-r7-card-c157 cite cards removed in commit 2d755599; carried as historical PASS per the round-9 "
    "precedent, the orchestrator may prefer to drop them. (4) For a convexity finding the spec does not name strike_cents "
    "explicitly; Lab 1 output and the grader show the middle strike. Not run: the full repo gate (pytest over all tests/, "
    "verify_refs over the whole registry, fetch_data --check, render of other units); the browser autograder UI was not "
    "driven (page_smoke ran in Pyodide only); lessons L01..L08 were read only where a changed card cites them and otherwise "
    "carried as byte-identical."
)
SUMMARY = (
    "FC2-d round 11: verdict FAIL with 1 FAIL row of 164 (163 PASS). The round-10 FAIL (curriculum brief SIMULATED) is "
    "fixed and PASS. The FAIL: a grader over-constraint (new-list identity assertion, test_project.py line 193) that a "
    "correct alternative fails. All gates in the slice pass on ccaeeaf (check_pages, check_dag, check_projects, run_labs "
    "11/11, run_graders 50/50, page_smoke, ruff, mypy strict, pytest FC2, verify_refs offline and live FC2, render and "
    "build_site checks). Mutants 91/91 killed; 14 alternatives pass 50/50."
)
rows = []
prev_ids = []
for r in prev["rows"]:
    rid = r["id"]
    prev_ids.append(rid)
    if rid in FRESH:
        loc, status, ev = FRESH[rid]
        row = {"id": rid, "check": r["check"], "location": loc, "status": status, "evidence": ev}
    elif rid == "fc2d-r2-scope-curriculum-brief":
        continue  # handled in FRESH
    else:
        if rid not in CARRY_FILES:
            raise SystemExit(f"no carry policy for {rid}")
        base_ev = r["evidence"]
        if r.get("status") != "PASS":
            raise SystemExit(f"carry of a non-PASS row {rid}")
        if rid in ("fc2d-r7-card-c156", "fc2d-r7-card-c157"):
            ev = FRESH[rid][2] + " Previous: " + base_ev
        else:
            ev = f"Carried from round 10 ({CARRY_FILES[rid]} byte-identical since the previous pin 47a36d8): " + base_ev
        row = {"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": ev}
        if rid in ("fc2d-r7-card-c156", "fc2d-r7-card-c157"):
            row["location"] = r["location"]
    rows.append(row)
    if rid == "fc2d-r2-scope-curriculum-brief":
        pass
# the scope row keeps its id and position (it was FAIL last round, now fresh PASS)
for n in NEW:
    rows.append(n)

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate row ids"
missing = [i for i in prev_ids if i not in ids]
assert not missing, f"lost row ids: {missing}"

mutants = []
for line in open(mutate_out, encoding="utf-8"):
    m = re.match(r"(KILLED|SURVIVED) (\S+?)\.py: (.*?) -> (.*)$", line.rstrip("\n"))
    if m:
        killed_by = m.group(4)
        mutants.append({"id": m.group(2), "description": m.group(3), "killed_by": None if m.group(1) == "SURVIVED" else killed_by})
assert len(mutants) == 91, len(mutants)

statuses = [r["status"] for r in rows]
fresh_pass = sum(1 for s in statuses if s == "PASS")
verdict = "PASS" if all(s == "PASS" for s in statuses) and all(m["killed_by"] for m in mutants) else "FAIL"

frag = {
    "unit": "FC2",
    "slice": "FC2-d",
    "round": 11,
    "verifier": "Claude Haiku 5.5, independent verifier for FC2-d round 11 (did not build FC2)",
    "pin": PIN,
    "base": BASE + " (round-10 pin); delta inside FC2-d: course/modules/FC/FC2/project.html line 289 (df_ppm bullet), course/modules/FC/FC2/cards.json (FC2-c007, c016, c047, c082, c124 changed; FC2-c164..c167 added); no grader, twin or lesson change; curriculum/02 line 428 and curriculum.json line 7797 (brief) changed outside the slice and re-verified",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD11-FC2-d",
    "scratch": S,
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": NOTES,
    "summary": SUMMARY,
}
json.dump(frag, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("rows", len(rows), "pass", sum(s == "PASS" for s in statuses), "fail", sum(s == "FAIL" for s in statuses),
      "unverifiable", sum(s == "UNVERIFIABLE" for s in statuses), "verdict", verdict,
      "mutants", len(mutants), "killed", sum(1 for m in mutants if m["killed_by"]))
