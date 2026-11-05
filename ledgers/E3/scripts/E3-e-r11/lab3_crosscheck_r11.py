# Cross-check of the Lab 3 reference case (answers copied from the page) against grader/reference.py.
import sys, re, importlib.util
from fractions import Fraction
page = open(sys.argv[1], encoding="utf-8").read()
ref_path = sys.argv[2]
block = re.search(r'<pre><code class="language-python" data-run>"""Rung 3 reference case.*?</code></pre>', page, re.S).group(0)
import html
code = html.unescape(re.sub(r"</?code[^>]*>|</?pre>", "", block))
ns = {}
# take only the ANSWERS literal
m = re.search(r"ANSWERS: list\[Answer\] = \[(.*?)\n\]", code, re.S)
answers = eval("[" + m.group(1) + "]", {"Fraction": Fraction})
print("answers:", len(answers))
mixed = 0
for a in answers:
    _, _, pa, qa, pb, qb = a
    def mix(prizes, probs):
        g = any(x > 0 and Fraction(p) > 0 for x, p in zip(prizes, probs))
        l = any(x < 0 and Fraction(p) > 0 for x, p in zip(prizes, probs))
        return g and l
    if mix(pa, qa) or mix(pb, qb): mixed += 1
print("mixed-sign answers (independent count):", mixed)
spec = importlib.util.spec_from_file_location("ref", ref_path)
ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
resp = []
for pid, ch, pa, qa, pb, qb in answers:
    resp.append({"pair_id": pid, "choice": ch, "prizes_a": pa, "probs_a": [str(Fraction(p)) for p in qa],
                 "prizes_b": pb, "probs_b": [str(Fraction(p)) for p in qb]})
r = ref.estimate(resp)
for k, v in sorted(r.items()):
    print(k, repr(v))
