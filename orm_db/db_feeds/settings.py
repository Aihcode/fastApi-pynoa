from ..crud_master.checkout import payment as payment_crud
from helpers.getdb import get_db

def run_started_settings():


    db = next(get_db())

    # payments
    if not payment_crud.get_payment_type(db, 1):
        if payment_crud.create_payment_type(db, {
            "title": "online",
            "created_at": "2022-01-01",
            "updated_at": "2022-01-01"
        }):
            print("started! payment type created")



    if not payment_crud.get_payment_method(db, 1):
        if payment_crud.create_payment_method(db, {
            "title": "stripe",
            "username": "test",
            "password": "test",
            "jwt_key": "test4545454sdsd4s5d4s5d4",
            "payment_type": 1,
            "created_at": "2022-01-01",
            "updated_at": "2022-01-01"
        }):
            print("started! payment method created (stripe)")

    
    if not payment_crud.get_payment_method(db, 2):
        if payment_crud.create_payment_method(db, {
            "title": "paypal",
            "public_key": "test",
            "secret_key": "test",
            "payment_type": 1,
            "created_at": "2022-01-01",
            "updated_at": "2022-01-01"
        }):
            print("started! payment method created (paypal)")

    payments_settings = payment_crud.get_payment_methods(db, 10, 0)
    print("(Pynoa payments) show settings:")

    for payment in payments_settings["data"]:
        payment_status = "[offline]" if payment.disabled else "[online]"
        print(">>", payment.title, "PID:", payment.id, payment_status)

    pass