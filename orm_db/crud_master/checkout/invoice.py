from sqlalchemy.orm import Session
from ... import models, schemas


def create(db: Session, invoice: schemas.InvoiceCreate):
    db_invoice = models.Invoice(**invoice.dict())
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice


def get_by_id(db: Session, invoice_id: int):
    return db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()


def get_all(db: Session):
    counter = db.query(models.Invoice).count()
    data = db.query(models.Invoice)
    counterByFilters = data.count()
    return {
        "data": data.all(),
        "counter_invoices": counter,
        "current_counter_show": counterByFilters,
    }


def update(db: Session, invoice_id: int, invoice: schemas.InvoiceCreate):
    db_invoice = (
        db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    )
    db_invoice.invoice_number = invoice.invoice_number
    db_invoice.order_id = invoice.order_id
    db_invoice.amount = invoice.amount
    db_invoice.discount = invoice.discount
    db_invoice.local_tax = invoice.local_tax
    db.commit()
    db.refresh(db_invoice)
    return db_invoice


def delete(db: Session, invoice_id: int):
    db_invoice = (
        db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    )
    db.delete(db_invoice)
    db.commit()
    return db_invoice


def invoice_json(db: Session, invoice_id: int):
    header = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    body = (
        db.query(models.OrderItem)
        .filter(models.OrderItem.order_id == header.order_id)
        .all()
    )

    return {
        "header": header,
        "body": body,
        "footer": [
            {
                "invoice_id": invoice_id,
                "order_id": header.order_id,
                "amount": header.amount,
                "discount": header.discount,
                "local_tax": header.local_tax,
                "created_at": header.created_at,
                "updated_at": header.updated_at,
            }
        ],
    }
