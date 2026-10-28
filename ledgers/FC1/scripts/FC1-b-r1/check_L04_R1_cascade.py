"""Verifier script: runs the L04 twin Book on problem R1 (cascade of two stops) and on the lesson's Example 1.4."""
import importlib.util
import sys

spec = importlib.util.spec_from_file_location("twin_l04", sys.argv[1])
twin = importlib.util.module_from_spec(spec)
sys.modules["twin_l04"] = twin
spec.loader.exec_module(twin)  # the module-level main() prints the lab output; that output is checked separately
Order, Book = twin.Order, twin.Book
b = Book()
b.match(Order(0, -1, "limit", 100, price=990))
b.match(Order(1, 1, "limit", 100, price=985))
b.match(Order(2, 1, "limit", 100, price=980))
b.pending.append(Order(3, -1, "stop", 100, stop=990))
b.pending.append(Order(4, -1, "stop", 100, stop=985))
b.activate()
b.match(Order(5, 1, "market", 100))
n = b.activate()
print("R1 activations", n, "fills", b.fills, "pending", len(b.pending))
