# Weather API Configuration Guide

## Obtener tu API Key de OpenWeather

1. Ve a https://openweathermap.org/api
2. Haz clic en "Sign Up" para crear una cuenta
3. Verifica tu email
4. Una vez logueado, ve a tu perfil > API keys
5. Copia tu API key (Free plan)

## Configuración en .env

```
OPENWEATHER_API_KEY=tu_api_key_aqui
```

Reemplaza `tu_api_key_aqui` con tu API key real.

## Iniciar la Aplicación

### Opción 1: Localmente

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python app.py
```

La API estará disponible en: **http://localhost:5000**

### Opción 2: Con Docker

```bash
# Construir la imagen
docker build -t weather-api .

# Ejecutar el contenedor
docker run -p 5000:5000 --env-file .env weather-api
```

## Pruebas

### Opción 1: Script Python

```bash
python test_api.py
```

Este script ejecutará pruebas automáticas de todos los endpoints.

### Opción 2: Script Bash

```bash
bash examples.sh
```

Este script muestra ejemplos de requests con curl.

### Opción 3: Manualmente con curl

```bash
# Health check
curl http://localhost:5000/health

# Clima por ciudad
curl http://localhost:5000/weather?city=Madrid

# Clima por coordenadas
curl http://localhost:5000/weather?lat=40.4168&lon=-3.7038

# Múltiples ciudades
curl -X POST http://localhost:5000/weather/multiple \
  -H "Content-Type: application/json" \
  -d '{"ciudades": ["Madrid", "Barcelona"]}'
```

## Solución de Problemas

### Error: "OPENWEATHER_API_KEY no está configurada en .env"

- Verifica que el archivo `.env` existe en el directorio raíz
- Asegúrate de que contiene: `OPENWEATHER_API_KEY=tu_api_key_aqui`
- Reemplaza con tu API key real

### Error: "API key inválida o expirada" (401)

- Verifica que copiaste correctamente tu API key
- Asegúrate de que tu cuenta de OpenWeatherMap está activa
- Intenta generar una nueva API key

### Error: "Ubicación no encontrada" (404)

- Verifica la ortografía del nombre de la ciudad
- Algunos nombres de ciudades pueden requerir más especificidad (ej: "New York, US")

### Error: "Tiempo de espera agotado (timeout)" (504)

- Intenta de nuevo, puede ser un problema de conectividad temporal
- Verifica tu conexión a internet
- Comprueba que openweathermap.org está accesible

## Límites de la API Gratuita

- **Solicitudes por minuto**: 60
- **Solicitudes diarias**: 1,000,000
- **Precisión de datos**: Similar a la versión de pago

Más información en: https://openweathermap.org/api

## Notas Importantes

- Las temperaturas se devuelven en **Kelvin**
- Para convertir a Celsius: °C = K - 273.15
- Para convertir a Fahrenheit: °F = (K - 273.15) × 9/5 + 32
