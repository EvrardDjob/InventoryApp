from django.db import models
from django.contrib.auth.models import User

CATEGORY = (
    ('stationary', 'Stationary'),
    ('electonics', 'Electonics'),
    ('food', 'Food'),
)

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=255, choices=CATEGORY, null=True)
    quantity = models.PositiveIntegerField(null=True)

    def __str__(self) ->str:
        return self.name
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(User, models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} ordered by {self.staff.username}"
    
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'