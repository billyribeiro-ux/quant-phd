import subprocess,pathlib
P=pathlib.Path('/tmp/AC4-v/AC4-d-r18'); PY='/tmp/verify18-AC4-d/.venv/bin/python'
base=pathlib.Path('/tmp/verify18-AC4-d/tests/labs/AC4/lab-AC4-L07-1.py').read_text()
exp7=(P/'L07.exp0').read_text().strip()
def run(name,src):
    f=P/'mut'/f'{name}.py'; f.write_text(src)
    r=subprocess.run([PY,'-I','-W','error',str(f)],capture_output=True,text=True,timeout=60)
    same=r.stdout.strip()==exp7
    print(name,'rc=',r.returncode,'output_same=',same, (r.stderr.strip().splitlines() or [''])[-1][:100])
# deletions
for name,old,new in [
 ("del_supplier_assert","assert supplier_increment(c, lo) == 0","pass"),
 ("del_buyer_assert","assert buyer_increment(c, hi) == 0","pass"),
 ("del_sum_assert","assert supplier_increment(c, t) + buyer_increment(c, t) == firm_surplus(c)","pass"),
 ("del_biconditional","assert (lo <= hi) == (firm_surplus(c) >= 0)","pass"),
 ("boundary_strict_only","assert (lo <= hi) == (firm_surplus(c) >= 0)","assert (lo < hi) == (firm_surplus(c) > 0)"),
]:
    assert base.count(old)==1, name
    run(name, base.replace(old,new))
# alternatives (correct)
alt_a=base.replace("return max(0, c.q + c.external - c.capacity)","return c.external - min(c.external, c.capacity - c.q)")
run("alt_a_D_via_min",alt_a)
alt_b=base.replace("    return Fraction(c.v) + Fraction(displaced(c) * (c.p_m - c.v), c.q)",
 "    from decimal import Decimal, getcontext\n    getcontext().prec = 60\n    return Fraction(Decimal(c.v) + Decimal(displaced(c) * (c.p_m - c.v)) / Decimal(c.q))")
assert alt_b!=base
run("alt_b_decimal_tmin",alt_b)
alt_c=base.replace("        if lo <= hi:\n            for t in (lo, hi, (lo + hi) / 2):","        if lo <= hi:\n            for t in (lo, hi, (lo + hi) / 2):")
alt_c=alt_c.replace("        assert (lo <= hi) == (firm_surplus(c) >= 0)","        assert (not (lo > hi)) == (firm_surplus(c) >= 0)")
run("alt_c_negated_form",alt_c)
