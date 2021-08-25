from django.contrib.auth.models import User
from django.db import models

from product.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=100)
    address_label = models.CharField(max_length=100, verbose_name='배송지 별칭')
    zipcode = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    payment_method = models.CharField(max_length=100, verbose_name='결제 수단(N페이, 카카오페이 등)', null=True)
    payment_status = models.CharField(max_length=10, default=False, verbose_name='결제 완료 여부')
    payment_unique_numbers = models.CharField(max_length=100, verbose_name='결제 고유번호', null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return '%s' % self.id