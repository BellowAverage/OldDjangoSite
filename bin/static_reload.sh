#!/bin/bash

echo "rm -rf static/" && rm -rf static/

echo "python3 manage.py collectstatic" && python3 manage.py collectstatic

echo "uwsgi --reload uwsgi.pid" && uwsgi --reload uwsgi.pid

if [ $? -ne 0 ]; then
    echo "Execution Failed."
        exit 1
        fi
        
        echo "All Commands Executed Successfully."
