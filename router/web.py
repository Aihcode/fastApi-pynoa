from config.app import Config
from fastapi import Request as requests
from fastapi.templating import Jinja2Templates
web = Config().web
templates = Jinja2Templates(directory="templates")

@web.get("/")
async def index(request: requests):
    """
    Retrieves the root endpoint of the WEB.

    This function is an asynchronous handler for the GET request to the root endpoint ("/"). It returns a JSON object containing a single key-value pair, where the key is "message" and the value is "Hello World".

    Returns:
        dict: A JSON object containing the message "Hello World".
    """
    return templates.TemplateResponse("/noabootstrap/index.html", {"request": request, "static": {
        "title": "Welcome to PyNoa",
        "description": "that is all you need to know about PyNoa",
        "apis": {
            "api": "http://localhost:8000/api",
            "public": "http://localhost:8000/api/public",
            "api_text": "Admin api",
            "public_text": "Public Store api"
        },
        "button_text": "Read Docs",
        "button_url": "http://localhost:8000/redoc"
    }})