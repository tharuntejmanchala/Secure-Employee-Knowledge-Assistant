from database import SessionLocal
from models import User

db = SessionLocal()

user = db.query(User).filter(
    User.email == "tharun@gmail.com"
).first()

print(user)