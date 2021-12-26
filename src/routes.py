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

        name_validate = self.utils.validate(id, name, "Name is required")

        if name_validate != True:
            return name_validate
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
            to_user = body.get("to_id")
            msg = body.get("message")

            msg_validate = self.utils.validate(id, msg, "Message is required")
            to_id_validate = self.utils.validate(id, msg, "To_id is required")

            if msg_validate != True:
                return msg_validate
            if to_id_validate != True:
                return to_id_validate
            else:
                self.utils.response(to_user, msg, id)

                return True
        else:
            return "Name not defined"

    def sendToAll(self, body, id):
        if self.utils.checkName(id):
            msg = body.get("message")

            msg_validate = self.utils.validate(id, msg, "Message is required")
            if msg_validate != True:
                return msg_validate
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
