"""Rung 2 completed solution: the payments of a k-unit auction in both formats, in integer cents."""


def payments(format_name: str, bids: list[int], units: int) -> list[int]:
    """Amount each bidder pays, in cents: 0 for a loser; a winner pays the uniform price or its own bid."""
    n = len(bids)
    ranked = sorted(range(n), key=lambda i: (-bids[i], i))
    winners = set(ranked[:units])
    clearing = bids[ranked[units]]
    paid = []
    for i in range(n):
        if i not in winners:
            paid.append(0)
        elif format_name == "uniform":
            paid.append(clearing)
        else:
            paid.append(bids[i])
    return paid


def main() -> None:
    bids = [5200, 4800, 6100, 3900]
    units = 2
    uniform = payments("uniform", bids, units)
    discriminatory = payments("discriminatory", bids, units)
    print("uniform payments (cents):", uniform, "| revenue:", sum(uniform))
    print("discriminatory payments (cents):", discriminatory, "| revenue:", sum(discriminatory))
    print("revenue gap (cents):", sum(discriminatory) - sum(uniform))


main()
