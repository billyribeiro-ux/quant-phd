# Proposed additional test (not applied to the repository): ad_derivative must be exact for x^3 at 1e5,
# which a central difference with step 1e-6 cannot meet to 1e-9 relative (round-off and truncation of the stencil).
import math
import sensitivity_engine as sol


def test_ad_derivative_is_exact_for_a_large_argument() -> None:
    value = sol.ad_derivative(lambda x: x * x * x, 1e5)
    assert math.isfinite(value) and abs(value - 3e10) <= 1e-9 * max(1.0, 3e10), "forward-mode AD must return 3e10"
