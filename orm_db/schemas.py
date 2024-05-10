from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    lastName: str
    firstName: str
    bio: str
    pass 

class UserUpdate(BaseModel):
    lastName: str
    firstName: str
    bio: str
    pass

class UserPassword(BaseModel):
    password: str
    pass

class User(UserBase):
    id : int
    email : str
    is_active : bool

    class Config:
        orm_model = True


class ProfilePicture(BaseModel):
    pic_url : str

class Profile(BaseModel):
    id : int
    user_id : int
    first_name : str
    last_name : str
    bio : str
    pic_url : str

    class Config:
        orm_model = True