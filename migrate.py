from users.model.UserModel import UserDB, UserVerifyDB

UserDB.drop_table()
UserVerifyDB.drop_table()

UserDB.create_table()
UserVerifyDB.create_table()
