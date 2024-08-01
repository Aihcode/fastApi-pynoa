from sqlalchemy.orm import Session

from .. import models
from json import loads

def __get_inventory_location_name__(db: Session, inventory_location_id: int):
    db_location = db.query(models.InventoryLocation).filter(
        models.InventoryLocation.id == inventory_location_id
    ).first()

    if not db_location:
        return {
            "name": "Unknown",
            "address": "Address Unknown"
        }

    return {
        "name": db_location.title,
        "address": db_location.address
    }

def __get_variants__(db: Session, product_id: int, cost: int = 0):
            db_inventory = db.query(models.Inventory).filter(
                models.Inventory.product_id == product_id
            )

            variants = []

            for inventory in db_inventory:
                db_one_variant = db.query(models.ProductVariant).filter(
                    models.ProductVariant.id == inventory.product_variant_id
                ).first()
                inventory_location_details = __get_inventory_location_name__(db, inventory.inventory_location_id)
                
                availability = "In Stock" if inventory.quantity > 0 else "Out Of Stock"
                
                if inventory.quantity <= 0:
                    stock_value = 0
                    estimated_sales = 0
                    estimated_earnings = 0
                    conversion_rate = 0
                else:    
                    stock_value = (cost * int(inventory.quantity))
                    estimated_sales = (db_one_variant.price * inventory.quantity)
                    estimated_earnings = ((db_one_variant.price - cost) * inventory.quantity)
                    conversion_rate = ((stock_value / estimated_sales) * 100)
                
                
                location_code = ("%s%s%s%s" % (inventory.inventory_location_id, inventory.id, int(inventory.lat), abs(int(inventory.lng))))
                variants.append(
                    {
                        "id": db_one_variant.id,
                        "title": db_one_variant.title,
                        "price": db_one_variant.price,
                        "availability": availability,
                        "currency_base": db_one_variant.currency_base,
                        "stock_value": float("{:.3f}".format(stock_value)),
                        "estimated_sales": float("{:.3f}".format(estimated_sales)),
                        "estimated_earnings": float("{:.3f}".format(estimated_earnings)),
                        "conversion_rate": float("{:.3f}".format(conversion_rate)),
                        "conversion_rate_string": ("%s%%" % round(conversion_rate)),
                        "inventory": [
                            {
                                "id": inventory.id,
                                "location_name": inventory_location_details["name"],
                                "location_address": inventory_location_details["address"],
                                "quantity": inventory.quantity,
                                "cancelled": inventory.cancelled,
                                "removed": inventory.removed,
                                "sales": inventory.sales,
                                "lat": inventory.lat,
                                "lng": inventory.lng,
                                "stock_location_code": location_code
                            }
                        ]
                    }
                )

            return variants

def __get_categories_from_mapper__(db: Session, mapper: list):
        categories = []

        for category in loads(mapper):
            category_load = (
                db.query(models.Category).filter(models.Category.id == category).first()
            )
            if category_load:
                categories.append(
                    {
                        "id": category_load.id,
                        "title": category_load.title,
                        "description": category_load.description,
                    }
                )

        return categories

def __get_tags_from_mapper__(db: Session, mapper: list):
        tags = []

        for tag in loads(mapper):
            tag_load = db.query(models.Tag).filter(models.Tag.id == tag).first()
            if tag_load:
                tags.append({"id": tag_load.id, "title": tag_load.title})

        return tags
