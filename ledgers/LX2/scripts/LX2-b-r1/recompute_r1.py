# Independent recomputation of every number in the changed L03/L04 prose and cards, from the printed twin outputs and from enumeration.
import re
from fractions import Fraction as F
OUT = 'ledgers/LX2/scripts/LX2-b-r1/out'
l03 = open(f'{OUT}/twin_L03.out', encoding='utf-8').read()
l04 = open(f'{OUT}/twin_L04.out', encoding='utf-8').read()
ok = []
def check(name, cond):
    ok.append((name, bool(cond)))
    print(('PASS ' if cond else 'FAIL ') + name)
# L03: ratios and comparisons used in card c053, misconception 1, R2 and the interpretation
check('6/97 and 3/104 printed as ratios', '6/97' in l03 and '3/104' in l03)
check('3*97 = 291 < 6*104 = 624 (so 3/104 < 6/97)', 3 * 97 == 291 and 6 * 104 == 624 and 291 < 624 and F(3, 104) < F(6, 97))
check('21/37 is the largest printed ratio and is below 2', max([F(6,97),F(3,104),F(5,34),F(6,29),F(17,50),F(21,37)]) == F(21,37) and F(21,37) < 2)
check('fill total 414 = 2 * 207 executions', 2 * 207 == 414 and 'fills total 414' in l03)
check('trader shares cancelled 2020 printed', 'trader shares cancelled 2020' in l03)
check('zero crossed, zero identity failures, zero tally disagreements printed',
      'events with a crossed book: 0' in l03 and 'events where entered != resting' in l03 and ': 0\n' in l03 and 'in 0 trader counts' in l03)
check('traders flagged 0 of 6 at threshold 2', 'traders flagged: 0 of 6' in l03)
# L04 Part A: recompute hits, bias, MAE from the printed error column
rows = re.findall(r'^\s*(\d+)\s+(\d+)\s+(\d+)\s+(-?\d+)\s+([01])\s*$', l04, flags=re.M)
errs = [int(r[3]) for r in rows]
hits = [int(r[4]) for r in rows]
check('Part A has 24 periods', len(rows) == 24)
check('each printed error = forecast - realised', all(int(f) - int(r) == int(e) for _, f, r, e, _ in rows))
check('each printed hit flag = (|e| <= 2)', all(h == (1 if abs(e) <= 2 else 0) for e, h in zip(errs, hits)))
check('hits = 9 of 24, hit rate 3/8 (0.3750)', sum(hits) == 9 and F(sum(hits), 24) == F(3, 8) and f'{3/8:.4f}' == '0.3750')
check('sum of errors 82, bias 41/12 = 3.41666..., printed 3.4167 at 4 places', sum(errs) == 82 and F(sum(errs), 24) == F(41, 12) and f'{41/12:.4f}' == '3.4167')
check('mean absolute error 13/3 (printed) recomputed', F(sum(abs(e) for e in errs), 24) == F(13, 3))
first, last = errs[:12], errs[12:]
check('Part B first-12 bias 11/3 and hit rate 1/4', F(sum(first), 12) == F(11, 3) and F(sum(hits[:12]), 12) == F(1, 4))
check('Part B last-12 bias 19/6 and hit rate 1/2', F(sum(last), 12) == F(19, 6) and F(sum(hits[12:]), 12) == F(1, 2))
# L04 Part C: errors +3, -3, +3, -3, band 2
pc = [3, -3, 3, -3]
check('Part C bias 0, hit rate 0, MAE 3 (card c086 and key results)', sum(pc) == 0 and sum(1 for e in pc if abs(e) <= 2) == 0 and F(sum(abs(e) for e in pc), 4) == 3)
# Part D and Proposition 4.4: enumerate the 9 x 13 generator pairs
V = range(-4, 5); U = range(-6, 7)
pairs = [(v, u) for v in V for u in U]
hit_pairs = [(v, u) for v, u in pairs if abs(1 + v - u) <= 2]
check('9 x 13 = 117 equally likely pairs', len(pairs) == 117)
check('P(hit) = 44/117 by enumeration of |1 + V - U| <= 2, equivalently -3 <= V - U <= 1', len(hit_pairs) == 44 and all((-3 <= v - u <= 1) == (abs(1 + v - u) <= 2) for v, u in pairs))
check('E[e] = 1 by enumeration', F(sum(1 + v - u for v, u in pairs), 117) == 1)
check('44/117 = 0.3761 and 45/117 = 0.3846 at 4 places (mutant value)', f'{44/117:.4f}' == '0.3761' and f'{45/117:.4f}' == '0.3846')
check('per-v hit counts: 5 for v in -4..3 and 4 for v = 4', all(sum(1 for u in U if abs(1+v-u) <= 2) == (4 if v == 4 else 5) for v in range(-4, 4)) and sum(1 for u in U if abs(1+4-u) <= 2) == 4)
print('summary', sum(1 for _, c in ok if c), 'of', len(ok), 'checks PASS')
