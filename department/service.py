from sqlalchemy.orm import Session
from department.schemas import Department, DepartmentCreate, DepartmentOut, DepartmentUpdate
from sqlalchemy.exc import SQLAlchemyError

class DepartmentService:
    def __init__ (self, db: Session):
        self.db = db

    def get_departments(self):
        return self.db.query(Department).all()

    def get_department(self, department_id: int):
        return self.db.get(Department, department_id)

    def create_department(self, payload: DepartmentCreate):
        data = payload.model_dump()
        department = Department(**data)
        try:
            self.db.add(department)
            self.db.commit()
            self.db.refresh(department)
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def update_department(self, department_id: int, payload: DepartmentUpdate):
        department = self.db.get(Department, department_id)
        if department is None: 
            return None
        updates = payload.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(department, field, value)
        try: 
            self.db.commit()
            self.db.refresh(department)
            return department
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete_department(self, department_id: int):
        department = self.db.get(Department, department_id)
        try: 
            self.db.delete(department)
            self.db.commit()
            return department
        except SQLAlchemyError:
            self.db.rollback()
            raise
"""

def get_departments(db:Session):
    return db.query(Department).all()

def get_department(db: Session, department_id:int):
    return db.get(Department, department_id)

def create_department(db: Session, payload: DepartmentCreate):
    data = payload.model_dump()
    department = Department(**data)
    db.add(department)
    db.commit()
    db.refresh(department)
    return department

def update_department(db: Session, department_id: int, payload:DepartmentUpdate):
    department = db.get(Department, department_id)
    if department is None: 
        return None
    updates = payload.model_dump(exclue_unset = True)
    for field, value in updates.items():
        setattr(department, field, value)
    db.commit()
    db.refresh(department)
    return department

def delete_department(db: Session, department_id: int):
    department = db.get(Department, department_id)
    if department is None: 
        return None
    db.delete(department)
    db.commit()
    return department
"""