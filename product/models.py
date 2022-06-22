from django.db import models

# Create your models here.
class Product(models.Model):
    author = models.ForeignKey('user.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    thumbnail = models.ImageField()
    desc = models.CharField(max_length=300)
    register_date = models.DateField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)


class Review(models.Model):
    author = models.ForeignKey('user.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)