from sqlalchemy.orm import Session

from ... import models, schemas


def create(db: Session, tag: schemas.Tag):
    db_tag = models.Tag(title=tag.title)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def update(db: Session, tag_id: int, tag: schemas.Tag):
    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    db_tag.title = tag.title
    db.commit()
    db.refresh(db_tag)
    return db_tag


def get_one(db: Session, tag_id: int):
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


def delete(db: Session, tag_id: int):
    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    db.delete(db_tag)
    db.commit()
    return {"message": "Tag deleted", "id": tag_id, "title": db_tag.title}

