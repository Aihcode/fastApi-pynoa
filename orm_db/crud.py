from sqlalchemy.orm import Session

from . import models, schemas
from helpers.passwordgen import get_password_hash
from json import dumps, loads
from datetime import datetime


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
        db_image_profile_default = (
            "https://ui-avatars.com/api/?name=%s+%s&format=svg&size=128"
        ) % (user.firstName, user.lastName)
        db_profile = models.Profile(
            first_name=user.firstName,
            last_name=user.lastName,
            bio=user.bio,
            pic_url=db_image_profile_default,
            user_id=db_user.id,
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
    profile.first_name = user.firstName or profile.first_name
    profile.last_name = user.lastName or profile.last_name
    profile.bio = user.bio or profile.bio
    db.commit()
    db.refresh(profile)
    return profile


def update_user_pic(db: Session, db_user: int, pic: schemas.ProfilePicture):
    if pic is None:
        pic = dumps(pic)
    profile = db.query(models.Profile).filter(models.Profile.user_id == db_user).first()
    print(profile, "pic")
    profile.pic_url = pic
    db.commit()
    db.refresh(profile)
    return profile


def create_category(db: Session, category: schemas.Category):
    db_category = models.Category(
        title=category.title, description=category.description
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(db: Session, category: schemas.Category, category_id: int):
    db_category = (
        db.query(models.Category).filter(models.Category.id == category_id).first()
    )
    db_category.title = category.title or db_category.title
    db_category.description = category.description or db_category.description
    db_category.updated_at = datetime.now()
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def get_categories(db: Session, skip: int = 0, limit: int = 10, keyword: str = ""):
    counter = db.query(models.Category).count()
    data = (
        db.query(models.Category)
        .filter(models.Category.title.contains(keyword))
        .offset(skip)
        .limit(limit)
    )
    counterByFilters = data.count()
    return {
        "data": data.all(),
        "counter_categories": counter,
        "current_counter_show": counterByFilters,
    }


def delete_category(db: Session, category_id: int):
    db_category = (
        db.query(models.Category).filter(models.Category.id == category_id).first()
    )
    db.delete(db_category)
    db.commit()
    return {
        "message": "Category deleted",
        "id": category_id,
        "title": db_category.title,
    }


def create_tag(db: Session, tag: schemas.Tag):
    db_tag = models.Tag(title=tag.title)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def update_tag(db: Session, tag_id: int, tag: schemas.Tag):
    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    db_tag.title = tag.title
    db.commit()
    db.refresh(db_tag)
    return db_tag


def get_tag(db: Session, tag_id: int):
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()


def get_tags(db: Session, skip: int = 0, limit: int = 10):
    counter = db.query(models.Tag).count()
    data = db.query(models.Tag).offset(skip).limit(limit)
    counterByFilters = data.count()
    return {
        "data": data.all(),
        "counter_tags": counter,
        "current_counter_show": counterByFilters,
    }


def delete_tag(db: Session, tag_id: int):
    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    db.delete(db_tag)
    db.commit()
    return {"message": "Tag deleted", "id": tag_id, "title": db_tag.title}


def create_collection(db: Session, collection: schemas.Collection):
    db_collection = models.Collection(
        title=collection.title,
        description=collection.description,
        category_condition=collection.category_condition,
        category_id=collection.category_id,
        tag_condition=collection.tag_condition,
        tag_id=collection.tag_id,
        sort_by=collection.sort_by,
    )
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    return db_collection


def update_collection(db: Session, collection: schemas.Collection):
    db_collection = (
        db.query(models.Collection)
        .filter(models.Collection.id == collection.id)
        .first()
    )
    db_collection.title = collection.title or db_collection.title
    db_collection.description = collection.description or db_collection.description
    db_collection.category_condition = (
        collection.category_condition or db_collection.category_condition
    )
    db_collection.tag_condition = (
        collection.tag_condition or db_collection.tag_condition
    )
    db_collection.sort_by = collection.sort_by or db_collection.sort_by
    db.commit()
    db.refresh(db_collection)
    return db_collection


def get_collection(db: Session, collection_id: int):
    return (
        db.query(models.Collection)
        .filter(models.Collection.id == collection_id)
        .first()
    )


def get_collections(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Collection).offset(skip).limit(limit).all()


def delete_collection(db: Session, collection_id: int):
    db_collection = (
        db.query(models.Collection)
        .filter(models.Collection.id == collection_id)
        .first()
    )
    db.delete(db_collection)
    db.commit()
    return {
        "message": "Collection deleted",
        "id": collection_id,
        "title": db_collection.title,
    }


def create_product(db: Session, product: schemas.Product):

    # get categories and tags

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
        title=product.title,
        description=product.description,
        cost=product.cost,
        categories_list=dumps(categories),
        tags_list=dumps(tags),
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
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

    db_product.title = product.title or db_product.title
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

        categories = []
        tags = []

        for category in loads(data.categories_list):
            category_load = (
                db.query(models.Category).filter(models.Category.id == category).first()
            )
            if category_load:
                categories.append(
                    {
                        "id": category_load.id,
                        "title": category_load.title,
                        "description": category_load.description,
                    }
                )

        for tag in loads(data.tags_list):
            tag_load = db.query(models.Tag).filter(models.Tag.id == tag).first()
            if tag_load:
                tags.append({"id": tag_load.id, "title": tag_load.title})

        predata = {
            "id": data.id,
            "title": data.title,
            "description": data.description,
            "cost": data.cost,
            "categories": categories,
            "tags": tags,
        }
        return predata


def get_products(db: Session, skip: int = 0, limit: int = 10):
    counter = db.query(models.Product).count()
    data = db.query(models.Product).offset(skip).limit(limit)
    predata = []
    if data:
        for product in data:
            categories = []
            tags = []

            for category in loads(product.categories_list):
                category_load = (
                    db.query(models.Category)
                    .filter(models.Category.id == category)
                    .first()
                )
                if category_load:
                    categories.append(
                        {
                            "id": category_load.id,
                            "title": category_load.title,
                            "description": category_load.description,
                        }
                    )

            for tag in loads(product.tags_list):
                tag_load = db.query(models.Tag).filter(models.Tag.id == tag).first()
                if tag_load:
                    tags.append({"id": tag_load.id, "title": tag_load.title})

            prodata = {
                "id": product.id,
                "title": product.title,
                "description": product.description,
                "cost": product.cost,
                "categories": categories,
                "tags": tags,
            }

            predata.append(prodata)

    counterByFilters = data.count()
    return {
        "data": predata,
        "counter_products": counter,
        "current_counter_show": counterByFilters,
    }


def delete_product(db: Session, product_id: int):
    db_product = (
        db.query(models.Product).filter(models.Product.id == product_id).first()
    )
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted", "id": product_id, "title": db_product.title}


def create_inventory_location(
    db: Session, inventory_location: schemas.InventoryLocation
):
    db_inventory_location = models.InventoryLocation(
        title=inventory_location.title, address=inventory_location.address
    )
    db.add(db_inventory_location)
    db.commit()
    db.refresh(db_inventory_location)
    return db_inventory_location


def update_inventory_location(
    db: Session, inventory_location: schemas.InventoryLocation
):
    db_inventory_location = (
        db.query(models.InventoryLocation)
        .filter(models.InventoryLocation.id == inventory_location.id)
        .first()
    )
    db_inventory_location.title = (
        inventory_location.title or db_inventory_location.title
    )
    db_inventory_location.address = (
        inventory_location.address or db_inventory_location.address
    )
    db.commit()
    db.refresh(db_inventory_location)
    return db_inventory_location


def get_inventory_location(db: Session, inventory_location_id: int):
    return (
        db.query(models.InventoryLocation)
        .filter(models.InventoryLocation.id == inventory_location_id)
        .first()
    )


def get_inventory_locations(db: Session, skip: int = 0, limit: int = 10):
    counter = db.query(models.InventoryLocation).count()
    data = db.query(models.InventoryLocation).offset(skip).limit(limit)
    counterByFilters = data.count()
    return {
        "data": data,
        "counter_locations": counter,
        "current_counter_show": counterByFilters,
    }


def delete_inventory_location(db: Session, inventory_location_id: int):
    db_inventory_location = (
        db.query(models.InventoryLocation)
        .filter(models.InventoryLocation.id == inventory_location_id)
        .first()
    )
    db.delete(db_inventory_location)
    db.commit()
    return {
        "message": "Inventory Location deleted",
        "id": inventory_location_id,
        "title": db_inventory_location.title,
    }


def create_product_variant(db: Session, product_variant: schemas.ProductVariant):
    db_product_variant = models.ProductVariant(
        title=product_variant.title, price=product_variant.price
    )
    db.add(db_product_variant)
    db.commit()
    db.refresh(db_product_variant)
    return db_product_variant


def update_product_variant(db: Session, product_variant: schemas.ProductVariant, id: int):
    db_product_variant = (
        db.query(models.ProductVariant)
        .filter(models.ProductVariant.id == id)
        .first()
    )
    db_product_variant.title = product_variant.title or db_product_variant.title
    db_product_variant.price = product_variant.price or db_product_variant.price
    db.commit()
    db.refresh(db_product_variant)
    return db_product_variant


def get_product_variant(db: Session, product_variant_id: int):
    return (
        db.query(models.ProductVariant)
        .filter(models.ProductVariant.id == product_variant_id)
        .first()
    )


def get_product_variants(db: Session, skip: int = 0, limit: int = 10):
    counter = db.query(models.ProductVariant).count()
    data = db.query(models.ProductVariant).offset(skip).limit(limit)
    counterByFilters = data.count()
    return {
        "data": data,
        "counter_variants": counter,
        "current_counter_show": counterByFilters,
    }


def delete_product_variant(db: Session, product_variant_id: int):
    db_product_variant = (
        db.query(models.ProductVariant)
        .filter(models.ProductVariant.id == product_variant_id)
        .first()
    )
    db.delete(db_product_variant)
    db.commit()
    return {
        "message": "Product Variant deleted",
        "id": product_variant_id,
        "title": db_product_variant.title,
    }


def create_product_option(db: Session, product_option: schemas.ProductOption):
    db_product_option = models.ProductOption(
        title=product_option.title, product_id=product_option.product_id
    )
    ID = db.query(models.Product).filter(models.Product.id == product_option.product_id).first().id

    if ID != int(product_option.product_id):
        return {"message": "Product does not exist"}
    
    db.add(db_product_option)
    db.commit()
    db.refresh(db_product_option)
    return db_product_option


def update_product_option(db: Session, product_option: schemas.ProductOption, option_id: int):
    db_product_option = (
        db.query(models.ProductOption)
        .filter(models.ProductOption.id == option_id)
        .first()
    )
    db_product_option.title = product_option.title or db_product_option.title
    db_product_option.product_id = (
        product_option.product_id or db_product_option.product_id
    )

    ID = db.query(models.Product).filter(models.Product.id == product_option.product_id).first().id

    if ID != int(product_option.product_id):
        return {"message": "Product does not exist"}

    db.commit()
    db.refresh(db_product_option)
    return db_product_option


def get_product_option(db: Session, product_option_id: int):
    return (
        db.query(models.ProductOption)
        .filter(models.ProductOption.id == product_option_id)
        .first()
    )


def get_product_options(db: Session, skip: int = 0, limit: int = 10):
    counter = db.query(models.ProductOption).count()
    data = db.query(models.ProductOption).offset(skip).limit(limit)
    counterByFilters = data.count()
    return {
        "data": data,
        "counter_options": counter,
        "current_counter_show": counterByFilters,
    }


def delete_product_option(db: Session, product_option_id: int):
    db_product_option = (
        db.query(models.ProductOption)
        .filter(models.ProductOption.id == product_option_id)
        .first()
    )
    db.delete(db_product_option)
    db.commit()
    return {
        "message": "Product Option deleted",
        "id": product_option_id,
        "title": db_product_option.title,
    }
