from sqlalchemy import (
    Boolean,
    DateTime,
    Column,
    ForeignKey,
    Integer,
    BigInteger,
    String,
    Float,
)
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
    validatetion_code = Column(String(800))
    is_verified = Column(Boolean, default=False)
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


class TeamMember(Base):
    __tablename__ = "team_members"
    __allow_unmapped__ = True
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))
    role = Column(String(800))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class Team(Base):
    __tablename__ = "teams"
    __allow_unmapped__ = True
    id = Column(Integer, primary_key=True)
    name = Column(String(400))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class Collection(Base):
    __tablename__ = "collections"
    id = Column(Integer, primary_key=True)
    title = Column(String(400))
    description = Column(String(800))
    category_condition = Column(String(800))
    category_id = Column(Integer, ForeignKey("categories.id"))
    tag_condition = Column(String(800))
    tag_id = Column(Integer, ForeignKey("tags.id"))
    sort_by = Column(String(800))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    title = Column(String(400))
    description = Column(String(800))
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
    price = Column(Float)
    currency_base = Column(String(75))
    media_id = Column(Integer, ForeignKey("media_galleries.id"))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class InventoryLocation(Base):
    __tablename__ = "inventory_locations"
    id = Column(Integer, primary_key=True)
    title = Column(String(400))
    address = Column(String(800))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    inventory_location_id = Column(Integer, ForeignKey("inventory_locations.id"))
    product_variant_id = Column(Integer, ForeignKey("product_variants.id"))
    quantity = Column(Integer)
    cancelled = Column(Integer)
    removed = Column(Integer)
    sales = Column(Integer)
    lat = Column(Float)
    lng = Column(Float)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(400))
    handle = Column(String(400), unique=True, index=True)
    description = Column(String(800))
    cost = Column(Float)
    categories_list = Column(String(800))
    tags_list = Column(String(800))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class ProductOption(Base):
    __tablename__ = "product_options"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    title = Column(String(400))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    email = Column(String(400), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    order_number = Column(String(400))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    amount = Column(Float)
    discount = Column(Float)
    local_tax = Column(Float)
    address = Column(String(800))
    email = Column(String(400))
    date_expiration = Column(DateTime, default=datetime.now())
    date_payment = Column(DateTime, default=datetime.now())
    payment = Column(String(800))
    phoneNumber = Column(String(400))
    status = Column(String(800))
    on_hold = Column(Boolean, default=True)
    is_shipped = Column(Boolean, default=False)
    is_credit = Column(Boolean, default=False)
    is_preorder = Column(Boolean, default=False)
    is_paid = Column(Boolean, default=False)
    is_processing = Column(Boolean, default=False)
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


class InvoiceCounter(Base):
    __tablename__ = "invoice_counters"
    id = Column(Integer, primary_key=True)
    invoice_number = Column(Integer)
    prefix = Column(String(800))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True)
    invoice_number = Column(String(800), index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    amount = Column(Float)
    discount = Column(Float)
    local_tax = Column(Float)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

class ShippingDelivery(Base):
    __tablename__ = "shipping_deliveries"
    id = Column(Integer, primary_key=True)
    title = Column(String(400))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class ShippingDeliveryRate(Base):
    __tablename__ = "shipping_deliveries_rates"
    id = Column(Integer, primary_key=True)
    shipping_delivery_id = Column(Integer, ForeignKey("shipping_deliveries.id"))
    price = Column(Float)
    by_weight = Column(Boolean, default=False)
    weight = Column(Float)
    weight_unit = Column(String(800))
    by_volume = Column(Boolean, default=False)
    volume = Column(Float)
    volume_unit = Column(String(800))
    by_flat_rate = Column(Boolean, default=False)
    by_quantity = Column(Boolean, default=False)
    quantity = Column(Float)
    discount = Column(Float)
    discount_type = Column(String(800))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class ShippingDeliveryTransaction(Base):
    __tablename__ = "shipping_addresses_transactions"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    address = Column(String(800))
    lat = Column(Float)
    lng = Column(Float)
    shipping_delivery_id = Column(Integer, ForeignKey("shipping_deliveries.id"))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class PaymentTransaction(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    payment_method = Column(String(800))
    payment_status = Column(String(800))
    created_at = Column(DateTime, default=datetime.now())


class PaymentMethod(Base):
    __tablename__ = "payment_methods"
    id = Column(Integer, primary_key=True)
    title = Column(String(400))
    username = Column(String(400))
    password = Column(String(800))
    secret_key = Column(String(800))
    public_key = Column(String(800))
    jwt_key = Column(String(800))
    payment_type = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class PaymentType(Base):
    __tablename__ = "payment_types"
    id = Column(Integer, primary_key=True)
    title = Column(String(400))
    method_auth = Column(String(800))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class MediaGallery(Base):
    __tablename__ = "media_galleries"
    id = Column(Integer, primary_key=True)
    linked_id = Column(Integer)  # product id, category id
    linked_type = Column(String(800))  # product, category
    media_url = Column(String(800))
    path = Column(String(800))
    alt = Column(String(800))
    name = Column(String(800))
    size = Column(BigInteger)
    mime_type = Column(String(800))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
