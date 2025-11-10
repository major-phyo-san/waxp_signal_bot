# data_fetcher.py
import requests, pandas as pd

# get_data ကို symbol ကို လက်ခံအောင် ပြင်ဆင်ပြီး df အပြည့်အစုံ ပြန်ပို့သည်
def get_data(symbol, limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit={limit}"
    
    try:
        data = requests.get(url).json()
        
        if not isinstance(data, list):
            # API Error တွေကို ရှောင်ရှားရန်
            print(f"Binance API Error for {symbol}: Data is not a list.")
            return pd.DataFrame() 

        df = pd.DataFrame(data, columns=[
            'time', 'open', 'high', 'low', 'close', 'volume', 
            'close_time', 'quote_asset_volume', 'trades', 
            'taker_base_vol', 'taker_quote_vol', 'ignore'
        ])
        
        # indicator တွက်ချက်ဖို့ 'close' နဲ့ 'volume' ကို float ပြောင်းပါ
        df['close'] = df['close'].astype(float)
        df['volume'] = df['volume'].astype(float)
        
        # df အားလုံးကို ပြန်ပို့သည် (indicators.py အတွက်)
        return df
    
    except requests.exceptions.RequestException as e:
        print(f"Data Fetcher Connection Error for {symbol}: {e}")
        return pd.DataFrame() 
    except Exception as e:
        print(f"Data Processing Error for {symbol}: {e}")
        return pd.DataFrame()
