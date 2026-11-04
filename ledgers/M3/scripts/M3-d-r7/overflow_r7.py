"""List elements whose right edge exceeds the 360 px viewport on project.html (light and dark). Read-only."""
import sys
from playwright.sync_api import sync_playwright

url = sys.argv[1]
JS = """
() => {
  const W = window.innerWidth;
  const out = [];
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    if (r.right > W + 1) {
      out.push([el.tagName, el.className && el.className.baseVal === undefined ? el.className : '', el.id,
                Math.round(r.left), Math.round(r.right), Math.round(r.width),
                (el.textContent || '').trim().slice(0, 70)]);
    }
  }
  return {W, sw: document.documentElement.scrollWidth, out: out.slice(0, 40)};
}
"""
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for scheme in ("light",):
        ctx = b.new_context(viewport={"width": 360, "height": 760}, color_scheme=scheme)
        p = ctx.new_page()
        p.goto(url, wait_until="load")
        p.wait_for_function("document.documentElement.dataset.ready === 'true'", timeout=60000)
        res = p.evaluate(JS)
        print(scheme, "innerWidth", res["W"], "scrollWidth", res["sw"])
        for row in res["out"]:
            print(row)
    b.close()
