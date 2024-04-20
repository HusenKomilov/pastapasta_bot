from django.db import models
from utils.models import BaseModel
from users.models import User


class Language(BaseModel):
    title = models.CharField(max_length=256)
    code = models.CharField(max_length=256)

    def __str__(self):
        return self.title


class LanguagePhrase(BaseModel):
    code = models.CharField(max_length=256)
    text = models.TextField()

    def __str__(self):
        return self.code


class Category(BaseModel):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title


class Product(BaseModel):
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="product", null=True, blank=True)
    price = models.IntegerField(default=0, null=True, blank=True)
    weight = models.IntegerField(default=0, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Card(BaseModel):
    product_title = models.CharField(max_length=128)
    product_price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
