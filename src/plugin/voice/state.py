# -*- coding=utf-8 -*-

from time import time

class State:
    def __init__(self,client,info={}):
        self.client = client
        self.access = {}
        self.info = info

    async def update(self, before, after):
        """ボイスチャンネルステータス変更時"""
        if before.bot or after.bot:
            return
        message = None
        if after.voice_channel is not None:
            server = after.voice_channel.server
        if before.voice_channel is not None:
            server = before.voice_channel.server

        if after.id not in self.access:
            self.access[after.id] = 0
        vc_client = self.client.voice_client_in(server)
        if vc_client is None or before.voice_channel == after.voice_channel or self.access[after.id] + 5 > time():
            return
        
        if before.voice_channel is not None:
            if vc_client.channel == before.voice_channel:
                message = f"さようなら {after.display_name}さん"
                self.access[after.id] = time()
        if after.voice_channel is not None:
            if self.access[after.id] + 5 < time() < self.access[after.id] + 60:
                message = f"おかえり {before.display_name}さん"
            elif vc_client.channel == after.voice_channel:
                message = f"こんにちは {before.display_name}さん"
                self.access[after.id] = time()


        if message is not None:
            message_channel = server.get_channel(self.info["channel"])
            await self.client.voice_text.create(message, "hikari", vc_client, server.id)
            if "おかえり" not in message:
                await self.client.send_message(message_channel,message)
            



