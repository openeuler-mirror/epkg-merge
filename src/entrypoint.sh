#!/bin/sh

gunicorn --config ./conf/gunicorn_conf.py run:app
