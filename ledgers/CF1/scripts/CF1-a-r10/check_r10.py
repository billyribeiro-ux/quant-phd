flows=[-10000,3000,3200,3400,3600,3800]
def npv(f,r): return sum(c/(1+r)**t for t,c in enumerate(f))
for r in (0,0.05,0.10,0.15,0.20): print('A',r,round(npv(flows,r),2))
print('misc 1000 outlay', round(-1000+600/1.2+600/1.44,2), 'undiscounted', -1000+600+600)
# conventional stream with C0 = 0: NPV stays positive at all rates
g=[0,100]
print('C0=0 conventional min over grid', min(npv(g,r/100) for r in range(-99,2000)))
# R1: loss fraction of same-period credit = r/(1+r)
for r in (0.05,0.1):
    same=(1+r)**-1; carried=(1+r)**-2
    print('R1 frac', r, (same-carried)/same, r/(1+r))
