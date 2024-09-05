# Telegram Bot for To-Do Lists and Notifications

This project is a Telegram bot that helps users manage To-Do lists and notifications. It provides functionalities to create, view, and manage tasks and reminders directly within Telegram.

## Project Overview

### Key Features

- **To-Do Lists**
  - Create new To-Do lists.
  - View existing lists.
  - Add, update, and delete tasks.
  - Mark tasks as complete or incomplete.

- **Notifications**
  - Create and schedule notifications.
  - View scheduled notifications.
  - Delete notifications.

## Files and Modules

### `main.py`

This is the entry point for the bot. It initializes the Telegram bot and starts the polling loop to keep the bot running. It also starts a separate thread to handle scheduled notifications.

### `notification.py`

Handles all functionalities related to notifications:

- **Database Operations**: Connects to an SQLite database to manage notifications.
- **Message Handlers**: 
  - Display notifications.
  - Create new notifications.
  - View details of a notification.
  - Delete notifications.
- **Scheduling**: Uses `schedule` to trigger notifications at specified times.

### `todo.py`

Manages To-Do lists and tasks:

- **Database Operations**: Connects to an SQLite database to manage To-Do lists and tasks.
- **Message Handlers**:
  - Create new To-Do lists.
  - View existing To-Do lists.
  - Add, update, and delete tasks in a list.
- **Task Management**: Allows marking tasks with different statuses (e.g., pending, in progress, completed).

## Setup and Usage

1. **Token Configuration**: Replace the `BOT_TOKEN` variable in `notification.py` and `todo.py` with your Telegram bot token obtained from [BotFather](https://t.me/botfather).

2. **Database Setup**: Initialize your SQLite database with SQLite using db.py file.
