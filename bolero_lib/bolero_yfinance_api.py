def GetRecentPriceData(symbol, interval_):
    import yfinance as yf
    # Valid intervals: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]")')
    #  Open        High         Low       Close   Adj Close  Volume
    df = yf.download(tickers=symbol, period="1d", interval=interval_)
    if(len(df) < 2):
        return None

    line = df.iloc[-2] # 一番最新の-1はゼロになっているので、最新から2番目にする。
    # print(line)
    return line

def CalcHighLowCloseOpen(symbol_data):
    hl = symbol_data["High"] - symbol_data["Low"]
    co = symbol_data["Close"] - symbol_data["Open"]
    return [hl, co]