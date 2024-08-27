import stripe
class gateway:
    def __init__(self):
        self.stripe_api_key = "rk_test_51MVP4dJsTOmaXHsxeyP45nU8oaYkt7mYxuWdymLWFBRGWhaTJCcG4gJ0HGxqmxMLeeLNc193vas3mJ6F3E0nUyOw00nor4ZnMJ"
        self.stripe_account_id = "acct_1MVP4dJsTOmaXHsx"
        pass

    def status(self):
        try:
            charge = stripe.Charge.retrieve(
            self.stripe_account_id,
            api_key=self.stripe_api_key
            )
            return charge.capture()
        except Exception as e:
            return e

    def create_product(self, name):
            stripe.api_key = self.stripe_api_key
            stripe_metadata = stripe.Product.create(
                name=name)
            
            return stripe_metadata
    
    def create_price(self, id: int, price: float):
        stripe.api_key = self.stripe_api_key
        stripe_metadata = stripe.Price.create(
            unit_amount=price,
            currency="usd",
            product=id)
        
        return stripe_metadata
    
    def update_product(self, product):
        stripe.api_key = self.stripe_api_key
        stripe_metadata = stripe.Product.modify(
            product["stripe_product_id"],
            name=product["title"])
        
        return stripe_metadata
    
    def update_price(self, price_id: int, active: bool = False):
        stripe.api_key = self.stripe_api_key
        stripe_metadata = stripe.Price.modify(
            price_id,
            nickname="Disabled",
            active=active)
        
        return stripe_metadata
    
    def delete_product(self, stripe_product_id):
        stripe.api_key = self.stripe_api_key
        stripe_metadata = stripe.Product.delete(stripe_product_id)
        
        return stripe_metadata
    
    def delete_price(self, price):
        stripe.api_key = self.stripe_api_key
        stripe_metadata = stripe.Price.delete(
            price)
        
        return stripe_metadata

    def get_checkout(self, items):
        stripe.api_key = self.stripe_api_key

        feched_items = [dict(price=item["stripe_price_id"], quantity=item["quantity"]) for item in items]

        return stripe.PaymentLink.create(
            line_items=feched_items
        )    

    def balance(self):
        try:
            return stripe.Balance.retrieve(api_key=self.stripe_api_key)
        except Exception as e:
            return e
        

    def list_products(self):
        try:
            return stripe.Product.list(api_key=self.stripe_api_key, limit=100)
        except Exception as e:
            return e
        

    def list_prices(self):
        try:
            return stripe.Price.list(api_key=self.stripe_api_key, limit=100)
        except Exception as e:
            return e