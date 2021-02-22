# -*- coding=utf-8 -*-
from discord.ext import commands
import discord

class RoleCheck:
    def _admin(self, message):
        if message.author.id in self.owner_id:
            return True

    def _user(self, message):
        if message.author.avatar is not None:
            return True

class Role(RoleCheck):

    @commands.group(pass_context=True, no_pm= True)
    async def role(self,ctx):
        if ctx.invoked_subcommand is None:
            await self.say("サブコマンドが存在しません")
            return

    @role.command(name="add", pass_context=True, no_pm=True, 
        brief= "権限付与申請",
        description= "権限付与申請コマンド",
        aliases=["申請",],
         help="申請チャンネルで権限付与申請が来た場合権限の確認をする")
    async def _add(self,ctx, *roles):
        await self.add(ctx, roles)
    @commands.command(name="add",aliases=["申請",], pass_context=True, hidden=True, no_pm=True)
    async def __add(self,ctx, *roles):
        await self.add(ctx, roles)

    async def add(self,ctx, roles):
        channel = self.role.channels[ctx.message.server]
        channel = await self.role.get_role_channel(ctx.message)
        if ctx.message.channel != channel:
            return

        for role_name in roles:
            res = await self.role.message_author(ctx.message, role_name)
            if res is None:
                continue
            if res is False:
                break
          
        await self.delete_message(ctx.message)






