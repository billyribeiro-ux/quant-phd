"""Witness calls for the round-7 survivors: each prints whether post accepts the entry (ValueError means rejected)."""
import importlib.util
import sys

def load(path):
    spec = importlib.util.spec_from_file_location("cand", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def outcome(fn):
    try:
        fn()
        return "accepted"
    except ValueError as error:
        return f"rejected ValueError: {error}"
    except Exception as error:  # noqa: BLE001 - witness script, shows any other exception
        return f"other {type(error).__name__}: {error}"

path, label = sys.argv[1], sys.argv[2]
m = load(path)
cases = {
    "account ' cash '": [{"date": "2024-01-02", "lines": [{"account": " cash ", "debit": 5, "credit": 0}, {"account": "common_stock", "debit": 0, "credit": 5}]}],
    "credit 5.0": [{"date": "2024-01-02", "lines": [{"account": "cash", "debit": 5, "credit": 0}, {"account": "common_stock", "debit": 0, "credit": 5.0}]}],
    "date 2024-W01-1": [{"date": "2024-W01-1", "lines": [{"account": "cash", "debit": 5, "credit": 0}, {"account": "common_stock", "debit": 0, "credit": 5}]}],
}
for name, txns in cases.items():
    print(label, name, "->", outcome(lambda t=txns: m.post(t)))
