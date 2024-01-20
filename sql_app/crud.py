import hashlib
from sqlalchemy.orm import Session

from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.CreateUser):
    db_user = models.User(first_name = user.first_name, last_name = user.last_name, username = user.username, hashed_password = hashlib.sha256(user.password.encode('UTF-8')).hexdigest())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    return user

def preferences_user(db: Session, username: str):
    user = db.query(models.Preferences).filter(models.Preferences.user == username).first()
    return user

def create_user_preferences(db: Session, username: str):
    db_user = models.Preferences(user = username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_preferences_like(db: Session, cuisine: str, username: str):
    user = preferences_user(db, username)
    print(user)
    print(getattr(user, cuisine))
    setattr(user, cuisine, getattr(user, cuisine) + 1)
    db.commit()
    db.refresh(user)

def update_preferences_dislike(db: Session, cuisine: str, username: str):
    user = preferences_user(db, username)
    setattr(user, cuisine, getattr(user, cuisine) - 1)
    db.commit()
    db.refresh(user)