from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from tgbot.handlers.onboarding.manage_data import SECRET_LEVEL_BUTTON
from tgbot.handlers.onboarding.static_text import github_button_text, secret_level_button_text

from product.models import Category, Product


def send_contact() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup([[
        KeyboardButton(text="Raqamni jo'natish", request_contact=True)
    ]], resize_keyboard=True, one_time_keyboard=True)


def send_location() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup([[
        KeyboardButton(text="Manzilni jo'natish", request_location=True)
    ]], resize_keyboard=True, one_time_keyboard=True)


def main_menyu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(text="🍴 Menyu"),
                KeyboardButton(text="📥 Savat")
            ],
            [
                KeyboardButton(text="KAFE LOKATSIYASI"),
                KeyboardButton(text="🚀 Buyurtma haqida")
            ],
            [
                KeyboardButton(text="✍️ Fikr bildirish"),
                KeyboardButton(text="☎️ Kontaktlar")
            ],
            [
                KeyboardButton(text="⚙️ Sozlamalar")
            ]
        ],
        resize_keyboard=True
    )


def menu_button() -> ReplyKeyboardMarkup:
    category = Category.objects.all()

    category_button = []

    category_button.append(["📥 Savat"])
    for i in range(0, len(category), 2):
        if i + 1 != len(category):
            category_button.append([category[i].title, category[i + 1].title])
        else:
            category_button.append([category[i].title])
    category_button.append(["🏘 Bosh menu"])
    markup = ReplyKeyboardMarkup(category_button, resize_keyboard=True, one_time_keyboard=True)
    return markup


def product_manu(category_id) -> ReplyKeyboardMarkup:
    product = Product.objects.filter(category_id=category_id)
    product_button = []

    for i in range(0, len(product), 2):
        if i + 1 != len(product):
            product_button.append([product[i].title, product[i + 1].title])
        else:
            product_button.append([product[i].title])
    markup = ReplyKeyboardMarkup(product_button, resize_keyboard=True, one_time_keyboard=True)
    return markup


def quantity_product() -> ReplyKeyboardMarkup:
    a = []
    a.append(["⬅️ Ortga"])
    for i in range(1, 11, 3):
        if i + 1 != 11:
            a.append([i, i + 1, i + 2])
        else:
            a.append([i])
    markup = ReplyKeyboardMarkup(a, resize_keyboard=True)
    return markup


def comment_button() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup([
        [
            KeyboardButton(text="😊Hammasi yoqdi ❤️"),
        ],
        [
            KeyboardButton(text="☺️Yaxshi ⭐️⭐️⭐️⭐️"),
        ],
        [
            KeyboardButton(text="😐Yoqmadi ⭐️⭐️⭐️"),
        ],
        [
            KeyboardButton(text="🙁Yomon ⭐️⭐️"),
        ],
        [
            KeyboardButton(text="😤Juda yomon 👎"),
        ],
        [
            KeyboardButton(text="🏘 Bosh menu")
        ]
    ], resize_keyboard=True, one_time_keyboard=True)
    return markup


def settings_button() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup([
        [
            KeyboardButton(text="🌐 Tilni tanlash"),
        ],
        [
            KeyboardButton(text="📱 Raqamni o'zgartirish")
        ],
        [
            KeyboardButton(text="🏘 Bosh menu")
        ]
    ], resize_keyboard=True, one_time_keyboard=True)
    return markup


def basket_button() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup([
        [
            KeyboardButton(text="🏘 Bosh menu"),
            KeyboardButton(text="🔄 Tozalash")
        ],
        [
            KeyboardButton(text="🛍 Пакет")
        ],
        [
            KeyboardButton(text="🚖 Buyurtma berish")
        ]
    ], resize_keyboard=True)
    return markup


def placing_button() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup([
        [
            KeyboardButton(text="🚖 Yetkazib berish")
        ],
        [
            KeyboardButton(text="🏃 Olib ketish")
        ],
        [
            KeyboardButton(text="🏘 Bosh menu")
        ]
    ], resize_keyboard=True)
    return markup


def language_inline() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="uz"),
        ],
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="ru")
        ]
    ])
    return markup


def make_keyboard_for_start_command() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(
            github_button_text, url="https://github.com/ohld/django-telegram-bot"),
        InlineKeyboardButton(secret_level_button_text,
                             callback_data=f'{SECRET_LEVEL_BUTTON}')
    ]]

    return InlineKeyboardMarkup(buttons)


def basket_button() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup([
        [
            KeyboardButton(text="🏘 Bosh menu"),
            KeyboardButton(text="🔄 Tozalash")
        ],
        [
            KeyboardButton(text="🛍 Пакет")
        ],
        [
            KeyboardButton(text="🚖 Buyurtma berish")
        ]
    ], resize_keyboard=True)
    return markup

# def category_button() -> ReplyKeyboardMarkup:
#     category = Category.objects.all()
#     category_button = []
#
#     for x in range(0, len(category), 2):
#         if x + 1 != len(category):
#             category_button.append([category[x].title, category[x + 1].title])
#         else:
#             category_button.append([category[x].title])
#     return ReplyKeyboardMarkup(category_button, resize_keyboard=True)
