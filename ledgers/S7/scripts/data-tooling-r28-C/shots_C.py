"""Round-28 part C: element screenshots of two S7 figures (pvalue-histogram on L03, cscv-explorer on L08) in light and
dark, at 360 and 1280 px, from the checkout's own course/ tree served on an ephemeral local port.
Output: <out>/<figure>-<width>-<theme>.png and log.json (console/page errors per shot).
Run: python -I shots_C.py <checkout> <out_dir>"""
import http.server
import json
import os
import socketserver
import sys
import threading

from playwright.sync_api import sync_playwright

ROOT, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)


def handler(*a, **k):
    return http.server.SimpleHTTPRequestHandler(*a, directory=os.path.join(ROOT, "course"), **k)


socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
port = httpd.server_address[1]
threading.Thread(target=httpd.serve_forever, daemon=True).start()
jobs = [("L03", "pvalue-histogram"), ("L08", "cscv-explorer")]
log = {}
with sync_playwright() as p:
    browser = p.chromium.launch()
    for page_id, fig in jobs:
        for width in (360, 1280):
            for theme in ("light", "dark"):
                ctx = browser.new_context(viewport={"width": width, "height": 900}, color_scheme=theme)
                page = ctx.new_page()
                errors = []
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
                page.goto(f"http://127.0.0.1:{port}/modules/S/S7/{page_id}.html", wait_until="load")
                page.wait_for_selector(f'[data-chart="{fig}"] svg', timeout=20000)
                el = page.locator(f'[data-chart="{fig}"]').first
                el.evaluate("e => e.scrollIntoView({block: 'center'})")
                page.wait_for_timeout(300)
                name = f"{fig}-{width}-{theme}.png"
                el.screenshot(path=os.path.join(OUT, name))
                log[name] = {"errors": errors, "box": el.bounding_box()}
                ctx.close()
    browser.close()
httpd.shutdown()
with open(os.path.join(OUT, "log.json"), "w") as fh:
    json.dump(log, fh, indent=1, default=str)
print(json.dumps({k: len(v["errors"]) for k, v in log.items()}))
