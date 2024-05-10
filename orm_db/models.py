from sqlalchemy import Boolean, DateTime, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    __allow_unmapped__ = True
    id = Column(Integer, primary_key=True)
    email = Column(String(400), unique=True, index=True)
    profile_id = Column(Integer, nullable=True)
    hashed_password = Column(String(800))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    is_client = Column(Boolean, default=True)
    last_access = Column(DateTime, default=datetime.now())
    token = Column(String(800))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class Profile(Base):
    __tablename__ = "profiles"
    __allow_unmapped__ = True
    id = Column(Integer, primary_key=True)
    first_name = Column(String(400))
    last_name = Column(String(400))
    bio = Column(String(800))
    pic_url = Column(String(800))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())



class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    title = Column(String(400))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    title = Column(String(400))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class ProductVariant(Base):
    __tablename__ = "product_variants"
    id = Column(Integer, primary_key=True)
    title = Column(String(400))
    price = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class ProductOption(Base):
    __tablename__ = "product_options"
    id = Column(Integer, primary_key=True)
    variant = Column(Integer, ForeignKey("product_variants.id"))
    title = Column(String(400))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class InventoryLocation(Base):
    __tablename__ = "inventory_locations"
    id = Column(Integer, primary_key=True)
    title = Column(String(400))
    address = Column(String(800))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

class inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True)
    inventory_location_id = Column(Integer, ForeignKey("inventory_locations.id"))
    product_variant_id = Column(Integer, ForeignKey("product_variants.id"))
    quantity = Column(Integer)
    cancelled = Column(Integer)
    removed = Column(Integer)
    sales = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    title = Column(String(400))
    description = Column(String(800))
    cost = Column(Integer)
    categories_list = Column(String(800))
    tags_list = Column(String(800))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    order_number = Column(String(400))
    amount = Column(Float)
    discount = Column(Float)
    local_tax = Column(Float)
    products = Column(String(800))
    address = Column(String(800))
    email = Column(String(400))
    date_expiration = Column(DateTime, default=datetime.now())
    date_payment = Column(DateTime, default=datetime.now())
    payment = Column(String(800))
    phoneNumber = Column(String(400))
    is_credit = Column(Boolean, default=False)
    is_preorder = Column(Boolean, default=False)
    is_paid = Column(Boolean, default=False)
    is_delivered = Column(Boolean, default=False)
    is_cancelled = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Float)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())



class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    payment_method = Column(String(800))
    payment_status = Column(String(800))
    created_at = Column(DateTime, default=datetime.now())