# For each standing card mutant file: the cards whose text differs from HEAD, and the word-level change in each.
import difflib, glob, json, os, sys
HEAD = json.load(open('course/modules/LX/LX2/cards.json', encoding='utf-8'))
cur = {c['id']: c for c in HEAD}
for f in sorted(glob.glob('ledgers/LX2/mutants/*card*.json')):
    m = {c['id']: c for c in json.load(open(f, encoding='utf-8'))}
    out = []
    for k in sorted(set(cur) | set(m)):
        a, b = cur.get(k), m.get(k)
        if a == b:
            continue
        if a is None or b is None:
            out.append(f"{k}: present only in {'mutant' if a is None else 'HEAD'}")
            continue
        for fld in sorted(set(a) | set(b)):
            if a.get(fld) == b.get(fld):
                continue
            sa, sb = str(a.get(fld)).split(), str(b.get(fld)).split()
            ops = [(t, ' '.join(sa[i1:i2]), ' '.join(sb[j1:j2])) for t, i1, i2, j1, j2 in difflib.SequenceMatcher(None, sa, sb).get_opcodes() if t != 'equal']
            out.append(f"{k}.{fld}: " + ' | '.join(f"[{t}] '{x}' -> '{y}'" for t, x, y in ops)[:400])
    print(os.path.basename(f), 'cards differing from HEAD:', len(out))
    for line in out[:8]:
        print('   ', line)
