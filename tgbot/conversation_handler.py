from telegram.ext import ConversationHandler, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
from tgbot.handlers.onboarding import handlers
from tgbot.handlers.utils import states

conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", handlers.command_start),
        MessageHandler(Filters.regex(
            "^(📥 Savat)$"), handlers.order_handler),
        MessageHandler(Filters.regex(
            "^(☎️ Kontaktlar)$"), handlers.contact_handler),
        MessageHandler(Filters.regex(
            "^(KAFE LOKATSIYASI)$"), handlers.cafe_location_handler),
        MessageHandler(Filters.regex(
            "^(🚀 Buyurtma haqida)$"), handlers.order_about_handler),
        MessageHandler(Filters.regex(
            "^(✍️ Fikr bildirish)$"), handlers.comment_handler),
        MessageHandler(Filters.regex(
            "^(🍴 Menyu)$"), handlers.menu_handler),
        MessageHandler(Filters.regex(
            "⚙️ Sozlamalar"), handlers.settings_handler),
        MessageHandler(Filters.all, handlers.back_to_home_handler)
    ],
    states={
        states.PHONE_STATE: [
            MessageHandler(Filters.contact, handlers.send_phone_number_handler),
        ],
        states.MENU_STATE: [
            MessageHandler(Filters.regex("^(🍴 Menyu)$"), handlers.menu_handler),
            MessageHandler(Filters.location, handlers.location_handler),
            MessageHandler(Filters.regex("^(📥 Savat)$"), handlers.order_handler),
            MessageHandler(Filters.regex("^(🏘 Bosh menu)$"),
                           handlers.back_to_home_handler),
        ],
        states.CATEGORY_STATE: [
            MessageHandler(Filters.regex("^(📥 Savat)$"), handlers.order_handler),
            MessageHandler(Filters.text, handlers.category_menu),
        ],
        states.PRODUCT_STATE: [
            MessageHandler(Filters.text, handlers.product_menu),
        ],
        states.QUANTITY_STATE: [
            MessageHandler(Filters.regex("^(⬅️ Ortga)$"), handlers.back_to_product_menu),
            MessageHandler(Filters.text, handlers.product_quantity)
        ],
        states.COMMENT_STATE: [
            MessageHandler(Filters.regex(
                "^(😊Hammasi yoqdi ❤️|☺️Yaxshi ⭐️⭐️⭐️⭐️)$"), handlers.comment_good_result_handler),
            MessageHandler(Filters.regex(
                "^(😐Yoqmadi ⭐️⭐️⭐️|🙁Yomon ⭐️⭐️|😤Juda yomon 👎)$"), handlers.comment_bad_result_handler),
            MessageHandler(Filters.regex("^(🏘 Bosh menu)$"),
                           handlers.back_to_home_handler),
            MessageHandler(Filters.all, handlers.back_to_home_handler)
        ],
        states.SETTINGS_STATE: [
            MessageHandler(Filters.regex(
                "^🌐 Tilni tanlash$"), handlers.language_handler),
            CallbackQueryHandler(handlers.lang_uz_handler, pattern="^uz$"),
            CallbackQueryHandler(handlers.lang_ru_handler, pattern="^ru$"),

            MessageHandler(Filters.regex(
                "^(📱 Raqamni o'zgartirish)$"), handlers.send_phone_number_handler),

            MessageHandler(Filters.regex(
                "^(🏘 Bosh menu)$"), handlers.back_to_home_handler),
        ],
        states.BASKET_STATE: [
            MessageHandler(Filters.regex(
                "^(🔄 Tozalash)$"), handlers.clear_card),
            MessageHandler(Filters.regex(
                "^(🚖 Buyurtma berish)$"), handlers.placing_order_handler),
            MessageHandler(Filters.regex(
                "^(🚖 Yetkazib berish)$"), handlers.delivery_handler),
            MessageHandler(Filters.regex(
                "^(🏃 Olib ketish)$"), handlers.take_away_handler),
            MessageHandler(Filters.regex("^🛍 Пакет$"), handlers.backet_pakect),
            MessageHandler(Filters.regex("^(🏘 Bosh menu)$"),
                           handlers.back_to_home_handler),
        ]
    },
    fallbacks=[MessageHandler(Filters.all, handlers.back_to_home_handler)]
)
