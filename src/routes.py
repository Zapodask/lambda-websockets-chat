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

        validation = self.utils.validate(
            id,
            [
                {
                    "name": "Name",
                    "value": name,
                }
            ],
        )

        if validation != True:
            return validation
        else:
            users = table.scan()

            for user in users["Items"]:
                if name == user.get("name"):
                    self.utils.response(id, "The name is already in use")
                    return "The name is already in use"

            table.update_item(
                Key={"connectionId": id},
                UpdateExpression="SET #name=:n",
                ExpressionAttributeNames={"#name": "name"},
                ExpressionAttributeValues={":n": name},
            )

            self.utils.response(id, "Name setted")

            return True

    def sendTo(self, body, id):
        if self.utils.checkName(id):
            to_id = body.get("to_id")
            msg = body.get("message")

            validation = self.utils.validate(
                id,
                [
                    {
                        "name": "To_id",
                        "value": to_id,
                    },
                    {
                        "name": "Message",
                        "value": msg,
                    },
                ],
            )

            if validation != True:
                return validation
            else:
                self.utils.response(to_id, msg, id)

                return True
        else:
            return "Name not defined"

    def sendToAll(self, body, id):
        if self.utils.checkName(id):
            msg = body.get("message")

            validation = self.utils.validate(
                id,
                [
                    {
                        "name": "Message",
                        "value": msg,
                    }
                ],
            )

            if validation != True:
                return validation
            else:
                id_list = []

                users = table.scan()
                for user in users["Items"]:
                    cid = user["connectionId"]
                    id_list.append(cid) if cid not in id_list else id_list

                self.utils.response(id_list, msg, id)

                return True
        else:
            return "Name not defined"

    def default(self, id):
        self.utils.response(id, "Action not allowed")

        return "Action not allowed"
