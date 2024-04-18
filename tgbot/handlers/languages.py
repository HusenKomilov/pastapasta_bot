from product.models import LanguagePhrase


def get_text(code: str) -> str:
    phrase = LanguagePhrase.objects.get(code=code)
    return phrase.text
