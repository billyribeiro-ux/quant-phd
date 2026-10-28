import subprocess,pathlib
P=pathlib.Path('/tmp/AC4-v/AC4-d-r18'); PY='/tmp/verify18-AC4-d/.venv/bin/python'
base=pathlib.Path('/tmp/verify18-AC4-d/tests/labs/AC4/lab-AC4-L08-1.py').read_text()
exp=(P/'L08.exp0').read_text().strip()
muts=[
 ("n01_eva_plus_tax","nopat = Fraction(d.oi) * (10_000 - TAX_BP) / 10_000","nopat = Fraction(d.oi) * (10_000 + TAX_BP) / 10_000"),
 ("n02_eva_tax_bp_as_percent","nopat = Fraction(d.oi) * (10_000 - TAX_BP) / 10_000","nopat = Fraction(d.oi) * (100 - TAX_BP) / 100"),
 ("n03_capitalized_no_addback_oi","replace(d, invested=d.invested + SPEND - first_year, oi=d.oi + SPEND - first_year)","replace(d, invested=d.invested + SPEND - first_year, oi=d.oi)"),
 ("n04_capitalized_full_amort_base","replace(d, invested=d.invested + SPEND - first_year, oi=d.oi + SPEND - first_year)","replace(d, invested=d.invested + SPEND, oi=d.oi + SPEND - first_year)"),
 ("n05_rate_bp_as_fraction","return Fraction(d.oi) - Fraction(RATE_BP, 10_000) * d.invested","return Fraction(d.oi) - Fraction(RATE_BP, 100) * d.invested"),
 ("n06_ratio_on_oi_wrong_scale","return Fraction(d.oi, d.invested)","return Fraction(d.oi, 2 * d.invested)"),
 ("n07_ri_side_strict_only","sign_ok = [(residual_income(d) >= 0) == (return_ratio(d) >= Fraction(RATE_BP, 10_000)) for d in divisions]","sign_ok = [(residual_income(d) > 0) == (return_ratio(d) >= Fraction(RATE_BP, 10_000)) for d in divisions]"),
 ("n08_gap_check_wrong_sign","gap_ok = [eva(d) - residual_income(d) == -Fraction(TAX_BP, 10_000) * d.oi for d in divisions]","gap_ok = [eva(d) - residual_income(d) == Fraction(TAX_BP, 10_000) * d.oi for d in divisions]"),
 ("n09_discord_pairs_same_name_order","if a.name < b.name:","if a.name <= b.name:"),
]
for name,old,new in muts:
    assert base.count(old)==1,name
    f=P/'mut'/f'L08_{name}.py'; f.write_text(base.replace(old,new,1))
    r=subprocess.run([PY,'-I','-W','error',str(f)],capture_output=True,text=True,timeout=60)
    print(name,'rc=',r.returncode,'output_same=',r.stdout.strip()==exp,(r.stderr.strip().splitlines() or [''])[-1][:90])
