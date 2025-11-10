# notifier.py
import requests
# config.py ကနေ Token နဲ့ Chat ID List ကို ယူပါ
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_IDS 

def notify(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    # ဤနေရာတွင် Token စစ်သော ကုတ်ဟောင်းကို ဖြုတ်ပြီးပါပြီ
    
    # Chat ID List ကို Loop ပတ်၍ Message ပို့ပါ
    for chat_id in TELEGRAM_CHAT_IDS: 
        params = {
            "chat_id": chat_id,
            "text": msg,
            "parse_mode": "HTML" # HTML Mode ဖွင့်ထားသည်
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status() 
            # print(f"Telegram message sent to {chat_id}.")
        except requests.exceptions.RequestException as e:
            # Unauthorized Error ကို ပြသပါ
            if response.status_code == 401:
                print(f"🚨 Telegram API Error (Status 401): Token is unauthorized. Check config.py.")
            else:
                print(f"⚠️ Telegram sending failed to {chat_id}. Error: {e}")
        except Exception as e:
            print(f"Telegram error: {e}")
