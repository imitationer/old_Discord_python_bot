# -*- coding=utf-8 -*-
import discord
from os import makedirs,remove
from shutil import rmtree
from uuid import uuid4
from voicetext import VoiceText
from re import compile,sub,DOTALL
from os.path import isdir
class ReadText:
    channels = None
    length = 0
    default_speaker = "hikari"
    path = "./voicetext"
    if isdir(path):
        rmtree(path)
    makedirs(path, exist_ok=True)

    play_list = {}
    def __init__(self,client, info={}):
        

        self.client = client
        channel = info.get("channel") 
        if channel is not None:
            self.channels = channel

        length = info.get("length")
        if length is not None:
            self.length = length
        
        speaker = info.get("speaker")
        if speaker is not None:
            self.default_speaker = speaker

        self.api = VoiceText(info["key"])

        self.speakers = ["show","haruka","hikari","takeru","santa","bear"]
        self.speace = compile(r"[.\n\t]")
        self.command = compile(r"(\<.+?\>)|@everyone|@here|\s+|\r")
        self.code = compile(r"(\`{3}(.+)?\`{3})", flags=DOTALL)
        self.url = compile(r"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+")

    async def read(self, message):

        vc_client = self.client.voice_client_in(message.server)
        _server_id = message.server.id


        if (self.client.user == message.author) or \
            (message.type != discord.MessageType.default) or\
            (message.channel.id not in self.channels) or \
            message.author.bot or message.content == "" or vc_client is None:
            return 
        string_message = sub(self.speace, " ", message.content)
        string_message = sub(self.command,"", string_message)

        if string_message.startswith("#") or string_message.startswith("tkb") or string_message.startswith("!"):
            return

        if "```" in string_message:
            string_message = sub(self.code, "、以下コード省略", string_message)

        # URLを省略
        if "http" in string_message:
            string_message = sub(self.url, "、以下URL省略", string_message)

        # 長すぎる文字は省略
        if (self.length is not None or self.length > 20) and len(string_message) >= self.length:
            string_message = string_message[:self.length] + "、以下省略"

        

        # 読み上げ者を変更
        speaker = self.default_speaker
        for x in self.speakers:
            if string_message.endswith(x):
                speaker = x
                string_message = string_message.rstrip(x)

        await self.create(string_message, speaker, vc_client, _server_id)

    async def create(self, string_message, speaker, vc_client, _server_id):
        if string_message == "":
            return
        if _server_id not in self.play_list:
            self.play_list[_server_id] = []

        # 音声wavファイル作成
        file_name = f"{self.path}/{uuid4()}.wav"
        with open(file_name, "wb") as f:
            f.write(self.api.speaker(speaker).to_wave(string_message))


        player = vc_client.create_ffmpeg_player(file_name, after=lambda: self.player(_server_id))
        self.play_list[_server_id].append({"client": player, "name": file_name})

        if len(self.play_list[_server_id]) == 1:  # 再生中のものがない場合
            self.play_list[_server_id][0]["client"].start()

    def player(self, server_id):
        play_list = self.play_list[server_id]
        if play_list[0]["client"].is_done():       # 再生が終わったら
            play_list[0]["client"].stop()          # 一応再生停止
            remove(play_list[0]["name"])           # 音声ファイル削除
            del play_list[0]                       # リストの0個目を削除
            if len(play_list) > 0:                 # 次再生すべき物があるか
                play_list[0]["client"].start()     # 次のを再生
