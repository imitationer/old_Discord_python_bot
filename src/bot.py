# -*- coding=utf-8 -*-

from discord.ext import commands

import inspect
from .commands import Commands
from .sub_func import Sub
from .plugin import ReadText
from .plugin import State
from .plugin import Role


class DicordBot(commands.Bot, Sub, Commands):
    def __init__(self, config):
        super().__init__(command_prefix=config.prefix)
        
        self.owner_id = config.owner 
        self.formatter = HelpSub()
        self.voice_text = ReadText(self, config.voice_info)
        self.voice_state = State(self, config.voice_info)
        self.role = Role(self)
        
        members = inspect.getmembers(self)
        a = [self.add_command(member) for name, member in members if isinstance(member, commands.Command) and member.parent is None]
        del a
        print(self.commands.keys())

    async def on_message(self, message):
        await self.voice_text.read(message)
        await self.process_commands(message)


class HelpSub(commands.formatter.HelpFormatter):

    def get_ending_note(self):
        command_name = self.context.invoked_with
        return "コマンドの詳細については {0}{1} <コマンド名> を入力して下さい\n" \
               "カテゴリーの詳細については {0}{1} <カテゴリー名> を入力して下さい".format(self.clean_prefix, command_name)

    