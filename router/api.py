from config.app import Config
from config.auth import get_current_active_user, User, Annotated, Depends

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