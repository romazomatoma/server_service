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

def SampleOfTimeAndPriceResample():
    def Resample(_df, freq):
        import pandas as pd
        dfNew = pd.DataFrame()
        dfNew["Open"] = _df["Open"].resample(freq).first()
        dfNew["Close"] = _df["Close"].resample(freq).last()
        dfNew["High"] = _df["High"].resample(freq).max()
        dfNew["Low"] = _df["Low"].resample(freq).min()
        return dfNew
    import yfinance as yf
    #  Open        High         Low       Close
    df = yf.download(tickers="USDJPY=X", period="1d", interval="1h")

    df = Resample(df, "6h")

    for time, line in df.iterrows():
        import bolero_yfinance_api
        c = line["Close"]
        print(str(time) + " " + str(c))

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

    import bolero_line_notify
    bolero_line_notify.SendMessageInterval([
        ["minute", ":00", lambda: func("USDJPY=X", "1m", 0.1)]
        ,["minute", ":00", lambda: func("^N225", "1m"
                                        , 100
                                        )]
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
    # SampleOfTimeAndPriceResample()
    MainOfNotifyMove10Pips()