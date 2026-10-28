# Runs the twin's book (unchanged code) and a variant whose loop reads the best ask once, before the loop.
# Confirms: the stale variant raises KeyError at self.levels[opposite][best] (the line that reads the removed level).
import importlib.util, sys, pathlib
TWIN = pathlib.Path('/tmp/verifyB5-CS2-b/tests/labs/CS2/lab-CS2-L08-1.py')
SCRATCH = pathlib.Path('/tmp/CS2-v/CS2-b-r5/exp')
SCRATCH.mkdir(parents=True, exist_ok=True)

def load(name, path):
    src = path.read_text(encoding='utf-8').replace('\nmain()\n', '\n')
    tmp = SCRATCH / f'{name}.py'
    tmp.write_text(src, encoding='utf-8')
    spec = importlib.util.spec_from_file_location(name, tmp)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

src = TWIN.read_text(encoding='utf-8')
s2 = src.replace('        while incoming.qty > 0:\n            best = self.best(opposite)', '        best = self.best(opposite)\n        while incoming.qty > 0:')
assert s2 != src
(SCRATCH / 'stale_variant_src.py').write_text(s2, encoding='utf-8')
good = load('twin_good', TWIN)
b = good.Book()
b.submit('S', 10000, 1, 1); b.submit('S', 10005, 5, 2)
print('correct trades', [(t.qty, t.price, t.maker) for t in b.submit('B', 10010, 3, 3)])
stale = load('twin_stale', SCRATCH / 'stale_variant_src.py')
b2 = stale.Book()
b2.submit('S', 10000, 1, 1); b2.submit('S', 10005, 5, 2)
try:
    print('stale trades', b2.submit('B', 10010, 3, 3))
except Exception as e:
    print('stale raised', type(e).__name__, e)
print('stale book asks after error', b2.prices['S'], 'live', sorted(b2.live))
