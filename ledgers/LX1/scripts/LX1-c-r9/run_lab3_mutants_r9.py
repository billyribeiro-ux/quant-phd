"""Round-9 fixer check: every LX1 project lab-3 mutant against (a) the page's expected block on the embedded
snapshot and (b) the three damaged snapshots of tests/test_lx1_project_lab3.py (blank GBP cell, non-decimal GBP
cell, removed month). A mutant is KILLED if any check differs from the expected behaviour."""

import csv
import glob
import html
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

WORKDIR = pathlib.Path("/Users/billyribeiro/dev/quant-phd")
PAGE = (WORKDIR / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")
SNAPSHOT = WORKDIR / "course/assets/data/market/fx_monthly.csv"
PY = str(WORKDIR / ".venv/bin/python")


def expected_block() -> tuple[str, float]:
    sec = re.search(r'<section class="lab[^"]*" id="lab-LX1-project-3".*?</section>', PAGE, re.S).group(0)
    body = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1)
    tol = float(re.search(r'<pre class="expected"[^>]*data-tolerance="([^"]+)"', sec).group(1))
    return html.unescape(body), tol


def is_num(t: str) -> bool:
    try:
        float(t)
        return True
    except ValueError:
        return False


def same(actual: str, expected: str, tol: float) -> bool:
    a, e = actual.split(), expected.split()
    if len(a) != len(e):
        return False
    for x, y in zip(a, e):
        if is_num(x) and is_num(y):
            if abs(float(x) - float(y)) > tol * (1 + abs(float(y))):
                return False
        elif x != y:
            return False
    return True


def run(script: str, data_rows: list[list[str]] | None, header: list[str]) -> subprocess.CompletedProcess[str]:
    wd = tempfile.mkdtemp(prefix="lx1c-r9-lab3-")
    try:
        os.makedirs(f"{wd}/data")
        target = f"{wd}/data/fx_monthly.csv"
        if data_rows is None:
            shutil.copy(SNAPSHOT, target)
        else:
            with open(target, "w", encoding="utf-8", newline="") as handle:
                writer = csv.writer(handle, lineterminator="\n")
                writer.writerow(header)
                writer.writerows(data_rows)
        with open(f"{wd}/lab.py", "w", encoding="utf-8") as handle:
            handle.write(open(script, encoding="utf-8").read())
        return subprocess.run(
            [PY, "-I", "-W", "error", f"{wd}/lab.py"],
            cwd=wd,
            capture_output=True,
            text=True,
            env={"PATH": "/usr/bin:/bin"},
        )
    finally:
        shutil.rmtree(wd)


def snapshot() -> tuple[list[str], list[list[str]]]:
    with SNAPSHOT.open(encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        return header, list(reader)


def damaged(header: list[str], rows: list[list[str]], kind: str) -> list[list[str]]:
    out = [list(r) for r in rows]
    if kind == "blank":
        index = header.index("GBP")
        for r in out:
            if r[0] == "2000-06":
                r[index] = ""
        return out
    if kind == "non_decimal":
        index = header.index("GBP")
        for r in out:
            if r[0] == "2000-06":
                r[index] = "n/a"
        return out
    return [r for r in out if r[0] != "1990-06"]  # gap


EXPECTED_MSG = {
    "blank": "ValueError: 2000-06: GBP cell '' is blank or not a decimal number",
    "non_decimal": "ValueError: 2000-06: GBP cell 'n/a' is blank or not a decimal number",
    "gap": "ValueError: month 1990-07 does not follow 1990-05",
}


def judge_damaged(script: str, kind: str) -> tuple[bool, str]:
    header, rows = snapshot()
    done = run(script, damaged(header, rows, kind), header)
    ok = done.returncode != 0 and done.stdout == "" and EXPECTED_MSG[kind] in done.stderr
    tail = done.stderr.strip().splitlines()[-1] if done.stderr.strip() else f"rc={done.returncode}"
    return (not ok), tail


if __name__ == "__main__":
    expected, tol = expected_block()
    names = sorted(glob.glob(str(WORKDIR / "ledgers/LX1/mutants/*.py")))
    for path in names:
        base = os.path.basename(path)
        text = open(path, encoding="utf-8").read()
        if "project lab 3" not in text:
            continue
        embedded = run(path, None, [])
        emb_killed = embedded.returncode != 0 or not same(embedded.stdout, expected, tol)
        damage = {k: judge_damaged(path, k) for k in ("blank", "non_decimal", "gap")}
        dmg_killed = [k for k, (killed, _) in damage.items() if killed]
        status = "KILLED" if (emb_killed or dmg_killed) else "SURVIVED"
        print(f"{status} | {base} | embedded={'differs' if emb_killed else 'matches'} | damaged_killed={dmg_killed}")
