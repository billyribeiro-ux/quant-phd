"""Reproduce the browser's Collector (py-worker.js) and print the message it would show for each failing test."""
import sys
import pytest

class Collector:
    def __init__(self):
        self.results = []
    def pytest_runtest_logreport(self, report):
        if report.when == "call" or report.outcome != "passed":
            message = ""
            if report.failed:
                crash = getattr(report.longrepr, "reprcrash", None)
                message = crash.message if crash is not None else str(report.longrepr)
            self.results.append((report.nodeid.split("::")[-1], report.outcome, message))

c = Collector()
code = pytest.main(["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"], plugins=[c])
for name, outcome, msg in c.results:
    if outcome == "failed":
        print(f"{name} | {msg!r}")
