from typing import List
from peewee import PostgresqlDatabase, Model, TextField, IntegerField
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

print(DB_HOST)

db = PostgresqlDatabase(
    database=DB_NAME, host=DB_HOST, port=DB_PORT, user=DB_USERNAME, password=DB_PASSWORD
)


class MyUser(Model):
    name = TextField()
    city = TextField()
    age = IntegerField()

    class Meta:
        database = db
        db_table = "MyUser"


if db.connect():
    # db.create_tables([MyUser])
    # result = db.get_tables()
    # print(result)
    # print("yay!")
    user = MyUser()
    user.name = "smithc"
    user.city = "sg"
    user.age = 12
    user.save()
    print(user.__dict__["__data__"])
    # res = db.execute_sql("""
    #     SELECT * FROM "MyUser";
    #     """).fetchall()
    # print(res)
    # user: List[MyUser] = list(MyUser.select().where(MyUser.name=="smithc"))
    # for i in user:
    #     print(i.name, i.city)
    # for u in user:
    #     print(u)
    # for i in MyUser.get(MyUser.name=='johny'):
    #     print(i)
