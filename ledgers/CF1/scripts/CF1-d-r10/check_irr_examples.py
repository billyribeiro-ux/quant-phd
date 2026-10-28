import sys
sys.path.insert(0, sys.argv[1])
import capbudget as c
print('close pair missed:', c.irr_roots([-100.0, 220.1, -121.11]))
print('close pair both:', c.irr_roots([-100.0, 221.0, -122.1]))
print('-1,1e5:', c.irr_roots([-1.0, 1e5]), ' -2e4,1:', c.irr_roots([-2e4, 1.0]))
print('two-root:', c.irr_roots([-100.0, 230.0, -132.0]))
print('grid ratio', (1e4 / 1e-4) ** (1 / 4000), 10 ** (8/4000))
print('wide pair 0.1 0.2 at rate', c.irr_roots([-100.0, 230.0, -132.0]))
