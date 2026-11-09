# Builds ledgers/SC1/SC1-d.json (round 1, closing delta) from the base fragment (read-only) and this round's outputs.
import json
import re
import sys

BASE = "/Users/billyribeiro/.fanout/frags/E-SC1-d.round18.json"
OUT = "/Users/billyribeiro/.fanout/wt/verifyF31-SC1-d/ledgers/SC1/SC1-d.json"
O = "/Users/billyribeiro/.fanout/wt/verifyF31-SC1-d/ledgers/SC1/scripts/SC1-d-r1/out/"
base = json.load(open(BASE, encoding="utf-8"))

CARRY_FILES = ("course/modules/SC/SC1/project.html, grader/ (reference.py, starter.py, instance.py, test_project.py), "
               "tests/labs/SC1/, tools/, notation/, references/references.json, plans/SC1-build-plan.md, "
               "L01/L05/L06/L08/index.html and the named mutant or alternative files")
CARRY = ("Carried from round 18 (" + CARRY_FILES + " byte-identical since the previous pin 50559266; "
         "none of them is in the closing delta except as stated in the re-verified rows): ")

fresh = {}
def fv(rid, check, location, status, evidence):
    fresh[rid] = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}

GATE_EVID = (
    "Round 1 (closing delta verifier) on pin 95f3f8cb, fresh runs in ledgers/SC1/scripts/SC1-d-r1/out/: "
    "check_pages_unit_r1.txt 'check_pages SC1: PASS' EXIT=0; check_dag_unit_r1.txt 'check_dag SC1: PASS' EXIT=0; "
    "check_projects_unit_r1.txt 'check_projects SC1: PASS' EXIT=0; run_labs_unit_r1.txt 'run_labs SC1: PASS (11/11)'; "
    "run_labs_project_r1.txt 'PASS (3/3)'; run_graders_0_49_r1.txt 'PASS (reference 50/50 seeds)'; "
    "page_smoke_project_r1.txt 'in-browser grader: All 136 tests pass ... page_smoke SC1: PASS'; "
    "page_smoke_L02_L03_r1.txt 'page_smoke modules/SC/SC1/L03.html: PASS' and L02 PASS; mypy_r1.txt 'Success: no issues found in 386 source files'; "
    "ruff_check_repo_r1.txt 'All checks passed!'; ruff_format_repo_r1.txt '555 files already formatted'; "
    "verify_refs_offline_r1.txt 'offline integrity: 560 entries, 0 problems'. Run with the checkout .venv symlink.")
fv("SC1-d-r10-gates", "gate", "repository", "PASS", GATE_EVID)
fv("SC1-d-r10-page-smoke", "2.9-structure / 2.6-autograder", "course/modules/SC/SC1/project.html",
   "PASS", "Round 1 fresh: page_smoke_project_r1.txt (EXIT=0) 'page_smoke modules/SC/SC1/project.html: PASS'; the in-browser grader reports 'All 136 tests pass' (seed 1774702427). project.html is byte-identical to pin 50559266 (git diff --quiet). The page's '136 tests' (project.html:226) matches the staged collect-only count in the mutant row.")

MUT_EVID = ("Round 1 fresh: tools/mutate_graders.py --unit SC1 --seeds 0-9 -> ledgers/SC1/scripts/SC1-d-r1/out/"
            "mutate_graders_unit_r1.txt 'mutate_graders SC1: PASS (94/94 killed)', EXIT=0. The directory ledgers/SC1/mutants/ "
            "holds 94 top-level .py files (ls count) = 90 carried at pin 50559266 plus r18_01..r18_04 added after the pin; "
            "r18_01..r18_04 are KILLED (reflection_tail swap, horizon cap, half grid, path smoothing). ")
for rid, loc in [
    ("SC1-d-r11-mutate-gate", "ledgers/SC1/mutants/ (top level)"),
    ("SC1-d-r7-mutants-all", "ledgers/SC1/mutants/ (all grader mutants)"),
    ("SC1-d-r10-mutant-seed-coverage", "ledgers/SC1/mutants/ on seeds 0-9"),
    ("SC1-d-r12-mutants-all-existing", "ledgers/SC1/mutants/*.py (94 files; the row said 82 at round 12, stale)"),
    ("SC1-d-r17-mutate-all", "ledgers/SC1/mutants/ (94 top-level files; the row said 90 at round 17, stale)"),
    ("SC1-d-r18-mutants-all", "tools/mutate_graders.py --unit SC1 --seeds 0-9 over all 94 mutants"),
    ("SC1-d-r18-mutants-new", "ledgers/SC1/mutants/r18_01..r18_04"),
]:
    fv(rid, "2.6-mutation", loc, "PASS", MUT_EVID + "Row subject changed in the delta (directory count), so re-verified from scratch.")
fv("SC1-d-r10-mutant-folder-hygiene", "2.6-mutation",
   "ledgers/SC1/lab-mutants/SC1-a-r10/ (4 files), SC1-a-r11/ (6), SC1-a-r12/ (9) = 19 lab-twin mutants; the carried row's path 'ledgers/SC1/mutants/SC1-a-r1x/' does not exist at 95f3f8cb",
   "PASS",
   "Re-verified: ls ledgers/SC1/lab-mutants/SC1-a-r10 | wc -l = 4, SC1-a-r11 = 6, SC1-a-r12 = 9 (19 total). ledgers/SC1/mutants/ contains no subdirectory and no lab-twin file (94 .py files, all m*/r* project-grader mutants, listed in mutate_graders_unit_r1.txt). The carried row cited the wrong directory; the location is corrected here, and the hygiene claim (lab-twin mutants are not in the project-grader set) holds. " + MUT_EVID)

fv("SC1-d-r17-continuity-attribution", "2.9-prose (attribution)", "course/modules/SC/SC1/project.html:243 vs L02.html Theorem 2.5 (line 289) and Remark 2.6 (line 303)",
   "PASS", "Re-verified: L02.html changed in the delta only at line 285 (A2 sketch; git diff -U0 hunk '@@ -285 +285 @@'), so Theorem 2.5 (heading at L02.html:289, conclusion: every path continuous) and Remark 2.6 (heading at line 303; conclusion line 308 'every path of W is continuous') are byte-identical to the pin. project.html:243 reads 'with continuous paths as in Theorem 2.5 and Remark 2.6 of Lesson 2', matching both. The carried row's note that the L02 delta hunk was at line 48 is stale: the L02 hunk is at line 285; the line-48 hunk belongs to L03.html.")
fv("SC1-d-r15-cross-references", "2.9-prose / 2.4", "project.html references: Lesson 2 Thm 2.5 and Remark 2.6 (project.html:243); L01 Def 1.1; L05 A3/A4; L06 Prop 1.3 and Cor 1.4; L05 Sections 1 and 3",
   "PASS", "Re-verified in the sources this round: L02.html:289 'Theorem 2.5 (a Brownian motion on [0, 1] with continuous paths)' and L02.html:303 'Remark 2.6'; L01.html 'Definition 1.1 (standard Brownian motion)'; L05.html 'Assumption A3 (strong Markov property; not proved here)' and 'Assumption A4'; L06.html 'Proposition 1.3 (discrete reflection identity)', 'Corollary 1.4 (discrete tail identity)'. project.html names no L03 item and no A2 item. L01, L05, L06 unchanged in the delta (git diff); L02 changed only at line 285.")
fv("SC1-d-r17-crossrefs", "2.9-prose / 2.4-attribution", "project.html:37, 42-46, 210, 222-224, 231-243, 247, 250, 531-537, 659 vs L01-L08",
   "PASS", "Re-verified: every lesson item that project.html cites is at its source: L01 Definition 1.1; L02 Theorem 2.5 and Remark 2.6 (headings at L02.html:289 and 303, unchanged by the delta); L05 A3, A4 (Assumption A3 heading present); L06 Proposition 1.3 and Corollary 1.4; L08 Proposition 1.2 and Corollary 1.3 (headings present). The L02 and L03 hunks change no cited item (L02 line 285 is the A2 sketch, which project.html does not cite; L03 line 51 is a why-it-matters paragraph, which project.html does not cite; grep of project.html for 'Lesson 2', 'Theorem 2.5', 'Remark 2.6' gives line 243 only). Internal lesson cross-references only; no bibliographic data typed here.")
fv("SC1-d-r18-L06-L08-L05-L01-labels", "round-18 fresh check", "project.html citations: L01 Def 1.1, L02 Thm 2.5 and Rem 2.6, L05 A3/A4, L06 Prop 1.3 and Cor 1.4, L08 Prop 1.2 and Cor 1.3",
   "PASS", "Re-verified headings: L01.html 'Definition 1.1 (standard Brownian motion)'; L02.html:289 'Theorem 2.5'; L02.html:303 'Remark 2.6'; L05.html 'Assumption A3 (strong Markov property; not proved here)' and 'Assumption A4 (standard facts used without proof)'; L06.html 'Proposition 1.3 (discrete reflection identity)' and 'Corollary 1.4 (discrete tail identity)'; L08.html 'Proposition 1.2 (running maximum and first passage on each path)' and 'Corollary 1.3 (distribution function of the first passage)'. Grep output in this round's shell; L01, L05, L06, L08 byte-identical to the pin.")
fv("SC1-d-r12-pathwise-only-l01", "2.9-prose (define before use)", "project.html conventions; L01.html Definition 1.1 (outside this slice)",
   "PASS", "Re-verified: the cited L01 Definition 1.1 is present (L01.html heading 'Definition 1.1 (standard Brownian motion)'), L05 A3/A4 and L06 Prop 1.3/Cor 1.4 and L08 Prop 1.2/Cor 1.3 are present as in the previous row. L01, L05, L06, L08 are byte-identical to the pin (git diff --quiet). The L06 Corollary 1.4 card changed in cards.json (SC1-c110), but the lesson statement it cites did not change.")

NUM_NEW = {
 "SC1-d-r1-L02-sketch-hunk": ("2.4-attribution / 2.2-math (changed sketch)", "course/modules/SC/SC1/L02.html:285 (A2 sketch, the only L02 hunk)",
   "PASS", "The delta's only L02 change is one sentence in the sketch for Assumption A2: 'choose dyadic times t^(k) in [t,1] that decrease to t (the constant sequence 1 when t=1)', replacing 'choose dyadic times t^(k) decreasing to t'. Checked by ledgers/SC1/scripts/SC1-d-r1/dyadic_sketch_r1.py (output out/dyadic_sketch_r1.txt): for 1894 rationals t in [0,1] (q up to 60, plus 1/3, 2/7, 1e-6, 999999/1e6), t_k = ceil(2^k t)/2^k is dyadic, lies in [t,1], is non-increasing in k, and satisfies 0 <= t_k - t < 2^-39 at k = 39: 0 violations. t=1 gives the constant 1 and t=0 the constant 0; t=1/3 gives 1, 1/2, 1/2, 3/8, 3/8, 11/32. So the parenthetical is correct. 'Decrease' is non-strict (constant for dyadic t); this is wording, not a false claim. The sketch is still labelled 'Sketch, not a proof' and A2 is still stated as an assumption (L02.html:283-284)."),
 "SC1-d-r1-L03-why-it-matters": ("2.9-prose (lab statements) / 2.2 (claims vs lesson)", "course/modules/SC/SC1/L03.html:51 (why-it-matters; only L03 hunk)",
   "PASS", "The changed paragraph's claims: (i) mesh = 'the longest interval of the partition' is the definition at L03.html:55; (ii) 'each squared increment has mean equal to its interval's length' and the sum has mean t: Lemma 2.2 and Theorem 2.3 proof (L03.html:110-112); (iii) the smooth-function sums shrink as the longest interval shrinks: Proposition 2.4(a) bound 4H^3|P| (L03.html:270); (iv) mean-square limit under Assumptions 3.1 and 3.2, 'stated in §1': Assumption 3.1 at L03.html:65 and 3.2 at L03.html:70, both inside section s1 (L03.html:53). (v) Lab 1 'prints each sample mean with its standard error': the lab text at L03.html:139 says it prints the sample mean and the standard error sd/sqrt(n); the twin run (ledgers/SC1/scripts/SC1-d-r1/out/twin_L03_1_r1.txt, python -I -W error, EXIT=0) prints 'mean ..., se ..., z = ...' for each N. The lab's 2^k equal steps (L03.html:133, N = 2^k for k 0..7) match 'partitions into 2^k equal steps'. Not a slice-d row; checked because its subject changed."),
 "SC1-d-r1-closing-delta-scope": ("2.9 delta scope (ruling 30)", "git diff 50559266..HEAD over slice d subjects",
   "PASS", "Delta over the slice's subjects, git diff --name-status 50559266..95f3f8cb: CHANGED: course/modules/SC/SC1/L02.html (one line, 285), L03.html (one line, 51), cards.json (c030, c031, c110, c119, c122, c210, c217 removed, c221, c224, new c243; cards outside slice d, see notes), plans/FINAL-ARCHITECT-RULINGS.md (items 24-37 appended; hunk '@@ -59,3 +59,78 @@', items 1-23 unchanged), ledgers/SC1/mutants/r18_01..r18_04 (added), ledgers/SC1/lab-mutants/SC1a-r16-* (added, slice a). UNCHANGED (git diff --quiet): project.html, grader/, tests/labs/SC1/, tools/, notation/, references/references.json, plans/SC1-build-plan.md, L01, L05, L06, L08, index.html. Re-verified rows: those citing the mutant directory, L02 Theorem 2.5/Remark 2.6, and the gates. Carried: rows whose subjects are unchanged."),
 "SC1-d-r1-ruling-37-no-new-mutants": ("2.6-mutation (ruling 37)", "plans/FINAL-ARCHITECT-RULINGS.md item 37; ledgers/SC1/mutants/",
   "PASS", "Item 37 'Closing round writes no new mutants' (FINAL-ARCHITECT-RULINGS.md, appended block): this round authored no mutant; its only new files are under ledgers/SC1/scripts/SC1-d-r1/ (gates_r1.sh, build_frag_r1.py, dyadic_sketch_r1.py, out/). The standing set of 94 is run (row SC1-d-r18-mutants-all) and killed 94/94. Ruling 26 kinds checked on the changed subjects: gates pass; no surviving mutant; the L02 sketch is correct; the L03 claims are supported by the lab output; no missing hypothesis introduced."),
 "SC1-d-r1-rulings-30-37-governance": ("2.9 governance (rulings 30 and 26)", "plans/FINAL-ARCHITECT-RULINGS.md items 26, 30, 37",
   "PASS", "Ruling 30 (delta closes a fixed slice): this fragment starts from the base fragment (pin 50559266), re-verifies every non-PASS row (none in the base) and every row whose subject changed (listed above), carries the rest with the carry prefix, and keeps all 240 base row ids. Ruling 26 FAIL kinds applied to the re-verified rows: none found, so the verdict is PASS."),
}
for rid, (chk, loc, st, ev) in NUM_NEW.items():
    fv(rid, chk, loc, st, ev)

# carried rows: every base row not re-verified
rows = []
for r in base["rows"]:
    rid = r["id"]
    if rid in fresh:
        rows.append(fresh[rid])
    else:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": CARRY + r["evidence"]})
rows.extend(NUM_NEW_ORDER if False else [])
for rid in NUM_NEW:
    rows.append(fresh[rid])

# mutants from this round's mutate_graders output (no new mutants authored)
mutants = []
for line in open(O + "mutate_graders_unit_r1.txt", encoding="utf-8"):
    m = re.match(r"KILLED (\S+?): (.*) -> (.*)$", line.rstrip("\n"))
    if m:
        mutants.append({"id": m.group(1), "description": m.group(2), "killed_by": m.group(3)})
assert len(mutants) == 94, len(mutants)

frag = {
    "unit": "SC1",
    "slice": "d",
    "round": 1,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-d, closing delta round 1 (rulings 30 and 37): did not build SC1-d; re-ran slice gates and the 94-mutant standing set, read the L02 and L03 hunks and the rulings delta, and checked the L02 sketch numerically.",
    "pin": "95f3f8cb",
    "base": "50559266",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyF31-SC1-d",
    "scratch": "/tmp/sc1d_r1_scratch",
    "scripts_dir": "ledgers/SC1/scripts/SC1-d-r1/",
    "verified_at": "2026-11-09T16:34:10+00:00",
    "verdict": "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Base fragment is ~/.fanout/frags/E-SC1-d.round18.json (pin 50559266, 240 rows, all PASS). All 240 base ids are kept; 15 base rows are re-verified, 225 are carried, and 5 rows are new (ids SC1-d-r1-*).",
        "Out of slice d, not verified here: cards.json changes (SC1-c030, c031, c110, c119, c122, c210, c221, c224 front/back edits; SC1-c217 removed; SC1-c243 new with only id, lesson, front, back and cite keys, no grade or basis). Cards are outside slice d per the base notes. Observation only: c243 has no grade or basis key, unlike the T-graded cards around it.",
        "Observation (wording, not a row): the A2 sketch says 'decrease to t'; the sequence is non-increasing and constant for dyadic t, so 'non-increasing' would be exact.",
        "Carried row SC1-d-r10-mutant-folder-hygiene had a wrong directory (ledgers/SC1/mutants/SC1-a-r1x/); the lab-twin mutants are in ledgers/SC1/lab-mutants/. Location corrected in this fragment; the claim holds.",
        "Stale counts corrected in re-verified rows: ledgers/SC1/mutants/ has 94 .py files at 95f3f8cb (90 at pin 50559266 plus r18_01..04).",
        "pytest tests/labs collects no tests (EXIT=5, out/pytest_labs_r1.txt): the lab twins are covered by run_labs, not by pytest. Not a gate row.",
        "test_project.py cannot be collected in place (it imports bm_checks and instance); collect-only in place fails with ImportError (collect_count_r1.txt, EXIT=2: bm_checks and instance are not on the path outside run_graders staging), so it was run in a staged scratch copy (/tmp/sc1d_r1_scratch/collect) with reference.py as bm_checks.py: 136 tests collected (out/collect_staged_r1.txt, EXIT=0).",
        "No SC1 blind-scorer file exists in ~/.fanout/blind (ten files, none for SC1); the exemplar calibration rows are carried from the base, and project.html is byte-identical to the pin.",
        "The base checkout /Users/billyribeiro/.fanout/wt/verifyE18-SC1-d no longer exists, so the r18 mutant bytes could not be compared with it; they were run at 95f3f8cb (all KILLED).",
        "Not checked: reference seeds 50-199; the full repository pytest suite (not a slice gate); live verify_refs; the vendor directory (not present in this checkout; no SC1 gate needs it)."
    ],
    "summary": "SC1-d closing delta round 1 on pin 95f3f8cb (base 50559266): verdict PASS. 240 base rows kept; 15 base rows re-verified from scratch (gates, the 94-mutant standing set, cross-reference rows citing L02 Theorem 2.5/Remark 2.6, the carried row with the wrong mutant directory); 225 carried with byte-identical subjects; 5 new rows for the changed L02 sketch, the changed L03 paragraph, the delta scope and the ruling 30/37 governance. Mutants 94/94 killed (no new mutants authored). Gates: check_pages, check_dag, check_projects, run_labs 11/11 and 3/3, run_graders 50/50 seeds, page_smoke project and L02/L03 PASS, mypy 386 files, ruff check and format PASS, verify_refs 560 entries 0 problems, collect-only 136.",
}

RULING_NOTE = " (FINAL-ARCHITECT-RULINGS.md items 10, 21 and 23 lie above the appended hunk at line 59 and are unchanged in the delta.) "
SCRIPT_NOTE = " (The SC1-d-r18 script and output files cited here were written by the base round 18 after pin 50559266; they are unchanged at 95f3f8cb, and the subjects they test are byte-identical.) "
for row in rows:
    if row["evidence"].startswith("Carried"):
        if row["id"] in ("SC1-d-r7-alt4-ruling10", "SC1-d-r15-plan-5-5-within-5se", "SC1-d-r17-plan-5-7-item4-draw-order"):
            row["evidence"] = row["evidence"].replace("): ", "):" + RULING_NOTE, 1)
        if "SC1-d-r18" in row["location"] or "SC1-d-r18" in row["evidence"][:300]:
            row["evidence"] = row["evidence"].replace("): ", "):" + SCRIPT_NOTE, 1)
errs = None
json.dump(frag, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows", len(rows), "mutants", len(mutants), "re-verified", len(fresh))
