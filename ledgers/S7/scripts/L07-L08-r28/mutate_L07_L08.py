"""Round 28 re-kill of the 13 verifier mutants for S7 L07-L08, applied to a scratch copy of the checkout.

Each mutant edits the input named in its row (twin and page code together where the row says so), runs the test
node or check that killed it, and restores the pristine files. The checkout itself is never edited.
Usage: .venv/bin/python -I mutate_L07_L08.py <pristine checkout> <scratch copy> <out json>
"""

from __future__ import annotations

import html
import json
import shutil
import subprocess
import sys
from pathlib import Path

SRC, COPY, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
PY = str(SRC / ".venv/bin/python")
PYTEST = str(SRC / ".venv/bin/pytest")
TWIN = {n: Path("tests/labs/S7") / f"lab-S7-L{n}.py" for n in ("L07-1", "L07-2", "L07-3", "L07-4", "L08-1", "L08-2", "L08-3", "L08-4")}
PAGE = {"L07": Path("course/modules/S/S7/L07.html"), "L08": Path("course/modules/S/S7/L08.html")}
FIG = {"L07": Path("course/modules/S/S7/figures-L07.js"), "L08": Path("course/modules/S/S7/figures-L08.js")}


def section(text: str, lab_id: str) -> tuple[int, int]:
    start = text.index(f'<section class="lab" id="{lab_id}"')
    return start, text.index("</section>", start)


def replace_in(path: Path, old: str, new: str, count: int = 1, within: str | None = None) -> None:
    if path.suffix == ".html":  # the page stores code HTML-escaped (&lt; &gt; &amp;)
        old, new = html.escape(old, quote=False), html.escape(new, quote=False)
    text = path.read_text(encoding="utf-8")
    if within is None:
        assert text.count(old) == count, (path, old, text.count(old))
        text = text.replace(old, new)
    else:
        a, b = section(text, within)
        block = text[a:b]
        assert block.count(old) == count, (path, within, old, block.count(old))
        text = text[:a] + block.replace(old, new) + text[b:]
    path.write_text(text, encoding="utf-8")


def twin_and_page(old: str, new: str, lab: str, count_twin: int = 1, count_page: int = 1) -> list:
    page = PAGE[lab[:3]]
    return [
        (TWIN[lab[4:]] if False else Path("tests/labs/S7") / f"lab-S7-{lab}.py", old, new, count_twin, None),
        (page, old, new, count_page, f"lab-S7-{lab}"),
    ]


MUTANTS = [
    {
        "id": "MU01",
        "desc": "L08 Lab 4 null resamples whole months without replacement (rng.permutation) instead of with replacement; twin and page code changed together",
        "edits": [
            (Path("tests/labs/S7/lab-S7-L08-4.py"), "draw = changes[rng.integers(0, len(changes), size=len(changes))]", "draw = changes[rng.permutation(len(changes))]", 1, None),
            (PAGE["L08"], "draw = changes[rng.integers(0, len(changes), size=len(changes))]", "draw = changes[rng.permutation(len(changes))]", 1, None),
        ],
        "check": ["-m", "pytest", "-p", "no:cacheprovider", "tests/test_labs.py::test_lab_runs_and_matches_its_page[lab-S7-L08-4]"],
    },
    {
        "id": "MU02",
        "desc": "L08 Lab 4 null seed 4008 changed to 4009; twin and page code changed together",
        "edits": [
            (Path("tests/labs/S7/lab-S7-L08-4.py"), "default_rng(4008)", "default_rng(4009)", 1, None),
            (PAGE["L08"], "default_rng(4008)", "default_rng(4009)", 1, None),
        ],
        "check": ["-m", "pytest", "-p", "no:cacheprovider", "tests/test_labs.py::test_lab_runs_and_matches_its_page[lab-S7-L08-4]"],
    },
    {
        "id": "MU03",
        "desc": "L07 Lab 1 normal formula loses the 1/2 in SR^2/2; twin and page code changed together",
        "edits": [
            (Path("tests/labs/S7/lab-S7-L07-1.py"), "normal = 1.0 + sr**2 / 2.0", "normal = 1.0 + sr**2", 1, None),
            (PAGE["L07"], "normal = 1.0 + sr**2 / 2.0", "normal = 1.0 + sr**2", 1, "lab-S7-L07-1"),
        ],
        "check": ["-m", "pytest", "-p", "no:cacheprovider", "tests/test_labs.py::test_lab_runs_and_matches_its_page[lab-S7-L07-1]"],
    },
    {
        "id": "MU04",
        "desc": "L08 Lab 3 trial list (2, 20, 200) changed to (2, 20, 199); twin and page code changed together",
        "edits": [
            (Path("tests/labs/S7/lab-S7-L08-3.py"), "for n_trials in (2, 20, 200):", "for n_trials in (2, 20, 199):", 1, None),
            (PAGE["L08"], "for n_trials in (2, 20, 200):", "for n_trials in (2, 20, 199):", 1, "lab-S7-L08-3"),
        ],
        "check": ["-m", "pytest", "-p", "no:cacheprovider", "tests/test_labs.py::test_lab_runs_and_matches_its_page[lab-S7-L08-3]"],
    },
    {
        "id": "MU05",
        "desc": "L08 Lab 3 rank counts the winner itself as below the winner (oos <= oos[best]); the twin then exits non-zero (rank above N + 1)",
        "edits": [
            (Path("tests/labs/S7/lab-S7-L08-3.py"), "np.sum(oos < oos[best])", "np.sum(oos <= oos[best])", 1, None),
            (PAGE["L08"], "np.sum(oos < oos[best])", "np.sum(oos <= oos[best])", 1, "lab-S7-L08-3"),
        ],
        "check": ["-m", "pytest", "-p", "no:cacheprovider", "tests/test_labs.py::test_lab_runs_and_matches_its_page[lab-S7-L08-3]"],
    },
    {
        "id": "MU06",
        "desc": "L08 Lab 3 PBO convention logit <= 0 changed to logit < 0 (twin only; the lab output is unchanged for even trial counts)",
        "edits": [
            (Path("tests/labs/S7/lab-S7-L08-3.py"), "np.array(logits) <= 0", "np.array(logits) < 0", 1, None),
        ],
        "check": ["-m", "pytest", "-p", "no:cacheprovider", "tests/test_labs.py::test_l08_lab3_pbo_counts_the_median_rank_as_overfit"],
    },
    {
        "id": "MU07",
        "desc": "L07 Lab 4 seed 4707 changed to 4708; twin and page code changed together",
        "edits": [
            (Path("tests/labs/S7/lab-S7-L07-4.py"), "default_rng(4707)", "default_rng(4708)", 1, None),
            (PAGE["L07"], "default_rng(4707)", "default_rng(4708)", 1, "lab-S7-L07-4"),
        ],
        "check": ["-m", "pytest", "-p", "no:cacheprovider", "tests/test_labs.py::test_lab_runs_and_matches_its_page[lab-S7-L07-4]"],
    },
    {
        "id": "MU08",
        "desc": "L07 Lab 4 Part 3: kurtosis term (m4/m2^2 - 1)/4 * s^2 replaced by s^2; twin and page code changed together",
        "edits": [
            (Path("tests/labs/S7/lab-S7-L07-4.py"), "(m4 / m2**2 - 1.0) / 4.0 * s**2", "s**2", 1, None),
            (PAGE["L07"], "(m4 / m2**2 - 1.0) / 4.0 * s**2", "s**2", 1, "lab-S7-L07-4"),
        ],
        "check": ["-m", "pytest", "-p", "no:cacheprovider", "tests/test_labs.py::test_lab_runs_and_matches_its_page[lab-S7-L07-4]"],
    },
    {
        "id": "MU09",
        "desc": "L07 Lab 4 Part 2: the naive statistic drops the common term; twin and page code changed together",
        "edits": [
            (Path("tests/labs/S7/lab-S7-L07-4.py"), "naive = 2.0 + common", "naive = 2.0", 1, None),
            (PAGE["L07"], "naive = 2.0 + common", "naive = 2.0", 1, "lab-S7-L07-4"),
        ],
        "check": ["-m", "pytest", "-p", "no:cacheprovider", "tests/test_labs.py::test_lab_runs_and_matches_its_page[lab-S7-L07-4]"],
    },
    {
        "id": "MU10",
        "desc": "L07 Lab 4 Part 3: skewness sign flipped in the standard error; twin and page code changed together",
        "edits": [
            (Path("tests/labs/S7/lab-S7-L07-4.py"), "(1.0 - m3 / m2**1.5 * s", "(1.0 + m3 / m2**1.5 * s", 1, None),
            (PAGE["L07"], "(1.0 - m3 / m2**1.5 * s", "(1.0 + m3 / m2**1.5 * s", 1, "lab-S7-L07-4"),
        ],
        "check": ["-m", "pytest", "-p", "no:cacheprovider", "tests/test_labs.py::test_lab_runs_and_matches_its_page[lab-S7-L07-4]"],
    },
    {
        "id": "MU11",
        "desc": "figures-L08.js readout writes omega as rank/N instead of rank/(N+1) (the readout text changes; the value does not)",
        "edits": [
            (FIG["L08"], "ω = ${split.rank}/${N + 1} = ${split.omega.toFixed(3)}", "ω = ${split.rank}/${N} = ${(split.rank / N).toFixed(3)}", 1, None),
        ],
        "check": ["figure"],
    },
    {
        "id": "MU12",
        "desc": "figures-L07.js standard error without the kurtosis term ((kurt-1)/4 sr^2 removed from sharpeStdError)",
        "edits": [
            (FIG["L07"], "return Math.sqrt((1 - skew * sr + ((kurt - 1) / 4) * sr * sr) / (T - 1));", "return Math.sqrt((1 - skew * sr) / (T - 1));", 1, None),
        ],
        "check": ["figure"],
    },
    {
        "id": "MU13",
        "desc": "L07.html line 440 with the superseded paired variance 0.10043 in the square root (the round-24 defect the round-25 FAIL recorded)",
        "edits": [
            (PAGE["L07"], "\\sqrt{0.100434/1259} = 0.008932", "\\sqrt{0.10043/1259} = 0.008932", 1, None),
        ],
        "check": ["arithmetic"],
    },
]


def restore(rel: Path) -> None:
    shutil.copyfile(SRC / rel, COPY / rel)


def run_check(mut: dict) -> dict:
    if mut["check"] == ["arithmetic"]:
        import math

        printed = round(math.sqrt(0.10043 / 1259), 6)
        return {"killed": printed != 0.008932, "evidence": f"sqrt(0.10043/1259) = {math.sqrt(0.10043 / 1259):.8f}, printed to 6 dp {printed:.6f}; the page prints 0.008932"}
    if mut["check"] == ["figure"]:
        base = "http://127.0.0.1:8766/modules/S/S7/"
        env = {"DRIVE_BASE": base, "DRIVE_ONLY_LIGHT_1280": "1", "PATH": "/usr/bin:/bin"}
        out = OUT.parent / f"fig-{mut['id']}"
        proc = subprocess.run([PY, "-I", str(SRC / "ledgers/S7/scripts/L07-L08-r28/drive_figs.py"), str(SRC), str(out)], cwd=COPY, env=env, capture_output=True, text=True, timeout=1500)
        summary = json.loads((out / "summary.json").read_text(encoding="utf-8")) if (out / "summary.json").exists() else {}
        mism = {k: v.get("n_mismatch") for k, v in summary.items()}
        killed = any((v or 0) > 0 for v in mism.values())
        return {"killed": killed, "evidence": f"drive_figs.py on the mutated copy (light, 1280 px, served on :8766): mismatches per figure {mism}; exit {proc.returncode}"}
    proc = subprocess.run([PY] + mut["check"] if mut["check"][0] != "-m" else [PYTEST] + mut["check"][2:], cwd=COPY, capture_output=True, text=True, timeout=900)
    tail = (proc.stdout + proc.stderr).strip().splitlines()[-3:]
    return {"killed": proc.returncode != 0, "evidence": f"exit {proc.returncode}: " + " | ".join(tail)}


def main() -> None:
    results = []
    for mut in MUTANTS:
        touched = []
        for rel, old, new, count, within in mut["edits"]:
            if rel not in touched:
                touched.append(rel)
        for rel in touched:
            restore(rel)
        try:
            for rel, old, new, count, within in mut["edits"]:
                if mut["check"] == ["arithmetic"]:
                    continue
                replace_in(COPY / rel, old, new, count, within)
            res = run_check(mut)
        finally:
            for rel in touched:
                restore(rel)
        results.append({"id": mut["id"], "desc": mut["desc"], **res})
        print(mut["id"], "killed" if res["killed"] else "SURVIVED", "|", res["evidence"][:220])
    OUT.write_text(json.dumps(results, indent=1, ensure_ascii=False), encoding="utf-8")
    print("killed", sum(1 for r in results if r["killed"]), "of", len(results))


if __name__ == "__main__":
    main()
