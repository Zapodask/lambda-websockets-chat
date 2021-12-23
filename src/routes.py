from src.db import table
from src.utils import response, checkName, validate


class Routes:
    def connect(self, id):
        data = {}
        data["connectionId"] = id

        table.put_item(Item=data)

        print(f"{id} connected")

    def disconnect(self, id):
        table.delete_item(Key={"connectionId": id})

        print(f"{id} has disconnected")

    def setName(self, body, id):
        name = body.get("name")

        if name:
            users = table.scan()

            for user in users["Items"]:
                if name == user.get("name"):
                    response(id, "The name is already in use")
                    return

            table.update_item(
                Key={"connectionId": id},
                UpdateExpression="SET #name=:n",
                ExpressionAttributeNames={"#name": "name"},
                ExpressionAttributeValues={":n": name},
            )

            response(id, "Name setted")
        else:
            response(id, "Name is required")

    def sendTo(self, body, id):
        if checkName(id):
            to_user = body.get("to_id")
            msg = body.get("message")

            if validate(id, msg, "Message is required") and validate(
                id, to_user, "To_id is required"
            ):
                response(to_user, msg, id)

    def sendToAll(self, body, id):
        if checkName(id):
            msg = body.get("message")

            if validate(id, msg, "Message is required"):
                id_list = []

                users = table.scan()
                for user in users["Items"]:
                    cid = user["connectionId"]
                    id_list.append(cid) if cid not in id_list else id_list

                response(id_list, msg, id)

    def default(self, id):
        response(id, "Action not allowed")
