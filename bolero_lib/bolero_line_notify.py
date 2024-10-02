def SendMessageInterval(interval, FuncOfReturnStr):
    import LINENotifyBot
    bot = LINENotifyBot.LINENotifyBot(access_token=LINENotifyBot.g_line_token_a001)

    bot.send("START!")

    def job():
        m = FuncOfReturnStr()
        if len(m) == 0: # メッセージ文字列が空なら
            return
        bot.send(m)
        print(m)

    job()

    import schedule
    schedule.every().minute.at(interval, "Asia/Tokyo").do(job)

    while True:
        schedule.run_pending()
        import time
        time.sleep(1)