from sqlalchemy.orm import Session
from ssa import models, schemas 

import crypt
import hmac
import string 
import secrets 


# Users methods from here.

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()  


def create_user(db: Session, user: schemas.UserCreate):
    salt = crypt.mksalt(crypt.METHOD_SHA512)
    password = crypt.crypt(user.password, salt=salt)

    key = "".join([secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(16)])
    salt_key = crypt.mksalt(crypt.METHOD_SHA512)
    personal_key = crypt.crypt(key, salt=salt_key)

    db_user = models.User(
        email=user.email, 
        password=password, 
        salt=salt, 
        salt_key=salt_key,
        personal_key=personal_key,
        amount=user.amount
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    db_user.personal_key = key
    return db_user


def delete_user(db: Session, user_id: int):
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()


def delete_user_by_email(db: Session, email: str):
    db.query(models.User).filter(models.User.email == email).delete()
    db.commit()


def update_user(db: Session, new_user: schemas.UserUpdate, user_id: int):
    db.query(models.User).filter(models.User.id == user_id).update(**new_user.dict())
    db.commit()


def update_user_amount(db: Session, user_id: int, amount: float):
    user =  db.query(models.User).filter(models.User.id == user_id).first()
    user.amount += amount
    db.commit()
    db.refresh(user)



# Categories methods from here.

def get_category(db : Session, cat_id : int):
    return db.query(models.Category).filter(models.Category.id == cat_id).first()


def get_category_by_name(db : Session, name : str):
    return db.query(models.Category).filter(models.Category.name == name).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()


def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, cat_id: int):
    db.query(models.Category).filter(models.Category.id == cat_id).delete()
    db.commit()


def delete_category_by_name(db: Session, name: str):
    db.query(models.Category).filter(models.Category.name == name).delete()
    db.commit()


def update_category(db: Session, category: schemas.CategoryUpdate, cat_id: int):
    db.query(models.Category).filter(models.Category.id == cat_id).update(**category.dict())
    db.commit()




# Algorithms methods from here.



# Calls methods from here.