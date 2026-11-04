"""Mechanical card checks for M2 (round 6, slice e).

For every card: (1) every labelled reference (Theorem/Proposition/Lemma/Definition/Remark/Example/
Assumption/Misconception/Problem/Corollary X.Y, Lab N Part Z) in the card must appear in the lesson of the card;
(2) duplicate ids and duplicate fronts across the whole file; (3) card lesson ids are real pages.
Usage: python -I cards_refs_r6.py <cards.json> <course dir>
"""
import json, os, re, sys, collections
cards = json.load(open(sys.argv[1]))
course = sys.argv[2]
pat = re.compile(r"\b(Theorem|Proposition|Lemma|Definition|Remark|Example|Assumption|Misconception|Problem|Corollary|Lab) (\d+(?:\.\d+)?|[MPERD]\d)\b")
texts = {}
def lesson_text(L):
    if L not in texts:
        p = os.path.join(course, L + '.html')
        if not os.path.exists(p):
            texts[L] = None
        else:
            import subprocess
            out = subprocess.run([sys.executable, '-I', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'totext.py'), p], capture_output=True, text=True).stdout
            texts[L] = out
    return texts[L]
ids = collections.Counter(c['id'] for c in cards)
fronts = collections.Counter(c['front'].strip().lower() for c in cards)
print('cards', len(cards), 'dup ids', [i for i, n in ids.items() if n > 1], 'dup fronts', [f for f, n in fronts.items() if n > 1])
bad = []
for c in cards:
    t = lesson_text(c['lesson'])
    if t is None:
        bad.append((c['id'], 'no lesson page', c['lesson'])); continue
    refs = set(m.group(0) for m in pat.finditer(c['front'] + ' ' + c['back']))
    for r in sorted(refs):
        # the lesson must contain the label followed by the number (labels may be in sans-serif spans)
        if not re.search(re.escape(r), t):
            bad.append((c['id'], c['lesson'], 'label not in lesson', r))
print('label/lesson mismatches', len(bad))
for b in bad:
    print(' ', b)
