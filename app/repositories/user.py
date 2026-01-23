from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.user import UserDB

class UserRepository(BaseRepository[UserDB]):
    def __init__(self, db: Session):
        super().__init__(UserDB, db)

    def get_by_username(self, username: str) -> UserDB | None:
        return self.db.query(self.model).filter(self.model.username == username).first()
