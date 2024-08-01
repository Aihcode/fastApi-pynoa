from sqlalchemy.orm import Session

from ... import models, schemas
from ..private import __get_categories_from_mapper__, __get_tags_from_mapper__, __get_variants__
from json import dumps
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
        handle=re.sub('\W+','', product.name).replace(" ", "-"),
        description=product.description,
        cost=product.cost,
        categories_list=dumps(categories),
        tags_list=dumps(tags),
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    # create product variants

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

    return db_product

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
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int):
    data = db.query(models.Product).filter(models.Product.id == product_id).first()

    if data:

        categories = __get_categories_from_mapper__(db, data.categories_list)
        tags = __get_tags_from_mapper__(db, data.tags_list)
        variants = __get_variants__(db, product_id, data.cost)

        predata = {
            "id": data.id,
            "name": data.name,
            "description": data.description,
            "cost": data.cost,
            "categories": categories,
            "tags": tags,
            "variants": variants,
        }
        return predata

def get_products(db: Session, skip: int = 0, limit: int = 10):
    counter = db.query(models.Product).count()
    data = db.query(models.Product).offset(skip).limit(limit)
    predata = []
    estimated_value = 0
    stock_value = 0
    stock_counter = 0
    if data:
        for product in data:
            categories = __get_categories_from_mapper__(db, product.categories_list)
            tags = __get_tags_from_mapper__(db, product.tags_list)
            variants = __get_variants__(db, product.id, product.cost)

            prodata = {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "cost": product.cost,
                "categories": categories,
                "tags": tags,
                "variants": variants,
            }

            # Get total stock value and total quantity of inventory
            for variant in variants:
                stock_value += variant["stock_value"]
                estimated_value += variant["estimated_sales"]
                stock_counter += variant["inventory"][0]["quantity"]

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
