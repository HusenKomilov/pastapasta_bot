from modeltranslation.translator import register, TranslationOptions
from product.models import Language, LanguagePhrase


@register(LanguagePhrase)
class NewsTranslationOptions(TranslationOptions):
    fields = ("code", 'text',)
