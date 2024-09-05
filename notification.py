from telebot import types, formatting
from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from datetime import datetime
import schedule

from db_notification import db_get_all_notifications, db_get_notification_by_id, db_insert_notification, db_delete_notification


def notification(bot):
    @bot.message_handler(func=lambda message: message.text == "Notifications")
    @bot.message_handler(commands=["shownotifications"])
    def display_notifications(message):
        notifications = db_get_all_notifications()

        keyboard = InlineKeyboardMarkup()
        for notification in notifications:
            title_button = InlineKeyboardButton(text=f"{notification['title']}",
                                                callback_data=f"notification_{notification['id']}")
            keyboard.add(title_button)

        caption = "Your List is Empty" if len(notifications) == 0 else f"Select your Notification:"
        bot.send_photo(message.chat.id, open("static/notification.png", "rb"), caption=caption,
                       reply_markup=keyboard)
        create_notification_button = KeyboardButton("+")
        go_back_button = KeyboardButton("🡸")
        reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
            create_notification_button).add(go_back_button)
        msg = bot.send_message(message.chat.id, "👇", reply_markup=reply_keyboard)
        bot.register_next_step_handler(msg, handle_notification_navigation)

    @bot.message_handler(commands=['menu'])
    def menu(message):
        text = "Choose whats you gonna manage: "
        button_todo = KeyboardButton('To-Do')
        button_reminder = KeyboardButton('Notifications')
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_todo, button_reminder)
        bot.send_message(message.chat.id, text, reply_markup=keyboard)

    def handle_notification_navigation(message):
        if message.text == "+":
            create_notification(message)
        elif message.text == "🡸":
            menu(message)

    @bot.message_handler(commands=["createnotification"])
    def create_notification(message):
        text = "Meeting, Discuss project details, 2024/07/15 14:30"
        msg = bot.send_message(message.chat.id,
                               f"Example: {formatting.mbold(text)}\nEnter name, description and date of your new Notification:",
                               parse_mode="MarkdownV2")
        bot.register_next_step_handler(msg, process_notification)

    def process_notification(message):
        try:
            data = message.text.split(", ")
            if len(data) != 3:
                raise ValueError("Wrong Input!")
            title, description = data[0], data[1]
            splitting_data = data[2].split(" ")
            year, month, day = map(int, splitting_data[0].split("/"))
            hours, minutes = map(int, splitting_data[1].split(":"))

            db_insert_notification(title, description, year, month, day, hours, minutes)
            schedule_notification(message, title, description, year, month, day, hours, minutes)
            display_notifications(message)
        except ValueError as e:
            bot.send_message(message.chat.id, f"Error: {str(e)}. Try correct format!", parse_mode="Markdown")
        except Exception as e:
            bot.send_message(message.chat.id, f"An unexpected error occurred: {str(e)}", parse_mode="Markdown")

    @bot.callback_query_handler(func=lambda call: call.data.startswith("notification_"))
    def show_notification_details(call: types.CallbackQuery):
        notification_id = call.data.split("_")[-1]
        curr_notification = db_get_notification_by_id(notification_id)

        update_button = KeyboardButton("Update(Coming soon)")
        delete_notification_button = KeyboardButton("❌")
        go_back_button = KeyboardButton("🡸")
        reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(update_button).add(
            delete_notification_button).add(go_back_button)

        date = f"{curr_notification['year']}/{curr_notification['month']}/{curr_notification['day']} {curr_notification['hours']}:{curr_notification['minutes']}"
        msg = bot.send_message(call.message.chat.id,
                               f"{formatting.mbold(curr_notification['title'])}\n{formatting.mitalic(date)}\n\nDescription: {curr_notification['description']}",
                               parse_mode="MarkdownV2", reply_markup=reply_keyboard)
        bot.register_next_step_handler(msg, lambda m: handle_notification_details_navigation(m, notification_id))

    def handle_notification_details_navigation(message, notification_id=None):
        if message.text == "Update(Coming soon)":
            bot.send_message(message.chat.id, "I still working on it!!", parse_mode="Markdown")
        elif message.text == "🡸":
            display_notifications(message)
        elif message.text == "❌":
            delete_notification(message, notification_id)

    def delete_notification(message, notification_id):
        db_delete_notification(notification_id)
        display_notifications(message)

    def schedule_notification(message, title, description, year, month, day, hours, minutes):
        notification_time = datetime(year, month, day, hours, minutes)
        schedule.every().day.at(notification_time.strftime("%H:%M")).do(send_notification_message, message, title,
                                                                        description, year, month, day, hours, minutes)

    def send_notification_message(message, title, description, year, month, day, hours, minutes):
        bot.send_message(message.chat.id,
                         f"🔔 Notification: {formatting.mbold(title)}  {formatting.mitalic(f'{year}/{month}/{day} {hours}:{minutes}')}\nDescription: {description}",
                         parse_mode="MarkdownV2")
