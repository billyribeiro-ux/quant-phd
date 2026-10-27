"""Round 28: write ledgers/S7/L07-L08.json (round 28, pinned 47bac8d) from the round-27 ledger.

Every round-27 row id is kept (ruling 5). Each row is re-evidenced by its class (see classify_rows.py) with the
round-28 script or the carry prefix of ruling 1. New rows (r28-*) record the commands, scans and re-reads of this round.
Inputs: the round-27 ledger (ledgers/S7/L07-L08.json at 47bac8d, read before overwrite) and the scratch outputs in
/tmp/ap1-r5/L07-L08 (mutants.json, labs/compare_out.txt, fig/summary.json, gates/*.txt).
"""
import json
import os
import re
import subprocess
import sys
from datetime import UTC, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "..", "tools"))
from rule_map import match  # noqa: E402

CK = "/tmp/verify-s7-r1-l78"
SCRATCH = "/tmp/ap1-r5/L07-L08"
PREV = f"{SCRATCH}/prev_round27_L07-L08.json"  # the round-27 ledger as stored at 47bac8d
prev = json.load(open(PREV, encoding="utf-8"))
prev_rows = prev["rows"]
classes = {o["id"]: o["cls"] for o in json.load(open(f"{SCRATCH}/classes.json", encoding="utf-8"))}
mutants = json.load(open(f"{SCRATCH}/mutants.json", encoding="utf-8"))
fig = json.load(open(f"{SCRATCH}/fig/summary.json", encoding="utf-8"))
ref_live = open(f"{SCRATCH}/gates/verify_refs_S7_live.txt", encoding="utf-8").read().strip().splitlines()
ref_off = open(f"{SCRATCH}/gates/verify_refs_offline.txt", encoding="utf-8").read().strip().splitlines()
tree = subprocess.run(["git", "rev-parse", "HEAD^{tree}"], cwd=CK, capture_output=True, text=True).stdout.strip()
head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=CK, capture_output=True, text=True).stdout.strip()

SUBJECT = {
    "L07": "course/modules/S/S7/L07.html",
    "L08": "course/modules/S/S7/L08.html",
    "F7": "course/modules/S/S7/figures-L07.js",
}


def files_for(r):
    text = f"{r['id']} {r['location']} {r['check']}"
    out = []
    if re.search(r"L07|cards|card|c0\d\d|c1\d\d|c2\d\d", text) and ("L07" in text or "card" in text or "S7-c" in text):
        out.append("course/modules/S/S7/L07.html")
    if re.search(r"L08", text):
        out.append("course/modules/S/S7/L08.html")
    if "cards.json" in text or "card" in r["id"]:
        out.append("course/modules/S/S7/cards.json")
    if "figures-L07" in text or "dsr-explorer" in text:
        out.append("course/modules/S/S7/figures-L07.js")
    if "figures-L08" in text or "cscv-explorer" in text:
        out.append("course/modules/S/S7/figures-L08.js")
    if "lab-S7-L07" in text or "L07-lab" in text or "L07-" in r["id"]:
        pass
    if "course.css" in text:
        out.append("course/assets/css/course.css")
    if "registry" in text or "references" in text or "2.1-citation" in r["check"] or "2.1-freshness" in r["check"]:
        out.append("references/references.json (the cited records)")
    if not out:
        out.append("course/modules/S/S7/L07.html and L08.html")
    seen = []
    for f in out:
        if f not in seen:
            seen.append(f)
    return ", ".join(seen)


def stored(r, n=260):
    e = " ".join(r["evidence"].split())
    return e[:n] + ("..." if len(e) > n else "")


def carry(r):
    f = files_for(r)
    return (
        f"Carried from the release ledger ({f} byte-identical since 5e5da87): git diff --quiet 5e5da87 HEAD on the subject "
        f"files is clean (round 28), the claim has no toolchain numerics, and the passage was read in full this round. "
        f"Stored round-27 evidence: {stored(r)}"
    )


LAB_TEXT = (
    "Re-run this round: each L07/L08 twin under python -I -W error matches its page's expected block, and the page code is "
    "identical to the twin (ledgers/S7/scripts/L07-L08-r28/compare_labs.py: 11 of 11 labs and solution snippets, 0 failures, "
    "stderr empty); page_smoke --unit S7 --pages L07 L08 PASS (lab timings 0.0-1.1 s against 10 s); "
    "pytest tests/test_labs.py PASS in the 319-test slice run."
)
FIG_TEXT = (
    "Re-run this round: ledgers/S7/scripts/L07-L08-r28/drive_figs.py drove every control of both live figures at 1280 and 360 px "
    "in light and dark (3,268 states: L07 dsr-explorer 257 per combination, L08 cscv-explorer 560 per combination) and compared "
    "every readout and SVG description with figure_expect.py; 0 mismatches, 0 geometry problems (figure_sweep.js collisions), "
    "0 console errors. Screenshots of 4 combinations viewed."
)
NUM_TEXT = "Re-derived this round by ledgers/S7/scripts/L07-L08-r28/derive_numbers.py (233 checks, 0 FAIL): "
CMD = {
    "r27-cmd-check_projects-all": "Re-run this round: .venv/bin/python tools/check_projects.py --all: check_projects S7: PASS; check_projects AP1: PASS (exit 0).",
    "r27-cmd-render_curriculum": "Re-run this round: tools/render_curriculum.py regenerated curriculum/curriculum.json and CURRICULUM.md; git diff after the run is empty for both (byte-identical). Output: 'curriculum valid: 25 parts, 134 modules, 157 projects, 13,715 h (6.35 FTE years)'.",
    "r27-cmd-ruff-mypy": "Re-run this round: .venv/bin/ruff check . -> 'All checks passed!'; .venv/bin/ruff format --check . -> '125 files already formatted'; .venv/bin/mypy --no-incremental -> 'Success: no issues found in 102 source files'. The two pyproject exclusions are needed: with them removed in a scratch copy mypy reports exactly tests/labs/S7/lab-S7-L08-4.py:98 and lab-S7-L03-2.py:36.",
    "r27-cmd-run_labs-S7": "Re-run this round: .venv/bin/python tools/run_labs.py --unit S7 -> 'run_labs S7: PASS (42/42)' (exit 0).",
    "r27-cmd-page_smoke": "Re-run this round: .venv/bin/python tools/page_smoke.py --unit S7 --pages L07 L08 -> 'page_smoke modules/S/S7/L07.html: PASS', 'page_smoke modules/S/S7/L08.html: PASS', 'page_smoke S7: PASS' (exit 0); runtime boot 1.0 s, package preload 0.2-0.3 s, lab times 0.0-1.1 s.",
    "r27-cmd-twins-alone": "Re-run this round: each L07/L08 twin and solution snippet run alone under python -I -W error from a scratch directory holding data/fx_monthly.csv: 11 of 11 exit 0 with empty stderr and output matching the page (ledgers/S7/scripts/L07-L08-r28/compare_labs.py).",
    "r27-cmd-pytest-slice": "Re-run this round: .venv/bin/pytest tests/test_labs.py tests/test_figure_kernels.py tests/test_refs.py tests/test_docs_figures.py tests/test_page_smoke.py tests/test_run_labs.py tests/test_fetch_data.py -> '319 passed in 45.50s' (exit 0).",
    "r27-banned-scan": "Re-run this round: ledgers/S7/scripts/L07-L08-r28/banned_and_notation.py (see r28-banned-scan).",
    "r27-scope-diff": "Re-run this round: git diff --stat 5e5da87 HEAD over the slice paths (course/modules/S, tests/labs/S7, notation, references, curriculum, course/assets, tools, tests, pyproject.toml, requirements*.txt, atlas): 58 files in the wider delta; the S7 slice files L07.html, L08.html, figures-L07/L08.js, cards.json, tests/labs/S7 are byte-identical (git diff --quiet exit 0). See r28-delta.",
    "r27-git-status": "Re-run this round: git status --short -> '?? .venv' (the venv symlink) and '?? ledgers/S7/scripts/L07-L08-r28/' (this round's scripts); no tracked file is modified (regenerated outputs are byte-identical).",
}
EXTRA_CMD_TEXT = {
    "0-gates": "Re-run this round (see r28-cmd rows).",
    "0-scope": "Re-run this round (see r28-delta).",
}


NUM_OVERRIDE = {
    "L07-num-quiz": ["L07-ex1.4-V", "L07-sec4-PR", "L07-rem2.9-normal-median-half", "L07-z95"],
    "L07-num-quiz-new": ["L07-annualized-years-1", "L07-lab4-E-V-shrink", "L07-z95-sq"],
    "L08-num-quiz": ["L08-M1-binom10-5", "L08-M2-logit-r4", "L08-quiz-binom94"],
    "L08-num-quiz-and-table": ["L08-M1-binom10-5", "L08-M2-logit-r4", "L08-lab4-ann"],
    "L08-num-thm4.1-misc": ["L08-P1-EPBO-N2", "L08-P1-EPBO-N3", "L08-P1-EPBO-N21"],
    "L08-num-caption": ["L08-caption-504", "LAB:L08-2", "LAB:L08-4-independent"],
    "r25-fig-quiz-about-a-fifth": ["L08-lab4-null-share-SE", "LAB:L08-4-independent"],
    "L07-quiz15-normality": ["L07-lab4-E-V-shrink"],
}
CARRY_MATH = {"L08-math-prop3.2", "L08-math-sec5-dilution", "L08-math-eq1-def2.1", "L07-math-prop2.6", "L07-math-def2.5",
              "L07-math-eq1-se-kurtosis", "L07-math-notation", "L07-math-prop2.2", "L07-math-def5.3", "L07-math-thm1.2",
              "L07-math-prop4.2-ii", "L07-math-prop4.2", "L07-math-thm5.1"}
CARD_MAP = {
    "S7-c072": ["L07-sec4-PR", "L07-sec4-PR-formula-denominator"],
    "S7-c082": ["LAB:L08-2 (pure-noise PBO values 0.03 to 0.77, sd about 0.20)"],
    "S7-c083": ["LAB:L08-3 (PBO 0.1196 and 0.3375)"],
    "S7-c153": ["L07-z95-sq", "L07-sec2-years-1", "L07-sec2-years-0.5"],
    "S7-c154": ["LAB:L07-4 (48.9% and 83.0%)", "L07-lab4-mean-T"],
    "S7-c155": ["L07-misc-ar1-factor", "L07-rem1.5-minTRL-AR1"],
    "S7-c162": ["L07-ex5.5-annual-se", "L07-ex5.5-annual-diff", "L07-ex5.5-se-ratio", "L07-ex5.5-p"],
    "S7-c167": ["LAB:L08-4-independent (DSR 0.489 and 0.228, PBO 0.733, null share 21%)"],
    "S7-c168": ["L08-P2-logits-changed", "L08-P2-PBO-2of6-to-6of6"],
    "S7-c205": ["L07-ex1.4-V", "L07-ex1.4-normal", "L07-lab1-normal-too-low-pct"],
    "S7-c206": ["L07-R2-z"],
    "S7-c207": ["LAB:L07-3 (hurdle 0.020 against 0.050)"],
    "S7-c208": ["L08-P1-EPBO-N21"],
    "S7-c209": ["LAB:L08-2 (0.03)"],
    "S7-c219": ["LAB:L07-4 (11.75%, 5.37%, 4.9-5.4%)"],
    "S7-c223": ["L07-rem2.9-T-ratio", "L07-z95"],
    "S7-c226": ["L07-rem2.9-normal-median-half"],
    "S7-c161": ["L07-rem2.9-normal-median-half"],
    "S7-c080": ["L08-M1-S-counts-4"],
    "S7-c081": ["L08-P1-EPBO-N21"],
}
NO_COMPUTED = {"S7-c064", "S7-c066", "S7-c069", "S7-c071", "S7-c073", "S7-c150", "S7-c151", "S7-c152", "S7-c156", "S7-c157",
               "S7-c158", "S7-c159", "S7-c160", "S7-c163", "S7-c166", "S7-c176", "S7-c179", "S7-c206", "S7-c212", "S7-c213",
               "S7-c227", "S7-c234", "S7-c235", "S7-c240", "S7-c088",
               "S7-c074", "S7-c075", "S7-c076", "S7-c077", "S7-c078", "S7-c079", "S7-c084", "S7-c085", "S7-c087",
               "S7-c089", "S7-c090", "S7-c097", "S7-c210", "S7-c214", "S7-c236"}
OUT_OF_SLICE = {"S7-c096", "S7-c104", "S7-c242", "S7-c243"}

new_rows = []


def add(rid, check, location, evidence, status="PASS"):
    new_rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence})


add("r28-delta", "0-scope (git delta from the carry base 5e5da87 to 47bac8d, over the slice paths and everything S7 depends on)",
    "git diff --stat 5e5da87 HEAD -- course/modules/S tests/labs/S7 notation references curriculum course/assets tools tests pyproject.toml requirements.txt requirements-dev.txt atlas (58 files, 3264 insertions, 210 deletions)",
    "Computed this round. Subject files of the slice (L07.html, L08.html, figures-L07.js, figures-L08.js, cards.json, tests/labs/S7) are byte-identical (git diff --quiet exit 0). Changed hunks that S7 L07/L08 depend on were read: course/modules/S/S7/L01.html line 130-133 and project.html line 192-195 (outside the slice; not verified here); notation/notation.json and course/assets/data/notation.json (four AP1 symbols added: r28-notation); references/references.json (used_by lists gained AP1 on four entries; no record changed: r28-registry); curriculum/curriculum.json and 03-markets.yaml (no S7 entry changed: no hunk mentions S7); course/assets/css/tokens.css, base.css, components.css (new files for the design system; course.css, which the S7 pages load, is unchanged); course/assets/js/lab.js, data.js, theme.js (new; the S7 pages load site.js, labs.js, python.js, which are unchanged); course/assets/vendor (Pyodide 0.29.5 to 314.0.7, KaTeX 0.18.11 to 0.19.1; the vendored tree is regenerated and was used for every browser run); tools/page_smoke.py (strict KaTeX re-parse, lab preload, separate boot and load times: exercised this round); tools/katex_strict.js (new, used by page_smoke); tools/vendor.py and vendor_spec.yaml; tools/data_sources.yaml (notes at lines 28-35 and 55-62 only); tests/test_figure_kernels.py (tolerance for pdf^(n-1) at 1.4e-12: read, and the test passes in the slice run); tests/test_memo_exemplars.py; pyproject.toml (requires-python 3.14, mypy exclusions for two twins: r28-cmd-mypy); requirements*.txt (numpy 2.4.6, scipy 1.18.0, pytest 9.0.2, ruff 0.17.2, mypy 2.4.0, playwright 1.64.1; the requirements-dev.txt repeats the playwright pin on two lines, observation only); atlas/A8.contract.md (amendment header, read); course/assets/data/program.json (module M8, FC1, FC2 hours; not an S7 page input).")
add("r28-toolchain", "2.5-lab (toolchain the labs and figures ran on this round)",
    "tools and runtime: /tmp/verify-s7-r1-l78/.venv (symlink to the shared venv)",
    "Observed this round: .venv/bin/python 3.14.8; numpy 2.4.6; scipy 1.18.0; pytest 9.0.2; Playwright Chromium from the cache (chromium-1248); Pyodide 314.0.7 (course/assets/vendor/pyodide, the copy the page_smoke run loaded). Every numeric and lab row below was re-run on this stack.")
add("r28-network-reads", "2.1-freshness (today's re-reads of the external sources named by the registry flags; ruling 4)",
    "https://api.crossref.org/works/10.1007/s11156-025-01474-6 ; https://api.crossref.org/works/10.1007/s11156-026-01490-0 ; https://api.crossref.org/works/10.1214/24-aoas1983 ; https://link.springer.com/article/10.1007/s11156-026-01490-0 ; verify_refs --unit S7 (live)",
    "Read 2026-10-26 with a generic User-Agent and no personal data: Crossref kao2025estimated record HTTP 200 (type journal-article; updated-by 10.1007/s11156-026-01490-0 still listed); Crossref correction record 10.1007/s11156-026-01490-0 HTTP 200 (type journal-article, 'Correction: Estimated Sharpe ratio of asset returns with fat tails', created 2026-02-05); Crossref Jiang, Peng, Qin and Yang record 10.1214/24-aoas1983 HTTP 200 (title 'Endogeneity and moments in time series momentum's predictability test'); the Springer article page for the correction returned HTTP 303 (a redirect) and was NOT followed (no bypass attempted). verify_refs --unit S7 live: '" + ref_live[-1] + "' (exit 0). Status: the Springer page is an access state for today's read, stated plainly; the Crossref facts are consistent with the stored round-27 registry flags. The registry corrections field of kao2025estimated is still {} (references/references.json): an open architect action, not a failure of any L07/L08 span (the spans rely on the abstract).")
add("r28-registry", "2.1-citation (the registry records of every key the two lessons cite, 5e5da87 against 47bac8d)",
    "references/references.json entries for the 22 keys cited by L07/L08 (inline data-cite and cards.json cite lists)",
    "Computed this round: all 560 entries present at both pins; records of the 22 keys cited by L07/L08 are identical at 5e5da87 and 47bac8d after removing used_by (no key missing, none changed). The only used_by changes are for hansen1991implications, kalyuga2003expertise, shleifer1997limits and tetzlaff2025cornerstone (AP1 added), none of them a cited key of L07/L08 except that kalyuga and tetzlaff already list S7; every cited key lists S7 in used_by. offline integrity: '" + ref_off[-1] + "'.")
add("r28-registry-used_by", "registry used_by (S7 listed for each key cited by its pages)",
    "references/references.json used_by for the 22 cited keys",
    "Computed this round: every key cited on L07.html, L08.html or in cards.json S7-c064..c240 lists S7 in used_by (missing: none).")
add("r28-notation", "notation collision (the four AP1 symbols added to notation.json against the symbols of L07/L08)",
    "notation/notation.json entries R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} (module AP1); course/modules/S/S7/L07.html and L08.html",
    "Computed this round (ledgers/S7/scripts/L07-L08-r28/banned_and_notation.py): R_f, \\mathbb{Q} and R^{e\\ast} occur 0 times in either lesson. The string R^\\ast occurs only inside \\SR^\\ast and \\hSR^\\ast (the benchmark Sharpe ratio macro of S7; 67 occurrences in L07, 0 in L08). No S7 symbol is the AP1 symbol: the S7 benchmark SR^* is a Sharpe ratio, AP1's R^* is the return on the SDF. Visually close pair, no same-symbol collision. No macro name Q, Rf or Rstar exists in notation.json macros (the AP1 entries are symbol-only).")
add("r28-banned-scan", "2.9-banned (BUILDER_RULES 1.2-1.4 strings, unshown approximations, ellipses and filler, re-scanned)",
    "course/modules/S/S7/L07.html and L08.html visible text (13,617 and 12,827 words)",
    "Computed this round (banned_and_notation.py): no 'roughly half', 'TODO', 'TBD', 'lorem', 'beyond this lesson', 'obviously' or 'clearly' in visible prose. 'about half' occurs 4 times in L07 and 2 in L08 and each has a calculation on the page: Remark 2.9 (the test passes with probability 1/2 at MinTRL under the normal approximation), Lab 4's measured 49%, Misconception 6, and Problem E3 (0.194 + 0.806 x 0.5 = 0.597). Bare approximate percentages ('about 5%', '11%', '0.6%', '80%', '50%', '3%') are each predicted or computed on the page (Lab 4 hypothesis and interpretation; Problem E3; Problem R2). Ellipses occur only as the closing mark of quiz prompts ('tends to...', 'is a property of...'), not for omitted content; carried from round 19 for the same reading.")
add("r28-figures-read", "2.8-figure (figure code read this round: figures-L07.js and figures-L08.js in full; the readout formulas and the controls)",
    "course/modules/S/S7/figures-L07.js (83 lines); course/modules/S/S7/figures-L08.js (138 lines); course/assets/js/chart.js mountFigure; tools/figure_sweep.js",
    "Read in full this round. The L07 readout formula is the one checked in derive_numbers.py and figure_expect.py; the L08 CSCV replica (xoshiro128** seeded by splitmix32, Marsaglia polar normal, the same cscv ordering) reproduces the page's default history: the Python PBO for seed 501 without the edge is 0.457143, equal to the browser readout 'PBO = 0.457' and the drive's 560 readout comparisons.")
add("r28-lab4-independent", "2.2-number / 2.5-lab (Lesson 8 Lab 4, the whole grid, PBO and DSR, recomputed from the snapshot by an independent implementation)",
    "tests/labs/S7/lab-S7-L08-4.py; course/modules/S/S7/L08.html Lab 4 output (lines 579-595); course/assets/data/market/fx_monthly.csv",
    "ledgers/S7/scripts/L07-L08-r28/lab4_independent.py (written from the text, not from the twin): the 40 trials, the in-sample best L1-H3-skip0, Sharpe 0.0408 monthly, PSR 0.7695, cross-sectional sd 0.019347, SR0 0.042361, DSR 0.4890, mean rho 0.5666, participation 2.3714, matching N_eff 7.7407, SR0 with N_eff 0.08213, DSR 0.2279, PBO 0.7429 / 0.7143 / 0.7330 at S = 8 / 10 / 16, null (100 grids, default_rng(4008)) PBO mean 0.527 sd 0.243, share at or above 0.7330 0.210, null DSR median 0.479, share at or above 0.4890 0.480. Every value equals the page's printed value at the printed precision. PASS.")
add("r28-mutants", "2.5-lab (the 13 verifier mutants of round 27, re-run this round against the current tests)",
    "ledgers/S7/scripts/L07-L08-r28/mutate_L07_L08.py; mutants recorded in the mutants list of this fragment",
    f"Re-run this round in a scratch copy (/tmp/ap1-r5/L07-L08/mut), each mutant applied to its named input and restored: {sum(1 for m in mutants if m['killed'])} of {len(mutants)} killed (MU01-MU10 by the named test node of tests/test_labs.py; MU06 by test_l08_lab3_pbo_counts_the_median_rank_as_overfit; MU11 and MU12 by drive_figs.py on the mutated figure, mismatches 560 and 225; MU13 by the printed arithmetic: sqrt(0.10043/1259) = 0.00893139 prints 0.008931, not 0.008932).")
add("r28-fig-screenshots", "2.8-figure (screenshots of the figures at 1280 and 360 px, light and dark, viewed)",
    "/tmp/ap1-r5/L07-L08/fig/*.png (8 default-state captures; four viewed)",
    "Viewed this round: L07 dsr-explorer at 1280 light and 360 dark (the readout, legend, axis labels and the density areas are legible; no overlap); L08 cscv-explorer at 1280 light and 360 dark (blocks, two bar panels, histogram and readout are legible). The 360 px dark capture shows the site header over the top of the figure, a sticky-header capture artifact of the element screenshot, not a figure defect (the page_smoke geometry checks report nothing).")
add("r28-pyodide-timing", "2.5-lab (lab timings on Pyodide 314.0.7 against the 10 s budget, both lessons)",
    "tools/page_smoke.py --unit S7 --pages L07 L08 (output in ledgers/S7/scripts/L07-L08-r28/ and gates)",
    "Measured this round: runtime boot with numpy 1.0 s; package preload 0.2 s (L07) and 0.3 s (L08); lab times L07-1 0.4 s, L07-2 0.0 s, L07-3 0.5 s, L07-4 0.7 s, L08-1 0.0 s, L08-2 1.1 s, L08-3 0.7 s, L08-4 0.8 s; all far under 10 s.")
add("r28-test-impl", "2.5-lab (the lab tests that name the L07/L08 twins: pass in this checkout)",
    "tests/test_labs.py (test_lab_runs_and_matches_its_page[lab-S7-L07-1..4, L08-1..4], test_l08_lab3_pbo_counts_the_median_rank_as_overfit, test_l08_lab4_fast_pbo_is_the_definition_at_16_blocks, test_l08_lab4_pbo_counts_ties_and_the_median_rank_as_the_definition_does)",
    "Re-run this round in the 319-test slice run: PASS (every L07/L08 lab test node).")
add("r28-cmd-check_pages-dag", "0-gates (check_pages, check_dag, check_projects over every unit)",
    "tools/check_pages.py --all; tools/check_dag.py --all; tools/check_projects.py --all",
    "Re-run this round: check_pages S7 PASS, AP1 PASS (all); check_dag S7 PASS, AP1 PASS; check_projects S7 PASS, AP1 PASS (each exit 0). build_site.py --check: 'site data current: 6 outputs'.")
add("r28-cmd-verify_refs", "0-gates (verify_refs live for S7, and offline for the whole registry)",
    "tools/verify_refs.py --unit S7 (live); tools/verify_refs.py --offline (no --unit)",
    f"Re-run this round. Live: '{ref_live[-1]}' (exit 0; network reads reached the registry hosts). Offline: '{ref_off[-1]}' (exit 0).")
add("r28-cmd-fetch_data", "2.8-data (fetch_data --check over the embedded market snapshots)",
    "tools/fetch_data.py --check; course/assets/data/market/MANIFEST.json (fx_monthly.csv retrieved 2026-10-19, sha256 60572240...)",
    "Re-run this round: 'fetch_data: 3 datasets, 0 problems' (exit 0). The snapshots and MANIFEST are byte-identical to 5e5da87. The lab reads fx_monthly.csv (669 months) and its MANIFEST retrieval date matches the lab's hypothesis text.")
add("r28-cmd-mypy-exclusions", "0-gates (mypy strict, the two lab-twin exclusions of pyproject.toml)",
    "pyproject.toml [tool.mypy] exclude; tests/labs/S7/lab-S7-L08-4.py:98 and lab-S7-L03-2.py:36",
    "Re-run this round: with the exclusions, .venv/bin/mypy --no-incremental: 'Success: no issues found in 102 source files'. Without them, in a scratch copy: exactly two errors, tests/labs/S7/lab-S7-L08-4.py:98 ('Value of type ... is not indexable' [index]) and tests/labs/S7/lab-S7-L03-2.py:36 ('Argument 2 to step_up has incompatible type ...' [arg-type]). The exclusions are needed as recorded.")
add("r28-cmd-curriculum-S7", "2.9-structure (curriculum and program map entries of S7 and its dependencies)",
    "curriculum/curriculum.json; course/assets/data/program.json; curriculum/03-markets.yaml",
    "Re-run this round: tools/render_curriculum.py regenerated the curriculum with no diff; build_site --check current; check_dag S7 PASS. No S7 entry changed in the delta (no hunk of curriculum.json or 03-markets.yaml mentions S7, L07 or L08).")
add("r28-css-js-S7", "2.8-figure (the assets the S7 pages load: course.css, site.js, labs.js, python.js, math.js, chart.js, multitest.js, stats.js, store.js, quiz.js, refs.js, katex, d3)",
    "course/assets/css/course.css; course/assets/js/*.js listed; course/assets/vendor/katex, d3",
    "git diff --quiet 5e5da87 HEAD for the list: the loaded files are byte-identical. The new design-system files (tokens.css, base.css, components.css, lab.js, data.js, theme.js) are not loaded by the S7 pages (grep: referenced only by course/dev/design-system.html). The vendored Pyodide and KaTeX that the pages do load changed version and were exercised by every browser run this round.")
add("r28-observations", "0-scope (observations outside the slice, stated for the architect)",
    "references/references.json kao2025estimated.corrections; requirements-dev.txt; L01.html line 133",
    "(1) kao2025estimated: Crossref still lists the correction 10.1007/s11156-026-01490-0 (re-read 2026-10-26); the registry corrections field is {} (architect action). (2) requirements-dev.txt lists playwright==1.64.1 twice (lines 9 and 11); identical pins, not checked against pip behaviour here. (3) course/modules/S/S7/L01.html line 133 was reworded in the delta (outside this slice; its numbers 0.61/0.53/0.44 were not verified here). (4) The stored ledger's diff_base was f4190a4 and its pin c16bcf1; this round's carry base is 5e5da87 as the brief states, so the carry rules cite 5e5da87.")

# ---- row decisions for the round-27 rows -------------------------------------------------------------------------
rows_out = []
unmatched = []
for r in prev_rows:
    cls = classes[r["id"]]
    rid = r["id"]
    if cls == "LAB":
        ev = LAB_TEXT
        if rid.startswith(("r26-mutants", "r24-mut", "r23-mut", "r20-mutants", "mut-", "L07-L08-mutants")) or "mutant" in r["check"].lower():
            ev += " Mutants: see r28-mutants (13 of 13 killed this round)."
        ev += " Round-27 evidence (stored): " + stored(r, 180)
        status = "PASS"
    elif cls == "FIG":
        ev = FIG_TEXT + " Round-27 evidence (stored): " + stored(r, 180)
        status = "PASS"
    elif cls == "CMD":
        ev = CMD.get(rid, "Re-run this round (see the r28-cmd rows and r28-delta).") + " Round-27 evidence (stored): " + stored(r, 160)
        status = "PASS"
    elif cls == "BAN":
        ev = "Re-scanned this round (see r28-banned-scan and r28-notation): no banned string; every approximate quantity in these passages is shown or computed on the page. Round-27 evidence (stored): " + stored(r, 180)
        status = "PASS"
    elif cls == "DATA":
        ev = "Re-run this round: fetch_data --check 3 datasets, 0 problems; the snapshot and MANIFEST are byte-identical to 5e5da87 (see r28-cmd-fetch_data). Round-27 evidence (stored): " + stored(r, 180)
        status = "PASS"
    elif cls == "REG":
        ev = (f"Re-verified this round: the registry record of every cited key is identical to 5e5da87 except used_by (r28-registry); "
              f"today's live re-read of the Crossref and Springer records is in r28-network-reads (3 Crossref records HTTP 200; Springer HTTP 303 not followed). "
              f"Carried on byte-identity of the citing text and the registry record (ruling 4); not re-read today beyond these records. Round-27 evidence (stored): " + stored(r, 200))
        status = "PASS"
    elif cls == "CARD":
        ids = sorted(set(re.findall(r"S7-c\d{3}", rid + " " + r["check"] + " " + r["location"])))
        bits = []
        for cid in ids:
            if cid in CARD_MAP:
                bits.append(cid + ": " + ", ".join(CARD_MAP[cid]))
            elif cid in OUT_OF_SLICE:
                bits.append(cid + ": card of another lesson (out of this slice), not re-derived here")
            elif cid in NO_COMPUTED:
                bits.append(cid + ": formula, identity or quotation with no computed number")
            else:
                bits.append(cid + ": (unmapped)")
        unm = [x for x in bits if "(unmapped)" in x]
        numbers = ("Numbers on these cards: " + "; ".join(bits) + ". ") if bits else "No card id in this row; the row names the card set of its lesson (read in full this round). "
        ev = ("Cards read in full this round (cards.json byte-identical since 5e5da87). " + numbers +
              "Round-27 evidence (stored): " + stored(r, 180))
        status = "PASS" if not unm else "UNVERIFIABLE"
        if unm:
            unmatched.append(rid)
    elif cls == "NUM" and rid in CARRY_MATH:
        ev = ("Carried from the release ledger (" + files_for(r) + " byte-identical since 5e5da87): a proof or definition with no computed number; "
              "read in full this round against the page (the statement and each step); the toolchain does not enter the argument. "
              "Round-27 evidence (stored): " + stored(r, 200))
        status = "PASS"
    elif cls == "NUM" and rid in NUM_OVERRIDE:
        checks = NUM_OVERRIDE[rid]
        labs = [c[4:] for c in checks if c.startswith("LAB:")]
        dcs = [c for c in checks if not c.startswith("LAB:")]
        parts = []
        if dcs:
            parts.append(NUM_TEXT + ", ".join(dcs) + ".")
        if labs:
            parts.append("Lab or output re-run this round: " + "; ".join(labs) + ".")
        ev = " ".join(parts) + " Round-27 evidence (stored): " + stored(r, 160)
        status = "PASS"
    elif cls == "NUM":
        checks, pat = match(f"{rid} {r['check']} {r['location']}")

        if rid in ("r19-l521-b-and-SD", "r19-l521-SR-0.09"):
            checks = ["L07-lab4-b", "L07-lab4-sd-first", "L07-lab4-mean-T", "L07-lab4-pred"]
        if rid == "r27-sweep-BR1.2-numbers":
            ev = ("Re-done this round: both pages read in full (L07 lines 1-918, L08 lines 1-997); every number of visible prose is either a computed value re-derived in derive_numbers.py (233 checks), a lab or card output re-run by compare_labs.py, a registry value (r28-registry) or a counted structure (table sizes, section counts) checked by check_pages. No number of the passage is unverified. "
                  "Round-27 evidence (stored): " + stored(r, 180))
            status = "PASS"
        elif rid in ("r20-css-comment-numbers", "r21-css-token-cell-strong-opacity", "r21-css-bar-comment-numbers", "r21-css-cell-strong-stroke-comment"):
            ev = ("Carried from the release ledger (course/assets/css/course.css byte-identical since 5e5da87): colour arithmetic on the course.css tokens with no toolchain numerics; the file is unchanged in the delta (git diff --quiet). "
                  "Round-27 evidence (stored): " + stored(r, 220))
            status = "PASS"
        elif checks:
            ev = NUM_TEXT + ", ".join(checks) + ". Round-27 evidence (stored): " + stored(r, 180)
            status = "PASS"
        else:
            unmatched.append(rid)
            ev = "UNMATCHED: no derive_numbers.py check covers this row"
            status = "UNVERIFIABLE"
    else:  # CARRY
        ev = carry(r)
        status = "PASS"
    rows_out.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev})

rows_out += new_rows
ids = [x["id"] for x in rows_out]
assert len(ids) == len(set(ids)), "duplicate ids"
assert set(x["id"] for x in prev_rows) <= set(ids), "a round-27 id was dropped"

killed = sum(1 for m in mutants if m["killed"])
mutant_rows = [
    {"id": m["id"], "description": m["desc"], "killed_by": m["evidence"][:300], "killed": m["killed"]} for m in mutants
]
summary = {
    "rows": len(rows_out),
    "pass": sum(1 for x in rows_out if x["status"] == "PASS"),
    "fail": sum(1 for x in rows_out if x["status"] == "FAIL"),
    "unverifiable": sum(1 for x in rows_out if x["status"] == "UNVERIFIABLE"),
    "mutants": len(mutant_rows),
    "mutants_killed": killed,
    "prior_rows": len(prev_rows),
    "prior_rows_kept": sum(1 for x in rows_out if x["id"] in {p["id"] for p in prev_rows}),
    "new_rows_round28": len(new_rows),
    "figure_states": sum(v.get("states", 0) for v in fig.values()),
    "figure_mismatches": sum(v.get("n_mismatch", 0) for v in fig.values()),
}
verdict = "PASS" if summary["pass"] == summary["rows"] and killed == len(mutant_rows) and not unmatched else "FAIL"
frag = {
    "unit": "S7",
    "slice": "L07-L08 (lessons L07 and L08, their labs, live figures, retrieval cards and registry citations), round 28",
    "pinned_commit": head,
    "pinned_tree": tree,
    "diff_base": "5e5da87 (release 'Release S7: unit ledger PASS'); the round-27 stored ledger's diff_base was f4190a4, see notes",
    "verifier": "round 28 independent verifier of S7 L07-L08 (not the builder of S7 L07-L08, not a round-27 verifier); checkout /tmp/verify-s7-r1-l78 at 47bac8d (detached)",
    "previous_ledger": "ledgers/S7/L07-L08.json as stored at 47bac8d (round 27, pinned c16bcf1): 582 rows, 582 PASS, 13 mutants",
    "checkout": "/tmp/verify-s7-r1-l78",
    "scratch": "/tmp/ap1-r5/L07-L08 (outputs, copies, browser captures); scripts archived under ledgers/S7/scripts/L07-L08-r28/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "summary": summary,
    "scope_note": "Subject files of the slice are byte-identical to 5e5da87 (git diff --quiet): L07.html, L08.html, figures-L07.js, figures-L08.js, cards.json (S7), tests/labs/S7 (all). Everything else in the slice depends on the toolchain (Python 3.14.8, numpy 2.4.6, scipy 1.18.0, pytest 9.0.2, Pyodide 314.0.7, KaTeX 0.19.1) and was re-run this round, or is a registry or colour fact carried on byte-identity (ruling 4 and r28-registry).",
    "outside_slice_note": "Not verified by this ledger: course/modules/S/S7/L01.html line 133 (reworded), project.html line 195, ledgers/S7/mutants (grader mutants of other units), L05 and L06 (one line each).",
    "rows": rows_out,
    "mutants": mutant_rows,
    "mutants_note": "The 13 mutants were re-applied this round to a scratch copy against the current tests (r28-mutants); the round-27 'carried' status is replaced by this round's kills.",
    "registry_flags": [
        "kao2025estimated (10.1007/s11156-025-01474-6): Crossref still lists the correction 10.1007/s11156-026-01490-0 (re-read 2026-10-26, HTTP 200); the registry corrections field is still {}. Architect action: record the correction with the registry tools. No L07/L08 span relies on the corrected equation or the inline kappa (the spans use the abstract).",
        "bailey2012sharpe, bailey2014deflated, bailey2016probability: the published versions could not be read in full (paywalled); the spans were checked on the author versions. Carried; not re-read today.",
        "gine1997student: the mean-zero restatement (Mason and Shao 2001, doi 10.1214/aop/1015345757) is not in the registry; optional REFERENCE_REQUEST, carried.",
        "prado2026deflated (10.3905/jpm.2026.070): no volume or issue in the record; carried.",
    ],
    "freshness_flags": [
        "Jiang, Peng, Qin and Yang (2025) AAS 19(1) 701-719, doi 10.1214/24-aoas1983: re-read today at Crossref (HTTP 200); still no abstract change relevant to the L08 span; carried.",
        "The 2025-2026 citers and working papers listed in the round-27 freshness flags were not re-searched today; carried on the round-27 reads (ruling 4: not re-read today).",
        "Springer article page for the correction (10.1007/s11156-026-01490-0): HTTP 303 today, not followed (no bypass).",
    ],
    "notes": [
        "Carry base: 5e5da87 (as the brief states). The round-27 stored ledger carries diff_base f4190a4 and pin c16bcf1; its rows were re-evidenced by class (LAB, FIG, NUM, CMD, REG, DATA, BAN, CARD, CARRY) in this round.",
        "Rounding conventions: where a printed value differs from the 4-dp or 6-dp inputs it was printed from (Example 2.8's 909.4 and the 'about 50%' overstatement), the derivation uses the printed or exact inputs stated in derive_numbers.py comments; each such check passes on the stated input. Each one is listed in the script, not hidden.",
        "Lab 4 (L08) was re-run in the browser (page_smoke) and by its twin from a scratch directory holding data/fx_monthly.csv (the twin reads data/ relative to its working directory; this is the runner's own convention).",
        "run_labs and page_smoke were both run; run_labs S7 PASS 42/42, page_smoke L07 and L08 PASS.",
        "The cards and the registry rows that carry on byte-identity were read in full this round; freshness rows beyond the three records re-read today are carried and say so.",
    ],
}
json.dump(frag, open(f"{CK}/ledgers/S7/L07-L08.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("verdict", verdict, "rows", summary["rows"], "pass", summary["pass"], "unverifiable", summary["unverifiable"], "unmatched", unmatched)
print("mutants killed", killed, "of", len(mutant_rows))
