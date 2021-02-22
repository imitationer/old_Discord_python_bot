# -*- coding=utf-8 -*-
from discord.ext import commands

class Group:
    @commands.group(pass_context=True, no_pm= True)
    async def tts(self,ctx):
        if ctx.message.author.voice_channel is None:
            await self.say("ボイスチャンネルに接続してからコマンド入力をして下さい")

        if ctx.invoked_subcommand is None:
            await self.say("サブコマンドが存在しません")

    @tts.command(name="join", pass_context=True,
        brief=": ボイスチャンネルに接続",
        description="ボイスチャンネル操作系コマンド:", 
        help="短縮コマンド !join\nメッセージ送信者がボイスチャンネルに接続している時\nメッセージ送信者がいるボイスチャンネルに接続する")
    async def __join(self,ctx):
        await self.join(ctx)

    @tts.command(name="disconnect", pass_context=True,
        brief= "ボイスチャンネルから切断",
        description= "ボイスチャンネル操作系コマンド:",
        aliases= ["dc",], 
        help= "メッセージ送信者がボイスチャンネルに接続している時\nメッセージ送信者がいるボイスチャンネルに切断する")
    async def __disconnect(self,ctx):
        await self.disconnect(ctx)

    @tts.command(name="reconnect", pass_context=True,
        brief= "ボイスチャンネルに再接続",
        description= "ボイスチャンネル操作系コマンド:",
        aliases= ["rc",], 
        help= "メッセージ送信者がボイスチャンネルに接続している時\nメッセージ送信者がいるボイスチャンネルに再接続する")
    async def __reconnect(self,ctx):
        await self.reconnect(ctx)

    @tts.command(name="move", pass_context=True,
        brief= "ボイスチャンネルを移動",
        description= "ボイスチャンネル操作系コマンド:",
        aliases= ["移動","mv"], 
        help= "メッセージ送信者がボイスチャンネルに接続している時\nメッセージ送信者がいるボイスチャンネルに移動する")
    async def __move(self,ctx):
        await self.join(ctx)