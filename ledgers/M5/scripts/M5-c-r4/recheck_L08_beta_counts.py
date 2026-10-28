import importlib.util, io, contextlib, re
spec = importlib.util.spec_from_file_location("L08", "/tmp/verifyB4-M5-c/tests/labs/M5/lab-M5-L08-1.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
import inspect
src = open("/tmp/verifyB4-M5-c/tests/labs/M5/lab-M5-L08-1.py").read()
for b in (0.5, 0.9, 0.95):
    m.BETA = b
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            m.part_a()
        except Exception as e:
            print("EXC", e)
    print(b, [l for l in buf.getvalue().splitlines() if "iterations" in l])
