import subprocess, sys, time
from playwright.sync_api import sync_playwright
srv = subprocess.Popen([sys.executable, "-m", "http.server", "8766", "--bind", "127.0.0.1"],
                       cwd="/tmp/verify-ap1-r10-m/course", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("http://127.0.0.1:8766/modules/AP/AP1/project.html", wait_until="load")
        pg.wait_for_selector('html[data-ready="true"]', timeout=90000)
        sec = pg.locator("#lab-AP1-project-3")
        sec.scroll_into_view_if_needed()
        sec.locator("button", has_text="Run").first.click()
        out = sec.locator("pre.output")
        pg.wait_for_function("(el) => el && !el.hidden && el.textContent.includes('max |in-sample error|')", arg=out.element_handle(), timeout=240000)
        text = out.inner_text()
        for line in text.splitlines():
            if "in-sample" in line or "checksums" in line or "rms" in line: print(line)
        print("page errors:", errs)
        b.close()
finally:
    srv.terminate()
