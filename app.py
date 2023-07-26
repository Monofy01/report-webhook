import datetime
import json

import jwt
from streaming_form_data import StreamingFormDataParser
from streaming_form_data.targets import ValueTarget
import base64

from src.config.enviroments import ENVS


def handler(event, context):
    try:
        print(f"REQUEST :: {event}")
        body = event['body']
        token = event['headers']['authorization']

        # Initiate the parser with request header
        parser = StreamingFormDataParser(headers=event['headers'])
        email = ValueTarget()
        url = ValueTarget()

        parser.register("email", email)
        parser.register("url", url)

        mydata = base64.b64decode(event["body"])

        parser.data_received(mydata)

        email_data = email.value.decode("utf-8")
        url_data = url.value.decode("utf-8")

        # Imprimir los resultados
        print("Email encontrado:", email_data)
        print("URL encontrada:", url_data)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Correcto',
                'code': 200,
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

        # secret_key = ENVS.JWT_SECRET
        # # Verificamos el token utilizando la clave secreta
        # decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        #
        # exp_timestamp = decoded_token.get('exp', 0)
        # current_timestamp = datetime.datetime.utcnow().timestamp()
        #
        # if exp_timestamp < current_timestamp:
        #     return 504  # Token expirado (504 Gateway Timeout)
        # return 200  # Token válido (200 OK)

    except Exception as e:
        print(e)
    except jwt.ExpiredSignatureError:
        return 504  # Token expirado (504 Gateway Timeout)
    except jwt.InvalidTokenError:
        return 401  # Token no válido (401 Unauthorized)
