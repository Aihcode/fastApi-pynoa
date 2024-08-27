from sqlalchemy.orm import Session

from . import models, schemas
from helpers.passwordgen import get_password_hash
from helpers.encryptgen import get_hashed_name
from json import dumps, loads
from datetime import datetime
from random import random, choice
import os
import re


from .crud_master.private import __get_categories_from_mapper__, __get_tags_from_mapper__, __get_variants__

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


def create_inventory(db: Session, inventory: schemas.Inventory):
    db_inventory = models.Inventory(
        product_id=inventory.product_id,
        inventory_location_id=inventory.inventory_location_id, 
        product_variant_id=inventory.product_variant_id,
        quantity=inventory.quantity or 0, 
        cancelled=inventory.cancelled or 0, 
        removed=inventory.removed or 0, 
        sales=inventory.sales or 0, 
        lat=inventory.lat, 
        lng=inventory.lng
    )
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def update_inventory(db: Session, inventory: schemas.Inventory, inventory_id: int):
    db_inventory = (
        db.query(models.Inventory)
        .filter(models.Inventory.id == inventory_id)
        .first()
    )

    quantityStock = inventory.quantity or db_inventory.quantity
    
    if inventory.quantity == 0:
        quantityStock = -1

    db_inventory.inventory_location_id = inventory.inventory_location_id or db_inventory.inventory_location_id
    db_inventory.product_variant_id = inventory.product_variant_id or db_inventory.product_variant_id
    db_inventory.quantity = quantityStock
    db_inventory.cancelled = inventory.cancelled or db_inventory.cancelled
    db_inventory.removed = inventory.removed or db_inventory.removed
    db_inventory.sales = inventory.sales or db_inventory.sales
    db_inventory.lat = inventory.lat or db_inventory.lat
    db_inventory.lng = inventory.lng or db_inventory.lng
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def get_inventory(db: Session, inventory_id: int):
    return (
        db.query(models.Inventory)
        .filter(models.Inventory.id == inventory_id)
        .first()
    )

def get_inventories(db: Session, skip: int = 0, limit: int = 10):
    counter = db.query(models.Inventory).count()
    data = db.query(models.Inventory).offset(skip).limit(limit)
    counterByFilters = data.count()
    return {
        "data": data,
        "counter_inventories": counter,
        "current_counter_show": counterByFilters,
    }

def delete_inventory(db: Session, inventory_id: int):
    db_inventory = (
        db.query(models.Inventory)
        .filter(models.Inventory.id == inventory_id)
        .first()
    )
    db.delete(db_inventory)
    db.commit()
    return {
        "message": "Inventory deleted",
        "id": inventory_id,
        "title": db_inventory.title,
    }

def create_product_variant(db: Session, product_variant: schemas.ProductVariant):
    db_product_variant = models.ProductVariant(
        title=product_variant.title, price=product_variant.price, currency_base=product_variant.currency_base
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
    db_product_variant.currency_base = product_variant.currency_base or db_product_variant.currency_base
    db.commit()
    db.refresh(db_product_variant)
    return db_product_variant


def get_product_variant(db: Session, product_variant_id: int):
    return (
        db.query(models.ProductVariant)
        .filter(models.ProductVariant.id == product_variant_id)
        .first()
    )


def get_product_variants(db: Session,variant_id: int = 0):
    data = db.query(models.ProductVariant).filter(models.ProductVariant.id == variant_id)
    return data


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



def create_team(db: Session, team: schemas.Team):
    db_team = models.Team(name=team.name)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


def update_team(db: Session, team: schemas.Team, team_id: int):
    db_team = db.query(models.Team).filter(models.Team.id == team_id).first()
    db_team.name = team.name or db_team.name
    db.commit()
    db.refresh(db_team)
    return db_team


def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.id == team_id).first()


def get_teams(db: Session, skip: int = 0, limit: int = 10):
    counter = db.query(models.Team).count()
    data = db.query(models.Team).offset(skip).limit(limit)
    counterByFilters = data.count()
    return {
        "data": data,
        "counter_teams": counter,
        "current_counter_show": counterByFilters,
    }

def create_team_member(db: Session, team_member: schemas.TeamMember):
    db_team_member = models.TeamMember(
        user_id=team_member.user_id, team_id=team_member.team_id, role=team_member.role
    )
    ID = db.query(models.Team).filter(models.Team.id == team_member.team_id).first().id

    if ID != int(team_member.team_id):
        return {"message": "Team does not exist"}
    
    db.add(db_team_member)
    db.commit()
    db.refresh(db_team_member)
    return db_team_member


def update_team_member(db: Session, team_member: schemas.TeamMember, team_member_id: int):
    db_team_member = (
        db.query(models.TeamMember)
        .filter(models.TeamMember.id == team_member_id)
        .first()
    )
    db_team_member.user_id = team_member.user_id or db_team_member.user_id
    db_team_member.team_id = team_member.team_id or db_team_member.team_id
    db_team_member.role = team_member.role or db_team_member.role

    ID = db.query(models.Team).filter(models.Team.id == team_member.team_id).first().id

    if ID != int(team_member.team_id):
        return {"message": "Team does not exist"}
    

    db.commit()
    db.refresh(db_team_member)
    return db_team_member


def get_team_member(db: Session, team_member_id: int):
    return (
        db.query(models.TeamMember)
        .filter(models.TeamMember.id == team_member_id)
        .first()
    )


def get_team_members(db: Session, skip: int = 0, limit: int = 10):
    counter = db.query(models.TeamMember).count()
    data = db.query(models.TeamMember).offset(skip).limit(limit)
    counterByFilters = data.count()
    return {
        "data": data,
        "counter_team_members": counter,
        "current_counter_show": counterByFilters,
    }

def __file_upload__(file, format_target: str):
    basePatch = './static/uploads/media/'
    if not os.path.exists(basePatch):
        os.mkdir(basePatch)
        pass

    fileType = '.webp'

    if len(format_target) > 0:
        fileType = '.' + format_target
    

    randomId = random()
    randomChoice = choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
    hashedName = get_hashed_name(str(randomId) + randomChoice + file.filename) + fileType
    fileUpload = os.path.join(basePatch, hashedName.replace('', ''))
    with open(fileUpload, "wb") as buffer:
        while contents := file.file.read(1024 * 1024):
            buffer.write(contents)

    return {
        "name": hashedName,
        "url": fileUpload,
        "type": fileType,
        "size": os.path.getsize(fileUpload),
        "path": basePatch,
        "format": format_target,
        "uuid": get_hashed_name(str(randomId) + randomChoice + file.filename)
    }

def upload_media(db: Session, user_id: int = 1, media: any = None, media_json: str = None):
    media_json = loads(media_json)
    if media:
        db_media = models.MediaGallery(
            name=media_json["name"],
            alt=( "%s - %s" % (media_json["name"], "pynoa media")),
            media_url=media_json["url"],
            mime_type=media_json["type"],
            size=media_json["size"],
            path=media_json["path"],
            user_id=user_id
        )
        db.add(db_media)
        db.commit()
        db.refresh(db_media)
        return {
        "id": db_media.id,
        "url": db_media.media_url,
        "type": db_media.mime_type,
        "size": db_media.size,
        "path": db_media.path,
        "name": db_media.name,
        "user": get_user(db, user_id)
    }
    


def get_media(db: Session, media_id: int):
    return db.query(models.MediaGallery).filter(models.MediaGallery.id == media_id).first()


def get_mediaGallery(db: Session, skip: int = 0, limit: int = 10):
    counter = db.query(models.MediaGallery).count()
    data = db.query(models.MediaGallery).offset(skip).limit(limit)
    counterByFilters = data.count()
    return {
        "data": data.all(),
        "counter_medias": counter,
        "current_counter_show": counterByFilters,
    }


def delete_media(db: Session, media_id: int):
    db_media = db.query(models.MediaGallery).filter(models.MediaGallery.id == media_id).first()
    temp_media = db_media
    db.delete(db_media)
    db.commit()

    if os.path.exists(db_media.path):
        os.remove(db_media.path)
    pass

    return {
        "id": media_id,
        "message": "Media deleted successfully",
        "deleted_media_resource": temp_media
    }


def get_mail_notifications(db: Session, is_validated: bool = False, skip: int = 0, limit: int = 10):
    counter = db.query(models.MailNotifications).count()
    data = db.query(models.MailNotifications).filter(models.MailNotifications.is_validated == is_validated).offset(skip).limit(limit)
    counterByFilters = data.count()
    return {
        "data": data.all(),
        "counter_mail_notifications": counter,
        "current_counter_show": counterByFilters,
    }


def get_mail_notification(db: Session, mail_notification_id: int):
    return db.query(models.MailNotifications).filter(
        models.MailNotifications.id == mail_notification_id
    ).first()


def create_mail_notification(db: Session, mail_notification: schemas.MailNotificationCreate):
    
    db_mail_notification = models.MailNotifications(
        from_param=mail_notification["from_param"],
        to_list=mail_notification["to_list"],
        subject=mail_notification["subject"],
        body=mail_notification["body"],
        token=mail_notification["token"],
        user_id=mail_notification["user_id"],
        is_validated=mail_notification["is_validated"]
    )
    db.add(db_mail_notification)
    db.commit()
    db.refresh(db_mail_notification)
    return db_mail_notification


def delete_mail_notification(db: Session, mail_notification_id: int):
    db_mail_notification = db.query(models.MailNotifications).filter(
        models.MailNotifications.id == mail_notification_id
    ).first()
    temp_mail_notification = db_mail_notification
    db.delete(db_mail_notification)
    db.commit()
    return {
        "id": mail_notification_id,
        "message": "Mail notification deleted successfully",
        "deleted_mail_notification_resource": temp_mail_notification
    }