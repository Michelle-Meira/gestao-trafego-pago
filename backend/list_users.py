import sys
sys.path.append('.')
from app.database import SessionLocal
from app.schemas.user_db import UserDB

db = SessionLocal()
try:
    users = db.query(UserDB).all()
    print("👥 USUÁRIOS NO BANCO:")
    for user in users:
        print(f"  ID: {user.id} | Email: {user.email} | Nome: {user.full_name} | Role: {user.role.value}")
    print(f"\nTotal: {len(users)} usuários")
finally:
    db.close()
