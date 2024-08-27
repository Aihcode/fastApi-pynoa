from sqlalchemy.orm import Session

from ... import models, schemas
from ..private import __get_categories_from_mapper__, __get_tags_from_mapper__, __get_variants__
from payments.stripe import gateway as stripe
from json import dumps
from pydash import omit
from datetime import datetime
import re

def create_product(db: Session, product: schemas.Product):
    # validate categories exists in the database
    categories = []
    if len(product.categories_list) > 0:
        for category_id in product.categories_list:
            category = (
                db.query(models.Category)
                .filter(models.Category.id == category_id)
                .first()
            )
            if category:
                categories.append(category.id)

    # validate tags exists in the database
    tags = []
    if len(product.tags_list) > 0:
        for tag_id in product.tags_list:
            tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
            if tag:
                tags.append(tag.id)        

    # create product
    db_product = models.Product(
        name=product.name,
        handle=(product.name).replace('/[^a-z0-9]+/g', "-").lower(),
        description=product.description,
        cost=product.cost,
        categories_list=dumps(categories),
        tags_list=dumps(tags)
    )
    
    db.add(db_product)
    db.commit()
    product_created = db_product
    db.refresh(db_product)

    

    # create product variants
    #stripe.create_price(id=db_product.stripe_product_id, price=product.cost)
    defaut_variant = models.ProductVariant(
        title="Default Title",
        price=0,
    )
    db.add(defaut_variant)
    db.commit()
    db.refresh(defaut_variant)

    default_inventory_location = db.query(models.InventoryLocation).limit(1).first()
    db.add(default_inventory_location)
    db.commit()
    db.refresh(default_inventory_location)

    
    db_inventory = models.Inventory(
           product_id=db_product.id,
           inventory_location_id=default_inventory_location.id,
           product_variant_id=defaut_variant.id,
           quantity=0,
           cancelled=False,
           removed=False,
           sales=0,
           lat=0,
           lng=0
      )
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)

    return {
        "message": "Product created",
        "id": db_product.id,
        "title": db_product.name,
        "created_at": db_product.created_at
    }

def update_product(db: Session, product: schemas.Product, product_id: int):
    db_product = (
        db.query(models.Product).filter(models.Product.id == product_id).first()
    )

    # get categories and tags

    # validate categories exists in the database
    categories_updated = []
    if len(product.categories_list) > 0:
        for category_id in product.categories_list:
            category = (
                db.query(models.Category)
                .filter(models.Category.id == category_id)
                .first()
            )
            if category:
                categories_updated.append(category.id)

    # validate tags exists in the database
    tags_updated = []
    if len(product.tags_list) > 0:
        for tag_id in product.tags_list:
            tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
            if tag:
                tags_updated.append(tag.id)

    db_product.name = product.name or db_product.name
    db_product.description = product.description or db_product.description
    db_product.cost = product.cost or db_product.cost
    db_product.categories_list = dumps(list(set(categories_updated)))
    db_product.tags_list = dumps(list(set(tags_updated)))
    db_product.updated_at = datetime.now() or db_product.updated_at
    db.commit()
    db.refresh(db_product)

    # update product on stripe
    try:
        stripe.update_product(db_product)
    except Exception as e:
        print(e)

    return db_product

def get_product(db: Session, product_id: int, omit_list: list = [], omit_into_variants: list = []):
    data = db.query(models.Product).filter(models.Product.id == product_id).first()

    if data:

        categories = __get_categories_from_mapper__(db, data.categories_list)
        tags = __get_tags_from_mapper__(db, data.tags_list)
        variants = __get_variants__(db, data, data.cost, omit_into_variants)

        predata = {
            "id": data.id,
            "name": data.name,
            "description": data.description,
            "cost": data.cost,
            "stripe_product_id": data.stripe_product_id,
            "categories": categories,
            "tags": tags,
            "variants": variants,
        }

        predata = omit(predata, omit_list)

        return predata

def get_products(db: Session, keyword: str = "", skip: int = 0, limit: int = 10, omit_list: list = [], omit_into_variants: list = []):
    counter = db.query(models.Product).count()
    if keyword != "":
        data = db.query(models.Product).filter(models.Product.name.contains(keyword)).offset(skip).limit(limit)
    else:
        data = db.query(models.Product).offset(skip).limit(limit)
    predata = []
    estimated_value = 0
    stock_value = 0
    stock_counter = 0
    if data:
        for product in data:
            categories = __get_categories_from_mapper__(db, product.categories_list)
            tags = __get_tags_from_mapper__(db, product.tags_list)
            variants = __get_variants__(db, product, product.cost, omit_into_variants)
            stripe_id = product.stripe_product_id

            prodata = {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "cost": product.cost,
                "stripe_product_id": stripe_id,
                "categories": categories,
                "tags": tags,
                "variants": variants,
            }

            # Get total stock value and total quantity of inventory
            for variant in variants:
                stock_value += variant["stock_value"]
                estimated_value += variant["estimated_sales"]
                stock_counter += variant["inventory"][0]["quantity"]


            prodata = omit(prodata, omit_list)
            predata.append(prodata)

    counterByFilters = data.count()
    return {
        "data": predata,
        "counter_products": counter,
        "current_counter_show": counterByFilters,
        "estimated_value": estimated_value,
        "stock_value": stock_value,
        "stock_counter": stock_counter,
    }

def delete_product(db: Session, product_id: int):
    db_product = (
        db.query(models.Product).filter(models.Product.id == product_id).first()
    )
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted", "id": product_id, "title": db_product.title}
