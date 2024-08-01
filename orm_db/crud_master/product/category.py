from sqlalchemy.orm import Session

from ... import models, schemas
from ..private import __get_categories_from_mapper__, __get_tags_from_mapper__, __get_variants__
from datetime import datetime

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