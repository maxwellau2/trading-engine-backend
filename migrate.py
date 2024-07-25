from users.model.UserModel import UserDB, UserVerifyDB
from orderfilling.api.models.TradeModel import TradeDB

UserDB.drop_table()
UserVerifyDB.drop_table()
TradeDB.drop_table()

UserDB.create_table()
UserVerifyDB.create_table()
TradeDB.create_table()