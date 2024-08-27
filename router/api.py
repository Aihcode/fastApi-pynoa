from config.app import Config
from config.auth import get_current_active_user, User, Annotated, Depends
from orm_db import crud as common_crud, schemas
from orm_db.crud_master.product import (
    product as product_crud,
    category as category_crud,
    tag as tag_crud,
)
from orm_db.crud_master.checkout import payment as payment_crud
from orm_db.crud_master.checkout import order as order_crud
from orm_db.crud_master.checkout import invoice as invoice_crud
from sqlalchemy.orm import Session
from fastapi import HTTPException, Body
from helpers.getdb import get_db
from fastapi import UploadFile, File
from random import random, choice
from json import dumps
from helpers.encryptgen import get_hashed_name
import os

api = Config().api


@api.get("/")
async def index(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Retrieves the root endpoint of the ADMIN API.

    This function is an asynchronous handler for the GET request to the root endpoint ("/"). It returns a JSON object containing a single key-value pair, where the key is "message" and the value is "Hello World API".

    Returns:
        dict: A JSON object containing the message "Hello World API".
    """
    return {"message": "Hello World API", "user": current_user}


# Start: Management products
@api.get("/products")
async def index_product(
    payload: schemas.ObjectByPaginationwithFilter = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return product_crud.get_products(
        db=next(get_db()),
        keyword=payload.keyword or "",
        limit=payload.limit or 10,
        skip=payload.skip or 0,
    )


@api.get("/product/{product_id}")
async def get_product(
    product_id: int,
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return product_crud.get_product(db=next(get_db()), product_id=product_id)


@api.post("/product")
async def post_product(
    payload: schemas.Product = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return product_crud.create_product(db=next(get_db()), product=payload)


@api.put("/product/{product_id}")
async def put_product(
    product_id: int,
    payload: schemas.Product = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return product_crud.update_product(
        db=next(get_db()), product=payload, product_id=product_id
    )


@api.delete("/product/{product_id}")
async def delete_product(
    product_id: int,
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return product_crud.delete_product(db=next(get_db()), product_id=product_id)


@api.get("/product/variant/{variant_id}")
async def index_product_variant(
    variant_id: int,
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return common_crud.get_product_variants(db=next(get_db()), variant_id=variant_id)


@api.post("/product/variant")
async def post_product_variant(
    payload: schemas.ProductVariant = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return common_crud.create_product_variant(
        db=next(get_db()), product_variant=payload
    )


@api.put("/product/variant/{variant_id}")
async def put_product_variant(
    variant_id: int,
    payload: schemas.ProductVariant = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return common_crud.update_product_variant(
        db=next(get_db()), product_variant=payload, id=variant_id
    )


@api.delete("/product/variant/{variant_id}")
async def delete_product_variant(
    variant_id: int,
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return common_crud.delete_product_variant(db=next(get_db()), variant_id=variant_id)


@api.get("/product/option")
async def index_product(
    payload: schemas.ProductOption = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return common_crud.get_product_options(
        db=next(get_db(), limit=payload.limit or 10, skip=payload.skip or 0)
    )


@api.post("/product/option")
async def post_product(
    payload: schemas.ProductOption = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return common_crud.create_product_option(db=next(get_db()), product_option=payload)


@api.put("/product/option/{option_id}")
async def put_product(
    option_id: int,
    payload: schemas.ProductOption = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return common_crud.update_product_option(
        db=next(get_db()), product_option=payload, option_id=option_id
    )


@api.delete("/product/option/{product_id}")
async def delete_product(
    product_id: int,
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return common_crud.delete_product(db=next(get_db()), product_id=product_id)


# end: Management product


# start: Management category


@api.get("/category")
async def all_category_product(
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
    return category_crud.get_categories(
        db=next(get_db()), limit=payload.limit or 10, skip=payload.skip or 0
    )


@api.get("/category/{category_id}", response_model=schemas.Category)
async def one_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")

    db_category = common_crud.get_category(db, category_id=category_id)
    return db_category


@api.post("/category")
async def post_category_product(
    payload: schemas.Category = Body(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """

    if not current_user:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_category = category_crud.create_category(db=db, category=payload)
    return {"message": "Category created", "data": db_category}


@api.put("/category/{category_id}")
async def put_category_product(
    category_id: int,
    payload: schemas.Category = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return category_crud.update_category(
        db=next(get_db()), category=payload, category_id=category_id
    )


@api.delete("/category/{category_id}")
async def delete_category_product(
    category_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return category_crud.delete_category(db=next(get_db()), category_id=category_id)


@api.get("/tag")
async def index_tag(
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
    return tag_crud.get_tags(
        db=next(get_db()), limit=payload.limit or 10, skip=payload.skip or 0
    )


@api.get("/tag/{tag_id}", response_model=schemas.Tag)
async def one_tag(tag_id: int, current_user=Depends(get_current_active_user)):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return tag_crud.get_one(db=next(get_db()), tag_id=tag_id)


@api.post("/tag")
async def post_tag(
    tag_body: schemas.Tag = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return tag_crud.create(db=next(get_db()), tag=tag_body)


@api.put("/tag/{tag_id}")
async def put_tag(
    tag_id: int,
    tag_body: schemas.Tag = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return tag_crud.update(db=next(get_db()), tag_id=tag_id, tag=tag_body)


@api.delete("/tag/{tag_id}")
async def delete_tag(
    tag_id: int,
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return tag_crud.delete(db=next(get_db()), tag_id=tag_id)


# end: Management category


# start: Management inventory


@api.get("/product/inventory/location")
async def index_inventory_location_product(
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
    return common_crud.get_inventory_location(
        db=next(get_db()), limit=payload.limit or 10, skip=payload.skip or 0
    )


@api.post("/product/inventory/location")
async def post_inventory_location_product(
    payload: schemas.InventoryLocation = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """

    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return common_crud.create_inventory_location(
        db=next(get_db()), inventory_location=payload
    )


@api.put("/product/inventory/location/{location_id}")
async def put_inventory_location_product(
    location_id: int,
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return common_crud.update_inventory_location(
        db=next(get_db()), location_id=location_id
    )


@api.delete("/product/inventory/location/{location_id}")
async def delete_inventory_location_product(
    location_id: int,
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return common_crud.delete_inventory_location(
        db=next(get_db()), location_id=location_id
    )


@api.get("/inventory")
async def index_inventory(
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

    return common_crud.get_inventories(
        db=next(get_db()), limit=payload.limit or 10, skip=payload.skip or 0
    )


@api.get("/inventory/{inventory_id}")
async def index_inventory(
    inventory_id: int,
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return common_crud.get_inventory(db=next(get_db()), inventory_id=inventory_id)


@api.post("/inventory")
async def post_inventory(
    payload: schemas.Inventory = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return common_crud.create_inventory(db=next(get_db()), inventory=payload)


@api.put("/inventory/{invenroty_id}")
async def put_inventory(
    invenroty_id: int,
    payload: schemas.Inventory = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return common_crud.update_inventory(
        db=next(get_db()), inventory=payload, inventory_id=invenroty_id
    )


@api.delete("/inventory/{invenroty_id}")
async def delete_inventory(
    invenroty_id: int,
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return common_crud.delete_inventory(db=next(get_db()), inventory_id=invenroty_id)


# end: Management inventory


# start: management Media


@api.patch("/media/upload/{convert}", response_model=schemas.MediaView)
def upload_media(
    file: Annotated[UploadFile, File()],
    convert: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):

    if not current_user:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    basePatch = "./static/uploads/media/"
    if not os.path.exists(basePatch):
        os.mkdir(basePatch)
        pass

    fileType = ".webp"

    if len(convert) > 0:
        fileType = "." + convert

    randomId = random()
    randomChoice = choice(
        [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
        ]
    )
    hashedName = (
        get_hashed_name(str(randomId) + randomChoice + file.filename) + fileType
    )
    fileUpload = os.path.join(basePatch, hashedName.replace("", ""))
    with open(fileUpload, "wb") as buffer:
        while contents := file.file.read(1024 * 1024):
            buffer.write(contents)

    if current_user is None:
        raise HTTPException(status_code=400, detail="User not found")
    baseHost = os.environ.get("SERVER_URL")
    return common_crud.upload_media(
        db=db,
        user_id=current_user["id"],
        media=fileUpload,
        media_json=dumps(
            {
                "url": ("%s%s" % (baseHost, fileUpload.replace("./", "/"))),
                "type": fileType,
                "size": os.path.getsize(fileUpload),
                "path": fileUpload,
                "name": hashedName,
            }
        ),
    )


@api.get("/media/{media_id}")
async def get_media(
    media_id: int,
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return common_crud.get_media(db=next(get_db()), media_id=media_id)


@api.get("/gallery/media")
async def get_media(
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
    return common_crud.get_mediaGallery(
        db=next(get_db()), limit=payload.limit or 10, skip=payload.skip or 0
    )


@api.delete("/media/{media_id}")
async def delete_media(
    media_id: int,
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return common_crud.delete_media(db=next(get_db()), media_id=media_id)


# end: management Media

# Begin: Management ORDER


@api.get("/orders")
async def index_order(
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
    return order_crud.get_orders(
        db=next(get_db()), limit=payload.limit or 10, skip=payload.skip or 0
    )


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


# End: Management ORDER


# Start: Management INVOICE


@api.get("/invoices")
async def get_invoices(
    payload: schemas.InvoiceFilter = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return invoice_crud.get_all(db=next(get_db()), payload=payload)


@api.get("/invoices/{invoice_id}")
async def get_invoice_by_id(
    invoice_id: int, current_user=Depends(get_current_active_user)
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return invoice_crud.get_by_id(db=next(get_db()), invoice_id=invoice_id)


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


@api.put("/invoice/{invoice_id}")
async def update_invoice(
    invoice_id: int,
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
    return invoice_crud.update(
        db=next(get_db()), invoice=payload, invoice_id=invoice_id
    )


@api.put("/invoice/cancel/{invoice_id}")
async def cancel_invoice(
    invoice_id: int, current_user=Depends(get_current_active_user)
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:

        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return invoice_crud.cancel(db=next(get_db()), invoice_id=invoice_id)


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


# End: Management INVOICE

# Start: Management payments


@api.get("/payment/types")
async def get_payments(
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
    return payment_crud.get_payment_types(db=next(get_db()), payload=payload)


@api.get("/payments/{payment_id}")
async def get_payment_by_id(
    payment_id: int, current_user=Depends(get_current_active_user)
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:
        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return payment_crud.get_payment_type(db=next(get_db()), payment_id=payment_id)


@api.post("/payment/type")
async def create_payment_type(
    payload: schemas.PaymentTypeCreate = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:

        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return payment_crud.create_payment_type(db=next(get_db()), payload=payload)


@api.put("/payment/type/{payment_id}")
async def update_payment_type(
    payment_id: int,
    payload: schemas.PaymentTypeCreate = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:

        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return payment_crud.update_payment_type(
        db=next(get_db()), payment_id=payment_id, payload=payload
    )


@api.delete("/payment/type/{payment_id}")
async def delete_payment_type(
    payment_id: int, current_user=Depends(get_current_active_user)
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:

        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return payment_crud.delete_payment_type(db=next(get_db()), payment_id=payment_id)


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


@api.get("/payment/method/{payment_id}")
async def get_payment_method_by_id(
    payment_id: int, current_user=Depends(get_current_active_user)
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:

        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return payment_crud.get_payment_method(db=next(get_db()), payment_id=payment_id)


@api.post("/payment/method")
async def create_payment_method(
    payload: schemas.PaymentMethodCreate = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:

        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return payment_crud.create_payment_method(db=next(get_db()), payload=payload)


@api.put("/payment/method/{payment_id}")
async def update_payment_method(
    payment_id: int,
    payload: schemas.PaymentMethodCreate = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:

        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return payment_crud.update_payment_method(
        db=next(get_db()), payment_id=payment_id, payload=payload
    )


@api.delete("/payment/method/{payment_id}")
async def delete_payment_method(
    payment_id: int, current_user=Depends(get_current_active_user)
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:

        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return payment_crud.delete_payment_method(db=next(get_db()), payment_id=payment_id)


@api.get("/payment/transactions")
async def get_payment_transactions(
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
    return payment_crud.get_payment_transactions(db=next(get_db()), payload=payload)


@api.get("/payment/transaction/{payment_id}")
async def get_payment_transaction_by_id(
    payment_id: int, current_user=Depends(get_current_active_user)
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:

        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return payment_crud.get_payment_transaction(
        db=next(get_db()), payment_id=payment_id
    )


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


@api.put("/payment/transaction/{payment_id}")
async def update_payment_transaction(
    payment_id: int,
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
    return payment_crud.update_payment_transaction(
        db=next(get_db()), payment_id=payment_id, payload=payload
    )


@api.delete("/payment/transaction/{payment_id}")
async def delete_payment_transaction(
    payment_id: int, current_user=Depends(get_current_active_user)
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.

    Returns:

        dict: A dictionary containing the message "Hello World API".
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return payment_crud.cancel_payment_transaction(
        db=next(get_db()), payment_id=payment_id
    )


# End: Management payments


# Start: Management shipping


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


@api.post("/shipping/rate")
async def create_shipping_rate(
    payload: schemas.ShippingDeliveryRateCreate = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return payment_crud.create_shipping_delivery_rate(
        db=next(get_db()), shipping_delivery_rate=payload
    )


@api.put("/shipping/rate/{rate_id}")
async def update_shipping_rate(
    rate_id: int,
    payload: schemas.ShippingDeliveryRateCreate = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return payment_crud.update_shipping_delivery_rate(
        db=next(get_db()),
        shipping_delivery_rate_id=rate_id,
        shipping_delivery_rate=payload,
    )


@api.delete("/shipping/rate/{rate_id}")
async def delete_shipping_rate(
    rate_id: int, current_user=Depends(get_current_active_user)
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return payment_crud.delete_shipping_delivery_rate(
        db=next(get_db()), shipping_delivery_rate_id=rate_id
    )


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


@api.get("/shipping/delivery/{delivery_id}")
async def get_shipping_delivery(
    delivery_id: int,
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return payment_crud.get_shipping_delivery(
        db=next(get_db()), shipping_delivery_id=delivery_id
    )


@api.post("/shipping/delivery")
async def create_shipping_delivery(
    payload: schemas.ShippingDeliveryCreate = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return payment_crud.create_shipping_delivery(
        db=next(get_db()), shipping_delivery=payload
    )


@api.delete("/shipping/delivery/{delivery_id}")
async def delete_shipping_delivery(
    delivery_id: int, current_user=Depends(get_current_active_user)
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return payment_crud.delete_shipping_delivery(
        db=next(get_db()), shipping_delivery_id=delivery_id
    )


@api.get("/shipping/transactions")
async def get_shipping_transactions(
    payload: schemas.ObjectByPagination = Body(...),
    current_user=Depends(get_current_active_user),
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return payment_crud.get_shipping_delivery_transactions(
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


@api.delete("/shipping/transaction/{transaction_id}")
async def delete_shipping_transaction(
    transaction_id: int, current_user=Depends(get_current_active_user)
):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return payment_crud.delete_shipping_delivery_transaction(
        db=next(get_db()), shipping_delivery_transaction_id=transaction_id
    )


# End: Management shipping


# Start: Admin navigation map


@api.get("/map/navigation")
async def get_map_navigation(current_user=Depends(get_current_active_user)):
    """
    A function that handles the GET request to the root endpoint ("/") of the ADMIN API.
    """
    if not current_user:
        raise HTTPException(status_code=409, detail="Not logged in")
    return {
        "admin": [
            {"title": "Dashboard", "url": "/dashboard", "api_prefix": "/admin/api/"},
            {
                "title": "Inventory",
                "url": "/inventory",
                "children": [
                    {
                        "title": "Products",
                        "url": "/products",
                        "children": [
                            {
                                "title": "Variants",
                                "url": "cgi/product/variant",
                            },
                            {
                                "title": "Inventory Location",
                                "url": "cgi/inventory/location",
                            },
                            {
                                "title": "Media Library",
                                "url": "cgi/media",
                            }
                        ],
                    },
                    {
                        "title": "Categories",
                        "url": "/category",
                    },
                    {"title": "Tags", "url": "/tag"},
                    {
                        "title": "Inventory",
                        "url": "/inventory",
                    },
                ],
            },
        ]
    }


# End: Admin navigation map
