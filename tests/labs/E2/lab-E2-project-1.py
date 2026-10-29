"""Rung 1 worked example: payments and revenue of a two-unit, four-bidder auction, in integer cents.

SIMULATED: the four bids are typed in for this example. They are illustrative, not generated and not data.
"""


def main() -> None:
    bids = [5200, 4800, 6100, 3900]  # cents; bidder i bids bids[i], for i = 0, 1, 2, 3
    units = 2  # the auction sells two identical units, so 1 <= units < n with n = 4
    n = len(bids)
    # Step 1. Rank the bidders from the highest bid to the lowest. A tie goes to the lower index.
    ranked = sorted(range(n), key=lambda i: (-bids[i], i))
    print("ranking (bidder indices, highest bid first):", ranked)
    # Step 2. The winners are the first `units` bidders in the ranking. Each winner receives one unit.
    winners = sorted(ranked[:units])
    print("winners (bidder indices):", winners)
    # Step 3. Uniform price: every winner pays the (units + 1)-th highest bid, the highest losing bid.
    # Counting from 0, that bid is bids[ranked[units]]: ranked[units] is the index of the bidder who holds it.
    uniform_price = bids[ranked[units]]
    uniform = [uniform_price if i in winners else 0 for i in range(n)]
    # Step 4. Discriminatory: each winner pays its own bid. A loser pays nothing in either format.
    discriminatory = [bids[i] if i in winners else 0 for i in range(n)]
    # Step 5. Revenue is the sum of what the bidders pay, in each format.
    print("uniform price (cents):", uniform_price)
    print("uniform payments (cents):", uniform)
    print("uniform revenue (cents):", sum(uniform))
    print("discriminatory payments (cents):", discriminatory)
    print("discriminatory revenue (cents):", sum(discriminatory))
    gap = sum(discriminatory) - sum(uniform)
    print("discriminatory minus uniform (cents):", gap)
    print(f"gap as a share of the uniform revenue: {100 * gap / sum(uniform):.1f} %")


main()
