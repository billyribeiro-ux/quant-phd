# Does a lottery whose positive-probability prizes contain a zero (and no gain, or no loss) have a certainty equivalent free of lambda?
import sys
from fractions import Fraction
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyD8-E3-d/course/modules/E/E3/grader")
import reference as ref
cases = {
    "{0 w.p.1/2, -100 w.p.1/2} (no gain, zero is neither gain nor loss)": ([0, -100], [Fraction(1, 2), Fraction(1, 2)]),
    "{0 w.p.1/2, 100 w.p.1/2} (no loss)": ([0, 100], [Fraction(1, 2), Fraction(1, 2)]),
    "{-100 w.p.1/2, 300 w.p.1/2} (mixed, control)": ([-100, 300], [Fraction(1, 2), Fraction(1, 2)]),
}
for name, (pr, pq) in cases.items():
    vals = []
    for lam in (0.5, 1.0, 2.0, 3.0):
        vals.append(ref._prospect_ce(pr, pq, 0.4, lam))
    print(f"{name}: unrounded CE at lambda 0.5,1,2,3 = {[round(v, 9) for v in vals]}  lambda-free: {max(vals)-min(vals) < 1e-9}")
