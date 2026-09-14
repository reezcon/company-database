from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError  
from roles.schemas import Role, RoleCreate, RoleUpdate

class RoleService:
    def __init__(self, db: Session):
        self.db = db

    def get_roles(self):
        return self.db.query(Role).all()

    def get_role(self, role_id: int):
        return self.db.get(Role, role_id)

    def create_role(self, payload: RoleCreate):
        data = payload.model_dump()
        role = Role(**data)
        try: 
            self.db.add(role)
            self.db.commit()
            self.db.refresh(role)
            return role
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def update_role(self, role_id: int, payload: RoleUpdate):
        role = self.db.get(Role, role_id)
        if role is None:
            return None
        updates = payload.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(role, field, value)
        try: 
            self.db.commit()
            self.db.refresh(role)
            return role
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete_role(self, role_id: int):
        role = self.db.get(Role, role_id)
        if role is None:
            return None
        try: 
            self.db.delete(role)
            self.db.commit()
            return role
        except SQLAlchemyError:
            self.db.rollback()
            raise

"""def get_roles(db: Session):
    return db.query(Role).all()

def get_role(db: Session, role_id:int):
    return db.get(Role, role_id)

def create_role(db: Session, payload: RoleCreate):
    data = payload.model_dump()
    role = Role(**data)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def update_role(db: Session, role_id: int, payload:RoleUpdate):
    role = db.get(Role, role_id)
    if role is None: 
        return None
    updates = payload.model_dump()
    for field, value in updates.items():
        setattr(role, field, value)
    db.commit()
    db.refresh(role)
    return role

def delete_role(db:Session, role_id: int):
    role = db.get(Role, role_id)
    if role is None: 
        return None
    db.delete(role)
    db.commit()
    return role"""