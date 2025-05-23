from django.db import models

class Sale(models.Model):
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_name} - {self.quantity} units sold"

class Dashboard(models.Model):
    total_sales = models.DecimalField(max_digits=15, decimal_places=2)
    total_transactions = models.PositiveIntegerField()
    last_sale_date = models.DateTimeField()

    def __str__(self):
        return f"Dashboard Stats: {self.total_transactions} transactions, Total Sales: {self.total_sales}"
