# 🚀 Quick Start - Weather API

## 30 segundos para empezar

### 1. Configura tu API Key
```bash
# Copia el archivo de ejemplo
cp .env.example .env

# Edita .env e inserta tu API key de OpenWeatherMap
nano .env  # o usa tu editor favorito
```

### 2. Instala dependencias
```bash
pip install -r requirements.txt
```

### 3. Inicia la aplicación
```bash
python app.py
```

La API estará en: **http://localhost:5000**

---

## Primeros Requests

### Health Check
```bash
curl http://localhost:5000/health
```

### Obtener Clima de Madrid
```bash
curl "http://localhost:5000/weather?city=Madrid"
```

### Múltiples Ciudades
```bash
curl -X POST http://localhost:5000/weather/multiple \
  -H "Content-Type: application/json" \
  -d '{"ciudades": ["Madrid", "Barcelona", "Valencia"]}'
```

---

## Alternativas

### Con Docker
```bash
docker build -t weather-api .
docker run -p 5000:5000 --env-file .env weather-api
```

### Ejecutar pruebas
```bash
python test_api.py
```

---

## 📚 Documentación Completa
- [README.md](README.md) - Documentación detallada
- [CONFIG.md](CONFIG.md) - Guía de configuración
- [examples.sh](examples.sh) - Más ejemplos de requests

---

## ⚠️ Importante
- Necesitas una API key de [OpenWeatherMap](https://openweathermap.org/api)
- Las temperaturas se devuelven en **Kelvin** (para convertir a °C: K - 273.15)
