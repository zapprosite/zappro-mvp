#!/usr/bin/env bash
set -e
echo "Smoke: containers sobem e endpoints respondem"
docker compose up -d
sleep 3
curl -fsS http://localhost:8080/ready >/dev/null
