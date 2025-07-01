from apps.products.models import Products



class Shopping_Cart:
    def __init__(self,request):
        self.session = request.session
        shopping_cart_session = self.session.get("shopping_cart")
        
        if not shopping_cart_session:
            shopping_cart_session = self.session["shopping_cart"] = {}
            
        self.shopping_cart = shopping_cart_session
        self.count = len(self.shopping_cart.keys())
        
        
    def add_to_shopping_cart(self,product,qty):
        product_id = str(product.id)
        if product_id not in self.shopping_cart:
            self.shopping_cart[product_id] = {"qty":0,"price":product.price,"final_price":product.fetch_discount_basket()}
        self.shopping_cart[product_id]["qty"]+= int(qty)
        self.count = len(self.shopping_cart.keys())
        self.save()
        
         
    def delete_from_shopping_cart(self,product):
        product_id = str(product.id)
        del self.shopping_cart[product_id]
        self.save()
      
        
    def update_shopping_cart(self,list_of_product_id,list_of_qty):
        counter = 0
        
        for product_id in list_of_product_id:
            self.shopping_cart[product_id]["qty"] = int(list_of_qty[counter])
            counter+= 1
        self.save()
        
    # def update_shopping_cart(self, list_of_product_id, list_of_qty):
    #     if len(list_of_product_id) != len(list_of_qty):
    #         raise ValueError("List of product IDs and list of quantities must have the same length")

    #     for product_id, qty in zip(list_of_product_id, list_of_qty):
    #         if product_id not in self.shopping_cart:
    #             raise ValueError(f"Product ID {product_id} not found in shopping cart")
    #         self.shopping_cart[product_id]["qty"] = int(qty)
    #     self.save()
        
        
    def save(self):
        self.session.modified = True
        
        
    def __iter__(self):
        list_of_id = self.shopping_cart.keys()
        products=Products.objects.filter(id__in=list_of_id)
        shopping_cart_copy = self.shopping_cart.copy()
        
        for product in products:
            shopping_cart_copy[str(product.id)]["product"] = product.to_dict()
            
        for item in shopping_cart_copy.values():
            item["total_price"] = int(item["final_price"]) * item["qty"]
            yield item
            

    def cal_total_price(self):
        sum = 0
        
        for item in self.shopping_cart.values():
            sum+= int(item["final_price"]) * item["qty"]
        return sum
    
    
