from config.app import Config
from router.web import web
from router.api import api
from router.apipublic import api as api_public
from router.auth import auth
from orm_db.database import engine
from orm_db import models
from orm_db.db_feeds.settings import run_started_settings
from fastapi_utilities import repeat_at
from config.schedule import startup as startup_schedule, email_notification, payments_status_update
from orm_db.schedules.stripe_products import stripe_create_product, stripe_update_product, delete_all_products_on_stripe
from helpers.mail import Email

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


# run migration of app settings
run_started_settings()


# cron tasks
@app.on_event("startup")
async def startup():
    print("Pynoa cron tasks initializing...")
    await startup_schedule()
    """Email().send(
        from_param="Acme <onboarding@resend.dev>",
        to_list=["delivered@resend.dev"],
        subject="hello world",
        html="<strong>it works! TEST</strong>",
    )"""
    

@app.on_event("startup")
@repeat_at(cron="*/1 * * * *")
async def every_2_minutes():
    print("Pynoa common tasks starting...")
    await startup_schedule()
    #Email().send()


@app.on_event("startup")
@repeat_at(cron="*/5 * * * *")
async def every_5_minutes():
    await email_notification()


@app.on_event("startup")
@repeat_at(cron="*/5 * * * *")
def every_5_v2_minutes():
    stripe_create_product()
    stripe_update_product()



@app.on_event("shutdown")
def shutdown():
    print("Shutting down...")
    pass

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)