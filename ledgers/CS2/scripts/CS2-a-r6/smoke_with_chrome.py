"""Run tools/page_smoke.py with the installed Google Chrome (channel="chrome").

The Playwright-managed chromium is not downloaded in this environment, so the
browser launch is pointed at the system Chrome. Arguments are passed through to
page_smoke.main unchanged. Usage: smoke_with_chrome.py --unit CS2 [--pages ...]
"""

import sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyB6-CS2-a"
sys.path.insert(0, f"{ROOT}/tools")
sys.argv = ["page_smoke.py", *sys.argv[1:]]

from playwright.sync_api._generated import BrowserType  # noqa: E402

_orig_launch = BrowserType.launch


def _launch(self, **kwargs):  # type: ignore[no-untyped-def]
    kwargs.setdefault("channel", "chrome")
    return _orig_launch(self, **kwargs)


BrowserType.launch = _launch  # type: ignore[method-assign]

import page_smoke  # noqa: E402

raise SystemExit(page_smoke.main())
