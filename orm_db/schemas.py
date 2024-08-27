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
    id: int
    email: str
    is_active: bool

    class Config:
        orm_model = True


class MediaView(BaseModel):
    id: int
    url: str
    size: int
    type: str
    path: str
    name: str

    class Config:
        orm_model = True


class ProfilePicture(BaseModel):
    pic_url: str


class Profile(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    bio: str
    pic_url: str

    class Config:
        orm_model = True


class Category(BaseModel):
    title: str
    description: str

    class Config:
        orm_model = True


class Tag(BaseModel):
    title: str


class ObjectByPagination(BaseModel):
    limit: int
    skip: int

class ObjectByPaginationwithFilter(BaseModel):
    limit: int
    skip: int
    keyword: str


class ObjectID(BaseModel):
    id: int


class Collection(BaseModel):
    title: str
    description: str
    category_condition: str
    category_id: int
    tag_condition: str
    tag_id: int
    sort_by: str

    class Config:
        orm_model = True


class Product(BaseModel):
    name: str
    description: str
    cost: float
    categories_list: list
    tags_list: list

    class Config:
        orm_model = True


class ProductView(BaseModel):
    id: int
    title: str
    description: str
    cost: float
    categories: list
    tags: list

    class Config:
        orm_model = True


class Inventory(BaseModel):
    product_id: int
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
    title: str
    address: str

    class Config:
        orm_model = True


class ProductVariant(BaseModel):
    title: str
    price: float
    currency_base: str

    class Config:
        orm_model = True


class ProductOption(BaseModel):
    variant: int
    title: str

    class Config:
        orm_model = True


class Team(BaseModel):
    name: str
    created_at: str
    updated_at: str

    class Config:
        orm_model = True


class TeamMember(BaseModel):
    user_id: int
    team_id: int
    role: str  # admin, member, moderator

    class Config:
        orm_model = True


class PaymentTypeCreate(BaseModel):
    name: str
    description: str
    created_at: str
    updated_at: str

    class Config:
        orm_model = True


class PaymentType(BaseModel):
    id: int
    name: str
    description: str
    created_at: str
    updated_at: str

    class Config:
        orm_model = True


class PaymentMethodCreate(BaseModel):
    name: str
    description: str
    created_at: str
    updated_at: str
    payment_type: int

    class Config:
        orm_model = True


class PaymentMethod(BaseModel):
    id: int
    name: str
    description: str
    created_at: str
    updated_at: str
    payment_type: int

    class Config:
        orm_model = True


class PaymentTransaction(BaseModel):
    id: int
    payment_method: int
    amount: float
    created_at: str
    updated_at: str

    class Config:
        orm_model = True


class PaymentTransactionCreate(BaseModel):
    payment_method: int
    amount: float
    created_at: str
    updated_at: str


class ShippingDeliveryRateCreate(BaseModel):
    name: str
    price: float
    created_at: str
    updated_at: str

    class Config:
        orm_model = True


class ShippingDeliveryCreate(BaseModel):
    title: str
    created_at: str
    updated_at: str


class ShippingDeliveryTransactionCreate(BaseModel):
    order_id: int
    address: str
    lat: float
    lng: float
    shipping_delivery_id: int
    created_at: str
    updated_at: str



class OrderCreate(BaseModel):
    user_id: int
    created_at: str
    updated_at: str

class OrderUpdate(BaseModel):
    user_id: int

class OrderItemCreate(BaseModel):
    order_id: int


class OrderItemUpdate(BaseModel):
    order_id: int


class InvoiceCreate(BaseModel):
    invoice_number: str
    order_id: int
    amount: float
    discount: float
    local_tax: float
    created_at: str
    updated_at: str

class InvoiceFilter(BaseModel):
    invoice_number: str
    order_id: int
    created_at: str
    updated_at: str


class MailNotification(BaseModel):
    title: str
    from_param: str
    to_list: list
    subject: str
    body: str
    token: str
    created_at: str
    updated_at: str


class MailNotificationCreate(MailNotification):
    user_id: int