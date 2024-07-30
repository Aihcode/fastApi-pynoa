from config.app import Config
from config.auth import get_current_active_user, User, Annotated, Depends
from orm_db import crud, schemas
from sqlalchemy.orm import Session
from fastapi import HTTPException, Body
from helpers.getdb import get_db
from fastapi import UploadFile, File
from random import random, choice
from json import dumps, loads
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


@api.get("/products")
async def index_product(
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
    return crud.get_products(
        db=next(get_db()), limit=payload.limit or 10, skip=payload.skip or 0
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
    return crud.get_product(db=next(get_db()), product_id=product_id)


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
    return crud.create_product(db=next(get_db()), product=payload)


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
    return crud.update_product(
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
    return crud.delete_product(db=next(get_db()), product_id=product_id)


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
    return crud.get_product_variants(
        db=next(get_db()), variant_id=variant_id
    )


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
    return crud.create_product_variant(db=next(get_db()), product_variant=payload)


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
    return crud.update_product_variant(
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
    return crud.delete_product_variant(db=next(get_db()), variant_id=variant_id)


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
    return crud.get_product_options(
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
    return crud.create_product_option(db=next(get_db()), product_option=payload)


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
    return crud.update_product_option(
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
    return crud.delete_product(db=next(get_db()), product_id=product_id)


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
    return crud.get_categories(
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

    db_category = crud.get_category(db, category_id=category_id)
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
    db_category = crud.create_category(db=db, category=payload)
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
    return crud.update_category(
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
    return crud.delete_category(db=next(get_db()), category_id=category_id)


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
    return crud.get_tags(
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
    return crud.get_tag(db=next(get_db()), tag_id=tag_id)


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
    return crud.create_tag(db=next(get_db()), tag=tag_body)


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
    return crud.update_tag(db=next(get_db()), tag_id=tag_id, tag=tag_body)


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
    return crud.delete_tag(db=next(get_db()), tag_id=tag_id)


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
    return crud.get_inventory_location(
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
    return crud.create_inventory_location(db=next(get_db()), inventory_location=payload)


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
    return crud.update_inventory_location(db=next(get_db()), location_id=location_id)


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
    return crud.delete_inventory_location(db=next(get_db()), location_id=location_id)


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
    
    return crud.get_inventories(db=next(get_db()), limit=payload.limit or 10, skip=payload.skip or 0)

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
    return crud.get_inventory(db=next(get_db()), inventory_id=inventory_id)


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
    return crud.create_inventory(db=next(get_db()), inventory=payload)


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
    return crud.update_inventory(db=next(get_db()), inventory=payload,inventory_id=invenroty_id)


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
    return crud.delete_inventory(db=next(get_db()), inventory_id=invenroty_id)


@api.patch("/media/upload/{convert}", response_model=schemas.MediaView)
def upload_media(file: Annotated[UploadFile, File()], convert: str, db:Session=Depends(get_db), current_user=Depends(get_current_active_user)):
    
    if not current_user:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    basePatch = './static/uploads/media/'
    if not os.path.exists(basePatch):
        os.mkdir(basePatch)
        pass

    fileType = '.webp'

    if len(convert) > 0:
        fileType = '.' + convert
    

    randomId = random()
    randomChoice = choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
    hashedName = get_hashed_name(str(randomId) + randomChoice + file.filename) + fileType
    fileUpload = os.path.join(basePatch, hashedName.replace('', ''))
    with open(fileUpload, "wb") as buffer:
        while contents := file.file.read(1024 * 1024):
            buffer.write(contents)

    
    if current_user is None:
        raise HTTPException(status_code=400, detail="User not found")
    baseHost = os.environ.get('SERVER_URL')
    return crud.upload_media(db=db, user_id=current_user['id'], media=fileUpload, media_json=dumps({
        "url": ("%s%s" % (baseHost, fileUpload.replace('./', '/'))),
        "type": fileType,
        "size": os.path.getsize(fileUpload),
        "path": fileUpload,
        "name": hashedName
    }))

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
    return crud.get_media(db=next(get_db()), media_id=media_id)


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
    return crud.get_mediaGallery(db=next(get_db()), limit=payload.limit or 10, skip=payload.skip or 0)

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
    return crud.delete_media(db=next(get_db()), media_id=media_id)