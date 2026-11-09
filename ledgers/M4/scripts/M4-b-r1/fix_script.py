p = "/Users/billyribeiro/.fanout/wt/verifyF21-M4-b/ledgers/M4/scripts/M4-b-r1/build_fragment.py"
s = open(p, encoding="utf-8").read()
reps = [
 ('"base": "329c1d7f1c9e0c4e0b0b5f5a3e3f0c1d0c9b8a7f is NOT used; base is the round-12 fragment', '"base": "round-12 fragment'),
 ('(" + S + "/../../../../../ledgers/M4/scripts/M4-b-r1 n/a);', '(" + S + "/twin_vs_page.out);'),
 ('14 removed incl. c241 of L05', '26 removed incl. c241 of L05'),
 ('defines sigma = sqrt(Var X) (L02.html:101)', 'defines sigma = sqrt(Var X) (L02.html:100-101)'),
]
for a, b in reps:
    n = s.count(a)
    print(n, a[:50])
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
