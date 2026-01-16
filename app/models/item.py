from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class ItemDB(Base):
    """
    SQLAlchemy model for the items table.
    """
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    description = Column(String, nullable=True)
    tax = Column(Float, nullable=True)
