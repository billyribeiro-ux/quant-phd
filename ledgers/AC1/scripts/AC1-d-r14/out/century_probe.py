import sys
sys.path.insert(0, ".")
import statements as sol
led = sol.post([{"date": "2100-01-05", "lines": [{"account": "cash", "debit": 5, "credit": 0}, {"account": "common_stock", "debit": 0, "credit": 5}]}])
for end in ("2100-02-28", "2100-02-29"):
    try:
        sol.balance_sheet(led, end)
        print(end, "accepted")
    except ValueError as e:
        print(end, "ValueError:", e)
