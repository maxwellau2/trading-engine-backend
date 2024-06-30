import os
from users.registration.service.Registration import Registration
from users.database import get_db_instance

# db = get_db_instance()
# print(db.connect())
# os.abort()
reg = Registration()
# reg.create_table()

# res = reg.create_user("max", "1234")
# res = reg.delete_user("max")
res = reg.change_password("max", "bear")

print(res)
