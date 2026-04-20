from app.db.session import SessionLocal
from app.models.role import Role


ROLES = [
    {"code": "admin", "name": "Администратор", "description": "Полный доступ"},
    {"code": "veterinarian", "name": "Ветеринар", "description": "Медицинская часть"},
    {"code": "user", "name": "Пользователь", "description": "Просмотр и выполнение задач"},
]


def seed_roles():
    db = SessionLocal()
    try:
        for role_data in ROLES:
            exists = db.query(Role).filter(Role.code == role_data["code"]).first()
            if not exists:
                db.add(Role(**role_data))
        db.commit()
        print("Роли добавлены")
    finally:
        db.close()


if __name__ == "__main__":
    seed_roles()