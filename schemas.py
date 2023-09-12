from pydantic import BaseModel

class User(BaseModel):
    id: int
    email: str
    password: str

class UserCreate(BaseModel):
    email: str
    password: str

class Tenant(BaseModel):
    id: int
    name: str
    description: str

class TenantCreate(BaseModel):
    name: str
    description: str