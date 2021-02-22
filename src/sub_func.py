# -*- coding=utf-8 -*-

from discord.ext import commands
import time

class Sub:
    
    async def on_ready(self):
        """接続準備完了時"""
        print(f"BOT-NAME :{self.user.name}")
        print("ログインしました")

    async def on_command_error(self,error, ctx):
        """コマンドエラー発生時"""
        #print(error)
        print(ctx.message.content)
        print("error")

    async def on_voice_state_update(self, before, after):
        await self.voice_state.update(before, after)

    async def on_member_join(self, member):
        """サーバーメンバー入室時"""
        return

    # 以下現在未使用
    async def on_message_delete(self, message):
        """メッセージ削除時"""
        return

    async def on_message_edit(self, before, after):
        """メッセージ編集時"""
        return

    async def on_reaction_add(self, reaction, user):
        """リアクション追加"""
        return

    async def on_reaction_remove(self, reaction, user):
        """リアクション削除"""
        return

    async def on_reaction_clear(self, message, reaction):
        """リアクション全削除"""
        return