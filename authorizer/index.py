import json
import boto3
import os
import jwt

client = boto3.client("secretsmanager")


def handler(event, context):
    print(json.dumps(event))

    secret = client.get_secret_value(SecretId=os.getenv("JWT_SECRET_ARN"))
    token = event.get("authorization")

    try:
        decoded = jwt.decode(token, secret, algorithms=["HS256"])

        return  ## Terminar aqui
    except:
        return "Access denied"
