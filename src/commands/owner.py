# -*- coding=utf-8 -*-

from discord.ext import commands
from functools import wraps
import discord

class OwnerOnly:
    def is_owner():
        def actual_decorator(func):
            @wraps(func)
            async def wrapper(self, ctx):
                if ctx.message.author.id not in self.owner_id:
                    await self.say("このコマンドはオーナー登録された人しか使用出来ません")
                    return
                await func(self, ctx)
            return wrapper
        return actual_decorator

    @commands.group(pass_context=True, brief="オーナー専用コマンド", hidden=True)
    @is_owner()
    async def owner(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.say("サブコマンドが存在しません")

    @owner.command(brief="Ping送信チェック用コマンド", pass_context=True, hidden=True)
    async def ping(self, ctx):
        await self.delete_message(ctx.message)
        await self.say("pong")

    @owner.command(name="eval",pass_context=True)
    async def _eval(self, ctx, code: str):
        await self.delete_message(ctx.message)
        res = eval(code)


    @owner.command(name="exec",pass_context=True)
    async def _exec(self, ctx, code: str):
        await self.delete_message(ctx.message)
        exec(code)
        
    @owner.command(name="del", pass_context=True)
    async def owner_del(self,ctx, amount: int):
        await self.delete_message(ctx.message)
        await self.purge_from(ctx.message.channel,limit=amount)
        await self.say("メッセージを削除しました")

    @owner.command(pass_context=True, no_pm=True)
    async def union(self, ctx, new_channel_name: str, *ids):
        _server = ctx.message.server
        new_channel = discord.utils.get(_server.channels, name=new_channel_name, type=discord.ChannelType.text)
        if new_channel is None:
            new_channel = await self.create_channel(_server, new_channel_name, type=discord.ChannelType.text)

        log_id = [await self.get_message(ctx.message.channel, i) for i in ids]
        for message in log_id:
            print(message)
            await self.send_message(new_channel, f"{message.channel.name}:{message.author.display_name}\n{message.timestamp.strftime('%Y/%m/%d %H:%M')}\n{message.content}")
                
        while True:
            log = [msg async for msg in self.logs_from(ctx.message.channel)]
            if len(log) > 1: # 1発言以下でdelete_messagesするとエラーになる
                await self.delete_messages(log)
            else:
                break
        await self.send_message(ctx.message.channel, "ログの移行完了")

    @owner.command(pass_context=True, no_pm=True)
    async def role(self, ctx, role_name: str):
        channel = await self.role.get_role_channel(ctx.message)
        for member in ctx.message.server.members:
            res = await self.role.member(ctx.message. member, role_name, channel)
            if res is None:
                continue
            if res is False:
                break
        await self.delete_message(ctx.message)