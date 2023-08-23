from django.db import models
from django.contrib.auth.models import User

KATEGORI = (
    ('smartphone', 'smartphone'),
    ('aksesoris', 'aksesoris'),
    ('perangkat lain', 'perangkat lain'),
)

class Product(models.Model):
    nama = models.CharField(max_length=100, null=True)
    kategori = models.CharField(max_length=20, choices=KATEGORI, null=True)
    kuantitas = models.PositiveBigIntegerField(null=True)
    hargam = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    harga = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.nama}-({self.kuantitas})'

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(User, models.CASCADE, null=True)
    order_kuantitas = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product} ordered by {self.staff}'
