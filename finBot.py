import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
from responses import FIXED_CHARGES_CATEGORY, FIXED_INCOME_CATEGORY, HEADER_FIXED_CHARGES, HEADER_FIXED_INCOME, HE
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning
import helper
from sheetApi import add_income, add_outcome

# Load env
load_dotenv()

# Ignore warning
filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

# ENV
BOT_TOKEN = os.getenv('BOT_TOKEN_PROD')
AUTH_USER_ID = int(os.getenv('AUTH_USER_ID'))
STEP_1_CATEGORY    = 0
STEP_1_OTHER       = 1
STEP_2_SERVICE     = 2
STEP_3_COST        = 3
STEP_1_CATEGORY_INCOME = 11
STEP_1_OTHER_INCOME    = 12
STEP_2_COST_INCOME     = 13


current_payment = {
    "category" : None,
    "category_display_name": None,
    "service"  : None,
    "cost"     : None,
    "date"     : None
}

current_income = {
    "service"   : None,
    "cost"      : None,
    "date"      : None
}


def fixed_charge_message():
  return HEADER_FIXED_CHARGES


def fixed_income_message():
  return HEADER_FIXED_INCOME


async def out(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(fixed_charge_message(), reply_markup=service_menu())
    return STEP_1_CATEGORY


async def income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(fixed_income_message(), reply_markup=income_menu())
    return STEP_1_CATEGORY_INCOME


async def fuel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_payment
    current_payment["category"] = 'Fuel'
    current_payment['category_display_name'] = FIXED_CHARGES_CATEGORY['Fuel']
    await update.callback_query.message.reply_text(HE.get('service_name'))
    return STEP_2_SERVICE


async def food(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_payment
    current_payment["category"] = 'Food'
    current_payment['category_display_name'] = FIXED_CHARGES_CATEGORY['Food']
    await update.callback_query.message.reply_text(HE.get('service_name'))
    return STEP_2_SERVICE


async def clothes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_payment
    current_payment["category"] = 'Clothes'
    current_payment['category_display_name'] = FIXED_CHARGES_CATEGORY['Clothes']
    await update.callback_query.message.reply_text(HE.get('service_name'))
    return STEP_2_SERVICE


async def tech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_payment
    current_payment["category"] = 'Tech'
    current_payment['category_display_name'] = FIXED_CHARGES_CATEGORY['Tech']
    await update.callback_query.message.reply_text(HE.get('service_name'))
    return STEP_2_SERVICE


async def groceries(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_payment
    current_payment["category"] = 'Groceries'
    current_payment['category_display_name'] = FIXED_CHARGES_CATEGORY['Groceries']
    await update.callback_query.message.reply_text(HE.get('service_name'))
    return STEP_2_SERVICE


async def hangouts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_payment
    current_payment["category"] = 'Hangouts'
    current_payment['category_display_name'] = FIXED_CHARGES_CATEGORY['Hangouts']
    await update.callback_query.message.reply_text(HE.get('service_name'))
    return STEP_2_SERVICE


async def other(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text(HE.get('other_category'))
    return STEP_1_OTHER


def service_menu():
    services = []
    for charge in FIXED_CHARGES_CATEGORY:
        services.append([InlineKeyboardButton(FIXED_CHARGES_CATEGORY[charge], callback_data=charge)])
    
    return InlineKeyboardMarkup(services)


def income_menu():
    incomes = []
    for income in FIXED_INCOME_CATEGORY:
        incomes.append([InlineKeyboardButton(FIXED_INCOME_CATEGORY[income], callback_data=income)])
    
    return InlineKeyboardMarkup(incomes)


async def bit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_income
    current_income["service"] = FIXED_INCOME_CATEGORY['Bit']
    await update.callback_query.message.reply_text(HE.get('income_amount'))
    return STEP_2_COST_INCOME


async def salary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_income
    current_income["service"] = FIXED_INCOME_CATEGORY['Salary']
    await update.callback_query.message.reply_text(HE.get('income_amount'))
    return STEP_2_COST_INCOME


async def other_income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text(HE.get('income_service'))
    return STEP_1_OTHER_INCOME


async def get_service_income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_income
    current_income['service'] = update.message.text
    await update.message.reply_text(HE.get('income_amount'))
    return STEP_2_COST_INCOME


async def get_cost_income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_income
    current_income['cost'] = update.message.text
    current_income['date'] = helper.get_date()
    await update.message.reply_text(f"{HE.get('income_completed')}\n{HE.get('service')}: {current_income['service']}\n{HE.get('cost')}: {current_income['cost']}\n{HE.get('date')}: {current_income['date']}\n.")
    if auth_user(update):
        add_income(current_income)
    return ConversationHandler.END


async def get_cost(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_payment
    current_payment['cost'] = update.message.text
    current_payment['date'] = helper.get_date()
    await update.message.reply_text(f"{HE.get('completed')}\n{HE.get('category')}: {current_payment['category_display_name']}\n{HE.get('service')}: {current_payment['service']}\n{HE.get('cost')}: {current_payment['cost']}\n{HE.get('date')}: {current_payment['date']}\n.")
    if auth_user(update):
        add_outcome(current_payment)
    return ConversationHandler.END


async def get_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_payment
    current_payment['service'] = update.message.text
    await update.message.reply_text(HE.get('service_cost'))
    return STEP_3_COST


async def get_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_payment
    current_payment['category'] = 'Other'
    current_payment['category_display_name'] = update.message.text
    await update.message.reply_text(HE.get('service_name'))
    return STEP_2_SERVICE


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HE.get('help'))


async def author(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HE.get('author'))


def auth_user(update):
    if update.message.from_user.id != AUTH_USER_ID:
        return False

    return True

app = ApplicationBuilder().token(BOT_TOKEN).build()

OUTCOME = ConversationHandler (
    entry_points = [CommandHandler("out", out)],
     states = {
        STEP_1_CATEGORY : [
            CallbackQueryHandler(fuel, pattern='Fuel'),
            CallbackQueryHandler(food, pattern='Food'),
            CallbackQueryHandler(clothes, pattern='Clothes'),
            CallbackQueryHandler(tech, pattern='Tech'),
            CallbackQueryHandler(groceries, pattern='Groceries'),
            CallbackQueryHandler(hangouts, pattern='Hangouts'),
            CallbackQueryHandler(other, pattern='Other')
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
    , fallbacks=[CommandHandler("out", out)], allow_reentry=True)


INCOME = ConversationHandler (
    entry_points = [CommandHandler("in", income)],
     states = {
        STEP_1_CATEGORY_INCOME : [
            CallbackQueryHandler(bit, pattern='Bit'),
            CallbackQueryHandler(salary, pattern='Salary'),
            CallbackQueryHandler(other_income, pattern='Other')
        ],
        STEP_1_OTHER_INCOME: [
            MessageHandler(filters.ALL , get_service_income)
        ],
        STEP_2_COST_INCOME : [
            MessageHandler(filters.ALL , get_cost_income)
        ]
    }
    , fallbacks=[CommandHandler("in", income)], allow_reentry=True)

app.add_handler(OUTCOME)
app.add_handler(INCOME)
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("author", author))
app.run_polling()