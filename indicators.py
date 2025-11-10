# indicators.py
import ta
import pandas as pd # ta.trend.MACD မှာ DataFrame လိုအပ်လို့ import လုပ်ပါ

def add_indicators(df):
    # RSI
    df['rsi'] = ta.momentum.RSIIndicator(df['close']).rsi()
    
    # MACD (MACD_Diff က MACD - MACD_Signal ဖြစ်သည်)
    macd = ta.trend.MACD(close=df['close'], window_fast=12, window_slow=26, window_sign=9)
    df['macd'] = macd.macd_diff()
    
    return df
