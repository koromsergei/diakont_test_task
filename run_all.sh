#!/bin/bash
. venv/bin/activate

python -m M1.main &

sleep 2

python -m M2.main &
python -m M3.main &

wait