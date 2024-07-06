import time
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
from users.database import get_db_instance


class UserDB(Model):
    id = UUIDField(primary_key=True, null=False, default=uuid.uuid4())
    username = TextField(null=False)
    password = TextField(null=False)
    # balance = FloatField(null=False)

    class Meta:
        database = get_db_instance()
        db_table = "Users"


class UserVerifyDB(Model):
    id = UUIDField(primary_key=True, null=False, default=uuid.uuid4())
    username = TextField(null=False)
    password = TextField(null=False)
    email = TextField(null=False)
    verification_key = TextField(null=False)
    created_at = IntegerField(null=False, default=int(time.time()))

    class Meta:
        database = get_db_instance()
        db_table = "UserVerify"


# db.connect()
