"""Round 7: hub placement answers, hours arithmetic, question marks in visible prose, and the two skill-check conventions (run with -I)."""
import html.parser
import re
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(".").resolve()
idx = (ROOT / "course/modules/PC/PC3/index.html").read_text(encoding="utf-8")
answers = re.findall(r'data-kind="numeric"[^>]*data-answer="([^"]+)" data-tolerance="([^"]+)"', idx)
expected = {
    "3.5": F(21, 6), "0.25": F(1, 2) * F(1, 2), "2": F(2), "3": F(3), "90.909091": F(100) / F(11, 10), "-10005": F(-10005),
    "10040": F(10040),
}
print("numeric placement answers in order:", answers)
for ans, tol in answers:
    ref = expected.get(ans)
    print(f"  answer {ans}: exact {float(ref) if ref is not None else 'n/a'} tolerance {tol}")
print("ln(e^2) =", 2.0, "; d/dx x^3 at 1 =", 3 * 1 ** 2, "; 100/1.1 =", f"{100 / 1.1:.9f}")
print("80 percent of 10 items = 8; 7/10 =", 7 / 10)
print("hours: 6*6 =", 6 * 6, "; 36+14 =", 36 + 14, "; 14/50 =", 14 / 50)
print("project lines in index: 2 + 6 + 4 + 2 =", 2 + 6 + 4 + 2)
print("project time budget (project.html): rung1 1 + rung2 1 + quote 3 + replay 2 + autograder 2 + analysis 4 + self-assessment 1 =", 1 + 1 + 3 + 2 + 2 + 4 + 1)
print("policy.py + pnl.py per project table: 3 + 2 =", 3 + 2)
# visible prose question marks
class T(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.p, self.k = [], 0
    def handle_starttag(self, t, a):
        if t in ("script", "style", "code", "pre"):
            self.k += 1
    def handle_endtag(self, t):
        if t in ("script", "style", "code", "pre"):
            self.k -= 1
    def handle_data(self, d):
        if not self.k:
            self.p.append(d)
for pg in ["index", "L01", "L02", "L03"]:
    t = T()
    t.feed((ROOT / f"course/modules/PC/PC3/{pg}.html").read_text(encoding="utf-8"))
    txt = " ".join(t.p)
    print(f"{pg}: question marks in prose (outside code): {txt.count('?')}")
