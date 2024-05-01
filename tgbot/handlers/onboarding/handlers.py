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
from product.models import Category, Product, Card, Order


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
    update.message.reply_text(text=get_text("go_menu"), reply_markup=keyboards.main_menyu())
    return ConversationHandler.END


def send_phone_entity_handler(update: Update, context: CallbackContext):
    phone_number_entity = list(filter(lambda e: e.type == "phone_number", update.message.entities))[0]
    phone_number = update.message.text[
                   phone_number_entity.offset:phone_number_entity.offset + phone_number_entity.length]
    user = User.get_user_by_username_or_user_id(update.message.from_user.id)
    user.phone_number = phone_number
    user.save()
    update.message.reply_text(text=get_text("go_menu"), reply_markup=keyboards.main_menyu())

    return ConversationHandler.END


def send_phone_resent_handler(update: Update, context: CallbackContext):
    update.message.reply_text("Telefon raqamingiz yozing yoki Pastdagi tugmani bosing",
                              reply_markup=keyboards.send_contact())


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
    print(context.user_data)
    try:
        product = Product.objects.get(title=product_title)
        context.user_data["card"] = {
            "product_title": product.title,
            "product_price": product.price,
            "product_weight": product.weight
        }
        text = f"""{product_title}\n\n {product.description} \n\n 
        Vazni: {product.weight} \n\n Narxi: {product.price}"""
        context.bot.send_message(chat_id, text, reply_markup=keyboards.quantity_product())
        return states.QUANTITY_STATE
    except Exception as e:
        print(e)
        update.message.reply_text("Bunaqa mahsulot yo'q", reply_markup=keyboards.menu_button())


# Error handler
def back_to_product_menu(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    print(context.user_data)
    return product_menu(update, context)
    # category_id = context.user_data['card']['category_id']
    # context.user_data['card']['product_title'] = ""
    # context.user_data['card']['product_quantity'] = 0
    # context.bot.send_message(chat_id, "Mahsulotlarni tanlang", reply_markup=keyboards.product_manu(category_id))


def product_quantity(update: Update, context: CallbackContext):
    quantity = update.message.text
    chat_id = int(update.message.chat.id)
    if quantity.isdigit():
        a = list(context.user_data.values())[0]
        user = User.objects.get(user_id=chat_id)
        product_title = a['product_title']
        product_price = int(a["product_price"])
        total_price = product_price * int(quantity)
        card, created = Card.objects.get_or_create(product_title=product_title, user=user)
        if created:
            card.product_price = product_price
            card.quantity = int(quantity)
            card.total_price = total_price
            card.save()
        else:
            card.product_price = product_price
            card.quantity = int(quantity)
            card.total_price = total_price
            card.save()

        update.message.reply_text("Ajoyib tanlov, biron narsa yana buyurtma qilamizmi?",
                                  reply_markup=keyboards.menu_button())
        return states.CATEGORY_STATE

    else:
        pass


def order_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    try:
        user = User.objects.get(user_id=chat_id)
        product = Card.objects.filter(user=user)
        text = "Savatingiz: \n\n\n"
        a = 0
        jami = 0
        for i in product:
            a += 1
            text += f"<b>{a}. {i.product_title}</b>\n"
            text += f"{i.product_price}*{i.quantity}={i.total_price}\n\n"
            jami += i.total_price

        text += f"🛍 Пакет 1 x 1 000 so'm = 1 000 so'm\n\n <b>Jami: {jami + 1000}</b>"

        context.bot.send_message(
            chat_id=chat_id, text=text, reply_markup=keyboards.basket_button(), parse_mode="HTML")
        return states.BASKET_STATE
    except Exception as e:
        context.bot.send_message(chat_id, get_text("basket"), reply_markup=keyboards.basket_button())
        return states.BASKET_STATE


def clear_card(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    user = User.objects.get(user_id=chat_id)
    try:
        Card.objects.filter(user=user).delete()
    except Exception as e:
        pass
    context.bot.send_message(chat_id, "Savatingiz bo'shatildi", reply_markup=keyboards.main_menyu())


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
    user = User.objects.get(user_id=chat_id)
    Order.objects.create(user=user)
    context.bot.send_message(chat_id=chat_id, text=get_text("delivery_car"))
    return ConversationHandler.END


def take_away_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    user = User.objects.get(user_id=chat_id)
    Order.objects.create(user=user)
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
