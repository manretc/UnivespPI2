#!/usr/bin/env bash
pip install -r requirements.txt
alembic init migrations
alembic revision --autogenerate -m "initial"
alembic upgrade head