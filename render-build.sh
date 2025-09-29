#!/usr/bin/env bash
pip install -r requirements.txt

if [ ! -d "migrations" ]; then
  alembic init migrations
fi

alembic revision --autogenerate -m "initial"
alembic upgrade head