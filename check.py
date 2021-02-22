# -*- coding=utf-8 -*-

import discord
import subprocess

class Check(discord.Client):
    cmd = "python3.6 main.py"
    async def on_ready(self):
        cmd = "python3.6 main.py"
        self.p = subprocess.Popen(cmd.split())

    async def on_message(self, message):
        mes = message.content.split()
        if len(mes) > 1 and mes[0] == "くりっち":
            if mes[1] == "再起動":
                await self.delete_message(message)
                mes = "くりっちの再起動を開始します"
                flag = await self.send_message(message.channel,mes)
                self.p.kill()
                self.p = subprocess.Popen(self.cmd.split())
                mes = "くりっちの再起動終了しました"
                await self.edit_message(flag,mes)
        

if __name__ == '__main__':
    import asyncio
    import time
    bot = Check()
    loop = asyncio.get_event_loop()
    while True:
        try:
            loop.run_until_complete(bot.start("token"))
        except Exception as e:
            print("Error", e)  # or use proper logging
        print("Waiting until restart")
        time.sleep(60)


    