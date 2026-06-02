#!/bin/bash

# Script con ejemplos de requests a la Weather API
# Ejecuta: bash examples.sh

BASE_URL="http://localhost:5000"

echo "================================"
echo "Weather API - Ejemplos de Uso"
echo "================================"

# 1. Health Check
echo -e "\n1. Health Check"
echo "GET /health"
curl -s "$BASE_URL/health" | jq . || echo "Error en la solicitud"

# 2. Información de la API
echo -e "\n\n2. Información de la API"
echo "GET /"
curl -s "$BASE_URL/" | jq . || echo "Error en la solicitud"

# 3. Clima por ciudad
echo -e "\n\n3. Clima por Ciudad"
echo "GET /weather?city=Madrid"
curl -s "$BASE_URL/weather?city=Madrid" | jq . || echo "Error en la solicitud"

# 4. Clima por coordenadas
echo -e "\n\n4. Clima por Coordenadas"
echo "GET /weather?lat=40.4168&lon=-3.7038"
curl -s "$BASE_URL/weather?lat=40.4168&lon=-3.7038" | jq . || echo "Error en la solicitud"

# 5. Clima para múltiples ciudades
echo -e "\n\n5. Clima para Múltiples Ciudades"
echo "POST /weather/multiple"
curl -s -X POST "$BASE_URL/weather/multiple" \
  -H "Content-Type: application/json" \
  -d '{
    "ciudades": ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao"]
  }' | jq . || echo "Error en la solicitud"

# 6. Error: Parámetros inválidos
echo -e "\n\n6. Error: Parámetros Inválidos"
echo "GET /weather (sin parámetros)"
curl -s "$BASE_URL/weather" | jq . || echo "Error en la solicitud"

# 7. Error: Ubicación no encontrada
echo -e "\n\n7. Error: Ubicación No Encontrada"
echo "GET /weather?city=CIUDADINVALIDAXYZ"
curl -s "$BASE_URL/weather?city=CIUDADINVALIDAXYZ" | jq . || echo "Error en la solicitud"

# 8. Error: Ruta no encontrada
echo -e "\n\n8. Error: Ruta No Encontrada"
echo "GET /endpoint-inexistente"
curl -s "$BASE_URL/endpoint-inexistente" | jq . || echo "Error en la solicitud"

echo -e "\n\n================================"
echo "Ejemplos completados"
echo "================================\n"
