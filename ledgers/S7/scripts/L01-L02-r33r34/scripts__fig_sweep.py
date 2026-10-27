"""Sweep every range control of the live L01 and L02 figures across its values (light theme, desktop) and dump readout/desc."""
import json
import sys
from pathlib import Path

CHECKOUT = Path(sys.argv[1])
sys.path.insert(0, str(CHECKOUT / "tools"))
import page_smoke  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

server, origin = page_smoke.serve()
out = []
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for scheme, width, name, chart in [(sc, w, n, c) for sc in ("light", "dark") for w in (1280, 360)
                                           for (n, c) in (("L01", "max-sharpe-density"), ("L02", "fwer-growth"), ("L02", "power-family"))]:
            pg = b.new_page(viewport={"width": width, "height": 900}, color_scheme=scheme)
            errors = []
            pg.on("pageerror", lambda e: errors.append(str(e)))
            pg.goto(f"{origin}/modules/S/S7/{name}.html", wait_until="load")
            pg.wait_for_selector('html[data-ready="true"]', timeout=60000)
            fig = pg.evaluate("(c) => { const r = document.querySelector(`[data-chart=\"${c}\"]`); return r.closest('figure') ? true : false; }", chart)
            rng = pg.evaluate("""(c) => { const r = document.querySelector(`[data-chart="${c}"]`); const f = r.closest('figure') || r.parentElement;
                return Array.from(f.querySelectorAll('input[type=range]')).map(i => ({min: +i.min, max: +i.max, step: +i.step || 1, value: i.value, idx: Array.from(document.querySelectorAll('input[type=range]')).indexOf(i)})); }""", chart)
            print(scheme, width, name, chart, "ranges", rng)
            if not rng:
                pg.close(); continue
            rg = rng[0]
            vals = []
            v = rg["min"]
            while v <= rg["max"] + 1e-9:
                vals.append(round(v, 6)); v += rg["step"]
            for v in vals:
                res = pg.evaluate("""([idx, v]) => { const el = Array.from(document.querySelectorAll('input[type=range]'))[idx];
                    el.value = String(v); el.dispatchEvent(new Event('input', {bubbles: true})); el.dispatchEvent(new Event('change', {bubbles: true})); return true; }""", [rg["idx"], v])
                pg.wait_for_timeout(120)
                txt = pg.evaluate("""(c) => { const r = document.querySelector(`[data-chart="${c}"]`); const d = r.querySelector('desc');
                    const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n, t = null;
                    while ((n = w.nextNode())) { if (/of daily data \\(T =|Power is/.test(n.data) && n.data.length < 400) { t = n.data.trim(); break; } }
                    return {desc: d ? d.textContent : null, text: t}; }""", chart)
                out.append({"page": name, "chart": chart, "scheme": scheme, "width": width, "control": rg, "value": v, **txt})
            print(scheme, width, name, chart, "states", len(vals), "page errors", errors)
            pg.close()
        b.close()
finally:
    server.shutdown()
Path(sys.argv[2]).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("total states", len(out))
