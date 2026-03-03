#!/usr/bin/env bash
set -e

pip install -r requirements.txt

flask db upgrade
