#!/usr/bin/env bash

HERE=$(pwd)
export PYTHONPATH="${HERE}/src"
pipenv run uvicorn project.asgi:application
