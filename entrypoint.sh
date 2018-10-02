#!/bin sh

cd /kaknas
export PYTHONPATH=/app/kaknas

uwsgi --http 0.0.0.0:5000 --module kaknas.app:app -L --master --enable-threads --threads 8
