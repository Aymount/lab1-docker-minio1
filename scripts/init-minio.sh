#!/usr/bin/env bash
set -euo pipefail

# Wrapper: run MinIO init inside the app container (requires docker-compose up -d)
echo "Initialisation du bucket MinIO via le conteneur 'app'..."
docker-compose run --rm app python scripts/init-minio.py
