"""Set each live control of the two L01 figures to chosen states and read the rendered readout and desc text."""
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
        pg = b.new_page(viewport={"width": 1000, "height": 900}, color_scheme="light")
        pg.goto(f"{origin}/modules/S/S7/L01.html", wait_until="load")
        pg.wait_for_selector('html[data-ready="true"]', timeout=60000)
        def state(years):
            pg.evaluate("""(v) => { const r = document.querySelector('[data-chart="max-sharpe-density"] ~ * input[type=range], figure input[type=range]');
                const el = Array.from(document.querySelectorAll('input[type=range]'))[0]; el.value = String(v);
                el.dispatchEvent(new Event('input', {bubbles: true})); el.dispatchEvent(new Event('change', {bubbles: true})); }""", years)
            pg.wait_for_timeout(400)
            return pg.evaluate("""() => {
                const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
                let n, t = null;
                while ((n = w.nextNode())) { if (n.data.includes('of daily data (T =')) { t = n.data.trim(); break; } }
                const d = document.querySelector('[data-chart="max-sharpe-density"] desc');
                return {readout: t || null, desc: d ? d.textContent : null};
            }""")
        for y in (1, 5, 20):
            r = state(y)
            print("YEARS", y, "READOUT:", r["readout"])
            print("YEARS", y, "DESC_TAIL:", (r["desc"] or "")[-260:])
        pg.close()
        b.close()
finally:
    server.shutdown()
