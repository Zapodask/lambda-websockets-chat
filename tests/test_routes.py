import pytest
import boto3

from moto import mock_dynamodb2
from unittest.mock import patch

from src.routes import Routes


table_name = "test-users"
id = "SADJKKJUdYBSAI="

routes = Routes()


@pytest.fixture(scope="function")
def dynamodb_fixture():
    with mock_dynamodb2():
        resource = boto3.resource("dynamodb")

        table = resource.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "connectionId", "KeyType": "HASH"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "connectionId", "AttributeType": "S"},
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 10,
                "WriteCapacityUnits": 10,
            },
        )

        table.put_item(Item={"connectionId": "DasdasdSFSDFD="})
        yield table


@patch("src.routes.table")
def test_connect(mock_table, dynamodb_fixture):
    mock_table.return_value = dynamodb_fixture

    res = routes.connect(id)

    assert res == f"{id} connected"


@patch("src.routes.table")
def test_disconnect(mock_table, dynamodb_fixture):
    mock_table.return_value = dynamodb_fixture

    res = routes.disconnect(id)

    assert res == f"{id} has disconnected"


@patch("src.routes.table")
@patch("src.routes.Utils.response", return_value=None)
def test_set_name(mock_table, mock_response, dynamodb_fixture):
    mock_table.return_value = dynamodb_fixture

    res = routes.setName({"name": "joao"}, id)

    assert res == True


@patch("src.routes.Utils.checkName", return_value=True)
@patch("src.routes.Utils.validate", return_value=True)
@patch("src.routes.Utils.response", return_value=None)
def test_send_to(mock_check_name, mock_validate, mock_response, dynamodb_fixture):
    res = routes.sendTo({"to_id": id, "message": "msg"}, id)

    assert res == True


@patch("src.routes.table")
@patch("src.routes.Utils.checkName", return_value=True)
@patch("src.routes.Utils.validate", return_value=True)
@patch("src.routes.Utils.response", return_value=None)
def test_send_to_all(
    mock_table, mock_check_name, mock_validate, mock_response, dynamodb_fixture
):
    mock_table.return_value = dynamodb_fixture

    res = routes.sendToAll({"message": "msg"}, id)

    assert res == True


@patch("src.routes.Utils.response", return_value=None)
def test_default(mock_response):
    res = routes.default(id)

    assert res == "Action not allowed"
