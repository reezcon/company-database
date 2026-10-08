import main  # makes sure every model is loaded before querying

from engine.engine import get_db
from user.schemas import User
from auth.service import hash_password

db = next(get_db())
for u in db.query(User).all():
    if not u.password.startswith("$argon2"):   # skip anything already hashed
        u.password = hash_password(u.password)
db.commit()