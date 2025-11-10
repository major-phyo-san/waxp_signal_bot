# config.py
# 🔑 Token အသစ်ကို ဤနေရာတွင် ထည့်ပါ (401 Error ဖြေရှင်းရန်)
TELEGRAM_BOT_TOKEN = "8354769502:AAEh0GFyWUk0ONOjhy7v9p_nellMa8vIygI" 

# Chat ID ကို List ပုံစံဖြင့် ထားပါ (Notifier မှာ Loop ပတ်ဖို့ လိုအပ်သည်)
TELEGRAM_CHAT_IDS = ["1942156483"] # သင့် Chat ID ကိုသာ ထည့်ပါ

# Symbol များစွာ စစ်ဆေးနိုင်ရန် List အဖြစ် ထားပါ
SYMBOLS = ["WAXPUSDT", "BTCUSDT", "SOLUSDT", "ETHUSDT"]

# Price Alert အတွက် သတ်မှတ်ချက်များ
PRICE_ALERT_THRESHOLD_PERCENT = 10 # 10% ပြောင်းလဲရင် Alert ပေးမည်
ALERT_PERIOD = 6 # ၆ နာရီအတွင်း စစ်ဆေးမည်

import requests, pandas as pd 
