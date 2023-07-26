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

        secret_key = ENVS.JWT_SECRET
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS384"])
        exp_timestamp = decoded_token.get('exp', 0)
        current_timestamp = datetime.datetime.utcnow().timestamp()

        if exp_timestamp < current_timestamp:
            return 504
        return 200

    except Exception as e:
        print(e)
    except jwt.ExpiredSignatureError:
        return 504
    except jwt.InvalidTokenError:
        return 403
