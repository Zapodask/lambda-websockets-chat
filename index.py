import json
import boto3
import os


client = boto3.client(
    "apigatewaymanagementapi",
    endpoint_url="https://7ji68guq04.execute-api.us-east-1.amazonaws.com/dev",
)

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.getenv("USERS_DB"))


def lambda_handler(event, context):
    print(json.dumps(event))

    request_context = event.get("requestContext")
    body = json.loads(event.get("body")) if event.get("body") else None

    if request_context:
        route_key = request_context.get("routeKey")
        connection_id = request_context.get("connectionId")

        if route_key == "$connect":
            print(f"{connection_id} está conectado")
        elif route_key == "$disconnect":
            print(f"{connection_id} desconectou")
        elif route_key == "$default":
            pass
        else:
            pass

    return {"statusCode": 200}
