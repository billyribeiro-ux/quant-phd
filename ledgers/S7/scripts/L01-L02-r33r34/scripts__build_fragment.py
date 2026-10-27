"""Build ledgers/S7/L01-L02.json (round 33, toolchain re-confirmation) from the release fragment plus this round's evidence."""
import json
import re
import subprocess
from pathlib import Path

CHK = Path("/tmp/verify-s7-r1-l12")
L = Path("/tmp/ap1-r5/s7-l12/logs")
PREV = Path("/tmp/ap1-r5/s7-l12/L01-L02.release-round24.json")
OUT = CHK / "ledgers/S7/L01-L02.json"
prev = json.loads(PREV.read_text(encoding="utf-8"))
prev_rows = prev["rows"]
prev_ids = [r["id"] for r in prev_rows]
BASE = "5e5da87"
TOOL = ("Python 3.14.8, numpy 2.4.6, scipy 1.18.0, pytest 9.0.2 (the repo .venv), Pyodide 314.0.7 and KaTeX 0.19.1 "
        "(vendored, LOCK.json hashes verified)")
SLICE_FILES = ["course/modules/S/S7/L01.html", "course/modules/S/S7/L02.html", "course/modules/S/S7/cards.json",
               "course/modules/S/S7/figures-L01.js", "course/modules/S/S7/figures-L02.js",
               "tests/labs/S7/lab-S7-L01-1.py", "tests/labs/S7/lab-S7-L01-2.py", "tests/labs/S7/lab-S7-L01-3.py",
               "tests/labs/S7/lab-S7-L01-4.py", "tests/labs/S7/lab-S7-L02-1.py", "tests/labs/S7/lab-S7-L02-2.py",
               "tests/labs/S7/lab-S7-L02-3.py"]
IDENT = {}
for f in SLICE_FILES:
    rc = subprocess.run(["git", "-C", str(CHK), "diff", "--quiet", BASE, "HEAD", "--", f]).returncode
    IDENT[f] = rc == 0
assert all(IDENT.values()), [f for f, v in IDENT.items() if not v]


def log_lines(name: str) -> list[str]:
    return (L / name).read_text(encoding="utf-8").splitlines()


RC = [l for l in log_lines("recompute.log") if l.startswith(("OK", "FAIL"))]
ARITH = [l for l in log_lines("arith_checks.log") if l.startswith(("OK", "FAIL"))]
INTER = [l for l in log_lines("intermediate_values.log") if l.startswith(("OK", "FAIL"))]


def rc_line(cid: str) -> str:
    hits = [l for l in RC if l.split("|")[0].split()[1] == cid]
    assert len(hits) == 1, (cid, hits)
    assert hits[0].startswith("OK"), hits[0]
    return hits[0].split("|", 1)[1].strip()


def arith_line(label: str) -> str:
    hits = [l for l in ARITH + INTER if label in l.split("|")[0]]
    assert hits and all(h.startswith("OK") for h in hits), (label, hits)
    return hits[0].split("|", 1)[1].strip()


def rederived(text: str) -> str:
    return f"Re-derived this round on {TOOL}: {text}"


# ---------------- numeric rows (2.2): every printed number re-derived by the scripts, plus twin outputs -----------
TWIN = {
    "L01-1": "run_labs --page L01 PASS (4/4) and the twin lab-S7-L01-1.py under python -I -W error: rc 0, stderr 0 bytes, stdout identical to the page's expected block (9 lines: 1.538, 2.504, 3.243; exact 1.5388, 2.5076, 3.2414)",
    "L01-2": "run_labs --page L01 PASS and the twin lab-S7-L01-2.py under python -I -W error: rc 0, stderr 0 bytes, stdout 1.612 / 0.034 / 0.52 identical to the page",
    "L01-3": "run_labs --page L01 PASS and the twin lab-S7-L01-3.py under python -I -W error: rc 0, stderr 0 bytes; stdout '1 0.005 0.000 / 5 1.179 1.193 / 20 1.893 1.901' identical to the page",
    "L01-4": "run_labs --page L01 PASS and the twin lab-S7-L01-4.py under python -I -W error: rc 0, stderr 0 bytes; stdout (14 lines: 0.506, 0.0064, 0.578, 0.0179, 7.20, 3.84, 2.25, 0.96) identical to the page",
    "L02-1": "run_labs --page L02 PASS and the twin lab-S7-L02-1.py under python -I -W error: rc 0, stderr 0 bytes; stdout 0.9226/0.0491/0.0491, 0.4713/0.0287/0.0287, 0.1656/0.0056/0.0056 identical to the page",
    "L02-2": "run_labs --page L02 PASS and the twin lab-S7-L02-2.py under python -I -W error: rc 0, stderr 0 bytes; stdout identical to the page (reported and recomputed Holm sets 4,7,8,9 and 2,4,6,7,8,9)",
    "L02-3": "run_labs --page L02 PASS and the twin lab-S7-L02-3.py under python -I -W error: rc 0, stderr 0 bytes; stdout 0.5837/0.5901, 0.5803/0.6212 identical to the page",
}
NUM = {
    "L01-num-s1-variance": [("rc", "L01-num-s1-variance")],
    "L01-num-ex23": [("rc", "L01-num-ex23")],
    "L01-num-rem24": [("rc", "L01-num-rem24")],
    "L01-num-s4-tenyears": [("rc", "L01-num-s4-tenyears")],
    "L01-num-lab2-hyp": [("rc", "L01-num-lab2-hyp")],
    "L01-num-lab2-interp": [("twin", "L01-2")],
    "L01-num-lab3": [("rc", "L01-num-lab3-approx"), ("twin", "L01-3")],
    "L01-num-misc3": [("rc", "L01-num-misc3")],
    "L01-num-misc4": [("rc", "L01-num-misc4")],
    "L01-num-M3": [("rc", "L01-num-M3")],
    "L01-num-P2-P3": [("rc", "L01-num-P2-P3")],
    "L01-num-E3": [("rc", "L01-num-E3")],
    "L01-num-R2": [("rc", "L01-num-R2")],
    "L01-num-quiz": [("rc", "L01-num-quiz")],
    "L01-num-fig-caption-n2": [("rc", "L01-num-fig-caption-n2"), ("rc", "L01-caption-expmax-N3-10000")],
    "L01-num-misc1": [("rc", "L01-num-misc1")],
    "L01-num-rem24-annualized": [("rc", "L01-num-rem24-annualized")],
    "L01-num-fig-density-caption": [("fig", "L01 max-sharpe-density readouts, 20 swept states x 2 themes x 2 widths")],
    "L01-num-s6-intro": [("rc", "L01-num-s6-intro")],
    "L01-num-ex67": [("rc", "L01-num-ex67")],
    "L01-num-s6-bullets": [("rc", "L01-num-M5"), ("rc", "L01-num-M5-min"), ("rc", "L01-num-M5-c")],
    "L01-num-lab4-hyp": [("rc", "L01-lab4-power-identity")],
    "L01-num-lab4-interp": [("twin", "L01-4"), ("misc5", None)],
    "L01-num-rem69": [("rc", "L01-num-rem69")],
    "L01-num-misc5": [("misc5", None), ("twin", "L01-4")],
    "L01-num-M5": [("rc", "L01-num-M5")],
    "L01-num-R4": [("rc", "L01-num-R4")],
    "L01-num-quiz-s6": [("rc", "L01-num-quiz-s6")],
    "L01-num-keyresults-lab4": [("twin", "L01-4")],
    "L02-num-M3": [("rc", "L02-num-M3")],
    "L02-num-s1": [("rc", "L02-num-s1")],
    "L02-num-lab1-hyp": [("rc", "L02-num-lab1-hyp")],
    "L02-num-lab2": [("twin", "L02-2"), ("rc", "L02-digit-second-261-467")],
    "L02-num-ex42": [("rc", "L02-num-ex42")],
    "L02-num-M1": [("rc", "L02-num-M1")],
    "L02-num-M2": [("rc", "L02-num-M2")],
    "L02-num-P1": [("rc", "L02-num-P1")],
    "L02-num-E1": [("rc", "L02-num-E1")],
    "L02-num-E2": [("rc", "L02-num-E2"), ("rc", "L02-digit-second-261-467")],
    "L02-num-E3": [("rc", "L02-num-E3")],
    "L02-num-R2": [("arith", "L02-num-R2")],
    "L02-num-quiz": [("rc", "L02-num-quiz")],
    "L01-num-fig-caption": [("rc", "L01-num-fig-caption-n2")],
    "L01-num-lab1-text-e968af2": [("twin", "L01-1"), ("arith", "L01-lab1-ratio")],
    "L01-num-M2-e968af2": [("rc", "L01-num-M2")],
    "L01-num-E1-display-factor-0f4068a": [("rc", "L01-num-E1")],
    "L01-num-E1-e968af2": [("rc", "L01-num-E1")],
    "L01-num-E2": [("rc", "L01-num-E1")],
    "L01-num-M1-e968af2": [("rc", "L01-num-M1")],
    "L01-num-M4": [("rc", "L01-num-M4")],
    "L01-num-recompute-r19-e968af2": [("rc", "L01-num-ex23"), ("rc", "L01-num-rem24"), ("rc", "L01-num-s6-intro"), ("rc", "L01-num-ex67"), ("rc", "L01-num-M1"), ("rc", "L01-num-M4")],
    "L02-num-recompute-r19-e968af2": [("rc", "L02-num-E1"), ("rc", "L02-num-ex42"), ("rc", "L02-num-M3")],
    "L02-num-misc-e968af2": [("rc", "L02-num-ex24")],
    "L02-num-ex24-e968af2": [("rc", "L02-num-ex24")],
    "L02-num-lab3-interp-e968af2": [("rc", "L02-num-lab3-interp"), ("twin", "L02-3")],
    "L02-num-lab1-interp-e968af2": [("rc", "L02-num-lab1-interp"), ("twin", "L02-1")],
    "L02-almost-surely-84-e968af2": [("rc", "L02-num-s1")],
    "L02-digit-second-261-467-e968af2": [("rc", "L02-digit-second-261-467"), ("rc", "L02-num-E2")],
    "L01-L02-numbers-unmentioned-0f4068a": [("rc", "L01-num-M1"), ("rc", "L01-num-M4"), ("rc", "L01-num-M5")],
    "L01-L02-numbers-sweep-0f4068a": [("rc", "L01-num-M1"), ("rc", "L01-num-M4"), ("rc", "L01-num-E1"), ("rc", "L01-num-M2")],
    "L01-hunk-H2-line588-0f4068a": [("rc", "L01-num-E1")],
    "L01-hunk-H3-line595-0f4068a": [("rc", "L01-num-E1")],
    "L01-L02-expmax-claims-a2a631a": [("rc", "L01-caption-expmax-N3-10000"), ("rc", "L01-num-fig-caption-n2")],
    "L02-cmd-m3-example42-a2a631a": [("rc", "L02-num-M3"), ("rc", "L02-num-ex42")],
    "L01-cmd-m1-m4-a2a631a": [("rc", "L01-num-M1"), ("rc", "L01-num-M4")],
    "L01-cmd-m5-a2a631a": [("rc", "L01-num-M5"), ("rc", "L01-num-M5-min"), ("rc", "L01-num-M5-c")],
    "L01-lab4-prose-numbers-202ea24": [("twin", "L01-4"), ("misc5", None)],
    "L01-cards-c190-num-29pct": [("rc", "L01-num-misc4")],
    "L02-cards-example42-power-recheck": [("rc", "L02-num-ex42")],
    "L02-cards-c221-numbers": [("twin", "L02-1")],
    "L01-cards-c222-numbers": [("twin", "L01-4"), ("rc", "L02-num-E1")],
    "L02-num-P2-corr-values": [("rc", "L02-num-P2-corr-values")],
    "L01-math-share-50-55": [("arith", "L01-math-share-50-55")],
    "L02-num-lab1-interp": [("rc", "L02-num-lab1-interp"), ("twin", "L02-1")],
    "L02-l129-c5-next-lab-pointer": [("twin", "L02-1")],
    "L02-num-P4": [("arith", "L02-num-P4")],
    "L01-lab1-second-table-e968af2": [("twin", "L01-1")],
    "L01-L02-cards-numbers-202ea24": [("rc", "L01-num-ex23"), ("arith", "L01-cards-c147-ratios"), ("arith", "L01-cards-c004-c005"), ("arith", "L01-cards-c004-approx-ratio"), ("rc", "L02-num-M3"), ("rc", "L01-num-quiz")],
    "L02-ex42-numbers-202ea24": [("rc", "L02-num-ex42")],
    "L01-fig-1-caption": [("rc", "L01-num-fig-caption-n2"), ("rc", "L01-caption-expmax-N3-10000")],
    "L02-cards-c232": [("rc", "L02-num-P2-corr-values")],
    "L01-lab4-prose-numbers-202ea24-x": [("twin", "L01-4")],
    "L01-L02-cmd-fig-samples-a2a631a": [("fig", "L01 readouts at years 1, 5, 20 and L02 default states; Python recomputation in logs/fig_expect.log")],
    "L01-L02-cmd-expmax-sweep-a2a631a": [("rc", "L01-caption-expmax-N3-10000"), ("quad", None)],
}
MISC5 = ("exact recursion (scripts/misc5_exact.py, logs/misc5_exact.log, grid dx = 0.01, 26,001 points, FFT convolution): "
         "P(reject at some look among 1..756) = 0.5130 (page: 0.51; Lab 4 simulates 0.506); by look 5 = 0.1420 (table 0.143), "
         "by look 36 = 0.2949 (table 0.297), by look 252 = 0.4407 (table 0.441)")
FIGTEXT = ("live readouts of the two L01 and three L02 figures, 264 states swept (2 themes x 2 widths: "
           "max-sharpe-density 20 x 4, fwer-growth 10 x 4, power-family 36 x 4) and compared with Python "
           "(scripts/fig_sweep.py, logs/fig_sweep.json, logs/fig_sweep_check.log): 0 mismatches; "
           "holm-staircase 2 states (logs/holm_states.log)")
QUAD = "adaptive quadrature (scipy.integrate.quad) against the trapezoid grid for N = 2, 3, 4, 10, 100, 1000, 10000: max |difference| 3.75e-13 (logs/expmax_quad_validation.log)"

rows_out: list[dict] = []
handled = set()


def emit(row_id: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> None:
    r = {"id": row_id, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows_out.append(r)
    handled.add(row_id)


# 1) numeric rows
for prev_row in prev_rows:
    rid = prev_row["id"]
    if prev_row["check"] != "2.2-number" or rid not in NUM or rid in ("L01-L02-cmd-fig-samples-a2a631a", "L01-L02-cmd-expmax-sweep-a2a631a"):
        continue
    parts = []
    for kind, key in NUM[rid]:
        if kind == "rc":
            parts.append(f"{key}: {rc_line(key)}")
        elif kind == "arith":
            parts.append(f"{key}: {arith_line(key)}")
        elif kind == "twin":
            parts.append(f"{key}: {TWIN[key]}")
        elif kind == "misc5":
            parts.append(MISC5)
        elif kind == "fig":
            parts.append(FIGTEXT)
        elif kind == "quad":
            parts.append(QUAD)
    ev = rederived("; ".join(parts) + f" [original scratch-scripted row evidence replaced; page location {prev_row['location'][:90]}]")
    if rid in ("L01-num-s6-bullets",):
        ev += " Also: the printed 'about 0.11' and '3.2% lower' re-checked: 1/(1+u*) = 0.1086; b756 ratio 3.035/3.136 - 1 = -3.2%."
    emit(rid, "2.2-number", prev_row["location"], "PASS", ev)
# any 2.2 row not in NUM stays unhandled -> must not happen
missing_num = [r["id"] for r in prev_rows if r["check"] == "2.2-number" and r["id"] not in NUM]
assert not missing_num, missing_num

# 2) command / gate rows (re-run this round; exact outputs in logs/)
CMD = {
 "L01-L02-cmd-run_labs-S7-a2a631a": ("2.5-lab", "tools/run_labs.py --unit S7 --page L01 and --page L02", "PASS",
   "Command: .venv/bin/python tools/run_labs.py --unit S7 --page L01 (rc 0): 'run_labs S7: PASS (4/4)'; with --page L02 (rc 0): 'run_labs S7: PASS (3/3)' (logs/run_labs_L01.log, logs/run_labs_L02.log). The unit-wide run over other lessons was not repeated (outside this slice). Tooling: " + TOOL + "."),
 "L01-L02-cmd-run_labs-L01-a2a631a": ("2.5-lab", "tools/run_labs.py --unit S7 --page L01", "PASS",
   "Command: .venv/bin/python tools/run_labs.py --unit S7 --page L01 (rc 0). Printed: 'run_labs S7: PASS (4/4)' (logs/run_labs_L01.log)."),
 "L01-L02-cmd-run_labs-L02-a2a631a": ("2.5-lab", "tools/run_labs.py --unit S7 --page L02", "PASS",
   "Command: .venv/bin/python tools/run_labs.py --unit S7 --page L02 (rc 0). Printed: 'run_labs S7: PASS (3/3)' (logs/run_labs_L02.log)."),
 "L01-L02-cmd-lab-twins-a2a631a": ("2.5-lab", "tests/labs/S7/lab-S7-L01-1..4, L02-1..3 under python -I -W error", "PASS",
   "Command (each twin, from an empty mktemp directory): /tmp/verify-s7-r1-l12/.venv/bin/python -I -W error tests/labs/S7/lab-S7-<id>.py: rc 0 for all seven, stderr 0 bytes each; stdout line counts 9, 3, 4, 14, 4, 6, 5 (L01-1..4, L02-1..3); a second run from a different empty directory reproduces the first run's stdout byte-for-byte (logs/twin-*.out, logs/twin2-*.out). Ruff/mypy: see L01-L02-cmd-ruff-mypy-a2a631a."),
 "L01-L02-cmd-ruff-mypy-a2a631a": ("2.5-lab", ".venv/bin/ruff check, ruff format --check, mypy on the seven slice twins", "PASS",
   "Commands: .venv/bin/ruff check tests/labs/S7/lab-S7-L01-*.py tests/labs/S7/lab-S7-L02-*.py: 'All checks passed!' (rc 0); .venv/bin/ruff format --check on the same seven files: '7 files already formatted' (rc 0); .venv/bin/mypy on the seven files: 'Success: no issues found in 7 source files' (rc 0). Full-repo mypy and ruff were not repeated (no file outside the slice changed for this slice; pyproject.toml changed only in the toolchain pins and the two S7 L03/L08 excludes)."),
 "L01-L02-cmd-lab-twins-S7-a2a631a": ("2.5-lab", "lab twins", "PASS", "See L01-L02-cmd-lab-twins-a2a631a."),
 "L01-L02-lab-timings-0f4068a": ("2.5-lab", "tools/page_smoke.py --unit S7 --pages L01 L02: lab timings", "PASS",
   "Command: .venv/bin/python tools/page_smoke.py --unit S7 --pages L01 L02 (rc 0; logs/page_smoke.log): runtime boot (with numpy) 1.0 s, package preload 0.2 s; lab timings L01-1 0.2 s, L01-2 0.2 s, L01-3 0.2 s, L01-4 0.5 s, L02-1 0.1 s, L02-2 0.0 s, L02-3 0.1 s, all against the 10 s budget (LAB_LIMIT_S = 10.0 in tools/page_smoke.py). Runtime: Pyodide 314.0.7 (vendored, LOCK.json hashes match)."),
 "L01-L02-cmd-page_smoke-a2a631a": ("2.8-figure", "tools/page_smoke.py --unit S7 --pages L01 L02", "PASS",
   "Command: .venv/bin/python tools/page_smoke.py --unit S7 --pages L01 L02 (rc 0; logs/page_smoke.log): 'page_smoke modules/S/S7/L01.html: PASS', 'page_smoke modules/S/S7/L02.html: PASS', 'page_smoke S7: PASS'. Covers both pages in light and dark at 1280 px and 360 px: zero console errors, zero page errors, zero external requests, KaTeX parsed with throwOnError and strict 'error', no horizontal scroll at 360 px, every chart has title and desc, every chart's text inside its SVG, and the light-theme sweep of every live control (no text leaves its SVG, overlaps, or is crossed by a mark)."),
 "L01-L02-fig-screens-e968af2": ("2.8-figure", "tools/page_smoke.py figure sweep and geometry", "PASS", "Re-run: see L01-L02-cmd-page_smoke-a2a631a (both pages PASS, light sweep at 1280 px and 360 px) and the 264-state readout sweep in L01-L02-cmd-fig-drive-a2a631a."),
 "L01-L02-fig-screens-765bcb1": ("2.8-figure", "tools/page_smoke.py figure sweep and geometry", "PASS", "Re-run: see L01-L02-cmd-page_smoke-a2a631a."),
 "L01-L02-cmd-pytest-figure-kernels-a2a631a": ("2.8-figure", "pytest tests/test_figure_kernels.py tests/test_docs_figures.py tests/test_run_labs.py", "PASS",
   "Command: .venv/bin/python -m pytest <file> -p no:cacheprovider -q: tests/test_figure_kernels.py '32 passed' (rc 0); tests/test_docs_figures.py '14 passed' (rc 0); tests/test_run_labs.py '6 passed' (rc 0); together '52 passed in 17.21s'. The test_figure_kernels tolerance change (tests/test_figure_kernels.py, lines 352-362: rel = max(1e-12, 5e-14*(n-1))) is in the run. Logs: logs/pytest_*.log, logs/pytest_slice.log."),
 "L01-L02-cmd-fig-drive-a2a631a": ("2.8-figure", "live figures driven in Chromium (Playwright, venv) over every control state", "PASS",
   "Command: .venv/bin/python -I scripts/fig_sweep.py (Chromium; page_smoke's own local server; no network) then scripts/fig_sweep_check.py: 264 states = (light, dark) x (1280 px, 360 px) x (L01 max-sharpe-density 20 years; L02 fwer-growth 10 alpha values; L02 power-family 36 mu values). Each state's readout (or desc) equals the Python recomputation: 'states' 264, 'mismatches' 0 (logs/fig_sweep_check.log); page errors 0 in every run (logs/fig_sweep_run.log). Holm staircase: its select control's two states (reported, recomputed) x 2 themes x 2 widths read from the live desc: Holm rejects 4,7,8,9 and 2,4,6,7,8,9; Bonferroni rejects 4,7,8 in both, equal to the Lab 2 output (logs/holm_states.log). Not repeated: the 276-state count of the release run (the states now are 264 + 8 Holm)."),
 "L01-L02-cmd-fig-samples-a2a631a": ("2.2-number", "live readouts at chosen states", "PASS", "Command: scripts/fig_states.py (years 1, 5, 20) and scripts/fig_expect.py: L01 readouts '1 year ... 1.54, 2.51, 3.24; ... 1.000', '5 years (T = 1,260) ... 0.69, 1.12, 1.45; ... 0.721', '20 years (T = 5,040) ... 0.34, 0.56, 0.72; ... 0.000' equal the Python values 1.54/2.51/3.24, 0.69/1.12/1.45, 0.34/0.56/0.72 and 1.000, 0.721, 0.000 (logs/fig_states.log, logs/fig_expect.log)."),
 "L01-L02-cmd-expmax-sweep-a2a631a": ("2.2-number", "scripts/recompute.py (N = 2..10000 sweep) and quadrature validation", "PASS", "Command: .venv/bin/python -I scripts/recompute.py (rc 0; all OK lines in logs/recompute.log), approx minus exact over N = 3..10000: min 0.006520, max 0.035846 (absolute), all positive; N = 2 approximation 0.519755 < exact 0.564190. " + QUAD + "."),
 "L01-L02-cmd-check_pages-a2a631a": ("2.9-structure", "tools/check_pages.py --unit S7", "PASS", "Command: .venv/bin/python tools/check_pages.py --unit S7 (rc 0): 'check_pages S7: PASS' (logs/check_pages.log)."),
 "L01-L02-cmd-check_dag-a2a631a": ("2.9-structure", "tools/check_dag.py --unit S7", "PASS", "Command: .venv/bin/python tools/check_dag.py --unit S7 (rc 0): 'check_dag S7: PASS' (logs/check_dag.log). Independent re-check (scripts/structure_checks.py): 39 concepts the curriculum assigns to S7; 39 <dfn data-concept> in L01-L08; no duplicates; none defined outside the assignment; none assigned but undefined."),
 "L01-L02-dag-a2a631a": ("2.9-structure", "check_dag and concept definitions", "PASS", "Re-run: check_dag S7 PASS (L01-L02-cmd-check_dag-a2a631a) and scripts/structure_checks.py: 39 = 39, duplicates none, L01 data-cite keys 15 and L02 3, all resolve in references.json (560 entries)."),
 "L01-L02-dag-e968af2": ("2.9-structure", "check_dag and concept definitions", "PASS", "Re-run: see L01-L02-dag-a2a631a (check_dag S7 PASS; 39 concept definitions, no duplicates)."),
 "L01-L02-cmd-dfn-check-a2a631a": ("2.9-structure", "concept-definition check", "PASS", "Command: .venv/bin/python -I scripts/structure_checks.py /tmp/verify-s7-r1-l12 (logs/structure_checks.log): 'concepts the curriculum assigns to S7: 39'; 'S7 lesson <dfn data-concept> count 39 duplicates []'; 'defined but not assigned to S7: []'; 'assigned to S7 but not defined in S7: []'. Original scratch dfn_check.py no longer exists; this re-implementation checks the same three counts."),
 "L01-L02-cmd-check_projects-a2a631a": ("2.6-projects", "tools/check_projects.py --unit S7", "PASS", "Command: .venv/bin/python tools/check_projects.py --unit S7 (rc 0): 'check_projects S7: PASS' (logs/check_projects.log). No project belongs to L01 or L02; the unit's project page course/modules/S/S7/project.html is the only S7 file that changed in the delta (one line, the Python-version sentence), outside this slice."),
 "L01-L02-cmd-render_curriculum-a2a631a": ("2.9-structure", "tools/render_curriculum.py and git diff --exit-code of its outputs", "PASS", "Commands: .venv/bin/python tools/render_curriculum.py (rc 0); then git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json (rc 0, no change). S7 module hours unchanged (curriculum.json hunks touch MS-FIN, PHD-FIN and the closure lists only)."),
 "L01-L02-cmd-build_site-a2a631a": ("2.9-structure", "tools/build_site.py --check", "PASS", "Command: .venv/bin/python tools/build_site.py --check (rc 0): 'site data current: 6 outputs' (logs/build_site.log)."),
 "L01-L02-cmd-fetch_data-a2a631a": ("2.8-figure", "tools/fetch_data.py --check", "PASS", "Command: .venv/bin/python tools/fetch_data.py --check (rc 0): 'fetch_data: 3 datasets, 0 problems' (logs/fetch_data.log). The L01/L02 pages read no snapshot; tools/data_sources.yaml gained two note paragraphs (H.10 rates); no data file changed."),
 "L01-L02-cmd-verify_refs-live-S7-a2a631a": ("2.1-citation", "tools/verify_refs.py --unit S7 --workers 1 (live)", "PASS", "Command: .venv/bin/python tools/verify_refs.py --unit S7 --workers 1 (rc 0), live: 'live re-verification of S7: 94 of 560 entries, 0 problems' (logs/verify_refs_live.log). koning2026anytime is among the entries re-resolved; the registry count is now 560 (was 558 at the round-24 pin)."),
 "L01-L02-cmd-verify_refs-offline-a2a631a": ("2.1-citation", "tools/verify_refs.py --offline", "PASS", "Command: .venv/bin/python tools/verify_refs.py --offline (rc 0): 'offline integrity: 560 entries, 0 problems' (logs/verify_refs_offline.log)."),
 "L01-L02-cmd-crossref-koning-a2a631a": ("2.1-citation", "Crossref metadata of koning2026anytime", "PASS", "Re-run through tools/verify_refs.py --unit S7 (live, 94 entries, 0 problems; logs/verify_refs_live.log), which re-resolves every S7 registry entry including koning2026anytime against Crossref. The earlier direct Crossref call was not repeated separately."),
 "L01-L02-cmd-fetch_data-a2a631a-x": ("2.8-figure", "fetch_data", "PASS", "See L01-L02-cmd-fetch_data-a2a631a."),
 "L01-L02-cmd-git-a2a631a": ("2.9-structure", "git state and slice-file identity", "PASS", "Commands: git rev-parse --short HEAD = bcf4e25; git status --short: only untracked .venv (symlink), data-tooling.json and history (pre-existing, not part of the slice); git diff --quiet 5e5da87 HEAD -- course/modules/S/S7/L01.html course/modules/S/S7/L02.html course/modules/S/S7/cards.json course/modules/S/S7/figures-L01.js course/modules/S/S7/figures-L02.js tests/labs/S7 (rc 0: all byte-identical); git diff --stat 5e5da87 HEAD over the listed paths: 55 files, only course/modules/S/S7/project.html of the S7 tree changed."),
 "L01-L02-cmd-prose-scan-a2a631a": ("2.9-banned", "banned strings and question marks in visible prose", "PASS", "Command: .venv/bin/python -I scripts/prose_scan.py logs (logs/prose_scan.log): BUILDER_RULES 1.3-1.4 strings ('TODO', 'TBD', 'lorem', 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'experts agree', 'it is well known', 'obviously', 'clearly'): 0 hits in L01 and L02. 'roughly': L01 2 (lines 60, 477 of the visible text), L02 1 (line 87); 'about ': see L01-banned-roughly-half. Ellipsis '…': L01 2 (quiz cloze stems at visible lines 445, 458), L02 3 (310, 325, 346); '?': L01 25, L02 13 (same counts as round 24). BUILDER_RULES.md unchanged in the delta."),
 "L01-L02-banned-scan-a2a631a": ("2.9-banned", "banned strings scan", "PASS", "See L01-L02-cmd-prose-scan-a2a631a (same scan, same counts: 0 banned hits; 5 quiz-cloze ellipses; 25 and 13 question marks)."),
 "L01-L02-banned-scan-0f4068a": ("2.9-banned", "banned strings scan", "PASS", "See L01-L02-cmd-prose-scan-a2a631a."),
 "L01-L02-question-sweep-0f4068a": ("2.9-banned", "question-mark sweep", "PASS", "See L01-L02-cmd-prose-scan-a2a631a: '?' counts L01 25, L02 13, unchanged."),
 "L01-L02-cmd-cards-scan-a2a631a": ("2.7-cards", "full card scan (all S7 cards) and the L01/L02 subset", "PASS", "Command: .venv/bin/python -I scripts/structure_checks.py /tmp/verify-s7-r1-l12 and scripts/prose_scan.py (logs/structure_checks.log, logs/prose_scan.log): 'cards total 243 S7 cards 243 L01 29 L02 27'; 'duplicate ids []'; 'duplicate fronts []'; 'cite keys in S7 cards not in registry: []'; 'A/B/D without cite: []'; 'C without basis' for L01/L02: none (the five C cards without basis, S7-c069, c163, c214, c234, c241, are in L06-L08, outside this slice). The scratch cards_scan.py no longer exists; this re-implements its inventory and checks."),
 "L01-L02-cards-scan-a2a631a": ("2.7-cards", "full card scan", "PASS", "See L01-L02-cmd-cards-scan-a2a631a (243 cards, 56 for L01/L02, no duplicates, cite keys resolve, grade rules hold for the slice)."),
 "L01-L02-cmd-refs-render-a2a631a": ("2.1-citation", "references section: cited keys resolve; page renders with no errors", "PASS", "Commands: scripts/structure_checks.py (distinct data-cite keys: L01 15, L02 3; all resolve in references/references.json, 560 entries; logs/structure_checks.log) and tools/page_smoke.py --pages L01 L02 (zero console errors, zero page errors, zero external requests: logs/page_smoke.log). The #references character counts of the release run (3,025 and 560) were not re-measured."),
 "L01-L02-refs-render-a2a631a": ("2.1-citation", "references section render", "PASS", "See L01-L02-cmd-refs-render-a2a631a."),
 "L01-L02-refs-render-765bcb1": ("2.1-citation", "references section render", "PASS", "See L01-L02-cmd-refs-render-a2a631a."),
 "L01-cite-refs-render": ("2.1-citation", "references section render", "PASS", "See L01-L02-cmd-refs-render-a2a631a: 15 distinct keys in L01, all resolve; page_smoke zero errors."),
 "L02-cite-refs-render": ("2.1-citation", "references section render", "PASS", "See L01-L02-cmd-refs-render-a2a631a: 3 distinct keys in L02, all resolve; page_smoke zero errors."),
 "L01-L02-cmd-git-a2a631a-x": ("2.9-structure", "git", "PASS", "See L01-L02-cmd-git-a2a631a."),
 "L01-L02-hours-a2a631a": ("2.9-structure", "hours", "PASS", "Re-run: check_pages S7 PASS (L01-L02-cmd-check_pages-a2a631a); data-hours in L01.html and L02.html unchanged (byte-identical)."),
 "L01-cmd-koning-spot-a2a631a": ("2.4-math", "python -I scripts/koning_spot.py (numpy seed 20261021, 400,000 paths)", "UNVERIFIABLE",
   "The round-24 command ran scripts/koning_spot.py from a scratch directory (/tmp/claude-0/...scratchpad/verify54h-L01-L02/r24/scripts/) that no longer exists in any checkout or in the repository, so it cannot be re-run as written; its printed values (0.0 max deviation, 0.05 size, 0.05012 ... 0.05004 stopping-time sizes) were not reproduced. A replacement check of the same claims (scripts/koning_replacement.py, logs/koning_replacement.log: claim 3 max deviation 0.0; martingale E_P[phi_n] in [0.0495, 0.0499]; E_P[phi_tau] = 0.04966, 0.04981, 0.04999 for three stopping times; size 0.04984) passes, but it is not the original check and does not count toward this row."),
 "L01-math-koning-theorem1-proof-a2a631a": ("2.4-math", "Koning-van Meer Theorem 1 proof as used by the L01 span", "PASS",
   "Carried proof (the subject, L01.html line 436 span, is byte-identical since 5e5da87; the proof is analytic): (i) E[phi_n | F_{n-1}] = phi_{n-1} by the tower property; (ii) values in [0,1] give uniform integrability, so E[phi_tau] = E[phi] for every stopping time tau, and a valid phi gives sup_tau E[phi_tau] <= alpha (claim 1); (iii) phi F_N-measurable gives phi_N = phi (claim 3), so 'matches it after N observations' follows from claims 1 and 3. Re-checked this round by reading the steps. The numerical spot-check that the round-24 row cited is NOT part of this verdict: its script is gone (see L01-cmd-koning-spot-a2a631a); the replacement check (logs/koning_replacement.log) is consistent with the claims, but it does not stand in for the original."),
}
for rid, (chk, loc, status, ev) in CMD.items():
    if rid.endswith("-x") or rid == "L01-L02-cmd-lab-twins-S7-a2a631a":
        continue
    emit(rid, chk, loc, status, ev,
         fix=("Commit the spot-check script to tools/ or tests/, so the row can be re-run from the repository, and re-run it; the round-24 scratch copy is gone." if status != "PASS" else None))

# lab rows (2.5) re-run through run_labs and twins
for rid in ["L01-lab-1-a2a631a", "L01-lab-2-a2a631a", "L01-lab-3-a2a631a", "L01-lab-4-a2a631a",
            "L02-lab-1-a2a631a", "L02-lab-2-a2a631a", "L02-lab-3-a2a631a"]:
    key = rid.split("-")[0] + "-" + rid.split("-")[2]
    emit(rid, "2.5-lab", f"{rid.split('-')[0]} lab {key.split('-')[1]} (tests/labs/S7/lab-S7-{key}.py) and its page expected block",
         "PASS", f"Re-run: run_labs --page {rid.split('-')[0]} PASS (logs/run_labs_{rid.split('-')[0]}.log) and the twin under python -I -W error: " + TWIN[key] + ". Page_smoke timing for this lab is in L01-L02-lab-timings-0f4068a. Runtime Pyodide 314.0.7.")
emit("L01-lab-1-simulated-label-e968af2", "2.5-lab", "L01 Lab 1 SIMULATED label (course/modules/S/S7/L01.html, lab 1 comment)", "PASS",
     "Re-run: run_labs --page L01 PASS (4/4); the page's '# SIMULATED' comment is inside the twin code that matched (logs/run_labs_L01.log). The label is unchanged since 5e5da87 (L01.html byte-identical).")
emit("L02-lab3-power-e968af2", "2.5-lab", "L02 Lab 3 power (tests/labs/S7/lab-S7-L02-3.py; page expected block)", "PASS",
     "Re-run: run_labs --page L02 PASS (3/3) and the twin lab-S7-L02-3.py under python -I -W error: rc 0, stderr 0 bytes; stdout 0.5837 / 0.6212 power and 0.0423 ... FWER values identical to the page (logs/twin2-L02-3.out).")

# structure rows that were re-run as commands (check_pages / check_dag already emitted)

# ---- new rows (this round's new checks only) ----
NEW = [
 ("T33-notation-collision", "2.4-math", "notation/notation.json (+4 AP1 symbols), course/assets/data/notation.json, L01.html, L02.html", "PASS",
  "Delta: notation.json gained four entries (R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}, all module AP1; the file's 'symbols' now has 8 entries; macros unchanged; diff in git diff 5e5da87 HEAD -- notation). Collision check on the slice: grep of L01.html and L02.html for R^\\ast, R^{e\\ast}, R_f and \\mathbb{Q} gives 0 hits; the registered symbols therefore keep their meaning on the slice. The lowercase \\ast appears only as a local superscript on letters that the registry does not register (n^\\ast, u^\\ast, alpha^\\ast(t), k^\\ast, x^\\ast; L01 lines 70-71, 453, 536-541, 658; L02 line 289). The registry's R^\\ast entry says it is defined in AP1 'where it is written x^\\ast', and L02 line 289 uses x^\\ast for a threshold; x^\\ast is not a registered symbol, so no registry rule (BUILDER_RULES 3.2) is broken, but a reader meeting both uses should be warned (advisory, not a failure). The registry's macros (\\E, \\Prob, \\SR, ...) are unchanged. Evidence: git diff 5e5da87 HEAD -- notation course/assets/data/notation.json; grep of the slice (logs/ and this round's session)."),
 ("T33-glossary-program-links", "2.9-structure", "course/assets/data/glossary.json, program.json, L01.html, L02.html (concept links)", "PASS",
  "Delta: glossary.json gained 9 AP1 entries and changed none of the S7 entries (diff: 0 removed, 0 changed keys among the 39 pre-existing ids; 'arbitrage-linear-program', 'equivalent-martingale-measure', 'fundamental-theorem-of-asset-pricing', 'law-of-one-price', 'minimum-variance-sdf', 'sdf-existence-uniqueness', 'sdf-mean-variance-frontier', 'state-price', 'stochastic-discount-factor' are new, none collides with an S7 concept id). program.json changed hours and FC1/M8 closure lists for MS-FIN and PHD-FIN only; no S7 module hours changed (curriculum.json has no S7 hunk). The slice's concept links (scripts/structure_checks.py and a link-id check against curriculum.json concepts): L01 has 17 concept links over 9 distinct ids and L02 has 9 links over 5 distinct ids; all 14 distinct ids are curriculum concept ids, and none of the L01 ids is a glossary id; L02's data-snooping-bias is the one glossary id (S7, unchanged). None of the new AP1 glossary ids collides with a link id. L01 defines 9 concepts and L02 defines 3 (39 unit definitions, none duplicated; check_dag S7 PASS; check_pages S7 PASS; build_site --check PASS)."),
 ("T33-pyodide314-vendor", "2.5-lab", "course/assets/vendor (LOCK.json, SPEC.yaml), tools/vendor_spec.yaml; labs run in Pyodide 314.0.7", "PASS",
  "Vendor check (python script over course/assets/vendor/LOCK.json): 56 files, 0 missing, 0 sha256 mismatches. KaTeX: course/assets/vendor/katex/katex.min.js carries version:\"0.19.1\" (LOCK: katex@0.19.1). Pyodide: course/assets/vendor/pyodide holds numpy-2.4.6-cp314 and scipy-1.18.0-cp314 wheels, pytest-9.0.2, pyodide.asm.mjs and python_stdlib.zip (SPEC.yaml pins 314.0.7). page_smoke loaded both pages with zero external requests (vendored only) and ran all seven labs in that runtime (logs/page_smoke.log: boot 1.0 s, labs 0.0-0.5 s, budget 10 s)."),
 ("T33-registry-entries", "2.1-citation", "references/references.json (17 keys cited by L01 and L02)", "PASS",
  "Registry delta: 560 entries before and after; 0 added, 0 removed; 0 entries changed in content apart from used_by (inline comparison of git show 5e5da87:references/references.json against HEAD, output in logs/refs_entry_diff.log). used_by changed for hansen1991implications, kalyuga2003expertise, shleifer1997limits and tetzlaff2025cornerstone (AP1 added; S7 membership unchanged). The 17 keys cited by the slice (L01: 15; L02: 3; union 17) have identical content and identical S7 membership, so every citation and grade row whose subject is the registry entry is carried. Live verification: 94 entries, 0 problems (L01-L02-cmd-verify_refs-live-S7-a2a631a)."),
 ("T33-decimal-coverage", "2.2-number", "every decimal in the visible prose of L01 and L02 (327 distinct tokens)", "PASS",
  "Completeness check of the numeric rows: the visible prose of L01 and L02 contains 327 distinct decimal tokens (scripts; the token list is reproducible by a regex over the text dumps). Before this round's scripts, 49 of them were not printed by any log or script. All 49 were recomputed: 41 intermediate values in logs/intermediate_values.log, the quantile arguments 1-1/(20e) = 0.981606, 1-1/(50e), Phi^-1(0.9995), Phi^-1(0.99995), 0.05/7 and 0.05/3 in logs/quantile_args.log, and the rest appear in the recomputed checks (logs/recompute.log, logs/arith_checks.log); 6.8 and 6.9 are section numbers and 1.05 is the problem's given value (3 of the 41 match only with the page's displayed-input arithmetic, namely 0.6955 = 0.4228 x 1.6449, 1.2052 = 0.5772 x 2.0881, 7436.82 = 1008 x 7.3778, which the page computes from its displayed inputs; from unrounded inputs the values are 0.6954, 1.2053 and 7436.78, which the page also states for 7436.78).  Advisory: displayed-input rounding in M1(b), M4(c) and Example 6.7."),
 ("T33-misc5-recursion", "2.2-number", "L01 misconception 5 (line 475 visible: '0.51') and Lab 4's table", "PASS",
  "Exact recursion of the daily z-test rejection share (scripts/misc5_exact.py, logs/misc5_exact.log): 0.5130 within 756 looks, against the page's 0.51 and Lab 4's simulated 0.506; table values exact 0.1420 (look 5, table 0.143), 0.2949 (look 36, table 0.297), 0.4407 (look 252, table 0.441). The simulated table is within Monte Carlo error of the exact recursion."),
 ("T33-holm-states", "2.8-figure", "course/modules/S/S7/figures-L02.js holm-staircase; L02.html section 3", "PASS",
  "Both states of the Holm select control, light and dark at 1280 and 360 px (logs/holm_states.log): as published: Holm rejects 4, 7, 8, 9; Bonferroni 4, 7, 8. Recomputed: Holm rejects 2, 4, 6, 7, 8, 9; Bonferroni 4, 7, 8. Both equal the Lab 2 output and the page text; the desc is the one the figure computes."),
]
for rid, chk, loc, status, ev in NEW:
    emit(rid, chk, loc, status, ev)

# 3) carried rows: every other row keeps its release verdict, with the carry prefix and the subject files
CHANGED_WORDS = ("tools/", "notation", "glossary", "program.json", "css", "page_smoke", "katex", "pyodide", "vendor", "BUILDER", "VERIFIER", "BLUEPRINT")
carried_flags = []
for prev_row in prev_rows:
    rid = prev_row["id"]
    if rid in handled:
        continue
    if prev_row["status"] != "PASS":
        raise SystemExit(f"release row {rid} is not PASS; this round must re-check it explicitly")
    text = prev_row["location"] + " " + prev_row["evidence"]
    if any(w in text for w in CHANGED_WORDS):
        carried_flags.append(rid)
    files = []
    if "L01" in rid and "L02" not in rid or "L01" in prev_row["location"]:
        files.append("course/modules/S/S7/L01.html")
    if "L02" in rid or "L02.html" in prev_row["location"]:
        files.append("course/modules/S/S7/L02.html")
    if "L01-L02" in rid and not files:
        files = ["course/modules/S/S7/L01.html", "course/modules/S/S7/L02.html"]
    if "cards" in rid or "cards.json" in text:
        files.append("course/modules/S/S7/cards.json")
    lesson = "L01" if ("L01" in rid or "L01.html" in prev_row["location"]) else ("L02" if ("L02" in rid or "L02.html" in prev_row["location"]) else None)
    if ("fig" in rid or "figures-L0" in text) and lesson:
        files.append(f"course/modules/S/S7/figures-{lesson}.js")
    if "lab" in rid and lesson:
        files.append(f"tests/labs/S7/lab-S7-{lesson}-*.py")
    files = list(dict.fromkeys(files)) or ["course/modules/S/S7/L01.html", "course/modules/S/S7/L02.html"]
    registry = prev_row["check"] == "2.1-citation" or prev_row["check"] == "2.3-grade" and ("cite" in text.lower() or "data-cite" in text)
    if registry:
        prefix = ("Carried from the release ledger (" + ", ".join(files) + " byte-identical since 5e5da87; "
                  "references/references.json entries of the cited keys content-identical since 5e5da87 except used_by, see T33-registry-entries):")
    else:
        prefix = "Carried from the release ledger (" + ", ".join(files) + " byte-identical since 5e5da87):"
    suffix = ""
    if rid in carried_flags:
        suffix = (" [round 33 check of this row's dependency words: the S7 pages load course.css, print.css, site.js, labs.js, python.js, "
                  "math.js, quiz.js, refs.js, store.js, fsrs.js, chart.js, stats.js and multitest.js, all byte-identical since 5e5da87; "
                  "course/assets/css/base.css, components.css, tokens.css, lab.js, data.js and theme.js are new files that the S7 pages do not load; "
                  "the vendored runtime pins changed (KaTeX 0.19.1, Pyodide 314.0.7) and were re-run by page_smoke, run_labs and the figure sweep: all PASS.]")
    emit(rid, prev_row["check"], prev_row["location"], "PASS", prefix + " " + prev_row["evidence"] + suffix)

# unique ids and totals
ids = [r["id"] for r in rows_out]
assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
missing = [i for i in prev_ids if i not in set(ids)]
print("release ids not emitted:", missing)
assert not missing, missing
print("rows out", len(rows_out), "carried-with-changed-words:", carried_flags)

# ---------------- top-level fields and summary ----------------
from datetime import datetime, timezone  # noqa: E402

carried = [r for r in rows_out if r["evidence"].startswith("Carried from the release ledger")]
unver = [r["id"] for r in rows_out if r["status"] == "UNVERIFIABLE"]
fails = [r["id"] for r in rows_out if r["status"] == "FAIL"]
passes = [r for r in rows_out if r["status"] == "PASS"]
verdict = "PASS" if len(passes) == len(rows_out) else "FAIL"
new_ids = [r["id"] for r in rows_out if r["id"] not in set(prev_ids)]
rerun_ids = [r["id"] for r in rows_out if r["id"] in set(prev_ids) and r["id"] in CMD]
notes = [
 "ROUND 33: toolchain re-confirmation of the released S7 L01-L02 slice (release commit 5e5da87; checkout bcf4e25). "
 f"Toolchain: {TOOL}. Delta read: git diff --stat 5e5da87 HEAD over the listed paths (55 files); the S7 files changed are only course/modules/S/S7/project.html (outside the slice). "
 "The slice's own files (L01.html, L02.html, cards.json, figures-L01.js, figures-L02.js, the seven twins) are byte-identical since 5e5da87 (git diff --quiet, all rc 0).",
 "Command rows re-run this round, all on the new toolchain: run_labs (L01 4/4, L02 3/3), the seven twins under python -I -W error (rc 0, stderr 0 bytes, repeated twice), check_pages, check_dag, check_projects, page_smoke for L01 and L02 (PASS; boot 1.0 s; lab timings 0.0-0.5 s against the 10 s budget), verify_refs --unit S7 (live: 94 of 560 entries, 0 problems) and --offline (560 entries, 0 problems), fetch_data --check, render_curriculum (no diff), build_site --check, pytest (test_figure_kernels 32, test_docs_figures 14, test_run_labs 6: all passed), ruff check, ruff format --check and mypy on the slice twins, and the figure sweep (264 states plus 8 Holm states, 0 mismatches).",
 "Numeric rows: every numeric row was re-derived with scripts/recompute.py (47 checks, all OK; logs/recompute.log), scripts/misc5_exact.py, scripts/arith and the intermediate-value checks (logs/arith_checks.log, logs/intermediate_values.log), and the figure readouts (logs/fig_sweep_check.log). Three display-rounding conventions are noted (T33-decimal-coverage).",
 "Scratch-dependent round-24 command rows whose scripts no longer exist (scratchpad under /tmp/claude-0): cards_scan, dfn_check, prose_scan, refs_render, fig_drive, fig_samples, expmax_sweep, m1_m4_m3_check, m3_power_check, m5_check and koning_spot. Each has an equivalent re-run in this round's scripts (scripts/structure_checks.py, prose_scan.py, fig_sweep.py, fig_states.py, recompute.py, misc5_exact.py, expmax quadrature), and the row evidence says so. koning_spot alone cannot be reproduced, so its row is UNVERIFIABLE (L01-cmd-koning-spot-a2a631a); the Koning Theorem 1 math row (L01-math-koning-theorem1-proof-a2a631a) stands on the analytic proof, which was re-derived, and is not counted against the spot-check.",
 "Carried rows: every release row whose subject files are byte-identical since 5e5da87 keeps its PASS with the prefix 'Carried from the release ledger (<files> byte-identical since 5e5da87):'. Citation and grade rows whose subject is a registry entry carry the registry proof: the 17 keys the slice cites are content-identical in references/references.json (only used_by changed, for hansen1991implications, kalyuga2003expertise, shleifer1997limits and tetzlaff2025cornerstone, each gaining AP1; S7 membership unchanged).",
 "Notation (T33-notation-collision): the four AP1 symbols do not occur in the slice; the lowercase \\ast local superscripts (x^\\ast on L02 line 289 among them) are not registered symbols. Advisory only.",
 "Advisories (not failures): (a) the figure readout prints 'probability 0.000' at 20 years where the value is 0.0004 (BUILDER_RULES prefers '< 0.001'); (b) the L01 caption's 'loose by roughly half a standard deviation' is 0.48-0.61 in units of a standard normal statistic, not of the maximum's sd (1.0-1.35); (c) display-rounding in M1(b), M4(c) and Example 6.7 (page arithmetic from displayed inputs; from unrounded inputs the last digit differs); (d) S7 cards S7-c069, c163, c214, c234 and c241 (lessons L06-L08, outside this slice) are grade C without basis.",
]
out = {
 "unit": "S7",
 "slice": "L01-L02",
 "round": 33,
 "verifier": "round-33 verifier (independent of the builders and of the round-24 verifier; toolchain re-confirmation of the released S7 L01-L02 slice: diff-scoped but strict, every command row re-run, every numeric row re-derived)",
 "pin": "bcf4e25",
 "base": "5e5da87",
 "previous_ledger": "ledgers/S7/L01-L02.json as it stood in this checkout (round 24, pin a2a631a, 464 rows, all PASS, verified on the old toolchain)",
 "checkout": "/tmp/verify-s7-r1-l12",
 "scratch": "/tmp/ap1-r5/s7-l12",
 "verified_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
 "verdict": verdict,
 "changed_since_base": {
   "course/modules/S/S7/L01.html, L02.html, cards.json, figures-L01.js, figures-L02.js, tests/labs/S7/*": "byte-identical since 5e5da87 (git diff --quiet 5e5da87 HEAD, rc 0)",
   "course/modules/S/S7/project.html": "one line (Python version sentence); outside the slice",
   "notation/notation.json, course/assets/data/notation.json": "+4 AP1 symbols (R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}); none used in the slice",
   "references/references.json": "used_by lists of 4 keys (AP1 added); entry content unchanged for every slice key",
   "course/assets/data/glossary.json": "+9 AP1 entries; no S7 entry changed",
   "course/assets/data/program.json, curriculum/curriculum.json, curriculum/03-markets.yaml, BLUEPRINT.md": "MS-FIN / PHD-FIN hours and closures; the M/FC/E prerequisites of AP1; no S7 module hours or hunks",
   "course/assets/vendor/LOCK.json, SPEC.yaml, tools/vendor_spec.yaml": "KaTeX 0.18.11 -> 0.19.1, Pyodide 0.29.5 -> 314.0.7 (56 LOCK files, hashes verified)",
   "tools/page_smoke.py, tools/build_site.py, tools/data_sources.yaml, tools/vendor.py, tools/katex_strict.js": "page_smoke extended (re-run: PASS for both pages); build_site one-line rename; data_sources notes",
   "tests/test_figure_kernels.py": "tolerance scaled by exponent (re-run: 32 passed)",
   "requirements*.txt, pyproject.toml": "toolchain pins (Python 3.14, numpy 2.4.6, scipy 1.18.0, pytest 9.0.2, ruff 0.17.2, mypy 2.4.0, playwright 1.64.1)",
   "course/assets/css/base.css, components.css, tokens.css; js/lab.js, data.js, theme.js (new); js/rubric.js (changed)": "not loaded by the S7 L01/L02 pages (course.css, print.css, site.js and its module graph are byte-identical); re-checked through page_smoke",
 },
 "line_numbering": "Rows cite the files of the checkout at bcf4e25 (L01.html 824 lines, L02.html 635 lines), which are byte-identical to 5e5da87.",
 "rows": rows_out,
 "mutants": [],
 "registry_flags": prev.get("registry_flags", []) + [
   "T33: references.json at HEAD: 560 entries; live verify_refs --unit S7: 94 of 560 entries, 0 problems (round 33, logs/verify_refs_live.log). The slice's 17 cited keys are content-identical to 5e5da87.",
 ],
 "freshness_flags": prev.get("freshness_flags", []),
 "open_questions": prev.get("open_questions", []),
 "notes": notes,
 "summary": {
   "rows": len(rows_out),
   "pass": len(passes),
   "fail": len(fails),
   "unverifiable": len(unver),
   "carried_unchanged_since_5e5da87": len(carried),
   "rerun_or_rederived_this_round": len(rows_out) - len(carried),
   "new_rows_this_round": len(new_ids),
   "new_row_ids": new_ids,
   "release_row_ids_kept": len(prev_ids),
   "mutants": 0,
   "mutants_killed": 0,
   "fail_ids": fails,
   "unverifiable_ids": unver,
   "verdict_rule": "PASS only if every row is PASS; UNVERIFIABLE counts as a failure.",
 },
}
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("WROTE", OUT, "rows", len(rows_out), "pass", len(passes), "unverifiable", unver, "verdict", verdict, "carried", len(carried), "new", new_ids)
