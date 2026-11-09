# Probes L04.html rendered in Chromium (file://) for math-free phrases that sit next to the three raw "<" sites
# (lines 56, 240, 249). Each needle is also checked in the source. KaTeX output has no backslash sequences, so
# needles contain no math. Run from the checkout root.
from playwright.sync_api import sync_playwright
root = "/Users/billyribeiro/.fanout/wt/verifyS4-M5-a/course/modules/M/M5/L04.html"
probes = {
    "line 56 (F6 proof): 'and F3 gives'": "and F3 gives",
    "line 56 (F6 proof): 'so the conclusion' is not used; 'If' + 'taking' + 'gives' (control, before the raw <)": "taking",
    "line 240 (open-set definition): 'is open when'": "is open when",
    "line 240 (closed-set definition, control): 'is closed when'": "is closed when",
    "line 249 (Prop 2.1 proof): 'and since y was arbitrary'": "since y was arbitrary",
    "line 249 (Prop 2.1 proof): 'Hence'": "Hence",
}
src = open(root, encoding="utf-8").read()
with sync_playwright() as pw:
    b = pw.chromium.launch()
    p = b.new_page()
    p.goto("file://" + root)
    p.wait_for_timeout(800)
    text = p.evaluate("() => document.querySelector('main').innerText")
    for label, needle in probes.items():
        print(f"{label}: source={'yes' if needle in src else 'NO'} rendered={'PRESENT' if needle in text else 'ABSENT'}")
    i = text.find("open ball")
    print("rendered around 'open ball':", repr(text[i:i+200]))
    b.close()
