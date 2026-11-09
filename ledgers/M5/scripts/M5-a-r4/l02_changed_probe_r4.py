# Probes the rendered L02 (Chromium, file://) for the sentences changed since the round-3 pin, and for the removed H2 item.
from playwright.sync_api import sync_playwright
P = "/Users/billyribeiro/.fanout/wt/verifyS4-M5-a/course/modules/M/M5/L02.html"
probes = [
    "Proposition 3.3 does not use (H2).",
    "This step does not use completeness, because Proposition 2.2 does not need it.",
    "Tending to zero is necessary for convergence (apply Proposition 2.2 to the partial sums and take",
    "and so in the converse direction of Corollary 3.2, which is proved from Theorem 2.5.",
    "Only the consequence on divergence uses it",
    "Proposition 3.3 (harmonic partial sums are not Cauchy)",
    "For the consequence, the harmonic series has partial sums",
    "Then (H_n) converges, and Proposition 2.2 makes it Cauchy",
]
with sync_playwright() as pw:
    b = pw.chromium.launch()
    p = b.new_page()
    p.goto("file://" + P)
    p.wait_for_timeout(700)
    text = p.evaluate("() => document.querySelector('main').innerText")
    for needle in probes:
        print("PRESENT" if needle in text else "ABSENT ", needle)
    # hypothesis list of Proposition 3.3: count hypothesis items in that block
    n = p.evaluate("""() => { const h = [...document.querySelectorAll('.block.proposition')].find(b => b.textContent.includes('harmonic partial sums are not Cauchy')); return h ? h.querySelectorAll('ol.hypotheses li').length : -1; }""")
    print("hypothesis items in Proposition 3.3 (rendered):", n)
    b.close()
