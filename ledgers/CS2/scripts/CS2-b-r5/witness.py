# Witness: memoized recursion vs table fill touch the same subproblems for D={1}, A=3
import sys
def coin_memo(D, A):
    memo = {0: 0}; touched = set()
    def f(a):
        touched.add(a)
        if a in memo: return memo[a]
        best = min((1 + f(a - c) for c in D if c <= a), default=float('inf'))
        memo[a] = best
        return best
    return f(A), touched
def coin_table(D, A):
    T = [0] + [float('inf')] * A
    for a in range(1, A + 1):
        T[a] = min((1 + T[a - c] for c in D if c <= a), default=float('inf'))
    return T[A], set(range(A + 1))
print("D={1},A=3 memo", coin_memo([1], 3), "table", coin_table([1], 3))
print("D={1,3,4},A=6 memo", coin_memo([1,3,4], 6)[1], "table touches", sorted(coin_table([1,3,4],6)[1]))
