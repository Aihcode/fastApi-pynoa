from helpers.getdb import get_db
from payments.stripe import gateway as stripe
from orm_db.models import QuequeTasks, Product, ProductVariant, Inventory
from sqlalchemy import and_
from datetime import datetime, date
from logging import Logger
from time import sleep

logger = Logger(__name__)


# private tools functions
def __get_current_variants__(id: int):
    db = next(get_db())

    productData = db.query(Product).filter(Product.id == id).first() 


    if productData:
        if productData.name is not None:
            inventory = db.query(Inventory).filter(Inventory.product_id == productData.id).all()

        
            variants = []

            for vinventory in inventory:
                variants.append(db.query(ProductVariant).filter(ProductVariant.id == vinventory.product_variant_id).first())

            return variants

    return []


def __create_new_task__(task: str, module: str, current_id: int, last_id: int):
    db = next(get_db())
    current_task = QuequeTasks(
        task=task, module=module, current_id=current_id, last_id=last_id
    )
    db.add(current_task)
    db.commit()
    db.refresh(current_task)
    return current_task


def __update_current_taks__(id: int, product_id: int):
    db = next(get_db())

    update_current_task = db.query(QuequeTasks).filter(QuequeTasks.id == id).first()
    update_current_task.current_id = product_id
    update_current_task.updated_at = datetime.now()
    db.commit()


def __end_current_taks__(id: int):
    db = next(get_db())

    update_current_task_end = db.query(QuequeTasks).filter(QuequeTasks.id == id).first()
    update_current_task_end.completed = True
    update_current_task_end.updated_at = datetime.now()
    db.commit()


# create product

def stripe_create_product():
    db = next(get_db())
    print("create_product")
    all_products = db.query(Product).filter(Product.on_stripe.is_not(True)).limit(1000).all()
    
    last_product_id = all_products[-1].id
    current_task = __create_new_task__("create_product", "product", 0, last_product_id)
    for product in all_products:
        __update_current_taks__(current_task.id, product.id)
        try:
            # require search into inventory to link to product variant
            product_variant = __get_current_variants__(product.id)
            
            # create product on stripe
            for product_variant in product_variant:
                if product_variant.stripe_variant_id is None or product_variant.stripe_variant_id == "" and product_variant.title is not None:
                    stripe_id = stripe().create_product(name=product_variant.title + " --variant " + str(product_variant.title))
                    stripe_price_id = stripe().create_price(stripe_id, int(product_variant.price * 100))
                    print(stripe_id.id, stripe_price_id.id)
                    db_variant = db.query(ProductVariant).filter(ProductVariant.id == product_variant.id).first()
                    db_variant.stripe_variant_id = stripe_id.id
                    db_variant.stripe_price_id = stripe_price_id.id
                    db.commit()
                    logger.info(msg="created product on stripe")

                    db_product = db.query(Product).filter(Product.id == product.id).first()
                    db_product.on_stripe = True
                    db.commit()

            logger.info("current_task.id" + str(current_task.id))
        except Exception as e:
            logger.error(msg=e)
        pass
        
        # complete and finished
        if product.id == last_product_id:
            __end_current_taks__(current_task.id)
            break

# update product
def stripe_update_product():
    db = next(get_db())
    today = date.today()
    print("update_product")
    all_products = db.query(Product).filter(and_(
        Product.updated_at >= datetime.combine(today, datetime.min.time()),
        Product.updated_at < datetime.combine(today, datetime.max.time())
    )).all()
    last_product_id = all_products[-1].id
    logger.info(msg="last_product_id=" + str(last_product_id))
    current_task = __create_new_task__("update_product", "product", 0, last_product_id)
    for product in all_products:
        logger.info(msg="product.id=" + str(product.id))
        __update_current_taks__(current_task.id, product.id)
        try:
            # require search into inventory to link to product variant
            product_variant = __get_current_variants__(product.id)

            for product_variant in product_variant:
                print("product_variant.id=" + str(product_variant.id))
                logger.info(msg="product_variant.id=" + str(product_variant.id) + " product_variant.stripe_price_id=" + str(product_variant.stripe_price_id))
                if product_variant.stripe_price_id is not None :
                    print("product_variant.stripe_price_id=" + str(product_variant.stripe_price_id))
                    stripe_id = product_variant.stripe_variant_id
                    old_stripe_id = product_variant.stripe_price_id
                        
                    new_stripe_id = stripe().create_price(stripe_id, int(product_variant.price * 100))
                    db_variant = db.query(ProductVariant).filter(ProductVariant.id == product_variant.id).first()
                    db_variant.stripe_price_id= new_stripe_id.id
                    db.commit()
                    sleep(2)
                    if old_stripe_id is not None:
                        stripe().update_price(price_id=old_stripe_id, active=False)
                    logger.info(msg="updated product on stripe")
        except Exception as e:
            logger.error(msg=e)
        pass
        
        # complete and finished
        if product.id == last_product_id:
            __end_current_taks__(current_task.id)
            break



def delete_all_products_on_stripe():

    products_list = stripe().list_products()

    prices_list = stripe().list_prices()

    all_prices = len(prices_list.data)
    index_prices = 0


    for price in prices_list.data:
        try:
            stripe().update_price(price.id, active=False)
            print(price.id, "deleted")
            index_prices += 1
        except Exception as e:
            print(e)    


    if index_prices == all_prices:

        for product in products_list.data:
            try:
                stripe().delete_product(product.id)
                print(product.id, "deleted")
            except Exception as e:
                print(e)