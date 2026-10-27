"""Round-29 part C: load course/dev/design-system.html (the only page that links base.css, components.css and tokens.css)
in Chromium at 1280 and 360 px, light and dark, from the checkout's own course/ tree. Records HTTP status of every
stylesheet and script, console errors and page errors. Run: python -I design_system_load_C.py <checkout> <out.json>"""
import http.server
import json
import os
import socketserver
import sys
import threading

from playwright.sync_api import sync_playwright

ROOT, OUT = sys.argv[1], sys.argv[2]


def handler(*a, **k):
    return http.server.SimpleHTTPRequestHandler(*a, directory=os.path.join(ROOT, "course"), **k)


class Quiet(http.server.SimpleHTTPRequestHandler):
    pass


socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.ThreadingTCPServer(("127.0.0.1", 0), lambda *a, **k: http.server.SimpleHTTPRequestHandler(*a, directory=os.path.join(ROOT, "course"), **k))
port = httpd.server_address[1]
threading.Thread(target=httpd.serve_forever, daemon=True).start()
result = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for width in (1280, 360):
        for theme in ("light", "dark"):
            ctx = b.new_context(viewport={"width": width, "height": 900}, color_scheme=theme)
            page = ctx.new_page()
            errs, reqs = [], []
            page.on("pageerror", lambda e: errs.append(str(e)))
            page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            page.on("response", lambda r: reqs.append([r.url.rsplit("/", 1)[-1], r.status]) if r.request.resource_type in ("stylesheet", "script") else None)
            page.goto(f"http://127.0.0.1:{port}/dev/design-system.html", wait_until="load")
            page.wait_for_timeout(500)
            result[f"{width}-{theme}"] = {
                "title": page.title(),
                "stylesheets_and_scripts": sorted({tuple(x) for x in reqs}),
                "errors": errs,
                "body_width_px": page.evaluate("document.documentElement.scrollWidth"),
            }
            ctx.close()
    b.close()
httpd.shutdown()
json.dump(result, open(OUT, "w"), indent=1, ensure_ascii=False)
print(json.dumps({k: {"errors": len(v["errors"]), "scrollWidth": v["body_width_px"]} for k, v in result.items()}))
