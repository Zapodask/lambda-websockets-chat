import json
import boto3
import os


client = boto3.client(
    "apigatewaymanagementapi",
    endpoint_url="https://2jab4axd2h.execute-api.us-east-1.amazonaws.com/dev",
)

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.getenv("USERS_DB"))


def sendTo(cid, data):
    client.post_to_connection(ConnectionId=cid, Data=data)


def handler(event, context):
    print(json.dumps(event))

    request_context = event.get("requestContext")
    body = json.loads(event.get("body")) if event.get("body") else None

    if request_context:
        route_key = request_context.get("routeKey")
        connection_id = request_context.get("connectionId")

        if route_key == "$connect":
            data = {}
            data["connectionId"] = connection_id
            data["name"] = ""

            table.put_item(Item=data)

            print(f"{connection_id} connected")
        elif route_key == "$disconnect":
            table.delete_item(Key={"connectionId": connection_id})

            print(f"{connection_id} has disconnected")
        elif route_key == "$default":
            pass
        elif route_key == "setName":
            name = body.get("name")

            if name:
                try:
                    table.update_item(
                        Key={"connectionId": connection_id},
                        UpdateExpression="SET #name=:n",
                        ExpressionAttributeNames={"#name": "name"},
                        ExpressionAttributeValues={":n": name},
                    )
                except Exception as e:
                    print(e)

                sendTo(connection_id, "Name setted")
            else:
                sendTo(connection_id, "Name required")
        elif route_key == "sendTo":
            pass
        elif route_key == "sendToAll":
            pass
        else:
            pass

    return {"statusCode": 200}
