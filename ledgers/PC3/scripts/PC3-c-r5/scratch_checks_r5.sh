#!/bin/bash
# Round-5 scratch checks for slice c, re-runnable. Copies the checkout's grader files into /tmp; writes nothing into the repo.
ROOT=/Users/billyribeiro/.fanout/wt/verifyE5-PC3-c
G=$ROOT/course/modules/PC/PC3/grader
PY=$ROOT/.venv/bin/python
W=/tmp/pc3c-r5-ws
rm -rf $W && mkdir -p $W/ref $W/starter $W/v21 $W/v22 $W/log
cp $G/engine.py $G/instance.py $G/test_project.py $W/ref/ && cp $G/reference.py $W/ref/market_maker.py
cp $G/engine.py $G/instance.py $G/test_project.py $G/starter.py $W/starter/ && cp $G/starter.py $W/starter/market_maker.py
for d in v21 v22; do cp $G/engine.py $G/instance.py $G/test_project.py $W/$d/; done
cp $ROOT/ledgers/PC3/mutants/v21_replay_scales_each_fill_by_quoted_size.py $W/v21/market_maker.py
cp $ROOT/ledgers/PC3/mutants/v22_replay_refuses_a_zero_fill_price.py $W/v22/market_maker.py
echo "== collect-only, reference workspace"
(cd $W/ref && $PY -I -m pytest --collect-only -q -p no:cacheprovider test_project.py | tail -1)
echo "== page command: log writer (no -I, as printed on the page), reference"
(cd $W/ref && $PY -c "import json, engine, market_maker; print(json.dumps(engine.play(market_maker.quote, 12345)))" > game_log.json; echo "exit $?"; $PY -c "import json; d=json.load(open('game_log.json')); print(sorted(d), len(d['turns']))")
echo "== page pytest flags, reference, seeds 0 39893 39901 7919"
for s in 0 39893 39901 7919; do (cd $W/ref && QF_SEED=$s $PY -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1 | sed "s/^/seed $s: /"); done
echo "== starter under the suite (must fail)"
(cd $W/starter && QF_SEED=0 $PY -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1)
echo "== survivors v21 and v22 under the page flags, seed 0"
for d in v21 v22; do (cd $W/$d && QF_SEED=0 $PY -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1 | sed "s/^/$d: /"); done
echo "== mypy --strict on grader files with reference as market_maker"
(cd $W/ref && $ROOT/.venv/bin/mypy --strict --python-version 3.14 engine.py instance.py test_project.py market_maker.py 2>&1 | tail -1)
echo "== print( in grader sources"
grep -c "print(" $G/*.py
echo "== grep atlas in project.html"
grep -c -i "atlas" $ROOT/course/modules/PC/PC3/project.html
