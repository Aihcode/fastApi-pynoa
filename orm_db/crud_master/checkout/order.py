from sqlalchemy.orm import Session
from ... import models, schemas



def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order_by_id(db: Session, order_id: int):
    return (
        db.query(models.Order).filter(models.Order.id == order_id).first()
    )


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    counter = db.query(models.Order).count()
    data = db.query(models.Order).offset(skip).limit(limit)
    counterByFilters = data.count()
    return {
        "data": data.all(),
        "counter_orders": counter,
        "current_counter_show": counterByFilters,
    }


def get_orders_by_customer_id(db: Session, customer_id: int, skip: int = 0, limit: int = 100):
    counter = db.query(models.Order).filter(models.Order.customer_id == customer_id).count()
    data = db.query(models.Order).filter(models.Order.customer_id == customer_id).offset(skip).limit(limit)
    counterByFilters = data.count()
    return {
        "data": data.all(),
        "counter_orders": counter,
        "current_counter_show": counterByFilters,
    }


def get_orders_by_status(db: Session, status: str, skip: int = 0, limit: int = 100):
    counter = db.query(models.Order).filter(models.Order.status == status).count()
    data = db.query(models.Order).filter(models.Order.status == status).offset(skip).limit(limit)
    counterByFilters = data.count()
    return {
        "data": data.all(),
        "counter_orders": counter,
        "current_counter_show": counterByFilters,
    }


def cancel_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    db_order.is_cancelled = True
    db.commit()

    __delete_order_items_by_order_id__(db, order_id)

    return db_order


def update_order(db: Session, order_id: int, order: schemas.OrderUpdate):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    db_order.status = order.status or db_order.status
    db_order.is_cancelled = order.is_cancelled or db_order.is_cancelled
    db_order.is_paid = order.is_paid or db_order.is_paid
    db_order.is_shipped = order.is_shipped or db_order.is_shipped
    db_order.is_delivered = order.is_delivered or db_order.is_delivered
    db_order.is_processing = order.is_processing or db_order.is_processing
    db_order.is_preorder = order.is_preorder or db_order.is_preorder
    db_order.is_credit = order.is_credit or db_order.is_credit
    db_order.on_hold = order.is_on_hold or db_order.on_hold
    db.commit()
    db.refresh(db_order)
    return db_order


def add_order_items(db: Session, order_id: int, order_items: schemas.OrderItemCreate):
    db_order_items = models.OrderItem(**order_items.dict(), order_id=order_id)
    db.add(db_order_items)
    db.commit()
    db.refresh(db_order_items)
    return db_order_items

def get_order_items_by_order_id(db: Session, order_id: int):
    return db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id)

def update_order_item(db: Session, order_item_id: int, order_item: schemas.OrderItemUpdate):
    db_order_item = db.query(models.OrderItem).filter(models.OrderItem.id == order_item_id).first()
    db_order_item.quantity = order_item.quantity or db_order_item.quantity
    db_order_item.price = order_item.price or db_order_item.price
    db.commit()
    db.refresh(db_order_item)
    return db_order_item


def delete_order_item_by_id(db: Session, item_id: int):
    db.query(models.Order).filter(models.OrderItem.id == item_id).delete()
    db.commit()

def __delete_order_items_by_order_id__(db: Session, order_id: int):
    db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).delete()
    db.commit()


def order_json(db: Session, order_id: int):
    header = db.query(models.Order).filter(models.Order.id == order_id).first()
    body = db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).all()

    return {
        "header": header,
        "body": body,
        "footer": [
            {
                "order_id": order_id,
                "customer_id": header.customer_id,
                "status": header.status,
                "is_cancelled": header.is_cancelled,
                "is_paid": header.is_paid,
                "is_shipped": header.is_shipped,
                "is_delivered": header.is_delivered,
                "is_processing": header.is_processing,
                "is_preorder": header.is_preorder,
                "is_credit": header.is_credit,
                "on_hold": header.on_hold,
                "created_at": header.created_at,
                "updated_at": header.updated_at,
                "counter_items": len(body),
                "total": sum([item.price * item.quantity for item in body]),
            }
        ]
    }