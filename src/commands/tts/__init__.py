# -*- coding=utf-8 -*-

from discord.ext import commands
from functools import wraps
from .group import Group

class Single:
    @commands.command("join",aliases=["くりくり","接続"], pass_context=True, hidden=True, no_pm=True)
    async def _join(self,ctx):
        await self.join(ctx)
    @commands.command("disconnect",aliases=["dc","切断"], pass_context=True, hidden=True, no_pm=True)
    async def _disconnect(self,ctx):
        await self.disconnect(ctx)
    @commands.command("reconnect",aliases=["rc","再接続"], pass_context=True, hidden=True, no_pm=True)
    async def _reconnect(self,ctx):
        await self.reconnect(ctx)
    @commands.command("move",aliases=["移動","mv"], pass_context=True, hidden=True, no_pm=True)
    async def _move(self,ctx):
        await self.join(ctx)



class TTS(Single,Group):
    def vc_client():
        def actual_decorator(func):
            @wraps(func)
            async def wrapper(self, ctx):
                server = ctx.message.server
                voice_channel = ctx.message.author.voice_channel
                if self.is_voice_connected(server):
                    vc_client = self.voice_client_in(server)
                else:
                    vc_client = None
                await func(self, ctx, server , voice_channel, vc_client)
                await self.delete_message(ctx.message)
            return wrapper
        return actual_decorator

    @vc_client()
    async def join(self,ctx, server, voice_channel, client):
        # VC接続していない
        if client is None:
            await self.join_voice_channel(voice_channel)
            message = f":white_check_mark: VC Channel '{voice_channel.name}'に接続しました"

        # 同じチャンネルに接続している
        elif client.channel == voice_channel:
            message = f":no_entry_sign: VC Channel '{voice_channel.name}'に既に接続しています"

        # 違うチャンネルに接続している
        else:
            await client.move_to(voice_channel)
            message = f":white_check_mark: VC Channel {voice_channel.name}に移動しました"

        await self.say(message)

    @vc_client()
    async def disconnect(self,ctx, server, voice_channel, client):
        # VC接続していない
        if client is None:
            message = ":no_entry_sign: VCに接続していない為切断出来ません"

        # 同じチャンネルに接続している
        elif client.channel == voice_channel:
            await client.disconnect()
            message = f":white_check_mark: VC Channel {voice_channel.name}から切断しました"

        # 違うチャンネルに接続している
        else:
            message = f":no_entry_sign: {ctx.message.author.display_name}と同じチャンネルに接続していない為切断出来ません"

        await self.say(message)

    @vc_client()
    async def reconnect(self,ctx, server, voice_channel, client):
        # VC接続していない
        if client is None:
            await self.join_voice_channel(voice_channel)
            message = f":white_check_mark: VC Channel {voice_channel.name}に接続しました"
            
        # 同じチャンネルに接続している
        elif client.channel == voice_channel:
            await client.disconnect()
            await self.join_voice_channel(voice_channel)
            message = f":white_check_mark: VC Channel {voice_channel.name}に再接続しました"
        # 違うチャンネルに接続している
        else:
            message = f":no_entry_sign: {ctx.message.author.display_name}と同じチャンネルに接続していない為再接続出来ません"
            
        await self.say(message)

  




