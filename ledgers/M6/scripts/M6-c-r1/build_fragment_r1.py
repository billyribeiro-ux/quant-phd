import json

ROOT = "/Users/billyribeiro/.fanout/wt/verifyF21-M6-c"
BASE_FRAG = "/Users/billyribeiro/.fanout/frags/C-M6-c.round6.json"
OUT = f"{ROOT}/ledgers/M6/M6-c.json"
PIN = "95f3f8cb21c2cd9fc904430bd30a6b734d01f672"
BASE_PIN = "9fd6aedde63046c002ed77af5b5152daf84a3abf"
S = "ledgers/M6/scripts/M6-c-r1"

base = json.load(open(BASE_FRAG, encoding="utf-8"))
base_rows = {r["id"]: r for r in base["rows"]}

SLICE_PAGES = (
    "course/modules/M/M6/L09.html, L10.html, L11.html, L12.html, tests/labs/M6/lab-M6-L09-1.py to L12-1.py, "
    "course/modules/M/M6/index.html, notation/"
)
SLICE_CARDS = (
    "course/modules/M/M6/cards.json objects M6-c085..c101, c103..c108, c114..c136, c142..c146 "
    "(M6-c109 absent at both pins; c137 removed and c102, c110, c141 changed are re-verified fresh, see "
    f"{S}/card_delta_r1.out)"
)


def carry(rid, files):
    row = dict(base_rows[rid])
    assert row["status"] == "PASS", rid
    row["evidence"] = (
        f"Carried from round 6 (byte-identical since the previous pin 9fd6aed: {files}): " + row["evidence"]
    )
    return row


NEW_CHECKS = {
    "c-delta-cited-lessons": "Delta: every L07 and L08 locator the slice cites is re-read after the hunks that changed these lessons",
}


def fresh(rid, location, evidence):
    return {
        "id": rid,
        "check": base_rows[rid]["check"] if rid in base_rows else NEW_CHECKS[rid],
        "location": location,
        "status": "PASS",
        "evidence": evidence,
    }


rows = []

# ---- commands re-run fresh on the pin ----
rows.append(fresh(
    "c-cmd-run-labs", "tests/labs/M6/lab-M6-L09-1.py .. lab-M6-L12-1.py",
    f"`.venv/bin/python tools/run_labs.py --unit M6` -> `run_labs M6: PASS (15/15)`, exit 0 ({S}/run_labs_M6.out)."))
rows.append(fresh(
    "c-cmd-twins-alone", "tests/labs/M6/lab-M6-L09-1.py .. L12-1.py; L09-L12.html lab sections",
    "Each twin run alone as `.venv/bin/python -I -W error tests/labs/M6/lab-M6-Lnn-1.py` from a scratch directory: "
    "exit 0, stderr 0 bytes, stdout 17/12/18/26 lines for L09/L10/L11/L12 "
    f"({S}/twin-L09..L12.out/.err). Page code equals twin and expected block equals twin output: checked by "
    "run_labs.py, which passes (row c-cmd-run-labs)."))
rows.append(fresh(
    "c-cmd-check-pages", "course/modules/M/M6/L09.html .. L12.html",
    f"`.venv/bin/python tools/check_pages.py --unit M6` -> `check_pages M6: PASS`, exit 0 ({S}/check_pages_M6.out); "
    f"`--page L09` -> `check_pages M6 L09: PASS` ({S}/check_pages_M6_hub.out). Includes the cards.json schema check."))
rows.append(fresh(
    "c-cmd-page-smoke", "course/modules/M/M6/L09.html .. L12.html",
    "`.venv/bin/python tools/page_smoke.py --unit M6 --pages L09 L10 L11 L12` -> `page_smoke M6: PASS`, exit 0; "
    f"every page PASS with its lab run in the browser ({S}/page_smoke_M6_L09_12.out)."))
rows.append(fresh(
    "c-cmd-check-dag", "course/modules/M/M6/*.html",
    f"`.venv/bin/python tools/check_dag.py --all` exit 0; line `check_dag M6: PASS` ({S}/check_dag_all.out)."))
rows.append(fresh(
    "c-cmd-ruff-mypy-pytest", "tests/labs/M6/lab-M6-L09-1.py .. L12-1.py",
    f"`ruff check tests/labs/M6` -> `All checks passed!`; `ruff format --check tests/labs/M6` -> `15 files already "
    f"formatted` ({S}/ruff_check_M6_labs.out, ruff_format_M6_labs.out). `mypy --no-incremental` -> `Success: no issues "
    f"found in 386 source files`, exit 0 ({S}/mypy_nocache.out). `pytest -k M6` -> 15 passed, exit 0 "
    f"({S}/pytest_M6_only.out; tests/test_labs.py and tests/test_run_labs.py -k M6 also pass). Outside this slice: "
    f"`pytest -k 'M6 or lab'` also collects tests/test_lx1_project_lab3.py, whose "
    f"test_a_population_sd_variant_of_the_two_pass_check_raises fails at HEAD ({S}/pytest_labs_M6.out)."))
rows.append(fresh(
    "c-cmd-verify-refs", "references/references.json; L09-L12 references sections",
    "`.venv/bin/python tools/verify_refs.py --offline` -> `offline integrity: 560 entries, 0 problems`, exit 0 "
    f"({S}/verify_refs_offline.out). references.json changed since 9fd6aed only in generated_at and in the used_by "
    "lists of BK1/BK4, DV1/FC2 and E9/LX1 (git diff, 11 lines): no M6 key changed. `tools/render_curriculum.py` then "
    "`git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json` exit 0 "
    f"({S}/render_curriculum.out, curriculum_diff.out). `tools/build_site.py --check` -> `site data current: 6 outputs`, "
    f"exit 0 ({S}/build_site_check.out). `tools/fetch_data.py --check` -> `3 datasets, 0 problems` "
    f"({S}/fetch_data_check.out). Live verify_refs not run (no M6 reference changed)."))

# ---- subjects byte-identical since 9fd6aed: carried ----
rows.append(carry("c-structure-sections", SLICE_PAGES))
rows.append(fresh(
    "c-why-words", "course/modules/M/M6/L09.html..L12.html line 52; L07.html line 136",
    "L10 line 52 'assuming Assumption CE of L07' is defined at course/modules/M/M6/L07.html line 136 "
    "('Assumption CE (not proved here)'); that line is unchanged by the L07 delta, whose only hunk is line 105. "
    "L12 line 52 'under the orthogonality hypothesis of section 1 (Assumption OA, defined there)': the definition is at "
    "L12 line 59 inside section 1 (header line 54), both unchanged. L09 and L11 line 52 unchanged. Process-word grep of "
    f"the four stripped texts ({S}/m6c_L09..L12.txt): none."))
rows.append(carry("c-notation", SLICE_PAGES))
rows.append(carry("c-cards-L09", SLICE_CARDS + "; course/modules/M/M6/L09.html and tests/labs/M6/lab-M6-L09-1.py"))
rows.append(fresh(
    "c-cards-L10", "course/modules/M/M6/cards.json M6-c102, c141 (changed), c137 (removed); c101, c103..c105, c142 unchanged",
    "M6-c102 (changed front and back): 'With capital K = 1000 cents, does the doubling strategy's high win probability "
    "make its expected final wealth exceed K?' -> wins with probability 1 - 2^(-m) = 0.9980468750, ruin leaves 489 cents, "
    "expected final wealth exactly K (Proposition 10.7). Checked against L10 line 134 (ruin 2^(-m), wealths K+1 and "
    "K+1-2^m, expectation K), lines 139-141 (algebra), line 295 (Lab 1 Part A prints 0.9980468750 and wealth_on_ruin "
    "489), and lines 302 and 320 (489 cents; exactly K). Re-derived: m = 9, 1 - 2^-9 = 511/512 = 0.998046875, "
    "K+1-2^9 = 489, E = 1000 (ledgers/M6/scripts/M6-c-r1/rederive_r1.out). "
    "M6-c141 (changed): 'stopped gain on the all-loss branch {tau > n} and its probability' -> D_(tau^n) = -(2^n - 1) "
    "cents and P(tau > n) = 2^-n (Example 10.8). Checked against L10 line 150, which states P(tau > n) = 2^-n and "
    "D_(tau^n) = -(2^n - 1) on {tau > n}; re-derived for n = 1, 2, 3, 5, 10 (rederive_r1.out: -1, -3, -7, -31, -1023) and "
    "matches Lab 1 Part B lines 297-301 (wealth_when_all_lose). Both are grade T, and both rest on proved content "
    "(Proposition 10.7; Example 10.8 with the independence argument). M6-c137 (removed): no card or lesson refers to it "
    f"({S}/cards_checks_r1.out). M6-c101, c103..c105 and c142 are byte-identical since 9fd6aed ({S}/card_delta_r1.out); "
    "re-read this round against L10 lines 159, 169, 302-310 and 324: each agrees with the current text."))
rows.append(fresh(
    "c-cards-L11", "course/modules/M/M6/cards.json M6-c106..c108, c110 (changed), c111..c113, c148 (added)",
    "M6-c110 (changed): 'E[S_N^2] = N, from the independence and zero mean of the steps (Problem R3)'. L11 Problem R3 "
    "solution (line 240): E[S_N^2] = sum E[X_i X_j], zero for i != j by independence and zero mean, E[X_i^2] = 1, so N. "
    "Re-derived for N = 1..12 by exact enumeration (rederive_r1.out). The Doob bound previously on c110 is now on M6-c148 "
    "(added): 'P(max over k <= N of |S_k| >= c) <= N/c^2 for c > 0; Problem R3 derives it from Corollary 11.4 with "
    "Z_k = S_k^2 and E[S_N^2] = N'. Checked against L11 line 125 (Corollary 11.4 holds under the assumptions of Theorem "
    "11.3, a nonnegative submartingale), line 240 (R3: Z_k = S_k^2 is a nonnegative submartingale, integrable since "
    "S_k^2 <= k^2, and Corollary 11.4 with lambda = c^2 gives N/c^2) and line 398 (key result, T, from Problem R3). The "
    "card carries its hypothesis through 'the fair walk' (Lemma 11.2, line 66: independent steps +1 or -1 with probability "
    "1/2, S_0 = 0). M6-c106 agrees with L11 line 60 (the CE qualifier); M6-c107 with Lemma 11.2; M6-c108 with the Theorem "
    "11.3 statement (lines 92-100); M6-c111 with Corollary 11.4 and Definition 11.1; M6-c112 and c113 with Part A and "
    "Part C output (lines 237-253: largest ratio 1.000000 at N = 1, 2, 4; bound_holds False at N = 1, 2). M6-c109 is absent "
    "at both pins (a gap; ruling 2). Cards c112 and c113 carry no grade key at either pin."))
rows.append(carry("c-cards-L12-c114", SLICE_CARDS + " (M6-c114, c118, c122 and c143..c146 included)"))
rows.append(carry("c-cards-L12-others", SLICE_CARDS + " (M6-c115..c124, c128, c129 included)"))
rows.append(fresh(
    "c-cards-dup", "course/modules/M/M6/cards.json",
    f"Python check ({S}/cards_checks_r1.py -> cards_checks_r1.out): 141 cards, duplicate ids 0, duplicate fronts 0, ids "
    f"prefixed M6-c, and every number token in the card text of the L09-L12 cards and of c147-c149 appears in its own "
    f"lesson (none missing). Per-card delta since 9fd6aed ({S}/card_delta_r1.out): added M6-c147, c148, c149; removed "
    f"M6-c049, c137; changed c002, c007, c017, c044, c062, c102, c110, c130, c141. The slice-c changes are verified in the "
    f"rows above; the others belong to other slices and are not verified here."))

rows.append(carry("c-lab-L09-claims", SLICE_PAGES))
rows.append(carry("c-lab-L10-claims-partB", SLICE_PAGES))
rows.append(carry("c-lab-L10-claims-partA", SLICE_PAGES))
rows.append(carry("c-lab-L11-claims", SLICE_PAGES))
rows.append(carry("c-lab-L12-claims", SLICE_PAGES))
rows.append(carry("c-num-L09", SLICE_PAGES))
rows.append(carry("c-num-L10", SLICE_PAGES))
rows.append(carry("c-num-L11-E2-rounding", SLICE_PAGES))
rows.append(carry("c-num-L11-other", SLICE_PAGES))
rows.append(carry("c-num-L11-signed", SLICE_PAGES))
rows.append(carry("c-num-L12", SLICE_PAGES))
rows.append(carry("c-num-L12-E1", SLICE_PAGES))
rows.append(carry("c-math-L09", SLICE_PAGES))
rows.append(carry("c-math-L10", SLICE_PAGES))
rows.append(carry("c-cond-misconception-L10", SLICE_PAGES))
rows.append(carry("c-math-L11", SLICE_PAGES))
rows.append(carry("c-math-L12-orthogonality-general", SLICE_PAGES))
rows.append(carry("c-math-L12-prop12.8b", SLICE_PAGES))
rows.append(carry("c-math-L12-prop12.8ac-prop12.10", SLICE_PAGES))
rows.append(carry("c-math-L12-R-problems", SLICE_PAGES))

rows.append(fresh(
    "c-defn-before-use", "course/modules/M/M6/L10.html line 52; L12.html lines 52, 59; L07.html line 136",
    "L10 line 52 names 'Assumption CE of L07', defined at L07 line 136 (unchanged; the L07 delta edited line 105 only). "
    "L12 line 52 names Assumption OA, defined at L12 line 59 inside section 1 (header line 54). L09 and L11 line 52 use no "
    "undefined name. Numbered forward references follow the unit's style."))
rows.append(carry("c-process-words-and-scope", SLICE_PAGES))
rows.append(fresh(
    "c-dag-links", "L09-L12 concept links; L10 line 52; L07 line 136",
    f"`tools/check_dag.py --all` exit 0; `check_dag M6: PASS` ({S}/check_dag_all.out). The prose link 'Assumption CE of "
    "L07' (L10 line 52) points to an earlier lesson of the same module; L07 changed only line 105, so the target is "
    "unchanged."))
rows.append(fresh(
    "c-attribution", "L09 line 55; L10 lines 56, 60; L11 lines 56, 60; L12 line 56; L07 lines 83, 134-136; L08 lines 59, 64, 73, 88",
    "Re-read after the L07 and L08 hunks: L08 Definition 1.1 (filtration) line 59, Definition 1.2 (natural filtration) line 64, "
    "Proposition 2.1 (natural filtration of the walk) line 73 and Definition 2.2 (martingale) line 88 are unchanged in "
    "content. The L08 hunks (lines 52 and 56) edit prose; line 52 now names Definition 1.2 for the natural filtration, "
    "consistent with line 64. L07 Theorem 2.2 (cell average, projection) line 83, Remark 2.6 and Assumption CE lines "
    "134-136: unchanged. The L07 hunk (line 105, Remark 2.3) is not cited by the slice. No bibliographic data cited."))
rows.append(carry("c-quiz-explain", SLICE_PAGES))
rows.append(carry("c-ddg-grades", SLICE_PAGES))
rows.append(carry("c-hours", SLICE_PAGES))
rows.append(fresh(
    "c-delta-r6-subject", "L07.html line 105; L08.html lines 52, 56; cards.json slice-c objects; L09-L12 unchanged",
    f"Every hunk of git diff 9fd6aed..HEAD touching the slice's subjects was read ({S}/card_delta_r1.out and the diffs): "
    "L07 one hunk at line 105 (Remark 2.3 prose); L08 two hunks at lines 52 and 56 (prose, and p(omega) to w(omega) in "
    "section 1); cards.json slice-c objects M6-c102, c110, c141 (changed), M6-c148 (added) and M6-c137 (removed), each "
    "read in the rows above. The L09-L12 pages, their four twins, the hub index.html and notation/ have no diff "
    "(git diff --quiet)."))
rows.append(fresh(
    "c-delta-cited-lessons", "course/modules/M/M6/L07.html lines 83, 104-105, 134-136; L08.html lines 52, 56, 59, 64, 73, 88",
    "The slice cites L07 and L08 locators (rows c-attribution, c-why-words, c-defn-before-use, c-dag-links). Both lessons "
    "changed since 9fd6aed, so each cited locator was re-read this round: L07 line 83 (Theorem 2.2) and line 136 "
    "(Assumption CE); L08 lines 59, 64, 73, 88 (Definitions 1.1 and 1.2, Proposition 2.1, Definition 2.2). Each still "
    "exists with the content the slice relies on. Line numbers are unchanged because each hunk replaces single lines "
    "(hunk headers @@ -102,7 +102,7 @@ for L07 and @@ -49,11 +49,11 @@ for L08)."))

# ---- standing mutant set (ruling 37: no new mutants) ----
standing = [
    ("ledgers/M6/mutants/m6c_r6_L09_depends_always_true.py", "L09",
     "Student-error mutant of the L09 twin: the depends check returns True for every event (line 51 gains 'or True')."),
    ("ledgers/M6/mutants/m6c_r6_L09_depends_check_skipped.py", "L09",
     "Student-error mutant of the L09 twin: the path-agreement check is skipped (line 61 'if False:')."),
    ("ledgers/M6/mutants/m6c_r6_L10_ruin_off_by_one.py", "L10",
     "Student-error mutant of the L10 twin: ruin tested with stake >= wealth (refuses the exact-fit bet)."),
    ("ledgers/M6/mutants/m6c_r6_L11_grid_drops_last.py", "L11",
     "Student-error mutant of the L11 twin: the Doob grid drops its last lambda value (range(1, 2(N+1)))."),
    ("ledgers/M6/mutants/M6-c-r4/m_r4_L10_loss_branch_plus_one.py", "L10",
     "Round-4 mutant of the L10 twin: the no-win branch returns net + 1."),
    ("ledgers/M6/mutants/M6-c-r3/m_c_L10_no_stop_on_win.py", "L10",
     "Round-3 mutant of the L10 twin: the win test is flip == 2 (the process never stops on a win)."),
    ("ledgers/M6/mutants/M6-c-r3/m_c_L10_wins_pay_zero.py", "L10",
     "Round-3 mutant of the L10 twin: a win returns net without the stake."),
]
mutants = []
for path, tw, desc in standing:
    name = path.rsplit("/", 1)[-1][:-3]
    mutants.append({
        "id": name,
        "description": f"{desc} File {path}; the twin differs by one line.",
        "killed_by": (
            f"Run alone under python -I -W error: stdout differs from the {tw} twin output (the expected-block "
            f"comparison of run_labs fails); exit 0 with empty stderr ({S}/mut/{name}.out vs twin_{tw}.out). "
            "Lab twins are demonstrations, so the kill is recorded, not graded as a grader mutant."
        ),
    })

notes = [
    "Closing delta (ruling 30) for slice c, from base pin 9fd6aed (round-6 fragment /Users/billyribeiro/.fanout/frags/C-M6-c.round6.json, round 6 by its own name) to pin 95f3f8cb. The round field is 1 as instructed for this verification.",
    "Subjects since 9fd6aed: L09-L12 pages, their four twins, the hub index.html and notation/ are byte-identical. L07 (one prose line, 105) and L08 (two prose lines, 52 and 56) changed and are cited by the slice; every cited locator was re-read. cards.json: slice-c objects M6-c102, c110, c141 changed (grades unchanged, all T), M6-c148 added, M6-c137 removed (card_delta_r1.out).",
    "Not verified here (other slices): the L04 twin, the M6 L01-L06 pages, and cards M6-c002, c007, c017, c044, c049, c062, c130, c147, c149.",
    "Rows whose subject is byte-identical since 9fd6aed carry the round-6 evidence under the carry prefix. Gates were re-run; changed cards and cited lessons were re-read. Base row ids are kept; c-delta-r6-subject and c-delta-cited-lessons are the delta rows.",
    "No new mutants authored (ruling 37). The seven standing mutants touching this slice were re-run against the current twins; each one's stdout differs from the twin output, so all seven are killed.",
    "Observed outside the slice, not graded: `pytest -k 'M6 or lab'` selects tests/test_lx1_project_lab3.py, whose test test_a_population_sd_variant_of_the_two_pass_check_raises fails at HEAD (LX1). The M6 selection passes (15 passed).",
    "Observed outside the slice, not a finding for slice c: notation of path weights differs between lessons. L08 section 1 now writes the weight as w(omega) (line 56), while L07 Remark 2.3 keeps p(omega) (line 105) and L08 section 2 uses p for the up-step probability.",
    "42 M6 cards carry no grade key (check_pages accepts this, and it is the pin's state). Not a finding for slice c.",
    "Not run: live verify_refs and the project graders (slice c has no grader and no reference change).",
]

summary = (
    "M6-c round 1 (closing delta from base 9fd6aed to 95f3f8cb): PASS. All rows PASS. Fresh: the gates (run_labs 15/15, "
    "twins alone exit 0, check_pages, page_smoke L09-L12, check_dag, ruff, mypy 386 files, pytest -k M6 15 passed, "
    "verify_refs offline 560/0, render_curriculum diff, build_site --check, fetch_data --check) and the changed cards "
    "(M6-c102, c110, c141; added c148; removed c137) with the cited L07/L08 locators. Carried: rows whose subjects are "
    "byte-identical since 9fd6aed. Seven standing mutants killed; no new mutants (ruling 37)."
)

fragment = {
    "unit": "M6",
    "slice": "c",
    "round": 1,
    "verifier": "Claude Haiku 5.5, independent verifier for M6-c, closing delta round 1 (did not build M6; no shared context with the builders)",
    "pin": PIN,
    "base": f"{BASE_PIN} (round-6 fragment {BASE_FRAG})",
    "checkout": ROOT,
    "scratch": f"{ROOT}/{S}/",
    "verified_at": "2026-11-09T16:00:00+00:00",
    "verdict": "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": summary,
}

with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
print("rows", len(rows), "PASS", sum(r["status"] == "PASS" for r in rows), "mutants", len(mutants))
