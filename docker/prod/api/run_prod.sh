#!/usr/bin/env bash

/usr/local/bin/gunicorn --config python:gunicorn_config wsgi
