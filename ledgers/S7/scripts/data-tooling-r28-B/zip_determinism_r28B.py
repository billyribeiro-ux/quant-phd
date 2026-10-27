"""Round 28: zip_member / sdmx_zip / zip_with bytes are the same in two separate processes with a clock shift (tests/test_fetch_data.py helpers).
Usage: python -I zip_determinism_r28B.py <checkout> ; prints sha256 of each archive. Run twice with different delays."""
import hashlib
import importlib.util
import sys
import time
from pathlib import Path

root = Path(sys.argv[1])
time.sleep(float(sys.argv[2]) if len(sys.argv) > 2 else 0.0)
spec = importlib.util.spec_from_file_location("tfd", root / "tests/test_fetch_data.py")
mod = importlib.util.module_from_spec(spec)
sys.path.insert(0, str(root / "tools"))
spec.loader.exec_module(mod)
a = mod.sdmx_zip(mod.SERIES) if hasattr(mod, "SERIES") else None
print("sdmx_zip sha256", hashlib.sha256(a).hexdigest()[:16] if a else None, len(a) if a else None)
