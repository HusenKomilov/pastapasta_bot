from django.contrib import admin

from .models import Category, Language, LanguagePhrase, Product
from modeltranslation.admin import TranslationAdmin

admin.site.register(Category)
# admin.site.register(Product)
admin.site.register(Language)


@admin.register(LanguagePhrase)
class LanguagePhraseAdmin(TranslationAdmin):
    list_display = ("code", "text")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category")
