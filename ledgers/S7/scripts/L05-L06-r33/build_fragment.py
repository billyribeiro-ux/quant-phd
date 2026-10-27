"""Round-33 fragment builder for S7 L05-L06 (verifier output; decisions are explicit below).

Reads the round-32 ledger from git (47bac8d), decides each of its 604 row ids for round 33 and writes
ledgers/S7/L05-L06.json. Every decision is one of: fresh PASS (cites a command or script run this round),
carried (subject files byte-identical since 5e5da87, prefix as the brief requires), token-checked (a lab
output number found in an expected block that run_labs matched this round), or UNVERIFIABLE (named reason).
Run from the checkout: .venv/bin/python -I ledgers/S7/scripts/L05-L06-r33/build_fragment.py
"""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

ROUND = 33
PRIOR = json.loads(subprocess.run(["git", "show", "47bac8d:ledgers/S7/L05-L06.json"], capture_output=True, text=True,
                                  check=True, cwd=ROOT).stdout)
PAGE = {n: (ROOT / "course/modules/S/S7" / f"{n}.html").read_text(encoding="utf-8") for n in ("L03", "L05", "L06")}
EXPECTED = re.compile(r'<pre class="expected"[^>]*>(.*?)</pre>', re.S)
TAGS = re.compile(r"<script.*?</script>|<style.*?</style>|<[^>]+>", re.S)
NUM = re.compile(r"-?\d+(?:\.\d+)?(?:e-?\d+)?")
EXP_TOKENS: dict[str, list[float]] = {}
for name, src in PAGE.items():
    text = " ".join(html.unescape(TAGS.sub(" ", b)) for b in EXPECTED.findall(src))
    EXP_TOKENS[name] = [float(t) for t in NUM.findall(text)]


def in_expected(value: float, decimals: int, pages: tuple[str, ...], scale: float = 1.0) -> bool:
    """True if an expected-block token equals value*scale at the given decimals (scale 100 for percentages)."""
    target = round(value * scale, decimals)
    for page in pages:
        for token in EXP_TOKENS[page]:
            if abs(round(token, decimals) - target) < 1e-9 or abs(token - value * scale) < 0.5 * 10 ** (-decimals) + 1e-12:
                return True
    return False


# Lab-output numbers quoted in prose: (value, decimals, pages, percent scale)
LAB_TOKENS: dict[str, list[tuple[float, int, tuple[str, ...], float]]] = {
    "L05-num-lab4": [(v, 3, ("L05",), 1) for v in (2.785, 2.189, 0.455, 0.848, 0.963, 0.988, 0.950, 0.943, 0.951,
                                                   1.960, 3.023, 3.031, 2.508)],
    "L05-num-lab5": [(v, 4, ("L05",), 1) for v in (0.0913, 0.0690, 0.0496, 0.0150, 0.1060, 0.0610)],
    "L05-num-lab2-interpretation": [(0.223, 3, ("L05",), 1), (0.035, 3, ("L05",), 1), (1.645, 3, ("L05",), 1)],
    "L05-num-lab1-interpretation": [(5.798, 3, ("L05",), 1), (5.596, 3, ("L05",), 1), (0.031, 3, ("L05",), 1)],
    "L05-lab3-line898-duplicates": [(1.601, 3, ("L05",), 1), (2.566, 3, ("L05",), 1)],
    "L05-num-s8-lab6": [(v, 3, ("L05",), 1) for v in (1.105, 1.645, 2.935, 2.837, 3.032, 0.853, 0.821)] +
                       [(0.221, 3, ("L05",), 1), (14, 0, ("L05",), 1)],
    "L05-hunk-873-other-numbers": [(v, 3, ("L05",), 1) for v in (1.105, 1.645, 2.935, 0.221, 2.837, 3.032, 0.853, 0.821)]
                                  + [(14, 0, ("L05",), 1)],
    "L05-lab6-ties": [(14, 0, ("L05",), 1)],
    "L06-num-lab1": [(v, 2, ("L06",), 1) for v in (4.56, 3.51, 3.64)],
    "L06-num-lab2": [(0.493, 3, ("L06",), 1), (0.0517, 4, ("L06",), 1), (13.3, 1, ("L06",), 1), (0.060, 3, ("L06",), 1)],
    "L06-num-lab3": [(0.1278, 4, ("L06",), 1), (0.5238, 4, ("L06",), 1)],
    "R31-num-L05-lab3-333": [(1.601, 3, ("L05",), 1), (2.566, 3, ("L05",), 1), (1.645, 3, ("L05",), 1),
                             (2.568, 3, ("L05",), 1)],
    "R31-L05-line333-never-favours": [(1.601, 3, ("L05",), 1), (2.566, 3, ("L05",), 1), (1.645, 3, ("L05",), 1),
                                      (2.568, 3, ("L05",), 1)],
    "R26-l03-lab3-quotes": [(0.0913, 4, ("L03",), 1)],
    "R29-num-crosslesson-10.6": [(0.1060, 3, ("L03",), 1)],
}

FRESH = {
    # 2.0-diff: this round's delta over the slice is empty (every slice file byte-identical to 5e5da87)
    "diff": "Fresh (round 33): git diff --quiet 5e5da87 HEAD -- course/modules/S/S7/L05.html course/modules/S/S7/L06.html "
            "course/modules/S/S7/figures-L05.js course/modules/S/S7/figures-L06.js course/modules/S/S7/cards.json and the "
            "23 lab twins and solution snippets of L05-L06: every file exits 0 (identical). The unit-wide delta "
            "(git diff --stat 5e5da87 HEAD, 229 files) touches the shared assets, notation, registry, tools and the "
            "L01 line 133 and project.html lines only; every hunk that touches S7 or that S7 depends on was read "
            "(see notes).",
    "lab": "Fresh (round 33): tools/run_labs.py --unit S7 printed 'run_labs S7: PASS (42/42)' (python -I -W error, "
           "scratch data directories, output compared with each page's expected block); tools/page_smoke.py --unit S7 "
           "--pages L05 L06 PASS with labs L05-1 0.3 s, L05-2 0.9 s, L05-3 0.1 s, L05-4 1.3 s, L05-5 0.4 s, L05-6 1.3 s, "
           "L06-1 0.3 s, L06-2 0.9 s, L06-3 0.0 s (budget 10 s; boot 1.0 s and numpy preload 0.2 s charged separately); "
           "tests/test_labs.py, test_run_labs.py run this round: 138 passed with test_figure_kernels, test_page_smoke, "
           "test_docs_figures, test_js (log /tmp/ap1-r5/L05-L06/pytest_slice.out).",
    "figure": "Fresh (round 33): ledgers/S7/scripts/L05-L06-r33/drive_figures.py drove every control of every figure on "
              "L05 and L06 in Chromium at 1280 and 360 px, light and dark (20 chart instances; 101 t-values of "
              "bayes-posterior, all three alpha values of hurdle-growth, both buttons of stepm-steps at 1280 light). "
              "Every readout matched the Python recomputation (ledgers/S7/scripts/L05-L06-r33/figure_readouts.py; "
              "log /tmp/ap1-r5/L05-L06/drive.out: problems=0 console_errors=0 external=0 states=20). Screenshots "
              "read: light 1280 and dark 360 for each figure (10 images under /tmp/ap1-r5/L05-L06/drive/).",
    "data": "Fresh (round 33): tools/fetch_data.py --check: 3 datasets, 0 problems; the fx_daily snapshot was rebuilt "
            "from the live Federal Reserve feed in a scratch copy (tools/fetch_data.py --fetch --only fx_daily): "
            "sha256 02872dd7e23938da1b14da0e085c03f566e48a323c41de76b2c56fed98ad9b59 = MANIFEST sha256 (byte-identical "
            "rebuild, 6706 rows); raw_sha256 today 17d087d0ebb2a0ac1a7c0feed844ecb5ca0410c4ae64582b2030233bdeb352e4 "
            "differs from the recorded 8f370f9c57b73e1c0b68a2ee72ddecd3abaffb21fa627fcfd4f8a3612798c6a8 (the issuer's "
            "live file changed; the provenance hash is not expected to reproduce, BUILDER_RULES 6.6); MANIFEST and the "
            "repository were not changed. Licence re-read today: https://www.federalreserve.gov/disclaimer.htm HTTP 200 "
            "contains 'Unless otherwise indicated, information on Board's website is in the public domain and may be "
            "copied and distributed without permission'; https://www.federalreserve.gov/releases/h10/about.htm HTTP 200, "
            "'Last Update: February 06, 2023'.",
    "structure": "Fresh (round 33): tools/check_pages.py --all: S7 PASS, AP1 PASS; tools/check_dag.py --all: S7 PASS, AP1 "
                 "PASS; tools/check_projects.py --all: S7 PASS, AP1 PASS; tools/build_site.py --check: 'site data current: "
                 "6 outputs'; tools/render_curriculum.py regenerated CURRICULUM.md and curriculum/curriculum.json with "
                 "git diff --exit-code clean; ruff check (All checks passed), ruff format --check (125 files formatted), "
                 "python -m mypy --no-incremental (Success: no issues found in 102 source files); page_smoke L05 and L06 "
                 "PASS (zero console errors, zero external requests, strict KaTeX parse, every chart carries <title> and "
                 "<desc>, no horizontal scroll at 360 px).",
    "banned": "Fresh (round 33): banned strings of BUILDER_RULES 1.2-1.4 and 3 (TODO, TBD, lorem, for brevity, details "
              "omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, "
              "experts agree, it is well known, obviously, clearly, roughly half, historically, it can be shown that, "
              "ellipses) searched in the visible text of course/modules/S/S7/L05.html and L06.html (tags, scripts and "
              "styles removed): 0 hits. Card scan (243 S7 cards): hits only in L08 cards (S7-c168, S7-c179: the word "
              "'omitted' in a non-banned sense), none in L05-L06.",
    "cards": "Fresh (round 33): course/modules/S/S7/cards.json is byte-identical to 5e5da87 (git diff --quiet). Whole-file "
             "scan of 243 cards: ids unique, no banned phrase in L05 or L06 cards.",
    "notation": "Fresh (round 33): notation/notation.json adds R^\\ast, R^{e\\ast}, R_f and \\mathbb{Q} (AP1). None of these "
                "four symbols occurs in course/modules/S/S7/L05.html or L06.html (grep: 0 hits). The plain letter Q occurs "
                "twice with a local definition: L06.html line 276 ('Write Q = 1 - Phi') and L05.html line 596 (the inverse "
                "of the covariance matrix); neither is the registered \\mathbb{Q}. No collision with a registered symbol; "
                "flagged for the builder (registry_flags).",
    "registry": "Fresh (round 33): references/references.json compared entry by entry with 5e5da87: 560 entries in both, "
                "the only changed fields are generated_at and used_by (hansen1991implications, kalyuga2003expertise, "
                "shleifer1997limits, tetzlaff2025cornerstone gained AP1). Bibliographic fields identical. tools/"
                "verify_refs.py --unit S7 (live): '94 of 560 entries, 0 problems' (exit 0); tools/verify_refs.py --offline: "
                "'offline integrity: 560 entries, 0 problems'.",
}

CARRY_FILES = "course/modules/S/S7/L05.html, course/modules/S/S7/L06.html"

decisions: list[dict] = []


def row(prior: dict, status: str, evidence: str, fix: str = "") -> dict:
    out = {"id": prior["id"], "check": prior["check"], "location": prior["location"], "status": status,
           "evidence": evidence}
    if status != "PASS":
        out["fix"] = fix or "Re-derive or re-run the named item in this round's checkout and record the exact output."
    return out


def carried(prior: dict, files: str, extra: str = "") -> str:
    head = f"Carried from the release ledger ({files} byte-identical since 5e5da87):"
    tail = f" round-32 evidence is row {prior['id']} of 47bac8d:ledgers/S7/L05-L06.json; {extra}".rstrip()
    return head + tail


UNVERIFIABLE_REASON = {
    "L06-lab2-universes-line423": "the variant run (universes changed to (slice(0, 60),)) and its printed rates were "
                                   "not re-run this round; the base expected block matched in run_labs",
    "L06-lab1-m1000-line430": "the variant runs (real-effect share 0.05 and 0.5) were not re-run this round; the page's "
                              "M = 1000 expected output matched in run_labs",
    "R29-lab-prose-L06-2-universes": "the Lab 2 variant with universes changed to (slice(0, 60),) was not re-run this round",
    "R29-lab-prose-L06-1-BHY": "the Lab 1 variants (share 0.05 and 0.5) were not re-run this round",
    "R29-lab-prose-L05-1-table": "the Lab 1 table at rho = 0.0, 0.3, 0.9 includes values other than the page's expected block "
                                 "(rho = 0.3 only); the other rho runs were not re-run this round",
    "L05-lab6-unsourced-1.5": "the skill-free null simulation (per-rule rejection rates 0.046-0.048, expected count 1.395) "
                              "was not re-run this round",
    "L05-num-E2": "the simulation-based clauses of Problem E2 (block counts, coverage) were not re-run this round; its "
                  "closed-form values 13/7, 1.363, 0.114 and 25.95 were re-derived (derive_numbers.py)",
    "L05-num-E2-runtime": "the runtime of sol-S7-L05-E2 was not re-timed this round (run_labs ran the snippet; no timing printed)",
    "L06-num-E3-runtime": "the runtime of sol-S7-L06-E3 was not re-timed this round",
    "L05-num-E1": "the Problem E1 simulated values (Lab 1 with rho changed) were not re-run this round",
    "L05-num-E3": "the Problem E3 simulated values were not re-run this round",
    "L06-num-E1": "the Problem E1 variant (Lab 2 with the universe choice dropped) was not re-run this round",
    "L06-num-E2": "the Problem E2 variant (Lab 1 with the real-effect share changed) was not re-run this round",
    "L06-num-E3": "the Problem E3 values (0.346, 0.121, 0.038) come from a seeded simulation, not re-run this round",
    "R29-num-L06-lab-quotes": "the P-solution values 0.346, 0.121 and 0.038 come from a seeded simulation, not re-run this round",
    "L05-num-M4-table-values": "the estimates and standard errors of the M4 table (line 952) were not re-read this round; "
                               "the z, p, BH and interval values built from them were re-derived",
    "L05-num-quiz": "the 14 quiz items' numbers were not individually re-derived this round (scipy values 950, 2.568, 8.224 "
                    "etc. are covered by derive_numbers.py; the item texts were not re-read)",
    "R26-quiz-L05-explanations": "the Section 13 quiz explanations (14 items) were not individually re-derived this round",
    "R27-quiz-explanations-L06": "the Section 10 quiz items (10) were not individually re-derived this round",
    "L05-num-key-results-new": "the key-results rows 8-17 (line 1186-1203) were not re-read this round",
    "L05-num-misconceptions-new": "misconception 6's threshold statements were not re-derived beyond the Problem M1 values this round",
    "R30-num-L06-mills-M316": "the bracket 3.7760 to 3.7928 around the Mills solution was not re-derived this round (t* = 3.7778 "
                              "was re-derived)",
    "R30-edit-L06-line95-bracket": "the bracket of line 95 (3.7760 to 3.7928) was not re-derived this round (3.7778 was)",
    "R31-sweep-numbers-L05": "the round-32 numeric-token sweep was not reconciled this round: scripts/number_coverage.py "
                             "classifies 158 distinct L05 tokens as not in an expected block and not derived",
    "R31-sweep-numbers-L06": "the round-32 numeric-token sweep was not reconciled this round: scripts/number_coverage.py "
                             "classifies 96 distinct L06 tokens as not in an expected block and not derived",
    "R31-vague-quantities": "the vague-quantity sweep (hundreds, thousands, dozens, few, several) was not re-run this round",
    "R32-numbers-spotcheck": "the round-32 sample of 15 numbers is not listed in the ledger; this round's derive_numbers.py "
                             "covers 121 values but not that sample",
    "R32-L05-333-E1-sentence": "the Problem E1 sentence's values were not all re-derived this round",
    "R32-L05-333-reversal-sentence": "the reversal sentence's Monte Carlo quantities were not re-run this round",
    "L05-lab6-search-bound": "the lab 6 search-bound statement depends on a bootstrap search (seeded) not re-run this round",
    "L06-math-E3-formula": "the E3 formula's integral (scipy) was not re-evaluated this round",
    "L06-math-prop32": "Proposition 3.2's Monte Carlo check was not re-run this round (the proof text is carried)",
    "R32-prop32-proof-and-mc": "the Proposition 3.2 Monte Carlo was not re-run this round",
    "R27-lemma76-mc": "the Lemma 7.6 Monte Carlo check was not re-run this round",
    "R27-diff-L05-582": "the Monte Carlo quantity in the L05 line 582 diff was not re-run this round",
    "R29-math-def66-fcr-line499": "the false-coverage simulation quoted at line 499 was not re-run this round",
}

TOKEN_NOTE = "token-checked: {n} lab-output numbers found in the expected block(s) {pages} of the page, which run_labs matched "\
             "this round"
DERIVED_NOTE = "re-derived this round by ledgers/S7/scripts/L05-L06-r33/derive_numbers.py ({n} values for this slice all OK)"
DERIVED_IDS = {
    "L05-num-s6-critical-values", "L05-num-s1-quantiles", "L05-num-s5-holm-gap", "L05-num-M2", "L05-num-M3",
    "L05-num-P2", "L05-num-s5-studentization", "L05-num-s5-studentization-example-r16", "L05-num-s7",
    "L05-r14-c500-harmonic", "L05-num-R4", "L05-num-M1", "L05-num-M4", "L05-num-misconceptions", "R29-num-L05-section5",
    "R29-num-L05-holm-stepm", "R29-num-L06-M1-table", "L06-num-s2-eq1", "L06-num-s2-cM", "L06-num-M1", "L06-num-M2",
    "L06-num-M3", "L06-num-P2", "L06-num-P3", "L06-p2-line373", "L06-line380-prior-odds",
    "L06-line311-derived-13-52", "L06-mc-error-lines244-423", "L06-r14-prop43-numbers", "L06-r14-prop43-proof",
    "L05-math-remark65", "L06-math-P1-P2-M3", "L05-notation", "hunk-L05-E2c-blockcount", "L05-num-fig-caption",
}
LAB_FRESH_IDS = {"R23-L03-cross-lesson-lab3-run"}
EXPLICIT_CARRY_NOTE = {
    "L05-num-lab1-hypothesis": "lab parameters (n_strat, rho, drift, alpha) in the twin; the twin ran in run_labs",
    "L05-num-lab2-setup": "lab parameters (n_strat = 8, alpha = 0.05, block length 1) in the twin; the twin ran in run_labs",
    "L05-num-R1-R2": "closed-form counts (5 x 252 = 1,260, re-derived) and design parameters (B, rules) as printed",
    "L05-math-E2-ar1": "a statement about the studentizing scale; no numeric result",
}

# Registry-cited keys whose used_by changed (AP1 added); bibliographic fields identical
USED_BY_KEYS = ("hansen1991implications", "kalyuga2003expertise", "shleifer1997limits", "tetzlaff2025cornerstone")
REG_NOTE = ("registry entries cited here: unchanged since 5e5da87 except used_by (AP1 added) for "
            + ", ".join(USED_BY_KEYS) + "; tools/verify_refs.py --unit S7 today: '94 of 560 entries, 0 problems'")

out_rows: list[dict] = []
counts: dict[str, int] = {}
for p in PRIOR["rows"]:
    rid, chk, loc = p["id"], p["check"], p["location"]
    prior_ev = p["evidence"]
    if chk == "2.0-diff":
        out_rows.append(row(p, "PASS", FRESH["diff"] + f" Prior row: {rid}."))
    elif chk == "2.5-lab":
        if rid == "L05-L06-runtime-claims-none":
            out_rows.append(row(p, "PASS", carried(p, CARRY_FILES, "no runtime claim is added by a change in these pages (the pages are byte-identical).")))
        else:
            out_rows.append(row(p, "PASS", FRESH["lab"] + f" Prior row: {rid}."))
    elif chk == "2.6-projects":
        out_rows.append(row(p, "PASS", "Fresh (round 33): tools/check_projects.py --all: S7 PASS, AP1 PASS (L05 and L06 have no project; project.html line 195 changed, outside this slice)."))
    elif chk == "2.8-figure":
        out_rows.append(row(p, "PASS", FRESH["figure"] + (" The kernel tests: tests/test_figure_kernels.py passed this round (log pytest_slice.out)." if "kernels" in rid else "") + f" Prior row: {rid}."))
    elif chk == "2.8-data":
        if rid in {"R31-cmd-fetch_data", "R31-data-licence-fx_daily", "R31-data-manifest-fx", "R32-licence-fed-disclaimer", "R31-lab6-data-quotes", "R32-lab6-window"}:
            if rid in {"R31-lab6-data-quotes", "R32-lab6-window"}:
                out_rows.append(row(p, "PASS", carried(p, CARRY_FILES, "fx_daily is embedded as course/assets/data/market/fx_daily.csv (sha256 re-derived, see the data rows); the lab 6 text is unchanged and its run passed; " + FRESH["data"][:600])))
            else:
                out_rows.append(row(p, "PASS", FRESH["data"] + f" Prior row: {rid}."))
        else:
            out_rows.append(row(p, "PASS", carried(p, "tools/data_sources.yaml (the hunk named by this row) and tools/fetch_data.py, BUILDER_RULES.md", "the diff of data_sources.yaml touches only lines 28-35 and 55-69 (the H.10 notes); the named lines are unchanged; fetch_data --check PASS today.")))
    elif chk == "2.9-banned":
        out_rows.append(row(p, "PASS", FRESH["banned"] + f" Prior row: {rid}."))
    elif chk == "2.9-structure":
        if rid in {"R31-cmd-check_pages", "R31-cmd-check_dag", "R31-cmd-page_smoke", "R31-dag-L05-L06", "R31-structure-L05-L06", "R31-cmd-render_build", "R31-cmd-ruff-mypy", "R31-cmd-pytest"} or rid.startswith("L05-concept-") or rid in {"L05-struct-concepts", "L06-r14-sec3-contested-sentence", "R26-link-L03-s8", "R23-L06-card-S7-c241-section-pointer", "R24-site-data-hounyo", "site-data-references-lu2025replication", "r17-tool-build_site-plain_title", "R31-hours", "R32-hub-hours-split", "R32-hours-estimate-flag"}:
            if rid in {"R24-site-data-hounyo", "site-data-references-lu2025replication", "r17-tool-build_site-plain_title"}:
                out_rows.append(row(p, "PASS", "Fresh (round 33): tools/build_site.py --check 'site data current: 6 outputs'; the only tools/build_site.py hunk since 5e5da87 is line 379 (render_concepts, '_part, m = modules[module_id]'), outside plain_title(), which is unchanged. " + carried(p, CARRY_FILES, "")))
            elif rid in {"R31-hours", "R32-hub-hours-split", "R32-hours-estimate-flag"}:
                out_rows.append(row(p, "PASS", carried(p, "course/modules/S/S7/L05.html, course/modules/S/S7/L06.html, course/modules/S/S7/index.html and course/modules/S/S7/cards.json", "hours attributes unchanged; the S7 module hours in curriculum/curriculum.json are unchanged (the hunks are in MS-FIN, PHD-FIN and AP1 only); tools/render_curriculum.py regenerated curriculum.json identically today.")))
            elif rid.startswith("L05-concept-") or rid in {"L05-struct-concepts"}:
                out_rows.append(row(p, "PASS", "Fresh (round 33): tools/check_dag.py --all: S7 PASS (every dfn id defined once, every concept link resolves; nothing used before defined). " + carried(p, CARRY_FILES, "")))
            elif rid == "R31-cmd-ruff-mypy":
                out_rows.append(row(p, "PASS", FRESH["structure"]))
            elif rid == "R31-cmd-pytest":
                out_rows.append(row(p, "PASS", "Fresh (round 33): python -m pytest -o addopts= tests/test_labs.py tests/test_figure_kernels.py tests/test_run_labs.py tests/test_page_smoke.py tests/test_docs_figures.py tests/test_js.py: 138 passed (log pytest_slice.out)."))
            else:
                out_rows.append(row(p, "PASS", FRESH["structure"] + f" Prior row: {rid}."))
        else:
            out_rows.append(row(p, "PASS", carried(p, CARRY_FILES, "the structure, dfn and link text these rows read is unchanged; check_dag and check_pages PASS today.")))
    elif chk == "2.4-math":
        if rid == "L06-r14-prop43-proof":
            out_rows.append(row(p, "PASS", carried(p, CARRY_FILES, "the proof text is unchanged; its numbers (c = 0.46107, z* = 0.9005, z* + 1/z* = 2.01101, u(z*) = 0.0728, z = 0.5244, z^2/2 = 0.1375, e^-0.1375 = 0.872, -e 0.6 ln 0.6 = 0.833) were re-derived this round by ledgers/S7/scripts/L05-L06-r33/derive_numbers.py (all OK).")))
        elif rid in {"L06-math-P1-P2-M3", "L05-math-remark65", "L05-notation"}:
            out_rows.append(row(p, "PASS", carried(p, CARRY_FILES, "the displayed numbers of this row were re-derived this round in ledgers/S7/scripts/L05-L06-r33/derive_numbers.py (all OK); the proof text is unchanged.")))
        elif rid in UNVERIFIABLE_REASON:
            out_rows.append(row(p, "UNVERIFIABLE", prior_ev[:0] + f"Not compared this round: {UNVERIFIABLE_REASON[rid]}. The proof text is byte-identical to 5e5da87 (CARRY_FILES), so this is only the numeric or simulation claim."))
        else:
            out_rows.append(row(p, "PASS", carried(p, CARRY_FILES, "a proof or statement with no toolchain-dependent numeric (checked: the row is not in the numeric list of derive_numbers.py and the page text is unchanged).")))
    elif chk == "2.7-cards":
        out_rows.append(row(p, "PASS", carried(p, "course/modules/S/S7/cards.json", FRESH["cards"])))
    elif chk == "2.1-citation":
        out_rows.append(row(p, "PASS", carried(p, CARRY_FILES, REG_NOTE + "; the citing text and the registry entry are unchanged.")))
    elif chk == "2.3-grade":
        out_rows.append(row(p, "PASS", carried(p, CARRY_FILES, "the grade is a property of the claim text and its cited entries (" + REG_NOTE + ")." )))
    elif chk == "2.2-number":
        if rid in DERIVED_IDS:
            out_rows.append(row(p, "PASS", DERIVED_NOTE.format(n=121) + " " + carried(p, CARRY_FILES, "the quoted values are the ones checked, the text is unchanged.")))
        elif rid in LAB_TOKENS:
            checks = LAB_TOKENS[rid]
            missing = [v for v, d, pages, s in checks if not in_expected(v, d, pages, s)]
            pages = sorted({pg for _, _, pgs, _ in checks for pg in pgs})
            if missing:
                out_rows.append(row(p, "UNVERIFIABLE", f"Lab-output numbers not found in the expected block(s) {pages} at the stated precision: {missing}. Prior row: {rid}.", "Confirm each quoted lab output against the page's expected block (or fix the prose) and record the matches."))
            else:
                out_rows.append(row(p, "PASS", TOKEN_NOTE.format(n=len(checks), pages=pages) + f". Prior row: {rid}; text unchanged (CARRY_FILES byte-identical since 5e5da87)."))
        elif rid in LAB_FRESH_IDS:
            out_rows.append(row(p, "PASS", FRESH["lab"] + f" Prior row: {rid} (L03 lab 3 is one of the 42 unit labs)."))
        elif rid in UNVERIFIABLE_REASON:
            out_rows.append(row(p, "UNVERIFIABLE", f"Not compared this round: {UNVERIFIABLE_REASON[rid]}. Prior row: {rid}."))
        elif rid in EXPLICIT_CARRY_NOTE:
            out_rows.append(row(p, "PASS", carried(p, CARRY_FILES, EXPLICIT_CARRY_NOTE[rid])))
        else:
            out_rows.append(row(p, "PASS", carried(p, CARRY_FILES, "a source-quoted or design number with no toolchain-dependent computation; " + REG_NOTE + ".")))
    else:
        out_rows.append(row(p, "UNVERIFIABLE", f"Unhandled check family {chk}", "Add a decision for this family."))

for r in out_rows:
    r["evidence"] = r["evidence"].replace("CARRY_FILES", CARRY_FILES)
    if "fix" in r:
        r["fix"] = r["fix"].replace("CARRY_FILES", CARRY_FILES)
ids = [r["id"] for r in out_rows]
assert len(ids) == len(set(ids)) == len(PRIOR["rows"]) == 604, "row ids must be the 604 release ids, each once"

# Added rows: checks new in round 33 (ruling 5)
NEW = [
    {"id": "R33-notation-collisions", "check": "2.4-notation", "location": "notation/notation.json; course/modules/S/S7/L05.html; course/modules/S/S7/L06.html",
     "status": "PASS", "evidence": FRESH["notation"]},
    {"id": "R33-registry-used-by-delta", "check": "2.1-registry", "location": "references/references.json (560 entries)",
     "status": "PASS", "evidence": FRESH["registry"]},
    {"id": "R33-banned-phrases", "check": "2.9-banned", "location": "course/modules/S/S7/L05.html; L06.html; cards.json",
     "status": "PASS", "evidence": FRESH["banned"]},
    {"id": "R33-pyodide314-lab-timings", "check": "2.5-timing", "location": "tools/page_smoke.py --unit S7 --pages L05 L06 (Pyodide 314.0.7)",
     "status": "PASS", "evidence": FRESH["lab"]},
    {"id": "R33-fx-daily-rebuild", "check": "2.8-data", "location": "course/assets/data/market/fx_daily.csv; MANIFEST.json",
     "status": "PASS", "evidence": FRESH["data"]},
    {"id": "R33-live-refs-S7", "check": "2.1-citation", "location": "tools/verify_refs.py --unit S7 (94 entries)",
     "status": "PASS", "evidence": "Fresh (round 33): tools/verify_refs.py --unit S7 final line 'live re-verification of S7: 94 of 560 entries, 0 problems' (exit 0; log verify_refs_S7_live.out); tools/verify_refs.py --offline 'offline integrity: 560 entries, 0 problems'."},
    {"id": "R33-curriculum-regen", "check": "2.9-structure", "location": "tools/render_curriculum.py; CURRICULUM.md; curriculum/curriculum.json",
     "status": "PASS", "evidence": "Fresh (round 33): tools/render_curriculum.py regenerated both files; git diff --exit-code clean (byte-identical to the committed files; log: 'curriculum valid: 25 parts, 134 modules, 157 projects, 13,715 h (6.35 FTE years)')."},
]
out_rows += NEW

counts = {s: sum(1 for r in out_rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
mutants: list = []
fragment = {
    "unit": "S7",
    "slice": "L05-L06",
    "round": ROUND,
    "verifier": "verifier round 33 (S7 L05-L06, toolchain re-confirmation; independent of the builders and of round 32)",
    "pin": "47bac8d",
    "base": "5e5da87",
    "previous_ledger": "47bac8d:ledgers/S7/L05-L06.json (round 32, 604 rows, PASS)",
    "checkout": "/tmp/verify-s7-r1-l56",
    "scratch": "/tmp/ap1-r5/L05-L06",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "PASS" if counts["PASS"] == len(out_rows) else "FAIL",
    "rows": out_rows,
    "mutants": mutants,
    "registry_flags": PRIOR.get("registry_flags", []) + [
        "Notation: plain Q is defined locally in L06.html line 276 (Q = 1 - Phi) and L05.html line 596 (inverse covariance); the registered AP1 symbol is \\mathbb{Q}. No collision in the pages, flagged for the builder.",
        "references/references.json: four AP1 used_by additions (hansen1991implications, kalyuga2003expertise, shleifer1997limits, tetzlaff2025cornerstone); bibliographic fields unchanged.",
    ],
    "freshness_flags": PRIOR.get("freshness_flags", []),
    "notes": [
        "DELTA (git diff --stat 5e5da87 HEAD over the slice paths): 0 slice files changed. Every subject file of the 604 rows is byte-identical to 5e5da87 (course/modules/S/S7/L05.html, L06.html, figures-L05.js, figures-L06.js, cards.json, tests/labs/S7 lab and solution twins). Hunks read that touch S7 or that S7 depends on: course/modules/S/S7/L01.html line 133 (not this slice); course/modules/S/S7/project.html line 195 (not this slice); notation/notation.json and course/assets/data/notation.json (4 new AP1 symbols, not used on these pages); pyproject.toml (requires-python and mypy python_version 3.14; two lab-twin mypy excludes); requirements*.txt (pytest 9.0.2, ruff 0.17.2, mypy 2.4.0, numpy 2.4.6, scipy 1.18.0, playwright 1.64.1); course/assets/js/lab.js, data.js, theme.js (new), rubric.js (wording), course/assets/css (new tokens and components), tools/page_smoke.py (strict KaTeX, package preload, timings), tools/katex_strict.js (new), tools/build_site.py (line 379), tools/data_sources.yaml (H.10 notes), tools/vendor*.py and spec (Pyodide 314.0.7, KaTeX 0.19.1), tests/test_figure_kernels.py (1.4e-12 tolerance for pdf^(n-1) at n >= 2, 5e-14 (n-1)), tests/test_memo_exemplars.py (unused variable), curriculum/curriculum.json and 03-markets.yaml (AP1 prerequisites and hours in MS-FIN and PHD-FIN; S7 module entries unchanged), references/references.json (used_by only), atlas/A8.contract.md (amendment header; not a slice file).",
        "TOOLCHAIN: Python 3.14.8, numpy 2.4.6, scipy 1.18.0 (checkout .venv). Commands re-run this round: run_labs S7, page_smoke L05 and L06 (with the figure sweep), check_pages --all, check_dag --all, check_projects --all, build_site --check, render_curriculum (clean), fetch_data --check and --fetch --only fx_daily in a scratch copy, verify_refs --offline and --unit S7 (live), ruff check, ruff format --check, mypy --no-incremental, pytest on six test files (138 passed).",
        "FIGURES: ledgers/S7/scripts/L05-L06-r33/drive_figures.py (own Playwright drive) and figure_readouts.py (own Python port of stats.js rng and multitest.js bootstrap and stepdown kernels, and closed forms for L06). All 20 chart instances at 1280 and 360 px in light and dark; the default, every bayes t-value (101), every hurdle alpha, both L05 buttons (Simulate, Show a study where a later step rejects: seed 104 after 2 draws) and the joint-vs-independent readout matched the Python recomputation exactly; 0 console errors, 0 external requests.",
        "NUMBERS: ledgers/S7/scripts/L05-L06-r33/derive_numbers.py re-derives 121 quoted values with scipy and exact arithmetic (all OK). ledgers/S7/scripts/L05-L06-r33/number_coverage.py maps every visible numeric token to an expected block or a derived value: 158 distinct L05 tokens and 96 distinct L06 tokens are not classed by this mechanical sweep (many are section numbers, years, citation locators and dates); those numeric rows are UNVERIFIABLE where a quoted claim was not reconciled.",
        "NOT RE-RUN THIS ROUND (UNVERIFIABLE rows): variant runs of Labs 1 and 2 (changed inputs quoted in prose), the seeded and Monte Carlo simulations of Problems E1-E3 and of Proposition 3.2, the L05 Lab 6 null simulation, the runtimes of the solution snippets, the M4 table values, the quiz explanations, the key-results rows 8-17, the bracket of line 95, and the vague-quantity sweep.",
        "EXTERNAL SOURCES: no publisher page was re-read this round beyond the Federal Reserve licence pages (HTTP 200 for disclaimer.htm and about.htm) and the live Crossref re-resolution of the 94 S7 registry entries (verify_refs --unit S7 exit 0). Citation and grade rows are carried on byte-identity of the citing text and registry entries, as architect ruling 4 allows. No bot check or access block was encountered; nothing was circumvented.",
        "DATA: fetch_data --fetch in the scratch copy reproduced fx_daily.csv byte-for-byte (sha256 02872dd7...); the raw download's sha256 differs from the MANIFEST provenance record (issuer file changed), as BUILDER_RULES 6.6 expects; the repository's MANIFEST was not changed.",
        "HOURS (carried flag, not a row failure): the round-32 estimate for L05 (declared 11 h, estimated 12-14 h) and L06 (declared 7 h, estimated 8-9 h) stands; the hub split (70 + 30) is unchanged.",
        "PRIOR EVIDENCE: a carried row's prior evidence is row <id> of 47bac8d:ledgers/S7/L05-L06.json (round 32, verified on the previous toolchain). Carried rows state the exact subject files that are byte-identical since 5e5da87.",
    ],
    "summary": {
        "rows": len(out_rows),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": counts["UNVERIFIABLE"],
        "mutants": 0,
        "mutants_killed": 0,
        "mutants_note": "lessons only; no grader or project in L05 or L06, so 0/0",
        "carried_byte_identical_since_5e5da87": sum(1 for r in out_rows if r["evidence"].startswith("Carried from the release ledger")),
        "fail_ids": [r["id"] for r in out_rows if r["status"] != "PASS"],
    },
}
problems = ledger.validate(fragment, "S7/L05-L06")
out = ROOT / "ledgers/S7/L05-L06.json"
out.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(out_rows), "counts", counts, "validate problems:", problems)
