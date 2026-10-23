"""Tests for tools/run_labs.py: extraction from HTML and the shared comparison rule."""

from __future__ import annotations

from pathlib import Path

import pytest

from run_labs import extract, outputs_match, run

ROOT = Path(__file__).resolve().parent.parent

PAGE = """<!doctype html><html><body>
<section class="lab" data-runtime="python" id="lab-x">
  <div class="lab-head"><h3>Lab</h3><div class="lab-actions"></div></div>
  <pre><code class="language-python" data-run>x = 1 &lt; 2
print("ok", x, 0.1 + 0.2)</code></pre>
  <pre class="expected" data-tolerance="1e-12">ok True 0.3</pre>
</section>
<section class="lab" data-runtime="sql" id="lab-sql"><pre><code data-run>select 1</code></pre></section>
</body></html>"""


def test_extract_reads_python_labs_and_unescapes_entities(tmp_path: Path) -> None:
    page = tmp_path / "p.html"
    page.write_text(PAGE, encoding="utf-8")
    labs = extract(page)
    assert [lab.lab_id for lab in labs] == ["lab-x"]
    assert labs[0].code.startswith("x = 1 < 2")
    assert labs[0].expected == "ok True 0.3"
    assert labs[0].tolerance == pytest.approx(1e-12)
    ok, detail = run(labs[0])
    assert ok, detail


@pytest.mark.parametrize(
    ("actual", "expected", "tol", "ok"),
    [
        ("gap 7.1e-15", "gap 0.0e+00", 1e-9, True),
        ("gap 1e-6", "gap 0", 1e-9, False),
        ("call 4.178300", "call 4.178300", 0.0, True),
        ("call 4.178300", "put 4.178300", 1.0, False),
        ("a b", "a b c", 1.0, False),
    ],
)
def test_outputs_match(actual: str, expected: str, tol: float, ok: bool) -> None:
    assert outputs_match(actual, expected, tol) is ok


def test_design_system_lab_passes() -> None:
    labs = extract(ROOT / "course" / "dev" / "design-system.html")
    assert labs, "design-system page must contain a Python lab"
    for lab in labs:
        ok, detail = run(lab)
        assert ok, detail
