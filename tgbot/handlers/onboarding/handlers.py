import datetime

from django.utils import timezone
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, ConversationHandler

from tgbot.handlers.onboarding import static_text
from tgbot.handlers.utils.info import extract_user_data_from_update
from tgbot.handlers.utils import states
from tgbot.handlers.languages import get_text
from tgbot.handlers.onboarding import keyboards

from users.models import User
from product.models import Category, Product


def command_start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat.id
    user, created = User.get_user_and_created(update, context)
    if created:
        context.bot.send_message(chat_id, text=get_text(code="welcome"),
                                 reply_markup=keyboards.send_contact())
        return states.PHONE_STATE

    context.bot.send_message(chat_id, text=get_text("welcome"), reply_markup=keyboards.main_menyu())


def send_phone_number_handler(update: Update, context: CallbackContext):
    user = User.get_user_by_username_or_user_id(update.message.from_user.id)
    user_phone = update.message.contact.phone_number
    user.phone_number = user_phone
    user.save()

    update.message.reply_text(text=get_text("go_menu"), reply_markup=keyboards.menu_button())
    return ConversationHandler.END


def menu_handler(update: Update, context: CallbackContext):
    update.message.reply_text(text=get_text("location"), reply_markup=keyboards.send_location())
    return states.MENU_STATE


def location_handler(update: Update, context: CallbackContext):
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude
    chat_id = update.message.chat.id
    context.chat_data['latitude'] = latitude
    context.chat_data['longitude'] = longitude
    context.bot.send_message(chat_id=chat_id, text=get_text("select_category"), reply_markup=keyboards.menu_button())
    return states.CATEGORY_STATE


def category_menu(update: Update, context: CallbackContext):
    text = update.message.text
    try:
        category_id = Category.objects.get(title=text).id

        update.message.reply_text("Mahsulotlarni tanlang", reply_markup=keyboards.product_manu(category_id))
        return states.PRODUCT_STATE

    except Exception as e:
        update.message.reply_text(get_text("back_home"), reply_markup=keyboards.main_menyu())
        return ConversationHandler.END


def product_menu(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    product_title = update.message.text
    # print(product_title)
    try:
        product = Product.objects.get(title=product_title)
        if context.user_data.get("card"):
            context.user_data['card'][product.title] = {
                "product_id": product.id,
                "product_price": product.price,
            }
        else:
            context.user_data["card"] = {
                product.title: {
                    "product.id": product.id,
                    "product_price": product.price
                }
            }
        text = f"""{product_title}\n\n {product.description} \n\n 
        Vazni: {product.weight} \n\n Narxi: {product.price}"""
        context.bot.send_message(chat_id, text, reply_markup=keyboards.quantity_product())
        return states.QUANTITY_STATE
    except Exception as e:
        update.message.reply_text("Bunaqa mahsulot yo'q", reply_markup=keyboards.menu_button())


def product_quantity(update: Update, context: CallbackContext):
    quantity = update.message.text
    if quantity.isdigit():

        product_title = list(context.user_data["card"])[-1]
        product = Product.objects.get(title=product_title)
        if context.user_data.get("card"):
            context.user_data["card"][product.title] = {
                "product_id": product.id,
                "product_price": product.price,
                "quantity": quantity
            }
        else:
            context.user_data["card"] = {
                product.title: {
                    "product_id": product.id,
                    "product_price": product.price,
                    "quantity": quantity
                }
            }

        update.message.reply_text("Ajoyib tanlov, biron narsa yana buyurtma qilamizmi?",
                                  reply_markup=keyboards.menu_button())
        return states.CATEGORY_STATE
    else:
        pass


# Error handler
def back_to_product_menu(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    category_id = context.user_data['category_id']
    context.user_data['product_title'] = ""
    context.user_data['product_quantity'] = 0
    context.bot.send_message(chat_id, "Mahsulotlarni tanlang", reply_markup=keyboards.product_manu(category_id))


def order_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    print(1233)
    paket = f"2. 🛍 Пакет 1 x 1 000 so'm = 1 000 so'm"
    try:
        card = [context.user_data['card']]
        for i in card:
            card
        # title = data["product_title"]
        # product_price = int(title["product_price"])
        # quantity = int(title["product_quantity"])
        # total_price = product_price * quantity
        # text = f"""Savatingizda \n\n {list(title.keys())} \n{quantity}x{product_price}={total_price}"""
        # text += paket
        # context.bot.send_message(
        #     chat_id=chat_id, text=text, reply_markup=keyboards.basket_button())
        return states.BASKET_STATE
    except Exception as e:
        context.bot.send_message(chat_id, get_text("basket"), reply_markup=keyboards.basket_button())
        return states.BASKET_STATE


def backet_pakect(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    context.bot.send_message(chat_id, text=get_text("welcome"))
    return back_to_home_handler(update, context)


def contact_handler(update: Update, context: CallbackContext):
    text = """Buyurtma va boshqa savollar bo'yicha javob olish uchun \
    "@pastarobot ga murojaat qiling, barchasiga javob beramiz :)"""
    context.bot.send_message(chat_id=update.message.chat_id, text=get_text("contact"))


def cafe_location_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    context.bot.send_location(chat_id, latitude=41.368091, longitude=69.273425)
    context.bot.send_message(chat_id, text=get_text("cafe_location"))


def order_about_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id, text=get_text("about_order"))


def comment_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=get_text("comment"),
                             reply_markup=keyboards.comment_button())
    return states.COMMENT_STATE


def comment_good_result_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    context.bot.send_message(chat_id=chat_id, text=get_text("comment_good"))
    return back_to_home_handler(update, context)


def comment_bad_result_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    context.bot.send_message(chat_id=chat_id, text=get_text("comment_negative"))
    return back_to_home_handler(update, context)


def back_to_home_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    first_name = update.message.from_user.first_name
    context.bot.send_message(chat_id=chat_id, text=get_text("back_home"),
                             reply_markup=keyboards.main_menyu())
    return ConversationHandler.END


def settings_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=get_text("settings"),
                             reply_markup=keyboards.settings_button())
    return states.SETTINGS_STATE


def language_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    context.bot.send_message(
        chat_id=chat_id, text=get_text("select_language"), reply_markup=keyboards.language_inline())


def lang_uz_handler(update: Update, context: CallbackContext):
    chat_id = update.callback_query.message.chat_id
    update.callback_query.message.delete()
    context.bot.send_message(chat_id=chat_id, text=get_text("back_home"),
                             reply_markup=keyboards.main_menyu())
    return ConversationHandler.END


def lang_ru_handler(update: Update, context: CallbackContext):
    chat_id = update.callback_query.message.chat_id
    first_name = update.callback_query.from_user.first_name
    update.callback_query.message.delete()
    context.bot.send_message(chat_id=chat_id, text=get_text("back_home"),
                             reply_markup=keyboards.main_menyu())
    return ConversationHandler.END


def placing_order_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    context.bot.send_message(chat_id=chat_id, text=get_text("delivery"),
                             reply_markup=keyboards.placing_button())


def delivery_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    context.bot.send_message(chat_id=chat_id, text=get_text("delivery_car"))
    return ConversationHandler.END


def take_away_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    context.bot.send_message(chat_id=chat_id, text=get_text("take_away"))


def secret_level(update: Update, context: CallbackContext) -> None:
    # callback_data: SECRET_LEVEL_BUTTON variable from manage_data.py
    """ Pressed 'secret_level_button_text' after /start command"""
    user_id = extract_user_data_from_update(update)['user_id']
    text = static_text.unlock_secret_room.format(
        user_count=User.objects.count(),
        active_24=User.objects.filter(updated_at__gte=timezone.now() - datetime.timedelta(hours=24)).count()
    )

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML
    )
