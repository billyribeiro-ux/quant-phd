"""Tests for lab extraction (coursekit.labs_in) and the shared output-comparison rule."""

from __future__ import annotations

from pathlib import Path

import pytest

from coursekit import compare_output, labs_in, load_page

PAGE = """<!doctype html><html><body>
<section class="lab" data-runtime="python" id="lab-X-L01-1">
  <div class="lab-head"><h3>Lab</h3><div class="lab-actions"></div></div>
  <pre><code class="language-python" data-run>x = 1 &lt; 2
print("ok", x, 0.1 + 0.2)</code></pre>
  <pre class="expected" data-tolerance="1e-12">ok True 0.3</pre>
</section>
<section class="lab" data-runtime="sql" id="lab-X-L01-2"><pre><code data-run>select 1</code></pre></section>
</body></html>"""


def test_labs_in_reads_labs_and_unescapes_entities(tmp_path: Path) -> None:
    page = tmp_path / "p.html"
    page.write_text(PAGE, encoding="utf-8")
    labs = labs_in(load_page(page))
    assert [(lab.id, lab.runtime) for lab in labs] == [("lab-X-L01-1", "python"), ("lab-X-L01-2", "sql")]
    assert labs[0].code.startswith("x = 1 < 2")
    assert labs[0].expected == "ok True 0.3"
    assert labs[0].tolerance == pytest.approx(1e-12)
    assert labs[1].expected is None


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
def test_compare_output(actual: str, expected: str, tol: float, ok: bool) -> None:
    assert compare_output(actual, expected, tol)[0] is ok
