from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from models import UserModel
from database import SessionLocal
from fastapi import FastAPI
import uvicorn
from schemas import User, UserCreate, Tenant, TenantCreate
from models import UserModel, TenantModel

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ===========   USER ENDPOINTS   ==================
@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_model = UserModel(**(user.model_dump()))
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model


@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    query_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if query_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return query_user


@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    user_list = db.query(UserModel).all()
    return user_list


# ===========   TENANT ENDPOINTS   ==================
@app.post("/tenants/")
def create_tenant(tenant: TenantCreate, db: Session = Depends(get_db)):
    tenant_model = TenantModel(**(tenant.model_dump()))
    db.add(tenant_model)
    db.commit()
    db.refresh(tenant_model)
    return tenant_model


@app.get("/tenants/{tenant_id}")
def read_tenant(tenant_id: int, db: Session = Depends(get_db)):
    query_tenant = db.query(TenantModel).filter(TenantModel.id == tenant_id).first()
    if query_tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return query_tenant


@app.get("/tenants")
def get_all_tenants(db: Session = Depends(get_db)):
    tenant_list = db.query(TenantModel).all()
    return tenant_list


# ===========   RUN APPLICATION   ==================
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)