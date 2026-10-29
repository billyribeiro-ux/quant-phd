"""Alternative correct implementation: integer numerators and denominators only, half-up via integer division."""
def _hu(num, den):
    return (2*num + den) // (2*den)
def outcome(structure, a, b, c):
    if structure not in ("monopoly","cournot","bertrand"): raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b*c: raise ValueError("a must exceed b*c")
    if b <= 0: raise ValueError("b must be positive")
    if c <= 0: raise ValueError("c must be positive")
    d=a-b*c
    if structure=="monopoly": vn,vd=d,2; fn,fd=a+b*c,2*b
    elif structure=="cournot": vn,vd=2*d,3; fn,fd=a+2*b*c,3*b
    else: vn,vd=d,1; fn,fd=c,1
    # profit=(f-c)*Q ; numerator over fd*vd
    pn,pd=(fn-c*fd)*vn, fd*vd
    csn,csd=vn*vn,2*b*vd*vd
    wn,wd=None,None
    cs_den=csd; w_den=csd*pd//__import__('math').gcd(csd,pd)
    wn=csn*(w_den//csd)+pn*(w_den//pd); wd=w_den
    dn,dd=(d*vd-vn)**2, 2*b*vd*vd
    return {"volume_trades":_hu(vn,vd),"fee_cents":_hu(fn,fd),"profit_cents":_hu(pn,pd),"consumer_surplus_cents":_hu(csn,csd),"welfare_cents":_hu(wn,wd),"deadweight_loss_cents":_hu(dn,dd)}
