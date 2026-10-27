"""Drive the live figures of S7 L01 and L02 in headless Chromium (Playwright, venv) and dump their <desc> and readout text."""
import json
import sys
from pathlib import Path

CHECKOUT = Path(sys.argv[1])
sys.path.insert(0, str(CHECKOUT / "tools"))
import page_smoke  # noqa: E402  (their own local server helper; no network)
from playwright.sync_api import sync_playwright  # noqa: E402

server, origin = page_smoke.serve()
out: dict[str, object] = {}
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for page_name in ("L01", "L02"):
            page = browser.new_page(viewport={"width": 1000, "height": 900}, color_scheme="light")
            page.goto(f"{origin}/modules/S/S7/{page_name}.html", wait_until="load")
            page.wait_for_selector('html[data-ready="true"]', timeout=60000)
            charts = page.evaluate("""() => Array.from(document.querySelectorAll('[data-chart]')).map(e => e.getAttribute('data-chart'))""")
            for chart in charts:
                info = page.evaluate(
                    """(id) => {
                        const root = document.querySelector(`[data-chart="${id}"]`);
                        const fig = root.closest('figure') || root.parentElement;
                        const desc = root.querySelector('desc') ? root.querySelector('desc').textContent : null;
                        const readouts = Array.from(fig.querySelectorAll('[data-readout], .readout, output')).map(e => e.textContent.trim());
                        const inputs = Array.from(fig.querySelectorAll('input[type=range]')).map(i => ({key: i.name || i.id, value: i.value, min: i.min, max: i.max}));
                        return {desc, readouts, inputs, figtext: fig.textContent.replace(/\\s+/g, ' ').trim().slice(0, 400)};
                    }""",
                    chart,
                )
                out[f"{page_name}:{chart}"] = info
        browser.close()
finally:
    server.shutdown()
Path(sys.argv[2]).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
for k, v in out.items():
    print(k, "| desc:", (v["desc"] or "")[:300])
    print("   readouts:", [r[:300] for r in v["readouts"]], "| inputs:", v["inputs"])
