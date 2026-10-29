import math, random, sys
import importlib.util
src = open('/tmp/verify20-CF1-c/tests/labs/CF1/lab-CF1-L06-1.py').read().replace('\nmain()\n', '\n')
ns = {'__name__': 'x'}
exec(compile(src, 'lab', 'exec'), ns)
rng = random.Random(6)
npvs = [ns['npv_of']([rng.randint(50000, 150000) for _ in range(5)]) for _ in range(50000)]
ordered = sorted(npvs)
q10 = ns['quantile'](ordered, 0.10); q90 = ns['quantile'](ordered, 0.90); med = ns['quantile'](ordered, 0.5)
print('q10 %.6f q50 %.6f q90 %.6f' % (q10, med, q90))
d = q90 - q10
print('diff %.6f rounds2 %.2f printed-diff %.2f gap %.4f' % (d, round(d,2), 143406.13-14896.62, (143406.13-14896.62)-d))
neg = sum(1 for x in npvs if x < 0)
print('neg count', neg, 'share', neg/50000, 'share4', round(neg/50000,4))
p = neg/50000
print('se', math.sqrt(p*(1-p)/50000), round(math.sqrt(p*(1-p)/50000),4))
print('2761/50000', 2761/50000, 'se at 2761', math.sqrt((2761/50000)*(1-2761/50000)/50000))
print('check 1000 ', 143406.126569 - 14896.623057, 143406.13-14896.62)
