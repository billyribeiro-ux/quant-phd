#!/usr/bin/env python3
"""Load every page of a unit in Chromium and fail on anything a learner would hit.

Serves ``course/`` locally (WASM runtimes do not load over file://) and, for
each page, in light and dark themes, each at desktop width and at 360 px:

* waits for ``<html data-ready="true">`` (site.js finished)
* zero console errors, page errors, failed requests and site.js step errors
* zero requests to any host but the local server (everything is vendored)
* zero unrendered math (``.katex-error``), and every rendered expression re-parses with KaTeX's
  ``throwOnError: true, strict: "error"`` (an undefined command renders as red text, not as an error)
* no horizontal scrolling at 360 px
* every chart's SVG carries ``<title>`` and ``<desc>``
* every chart's text lies inside its SVG

At both widths in the light theme it then sweeps every live figure: each
control runs through all its values (every range step, select option and
checkbox state; the full product of them when it has at most
``SWEEP_PRODUCT_LIMIT`` states, else one control at a time from the default),
and each button is pressed ``SWEEP_PRESSES`` times, or as many times as the
chart's ``data-sweep-presses`` asks: one count for every button, or a
comma-separated count per button in document order (a figure that draws random
states needs many). In every state no chart text may leave its SVG, overlap
another text, or be crossed by a plotted line, segment, rule, dot or bar, no
plotted segment may lie outside the plot area, and no axis may repeat a tick
label (tools/figure_sweep.js). Geometry does not depend on the theme, so
the dark theme is not swept.

Then, once per page at desktop width: runs every lab in Pyodide and requires
its output to match the page within 10 s of runtime (the runtime is started
first, and every package the page's labs declare or import is loaded before
any lab's timer starts; both times are printed separately, so boot and wheel
loading are not charged to a lab); completion labs are filled with
their solution twin first. On a project page with an autograder, it pastes the
reference solution into the in-browser grader and requires every test to pass
within 60 s: the same suite therefore passes in Pyodide and in local pytest.

Usage::

    python3 tools/page_smoke.py --unit S7
    python3 tools/page_smoke.py --unit S7 --pages L01 project --skip-labs
"""

from __future__ import annotations

import argparse
import ast
import functools
import http.server
import json
import math
import re
import socketserver
import sys
import threading
import time
from pathlib import Path
from typing import Any

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Locator, Page, sync_playwright

from coursekit import COURSE, Lab, Unit, built_units, labs_in, load_page, unit

LAB_LIMIT_S = 10.0
GRADER_LIMIT_S = 60.0
VIEWPORTS = (("desktop", 1280, 900), ("mobile", 360, 760))
SWEEP_PRODUCT_LIMIT = 300
SWEEP_PRESSES = 3


MIME_TYPES = {
    ".mjs": "text/javascript",
    ".js": "text/javascript",
    ".wasm": "application/wasm",
    ".json": "application/json",
    ".woff2": "font/woff2",
}


class _Quiet(http.server.SimpleHTTPRequestHandler):
    """Static file handler with the MIME types module workers and WASM require, and no request log."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # The base class handles the request inside __init__, so the map must be set first.
        self.extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, **MIME_TYPES}
        super().__init__(*args, **kwargs)

    def log_message(self, format: str, *args: object) -> None:
        return


def serve() -> tuple[socketserver.TCPServer, str]:
    handler = functools.partial(_Quiet, directory=str(COURSE))
    server = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
    server.daemon_threads = True
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}"


def load(page: Page, url: str, origin: str) -> list[str]:
    problems: list[str] = []
    page.on("console", lambda m: problems.append(f"console {m.type}: {m.text}") if m.type == "error" else None)
    page.on("pageerror", lambda e: problems.append(f"page error: {e}"))
    page.on("requestfailed", lambda r: problems.append(f"request failed: {r.url}"))
    page.on(
        "response",
        lambda r: problems.append(f"HTTP {r.status}: {r.url}") if r.status >= 400 else None,
    )

    def guard(route):  # type: ignore[no-untyped-def]
        if route.request.url.startswith(origin) or route.request.url.startswith(("data:", "blob:")):
            route.continue_()
        else:
            problems.append(f"external request blocked: {route.request.url}")
            route.abort()

    page.route("**/*", guard)
    page.goto(url)
    page.wait_for_selector("html[data-ready='true']", timeout=90000)
    problems.extend(f"site.js: {e}" for e in page.evaluate("window.__qf.errors"))
    if (n := page.locator(".katex-error").count()) > 0:
        problems.append(f"{n} math expressions failed to render")
    problems.extend(strict_math(page))
    for chart in page.locator("[data-chart]").all():
        if chart.locator("svg > title").count() == 0 or chart.locator("svg > desc").count() == 0:
            problems.append(f"chart {chart.get_attribute('data-chart')} lacks an SVG <title> or <desc>")
    problems.extend(f"chart {name}: text {text!r} leaves its SVG" for name, text in page.evaluate(ESCAPED_TEXT))
    return problems


# Every SVG <text> in a chart must lie inside its SVG (1 px tolerance), except text in a clipped group, which the
# clip hides rather than lets spill.
ESCAPED_TEXT = """() => [...document.querySelectorAll("[data-chart] svg")].flatMap((svg) => {
  const box = svg.getBoundingClientRect();
  return [...svg.querySelectorAll("text")]
    .filter((t) => !t.closest("[clip-path]") && t.textContent.trim())
    .filter((t) => {
      const r = t.getBoundingClientRect();
      return r.left < box.left - 1 || r.right > box.right + 1 || r.top < box.top - 1 || r.bottom > box.bottom + 1;
    })
    .map((t) => [svg.closest("[data-chart]").dataset.chart, t.textContent.trim()]);
})"""


SWEEP_SCRIPT = Path(__file__).with_name("figure_sweep.js")
STRICT_MATH_SCRIPT = Path(__file__).with_name("katex_strict.js")
NOTATION = COURSE / "assets" / "data" / "notation.json"


@functools.cache
def notation_macros() -> dict[str, str]:
    notation = json.loads(NOTATION.read_text(encoding="utf-8"))
    return {name: str(entry["tex"]) for name, entry in notation["macros"].items()}


def strict_math(page: Page) -> list[str]:
    """Re-parse every rendered expression strictly (tools/katex_strict.js); one problem per failing expression."""
    page.evaluate(STRICT_MATH_SCRIPT.read_text(encoding="utf-8"))
    errors = page.evaluate(
        "(macros) => window.__strictMath.strictMathErrors(window.katex, window.__strictMath.renderedMath(document),"
        " macros)",
        notation_macros(),
    )
    return [f"math does not parse strictly: {e['tex']!r}: {e['message']}" for e in errors]


def control_values(control: dict[str, Any]) -> list[Any]:
    if control["kind"] != "range":
        return list(control["values"])
    n = round((control["max"] - control["min"]) / control["step"])
    return [round(control["min"] + i * control["step"], 10) for i in range(n + 1)]


def sweep_figures(page: Page) -> list[str]:
    """Every state of every live figure on the page, checked by figure_sweep.js (see the module docstring)."""
    page.evaluate(SWEEP_SCRIPT.read_text(encoding="utf-8"))
    problems: list[str] = []
    width = page.viewport_size["width"] if page.viewport_size else 0
    for chart in page.locator("[data-chart]").all():
        presses = [int(n) for n in (chart.get_attribute("data-sweep-presses") or str(SWEEP_PRESSES)).split(",")]
        problems += sweep_chart(chart, f"{width} px, chart {chart.get_attribute('data-chart')}", presses)
    return problems


def sweep_chart(chart: Locator, where: str, presses: list[int]) -> list[str]:
    controls = chart.evaluate("(el) => window.__figureSweep.controls(el)")
    settable = [(i, c) for i, c in enumerate(controls) if c["kind"] != "button"]
    grids = [control_values(c) for _, c in settable]
    states: list[list[tuple[int, Any]]] = [[]]
    if math.prod(len(g) for g in grids) <= SWEEP_PRODUCT_LIMIT:
        for (i, _), grid in zip(settable, grids, strict=True):
            states = [[*state, (i, v)] for state in states for v in grid]
    else:
        states = [[(i, v)] for (i, _), grid in zip(settable, grids, strict=True) for v in grid]
    defaults = [(i, c["value"]) for i, c in settable]
    problems: list[str] = []

    def check(label: str) -> None:
        found = chart.evaluate("(el) => window.__figureSweep.collisions(el)")
        problems.extend(f"{where} [{label}]: {p}" for p in found)

    def set_all(assignment: list[tuple[int, Any]]) -> None:
        for i, v in assignment:
            chart.evaluate("(el, [i, v]) => window.__figureSweep.set(el, i, v)", [i, v])

    check("default")
    for state in states:
        set_all(state)
        check(", ".join(f"{controls[i]['label']} = {v}" for i, v in state))
        set_all(defaults)
    buttons = [i for i, c in enumerate(controls) if c["kind"] == "button"]
    for b, i in enumerate(buttons):
        for press in range(1, presses[min(b, len(presses) - 1)] + 1):
            set_all([(i, None)])
            check(f"{controls[i]['label']} pressed {press}x")
    return problems


def lab_preload(labs: list[Lab]) -> tuple[str, list[str]]:
    """The labs' top-level import statements, deduplicated in order, and the union of their data-packages.

    Imports are read from the parsed source, so text inside a string, a parenthesized multi-line import and a
    statement sharing a line with an import are all handled. A ``from __future__`` import is dropped because it
    is legal only at the top of a file. Completion labs are parsed from their twin, since their page code has
    ``___`` blanks. The worker runs the import lines after loadPackagesFromImports, so every wheel a lab needs is
    loaded before any lab's timer starts; importing is side-effect free for the standard library, NumPy and SciPy.
    """
    lines: dict[str, None] = {}
    for lab in labs:
        source = lab.twin.read_text(encoding="utf-8") if lab.completion else lab.code
        try:
            body = ast.parse(source).body
        except SyntaxError as error:
            raise SyntaxError(f"{lab.id}: not valid Python ({error.msg}, line {error.lineno})") from error
        for node in body:
            if isinstance(node, ast.ImportFrom) and node.module == "__future__":
                continue
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                lines.setdefault(ast.unparse(node))
    packages = list(dict.fromkeys(p for lab in labs for p in lab.packages))
    return "\n".join(lines), packages


def run_labs(page: Page, page_path: Path) -> list[str]:
    problems: list[str] = []
    labs = labs_in(load_page(page_path))
    if not labs:
        return problems
    warm = "async () => { const m = await import('/assets/js/python.js'); await m.runPython('pass', ['numpy']); }"
    started = time.perf_counter()
    page.evaluate(warm)  # start Pyodide first, so no lab is charged for the runtime's boot
    print(f"  runtime boot (with numpy): {time.perf_counter() - started:.1f} s")
    try:
        imports, packages = lab_preload(labs)
    except SyntaxError as error:
        return [f"{page_path.name}: lab code cannot be preloaded, {error}"]
    started = time.perf_counter()
    # Load every package the labs declare or import, so no lab's timer includes downloading a wheel.
    try:
        page.evaluate(
            "async ([code, packages]) => { const m = await import('/assets/js/python.js'); "
            "const r = await m.runPython(code, packages); if (r.error) throw new Error(r.error); }",
            [imports, packages],
        )
    except PlaywrightError as error:
        problems.append(f"package preload failed: {error}")
        return problems
    print(f"  package preload ({', '.join(packages) or 'none'}): {time.perf_counter() - started:.1f} s")
    for lab in labs:
        section = page.locator(f"#{lab.id}")
        if lab.completion:
            section.locator("textarea").fill(lab.twin.read_text(encoding="utf-8").rstrip("\n"))
        started = time.perf_counter()
        section.get_by_role("button", name="Run").click()
        page.wait_for_function(
            f"['ok','bad'].some(c => document.querySelector('#{lab.id} .status').classList.contains(c))",
            timeout=180000,
        )
        status = section.locator(".status").inner_text()
        reported = re.search(r"in ([\d.]+) s", status)
        seconds = float(reported.group(1)) if reported else time.perf_counter() - started
        if "matches the expected result" not in status:
            problems.append(f"{lab.id}: {status}")
        if seconds > LAB_LIMIT_S:
            problems.append(f"{lab.id}: ran {seconds:.1f} s in Pyodide (limit {LAB_LIMIT_S:.0f} s)")
        print(f"  lab {lab.id}: {seconds:.1f} s")
    return problems


def run_grader(page: Page, u: Unit) -> list[str]:
    panel = page.locator("section.grader-panel")
    if panel.count() == 0:
        return []
    grader = u.directory / (panel.get_attribute("data-grader") or "grader/")
    page.wait_for_selector("section.grader-panel textarea", timeout=30000)
    panel.locator("textarea").fill((grader / "reference.py").read_text(encoding="utf-8"))
    started = time.perf_counter()
    panel.get_by_role("button", name="Run the autograder").click()
    page.wait_for_function(
        "/tests pass on seed|could not run/.test(document.querySelector('section.grader-panel .status').textContent)",
        timeout=300000,
    )
    elapsed = time.perf_counter() - started
    status = panel.locator(".status").inner_text()
    print(f"  in-browser grader: {status} ({elapsed:.1f} s)")
    problems = [] if status.startswith("All ") else [f"in-browser grader on the reference solution: {status}"]
    if elapsed > GRADER_LIMIT_S:
        problems.append(f"in-browser grader took {elapsed:.1f} s (limit {GRADER_LIMIT_S:.0f} s)")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--unit")
    target.add_argument("--all", action="store_true", help="every built unit plus the site pages")
    parser.add_argument("--pages", nargs="*", help="page names within --unit (index, L01, project); default: all")
    parser.add_argument("--skip-labs", action="store_true", help="render checks only")
    parser.add_argument("--skip-sweep", action="store_true", help="do not sweep the figures' control states")
    args = parser.parse_args()
    units = built_units() if args.all else [unit(args.unit)]
    owner = {p: u for u in units for p in u.pages() if not args.pages or p.stem in args.pages}
    paths = list(owner)
    if not args.pages:
        paths += [COURSE / "index.html", COURSE / "concepts.html", COURSE / "review.html"]
    server, origin = serve()
    failures = 0
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            for path in paths:
                url = f"{origin}/{path.relative_to(COURSE).as_posix()}"
                problems: list[str] = []
                for scheme in ("light", "dark"):
                    for name, width, height in VIEWPORTS:
                        context = browser.new_context(viewport={"width": width, "height": height}, color_scheme=scheme)
                        page = context.new_page()
                        found = load(page, url, origin)
                        if name == "mobile":
                            overflow = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
                            if overflow > 1:
                                found.append(f"horizontal scroll of {overflow} px at {width} px wide")
                        if scheme == "light" and not args.skip_sweep:
                            found += sweep_figures(page)
                        if scheme == "light" and name == "desktop" and not args.skip_labs:
                            found += run_labs(page, path)
                            if path.name == "project.html":
                                found += run_grader(page, owner[path])
                        problems += [f"[{scheme} {name}] {p}" for p in found]
                        context.close()
                for problem in problems:
                    print(f"FAIL {path.relative_to(COURSE)}: {problem}")
                print(f"page_smoke {path.relative_to(COURSE)}: {'PASS' if not problems else 'FAIL'}")
                failures += bool(problems)
            browser.close()
    finally:
        server.shutdown()
    scope = "all" if args.all else args.unit
    print(f"page_smoke {scope}: {'PASS' if not failures else f'FAIL ({failures} pages)'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
