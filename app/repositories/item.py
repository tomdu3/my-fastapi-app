from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.item import ItemDB

class ItemRepository(BaseRepository[ItemDB]):
    def __init__(self, db: Session):
        super().__init__(ItemDB, db)

    def search(self, q: str | None = None) -> list[ItemDB]:
        query = self.db.query(self.model)
        if q:
            query = query.filter(self.model.name.contains(q))
        return query.all()
