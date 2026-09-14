from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from user.schemas import User, UserCreate, UserUpdate

class UserService:
    def __init__ (self, db:Session):
        self.db = db

    def get_users(self):
        return self.db.query(User).all()

    def get_user(self, user_id: int):
        return self.db.get(User, user_id)

    def create_user(self, payload: UserCreate):
        data = payload.model_dump(exclude={"password"})
        user = User(**data, password = payload.password)
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def update_user(self, user_id: int, payload: UserUpdate):
        user = self.db.get(User, user_id)
        if user is None:
            return None
        updates = payload.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(user, field, value)
        try:
            self.db.commit()
            self.db.refresh(user)
            return user
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete_user(self, user_id: int):
        user = self.db.get(User, user_id)
        if user is None: 
            return None 
        try:
            self.db.delete(user)
            self.db.commit()
            return user
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def check_duplicates(self, username: str = None, email: str=None, phone_number:str = None, exclude_user_id:int =None):
        checks = [(User.username, username, "username"),
                  (User.email, email, "email"),
                  (User.phone_number, phone_number, "phone number")]
        for column, value, label in checks:
            if value is None:
                continue
            query = self.db.query(User).filter(column == value)
            if exclude_user_id is not None:
                query = query.filter(User.user_id != exclude_user_id)
            if query.first() is not None:
                raise ValueError(f"That {label} is already in use")
        

"""def get_users(db: Session):
    return db.query(User).all()

def get_user(db: Session, user_id:int):
    return db.get(User, user_id)

def create_user(db: Session, payload: UserCreate):
    data = payload.model_dump(exclude={"password"})
    user = User(**data, password=payload.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user_id: int, payload:UserUpdate):
    user = db.get(User, user_id)
    if user is None:
        return None
    updates = payload.model_dump(exclude_unset = True)
    for field, value in updates.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db:Session, user_id: int):
    user = db.get(User, user_id)
    if user is None:
        return None
    db.delete(user)
    db.commit()
    return user"""