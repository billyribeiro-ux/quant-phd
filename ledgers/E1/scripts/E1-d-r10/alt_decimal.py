"""Alternative correct implementation: Decimal with 60 digits, ROUND_HALF_UP, closed forms as Decimal."""
from decimal import Decimal, ROUND_HALF_UP, getcontext
getcontext().prec = 60
def _r(x):
    return int(x.quantize(Decimal(1), rounding=ROUND_HALF_UP))
def outcome(structure, a, b, c):
    if structure not in ("monopoly","cournot","bertrand"): raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b*c: raise ValueError("a must exceed b*c")
    if b <= 0: raise ValueError("b must be positive")
    if c <= 0: raise ValueError("c must be positive")
    A,B,C=Decimal(a),Decimal(b),Decimal(c); d=A-B*C
    if structure=="monopoly": Q=d/2; f=(A+B*C)/(2*B)
    elif structure=="cournot": Q=2*d/3; f=(A+2*B*C)/(3*B)
    else: Q=d; f=C
    p=(f-C)*Q; cs=Q*Q/(2*B); w=cs+p; dwl=(d-Q)**2/(2*B)
    return {"volume_trades":_r(Q),"fee_cents":_r(f),"profit_cents":_r(p),"consumer_surplus_cents":_r(cs),"welfare_cents":_r(w),"deadweight_loss_cents":_r(dwl)}
