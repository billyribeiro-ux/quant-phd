import sys, re, random
src=open('/tmp/verifyB2-CS2-b/tests/labs/CS2/lab-CS2-L06-1.py').read()
# take function definitions only (exclude the top-level main() call)
body=src.split('\nmain()')[0]
ns={}
exec(compile(body,'lab','exec'),ns)
rng=random.Random(20261028)
calls=0; total=0
orig=None
for k in range(40):
    n=3+k%5; p=0.2+0.1*(k%4)
    adj=ns['random_graph'](rng,n,p)
    for s in range(n):
        ns['brute_min_hops'](adj,s)
# count simple paths the lab's extend visits: re-implement by instrumenting extend text
import types
code=body.replace("    def extend(v: int, length: int) -> None:\n        for u in adj[v]:\n            if u in on_path:\n                continue",
 "    def extend(v: int, length: int) -> None:\n        CNT[0]+=1\n        for u in adj[v]:\n            if u in on_path:\n                continue")
assert code!=body
ns2={'CNT':[0]}
exec(compile(code,'lab2','exec'),ns2)
rng=random.Random(20261028)
for k in range(40):
    n=3+k%5; p=0.2+0.1*(k%4)
    adj=ns2['random_graph'](rng,n,p)
    for s in range(n):
        ns2['brute_min_hops'](adj,s)
print("extend calls (= simple paths from each source, no pruning):", ns2['CNT'][0])
