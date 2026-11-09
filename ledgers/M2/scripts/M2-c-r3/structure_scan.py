"""Structure and count checks for L13-L18 (verifier round 3). Standard library only."""
import re
for n in range(13, 19):
    p = f"course/modules/M/M2/L{n:02d}.html"
    t = open(p, encoding="utf-8").read()
    why = re.search(r'<p class="why-it-matters">(.*?)</p>', t, flags=re.S).group(1)
    why_words = len(re.sub(r"<[^>]+>|\\\(.*?\\\)", " ", why).split())
    hours = re.search(r'data-hours="(\d+)"', t).group(1)
    mis = len(re.findall(r'<li class="misconception">', t))
    quiz = len(re.findall(r'<li class="item"', t))
    tiers = {tier: len(re.findall(r'<div class="problem" id="%s-' % tier, t)) for tier in ("mech", "proof", "emp", "res")}
    sols = len(re.findall(r'<details class="solution">', t))
    labs = re.findall(r'<section class="lab"[^>]*id="([^"]+)"', t)
    marks = [t.find(m) for m in ("why-it-matters", 'id="s1"', 'class="lab"', "canon-breaks", 'class="misconceptions"', 'class="problem-set"', 'id="key-results"', 'class="quiz"', 'class="references"')]
    order_ok = all(x >= 0 for x in marks) and marks == sorted(marks)
    print(f"L{n:02d} order_ok={order_ok} why_words={why_words} hours={hours} misconceptions={mis} quiz_items={quiz} problems={tiers} solutions={sols} labs={labs}")
