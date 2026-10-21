"""Every inline lab on every built page runs locally and matches its page (tools/run_labs.py)."""

from __future__ import annotations

import contextlib
import io
import itertools
import json
import os
import re
import runpy
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

import coursekit
from coursekit import MARKET_DATA, ROOT, Lab, built_units, labs_in, load_page, snippets_in, twin_workdir
from embed_labs import embed, remark
from run_labs import check_lab, run_twin


def all_labs() -> list[Lab]:
    found: list[Lab] = []
    for u in built_units():
        for path in u.pages():
            page = load_page(path)
            found.extend(labs_in(page) + snippets_in(page))
    return found


@pytest.mark.parametrize("lab", all_labs(), ids=lambda lab: lab.id)
def test_lab_runs_and_matches_its_page(lab: Lab) -> None:
    problems = check_lab(lab)
    assert not problems, "\n".join(problems)


def test_refresh_re_marks_labs_but_keeps_completion_blanks() -> None:
    twins = ROOT / "tests" / "labs" / "S7"
    page = (
        '<section class="lab" id="lab-S7-L01-1" data-runtime="python"><pre><code class="language-python" data-run>'
        'old code</code></pre><pre class="expected" data-tolerance="1e-6">old output</pre></section>'
        '<section class="lab completion" id="lab-S7-project-2" data-runtime="python"><pre><code class="language-python"'
        ' data-run>x = ___</code></pre><pre class="expected" data-tolerance="1e-6">old</pre></section>'
        '<section class="lab" id="lab-S7-nonexistent-9"><pre><code class="language-python" data-run>kept</code></pre>'
        '<pre class="expected">kept</pre></section>'
    )
    out = remark(page, twins)
    assert "@@LAB:lab-S7-L01-1.py@@" in out and "@@OUT:lab-S7-L01-1.py@@" in out
    assert "x = ___" in out and "@@OUT:lab-S7-project-2.py@@" in out, "a completion lab keeps its blanks"
    assert out.count("kept") == 2, "a lab without a twin is left alone"
    assert remark(page, twins, {"lab-S7-project-2"}).count("@@") == 2, "only the listed labs are re-marked"


LISTING = 'from pathlib import Path\n\nprint(sorted(p.name for p in Path("data").iterdir()))\n'
TWINS = ROOT / "tests" / "labs" / "S7"


def data_lab(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, code: str, files: tuple[str, ...]) -> Lab:
    """A lab whose twin is written under tmp_path (coursekit.LAB_TWINS points there)."""
    monkeypatch.setattr(coursekit, "LAB_TWINS", tmp_path)
    (tmp_path / "S7").mkdir(exist_ok=True)
    lab = Lab(tmp_path / "L09.html", "lab-S7-L09-1", "python", code, "", 1e-9, ("numpy",), files=files)
    lab.twin.write_text(code, encoding="utf-8")
    return lab


def test_a_twin_sees_exactly_its_data_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    stdout, stderr, _ = run_twin(data_lab(tmp_path, monkeypatch, LISTING, ("ust_daily.csv", "fx_daily.csv")))
    assert (stdout, stderr) == ("['fx_daily.csv', 'ust_daily.csv']\n", "")
    stdout, stderr, _ = run_twin(data_lab(tmp_path, monkeypatch, LISTING, ()))
    assert (stdout, stderr) == ("[]\n", ""), "a lab that declares no data sees none, as in the browser"


def test_a_twin_reads_the_committed_bytes_and_cannot_alter_them(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    code = (
        "import hashlib\nfrom pathlib import Path\n\n"
        'path = Path("data/fx_monthly.csv")\nprint(hashlib.sha256(path.read_bytes()).hexdigest())\n'
        'path.write_text("overwritten")\n'
    )
    before = (MARKET_DATA / "fx_monthly.csv").read_bytes()
    stdout, stderr, _ = run_twin(data_lab(tmp_path, monkeypatch, code, ("fx_monthly.csv",)))
    manifest = {e["file"]: e for e in json.loads((MARKET_DATA / "MANIFEST.json").read_text())["datasets"]}
    assert (stdout.strip(), stderr) == (manifest["fx_monthly.csv"]["sha256"], "")
    assert (MARKET_DATA / "fx_monthly.csv").read_bytes() == before, "a twin works on a copy"


def test_an_undeclared_data_file_is_reported(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    lab = data_lab(tmp_path, monkeypatch, LISTING, ("ff_factors.csv",))
    assert any("not embedded snapshots" in p for p in check_lab(lab))


# The real-data labs: each twin's first line reports the snapshot it read, as MANIFEST records it.
REAL_DATA_LABS = {
    "lab-S7-L05-6": ("fx_daily.csv",),
    "lab-S7-L08-4": ("fx_monthly.csv",),
    "lab-S7-project-3": ("fx_monthly.csv",),
}


def twin_output(lab_id: str) -> str:
    """The twin's stdout, run as run_labs.py runs it, in a directory whose data/ holds exactly its data-files."""
    with twin_workdir(REAL_DATA_LABS[lab_id]) as work:
        result = subprocess.run(
            [sys.executable, "-I", "-W", "error", str(TWINS / f"{lab_id}.py")],
            capture_output=True,
            text=True,
            check=True,
            cwd=work,
        )
    assert result.stderr == ""
    return result.stdout


def test_l08_lab4_fast_pbo_is_the_definition_at_16_blocks() -> None:
    """Lesson 8's Lab 4 takes its 16-block PBO from pbo_fast(). In the browser it checks pbo_fast() against pbo()
    at 8 and 10 blocks only, to keep the lab fast (pbo() at 16 blocks makes 12,870 passes); here the 16-block
    identity is checked too, on the lab's own trials."""
    here = Path.cwd()
    with twin_workdir(REAL_DATA_LABS["lab-S7-L08-4"]) as work, contextlib.redirect_stdout(io.StringIO()):
        os.chdir(work)
        try:
            lab = runpy.run_path(str(TWINS / "lab-S7-L08-4.py"))
        finally:
            os.chdir(here)
    by_definition = lab["pbo"](lab["trials"], 16)
    assert by_definition == lab["pbo_fast"](lab["trials"], *lab["halves"](16)) == lab["observed_pbo"]


def test_l08_lab4_pbo_counts_ties_and_the_median_rank_as_the_definition_does() -> None:
    """The lab's trials never tie and never put the selected configuration at the median out of sample, so the
    identity above cannot tell a tie's half credit or the logit's non-strict inequality from their mistakes. Here a
    duplicated column ties exactly with the selected one in some splits, and five configurations put the selected
    one at the median rank 3 in others; pbo(), pbo_fast() and a direct count of the definition must agree."""
    here = Path.cwd()
    with twin_workdir(REAL_DATA_LABS["lab-S7-L08-4"]) as work, contextlib.redirect_stdout(io.StringIO()):
        os.chdir(work)
        try:
            lab = runpy.run_path(str(TWINS / "lab-S7-L08-4.py"))
        finally:
            os.chdir(here)
    base = np.random.default_rng(16).normal(0.0, 1.0, (64, 4))
    m = np.column_stack([base[:, 0], base])  # columns 0 and 1 are identical: their Sharpe ratios tie exactly
    n_blocks, n = 16, m.shape[1]
    blocks = np.split(m, n_blocks)
    overfit = ties = medians = splits = 0
    for combo in itertools.combinations(range(n_blocks), n_blocks // 2):
        train = np.vstack([blocks[i] for i in combo])
        test = np.vstack([blocks[i] for i in range(n_blocks) if i not in combo])
        best = int(np.argmax(train.mean(axis=0) / train.std(axis=0, ddof=1)))
        oos = test.mean(axis=0) / test.std(axis=0, ddof=1)
        below, equal = int(np.sum(oos < oos[best])), int(np.sum(oos == oos[best])) - 1
        rank = 1 + below + 0.5 * equal  # tied configurations share the average of their ranks
        overfit += rank <= (n + 1) / 2  # logit(rank / (N + 1)) <= 0
        ties += equal > 0
        medians += rank == (n + 1) / 2
        splits += 1
    assert ties > 0 and medians > 0, "the test matrix must exercise a tie and the median rank"
    by_count = overfit / splits
    assert lab["pbo"](m, n_blocks) == by_count
    assert lab["pbo_fast"](m, *lab["halves"](n_blocks)) == by_count


def test_l08_lab3_pbo_counts_the_median_rank_as_overfit() -> None:
    """Lab 3 runs 2, 20 and 200 configurations, an even count, and draws continuous returns, so no two out-of-sample
    metrics tie and the selected one never sits at the median rank: its logit is never exactly 0. Here three
    configurations over four blocks put the in-sample winner at the middle rank 2 in all six splits: every logit is
    0, which PBO counts as overfit (logit <= 0)."""
    m = np.array(
        [
            [0.35, 0.82, 0.33],
            [-1.3, 0.91, 0.45],
            [-0.54, 0.58, 0.36],
            [0.29, 0.03, 0.55],
            [-0.74, -0.16, -0.48],
            [0.6, 0.04, -0.29],
            [-0.78, -0.26, 0.01],
            [-0.28, 1.29, 1.01],
        ]
    )
    with contextlib.redirect_stdout(io.StringIO()):
        lab = runpy.run_path(str(TWINS / "lab-S7-L08-3.py"))
    assert lab["pbo"](m, 4) == 1.0


@pytest.mark.parametrize("lab_id", sorted(REAL_DATA_LABS))
def test_each_real_data_lab_reports_what_manifest_records(lab_id: str) -> None:
    pages = {lab.id: lab for lab in all_labs()}
    assert pages[lab_id].files == REAL_DATA_LABS[lab_id], "the page's data-files and this test must agree"
    first = twin_output(lab_id).splitlines()[0]
    found = re.match(r"(\S+): (\d+) (?:days|months) from (\S+) to ([^,\s]+)", first)
    assert found, f"{lab_id} must open by reporting its snapshot: {first!r}"
    name, rows, start, end = found.groups()
    entry = {e["file"]: e for e in json.loads((MARKET_DATA / "MANIFEST.json").read_text())["datasets"]}[name]
    assert (int(rows), start, end) == (entry["rows"], entry["first"], entry["last"])


def test_embed_labs_runs_a_twin_with_its_data_files(tmp_path: Path) -> None:
    page = tmp_path / "L09.html"
    page.write_text(
        '<html data-unit="S7"><section class="lab" id="lab-S7-project-3" data-runtime="python" '
        'data-files="fx_monthly.csv"><pre><code class="language-python" data-run>'
        "@@LAB:lab-S7-project-3.py@@</code></pre>"
        '<pre class="expected" data-tolerance="1e-9">@@OUT:lab-S7-project-3.py@@</pre></section></html>'
    )
    assert embed(page) == 2
    expected = load_page(page).dom.first("pre", "expected")
    assert expected is not None and expected.text() == twin_output("lab-S7-project-3").rstrip("\n")
