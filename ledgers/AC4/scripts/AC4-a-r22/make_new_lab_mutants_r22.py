import pathlib,sys
root=pathlib.Path('/tmp/verify22-AC4-a')
src2=(root/'tests/labs/AC4/lab-AC4-L02-1.py').read_text()
src1=(root/'tests/labs/AC4/lab-AC4-L01-1.py').read_text()
out=root/'ledgers/AC4/mutants/AC4-a-r22'
muts={
 'L02_q01_step_at_2510.py': (src2,'STEP_ABOVE_UNITS = 2000','STEP_ABOVE_UNITS = 2510'),
 'L02_q02_margin_ratio_over_price_minus_fixed.py': (src2,'    margin = price - variable\n','    margin = price - variable - 1\n'),
 'L01_q01_residual_uses_low_month_only.py': (src1,'residuals.append(cents(residual))','residuals.append(cents(residual)) if hours != 428 else residuals.append(0)'),
}
for name,(s,a,b) in muts.items():
    assert s.count(a)==1,(name,s.count(a))
    (out/name).write_text(s.replace(a,b))
    print('wrote',name)
