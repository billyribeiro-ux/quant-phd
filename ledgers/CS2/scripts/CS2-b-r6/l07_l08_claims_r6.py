import sys, re, types
# Load a twin's definitions without running its trailing main() call.
def load(path):
    src = open(path, encoding="utf-8").read()
    src = re.sub(r"\nmain\(\)\s*$", "\n", src)
    mod = types.ModuleType("twin")
    exec(compile(src, path, "exec"), mod.__dict__)
    return mod

base = "/Users/billyribeiro/.fanout/wt/verifyB6-CS2-b/tests/labs/CS2/"
l07 = load(base + "lab-CS2-L07-1.py")
# Instrumented copy of the memoized LCS recursion: classify each call.
def lcs_classify(x, y):
    cache = {}
    calls = {"base": 0, "hit": 0, "computed": 0}
    def go(i, j):
        if i == 0 or j == 0:
            calls["base"] += 1
            return 0
        if (i, j) in cache:
            calls["hit"] += 1
            return cache[(i, j)]
        calls["computed"] += 1
        v = go(i-1, j-1) + 1 if x[i-1] == y[j-1] else max(go(i-1, j), go(i, j-1))
        cache[(i, j)] = v
        return v
    go(len(x), len(y))
    return calls, len(cache)
print("L07 memo", l07.lcs_memo("ACGTACG", "TGCATGC"))
print("L07 table", l07.lcs_table("ACGTACG", "TGCATGC"))
print("L07 naive", l07.lcs_naive_calls("ACGTACG", "TGCATGC"))
print("L07 classify (calls by kind, stored)", lcs_classify("ACGTACG", "TGCATGC"))
print("L07 coins memo(1,3,4),20", l07.coins_memo((1,3,4), 20), "naive", l07.coins_naive_calls((1,3,4), 20))
print("L07 coins memo(1,3,4),6", l07.coins_memo((1,3,4), 6), "greedy", l07.greedy_count((1,3,4), 6), "table", l07.coins_table((1,3,4),6))
print("L07 denominations {1}, amount 3 memo stored", l07.coins_memo((1,), 3))
print("L07 Part A first instance", l07.lcs_table(*l07.make_lcs_instances(l07.Lcg(l07.SEED))[0]))
print("L07 lcs AB/BA", l07.lcs_table("AB", "BA"))
print("L07 P3 greedy vs f for 1..6 with {1,3,4}")
for a in range(1, 7):
    print(" ", a, l07.greedy_count((1,3,4), a), l07.coins_table((1,3,4), a)[0])
print("L07 coins impossible count", sum(1 for d, a in l07.make_coin_instances(l07.Lcg(l07.SEED)) if l07.coins_table(d, a)[0] is None))
