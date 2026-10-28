import subprocess,sys,pathlib
P=pathlib.Path('/tmp/AC4-v/AC4-d-r18')
base=pathlib.Path('/tmp/verify18-AC4-d/tests/labs/AC4/lab-AC4-L07-1.py').read_text()
base8=pathlib.Path('/tmp/verify18-AC4-d/tests/labs/AC4/lab-AC4-L08-1.py').read_text()
exp7=(P/'L07.exp0').read_text(); exp8=(P/'L08.exp0').read_text()
muts=[
 ("L07","n01_displaced_no_external","return max(0, c.q + c.external - c.capacity)","return max(0, c.q - c.capacity)"),
 ("L07","n02_floor_integer_floor","return Fraction(c.v) + Fraction(displaced(c) * (c.p_m - c.v), c.q)","return Fraction(c.v) + Fraction(displaced(c) * (c.p_m - c.v) // c.q)"),
 ("L07","n03_strict_equality_assert","assert (lo <= hi) == (firm_surplus(c) >= 0)","assert (lo < hi) == (firm_surplus(c) > 0)"),
 ("L07","n04_buyer_gain_sign","return c.q * (Fraction(c.r_net) - t)","return c.q * (t - Fraction(c.r_net))"),
 ("L07","n05_firm_surplus_price","return c.q * (c.r_net - c.v) - displaced(c) * (c.p_m - c.v)","return c.q * (c.r_net - c.v) - displaced(c) * c.p_m"),
 ("L07","n06_tmax_market_price","return Fraction(c.r_net)\n","return Fraction(c.p_m)\n"),
 ("L07","n07_midpoint_wrong","(lo + hi) / 2","(lo + hi)"),
 ("L07","n08_no_sum_check","assert supplier_increment(c, t) + buyer_increment(c, t) == firm_surplus(c)","pass"),
 ("L07","n09_boundary_dropped_from_list","cases = [*generate(SEED, N_CASES), BOUNDARY]","cases = [*generate(SEED, N_CASES), BOUNDARY, BOUNDARY]"),
 ("L07","n10_nonempty_strict_count","empty = [c for c in fits if t_min(c) > t_max(c)]","empty = [c for c in fits if t_min(c) >= t_max(c)]"),
 ("L07","n11_no_boundary_assert_feasible","feasible = [c for c in fits if t_min(c) <= t_max(c)]","feasible = [c for c in fits if t_min(c) < t_max(c)]"),
 ("L07","n12_check_skip_equal","for c in fits:\n        lo, hi","for c in [x for x in fits if x is not BOUNDARY]:\n        lo, hi"),
]
results=[]
for lab,name,old,new in muts:
    src=base
    if src.count(old)<1: print("NOMATCH",name); continue
    m=src.replace(old,new,1)
    f=P/'mut'/f'{name}.py'; f.write_text(m)
    r=subprocess.run(['/tmp/verify18-AC4-d/.venv/bin/python','-I','-W','error',str(f)],capture_output=True,text=True,timeout=60)
    out=r.stdout
    killed = (r.returncode!=0) or (out.strip()!=exp7.strip())
    print(name, 'KILLED' if killed else 'SURVIVED', 'rc=',r.returncode, (r.stderr.strip().splitlines() or [''])[-1][:120])
