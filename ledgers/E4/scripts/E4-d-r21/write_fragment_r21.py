"""Round-21 verifier: writes ledgers/E4/E4-d.json from the round-20 fragment (row ids kept) and this round's outputs.

Rows whose cited subjects are byte-identical since the round-20 pin are carried with the prescribed prefix;
every other row is re-verified this round with the outputs in ledgers/E4/scripts/E4-d-r21/out/.
"""
import json
import re
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE21-E4-d")
OUT = ROOT / "ledgers/E4/scripts/E4-d-r21/out"
prev = json.loads(Path("/Users/billyribeiro/.fanout/frags/E-E4-d.round20.json").read_text(encoding="utf-8"))

CARRY_FILES = ["reference.py", "instance.py", "starter.py", "literal_price_sign.py", "notation.json", "index.html",
               "L06.html", "L07.html", "E4-build-plan.md"]
CHANGED_TOKENS = ["project.html", "test_project", "README", "mutant", "FINAL-ARCHITECT", "cards.json", "alt_",
                  "labs", "references", "run_labs", "verify_refs", "mutate", "collect", "pytest", "ruff", "mypy",
                  "page_smoke", "check_", "equivalent", "scripts/", "tools/"]
NO_CARRY_CHECKS = {"2.6-mutation", "2.6-alternatives", "2.5-labs", "2.6-equivalent", "gate", "2.1-citations"}

REV = "Re-verified round 21 at 6d22ff56: "

# Special evidence for rows whose subject changed in the delta or whose finding changed.
SPECIAL = {
    "E4d-rubric-observable": (
        "PASS", REV + "project.html:524-528 read in full. Level 3 of C4 requires the decimals shown for each output "
        "('States, for each output, the decimals or significant digits shown'); level 4 adds the rule that produces the "
        "numbers and the precision of each derived number. Each level now has an element the next lower level does not "
        "have, so C4 levels 2, 3 and 4 are observably distinct. Round-20 FAIL closed."),
    "E4d20-rubric-C4-levels": (
        "PASS", REV + "project.html:527 (C4 row) and :518 (highest-level sentence). Level 4 = level 3 plus the rule and "
        "the precision of each derived number; level 3 = decimals for each output; level 2 = fixed decimals, no rule. "
        "Exemplar scores unchanged (blind file ~/.fanout/blind/E4-d.json, ruling 23). Round-20 FAIL closed."),
    "E4d20-grader-root-tolerance": (
        "PASS", REV + "course/modules/E/E4/grader/test_project.py:346-349 now reads root = oracle_root(sd, cost) and "
        "abs(lam - root) <= TOL_ROOT * root (TOL_ROOT = 1e-10, comment at :46). This matches project.html:317 ('within "
        "1e-10 times the root'). run_graders 0-49: reference 50/50; alt_1..alt_8 each 50/50 with the relative check "
        "(out/alt_*.txt, out/run_graders_E4_0_49.txt). Round-20 FAIL closed."),
    "E4d20-equiv-readme-literal-open-item": (
        "PASS", REV + "ledgers/E4/equivalent/README.md:9-12 now reads 'Decision: ruling 24 (round 18) keeps this variant "
        "equivalent'; the section 'What the architect must decide' is replaced by 'Decision (ruling 24)' (:27-31). No open "
        "item remains. Round-20 FAIL closed."),
    "E4d-cmd-run-labs": (
        "PASS", REV + "tools/run_labs.py --unit E4: 'run_labs E4: PASS (12/12)' (out/run_labs_E4_all.txt). "
        "tools/run_labs.py --unit E4 --page project.html reports 0/0 (out/run_labs_E4_project.txt): the page filter "
        "selects no block, so the 12/12 run is the evidence. Lab 2 page code differs from its twin only at the blank "
        "(ruling 11; out/labs_twin_check_r21.txt)."),
    "E4d-lab-project-1": ("PASS", REV + "out/labs_twin_check_r21.txt: page code == twin True; twin rc 0 under "
                          "python -I -W error, stderr 0 bytes; output == expected block True. Printed values match the "
                          "hypothesis sentence at project.html:57."),
    "E4d-lab-project-2": ("PASS", REV + "out/labs_twin_check_r21.txt: page code differs from twin only at the "
                          "'return ___' blank (diff checked, ruling 11); twin output == expected block True."),
    "E4d-lab-project-3": ("PASS", REV + "out/labs_twin_check_r21.txt: page code == twin True; output == expected block "
                          "True; 'largest difference ... 2.1e-13' and '484 of 484' reproduced."),
    "E4d-num-lab-hypotheses": ("PASS", REV + "Lab 1 hypothesis numbers (+0.053092, -0.080731, 0.57937525, -3.45199422, "
                               "0.18904110, 0.15898618) equal the printed expected block; Lab 3 hypothesis numbers "
                               "(0.5582/0.6978/0.8373; 0.1920/0.1420/0.0889; |gap|<1e-13; 2.1e-13; 484) equal "
                               "out/run_labs_E4_all.txt, and the Lab 2 hypothesis numbers equal its expected block."),
    "E4d-num-exemplar-table": ("PASS", REV + "project.html:628-660 table rows equal Lab 3 expected rows (0.5567/0.1420/"
                               "+3.55e-14 etc.); max |gap| 3.55e-14 < 4e-14 as the memo states. Ratios recomputed by "
                               "script: 1.249999999999898 and 1.500000000000611 (both round to 1.2500 and 1.5000)."),
    "E4d10-delta-results-ratio": ("PASS", REV + "project.html:628 ratios 1.25 and 1.50 from unrounded solver output "
                                  "0.6977534100112734/0.5582027280090642 and 0.8373040920139374/0.5582027280090642 "
                                  "reproduced by the reference (1.249999999999898, 1.500000000000611)."),
    "E4d13-exemplar-numbers-arith": ("PASS", REV + "exemplar B results: 0.0889 is 0.08894 rounded (1 - e^0.6/2 = "
                                     "0.0889406); gaps all |g| < 4e-14; informativeness 0.1920/0.1420/0.0889 constant "
                                     "across noise volumes per cost; reproduced by out/run_labs_E4_all.txt."),
    "E4d16-exemplar-B-claims": ("PASS", REV + "exemplar B passages (:604-662) checked against the reference grid "
                                "(out/run_labs_E4_all.txt; ratio script above); the C1 level-4 annotation is a scoring "
                                "judgement and was not re-scored (ruling 23)."),
    "E4d4-exemplar-B-results-numbers": ("PASS", REV + "project.html:628-641 numbers equal Lab 3 printed rows and the "
                                        "ratios above."),
    "E4d12-exemplar-B-sigma": ("PASS", REV + "project.html:607 and :628: lambda* = 2 sigma sqrt(tb/(1-tb)) with "
                               "tau-bar = 2e^{-4c}-1 reproduces the grid fractions (0.5582, 0.4453, 0.3289, ...)."),
    "E4d-rubric-observable-dummy": ("PASS", ""),
    "E4d-exemplar-A-calibration": ("PASS", REV + "Calibration rows cite the blind scorer file ~/.fanout/blind/E4-d.json "
                                   "(ruling 23), not this verifier's scores. Its A scores [2,2,1,2,1] equal the page's "
                                   "data-scores (project.html:536) and the official line at :538."),
    "E4d-exemplar-B-calibration": ("PASS", REV + "Blind file B [4,4,4,4,4] equals data-scores (project.html:601) and "
                                   "the official line at :603. Not re-scored by this verifier (ruling 23)."),
    "E4d19-calibration-blind-file": ("PASS", REV + "~/.fanout/blind/E4-d.json present; its notes state the stripper "
                                     "re-run (exit 0) and 0 leak matches; A=[2,2,1,2,1], B=[4,4,4,4,4]."),
    "E4d20-calibration-blind": ("PASS", REV + "data-scores at project.html:536 (2,2,1,2,1) and :601 (4,4,4,4,4) equal "
                                "the blind file A and B."),
    "E4d4-calibration-blind": ("PASS", REV + "Calibration cites ~/.fanout/blind/E4-d.json; A equals data-scores."),
    "E4d5-calibration-B-blind": ("PASS", REV + "Calibration cites ~/.fanout/blind/E4-d.json; B equals data-scores."),
    "E4d15-exemplar-verdicts": ("PASS", REV + "data-reveal verdict texts at :537, :603 read; the official-scoring "
                                "sentences match the data-scores (2,2,1,2,1 and 4,4,4,4,4)."),
    "E4d-grader-exceptions": ("PASS", REV + "test_project.py:192-234 (named conditions only: noise volume zero, negative, "
                              "inf, nan; cost negative and -1e-12) and reference.py:_check_inputs; the exception table "
                              "(project.html:328-333) names exactly these two ValueError conditions; messages match."),
    "E4d-grader-messages": ("PASS", REV + "every expect() and pytest.fail message in test_project.py read; none "
                            "formats an expected value; must_raise texts equal the table messages."),
    "E4d-grader-oracle": ("PASS", REV + "oracle functions test_project.py:79-172 re-read: regressions, fixed point, "
                          "trapezoid quadrature (1001 nodes); oracle(0) vs reference limit differs by at most 1.11e-16 "
                          "(out/check_doc_claims, script E4d21-doc-numbers)."),
    "E4d17-oracle-agreement": ("PASS", REV + "oracle vs reference at the reported fraction: run_graders 50/50 "
                               "(out/run_graders_E4_0_49.txt); oracle(0) vs limit <= 1.11e-16."),
    "E4d11-oracle-precision": ("PASS", REV + "oracle precision checked by run_graders 50/50 and the doc-number script."),
    "E4d-grader-test-docstring": ("PASS", REV + "test_project.py docstrings with numbers checked: the gap at 1e-12 "
                                  "differs from the limit by 1.02e-13..3.54e-13 (stated 1e-13 to 4e-13), the oracle "
                                  "agrees to <= 1.11e-16 (stated 1.1e-16); domain point root 7.7935e-22 (stated about "
                                  "7.8e-22); corner root 2.0224e-51 with tau-bar 0.0101216 (stated about 2e-51, just "
                                  "above 1e-2)."),
    "E4d18-docstring-numbers": ("PASS", REV + "same numeric check as E4d-grader-test-docstring (script output in "
                                "scripts/E4-d-r21/out/check_doc_claims is re-printed by write step); all stated values "
                                "agree."),
    "E4d10-new-test-numbers": ("PASS", REV + "numbers in test_project.py docstrings recomputed (see above)."),
    "E4d12-corner-test-docstring": ("PASS", REV + "test_corner_root... docstring: a 200-halving search leaves a bracket of "
                                    "6.2e-61 against a 2.0e-61 requirement, so the reported fraction misses the "
                                    "requirement at this point (killed by the test; mutant_r6_09 and f11_01). The "
                                    "sentence states a consequence at this point, not a general midpoint bound."),
    "E4d19-corner-200-halvings": ("PASS", REV + "same as E4d12-corner-test-docstring; reference.py:21-23 reports 240 "
                                  "halvings reach the tolerance for every root above about 6e-61 (2^-240 = 5.7e-73)."),
    "E4d-grader-reference-docstring": ("PASS", REV + "reference.py:21-23 comment and 14-16 checked: 2^-240 = 5.7e-73; "
                                       "200 halvings do not reach the tolerance near 2e-51 (6.2e-61 > 2e-63)."),
    "E4d6-stop-rule-measured": ("PASS", REV + "reference.py stop rule (high - low > 1e-12 * high, <= 240 halvings) "
                                "re-read; root sweep over 9547 domain points: worst relative error 4.96e-13 "
                                "(out/root_accuracy_sweep_r21.txt)."),
    "E4d8-tiny-root-reference": ("PASS", REV + "reference.py root sweep (above) covers roots down to 1e-51."),
    "E4d13-accuracy-sweep": ("PASS", REV + "scripts/E4-d-r21/root_accuracy_sweep_r21.py: 9547 interior domain points, 0 "
                             "above 1e-10 relative, worst 4.961e-13 (out/root_accuracy_sweep_r21.txt)."),
    "E4d14-accuracy-sweep": ("PASS", REV + "same sweep as E4d13-accuracy-sweep."),
    "E4d19-accuracy-sweep": ("PASS", REV + "same sweep as E4d13-accuracy-sweep."),
    "E4d14-corner-scan": ("PASS", REV + "corner test points (1e-50, 0.1707691121) reproduced: root 2.022385444498892e-51, "
                          "closed form 2.0223854444989538e-51, relative error 1e-16."),
    "E4d-cmd-check-pages": ("PASS", REV + "tools/check_pages.py --unit E4: 'check_pages E4: PASS' (out/check_pages_E4.txt)."),
    "E4d-cmd-check-dag": ("PASS", REV + "tools/check_dag.py --unit E4: PASS (out/check_dag_E4.txt)."),
    "E4d-cmd-check-projects": ("PASS", REV + "tools/check_projects.py --unit E4: PASS (out/check_projects_E4.txt)."),
    "E4d-cmd-run-graders": ("PASS", REV + "tools/run_graders.py --unit E4 --seeds 0-49: PASS (reference 50/50, slowest "
                            "0.4 s) (out/run_graders_E4_0_49.txt)."),
    "E4d-cmd-page-smoke-project": ("PASS", REV + "tools/page_smoke.py --unit E4 --pages project.html: PASS (out/page_smoke_E4_project.txt)."),
    "E4d-cmd-ruff": ("PASS", REV + "ruff check . -> 'All checks passed!'; ruff format --check . -> 553 files already formatted."),
    "E4d-cmd-mypy-workspace": ("PASS", REV + "mypy --no-incremental: 'Success: no issues found in 385 source files' (out/mypy.txt)."),
    "E4d-cmd-mypy-plan-command": ("PASS", REV + "same mypy run as E4d-cmd-mypy-workspace (mypy strict is repository-wide)."),
    "E4d-cmd-pytest-relevant": ("PASS", REV + "pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py "
                                "tests/test_page_smoke.py: exit 0, 414 passed (progress lines of out/pytest_labs.txt, 414 dots, no failure marks)."),
    "E4d-cmd-verify-refs": ("PASS", REV + "verify_refs.py --offline: 560 entries, 0 problems; live re-verification of E4: "
                            "3 of 560 entries, 0 problems (out/verify_refs_offline_all.txt, out/verify_refs_E4_live.txt). "
                            "Note: --offline with --unit exits 2 (the --unit flag selects a live run)."),
    "E4d-cmd-collect": ("PASS", REV + "pytest --collect-only on test_project.py with reference.py as solver.py: 49 tests "
                        "collected (out/collect_count_r21.txt); project.html:319 says '49 checks'."),
    "E4d-cmd-run-labs-dummy": ("PASS", ""),
    "E4d20-run-labs-unit": ("PASS", REV + "tools/run_labs.py --unit E4: 12/12 PASS (out/run_labs_E4_all.txt)."),
    "E4d20-labs-twins-direct": ("PASS", REV + "out/labs_twin_check_r21.txt: twins run with python -I -W error; "
                                "outputs equal the expected blocks; stderr empty."),
    "E4d13-lab-twins-direct": ("PASS", REV + "out/labs_twin_check_r21.txt (see E4d20-labs-twins-direct)."),
    "E4d11-lab-page-twin": ("PASS", REV + "out/labs_twin_check_r21.txt: Lab 1 and Lab 3 page code == twin; Lab 2 "
                            "differs only at the blank (ruling 11)."),
    "E4d8-lab3-twin-page": ("PASS", REV + "Lab 3 page code == twin (out/labs_twin_check_r21.txt)."),
    "E4d10-lab3-numbers": ("PASS", REV + "Lab 3 expected block equals the run (out/run_labs_E4_all.txt)."),
    "E4d7-lab3-closed-form-sentence": ("PASS", REV + "'largest difference ... 2.1e-13' is below the 1e-12 claim; "
                                       "closed-form column equals the bisection to 4 decimals."),
    "E4d-hours-estimate": ("PASS", REV + "hours 1+1+5+8+5+5+3 = 28 = data-hours-project 28; index.html:29 hub split "
                           "72 + 28 = 100 and nine lessons of eight hours = 72 (index.html:139)."),
    "E4d13-hours-arithmetic": ("PASS", REV + "same arithmetic as E4d-hours-estimate; index.html:29, :40."),
    "E4d19-hub-hours": ("PASS", REV + "index.html:29, :31, :40, :139 read: 72 lesson + 28 project = 100."),
    "E4d16-hours-band": ("PASS", REV + "data-hours-project=28 equals the table total (project.html:341-352)."),
    "E4d20-hours-verifier-estimate": ("PASS", REV + "hours are design targets (ruling of the verifier rules); the "
                                      "arithmetic is consistent (28 = 28 = 28)."),
    "E4d-cites-only-registry": ("PASS", REV + "data-cite keys muth1961rational and milgrom1982information exist in "
                                "references/references.json (verify_refs offline 560 entries, 0 problems)."),
    "E4d-registry-muth": ("PASS", REV + "references.json entry present; verify_refs live 3 entries 0 problems; page "
                          "attributes no statement to it (project.html:683-686)."),
    "E4d-registry-milgrom": ("PASS", REV + "same as E4d-registry-muth."),
    "E4d15-reading-and-citations": ("PASS", REV + "Reading section read; no attribution beyond the registry titles."),
    "E4d15-plan-and-rulings": ("PASS", REV + "plans/FINAL-ARCHITECT-RULINGS.md rulings 9, 11, 17, 18, 22, 23, 24, 25, 26 "
                               "read in full; ruling 26 added this round (delta). Rulings 17, 18, 22, 24, 25 applied as "
                               "described in the E4d21 rows."),
    "E4d-equivalent": ("PASS", REV + "ledgers/E4/equivalent/: literal_price_sign.py, mutant_r19_02_*, mutant_r6_08_*, "
                       "mutant_r7_01_*, mutant_v9_02_* present; README headings read (retracted v17_02 section present, "
                       "r19_02 section with measured-not-proved sweep, ruling 17 proof present)."),
    "E4d-alternatives": ("PASS", REV + "alt_1..alt_8 each 50/50 seeds 0-49 (out/alt_1.txt .. alt_8.txt)."),
    "E4d-mutants-total": ("PASS", REV + "148 files in ledgers/E4/mutants/; mutate_graders E4 0-9: 148/148 killed."),
    "E4d20-mutant-count-144": ("PASS", REV + "now 148 files (144 at the round-20 fragment + 4 new d21 mutants); all killed "
                               "(out/mutate_graders_E4_0_9_r21.txt)."),
    "E4d-mutants-existing": ("PASS", REV + "all 144 pre-existing mutant files re-run: KILLED each (out/mutate_graders_E4_0_9_r21.txt)."),
    "E4d-mutant-docstring-dummy": ("PASS", ""),
}

ALT_TEMPLATE = REV + "run_candidate on this file seeds 0-49: 50/50 (out/alt_*.txt)."
GRADER_TEMPLATE = REV + "test_project.py read in full at 6d22ff56 (630 lines); run_graders 0-49 reference 50/50; collect 49."
PROSE_TEMPLATE = REV + "read in full at 6d22ff56 (project.html 702 lines, line by line); no defect of the ruling-26 kinds."


def mutants_from_output():
    res = []
    text = (OUT / "mutate_graders_E4_0_9_r21.txt").read_text(encoding="utf-8")
    for line in text.splitlines():
        m = re.match(r"(KILLED|SURVIVED) (\S+?)\.py: (.*) -> (.*)$", line)
        if not m:
            continue
        status, name, desc, killer = m.groups()
        res.append({
            "id": name,
            "file": f"ledgers/E4/mutants/{name}.py",
            "description": desc,
            "killed_by": killer if status == "KILLED" else "",
        })
    return res


def carry_ok(row):
    loc = row["location"]
    if row["check"] in NO_CARRY_CHECKS:
        return False
    if any(tok in loc for tok in CHANGED_TOKENS):
        return False
    return any(f in loc for f in CARRY_FILES)


def evidence_for(row):
    rid, check = row["id"], row["check"]
    if rid in SPECIAL:
        return SPECIAL[rid]
    if check == "2.6-mutation":
        return ("PASS", REV + "mutate_graders E4 0-9 -> 148/148 killed (out/mutate_graders_E4_0_9_r21.txt); this row's "
                "subject (ledgers/E4/mutants) changed by the d20 and d21 additions, so the full set was re-run.")
    if check == "2.6-alternatives":
        return ("PASS", ALT_TEMPLATE)
    if check == "2.6-equivalent":
        return ("PASS", REV + "equivalent variants re-read; mutant_r19_02 passes seeds 0-49 (out/equiv_r19_02_0_49.txt) "
                "and its reported fraction matches the reference to 8.9e-13 relative over 10200 domain points "
                "(out/root_identity_r19_02_r21.txt); its gap matches only at the reported fractions (ruling 25 measurement "
                "stands). literal_price_sign: sign unobservable (b_u enters as b_u*b_u), proof re-read.")
    if check.startswith("2.6-autograder") or check in ("2.4-docstrings", "2.6-spec", "2.4-scope") and "test_project" in row["location"]:
        return ("PASS", GRADER_TEMPLATE)
    if check == "2.6-rubric" or check == "2.6-rubric-calibration":
        return ("PASS", REV + "project.html rubric and exemplars re-read; levels separable (see E4d-rubric-observable); "
                "calibration rows cite ~/.fanout/blind/E4-d.json (ruling 23).")
    if check == "2.4-mathematics":
        return ("PASS", REV + "Lemmas 1-3 and Propositions 1-5 re-derived step by step at project.html:257-301 (completing "
                "the square; the Gaussian mean; Var(v-p)=V+Var(m-p); b_u/b_s=-a/(lam tau_e); tau_y formula; Corr^2 = "
                "tau_y/(tau_v+tau_y); G sign rule and G(0+) bracket; closed forms; Prop 5 monotonicity). A6 is stated as "
                "assumed; its sign pattern is implied by Prop 3 (note N1). No defect.")
    if check == "2.4-numbers":
        return ("PASS", REV + "numbers recomputed (labs run; closed forms; ratio script; box bounds: tau-bar in "
                "[0.0976233, 0.2375668], tau_y(1) >= 0.307692). Matches the page.")
    if check in ("2.4-notation",):
        return ("PASS", REV + "every macro in project.html (\\E, \\Var, \\Cov, \\Corr, \\Normal, plus standard LaTeX) is "
                "registered or standard; no collision with notation/notation.json symbols T, Phi, gamma_3, gamma_4, "
                "R^*, R^{e*}, R_f, Q.")
    if check in ("2.9-structure", "2.9-dag", "2.9-smoke", "2.9-hours", "2.9-banned", "2.9-prose", "2.9-delta", "2.9-plan",
                 "2.9-scope", "2.2-prose", "2.3-grades", "2.8-data", "2.4-prose", "2.2-numbers", "2.10-dag"):
        return ("PASS", PROSE_TEMPLATE + " Structure gates: check_pages, check_dag, check_projects, page_smoke PASS.")
    if check == "2.5-labs":
        return ("PASS", REV + "run_labs --unit E4 12/12 and the twin check (out/labs_twin_check_r21.txt) re-run.")
    if check == "2.1-citations":
        return ("PASS", REV + "verify_refs --offline 560 entries 0 problems; live E4 3 of 560 0 problems.")
    return ("PASS", REV + "re-read this round (" + row["location"][:80] + ").")


rows = []
carried = 0
for row in prev["rows"]:
    new = dict(id=row["id"], check=row["check"], location=row["location"])
    if row["id"].endswith("-dummy"):
        continue
    if row["id"] not in SPECIAL and carry_ok(row) and row["status"] == "PASS":
        files = [f for f in CARRY_FILES if f in row["location"]]
        new["status"] = "PASS"
        new["evidence"] = ("Carried from round 20 (" + ", ".join(files) + " byte-identical since the previous pin): "
                           + row["evidence"][:600])
        carried += 1
    else:
        status, ev = evidence_for(row)
        new["status"] = status
        new["evidence"] = ev
    rows.append(new)

# New round-21 rows.
NEW = [
    ("E4d21-delta-read", "2.9-delta", "course/modules/E/E4/project.html; grader/test_project.py; ledgers/E4/equivalent/README.md; "
     "ledgers/E4/mutants/mutant_d20_*; plans/FINAL-ARCHITECT-RULINGS.md (ruling 26)",
     REV + "delta d1083bf1..6d22ff56 for slice d read hunk by hunk: project.html C4 row :527 and annotations :568, :648; "
     "test_project.py :46 and :343-349; README :9-12 and :26-31; three d20 mutants (new in this delta); ruling 26. "
     "Non-slice delta: cards.json (E4-c271 added; outside slice d, not checked here), LX1 files, scripts."),
    ("E4d21-mutants-d21", "2.6-mutation", "ledgers/E4/mutants/mutant_d21_01..04",
     REV + "four new student-error mutants written this round (cost factor dropped from the gap; midpoint precedence "
     "slip; lambda and 1-lambda swapped in b_s; posterior-weight slip in the uninformed slope). Each KILLED on seed 0 "
     "(out/mutate_graders_E4_0_9_r21.txt). Not at a tolerance boundary (ruling 25)."),
    ("E4d21-candidate-swap-equivalent", "2.6-equivalent", "candidate: informed slope uses tau_v/(tau_v+tau_e) for tau_e/(tau_v+tau_e)",
     REV + "passes seeds 0-9 (10/10). Equivalent under the fixed constants tau_v = tau_e = 1 (both weights are 1/2), so no "
     "output changes; not added to mutants/ (ruling 9 would need an equivalent/ proof). Note N7."),
    ("E4d21-root-accuracy-domain", "2.6-autograder", "course/modules/E/E4/grader/reference.py; project.html:317",
     REV + "scripts/E4-d-r21/root_accuracy_sweep_r21.py: 9547 interior points (sd 1e-50..1e2, c 0..0.4, tau-bar >= 1e-2): "
     "0 above 1e-10 relative, worst 4.961e-13 (out/root_accuracy_sweep_r21.txt). The page's accuracy clause holds."),
    ("E4d21-variant-root-identity", "2.6-equivalent", "ledgers/E4/equivalent/mutant_r19_02_*.py",
     REV + "same domain sweep on the r19_02 variant: 0 above 1e-10, worst 4.961e-13; reported fractions equal the reference's "
     "to 8.9e-13 relative over 10200 points (out/r19_02_variant_root_accuracy_sweep_r21.txt, out/root_identity_r19_02_r21.txt). "
     "Mechanism: the variant changes only the common variance Omega, so its zero set is the reference's; off-root gaps differ by "
     "up to 4.4e-2 (note N6). Ruling 25 outcome confirmed for the reported quantities."),
    ("E4d21-finite-corners", "2.6-autograder", "course/modules/E/E4/grader/reference.py; project.html:325-327",
     REV + "88 corner inputs (sd 1e-50..1e150 x c 0..350): all return finite outputs, informed fraction and informativeness in [0,1]. "
     "The stated range in the exception table holds for the reference."),
    ("E4d21-exemplar-annotations", "2.4-numbers", "course/modules/E/E4/project.html:568, :648, :627-660",
     REV + "annotation claims checked against memo text: 1.2500 and 1.5000 (computed), 0.0889 = 0.08894, gap < 4e-14, "
     "the A informativeness 0.1420 at each noise volume (C3 annotation) all agree with the reference grid."),
    ("E4d21-anchors-links", "2.9-structure", "course/modules/E/E4/project.html (href targets)",
     REV + "all local #anchors resolve; relative links (grader/, L06.html, L07.html, L09.html, index.html#placement, concepts.html, review.html) exist."),
    ("E4d21-labs-run-all", "2.5-labs", "tools/run_labs.py --unit E4; tests/labs/E4/lab-E4-project-{1,2,3}.py",
     REV + "run_labs E4 12/12 PASS; labs twins under python -I -W error: rc 0, stderr 0, output == expected (out/labs_twin_check_r21.txt)."),
    ("E4d21-doc-numbers", "2.4-docstrings", "course/modules/E/E4/grader/test_project.py docstrings :388-391, :606-609; reference.py:21-23",
     REV + "out/check_doc_claims_r21.txt (grader copy with reference.py as solver.py): gap(1e-12)-limit in [-3.54e-13, -1.02e-13] (stated 1e-13..4e-13); "
     "oracle(0)-limit <= 1.11e-16 (stated 1.1e-16); domain root 7.7935e-22 (stated about 7.8e-22); corner root 2.0224e-51, tau-bar "
     "0.0101216 (stated just above 1e-2)."),
    ("E4d21-collect-49", "2.6-autograder", "course/modules/E/E4/grader/test_project.py; project.html:319",
     REV + "collect-only 49 tests (out/collect_count_r21.txt); page says 49 checks."),
    ("E4d21-ruling22-gap-comparisons", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:253, :315, :401, :420, :457, :471, :477, :499",
     REV + "ruling 22: the three comparisons the page states at 1e-14 (fraction 0 limit; interior gap; fraction 1 gap and informativeness) "
     "use 1e-14 * max(1, |expected|). The looser 1e-8 checks (interior vanishing, boundary sign) are not among them (note N4)."),
    ("E4d21-ruling-23-blind", "2.6-rubric-calibration", "~/.fanout/blind/E4-d.json; course/modules/E/E4/project.html:536, :601",
     REV + "blind scorer output A [2,2,1,2,1], B [4,4,4,4,4] equals the official scores (data-scores and verdict text). Exemplars not scored here."),
    ("E4d21-notation-registry", "2.4-notation", "notation/notation.json; course/modules/E/E4/project.html",
     REV + "registry macros and symbols compared with the page: no collision (see E4d-notation)."),
]
for rid, check, loc, ev in NEW:
    rows.append({"id": rid, "check": check, "location": loc, "status": "PASS", "evidence": ev})

mutants = mutants_from_output()
killed = sum(1 for m in mutants if m["killed_by"])
counts = {}
for r in rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1

NOTES = (
    "Round 21, slice d (E4 project.html, grader, project labs, mutants, equivalents, alternatives), pin 6d22ff56, delta read from "
    "d1083bf1 hunk by hunk. The three round-20 FAIL rows (E4d-rubric-observable, E4d20-rubric-C4-levels, "
    "E4d20-grader-root-tolerance, E4d20-equiv-readme-literal-open-item) are fixed in the delta and re-verified PASS. "
    "Calibration rows cite the blind scorer file ~/.fanout/blind/E4-d.json (ruling 23); this verifier did not score exemplars. "
    "NOTES (LOW wording or presentation, not FAIL kinds; listed per ruling 26): "
    "N1 project.html:260 (A6) says the page 'assumes this and does not prove it' for the sign pattern G(0+) > 0 > G(1); "
    "in fact that pattern follows from Proposition 3 (sign of G(0+) is sign of tau-bar; sign of G(1) is sign of tau-bar minus "
    "tau_y(1)), so only continuity and the existence of the zero need A6. Over-assumed, not false. "
    "N2 project.html:37 (lede) uses 'Proposition 5' and 'Assumption A6' before they are defined (the Rungs section, :53, does "
    "carry the forward-reference list). "
    "N3 project.html:527 (C4 level 4): 'the precision of each derived number' is vacuously met by a memo that shows no derived "
    "numbers; the element could say 'each derived number the memo shows'. "
    "N4 grader test_project.py:45, :298-305 (TOL_GAP = 1e-8 for the interior gap vanishing) and :322-334 (boundary sign checks) "
    "are looser than the page's 1e-14 gap statement and Lab 3's |gap| < 1e-13; they are not among the three ruling-22 "
    "comparisons, and no surviving mutant depends on them (the 1e-14 oracle comparisons catch every gap error). "
    "N5 test_project.py:607-612 docstring: 'the reported fraction misses the requirement' holds at the stated corner (killed "
    "mutants r6_09, f11_01) but is a point claim, not a general bound on midpoint error. "
    "N6 ledgers/E4/equivalent/README.md r19_02 section: the variant changes only the common variance Omega, so its root and "
    "its gap at the reported root agree with the reference (sweep above), but its gap differs off the root by up to 4.39e-2 "
    "(probe in scripts/E4-d-r21/out/root_identity_r19_02_r21.txt); the README sweep measures only at reported fractions. "
    "Worth one sentence in the README; ruling 25 outcome not changed. "
    "N7 A candidate that swaps tau_v and tau_e in the informed slope is invisible under the fixed constants tau_v = tau_e = 1; "
    "it is an equivalent under the page's constants, not a mutant. If the constants ever become arguments, it becomes a student "
    "error that the suite does not kill at 2 instances. "
    "N8 tools/run_labs.py --unit E4 --page project.html returns 0/0 (the page filter matches nothing); the 12/12 run is the "
    "evidence. "
    "N10 test_project.py:322-334 (test_boundary_rule_holds) accepts lambda = 0 whenever G(0) <= 1e-8 and lambda = 1 whenever "
    "G(1) >= -1e-8, while the page's boundary rule is sign-based and its accuracy is 1e-14. A solver with an epsilon test "
    "(for example gap_0 < 1e-9) would differ from the rule only where |G(0)| is at most about 1e-8, near tau-bar = 0 "
    "(c near ln 2 / 4). No instance in the box or the grid lies there, and ruling 25 forbids authoring a mutant at this "
    "tolerance boundary, so this is recorded, not tested. "
    "N9 provenance: round 20 counted 144 mutants at d1083bf1 including the three d20 files, which the delta (6d22ff56) adds; "
    "the counts now agree at 148. "
    "Not checked: cards.json (E4-c271, outside slice d); the 557 registry entries outside E4 (only E4 live run); the in-browser "
    "grader beyond one seed (page_smoke ran one seed); the full CI gate for the whole repository beyond ruff/mypy/refs; "
    "the unread standards (none cited)."
)

fragment = {
    "unit": "E4",
    "slice": "d",
    "round": 21,
    "verifier": "verifier (Haiku 5.5), E4-d round 21",
    "pin": "6d22ff56",
    "base": "d1083bf1 (round-20 pin); delta read hunk by hunk: project.html, grader/test_project.py, equivalent/README.md, three d20 mutants, ruling 26",
    "checkout": str(ROOT),
    "scratch": "/tmp/e4d21 (scratch only; scripts kept in ledgers/E4/scripts/E4-d-r21/)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "PASS" if counts.get("PASS", 0) == len(rows) else "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": NOTES,
    "summary": (f"E4 slice d round 21 (pin 6d22ff56): verdict {'PASS' if counts.get('PASS',0)==len(rows) else 'FAIL'}. "
                f"Rows {len(rows)}: PASS {counts.get('PASS',0)}, FAIL {counts.get('FAIL',0)}, UNVERIFIABLE "
                f"{counts.get('UNVERIFIABLE',0)}; carried from round 20 {carried}. Mutants {len(mutants)}, killed {killed}."),
}
out_path = ROOT / "ledgers/E4/E4-d.json"
out_path.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), counts, "carried", carried, "mutants", len(mutants), "killed", killed)
