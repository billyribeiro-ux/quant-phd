from playwright.sync_api import sync_playwright
URL = "http://127.0.0.1:8765/units/../modules/M/M2/project.html"
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("http://127.0.0.1:8765/modules/M/M2/project.html")
    pg.wait_for_selector('html[data-ready="true"]', timeout=60000)
    res = pg.evaluate("""() => {
      const out = {};
      for (const id of ['exemplar-a','exemplar-b']) {
        const ex = document.getElementById(id);
        out[id] = {annotations: [...ex.querySelectorAll('.annotation')].map(a => a.hidden || getComputedStyle(a).display==='none'),
                   verdict: [...ex.querySelectorAll('[data-reveal]')].map(a => a.hidden || getComputedStyle(a).display==='none')};
      }
      return out;
    }""")
    print("before reveal (true = hidden):", res)
    btn = pg.get_by_role("button", name="Reveal the official scoring")
    print("reveal button count:", btn.count())
    btn.first.click()
    pg.wait_for_timeout(500)
    res2 = pg.evaluate("""() => {
      const out = {};
      for (const id of ['exemplar-a','exemplar-b']) {
        const ex = document.getElementById(id);
        out[id] = [...ex.querySelectorAll('.annotation, [data-reveal]')].map(a => a.hidden || getComputedStyle(a).display==='none');
      }
      return out;
    }""")
    print("after reveal (true = hidden):", res2)
    print("page errors:", errs)
    b.close()
