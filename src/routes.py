from src.db import table
from src.utils import Utils


class Routes:
    utils = Utils()

    def connect(self, id):
        data = {}
        data["connectionId"] = id

        table.put_item(Item=data)

        return f"{id} connected"

    def disconnect(self, id):
        table.delete_item(Key={"connectionId": id})

        return f"{id} has disconnected"

    def setName(self, body, id):
        name = body.get("name")

        if name:
            users = table.scan()

            for user in users["Items"]:
                if name == user.get("name"):
                    self.utils.response(id, "The name is already in use")
                    return

            table.update_item(
                Key={"connectionId": id},
                UpdateExpression="SET #name=:n",
                ExpressionAttributeNames={"#name": "name"},
                ExpressionAttributeValues={":n": name},
            )

            self.utils.response(id, "Name setted")
        else:
            self.utils.response(id, "Name is required")

    def sendTo(self, body, id):
        if self.utils.checkName(id):
            to_user = body.get("to_id")
            msg = body.get("message")

            if self.utils.validate(
                id, msg, "Message is required"
            ) and self.utils.validate(id, to_user, "To_id is required"):
                self.utils.response(to_user, msg, id)

    def sendToAll(self, body, id):
        if self.utils.checkName(id):
            msg = body.get("message")

            if self.utils.validate(id, msg, "Message is required"):
                id_list = []

                users = table.scan()
                for user in users["Items"]:
                    cid = user["connectionId"]
                    id_list.append(cid) if cid not in id_list else id_list

                self.utils.response(id_list, msg, id)

    def default(self, id):
        self.utils.response(id, "Action not allowed")
