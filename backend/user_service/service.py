from sqlalchemy.orm import Session
from fastapi import HTTPException

from repository import UserRepository
from schemas import UserOut, TokenOut
from auth import hash_password, verify_password, create_token


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)
        self.db = db

    def register(self, name: str, email: str, password: str) -> TokenOut:
        if self.repo.get_by_email(email):
            raise HTTPException(status_code=409, detail="Email already registered")
        hashed = hash_password(password)
        user = self.repo.create(name=name, email=email, password_hash=hashed)
        self.db.commit()
        self.db.refresh(user)
        token = create_token(user.id, user.email)
        return TokenOut(access_token=token, user=UserOut.model_validate(user))

    def login(self, email: str, password: str) -> TokenOut:
        user = self.repo.get_by_email(email)
        if not user or not user.password_hash:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        if not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        token = create_token(user.id, user.email)
        return TokenOut(access_token=token, user=UserOut.model_validate(user))

    def get_user(self, user_id: int) -> UserOut:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserOut.model_validate(user)

    def upsert_user(self, name: str, email: str) -> UserOut:
        user = self.repo.upsert(name, email)
        self.db.commit()
        self.db.refresh(user)
        return UserOut.model_validate(user)

    def list_users(self) -> list[UserOut]:
        return [UserOut.model_validate(u) for u in self.repo.list_all()]
