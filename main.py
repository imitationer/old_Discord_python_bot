# -*- coding=utf-8 -*-

from src.bot import DicordBot
import config


if __name__ == '__main__':
    import asyncio
    import time
    bot = DicordBot(config)
    loop = asyncio.get_event_loop()
    while True:
        try:
            loop.run_until_complete(bot.start(config.token))
        except Exception as e:
            print("Error", e)  # or use proper logging
        print("Waiting until restart")
        time.sleep(60)