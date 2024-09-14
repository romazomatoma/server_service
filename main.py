def GetNowTime():
    import datetime
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    return datetime.datetime.now(JST)

def SendMessageInterval(interval, FuncOfReturnStr):
    import LINENotifyBot
    bot = LINENotifyBot.LINENotifyBot(access_token=LINENotifyBot.g_line_token_a001)

    def job():
        m = FuncOfReturnStr()
        bot.send(m)
        print(m)

    job()

    import schedule
    schedule.every().minute.at(interval).do(job)

    while True:
        schedule.run_pending()
        import time
        time.sleep(1)

def SampleOfIntervalCall():
    def func():
        return GetNowTime().strftime('%m/%d %H:%M:%S')
    SendMessageInterval(":00", func)

def main():
    SampleOfIntervalCall()

main()