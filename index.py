import json
import boto3
import os


endpoint_url = (
    f'{os.getenv("API_ENDPOINT").replace("wss", "https", 1)}/{os.getenv("STAGE_NAME")}'
)

client = boto3.client(
    "apigatewaymanagementapi",
    endpoint_url=endpoint_url,
)

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.getenv("USERS_DB"))


def getName(id):
    user = table.get_item(Key={"connectionId": id})

    name = user["Item"].get("name")

    return name


def response(id, data, fid=None):
    if fid != None:
        name = getName(fid)
        data = {"message": data, "from": {"name": name, "id": fid}}

    ids = []
    if isinstance(id, str):
        ids.append(id)
        ids.append(fid) if fid != None else ids
    else:
        ids = id

    for i in ids:
        client.post_to_connection(ConnectionId=i, Data=str(data))


def checkName(id):
    name = getName(id)

    if name == None:
        response(id, "Choose a name first")
        return False
    else:
        return True


def validate(id, value, errorMessage):
    if value == None:
        response(id, errorMessage)
        return False
    else:
        return True


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

            table.put_item(Item=data)

            print(f"{connection_id} connected")
        elif route_key == "$disconnect":
            table.delete_item(Key={"connectionId": connection_id})

            print(f"{connection_id} has disconnected")
        elif route_key == "$default":
            response(connection_id, "Choose a action")
        elif route_key == "setName":
            name = body.get("name")

            if name:
                users = table.scan()

                for user in users["Items"]:
                    if name == user.get("name"):
                        response(connection_id, "The name is already in use")
                        return {"statusCode": 400}

                table.update_item(
                    Key={"connectionId": connection_id},
                    UpdateExpression="SET #name=:n",
                    ExpressionAttributeNames={"#name": "name"},
                    ExpressionAttributeValues={":n": name},
                )

                response(connection_id, "Name setted")
            else:
                response(connection_id, "Name is required")
        elif route_key == "sendTo":
            if checkName(connection_id):
                to_user = body.get("to_id")
                msg = body.get("message")

                if validate(connection_id, msg, "Message is required") and validate(
                    connection_id, to_user, "To_id is required"
                ):
                    response(to_user, msg, connection_id)
        elif route_key == "sendToAll":
            if checkName(connection_id):
                msg = body.get("message")

                if validate(connection_id, msg, "Message is required"):
                    id_list = []

                    users = table.scan()
                    for user in users["Items"]:
                        cid = user["connectionId"]
                        id_list.append(cid) if cid not in id_list else id_list

                    response(id_list, msg, connection_id)
        else:
            response(connection_id, "Action not allowed")

    return {"statusCode": 200}
