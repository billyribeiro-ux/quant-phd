"""Round-11 verifier d: does math.ceil(0.99 * n) (float) equal (99 n + 99) // 100 (exact integers) for every n in 1..2,000,000?"""

import math

bad = [n for n in range(1, 2_000_001) if math.ceil(0.99 * n) != (99 * n + 99) // 100]
print("n in 1..2000000 where float ceiling differs from exact index:", "none" if not bad else bad[:10])
