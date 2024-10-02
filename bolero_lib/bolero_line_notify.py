def SendMessageInterval(interval, FuncOfReturnStr):
    import LINENotifyBot
    bot = LINENotifyBot.LINENotifyBot(access_token=LINENotifyBot.g_line_token_a001)

    def job():
        m = FuncOfReturnStr()
        bot.send(m)
        print(m)

    job()

    import schedule
    schedule.every().minute.at(interval, "Asia/Tokyo").do(job)

    while True:
        schedule.run_pending()
        import time
        time.sleep(1)