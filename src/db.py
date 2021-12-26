from boto3 import resource
from os import getenv


table = resource("dynamodb").Table(getenv("USERS_DB"))
