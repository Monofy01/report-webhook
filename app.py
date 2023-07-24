import base64
import datetime
import json
import re

import jwt

from src.config.enviroments import ENVS


def handler(event, context):
    print(f"REQUEST :: {event}")
    body = event['body']
    token = event['headers']['authorization']

    # Decodifica el cuerpo del form-data
    decoded_data = base64.b64decode(body).decode('utf-8')
    data = base64.b64decode(body).decode('utf-8')

    # Expresiones regulares para el email y la URL
    email_pattern = r'(?<=name="email"; filename="email"\r\n\r\n).*?(?=\r\n--)'
    url_pattern = r'(?<=name="url"; filename="url"\r\n\r\n).*?(?=\r\n--)'

    # Buscar el email y la URL utilizando las expresiones regulares
    email_match = re.search(email_pattern, data, re.DOTALL)
    url_match = re.search(url_pattern, data, re.DOTALL)

    # Extraer los resultados encontrados
    email = email_match.group(0).strip() if email_match else None
    url = url_match.group(0).strip() if url_match else None

    # Imprimir los resultados
    print("Email encontrado:", email)
    print("URL encontrada:", url)

    secret_key = ENVS.JWT_SECRET

    try:
        # Verificamos el token utilizando la clave secreta
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])

        exp_timestamp = decoded_token.get('exp', 0)
        current_timestamp = datetime.datetime.utcnow().timestamp()

        if exp_timestamp < current_timestamp:
            return 504  # Token expirado (504 Gateway Timeout)
        return 200  # Token válido (200 OK)

    except jwt.ExpiredSignatureError:
        return 504  # Token expirado (504 Gateway Timeout)
    except jwt.InvalidTokenError:
        return 401  # Token no válido (401 Unauthorized)
