cd /tmp/verifyB3-M2-b
for n in 07 08 09 10 11 12; do
  .venv/bin/python -I ledgers/M2/scripts/M2-b-r1/embed_match.py course/modules/M/M2/L$n.html /tmp/m2-v/b3/L$n.out
done
