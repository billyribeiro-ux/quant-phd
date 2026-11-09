"""Structure counts for L04-L06: problems per tier, misconceptions, quiz items, key-result rows, section order,
solution blocks, hours, and quiz answer keys (data-answer vs the answer the page's own explanation gives).
Run: python3 -I structure_counts.py <checkout_root>
"""
import html
import re
import sys

root = sys.argv[1]
for p in ("L04", "L05", "L06"):
    s = open(f"{root}/course/modules/PC/PC3/{p}.html", encoding="utf-8").read()
    tiers = re.findall(r'<div class="tier" data-tier="(\w+)">(.*?)</div>\s*</div>', s, re.S)
    counts = {}
    for name, body in tiers:
        counts[name] = len(re.findall(r'<div class="problem"', body))
    sols = len(re.findall(r'<details class="solution">', s))
    misc = len(re.findall(r'<li class="misconception">', s))
    quiz = len(re.findall(r'<li class="item"', s))
    kr = len(re.findall(r'<tr><td>', s))
    hours = re.search(r'data-hours="(\d+)"', s).group(1)
    secs = re.findall(r'<h2 id="(s\d+)"><span class="section-number">(\d+)</span>([^<]*)', s)
    print(p, "hours", hours, "tiers", counts, "solutions", sols, "misconceptions", misc, "quiz items", quiz,
          "key-result rows", kr)
    print("   sections:", [(n, t) for _, n, t in secs])
    items = re.findall(r'<li class="item" data-kind="(\w+)">(.*?)</li>', s, re.S)
    for kind, body in items:
        ans = re.search(r'data-answer="([^"]+)"', body)
        tol = re.search(r'data-tolerance="([^"]+)"', body)
        prompt = html.unescape(re.sub(r"<[^>]+>", "", re.search(r'<p class="prompt">(.*?)</p>', body, re.S).group(1)))
        if kind == "numeric":
            print("   numeric key", ans.group(1), "tol", tol.group(1), "|", prompt[:90])
        else:
            correct = re.findall(r'<label class="option" data-correct>(.*?)</label>', body, re.S)
            allopts = re.findall(r'<label class="option"[^>]*>(.*?)</label>', body, re.S)
            print("   mc", len(allopts), "options; correct:", [html.unescape(re.sub(r"<[^>]+>", "", c)).strip()[:60] for c in correct], "|", prompt[:70])
