import boto3
import os

from src.db import table


endpoint_url = (
    f'{os.getenv("API_ENDPOINT").replace("wss", "https", 1)}/{os.getenv("STAGE_NAME")}'
)

client = boto3.client(
    "apigatewaymanagementapi",
    endpoint_url=endpoint_url,
)


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
