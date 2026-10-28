import sys
from playwright.sync_api import sync_playwright
url = "http://127.0.0.1:8765/modules/M/M1/project.html"
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(url)
    pg.wait_for_selector('html[data-ready="true"]', timeout=20000)
    ann = pg.evaluate("""() => [...document.querySelectorAll('#exemplar-a .annotation, #exemplar-b .annotation')].map(e => e.hidden)""")
    verd = pg.evaluate("""() => [...document.querySelectorAll('#exemplar-a [data-reveal], #exemplar-b [data-reveal]')].map(e => e.hidden)""")
    btn = pg.get_by_role("button", name="Reveal the official scoring")
    print("before reveal: annotation hidden flags", ann, "verdict hidden flags", verd, "button count", btn.count())
    if btn.count():
        btn.first.click()
        pg.wait_for_timeout(500)
        ann2 = pg.evaluate("""() => [...document.querySelectorAll('#exemplar-a .annotation, #exemplar-b .annotation')].map(e => e.hidden)""")
        verd2 = pg.evaluate("""() => [...document.querySelectorAll('#exemplar-a [data-reveal], #exemplar-b [data-reveal]')].map(e => e.hidden)""")
        print("after reveal: annotation hidden flags", ann2, "verdict hidden flags", verd2)
    print("page errors:", errs)
    b.close()
