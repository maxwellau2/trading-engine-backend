from peewee import PostgresqlDatabase
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()


def get_db_instance():
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    print(DB_HOST)

    db = PostgresqlDatabase(
        database=DB_NAME,
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USERNAME,
        password=DB_PASSWORD,
    )
    return db
