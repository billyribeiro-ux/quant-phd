"""Every inline lab on every built page runs locally and matches its page (tools/run_labs.py)."""

from __future__ import annotations

import pytest

from coursekit import ROOT, Lab, built_units, labs_in, load_page, snippets_in
from embed_labs import remark
from run_labs import check_lab


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
