from moto import mock_dynamodb2

from src.routes import Routes


routes = Routes()

id = "SADJKKJUdYBSAI="


@mock_dynamodb2
def test_connect():
    res = routes.connect(id)

    assert res == f"{id} connected"


@mock_dynamodb2
def test_disconnect():
    res = routes.disconnect(id)

    assert res == f"{id} has disconnected"
