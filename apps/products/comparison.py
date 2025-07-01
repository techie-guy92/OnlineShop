class Comparison_Of_Products:
    def __init__(self,request):
        self.session = request.session
        comparison_list = self.session.get("comparison_list")
        
        if not comparison_list:
            comparison_list = self.session["comparison_list"] = []
        
        self.comparison_list = comparison_list
        self.count = len(self.comparison_list)
        
        
    def __iter__(self):
        comparison_list_copy = self.comparison_list.copy()
        
        for item in comparison_list_copy:
            yield item
            
            
    def add_to_comparison_list(self,productId):
        productId = int(productId)
        
        if productId not in self.comparison_list:
            self.comparison_list.append(productId)
            
        self.count = len(self.comparison_list)
        self.session.modified = True
        
        
    def delete_from_comparison_list(self,product_Id):
        self.comparison_list.remove(int(product_Id))
        self.count = len(self.comparison_list)
        self.session.modified = True
        
        
    def clear_comparison_list(self):
        del self.session["comparison_list"]
        self.session.modified = True
        