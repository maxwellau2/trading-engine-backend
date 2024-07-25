import time
from typing import List
from peewee import (
    Model,
    TextField,
    IntegerField,
    UUIDField,
    FloatField,
)
import uuid
from dotenv import load_dotenv
from database import get_db_instance


class TradeDB(Model):
    trade_id = UUIDField(primary_key=True, null=False, default=uuid.uuid4())
    ticker = TextField(null=False)
    qty = FloatField(null=False)
    price = FloatField(null=False)
    created_at = IntegerField(null=False, default=int(time.time()))  # epoch time

    class Meta:
        database = get_db_instance()
        db_table = "Trades"