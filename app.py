import datetime
import json

import jwt
from jwt import ExpiredSignatureError, InvalidAlgorithmError, InvalidSignatureError
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

        secret_key = ENVS.JWT_SECRET
        decoded_token = jwt.decode(token.split("Bearer ")[-1], secret_key, algorithms=["HS384"])
        exp_timestamp = decoded_token.get('exp', 0)
        current_timestamp = datetime.datetime.utcnow().timestamp()

        if exp_timestamp < current_timestamp:
            return {
                'statusCode': 504,
                'body': json.dumps("El token ingresado ha expirado")
            }
        return {
            'statusCode': 200,
            'body': json.dumps("Se ha realizado correctamente la peticion")
        }

    except ExpiredSignatureError as e:
        return {
            'statusCode': 504,
            'body': json.dumps("El token ingresado ha expirado")
        }
    except InvalidAlgorithmError as e:
        return {
            'statusCode': 500,
            'body': json.dumps("El token ingresado no corresponde al cifrado HS384")
        }
    except InvalidSignatureError as e:
        return {
            'statusCode': 403,
            'body': json.dumps("El token ingresado no es valido")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
