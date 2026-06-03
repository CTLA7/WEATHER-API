import os
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
from functools import wraps
from typing import Dict, Any, Optional, Tuple

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Configuración
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
OPENWEATHER_BASE_URL = 'https://api.openweathermap.org/data/2.5'
REQUEST_TIMEOUT = 10


def validate_api_key(f):
    """Decorador para validar la API key"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not OPENWEATHER_API_KEY:
            return jsonify({
                'error': 'API key no configurada',
                'code': 'MISSING_API_KEY'
            }), 500
        return f(*args, **kwargs)
    return decorated_function


def handle_weather_request(url: str, params: Dict[str, Any]) -> Tuple[Optional[Dict], int, str]:
    """
    Realiza una solicitud a OpenWeather API y maneja errores.
    Retorna: (datos, status_code, error_message)
    """
    try:
        response = requests.get(
            url,
            params=params,
            timeout=REQUEST_TIMEOUT
        )
        
        # Manejo de códigos de estado HTTP
        if response.status_code == 401:
            return None, 401, 'API key inválida o expirada'
        elif response.status_code == 404:
            return None, 404, 'Ubicación no encontrada'
        elif response.status_code == 429:
            return None, 429, 'Límite de solicitudes excedido'
        elif response.status_code >= 500:
            return None, 503, 'Servicio de OpenWeather no disponible'
        
        response.raise_for_status()
        return response.json(), 200, ''
        
    except requests.exceptions.Timeout:
        return None, 504, 'Tiempo de espera agotado (timeout)'
    except requests.exceptions.ConnectionError:
        return None, 503, 'Error de conexión con OpenWeather API'
    except requests.exceptions.RequestException as e:
        return None, 500, f'Error en la solicitud: {str(e)}'
    except ValueError:
        return None, 500, 'Respuesta JSON inválida de OpenWeather API'


def validate_coordinates(lat: Any, lon: Any) -> Tuple[bool, str]:
    """Valida coordenadas de latitud y longitud"""
    try:
        lat = float(lat)
        lon = float(lon)
        if not (-90 <= lat <= 90):
            return False, 'Latitud debe estar entre -90 y 90'
        if not (-180 <= lon <= 180):
            return False, 'Longitud debe estar entre -180 y 180'
        return True, ''
    except (ValueError, TypeError):
        return False, 'Coordenadas deben ser números válidos'


def format_weather_response(data: Dict) -> Dict[str, Any]:
    """Formatea la respuesta de OpenWeather API a un formato limpio"""
    try:
        return {
            'ciudad': data.get('name', 'N/A'),
            'país': data.get('sys', {}).get('country', 'N/A'),
            'coordenadas': {
                'latitud': data.get('coord', {}).get('lat'),
                'longitud': data.get('coord', {}).get('lon')
            },
            'temperatura': {
                'actual': data.get('main', {}).get('temp'),
                'sensible': data.get('main', {}).get('feels_like'),
                'mínima': data.get('main', {}).get('temp_min'),
                'máxima': data.get('main', {}).get('temp_max'),
                'unidad': 'Kelvin'
            },
            'clima': {
                'principal': data.get('weather', [{}])[0].get('main', 'N/A'),
                'descripción': data.get('weather', [{}])[0].get('description', 'N/A'),
                'icono': data.get('weather', [{}])[0].get('icon', 'N/A')
            },
            'humedad': f"{data.get('main', {}).get('humidity', 'N/A')}%",
            'presión': f"{data.get('main', {}).get('pressure', 'N/A')} hPa",
            'velocidad_viento': f"{data.get('wind', {}).get('speed', 'N/A')} m/s",
            'nubosidad': f"{data.get('clouds', {}).get('all', 'N/A')}%",
            'visibilidad': f"{data.get('visibility', 'N/A')} m"
        }
    except Exception as e:
        return None


@app.route('/health', methods=['GET'])
def health():
    """Endpoint de salud - verifica que la API esté operativa"""
    return jsonify({
        'status': 'healthy',
        'message': 'API Weather está operativa',
        'version': '1.0.0'
    }), 200


@app.route('/', methods=['GET'])
def index():
    """Endpoint raíz - proporciona información de la API"""
    return jsonify({
        'nombre': 'Weather API',
        'versión': '1.0.0',
        'descripción': 'API REST para consultar datos de clima usando OpenWeather API',
        'endpoints': {
            'GET /health': 'Verifica el estado de la API',
            'GET /': 'Información de la API',
            'GET /weather': 'Obtiene clima por ciudad o coordenadas (parámetros: city o lat/lon)',
            'POST /weather/multiple': 'Obtiene clima para múltiples ciudades'
        }
    }), 200


@app.route('/weather', methods=['GET'])
@validate_api_key
def get_weather():
    """
    Obtiene información del clima
    Parámetros:
    - city: nombre de la ciudad
    - lat/lon: coordenadas (latitud y longitud)
    """
    city = request.args.get('city')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    # Validar que se proporcione al menos una forma de ubicación
    if not city and not (lat and lon):
        return jsonify({
            'error': 'Parámetros inválidos',
            'message': 'Proporcione "city" o ambos "lat" y "lon"',
            'código': 400
        }), 400
    
    # Si se proporciona ciudad
    if city:
        if not isinstance(city, str) or len(city.strip()) == 0:
            return jsonify({
                'error': 'Ciudad inválida',
                'message': 'La ciudad debe ser una cadena no vacía',
                'código': 400
            }), 400
        
        params = {
            'q': city,
            'appid': OPENWEATHER_API_KEY
        }
        url = f'{OPENWEATHER_BASE_URL}/weather'
    
    # Si se proporcionan coordenadas
    else:
        is_valid, error_msg = validate_coordinates(lat, lon)
        if not is_valid:
            return jsonify({
                'error': 'Coordenadas inválidas',
                'message': error_msg,
                'código': 400
            }), 400
        
        params = {
            'lat': lat,
            'lon': lon,
            'appid': OPENWEATHER_API_KEY
        }
        url = f'{OPENWEATHER_BASE_URL}/weather'
    
    # Realizar solicitud
    data, status_code, error_msg = handle_weather_request(url, params)
    
    if status_code != 200:
        return jsonify({
            'error': error_msg,
            'código': status_code
        }), status_code
    
    # Formatear respuesta
    formatted_data = format_weather_response(data)
    if formatted_data is None:
        return jsonify({
            'error': 'Error al procesar datos del clima',
            'código': 500
        }), 500
    
    return jsonify({
        'exito': True,
        'datos': formatted_data
    }), 200


@app.route('/weather/multiple', methods=['POST'])
@validate_api_key
def get_weather_multiple():
    """
    Obtiene información del clima para múltiples ciudades
    Body JSON requerido:
    {
        "ciudades": ["Madrid", "Barcelona", "Valencia"]
    }
    """
    # Validar que sea JSON
    if not request.is_json:
        return jsonify({
            'error': 'Formato inválido',
            'message': 'El cuerpo debe ser JSON',
            'código': 400
        }), 400
    
    data = request.get_json()
    
    # Validar que contenga la clave "ciudades"
    if 'ciudades' not in data:
        return jsonify({
            'error': 'Parámetro faltante',
            'message': 'El JSON debe contener la clave "ciudades"',
            'código': 400
        }), 400
    
    ciudades = data.get('ciudades')
    
    # Validar que sea una lista
    if not isinstance(ciudades, list):
        return jsonify({
            'error': 'Formato inválido',
            'message': '"ciudades" debe ser una lista',
            'código': 400
        }), 400
    
    # Validar que no esté vacía
    if len(ciudades) == 0:
        return jsonify({
            'error': 'Lista vacía',
            'message': '"ciudades" no puede estar vacía',
            'código': 400
        }), 400
    
    # Validar máximo de ciudades (para evitar uso excesivo de API)
    if len(ciudades) > 50:
        return jsonify({
            'error': 'Límite excedido',
            'message': 'Máximo 50 ciudades por solicitud',
            'código': 400
        }), 400
    
    # Validar que cada ciudad sea una cadena válida
    for i, city in enumerate(ciudades):
        if not isinstance(city, str) or len(city.strip()) == 0:
            return jsonify({
                'error': 'Ciudad inválida',
                'message': f'La ciudad en índice {i} debe ser una cadena no vacía',
                'código': 400
            }), 400
    
    # Obtener clima para cada ciudad
    resultados = []
    errores = []
    
    for ciudad in ciudades:
        params = {
            'q': ciudad,
            'appid': OPENWEATHER_API_KEY
        }
        url = f'{OPENWEATHER_BASE_URL}/weather'
        
        weather_data, status_code, error_msg = handle_weather_request(url, params)
        
        if status_code == 200:
            formatted_data = format_weather_response(weather_data)
            if formatted_data:
                resultados.append({
                    'ciudad_solicitada': ciudad,
                    'exito': True,
                    'datos': formatted_data
                })
            else:
                errores.append({
                    'ciudad': ciudad,
                    'error': 'Error al procesar datos'
                })
        else:
            errores.append({
                'ciudad': ciudad,
                'error': error_msg,
                'código': status_code
            })
    
    return jsonify({
        'total_solicitadas': len(ciudades),
        'exitosas': len(resultados),
        'fallidas': len(errores),
        'resultados': resultados,
        'errores': errores if errores else None
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Manejo de rutas no encontradas"""
    return jsonify({
        'error': 'Ruta no encontrada',
        'message': f'El endpoint {request.path} no existe',
        'código': 404
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Manejo de método HTTP no permitido"""
    return jsonify({
        'error': 'Método no permitido',
        'message': f'El método {request.method} no es permitido para {request.path}',
        'código': 405
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Manejo de errores internos"""
    return jsonify({
        'error': 'Error interno del servidor',
        'código': 500
    }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
