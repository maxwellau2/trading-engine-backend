from typing import List
from peewee import (
    PostgresqlDatabase,
    Model,
    TextField,
    IntegerField,
    UUIDField,
    FloatField,
)
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")


db = PostgresqlDatabase(
    database=DB_NAME, host=DB_HOST, port=DB_PORT, user=DB_USERNAME, password=DB_PASSWORD
)


class UserDB(Model):
    id = UUIDField(primary_key=True, null=False, default=uuid.uuid4())
    username = TextField(null=False)
    password = TextField(null=False)
    # balance = FloatField(null=False)

    class Meta:
        database = db
        db_table = "Users"
