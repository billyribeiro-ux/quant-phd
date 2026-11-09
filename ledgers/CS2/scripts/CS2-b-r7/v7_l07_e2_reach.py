"""Round 7 (CS2 slice b): independent re-derivation of the L07 E2 solution (reachable pairs, table cells)."""
import sys

x, y = "ACGTACG", "TGCATGC"
m, n = len(x), len(y)
reached = set()
stack = [(m, n)]
while stack:
    i, j = stack.pop()
    if i == 0 or j == 0 or (i, j) in reached:
        continue
    reached.add((i, j))
    if x[i - 1] == y[j - 1]:
        stack.append((i - 1, j - 1))
    else:
        stack.append((i - 1, j))
        stack.append((i, j - 1))
table_pairs = {(i, j) for i in range(1, m + 1) for j in range(1, n + 1)}
print(f"table pairs with 1<=i<={m}, 1<=j<={n}: {len(table_pairs)}")
print(f"pairs reached from ({m},{n}) with i,j>=1: {len(reached)}; subset of table: {reached <= table_pairs}")
print(f"matching pairs among reached: {sum(1 for i,j in reached if x[i-1]==y[j-1])}")
