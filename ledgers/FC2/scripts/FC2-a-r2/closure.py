import sys
sys.path.insert(0, "/tmp/verifyC2-FC2-a/tools")
import coursekit
c = coursekit.prerequisite_closure("FC2")
print(sorted(c))
print({"M1","M2","AC1","E1","P0.1"} <= c)
