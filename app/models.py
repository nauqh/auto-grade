from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from .database import Base


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, index=True)
    name = Column(String)
    module = Column(String)
    submitted_at = Column(DateTime(timezone=True),
                          server_default=func.now(), nullable=False)
    submission = Column(JSON)
