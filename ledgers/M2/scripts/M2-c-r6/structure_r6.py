"""Round-6 structure scan for M2 slice c (L13-L18): why-it-matters word count (BUILDER_RULES 4.2 item 1),
misconception count, problem-set tier counts, quiz item count, solution blocks, and section order."""
import html
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
for n in range(13, 19):
    src = (root / f"course/modules/M/M2/L{n}.html").read_text(encoding="utf8")
    wim = re.search(r'<p class="why-it-matters">(.*?)</p>', src, flags=re.S)
    words = len(html.unescape(re.sub(r"<[^>]+>", " ", wim.group(1))).split())
    mis = len(re.findall(r'<li class="misconception">', src))
    tiers = {t: len(re.findall(rf'data-tier="{t}".*?</div>\s*</div>', src, flags=re.S)) for t in ("mechanics", "proof", "empirical", "research")}
    probs = {t: len(re.findall(r'<div class="problem"', re.search(rf'data-tier="{t}".*?(?=<div class="tier"|</section>)', src, flags=re.S).group(0))) for t in ("mechanics", "proof", "empirical", "research")}
    sols = len(re.findall(r'<details class="solution">', src))
    quiz = len(re.findall(r'<li class="item"', src))
    expl = len(re.findall(r'<div class="explain" hidden>', src))
    order = [m.start() for m in (re.search(p, src) for p in (r'id="why|class="why-it-matters"', r'class="core-content"|id="s1"', r'class="lab"', r'class="canon-breaks"', r'class="misconceptions"', r'class="problem-set"', r'id="key-results"', r'class="quiz"', r'class="references"'))]
    print(f"L{n}: why-it-matters words {words}; misconceptions {mis}; problems per tier {probs}; solutions {sols}; quiz items {quiz}; explanations {expl}; section-order-ok {order == sorted(order)}")
