#!/usr/bin/env python3
"""Browser smoke test for the static site (Playwright + Chromium).

Serves ``course/`` from a local HTTP server and opens every registered page in
light and dark themes at desktop and phone widths. A page fails if:

* anything is logged with ``console.error`` or an uncaught exception occurs
  (refs.js and math.js report unknown citation keys and KaTeX errors this way);
* it requests anything outside the local server (the site must work offline);
* any local request fails;
* the page scrolls horizontally at phone width;
* its page-specific checks fail (rendered module count, math, citations, and
  running an in-page Python lab to the expected output).

Screenshots are written to ``.cache/screens/`` for review.

Usage::

    python3 tools/build_site.py && python3 tools/page_smoke.py
"""

from __future__ import annotations

import functools
import http.server
import json
import os
import sys
import threading
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from playwright.sync_api import Browser, BrowserContext, ConsoleMessage, Error, Page, Request, Route, sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "course"
SCREENS = ROOT / ".cache" / "screens"
VIEWPORTS = {"desktop": (1280, 900), "phone": (375, 812)}
THEMES: tuple[Literal["light", "dark"], ...] = ("light", "dark")


_MIME = {
    ".mjs": "text/javascript",
    ".js": "text/javascript",
    ".wasm": "application/wasm",
    ".json": "application/json",
    ".woff2": "font/woff2",
}


class _Handler(http.server.SimpleHTTPRequestHandler):
    def guess_type(self, path: str | os.PathLike[str]) -> str:
        return _MIME.get(Path(path).suffix) or super().guess_type(path)

    def log_message(self, format: str, *args: object) -> None:
        return


@contextmanager
def serve(directory: Path) -> Iterator[str]:
    handler = functools.partial(_Handler, directory=str(directory))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        server.server_close()


@dataclass
class Result:
    page: str
    variant: str
    problems: list[str] = field(default_factory=list)


def check_program_map(page: Page, problems: list[str]) -> None:
    page.wait_for_selector("html[data-map-ready='true']", timeout=20_000)
    curriculum = json.loads((ROOT / "curriculum" / "curriculum.json").read_text(encoding="utf-8"))
    expected = curriculum["stats"]["modules"]
    rendered = page.locator(".module").count()
    if rendered != expected:
        problems.append(f"rendered {rendered} modules, curriculum has {expected}")
    if page.locator(".card").count() != len(curriculum["credentials"]):
        problems.append("credential cards do not match curriculum credentials")
    page.fill("#filter-search", "black-scholes")
    visible = page.locator(".module:not([hidden])").count()
    if not 0 < visible < expected:
        problems.append(f"search filter showed {visible} modules for 'black-scholes'")
    page.fill("#filter-search", "")


def check_design_system(page: Page, problems: list[str], run_lab: bool) -> None:
    page.wait_for_selector(".cite", timeout=20_000)
    if page.locator(".katex").count() == 0:
        problems.append("no KaTeX output rendered")
    if page.locator(".katex-error, .cite-missing").count():
        problems.append("math error or unverified citation marker present")
    if page.locator("[data-references] li").count() == 0:
        problems.append("reference list is empty")
    if run_lab:
        page.click("#lab-ds-1 .lab-actions button")
        page.wait_for_selector(
            "#lab-ds-1 .lab-status[data-state='pass'], #lab-ds-1 .lab-status[data-state='fail']", timeout=180_000
        )
        state = page.get_attribute("#lab-ds-1 .lab-status", "data-state")
        if state != "pass":
            problems.append(f"lab did not match expected output: {page.inner_text('#lab-ds-1 .lab-output')!r}")


PAGES: dict[str, Callable[[Page, list[str], bool], None]] = {
    "index.html": lambda page, problems, _first: check_program_map(page, problems),
    "dev/design-system.html": check_design_system,
}


def monitor(context: BrowserContext, page: Page, base_url: str, problems: list[str]) -> None:
    """Record console errors, uncaught exceptions, failed local requests and any external request."""

    def on_route(route: Route) -> None:
        if route.request.url.startswith(base_url):
            route.continue_()
        else:
            problems.append(f"external request blocked: {route.request.url}")
            route.abort()

    def on_console(message: ConsoleMessage) -> None:
        if message.type == "error":
            problems.append(f"console.error: {message.text}")

    def on_page_error(error: Error) -> None:
        problems.append(f"uncaught: {error}")

    def on_request_failed(request: Request) -> None:
        if request.url.startswith(base_url):
            problems.append(f"request failed: {request.url}")

    context.route("**/*", on_route)
    page.on("console", on_console)
    page.on("pageerror", on_page_error)
    page.on("requestfailed", on_request_failed)


def check_variant(
    browser: Browser, base_url: str, path: str, theme: Literal["light", "dark"], viewport: str, first: bool
) -> Result:
    result = Result(path, f"{theme}/{viewport}")
    width, height = VIEWPORTS[viewport]
    context = browser.new_context(
        viewport={"width": width, "height": height}, color_scheme=theme, service_workers="block"
    )
    page = context.new_page()
    monitor(context, page, base_url, result.problems)
    page.goto(f"{base_url}/{path}", wait_until="networkidle")
    PAGES[path](page, result.problems, first)
    overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    if overflow > 0:
        result.problems.append(f"horizontal page scroll of {overflow}px")
    name = path.replace("/", "_").removesuffix(".html")
    page.evaluate("window.scrollTo(0, 0)")
    page.screenshot(path=str(SCREENS / f"{name}-{theme}-{viewport}.png"), full_page=False)
    context.close()
    return result


def smoke(base_url: str) -> list[Result]:
    SCREENS.mkdir(parents=True, exist_ok=True)
    results: list[Result] = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for path in PAGES:
            first = True
            for theme in THEMES:
                for viewport in VIEWPORTS:
                    results.append(check_variant(browser, base_url, path, theme, viewport, first))
                    first = False
        browser.close()
    return results


def main() -> int:
    if not (SITE / "assets" / "data" / "curriculum.json").exists():
        print("site data missing: run `python3 tools/build_site.py` first", file=sys.stderr)
        return 1
    with serve(SITE) as base_url:
        results = smoke(base_url)
    failed = 0
    for result in results:
        status = "PASS" if not result.problems else "FAIL"
        print(f"{status} {result.page} [{result.variant}]")
        for problem in result.problems:
            print(f"     - {problem}")
        failed += bool(result.problems)
    print(f"page smoke: {len(results) - failed}/{len(results)} passed; screenshots in {SCREENS.relative_to(ROOT)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
