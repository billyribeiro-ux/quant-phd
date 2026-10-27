import re
from playwright.sync_api import sync_playwright
URL = "http://127.0.0.1:8765/modules/AP/AP1/project.html"
A = {"C1": 2, "C2": 2, "C3": 1, "C4": 2, "C5": 2, "C6": 2}
B = {"C1": 4, "C2": 4, "C3": 4, "C4": 4, "C5": 3, "C6": 4}
S = {c: 3 for c in A}
errors = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("console", lambda m: errors.append("console:" + m.text) if m.type == "error" else None)
    page.goto(URL, wait_until="load")
    page.wait_for_selector("form.rubric-form", timeout=30000)
    radios = page.locator("form.rubric-form input[type=radio]")
    names = [radios.nth(i).get_attribute("name") for i in range(radios.count())]
    pat = re.compile(r"^(?P<prefix>[^-]+)-(?P<target>.+)-(?P<crit>C\d)$")
    targets = []
    for n in names:
        m = pat.match(n)
        if m and m.group("target") not in targets: targets.append(m.group("target"))
    print("radios:", len(names), "| targets:", targets)
    scores = {}
    for t in targets:
        scores[t] = B if t == "exemplar-b" else A if t == "exemplar-a" else S
    for t in targets:
        for c, v in scores[t].items():
            name = next(n for n in names if pat.match(n) and pat.match(n).group("target") == t and pat.match(n).group("crit") == c)
            page.locator(f'input[name="{name}"][value="{v}"]').check()
    page.get_by_role("button", name="Reveal the official scoring").click()
    page.wait_for_selector(".rubric-results .rubric-summary", timeout=15000)
    for s in page.locator(".rubric-results .rubric-summary").all_inner_texts(): print("SUMMARY:", s[:260])
    tbl = page.locator(".rubric-results table").first
    rows = tbl.locator("tr").all_inner_texts()
    for r in rows[:8]: print("ROW:", r.replace("\n", " | ")[:200])
    print("C3 row:", [r.replace("\n", " | ") for r in rows if "C3" in r][:2])
    print("exemplar-a visible annotation count:", page.locator("#exemplar-a .annotation").first.is_visible())
    print("errors:", errors)
    browser.close()
