"""Verifier r10: facts stated in Exemplar B (prize range, prize counts, pair 0 and pair 3 values, mixed count)."""
import re, html
from fractions import Fraction
page = open("/Users/billyribeiro/.fanout/wt/verifyD10-E3-e/course/modules/E/E3/project.html", encoding="utf-8").read()
sec = re.search(r'<section class="lab[^"]*" id="lab-E3-project-3".*?</section>', page, re.S).group(0)
code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1))
s = code.index("ANSWERS: list"); e = code.index("\n]\n", s) + 3
ns = {}; exec("from fractions import Fraction\n" + code[s:e], ns)
A = ns["ANSWERS"]
prizes = [x for a in A for x in (a[2] + a[4])]
print("min prize", min(prizes), "max prize", max(prizes))
print("prize counts per lottery", sorted({len(a[2]) for a in A} | {len(a[4]) for a in A}))
print("pair0", A[0][2], A[0][3], A[0][4], A[0][5])
print("pair3", A[3][2], A[3][3], A[3][4], A[3][5])
mixed = lambda p, q: any(x > 0 and Fraction(y) > 0 for x, y in zip(p, q)) and any(x < 0 and Fraction(y) > 0 for x, y in zip(p, q))
print("pairs with a mixed lottery", sum(1 for a in A if mixed(a[2], a[3]) or mixed(a[4], a[5])))
print("probabilities sum exactly 1 for every lottery", all(sum(Fraction(y) for y in a[3]) == 1 and sum(Fraction(y) for y in a[5]) == 1 for a in A))
print("pair ids in data", len(A))
