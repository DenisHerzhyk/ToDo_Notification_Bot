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

- **Database Operations**: Interacts with the SQLite database through functions defined in `db_notification.py`.
- **Message Handlers**: 
  - Display notifications.
  - Create new notifications.
  - View details of a notification.
  - Delete notifications.
- **Scheduling**: Uses `schedule` to trigger notifications at specified times.

### `todo.py`

Manages To-Do lists and tasks:

- **Database Operations**: Interacts with the SQLite database through functions defined in `db_todo.py`.
- **Message Handlers**:
  - Create new To-Do lists.
  - View existing To-Do lists.
  - Add, update, and delete tasks in a list.
- **Task Management**: Allows marking tasks with different statuses (e.g., pending, in progress, completed).

### `db_notification.py`

Contains database-related functions for managing notifications:

- **Database Connection**: Provides a connection to the SQLite database.
- **Get All Notifications**: Fetches all notifications from the database.
- **Get Notification by ID**: Fetches a specific notification by its ID.
- **Insert Notification**: Adds a new notification to the database.
- **Delete Notification**: Removes a notification from the database.

### `db_todo.py`

Contains database-related functions for managing To-Do lists and tasks:

- **Database Connection**: Provides a connection to the SQLite database.
- **Get All Lists**: Fetches all To-Do lists from the database.
- **Insert and Display Lists**: Adds a new To-Do list and fetches all lists.
- **Delete and Display Lists**: Removes a To-Do list and fetches all remaining lists.
- **Get Tasks by List ID**: Fetches all tasks associated with a specific To-Do list.
- **Get List Name by ID**: Fetches the name of a To-Do list by its ID.
- **Get Task Status**: Fetches the status and name of a specific task.
- **Update Task Status**: Updates the status of a specific task.
- **Insert and Display Tasks**: Adds a new task to a To-Do list and fetches all tasks in that list.
- **Delete and Display Task**: Removes a task from a To-Do list and fetches all remaining tasks.

## Setup and Usage

1. **Token Configuration**: Create a `.env` file in the project root directory and add your Telegram bot token:
   ```env
   BOT_TOKEN=your_telegram_bot_token_here
