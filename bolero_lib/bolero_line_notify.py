def SendMessageInterval(scheduleList): # [[scheduleType, scheduleInterval, func]]の構造。
    import LINENotifyBot
    bot = LINENotifyBot.LINENotifyBot(access_token=LINENotifyBot.g_line_token_a001)

    # bot.send("START!")

    def job(func):
        m = func() # 送る文字列を返す関数。
        if len(m) == 0: # メッセージ文字列が空なら
            return
        bot.send(m)
        print(m)

    for s in scheduleList:
        scheduleType = s[0]
        scheduleInterval = s[1]
        func = s[2]

        import schedule

        if scheduleType == "minute":
            schedule.every().minute.at(scheduleInterval, "Asia/Tokyo").do(lambda func=func: job(func))
        elif scheduleType == "every_day":
            schedule.every().day.at(scheduleInterval, "Asia/Tokyo").do(lambda func=func: job(func))

    while True:
        schedule.run_pending()
        import time
        time.sleep(1)

def SimpleSendMessage(mes):
    import LINENotifyBot
    bot = LINENotifyBot.LINENotifyBot(access_token=LINENotifyBot.g_line_token_a001)
    bot.send(mes)