"""Verifier check (CS2-d round 2): card CS2-c035 ratio ranges from the printed L03 lab output (tests/labs/CS2/lab-CS2-L03-1.py).

Sizes N = 16..4096 (doubling). The printed 'N doubled from the row above' ratios are at rows N = 32..4096.
The card asks for the doublings from N = 64 to N = 4096, i.e. the rows N = 128..4096.
"""
sizes = [16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
sorted_moves = [107 * 0 + 98, 284, 1002, 4514, 17663, 65561, 269578, 1086043, 4378444]
heap_moves = [361, 929, 2209, 4933, 10623, 21095, 42401, 87863, 181761]
for name, moves in [("sorted-list moves", sorted_moves), ("heap moves", heap_moves)]:
    ratios = {sizes[i]: moves[i] / moves[i - 1] for i in range(1, len(sizes))}
    in_range = {n: round(r, 4) for n, r in ratios.items() if 128 <= n <= 4096}
    print(name, "ratio at row N:", {n: round(r, 4) for n, r in ratios.items()})
    print(name, "doublings 64->4096 (rows 128..4096):", in_range, "min", min(in_range.values()), "max", max(in_range.values()))
