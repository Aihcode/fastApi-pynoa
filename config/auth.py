from datetime import datetime, timedelta, timezone
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from orm_db import models
from orm_db.crud import get_user_by_email as get_user_db
from helpers.passwordgen import get_password_hash, verify_password
from helpers.getdb import get_db
from json import dumps, loads
import os

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

UserDb = Annotated[models.User, Depends(get_user_db)]

class Token(BaseModel):
    token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None

class User(BaseModel):
    email: str
    profile_id: int

class UserRole(BaseModel):
    id: int
    is_admin: bool
    is_client: bool
    is_active: bool

class Profile(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    bio: str
    pic_url: str
    

class CustomProfile(Profile):
    is_admin: bool
    is_client: bool
    is_active: bool
    message: str

class UserInDB(User):
    hashed_password: str

class UserLoggedIn(User):
    token: str
    profile_id: int

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




def get_user(db, email: str):
    checkUser = get_user_db(db, email=email)
    return checkUser


def authenticate_user(db, username: str, password: str):
    user = get_user(db, email=username)
    print(user.id, user.hashed_password, get_password_hash(password + "notreallyhashed"), password, 'pre-verify')
    if not user:
        return False
    if not verify_password(password + "notreallyhashed", user.hashed_password):
        return False
    return user


def create_access_token(db, data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    if encoded_jwt is not None:
        db.query(models.User).filter(models.User.email == data['sub']).update({models.User.last_access: datetime.now(timezone.utc), models.User.token: encoded_jwt})
        db.commit()
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session=Depends(get_db)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(email=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    profileData = {
        'id': 0,
        'user_id': 0,
        'first_name': '',
        'last_name': '',
        'bio': '',
        'pic_url': '',
        'teams': [],
        'is_admin': False,
        'is_client': False,
        'is_active': False,
        'message': 'User Profile Not Found'
    }
    profile = db.query(models.Profile).filter(models.Profile.user_id == user.id).first()
    
    if profile is not None and user is not None:

        profilePic = ('https://ui-avatars.com/api/?name=%s+%s&format=svg&size=128') % (profile.first_name, profile.last_name)
        if profile.pic_url is not None:
            profilePic = str(profile.pic_url).replace('./', os.getenv('SERVER_URL') + '/')

        profileData = {
            'id': profile.id,
            'user_id': profile.user_id,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'bio': profile.bio,
            'pic_url': profilePic,
            'teams': [],
            'is_admin': user.is_admin,
            'is_client': user.is_client,
            'is_active': user.is_active,
            'message': 'User Profile Found'
        }
   
    return profileData


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user




async def get_current_user_role(token: Annotated[str, Depends(oauth2_scheme)], db: Session=Depends(get_db)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(email=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
   
    return user


async def get_current_active_user_role(
    current_user: Annotated[UserRole, Depends(get_current_user_role)],
):
    return current_user