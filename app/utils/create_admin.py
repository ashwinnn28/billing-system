from app.database.database import SessionLocal
from app.models.user import User
from app.core.security import hash_password


db = SessionLocal()

existing_admin = db.query(User).filter(
    User.email == "admin@test.com"
).first()

if existing_admin:
    print("Admin user already exists")
else:
    admin = User(
        name="Admin",
        email="admin@test.com",
        password=hash_password("admin123"),
        role="admin",
        is_active=True
    )

    db.add(admin)
    db.commit()

    print("Admin created successfully")

db.close()