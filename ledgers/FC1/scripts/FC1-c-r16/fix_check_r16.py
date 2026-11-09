"""Round 16, FC1-c: run the two proposed accepted-input tests (values above 2**31) against the reference solution in a scratch dir."""
import shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD16-FC1-c")
work = Path(tempfile.mkdtemp(prefix="fc1c16-fix-"))
shutil.copy(ROOT / "course/modules/FC/FC1/grader/reference.py", work / "instruments.py")
(work / "test_fix.py").write_text(
    "import instruments as sol\n\n"
    "def test_trade_price_above_int32_is_accepted() -> None:\n"
    "    assert sol.CashTrade(10, 2**31, 1, 2).events() == [(2, -(10 * 2**31))]\n\n"
    "def test_bond_coupon_above_int32_bps_is_accepted() -> None:\n"
    "    assert sol.Bond(10_000, 2**31, 1).events() == [(1, 2**31 + 10_000)]\n", encoding="utf-8")
r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_fix.py"],
                   cwd=work, capture_output=True, text=True)
print(r.stdout.strip().splitlines()[-1], "rc", r.returncode)
shutil.rmtree(work, ignore_errors=True)
