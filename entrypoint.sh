#! /usr/bin/env sh
sleep 2
python3 run_db_init.py

gunicorn sql_app.main:app -b 0.0.0.0:80 -k uvicorn.workers.UvicornWorker --workers 4
