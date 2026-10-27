import subprocess, time, sys, socket
from playwright.sync_api import sync_playwright
PORT = 8765
srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                       cwd="/tmp/verify-ap1-r10-m/course", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        errors = []
        pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(f"http://127.0.0.1:{PORT}/modules/AP/AP1/project.html", wait_until="load")
        pg.wait_for_selector('html[data-ready="true"]', timeout=60000)
        form = pg.locator("#self-assessment")
        radios = form.locator('input[type=radio]')
        names = {}
        for i in range(radios.count()):
            names.setdefault(radios.nth(i).get_attribute("name"), []).append(i)
        print("radio groups:", len(names), "radios:", radios.count())
        for name, idxs in names.items():
            radios.nth(idxs[1]).check()  # choose level 2 (second option)
        btn = form.locator("button", has_text="Reveal the official scoring")
        print("reveal buttons:", btn.count())
        btn.first.click()
        pg.wait_for_timeout(500)
        summaries = form.locator(".rubric-summary").count()
        table_rows = pg.locator("#self-assessment table tr").count()
        print("summaries after reveal:", summaries, "table rows:", table_rows)
        exA = pg.locator("#exemplar-a .annotation")
        print("exemplar A annotations visible:", exA.first.is_visible() if exA.count() else "none")
        print("console/page errors:", errors)
        b.close()
finally:
    srv.terminate()
