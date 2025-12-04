"""
Configuración del proyecto ABC Dataset.
Carga variables de entorno desde el archivo .env
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# API Endpoint
API_ENDPOINT = os.getenv('END_POINT')

# Validar que el endpoint esté configurado
if not API_ENDPOINT:
    raise ValueError("END_POINT no está configurado en el archivo .env. Por favor, crea un archivo .env basado en .env.example")
