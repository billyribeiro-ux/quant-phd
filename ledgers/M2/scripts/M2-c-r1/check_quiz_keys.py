"""Print each retrieval-quiz item's prompt and its keyed (data-correct) option, with its explanation (verifier scratch)."""
import html
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
clean = lambda s: html.unescape(re.sub(r"<[^>]+>", "", s)).strip()
for n in range(13, 19):
    page = open(f"{ROOT}/course/modules/M/M2/L{n}.html", encoding="utf-8").read()
    quiz = re.search(r'<section class="quiz" id="quiz".*?</section>', page, re.S).group(0)
    for k, item in enumerate(re.findall(r'<li class="item".*?</li>', quiz, re.S), 1):
        prompt = clean(re.search(r'<p class="prompt">(.*?)</p>', item, re.S).group(1))
        opts = re.findall(r'<label class="option"([^>]*)>(.*?)</label>', item, re.S)
        keyed = [clean(t) for attrs, t in opts if "data-correct" in attrs]
        expl = re.search(r'<div class="explain"[^>]*>(.*?)</div>', item, re.S)
        expl_t = clean(expl.group(1)) if expl else "NO EXPLAIN"
        print(f"L{n} q{k}: {prompt[:110]}")
        print(f"    options={len(opts)} keyed={keyed}")
        print(f"    explain: {expl_t[:200]}")
