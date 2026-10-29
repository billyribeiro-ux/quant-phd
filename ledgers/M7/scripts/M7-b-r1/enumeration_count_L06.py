"""Count the active sets that the L06 twin's Part B actually examines (slice M7-b, round 1). Run with python -I."""

from itertools import product

N_ASSETS = 4
examined = 0
skipped = []
for mask in product((0, 1), repeat=N_ASSETS):
    free = [i for i in range(N_ASSETS) if not mask[i]]
    if not free:
        skipped.append(mask)
        continue
    examined += 1
print("masks generated:", 2**N_ASSETS, "examined:", examined, "skipped (all assets fixed at zero):", skipped)
