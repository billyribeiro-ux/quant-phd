"""The figure contract in tools/check_pages.py catches each way a figure can be wired wrong."""

from __future__ import annotations

from pathlib import Path

import pytest

from check_pages import check_code, check_figures
from coursekit import load_page

D3 = '<script defer src="../../../assets/vendor/d3/d3.min.js"></script>'
FIGURE = (
    '<figure><div class="chart" data-chart="bh-geometry"></div>'
    '<figcaption>The one thing to see. <span class="source">Computed live.</span></figcaption></figure>'
)
MODULE = 'const FIGURES = { "bh-geometry": bhGeometry };\nexport function drawFigures() {}\n'


def problems_for(tmp_path: Path, *, html_attrs: str, head: str, body: str, module: str | None) -> list[str]:
    page = tmp_path / "L03.html"
    page.write_text(
        f'<!doctype html><html lang="en" {html_attrs}><head>{head}</head><body><main>{body}</main></body></html>'
    )
    if module is not None:
        (tmp_path / "figures-L03.js").write_text(module)
    found: list[str] = []
    check_figures(load_page(page), found)
    return found


def test_a_correctly_wired_figure_passes(tmp_path: Path) -> None:
    attrs = 'data-figures="figures-L03.js"'
    assert problems_for(tmp_path, html_attrs=attrs, head=D3, body=FIGURE, module=MODULE) == []


@pytest.mark.parametrize(
    ("attrs", "head", "body", "module", "expected"),
    [
        pytest.param("", D3, FIGURE, MODULE, "need <html data-figures>", id="no-module-declared"),
        pytest.param('data-figures="figures-L03.js"', D3, FIGURE, None, "does not exist", id="module-missing"),
        pytest.param(
            'data-figures="figures-L03.js"', D3, FIGURE, "const FIGURES = {};\n", "is not defined", id="chart-undefined"
        ),
        pytest.param('data-figures="figures-L03.js"', "", FIGURE, MODULE, "must load", id="no-d3"),
        pytest.param(
            'data-figures="figures-L03.js"',
            D3,
            FIGURE.replace('<span class="source">Computed live.</span>', ""),
            MODULE,
            "span.source",
            id="no-source-line",
        ),
        pytest.param(
            'data-figures="figures-L03.js"',
            D3,
            '<div class="chart" data-chart="bh-geometry"></div>',
            MODULE,
            "<figcaption>",
            id="not-in-a-figure",
        ),
    ],
)
def test_each_wiring_fault_is_reported(
    tmp_path: Path, attrs: str, head: str, body: str, module: str | None, expected: str
) -> None:
    found = problems_for(tmp_path, html_attrs=attrs, head=head, body=body, module=module)
    assert any(expected in p for p in found), found


def test_pages_without_figures_need_nothing(tmp_path: Path) -> None:
    assert problems_for(tmp_path, html_attrs="", head="", body="<p>No charts.</p>", module=None) == []


@pytest.mark.parametrize(
    ("body", "ok"),
    [
        pytest.param('<pre><code class="language-python" data-run>print(1)</code></pre>', True, id="lab-code"),
        pytest.param(
            '<pre><code class="language-python" data-check="sol-S7-L06-E3">print(1)</code></pre>'
            '<pre class="expected" data-check="sol-S7-L06-E3">1</pre>',
            True,
            id="checked-snippet",
        ),
        pytest.param('<pre><code class="language-pseudocode">for each split</code></pre>', True, id="pseudocode"),
        pytest.param('<pre><code class="language-python">print(1)</code></pre>', False, id="unchecked-python"),
        pytest.param(
            '<pre><code class="language-python" data-check="sol-S7-L06-E3">print(1)</code></pre>', False, id="no-output"
        ),
    ],
)
def test_python_on_a_page_must_have_run(tmp_path: Path, body: str, ok: bool) -> None:
    page = tmp_path / "L06.html"
    page.write_text(f'<!doctype html><html lang="en"><head></head><body><main>{body}</main></body></html>')
    found: list[str] = []
    check_code(load_page(page), found)
    assert (found == []) is ok, found
