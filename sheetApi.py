import os
from gspread import service_account
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

# Load env
load_dotenv()

SCOPES           = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

TOKEN            = os.getenv('GOOGLE_TOKEN_FILE')
BUDGET_SHEET     = os.getenv('GOOGLE_SHEET_NAME')
TRANSACTIONS_TAB = os.getenv('GOOGLE_SHEET_TRANSACTIONS')


# Example row
# ['', '1/19/2023', '55₪', '', 'Other', '💳 Credit Card', 'מנוי לסלו פארק', '✅', '']
def authenticate():
    gspread_client = service_account(filename=TOKEN)
    return gspread_client

def write_data(client,data):
    sheet = client.open(BUDGET_SHEET)
    print(TRANSACTIONS_TAB)
    transaction_worksheet = sheet.worksheet(TRANSACTIONS_TAB)
    avalible_row = next_available_row(transaction_worksheet)
    print(avalible_row)
    # sheet_instance.update_cell(1,2,data)


def next_available_row(worksheet):
    return len(worksheet.get_all_values()) + 1


client = authenticate()
output={}
write_data(client,output)
