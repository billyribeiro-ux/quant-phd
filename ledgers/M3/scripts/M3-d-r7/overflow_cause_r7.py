"""Diagnose the 360 px horizontal scroll on project.html: scrollWidth before and after making the long
identifier inside the 'Alternating steps' bullet breakable (diagnostic only; no page file is changed)."""
import sys
from playwright.sync_api import sync_playwright

url = sys.argv[1]
with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width": 360, "height": 760}, color_scheme="light")
    p = ctx.new_page()
    p.goto(url, wait_until="load")
    p.wait_for_function("document.documentElement.dataset.ready === 'true'", timeout=60000)
    before = p.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
    print("before: scrollWidth, innerWidth =", before)
    li = p.evaluate("""() => { const el = [...document.querySelectorAll('li')].find(
        x => x.textContent.includes('Alternating steps')); const c = el.querySelector('code:not(.x)');
        const codes=[...el.querySelectorAll('code')].map(c=>[c.textContent.slice(0,60), Math.round(c.getBoundingClientRect().width)]);
        return codes; }""")
    print("code elements in the Alternating-steps bullet (text, width px):", li)
    p.add_style_tag(content="code{overflow-wrap:anywhere !important; word-break:break-all !important}")
    after = p.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
    print("after breaking code identifiers: scrollWidth, innerWidth =", after)
    b.close()
