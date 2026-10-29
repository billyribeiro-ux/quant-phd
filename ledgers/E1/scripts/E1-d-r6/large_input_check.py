import sys, importlib.util
sys.path.insert(0, sys.argv[1])
spec = importlib.util.spec_from_file_location("m", sys.argv[2]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print(m.outcome("cournot", 15000000000000002, 1, 1)["volume_trades"], "expected 10000000000000001")
