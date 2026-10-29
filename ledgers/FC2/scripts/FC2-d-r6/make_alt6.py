# Round 6 FC2-d: builds alt6, an integer-only cross-multiplied alternative derived from the reference.
# Each replaced block is asserted to occur exactly once, so the alternative cannot silently drift from the reference.
import sys

src = open(sys.argv[1], encoding="utf-8").read()


def swap(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, old[:60]
    return text.replace(old, new)


s = src
s = swap(
    s,
    "    gap = Fraction(call_cents) - Fraction(put_cents) - (Fraction(spot_cents) - Fraction(strike_cents * df_ppm, PPM))\n"
    "    return _half_up(gap)\n",
    "    num = (call_cents - put_cents - spot_cents) * PPM + strike_cents * df_ppm\n"
    "    return (2 * num + PPM) // (2 * PPM)\n",
)
s = swap(
    s,
    "        gap = Fraction(calls[k]) - Fraction(puts[k]) - (Fraction(spot) - Fraction(strike * df_ppm, PPM))\n"
    "        gross = _half_up(abs(gap))\n",
    "        num = (calls[k] - puts[k] - spot) * PPM + strike * df_ppm\n"
    "        rounded = (2 * num + PPM) // (2 * PPM)\n"
    "        gross = (2 * abs(num) + PPM) // (2 * PPM)\n",
)
s = swap(s, "_explain_parity(_half_up(gap), net, fee, spread)", "_explain_parity(rounded, net, fee, spread)")
s = swap(
    s,
    "    return [j for j in range(1, len(strikes_cents) - 1) if _second_difference(strikes_cents, calls_cents, j) < 0]\n",
    "    out = []\n"
    "    for j in range(1, len(strikes_cents) - 1):\n"
    "        low, mid, high = strikes_cents[j - 1], strikes_cents[j], strikes_cents[j + 1]\n"
    "        # call above chord <=> calls[j]*(high-low) > calls[j-1]*(high-mid) + calls[j+1]*(mid-low)\n"
    "        if calls_cents[j] * (high - low) > calls_cents[j - 1] * (high - mid) + calls_cents[j + 1] * (mid - low):\n"
    "            out.append(j)\n"
    "    return out\n",
)
s = swap(
    s,
    "        gross = _half_up(-_second_difference(strikes, calls, j))\n",
    "        low, mid, high = strikes[j - 1], strikes[j], strikes[j + 1]\n"
    "        big_n = calls[j] * (high - low) - calls[j - 1] * (high - mid) - calls[j + 1] * (mid - low)\n"
    "        big_d = high - low\n"
    "        gross = (2 * big_n + big_d) // (2 * big_d)\n",
)
sys.stdout.write(
    '"""Integer-only cross-multiplied alternative: parity and convexity exact in integers, no Fraction."""\n' + s
)
