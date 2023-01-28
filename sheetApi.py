import os
from gspread import service_account
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
from datetime import datetime

# Load env
load_dotenv()

SCOPES           = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

TOKEN            = os.getenv('GOOGLE_TOKEN_FILE')
BUDGET_SHEET     = os.getenv('GOOGLE_SHEET_NAME')
TRANSACTIONS_TAB = os.getenv('GOOGLE_SHEET_TRANSACTIONS')


# Example row
def authenticate():
    gspread_client = service_account(filename=TOKEN)
    return gspread_client

def write_data(client,data):
    sheet = client.open(BUDGET_SHEET)
    transaction_worksheet = sheet.worksheet(TRANSACTIONS_TAB)
    avalible_row = next_available_row(transaction_worksheet)
    transaction_worksheet.update(f'B{avalible_row}:H{avalible_row}', [data], value_input_option='USER_ENTERED')

def next_available_row(worksheet):
    return len(worksheet.get_all_values()) + 1


def add_outcome(data):
    client = authenticate()
    outcome_data = [data['date'], data['cost'], '', data['category'], '💳 Credit Card', data['service'], '✅']
    write_data(client,outcome_data)


def add_income(data):
    client = authenticate()
    outcome_data = [data['date'], '', data['cost'], '↕️ Account Transfer', '💳 Credit Card', data['service'], '✅']
    write_data(client,outcome_data)