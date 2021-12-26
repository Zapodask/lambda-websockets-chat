import boto3
import os

from src.db import table


class Utils:
    endpoint_url = f'{os.getenv("API_ENDPOINT").replace("wss", "https", 1)}/{os.getenv("STAGE_NAME")}'

    client = boto3.client(
        "apigatewaymanagementapi",
        endpoint_url=endpoint_url,
    )

    def getName(self, id):
        user = table.get_item(Key={"connectionId": id})

        name = user["Item"].get("name")

        return name

    def response(self, id, msg, fid=None):
        data = {}
        if fid != None:
            name = self.getName(fid)
            data = {"message": msg, "from": {"name": name, "id": fid}}
        else:
            data["message"] = msg

        ids = []
        if isinstance(id, str):
            ids.append(id)
            ids.append(fid) if fid != None else ids
        else:
            ids = id

        for i in ids:
            self.client.post_to_connection(ConnectionId=i, Data=str(data))

    def responseAll(self, id, msg):
        id_list = []

        users = table.scan()
        for user in users["Items"]:
            cid = user["connectionId"]
            id_list.append(cid) if cid not in id_list else id_list

        self.response(id_list, msg, id)

    def checkName(self, id):
        name = self.getName(id)

        if name == None:
            rtc = "Choose a name first"
            self.response(id, rtc)
            return rtc
        else:
            return True

    def validate(self, id, value, errorMessage):
        if value == None:
            self.response(id, errorMessage)
            return errorMessage
        else:
            return True
