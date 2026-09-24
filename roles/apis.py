from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
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
    try:
        return service(db).create_role(payload)
    except ValueError as e:
            raise HTTPException(status_code=409, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while creating role")

# UPDATE
@router.put("/{role_id}", response_model=RoleOut)
async def update_role(role_id: int, payload: RoleUpdate, db: Session= session) :
    try:
        role = service(db).update_role(role_id, payload)
    except ValueError as e: 
        raise HTTPException(status_code=409, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while updating user")
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