# Loads L04.html and L02.html in headless Chromium (Playwright, from the project venv) from file://, and prints
# whether the text around each raw "<" (in math) survives in the rendered DOM. Run from the checkout root.
import sys
from playwright.sync_api import sync_playwright
root = "/Users/billyribeiro/.fanout/wt/verifyS4-M5-a/course/modules/M/M5/"
checks = {
    "L04.html": ["A set “", "is open when", "for each \\(x\\in U\\)", "The open ball", "is closed when"],
}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    p = b.new_page()
    for page_name in ["L04.html"]:
        p.goto("file://" + root + page_name)
        p.wait_for_timeout(800)
        text = p.evaluate("() => document.querySelector('main').innerText")
        print(page_name, "innerText length", len(text))
        for needle in ["The open ball", "is open when", "is closed when", "A set", "is not open by Remark 2.2", "for every x"]:
            print(repr(needle), "present" if needle in text else "ABSENT")
        # the paragraph containing the open-ball definition: what is shown
        i = text.find("open ball")
        print("around 'open ball':", repr(text[max(0, i-80): i+260]) if i >= 0 else "not found")
        # DOM: count of bogus elements whose tag names start with 'r' or 'c' or 'd' right after a '<'
        bogus = p.evaluate("""() => Array.from(document.querySelectorAll('main *')).map(e => e.tagName.toLowerCase()).filter(t => /[\\\\()]/.test(t))""")
        print("elements with backslash or paren in tag name:", bogus[:10])
    b.close()
