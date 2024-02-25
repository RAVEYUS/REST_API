from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
class users (Base):
    __tablename__ = 'users'
    id=Column(Integer, primary_key=True,index=True)
    Header = Column(String(255))
    Body = Column(String(255), unique=True, index=True)
