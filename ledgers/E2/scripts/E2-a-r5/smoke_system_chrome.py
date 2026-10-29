"""Run tools/page_smoke.py unchanged, but launch the installed system Google Chrome (channel="chrome").

The verifier machine has no Playwright-managed chromium download; this wrapper only changes which
browser binary is launched. Usage: python smoke_system_chrome.py --unit E2 --pages index L01 L02 L03
"""

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "tools"))

import playwright.sync_api as psa  # noqa: E402

_orig_launch = psa.BrowserType.launch


def _launch(self, *args, **kwargs):  # type: ignore[no-untyped-def]
    kwargs.setdefault("channel", "chrome")
    return _orig_launch(self, *args, **kwargs)


psa.BrowserType.launch = _launch  # type: ignore[method-assign]

import page_smoke  # noqa: E402

sys.exit(page_smoke.main())
