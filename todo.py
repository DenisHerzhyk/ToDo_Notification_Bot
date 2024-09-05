from telebot import types, formatting
from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from db_todo import db_get_all_lists, db_insert_and_display_lists, db_delete_and_display_lists, db_get_tasks_by_id, \
    db_get_list_name_by_id, db_get_task_status, db_update_task_status, db_insert_and_display_tasks, db_delete_and_display_task


def todo(bot):
    status_emoji = {0: "🔴", 1: "🟠", 2: "🟢"}



    @bot.message_handler(commands=['start', 'help'])
    def start(message):
        bot.send_message(message.chat.id,
                         "I'm here to assist you with managing your tasks and notifications.\n\n"
                         "⚙️General:\n"
                         "/start, /help - push bot and start to create lists.\n"
                         "/menu - choose menu to work with To-Do lists or Notifications\n\n"
                         "📋To-Do List: \n"
                         "/showtodo - display all your existed list.\n"
                         "/createtodo - create new list setting the name.\n\n"
                         "⏰Notification: \n"
                         "/shownotifications - display the list of active notifications.\n"
                         "/createnotification - create new notification setting the information "
                         "(title, description, year, month, day, hours, minutes) in this format: "
                         f"{formatting.mbold('Meeting, Meeting with colleges, 2024/08/05 14:30')}\n\n"
                         "⚡️Feel free to use these commands to stay organized and on track with your schedule!",
                         parse_mode="Markdown")
        menu(message)

    @bot.message_handler(commands=['menu'])
    def menu(message):
        text = "Choose whats you gonna manage: "
        button_todo = KeyboardButton('To-Do')
        button_reminder = KeyboardButton('Notifications')
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_todo, button_reminder)
        bot.send_message(message.chat.id, text, reply_markup=keyboard)

    @bot.message_handler(func=lambda message: message.text == 'To-Do')
    @bot.message_handler(commands=['showtodo'])
    def display_todo_lists(message):
        lists = db_get_all_lists()

        keyboard = InlineKeyboardMarkup()
        todo_list_names(lists, keyboard)
        caption = "Your List is Empty" if len(lists) == 0 else "Select your To-Do list: "
        bot.send_photo(message.chat.id, open("static/todo.png", "rb"), caption=caption, reply_markup=keyboard)

        create_button = KeyboardButton("+")
        go_back_button = KeyboardButton("🡸")
        reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(create_button).add(
            go_back_button)
        msg = bot.send_message(message.chat.id, "👇", reply_markup=reply_keyboard)
        bot.register_next_step_handler(msg, lambda m: handle_todo_navigation(m))

    def handle_todo_navigation(message):
        if message.text == "+":
            create_todo_list(message)
        elif message.text == "🡸":
            menu(message)

    @bot.message_handler(commands=['createtodo'])
    def create_todo_list(message):
        msg = bot.send_message(message.chat.id, "Enter name of your new To-Do list: ", parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_todo_list)

    def process_todo_list(message):
        todo_name = message.text
        lists = db_insert_and_display_lists(todo_name)

        keyboard = InlineKeyboardMarkup()
        todo_list_names(lists, keyboard)
        display_todo_lists(message)

    def delete_todo_list(message, list_id):
        try:
            lists = db_delete_and_display_lists(list_id)

            keyboard = InlineKeyboardMarkup()
            todo_list_names(lists, keyboard)
            try:
                bot.edit_message_reply_markup(message.chat.id, message.message_id, reply_markup=keyboard)
            except Exception:
                display_todo_lists(message)
        except Exception as e:
            bot.send_message(message.chat.id, f"Error: {e}", parse_mode="Markdown")

    def todo_list_names(lists, keyboard):
        for row in lists:
            todo_names_buttons = InlineKeyboardButton(text=row['name'], callback_data=f"todo_{row['id']}")
            keyboard.add(todo_names_buttons)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("todo_"))
    def display_todo_tasks(call: types.CallbackQuery):
        list_id = call.data.split("_")[-1]
        show_tasks(call.message, list_id)

    def show_tasks(message, list_id):
        tasksall = db_get_tasks_by_id(list_id)

        keyboard = InlineKeyboardMarkup()
        todo_task_names(tasksall, keyboard)

        list_name = db_get_list_name_by_id(list_id)

        bot.send_message(message.chat.id, f"✨__{formatting.mbold(list_name)}__ \nYour Tasks:", reply_markup=keyboard,
                         parse_mode="MarkdownV2")

        create_task_button = KeyboardButton("+1")
        go_back_button = KeyboardButton("🡸")
        delete_list_button = KeyboardButton("❌")
        reply_keyboard = (
            ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(create_task_button).add(
                delete_list_button).add(go_back_button))
        msg = bot.send_message(message.chat.id, "👇", reply_markup=reply_keyboard)
        bot.register_next_step_handler(msg, lambda m: handle_task_navigation(m, list_id))

    def handle_task_navigation(message, list_id=None):
        if message.text == "🡸":
            display_todo_lists(message)
        if message.text == "+1":
            create_todo_task(message, list_id)
        elif message.text == "❌":
            delete_todo_list(message, list_id)

    @bot.callback_query_handler(lambda call: call.data.startswith("task_"))
    def change_task_status(call: types.CallbackQuery):
        list_id = call.data.split("_")[-2]
        task_id = call.data.split("_")[-1]

        task = db_get_task_status(task_id)

        new_status = (task['status'] + 1) % 3
        update_task_status(task_id, new_status)

        tasksall = db_get_tasks_by_id(list_id)

        keyboard = InlineKeyboardMarkup()
        todo_task_names(tasksall, keyboard)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=keyboard)

    def update_task_status(task_id, new_status):
        db_update_task_status(task_id, new_status)

    def create_todo_task(message, list_id=None):
        if list_id is None:
            bot.send_message(message.chat.id, "Please select a list!")
            return

        msg = bot.send_message(message.chat.id, "Please enter name of your new Task: ", parse_mode="Markdown")
        bot.register_next_step_handler(msg, lambda m: process_todo_task(m, list_id))

    def process_todo_task(message, list_id):
        task_name = message.text
        tasksall = db_insert_and_display_tasks(list_id,task_name)

        keyboard = InlineKeyboardMarkup()
        todo_task_names(tasksall, keyboard)
        show_tasks(message, list_id)

    @bot.callback_query_handler(lambda call: call.data.startswith("delete_task_"))
    def delete_todo_task(call: types.CallbackQuery):
        list_id = call.data.split("_")[-2]
        task_id = call.data.split("_")[-1]

        tasksall = db_delete_and_display_task(list_id, task_id)

        keyboard = InlineKeyboardMarkup()
        todo_task_names(tasksall, keyboard)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=keyboard)

    def todo_task_names(tasksall, keyboard):
        for row in tasksall:
            if 'list_id' in row.keys() and 'id' in row.keys():
                task_name_button = InlineKeyboardButton(text=f"{status_emoji[row['status']]} {row['name']}",
                                                        callback_data=f"task_{row['list_id']}_{row['id']}")
                delete_button = InlineKeyboardButton(text="✖",
                                                     callback_data=f"delete_task_{row['list_id']}_{row['id']}")
                keyboard.add(task_name_button, delete_button)
