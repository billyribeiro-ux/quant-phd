import json, re, sys
cards = json.load(open(sys.argv[1]))
changed = ['E1-c018','E1-c023','E1-c030','E1-c039','E1-c056','E1-c101','E1-c160','E1-c161','E1-c162','E1-c163','E1-c164','E1-c165','E1-c166']
def toks(c):
    return set(re.findall(r'[a-z0-9]+', (c['front'] + ' ' + c['back']).lower()))
by = {c['id']: c for c in cards}
for cid in changed:
    a = toks(by[cid])
    best = max(((len(a & toks(c)) / len(a | toks(c)), c['id']) for c in cards if c['id'] != cid))
    print(cid, 'max Jaccard vs other cards: %.3f with %s' % (best[0], best[1]))
