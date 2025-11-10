# strategy.py
from config import PRICE_ALERT_THRESHOLD_PERCENT, ALERT_PERIOD

# ပုံမှန် Signal တွက်ချက်ခြင်း (rsi > 70/macd < 0 စသည်ဖြင့်)
def generate_signal(df):
    last = df.iloc[-1]
    
    # LONG Signal (RSI အနိမ့်ပိုင်းကနေတက်ပြီး MACD က မြင့်လာရင်)
    if last['rsi'] < 30 and last['macd'] > 0:
        return "LONG"
    # SHORT Signal (RSI အမြင့်ပိုင်းကနေကျပြီး MACD က ကျလာရင်)
    elif last['rsi'] > 70 and last['macd'] < 0:
        return "SHORT"
    else:
        return "HOLD"

# 🔔 ချက်ချင်း စျေးနှုန်းပြောင်းလဲမှု သတိပေးချက် function
def check_price_alert(df, symbol):
    # စစ်ဆေးရန် ကာလအတွင်း အမြင့်ဆုံးနှင့် အနိမ့်ဆုံး စျေးနှုန်းများကို ယူခြင်း
    period_df = df.iloc[-ALERT_PERIOD:] 
    
    current_price = period_df['close'].iloc[-1]
    min_price = period_df['close'].min()
    max_price = period_df['close'].max()
    
    alert_msg = None
    
    # အောက်သို့ ပြုတ်ကျခြင်း ရှိမရှိ စစ်ဆေးခြင်း
    drop_percent = ((min_price - current_price) / min_price) * 100
    if drop_percent >= PRICE_ALERT_THRESHOLD_PERCENT:
        alert_msg = (
            f"🚨 <b>PRICE CRASH ALERT ({symbol})</b> 🚨\n"
            f"---------------------------------\n"
            f"💰 Price dropped by <b>{drop_percent:.2f}%</b> in the last {ALERT_PERIOD} hours!\n"
            f"💸 Current Price: ${current_price:.4f}\n"
            f"---"
        )
        
    # အပေါ်သို့ တက်ခြင်း ရှိမရှိ စစ်ဆေးခြင်း (Drop မဖြစ်မှသာ စစ်ဆေးပါ)
    pump_percent = ((current_price - min_price) / min_price) * 100
    if pump_percent >= PRICE_ALERT_THRESHOLD_PERCENT and not alert_msg: 
        alert_msg = (
            f"🚀 <b>PRICE PUMP ALERT ({symbol})</b> 🚀\n"
            f"---------------------------------\n"
            f"💰 Price pumped by <b>{pump_percent:.2f}%</b> in the last {ALERT_PERIOD} hours!\n"
            f"💸 Current Price: ${current_price:.4f}\n"
            f"---"
        )
    
    return alert_msg
