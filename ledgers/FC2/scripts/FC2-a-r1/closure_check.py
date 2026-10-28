"""FC2 slice a, round 1: prerequisite closure of FC2 as computed by the project's own coursekit."""
import sys
sys.path.insert(0, "/tmp/verifyC1-FC2-a/tools")
import coursekit

closure = coursekit.prerequisite_closure("FC2")
print("closure of FC2:", sorted(closure))
expected_named_on_hub = {"M1", "M2", "AC1", "E1", "P0.1"}
print("hub-named additions present:", expected_named_on_hub <= closure)
