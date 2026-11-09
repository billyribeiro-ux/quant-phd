#!/bin/sh
# Scan the reference over seeds 0-399 with 8 workers. Run from the checkout root.
D=ledgers/E3/scripts/E3-d-r15/verifier
R=$(pwd)
seq 0 399 | xargs -P 8 -I{} sh $D/suite_one.sh $R $R/course/modules/E/E3/grader/reference.py {} > $D/reference_scan_0_399.raw 2>&1
sort -t' ' -k1.6 -n $D/reference_scan_0_399.raw > $D/reference_scan_0_399.txt
echo DONE > $D/reference_scan.done
