from pydoc import describe
from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.formfields import PhoneNumberField

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=151)
    image = models.ImageField(upload_to='products/')

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=151)
    image = models.ImageField(upload_to='products/')

class Brand(models.Model):
    name = models.CharField(max_length=150)
    
class Product(models.Model):
    name = models.CharField(max_length=400)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
    brand = models.ForeignKey(Brand,  on_delete=models.CASCADE)
    image_title = models.ImageField(upload_to='products/')

class ImgProduct(models.Model):
    image = models.ImageField(upload_to='products/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

class Basket(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField("дата добавления в корзину", auto_now_add=True)

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField("дата оформления заказа", auto_now_add=True)
    price = models.FloatField("общая цена заказа")
    amount = models.IntegerField("количество единиц товара", default=0)
    inf_card = models.CharField(max_length=151)

class ClientInf(models.Model):
    phone_number = PhoneNumberField()
    email = models.CharField(max_length=151)

