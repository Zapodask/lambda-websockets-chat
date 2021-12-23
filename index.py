import json
from src.routes import Routes


routes = Routes()


def handler(event, context):
    print(json.dumps(event))

    request_context = event.get("requestContext")
    body = json.loads(event.get("body")) if event.get("body") else None

    if request_context:
        route_key = request_context.get("routeKey")
        connection_id = request_context.get("connectionId")

        if route_key == "$connect":
            routes.connect(connection_id)
        elif route_key == "$disconnect":
            routes.disconnect(connection_id)
        elif route_key == "setName":
            routes.setName(body, connection_id)
        elif route_key == "sendTo":
            routes.sendTo(body, connection_id)
        elif route_key == "sendToAll":
            routes.sendToAll(body, connection_id)
        else:
            routes.default(connection_id)

    return {"statusCode": 200}
