import boto3
import os

from src.db import table


class Utils:
    endpoint_url = f'{os.getenv("API_ENDPOINT").replace("wss", "https", 1)}/{os.getenv("STAGE_NAME")}'

    client = boto3.client(
        "apigatewaymanagementapi",
        endpoint_url=endpoint_url,
    )

    def getName(self, id: str):
        user = table.get_item(Key={"connectionId": id})

        name = user["Item"].get("name")

        return name

    def response(self, id: str, msg: str = None, fid: str = None, error: list = None):
        data = {}
        if fid != None:
            name = self.getName(fid)
            data = {"message": msg, "from": {"name": name, "id": fid}}
        elif msg != None:
            data["message"] = msg
        elif error != None:
            data["error"] = error

        ids = []
        if isinstance(id, str):
            ids.append(id)
            ids.append(fid) if fid != None else ids
        else:
            ids = id

        for i in ids:
            self.client.post_to_connection(ConnectionId=i, Data=str(data))

    def responseAll(self, id: str, msg: str):
        id_list = []

        users = table.scan()
        for user in users["Items"]:
            cid = user["connectionId"]
            id_list.append(cid) if cid not in id_list else id_list

        self.response(id_list, msg, id)

    def checkName(self, id: str):
        name = self.getName(id)

        if name == None:
            self.response(id, "Choose a name first")
            return False
        else:
            return True

    def validate(self, id: str, validations: list):
        errors = []

        for item in validations:
            name = item.get("name")
            value = item.get("value")

            if value == None or value == "":
                errors.append(f"{name} is required")

        if errors != []:
            self.response(id, error=errors)

            return errors

        return True
