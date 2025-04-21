#!/bin/bash

echo "🚀 Iniciando a aplicação com Docker Compose..."
set -a
source .env
set +a
docker-compose up --build