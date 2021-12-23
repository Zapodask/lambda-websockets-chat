from boto3 import resource
from os import getenv

dynamodb = resource("dynamodb")
table = dynamodb.Table(getenv("USERS_DB"))
