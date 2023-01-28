import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
from responses import FIXED_CHARGES_CATEGORY, HEADER_FIXED_CHARGES, HE
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning
import helper

# Load env
load_dotenv()

# Ignore warning
filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

# ENV
BOT_TOKEN = os.getenv('BOT_TOKEN')
STEP_1_CATEGORY    = 0
STEP_1_OTHER       = 1
STEP_2_SERVICE     = 2
STEP_3_COST        = 3


current_payment = {
    "category" : None,
    "service"  : None,
    "cost"     : None,
    "date"     : None
}


def main_menu_message():
  return HEADER_FIXED_CHARGES


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(main_menu_message(), reply_markup=service_menu())
    return STEP_1_CATEGORY


async def fuel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_payment
    current_payment["category"] = FIXED_CHARGES_CATEGORY['fuel']
    await update.callback_query.message.reply_text(HE.get('service_name'))
    return STEP_2_SERVICE


async def food(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_payment
    current_payment["category"] = FIXED_CHARGES_CATEGORY['food']
    await update.callback_query.message.reply_text(HE.get('service_name'))
    return STEP_2_SERVICE


async def clothes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_payment
    current_payment["category"] = FIXED_CHARGES_CATEGORY['clothes']
    await update.callback_query.message.reply_text(HE.get('service_name'))
    return STEP_2_SERVICE


async def tech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_payment
    current_payment["category"] = FIXED_CHARGES_CATEGORY['tech']
    await update.callback_query.message.reply_text(HE.get('service_name'))
    return STEP_2_SERVICE


async def other(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text(HE.get('other_category'))
    return STEP_1_OTHER


def service_menu():
    services = []
    for index,charge in enumerate(FIXED_CHARGES_CATEGORY):
        services.append([InlineKeyboardButton(FIXED_CHARGES_CATEGORY[charge], callback_data=charge)])
    
    return InlineKeyboardMarkup(services)


async def get_cost(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_payment
    current_payment['cost'] = update.message.text
    current_payment['date'] = helper.get_date()
    await update.message.reply_text(f"{HE.get('completed')}\n{HE.get('category')}: {current_payment['category']}\n{HE.get('service')}: {current_payment['service']}\n{HE.get('cost')}: {current_payment['cost']}\n{HE.get('date')}: {current_payment['date']}\n.")
    return ConversationHandler.END


async def get_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_payment
    current_payment['service'] = update.message.text
    await update.message.reply_text(HE.get('service_cost'))
    return STEP_3_COST


async def get_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_payment
    current_payment['category'] = update.message.text
    await update.message.reply_text(HE.get('service_name'))
    return STEP_2_SERVICE


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HE.get('help'))


async def author(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HE.get('author'))


app = ApplicationBuilder().token(BOT_TOKEN).build()

CH = ConversationHandler (
    entry_points = [CommandHandler("add", add)],
     states = {
        STEP_1_CATEGORY : [
            CallbackQueryHandler(fuel, pattern='fuel'),
            CallbackQueryHandler(food, pattern='food'),
            CallbackQueryHandler(clothes, pattern='clothes'),
            CallbackQueryHandler(tech, pattern='tech'),
            CallbackQueryHandler(other, pattern='other')
        ],
        STEP_1_OTHER: [
            MessageHandler(filters.ALL , get_category)
        ],
        STEP_2_SERVICE : [
            MessageHandler(filters.ALL , get_service)
        ],
        STEP_3_COST : [
            MessageHandler(filters.ALL , get_cost)
        ]
    }
    , fallbacks=[CommandHandler("add", add)], allow_reentry=True)


app.add_handler(CH)
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("author", author))
app.run_polling()