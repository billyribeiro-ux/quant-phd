# Card FC1-c089: "Does the bound NP <= G hold when one consideration is negative? No. ..."
# Compute NP and G (Section 2 definitions) for two batches that each contain one negative consideration.
def stats(trades):
    x = {}
    for buyer, seller, c in trades:
        x[buyer] = x.get(buyer, 0) - c
        x[seller] = x.get(seller, 0) + c
    NP = sum(max(-v, 0) for v in x.values())
    G = sum(c for _, _, c in trades)
    return NP, G, NP <= G, sum(x.values())
print("single trade c=-100 (R2 example):", stats([("A", "B", -100)]))
print("two trades A buys from B: c=+100 and c=-50:", stats([("A", "B", 100), ("A", "B", -50)]))
print("two trades A buys from B: c=+100 and c=-10:", stats([("A", "B", 100), ("A", "B", -10)]))
