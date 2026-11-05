#!/bin/bash
# Verifier r10: collect-only count of the E3 suite, run in a scratch dir holding the reference as elicit.py.
G=/Users/billyribeiro/.fanout/wt/verifyD10-E3-e/course/modules/E/E3/grader
rm -rf /tmp/e3e_r10/collect && mkdir -p /tmp/e3e_r10/collect && cp $G/reference.py /tmp/e3e_r10/collect/elicit.py && cp $G/instance.py $G/test_project.py /tmp/e3e_r10/collect/
cd /tmp/e3e_r10/collect && /Users/billyribeiro/.fanout/wt/verifyD10-E3-e/.venv/bin/python -m pytest --collect-only -q -p no:cacheprovider test_project.py
