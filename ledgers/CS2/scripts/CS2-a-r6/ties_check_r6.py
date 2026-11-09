import random
rng = random.Random(20261028 + 1)
tie_pairs = 0
for _ in range(2000):
    a = rng.randint(1, 8); b = rng.randint(1, 8)
    L = sorted(rng.randrange(20) for _ in range(a))
    R = sorted(rng.randrange(20) for _ in range(b))
    if set(L) & set(R):
        tie_pairs += 1
print("pairs with a tie between left and right keys:", tie_pairs, "of 2000")
