"""Forward-reference scan for E3 lessons L01-L08 (verifier round 14, slice e).

For each lesson, finds where each labelled block (Definition/Proposition/Theorem/Lemma/Corollary/Remark/Example/
Assumption/Observation) is defined, then lists every textual mention of that label that occurs earlier in the page
than the definition. Mentions in the why-it-matters paragraph and in the quiz and problem explanations are tagged.
"""
import re
import sys
import html

ROOT = sys.argv[1]
LABEL = r"(Definition|Proposition|Theorem|Lemma|Corollary|Remark|Example|Observation|Assumptions?|Problem)\s+([A-Z]?\d+(?:\.\d+)?)"
for n in range(1, 9):
    path = f"{ROOT}/course/modules/E/E3/L0{n}.html"
    raw = open(path, encoding="utf-8").read()
    raw = re.sub(r"<script.*?</script>", "", raw, flags=re.S)
    raw = re.sub(r"<pre.*?</pre>", "", raw, flags=re.S)
    text = html.unescape(raw)
    # definition sites: a block-title span that starts with the label
    defs = {}
    for m in re.finditer(r'<span class="block-title[^>]*>\s*(' + LABEL + r')', text):
        key = m.group(2) + " " + m.group(3)
        defs.setdefault(key, m.start())
    # problems have ids; their spans are 'problem-title'
    for m in re.finditer(r'<span class="problem-title">\s*([A-Z]\d)\s*·', text):
        defs.setdefault("Problem " + m.group(1), m.start())
    quiz_start = text.find('<section class="quiz"')
    wim_end = text.find('</p>', text.find('class="why-it-matters"'))
    out = []
    for m in re.finditer(LABEL, text):
        key = m.group(1) + " " + m.group(2)
        if key not in defs:
            continue
        pos = m.start()
        if pos < defs[key] and not (m.start() >= defs[key] - 60 and m.start() <= defs[key] + 60):
            tag = "WHY-IT-MATTERS" if pos < wim_end else ("QUIZ/PROBLEM" if quiz_start != -1 and pos > quiz_start else "BODY")
            out.append((tag, key, text[max(0, pos - 70):pos + 40].replace("\n", " ")))
    print(f"== L0{n}: forward mentions {len(out)}")
    for tag, key, ctx in out:
        print(f"  [{tag}] {key}: ...{ctx}...")
