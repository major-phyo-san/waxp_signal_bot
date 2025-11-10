# main.py
import schedule, time
from data_fetcher import get_data 
from indicators import add_indicators
from strategy import generate_signal, check_price_alert 
from notifier import notify
from config import SYMBOLS # Symbol List ကို ယူသည်

# Symbol တစ်ခုချင်းစီအတွက် Signal တွက်ချက်ခြင်း function
def check_signal(symbol):
    df = get_data(symbol) 
    
    if df.empty or len(df) < 24: # 24H data စစ်ဆေးရန် အနည်းဆုံး 24 bars ရှိရပါမည်
        print(f"⚠️ {symbol} အတွက် Data မလုံလောက်ပါ (24H change တွက်ရန်)")
        return
        
    df = add_indicators(df)
    
    # 🔔 Price Alert စစ်ဆေးခြင်း
    price_alert_msg = check_price_alert(df, symbol)
    if price_alert_msg:
        notify(price_alert_msg)
        
    # 📊 ပုံမှန် Indicator Signal တွက်ချက်ခြင်း
    last = df.iloc[-1]
    
    signal = generate_signal(df)
    price = last['close']
    rsi_val = last['rsi']
    macd_val = last['macd']
    volume_val = last['volume']
    
    # --- 🟢 စျေးနှုန်း ပြောင်းလဲမှု တွက်ချက်ခြင်း (24H) ---
    # 24H အရင်စျေးနှုန်းကို ယူခြင်း (Index -24)
    # data_fetcher က 1h interval ယူထားတာကြောင့် -24 index သည် 24 နာရီအကြာက စျေးနှုန်းဖြစ်သည်
    price_24h_ago = df.iloc[-24]['close'] 
    
    # ရာခိုင်နှုန်း ပြောင်းလဲမှုကို တွက်ချက်ခြင်း
    change_percent = ((price - price_24h_ago) / price_24h_ago) * 100
    
    # 24H Change Display အတွက် အရောင်နှင့် Icon သတ်မှတ်ခြင်း
    if change_percent > 0:
        change_display = f"🟢 <b>+{change_percent:.2f}%</b>"
    elif change_percent < 0:
        change_display = f"🔴 <b>{change_percent:.2f}%</b>"
    else:
        change_display = f"🟡 <b>{change_percent:.2f}%</b>"
    
    # --- 🟢 လက်ရှိ စျေးနှုန်း အရောင် ပြောင်းလဲမှု (Previous Hour) ---
    previous_price = df.iloc[-2]['close']
    
    if price > previous_price:
        price_icon = "🟢" # Green Up Icon
    elif price < previous_price:
        price_icon = "🔴" # Red Down Icon
    else:
        price_icon = "🟡" # No Change Icon
        
    # Current Price ဂဏန်းကို Bold လုပ်ရန်
    current_price_display = f"<b>${price:.4f}</b>"

    # 🔑 Signal အရ အရောင်နှင့် စာသား သတ်မှတ်ခြင်း
    if signal == "LONG":
        signal_display = f"🟢 <b><tg-spoiler>LONG (BUY)</tg-spoiler></b>" 
    elif signal == "SHORT":
        signal_display = f"🔴 <b><tg-spoiler>SHORT (SELL)</tg-spoiler></b>"
    else:
        signal_display = f"🟡 <b>HOLD</b>"

    # 💡 RSI အခြေအနေ တွက်ချက်ခြင်း
    rsi_status = ""
    if rsi_val <= 35:
        rsi_status = "Oversold!"
    elif rsi_val >= 65:
        rsi_status = "Overbought!"
    
    
    # ဇယား Message တည်ဆောက်ခြင်း (HTML Mode)
    msg = (
        f"📈📉 <b>{symbol} Hourly Signal</b>\n"
        f"----------------------------------------\n"
        f"⏳ Timeframe: <b>1 Hour</b>\n"
        f"💰 <b>Current Price:</b> {price_icon} {current_price_display}\n"
        f"📊 <b>24H Change:</b> {change_display}\n" # ⬅️ ဤလိုင်းအသစ်ကို ထပ်ထည့်လိုက်သည်
        f"✨ <b>Signal:</b> {signal_display}\n"
        f"----------------------------------------\n"
        f"📉 <b>Indicator Details:</b>\n"
        f"<code>" 
        f"| Indicator   | Value     | Status      |\n" 
        f"|-------------|-----------|-------------|\n"
        f"| RSI         | {rsi_val: <9.2f} | {rsi_status:<11}|\n" 
        f"| MACD Diff   | {macd_val: <9.4f} | {'':<11} |\n"
        f"| Volume      | {volume_val: <9.0f} | {'':<11} |\n"
        f"</code>\n"
        f"---"
        f"\n"
        f"<a href='https://www.tradingview.com/chart/?symbol=BINANCE%3A{symbol}'>📈 Trading View Chart ကို ဤနေရာတွင် ကြည့်ရန်</a>" 
    )
    
    # Terminal မှာ Output ပြခြင်း
    print(f"📊 {symbol} ${price:.4f} | Signal: {signal} | 24H Change: {change_percent:.2f}%")
    
    # ပုံမှန် Signal Message ပို့ခြင်း
    notify(msg) 

# Symbol စာရင်းအားလုံးကို Loop ပတ်ပြီး check_signal function ခေါ်ခြင်း
def run_bot():
    for symbol in SYMBOLS:
        check_signal(symbol)

# Bot ကို စတင်ခြင်း
schedule.every(30).minutes.do(run_bot) 

print("🚀 Signal Bot started (checks every 30 minutes).")

# ⬇️ Run တာနဲ့ ချက်ချင်း Message ပို့စေရန် ဤလိုင်းကို ထပ်ထည့်ပါ
run_bot() 

# Bot ကို အမြဲ Run နေစေရန်
while True:
    schedule.run_pending()
    time.sleep(1)
