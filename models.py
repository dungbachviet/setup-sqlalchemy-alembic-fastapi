from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    field_1 = Column(String)
    field_2 = Column(String)

class TenantModel(Base):
    __tablename__ = 'tenants'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    
