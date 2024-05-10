from config.app import Config
from router.web import web
from router.api import api
from router.apipublic import api as api_public
from router.auth import auth
from orm_db.database import engine
from orm_db import models

models.Base.metadata.create_all(bind=engine)


app = Config().add_middleware()
"""
    Routers:
        web
        api
        api_public
        auth
"""
app.include_router(auth)
app.include_router(web)
app.include_router(api)
app.include_router(api_public)