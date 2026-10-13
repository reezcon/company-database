from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from department.schemas import Department, DepartmentCreate, DepartmentOut, DepartmentUpdate
from engine.engine import get_db
from department.service import DepartmentService as service

from auth.apis import require_admin_or_manager, require_admin

router = APIRouter(prefix="/departments", tags = ["Departments"])
session = Depends(get_db)

# READ all departments
@router.get("", response_model=list[DepartmentOut])
async def read_departments(db: Session = session,
                           _: Department = Depends(require_admin_or_manager)):
    return service(db).get_departments()

# READ one department
@router.get("/{department_id}")
async def read_department(department_id:int, db: Session = session,
                           _: Department = Depends(require_admin_or_manager)):
    department = service(db).get_department(department_id)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department 

# CREATE
@router.post("", response_model=DepartmentOut)
async def create_department(payload:DepartmentCreate, db: Session=session,
                           _: Department = Depends(require_admin_or_manager)):
    try:
        return service(db).create_department(payload)
    except ValueError as e:
        raise HTTPException(status_code=409, detail =str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while creating department")

# UPDATE
@router.put("/{department_id}", response_model=DepartmentOut)
async def update_department(department_id:int, payload:DepartmentUpdate, db: Session=session,
                           _: Department = Depends(require_admin_or_manager)):
    try:
        department = service(db).update_department(department_id, payload)
    except ValueError as e: 
        raise HTTPException(status_code=409, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while updating user")
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

# DELETE
@router.delete("/{department_id}")
async def delete_department(department_id: int, db: Session = session,
                           _: Department = Depends(require_admin)):
    department = service(db).delete_department(department_id)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return {"detail":f"Department {department_id} is deleted"}