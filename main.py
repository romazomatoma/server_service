def SampleOfIntervalCall():
    def GetNowTime():
        import datetime
        t_delta = datetime.timedelta(hours=9)
        JST = datetime.timezone(t_delta, 'JST')
        return datetime.datetime.now(JST)

    def GetComputerInfo():
        import socket
        hostName = socket.gethostname()
        ip_address = socket.gethostbyname(hostName)
        return ip_address + ", " + hostName

    def func():
        pcInfo = GetComputerInfo()
        timeStr = GetNowTime().strftime('%m/%d %H:%M:%S')
        return pcInfo + " : " + timeStr

    import bolero_line_notify
    bolero_line_notify.SendMessageInterval(":00", func)

def SampleOfYahooFApiTime():
    # pip install yfinanceインストール可能。
    # yfinanceは取得銘柄に応じて、時間が異なる。
    import yfinance as yf

    # 参考：世界の現在時刻
    # https://www.time-j.net/WorldTime/NOW

    gold = yf.download(tickers="GC=F", period="1d", interval="1m")
    print(f"gold(14時間のずれのためNY時間): {gold}")
    usdjpy = yf.download(tickers="USDJPY=X", period="1d", interval="1m")
    print(f"usdjpy(8時間のずれのためロンドン時間): {usdjpy}")

def SampleOfCheckHighLowColoseOpen():
    import bolero_yfinance_api
    symData = bolero_yfinance_api.GetRecentPriceData("USDJPY=X", "60m")
    # print(symData)
    hlco = bolero_yfinance_api.CalcHighLowCloseOpen(symData)
    print(hlco)

def SampleOfCheck1DayHLCO():
    import yfinance as yf
    #  Open        High         Low       Close   Adj Close  Volume
    df = yf.download(tickers="USDJPY=X", period="1d", interval="1m")
    for time, line in df.iterrows():
        import bolero_yfinance_api
        hlco = bolero_yfinance_api.CalcHighLowCloseOpen(line)
        hlco = ConvertJpPips(hlco)
        print(str(time) + " pips:h-l,c-o" + str(hlco))

def SampleOfTimeAndPrice():
    # https://www.oanda.jp/lab-education/blog_column/local_time/#:~:text=OANDA%E3%81%AEMT5/MT4%E3%81%AE,%E3%81%8CGMT+2%E3%81%A8%E3%81%AA%E3%82%8A%E3%81%BE%E3%81%99%E3%80%82
    # OANDAのMT5/MT4のサーバの時間は米国夏時間がGMT+3、米国冬時間がGMT+2となります。
    import yfinance as yf
    #  Open        High         Low       Close   Adj Close  Volume
    df = yf.download(tickers="USDJPY=X", period="1d", interval="60m")
    for time, line in df.iterrows():
        import bolero_yfinance_api
        c = line["Close"]
        print(str(time) + " " + str(c))

# 直近N時間でリサンプルを行い足を求める。上限は5dayまで
def GetRecentHourCandle(symbol, hour):
    def Resample(_df, freq):
        # todo: リサンプルする場合、最初の時間を採用してしまうので、最後の時間を採用したい。
        dfNew = _df.resample(freq, origin='start').agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last'
            })
        return dfNew
    import yfinance as yf
    df = yf.download(tickers=symbol, period="5d", interval="1h")
    if (len(df) < hour):
        return None
    df2 = df.tail(hour)
    df3 = Resample(df2, str(hour) + "h")
    return df3.iloc[-1]

def SampleOfGetRecentHourCandle():
    def Show(df):
        for time, line in df.iterrows():
            c = line
            print(str(time) + " " + str(c))
        print("---")

    import yfinance as yf
    df = yf.download(tickers="USDJPY=X", period="1d", interval="1h")

    Show(df)
    print("以下にGetRecentHourCandleを使った結果")
    Show(GetRecentHourCandle("USDJPY=X", 12))

# 毎分チェックし、10pips以上動いたら知らせる。
def MainOfNotifyMove10Pips():
    def func(symbol, interval
             , priceMovementCheck = -1
             ):
        import bolero_yfinance_api
        symData = bolero_yfinance_api.GetRecentPriceData(symbol, interval)
        if symData is None:
            return ""
        hlco = bolero_yfinance_api.CalcHighLowCloseOpen(symData)
        if (hlco[0] < priceMovementCheck):
            return ""
        return symbol + " : higl-low:" + str(hlco[0]) + ", close-open:" + str(hlco[1])

    # 定期配信用
    def funcOfRegularSubscription(symbol):
        c = GetRecentHourCandle(symbol, 12)
        import bolero_yfinance_api
        hlco = bolero_yfinance_api.CalcHighLowCloseOpen(c)
        def Format(num):
            return '{:.2f}'.format(num)
        return "定期配信(12h)\n" + str(c.name) + "\n" + symbol + "\n脚長:" + Format(hlco[0]) + "\n差額:" + Format(hlco[1])

    # デバッグ用
    # print(funcOfRegularSubscription("USDJPY=X"))

    import bolero_line_notify
    bolero_line_notify.SendMessageInterval([
        ["minute", ":00", lambda: func("USDJPY=X", "1m", 0.1)]
        ,["minute", ":00", lambda: func("^N225", "1m",100)]
        ,["every_day", "09:00", lambda: funcOfRegularSubscription("^N225")]
        ,["every_day", "21:00", lambda: funcOfRegularSubscription("^N225")]
        ,["every_day", "09:00", lambda: funcOfRegularSubscription("USDJPY=X")]
        ,["every_day", "21:00", lambda: funcOfRegularSubscription("USDJPY=X")]
    ])

if __name__ == '__main__':
    # 実行パスを追加する。
    # https://rinoguchi.net/2019/11/python-module-import.html
    # ④実行時にモジュール検索パスリスト sys.path に追加
    import sys
    import os
    libDir = os.path.join(os.getcwd(), "bolero_lib")
    # print(libDir)
    sys.path.append(libDir)

    # SampleOfIntervalCall()
    # SampleOfYahooFApiTime()
    # SampleOfCheckHighLowColoseOpen()
    # SampleOfCheck1DayHLCO()
    # SampleOfTimeAndPrice()
    # SampleOfGetRecentHourCandle()
    MainOfNotifyMove10Pips()