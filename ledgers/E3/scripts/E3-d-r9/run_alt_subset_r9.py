import sys
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyC9-E3-d/ledgers/E3/scripts")
import run_alternatives as ra
name = sys.argv.pop(1)
ra.ALTERNATIVES = {name: ra.ALTERNATIVES[name]}
sys.exit(ra.main())
