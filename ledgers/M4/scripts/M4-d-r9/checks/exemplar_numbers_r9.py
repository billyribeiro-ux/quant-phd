"""Round-9 check: word counts of the two exemplars' passages (body = memo-text paragraphs; headings separately),
the Summary counts, and the prose numbers the exemplar annotations quote, recomputed from the Lab 1 and Lab 3 outputs.
Word = a run of characters between spaces (project.html line 326). Usage: python -I <this file> (from the checkout root)
"""
import html
import math
import pathlib
import re
import statistics
from fractions import Fraction

text = pathlib.Path("course/modules/M/M4/project.html").read_text(encoding="utf-8")


def article(aid: str) -> str:
    s = text.index(f'id="{aid}"')
    return text[s: text.index("</article>", s)]


def words(fragment: str) -> int:
    plain = html.unescape(re.sub(r"<[^>]+>", " ", fragment))
    return len(plain.split())


for aid in ("exemplar-a", "exemplar-b"):
    art = article(aid)
    passages = re.findall(r'<div class="memo-text">(.*?)</div>', art, re.S)
    heads = [words(re.search(r"<h5>(.*?)</h5>", p, re.S).group(1)) for p in passages]
    bodies = [words(re.sub(r"<h5>.*?</h5>", "", p, flags=re.S)) for p in passages]
    print(f"{aid}: passages {len(passages)}, body words per passage {bodies}, total body {sum(bodies)}, heading words {sum(heads)}")
    summary = re.search(r"<h5>Summary</h5>\s*<p>(.*?)</p>", art, re.S)
    if summary:
        print(f"{aid}: Summary words {words(summary.group(1))}")

# Lab 1 and Lab 3 numbers quoted in prose
target = 3_000_000 * 3_000_000 * 4e-4 + 2 * 3_000_000 * 2_000_000 * 1e-4 + 2_000_000 * 2_000_000 * 9e-4
sd = math.sqrt(target)
z99 = statistics.NormalDist().inv_cdf(0.99)
print("target", round(target, 3), "sd", round(sd, 3), "z99", round(z99, 6), "parametric 99% loss", z99 * sd, "rounded", round(z99 * sd))
print("gaussian 99 minus parametric", 213213 - 210946, "student minus gaussian", 243004 - 210946,
      "ratio pct", round(100 * (243004 - 210946) / 210946, 2), "ratio t/g", round(243004 / 210946, 4))
print("1.0447 minus 1 in percent of 1:", round(100 * (1.0447 - 1), 2), "; inflation 5/3 =", round(5 / 3, 6))
print("1.0017 within 5%:", abs(1.0017 - 1) <= 0.05, "; 1.0447 within 5%:", abs(1.0447 - 1) <= 0.05)
print("213213 cents in dollars", 213213 / 100, "; exemplar A quotes about 2,130 dollars")
print("0.99*101 =", float(Fraction(99, 100) * 101), "; 0.99*20000 =", float(Fraction(99, 100) * 20000))
print("ceil(0.99*100)", math.ceil(Fraction(99, 100) * 100), "floor", math.floor(Fraction(99, 100) * 100))
print("0.99*19987 =", float(Fraction(99, 100) * 19987))
