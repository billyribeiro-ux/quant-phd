#!/bin/sh
# Runs each lesson twin L07-L12 alone under python -I -W error from a scratch copy, then diffs stdout against the page's expected block.
# Usage: twins_alone.sh <checkout-root> <scratch-dir>
set -eu
ROOT="$1"; SCRATCH="$2"
mkdir -p "$SCRATCH"
for L in 07 08 09 10 11 12; do
  cp "$ROOT/tests/labs/M2/lab-M2-L$L-1.py" "$SCRATCH/lab-M2-L$L-1.py"
  ( cd "$SCRATCH" && /usr/bin/env -i PATH=/usr/bin:/bin "$ROOT/.venv/bin/python" -I -W error "lab-M2-L$L-1.py" > "out-L$L.txt" 2> "err-L$L.txt"; echo "L$L exit=$? stderr_bytes=$(wc -c < err-L$L.txt)" )
  sha=$(shasum -a 256 "$ROOT/tests/labs/M2/lab-M2-L$L-1.py" | cut -c1-16)
  echo "L$L twin_sha256_prefix=$sha stdout_lines=$(wc -l < "$SCRATCH/out-L$L.txt")"
done
