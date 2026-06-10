from sqlalchemy.orm import Session
from models import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, name: str, email: str, password_hash: str) -> User:
        user = User(name=name, email=email, password_hash=password_hash)
        self.db.add(user)
        self.db.flush()
        return user

    def upsert(self, name: str, email: str) -> User:
        user = self.get_by_email(email)
        if user:
            user.name = name
        else:
            user = User(name=name, email=email)
            self.db.add(user)
        self.db.flush()
        return user

    def list_all(self) -> list[User]:
        return self.db.query(User).all()
