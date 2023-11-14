import os
import shutil
import telebot
from telebot import types

bot_token = os.environ.get("TELEGRAM_TOKEN")
bot = telebot.TeleBot(bot_token)

adds = [int(x) for x in os.environ.get("TELEGRAM_CHAT_ID").split(',')]


def list_files_and_folders(directory):
    items = os.listdir(directory)
    file_list = []
    folder_list = []

    for item in items:
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            file_list.append(f"📄 {item}")
        elif os.path.isdir(item_path):
            folder_list.append(f"📁 {item}")

    return file_list, folder_list


@bot.message_handler(commands=['start'])
def send_files_and_folders(message):
    user_id = message.chat.id

    if user_id not in adds:
        return None

    current_directory = os.getcwd()
    files, folders = list_files_and_folders(current_directory)

    markup = types.ReplyKeyboardMarkup(row_width=1)
    for file in files:
        markup.add(types.KeyboardButton(file))
    for folder in folders:
        markup.add(types.KeyboardButton(folder))

    bot.send_message(message.chat.id, "اختر احد الملفات او الفايلات:", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def send_options(message):
    user_id = message.chat.id

    if user_id not in adds:
        return None

    try:
        chat_id = message.chat.id
        selected_item = message.text.split(" ", 1)[1]

        markup = types.InlineKeyboardMarkup()
        delete_button = types.InlineKeyboardButton("حذف", callback_data=f"delete_{selected_item}")
        download_button = types.InlineKeyboardButton("تحميل", callback_data=f"download_{selected_item}")
        markup.add(delete_button, download_button)

        global a

        a = bot.send_message(chat_id, "اختر احد الخيارات:", reply_markup=markup)

        remove_markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(chat_id, "😁", reply_markup=remove_markup)


    except Exception as e:
        bot.reply_to(message, f"حدث خطأ راسل المطور @vpsRdp_r")


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    user_id = call.from_user.id

    if user_id not in adds:
        return None

    try:
        chat_id = call.message.chat.id
        selected_item = call.data.split('_')[1]

        item_path = os.path.join(os.getcwd(), selected_item)

        if call.data.startswith("download"):
            if os.path.isfile(item_path):

                with open(item_path, 'rb') as file:
                    bot.delete_message(chat_id, message_id=a.message_id)
                    bot.send_document(chat_id, file)
            elif os.path.isdir(item_path):

                shutil.make_archive(item_path, 'zip', item_path)
                with open(item_path + '.zip', 'rb') as zip_file:
                    bot.delete_message(chat_id, message_id=a.message_id)
                    bot.send_document(chat_id, zip_file)

                os.remove(item_path + '.zip')

        elif call.data.startswith("delete"):
            if os.path.isfile(item_path):

                os.remove(item_path)
                bot.delete_message(chat_id, message_id=a.message_id)
                bot.send_message(chat_id, f" الملف '{selected_item}' تم حذفه ")
            elif os.path.isdir(item_path):

                shutil.rmtree(item_path)
                bot.delete_message(chat_id, message_id=a.message_id)
                bot.send_message(chat_id, f" المجلد '{selected_item}' تم حذفه ")

    except Exception as e:
        bot.send_message(chat_id, f"حدث خطأ راسل المطور @vpsRdp_r")


bot.polling()
