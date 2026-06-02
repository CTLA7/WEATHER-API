#!/usr/bin/env python3
"""
Script para probar los endpoints de la Weather API
Ejecuta: python test_api.py
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:5000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(title: str):
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.YELLOW}TEST: {title}{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")

def print_result(success: bool, message: str, data: Dict = None):
    status = f"{Colors.GREEN}✓ EXITOSO{Colors.END}" if success else f"{Colors.RED}✗ FALLIDO{Colors.END}"
    print(f"{status}: {message}")
    if data:
        print(f"Respuesta:\n{json.dumps(data, indent=2, ensure_ascii=False)}")

def test_health():
    print_test("GET /health")
    try:
        response = requests.get(f"{BASE_URL}/health")
        success = response.status_code == 200
        print_result(success, f"Status: {response.status_code}", response.json())
    except Exception as e:
        print_result(False, f"Error: {str(e)}")

def test_index():
    print_test("GET /")
    try:
        response = requests.get(f"{BASE_URL}/")
        success = response.status_code == 200
        print_result(success, f"Status: {response.status_code}", response.json())
    except Exception as e:
        print_result(False, f"Error: {str(e)}")

def test_weather_by_city():
    print_test("GET /weather?city=Madrid")
    try:
        response = requests.get(f"{BASE_URL}/weather", params={"city": "Madrid"})
        success = response.status_code == 200
        print_result(success, f"Status: {response.status_code}", response.json())
    except Exception as e:
        print_result(False, f"Error: {str(e)}")

def test_weather_by_coordinates():
    print_test("GET /weather?lat=40.4168&lon=-3.7038")
    try:
        response = requests.get(f"{BASE_URL}/weather", params={"lat": "40.4168", "lon": "-3.7038"})
        success = response.status_code == 200
        print_result(success, f"Status: {response.status_code}", response.json())
    except Exception as e:
        print_result(False, f"Error: {str(e)}")

def test_weather_invalid_params():
    print_test("GET /weather sin parámetros (debe fallar)")
    try:
        response = requests.get(f"{BASE_URL}/weather")
        success = response.status_code == 400
        print_result(success, f"Status: {response.status_code} (esperado: 400)", response.json())
    except Exception as e:
        print_result(False, f"Error: {str(e)}")

def test_weather_invalid_coordinates():
    print_test("GET /weather con coordenadas inválidas (debe fallar)")
    try:
        response = requests.get(f"{BASE_URL}/weather", params={"lat": "150", "lon": "-3.7038"})
        success = response.status_code == 400
        print_result(success, f"Status: {response.status_code} (esperado: 400)", response.json())
    except Exception as e:
        print_result(False, f"Error: {str(e)}")

def test_weather_city_not_found():
    print_test("GET /weather?city=CIUDADINVALIDAXYZ123 (debe fallar con 404)")
    try:
        response = requests.get(f"{BASE_URL}/weather", params={"city": "CIUDADINVALIDAXYZ123"})
        success = response.status_code == 404
        print_result(success, f"Status: {response.status_code} (esperado: 404)", response.json())
    except Exception as e:
        print_result(False, f"Error: {str(e)}")

def test_multiple_weather():
    print_test("POST /weather/multiple con 3 ciudades")
    try:
        payload = {
            "ciudades": ["Madrid", "Barcelona", "Valencia"]
        }
        response = requests.post(
            f"{BASE_URL}/weather/multiple",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        success = response.status_code == 200
        data = response.json()
        print_result(success, f"Status: {response.status_code}", data)
        if success:
            print(f"  Exitosas: {data.get('exitosas')}/{data.get('total_solicitadas')}")
            print(f"  Fallidas: {data.get('fallidas')}/{data.get('total_solicitadas')}")
    except Exception as e:
        print_result(False, f"Error: {str(e)}")

def test_multiple_weather_empty():
    print_test("POST /weather/multiple con lista vacía (debe fallar)")
    try:
        payload = {
            "ciudades": []
        }
        response = requests.post(
            f"{BASE_URL}/weather/multiple",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        success = response.status_code == 400
        print_result(success, f"Status: {response.status_code} (esperado: 400)", response.json())
    except Exception as e:
        print_result(False, f"Error: {str(e)}")

def test_multiple_weather_invalid_json():
    print_test("POST /weather/multiple sin JSON (debe fallar)")
    try:
        response = requests.post(
            f"{BASE_URL}/weather/multiple",
            data="invalid",
            headers={"Content-Type": "text/plain"}
        )
        success = response.status_code == 400
        print_result(success, f"Status: {response.status_code} (esperado: 400)", response.json())
    except Exception as e:
        print_result(False, f"Error: {str(e)}")

def test_multiple_weather_too_many():
    print_test("POST /weather/multiple con 51 ciudades (debe fallar)")
    try:
        payload = {
            "ciudades": [f"city_{i}" for i in range(51)]
        }
        response = requests.post(
            f"{BASE_URL}/weather/multiple",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        success = response.status_code == 400
        print_result(success, f"Status: {response.status_code} (esperado: 400)", response.json())
    except Exception as e:
        print_result(False, f"Error: {str(e)}")

def test_not_found():
    print_test("GET /endpoint-inexistente (debe fallar con 404)")
    try:
        response = requests.get(f"{BASE_URL}/endpoint-inexistente")
        success = response.status_code == 404
        print_result(success, f"Status: {response.status_code} (esperado: 404)", response.json())
    except Exception as e:
        print_result(False, f"Error: {str(e)}")

def main():
    print(f"\n{Colors.YELLOW}{'='*60}")
    print(f"INICIANDO PRUEBAS DE LA WEATHER API")
    print(f"Base URL: {BASE_URL}")
    print(f"{'='*60}{Colors.END}\n")
    
    try:
        # Tests de endpoints básicos
        test_health()
        test_index()
        
        # Tests de /weather
        test_weather_by_city()
        test_weather_by_coordinates()
        
        # Tests de validación
        test_weather_invalid_params()
        test_weather_invalid_coordinates()
        test_weather_city_not_found()
        
        # Tests de /weather/multiple
        test_multiple_weather()
        test_multiple_weather_empty()
        test_multiple_weather_invalid_json()
        test_multiple_weather_too_many()
        
        # Tests de errores HTTP
        test_not_found()
        
        print(f"\n{Colors.YELLOW}{'='*60}")
        print(f"PRUEBAS COMPLETADAS")
        print(f"{'='*60}{Colors.END}\n")
        
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Pruebas interrumpidas por el usuario{Colors.END}\n")
    except Exception as e:
        print(f"\n{Colors.RED}Error durante las pruebas: {str(e)}{Colors.END}\n")

if __name__ == "__main__":
    main()
