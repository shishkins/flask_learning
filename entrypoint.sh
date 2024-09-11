#!/usr/bin/env bash
gunicorn -b 0.0.0.0:8080 --preload --workers 8 --threads 4 -t 600 --max-requests 500 --max-requests-jitter 100 -R manage:app