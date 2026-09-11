from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from engine.engine import get_db
from roles.schemas import Role, RoleCreate, RoleOut, RoleUpdate
from roles.service import RoleService as service

#app = FastAPI()
router = APIRouter(prefix ="/roles", tags=["Roles"])
session = Depends(get_db)

# READ all roles
@router.get("", response_model=list[RoleOut])
async def read_roles(db: Session = session):
    return service(db).get_roles()

# READ one role
@router.get("/{role_id}")
async def read_role(role_id: int, db:Session = session):
    role = service(db).get_role(role_id)
    if role is None: 
        raise HTTPException(status_code=404, detail="Role not found")
    return role

# CREATE
@router.post("", response_model=RoleOut)
async def create_role(payload: RoleCreate, db: Session= session):
    data = payload.model_dump()
    return service(db).create_role(payload)
                    
# UPDATE
@router.put("/{role_id}", response_model=RoleOut)
async def update_role(role_id: int, payload: RoleUpdate, db: Session= session) :
    role = service(db).update_role(role_id, payload)
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

# DELETE
@router.delete("/{role_id}")
async def delete_role(role_id: int, db: Session = session):
    role = service(db).delete_role(role_id)
    if role is None: 
        raise HTTPException(status_code=404, detail = "Role not found")
    return{"detail": f"Role {role_id} deleted"}