# Weather API - OpenWeather REST API

API REST en Flask que consume la OpenWeather API para obtener datos del clima en tiempo real.

## Características

- ✅ GET `/health` - Verifica el estado de la API
- ✅ GET `/` - Información de la API
- ✅ GET `/weather` - Obtiene clima por ciudad o coordenadas
- ✅ POST `/weather/multiple` - Obtiene clima para múltiples ciudades
- ✅ Validaciones completas de entrada
- ✅ Manejo de errores (401, 404, 429, timeout)
- ✅ Respuestas JSON limpias y estructuradas
- ✅ Configuración con variables de entorno (.env)

## Requisitos

- Python 3.8+
- pip
- Cuenta en [OpenWeatherMap](https://openweathermap.org/api) (API key gratuita)

## Instalación

1. **Clona o descarga el proyecto**
```bash
cd weather-api
```

2. **Crea un archivo `.env` a partir de `.env.example`**
```bash
cp .env.example .env
```

3. **Configura tu API key de OpenWeather**
Edita `.env` e inserta tu API key:
```
OPENWEATHER_API_KEY=tu_api_key_aqui
```

4. **Instala las dependencias**
```bash
pip install -r requirements.txt
```

## Uso

### Iniciar la aplicación
```bash
python app.py
```

La API estará disponible en `http://localhost:5000`

### Endpoints

#### 1. Health Check
```bash
curl http://localhost:5000/health
```

**Respuesta (200):**
```json
{
  "status": "healthy",
  "message": "API Weather está operativa",
  "version": "1.0.0"
}
```

---

#### 2. Información de la API
```bash
curl http://localhost:5000/
```

**Respuesta (200):**
```json
{
  "nombre": "Weather API",
  "versión": "1.0.0",
  "descripción": "API REST para consultar datos de clima usando OpenWeather API",
  "endpoints": { ... }
}
```

---

#### 3. Obtener clima por ciudad
```bash
curl "http://localhost:5000/weather?city=Madrid"
```

**Respuesta (200):**
```json
{
  "exito": true,
  "datos": {
    "ciudad": "Madrid",
    "país": "ES",
    "coordenadas": {
      "latitud": 40.4168,
      "longitud": -3.7038
    },
    "temperatura": {
      "actual": 293.15,
      "sensible": 292.15,
      "mínima": 291.15,
      "máxima": 295.15,
      "unidad": "Kelvin"
    },
    "clima": {
      "principal": "Clear",
      "descripción": "clear sky",
      "icono": "01d"
    },
    "humedad": "65%",
    "presión": "1013 hPa",
    "velocidad_viento": "3.5 m/s",
    "nubosidad": "10%",
    "visibilidad": "10000 m"
  }
}
```

---

#### 4. Obtener clima por coordenadas
```bash
curl "http://localhost:5000/weather?lat=40.4168&lon=-3.7038"
```

---

#### 5. Obtener clima para múltiples ciudades
```bash
curl -X POST http://localhost:5000/weather/multiple \
  -H "Content-Type: application/json" \
  -d '{
    "ciudades": ["Madrid", "Barcelona", "Valencia"]
  }'
```

**Respuesta (200):**
```json
{
  "total_solicitadas": 3,
  "exitosas": 3,
  "fallidas": 0,
  "resultados": [
    {
      "ciudad_solicitada": "Madrid",
      "exito": true,
      "datos": { ... }
    },
    { ... }
  ],
  "errores": null
}
```

---

### Manejo de Errores

#### 400 - Solicitud Inválida
```json
{
  "error": "Parámetros inválidos",
  "message": "Proporcione \"city\" o ambos \"lat\" y \"lon\"",
  "código": 400
}
```

#### 401 - API Key Inválida
```json
{
  "error": "API key inválida o expirada",
  "código": 401
}
```

#### 404 - Ubicación No Encontrada
```json
{
  "error": "Ubicación no encontrada",
  "código": 404
}
```

#### 429 - Límite de Solicitudes
```json
{
  "error": "Límite de solicitudes excedido",
  "código": 429
}
```

#### 504 - Timeout
```json
{
  "error": "Tiempo de espera agotado (timeout)",
  "código": 504
}
```

#### 503 - Servicio No Disponible
```json
{
  "error": "Servicio de OpenWeather no disponible",
  "código": 503
}
```

---

## Validaciones

### GET /weather
- **city**: Debe ser una cadena no vacía
- **lat/lon**: Números válidos dentro de rangos (-90 a 90 para latitud, -180 a 180 para longitud)
- Requerido: al menos uno de `city` o el par `lat/lon`

### POST /weather/multiple
- **ciudades**: Debe ser un array
- Máximo 50 ciudades por solicitud
- Cada ciudad debe ser una cadena no vacía
- No puede estar vacío

---

## Variables de Entorno

| Variable | Valor | Obligatoria |
|----------|-------|------------|
| `OPENWEATHER_API_KEY` | Tu API key de OpenWeather | Sí |

---

## Docker

Si quieres ejecutar la aplicación en Docker:

```bash
docker build -t weather-api .
docker run -p 5000:5000 --env-file .env weather-api
```

---

## Dependencias

- **Flask** (3.0.0): Framework web
- **requests** (2.31.0): Cliente HTTP para OpenWeather API
- **python-dotenv** (1.0.0): Carga variables de entorno desde .env

---

## Notas

- Todas las temperaturas se devuelven en **Kelvin** (escala de OpenWeather API)
- El timeout de solicitud está configurado en **10 segundos**
- La API está configurada en modo **debug** por defecto
- Respuestas JSON con soporte para caracteres acentuados

---

## Licencia

Este proyecto está bajo licencia MIT.

