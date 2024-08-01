from sqlalchemy.orm import Session
from ... import models, schemas


def create_payment_type(db: Session, payment_type: schemas.PaymentTypeCreate):
    db_payment_type = models.PaymentType(**payment_type.dict())
    db.add(db_payment_type)
    db.commit()
    db.refresh(db_payment_type)
    return db_payment_type


def get_payment_type(db: Session, payment_type_id: int):
    return (
        db.query(models.PaymentType)
        .filter(models.PaymentType.id == payment_type_id)
        .first()
    )


def get_payment_types(db: Session, limit: int = 10, offset: int = 0):
    counter = db.query(models.PaymentType).count()
    data = db.query(models.PaymentType).offset(offset).limit(limit)
    counterByFilters = data.count()
    return {
        "data": data.all(),
        "counter_payment_types": counter,
        "current_counter_show": counterByFilters,
    }


def update_payment_type(
    db: Session, payment_type_id: int, payment_type: schemas.PaymentTypeCreate
):
    db_payment_type = get_payment_type(db, payment_type_id)
    if not db_payment_type:
        return None
    db_payment_type.name = payment_type.name
    db.commit()
    db.refresh(db_payment_type)
    return db_payment_type


def delete_payment_type(db: Session, payment_type_id: int):
    db_payment_type = get_payment_type(db, payment_type_id)
    if not db_payment_type:
        return None
    db.delete(db_payment_type)
    db.commit()
    return db_payment_type


def create_payment_method(db: Session, payment_method: schemas.PaymentMethodCreate):
    db_payment_method = models.PaymentMethod(**payment_method.dict())
    db.add(db_payment_method)
    db.commit()
    db.refresh(db_payment_method)
    return db_payment_method


def get_payment_method(db: Session, payment_method_id: int):
    return (
        db.query(models.PaymentMethod)
        .filter(models.PaymentMethod.id == payment_method_id)
        .first()
    )


def get_payment_methods(db: Session, limit: int = 10, offset: int = 0):
    counter = db.query(models.PaymentMethod).count()
    data = db.query(models.PaymentMethod).offset(offset).limit(limit)
    counterByFilters = data.count()
    return {
        "data": data.all(),
        "counter_payment_methods": counter,
        "current_counter_show": counterByFilters,
    }


def update_payment_method(
    db: Session, payment_method_id: int, payment_method: schemas.PaymentMethodCreate
):  # noqa
    db_payment_method = get_payment_method(db, payment_method_id)
    if not db_payment_method:
        return None
    db_payment_method.name = payment_method.name
    db.commit()
    db.refresh(db_payment_method)
    return db_payment_method


def delete_payment_method(db: Session, payment_method_id: int):
    db_payment_method = get_payment_method(db, payment_method_id)
    if not db_payment_method:
        return None
    db.delete(db_payment_method)
    db.commit()
    return db_payment_method


def create_payment_transaction(
    db: Session, payment_transaction: schemas.PaymentTransactionCreate
):
    db_payment_transaction = models.PaymentTransaction(**payment_transaction.dict())
    db.add(db_payment_transaction)
    db.commit()
    db.refresh(db_payment_transaction)
    return db_payment_transaction


def get_payment_transaction(db: Session, payment_transaction_id: int):
    return (
        db.query(models.PaymentTransaction)
        .filter(models.PaymentTransaction.id == payment_transaction_id)
        .first()
    )


def get_payment_transactions(db: Session, limit: int = 10, offset: int = 0):
    counter = db.query(models.PaymentTransaction).count()
    data = db.query(models.PaymentTransaction).offset(offset).limit(limit)
    counterByFilters = data.count()
    return {
        "data": data.all(),
        "counter_payment_transactions": counter,
        "current_counter_show": counterByFilters,
    }


def delete_payment_transaction(db: Session, payment_transaction_id: int):
    db_payment_transaction = get_payment_transaction(db, payment_transaction_id)
    if not db_payment_transaction:
        return None
    db.delete(db_payment_transaction)
    db.commit()
    return db_payment_transaction


def create_shipping_delivery_rate(
    db: Session, shipping_delivery_rate: schemas.ShippingDeliveryRateCreate
):
    db_shipping_delivery_rate = models.ShippingDeliveryRate(
        **shipping_delivery_rate.dict()
    )
    db.add(db_shipping_delivery_rate)
    db.commit()
    db.refresh(db_shipping_delivery_rate)
    return db_shipping_delivery_rate


def update_shipping_delivery_rate(
    db: Session,
    shipping_delivery_rate_id: int,
    shipping_delivery_rate: schemas.ShippingDeliveryRateCreate,
):
    db_shipping_delivery_rate = get_shipping_delivery_rate(
        db, shipping_delivery_rate_id
    )
    if not db_shipping_delivery_rate:
        return None
    db_shipping_delivery_rate.rate = shipping_delivery_rate.rate
    db.commit()
    db.refresh(db_shipping_delivery_rate)
    return db_shipping_delivery_rate


def get_shipping_delivery_rate(db: Session, shipping_delivery_rate_id: int):
    return (
        db.query(models.ShippingDeliveryRate)
        .filter(models.ShippingDeliveryRate.id == shipping_delivery_rate_id)
        .first()
    )


def get_shipping_delivery_rates(db: Session, limit: int = 10, offset: int = 0):
    counter = db.query(models.ShippingDeliveryRate).count()
    data = db.query(models.ShippingDeliveryRate).offset(offset).limit(limit)
    counterByFilters = data.count()
    return {
        "data": data.all(),
        "counter_shipping_delivery_rates": counter,
        "current_counter_show": counterByFilters,
    }


def delete_shipping_delivery_rate(db: Session, shipping_delivery_rate_id: int):
    db_shipping_delivery_rate = get_shipping_delivery_rate(
        db, shipping_delivery_rate_id
    )
    if not db_shipping_delivery_rate:
        return None
    db.delete(db_shipping_delivery_rate)
    db.commit()
    return db_shipping_delivery_rate


def create_shipping_delivery(db: Session, shipping_delivery: schemas.ShippingDeliveryCreate):
    db_shipping_delivery = models.ShippingDelivery(**shipping_delivery.dict())
    db.add(db_shipping_delivery)
    db.commit()
    db.refresh(db_shipping_delivery)
    return db_shipping_delivery


def get_shipping_delivery(db: Session, shipping_delivery_id: int):
    return (
        db.query(models.ShippingDelivery)
        .filter(models.ShippingDelivery.id == shipping_delivery_id)
        .first()
    )


def get_shipping_deliveries(db: Session, limit: int = 10, offset: int = 0):
    counter = db.query(models.ShippingDelivery).count()
    data = db.query(models.ShippingDelivery).offset(offset).limit(limit)
    counterByFilters = data.count()
    return {
        "data": data.all(),
        "counter_shipping_deliveries": counter,
        "current_counter_show": counterByFilters,
    }


def delete_shipping_delivery(db: Session, shipping_delivery_id: int):
    db_shipping_delivery = get_shipping_delivery(db, shipping_delivery_id)
    if not db_shipping_delivery:
        return None
    db.delete(db_shipping_delivery)
    db.commit()
    return db_shipping_delivery


def create_shipping_delivery_transaction(
    db: Session, shipping_delivery_transaction: schemas.ShippingDeliveryTransactionCreate):
    db_shipping_delivery_transaction = models.ShippingDeliveryTransaction(
        **shipping_delivery_transaction.dict()
    )
    db.add(db_shipping_delivery_transaction)
    db.commit()
    db.refresh(db_shipping_delivery_transaction)
    return db_shipping_delivery_transaction


def get_shipping_delivery_transaction(db: Session, shipping_delivery_transaction_id: int):
    return (
        db.query(models.ShippingDeliveryTransaction)
        .filter(models.ShippingDeliveryTransaction.id == shipping_delivery_transaction_id)
        .first()
    )


def get_shipping_delivery_transactions(db: Session, limit: int = 10, offset: int = 0):
    counter = db.query(models.ShippingDeliveryTransaction).count()
    data = db.query(models.ShippingDeliveryTransaction).offset(offset).limit(limit)
    counterByFilters = data.count()
    return {
        "data": data.all(),
        "counter_shipping_delivery_transactions": counter,
        "current_counter_show": counterByFilters,
    }


def delete_shipping_delivery_transaction(db: Session, shipping_delivery_transaction_id: int):
    db_shipping_delivery_transaction = get_shipping_delivery_transaction(
        db, shipping_delivery_transaction_id
    )
    if not db_shipping_delivery_transaction:
        return None
    db.delete(db_shipping_delivery_transaction)
    db.commit()
    return db_shipping_delivery_transaction