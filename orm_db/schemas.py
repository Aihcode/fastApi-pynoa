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

class Category(BaseModel):
    title : str
    description : str

    class Config:
        orm_model = True

class Tag(BaseModel):
    title : str

class ObjectByPagination(BaseModel):
    limit : int
    skip : int

class ObjectID(BaseModel):
    id : int


class Collection(BaseModel):
    id : int
    title : str
    description : str
    category_condition : str
    category_id : int
    tag_condition : str
    tag_id : int
    sort_by : str

    class Config:
        orm_model = True

class Product(BaseModel):
    title : str
    description : str
    cost : float
    categories_list : list
    tags_list : list

    class Config:
        orm_model = True

class ProductView(BaseModel):
    id : int
    title : str
    description : str
    cost : float
    categories : list
    tags : list

    class Config:
        orm_model = True


class Inventory(BaseModel):
    id : int
    inventory_location_id: int
    product_variant_id: int
    quantity: int
    cancelled: int
    removed: int
    sales: int
    lat: float
    lng: float

    class Config:
        orm_model = True


class InventoryLocation(BaseModel):
    id : int
    title : str
    address : str

    class Config:
        orm_model = True

class ProductVariant(BaseModel):
    id: int
    title: str
    price: float

    class Config:
        orm_model = True

class ProductOption(BaseModel):
    id: int
    variant: int
    title: str
    

    class Config:
        orm_model = True