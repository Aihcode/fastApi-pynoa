from sqlalchemy.orm import Session

from . import models, schemas
from helpers.passwordgen import get_password_hash
from json import dumps

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    profileRes = ""
    fake_hashed_password = get_password_hash(user.password + "notreallyhashed")
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    if db_user.id > 0:
        db_profile = models.Profile(
            first_name=user.firstName,
            last_name=user.lastName,
            bio=user.bio,
            pic_url="https://i.pravatar.cc/150?u=a04258114e29026702d",
            user_id=db_user.id
        )
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        update_user = db.query(models.User).filter(models.User.id == db_user.id).first()
        update_user.profile_id = db_profile.id
        db.commit()
        db.refresh(update_user)
        profileRes = db_profile
    return profileRes


def update_user(db: Session, db_user: int, user: schemas.UserUpdate):
    profile = db.query(models.Profile).filter(models.Profile.user_id == db_user).first()
    profile.first_name = user.firstName
    profile.last_name = user.lastName
    profile.bio = user.bio
    db.commit()
    db.refresh(profile)
    return profile


def update_user_pic(db: Session, db_user: int, pic: schemas.ProfilePicture):
    if pic is None:
        pic = dumps(pic)
    profile = db.query(models.Profile).filter(models.Profile.user_id == db_user).first()
    print(profile, 'pic')
    profile.pic_url = pic
    db.commit()
    db.refresh(profile)
    return profile