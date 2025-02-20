import os
import json
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from agent.agent import agent
from telegram.constants import ParseMode
from notion_client import Client
from notion_integration import write_activity
from telegram.ext import CallbackQueryHandler
from agent.prompts import SYSTEM_PROMPT

# 🔐 Load our secret settings
load_dotenv()

# 🔑 Get the bot token (like getting the key to start our bot)
TOKEN = os.getenv('TELEGRAM_TOKEN')

NOTION_API_KEY = os.getenv('NOTION_API_KEY')
client = Client(auth=NOTION_API_KEY)

# 👋 This function runs when someone starts the bot
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Greets users when they first start the bot"""
    await update.message.reply_text('Hello! 👋 I am your friendly bot assistant! Send me any message and I will respond! 🌟')



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responds to user messages with a friendly message"""
    
    if "messages" not in context.user_data:
        context.user_data["messages"] = [{
            "role": "system",
            "content": SYSTEM_PROMPT
        }]

    # Add user message to the chat history
    context.user_data["messages"].append({"role": "user", "content": update.message.text})

    messages = context.user_data["messages"]

    response = agent(messages)

    if response["content"] != "":
        context.user_data["messages"].append({"role": "assistant", "content": response["content"]})
        await update.message.reply_text(response["content"], parse_mode=ParseMode.MARKDOWN)
    else:
        context.user_data["messages"].append({"role": "assistant", "content": response["trip_summary"]["summary"]})
        await update.message.reply_text(response["trip_summary"]["summary"], parse_mode=ParseMode.MARKDOWN)

        # Ask if we should save in Notion...
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data='save_yes')],
            [InlineKeyboardButton("No", callback_data='save_no')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Do you want to save this information?', reply_markup=reply_markup)

        await write_activity(
            location=response["trip_summary"]["location"],
            language=response["trip_summary"]["language"],
            currency=response["trip_summary"]["currency"],
            landscape_types=response["trip_summary"]["landscape_types"],
            best_months_to_visit=response["trip_summary"]["best_months_to_visit"],
            budget=response["trip_summary"]["budget"],
            food=response["trip_summary"]["food"],
            activities=response["trip_summary"]["activities"]
        )



# 🔑 This function handles any callback queries
async def handle_callback(update, messages):
    """Handles callback queries from inline buttons."""
    query = update.callback_query
    await query.answer()

    if query.data == 'save_yes':
        await query.edit_message_text("Saving to Notion...")
        
        # print(messages)
        # # Save to Notion
        # await write_activity(
        #     location=response["trip_summary"]["location"],
        #     language=response["trip_summary"]["language"],
        #     currency=response["trip_summary"]["currency"],
        #     landscape_types=response["trip_summary"]["landscape_types"],
        #     best_months_to_visit=response["trip_summary"]["best_months_to_visit"],
        #     budget=response["trip_summary"]["budget"],
        #     food=response["trip_summary"]["food"],
        #     activities=response["trip_summary"]["activities"]
        # )

        await query.edit_message_text("Activity saved to Notion successfully! ✅")

    elif query.data == 'save_no':
        await query.edit_message_text("Okay, no worries. Let me know if you change your mind! 😊")



# 🚨 This function handles any errors that might happen
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Logs errors"""
    print(f'Oops! 😅 Update {update} caused error {context.error}')



# 🎮 Main function that runs our bot
def main():
    # Create the bot application
    app = Application.builder().token(TOKEN).build()
    
    # Tell the bot what to do with different types of messages
    app.add_handler(CommandHandler('start', start_command))  # Handles /start command
    app.add_handler(MessageHandler(filters.TEXT, handle_message))  # Handles text messages
    app.add_handler(CallbackQueryHandler(handle_callback))

    # Add our error handler
    app.add_error_handler(error)
    
    # Start the bot
    print('🚀 Starting bot...')
    app.run_polling(poll_interval=1)

if __name__ == '__main__':
    main()