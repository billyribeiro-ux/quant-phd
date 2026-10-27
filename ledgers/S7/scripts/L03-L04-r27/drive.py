"""Chromium drive of the five L03/L04 figures (round 27, pin 49def2c).

For each page (L03, L04), width (1280, 360 px) and colour scheme (light, dark), and each chart:
  * loads the page fresh from a local static server over course/ (no external hosts allowed),
  * waits for <html data-ready="true">,
  * injects tools/figure_sweep.js (the repo's own sweep helpers),
  * sets EVERY combination of the settable controls over its full range (range: each step; checkbox: both),
  * presses every button 1-4 times with the controls at their defaults,
  * records for every state: the control values read back from the DOM, the .figure-readout text, the svg <desc>,
    the svg <title> and the figcaption text, and any console or page error and any non-local request.
Output: JSON lines in ledgers/S7/scripts/L03-L04-r27/drive_out.json.
Usage: .venv/bin/python ledgers/S7/scripts/L03-L04-r27/drive.py
"""

from __future__ import annotations

import json
import sys
import threading
import functools
import http.server
import socketserver
import itertools
import pathlib

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[4]
COURSE = ROOT / "course"
SWEEP = ROOT / "tools" / "figure_sweep.js"
OUT = pathlib.Path(__file__).with_name("drive_out.json")
PAGES = {"L03": "modules/S/S7/L03.html", "L04": "modules/S/S7/L04.html"}
CHARTS = {"L03": ["bh-geometry", "pvalue-histogram"], "L04": ["bootstrap-blocks", "bootstrap-variance", "rc-vs-spa"]}
WIDTHS = [1280, 360]
SCHEMES = ["light", "dark"]
PRESSES = 4
SHOTS = pathlib.Path("/tmp/ap1-r5/s7-l34/shots")


def serve() -> tuple[socketserver.TCPServer, str]:
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(COURSE))
    handler.log_message = lambda *a, **k: None  # type: ignore[method-assign]
    srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}"


def grid(c: dict) -> list:
    if c["kind"] == "check":
        return [False, True]
    if c["kind"] == "select":
        return list(c["values"])
    if c["kind"] == "range":
        n = round((c["max"] - c["min"]) / c["step"])
        digits = max(0, -int(f"{c['step']:e}".split("e")[1]))
        return [round(c["min"] + i * c["step"], digits + 2) for i in range(n + 1)]
    return []


def main() -> int:
    srv, base = serve()
    results: list[dict] = []
    problems: list[str] = []
    SHOTS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for page_id, rel in PAGES.items():
            for width in WIDTHS:
                for scheme in SCHEMES:
                    ctx = browser.new_context(viewport={"width": width, "height": 900}, color_scheme=scheme)
                    ctx.add_init_script(f"try{{localStorage.setItem('qf-theme','{scheme}')}}catch(e){{}}")
                    for chart_id in CHARTS[page_id]:
                        page = ctx.new_page()
                        errors: list[str] = []
                        hosts: set[str] = set()
                        page.on("console", lambda m, e=errors: e.append(f"console {m.type}: {m.text}") if m.type == "error" else None)
                        page.on("pageerror", lambda x, e=errors: e.append(f"pageerror: {x}"))
                        page.on("request", lambda r, h=hosts: h.add(r.url.split("/")[2]))

                        def load() -> None:
                            page.goto(f"{base}/{rel}", wait_until="load")
                            page.wait_for_selector('html[data-ready="true"]', timeout=90000)
                            page.add_script_tag(path=str(SWEEP))

                        load()
                        el = page.locator(f'[data-chart="{chart_id}"]')
                        el.scroll_into_view_if_needed()
                        ctrl = el.evaluate("(el) => window.__figureSweep.controls(el)")
                        settable = [(i, c) for i, c in enumerate(ctrl) if c["kind"] != "button"]
                        buttons = [i for i, c in enumerate(ctrl) if c["kind"] == "button"]
                        defaults = {i: c["value"] for i, c in settable}

                        def read(tag: str, presses: int) -> dict:
                            state = el.evaluate(
                                """(el) => {
                                  const cs = window.__figureSweep.controls(el);
                                  const fig = el.closest('figure');
                                  return {
                                    controls: cs.map((c) => (c.kind === 'button' ? null : c.value)),
                                    readout: (el.querySelector('.figure-readout') || {}).textContent || null,
                                    desc: (el.querySelector('svg > desc') || {}).textContent || null,
                                    title: (el.querySelector('svg > title') || {}).textContent || null,
                                    caption: fig && fig.querySelector('figcaption') ? fig.querySelector('figcaption').textContent : null,
                                  };
                                }""")
                            state.update({"page": page_id, "chart": chart_id, "width": width, "scheme": scheme, "tag": tag, "presses": presses})
                            return state

                        # every combination of the settable controls across its full range
                        values = [grid(c) for _, c in settable]
                        combos = list(itertools.product(*values))
                        for combo in combos:
                            for (i, _), v in zip(settable, combo):
                                el.evaluate("(el, [i, v]) => window.__figureSweep.set(el, i, v)", [i, v])
                            results.append(read("grid", 0))
                            for (i, _), _v in zip(settable, combo):
                                el.evaluate("(el, [i, v]) => window.__figureSweep.set(el, i, v)", [i, defaults[i]])
                        # button presses with the controls at their defaults
                        if width == 1280 and scheme == "light" or width == 360 and scheme == "dark":
                            pass
                        for b in buttons:
                            load()
                            el = page.locator(f'[data-chart="{chart_id}"]')
                            results.append(read("press", 0))
                            for n in range(1, PRESSES + 1):
                                el.evaluate("(el, i) => window.__figureSweep.set(el, i, null)", b)
                                results.append(read("press", n))
                        # screenshots of the default state, for the two configurations the review uses
                        if (width, scheme) in [(1280, "light"), (360, "dark")]:
                            load()
                            el = page.locator(f'[data-chart="{chart_id}"]')
                            el.screenshot(path=str(SHOTS / f"{page_id}-{chart_id}-{width}-{scheme}.png"))
                        if errors:
                            problems.append(f"{page_id} {chart_id} {width} {scheme}: {errors[:3]}")
                        external = {h for h in hosts if not h.startswith("127.0.0.1")}
                        if external:
                            problems.append(f"{page_id} {chart_id} {width} {scheme}: external hosts {sorted(external)}")
                        page.close()
                    ctx.close()
        browser.close()
    srv.shutdown()
    OUT.write_text(json.dumps({"states": results, "problems": problems}, ensure_ascii=False), encoding="utf-8")
    print(f"states {len(results)}")
    print(f"problems {len(problems)}")
    for p in problems[:10]:
        print(p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
