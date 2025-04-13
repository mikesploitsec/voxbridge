@echo off
echo Rebuilding docker app

docker compose down
docker compose build
docker compose up -d

echo Done.
