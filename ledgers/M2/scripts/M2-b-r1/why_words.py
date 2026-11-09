# Word counts of the why-it-matters paragraph under three counting rules (python -I).
import re, html
for n in range(7, 13):
    src = open(f"course/modules/M/M2/L{n:02d}.html", encoding="utf-8").read()
    raw = re.search(r'<p class="why-it-matters">(.*?)</p>', src, re.S).group(1)
    plain = html.unescape(re.sub(r"<[^>]+>", "", raw))
    math_free = re.sub(r"\\\(.*?\\\)", " ", plain)
    a = len(math_free.split())                       # prose words only, math removed
    b = len(plain.split())                           # math spans count as whitespace-separated tokens
    c = len(re.findall(r"[A-Za-z][A-Za-z'-]*", plain))  # alphabetic words, incl. inside math
    print(f"L{n:02d} prose_only={a} tokens_incl_math={b} alpha_words={c}")
