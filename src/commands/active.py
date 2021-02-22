# -*- coding=utf-8 -*-

from discord.ext import commands
from functools import wraps


class ActiveOnly:
    def is_active():
        def actual_decorator(func):
            @wraps(func)
            async def wrapper(self, ctx, amount):
                roles = [role.name for role in ctx.message.author.roles]
                
                if "activeonly" not in roles and ctx.message.author.id not in self.owner_id:
                    await self.say("このコマンドは登録された人しか使用出来ません")
                    return
                try:
                    amount = int(amount)
                except:
                    await self.say("メッセージを消す数値を指定して下さい")
                    return
                else:
                    await func(self, ctx, amount)
                
            return wrapper
        return actual_decorator
    
    @commands.command(name="del", pass_context=True, brief="アクティブオンリー専用メッセージ削除コマンド", hidden=True, no_pm=True)
    @is_active()
    async def active_del(self,ctx, amount):
        await self.delete_message(ctx.message)
        try:
            amount = int(amount)
        except:
            return
        await self.purge_from(ctx.message.channel,limit=amount,check=lambda m: m.author == self.user)
        await self.say("メッセージを削除しました")