# -*- coding=utf-8 -*-

from .tts import TTS
from .owner import OwnerOnly
from .active import ActiveOnly
from .role import Role

"""
@commands.command(
        name= ,         # メインコマンド: str
        help= ,         # 詳細help: str
        brief= ,        # 簡易help: str
        aliases= ,      # 別名: list
        pass_context= , # ctxを最初の引数で返すか: boolean
        enabled= ,      # コマンドの有効無効 : boolean
        description= ,  # help コマンドの前に付ける: str
        hidden= ,       # helpから見えなくするか
        no_pm=          # DMからを受け付けるか Trueは無視)
"""


class Commands(TTS,OwnerOnly,ActiveOnly,Role):
        pass