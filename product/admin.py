from django.contrib import admin

from .models import Category, Language, LanguagePhrase, Product, Card, Order
from modeltranslation.admin import TranslationAdmin

admin.site.register(Category)
# admin.site.register(Card)
# admin.site.register(Order)
admin.site.register(Language)


@admin.register(LanguagePhrase)
class LanguagePhraseAdmin(TranslationAdmin):
    list_display = ("code", "text")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category")


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("user", "quantity", "product_title", "product_price", "total_price", "created_ad")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "created_ad")
