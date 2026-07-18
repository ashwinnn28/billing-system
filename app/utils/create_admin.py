from app.core.config import settings
from app.core.security import hash_password
from app.database.database import SessionLocal
from app.models.user import User


def create_admin_user() -> None:
    db = SessionLocal()
    try:
        existing_admin = db.query(User).filter(
            User.email == settings.admin_email
        ).first()

        if existing_admin:
            return

        admin = User(
            name="Admin",
            email=settings.admin_email,
            password=hash_password(settings.admin_password),
            role="admin",
            is_active=True,
        )

        db.add(admin)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    create_admin_user()