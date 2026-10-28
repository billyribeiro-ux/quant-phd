import importlib.util,sys
def load(p,n):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
ref=load('/tmp/verifyC1-FC1-c/course/modules/FC/FC1/grader/reference.py','ref')
v02=load('/tmp/verifyC1-FC1-c/ledgers/FC1/mutants/v02_price_rounded_half_even.py','v02')
v04=load('/tmp/verifyC1-FC1-c/ledgers/FC1/mutants/v04_price_from_float_discounting.py','v04')
v01=load('/tmp/verifyC1-FC1-c/ledgers/FC1/mutants/v01_print_on_refused_quantity.py','v01')
print("ref price Bond(1,0,1) at 10000 bps:", ref.bond_price_cents(ref.Bond(1,0,1),10000))
print("v02 price same input:", v02.bond_price_cents(v02.Bond(1,0,1),10000))
print("v02 price Bond(10000,500,3) at 400 (fixture):", v02.bond_price_cents(v02.Bond(10000,500,3),400))
print("ref price Bond(10001,5000,2)? ", ref.bond_price_cents(ref.Bond(1,0,1),-5000*0+0))
# float mutant: find a case with an exact half in exact arithmetic where float round differs
from fractions import Fraction as F
for face,cpn,n,yb in [(1,0,1,10000),(3,0,1,10000),(5,0,1,10000),(10001,0,1,10000)]:
    print("case",face,cpn,n,yb,"ref",ref.bond_price_cents(ref.Bond(face,cpn,n),yb),"v04",v04.bond_price_cents(v04.Bond(face,cpn,n),yb))
print("v01 quantity refused, stdout captured by call:")
try: v01.CashTrade(0,9850,1,2)
except ValueError as e: print("ValueError:",e)
