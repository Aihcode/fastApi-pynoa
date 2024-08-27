import os
from helpers.mail import Email
from helpers.getdb import get_db
from helpers.encryptgen import get_hashed_token
from orm_db import crud, models
from json import loads, dumps


async def startup():
    print("schedule tasks daemon started")

    db = next(get_db())
    db_users = db.query(models.User).filter(models.User.is_verified.is_(None)).all()

    for user in db_users:
        confirmation_token = get_hashed_token(user.email)
        print(user.email, confirmation_token)

        url = "Please confirm your email to activate your account: <a href='{resend}/confirm-email?token={token}'>{resend}/confirm-email?token={token}</a>".format(token=confirmation_token, resend=os.environ["SERVER_URL"])
        
        mail_notification = {
            "title": "Please confirm your email to activate your account",
            "from_param": "Acme <onboarding@resend.dev>",
            "to_list": [user.email],
            "subject": "Please confirm your email",
            "body": url,
            "is_validated": False,
            "user_id": user.id,
            "token": confirmation_token
        }

        crud_status = crud.create_mail_notification(db, mail_notification=mail_notification)

        print(crud_status)

        user.is_verified = False
        db.add(user)
        db.commit()
    
    return {
        "message": "Schedule tasks daemon started"
    }


async def email_notification():
    print("schedule tasks email notification daemon started")
    db = next(get_db())
    notifications = db.query(models.MailNotifications).filter(models.MailNotifications.is_sent.is_(None)).limit(100)

    for notification in notifications:
        if notification.from_param != "":
            email_status = Email().send(from_param=notification.from_param, to_list=[notification.to_list], subject=notification.subject, html=notification.body)

            if email_status is not None:
                notification.title = notification.title + " - Sent"
                notification.is_validated = True
                db.add(notification)
                db.commit()
                print("notification sent", notification.title)



async def payments_status_update():
    print("schedule tasks payments status update daemon started")
    return True