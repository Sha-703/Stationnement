from django.test import TestCase
from .models import Sale

class SaleModelTest(TestCase):

    def setUp(self):
        Sale.objects.create(item_name="Test Item", quantity=10, price=100.0)

    def test_sale_creation(self):
        sale = Sale.objects.get(item_name="Test Item")
        self.assertEqual(sale.quantity, 10)
        self.assertEqual(sale.price, 100.0)

    def test_sale_total(self):
        sale = Sale.objects.get(item_name="Test Item")
        self.assertEqual(sale.total(), 1000.0)  # Assuming total() method calculates quantity * price

    def test_sale_str(self):
        sale = Sale.objects.get(item_name="Test Item")
        self.assertEqual(str(sale), "Test Item - 10")  # Assuming __str__ method returns item_name and quantity