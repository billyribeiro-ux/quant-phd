"""Holm staircase figure: both states of its select control, read from the live page (light, desktop and 360 px)."""
import sys
from pathlib import Path
CHECKOUT = Path(sys.argv[1])
sys.path.insert(0, str(CHECKOUT / "tools"))
import page_smoke  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402
server, origin = page_smoke.serve()
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for scheme in ("light", "dark"):
            for width in (1280, 360):
                pg = b.new_page(viewport={"width": width, "height": 900}, color_scheme=scheme)
                pg.goto(f"{origin}/modules/S/S7/L02.html", wait_until="load")
                pg.wait_for_selector('html[data-ready="true"]', timeout=60000)
                for val in ("reported", "recomputed"):
                    pg.evaluate("""(v) => { const s = document.querySelector('[data-chart="holm-staircase"]').closest('figure').querySelector('select');
                        s.value = v; s.dispatchEvent(new Event('change', {bubbles: true})); }""", val)
                    pg.wait_for_timeout(150)
                    d = pg.evaluate("""() => document.querySelector('[data-chart="holm-staircase"] desc').textContent""")
                    print(scheme, width, val, "|", d[-140:])
                pg.close()
        b.close()
finally:
    server.shutdown()
