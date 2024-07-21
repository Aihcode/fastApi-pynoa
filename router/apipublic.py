from config.app import Config
from config.auth import get_current_active_user, User, Annotated, Depends
api = Config().api_public

"""
   PUBLIC API
"""
@api.get("/")
async def index(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    A function that handles the GET request to the root endpoint ("/") of the PUBLIC API.

    Returns:
        dict: A dictionary containing the message "Hello World API public".
    """
    return {"message": "Hello World API public", "user": current_user}


@api.get("/products")
async def products():
    return {"message": "Hello World API public"}

@api.get("/product/{id}")
async def product(id):
    return {"message": "Hello World API public"}

@api.get("/orders")
async def order():
    return {"message": "Hello World API public"}

@api.get("/order")
async def order():
    return {"message": "Generate and save an order in the API public"}

@api.get("/order/{id}")
async def order(id):
    return {"message": "Hello World API public"}

@api.get("/collection")
async def collection():
    return {"message": "Hello World API public"}