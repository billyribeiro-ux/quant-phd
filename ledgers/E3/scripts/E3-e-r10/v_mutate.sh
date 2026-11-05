#!/bin/bash
# Verifier r10: tools/mutate_graders.py over every E3 mutant, seeds 0-9 (unbuffered), exit code recorded.
cd /Users/billyribeiro/.fanout/wt/verifyD10-E3-e || exit 1
.venv/bin/python -u tools/mutate_graders.py --unit E3 --seeds 0-9
echo "exit=$?"
