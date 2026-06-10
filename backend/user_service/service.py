from sqlalchemy.orm import Session
from repository import UserRepository
from schemas import UserOut
from fastapi import HTTPException


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)
        self.db = db

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
