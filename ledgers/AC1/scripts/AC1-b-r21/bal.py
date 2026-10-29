import sys, types
src = open('/tmp/verify21-AC1-b/tests/labs/AC1/lab-AC1-L05-1.py').read().replace("\nmain()\n", "\n")
mod = types.ModuleType('l05x'); sys.modules['l05x'] = mod
exec(compile(src, 'l05x', 'exec'), mod.__dict__)
m = mod
c = m.generate(m.SEED)
alloc = m.allocate(c.price_cents, [o.standalone_cents for o in c.obligations])
rec = [0, *m.cumulative(m.revenue_schedule(c, alloc, False))]
for up in (40, 0):
    b = m.billing_schedule(c.price_cents, up)
    bc = m.cumulative(b)
    bal = [x - y for x, y in zip(bc, rec)]
    print('upfront', up, 'balances', bal)
    print(' first asset month', next((i for i, v in enumerate(bal) if v < 0), None), 'asset months', [i for i, v in enumerate(bal) if v < 0])
    print(' peak liability', max(bal), 'at month', bal.index(max(bal)))
print('rev_cum', rec)
print('price', c.price_cents)
