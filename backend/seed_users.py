from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from backend.infrastructure.database.connection import SessionLocal, init_db
from backend.infrastructure.orm.models.user_model import UserModel
from backend.infrastructure.auth.password_handler import hash_password
from backend.domain.enums.role import Role


def seed_users():
    init_db()
    db = SessionLocal()

    users_to_create = [
        {
            "id": "admin-user-1",
            "name": "Admin User",
            "email": "admin@opscenter.com",
            "password": "admin123",
            "role": Role.ADMIN,
        },
        {
            "id": "supervisor-user-1",
            "name": "Supervisor User",
            "email": "supervisor@opscenter.com",
            "password": "super123",
            "role": Role.SUPERVISOR,
        },
        {
            "id": "operator-user-1",
            "name": "Operator User",
            "email": "operator@opscenter.com",
            "password": "oper123",
            "role": Role.OPERATOR,
        },
    ]

    try:
        for user_data in users_to_create:
            existing = (
                db.query(UserModel)
                .filter(UserModel.email == user_data["email"])
                .first()
            )

            if existing:
                print(f"Usuario ya existe: {user_data['email']}")
                continue

            user = UserModel(
                id=user_data["id"],
                name=user_data["name"],
                email=user_data["email"],
                hashed_password=hash_password(user_data["password"]),
                role=user_data["role"],
            )

            db.add(user)
            print(f"Usuario creado: {user_data['email']}")

        db.commit()
        print("Seed completado.")
    except Exception as e:
        db.rollback()
        print(f"Error en seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_users()