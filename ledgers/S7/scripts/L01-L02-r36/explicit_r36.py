"""Round-36 explicit rows for the S7 L01-L02 fragment (commit 47bac8d; base a90b52b; imported by build_fragment_r36.py).

Values are from this round's command outputs (logs under /tmp/ap1-r5/s7-l12-r36/) or from scripts archived in this repository:
ledgers/S7/scripts/L01-L02-r36/ (caption_six_numbers_r36.py, build_fragment_r36.py, explicit_r36.py) and
ledgers/S7/scripts/L01-L02-r35/ (expmax_gap_r35.py, visible_text_r35.py, koning_sim_r35.py, ...).
"""

from __future__ import annotations

S = "ledgers/S7/scripts/L01-L02-r36"
S35 = "ledgers/S7/scripts/L01-L02-r35"
A = "ledgers/S7/scripts/L01-L02-r33r34"
LOG = "/tmp/ap1-r5/s7-l12-r36"
CAP = "L01.html line 133 (figcaption, commit 47bac8d)"

# Rows that a caption change touches: the round-36 finding is prepended; the superseded round-35 text is kept after it.
CAPTION_NOTE = (
    "Round 36 (commit 47bac8d): the caption at line 133 now reads 'The dependence-free bound (1), \\(\\sqrt{2 \\ln N}\\), exceeds "
    "the exact expectation, computed by numerical integration, by 0.61 standard deviations at N = 10 (2.146 against 1.539), by 0.53 "
    "at N = 100 (3.035 against 2.508) and by 0.44 at N = 10,000 (4.292 against 3.852).' The six numbers were recomputed from scratch "
    f"by {S}/caption_six_numbers_r36.py (all six match the page at 3 dp; gaps 0.607213, 0.527261, 0.440316 SD, which round to 0.61, "
    "0.53, 0.44 from the unrounded and from the 3-dp values). The sentence is ruled in T34-banned-roughly-half-caption. "
    "The first two caption sentences (the (3) sign and the N = 2 values) are unchanged. "
)

EXPLICIT: dict[str, dict[str, str]] = {}


def caption_row(rid: str, status: str = "PASS", extra: str = "") -> None:
    EXPLICIT[rid] = {"status": status, "evidence": CAPTION_NOTE + extra + " Superseded round-35 text follows: "}


# ---------- caption rows: re-derived for the new sentence ----------
EXPLICIT["T34-banned-roughly-half-caption"] = {
    "status": "PASS",
    "evidence": (
        "Round 36 ruling on the new sentence (orchestrator request, commit 47bac8d). (1) The banned phrase is absent: the visible "
        f"text of L01 has no 'roughly half' (T36-prose-differential; {LOG}/prose_head.log). (2) BUILDER_RULES 1.2(c) 'derived in a "
        "calculation shown on the page': the page displays the bound formula \\(\\sqrt{2 \\ln N}\\) in the caption itself and in "
        "Theorem 2.1 (L01 lines 82-92), prints both values at each N (2.146 against 1.539; 3.035 against 2.508; 4.292 against 3.852), "
        "names the method ('computed by numerical integration'), and the source line directly below the caption displays the integrand "
        "\\(x \\cdot N\\varphi(x)\\Phi(x)^{N-1}\\) with 'numerically'. A reader can reproduce 1.539 by integrating that integrand "
        "over the real line and check the subtraction 2.146 - 1.539 = 0.607 -> 0.61. Not printed on the page: the integration range "
        "(the real line) and the identity that makes the integrand the density of the maximum. Ruling: the sentence meets 1.2(c). "
        "The gap is not a free number: its inputs and method are shown. This is judgment; the orchestrator confirms. PASS."
    ),
}
caption_row("T35-expmax-gap-numbers", extra=(
    "Round 36 check of the three gaps: unchanged in value (0.607213, 0.527261, 0.440316; rounded 0.61, 0.53, 0.44). "
    "The N = 10 and N = 100 values now printed by the page (1.539, 2.508, 3.852, 2.146, 3.035, 4.292) are recomputed in "
    "T36-caption-six-numbers."))
caption_row("T35-caption-unit-sd", extra=(
    "Unit unchanged: the page defines Z_n as standard normal (Section 2, Theorem 2.1) and the y-axis is 'Expected maximum (SD units)' "
    "(figures-L01.js line 61). The sentence now also names 'computed by numerical integration', which is the method of T36-caption-method."))
caption_row("T35-caption-sign-sweep", extra=(
    f"Round 36 re-run: {S35}/expmax_gap_r35.py (rc 0; {LOG}/expmax_r35_rerun.log): (3) - exact > 0 for every N = 3..10000 (True). "
    "The two sentences this row covers are unchanged in text."))
caption_row("L01-num-fig-caption-n2", extra="1/sqrt(pi) = 0.564190 and (3) at N = 2 = 0.519755 still round to the caption's 0.564 and 0.520.")
caption_row("L01-num-fig-caption", extra="The desc (figures-L01.js lines 55-71) is unchanged; its 'just above it from N = 3 on' still agrees with the sweep.")
caption_row("L01-fig-1-caption", extra="The 'roughly half' sentence is absent; the replacement is ruled in T34-banned-roughly-half-caption.")
caption_row("L01-fig-expected-max", extra="Caption checked in T35-caption-sign-sweep, T36-caption-six-numbers and T36-caption-method.")
caption_row("L01-fig-expected-max-desc-202ea24", extra="Desc unchanged; agrees with the recomputed sweep.")
caption_row("L01-fig-expected-max-gap-e968af2", extra="The three gaps are unchanged in value (T36-caption-six-numbers).")
caption_row("L01-fig-expected-max-765bcb1", extra="Caption checked as above; rendering by page_smoke (round 36 PASS).")
caption_row("L01-fig-expected-max-a2a631a", extra="Caption checked as above; rendering by page_smoke (round 36 PASS).")
caption_row("L01-fig-1-legibility", extra=(
    f"Round 36 page_smoke --unit S7 --pages L01 L02: PASS (log {LOG}/page_smoke.log); the new caption adds no overflow flag at 360 px. "
    "The caption text itself was not screenshot."))
caption_row("L01-fig-1-provenance", extra="The source line below the caption is unchanged; it names the integrand the new sentence relies on (T36-caption-method).")
caption_row("L01-fig-1-furniture", extra="Title, axes, source line and caption present; only the caption sentence changed.")
caption_row("L01-banned-roughly-half", extra="'roughly half' absent from L01 visible text after 47bac8d (T36-prose-differential).")
caption_row("L01-L02-fig-captions-states-8d2fca9", extra="Only the section 3 caption changed; page_smoke PASS (round 36).")
caption_row("L01-L02-expmax-claims-a2a631a", extra="The caption sentence cited is the one in T36-caption-six-numbers; Lab 1 text unchanged.")
caption_row("L01-fig-drive-e968af2", extra="Section 3 figure is static; its caption is ruled above.")
caption_row("T33-decimal-coverage", extra="Round 36 differential: the six new decimals (2.146, 1.539, 3.035, 2.508, 4.292, 3.852) are recomputed in T36-caption-six-numbers; no other decimal changed (T36-decimal-differential).")

# ---------- round-36 command re-runs ----------
EXPLICIT["L01-L02-cmd-page_smoke-a2a631a"] = {
    "status": "PASS",
    "evidence": (
        f"Round 36 re-run on 47bac8d: .venv/bin/python tools/page_smoke.py --unit S7 --pages L01 L02 (rc 0, log {LOG}/page_smoke.log): "
        "'page_smoke modules/S/S7/L01.html: PASS', 'page_smoke modules/S/S7/L02.html: PASS', 'page_smoke S7: PASS'. PASS."
    ),
}
EXPLICIT["L01-L02-lab-timings-0f4068a"] = {
    "status": "PASS",
    "evidence": (
        f"Round 36 (same page_smoke run, {LOG}/page_smoke.log): runtime boot 1.0 s; package preload 0.2 s; L01 labs 0.2, 0.1, 0.2, "
        "0.5 s; L02 labs 0.1, 0.0, 0.1 s. All far below 10 s. PASS."
    ),
}
EXPLICIT["L01-L02-cmd-run_labs-S7-a2a631a"] = {
    "status": "PASS",
    "evidence": f"Round 36 re-run: .venv/bin/python tools/run_labs.py --unit S7 (rc 0, {LOG}/run_labs.log): 'run_labs S7: PASS (42/42)'. PASS.",
}
EXPLICIT["L01-L02-cmd-run_labs-L01-a2a631a"] = {
    "status": "PASS",
    "evidence": (
        "Round 36: the unit-wide run (42/42, above) includes L01 (its 4 labs). The per-page run was not repeated in round 36; "
        "the round-35 per-page result (4/4, expected-block output compared) stands for L01 because no lab file or lab expected block changed "
        "(git diff a90b52b HEAD: only L01.html line 133). PASS."
    ),
}
EXPLICIT["L01-L02-cmd-run_labs-L02-a2a631a"] = {
    "status": "PASS",
    "evidence": (
        "Round 36: the unit-wide run (42/42) includes L02 (its 3 labs). No L02 file changed since e6d10ab (git diff --quiet rc 0). PASS."
    ),
}
EXPLICIT["L01-L02-cmd-ruff-mypy-a2a631a"] = {
    "status": "PASS",
    "evidence": (
        f"Round 36 re-run on 47bac8d (logs {LOG}/ruff_check.log, ruff_format.log, mypy.log): .venv/bin/ruff check . -> 'All checks passed!' "
        "(rc 0); .venv/bin/ruff format --check . -> '125 files already formatted' (rc 0); .venv/bin/mypy --no-incremental -> "
        "'Success: no issues found in 102 source files' (rc 0). pyproject.toml changed at 47bac8d only in a comment (T36-comment-only-nonS7). PASS."
    ),
}
EXPLICIT["L01-L02-cmd-pytest-figure-kernels-a2a631a"] = {
    "status": "PASS",
    "evidence": (
        f"Round 36 re-run on 47bac8d (tests/test_figure_kernels.py changed in a comment only, T36-comment-only-nonS7): .venv/bin/python -m "
        f"pytest -p no:cacheprovider -v tests/test_koning_spot.py tests/test_figure_kernels.py tests/test_docs_figures.py (rc 0, {LOG}/pytest3.log): "
        "'49 passed in 17.61s'. The Koning file ran 3 tests. PASS."
    ),
}
EXPLICIT["L01-L02-cmd-check_pages-a2a631a"] = {
    "status": "PASS",
    "evidence": f"Round 36 re-run: .venv/bin/python tools/check_pages.py --unit S7 (rc 0): 'check_pages S7: PASS' ({LOG}/check_pages.log). PASS.",
}
EXPLICIT["L01-L02-cmd-check_dag-a2a631a"] = {
    "status": "PASS",
    "evidence": f"Round 36 re-run: .venv/bin/python tools/check_dag.py --unit S7 (rc 0): 'check_dag S7: PASS' ({LOG}/check_dag.log). PASS.",
}
EXPLICIT["L01-L02-cmd-verify_refs-live-S7-a2a631a"] = {
    "status": "PASS",
    "evidence": (
        f"Round 36 re-run (live): .venv/bin/python tools/verify_refs.py --unit S7 --workers 1 (rc 0, {LOG}/verify_live.log): "
        "'live re-verification of S7: 94 of 560 entries, 0 problems'. PASS."
    ),
}
EXPLICIT["L01-L02-cmd-verify_refs-offline-a2a631a"] = {
    "status": "PASS",
    "evidence": f"Round 36 re-run: .venv/bin/python tools/verify_refs.py --offline (rc 0, {LOG}/verify_off.log): 'offline integrity: 560 entries, 0 problems'. PASS.",
}
EXPLICIT["L01-L02-cmd-crossref-koning-a2a631a"] = {
    "status": "PASS",
    "evidence": (
        "Round 36: koning2026anytime is in the S7 live scope (used_by ['S7']); the live run above (94 of 560, 0 problems, rc 0) "
        "re-verified its Crossref record. PASS."
    ),
}
EXPLICIT["L01-L02-cmd-git-a2a631a"] = {
    "status": "PASS",
    "evidence": (
        "Round 36: HEAD = 47bac8d (short), base a90b52b. git diff --stat a90b52b HEAD: 3 files (course/modules/S/S7/L01.html 2 +-, "
        "pyproject.toml 3 +-, tests/test_figure_kernels.py 4 +-). The S7 change is line 133 only (git diff -U0). Earlier history: "
        "e6d10ab..a90b52b in round 35. PASS."
    ),
}
EXPLICIT["L01-cmd-koning-spot-a2a631a"] = {
    "status": "PASS",
    "evidence": (
        "Round 35 evidence, carried: the committed test and its claims are unchanged since e6d10ab (tests/test_koning_spot.py). "
        "Round 36 re-run of the three-file pytest (49 passed in 17.61s on 47bac8d, after the comment-only change in "
        "test_figure_kernels.py) keeps the Koning file green. The round-35 simulation (koning_sim_r35.py, all six-SE checks PASS) and "
        "mutants (5 of 5 killed) are not repeated in round 36. Round-35 text follows: " 
    ),
}
EXPLICIT["T34-koning-test-mutants"] = {"status": "PASS", "evidence": (
    "Round 36: the mutants are committed in ledgers/S7/mutants/koning-r35/ and the committed test they mutate is unchanged since e6d10ab. "
    "Round-35 run (5 of 5 killed) stands; not repeated. Round-35 text follows: ")}

# ---------- new round-36 rows ----------
NEW_ROWS: list[dict[str, str]] = [
    {
        "id": "T36-caption-six-numbers",
        "check": "2.2-number",
        "location": "course/modules/S/S7/L01.html line 133 (figcaption)",
        "status": "PASS",
        "evidence": (
            f"{S}/caption_six_numbers_r36.py (rc 0, scipy quad and grid; {LOG}/). Bound sqrt(2 ln N) and exact E[max] of N iid "
            "N(0,1): N = 10: 2.145966 -> 2.146, 1.5387527308 -> 1.539; N = 100: 3.034854 -> 3.035, 2.5075936364 -> 2.508; "
            "N = 10,000: 4.291932 -> 4.292, 3.8516158171 -> 3.852. Gap unrounded 0.607213, 0.527261, 0.440316 -> 0.61, 0.53, 0.44; "
            "from the 3-dp values 0.607, 0.527, 0.440 -> same. All six match the page; the quad and grid agree to 1e-9. PASS."
        ),
    },
    {
        "id": "T36-caption-method",
        "check": "2.2-number",
        "location": "course/modules/S/S7/L01.html line 133 (figcaption) and line 134 (source line)",
        "status": "PASS",
        "evidence": (
            "Reproducibility of the exact value 1.539 from the page (BUILDER_RULES 1.2(c)). Shown on the page: the bound formula "
            "(caption and Theorem 2.1); both values; the method 'computed by numerical integration'; the source line 'the exact curve "
            "integrates x N phi(x) Phi(x)^(N-1) numerically, where phi is the standard normal density'. Not shown: the integration "
            "range (taken as the real line) and the identity that N phi Phi^(N-1) is the density of the maximum. Reproduction needs only the "
            "displayed integrand over the real line; the script integrates it and gets 1.5387527308. Ruling: meets 1.2(c) on this reading; "
            "the two unstated items are recorded as a gap for the orchestrator. PASS (judgment)."
        ),
    },
    {
        "id": "T36-git-delta",
        "check": "2.9-structure",
        "location": "git diff a90b52b 47bac8d",
        "status": "PASS",
        "evidence": (
            "git diff --stat a90b52b HEAD: 3 files. course/modules/S/S7/L01.html: git diff -U0 gives only '@@ -133 +133 @@'. "
            "pyproject.toml: 3 lines, all comments plus no change to the exclude list (mypy_path, files, exclude unchanged). "
            "tests/test_figure_kernels.py: 4 lines in lines 353-357, comment text only, no assert changed. Every other S7 slice file is "
            "byte-identical since a90b52b (git diff --quiet rc 0 for L02.html, cards.json, figures-L01.js, figures-L02.js, tests/labs/S7, "
            "tests/test_koning_spot.py, references/references.json)."
        ),
    },
    {
        "id": "T36-comment-only-nonS7",
        "check": "2.9-structure",
        "location": "pyproject.toml; tests/test_figure_kernels.py (non-S7 gate inputs)",
        "status": "PASS",
        "evidence": (
            "The two non-S7 changes are comment-only: checked by the builder (every changed line in git diff a90b52b HEAD for both files "
            "starts with '#' after the +/- sign, or is the comment inside a test) and by the gates this round (ruff check, ruff format, "
            "mypy --no-incremental, the 49 pytest tests, all rc 0). Rows whose text names these files are re-run or carried on their "
            "slice subjects. PASS."
        ),
    },
    {
        "id": "T36-visible-text-diff",
        "check": "2.9-structure",
        "location": "L01.html and L02.html visible text",
        "status": "PASS",
        "evidence": (
            f"python -I {S35}/visible_text_r35.py a90b52b and HEAD: L01.txt changes at line 60 only; L02.txt identical. PASS."
        ),
    },
    {
        "id": "T36-prose-differential",
        "check": "2.9-banned",
        "location": "L01.html visible text (banned strings, question marks, ellipses)",
        "status": "PASS",
        "evidence": (
            f"{A}/scripts__prose_scan.py on the a90b52b and 47bac8d texts ({LOG}/prose_a90.log, prose_head.log): the only difference is "
            "'L01 chars 76104 -> 76233'. Every HIT count is unchanged ('roughly' 1, '?' 25, 'about ' 18, ellipsis 2). No banned string "
            "is added. PASS."
        ),
    },
    {
        "id": "T36-decimal-differential",
        "check": "2.2-number",
        "location": "L01.html visible text (decimal tokens)",
        "status": "PASS",
        "evidence": (
            "Decimal tokens, a90b52b 421 -> 47bac8d 427. Added: 2.146, 1.539, 3.035, 2.508, 4.292, 3.852 (each recomputed in "
            "T36-caption-six-numbers). Removed: none. The 0.61, 0.53, 0.44 were already present at a90b52b and are re-derived in "
            "T36-caption-six-numbers. L02 unchanged. PASS."
        ),
    },
    {
        "id": "T36-recompute-47",
        "check": "2.2-number",
        "location": "L01.html, L02.html (derived numbers the archived script names)",
        "status": "PASS",
        "evidence": f"python -I {A}/scripts__recompute.py <txt dir> on the 47bac8d visible text: 'TOTAL checks 47 failures 0: []' (rc 0). PASS.",
    },
    {
        "id": "T36-structure-checks",
        "check": "2.9-structure",
        "location": "L01.html, L02.html (data-cite keys, dfn, references)",
        "status": "PASS",
        "evidence": (
            f"python -I {A}/scripts__structure_checks.py <repo> (rc 0): L01 distinct data-cite keys 15, unresolved []; L02 distinct keys 3, "
            "unresolved []. The change is text inside one figcaption; no id, dfn or data-cite changed. PASS."
        ),
    },
]

NOTES = [
    "ROUND 36: verifier re-check at 47bac8d (base a90b52b). Delta: course/modules/S/S7/L01.html line 133 (the caption now shows the "
    "bound formula, the two values at N = 10, 100, 10,000 and the method, 'computed by numerical integration'); pyproject.toml and "
    "tests/test_figure_kernels.py changed in comments only (T36-comment-only-nonS7). Six numbers recomputed from scratch "
    "(caption_six_numbers_r36.py; all match). Ruling on the 1.2(c) question: PASS as a judgment; the integration range and the "
    "density identity are not printed (T36-caption-method).",
    "Gates on 47bac8d (exact output in the rows): page_smoke --unit S7 --pages L01 L02 PASS; check_pages, check_dag S7 PASS; run_labs "
    "--unit S7 42/42; verify_refs --unit S7 live 94 of 560, 0 problems; verify_refs --offline 560, 0 problems; ruff check and format "
    "pass; mypy --no-incremental 102 files pass; pytest on the three files 49 passed.",
    "Carry: rows carried from round 35 keep their subjects byte-identical since a90b52b (git diff --quiet). L01.html rows use the "
    "line-level variant ('except line 133'). Rows that cite the caption were re-derived above. Rows that name the comment-only "
    "non-S7 files are carried on their slice subjects (the files are not in their prefixes) and the gates re-ran this round.",
    "Round-35 notes still apply where not superseded (Koning ruling, the decision on archived scripts, the judgment calls). The "
    "architect should confirm the 1.2(c) reading for the new caption (T36-caption-method).",
]

# ---------- round-35 rows superseded or re-run this round (the round-35 result is kept after the round-36 text) ----------
SUPERSEDED = "Round 36: superseded for the 47bac8d delta by "
EXPLICIT["T35-git-hunk-scope"] = {"status": "PASS", "evidence": SUPERSEDED + "T36-git-delta (a90b52b..47bac8d). Round-35 result for e6d10ab..a90b52b follows: "}
EXPLICIT["T35-carry-identity"] = {"status": "PASS", "evidence": (
    "Round 36: the carry of every row was re-checked by build_fragment_r36.py against a90b52b (it exits on any changed subject file "
    "and on any unhandled row). Round-35 description follows: ")}
EXPLICIT["T35-visible-text-diff"] = {"status": "PASS", "evidence": SUPERSEDED + "T36-visible-text-diff (a90b52b..47bac8d: line 60 only). Round-35 result for e6d10ab..a90b52b follows: "}
EXPLICIT["T35-prose-differential"] = {"status": "PASS", "evidence": SUPERSEDED + "T36-prose-differential. Round-35 result follows: "}
EXPLICIT["T35-decimal-differential"] = {"status": "PASS", "evidence": SUPERSEDED + "T36-decimal-differential. Round-35 result follows: "}
EXPLICIT["T35-recompute-47"] = {"status": "PASS", "evidence": SUPERSEDED + "T36-recompute-47 (47 checks, 0 failures on 47bac8d). Round-35 result follows: "}
EXPLICIT["T35-structure-checks"] = {"status": "PASS", "evidence": SUPERSEDED + "T36-structure-checks (rc 0 on 47bac8d). Round-35 result follows: "}
EXPLICIT["L01-num-recompute-r19-e968af2"] = {"status": "PASS", "evidence": (
    f"Round 36 re-run: python -I {A}/scripts__recompute.py on the 47bac8d visible text: 'TOTAL checks 47 failures 0: []' (T36-recompute-47). "
    "Round-35 text follows: ")}
EXPLICIT["L01-L02-numbers-unmentioned-0f4068a"] = {"status": "PASS", "evidence": (
    "Round 36: the numeric tokens the 47bac8d delta changes are the six decimals of the new caption, each recomputed in "
    "T36-caption-six-numbers; the differential is T36-decimal-differential. Round-35 text follows: ")}
EXPLICIT["L01-L02-numbers-sweep-0f4068a"] = {"status": "PASS", "evidence": (
    "Round 36: the sweep is T36-recompute-47 (47 checks, 0 failures) plus T36-decimal-differential. L02 text identical to a90b52b. "
    "Round-35 text follows: ")}
EXPLICIT["L01-L02-cmd-expmax-sweep-a2a631a"] = {"status": "PASS", "evidence": (
    f"Round 36 re-run: .venv/bin/python -I {S35}/expmax_gap_r35.py (rc 0, {LOG}/expmax_r35_rerun.log): (3) - exact > 0 for every "
    "N = 3..10000 (True). Round-35 text follows: ")}
EXPLICIT["L01-L02-cmd-prose-scan-a2a631a"] = {"status": "PASS", "evidence": (
    "Round 36: superseded by T36-prose-differential (a90b52b and 47bac8d: only the character count changes). Round-35 text follows: ")}

# Carried on named subject files (scripts and sources unchanged since a90b52b; their L01 line-level subjects are outside line 133).
CARRY_EXTRA: dict[str, list[str]] = {
    "L01-cmd-m1-m4-a2a631a": ["course/modules/S/S7/L01.html"],
    "L02-cmd-m3-example42-a2a631a": ["course/modules/S/S7/L02.html"],
    "L01-cmd-m5-a2a631a": ["course/modules/S/S7/L01.html"],
    "L01-L02-cmd-check_projects-a2a631a": ["tools/check_projects.py", "course/modules/S/S7/project.html"],
    "T35-quiz10-about-half": ["course/modules/S/S7/L01.html"],
    "T35-koning-claims-coverage": ["tests/test_koning_spot.py", "course/modules/S/S7/L01.html"],
    "T35-koning-quoted-digits": ["course/modules/S/S7/L02.html", "course/modules/S/S7/cards.json", "course/modules/S/S7/L01.html"],
}
