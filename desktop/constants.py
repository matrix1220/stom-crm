import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

percentage = {
    "Xamza": 0.5, "Shavkat": 0.5, "UZI": 0.45, "Sadulla": 0.5, "Raximbergan": 0.5, "Oybek": 0.5,
    "Azamat": 0.5, "Bobur": 0.5, "Sherzod": 0.5, "Odilbek": 0.5, "Otabek": 0.5, "Ra'no": 0.5,
    "Baxrom": 0.5, "Abdulla": 0.5, "Orif": 0.5, "Jaloladdin": 1
}


names = percentage.keys()

files_location = os.getenv("FILES_LOCATION")
date = datetime.now().strftime("%Y-%m-%d")
files_location = os.path.join(files_location, date)
os.makedirs(files_location, exist_ok=True)

payments_file = os.path.join(files_location, "payments.csv")
labor_share_file = os.path.join(files_location, "labor_share.csv")
other_expences_file = os.path.join(files_location, "other_expences.csv")
bank_file = os.path.join(files_location, "bank.csv")
