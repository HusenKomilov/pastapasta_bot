from django.db import models
from utils.models import BaseModel


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
