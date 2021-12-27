from unittest.mock import patch

from src.routes import Routes


routes = Routes()

id = "SADJKKJUdYBSAI="


@patch("src.routes.table")
def test_connect(mock_table):
    res = routes.connect(id)

    assert res == f"{id} connected"


@patch("src.routes.table")
def test_disconnect(mock_table):
    res = routes.disconnect(id)

    assert res == f"{id} has disconnected"


@patch("src.routes.table")
@patch("src.routes.Utils.response", return_value=None)
def test_set_name(mock_table, mock_response):
    res = routes.setName({"name": "test_name"}, id)

    assert res == True


@patch("src.routes.table")
@patch("src.routes.Utils.response", return_value=None)
def test_set_name_validate_body(mock_table, mock_response):
    res = routes.setName({}, id)

    assert "Name is required" in res


@patch(
    "src.routes.table.scan",
    return_value={"Items": [{"connectionId": "AAAAA=", "name": "test_name"}]},
)
@patch("src.routes.Utils.response", return_value=None)
def test_set_name_already_in_use(mock_table, mock_response):
    res = routes.setName({"name": "test_name"}, id)

    assert res == "The name is already in use"


@patch("src.routes.Utils.checkName", return_value=True)
@patch("src.routes.Utils.response", return_value=None)
def test_send_to(mock_check_name, mock_response):
    res = routes.sendTo({"to_id": id, "message": "msg"}, id)

    assert res == True


@patch("src.routes.Utils.checkName", return_value=False)
@patch("src.routes.Utils.response", return_value=None)
def test_send_to_check_name(mock_check_name, mock_response):
    res = routes.sendTo({"to_id": id, "message": "msg"}, id)

    assert res == "Name not defined"


@patch("src.routes.Utils.checkName", return_value=True)
@patch("src.routes.Utils.response", return_value=None)
def test_send_to_validate_body(mock_check_name, mock_response):
    res = routes.sendTo({"to_id": ""}, id)

    assert "To_id is required" in res and "Message is required" in res


@patch("src.routes.table")
@patch("src.routes.Utils.checkName", return_value=True)
@patch("src.routes.Utils.response", return_value=None)
def test_send_to_all(mock_table, mock_check_name, mock_response):
    res = routes.sendToAll({"message": "msg"}, id)

    assert res == True


@patch("src.routes.table")
@patch("src.routes.Utils.checkName", return_value=False)
@patch("src.routes.Utils.response", return_value=None)
def test_send_to_all_check_name(mock_table, mock_check_name, mock_response):
    res = routes.sendToAll({"message": "msg"}, id)

    assert res == "Name not defined"


@patch("src.routes.table")
@patch("src.routes.Utils.checkName", return_value=True)
@patch("src.routes.Utils.response", return_value=None)
def test_send_to_all_validate_body(mock_table, mock_check_name, mock_response):
    res = routes.sendToAll({}, id)

    assert "Message is required" in res


@patch("src.routes.Utils.response", return_value=None)
def test_default(mock_response):
    res = routes.default(id)

    assert res == "Action not allowed"
