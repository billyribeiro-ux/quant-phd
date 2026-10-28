exec(open("/tmp/m1-v6/d/mkalts.py").read().split("ALTS = {}")[0])
s = REF.replace('''    if r == 0:
        return float(n)''', '''    if r == 0:
        return n''')
assert s != REF
open("/tmp/m1-v6/d/alts/witness_int_zero_rate.py", "w").write(s)
print("ok")
