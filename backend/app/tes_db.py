from app.database.db import SessionLocal
from app.models.user import User

db=SessionLocal()

new_user=User(
    name="Alan",
    email="alan@test.com",
    password="123456"
)

db.add(new_user)

db.commit()

print("user added successfully")
db.close()