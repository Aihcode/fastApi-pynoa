from config.app import Config
from config.auth import get_current_active_user, Depends
from orm_db import schemas
from fastapi import HTTPException, Body
from helpers.getdb import get_db
from orm_db.crud_master.product import (
    product as product_crud,
    category as category_crud,
    tag as tag_crud,
)
from orm_db.crud_master.checkout import payment as payment_crud
from orm_db.crud_master.checkout import order as order_crud
from orm_db.crud_master.checkout import invoice as invoice_crud
from pydash import omit

api = Config().api_public

"""
   PUBLIC API
"""


@api.get("/")
async def index(
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the PUBLIC API.

    Returns:
        dict: A dictionary containing the message "Hello World API public".
    """
    return {"message": "Hello World API public", "user": current_user}


@api.get("/products")
async def products(
    payload: schemas.ObjectByPaginationwithFilter = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the PUBLIC API.

    Returns:
        dict: A dictionary containing the message "Hello World API public".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return product_crud.get_products(
        db=next(get_db()),
        keyword=payload.keyword or "",
        limit=payload.limit or 10,
        skip=payload.skip or 0,
        omit_list=["stripe_product_id"],
        omit_into_variants=["price_stripe_id"],
    )


@api.get("/product/{product_id}")
async def product(product_id: int, current_user=Depends(get_current_active_user)):
    """
    A function that handles the GET request to the root endpoint ("/") of the PUBLIC API.

    Returns:
        dict: A dictionary containing the message "Hello World API public".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return product_crud.get_product(
        db=next(get_db()),
        product_id=product_id,
        omit_list=["stripe_product_id"],
        omit_into_variants=["price_stripe_id"],
    )


@api.get("/filters")
async def filters(
    payload: schemas.ObjectByPagination = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the PUBLIC API.

    Returns:
        dict: A dictionary containing the message "Hello World API public".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")

    categories = category_crud.get_categories(
        db=next(get_db()), limit=payload.limit or 10, skip=payload.skip or 0
    )
    tags = tag_crud.get_tags(
        db=next(get_db()), limit=payload.limit or 10, skip=payload.skip or 0
    )

    hardCategories = []
    hardTags = []

    for category in categories["data"]:
        hardCategories.append({"id": category.id, "title": category.title})

    for tag in tags["data"]:
        hardTags.append({"id": tag.id, "title": tag.title})

    return {"categories": hardCategories, "tags": hardTags}


@api.post("/payment/transaction")
async def create_payment_transaction(
    payload: schemas.PaymentTransactionCreate = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:

        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return payment_crud.create_payment_transaction(db=next(get_db()), payload=payload)


@api.get("/shipping/rates")
async def get_shipping_rates(
    payload: schemas.ObjectByPagination = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return payment_crud.get_shipping_delivery_rate(db=next(get_db()), payload=payload)


@api.get("/shipping/deliveries")
async def get_shipping_deliveries(
    payload: schemas.ObjectByPagination = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return payment_crud.get_shipping_deliveries(
        db=next(get_db()), limit=payload.limit or 10, skip=payload.skip or 0
    )


@api.get("/shipping/transaction/{transaction_id}")
async def get_shipping_transaction(
    transaction_id: int,
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return payment_crud.get_shipping_delivery_transaction(
        db=next(get_db()), shipping_delivery_transaction_id=transaction_id
    )


@api.get("/payment/methods")
async def get_payment_methods(
    payload: schemas.ObjectByPagination = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:

        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return payment_crud.get_payment_methods(db=next(get_db()), payload=payload)


@api.get("/order/{order_id}")
async def index_order(
    order_id: int,
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return order_crud.get_order_by_id(db=next(get_db()), order_id=order_id)


@api.post("/order")
async def create_order(
    payload: schemas.OrderCreate = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return order_crud.create_order(db=next(get_db()), order=payload)


@api.put("/order/{order_id}")
async def update_order(
    order_id: int,
    payload: schemas.OrderUpdate = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return order_crud.update_order(db=next(get_db()), order_id=order_id, order=payload)


@api.post("/order/cancel/{order_id}")
async def cancel_order(order_id: int, current_user=Depends(get_current_active_user)):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return order_crud.cancel_order(db=next(get_db()), order_id=order_id)


@api.post("/order/item/{order_id}")
async def create_order_item(
    order_id: int,
    payload: schemas.OrderItemCreate = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return order_crud.add_order_items(
        db=next(get_db()), order_id=order_id, order_item=payload
    )


@api.put("/order/item/{order_id}")
async def update_order_item(
    order_id: int,
    payload: schemas.OrderItemUpdate = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return order_crud.update_order_item(
        db=next(get_db()), order_item_id=order_id, order_item=payload
    )


@api.delete("/order/item/{order_id}")
async def delete_order_item(
    order_id: int, current_user=Depends(get_current_active_user)
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return order_crud.delete_order_item_by_id(db=next(get_db()), order_item_id=order_id)


@api.get("/order/json/{order_id}")
async def json_order(
    order_id: int,
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return order_crud.order_json(db=next(get_db()), order_id=order_id)


@api.post("/invoice")
async def create_invoice(
    payload: schemas.InvoiceCreate = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return invoice_crud.create(db=next(get_db()), invoice=payload)


@api.get("/invoice/json/{invoice_id}")
async def json_invoice(invoice_id: int, current_user=Depends(get_current_active_user)):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:

        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return invoice_crud.invoice_json(db=next(get_db()), invoice_id=invoice_id)
